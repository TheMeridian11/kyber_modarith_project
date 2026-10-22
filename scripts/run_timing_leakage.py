#!/usr/bin/env python3
"""EXP-008: collect the committed fixed-budget statistical timing screen."""
import argparse
import gzip
import hashlib
import json
import os
import signal
import subprocess
import sys
from pathlib import Path
import collect_run_metadata as metadata
import run_validation as validation
import run_incremental_comparison as assembly
import analyse_timing_leakage as analysis
ROOT=metadata.ROOT
PROTOCOL=ROOT/"tests/timing_leakage_protocol.json"
SUPPORT=("scripts/run_timing_leakage.py","scripts/analyse_timing_leakage.py","tests/test_timing_leakage.c",
 "tests/timing_leakage_protocol.json","scripts/collect_run_metadata.py","scripts/run_validation.py",
 "scripts/run_incremental_comparison.py","notes/experiments/EXP-008-timing-leakage.md",
 "tests/reference/dudect/dudect.h","tests/reference/dudect/LICENSE")
SYMBOLS=("basemul","polyvec_basemul_acc_montgomery","invntt","ntt","poly_ntt","poly_tomont",
 "poly_reduce","poly_add","indcpa_dec","montgomery_reduce","barrett_reduce")
WRAPPERS=("basemul_path","dot_path","inverse_path","error_path","keygen_path","decrypt_path",
 "negative_control","positive_control","main")

def load_protocol():
    p=json.loads(PROTOCOL.read_text())
    for name,h in {**p['accepted_inputs'],**p['reference_sha256']}.items():
        if metadata.sha256(ROOT/name)!=h:raise RuntimeError(f"Pinned input changed: {name}")
    if p['samples_per_process']!=50000 or p['looks']!=[25000,50000] or p['threshold_abs_t']!=analysis.THRESHOLD:
        raise RuntimeError("Protocol/analysis budget mismatch; review changes before collection.")
    return p

def source_maps():
    a=json.loads((ROOT/'results/EXP-003/RUN-0001/manifest.json').read_text())
    b=json.loads((ROOT/'results/EXP-005/RUN-0001/manifest.json').read_text())
    for m in (a,b):
        if m['status']!='completed' or m['provenance_recheck']!='pass':raise RuntimeError('Validation incomplete')
    base=validation.source_snapshot()
    if base!=a['source_file_sha256']['baseline'] or base!=b['source_file_sha256']['baseline']:raise RuntimeError('Original source differs')
    return {'baseline':base,'exp003':a['source_file_sha256']['staged-invntt'],'exp005':b['source_file_sha256']['raw-error-ntt']}

def read_blob(commit,name):
    if Path(name).is_absolute() or '..' in Path(name).parts:raise RuntimeError('Invalid source path')
    r=subprocess.run(['git','show',f'{commit}:implementation/kyber-optimised-ref/{name}'],cwd=ROOT,
        env={'PATH':'/usr/bin:/bin','LC_ALL':'C','GIT_OPTIONAL_LOCKS':'0'},capture_output=True,timeout=30)
    if r.returncode:raise RuntimeError('Cannot restore historical source')
    return r.stdout

def restore(directory,commit,files):
    directory.mkdir()
    for name,h in files.items():
        data=read_blob(commit,name)
        if hashlib.sha256(data).hexdigest()!=h:raise RuntimeError('Historical source mismatch')
        dest=directory/name;dest.parent.mkdir(parents=True,exist_ok=True)
        with dest.open('xb') as out:out.write(data)

def execute(run_dir,snapshot,p,args):
    compiler=snapshot['environment']['available_compiler']
    if compiler['version']!=p['compiler_version']:raise RuntimeError('Unreviewed compiler version')
    accepted_assembly=json.loads((ROOT/'notes/evidence/ACT-0017/exp-007-run-0001-review.json').read_text())['assembly_normalised']
    source=source_maps();build=run_dir/'build';env={'PATH':'/usr/bin:/bin','LC_ALL':'C','TMPDIR':str(build)}
    m={'schema_version':1,'record_type':p['record_type'],'experiment_id':args.experiment,'run_id':args.run,
       'status':'running','source_commit':snapshot['provenance']['source_commit'],'upstream_commit':metadata.PIN,
       'metadata_sha256':metadata.sha256(run_dir/'metadata.json'),'protocol':p,'compiler':compiler,
       'source_file_sha256':source,'support_file_sha256':{n:metadata.sha256(ROOT/n) for n in SUPPORT},
       'tool_sha256':{'/usr/bin/objdump':metadata.sha256(Path('/usr/bin/objdump'))},
       'build_flags':list(validation.FLAGS),'invocation_arguments':sys.argv[1:],'process_environment':env,
       'steps':[],'executables':{},'assembly':{},'measurements':[],'provenance_recheck':'not-run',
       'interpretation':'A signal requires diagnosis; no signal is not proof of constant time.'}
    dirs={'baseline':validation.BASELINE,'exp003':build/'exp003-source','exp005':build/'exp005-source'}
    def identity():
        validation.check_source_state(m['source_commit'],source['baseline'])
        if source_maps()!=source or load_protocol()!=p:raise RuntimeError('Inputs changed')
        for name,h in m['support_file_sha256'].items():
            if metadata.sha256(ROOT/name)!=h:raise RuntimeError(f'Support changed: {name}')
        for name,h in {**m['tool_sha256'],compiler['path']:compiler['sha256']}.items():
            if metadata.sha256(Path(name))!=h:raise RuntimeError('Tool changed')
        for v in ('exp003','exp005'):
            if dirs[v].exists():
                actual={q.relative_to(dirs[v]).as_posix():metadata.sha256(q) for q in dirs[v].rglob('*') if q.is_file()}
                if actual!=source[v]:raise RuntimeError('Restored source changed')
        for e in m['executables'].values():
            if metadata.sha256(run_dir/e['path'])!=e['sha256']:raise RuntimeError('Executable changed')
    def step(label,cmd,cwd=ROOT):
        if not validation.run_step(run_dir,m,label,cmd,cwd,env,p['timeout_seconds_per_process']):
            raise RuntimeError(f'Execution failed: {label}')
        return m['steps'][-1]
    try:
        build.mkdir();(run_dir/'raw').mkdir();(run_dir/'derived').mkdir()
        for name in (*SUPPORT,*p['accepted_inputs']):metadata.git('cat-file','-e',f"{m['source_commit']}:{name}")
        identity()
        for v in ('exp003','exp005'):restore(dirs[v],p['restoration_commits'][v],source[v])
        for parameter,k in validation.PARAMETERS:
            for v,number in p['variants'].items():
                tag=f'{v}-{parameter}';exe=build/f'leak-{tag}'
                print(f'Building Kyber{parameter}: {v}...',flush=True)
                step('build-'+tag,[compiler['path'],*validation.FLAGS,f'-DKYBER_K={k}',f'-DLEAK_VARIANT={number}',
                     '-I',str(dirs[v]),*validation.SOURCES[:-1],str(ROOT/'tests/test_timing_leakage.c'),'-o',str(exe)],dirs[v])
                m['executables'][tag]={'path':str(exe.relative_to(run_dir)),'sha256':metadata.sha256(exe)}
                for sym in [f'pqcrystals_kyber{parameter}_ref_{s}' for s in SYMBOLS]+list(WRAPPERS):
                    s=step('assembly-'+tag+'-'+sym,['/usr/bin/objdump','-d','--disassemble='+sym,str(exe)])
                    text=(run_dir/s['stdout']).read_text();record=assembly.assembly_record(text,sym)
                    if not record['instructions']:raise RuntimeError('Missing assembly body')
                    if sym.startswith('pqcrystals_'):
                        ref=(tag+'/'+sym).replace('exp003-','exp005-')
                        if record!=accepted_assembly[ref]:raise RuntimeError('Production assembly differs from accepted normal code: '+ref)
                    m['assembly'][tag+'/'+sym]={'path':s['stdout'],'normalised':record}
        # Reverse variant order in repetition 2; seeds remain paired across builds.
        for rep,seed in enumerate(p['seeds'],1):
            variants=list(p['variants']);variants=variants if rep==1 else variants[::-1]
            for parameter,_ in validation.PARAMETERS:
                for v in variants:
                    tag=f'{v}-{parameter}';exe=run_dir/m['executables'][tag]['path']
                    print(f'Measuring repetition {rep}, Kyber{parameter}, {v}: controls and 16 path/profile cells...',flush=True)
                    cases=[(c,0) for c in p['controls']]+[(path,prof) for path in p['paths'] for prof in range(2)]
                    for path,profile in cases:
                        label=f'timing-{tag}-rep{rep}-{path}-profile{profile}'
                        s=step(label,[str(exe),path,str(profile),str(p['samples_per_process']),str(seed),str(args.cpu)])
                        completion=json.loads((run_dir/s['stderr']).read_text())
                        expected={'path':path,'profile':profile,'samples':p['samples_per_process'],
                            'calibration':p['calibration_per_process'],'warmup':p['warmup_per_process'],'seed':seed,'cpu':args.cpu}
                        if any(completion.get(k)!=val for k,val in expected.items()) or not isinstance(completion.get('checksum'),int):
                            raise RuntimeError('Incomplete/mismatched harness record')
                        raw=run_dir/s['stdout'];zipped=raw.with_suffix('.bin.gz')
                        data=raw.read_bytes()
                        with zipped.open('xb') as out:out.write(gzip.compress(data,mtime=0))
                        if gzip.decompress(zipped.read_bytes())!=data:raise RuntimeError('Compression identity failed')
                        original=s['stdout'];s['uncompressed_stdout_sha256']=s.pop('stdout_sha256')
                        s['stdout']=zipped.relative_to(run_dir).as_posix();s['stdout_sha256']=metadata.sha256(zipped)
                        s['stdout_encoding']='gzip; KTL00801 + repeated little-endian <QIIB records'
                        s['original_stdout_path']=original
                        validation.save_manifest(run_dir,m);raw.unlink() # Exact lossless archive replaces temporary stream.
                        result=analysis.analyse(zipped,p['samples_per_process'],p['minimum_per_class_per_view'])
                        control=path in p['controls']
                        control_ok=result['adequate'] and (any(x['flag'] for x in result['statistics'] if x['view']=='raw-mean' and x['look']==p['samples_per_process']) if path=='positive-control' else not result['flag']) if control else None
                        item={'variant':v,'parameter':parameter,'repetition':rep,'path':path,'profile':profile,
                            'raw':s['stdout'],'raw_sha256':s['stdout_sha256'],'completion':completion,'control_ok':control_ok,**result}
                        m['measurements'].append(item);validation.save_manifest(run_dir,m)
        identity();m['provenance_recheck']='pass';m['status']='completed'
        controls=[x for x in m['measurements'] if x['path'] in p['controls']]
        targets=[x for x in m['measurements'] if x['path'] not in p['controls']]
        m['assessment']=('inconclusive-controls-or-coverage' if not all(x['control_ok'] for x in controls) or not all(x['adequate'] for x in targets)
                         else 'timing-differences-require-review' if any(x['flag'] for x in targets) else 'no-difference-detected-within-budget')
        summary=run_dir/'derived/summary.json';summary.write_text(json.dumps({'assessment':m['assessment'],'measurements':m['measurements']},indent=2,allow_nan=False)+'\n')
        m['derived']={'summary':{'path':str(summary.relative_to(run_dir)),'sha256':metadata.sha256(summary)}}
    except KeyboardInterrupt:m['status']='interrupted'
    except (OSError,RuntimeError,ValueError,subprocess.TimeoutExpired) as exc:m['status']='failed';m['error']=str(exc)
    finally:validation.save_manifest(run_dir,m)
    print(f"Timing-leakage status: {m['status']}; assessment: {m.get('assessment','inconclusive')}")
    print(f'Record: {run_dir}/manifest.json')
    return 0 if m['status']=='completed' else 1

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--experiment',default='EXP-008')
    parser.add_argument('--run',required=True);parser.add_argument('--cpu',type=int,default=0);parser.add_argument('--compiler',default='gcc')
    args=parser.parse_args();p=load_protocol()
    if sys.platform!='linux' or args.experiment!='EXP-008' or args.cpu!=p['cpu']:parser.error('Committed protocol requires Linux, EXP-008 and CPU 0')
    source_maps()
    result=subprocess.run([sys.executable,'-B',str(ROOT/'scripts/collect_run_metadata.py'),'--experiment',args.experiment,
        '--run',args.run,'--variant','timing-leakage','--compiler',args.compiler],cwd=ROOT)
    if result.returncode:return result.returncode
    run_dir=ROOT/'results'/args.experiment/args.run
    return execute(run_dir,json.loads((run_dir/'metadata.json').read_text()),p,args)
if __name__=='__main__':
    signal.signal(signal.SIGTERM,validation.interrupt_requested)
    try:sys.exit(main())
    except (OSError,RuntimeError,ValueError,subprocess.TimeoutExpired) as exc:
        print(f'ERROR: {exc}. Preserve any attempt and use a new run ID.',file=sys.stderr);sys.exit(1)
