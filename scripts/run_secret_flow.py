#!/usr/bin/env python3
"""EXP-007: archive controlled Memcheck secret-flow checks; no timings."""
import argparse
import hashlib
import json
import os
import re
import signal
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import collect_run_metadata as metadata
import run_validation as validation

ROOT = metadata.ROOT
HARNESS = ROOT / "tests/test_secret_flow.c"
PATHS = ("basemul", "basemul-first", "dot", "dot-first", "inverse", "error-path", "keygen-dot", "indcpa-dec")
CONTROLS = ("negative-control", "positive-branch", "positive-address")
VARIANTS = {"baseline": 0, "exp005": 5, "exp006": 6}
EXP005_COMMIT = "4bd813ed71a90c7722275dc802336852214a5388"
INPUTS = {
 "results/EXP-005/RUN-0001/manifest.json": "6bf9833c02e9744e92360cecd37d6668cb4c4dc01ad4803ee72315fce8f0bd5d",
 "results/EXP-006/RUN-0001/manifest.json": "738fe9501ed4f7df3f5766577f5d6e0e359d1d6f0630b4617175e5bee527c499",
 "notes/evidence/ACT-0013/exp-005-run-0001-review.json": "e583f1ef74776363536778f409be2bc872ec6a99dfa223628c6557e9fee1669f",
 "notes/evidence/ACT-0015/exp-006-run-0001-review.json": "b9e7f1e0a633c6abab769057086c7908cf2b3a49b8f8727fa52117a40e199696",
}
SUPPORT = ("scripts/run_secret_flow.py", "tests/test_secret_flow.c",
           "scripts/collect_run_metadata.py", "scripts/run_validation.py",
           "notes/experiments/EXP-007-secret-flow.md")
FLAGS = (*validation.FLAGS, "-g")
SYMBOLS = ("basemul", "polyvec_basemul_acc_montgomery", "invntt", "ntt",
           "poly_ntt", "poly_tomont", "poly_reduce", "poly_add", "indcpa_dec",
           "montgomery_reduce", "barrett_reduce")

def sources():
    for name, digest in INPUTS.items():
        if metadata.sha256(ROOT / name) != digest:
            raise RuntimeError(f"Accepted input changed: {name}")
    a = json.loads((ROOT / "results/EXP-005/RUN-0001/manifest.json").read_text())
    b = json.loads((ROOT / "results/EXP-006/RUN-0001/manifest.json").read_text())
    if any(x["status"] != "completed" or x["provenance_recheck"] != "pass" for x in (a,b)):
        raise RuntimeError("Validation is incomplete.")
    base = validation.source_snapshot()
    if base != a["source_file_sha256"]["baseline"] or base != b["source_file_sha256"]["baseline"]:
        raise RuntimeError("Original reference identity changed.")
    current = ROOT / "implementation/kyber-optimised-ref"
    observed = {p.relative_to(current).as_posix(): metadata.sha256(p) for p in current.rglob("*")
                if p.is_file() and (p.suffix in (".c", ".h") or p.name == "Makefile")}
    if observed != b["source_file_sha256"]["keygen-dot"] or any(p.is_symlink() for p in current.rglob("*")):
        raise RuntimeError("Current arithmetic differs from accepted EXP-006.")
    return {"baseline": base, "exp005": a["source_file_sha256"]["raw-error-ntt"], "exp006": observed}

def read_blob(name):
    if Path(name).is_absolute() or ".." in Path(name).parts:
        raise RuntimeError("Invalid source path.")
    result = subprocess.run(["git", "show", f"{EXP005_COMMIT}:implementation/kyber-optimised-ref/{name}"],
        cwd=ROOT, env={"PATH":"/usr/bin:/bin", "LC_ALL":"C", "GIT_OPTIONAL_LOCKS":"0"},
        capture_output=True, timeout=30, check=False)
    if result.returncode: raise RuntimeError(f"Cannot restore EXP-005: {name}")
    return result.stdout

def restore_exp005(directory, expected):
    directory.mkdir()
    for name, digest in expected.items():
        data = read_blob(name)
        if hashlib.sha256(data).hexdigest() != digest:
            raise RuntimeError(f"Historical source mismatch: {name}")
        target = directory / name
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("xb") as out: out.write(data)

def tool_snapshot(prefix):
    prefix = prefix.resolve()
    launcher = prefix / "bin/valgrind"
    library = prefix / "libexec/valgrind"
    env = {"PATH":"/usr/bin:/bin", "LC_ALL":"C", "VALGRIND_LIB":str(library)}
    result = subprocess.run([str(launcher),"--version"],env=env,capture_output=True,text=True,timeout=30)
    if result.returncode or result.stdout.strip() != "valgrind-3.22.0":
        raise RuntimeError("This protocol requires Valgrind 3.22.0; review a tool change before running.")
    paths = [launcher, prefix/"bin/valgrind.bin", prefix/"include/valgrind/valgrind.h", prefix/"include/valgrind/memcheck.h",
             library/"memcheck-amd64-linux", library/"vgpreload_core-amd64-linux.so",
             library/"vgpreload_memcheck-amd64-linux.so", Path("/usr/bin/objdump")]
    return {"version":result.stdout.strip(), "prefix":str(prefix), "library":str(library),
            "file_sha256":{str(p):metadata.sha256(p) for p in paths}}

def parse_report(path):
    root = ET.parse(path).getroot()
    if root.tag != "valgrindoutput" or root.findtext("tool") != "memcheck":
        raise RuntimeError("Not a Memcheck report.")
    if root.findtext("protocolversion") != "4" or root.findall("fatal_signal"):
        raise RuntimeError("Unsupported or aborted Memcheck report.")
    states = [x.findtext("state") for x in root.findall("status")]
    if not states or states[-1] != "FINISHED": raise RuntimeError("Incomplete XML report.")
    errors = [{"unique":x.findtext("unique"), "kind":x.findtext("kind"),
               "what":x.findtext("what") or x.findtext("xwhat/text"),
               "frames":[{"function":f.findtext("fn"), "file":f.findtext("file"),
                          "line":f.findtext("line")} for f in x.findall("stack/frame")],
               "origin":x.findtext("origin/what")} for x in root.findall("error")]
    counts = {x.findtext("unique"):int(x.findtext("count")) for x in root.findall("errorcounts/pair")}
    if set(counts) != {x["unique"] for x in errors} or any(n <= 0 for n in counts.values()):
        raise RuntimeError("Error count/context mismatch.")
    if root.findall("suppcounts/pair"): raise RuntimeError("Suppressed errors are not accepted.")
    return {"errors":errors, "error_contexts":len(errors), "error_occurrences":sum(counts.values()),
            "counts":counts, "finished":True}

def classify(label, mode, code, report, output):
    cases = 1 if label in CONTROLS else 8
    if not re.fullmatch(rf"path={re.escape(label)} mode={mode} cases={cases} checksum=[0-9]+\n", output):
        return "execution-error"
    expected = {"positive-branch":("UninitCondition","positive_branch"),
                "positive-address":("UninitValue","positive_address")}
    if mode == "marked" and label in expected:
        kind, fn = expected[label]
        if code != 99 or not report["errors"]: return "control-insensitive"
        if all(e["kind"] == kind and any((f["function"] or "").startswith(fn)
              for f in e["frames"]) for e in report["errors"]): return "control-detected"
        return "unexpected-control-diagnostic"
    if code == 0 and not report["errors"]: return "no-dependency-observed"
    if code == 99 and report["errors"]: return "diagnostic-detected"
    return "execution-error"

def execute(run_dir, snapshot, source_map, tool, args):
    compiler = snapshot["environment"]["available_compiler"]
    if compiler["version"] != "13.3.0": raise RuntimeError("Protocol compiler is GCC 13.3.0.")
    build = run_dir / "build"
    env = {"PATH":"/usr/bin:/bin", "LC_ALL":"C", "TMPDIR":str(build), "VALGRIND_LIB":tool["library"]}
    manifest = {"schema_version":1, "record_type":"dynamic-secret-flow", "experiment_id":args.experiment,
      "run_id":args.run, "status":"running", "source_commit":snapshot["provenance"]["source_commit"],
      "upstream_commit":metadata.PIN, "source_file_sha256":source_map,
      "restored_exp005_commit":EXP005_COMMIT, "accepted_inputs":INPUTS,
      "metadata_sha256":metadata.sha256(run_dir/"metadata.json"), "compiler":compiler,
      "tool":tool, "build_flags":list(FLAGS), "support_file_sha256":{n:metadata.sha256(ROOT/n) for n in SUPPORT},
      "process_environment":env, "invocation_arguments":sys.argv[1:],
      "protocol":{"variants":VARIANTS, "primary_candidate":"exp005", "secondary":"exp006",
        "paths":PATHS, "controls":CONTROLS, "patterns_per_path":8, "modes":["defined","marked"],
        "seed":1, "timeout_seconds_per_process":args.timeout, "positive_error_exit":99,
        "default_suppressions":False, "declassification":"test boundaries after complete target calls",
        "scope":"seven arithmetic path/operand-role cases and IND-CPA decryption; not whole KEM constant-time proof"},
      "steps":[], "executables":{}, "reports":[], "assembly":{}, "provenance_recheck":"not-run",
      "benchmark_executed":False, "statistical_leakage":"not-run"}
    validation.save_manifest(run_dir,manifest)
    dirs = {"baseline":validation.BASELINE, "exp005":build/"exp005-source",
            "exp006":ROOT/"implementation/kyber-optimised-ref"}
    def identity():
        validation.check_source_state(manifest["source_commit"], source_map["baseline"])
        if sources() != source_map or tool_snapshot(Path(tool["prefix"])) != tool:
            raise RuntimeError("Source or tools changed during testing.")
        for n,digest in manifest["support_file_sha256"].items():
            if metadata.sha256(ROOT/n) != digest: raise RuntimeError(f"Support changed: {n}")
        if metadata.sha256(Path(compiler["path"])) != compiler["sha256"]:
            raise RuntimeError("Compiler changed.")
        if dirs["exp005"].exists():
            observed = {p.relative_to(dirs["exp005"]).as_posix():metadata.sha256(p)
                        for p in dirs["exp005"].rglob("*") if p.is_file()}
            if observed != source_map["exp005"]: raise RuntimeError("Restored source changed.")
        for item in manifest["executables"].values():
            if metadata.sha256(run_dir/item["path"]) != item["sha256"]:
                raise RuntimeError("Executable changed.")
    try:
        build.mkdir(); (run_dir/"raw").mkdir()
        for n in (*SUPPORT,*INPUTS): metadata.git("cat-file","-e",f"{manifest['source_commit']}:{n}")
        identity()
        restore_exp005(dirs["exp005"], source_map["exp005"])
        for parameter,k in validation.PARAMETERS:
            for variant,number in VARIANTS.items():
                tag = f"{variant}-{parameter}"
                print(f"Checking Kyber{parameter} {variant}: controls and eight path/role cases...", flush=True)
                exe = build/f"flow-{tag}"
                cmd = [compiler["path"],*FLAGS,f"-DKYBER_K={k}",f"-DFLOW_VARIANT={number}",
                       "-I",str(dirs[variant]),"-I",str(Path(tool["prefix"])/"include"),
                       *validation.SOURCES[:-1],str(HARNESS),"-o",str(exe)]
                if not validation.run_step(run_dir,manifest,f"build-{tag}",cmd,dirs[variant],env,args.timeout):
                    raise RuntimeError("Build failed; inspect logs.")
                manifest["executables"][tag] = {"path":str(exe.relative_to(run_dir)),"sha256":metadata.sha256(exe)}
                symbols = [f"pqcrystals_kyber{parameter}_ref_{s}" for s in SYMBOLS]
                if number == 6: symbols.append(f"pqcrystals_kyber{parameter}_ref_polyvec_basemul_acc_keygen")
                symbols.extend(("positive_branch","positive_address","negative_control"))
                for symbol in symbols:
                    label = f"assembly-{tag}-{symbol}"
                    if not validation.run_step(run_dir,manifest,label,["/usr/bin/objdump","-d",f"--disassemble={symbol}",str(exe)],ROOT,env,args.timeout):
                        raise RuntimeError("Assembly extraction failed.")
                    step = manifest["steps"][-1]
                    if f"<{symbol}>:" not in (run_dir/step["stdout"]).read_text():
                        raise RuntimeError(f"Missing symbol: {symbol}")
                    manifest["assembly"][f"{tag}/{symbol}"] = step["stdout"]
                # Defined twins distinguish real uninitialised memory from deliberate marking.
                for label in (*CONTROLS,*PATHS):
                    for mode in ("defined","marked"):
                        name = f"flow-{tag}-{label}-{mode}"
                        xml = run_dir/"raw"/(name+".xml")
                        cmd = [str(Path(tool["prefix"])/"bin/valgrind"),"--tool=memcheck",
                               "--xml=yes",f"--xml-file={xml}","--error-exitcode=99",
                               "--track-origins=yes","--undef-value-errors=yes","--error-limit=no",
                               "--default-suppressions=no","--leak-check=no",str(exe),label,mode]
                        validation.run_step(run_dir,manifest,name,cmd,ROOT,env,args.timeout)
                        step = manifest["steps"][-1]
                        report = parse_report(xml)
                        outcome = classify(label,mode,step["exit_code"],report,(run_dir/step["stdout"]).read_text())
                        manifest["reports"].append({"variant":variant,"parameter":parameter,"path":label,"mode":mode,
                            "step":name,"xml":str(xml.relative_to(run_dir)),"xml_sha256":metadata.sha256(xml),
                            "outcome":outcome,**report})
                        validation.save_manifest(run_dir,manifest)
                        if label in CONTROLS and outcome not in ("control-detected","no-dependency-observed"):
                            raise RuntimeError("Sensitivity control failed; candidate conclusions are inconclusive.")
                        if label not in CONTROLS and outcome == "execution-error":
                            raise RuntimeError("Execution error; preserve this attempt.")
        identity(); manifest["provenance_recheck"] = "pass"
        manifest["status"] = "completed"
        manifest["assessment"] = ("diagnostics-require-review" if any(r["outcome"] == "diagnostic-detected"
                                 for r in manifest["reports"]) else "no-dependency-observed-in-tested-paths")
    except KeyboardInterrupt:
        manifest["status"] = "interrupted"
    except (OSError,RuntimeError,ValueError,ET.ParseError,subprocess.TimeoutExpired) as exc:
        manifest["status"] = "failed"; manifest["error"] = str(exc)
    finally:
        validation.save_manifest(run_dir,manifest)
    print(f"Secret-flow status: {manifest['status']}; assessment: {manifest.get('assessment','inconclusive')}")
    print(f"Record: {run_dir}/manifest.json")
    print("No performance or statistical timing-leakage measurements were collected.")
    return 0 if manifest["status"] == "completed" else 1

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--experiment",default="EXP-007"); p.add_argument("--run",required=True)
    p.add_argument("--compiler",default="gcc"); p.add_argument("--timeout",type=int,default=120)
    p.add_argument("--valgrind-prefix",type=Path,default=Path("/usr"))
    args = p.parse_args()
    if sys.platform != "linux" or args.timeout <= 0: p.error("Linux and a positive timeout are required.")
    if args.experiment != "EXP-007": p.error("This protocol is EXP-007.")
    source_map = sources(); tool = tool_snapshot(args.valgrind_prefix)
    command = [sys.executable,"-B",str(ROOT/"scripts/collect_run_metadata.py"),
               "--experiment",args.experiment,"--run",args.run,"--variant","secret-flow",
               "--compiler",args.compiler]
    result = subprocess.run(command,cwd=ROOT,check=False)
    if result.returncode: return result.returncode
    run_dir = ROOT/"results"/args.experiment/args.run
    return execute(run_dir,json.loads((run_dir/"metadata.json").read_text()),source_map,tool,args)

if __name__ == "__main__":
    signal.signal(signal.SIGTERM,validation.interrupt_requested)
    try: sys.exit(main())
    except (OSError,RuntimeError,ValueError,subprocess.TimeoutExpired) as exc:
        print(f"ERROR: {exc}. Preserve any created run; use a new ID to retry.",file=sys.stderr); sys.exit(1)
