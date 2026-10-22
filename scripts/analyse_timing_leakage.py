#!/usr/bin/env python3
"""EXP-008 raw-stream validation and fixed-look Welch screening; no p-value claim."""
import gzip
import math
import statistics
import struct
from pathlib import Path
RECORD=struct.Struct("<QIIB")
THRESHOLD=10.0
CALIBRATION=2000

def welch(x,y):
    if min(len(x),len(y))<2: raise ValueError("Too few observations")
    mx,my=statistics.fmean(x),statistics.fmean(y)
    vx,vy=statistics.variance(x,mx),statistics.variance(y,my)
    se2=vx/len(x)+vy/len(y)
    t=(mx-my)/math.sqrt(se2) if se2 else (0.0 if mx==my else None)
    return {"n0":len(x),"n1":len(y),"mean0":mx,"mean1":my,"variance0":vx,"variance1":vy,
            "difference0_minus1":mx-my,"standard_error":math.sqrt(se2),"t":t,
            "flag":t is None or abs(t)>THRESHOLD}

def analyse(path,samples,minimum=10000):
    path=Path(path)
    data=gzip.decompress(path.read_bytes()) if path.suffix==".gz" else path.read_bytes()
    if data[:8]!=b"KTL00801" or len(data)!=8+17*(CALIBRATION+samples): raise ValueError("Truncated/wrong raw stream")
    rows=list(RECORD.iter_unpack(data[8:]))
    if any(c not in (0,1) for _,_,_,c in rows):raise ValueError("Invalid class")
    for i in range(0,len(rows),1000):
        if sum(c for _,_,_,c in rows[i:i+1000])!=500:raise ValueError("Unbalanced class block")
    valid=lambda r:r[0]>0 and r[1]==r[2]
    rejected=[i for i,r in enumerate(rows) if not valid(r)]
    calibration=sorted(r[0] for r in rows[:CALIBRATION] if valid(r))
    if len(calibration)<1900:raise ValueError("Insufficient valid calibration")
    calibration_p99=calibration[math.ceil(.99*len(calibration))-1]
    stats=[]
    for look in (samples//2,samples):
        current=[r for r in rows[CALIBRATION:CALIBRATION+look] if valid(r)]
        center=statistics.fmean(r[0] for r in current) if current else 0
        pooled=sorted(r[0] for r in current)
        cutoff=pooled[math.ceil(.99*len(pooled))-1] if pooled else 0
        for view in ("raw-mean","crop99-mean","second-moment"):
            selected=[r for r in current if view!="crop99-mean" or r[0]<=cutoff]
            groups=[[float((r[0]-center)**2 if view=="second-moment" else r[0]) for r in selected if r[3]==c] for c in (0,1)]
            item={"look":look,"view":view,"adequate":min(map(len,groups))>=minimum,"crop99_cutoff":cutoff}
            if min(map(len,groups))>=2:item.update(welch(*groups))
            else:item.update({"n0":len(groups[0]),"n1":len(groups[1]),"t":None,"flag":False})
            stats.append(item)
    adequate=all(s['adequate'] for s in stats) and len(rejected)<=.01*len(rows)
    return {"samples":samples,"calibration":CALIBRATION,"timer_units":"TSC ticks, not core cycles",
        "record_count":len(rows),"excluded_indices":rejected,"calibration_p99_reference_only":calibration_p99,"threshold":THRESHOLD,
        "statistics":stats,"adequate":adequate,"flag":any(s['flag'] for s in stats),
        "assessment":"inconclusive" if not adequate else "timing-difference-requires-review" if any(s['flag'] for s in stats) else "no-difference-detected-within-budget"}
