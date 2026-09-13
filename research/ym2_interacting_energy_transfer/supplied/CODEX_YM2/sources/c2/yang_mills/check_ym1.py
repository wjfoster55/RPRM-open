"""One Maxwell-mode calibration: exact retained update and finite-box control.

No prior photon/cube replay, ODE solver, spectral diagonalization or model fit.
"""
import argparse, hashlib, json, math, sys
from fractions import Fraction as F
from pathlib import Path

def retain(Q,P,k):return (k*k*Q*Q/2,P*P/2,k*Q*P)
def evolve(Q,P,k,c,s):return (Q*c+P*s/k,P*c-k*Q*s)
def descend(b,e,z,c,s):return (b*c*c+e*s*s+z*s*c,e*c*c+b*s*s-z*s*c,z*(c*c-s*s)+2*(e-b)*s*c)
def serial(v):
    if isinstance(v,F):return str(v)
    if isinstance(v,dict):return {k:serial(x) for k,x in v.items()}
    if isinstance(v,(tuple,list)):return [serial(x) for x in v]
    return v

def check():
    k,c,s=F(1),F(3,5),F(4,5)
    states=[('plus',F(1),F(1)),('minus',F(1),F(-1)),('zero',F(0),F(0)),('pure_electric',F(0),F(1)),('antipode_plus',F(-1),F(-1))]
    rows=[]
    for name,Q,P in states:
        initial=retain(Q,P,k);QP=evolve(Q,P,k,c,s)
        actual=retain(*QP,k);predicted=descend(*initial,c,s)
        assert actual==predicted
        assert actual[0]+actual[1]==initial[0]+initial[1]<=2
        assert actual[2]**2==4*actual[0]*actual[1]
        assert descend(*actual,c,-s)==initial
        assert evolve(*QP,k,c,-s)==(Q,P)
        # Composition is checked against direct full-state evolution for the
        # same fixed phase twice; proof in the bridge covers arbitrary times.
        assert descend(*actual,c,s)==retain(*evolve(Q,P,k,c*c-s*s,2*s*c),k)
        rows.append({'id':name,'state':(Q,P),'retained_initial':initial,'state_after':QP,'retained_after':actual,'pass':True})
    assert rows[0]['retained_initial'][:2]==rows[1]['retained_initial'][:2]
    assert rows[0]['retained_after'][0]==F(49,50) and rows[1]['retained_after'][0]==F(1,50)
    assert rows[0]['retained_initial']==rows[4]['retained_initial']
    assert rows[0]['retained_after']==rows[4]['retained_after']

    # Independent direct field sampling: no use of retained updater. For this
    # band-limited single mode, 16 equispaced nodes integrate sin²/cos² exactly
    # in real arithmetic. Float error is checked against an explicit tolerance.
    L=2*math.pi;V=L**3;alpha=math.sqrt(2/V);N=16;tol=2e-12
    field_rows=[]
    for row in rows[:2]:
        for label,(Q,P) in [('initial',row['state']),('after',row['state_after'])]:
            Q,P=float(Q),float(P)
            e_terms=[];b_terms=[];transfer=[]
            for j in range(N):
                x=L*j/N
                Ey=-alpha*P*math.cos(x)
                Bz=-alpha*Q*math.sin(x)
                curlB_y=alpha*Q*math.cos(x)
                e_terms.append(Ey*Ey/2);b_terms.append(Bz*Bz/2)
                transfer.append(-Ey*curlB_y)
            measured=[V*math.fsum(b_terms)/N,V*math.fsum(e_terms)/N,V*math.fsum(transfer)/N]
            reference=[Q*Q/2,P*P/2,Q*P]
            error=max(abs(x-y) for x,y in zip(measured,reference))
            assert error<=tol
            field_rows.append({'state':row['id'],'time':label,'UB_UE_transfer':measured,'max_abs_error':error,'pass':True})
    boxes=[{'L_over_2pi_length_unit':m,'gap_in_hbar_c_over_length_unit':str(F(1,m))} for m in (1,2,4,8)]
    assert all(F(boxes[i+1]['gap_in_hbar_c_over_length_unit'])==F(boxes[i]['gap_in_hbar_c_over_length_unit'])/2 for i in range(3))
    return serial({'status':'PASS','evidence_grade':'NEW_BOUNDED_DEVELOPMENT_CALIBRATION',
                   'definition':'fixed k=1, c=3/5,s=4/5; five preselected amplitude cases, two field witnesses, four finite-box entries',
                   'exact_arithmetic':'fractions.Fraction; no floating solver','rows':rows,
                   'field_sampling':{'nodes':N,'absolute_tolerance':tol,'rows':field_rows},
                   'finite_box_control':boxes,
                   'analytic_limit':'For any epsilon>0 choose integer m>1/epsilon; gap=1/m<epsilon. The table alone is not the proof.',
                   'not_calculated':['interacting non-Abelian evolution','quantum interacting spectrum','continuum/thermodynamic mass gap','old cube/photon calibration'],
                   'entrypoint_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'python':sys.version})

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    if args.output.exists():raise SystemExit('Refusing to overwrite receipt')
    result=check();args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    print(json.dumps({'status':result['status'],'exact_states':len(result['rows']),'field_samples':len(result['field_sampling']['rows']),'output':str(args.output)}))
