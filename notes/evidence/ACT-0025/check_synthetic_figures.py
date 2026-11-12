#!/usr/bin/env python3
"""Synthetic rendering check only; produces no EXP-010 research result."""
import hashlib
import json
from pathlib import Path
import random
import sys
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(ROOT / "scripts"), str(ROOT / "analysis")]
import analyse_random_seed_comparison as analysis
import build_random_seed_figures as figures
import random_seed_common as common

plan = common.load_plan(common.load_protocol())
rng = random.Random(61723)  # Graph-test values only; never experimental seed generation.
loaded = []
for session in range(1, 6):
    rows = []
    for block, k, position, variant, seed in common.schedule(plan, session):
        for op_index, operation in enumerate(figures.OPS):
            effect = 10 + common.PARAMETERS.index(k) * 3 + op_index * 2 + rng.uniform(-1.5, 1.5)
            if variant == "exp005":
                effect += 3 if operation == "keygen" else (-.3 if k == 1024 else .4)
            if block == 1 and session == 1 and k == 512 and operation == "keygen" and variant == "exp003":
                effect = -5  # Ensure negative values are retained and visible.
            median = 20000 * (1 + block / 100) * (1 if variant == "baseline" else 1 - effect / 100)
            rows.append(dict(parameter_set=f"Kyber{k}", operation=operation, block=block, variant=variant,
                             samples=1000, fixture_seed=seed, position=position, median_ns=median))
    pairs, estimates = analysis.derive(rows, 12, session)
    manifest = dict(session=session, protocol={}, source_file_sha256={}, support_file_sha256={},
                    compiler={}, build_flags=[], tool_sha256={})
    loaded.append((manifest, pairs, estimates))
with patch.object(analysis, "read_run", side_effect=lambda p: loaded[int(p.name)]):
    _, pairs, _, totals, boxes = analysis.combine([Path(str(i)) for i in range(5)])
assert len(pairs) == 1620 and len(boxes) == 27
assert min(r["improvement_pct"] for r in pairs) < 0
figures.plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10,
                           "svg.hashsalt": "kyber-exp010-dot-box-v1", "pdf.fonttype": 42})
directories = [Path("/tmp/kyber-exp010-synthetic-plots"), Path("/tmp/kyber-exp010-synthetic-plots-copy")]
for directory in directories:
    directory.mkdir(exist_ok=False)
    figures.plot(directory, pairs, totals, boxes, development=True)
    figures.plot(directory, pairs, totals, boxes, direct=True, development=True)
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
files = {p.name: sha(p) for p in directories[0].iterdir()}
assert files == {p.name: sha(p) for p in directories[1].iterdir()}
report = dict(development_only=True, input="synthetic values; not measured results",
              plotted_points_original_reference=1080, plotted_points_direct=540,
              negative_values_included=True, reproduced_files=len(files), byte_identical=True,
              matplotlib=figures.matplotlib.__version__, outputs=files)
print(json.dumps(report))
(directories[0] / "plot-check.json").write_text(json.dumps(report, indent=2) + "\n")
