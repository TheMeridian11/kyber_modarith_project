#!/usr/bin/env python3
"""Build and archive the pinned baseline's existing functional tests."""

import argparse
import json
import os
import signal
import subprocess
import sys
from pathlib import Path

import collect_run_metadata as metadata

ROOT = metadata.ROOT
BASELINE = ROOT / "implementation" / "kyber-baseline-ref"
UPSTREAM_REF = metadata.UPSTREAM / "ref"
SOURCES = (
    "kem.c", "indcpa.c", "polyvec.c", "poly.c", "ntt.c", "cbd.c",
    "reduce.c", "verify.c", "fips202.c", "symmetric-shake.c",
    "randombytes.c", "test/test_kyber.c",
)
# Explicitly match the pinned upstream functional-test flags.
FLAGS = (
    "-Wall", "-Wextra", "-Wpedantic", "-Wmissing-prototypes",
    "-Wredundant-decls", "-Wshadow", "-Wpointer-arith",
    "-O3", "-fomit-frame-pointer", "-z", "noexecstack",
)
PARAMETERS = ((512, 2), (768, 3), (1024, 4))


def source_snapshot():
    """Require the baseline's C, headers and Makefile to match upstream."""
    def files(directory):
        return {
            path.relative_to(directory).as_posix(): path
            for path in directory.rglob("*")
            if path.is_file() and
            (path.suffix in (".c", ".h") or path.name == "Makefile")
        }

    baseline = files(BASELINE)
    upstream = files(UPSTREAM_REF)
    if not baseline or baseline.keys() != upstream.keys():
        raise RuntimeError("Baseline and upstream source file sets differ.")
    hashes = {}
    for name, path in sorted(baseline.items()):
        if path.is_symlink() or upstream[name].is_symlink():
            raise RuntimeError(f"Source symlinks are not supported: {name}")
        digest = metadata.sha256(path)
        if digest != metadata.sha256(upstream[name]):
            raise RuntimeError(f"Baseline differs from pinned upstream: {name}")
        hashes[name] = digest
    return hashes


def check_source_state(source_commit, expected_hashes):
    if metadata.git("rev-parse", "HEAD") != source_commit:
        raise RuntimeError("Project commit changed during validation.")
    if metadata.source_status():
        raise RuntimeError("Files outside results/ changed during validation.")
    if metadata.git("rev-parse", "HEAD", cwd=metadata.UPSTREAM) != metadata.PIN:
        raise RuntimeError("Upstream commit changed during validation.")
    if metadata.git(
        "status", "--porcelain=v1", "--untracked-files=all",
        "--ignore-submodules=none", cwd=metadata.UPSTREAM,
    ):
        raise RuntimeError("Upstream working tree changed during validation.")
    if source_snapshot() != expected_hashes:
        raise RuntimeError("Baseline source contents changed during validation.")


def save_manifest(run_dir, manifest):
    # Only this attempt's manifest is mutable; raw logs are never replaced.
    temporary = run_dir / "manifest.json.tmp"
    temporary.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    temporary.replace(run_dir / "manifest.json")


def stop_process_group(process):
    try:
        os.killpg(process.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    process.wait()


def run_step(run_dir, manifest, label, argv, cwd, environment, timeout):
    stdout_path = run_dir / "raw" / f"{label}.stdout.log"
    stderr_path = run_dir / "raw" / f"{label}.stderr.log"
    step = {
        "label": label,
        "argv": [str(value) for value in argv],
        "cwd": str(cwd),
        "status": "running",
        "exit_code": None,
        "timeout_seconds": timeout,
        "stdout": stdout_path.relative_to(run_dir).as_posix(),
        "stderr": stderr_path.relative_to(run_dir).as_posix(),
    }
    manifest["steps"].append(step)
    save_manifest(run_dir, manifest)
    try:
        with stdout_path.open("xb") as stdout, stderr_path.open("xb") as stderr:
            process = subprocess.Popen(
                step["argv"], cwd=cwd, env=environment,
                stdout=stdout, stderr=stderr, start_new_session=True,
            )
            try:
                step["exit_code"] = process.wait(timeout=timeout)
                step["status"] = (
                    "completed" if step["exit_code"] == 0 else "failed"
                )
            except subprocess.TimeoutExpired:
                stop_process_group(process)
                step["exit_code"] = process.returncode
                step["status"] = "timed-out"
            except KeyboardInterrupt:
                stop_process_group(process)
                step["exit_code"] = process.returncode
                step["status"] = "interrupted"
                raise
    except OSError as error:
        step["status"] = "launch-error"
        step["error"] = str(error)
    finally:
        for name, path in (("stdout", stdout_path), ("stderr", stderr_path)):
            if path.is_file():
                step[name + "_sha256"] = metadata.sha256(path)
        save_manifest(run_dir, manifest)
    return step["status"] == "completed"


def execute_validation(run_dir, snapshot, expected_hashes, timeout):
    build_dir = run_dir / "build"
    raw_dir = run_dir / "raw"
    compiler = snapshot["environment"]["available_compiler"]
    # A defined environment prevents inherited include/library overrides.
    environment = {
        "PATH": "/usr/bin:/bin",
        "LC_ALL": "C",
        "TMPDIR": str(build_dir),
    }
    manifest = {
        "schema_version": 1,
        "record_type": "functional-validation",
        "status": "running",
        "experiment_id": snapshot["experiment_id"],
        "run_id": snapshot["run_id"],
        "variant": "baseline",
        "source_commit": snapshot["provenance"]["source_commit"],
        "upstream_commit": metadata.PIN,
        "metadata_file": "metadata.json",
        "metadata_sha256": metadata.sha256(run_dir / "metadata.json"),
        "runner_path": "scripts/run_validation.py",
        "runner_sha256": metadata.sha256(Path(__file__).resolve()),
        "source_directory": BASELINE.relative_to(ROOT).as_posix(),
        "source_file_sha256": expected_hashes,
        "compiler": compiler,
        "build_flags": list(FLAGS),
        "process_environment": environment,
        "invocation_arguments": sys.argv[1:],
        "rng_mode": "upstream operating-system randomness; inputs not archived",
        "expected_cases_per_parameter": {
            "valid_exchange": 1000,
            "random_replaced_secret_key": 1000,
            "nonzero_single_byte_ciphertext_corruption": 1000,
        },
        "steps": [],
        "executables": {},
        "checks": {
            "upstream_functional": {
                str(parameter): "not-run" for parameter, _ in PARAMETERS
            },
            "deterministic_vectors": "not-run",
            "arithmetic_safety": "not-run",
            "timing_behaviour": "not-run",
        },
        "provenance_recheck": "not-run",
        "benchmark_executed": False,
    }
    save_manifest(run_dir, manifest)
    try:
        build_dir.mkdir()
        raw_dir.mkdir()
        source_commit = manifest["source_commit"]
        metadata.git("cat-file", "-e", f"{source_commit}:scripts/run_validation.py")
        check_source_state(source_commit, expected_hashes)
        if metadata.sha256(Path(compiler["path"])) != compiler["sha256"]:
            raise RuntimeError("Compiler changed after metadata collection.")
        for parameter, k in PARAMETERS:
            executable = build_dir / f"test_kyber{parameter}"
            compile_command = [
                compiler["path"], *FLAGS, f"-DKYBER_K={k}",
                *SOURCES, "-o", str(executable),
            ]
            print(f"Building Kyber{parameter} functional test...", flush=True)
            if not run_step(
                run_dir, manifest, f"build-{parameter}", compile_command,
                BASELINE, environment, timeout,
            ):
                raise RuntimeError(f"Kyber{parameter} build did not complete.")
            if not executable.is_file() or executable.is_symlink():
                raise RuntimeError(f"Expected executable missing: {executable}")
            manifest["executables"][str(parameter)] = {
                "path": executable.relative_to(run_dir).as_posix(),
                "sha256": metadata.sha256(executable),
                "build_step": f"build-{parameter}",
            }
            print(f"Checking Kyber{parameter}...", flush=True)
            manifest["checks"]["upstream_functional"][str(parameter)] = "running"
            passed = run_step(
                run_dir, manifest, f"test-{parameter}", [str(executable)],
                BASELINE, environment, timeout,
            )
            state = manifest["steps"][-1]["status"]
            manifest["checks"]["upstream_functional"][str(parameter)] = (
                "pass" if passed else "fail" if state == "failed"
                else "inconclusive"
            )
            if not passed:
                raise RuntimeError(f"Kyber{parameter} functional test did not pass.")
        manifest["provenance_recheck"] = "running"
        check_source_state(source_commit, expected_hashes)
        if metadata.sha256(Path(compiler["path"])) != compiler["sha256"]:
            raise RuntimeError("Compiler changed during validation.")
        for executable in manifest["executables"].values():
            if metadata.sha256(run_dir / executable["path"]) != executable["sha256"]:
                raise RuntimeError("An executable changed during validation.")
        manifest["provenance_recheck"] = "pass"
        manifest["status"] = "completed"
    except KeyboardInterrupt:
        manifest["status"] = "interrupted"
        manifest["error"] = "Interrupted; partial logs are preserved."
    except (OSError, RuntimeError, subprocess.TimeoutExpired) as error:
        manifest["status"] = "failed"
        manifest["error"] = str(error)
    finally:
        for parameter, state in manifest["checks"]["upstream_functional"].items():
            if state == "running":
                manifest["checks"]["upstream_functional"][parameter] = "inconclusive"
        if manifest["provenance_recheck"] == "running":
            manifest["provenance_recheck"] = "inconclusive"
        save_manifest(run_dir, manifest)

    print(f"Validation status: {manifest['status']}")
    print(f"Record: {run_dir.relative_to(ROOT).as_posix()}/manifest.json")
    print("No performance measurements were collected.")
    return 0 if manifest["status"] == "completed" else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--experiment", default="EXP-000")
    parser.add_argument("--run", required=True)
    parser.add_argument("--compiler", default="gcc")
    parser.add_argument("--host-os", default="unknown")
    parser.add_argument("--power-mode", default="unknown")
    parser.add_argument("--background-load", default="unknown")
    parser.add_argument("--timeout", type=int, default=120)
    args = parser.parse_args()
    if args.timeout <= 0:
        parser.error("--timeout must be positive.")
    if sys.platform != "linux":
        parser.error("Run inside Ubuntu/WSL or Linux.")

    # Fail before reserving a run if the baseline arithmetic has changed.
    expected_hashes = source_snapshot()
    collector_command = [
        sys.executable, "-B", str(ROOT / "scripts" / "collect_run_metadata.py"),
        "--experiment", args.experiment, "--run", args.run,
        "--variant", "baseline", "--compiler", args.compiler,
        "--host-os", args.host_os, "--power-mode", args.power_mode,
        "--background-load", args.background_load,
    ]
    collection = subprocess.run(
        collector_command, cwd=ROOT, text=True, capture_output=True, check=False,
    )
    if collection.returncode:
        print(collection.stdout, end="")
        print(collection.stderr, end="", file=sys.stderr)
        return collection.returncode

    run_dir = ROOT / "results" / args.experiment / args.run
    snapshot = json.loads((run_dir / "metadata.json").read_text(encoding="utf-8"))
    return execute_validation(run_dir, snapshot, expected_hashes, args.timeout)


def interrupt_requested(signum, frame):
    raise KeyboardInterrupt("Termination requested.")


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, interrupt_requested)
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("Interrupted. Preserve any created run directory.", file=sys.stderr)
        sys.exit(130)
    except (OSError, RuntimeError, ValueError, subprocess.TimeoutExpired) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        print("Preserve any created run directory; use a new ID for a retry.",
              file=sys.stderr)
        sys.exit(1)
