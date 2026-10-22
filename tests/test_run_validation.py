"""Infrastructure checks using dummy processes; no Kyber execution or Git calls."""

import contextlib
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import run_validation as runner


@unittest.skipUnless(sys.platform == "linux", "Linux process-group checks")
class StepTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="kyber-runner-check-")
        self.addCleanup(self.temporary.cleanup)
        self.run_dir = Path(self.temporary.name)
        (self.run_dir / "raw").mkdir()
        self.manifest = {"steps": []}
        self.environment = {"PATH": "/usr/bin:/bin", "LC_ALL": "C"}

    def step(self, code, timeout=5):
        return runner.run_step(
            self.run_dir, self.manifest, "dummy",
            [sys.executable, "-c", code], self.run_dir,
            self.environment, timeout,
        )

    def test_success_preserves_output_and_hashes(self):
        self.assertTrue(self.step("import sys; print('ok'); print('note', file=sys.stderr)"))
        step = self.manifest["steps"][0]
        self.assertEqual(step["exit_code"], 0)
        self.assertEqual((self.run_dir / step["stdout"]).read_text(), "ok\n")
        self.assertEqual((self.run_dir / step["stderr"]).read_text(), "note\n")
        self.assertEqual(step["stdout_sha256"],
                         runner.metadata.sha256(self.run_dir / step["stdout"]))
        self.assertEqual(json.loads((self.run_dir / "manifest.json").read_text()),
                         self.manifest)

    def test_nonzero_exit_is_failure(self):
        self.assertFalse(self.step("import sys; print('failure'); sys.exit(7)"))
        step = self.manifest["steps"][0]
        self.assertEqual(step["exit_code"], 7)
        self.assertEqual(step["status"], "failed")
        self.assertIn("failure", (self.run_dir / step["stdout"]).read_text())

    def test_timeout_is_not_pass(self):
        self.assertFalse(self.step("import time; time.sleep(5)", timeout=0.05))
        step = self.manifest["steps"][0]
        self.assertEqual(step["status"], "timed-out")
        self.assertLess(step["exit_code"], 0)

    def test_missing_executable_preserves_failure(self):
        result = runner.run_step(
            self.run_dir, self.manifest, "missing",
            [str(self.run_dir / "nonexistent")], self.run_dir,
            self.environment, 5,
        )
        self.assertFalse(result)
        self.assertEqual(self.manifest["steps"][0]["status"], "launch-error")

    def test_existing_raw_output_is_not_overwritten(self):
        original = self.run_dir / "raw" / "dummy.stdout.log"
        original.write_text("preserved")
        self.assertFalse(self.step("print('replacement')"))
        self.assertEqual(original.read_text(), "preserved")

    def test_keyboard_interrupt_saves_step(self):
        process = Mock(returncode=-9)
        process.wait.side_effect = KeyboardInterrupt
        with patch.object(runner.subprocess, "Popen", return_value=process):
            with patch.object(runner, "stop_process_group") as stop:
                with self.assertRaises(KeyboardInterrupt):
                    self.step("pass")
        stop.assert_called_once_with(process)
        self.assertEqual(self.manifest["steps"][0]["status"], "interrupted")

    def test_termination_handler_uses_interrupt_path(self):
        with self.assertRaises(KeyboardInterrupt):
            runner.interrupt_requested(15, None)


class SourceTests(unittest.TestCase):
    def test_changed_source_is_rejected(self):
        with tempfile.TemporaryDirectory(prefix="kyber-source-check-") as name:
            root = Path(name)
            baseline, upstream = root / "baseline", root / "upstream"
            baseline.mkdir()
            upstream.mkdir()
            (baseline / "sample.h").write_text("/* candidate */")
            (upstream / "sample.h").write_text("/* reference */")
            with patch.object(runner, "BASELINE", baseline):
                with patch.object(runner, "UPSTREAM_REF", upstream):
                    with self.assertRaisesRegex(RuntimeError, "differs"):
                        runner.source_snapshot()

    def test_missing_source_is_rejected(self):
        with tempfile.TemporaryDirectory(prefix="kyber-source-check-") as name:
            root = Path(name)
            baseline, upstream = root / "baseline", root / "upstream"
            baseline.mkdir()
            upstream.mkdir()
            (upstream / "sample.h").write_text("/* reference */")
            with patch.object(runner, "BASELINE", baseline):
                with patch.object(runner, "UPSTREAM_REF", upstream):
                    with self.assertRaisesRegex(RuntimeError, "file sets"):
                        runner.source_snapshot()


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="kyber-workflow-check-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.run_dir = self.root / "results" / "EXP-000" / "RUN-0001"
        self.run_dir.mkdir(parents=True)
        self.baseline = self.root / "baseline"
        self.baseline.mkdir()
        self.compiler = self.root / "dummy-compiler"
        self.compiler.write_text("test double; never executed")
        self.snapshot = {
            "experiment_id": "EXP-000", "run_id": "RUN-0001",
            "provenance": {"source_commit": "test-double"},
            "environment": {"available_compiler": {
                "path": str(self.compiler),
                "sha256": runner.metadata.sha256(self.compiler),
            }},
        }
        (self.run_dir / "metadata.json").write_text(json.dumps(self.snapshot))
        self.failed_label = None
        self.interrupted_label = None
        self.state_checks = Mock()
        self.labels = []

    def fake_step(self, run_dir, manifest, label, argv, cwd, environment, timeout):
        self.labels.append(label)
        passed = label != self.failed_label
        status = "completed" if passed else "failed"
        if label == self.interrupted_label:
            status = "interrupted"
        manifest["steps"].append({"label": label, "status": status})
        if status == "interrupted":
            raise KeyboardInterrupt
        if label.startswith("build-") and passed:
            Path(argv[-1]).write_bytes(b"dummy executable; never executed")
        return passed

    def execute(self):
        with contextlib.ExitStack() as stack:
            stack.enter_context(patch.object(runner, "ROOT", self.root))
            stack.enter_context(patch.object(runner, "BASELINE", self.baseline))
            stack.enter_context(patch.object(runner.metadata, "git", return_value=""))
            stack.enter_context(patch.object(
                runner, "check_source_state", self.state_checks))
            stack.enter_context(patch.object(runner, "run_step", self.fake_step))
            stack.enter_context(contextlib.redirect_stdout(io.StringIO()))
            result = runner.execute_validation(
                self.run_dir, self.snapshot, {"fixture": "test-double"}, 5,
            )
        manifest = json.loads((self.run_dir / "manifest.json").read_text())
        return result, manifest

    def test_all_parameters_and_evidence_categories(self):
        result, manifest = self.execute()
        self.assertEqual(result, 0)
        self.assertEqual(self.labels, [
            "build-512", "test-512", "build-768", "test-768",
            "build-1024", "test-1024",
        ])
        self.assertEqual(manifest["status"], "completed")
        self.assertEqual(manifest["provenance_recheck"], "pass")
        self.assertFalse(manifest["benchmark_executed"])
        self.assertEqual(set(manifest["checks"]["upstream_functional"].values()), {"pass"})
        self.assertEqual(manifest["checks"]["arithmetic_safety"], "not-run")
        self.assertEqual(manifest["checks"]["timing_behaviour"], "not-run")

    def test_build_failure_stops_before_tests(self):
        self.failed_label = "build-512"
        result, manifest = self.execute()
        self.assertEqual(result, 1)
        self.assertEqual(self.labels, ["build-512"])
        self.assertEqual(set(manifest["checks"]["upstream_functional"].values()),
                         {"not-run"})

    def test_functional_failure_stops_remaining_parameters(self):
        self.failed_label = "test-512"
        result, manifest = self.execute()
        self.assertEqual(result, 1)
        self.assertEqual(self.labels, ["build-512", "test-512"])
        self.assertEqual(manifest["checks"]["upstream_functional"]["512"], "fail")
        self.assertEqual(manifest["checks"]["upstream_functional"]["768"], "not-run")

    def test_interrupted_test_is_inconclusive(self):
        self.interrupted_label = "test-512"
        result, manifest = self.execute()
        self.assertEqual(result, 1)
        self.assertEqual(manifest["status"], "interrupted")
        self.assertEqual(manifest["checks"]["upstream_functional"]["512"], "inconclusive")

    def test_changed_provenance_invalidates_completed_tests(self):
        self.state_checks.side_effect = [None, RuntimeError("source changed")]
        result, manifest = self.execute()
        self.assertEqual(result, 1)
        self.assertEqual(manifest["status"], "failed")
        self.assertNotEqual(manifest["provenance_recheck"], "pass")
        self.assertEqual(manifest["error"], "source changed")

    def test_setup_failure_has_manifest(self):
        (self.run_dir / "build").mkdir()
        result, manifest = self.execute()
        self.assertEqual(result, 1)
        self.assertEqual(manifest["status"], "failed")
        self.assertEqual(self.labels, [])


if __name__ == "__main__":
    unittest.main()
