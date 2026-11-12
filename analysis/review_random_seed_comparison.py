#!/usr/bin/env python3
"""Audit retained EXP-010 data without collecting timings or running Git."""
import argparse
import csv
from fractions import Fraction
import hashlib
import itertools
import json
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import analyse_random_seed_comparison as analysis
import analyse_final_comparison as closing
import random_seed_common as common
import run_comparison as paired
import run_validation as validation


def sha(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def median(values):
    values = sorted(values)
    n = len(values)
    assert n
    return (values[(n - 1) // 2] + values[n // 2]) / 2


def quartile(values, numerator):
    values = sorted(values)
    position = Fraction((len(values) - 1) * numerator, 4)
    lower = position.numerator // position.denominator
    weight = position - lower
    return values[lower] * (1 - weight) + values[min(lower + 1, len(values) - 1)] * weight


def equal(actual, expected):
    assert math.isclose(float(actual), float(expected), rel_tol=1e-12, abs_tol=1e-10), (actual, expected)


def rows(path):
    with path.open(newline="") as stream:
        return list(csv.DictReader(stream))


def source_map(directory):
    assert not any(p.is_symlink() for p in directory.rglob("*"))
    return {p.relative_to(directory).as_posix(): sha(p) for p in directory.rglob("*")
            if p.is_file() and (p.suffix in (".c", ".h") or p.name == "Makefile")}


def audit_session(run, manifest, expected_pairs, expected_estimates):
    """Recalculate arithmetic directly from integers, independently of derive()."""
    for name, expected in manifest["support_file_sha256"].items():
        assert sha(ROOT / name) == expected, name
    assert manifest["upstream_commit"] == "3edd5af5991927164edd4aacebfcbee00b8064e7"
    meta = json.loads((run / "metadata.json").read_text())
    assert meta["provenance"]["upstream_tree_clean"] is True
    assert meta["provenance"]["upstream_commit"] == manifest["upstream_commit"]
    assert meta["environment"]["collector_affinity"] == [0]
    assert manifest["run_id"] == run.name
    dirs = {"baseline": ROOT / "implementation/kyber-baseline-ref",
            "exp003": run / "build/exp003-source", "exp005": run / "build/exp005-source"}
    for variant, directory in dirs.items():
        assert source_map(directory) == manifest["source_file_sha256"][variant]
    assert manifest["process_environment"] == {
        "LC_ALL": "C", "PATH": "/usr/bin:/bin", "TMPDIR": str(run / "build")}
    steps = {step["label"]: step for step in manifest["steps"]}
    for tag, item in manifest["executables"].items():
        executable = common.record_file(run, item["path"])
        assert sha(executable) == item["sha256"], tag
        variant, parameter = tag.rsplit("-", 1)
        k = {512: 2, 768: 3, 1024: 4}[int(parameter)]
        expected = paired.build_command(manifest["compiler"]["path"], dirs[variant], k, executable)
        assert steps["build-" + tag]["argv"] == expected
    for step in manifest["steps"]:
        assert step["timeout_seconds"] == 120
        if step["label"].startswith("build-"):
            tag = step["label"].removeprefix("build-")
        elif step["label"].startswith("assembly-"):
            variant, parameter, function = step["label"].removeprefix("assembly-").split("-", 2)
            tag = variant + "-" + parameter
            symbol = f"pqcrystals_kyber{parameter}_ref_{function}"
            assert step["argv"] == ["/usr/bin/objdump", "-d", "--insn-width=16",
                "--disassemble=" + symbol, str(run / manifest["executables"][tag]["path"])]
        else:
            variant, parameter, _, _ = step["label"].removeprefix("timing-").split("-")
            tag = variant + "-" + parameter
            assert step["argv"][0] == str(run / manifest["executables"][tag]["path"])
        assert step["cwd"] == str(dirs[tag.rsplit("-", 1)[0]])
    process = {}
    diagnostics = []
    total_rows = 0
    for dataset in manifest["datasets"]:
        parameter = f"Kyber{dataset['parameter']}"
        values = {op: [] for op in ("keygen", "encap", "decap")}
        with (run / dataset["path"]).open(newline="") as stream:
            reader = csv.DictReader(stream)
            assert reader.fieldnames == ["parameter_set", "operation", "iteration", "elapsed_ns", "roundtrip_ok"]
            for index, row in enumerate(reader):
                operation = ("keygen", "encap", "decap")[index % 3]
                assert row["parameter_set"] == parameter and row["operation"] == operation
                assert int(row["iteration"]) == index // 3 and row["roundtrip_ok"] == "1"
                duration = int(row["elapsed_ns"])
                assert duration >= 0
                values[operation].append(Fraction(duration))
                total_rows += 1
        for op, observations in values.items():
            assert len(observations) == 1000
            key = (parameter, op, dataset["block"], dataset["variant"])
            assert key not in process
            process[key] = dict(median=median(observations), minimum=min(observations),
                                maximum=max(observations), seed=dataset["fixture_seed"],
                                position=dataset["position"])
        tag = f"{dataset['variant']}-{dataset['parameter']}"
        step = steps[f"timing-{tag}-block-{dataset['block']:04d}"]
        diagnostics.append(dict(line.split("=", 1) for line in (run / step["stderr"]).read_text().splitlines()))
    for row in rows(run / "derived/process-summary.csv"):
        item = process[(row["parameter_set"], row["operation"], int(row["block"]), row["variant"])]
        assert int(row["samples"]) == 1000 and row["fixture_seed"] == item["seed"]
        assert int(row["position"]) == item["position"]
        for name, key in (("median_ns", "median"), ("min_ns", "minimum"), ("max_ns", "maximum")):
            equal(row[name], item[key])
    effects = {}
    for row in expected_pairs:
        ref, cand = (process[(row["parameter_set"], row["operation"], row["block"], v)]
                     for v in (row["reference"], row["candidate"]))
        effect = 100 * (ref["median"] - cand["median"]) / ref["median"]
        equal(row["improvement_pct"], effect)
        equal(row["speedup"], ref["median"] / cand["median"])
        key = tuple(row[name] for name in ("reference", "candidate", "parameter_set", "operation"))
        effects.setdefault(key, []).append(effect)
    session_estimates = {}
    for row in expected_estimates:
        key = tuple(row[name] for name in ("reference", "candidate", "parameter_set", "operation"))
        vals = effects[key]
        assert len(vals) == 12
        session_estimates[key] = median(vals)
        equal(row["median_paired_improvement_pct"], median(vals))
        equal(row["min_paired_improvement_pct"], min(vals))
        equal(row["max_paired_improvement_pct"], max(vals))
        assert row["positive_blocks"] == sum(v > 0 for v in vals)
        assert row["negative_blocks"] == sum(v < 0 for v in vals)
    report = dict(run_id=run.name, session=manifest["session"], manifest_sha256=sha(run / "manifest.json"),
        status="accepted", steps=225, raw_files=450, builds=9, binaries_hash_verified=9,
        assembly_bodies=108, measurement_processes=108, measured_exchanges=108000,
        checked_warmup_exchanges=10800, duration_rows=total_rows,
        independent_process_summaries=len(process), independent_paired_effects=len(expected_pairs),
        independent_session_estimates=len(session_estimates), support_files_matching=len(manifest["support_file_sha256"]),
        source_commit=manifest["source_commit"], environment=meta["environment"],
        manual_conditions=meta["manual_conditions"], session_note=manifest["session_note"],
        clock_resolution_ns=sorted({int(d["clock_resolution_ns"]) for d in diagnostics}),
        empty_timer_pair_min_ns_range=[min(int(d["empty_timer_pair_min_ns"]) for d in diagnostics),
                                      max(int(d["empty_timer_pair_min_ns"]) for d in diagnostics)])
    return report, effects, session_estimates


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    assert not args.output.exists(), "Use a new output path"
    runs = [ROOT / f"results/EXP-010/RUN-{i:04d}" for i in range(1, 6)]
    loaded, pairs, estimates, totals, boxes = analysis.combine(runs)
    reviews, all_effects, all_sessions = [], {}, {}
    for run, (manifest, run_pairs, run_estimates) in zip(runs, loaded):
        report, effects, sessions = audit_session(run, manifest, run_pairs, run_estimates)
        reviews.append(report)
        for key in effects:
            all_effects.setdefault(key, []).extend(effects[key])
            all_sessions.setdefault(key, []).append(sessions[key])
    for row, box in zip(totals, boxes):
        key = tuple(row[name] for name in ("reference", "candidate", "parameter_set", "operation"))
        sessions, effects = all_sessions[key], all_effects[key]
        assert len(sessions) == 5 and len(effects) == 60
        for field, value in (("median_session_improvement_pct", median(sessions)),
                             ("min_session_improvement_pct", min(sessions)),
                             ("max_session_improvement_pct", max(sessions))):
            equal(row[field], value)
        assert row["positive_sessions"] == sum(v > 0 for v in sessions)
        assert row["negative_sessions"] == sum(v < 0 for v in sessions)
        for field, value in (("q1_pct", quartile(effects, 1)), ("q3_pct", quartile(effects, 3)),
                             ("pooled_block_median_pct", median(effects)), ("min_pct", min(effects)), ("max_pct", max(effects))):
            equal(box[field], value)
        assert box["positive_blocks"] == sum(v > 0 for v in effects)
        assert box["negative_blocks"] == sum(v < 0 for v in effects)
    old_runs = [ROOT / f"results/EXP-009/RUN-{i:04d}" for i in range(1, 4)]
    _, old_sessions, old_totals = closing.combine(old_runs)
    assert (ROOT / "analysis/final-comparison-EXP-009/three-session-effects.csv").read_bytes() == analysis.csv_bytes(old_totals)
    assert (ROOT / "analysis/final-comparison-EXP-009/session-effects.csv").read_bytes() == analysis.csv_bytes(old_sessions)
    comparison = []
    for old, new in zip(old_totals, totals):
        keys = ("reference", "candidate", "parameter_set", "operation")
        assert all(old[key] == new[key] for key in keys)
        comparison.append(dict(**{key: new[key] for key in keys},
            exp009_median_pct=old["median_session_improvement_pct"],
            exp010_median_pct=new["median_session_improvement_pct"],
            difference_percentage_points=new["median_session_improvement_pct"] - old["median_session_improvement_pct"],
            exp009_positive_sessions=old["positive_sessions"], exp009_negative_sessions=old["negative_sessions"],
            exp010_positive_sessions=new["positive_sessions"], exp010_negative_sessions=new["negative_sessions"]))
    provenance_checks = {}
    for directory, code_key in ((ROOT / "analysis/random-seed-EXP-010", "analysis_sha256"),
                                (ROOT / "analysis/figures/EXP-010", "code_sha256")):
        provenance = json.loads((directory / "provenance.json").read_text())
        for group in ("inputs", code_key):
            for name, expected in provenance[group].items():
                assert sha(ROOT / name) == expected, name
        for name, expected in provenance["outputs"].items():
            assert sha(directory / name) == expected, name
        provenance_checks[directory.relative_to(ROOT).as_posix()] = len(provenance["outputs"])
    for name, data in (("paired-effects", pairs), ("session-effects", estimates),
                       ("five-session-effects", totals), ("box-statistics", boxes)):
        assert (ROOT / f"analysis/random-seed-EXP-010/{name}.csv").read_bytes() == analysis.csv_bytes(data)
    for stem, direct in (("exp010-original-reference-dot-box", False), ("exp010-direct-candidate-dot-box", True)):
        data = [row for row in pairs if (row["reference"] == "exp003") == direct]
        assert (ROOT / f"analysis/figures/EXP-010/{stem}.csv").read_bytes() == analysis.csv_bytes(data)
    report = dict(activity_id="ACT-0026", experiment="EXP-010", outcome="accepted",
        audit_script_sha256=sha(Path(__file__)), git_commands_executed=False, new_measurements_collected=False,
        sessions=reviews, unique_saved_seeds=60, total_duration_rows=sum(r["duration_rows"] for r in reviews),
        total_measured_exchanges=540000, total_checked_warmup_exchanges=54000,
        total_raw_files=2250, total_steps=1125, total_builds=45, total_matching_assembly_bodies=540,
        selected_source_files=len(common.selected_source_hashes()),
        independent_arithmetic="Raw integer durations; sorted rational medians, rational paired ratios and explicitly interpolated quartiles; float comparisons within 1e-10 absolute or 1e-12 relative tolerance.",
        original_comparison_raw_reanalysis="pass", original_and_followup_pooled=False,
        current_support_matches_every_record=True, derived_csv_reproduction="byte-identical",
        saved_artifact_provenance_checks=provenance_checks, figure_data_matches_verified_pairs=True,
        original_reference_pairs_per_candidate=540, original_reference_all_positive=all(
            row["improvement_pct"] > 0 for row in pairs if row["reference"] == "baseline"),
        five_session_effects=totals, box_statistics=boxes, comparison_with_exp009=comparison,
        limitations=["Single WSL host; no confidence intervals, population significance or portability claim.",
            "One matched block per seed; input variation cannot be separated from measurement variation.",
            "Power, background load, breaks, temperature and physical core placement were not recorded for these sessions.",
            "Warm-up success follows the hash-verified harness and successful process exits; only measured durations are recorded as CSV rows.",
            "Source/assembly identity and round trips do not add a new timing-leakage or constant-time result."])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x") as stream:
        stream.write(json.dumps(report, indent=2) + "\n")
    print("Accepted all five sessions: 1620000 raw duration rows, 45 binaries, 540 assembly bodies; independent arithmetic and saved graph data agree.")


if __name__ == "__main__":
    main()
