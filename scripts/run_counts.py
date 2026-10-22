#!/usr/bin/env python3
"""Record baseline reduction calls in a separate, untimed instrumented build."""

import argparse
import csv
import json
import signal
import subprocess
import sys
from pathlib import Path

import collect_run_metadata as metadata
import run_validation as validation

ROOT = metadata.ROOT
HARNESS = ROOT / "benchmarks" / "count_reductions.c"
FLAGS = (*validation.FLAGS, "-fno-lto")
OPERATIONS = ("keygen", "encap", "decap")
CSV_FIELDS = (
    "parameter_set", "operation", "iteration",
    "montgomery_calls", "barrett_calls", "roundtrip_ok",
)
# Source-derived predictions from EXP-000; never generate observations from these.
EXPECTED = {
    512: ((6656, 2048), (9088, 4736), (13312, 6656)),
    768: ((11904, 3072), (14976, 6400), (20736, 8576)),
    1024: ((18432, 4096), (22144, 8064), (29440, 10496)),
}


def build_command(compiler, parameter, k, executable):
    return [
        compiler, *FLAGS, f"-DKYBER_K={k}", "-I", str(validation.BASELINE),
        *validation.SOURCES[:-1], str(HARNESS),
        f"-Wl,--wrap=pqcrystals_kyber{parameter}_ref_montgomery_reduce",
        f"-Wl,--wrap=pqcrystals_kyber{parameter}_ref_barrett_reduce",
        "-o", str(executable),
    ]


def summarise_csv(path, parameter, iterations):
    observations = {operation: [] for operation in OPERATIONS}
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != list(CSV_FIELDS):
            raise RuntimeError(f"Unexpected CSV header: {path}")
        rows = 0
        for rows, row in enumerate(reader, start=1):
            index, position = divmod(rows - 1, 3)
            operation = OPERATIONS[position]
            if (index >= iterations or row["parameter_set"] != f"Kyber{parameter}"
                    or row["operation"] != operation or row["iteration"] != str(index)
                    or row["roundtrip_ok"] != "1" or None in row):
                raise RuntimeError(f"Invalid or failed observation: {path}, row {rows}")
            try:
                counts = (int(row["montgomery_calls"]), int(row["barrett_calls"]))
            except (ValueError, TypeError) as error:
                raise RuntimeError(f"Invalid count: {path}, row {rows}") from error
            if any(not 0 <= value < 2**64 for value in counts):
                raise RuntimeError(f"Count outside uint64 range: {path}, row {rows}")
            observations[operation].append(counts)
        if rows != iterations * 3:
            raise RuntimeError(f"Incomplete CSV: {path}; {rows} rows")

    summaries = []
    for position, operation in enumerate(OPERATIONS):
        values = observations[operation]
        if len(set(values)) != 1:
            raise RuntimeError(f"Counts vary across fixtures: Kyber{parameter} {operation}")
        observed = values[0]
        expected = EXPECTED[parameter][position]
        if observed != expected:
            raise RuntimeError(
                f"Count prediction mismatch: Kyber{parameter} {operation}; "
                f"observed {observed}, expected {expected}. Preserve and investigate."
            )
        summaries.append({
            "parameter_set": f"Kyber{parameter}", "operation": operation,
            "samples": len(values), "montgomery_calls": observed[0],
            "barrett_calls": observed[1],
        })
    return summaries


def execute_counts(run_dir, snapshot, source_hashes, args):
    compiler = snapshot["environment"]["available_compiler"]
    build_dir = run_dir / "build"
    environment = {"PATH": "/usr/bin:/bin", "LC_ALL": "C", "TMPDIR": str(build_dir)}
    support_hashes = {
        name: metadata.sha256(ROOT / name)
        for name in ("scripts/run_counts.py", "scripts/run_validation.py",
                     "scripts/collect_run_metadata.py", "benchmarks/count_reductions.c")
    }
    manifest = {
        "schema_version": 1, "record_type": "reduction-counts",
        "experiment_id": args.experiment, "run_id": args.run, "variant": "baseline",
        "status": "running", "source_commit": snapshot["provenance"]["source_commit"],
        "upstream_commit": metadata.PIN, "metadata_file": "metadata.json",
        "metadata_sha256": metadata.sha256(run_dir / "metadata.json"),
        "source_file_sha256": source_hashes, "support_file_sha256": support_hashes,
        "compiler": compiler, "build_flags": list(FLAGS),
        "process_environment": environment, "invocation_arguments": sys.argv[1:],
        "protocol": {
            "instrumentation": "GNU linker --wrap on external reduction references",
            "iterations_per_operation": args.iterations, "fixture_seed": args.seed,
            "input_mode": "derand-shake256-v1", "fixture_phase": 1,
            "operations": list(OPERATIONS), "counter_reset": "before each KEM operation",
            "decapsulation_input": "valid ciphertext from the same exchange",
            "unit": "reduction-function invocations",
            "performance_measurements": False,
        },
        "predicted_counts": {
            str(parameter): dict(zip(OPERATIONS, values))
            for parameter, values in EXPECTED.items()
        },
        "steps": [], "executables": {}, "datasets": [],
        "checks": {
            "reduction_counts": {str(p): "not-run" for p, _ in validation.PARAMETERS},
            "arithmetic_safety": "not-run", "timing_behaviour": "not-run",
        },
        "provenance_recheck": "not-run", "counts_executed": False,
        "benchmark_executed": False,
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
        summaries = []
        for parameter, k in validation.PARAMETERS:
            executable = build_dir / f"count_kyber{parameter}"
            command = build_command(compiler["path"], parameter, k, executable)
            print(f"Building Kyber{parameter} reduction counter...", flush=True)
            if not validation.run_step(
                run_dir, manifest, f"build-{parameter}", command,
                validation.BASELINE, environment, args.timeout,
            ):
                raise RuntimeError(f"Build failed for Kyber{parameter}.")
            manifest["executables"][str(parameter)] = {
                "path": executable.relative_to(run_dir).as_posix(),
                "sha256": metadata.sha256(executable),
            }
            label = f"counts-{parameter}"
            command = [str(executable), str(args.iterations), str(args.seed)]
            print(f"Counting Kyber{parameter} reductions...", flush=True)
            manifest["counts_executed"] = True
            states = manifest["checks"]["reduction_counts"]
            states[str(parameter)] = "running"
            if not validation.run_step(
                run_dir, manifest, label, command,
                validation.BASELINE, environment, args.timeout,
            ):
                states[str(parameter)] = (
                    "fail" if manifest["steps"][-1]["status"] == "failed" else "inconclusive"
                )
                raise RuntimeError(f"Counting failed: {label}; inspect raw logs.")
            step = manifest["steps"][-1]
            csv_path = run_dir / "raw" / f"{label}.csv"
            if csv_path.exists():
                raise RuntimeError(f"Refusing to replace {csv_path}")
            (run_dir / step["stdout"]).rename(csv_path)
            step["stdout"] = csv_path.relative_to(run_dir).as_posix()
            validation.save_manifest(run_dir, manifest)
            try:
                summaries.extend(summarise_csv(csv_path, parameter, args.iterations))
            except RuntimeError:
                states[str(parameter)] = "fail"
                raise
            states[str(parameter)] = "pass"
            manifest["datasets"].append({
                "parameter_set": f"Kyber{parameter}", "path": step["stdout"],
                "sha256": metadata.sha256(csv_path), "rows": args.iterations * 3,
            })

        manifest["provenance_recheck"] = "running"
        validation.check_source_state(source_commit, source_hashes)
        if metadata.sha256(Path(compiler["path"])) != compiler["sha256"]:
            raise RuntimeError("Compiler changed during counting.")
        for name, digest in support_hashes.items():
            if metadata.sha256(ROOT / name) != digest:
                raise RuntimeError(f"Support file changed: {name}")
        for executable in manifest["executables"].values():
            if metadata.sha256(run_dir / executable["path"]) != executable["sha256"]:
                raise RuntimeError("Executable changed during counting.")
        manifest["provenance_recheck"] = "pass"
        (run_dir / "derived").mkdir()
        summary_path = run_dir / "derived" / "summary.csv"
        with summary_path.open("x", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(summaries[0]), lineterminator="\n")
            writer.writeheader()
            writer.writerows(summaries)
        manifest["summary"] = {
            "path": "derived/summary.csv", "sha256": metadata.sha256(summary_path),
            "method": "observed calls per operation; require agreement across fixtures",
        }
        manifest["status"] = "completed"
    except KeyboardInterrupt:
        manifest["status"] = "interrupted"
        manifest["error"] = "Interrupted; preserve partial evidence."
    except (OSError, RuntimeError, ValueError, subprocess.TimeoutExpired) as error:
        manifest["status"] = "failed"
        manifest["error"] = str(error)
    finally:
        for parameter, state in manifest["checks"]["reduction_counts"].items():
            if state == "running":
                manifest["checks"]["reduction_counts"][parameter] = "inconclusive"
        if manifest["provenance_recheck"] == "running":
            manifest["provenance_recheck"] = "inconclusive"
        validation.save_manifest(run_dir, manifest)
    print(f"Counting status: {manifest['status']}")
    print(f"Record: {run_dir.relative_to(ROOT).as_posix()}/manifest.json")
    print("No performance measurements were collected.")
    return 0 if manifest["status"] == "completed" else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--experiment", default="EXP-000")
    parser.add_argument("--run", required=True)
    parser.add_argument("--iterations", type=int, default=10)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--compiler", default="gcc")
    parser.add_argument("--timeout", type=int, default=120)
    args = parser.parse_args()
    if sys.platform != "linux":
        parser.error("Run inside Ubuntu/WSL or Linux.")
    if not (1 <= args.iterations <= 1000 and 0 <= args.seed < 2**64 and args.timeout > 0):
        parser.error("Invalid iterations, seed or timeout.")
    source_hashes = validation.source_snapshot()
    command = [
        sys.executable, "-B", str(ROOT / "scripts/collect_run_metadata.py"),
        "--experiment", args.experiment, "--run", args.run,
        "--variant", "baseline", "--compiler", args.compiler,
    ]
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, check=False)
    if result.returncode:
        print(result.stdout, end="")
        print(result.stderr, end="", file=sys.stderr)
        return result.returncode
    run_dir = ROOT / "results" / args.experiment / args.run
    snapshot = json.loads((run_dir / "metadata.json").read_text(encoding="utf-8"))
    return execute_counts(run_dir, snapshot, source_hashes, args)


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
