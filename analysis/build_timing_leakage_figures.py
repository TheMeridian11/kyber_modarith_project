#!/usr/bin/env python3
"""Plot audited EXP-008 diagnostics; |t| is not a security score."""
import argparse
import csv
import hashlib
import json
import platform
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path,default=ROOT/"analysis/figures/ACT-0018")
    args=parser.parse_args()
    review_path=ROOT/"notes/evidence/ACT-0018/exp-008-run-0001-review.json"
    run_path=ROOT/"results/EXP-008/RUN-0001/manifest.json"
    review=json.loads(review_path.read_text());run=json.loads(run_path.read_text())
    if sha(run_path)!=review["manifest_sha256"] or not review["accepted_for_closing_comparison"]:
        raise ValueError("Unaccepted/mismatched evidence")
    rows=review["statistics"];paths=run["protocol"]["paths"];variants=["baseline","exp003","exp005"]
    columns=[(v,k) for v in variants for k in (512,768,1024)]
    matrix=np.empty((8,9))
    for y,path in enumerate(paths):
        for x,(v,k) in enumerate(columns):
            group=[r for r in rows if (r["path"],r["variant"],r["parameter"])==(path,v,k)]
            if len(group)!=24:raise ValueError("Incomplete figure group")
            matrix[y,x]=max(abs(r["t"]) for r in group)
    plt.rcParams.update({"font.family":"DejaVu Sans","font.size":10,"svg.hashsalt":"kyber-act0018","pdf.fonttype":42})
    fig=plt.figure(figsize=(11.2,8.5))
    grid=fig.add_gridspec(2,2,height_ratios=[2.2,1],width_ratios=[1,.035],hspace=.7,wspace=.05)
    ax=fig.add_subplot(grid[0,0]);cax=fig.add_subplot(grid[0,1])
    im=ax.imshow(matrix,vmin=0,vmax=10,cmap="Blues",aspect="auto")
    fig.colorbar(im,cax=cax,label="Maximum |Welch t| (threshold 10)")
    labels=["Base multiplication: second operand","Base multiplication: first operand","Vector dot: second operand","Vector dot: first operand","Inverse NTT","Error NTT + addition","Keygen arithmetic path","IND-CPA decryption"]
    ax.set_yticks(range(8),labels,fontsize=9)
    ax.set_xticks(range(9),[f"{['Original','EXP-003','EXP-005'][variants.index(v)]}\n{k}" for v,k in columns],fontsize=9)
    for y in range(8):
        for x in range(9):ax.text(x,y,f"{matrix[y,x]:.2f}",ha="center",va="center",fontsize=10,color="#16364a")
    for x in (2.5,5.5):ax.axvline(x,color="white",lw=3)
    ax.set_title("Timing screen: all tested target statistics below the threshold",loc="left",fontsize=13,pad=15)
    ax.set_xlabel("Parameter set within each implementation",labelpad=9)
    controls=fig.add_subplot(grid[1,0]);colors=["#376f8e","#bf7531"]
    for x,path in enumerate(("negative-control","positive-control")):
        cells=[c for c in run["measurements"] if c["path"]==path]
        values=[max(abs(s["t"]) for s in c["statistics"]) if x==0 else abs(next(s["t"] for s in c["statistics"] if s["view"]=="raw-mean" and s["look"]==50000)) for c in cells]
        if len(values)!=18:raise ValueError("Incomplete control set")
        controls.scatter(x+np.linspace(-.12,.12,18),values,c=colors[x],s=28,edgecolors="white",linewidths=.4,zorder=3)
    controls.axhline(10,color="#8f3434",linestyle="--",lw=1)
    controls.text(1.33,10,"Threshold 10",ha="right",va="bottom",color="#8f3434",fontsize=9)
    controls.set_yscale("log");controls.set_ylim(.3,400);controls.set_xlim(-.4,1.4)
    controls.set_xticks([0,1],["18 negative controls\nmaximum over all six statistics","18 deliberate positive controls\nfinal uncropped mean statistic"],fontsize=9)
    controls.set_ylabel("|Welch t| (log scale)")
    controls.grid(axis="y",which="major",alpha=.2)
    controls.set_title("Controls: quiet negatives and detected deliberate differences",loc="left",fontsize=11,pad=10)
    fig.subplots_adjust(left=.30,right=.92,top=.93,bottom=.16)
    fig.text(.03,.045,"EXP-008/RUN-0001 · 50,000 analysis observations per process\nTop cell: maximum over 2 profiles × 2 repetitions × 2 looks × 3 views.\nNo difference detected within this budget; no whole-program constant-time proof or security ranking.",fontsize=9,color="#333333")
    args.output.mkdir(parents=True,exist_ok=True)
    stem=args.output/"exp008-timing-screen"
    for suffix in ("svg","pdf","png"):
        dest=stem.with_suffix("."+suffix)
        if dest.exists():raise ValueError("Refusing to replace an existing figure")
        extra={"metadata":{"Date":None}} if suffix=="svg" else {"metadata":{"CreationDate":None,"ModDate":None}} if suffix=="pdf" else {}
        fig.savefig(dest,dpi=300,**extra)
        if suffix=="svg":dest.write_text("\n".join(line.rstrip() for line in dest.read_text().splitlines())+"\n")
    plt.close(fig)
    table=stem.with_suffix(".csv")
    with table.open("x",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator="\n");writer.writeheader();writer.writerows(rows)
    outputs={p.name:sha(p) for p in sorted(args.output.iterdir()) if p.is_file()}
    provenance=dict(activity_id="ACT-0018",inputs={str(p.relative_to(ROOT)):sha(p) for p in (review_path,run_path)},
        generator_sha256=sha(__file__),python=platform.python_version(),matplotlib=matplotlib.__version__,numpy=np.__version__,outputs=outputs,
        interpretation="Descriptive diagnostic maxima, not calibrated family-wise inference, sensitivity bound or security score")
    with (args.output/"provenance.json").open("x") as f:json.dump(provenance,f,indent=2);f.write("\n")
    print("Generated EXP-008 SVG/PDF/PNG and all 1944 plotted-source statistics")
if __name__=="__main__":main()
