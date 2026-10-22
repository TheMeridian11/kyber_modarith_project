#!/usr/bin/env python3
"""Generate the audited EXP-007 coverage matrix, not a security score."""
import csv,hashlib,json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
ROOT=Path(__file__).resolve().parents[1]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    source=ROOT/'notes/evidence/ACT-0017/exp-007-run-0001-review.json'
    review=json.loads(source.read_text());raw=ROOT/'results/EXP-007/RUN-0001/manifest.json'
    if sha(raw)!=review['manifest_sha256'] or review['status']!='accepted-with-bounded-claims':raise RuntimeError('Unaccepted/mismatched result')
    paths=['basemul','basemul-first','dot','dot-first','inverse','error-path','keygen-dot','indcpa-dec','negative-control','positive-branch','positive-address']
    variants=['baseline','exp005','exp006'];params=[512,768,1024]
    out=ROOT/'analysis/figures/ACT-0017';out.mkdir(parents=True,exist_ok=True)
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'svg.hashsalt':'kyber-act0017','pdf.fonttype':42})
    fig,ax=plt.subplots(figsize=(10,6.8));data=[]
    for y,path in enumerate(paths):
        for x,(v,p) in enumerate((v,p) for v in variants for p in params):
            row=next(t for t in review['reports'] if t['variant']==v and t['parameter']==p and t['path']==path and t['mode']=='marked')
            detected=row['outcome']=='control-detected';expected=path.startswith('positive-')
            if detected!=expected:raise RuntimeError('Unexpected matrix outcome')
            ax.add_patch(plt.Rectangle((x-.47,y-.44),.94,.88,color='#e7ae66' if detected else '#cae4ef',lw=0))
            ax.text(x,y,'Detected' if detected else 'Quiet',ha='center',va='center',fontsize=8.5)
            data.append(row)
    ax.set_xlim(-.5,8.5);ax.set_ylim(10.5,-1.1);ax.set_xticks(range(9),[str(p) for v in variants for p in params]);ax.xaxis.tick_top()
    ax.set_yticks(range(11),['Base multiply: second secret','Base multiply: first secret','Vector dot: second secret','Vector dot: first secret','Inverse NTT','Error NTT + final reduction','Keygen dot + final reduction','IND-CPA decryption','Negative control','Positive branch control','Positive address control'])
    ax.tick_params(length=0);ax.spines[['top','right','bottom','left']].set_visible(False)
    for x,label in [(1,'Original reference'),(4,'EXP-005'),(7,'EXP-006')]:ax.text(x,-.82,label,ha='center',weight='bold')
    ax.axhline(7.5,color='#666666',lw=.8);fig.suptitle('Dynamic secret-flow checks: exercised paths and sensitivity controls',fontsize=14,y=.99)
    fig.text(.5,.07,'All 72 marked target processes and 72 defined twins were quiet. All 18 marked positive controls were detected.\nEach target process used eight fixtures; base multiplication exercised all 128 pairs per fixture.',ha='center',fontsize=9)
    fig.text(.5,.018,'Quiet means no marked-secret branch/address dependency observed on these paths.\nThis is not a statistical timing result or proof of whole-program constant time.',ha='center',fontsize=9,weight='bold')
    fig.tight_layout(rect=(0,.13,1,.95))
    files=[]
    for ext in ('png','svg','pdf'):
        p=out/('exp007-secret-flow.'+ext);md={'Date':None} if ext=='svg' else {'CreationDate':None,'ModDate':None} if ext=='pdf' else {}
        fig.savefig(p,dpi=300,bbox_inches='tight',metadata=md)
        if ext=='svg':p.write_text('\n'.join(l.rstrip(' \t') for l in p.read_text().splitlines())+'\n')
        files.append(p)
    plt.close(fig)
    table=out/'exp007-secret-flow.csv'
    with table.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(data[0]),lineterminator='\n');w.writeheader();w.writerows(data)
    files.append(table)
    provenance={'activity_id':'ACT-0017','analysis_sha256':sha(Path(__file__)),'inputs':{str(p.relative_to(ROOT)):sha(p) for p in (source,raw)},'outputs':{p.name:sha(p) for p in files},'matplotlib':matplotlib.__version__,'meaning':'Executed marked-mode process outcomes, not a quantitative security score.'}
    (out/'provenance.json').write_text(json.dumps(provenance,indent=2,sort_keys=True)+'\n')
    print('Saved EXP-007 coverage figure and data')
if __name__=='__main__':main()
