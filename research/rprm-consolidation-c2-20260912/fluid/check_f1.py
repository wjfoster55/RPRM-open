"""Bounded source-result arithmetic and the original two-state dynamic witness.

No panel regeneration, tuning, oracle self-test, or skip-engine benchmark.
Requires standard-library Python and Node. Writes only the requested receipt.
"""
import argparse, hashlib, json, math, re, subprocess, tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent

def check():
    p12 = HERE/'sources/PR12/noita_lab'
    p13 = HERE/'sources/PR13/broadphase_lab'
    raw = p13/'artifacts/broadphase_results.json'
    d = json.loads(raw.read_text(encoding='utf-8'))  # original includes Infinity
    n = d['n_records']
    for key in ('naive', 'pure_ca', 'ca_sleeping', 'P'):
        r = d[key]
        assert r['n']==n==sum(r[k] for k in ('tp','fp','fn','tn'))
        assert r['tp']+r['fn']==d['n_nochange']
        assert math.isclose(r['cert_rate'], (r['tp']+r['fp'])/n)
        assert math.isclose(r['fp_rate'], r['fp']/n)
        for count in ('tp','fp','fn','tn','n'):
            assert sum(f[key][count] for f in d['per_family'].values())==r[count]
    hh=d['head_to_head']
    assert d['P']['tp']-d['ca_sleeping']['tp']==hh['p_only']-hh['cas_only']
    assert sum(d['p_only_families'].values())==hh['p_only']==5754
    assert hh['cas_only']==589
    ratio=d['P']['cert_rate']/d['ca_sleeping']['cert_rate']
    assert math.isclose(ratio,hh['ratio'])

    text=(p12/'artifacts/dynamic_frontier_results.md').read_text(encoding='utf-8')
    rows=re.findall(r'^\| (8|10|12) \| (140|180|220) \| (\d+) \| (\d+) \| (\d+) \|',text,re.M)
    assert len(rows)==9
    disagree=sum(int(a)*int(b) for _,_,_,a,b in rows)
    pairs=sum(int(c)*(int(c)-1)//2 for _,_,c,_,_ in rows)
    assert (disagree,pairs)==(84,144)
    wi=(p12/'artifacts/witnessed_invalidation_table.md').read_text(encoding='utf-8')
    timers=re.findall(r'^\| (basin|utube|dam|stress) \| (\d+) \| (\d+) \| (\d+) \| (\d+) \|$',wi,re.M)
    assert len(timers)==4
    assert sum(int(r[2]) for r in timers)==490
    assert sum(int(r[1]) for r in timers)==0
    assert sum(int(r[4]) for r in timers)==0

    # Independent standard-library transcription of the pinned initializer.
    W,H,V,dx,floor,crest_y=64,48,180,32,46,36
    walls=[int(x in (0,W-1) or y in (0,H-1) or (x==dx and crest_y<=y<=floor)) for y in range(H) for x in range(W)]
    monitor=[y*W+x for y in range(1,H-1) for x in range(dx+1,W-1)]
    cell_orders={'tall':[(y,x) for y in range(1,floor+1) for x in range(dx-6,dx)],
                 'flat':[(y,x) for y in range(floor,0,-1) for x in range(1,dx)]}
    outcomes={}
    with tempfile.TemporaryDirectory(prefix='f1-witness-') as tmp:
        for name,cells in cell_orders.items():
            mass=[0]*(W*H)
            for y,x in cells[:V]: mass[y*W+x]=1
            assert sum(mass)==V and all(not(w and m) for w,m in zip(walls,mass))
            spec={'W':W,'H':H,'walls':walls,'mass':mass,'model':'B','steps':300,'monitor':monitor,'thresh':0.5,'snapshotSteps':[]}
            sp=Path(tmp)/f'{name}.json';op=Path(tmp)/f'{name}-out.json'
            sp.write_text(json.dumps(spec),encoding='utf-8')
            subprocess.run(['node',str(p12/'experiments/dynamic_frontier_sim.js'),str(sp),str(op)],check=True,capture_output=True,text=True)
            out=json.loads(op.read_text())
            assert out['totalMass']==V
            outcomes[name]={k:out[k] for k in ('Qdyn','firstBreach','maxMonitored','finalMonitored','totalMass','series')}
            outcomes[name]['initial_occupied_y_range']=[min(y for y,x in cells[:V]),max(y for y,x in cells[:V])]
            outcomes[name]['input_sha256']=hashlib.sha256(sp.read_bytes()).hexdigest()
    assert (outcomes['tall']['Qdyn'],outcomes['tall']['firstBreach'],outcomes['tall']['maxMonitored'])==(1,11,22)
    assert (outcomes['flat']['Qdyn'],outcomes['flat']['firstBreach'],outcomes['flat']['maxMonitored'])==(0,-1,0)
    return {'status':'PASS','grade':'DEVELOPMENT_SOURCE_RECONCILIATION_AND_TWO_STATE_REPLAY',
            'broadphase':{'saved_aggregate_sha256':hashlib.sha256(raw.read_bytes()).hexdigest(),'n_records':n,'P_tp':d['P']['tp'],'comparator_tp':d['ca_sleeping']['tp'],'certification_rate_ratio':ratio,'p_only':5754,'comparator_only':589,'raw_per_frame_records_available':False},
            'saved_dynamic_panel_arithmetic':{'classes':9,'disagree':disagree,'pairs':pairs,'full_panel_rerun':False},
            'saved_invalidation_arithmetic':{'settled_timer_reverifies':490,'active_timer_refloods':0,'reported_unwitnessed':0,'scenario_rerun':False},
            'fresh_dynamic_witness':outcomes,
            'limits':['Pinned model B only; no physical validation.','Quasistatic solver not rerun.','Historical aggregate consistency is not raw-record independent verification.','No performance or universal soundness conclusion.']}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    if args.output.exists(): raise SystemExit('Refusing to overwrite receipt')
    result=check();args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    print(json.dumps({'status':result['status'],'new_rollouts':2,'saved_panel_arithmetic':'PASS','output':str(args.output)},indent=2))
