#!/usr/bin/env python3
"""Independently audit EXP-008 streams with NumPy; never modify a run."""
import argparse
import gzip
import hashlib
import itertools
import json
import math
import sys
import tarfile
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from run_incremental_comparison import assembly_record

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def audit(run):
    m = json.loads((run / "manifest.json").read_text())
    p = m["protocol"]
    assert m["status"] == "completed" and m["provenance_recheck"] == "pass"
    assert p == json.loads((ROOT / "tests/timing_leakage_protocol.json").read_text())
    assert sha(run / "metadata.json") == m["metadata_sha256"]
    snapshot = json.loads((run / "metadata.json").read_text())
    assert snapshot["provenance"]["source_commit"] == m["source_commit"]
    for name, digest in {**p["accepted_inputs"], **p["reference_sha256"], **m["support_file_sha256"]}.items():
        assert sha(ROOT / name) == digest, name
    for name, digest in {**m["tool_sha256"], m["compiler"]["path"]: m["compiler"]["sha256"]}.items():
        assert sha(name) == digest, name
    for exe in m["executables"].values():
        assert sha(run / exe["path"]) == exe["sha256"]
    assert len(m["executables"]) == 9
    for variant, files in m["source_file_sha256"].items():
        directory = ROOT / "implementation/kyber-baseline-ref" if variant == "baseline" else run / "build" / (variant + "-source")
        assert len(files) == 35
        for name, digest in files.items():
            assert sha(directory / name) == digest, (variant, name)
    steps = {s["stdout"]: s for s in m["steps"]}
    assert len(steps) == len(m["steps"]) == 513
    raw_hashes = {}
    for s in m["steps"]:
        assert s["status"] == "completed" and s["exit_code"] == 0
        for stream in ("stdout", "stderr"):
            raw_hashes[s[stream]] = sha(run / s[stream])
            assert raw_hashes[s[stream]] == s[stream + "_sha256"]
    assert set(raw_hashes) == {f.relative_to(run).as_posix() for f in (run / "raw").iterdir()}
    ref = json.loads((ROOT / "notes/evidence/ACT-0017/exp-007-run-0001-review.json").read_text())["assembly_normalised"]
    archive = ROOT / "notes/evidence/ACT-0017/timing-leakage-final-smoke.tar.gz"
    with tarfile.open(archive) as tar:
        development = json.load(tar.extractfile("run/manifest.json"))
    production = wrappers = 0
    for key, entry in m["assembly"].items():
        tag, symbol = key.split("/", 1)
        observed = assembly_record((run / entry["path"]).read_text(), symbol)
        assert observed == entry["normalised"] == development["assembly"][key]["normalised"], key
        if symbol.startswith("pqcrystals_"):
            assert observed == ref[key.replace("exp003-", "exp005-")], key
            production += 1
        else:
            wrappers += 1
    assert (production, wrappers) == (99, 81)
    dtype = np.dtype([("ticks", "<u8"), ("a0", "<u4"), ("a1", "<u4"), ("class", "u1")])
    expected = {(v, k, rep, path, prof) for v, k, rep in itertools.product(p["variants"], (512, 768, 1024), (1, 2))
                for path, prof in [(c, 0) for c in p["controls"]] + list(itertools.product(p["paths"], (0, 1)))}
    seen, rows, discrepancies = set(), [], []
    for cell in m["measurements"]:
        identity = tuple(cell[k] for k in ("variant", "parameter", "repetition", "path", "profile"))
        assert identity in expected and identity not in seen
        seen.add(identity)
        s = steps[cell["raw"]]
        assert cell["raw_sha256"] == s["stdout_sha256"]
        data = gzip.decompress((run / cell["raw"]).read_bytes())
        assert hashlib.sha256(data).hexdigest() == s["uncompressed_stdout_sha256"]
        assert data[:8] == b"KTL00801" and len(data) == 8 + 52000 * 17
        a = np.frombuffer(data, dtype=dtype, offset=8)
        assert np.all(a["class"] <= 1) and np.all(a["class"].reshape(-1, 1000).sum(axis=1) == 500)
        valid = (a["ticks"] > 0) & (a["a0"] == a["a1"])
        excluded = np.flatnonzero(~valid).tolist()
        assert excluded == cell["excluded_indices"]
        cal = np.sort(a["ticks"][:2000][valid[:2000]])
        assert len(cal) >= 1900 and int(cal[math.ceil(.99 * len(cal))-1]) == cell["calibration_p99_reference_only"]
        completion = json.loads((run / s["stderr"]).read_text())
        assert completion == cell["completion"]
        wanted = dict(path=cell["path"], profile=cell["profile"], samples=50000, calibration=2000,
                      warmup=1000, cpu=0, seed=p["seeds"][cell["repetition"]-1])
        assert all(completion[k] == value for k, value in wanted.items())
        assert s["argv"][-5:] == [cell["path"], str(cell["profile"]), "50000", str(wanted["seed"]), "0"]
        assert len(cell["statistics"]) == 6
        computed = []
        for look in p["looks"]:
            q = a[2000:2000+look][valid[2000:2000+look]]
            ticks = q["ticks"].astype(np.float64)
            cutoff = int(np.sort(q["ticks"])[math.ceil(.99 * len(q))-1])
            center = ticks.mean()
            for view in p["views"]:
                mask = ticks <= cutoff if view == "crop99-mean" else np.ones(len(ticks), dtype=bool)
                values = (ticks-center)**2 if view == "second-moment" else ticks
                groups = [values[mask & (q["class"] == c)] for c in (0, 1)]
                n = [len(g) for g in groups]
                means = [float(g.mean()) for g in groups]
                variances = [float(g.var(ddof=1)) for g in groups]
                se = math.sqrt(variances[0]/n[0] + variances[1]/n[1])
                diff = means[0]-means[1]
                t = diff/se if se else (0. if diff == 0 else None)
                out = dict(look=look, view=view, adequate=min(n)>=10000, crop99_cutoff=cutoff,
                           n0=n[0], n1=n[1], mean0=means[0], mean1=means[1], variance0=variances[0],
                           variance1=variances[1], difference0_minus1=diff, standard_error=se,
                           t=t, flag=t is None or abs(t)>10)
                recorded = cell["statistics"][len(computed)]
                for key, value in out.items():
                    if isinstance(value, float):
                        assert math.isclose(value, recorded[key], rel_tol=1e-8, abs_tol=1e-7), (identity, key, value, recorded[key])
                    else:
                        assert value == recorded[key], (identity, key)
                computed.append(out)
                rows.append({**dict(zip(("variant", "parameter", "repetition", "path", "profile"), identity)), **out})
        adequate = all(s["adequate"] for s in computed) and len(excluded) <= .01 * len(a)
        flagged = any(s["flag"] for s in computed)
        assert adequate == cell["adequate"] and flagged == cell["flag"]
        control = cell["path"] in p["controls"]
        control_ok = adequate and (computed[3]["flag"] if cell["path"] == "positive-control" else not flagged) if control else None
        assert cell["control_ok"] == control_ok
    assert seen == expected and len(rows) == 1944
    summary = m["derived"]["summary"]
    assert sha(run / summary["path"]) == summary["sha256"]
    assert json.loads((run / summary["path"]).read_text()) == {"assessment": m["assessment"], "measurements": m["measurements"]}
    targets = [s for s in rows if s["path"] in p["paths"]]
    negatives = [s for s in rows if s["path"] == "negative-control"]
    positives = [s for s in rows if s["path"] == "positive-control" and s["view"] == "raw-mean" and s["look"] == 50000]
    assert not any(s["flag"] for s in targets + negatives)
    assert all(s["flag"] for s in positives) and all(c["adequate"] for c in m["measurements"])
    assert m["assessment"] == "no-difference-detected-within-budget"
    return dict(activity_id="ACT-0018", record_type="independent-timing-leakage-review", accepted_for_closing_comparison=True,
        source_commit=m["source_commit"], manifest_sha256=sha(run/"manifest.json"), metadata_sha256=m["metadata_sha256"],
        review_script_sha256=sha(__file__), numpy_version=np.__version__, comparison_tolerance=dict(relative=1e-8, absolute=1e-7),
        assessment=m["assessment"], checked_steps=513, raw_files=len(raw_hashes), checked_builds=9,
        checked_production_bodies=production, checked_harness_bodies=wrappers, raw_sha256=raw_hashes,
        samples=dict(target_processes=288, control_processes=36, analysis=16200000, calibration=648000,
                     excluded=sum(len(c["excluded_indices"]) for c in m["measurements"]), recomputed_statistics=len(rows)),
        target_max_abs_t=max(targets, key=lambda s: abs(s["t"])), negative_max_abs_t=max(abs(s["t"]) for s in negatives),
        positive_final_raw_abs_t_range=[min(abs(s["t"]) for s in positives), max(abs(s["t"]) for s in positives)],
        target_max_by_variant={v:max(abs(s["t"]) for s in targets if s["variant"]==v) for v in p["variants"]},
        minimum_class_count=min(min(s["n0"],s["n1"]) for s in rows), statistics=rows,
        limitation="No class difference detected within this protocol/budget; not a constant-time proof, full-KEM screen, or cross-platform conclusion.")

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", type=Path, default=ROOT/"results/EXP-008/RUN-0001")
    parser.add_argument("--out", type=Path, required=True)
    args=parser.parse_args()
    result=audit(args.run)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("x") as f:json.dump(result,f,indent=2,allow_nan=False);f.write("\n")
    print(json.dumps({k:v for k,v in result.items() if k not in ("statistics","raw_sha256")},indent=2))
if __name__ == "__main__":main()
