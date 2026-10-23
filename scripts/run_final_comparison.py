#!/usr/bin/env python3
"""EXP-009: one committed, balanced session of original/EXP-003/EXP-005."""
import argparse
import json
import os
import signal
import subprocess
import sys
from pathlib import Path
import collect_run_metadata as metadata
import run_validation as validation
import run_timing as timing
import run_comparison as paired
import run_incremental_comparison as assembly
import run_timing_leakage as historical
import analyse_final_comparison as analysis
ROOT = metadata.ROOT
PROTOCOL = ROOT / "tests/final_comparison_protocol.json"
LEAKAGE = "results/EXP-008/RUN-0001/manifest.json"
REVIEW = "notes/evidence/ACT-0018/exp-008-run-0001-review.json"
SUPPORT = tuple(sorted(set((*assembly.SUPPORT, *historical.SUPPORT,
    "scripts/run_final_comparison.py", "scripts/analyse_final_comparison.py",
    "tests/final_comparison_protocol.json", "notes/experiments/EXP-009-final-comparison.md"))))

def load_protocol():
    p=json.loads(PROTOCOL.read_text())
    if (p["experiment"],p["sessions"],p["blocks"],p["iterations"],p["warmup"],p["cpu"]) != ("EXP-009",3,12,1000,100,0):
        raise RuntimeError("Unexpected frozen protocol; review amendments before collection")
    for name,digest in p["accepted_inputs"].items():
        if metadata.sha256(ROOT/name)!=digest:raise RuntimeError("Accepted input changed: "+name)
    m=json.loads((ROOT/LEAKAGE).read_text()); review=json.loads((ROOT/REVIEW).read_text())
    if not review["accepted_for_closing_comparison"] or review["manifest_sha256"]!=metadata.sha256(ROOT/LEAKAGE) or m["assessment"]!="no-difference-detected-within-budget":
        raise RuntimeError("Security evidence not accepted")
    return p

def assembly_gate(p, leakage):
    expected={key:entry["normalised"] for key,entry in leakage["assembly"].items() if "/pqcrystals_" in key}
    for tag,name in p["keypair_assembly"].items():
        parameter=tag.rsplit("-",1)[1]; symbol=f"pqcrystals_kyber{parameter}_ref_indcpa_keypair_derand"
        expected[tag+"/"+symbol]=assembly.assembly_record((ROOT/name).read_text(),symbol)
    if len(expected)!=108:raise RuntimeError("Incomplete reviewed assembly coverage")
    return expected

def order_for_block(p,session,block,parameter):
    index=analysis.PARAMETERS.index(parameter)
    return p["permutations"][(block-1+2*(session-1)+index)%6]

def refuse_completed_session(session):
    for path in (ROOT/"results/EXP-009").glob("RUN-*/manifest.json"):
        m=json.loads(path.read_text())
        if m.get("session")==session and m.get("status")=="completed":
            raise RuntimeError(f"Session {session} already completed in {path.parent.name}; retain it and review, do not select a rerun")

def execute(run_dir,snapshot,p,args,original_affinity):
    leakage=json.loads((ROOT/LEAKAGE).read_text()); expected=assembly_gate(p,leakage)
    source=historical.source_maps();compiler=snapshot["environment"]["available_compiler"]
    build=run_dir/"build";env={"PATH":"/usr/bin:/bin","LC_ALL":"C","TMPDIR":str(build)}
    dirs={"baseline":validation.BASELINE,"exp003":build/"exp003-source","exp005":build/"exp005-source"}
    m=dict(schema_version=1,record_type=p["record_type"],experiment_id=args.experiment,run_id=args.run,session=args.session,
        status="running",source_commit=snapshot["provenance"]["source_commit"],upstream_commit=metadata.PIN,
        metadata_sha256=metadata.sha256(run_dir/"metadata.json"),protocol=p,compiler=compiler,
        source_file_sha256=source,support_file_sha256={n:metadata.sha256(ROOT/n) for n in SUPPORT},
        tool_sha256=leakage["tool_sha256"],build_flags=list(validation.FLAGS),
        process_environment=env,invocation_arguments=sys.argv[1:],
        affinity=dict(original=original_affinity,selected_logical_cpu=args.cpu,observed=sorted(os.sched_getaffinity(0)),physical_core_placement="unknown"),
        steps=[],executables={},assembly={},datasets=[],derived={},
        checks=dict(reviewed_assembly_match="not-run",measured_roundtrips="not-run",csv_integrity="not-run",harness_diagnostics="not-run"),
        provenance_recheck="not-run",benchmark_executed=False,
        security_interpretation="Reuse accepted security evidence for exact source/normal-code identities; throughput is not a leakage test")
    def identity():
        validation.check_source_state(m["source_commit"],source["baseline"])
        if load_protocol()!=p or historical.source_maps()!=source or source!=leakage["source_file_sha256"]:
            raise RuntimeError("Source/protocol identities changed")
        if compiler!=leakage["compiler"] or list(validation.FLAGS)!=leakage["build_flags"]:
            raise RuntimeError("Compiler/flags differ from reviewed builds")
        for name,digest in {**m["tool_sha256"],compiler["path"]:compiler["sha256"]}.items():
            if metadata.sha256(Path(name))!=digest:raise RuntimeError("Tool changed")
        if sorted(os.sched_getaffinity(0))!=[args.cpu]:raise RuntimeError("CPU affinity changed")
        for name,digest in m["support_file_sha256"].items():
            if metadata.sha256(ROOT/name)!=digest:raise RuntimeError("Support changed: "+name)
        for v in ("exp003","exp005"):
            if dirs[v].exists():
                if any(f.is_symlink() for f in dirs[v].rglob("*")):raise RuntimeError("Unexpected source symlink")
                actual={f.relative_to(dirs[v]).as_posix():metadata.sha256(f) for f in dirs[v].rglob("*") if f.is_file()}
                if actual!=source[v]:raise RuntimeError("Restored source changed")
        for e in m["executables"].values():
            if metadata.sha256(run_dir/e["path"])!=e["sha256"]:raise RuntimeError("Executable changed")
    def step(label,command,cwd):
        if not validation.run_step(run_dir,m,label,command,cwd,env,p["timeout_seconds"]):
            raise RuntimeError("Failed step: "+label+"; retain this attempt")
        return m["steps"][-1]
    try:
        build.mkdir();(run_dir/"raw").mkdir();(run_dir/"derived").mkdir()
        for name in (*SUPPORT,*p["accepted_inputs"]):metadata.git("cat-file","-e",f"{m['source_commit']}:{name}")
        identity()
        for v in ("exp003","exp005"):
            historical.restore(dirs[v],leakage["protocol"]["restoration_commits"][v],source[v])
        for parameter,k in validation.PARAMETERS:
            for v in p["variants"]:
                tag=f"{v}-{parameter}";exe=build/("bench-"+tag)
                print(f"Building Kyber{parameter}: {v}...",flush=True)
                step("build-"+tag,paired.build_command(compiler["path"],dirs[v],k,exe),dirs[v])
                m["executables"][tag]=dict(path=exe.relative_to(run_dir).as_posix(),sha256=metadata.sha256(exe))
                for function in (*historical.SYMBOLS,"indcpa_keypair_derand"):
                    symbol=f"pqcrystals_kyber{parameter}_ref_{function}"
                    s=step("assembly-"+tag+"-"+function,["/usr/bin/objdump","-d","--insn-width=16","--disassemble="+symbol,str(exe)],dirs[v])
                    record=assembly.assembly_record((run_dir/s["stdout"]).read_text(),symbol)
                    key=tag+"/"+symbol
                    if record!=expected[key]:raise RuntimeError("Generated code differs from reviewed body: "+key)
                    m["assembly"][key]=dict(path=s["stdout"],normalised=record)
        m["checks"]["reviewed_assembly_match"]="pass";identity()
        summaries=[]
        for block in range(1,p["blocks"]+1):
            rotation=(block-1)%3
            parameters=analysis.PARAMETERS[rotation:]+analysis.PARAMETERS[:rotation]
            seed=p["session_seeds"][args.session-1]+block-1
            for parameter in parameters:
                for position,v in enumerate(order_for_block(p,args.session,block,parameter),1):
                    tag=f"{v}-{parameter}";exe=run_dir/m["executables"][tag]["path"]
                    print(f"Session {args.session}, block {block}/{p['blocks']}, Kyber{parameter}: {v}...",flush=True)
                    m["benchmark_executed"]=True
                    s=step(f"timing-{tag}-block-{block:04d}",[str(exe),str(p["iterations"]),str(p["warmup"]),str(seed)],dirs[v])
                    diagnostics=dict(line.split("=",1) for line in (run_dir/s["stderr"]).read_text().splitlines())
                    wanted=dict(timer=p["timer"],unit="ns",iterations=str(p["iterations"]),warmup=str(p["warmup"]),seed=str(seed),input_mode="derand-shake256-v1")
                    if any(diagnostics.get(k)!=value for k,value in wanted.items()):raise RuntimeError("Harness diagnostics mismatch")
                    for key in ("clock_resolution_ns","empty_timer_pair_min_ns"):
                        if int(diagnostics[key])<0:raise RuntimeError("Invalid timer diagnostics")
                    csv_path=(run_dir/s["stdout"]).with_suffix(".csv")
                    if csv_path.exists():raise RuntimeError("Refusing to overwrite raw CSV")
                    (run_dir/s["stdout"]).rename(csv_path);s["stdout"]=csv_path.relative_to(run_dir).as_posix()
                    for row in timing.summarise_csv(csv_path,parameter,p["iterations"],block):
                        row["block"]=row.pop("repetition")
                        summaries.append(dict(variant=v,position=position,fixture_seed=seed,**row))
                    m["datasets"].append(dict(parameter=parameter,variant=v,block=block,position=position,fixture_seed=seed,
                        path=s["stdout"],sha256=metadata.sha256(csv_path),rows=p["iterations"]*3))
                    validation.save_manifest(run_dir,m)
        pairs,aggregate=analysis.derive(summaries,p["blocks"],args.session)
        for name,rows in (("process-summary",summaries),("paired-comparison",pairs),("comparison",aggregate)):
            dest=run_dir/"derived"/(name+".csv");analysis.write_csv(dest,rows)
            m["derived"][name]=dict(path=dest.relative_to(run_dir).as_posix(),sha256=metadata.sha256(dest),rows=len(rows))
        identity();m["checks"]={key:"pass" for key in m["checks"]};m["provenance_recheck"]="pass";m["status"]="completed"
    except KeyboardInterrupt:m["status"]="interrupted";m["error"]="Interrupted; preserve attempt and allocate a new run ID"
    except (OSError,RuntimeError,ValueError,KeyError,subprocess.TimeoutExpired) as exc:
        m["status"]="failed";m["error"]=str(exc)
    finally:validation.save_manifest(run_dir,m)
    print(f"Comparison status: {m['status']}; session {args.session}")
    if "error" in m:print(m["error"])
    print(f"Record: {run_dir}/manifest.json")
    return 0 if m["status"]=="completed" else 1

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--experiment",default="EXP-009")
    parser.add_argument("--run",required=True);parser.add_argument("--session",type=int,choices=(1,2,3),required=True)
    parser.add_argument("--cpu",type=int,default=0);parser.add_argument("--compiler",default="gcc")
    for name in ("host-os","power-mode","background-load"):parser.add_argument("--"+name,default="unknown")
    args=parser.parse_args();p=load_protocol()
    if sys.platform!="linux" or args.experiment!="EXP-009" or args.cpu!=p["cpu"]:parser.error("Requires Linux/WSL, EXP-009, CPU 0")
    original=sorted(os.sched_getaffinity(0))
    if args.cpu not in original:parser.error("CPU 0 not available")
    refuse_completed_session(args.session)
    os.sched_setaffinity(0,{args.cpu})
    try:
        command=[sys.executable,"-B",str(ROOT/"scripts/collect_run_metadata.py"),"--experiment",args.experiment,
            "--run",args.run,"--variant","original-exp003-exp005","--compiler",args.compiler,
            "--host-os",args.host_os,"--power-mode",args.power_mode,"--background-load",args.background_load]
        result=subprocess.run(command,cwd=ROOT)
        if result.returncode:return result.returncode
        run_dir=ROOT/"results"/args.experiment/args.run
        return execute(run_dir,json.loads((run_dir/"metadata.json").read_text()),p,args,original)
    finally:os.sched_setaffinity(0,set(original))
if __name__=="__main__":
    signal.signal(signal.SIGTERM,validation.interrupt_requested)
    try:sys.exit(main())
    except (OSError,RuntimeError,ValueError,subprocess.TimeoutExpired) as exc:
        print(f"ERROR: {exc}. Preserve any attempt; use a new run ID after a failure.",file=sys.stderr);sys.exit(1)
