#!/usr/bin/env python3
"""Frozen plan and shared validation for the EXP-010 follow-up."""
import collections
import itertools
import json
import re
from pathlib import Path

import collect_run_metadata as metadata
import run_final_comparison as closing
import run_timing_leakage as historical

ROOT = metadata.ROOT
PROTOCOL = ROOT / "tests/random_seed_protocol.json"
PLAN = ROOT / "tests/random_seed_plan.json"
PARAMETERS = (512, 768, 1024)
VARIANTS = ("baseline", "exp003", "exp005")
COMPARISONS = (("baseline", "exp003"), ("baseline", "exp005"), ("exp003", "exp005"))
BUDGET = dict(schema_version=1, experiment="EXP-010", record_type="random-seed-follow-up",
              sessions=5, blocks=12, iterations=1000, warmup=100, cpu=0,
              timer="CLOCK_MONOTONIC_RAW", units="ns", timeout_seconds=120)
CHECKS = ("reviewed_assembly_match", "measured_roundtrips", "csv_integrity", "harness_diagnostics")
SUPPORT = tuple(sorted(set((*closing.SUPPORT,
    "scripts/random_seed_common.py", "scripts/run_random_seed_comparison.py",
    "scripts/analyse_random_seed_comparison.py", "tests/random_seed_protocol.json",
    "tests/random_seed_plan.json", "tests/test_random_seed_comparison.py",
    "analysis/build_random_seed_figures.py", "notes/experiments/EXP-010-random-seeds.md"))))


def validate_protocol(protocol):
    for key, value in BUDGET.items():
        if type(protocol.get(key)) is not type(value) or protocol[key] != value:
            raise ValueError("Unexpected EXP-010 protocol field: " + key)
    if protocol.get("variants") != list(VARIANTS):
        raise ValueError("Unexpected variants")
    if protocol.get("comparisons") != [list(pair) for pair in COMPARISONS]:
        raise ValueError("Unexpected comparisons")
    if protocol.get("seed_plan_path") != "tests/random_seed_plan.json":
        raise ValueError("Unexpected seed-plan path")
    if not re.fullmatch(r"[0-9a-f]{64}", protocol.get("seed_plan_sha256", "")):
        raise ValueError("Missing seed-plan hash")
    required = {"tests/final_comparison_protocol.json", "analysis/final_candidate.json"}
    if set(protocol.get("accepted_inputs", {})) != required:
        raise ValueError("Missing accepted reference pins")
    return protocol


def load_protocol():
    protocol = validate_protocol(json.loads(PROTOCOL.read_text()))
    for name, digest in protocol["accepted_inputs"].items():
        if metadata.sha256(ROOT / name) != digest:
            raise ValueError("Accepted input changed: " + name)
    closing.load_protocol()  # Also checks the underlying validation/security pins.
    return protocol


def validate_plan(plan):
    if plan.get("schema_version") != 1 or plan.get("experiment") != "EXP-010":
        raise ValueError("Wrong seed-plan identity")
    sessions = plan.get("sessions", [])
    if len(sessions) != 5 or [s.get("session") for s in sessions] != list(range(1, 6)):
        raise ValueError("Exactly five ordered sessions required")
    seen = set()
    permutations = collections.Counter({p: 2 for p in itertools.permutations(VARIANTS)})
    for session in sessions:
        seeds = session.get("seeds", [])
        if len(seeds) != 12:
            raise ValueError("Exactly twelve seeds per session required")
        for seed in seeds:
            if not isinstance(seed, str) or not re.fullmatch(r"0|[1-9][0-9]*", seed):
                raise ValueError("Seeds must be canonical unsigned decimal strings")
            if int(seed) >= 2**64 or seed in seen:
                raise ValueError("Seed is outside uint64 or reused")
            seen.add(seed)
        orders = session.get("orders", {})
        if set(orders) != {str(k) for k in PARAMETERS}:
            raise ValueError("Missing parameter order schedules")
        for sequence in orders.values():
            if collections.Counter(tuple(order) for order in sequence) != permutations:
                raise ValueError("Each of the six variant orders must occur twice")
    return plan


def load_plan(protocol, path=PLAN):
    if metadata.sha256(path) != protocol["seed_plan_sha256"]:
        raise ValueError("Seed plan changed; do not regenerate it after measurement")
    return validate_plan(json.loads(path.read_text()))


def schedule(plan, session):
    if type(session) is not int or not 1 <= session <= 5:
        raise ValueError("Session must be 1..5")
    selected = plan["sessions"][session - 1]
    for block, seed in enumerate(selected["seeds"], 1):
        rotation = (block - 1) % 3
        for parameter in PARAMETERS[rotation:] + PARAMETERS[:rotation]:
            for position, variant in enumerate(selected["orders"][str(parameter)][block - 1], 1):
                yield block, parameter, position, variant, seed


def selected_source_hashes():
    directory = ROOT / "implementation/kyber-optimised-ref"
    files = [p for p in directory.rglob("*") if p.is_file()
             and (p.suffix in (".c", ".h") or p.name == "Makefile")]
    if any(p.is_symlink() for p in directory.rglob("*")):
        raise ValueError("Unexpected selected-source symlink")
    actual = {p.relative_to(directory).as_posix(): metadata.sha256(p) for p in files}
    pin = json.loads((ROOT / "analysis/final_candidate.json").read_text())["source_file_sha256"]
    if actual != pin:
        raise ValueError("Working optimisation source differs from the selected 35-file pin")
    return actual


def accepted_context():
    reference = closing.load_protocol()
    leakage = json.loads((ROOT / closing.LEAKAGE).read_text())
    sources = historical.source_maps()
    if sources != leakage["source_file_sha256"] or selected_source_hashes() != sources["exp005"]:
        raise ValueError("Sources differ from accepted evidence")
    return leakage, sources, closing.assembly_gate(reference, leakage)


def record_file(directory, relative):
    """Read retained relative paths only; reject escapes and symlinks."""
    if not isinstance(relative, str) or "\\" in relative:
        raise ValueError("Invalid record path")
    candidate = directory / relative
    if Path(relative).is_absolute() or ".." in Path(relative).parts:
        raise ValueError("Record path escapes its directory")
    if not candidate.resolve().is_relative_to(directory.resolve()):
        raise ValueError("Record path escapes its directory")
    if any(p.is_symlink() for p in (candidate, *candidate.parents) if p != directory.parent):
        raise ValueError("Record symlink is not supported")
    return candidate
