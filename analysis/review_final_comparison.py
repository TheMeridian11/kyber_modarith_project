#!/usr/bin/env python3
"""Audit three frozen EXP-009 sessions and materialise the closing evidence."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import re
import statistics
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "analysis"), str(ROOT / "scripts")]
import review_final_session as session_audit
import analyse_final_comparison as final_analysis


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def csv_rows(path):
    with Path(path).open(newline="") as stream:
        return list(csv.DictReader(stream))


def save_json(path, value):
    with path.open("x") as stream:
        json.dump(value, stream, indent=2, sort_keys=True)
        stream.write("\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "notes/evidence/ACT-0020")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    runs = [ROOT / f"results/EXP-009/RUN-{i:04d}" for i in (1, 2, 3)]
    reviews = [session_audit.audit(run) for run in runs]
    old_review = ROOT / "notes/evidence/ACT-0019/exp-009-run-0001-review.json"
    assert reviews[0] == json.loads(old_review.read_text())
    loaded, estimates, combined = final_analysis.combine(runs)
    # Check the already-written aggregate artifacts against these raw reconstructions.
    aggregate_dir = ROOT / "analysis/final-comparison-EXP-009"
    provenance = json.loads((aggregate_dir / "provenance.json").read_text())
    assert provenance["analysis_script_sha256"] == sha(ROOT / "scripts/analyse_final_comparison.py")
    for name, digest in provenance["inputs"].items():
        assert sha(ROOT / name) == digest
    for name, digest in provenance["outputs"].items():
        assert sha(aggregate_dir / name) == digest
    for filename, expected in (("session-effects.csv", estimates), ("three-session-effects.csv", combined)):
        assert csv_rows(aggregate_dir / filename) == [{k: str(v) for k, v in row.items()} for row in expected]
    contrasts = []
    for total in combined:
        group = [row for row in estimates if all(row[k] == total[k] for k in ("reference", "candidate", "parameter_set", "operation"))]
        assert len(group) == 3
        values = [row["median_paired_improvement_pct"] for row in group]
        assert (statistics.median(values), min(values), max(values)) == tuple(total[k] for k in
               ("median_session_improvement_pct", "min_session_improvement_pct", "max_session_improvement_pct"))
        contrasts.append(total | dict(session_estimates_pct=values,
                                      positive_blocks=sum(row["positive_blocks"] for row in group),
                                      negative_blocks=sum(row["negative_blocks"] for row in group)))
    # Reuse the prior reviewed keygen frame facts only after exact body matching.
    prior_path = ROOT / "notes/evidence/ACT-0013/exp-005-run-0001-review.json"
    prior = json.loads(prior_path.read_text())
    keygen = []
    for parameter in (512, 768, 1024):
        for variant, previous in (("exp003", "staged-invntt"), ("exp005", "raw-error-ntt")):
            key = f"{variant}-{parameter}/pqcrystals_kyber{parameter}_ref_indcpa_keypair_derand"
            bodies = [m["assembly"][key]["normalised"] for m, _ in loaded]
            assert bodies[0] == bodies[1] == bodies[2] == prior["assembly"][str(parameter)][previous]["indcpa_keypair_derand"]
            body = bodies[0]
            facts = prior["keygen_assembly_facts"][str(parameter)][previous]
            reserve = sum(int(match.group(1), 16) for line in body["instructions"]
                          if (match := re.search(r": sub \$0x([0-9a-f]+),%rsp$", line)))
            saved = 8 * sum(": push " in line for line in body["instructions"])
            assert reserve == facts["stack_reservation_bytes"] and saved == facts["saved_register_bytes"]
            assert reserve + saved == facts["local_stack_excluding_entry_return_and_callees"]
            assert facts["stack_canary"] and facts["endbr64"]
            assert any("%fs:0x28" in line for line in body["instructions"]) and any("<__stack_chk_fail@plt>" in line for line in body["instructions"])
            keygen.append(dict(parameter_set=f"Kyber{parameter}", variant=variant, body_bytes=body["size_bytes"],
                               stack_reservation_bytes=reserve, saved_register_bytes=saved,
                               local_stack_bytes=reserve + saved, stack_canary_present=True, endbr64_present=True,
                               stack_page_probes=facts["stack_page_probe_count"]))
    # Source/body contrasts establish which earlier changes are inherited.
    sources = loaded[0][0]["source_file_sha256"]
    changed = sorted(n for n in sources["exp003"] if sources["exp003"][n] != sources["exp005"][n])
    assert changed == ["indcpa.c"]
    for parameter in (512, 768, 1024):
        for function in ("basemul", "polyvec_basemul_acc_montgomery", "invntt", "ntt", "poly_ntt", "poly_tomont",
                         "poly_reduce", "poly_add", "indcpa_dec", "montgomery_reduce", "barrett_reduce"):
            symbol = f"pqcrystals_kyber{parameter}_ref_{function}"
            assert loaded[0][0]["assembly"][f"exp003-{parameter}/" + symbol]["normalised"] == loaded[0][0]["assembly"][f"exp005-{parameter}/" + symbol]["normalised"]
        for variant in ("exp003", "exp005"):
            key = f"{variant}-{parameter}/pqcrystals_kyber{parameter}_ref_polyvec_basemul_acc_montgomery"
            assert not any("__stack_chk_fail" in line for line in loaded[0][0]["assembly"][key]["normalised"]["instructions"])
    session_reports = {}
    for index, review in enumerate(reviews, 1):
        if index == 1:
            session_reports[f"RUN-{index:04d}"] = dict(path=old_review.relative_to(ROOT).as_posix(), sha256=sha(old_review), rechecked=True)
            continue
        review["activity_id"] = "ACT-0020"
        review["audit_driver_sha256"] = sha(__file__)
        review["limitations"][0] = "Individual-session audit; the combined review supplies the three-session interpretation."
        target = args.output / f"exp-009-run-{index:04d}-review.json"
        save_json(target, review)
        session_reports[f"RUN-{index:04d}"] = dict(file=target.name, sha256=sha(target), rechecked=True)
    summary = dict(activity_id="ACT-0020", all_three_sessions_accepted=True, predeclared_collection_complete=True,
                   record_type="closing-three-session-review", audit_driver_sha256=sha(__file__),
                   per_session_audit_code_sha256=sha(ROOT / "analysis/review_final_session.py"),
                   source_commits=[m["source_commit"] for m, _ in loaded],
                   manifest_sha256={run.relative_to(ROOT).as_posix(): sha(run / "manifest.json") for run in runs},
                   session_reviews=session_reports, protocol_and_support_identical=True,
                   compiler_tools_sources_and_flags_identical=True,
                   coverage={k: sum(r["coverage"][k] for r in reviews) for k in reviews[0]["coverage"]},
                   aggregate_outputs={p.name: sha(p) for p in sorted(aggregate_dir.iterdir()) if p.is_file()},
                   contrasts=contrasts, keygen_code_and_local_stack=keygen,
                   inherited_tradeoff="Both candidates retain the general-dot body without its former local array/canary; keygen canaries remain present.",
                   previous_keygen_review_sha256=sha(prior_path),
                   source_difference_exp003_to_exp005=changed,
                   limitations=["Three separate invocations on one WSL host; no independence, population significance or portability guarantee.",
                                "Unknown manual power/background/physical-core conditions and unrecorded break duration are not imputed.",
                                "Session ranges are descriptive, not confidence intervals; inner timings are not independent replicates.",
                                "Ordinary performance data add no new leakage finding; dedicated security claims retain their original scope.",
                                "Candidate selection is a documented workload-sensitive interpretation, not an automatic aggregate score."])
    save_json(args.output / "exp-009-three-session-review.json", summary)
    print(json.dumps({"accepted_sessions": 3, "duration_rows": summary["coverage"]["duration_rows"],
                      "assembly_bodies": summary["coverage"]["assembly_bodies"], "contrast_groups": len(contrasts),
                      "unchanged_support": True, "keygen_tradeoff_rows": len(keygen)}))


if __name__ == "__main__":
    main()
