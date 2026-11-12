#!/usr/bin/env python3
"""Rebuild EXP-010 summaries from raw matched observations, preserving sessions."""
import argparse
import csv
import io
import itertools
import json
import statistics
from pathlib import Path

import analyse_final_comparison as closing_analysis
import collect_run_metadata as metadata
import random_seed_common as common
import run_incremental_comparison as assembly
import run_timing as timing
import run_validation as validation

derive = closing_analysis.derive
write_csv = closing_analysis.write_csv


def csv_bytes(rows):
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=list(rows[0]), lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue().encode("utf-8")


def read_run(run):
    m = json.loads((run / "manifest.json").read_text())
    if (m.get("development_only") or m.get("experiment_id") != "EXP-010"
            or m.get("record_type") != common.BUDGET["record_type"]
            or m.get("status") != "completed" or m.get("provenance_recheck") != "pass"
            or m.get("benchmark_executed") is not True
            or m.get("checks") != {key: "pass" for key in common.CHECKS}):
        raise ValueError("Not a completed formal EXP-010 session")
    p = common.validate_protocol(m["protocol"])
    if p != common.load_protocol():
        raise ValueError("Run differs from the frozen EXP-010 protocol")
    if m["seed_plan_sha256"] != p["seed_plan_sha256"]:
        raise ValueError("Manifest seed-plan identity differs")
    plan = common.load_plan(p, common.record_file(run, "seed-plan.json"))
    schedule = list(common.schedule(plan, m["session"]))
    leakage, sources, expected_assembly = common.accepted_context()
    if m["source_file_sha256"] != sources or m["compiler"] != leakage["compiler"]:
        raise ValueError("Unreviewed source/compiler identity")
    if m["tool_sha256"] != leakage["tool_sha256"] or m["build_flags"] != list(validation.FLAGS):
        raise ValueError("Unreviewed build/tool identity")
    if m["affinity"]["observed"] != [p["cpu"]] or m["affinity"]["selected_logical_cpu"] != p["cpu"]:
        raise ValueError("Unexpected CPU affinity")
    if set(m["support_file_sha256"]) != set(common.SUPPORT):
        raise ValueError("Incomplete support provenance")
    if metadata.sha256(run / "metadata.json") != m["metadata_sha256"]:
        raise ValueError("Metadata changed")
    snapshot = json.loads((run / "metadata.json").read_text())
    if (snapshot.get("development_only") or snapshot["experiment_id"] != "EXP-010"
            or snapshot["run_id"] != m["run_id"] or snapshot["variant"] != "random-seed-three-way"
            or snapshot["provenance"]["source_commit"] != m["source_commit"]
            or snapshot["provenance"]["source_tree_clean"] is not True
            or snapshot["environment"]["available_compiler"] != m["compiler"]):
        raise ValueError("Metadata/manifest provenance mismatch")
    tags = {f"{v}-{k}" for v, k in itertools.product(common.VARIANTS, common.PARAMETERS)}
    if set(m["executables"]) != tags or set(m["assembly"]) != set(expected_assembly):
        raise ValueError("Incomplete build/assembly coverage")
    if len(m["steps"]) != 225 or len(m["datasets"]) != 108:
        raise ValueError("Incomplete execution coverage")
    steps = {}
    streams = set()
    for step in m["steps"]:
        if step["label"] in steps or step["status"] != "completed" or step["exit_code"] != 0:
            raise ValueError("Duplicate or failed step")
        steps[step["label"]] = step
        for stream in ("stdout", "stderr"):
            if step[stream] in streams:
                raise ValueError("Reused raw output path")
            streams.add(step[stream])
            if metadata.sha256(common.record_file(run, step[stream])) != step[stream + "_sha256"]:
                raise ValueError("Raw output changed")
    expected_labels = {"build-" + tag for tag in tags}
    for key, expected in expected_assembly.items():
        tag, symbol = key.split("/")
        suffix = symbol.removeprefix(f"pqcrystals_kyber{tag.rsplit('-', 1)[1]}_ref_")
        label = "assembly-" + tag + "-" + suffix
        expected_labels.add(label)
        record = m["assembly"][key]
        step = steps[label]
        if record["path"] != step["stdout"]:
            raise ValueError("Assembly path mismatch")
        actual = assembly.assembly_record(common.record_file(run, record["path"]).read_text(), symbol)
        if actual != expected or record["normalised"] != expected:
            raise ValueError("Assembly differs from accepted normal code")
    for tag in tags:
        if common.record_file(run, steps["build-" + tag]["stderr"]).read_text().strip():
            raise ValueError("Build produced diagnostics")
    summaries = []
    timing_labels = []
    for dataset, (block, parameter, position, variant, seed) in zip(m["datasets"], schedule):
        wanted = dict(block=block, parameter=parameter, position=position, variant=variant,
                      fixture_seed=seed, rows=3000)
        if any(dataset.get(key) != value for key, value in wanted.items()):
            raise ValueError("Wrong seed, order, row count or dataset matrix")
        tag = f"{variant}-{parameter}"
        label = f"timing-{tag}-block-{block:04d}"
        expected_labels.add(label)
        timing_labels.append(label)
        step = steps[label]
        path = common.record_file(run, dataset["path"])
        if dataset["path"] != step["stdout"] or metadata.sha256(path) != dataset["sha256"]:
            raise ValueError("Dataset/raw output mismatch")
        if (len(step["argv"]) != 4 or step["argv"][-3:] != ["1000", "100", seed]
                or Path(step["argv"][0]).name != "bench-" + tag):
            raise ValueError("Wrong benchmark invocation")
        diagnostics = dict(line.split("=", 1) for line in common.record_file(run, step["stderr"]).read_text().splitlines())
        wanted_diag = dict(timer=p["timer"], unit="ns", iterations="1000", warmup="100",
                           seed=seed, input_mode="derand-shake256-v1")
        if any(diagnostics.get(key) != value for key, value in wanted_diag.items()):
            raise ValueError("Harness diagnostics mismatch")
        for key in ("clock_resolution_ns", "empty_timer_pair_min_ns"):
            if int(diagnostics[key]) < 0:
                raise ValueError("Invalid timer diagnostics")
        for row in timing.summarise_csv(path, parameter, 1000, block):
            row["block"] = row.pop("repetition")
            summaries.append(dict(variant=variant, position=position, fixture_seed=seed, **row))
    if set(steps) != expected_labels or [s["label"] for s in m["steps"] if s["label"].startswith("timing-")] != timing_labels:
        raise ValueError("Unexpected step matrix or execution sequence")
    pairs, estimates = derive(summaries, 12, m["session"])
    for name, rows in (("process-summary", summaries), ("paired-comparison", pairs), ("comparison", estimates)):
        entry = m["derived"][name]
        path = common.record_file(run, entry["path"])
        if entry["rows"] != len(rows) or metadata.sha256(path) != entry["sha256"] or path.read_bytes() != csv_bytes(rows):
            raise ValueError("Derived table does not reproduce")
    return m, pairs, estimates


def combine(runs):
    loaded = [read_run(Path(run)) for run in runs]
    if sorted(m["session"] for m, _, _ in loaded) != [1, 2, 3, 4, 5]:
        raise ValueError("Exactly five distinct successful sessions are required")
    first = loaded[0][0]
    for m, _, _ in loaded:
        for key in ("protocol", "source_file_sha256", "support_file_sha256", "compiler", "build_flags", "tool_sha256"):
            if m[key] != first[key]:
                raise ValueError("Session identities differ: " + key)
    pairs = sorted([r for _, rs, _ in loaded for r in rs],
                   key=lambda r: (r["session"], r["reference"], r["candidate"], r["parameter_set"], r["operation"], r["block"]))
    estimates = sorted([r for _, _, rs in loaded for r in rs],
                       key=lambda r: (r["session"], r["reference"], r["candidate"], r["parameter_set"], r["operation"]))
    totals, boxes = [], []
    for reference, candidate in common.COMPARISONS:
        for k, operation in itertools.product(common.PARAMETERS, timing.OPERATIONS):
            group = dict(reference=reference, candidate=candidate, parameter_set=f"Kyber{k}", operation=operation)
            matches = lambda r: all(r[key] == value for key, value in group.items())
            values = [r["median_paired_improvement_pct"] for r in estimates if matches(r)]
            effects = [r["improvement_pct"] for r in pairs if matches(r)]
            if len(values) != 5 or len(effects) != 60:
                raise ValueError("Incomplete summary group")
            totals.append(dict(**group, sessions=5, median_session_improvement_pct=statistics.median(values),
                min_session_improvement_pct=min(values), max_session_improvement_pct=max(values),
                positive_sessions=sum(v > 0 for v in values), negative_sessions=sum(v < 0 for v in values)))
            q1, _, q3 = statistics.quantiles(effects, n=4, method="inclusive")
            boxes.append(dict(**group, blocks=60, q1_pct=q1, pooled_block_median_pct=statistics.median(effects),
                q3_pct=q3, min_pct=min(effects), max_pct=max(effects),
                positive_blocks=sum(v > 0 for v in effects), negative_blocks=sum(v < 0 for v in effects)))
    return loaded, pairs, estimates, totals, boxes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runs", nargs=5, type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    loaded, pairs, estimates, totals, boxes = combine(args.runs)
    args.output.mkdir(parents=True, exist_ok=False)
    for name, rows in (("paired-effects", pairs), ("session-effects", estimates),
                       ("five-session-effects", totals), ("box-statistics", boxes)):
        write_csv(args.output / (name + ".csv"), rows)
    report = dict(record_type="random-seed-five-session-analysis", experiment="EXP-010",
        sessions=5, unique_block_seeds=60, duration_rows=1620000,
        seed_plan_sha256=loaded[0][0]["protocol"]["seed_plan_sha256"],
        inputs={str(run / "manifest.json"): metadata.sha256(run / "manifest.json") for run in args.runs},
        analysis_sha256={name: metadata.sha256(common.ROOT / name) for name in
                        ("scripts/analyse_random_seed_comparison.py", "scripts/random_seed_common.py", "scripts/analyse_final_comparison.py")},
        source_commits=[m["source_commit"] for m, _, _ in loaded],
        interpretation="Median of five session medians. Pooled box statistics describe observed block spread only; no confidence interval, input-only variance or portability claim.",
        outputs={p.name: metadata.sha256(p) for p in args.output.iterdir() if p.is_file()})
    (args.output / "provenance.json").write_text(json.dumps(report, indent=2) + "\n")
    print("Verified five sessions, 60 seeds and all raw observations; wrote descriptive summaries.")


if __name__ == "__main__":
    main()
