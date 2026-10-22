#!/usr/bin/env python3
"""Collect a metadata snapshot without building or running Kyber."""

import argparse
import hashlib
import json
import os
import platform
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UPSTREAM = ROOT / "external" / "kyber-official"
PIN = "3edd5af5991927164edd4aacebfcbee00b8064e7"


def command(argv, cwd=ROOT):
    environment = dict(os.environ, LC_ALL="C", GIT_OPTIONAL_LOCKS="0")
    result = subprocess.run(
        argv, cwd=cwd, env=environment, text=True,
        capture_output=True, timeout=30, check=False,
    )
    if result.returncode:
        raise RuntimeError(
            f"Command failed: {argv!r}\n{result.stderr.strip()}"
        )
    return result.stdout.strip()


def git(*args, cwd=ROOT):
    return command(["git", *args], cwd)


def source_status():
    # Existing result records must not prevent the next snapshot.
    return git(
        "status", "--porcelain=v1", "--untracked-files=all",
        "--ignore-submodules=none", "--", ".", ":(exclude)results",
    )


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_text(path):
    try:
        return Path(path).read_text(encoding="utf-8").strip()
    except OSError:
        return None


def proc_fields(path):
    fields = {}
    for line in (read_text(path) or "").splitlines():
        key, separator, value = line.partition(":")
        if separator:
            fields.setdefault(key.strip(), value.strip())
    return fields


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--experiment", required=True)
    parser.add_argument("--run", required=True)
    parser.add_argument("--variant", default="baseline")
    parser.add_argument("--compiler", default="gcc")
    parser.add_argument("--binary", type=Path)
    parser.add_argument("--host-os", default="unknown")
    parser.add_argument("--power-mode", default="unknown")
    parser.add_argument("--background-load", default="unknown")
    args = parser.parse_args()

    for value, pattern, label in (
        (args.experiment, r"EXP-[0-9]{3}", "experiment"),
        (args.run, r"RUN-[0-9]{4}", "run"),
        (args.variant, r"[a-z0-9][a-z0-9-]{0,63}", "variant"),
    ):
        if not re.fullmatch(pattern, value):
            parser.error(f"Invalid {label}: {value!r}")

    if platform.system() != "Linux":
        parser.error("Run this collector inside Linux or Ubuntu/WSL.")

    results = ROOT / "results"
    experiment_dir = results / args.experiment
    run_dir = experiment_dir / args.run
    if any(path.is_symlink() for path in (results, experiment_dir, run_dir)):
        parser.error("Result directories must not be symbolic links.")
    if any(path.exists() and not path.is_dir()
           for path in (results, experiment_dir, run_dir)):
        parser.error("Result paths must be directories.")
    if run_dir.exists():
        parser.error("Run ID already exists; use a new ID.")

    if source_status():
        parser.error("Commit changes outside results/ before collecting metadata.")

    source_commit = git("rev-parse", "HEAD")
    collector = Path(__file__).resolve()
    collector_relative = collector.relative_to(ROOT).as_posix()
    git("cat-file", "-e", f"{source_commit}:{collector_relative}")
    tree_entry = git("ls-tree", "HEAD", "--", "external/kyber-official").split()
    if len(tree_entry) < 3 or tree_entry[:2] != ["160000", "commit"]:
        parser.error("The committed upstream submodule entry is missing.")

    upstream_commit = git("rev-parse", "HEAD", cwd=UPSTREAM)
    if tree_entry[2] != PIN or upstream_commit != PIN:
        parser.error("The recorded and checked-out upstream revisions must match PIN.")
    if git(
        "status", "--porcelain=v1", "--untracked-files=all",
        "--ignore-submodules=none", cwd=UPSTREAM,
    ):
        parser.error("The upstream checkout contains uncommitted changes.")

    compiler_found = shutil.which(args.compiler)
    if compiler_found is None:
        parser.error(f"Compiler not found: {args.compiler}")
    compiler = Path(compiler_found).resolve()
    compiler_version = command(
        [str(compiler), "-dumpfullversion", "-dumpversion"]
    )
    if not re.fullmatch(r"\d+(?:\.\d+)*", compiler_version):
        parser.error("Expected a numeric GCC-compatible compiler version.")

    executable = None
    if args.binary is not None:
        binary = args.binary
        if not binary.is_absolute():
            binary = ROOT / binary
        binary = binary.resolve()
        if not binary.is_relative_to(ROOT) or not binary.is_file():
            parser.error("--binary must identify a file inside this repository.")
        executable = {
            "path": binary.relative_to(ROOT).as_posix(),
            "sha256": sha256(binary),
            "build_provenance": "not-recorded",
        }

    try:
        release = platform.freedesktop_os_release()
    except OSError:
        release = {}
    cpu = proc_fields("/proc/cpuinfo")
    memory = proc_fields("/proc/meminfo").get("MemTotal")
    visible_ram = int(memory.split()[0]) * 1024 if memory else None
    kernel = platform.release()
    affinity = sorted(os.sched_getaffinity(0))
    governors = {}
    for path in sorted(Path("/sys/devices/system/cpu/cpufreq").glob(
        "policy*/scaling_governor"
    )):
        governors[path.parent.name] = read_text(path)

    metadata = {
        "schema_version": 1,
        "record_type": "metadata-only",
        "experiment_id": args.experiment,
        "run_id": args.run,
        "variant": args.variant,
        "provenance": {
            "source_commit": source_commit,
            "branch": git("rev-parse", "--abbrev-ref", "HEAD"),
            "source_tree_clean": True,
            "cleanliness_scope": (
                "Git-visible tracked and non-ignored untracked files "
                "outside results/"
            ),
            "upstream_commit": upstream_commit,
            "upstream_tree_clean": True,
            "collector_path": collector_relative,
            "collector_sha256": sha256(collector),
            "collector_arguments": sys.argv[1:],
        },
        "environment": {
            "os": {key: release.get(key) for key in
                   ("ID", "VERSION_ID", "PRETTY_NAME")},
            "kernel_release": kernel,
            "architecture": platform.machine(),
            "wsl_detected": "microsoft" in kernel.lower(),
            "cpu_model": cpu.get("model name", cpu.get("Hardware")),
            "logical_cpus_visible": os.cpu_count(),
            "collector_affinity": affinity,
            "linux_visible_ram_bytes": visible_ram,
            "scaling_governors": governors or None,
            "python": {
                "path": str(Path(sys.executable).resolve()),
                "version": platform.python_version(),
            },
            "available_compiler": {
                "requested": args.compiler,
                "path": str(compiler),
                "version": compiler_version,
                "sha256": sha256(compiler),
            },
        },
        "manual_conditions": {
            "host_os": args.host_os,
            "power_mode": args.power_mode,
            "background_load": args.background_load,
            "physical_core_placement": "unknown",
        },
        "executable": executable,
        "build": {"status": "not-recorded", "command": None, "flags": None},
        "execution": {
            "benchmark_executed": False,
            "correctness": "not-run",
            "arithmetic_safety": "not-run",
            "timing_behaviour": "not-run",
        },
    }

    if git("rev-parse", "HEAD") != source_commit or source_status():
        raise RuntimeError("Source state changed during collection; no record saved.")

    if git("rev-parse", "HEAD", cwd=UPSTREAM) != upstream_commit or git(
        "status", "--porcelain=v1", "--untracked-files=all",
        "--ignore-submodules=none", cwd=UPSTREAM,
    ):
        raise RuntimeError("Upstream state changed; no record saved.")

    payload = json.dumps(metadata, indent=2, sort_keys=True) + "\n"
    experiment_dir.mkdir(parents=True, exist_ok=True)
    run_dir.mkdir()  # No exist_ok: reused IDs must fail.
    destination = run_dir / "metadata.json"
    try:
        with destination.open("x", encoding="utf-8") as handle:
            handle.write(payload)
    except OSError as error:
        raise RuntimeError(
            "Writing failed. Preserve the incomplete run directory and "
            "use a new run ID after investigating."
        ) from error

    print(f"Saved {destination.relative_to(ROOT).as_posix()}")
    print("Metadata only: no build, correctness test or benchmark was run.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, RuntimeError, subprocess.TimeoutExpired) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        sys.exit(1)
