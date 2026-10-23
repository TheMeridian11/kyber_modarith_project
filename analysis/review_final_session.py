#!/usr/bin/env python3
"""Audit retained EXP-009 data and local build identities without running Git or benchmarks."""
import argparse
from collections import Counter
import csv
import hashlib
import itertools
import json
from pathlib import Path
import statistics
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import analyse_final_comparison as final_analysis
import run_final_comparison as runner


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def rows(path):
    with Path(path).open(newline="") as stream:
        return list(csv.DictReader(stream))


def audit(run):
    # The frozen analyser reconstructs all three CSV tables byte-for-byte.
    m, aggregate = final_analysis.read_run(run)
    p = runner.load_protocol()
    assert p == m["protocol"]
    snapshot = json.loads((run / "metadata.json").read_text())
    assert snapshot["provenance"]["source_commit"] == m["source_commit"]
    assert snapshot["provenance"]["upstream_commit"] == m["upstream_commit"] == runner.metadata.PIN
    assert snapshot["provenance"]["source_tree_clean"] and snapshot["provenance"]["upstream_tree_clean"]
    assert snapshot["environment"]["collector_affinity"] == m["affinity"]["observed"] == [p["cpu"]]
    assert m["affinity"]["selected_logical_cpu"] == p["cpu"]
    assert m["benchmark_executed"]
    assert set(m["support_file_sha256"]) == set(runner.SUPPORT)
    for name, digest in m["support_file_sha256"].items():
        assert sha(ROOT / name) == digest, name
    leakage = json.loads((ROOT / runner.LEAKAGE).read_text())
    assert m["source_file_sha256"] == runner.historical.source_maps() == leakage["source_file_sha256"]
    assert m["compiler"] == leakage["compiler"] == snapshot["environment"]["available_compiler"]
    assert m["build_flags"] == leakage["build_flags"] == list(runner.validation.FLAGS)
    assert m["tool_sha256"] == leakage["tool_sha256"]
    for name, digest in {**m["tool_sha256"], m["compiler"]["path"]: m["compiler"]["sha256"]}.items():
        assert sha(name) == digest, name
    directories = {"baseline": runner.validation.BASELINE,
                   "exp003": run / "build/exp003-source", "exp005": run / "build/exp005-source"}
    for variant, source in m["source_file_sha256"].items():
        assert len(source) == 35
        for name, digest in source.items():
            assert sha(directories[variant] / name) == digest, (variant, name)
        if variant != "baseline":
            assert not any(f.is_symlink() for f in directories[variant].rglob("*"))
            assert {f.relative_to(directories[variant]).as_posix() for f in directories[variant].rglob("*") if f.is_file()} == set(source)
    expected_tags = {f"{v}-{k}" for v, k in itertools.product(p["variants"], final_analysis.PARAMETERS)}
    assert set(m["executables"]) == expected_tags
    for entry in m["executables"].values():
        assert sha(run / entry["path"]) == entry["sha256"]
    assert m["process_environment"] == {"PATH": "/usr/bin:/bin", "LC_ALL": "C", "TMPDIR": str(run / "build")}
    steps = {s["label"]: s for s in m["steps"]}
    assert len(steps) == 225
    raw_hashes = {}
    for s in m["steps"]:
        assert s["timeout_seconds"] == p["timeout_seconds"]
        for stream in ("stdout", "stderr"):
            assert s[stream] not in raw_hashes
            raw_hashes[s[stream]] = sha(run / s[stream])
            assert raw_hashes[s[stream]] == s[stream + "_sha256"]
    assert len(raw_hashes) == 450
    assert set(raw_hashes) == {f.relative_to(run).as_posix() for f in (run / "raw").iterdir()}
    expected_assembly = runner.assembly_gate(p, leakage)
    assert set(m["assembly"]) == set(expected_assembly)
    normalised = {}
    expected_labels = []
    for parameter, k in runner.validation.PARAMETERS:
        for variant in p["variants"]:
            tag = f"{variant}-{parameter}"
            exe = run / m["executables"][tag]["path"]
            label = "build-" + tag
            expected_labels.append(label)
            s = steps[label]
            assert s["argv"] == runner.paired.build_command(m["compiler"]["path"], directories[variant], k, exe)
            assert s["cwd"] == str(directories[variant])
            assert (run / s["stderr"]).read_bytes() == (run / s["stdout"]).read_bytes() == b""
            for function in (*runner.historical.SYMBOLS, "indcpa_keypair_derand"):
                symbol = f"pqcrystals_kyber{parameter}_ref_{function}"
                key = tag + "/" + symbol
                label = "assembly-" + tag + "-" + function
                expected_labels.append(label)
                s = steps[label]
                assert s["argv"] == ["/usr/bin/objdump", "-d", "--insn-width=16", "--disassemble=" + symbol, str(exe)]
                assert s["cwd"] == str(directories[variant]) and not (run / s["stderr"]).read_bytes()
                assert s["stdout"] == m["assembly"][key]["path"]
                observed = runner.assembly.assembly_record((run / s["stdout"]).read_text(), symbol)
                assert observed == m["assembly"][key]["normalised"] == expected_assembly[key], key
                normalised[key] = observed
    expected_datasets = []
    for block in range(1, p["blocks"] + 1):
        rotation = (block - 1) % 3
        parameters = final_analysis.PARAMETERS[rotation:] + final_analysis.PARAMETERS[:rotation]
        seed = p["session_seeds"][m["session"] - 1] + block - 1
        for parameter in parameters:
            for position, variant in enumerate(runner.order_for_block(p, m["session"], block, parameter), 1):
                expected_datasets.append((parameter, variant, block, position, seed))
                tag = f"{variant}-{parameter}"
                label = f"timing-{tag}-block-{block:04d}"
                expected_labels.append(label)
                s = steps[label]
                assert s["argv"] == [str(run / m["executables"][tag]["path"]), str(p["iterations"]), str(p["warmup"]), str(seed)]
                assert s["cwd"] == str(directories[variant])
    assert [s["label"] for s in m["steps"]] == expected_labels
    assert [tuple(d[k] for k in ("parameter", "variant", "block", "position", "fixture_seed")) for d in m["datasets"]] == expected_datasets
    order_counts = {}
    for parameter in final_analysis.PARAMETERS:
        counts = Counter(tuple(d["variant"] for d in m["datasets"] if d["parameter"] == parameter and d["block"] == b) for b in range(1, 13))
        assert counts == Counter({tuple(order): 2 for order in p["permutations"]})
        order_counts[str(parameter)] = {" / ".join(order): n for order, n in counts.items()}
    # Independent calculation: no frozen summary/derive helpers are used below.
    ops = ("keygen", "encap", "decap")
    independent = {}
    diagnostics = []
    for d in m["datasets"]:
        data = rows(run / d["path"])
        assert len(data) == 3000
        values = {op: [] for op in ops}
        for index, row in enumerate(data):
            assert set(row) == {"parameter_set", "operation", "iteration", "elapsed_ns", "roundtrip_ok"}
            assert row["parameter_set"] == f"Kyber{d['parameter']}" and row["operation"] == ops[index % 3]
            assert int(row["iteration"]) == index // 3 and row["roundtrip_ok"] == "1"
            elapsed = int(row["elapsed_ns"])
            assert 0 < elapsed < 2**64
            values[row["operation"]].append(elapsed)
        for op, durations in values.items():
            independent[(d["variant"], d["parameter"], d["block"], op)] = dict(
                samples=len(durations), median_ns=statistics.median(durations), min_ns=min(durations), max_ns=max(durations))
        s = steps[f"timing-{d['variant']}-{d['parameter']}-block-{d['block']:04d}"]
        lines = (run / s["stderr"]).read_text().splitlines()
        diag = dict(line.split("=", 1) for line in lines)
        assert len(lines) == len(diag) == 8
        assert int(diag["clock_resolution_ns"]) > 0 and int(diag["empty_timer_pair_min_ns"]) >= 0
        diagnostics.append(diag)
    for row in rows(run / "derived/process-summary.csv"):
        key = (row["variant"], int(row["parameter_set"][5:]), int(row["block"]), row["operation"])
        assert all(float(row[k]) == value for k, value in independent[key].items())
    pair_rows = rows(run / "derived/paired-comparison.csv")
    effects = {}
    for row in pair_rows:
        parameter, block = int(row["parameter_set"][5:]), int(row["block"])
        a, b = [independent[(v, parameter, block, row["operation"])]["median_ns"] for v in (row["reference"], row["candidate"])]
        effect = 100 * (1 - b / a)
        assert float(row["improvement_pct"]) == effect and float(row["speedup"]) == a / b
        effects[(row["reference"], row["candidate"], parameter, block, row["operation"])] = effect
    order_strata = []
    for row in aggregate:
        key = (row["reference"], row["candidate"], int(row["parameter_set"][5:]))
        values = [effects[(*key, b, row["operation"])] for b in range(1, 13)]
        assert row["median_paired_improvement_pct"] == statistics.median(values)
        assert row["min_paired_improvement_pct"] == min(values) and row["max_paired_improvement_pct"] == max(values)
        assert (row["positive_blocks"], row["negative_blocks"]) == (sum(v > 0 for v in values), sum(v < 0 for v in values))
        groups = {name: [float(r["improvement_pct"]) for r in pair_rows if
                       all(r[k] == row[k] for k in ("reference", "candidate", "parameter_set", "operation")) and
                       (int(r["reference_position"]) < int(r["candidate_position"])) == before]
                  for name, before in (("reference_first", True), ("candidate_first", False))}
        assert all(len(g) == 6 for g in groups.values())
        order_strata.append({k: row[k] for k in ("reference", "candidate", "parameter_set", "operation")} |
                            {k + "_median_pct": statistics.median(v) for k, v in groups.items()})
    return dict(activity_id="ACT-0019", experiment_id=m["experiment_id"], run_id=m["run_id"], session=m["session"],
                accepted_session=True, final_candidate_selected=False, source_commit=m["source_commit"],
                manifest_sha256=sha(run / "manifest.json"), metadata_sha256=sha(run / "metadata.json"),
                audit_code_sha256=sha(__file__), frozen_support_sha256=m["support_file_sha256"],
                source_file_sha256=m["source_file_sha256"], compiler=m["compiler"], tool_sha256=m["tool_sha256"],
                executable_sha256={k: v["sha256"] for k, v in m["executables"].items()},
                raw_file_sha256=raw_hashes, assembly_normalised=normalised,
                checks=dict(frozen_reanalysis="pass", independent_arithmetic="pass", source_tool_binary_identity="pass",
                            reviewed_assembly="pass", warning_free_builds="pass", exact_step_order="pass", balanced_orders="pass"),
                coverage=dict(builds=9, assembly_bodies=108, measurement_processes=108, completed_steps=225,
                              raw_files=450, duration_rows=324000, measured_roundtrips=108000, warmup_roundtrips=10800,
                              process_summaries=324, paired_effects=324, aggregate_groups=27),
                derived=m["derived"], order_counts=order_counts, session_estimates=aggregate,
                descriptive_order_strata=order_strata,
                timer_diagnostics={k: dict(min=min(int(d[k]) for d in diagnostics), max=max(int(d[k]) for d in diagnostics))
                                   for k in ("clock_resolution_ns", "empty_timer_pair_min_ns")},
                manual_conditions=snapshot["manual_conditions"],
                limitations=["One of three predeclared sessions; no final selection or cross-session inference.",
                             "No outlier exclusion or timer-overhead subtraction; paired range is not a confidence interval.",
                             "Normal-code identities support scoped reuse of accepted security evidence; no new leakage test.",
                             "WSL logical affinity is not physical-core/frequency control; manual power and load fields remain as recorded."])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", type=Path, default=ROOT / "results/EXP-009/RUN-0001")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    review = audit(args.run.resolve())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x") as stream:
        json.dump(review, stream, indent=2, sort_keys=True)
        stream.write("\n")
    print(json.dumps({k: review[k] for k in ("accepted_session", "session", "coverage", "checks", "timer_diagnostics")}))


if __name__ == "__main__":
    main()
