#!/usr/bin/env python3
"""Compare the validated EXP-001 candidate with a freshly built baseline."""

import argparse
import csv
import json
import os
import re
import signal
import statistics
import subprocess
import sys
from pathlib import Path

import collect_run_metadata as metadata
import run_candidate_validation as candidate
import run_timing as timing
import run_validation as validation

ROOT = metadata.ROOT
VALIDATION = ROOT / "results/EXP-001/RUN-0001/manifest.json"
REVIEW = ROOT / "notes/evidence/ACT-0007/run-0001-review.json"
SUPPORT = tuple(dict.fromkeys((
    "scripts/run_comparison.py", "scripts/run_timing.py", "benchmarks/bench_kem.c",
    *candidate.SUPPORT,
)))
FUNCTIONS = ("basemul", "montgomery_reduce")


def normalise_assembly(text, symbol):
    """Keep instructions/operands; ignore only addresses and direct-call locations."""
    marker = f"<{symbol}>:"
    if text.count(marker) != 1:
        raise RuntimeError(f"Missing or ambiguous assembly symbol: {symbol}")
    body = text.split(marker, 1)[1].split("Disassembly of section", 1)[0]
    instructions = []
    for line in body.splitlines():
        match = re.match(r"^\s*[0-9a-f]+:\s+(?:[0-9a-f]{2}\s+)+(.+?)\s*$", line)
        if match:
            instruction = " ".join(match[1].split())
            instruction = re.sub(r"^(callq?) [0-9a-f]+ (<[^>]+>)$", r"\1 \2", instruction)
            instructions.append(instruction)
    if not instructions or instructions[-1] != "ret":
        raise RuntimeError(f"Incomplete assembly: {symbol}")
    return instructions


def load_gate(sources):
    review = json.loads(REVIEW.read_text())
    recorded = json.loads(VALIDATION.read_text())
    if (review.get("accepted_for_comparison") is not True
            or metadata.sha256(VALIDATION) != review["manifest_sha256"]
            or recorded["status"] != "completed"
            or recorded["provenance_recheck"] != "pass"
            or recorded["checks"]["parameters"] != {"512": "pass", "768": "pass", "1024": "pass"}
            or recorded["source_file_sha256"] != sources
            or recorded["build_modes"]["normal"] != list(validation.FLAGS)):
        raise RuntimeError("Current source/flags do not match the accepted validation and review.")
    return {
        "validation_manifest": VALIDATION.relative_to(ROOT).as_posix(),
        "validation_manifest_sha256": metadata.sha256(VALIDATION),
        "review": REVIEW.relative_to(ROOT).as_posix(),
        "review_sha256": metadata.sha256(REVIEW),
        "validation_source_commit": recorded["source_commit"],
        "compiler": recorded["compiler"], "objdump": recorded["objdump"],
        "assembly": review["assembly"],
    }


def build_command(compiler, directory, k, executable):
    return [compiler, *validation.FLAGS, f"-DKYBER_K={k}", "-I", str(directory),
            *validation.SOURCES[:-1], str(timing.HARNESS), "-o", str(executable)]


def order_for_block(block):
    return ("baseline", "fused-basemul") if block % 2 else ("fused-basemul", "baseline")


def comparison_rows(summaries, blocks):
    indexed = {}
    for row in summaries:
        key = (row["parameter_set"], row["block"], row["operation"], row["variant"])
        if key in indexed or row["median_ns"] <= 0:
            raise RuntimeError("Duplicate summary or non-positive median.")
        indexed[key] = row
    expected = {
        (f"Kyber{p}", block, op, variant)
        for p, _ in validation.PARAMETERS for block in range(1, blocks + 1)
        for op in timing.OPERATIONS for variant in candidate.VARIANTS
    }
    if indexed.keys() != expected:
        raise RuntimeError("Incomplete or unexpected comparison groups.")
    pairs, aggregate = [], []
    for p, _ in validation.PARAMETERS:
        for op in timing.OPERATIONS:
            group = []
            for block in range(1, blocks + 1):
                b = indexed[(f"Kyber{p}", block, op, "baseline")]
                c = indexed[(f"Kyber{p}", block, op, "fused-basemul")]
                if b["samples"] != c["samples"]:
                    raise RuntimeError("Unequal sample counts within a comparison pair.")
                group.append({
                    "parameter_set": f"Kyber{p}", "operation": op, "block": block,
                    "first_variant": order_for_block(block)[0],
                    "baseline_median_ns": b["median_ns"], "candidate_median_ns": c["median_ns"],
                    "speedup": b["median_ns"] / c["median_ns"],
                    "improvement_pct": 100 * (1 - c["median_ns"] / b["median_ns"]),
                })
            pairs.extend(group)
            improvements = [r["improvement_pct"] for r in group]
            aggregate.append({
                "parameter_set": f"Kyber{p}", "operation": op, "pairs": blocks,
                "baseline_median_of_medians_ns": statistics.median(r["baseline_median_ns"] for r in group),
                "candidate_median_of_medians_ns": statistics.median(r["candidate_median_ns"] for r in group),
                "median_paired_speedup": statistics.median(r["speedup"] for r in group),
                "median_paired_improvement_pct": statistics.median(improvements),
                "min_paired_improvement_pct": min(improvements),
                "max_paired_improvement_pct": max(improvements),
            })
    return pairs, aggregate


def execute_comparison(run_dir, snapshot, sources, gate, args, original_affinity):
    compiler = snapshot["environment"]["available_compiler"]
    build = run_dir / "build"
    environment = {"PATH": "/usr/bin:/bin", "LC_ALL": "C", "TMPDIR": str(build)}
    support = {name: metadata.sha256(ROOT / name) for name in SUPPORT}
    manifest = {
        "schema_version": 1, "record_type": "paired-timing", "purpose": "EXP-001-comparison",
        "experiment_id": args.experiment, "run_id": args.run, "variant": "baseline-vs-fused-basemul",
        "status": "running", "source_commit": snapshot["provenance"]["source_commit"],
        "upstream_commit": metadata.PIN, "metadata_file": "metadata.json",
        "metadata_sha256": metadata.sha256(run_dir / "metadata.json"),
        "source_file_sha256": sources, "support_file_sha256": support,
        "compiler": compiler, "build_flags": list(validation.FLAGS),
        "validation_evidence": {k: v for k, v in gate.items() if k != "assembly"},
        "process_environment": environment, "invocation_arguments": sys.argv[1:],
        "protocol": {
            "timer": "CLOCK_MONOTONIC_RAW", "units": "ns", "blocks": args.blocks,
            "iterations_per_operation": args.iterations, "warmup_triplets_per_process": args.warmup,
            "fixture_seed": args.seed, "input_mode": "derand-shake256-v1",
            "same_fixtures_in_every_block": True, "operations": list(timing.OPERATIONS),
            "order": "block, then 512/768/1024; adjacent variant pairs; baseline first in odd blocks",
            "timer_overhead_subtracted": False, "outliers_removed": False,
            "original_affinity": original_affinity, "selected_logical_cpu": args.cpu,
            "observed_affinity": sorted(os.sched_getaffinity(0)), "physical_core_placement": "unknown",
        },
        "checks": {"reviewed_assembly_match": "not-run", "measured_roundtrips": "not-run",
                   "csv_integrity": "not-run", "statistical_leakage": "not-run",
                   "constant_time_proof": "not-established"},
        "steps": [], "executables": {}, "datasets": [], "derived": {},
        "provenance_recheck": "not-run", "benchmark_executed": False,
    }
    validation.save_manifest(run_dir, manifest)

    def check_identity():
        validation.check_source_state(manifest["source_commit"], sources["baseline"])
        if candidate.source_snapshot() != sources or load_gate(sources) != gate:
            raise RuntimeError("Candidate or accepted validation evidence changed.")
        for tool in (compiler, gate["objdump"]):
            if metadata.sha256(Path(tool["path"])) != tool["sha256"]:
                raise RuntimeError("Compiler or disassembler changed.")
        if sorted(os.sched_getaffinity(0)) != [args.cpu]:
            raise RuntimeError("Requested CPU affinity changed.")
        for name, digest in support.items():
            if metadata.sha256(ROOT / name) != digest:
                raise RuntimeError(f"Support file changed: {name}")
        for item in manifest["executables"].values():
            if metadata.sha256(run_dir / item["path"]) != item["sha256"]:
                raise RuntimeError("Timing executable changed.")

    def step(label, command, directory):
        if not validation.run_step(run_dir, manifest, label, command, directory, environment, args.timeout):
            raise RuntimeError(f"Step failed or incomplete: {label}; inspect retained logs.")
        return manifest["steps"][-1]

    try:
        build.mkdir()
        (run_dir / "raw").mkdir()
        if compiler["sha256"] != gate["compiler"]["sha256"]:
            raise RuntimeError("Use the compiler whose generated code was reviewed.")
        for name in (*SUPPORT, REVIEW.relative_to(ROOT).as_posix()):
            metadata.git("cat-file", "-e", f"{manifest['source_commit']}:{name}")
        check_identity()
        manifest["checks"]["reviewed_assembly_match"] = "running"
        for parameter, k in validation.PARAMETERS:
            for variant, directory in candidate.VARIANTS.items():
                label = f"{variant}-{parameter}"
                executable = build / label
                print(f"Building Kyber{parameter}: {variant}...", flush=True)
                step("build-" + label, build_command(compiler["path"], directory, k, executable), directory)
                manifest["executables"][label] = {
                    "path": executable.relative_to(run_dir).as_posix(),
                    "sha256": metadata.sha256(executable),
                }
                for function in FUNCTIONS:
                    symbol = f"pqcrystals_kyber{parameter}_ref_{function}"
                    item = step(f"assembly-{label}-{function}",
                                [gate["objdump"]["path"], "-d", "--disassemble=" + symbol, str(executable)],
                                directory)
                    observed = normalise_assembly((run_dir / item["stdout"]).read_text(), symbol)
                    if observed != gate["assembly"][str(parameter)][variant][function]["instructions"]:
                        raise RuntimeError(f"Timing-build assembly differs from reviewed code: {label}, {function}")
        manifest["checks"]["reviewed_assembly_match"] = "pass"
        summaries = []
        for block in range(1, args.blocks + 1):
            for parameter, _ in validation.PARAMETERS:
                for position, variant in enumerate(order_for_block(block), start=1):
                    label = f"{variant}-{parameter}"
                    executable = run_dir / manifest["executables"][label]["path"]
                    name = f"timing-{label}-block-{block:04d}"
                    print(f"Measuring Kyber{parameter}, block {block}, {variant}...", flush=True)
                    manifest["benchmark_executed"] = True
                    manifest["checks"].update(measured_roundtrips="running", csv_integrity="running")
                    item = step(name, [str(executable), str(args.iterations), str(args.warmup), str(args.seed)],
                                candidate.VARIANTS[variant])
                    csv_path = run_dir / "raw" / (name + ".csv")
                    if csv_path.exists():
                        raise RuntimeError(f"Refusing to replace {csv_path}")
                    (run_dir / item["stdout"]).rename(csv_path)
                    item["stdout"] = csv_path.relative_to(run_dir).as_posix()
                    validation.save_manifest(run_dir, manifest)
                    for row in timing.summarise_csv(csv_path, parameter, args.iterations, block):
                        row["block"] = row.pop("repetition")
                        summaries.append({"variant": variant, **row})
                    manifest["datasets"].append({
                        "variant": variant, "parameter_set": f"Kyber{parameter}", "block": block,
                        "position_in_pair": position, "path": item["stdout"],
                        "sha256": metadata.sha256(csv_path), "rows": args.iterations * 3,
                    })
        pairs, aggregate = comparison_rows(summaries, args.blocks)
        manifest["checks"].update(measured_roundtrips="pass", csv_integrity="pass")
        manifest["provenance_recheck"] = "running"
        check_identity()
        derived = run_dir / "derived"
        derived.mkdir()
        for name, rows in (("process-summary", summaries), ("paired-comparison", pairs), ("comparison", aggregate)):
            path = derived / (name + ".csv")
            with path.open("x", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
                writer.writeheader()
                writer.writerows(rows)
            manifest["derived"][name] = {
                "path": path.relative_to(run_dir).as_posix(), "sha256": metadata.sha256(path), "rows": len(rows),
            }
        manifest["analysis"] = {
            "speedup": "baseline process median / candidate process median",
            "improvement_pct": "100 * (1 - candidate process median / baseline process median)",
            "aggregate": "median of paired effects; min/max describe observed pairs, not confidence intervals",
            "unit_of_comparison": "matched process pair; inner observations are not independent experiments",
        }
        manifest["provenance_recheck"] = "pass"
        manifest["status"] = "completed"
    except KeyboardInterrupt:
        manifest["status"] = "interrupted"
        manifest["error"] = "Interrupted; preserve partial evidence."
    except (OSError, RuntimeError, ValueError, subprocess.TimeoutExpired) as error:
        manifest["status"] = "failed"
        manifest["error"] = str(error)
    finally:
        for name, state in manifest["checks"].items():
            if state == "running":
                manifest["checks"][name] = "inconclusive"
        if manifest["provenance_recheck"] == "running":
            manifest["provenance_recheck"] = "inconclusive"
        validation.save_manifest(run_dir, manifest)
    print(f"Comparison status: {manifest['status']}")
    print(f"Record: {run_dir}/manifest.json")
    return 0 if manifest["status"] == "completed" else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--experiment", default="EXP-001")
    parser.add_argument("--run", required=True)
    parser.add_argument("--blocks", type=int, default=5)
    parser.add_argument("--iterations", type=int, default=1000)
    parser.add_argument("--warmup", type=int, default=100)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--cpu", type=int)
    parser.add_argument("--compiler", default="gcc")
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--host-os", default="unknown")
    parser.add_argument("--power-mode", default="unknown")
    parser.add_argument("--background-load", default="unknown")
    args = parser.parse_args()
    if sys.platform != "linux":
        parser.error("Run inside Ubuntu/WSL or Linux.")
    if (args.experiment != "EXP-001" or not 1 <= args.blocks <= 100
            or not 1 <= args.iterations <= 1000000 or not 0 <= args.warmup <= 1000000
            or not 0 <= args.seed < 2**64 or args.timeout <= 0):
        parser.error("Use EXP-001 and valid blocks, iterations, warmup, seed and timeout.")
    original_affinity = sorted(os.sched_getaffinity(0))
    if args.cpu is None:
        args.cpu = original_affinity[0]
    if args.cpu not in original_affinity:
        parser.error("--cpu must be in the current allowed CPU set.")
    sources = candidate.source_snapshot()
    gate = load_gate(sources)
    os.sched_setaffinity(0, {args.cpu})
    command = [
        sys.executable, "-B", str(ROOT / "scripts/collect_run_metadata.py"),
        "--experiment", args.experiment, "--run", args.run, "--variant", "baseline-vs-fused-basemul",
        "--compiler", args.compiler, "--host-os", args.host_os,
        "--power-mode", args.power_mode, "--background-load", args.background_load,
    ]
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, check=False)
    if result.returncode:
        print(result.stdout, end="")
        print(result.stderr, end="", file=sys.stderr)
        return result.returncode
    run_dir = ROOT / "results" / args.experiment / args.run
    snapshot = json.loads((run_dir / "metadata.json").read_text())
    return execute_comparison(run_dir, snapshot, sources, gate, args, original_affinity)


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, validation.interrupt_requested)
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("Interrupted; preserve any created run directory.", file=sys.stderr)
        sys.exit(130)
    except (OSError, RuntimeError, ValueError, subprocess.TimeoutExpired) as error:
        print(f"ERROR: {error}; preserve any created run directory.", file=sys.stderr)
        sys.exit(1)
