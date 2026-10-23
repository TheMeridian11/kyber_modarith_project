#!/usr/bin/env python3
"""Recompute EXP-009 from raw CSVs; keep blocks and sessions as distinct units."""
import argparse
import csv
import itertools
import json
import statistics
from pathlib import Path
import collect_run_metadata as metadata
import run_timing as timing
VARIANTS = ("baseline", "exp003", "exp005")
COMPARISONS = (("baseline", "exp003"), ("baseline", "exp005"), ("exp003", "exp005"))
PARAMETERS = (512, 768, 1024)

def derive(summaries, blocks, session):
    indexed = {}
    for row in summaries:
        key = (row["parameter_set"], row["operation"], row["block"], row["variant"])
        if key in indexed or row["median_ns"] <= 0 or row["samples"] <= 0:
            raise ValueError("Duplicate/invalid process summary")
        indexed[key] = row
    expected = {(f"Kyber{k}", op, b, v) for k, op, b, v in itertools.product(PARAMETERS, timing.OPERATIONS, range(1, blocks+1), VARIANTS)}
    if set(indexed) != expected:
        raise ValueError("Incomplete or unexpected matrix")
    pairs, aggregate = [], []
    for reference, candidate in COMPARISONS:
        for parameter, op in itertools.product(PARAMETERS, timing.OPERATIONS):
            group = []
            for block in range(1, blocks+1):
                a, b = (indexed[(f"Kyber{parameter}", op, block, v)] for v in (reference, candidate))
                if a["samples"] != b["samples"] or a["fixture_seed"] != b["fixture_seed"]:
                    raise ValueError("Unmatched fixture/sample count")
                group.append(dict(session=session, parameter_set=f"Kyber{parameter}", operation=op,
                    reference=reference, candidate=candidate, block=block, fixture_seed=a["fixture_seed"],
                    reference_position=a["position"], candidate_position=b["position"],
                    reference_median_ns=a["median_ns"], candidate_median_ns=b["median_ns"],
                    speedup=a["median_ns"]/b["median_ns"], improvement_pct=100*(1-b["median_ns"]/a["median_ns"])))
            pairs.extend(group)
            effects = [r["improvement_pct"] for r in group]
            aggregate.append(dict(session=session,parameter_set=f"Kyber{parameter}",operation=op,
                reference=reference,candidate=candidate,blocks=blocks,
                reference_median_of_medians_ns=statistics.median(r["reference_median_ns"] for r in group),
                candidate_median_of_medians_ns=statistics.median(r["candidate_median_ns"] for r in group),
                median_paired_improvement_pct=statistics.median(effects),
                min_paired_improvement_pct=min(effects),max_paired_improvement_pct=max(effects),
                positive_blocks=sum(v>0 for v in effects),negative_blocks=sum(v<0 for v in effects)))
    return pairs, aggregate

def write_csv(path, rows):
    with path.open("x", newline="", encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator="\n")
        writer.writeheader();writer.writerows(rows)

def read_run(run):
    m=json.loads((run/"manifest.json").read_text())
    if m.get("development_only") or m["record_type"] != "three-way-final-timing" or m["status"]!="completed" or m["provenance_recheck"]!="pass" or any(v!="pass" for v in m["checks"].values()):
        raise ValueError("Incomplete/unaccepted session")
    p=m["protocol"]; session=m["session"]
    if (p["blocks"],p["iterations"],p["warmup"],p["sessions"],p["cpu"])!=(12,1000,100,3,0) or session not in (1,2,3):
        raise ValueError("Not the formal frozen budget")
    if metadata.sha256(run/"metadata.json")!=m["metadata_sha256"]:raise ValueError("Metadata changed")
    if len(m["executables"])!=9 or len(m["assembly"])!=108 or len(m["steps"])!=225:
        raise ValueError("Incomplete build/assembly/measurement coverage")
    steps={s["stdout"]:s for s in m["steps"]}
    for s in m["steps"]:
        if s["exit_code"]!=0 or s["status"]!="completed":raise ValueError("Failed step")
        for stream in ("stdout","stderr"):
            if metadata.sha256(run/s[stream])!=s[stream+"_sha256"]:raise ValueError("Raw output changed")
    summaries=[];seen=set()
    for d in m["datasets"]:
        key=(d["parameter"],d["block"],d["variant"])
        if key in seen:raise ValueError("Duplicate dataset")
        seen.add(key)
        index=PARAMETERS.index(d["parameter"])
        order=p["permutations"][(d["block"]-1+2*(session-1)+index)%6]
        seed=p["session_seeds"][session-1]+d["block"]-1
        if d["position"]!=order.index(d["variant"])+1 or d["fixture_seed"]!=seed or d["rows"]!=3000:
            raise ValueError("Wrong order/fixture/row count")
        if metadata.sha256(run/d["path"])!=d["sha256"]:raise ValueError("CSV changed")
        step=steps[d["path"]]
        if step["argv"][-3:]!=["1000","100",str(seed)]:raise ValueError("Wrong benchmark invocation")
        diagnostics=dict(line.split("=",1) for line in (run/step["stderr"]).read_text().splitlines())
        expected_diag=dict(timer=p["timer"],unit="ns",iterations="1000",warmup="100",seed=str(seed),input_mode="derand-shake256-v1")
        if any(diagnostics.get(k)!=v for k,v in expected_diag.items()):raise ValueError("Harness diagnostics mismatch")
        for row in timing.summarise_csv(run/d["path"],d["parameter"],p["iterations"],d["block"]):
            row["block"]=row.pop("repetition")
            summaries.append(dict(variant=d["variant"],position=d["position"],fixture_seed=seed,**row))
    if seen!={(k,b,v) for k,b,v in itertools.product(PARAMETERS,range(1,13),VARIANTS)}:raise ValueError("Incomplete dataset matrix")
    pairs, aggregate=derive(summaries,12,session)
    import io
    for name, rows in (("process-summary",summaries),("paired-comparison",pairs),("comparison",aggregate)):
        buffer=io.StringIO(newline=""); writer=csv.DictWriter(buffer,fieldnames=list(rows[0]),lineterminator="\n")
        writer.writeheader();writer.writerows(rows)
        entry=m["derived"][name]
        if metadata.sha256(run/entry["path"])!=entry["sha256"] or (run/entry["path"]).read_bytes()!=buffer.getvalue().encode():
            raise ValueError("Derived table does not reproduce")
    return m, aggregate

def combine(runs):
    loaded=[read_run(r) for r in runs]
    if sorted(m["session"] for m,_ in loaded)!=[1,2,3]:raise ValueError("Exactly three distinct sessions required")
    first=loaded[0][0]
    for m,_ in loaded:
        for key in ("protocol","source_file_sha256","support_file_sha256","compiler","build_flags","tool_sha256"):
            if m[key]!=first[key]:raise ValueError("Session identities/protocols differ: "+key)
    rows=sorted([r for _,rs in loaded for r in rs],key=lambda r:(r["session"],r["reference"],r["candidate"],r["parameter_set"],r["operation"]))
    combined=[]
    for ref,cand in COMPARISONS:
        for k,op in itertools.product(PARAMETERS,timing.OPERATIONS):
            selected=[r["median_paired_improvement_pct"] for r in rows if (r["reference"],r["candidate"],r["parameter_set"],r["operation"])==(ref,cand,f"Kyber{k}",op)]
            combined.append(dict(reference=ref,candidate=cand,parameter_set=f"Kyber{k}",operation=op,sessions=3,
                median_session_improvement_pct=statistics.median(selected),min_session_improvement_pct=min(selected),
                max_session_improvement_pct=max(selected),positive_sessions=sum(v>0 for v in selected),negative_sessions=sum(v<0 for v in selected)))
    return loaded,rows,combined

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runs",nargs=3,type=Path,required=True)
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args()
    loaded,rows,combined=combine(args.runs)
    args.output.mkdir(parents=True,exist_ok=False)
    write_csv(args.output/"session-effects.csv",rows);write_csv(args.output/"three-session-effects.csv",combined)
    provenance=dict(record_type="final-three-session-analysis",analysis_script_sha256=metadata.sha256(Path(__file__)),
        inputs={str(run/"manifest.json"):metadata.sha256(run/"manifest.json") for run in args.runs},
        source_commits=[m["source_commit"] for m,_ in loaded],
        interpretation="Three session estimates and their descriptive range; not a confidence interval or population guarantee.",
        outputs={p.name:metadata.sha256(p) for p in args.output.iterdir() if p.is_file()})
    (args.output/"provenance.json").write_text(json.dumps(provenance,indent=2)+"\n")
    print("Verified all three sessions; wrote descriptive effects without pooling inner samples.")
if __name__=="__main__":main()
