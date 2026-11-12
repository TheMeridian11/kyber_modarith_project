#!/usr/bin/env python3
"""EXP-010 plan/analysis tests and an explicitly non-formal integration smoke."""
import argparse
import collections
import copy
import hashlib
import itertools
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import analyse_random_seed_comparison as analysis
import collect_run_metadata as metadata
import random_seed_common as common
import run_random_seed_comparison as runner
import run_validation as validation


def process_summaries(session=1, effects=None):
    plan = common.load_plan(common.load_protocol())
    rows = []
    for block, k, position, variant, seed in common.schedule(plan, session):
        effect = (effects or [10.0] * 12)[block - 1]
        factor = {"baseline": 1.0, "exp003": 1.0 - effect / 100, "exp005": .75}[variant]
        for operation in ("keygen", "encap", "decap"):
            rows.append(dict(parameter_set=f"Kyber{k}", operation=operation, block=block,
                             variant=variant, samples=1000, fixture_seed=seed, position=position,
                             median_ns=1000 * block * factor))
    return rows


def analysis_fixture(directory):
    """Temporary synthetic metadata/order fixture; never a new measured run.

    Reuses old raw durations to exercise parsing at the real matrix size. Seed
    labels/order are deliberately substituted for this test only. The fixture
    is deleted by TemporaryDirectory and must never enter results/.
    """
    original = ROOT / "results/EXP-009/RUN-0001"
    m = json.loads((original / "manifest.json").read_text())
    p = common.load_protocol()
    plan = common.load_plan(p)
    m.update(protocol=p, record_type=p["record_type"], experiment_id="EXP-010", run_id="SYNTHETIC-UNIT-FIXTURE",
             seed_plan_sha256=p["seed_plan_sha256"], development_only=False,
             support_file_sha256={name: metadata.sha256(ROOT / name) for name in common.SUPPORT})
    snapshot = json.loads((original / "metadata.json").read_text())
    snapshot.update(experiment_id="EXP-010", run_id=m["run_id"], variant="random-seed-three-way")
    (directory / "metadata.json").write_text(json.dumps(snapshot) + "\n")
    m["metadata_sha256"] = metadata.sha256(directory / "metadata.json")
    (directory / "seed-plan.json").write_bytes(common.PLAN.read_bytes())
    (directory / "raw").mkdir()
    (directory / "derived").mkdir()
    old_steps = {s["label"]: s for s in m["steps"]}
    old_data = {(d["block"], d["parameter"], d["variant"]): d for d in m["datasets"]}
    m["steps"] = [s for s in m["steps"] if not s["label"].startswith("timing-")]
    for step in m["steps"]:
        for stream in ("stdout", "stderr"):
            shutil.copyfile(original / step[stream], directory / step[stream])
    m["datasets"] = []
    summaries = []
    for block, k, position, variant, seed in common.schedule(plan, 1):
        label = f"timing-{variant}-{k}-block-{block:04d}"
        step = copy.deepcopy(old_steps[label])
        dataset = copy.deepcopy(old_data[(block, k, variant)])
        step["argv"][-1] = seed
        shutil.copyfile(original / step["stdout"], directory / step["stdout"])
        lines = (original / step["stderr"]).read_text().splitlines()
        (directory / step["stderr"]).write_text("\n".join("seed=" + seed if line.startswith("seed=") else line for line in lines) + "\n")
        step["stderr_sha256"] = metadata.sha256(directory / step["stderr"])
        dataset.update(position=position, fixture_seed=seed)
        m["steps"].append(step)
        m["datasets"].append(dataset)
        for row in runner.timing.summarise_csv(directory / step["stdout"], k, 1000, block):
            row["block"] = row.pop("repetition")
            summaries.append(dict(variant=variant, position=position, fixture_seed=seed, **row))
    pairs, estimates = analysis.derive(summaries, 12, 1)
    for name, rows in (("process-summary", summaries), ("paired-comparison", pairs), ("comparison", estimates)):
        entry = m["derived"][name]
        (directory / entry["path"]).write_bytes(analysis.csv_bytes(rows))
        entry["sha256"] = metadata.sha256(directory / entry["path"])
    (directory / "manifest.json").write_text(json.dumps(m) + "\n")
    return m


class RandomSeedTests(unittest.TestCase):
    def test_saved_plan_unique_uint64_and_balanced(self):
        p = common.load_protocol()
        plan = common.load_plan(p)
        seeds = [seed for s in plan["sessions"] for seed in s["seeds"]]
        self.assertEqual(len(set(seeds)), 60)
        self.assertTrue(all(0 <= int(seed) < 2**64 for seed in seeds))
        for session in range(1, 6):
            schedule = list(common.schedule(plan, session))
            self.assertEqual(len(schedule), 108)
            for k in common.PARAMETERS:
                selected = [row for row in schedule if row[1] == k]
                self.assertEqual(collections.Counter((r[3], r[2]) for r in selected),
                                 collections.Counter({(v, pos): 4 for v in common.VARIANTS for pos in (1, 2, 3)}))
                for block in range(1, 13):
                    self.assertEqual(len({r[4] for r in selected if r[0] == block}), 1)
        self.assertEqual(common.selected_source_hashes(), common.accepted_context()[1]["exp005"])

    def test_reject_duplicate_out_of_range_or_rounded_seeds(self):
        plan = common.load_plan(common.load_protocol())
        for bad in (plan["sessions"][1]["seeds"][0], str(2**64), -1, 1.2, "01", "1e10"):
            changed = copy.deepcopy(plan)
            changed["sessions"][0]["seeds"][0] = bad
            with self.assertRaises(ValueError):
                common.validate_plan(changed)

    def test_reject_unbalanced_order_or_missing_session(self):
        plan = common.load_plan(common.load_protocol())
        changed = copy.deepcopy(plan)
        changed["sessions"].pop()
        with self.assertRaises(ValueError):
            common.validate_plan(changed)
        changed = copy.deepcopy(plan)
        changed["sessions"][0]["orders"]["512"] = [["baseline", "exp003", "exp005"]] * 12
        with self.assertRaises(ValueError):
            common.validate_plan(changed)

    def test_plan_hash_and_budget_are_enforced(self):
        p = common.load_protocol()
        p["iterations"] = 999
        with self.assertRaises(ValueError):
            common.validate_protocol(p)
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "plan.json"
            path.write_bytes(common.PLAN.read_bytes() + b" ")
            with self.assertRaises(ValueError):
                common.load_plan(common.load_protocol(), path)

    def test_effects_are_paired_and_adverse_effects_retained(self):
        pairs, estimates = analysis.derive(process_summaries(effects=[-10.0] * 6 + [30.0] * 6), 12, 1)
        row = estimates[0]
        self.assertAlmostEqual(row["median_paired_improvement_pct"], 10)
        self.assertEqual(row["negative_blocks"], 6)
        self.assertEqual(row["positive_blocks"], 6)
        ratio = 100 * (1 - row["candidate_median_of_medians_ns"] / row["reference_median_of_medians_ns"])
        self.assertNotAlmostEqual(ratio, 10)
        self.assertEqual(len(pairs), 324)

    def test_reject_unmatched_or_missing_observations(self):
        rows = process_summaries()
        for changed in (rows[:-1], rows + [rows[0]]):
            with self.assertRaises(ValueError):
                analysis.derive(changed, 12, 1)
        for key, value in (("fixture_seed", "0"), ("samples", 999), ("median_ns", 0)):
            changed = copy.deepcopy(rows)
            changed[0][key] = value
            with self.assertRaises(ValueError):
                analysis.derive(changed, 12, 1)

    def test_session_summary_is_not_pooled_box_median(self):
        effects = [[0] * 12, [0] * 12, [0] * 6 + [100] * 6, [90] * 12, [90] * 12]
        # Avoid zero candidate medians while preserving a distinct pooled/session result.
        effects[2] = [0] * 6 + [80] * 6
        loaded = []
        for session, values in enumerate(effects, 1):
            pairs, rows = analysis.derive(process_summaries(session, values), 12, session)
            m = dict(session=session, protocol={}, source_file_sha256={}, support_file_sha256={},
                     compiler={}, build_flags=[], tool_sha256={})
            loaded.append((m, pairs, rows))
        with patch.object(analysis, "read_run", side_effect=lambda p: loaded[int(p.name)]):
            _, pairs, rows, totals, boxes = analysis.combine([Path(str(i)) for i in range(5)])
            self.assertEqual(len(pairs), 1620)
            self.assertEqual(len(rows), 135)
            self.assertAlmostEqual(totals[0]["median_session_improvement_pct"], 40)
            self.assertAlmostEqual(boxes[0]["pooled_block_median_pct"], 40)
            # Change the middle session so its own median differs from pooled middle values.
            loaded[2] = (loaded[2][0], *analysis.derive(process_summaries(3, [10] * 7 + [80] * 5), 12, 3))
            _, _, _, totals, boxes = analysis.combine([Path(str(i)) for i in range(5)])
            self.assertAlmostEqual(totals[0]["median_session_improvement_pct"], 10)
            self.assertAlmostEqual(boxes[0]["pooled_block_median_pct"], 10)
            # Low values in both high-median sessions move the pooled median only.
            loaded[3] = (loaded[3][0], *analysis.derive(process_summaries(4, [-20] * 5 + [90] * 7), 12, 4))
            loaded[4] = (loaded[4][0], *analysis.derive(process_summaries(5, [-20] * 5 + [90] * 7), 12, 5))
            _, _, _, totals, boxes = analysis.combine([Path(str(i)) for i in range(5)])
            self.assertAlmostEqual(totals[0]["median_session_improvement_pct"], 10)
            self.assertAlmostEqual(boxes[0]["pooled_block_median_pct"], 0)
            with self.assertRaises(ValueError):
                analysis.combine([Path(str(i)) for i in (0, 0, 2, 3, 4)])
            loaded[4][0]["compiler"] = {"changed": True}
            with self.assertRaises(ValueError):
                analysis.combine([Path(str(i)) for i in range(5)])

    def test_failures_and_development_runs_cannot_be_analysed(self):
        with tempfile.TemporaryDirectory() as d:
            directory = Path(d)
            for value in (dict(development_only=True), dict(status="failed"), dict(status="interrupted")):
                (directory / "manifest.json").write_text(json.dumps(value))
                with self.assertRaises(ValueError):
                    analysis.read_run(directory)

    def test_completed_session_cannot_be_replaced(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            record = root / "results/EXP-010/RUN-0001"
            record.mkdir(parents=True)
            (record / "manifest.json").write_text(json.dumps(dict(status="completed", session=1)))
            with patch.object(runner, "ROOT", root):
                with self.assertRaises(RuntimeError):
                    runner.refuse_completed_session(1)
                runner.refuse_completed_session(2)

    def test_record_paths_cannot_escape_run(self):
        with tempfile.TemporaryDirectory() as d:
            for value in ("../outside", "/outside", "raw\\outside"):
                with self.assertRaises(ValueError):
                    common.record_file(Path(d), value)

    def test_full_raw_reanalysis_and_tamper_rejection(self):
        with tempfile.TemporaryDirectory(prefix="synthetic-exp010-analysis-") as d:
            directory = Path(d)
            original = analysis_fixture(directory)
            _, pairs, estimates = analysis.read_run(directory)
            self.assertEqual(len(pairs), 324)
            self.assertEqual(len(estimates), 27)
            for field in ("fixture_seed", "position"):
                changed = copy.deepcopy(original)
                changed["datasets"][0][field] = "0" if field == "fixture_seed" else 9
                (directory / "manifest.json").write_text(json.dumps(changed))
                with self.assertRaises(ValueError):
                    analysis.read_run(directory)
            changed = copy.deepcopy(original)
            changed["datasets"][0], changed["datasets"][1] = changed["datasets"][1], changed["datasets"][0]
            (directory / "manifest.json").write_text(json.dumps(changed))
            with self.assertRaises(ValueError):
                analysis.read_run(directory)
            (directory / "manifest.json").write_text(json.dumps(original))
            raw = directory / original["datasets"][0]["path"]
            saved = raw.read_bytes()
            raw.write_bytes(saved + b"\n")
            with self.assertRaises(ValueError):
                analysis.read_run(directory)
            raw.write_bytes(saved)
            changed = copy.deepcopy(original)
            entry = changed["derived"]["comparison"]
            path = directory / entry["path"]
            path.write_bytes(path.read_bytes() + b"\n")
            entry["sha256"] = metadata.sha256(path)
            (directory / "manifest.json").write_text(json.dumps(changed))
            with self.assertRaises(ValueError):
                analysis.read_run(directory)


def integration_smoke(output):
    """Real builds/assembly/round trips; Git checks stubbed and no formal results."""
    import os
    from types import SimpleNamespace
    output.mkdir(parents=True, exist_ok=False)
    p, plan = runner.preflight("gcc", 0)
    p = dict(p, iterations=8, warmup=2)
    snapshot = json.loads((ROOT / "results/EXP-009/RUN-0001/metadata.json").read_text())
    snapshot["development_only"] = True
    (output / "metadata.json").write_text(json.dumps(snapshot, indent=2) + "\n")
    cached = ROOT / "results/EXP-009/RUN-0001/build/exp003-source"
    sources = {"exp003": cached, "exp005": ROOT / "implementation/kyber-optimised-ref"}

    def restore(directory, commit, files):
        variant = "exp003" if directory.name == "exp003-source" else "exp005"
        directory.mkdir()
        for name, digest in files.items():
            source = sources[variant] / name
            if metadata.sha256(source) != digest:
                raise ValueError("Cached development source does not match the reviewed pin")
            dest = directory / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, dest)

    def source_check(commit, expected):
        if validation.source_snapshot() != expected:
            raise ValueError("Development baseline changed")

    args = SimpleNamespace(run="DEVELOPMENT", session=1, cpu=0,
                           session_note="Development smoke only: 8 measured and 2 warm-up exchanges; not research evidence")
    affinity = sorted(os.sched_getaffinity(0))
    try:
        os.sched_setaffinity(0, {0})
        with patch.object(common, "load_protocol", return_value=p), \
             patch.object(metadata, "git", return_value="development-only-stub"), \
             patch.object(validation, "check_source_state", side_effect=source_check), \
             patch.object(runner.historical, "restore", side_effect=restore):
            code = runner.execute(output, snapshot, p, plan, args, affinity)
        if code:
            raise RuntimeError("Development smoke failed; inspect retained manifest")
        with unittest.TestCase().assertRaises(ValueError):
            analysis.read_run(output)
    finally:
        os.sched_setaffinity(0, set(affinity))
    manifest = json.loads((output / "manifest.json").read_text())
    report = dict(development_only=True, formal_measurements=False, builds=len(manifest["executables"]),
                  assembly_bodies=len(manifest["assembly"]), processes=len(manifest["datasets"]),
                  measured_exchanges=108 * 8, warmup_exchanges=108 * 2,
                  git_commands_executed=False, historical_restore="hash-verified cached source copied in temporary directory",
                  formal_analyser_rejects_development=True,
                  manifest_sha256=metadata.sha256(output / "manifest.json"))
    (output / "smoke-review.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report))


if __name__ == "__main__":
    if "--integration-smoke" in sys.argv:
        parser = argparse.ArgumentParser()
        parser.add_argument("--integration-smoke", action="store_true")
        parser.add_argument("--output", type=Path, required=True)
        integration_smoke(parser.parse_args().output)
    else:
        unittest.main()
