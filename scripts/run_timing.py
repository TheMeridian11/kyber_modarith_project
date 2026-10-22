#!/usr/bin/env python3
"""Collect baseline per-operation timings; arithmetic remains unchanged."""

import argparse
import csv
import json
import os
import signal
import statistics
import subprocess
import sys
from pathlib import Path

import collect_run_metadata as metadata
import run_validation as validation

ROOT = metadata.ROOT
HARNESS = ROOT / "benchmarks" / "bench_kem.c"
OPERATIONS = ("keygen", "encap", "decap")
CSV_FIELDS = ("parameter_set", "operation", "iteration", "elapsed_ns", "roundtrip_ok")


def summarise_csv(path, parameter, iterations, repetition):
    values = {operation: [] for operation in OPERATIONS}
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != list(CSV_FIELDS):
            raise RuntimeError(f"Unexpected CSV header: {path}")
        rows = 0
        for rows, row in enumerate(reader, start=1):
            index, position = divmod(rows - 1, 3)
            operation = OPERATIONS[position]
            if (index >= iterations or row["parameter_set"] != f"Kyber{parameter}"
                    or row["operation"] != operation
                    or row["iteration"] != str(index)
                    or row["roundtrip_ok"] != "1" or None in row):
                raise RuntimeError(f"Invalid or failed CSV sample: {path}, row {rows}")
            try:
                elapsed = int(row["elapsed_ns"])
            except (ValueError, TypeError) as error:
                raise RuntimeError(f"Invalid duration: {path}, row {rows}") from error
            if not 0 < elapsed < 2**64:
                raise RuntimeError(f"Invalid duration: {path}, row {rows}")
            values[operation].append(elapsed)
        if rows != iterations * 3:
            raise RuntimeError(f"Incomplete CSV: {path}; {rows} rows")
    return [
        {
            "parameter_set": f"Kyber{parameter}", "repetition": repetition,
            "operation": operation, "samples": len(data),
            "median_ns": statistics.median(data), "min_ns": min(data),
            "max_ns": max(data),
        }
        for operation, data in values.items()
    ]


def execute_timing(run_dir, snapshot, source_hashes, args, original_affinity):
    compiler = snapshot["environment"]["available_compiler"]
    build_dir = run_dir / "build"
    environment = {"PATH": "/usr/bin:/bin", "LC_ALL": "C", "TMPDIR": str(build_dir)}
    support_hashes = {
        name: metadata.sha256(ROOT / name)
        for name in ("scripts/run_timing.py", "scripts/run_validation.py",
                     "scripts/collect_run_metadata.py", "benchmarks/bench_kem.c")
    }
    manifest = {
        "schema_version": 1, "record_type": "raw-timing", "purpose": "baseline-pilot",
        "experiment_id": args.experiment, "run_id": args.run, "variant": "baseline",
        "status": "running", "source_commit": snapshot["provenance"]["source_commit"],
        "upstream_commit": metadata.PIN, "metadata_file": "metadata.json",
        "metadata_sha256": metadata.sha256(run_dir / "metadata.json"),
        "source_file_sha256": source_hashes, "support_file_sha256": support_hashes,
        "compiler": compiler, "build_flags": list(validation.FLAGS),
        "process_environment": environment, "invocation_arguments": sys.argv[1:],
        "protocol": {
            "timer": "CLOCK_MONOTONIC_RAW", "units": "ns",
            "iterations_per_operation": args.iterations,
            "warmup_triplets_per_process": args.warmup,
            "repetitions": args.repetitions, "fixture_seed": args.seed,
            "input_mode": "derand-shake256-v1",
            "operations": list(OPERATIONS),
            "timer_overhead_subtracted": False, "outliers_removed": False,
            "order": "repetition outer loop; parameters 512,768,1024; keygen,encap,decap",
            "original_affinity": original_affinity,
            "selected_logical_cpu": args.cpu,
            "observed_affinity": sorted(os.sched_getaffinity(0)),
            "physical_core_placement": "unknown",
        },
        "steps": [], "executables": {}, "datasets": [],
        "checks": {"measured_roundtrips": "not-run", "csv_integrity": "not-run",
                   "arithmetic_safety": "not-run", "timing_behaviour": "not-run"},
        "provenance_recheck": "not-run", "benchmark_executed": False,
    }
    validation.save_manifest(run_dir, manifest)
    try:
        build_dir.mkdir()
        (run_dir / "raw").mkdir()
        source_commit = manifest["source_commit"]
        for name in support_hashes:
            metadata.git("cat-file", "-e", f"{source_commit}:{name}")
        validation.check_source_state(source_commit, source_hashes)
        if metadata.sha256(Path(compiler["path"])) != compiler["sha256"]:
            raise RuntimeError("Compiler changed after collection.")
        for parameter, k in validation.PARAMETERS:
            executable = build_dir / f"bench_kyber{parameter}"
            command = [
                compiler["path"], *validation.FLAGS, f"-DKYBER_K={k}",
                "-I", str(validation.BASELINE),
                *validation.SOURCES[:-1], str(HARNESS), "-o", str(executable),
            ]
            print(f"Building Kyber{parameter} timing harness...", flush=True)
            if not validation.run_step(
                run_dir, manifest, f"build-{parameter}", command,
                validation.BASELINE, environment, args.timeout,
            ):
                raise RuntimeError(f"Build failed for Kyber{parameter}.")
            manifest["executables"][str(parameter)] = {
                "path": executable.relative_to(run_dir).as_posix(),
                "sha256": metadata.sha256(executable),
            }

        summaries = []
        for repetition in range(1, args.repetitions + 1):
            for parameter, _ in validation.PARAMETERS:
                executable = run_dir / manifest["executables"][str(parameter)]["path"]
                label = f"timing-{parameter}-rep-{repetition:04d}"
                command = [str(executable), str(args.iterations),
                           str(args.warmup), str(args.seed)]
                print(f"Measuring Kyber{parameter}, repetition {repetition}...", flush=True)
                manifest["benchmark_executed"] = True
                manifest["checks"]["measured_roundtrips"] = "running"
                manifest["checks"]["csv_integrity"] = "running"
                if not validation.run_step(
                    run_dir, manifest, label, command,
                    validation.BASELINE, environment, args.timeout,
                ):
                    raise RuntimeError(f"Measurement failed: {label}; inspect raw logs.")
                # Rename the completed raw stdout without changing its bytes.
                step = manifest["steps"][-1]
                csv_path = run_dir / "raw" / f"{label}.csv"
                if csv_path.exists():
                    raise RuntimeError(f"Refusing to replace {csv_path}")
                (run_dir / step["stdout"]).rename(csv_path)
                step["stdout"] = csv_path.relative_to(run_dir).as_posix()
                validation.save_manifest(run_dir, manifest)
                summaries.extend(summarise_csv(
                    csv_path, parameter, args.iterations, repetition,
                ))
                manifest["datasets"].append({
                    "parameter_set": f"Kyber{parameter}", "repetition": repetition,
                    "path": step["stdout"], "sha256": metadata.sha256(csv_path),
                    "rows": args.iterations * 3,
                })

        manifest["checks"]["measured_roundtrips"] = "pass"
        manifest["checks"]["csv_integrity"] = "pass"
        manifest["provenance_recheck"] = "running"
        validation.check_source_state(source_commit, source_hashes)
        if metadata.sha256(Path(compiler["path"])) != compiler["sha256"]:
            raise RuntimeError("Compiler changed during timing.")
        for name, digest in support_hashes.items():
            if metadata.sha256(ROOT / name) != digest:
                raise RuntimeError(f"Support file changed: {name}")
        for executable in manifest["executables"].values():
            if metadata.sha256(run_dir / executable["path"]) != executable["sha256"]:
                raise RuntimeError("Executable changed during timing.")
        if sorted(os.sched_getaffinity(0)) != [args.cpu]:
            raise RuntimeError("Requested CPU affinity changed.")
        manifest["provenance_recheck"] = "pass"
        derived = run_dir / "derived"
        derived.mkdir()
        summary_path = derived / "summary.csv"
        with summary_path.open("x", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(summaries[0]))
            writer.writeheader()
            writer.writerows(summaries)
        manifest["summary"] = {
            "path": "derived/summary.csv", "sha256": metadata.sha256(summary_path),
            "method": "per-process, per-operation median/min/max; no exclusions",
        }
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
    print(f"Timing status: {manifest['status']}")
    print(f"Record: {run_dir.relative_to(ROOT).as_posix()}/manifest.json")
    return 0 if manifest["status"] == "completed" else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--experiment", default="EXP-000")
    parser.add_argument("--run", required=True)
    parser.add_argument("--iterations", type=int, default=1000)
    parser.add_argument("--warmup", type=int, default=100)
    parser.add_argument("--repetitions", type=int, default=5)
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
    if not (1 <= args.iterations <= 1000000 and 0 <= args.warmup <= 1000000
            and 1 <= args.repetitions <= 100 and 0 <= args.seed < 2**64
            and args.timeout > 0):
        parser.error("Invalid iterations, warmup, repetitions, seed or timeout.")
    original_affinity = sorted(os.sched_getaffinity(0))
    if args.cpu is None:
        args.cpu = original_affinity[0]
    if args.cpu not in original_affinity:
        parser.error("--cpu must be in the current allowed CPU set.")
    source_hashes = validation.source_snapshot()
    # Pin this process before collecting metadata; children inherit affinity.
    os.sched_setaffinity(0, {args.cpu})
    command = [
        sys.executable, "-B", str(ROOT / "scripts/collect_run_metadata.py"),
        "--experiment", args.experiment, "--run", args.run, "--variant", "baseline",
        "--compiler", args.compiler, "--host-os", args.host_os,
        "--power-mode", args.power_mode, "--background-load", args.background_load,
    ]
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, check=False)
    if result.returncode:
        print(result.stdout, end="")
        print(result.stderr, end="", file=sys.stderr)
        return result.returncode
    run_dir = ROOT / "results" / args.experiment / args.run
    snapshot = json.loads((run_dir / "metadata.json").read_text(encoding="utf-8"))
    return execute_timing(run_dir, snapshot, source_hashes, args, original_affinity)


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, validation.interrupt_requested)
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("Interrupted. Preserve any created run directory.", file=sys.stderr)
        sys.exit(130)
    except (OSError, RuntimeError, ValueError, subprocess.TimeoutExpired) as error:
        print(f"ERROR: {error}; preserve any created run directory.", file=sys.stderr)
        sys.exit(1)
