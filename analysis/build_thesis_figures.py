#!/usr/bin/env python3
"""Reproduce ACT-0016 scientific figures/tables from pinned retained results."""
import argparse
import csv
import hashlib
import importlib.metadata
import json
import math
import platform
import statistics
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.colors import TwoSlopeNorm
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
EXPS = ("001","002","003","005","006")
PARAMS = ("Kyber512","Kyber768","Kyber1024")
OPS = ("keygen","encap","decap")
COLOURS = ("#0072B2","#D55E00","#009E73")
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()

def rows(path):
    with path.open(newline="",encoding="utf-8") as stream: return list(csv.DictReader(stream))
def csv_write(path,data):
    with path.open("w",newline="",encoding="utf-8") as stream:
        w=csv.DictWriter(stream,fieldnames=list(data[0]),lineterminator="\n"); w.writeheader();w.writerows(data)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path,default=ROOT/"analysis/figures/ACT-0016")
    args=parser.parse_args(); out=args.output.resolve()
    if out==ROOT or out.is_relative_to(ROOT/"results"):
        raise RuntimeError("Use a separate figure directory; results are immutable.")
    inputs=json.loads((ROOT/"analysis/figure_inputs.json").read_text())["files"]
    for name,digest in inputs.items():
        if sha(ROOT/name)!=digest: raise RuntimeError(f"Pinned figure input changed: {name}")
    out.mkdir(parents=True,exist_ok=True)
    plt.rcParams.update({"font.family":"DejaVu Sans","font.size":10,"axes.spines.top":False,
        "axes.spines.right":False,"axes.titlesize":12,"axes.labelsize":10,
        "svg.hashsalt":"kyber-act0016","pdf.fonttype":42,"ps.fonttype":42})
    pairs={};summary={};table=[]
    for x in EXPS:
        directory=ROOT/f"results/EXP-{x}/RUN-0002"
        manifest=json.loads((directory/"manifest.json").read_text())
        if manifest["status"]!="completed" or manifest["provenance_recheck"]!="pass":
            raise RuntimeError("Unaccepted run status")
        for kind in ("comparison","paired-comparison"):
            rec=manifest["derived"][kind]
            if sha(directory/rec["path"])!=rec["sha256"]:raise RuntimeError("Derived identity mismatch")
        pairs[x]=rows(directory/"derived/paired-comparison.csv")
        summary[x]=rows(directory/"derived/comparison.csv")
        if len(pairs[x])!=45 or len(summary[x])!=9:raise RuntimeError("Incomplete comparison")
        for p in PARAMS:
            for op in OPS:
                subset=[r for r in pairs[x] if r["parameter_set"]==p and r["operation"]==op]
                if sorted(int(r["block"]) for r in subset)!=[1,2,3,4,5]:raise RuntimeError("Pair IDs")
                values=[float(r["improvement_pct"]) for r in subset]
                agg=next(r for r in summary[x] if r["parameter_set"]==p and r["operation"]==op)
                for field,value in (("median_paired_improvement_pct",statistics.median(values)),
                                    ("min_paired_improvement_pct",min(values)),("max_paired_improvement_pct",max(values))):
                    if not math.isclose(float(agg[field]),value,rel_tol=1e-12,abs_tol=1e-12):raise RuntimeError("Aggregate mismatch")
                for r in subset:
                    before=next(float(v) for k,v in r.items() if k in ("baseline_median_ns","exp001_median_ns","exp002_median_ns","exp003_median_ns","exp005_median_ns"))
                    after=next(float(v) for k,v in r.items() if k in ("candidate_median_ns",f"exp{x}_median_ns"))
                    if not math.isclose(float(r["improvement_pct"]),100*(before-after)/before,abs_tol=1e-10):raise RuntimeError("Pair formula mismatch")
                table.append({"experiment":"EXP-"+x,"reference":{"001":"original","002":"EXP-001","003":"EXP-002","005":"EXP-003","006":"EXP-005"}[x],
                    "parameter":p,"operation":op,"pairs":5,"median_paired_time_reduction_pct":statistics.median(values),
                    "observed_min_pct":min(values),"observed_max_pct":max(values),"positive_pairs":sum(v>0 for v in values),
                    "source":"results/EXP-"+x+"/RUN-0002/derived/paired-comparison.csv"})
    csv_write(out/"incremental-effects.csv",table)
    csv_write(out/"exp006-paired-effects.csv",pairs["006"])
    exports=[]
    def save(fig,name):
        for ext in ("png","svg","pdf"):
            path=out/(name+"."+ext)
            md=({"Date":None} if ext=="svg" else {"CreationDate":None,"ModDate":None} if ext=="pdf" else {})
            fig.savefig(path,dpi=300,bbox_inches="tight",metadata=md)
            exports.append(path.name)
        plt.close(fig)
    fig,axes=plt.subplots(1,3,figsize=(11.5,4.4),sharex=True,sharey=True)
    for ax,p in zip(axes,PARAMS):
        ax.axvspan(-3.5,0,color="#faf2ed");ax.axvline(0,color="#555555",lw=1)
        for y,op in enumerate(OPS):
            sub=[r for r in pairs["006"] if r["parameter_set"]==p and r["operation"]==op]
            vals=[float(r["improvement_pct"]) for r in sub]
            ax.plot([min(vals),max(vals)],[y,y],c="#777777",lw=1.1,zorder=2)
            for r,v,dy in zip(sub,vals,(-.14,-.07,0,.07,.14)):
                ax.scatter(v,y+dy,s=32,marker="o" if int(r["block"])%2 else "s",color=COLOURS[y],alpha=.8,zorder=3)
            med=statistics.median(vals)
            ax.scatter(med,y,s=88,marker="|",c="black",linewidths=2,zorder=4)
            ax.text(3.35,y,f"{med:+.2f}%",ha="right",va="center",weight="bold",fontsize=10)
        ax.set_title(p,pad=12);ax.set_xlim(-3.5,3.5);ax.set_ylim(2.5,-.5)
        ax.set_xticks((-3,-2,-1,0,1,2));ax.grid(axis="x",alpha=.15);ax.set_axisbelow(True)
        ax.set_yticks(range(3),["Keygen","Encapsulation","Decapsulation"])
    fig.suptitle("EXP-006 versus EXP-005: fewer reductions, mixed timing results",fontsize=15,y=1.01)
    fig.supxlabel("Paired time reduction (%) — positive values are faster",y=.12)
    legend=[Line2D([],[],marker="o",ls="",color="#555555",label="EXP-005 first (3 pairs)"),
            Line2D([],[],marker="s",ls="",color="#555555",label="EXP-006 first (2 pairs)"),
            Line2D([],[],marker="|",ls="",color="black",markersize=12,label="Median; line = observed range")]
    fig.legend(handles=legend,loc="lower center",bbox_to_anchor=(.5,-.01),ncol=3,frameon=False,fontsize=9)
    fig.text(.5,-.055,"Five matched process pairs per parameter in one session. Ranges are not confidence intervals.",ha="center",fontsize=9,color="#444444")
    fig.tight_layout(rect=(0,.19,1,.96));save(fig,"exp006-paired-effects")

    matrix=np.array([[next(t["median_paired_time_reduction_pct"] for t in table if t["parameter"]==p and t["operation"]==op and t["experiment"]=="EXP-"+x) for x in EXPS] for p in PARAMS for op in OPS])
    fig,ax=plt.subplots(figsize=(9,6.2)); limit=max(3,float(np.max(np.abs(matrix))))
    im=ax.imshow(matrix,cmap="BrBG",norm=TwoSlopeNorm(vmin=-limit,vcenter=0,vmax=limit),aspect="auto")
    ax.set_yticks(range(9),[f"{p} · {op}" for p in PARAMS for op in OPS])
    ax.set_xticks(range(5),["EXP-001\nvs original","EXP-002\nvs EXP-001","EXP-003\nvs EXP-002","EXP-005\nvs EXP-003","EXP-006\nvs EXP-005"])
    for i in range(9):
        for j in range(5):
            ax.text(j,i,f"{matrix[i,j]:+.2f}%",ha="center",va="center",fontsize=10,
                    color="white" if abs(matrix[i,j])>.65*limit else "#171717")
    for y in (2.5,5.5):ax.axhline(y,color="white",lw=3)
    ax.tick_params(length=0);fig.colorbar(im,ax=ax,pad=.03,label="Median paired time reduction (%)")
    fig.suptitle("Incremental effects across the optimisation trials",fontsize=15,y=1.0)
    fig.text(.5,.015,"Each column uses its own freshly measured predecessor (5 pairs, one session).\nThese percentages are conditional effects; they must not be added or multiplied into a total gain.",ha="center",fontsize=9)
    fig.tight_layout(rect=(0,.08,1,.96));save(fig,"incremental-effects-overview")

    counts=[]
    base=ROOT/"results/EXP-000/RUN-0004"
    m=json.loads((base/"manifest.json").read_text())
    if sha(base/m["summary"]["path"])!=m["summary"]["sha256"]:raise RuntimeError("Original counts mismatch")
    countsets={"original":rows(base/"derived/summary.csv")}
    for x in EXPS:
        m=json.loads((ROOT/f"results/EXP-{x}/RUN-0001/manifest.json").read_text())
        if m["status"]!="completed" or m["provenance_recheck"]!="pass":raise RuntimeError("Count validation incomplete")
        countsets["EXP-"+x]=m["reduction_counts"]
    for stage,data in countsets.items():
        if len(data)!=9:raise RuntimeError("Missing count groups")
        for row in data:
            if int(row["samples"])!=10:raise RuntimeError("Unexpected count sample budget")
            counts.append({"stage":stage,**row})
    csv_write(out/"reduction-counts.csv",counts)
    fig,axes=plt.subplots(3,2,figsize=(10.5,8.1),sharex=True)
    stages=list(countsets)
    for row,p in enumerate(PARAMS):
        for col,(field,title) in enumerate((("montgomery_calls","Montgomery calls"),("barrett_calls","Barrett calls"))):
            ax=axes[row,col]
            for op,colour in zip(OPS,COLOURS):
                vals=[int(next(r[field] for r in countsets[s] if r["parameter_set"]==p and r["operation"]==op)) for s in stages]
                ax.plot(range(6),vals,marker="o",lw=1.5,ms=4,color=colour,label=op)
            ax.set_ylim(bottom=0);ax.grid(axis="y",alpha=.2);ax.set_axisbelow(True)
            ax.set_title(f"{p} · {title}",loc="left",fontsize=11)
            ax.set_xticks(range(6),["Original","001","002","003","005","006"])
    fig.suptitle("Observed modular-reduction calls per complete operation",fontsize=15,y=1)
    fig.legend(*axes[0,0].get_legend_handles_labels(),loc="lower center",bbox_to_anchor=(.5,.055),ncol=3,frameon=False)
    fig.text(.5,.02,"10 deterministic fixtures per parameter and stage; counts agreed within every group.\nInstrumented builds count function calls, not instructions, elapsed time or leakage.",ha="center",fontsize=9)
    fig.tight_layout(rect=(0,.11,1,.97));save(fig,"reduction-counts")
    for name,digest in inputs.items():
        if sha(ROOT/name)!=digest:raise RuntimeError("Input changed during figure generation")
    versions={p:importlib.metadata.version(p) for p in ("matplotlib","numpy","pillow","contourpy","cycler","fonttools","kiwisolver","packaging","pyparsing","python-dateutil","six","tzdata")}
    manifest={"activity_id":"ACT-0016","record_type":"derived-thesis-figures","source_results_commit":"42d68a7da90f5d19d0539a0e8825a24852121e41",
      "analysis_code_sha256":sha(Path(__file__)),"input_index_sha256":sha(ROOT/"analysis/figure_inputs.json"),
      "python":platform.python_version(),"packages":versions,"input_sha256":inputs,
      "outputs":{name:sha(out/name) for name in [*exports,"incremental-effects.csv","exp006-paired-effects.csv","reduction-counts.csv"]},
      "checks":{"timing_groups":45,"paired_effects_recomputed":225,"count_groups":54,"raw_results_modified":False},
      "interpretation":"Single-session incremental results; ranges are observed extrema, not confidence intervals. No cumulative performance or leakage claim."}
    (out/"provenance.json").write_text(json.dumps(manifest,indent=2,sort_keys=True)+"\n")
    print(f"Saved {len(exports)} figure exports and 3 data tables to {out}")
if __name__=="__main__":main()
