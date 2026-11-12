#!/usr/bin/env python3
"""Collect one committed EXP-010 session using the saved random-seed plan."""
import argparse
import json
import os
import re
import shutil
import signal
import subprocess
import sys
from pathlib import Path

import analyse_random_seed_comparison as analysis
import collect_run_metadata as metadata
import random_seed_common as common
import run_comparison as paired
import run_incremental_comparison as assembly
import run_timing as timing
import run_timing_leakage as historical
import run_validation as validation

ROOT = common.ROOT


def refuse_completed_session(session):
    for path in (ROOT / "results/EXP-010").glob("RUN-*/manifest.json"):
        m = json.loads(path.read_text())
        if m.get("session") == session and m.get("status") == "completed":
            raise RuntimeError(f"Session {session} is already completed in {path.parent.name}; do not replace it")


def preflight(compiler_name, cpu):
    p = common.load_protocol()
    plan = common.load_plan(p)
    leakage, _, _ = common.accepted_context()
    compiler = shutil.which(compiler_name)
    if compiler is None or str(Path(compiler).resolve()) != leakage["compiler"]["path"]:
        raise RuntimeError("Compiler path differs from the reviewed build")
    if cpu != p["cpu"] or cpu not in os.sched_getaffinity(0):
        raise RuntimeError("The frozen protocol requires available guest CPU 0")
    for name, digest in {**leakage["tool_sha256"], compiler: leakage["compiler"]["sha256"]}.items():
        if metadata.sha256(Path(name)) != digest:
            raise RuntimeError("Recorded compiler/disassembler changed: " + name)
    return p, plan


def execute(run_dir, snapshot, p, plan, args, original_affinity):
    leakage, sources, expected = common.accepted_context()
    compiler = snapshot["environment"]["available_compiler"]
    build = run_dir / "build"
    environment = {"PATH": "/usr/bin:/bin", "LC_ALL": "C", "TMPDIR": str(build)}
    dirs = {"baseline": validation.BASELINE, "exp003": build / "exp003-source", "exp005": build / "exp005-source"}
    m = dict(schema_version=1, record_type=p["record_type"], experiment_id="EXP-010", run_id=args.run,
        session=args.session, status="running", development_only=snapshot.get("development_only", False),
        source_commit=snapshot["provenance"]["source_commit"], upstream_commit=metadata.PIN,
        metadata_sha256=metadata.sha256(run_dir / "metadata.json"), protocol=p,
        seed_plan_sha256=p["seed_plan_sha256"], source_file_sha256=sources,
        support_file_sha256={name: metadata.sha256(ROOT / name) for name in common.SUPPORT},
        compiler=compiler, tool_sha256=leakage["tool_sha256"], build_flags=list(validation.FLAGS),
        process_environment=environment, invocation_arguments=sys.argv[1:],
        session_note=args.session_note,
        affinity=dict(original=original_affinity, selected_logical_cpu=args.cpu,
                      observed=sorted(os.sched_getaffinity(0)), physical_core_placement="unknown"),
        steps=[], executables={}, assembly={}, datasets=[], derived={},
        checks={key: "not-run" for key in common.CHECKS}, provenance_recheck="not-run", benchmark_executed=False,
        interpretation="Random-seed performance follow-up; source and normal-code identities reuse bounded prior validation. This is not a new leakage test.")

    def identity():
        validation.check_source_state(m["source_commit"], sources["baseline"])
        if common.load_protocol() != p or common.load_plan(p) != plan:
            raise RuntimeError("Protocol or seed plan changed")
        if common.selected_source_hashes() != sources["exp005"] or historical.source_maps() != sources:
            raise RuntimeError("Source identities changed")
        if compiler != leakage["compiler"] or list(validation.FLAGS) != leakage["build_flags"]:
            raise RuntimeError("Compiler or flags differ from reviewed builds")
        for name, digest in {**m["tool_sha256"], compiler["path"]: compiler["sha256"]}.items():
            if metadata.sha256(Path(name)) != digest:
                raise RuntimeError("Tool changed")
        for name, digest in m["support_file_sha256"].items():
            if metadata.sha256(ROOT / name) != digest:
                raise RuntimeError("Support changed: " + name)
        if sorted(os.sched_getaffinity(0)) != [args.cpu]:
            raise RuntimeError("CPU affinity changed")
        for variant in ("exp003", "exp005"):
            if dirs[variant].exists():
                if any(f.is_symlink() for f in dirs[variant].rglob("*")):
                    raise RuntimeError("Unexpected restored-source symlink")
                actual = {f.relative_to(dirs[variant]).as_posix(): metadata.sha256(f)
                          for f in dirs[variant].rglob("*") if f.is_file()}
                if actual != sources[variant]:
                    raise RuntimeError("Restored source changed")
        for entry in m["executables"].values():
            if metadata.sha256(run_dir / entry["path"]) != entry["sha256"]:
                raise RuntimeError("Executable changed")

    def step(label, command, cwd):
        if not validation.run_step(run_dir, m, label, command, cwd, environment, p["timeout_seconds"]):
            raise RuntimeError("Failed step: " + label)
        return m["steps"][-1]

    validation.save_manifest(run_dir, m)
    try:
        build.mkdir()
        (run_dir / "raw").mkdir()
        (run_dir / "derived").mkdir()
        with (run_dir / "seed-plan.json").open("xb") as stream:
            stream.write(common.PLAN.read_bytes())
        if metadata.sha256(run_dir / "seed-plan.json") != p["seed_plan_sha256"]:
            raise RuntimeError("Copied seed plan differs")
        for name in (*common.SUPPORT, *p["accepted_inputs"]):
            metadata.git("cat-file", "-e", f"{m['source_commit']}:{name}")
        identity()
        for variant in ("exp003", "exp005"):
            historical.restore(dirs[variant], leakage["protocol"]["restoration_commits"][variant], sources[variant])
        for parameter, k in validation.PARAMETERS:
            for variant in common.VARIANTS:
                tag = f"{variant}-{parameter}"
                executable = build / ("bench-" + tag)
                print(f"Building Kyber{parameter}: {variant}...", flush=True)
                result = step("build-" + tag, paired.build_command(compiler["path"], dirs[variant], k, executable), dirs[variant])
                if (run_dir / result["stderr"]).read_text().strip():
                    raise RuntimeError("Build produced diagnostics: " + tag)
                m["executables"][tag] = dict(path=executable.relative_to(run_dir).as_posix(), sha256=metadata.sha256(executable))
                for function in (*historical.SYMBOLS, "indcpa_keypair_derand"):
                    symbol = f"pqcrystals_kyber{parameter}_ref_{function}"
                    result = step("assembly-" + tag + "-" + function,
                        ["/usr/bin/objdump", "-d", "--insn-width=16", "--disassemble=" + symbol, str(executable)], dirs[variant])
                    record = assembly.assembly_record((run_dir / result["stdout"]).read_text(), symbol)
                    key = tag + "/" + symbol
                    if record != expected[key]:
                        raise RuntimeError("Generated code differs from reviewed body: " + key)
                    m["assembly"][key] = dict(path=result["stdout"], normalised=record)
        m["checks"]["reviewed_assembly_match"] = "pass"
        identity()
        summaries = []
        for block, parameter, position, variant, seed in common.schedule(plan, args.session):
            tag = f"{variant}-{parameter}"
            executable = run_dir / m["executables"][tag]["path"]
            print(f"Session {args.session}, trial {block}/12, Kyber{parameter}: {variant}...", flush=True)
            m["benchmark_executed"] = True
            result = step(f"timing-{tag}-block-{block:04d}",
                [str(executable), str(p["iterations"]), str(p["warmup"]), seed], dirs[variant])
            diagnostics = dict(line.split("=", 1) for line in (run_dir / result["stderr"]).read_text().splitlines())
            wanted = dict(timer=p["timer"], unit="ns", iterations=str(p["iterations"]), warmup=str(p["warmup"]),
                          seed=seed, input_mode="derand-shake256-v1")
            if any(diagnostics.get(key) != value for key, value in wanted.items()):
                raise RuntimeError("Harness diagnostics mismatch")
            for key in ("clock_resolution_ns", "empty_timer_pair_min_ns"):
                if int(diagnostics[key]) < 0:
                    raise RuntimeError("Invalid timer diagnostics")
            csv_path = (run_dir / result["stdout"]).with_suffix(".csv")
            if csv_path.exists():
                raise RuntimeError("Refusing to overwrite raw CSV")
            (run_dir / result["stdout"]).rename(csv_path)
            result["stdout"] = csv_path.relative_to(run_dir).as_posix()
            for row in timing.summarise_csv(csv_path, parameter, p["iterations"], block):
                row["block"] = row.pop("repetition")
                summaries.append(dict(variant=variant, position=position, fixture_seed=seed, **row))
            m["datasets"].append(dict(parameter=parameter, variant=variant, block=block, position=position,
                fixture_seed=seed, path=result["stdout"], sha256=metadata.sha256(csv_path), rows=p["iterations"] * 3))
            validation.save_manifest(run_dir, m)
        pairs, estimates = analysis.derive(summaries, 12, args.session)
        for name, rows in (("process-summary", summaries), ("paired-comparison", pairs), ("comparison", estimates)):
            dest = run_dir / "derived" / (name + ".csv")
            analysis.write_csv(dest, rows)
            m["derived"][name] = dict(path=dest.relative_to(run_dir).as_posix(), sha256=metadata.sha256(dest), rows=len(rows))
        identity()
        m["checks"] = {key: "pass" for key in common.CHECKS}
        m["provenance_recheck"] = "pass"
        m["status"] = "completed"
    except KeyboardInterrupt:
        m["status"] = "interrupted"
        m["error"] = "Interrupted; retain the attempt and retry the same session with a new run ID"
    except (OSError, RuntimeError, ValueError, KeyError, subprocess.TimeoutExpired) as error:
        m["status"] = "failed"
        m["error"] = str(error)
    finally:
        validation.save_manifest(run_dir, m)
    print(f"Random-seed comparison: {m['status']}; session {args.session}")
    print("Record:", run_dir / "manifest.json")
    if "error" in m:
        print("Reason:", m["error"])
    return 0 if m["status"] == "completed" else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run")
    parser.add_argument("--session", type=int, choices=range(1, 6))
    parser.add_argument("--cpu", type=int, default=0)
    parser.add_argument("--compiler", default="gcc")
    parser.add_argument("--check", action="store_true", help="Read-only source/plan/tool preflight; no benchmark or Git commands")
    parser.add_argument("--session-note", default="Break, physical placement and thermal conditions not recorded")
    for name in ("host-os", "power-mode", "background-load"):
        parser.add_argument("--" + name, default="unknown")
    args = parser.parse_args()
    if sys.platform != "linux":
        parser.error("Run in Ubuntu/WSL")
    p, plan = preflight(args.compiler, args.cpu)
    if args.check:
        print("Preflight passed: 35 selected files, accepted tools, 60 unique seeds and balanced schedules. No measurements collected.")
        return 0
    if args.session is None or not args.run or not re.fullmatch(r"RUN-[0-9]{4}", args.run):
        parser.error("Specify --session 1..5 and a fresh --run RUN-NNNN")
    parent = ROOT / "results/EXP-010"
    if (ROOT / "results").is_symlink() or parent.is_symlink():
        parser.error("Result directories must not be symlinks")
    parent.mkdir(parents=True, exist_ok=True)
    lock = parent / ".collection.lock"
    try:
        lock_handle = lock.open("x")
    except FileExistsError:
        raise RuntimeError("Collection lock exists. Check whether another run is active before investigating a stale lock")
    original = sorted(os.sched_getaffinity(0))
    try:
        with lock_handle:
            json.dump(dict(pid=os.getpid(), session=args.session, run=args.run), lock_handle)
        refuse_completed_session(args.session)
        os.sched_setaffinity(0, {args.cpu})
        command = [sys.executable, "-B", str(ROOT / "scripts/collect_run_metadata.py"),
            "--experiment", "EXP-010", "--run", args.run, "--variant", "random-seed-three-way",
            "--compiler", args.compiler, "--host-os", args.host_os, "--power-mode", args.power_mode,
            "--background-load", args.background_load]
        result = subprocess.run(command, cwd=ROOT)
        if result.returncode:
            return result.returncode
        run_dir = parent / args.run
        snapshot = json.loads((run_dir / "metadata.json").read_text())
        return execute(run_dir, snapshot, p, plan, args, original)
    finally:
        os.sched_setaffinity(0, set(original))
        lock.unlink()


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, validation.interrupt_requested)
    try:
        sys.exit(main())
    except (OSError, RuntimeError, ValueError, KeyError, subprocess.TimeoutExpired) as error:
        print(f"ERROR: {error}. Retain any failed attempt; use a new run ID for the same session.", file=sys.stderr)
        sys.exit(1)
