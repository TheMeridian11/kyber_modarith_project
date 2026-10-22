#!/usr/bin/env python3
"""Compare validated EXP-003 with a fresh build of the accepted EXP-002 source."""

import argparse
import csv
import json
import os
import re
import signal
import hashlib
import subprocess
import sys
from pathlib import Path

import collect_run_metadata as metadata
import run_invntt_validation as candidate
import run_incremental_comparison as incremental
import run_comparison as paired
import run_timing as timing
import run_validation as validation

ROOT = metadata.ROOT
VALIDATION = ROOT / "results/EXP-003/RUN-0001/manifest.json"
REFERENCE = ROOT / "results/EXP-002/RUN-0002/manifest.json"
REVIEW = ROOT / "notes/evidence/ACT-0011/exp-003-run-0001-review.json"
SUPPORT = tuple(dict.fromkeys((
    "scripts/run_invntt_comparison.py", *incremental.SUPPORT, *candidate.SUPPORT,
)))
VARIANTS = ("wide-dot", "staged-invntt")
FUNCTIONS = ("invntt", "montgomery_reduce", "barrett_reduce")


assembly_record = incremental.assembly_record


def load_gate(sources):
    review = json.loads(REVIEW.read_text())
    recorded = json.loads(VALIDATION.read_text())
    reference = json.loads(REFERENCE.read_text())
    if (review.get("accepted_for_comparison") is not True
            or metadata.sha256(VALIDATION) != review["manifest_sha256"]
            or metadata.sha256(REFERENCE) != review["reference_manifest_sha256"]
            or recorded["status"] != "completed" or reference["status"] != "completed"
            or recorded["provenance_recheck"] != "pass" or reference["provenance_recheck"] != "pass"
            or recorded["checks"]["parameters"] != {"512": "pass", "768": "pass", "1024": "pass"}
            or recorded["source_file_sha256"] != sources
            or reference["source_file_sha256"]["wide-dot"] != candidate.reference_sources()["wide-dot"]
            or recorded["build_modes"]["normal"] != list(validation.FLAGS)
            or reference["build_flags"] != list(validation.FLAGS)
            or recorded["compiler"] != reference["compiler"]
            or recorded["objdump"] != reference["validation_evidence"]["objdump"]):
        raise RuntimeError("Sources, flags or tools differ from the accepted evidence.")
    return {
        "validation_manifest": VALIDATION.relative_to(ROOT).as_posix(),
        "validation_manifest_sha256": metadata.sha256(VALIDATION),
        "reference_manifest": REFERENCE.relative_to(ROOT).as_posix(),
        "reference_manifest_sha256": metadata.sha256(REFERENCE),
        "review": REVIEW.relative_to(ROOT).as_posix(), "review_sha256": metadata.sha256(REVIEW),
        "validation_source_commit": recorded["source_commit"],
        "reference_source_commit": reference["source_commit"],
        "reference_source_file_sha256": reference["source_file_sha256"]["wide-dot"],
        "compiler": recorded["compiler"], "objdump": recorded["objdump"],
        "assembly": review["assembly"],
    }


def read_reference_blob(commit, name):
    if not re.fullmatch(r"[0-9a-f]{40}", commit) or Path(name).is_absolute() or ".." in Path(name).parts:
        raise RuntimeError("Invalid historical source identity.")
    command = ["git", "show", f"{commit}:implementation/kyber-optimised-ref/{name}"]
    result = subprocess.run(command, cwd=ROOT, capture_output=True, check=False, timeout=30,
                            env={**os.environ, "LC_ALL": "C", "GIT_OPTIONAL_LOCKS": "0"})
    if result.returncode:
        raise RuntimeError(f"Cannot read the retained EXP-002 source: {name}")
    return result.stdout  # Keep exact bytes, including the final newline.


def restore_reference(directory, gate):
    directory.mkdir()
    for name, digest in gate["reference_source_file_sha256"].items():
        data = read_reference_blob(gate["reference_source_commit"], name)
        if hashlib.sha256(data).hexdigest() != digest:
            raise RuntimeError(f"Historical EXP-002 source hash differs: {name}")
        target = directory / name
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("xb") as handle:
            handle.write(data)
    check_reference(directory, gate)


def check_reference(directory, gate):
    expected = gate["reference_source_file_sha256"]
    observed = {p.relative_to(directory).as_posix(): metadata.sha256(p)
                for p in directory.rglob("*") if p.is_file()}
    if observed != expected or any(p.is_symlink() for p in directory.rglob("*")):
        raise RuntimeError("Restored EXP-002 source changed.")


def order_for_block(block):
    return VARIANTS if block % 2 else VARIANTS[::-1]


def comparison_rows(summaries, blocks):
    # Reuse the accepted paired calculation with explicit experiment names.
    labels = dict(zip(VARIANTS, ("baseline", "fused-basemul")))
    if any(r["variant"] not in labels for r in summaries):
        raise RuntimeError("Unexpected comparison variant.")
    rows = [{**r, "variant": labels[r["variant"]]} for r in summaries]
    pairs, aggregate = paired.comparison_rows(rows, blocks)
    for row in (*pairs, *aggregate):
        for key in list(row):
            if key.startswith("baseline_"):
                row[key.replace("baseline_", "exp002_", 1)] = row.pop(key)
            elif key.startswith("candidate_"):
                row[key.replace("candidate_", "exp003_", 1)] = row.pop(key)
        if "first_variant" in row:
            row["first_variant"] = order_for_block(row["block"])[0]
    return pairs, aggregate


def execute_comparison(run_dir, snapshot, sources, gate, args, original_affinity):
    compiler = snapshot["environment"]["available_compiler"]
    build = run_dir / "build"
    environment = {"PATH": "/usr/bin:/bin", "LC_ALL": "C", "TMPDIR": str(build)}
    support = {name: metadata.sha256(ROOT / name) for name in SUPPORT}
    manifest = {
        "schema_version": 1, "record_type": "paired-timing", "purpose": "EXP-003-incremental-comparison",
        "experiment_id": args.experiment, "run_id": args.run, "variant": "wide-dot-vs-staged-invntt",
        "status": "running", "source_commit": snapshot["provenance"]["source_commit"],
        "upstream_commit": metadata.PIN, "metadata_file": "metadata.json",
        "metadata_sha256": metadata.sha256(run_dir / "metadata.json"),
        "source_file_sha256": {"wide-dot": gate["reference_source_file_sha256"],
                               "staged-invntt": sources["staged-invntt"]},
        "support_file_sha256": support,
        "control_source": {"commit": gate["reference_source_commit"],
                           "path": "implementation/kyber-optimised-ref",
                           "restored_to": "build/exp002-source",
                           "method": "read-only git show; each file checked against accepted SHA-256"},
        "compiler": compiler, "build_flags": list(validation.FLAGS),
        "validation_evidence": {k: v for k, v in gate.items() if k != "assembly"},
        "process_environment": environment, "invocation_arguments": sys.argv[1:],
        "protocol": {
            "timer": "CLOCK_MONOTONIC_RAW", "units": "ns", "blocks": args.blocks,
            "iterations_per_operation": args.iterations, "warmup_triplets_per_process": args.warmup,
            "fixture_seed": args.seed, "input_mode": "derand-shake256-v1",
            "same_fixtures_in_every_block": True, "operations": list(timing.OPERATIONS),
            "order": "block, then 512/768/1024; adjacent variant pairs; EXP-002 first in odd blocks",
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
    reference_dir = build / "exp002-source"
    directories = {"wide-dot": reference_dir, "staged-invntt": candidate.CANDIDATE}

    def check_identity():
        validation.check_source_state(manifest["source_commit"], sources["baseline"])
        if candidate.source_snapshot() != sources or load_gate(sources) != gate:
            raise RuntimeError("Candidate or accepted validation evidence changed.")
        if reference_dir.exists():
            check_reference(reference_dir, gate)
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
        restore_reference(reference_dir, gate)
        manifest["checks"]["reviewed_assembly_match"] = "running"
        for parameter, k in validation.PARAMETERS:
            for variant, directory in directories.items():
                label = f"{variant}-{parameter}"
                executable = build / label
                print(f"Building Kyber{parameter}: {variant}...", flush=True)
                step("build-" + label, paired.build_command(compiler["path"], directory, k, executable), directory)
                manifest["executables"][label] = {
                    "path": executable.relative_to(run_dir).as_posix(),
                    "sha256": metadata.sha256(executable),
                }
                for function in FUNCTIONS:
                    symbol = f"pqcrystals_kyber{parameter}_ref_{function}"
                    item = step(f"assembly-{label}-{function}",
                                [gate["objdump"]["path"], "-d", "--insn-width=16", "--disassemble=" + symbol, str(executable)],
                                directory)
                    observed = assembly_record((run_dir / item["stdout"]).read_text(), symbol)
                    if observed != gate["assembly"][str(parameter)][variant][function]:
                        raise RuntimeError(f"Timing-build assembly differs from reviewed code: {label}, {function}")
        manifest["checks"]["reviewed_assembly_match"] = "pass"
        check_identity()
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
                                directories[variant])
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
            "speedup": "EXP-002 process median / EXP-003 process median",
            "improvement_pct": "100 * (1 - EXP-003 process median / EXP-002 process median)",
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
    parser.add_argument("--experiment", default="EXP-003")
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
    if (args.experiment != "EXP-003" or not 1 <= args.blocks <= 100
            or not 1 <= args.iterations <= 1000000 or not 0 <= args.warmup <= 1000000
            or not 0 <= args.seed < 2**64 or args.timeout <= 0):
        parser.error("Use EXP-003 and valid blocks, iterations, warmup, seed and timeout.")
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
        "--experiment", args.experiment, "--run", args.run, "--variant", "wide-dot-vs-staged-invntt",
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
