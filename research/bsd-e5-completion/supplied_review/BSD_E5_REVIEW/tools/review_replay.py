"""Compare documented result fields and independently check delivered readbacks."""
from fractions import Fraction as Q
from pathlib import Path
import argparse,json,hashlib


def check(x,msg):
    if not x:raise ValueError(msg)
def point(x):
    if x=='O':return None
    p=(Q(x['x']),Q(x['y']))
    check(p[1]**2==p[0]**3-25*p[0],'off-curve decoded point');return p
K={'O':None,'T0':(Q(0),Q(0)),'Tplus':(Q(5),Q(0)),'Tminus':(Q(-5),Q(0))}
P=(Q(-4),Q(6))
def add(p,q):
    if p is None:return q
    if q is None:return p
    x,y=p;u,v=q
    if x==u and y==-v:return None
    m=(3*x*x-25)/(2*y) if p==q else (v-y)/(u-x)
    z=m*m-x-u
    return z,m*(x-z)-y
def mul(k,p):
    if k<0:k=-k;p=None if p is None else (p[0],-p[1])
    r=None
    while k:
        if k&1:r=add(r,p)
        p=add(p,p);k>>=1
    return r

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,required=True);ap.add_argument('--fresh',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    R,F=args.root,args.fresh
    pairs=[('arithmetic','evidence/arithmetic.json','arithmetic.json',{'utc','python'}),
      ('model_binding','evidence/model_binding.json','model_binding.json',{'generated_at_utc','command','python_version','input_locator'}),
      ('analytic','evidence/analytic.json','analytic/evidence/analytic.json',{'run','elapsed_seconds_display_only'}),
      ('interval','DERIVATIVE_INTERVAL.json','analytic/DERIVATIVE_INTERVAL.json',{'run'})]
    comparisons=[]
    for name,a,b,omit in pairs:
        old=json.loads((R/a).read_text());new=json.loads((F/b).read_text())
        check(old.keys()==new.keys(),f'{name} keys differ')
        failures=[k for k in old if k not in omit and old[k]!=new[k]]
        check(not failures,f'{name} mathematical mismatches: {failures}')
        comparisons.append({'stage':name,'all_nonmetadata_fields_equal':True,'fields_compared':sorted(set(old)-omit),
          'excluded_environment_metadata':sorted(omit)})
    d=json.loads((R/'evidence/arithmetic.json').read_text());trace_count=0
    records=list(d['tower_tests']['records'])
    for row in records:
        pt=point(row['point'])
        check(pt==add(mul(row['source_m'],P),K[row['source_torsion']]),'source point mismatch')
    extras=[{'point':a['point'],'level':4,**a['level4']} for a in d['rational_x_search']['decoded_spots']]
    for row in records+extras:
        pt=point(row['point']);n=row['level'];m=row['m'];T=K[row['torsion']];r=point(row['remainder'])
        check(0<=m<2**n,'quotient coordinate range')
        check(add(add(mul(m,P),T),mul(2**n,r))==pt,'readback identity')
        prev=pt;bits=0
        for j,step in enumerate(row['trace']):
            nxt=point(step['remainder']);b=step['bit'];t=K[step['torsion']]
            check(b in [0,1] and type(b)==int,'non-bit coordinate')
            check(add(add(mul(b,P),t),mul(2,nxt))==prev,'trace reconstruction')
            prev=nxt;bits+=b*2**j;trace_count+=1
        check(bits==m,'trace bits disagree with coefficient')
    checks=json.loads((R/'CONTROLS.json').read_text())
    print('control document keys',list(checks))
    items=checks.get('controls',[])
    if not items:
        items=next(v for v in checks.values() if isinstance(v,list) and v and isinstance(v[0],dict) and 'id' in v[0])
    control_ids=[v['id'] for v in items]
    check(len(control_ids)==6 and len(set(control_ids))==6,'control id coverage')
    analytic=json.loads((F/'analytic/evidence/analytic.json').read_text())
    arith=json.loads((F/'arithmetic.json').read_text())
    binding=json.loads((F/'model_binding.json').read_text())
    check(all(c['status']=='CONFIRMED' for c in arith['controls']+analytic['controls']),'fresh control failed')
    check(binding['status']=='CONFIRMED','fresh model binding failed')
    print('six controls',control_ids)
    delta=-16*4*(-25)**3
    counts={p:1+sum((y*y-x*x*x+25*x)%p==0 for x in range(p) for y in range(p)) for p in (3,7)}
    for p in counts:check(delta%p!=0,'prime is not good')
    check(counts[3]==4 and counts[7]==8,'torsion count premises')
    check(len(K)==4 and all(mul(2,t) is None for t in K.values()),'torsion witnesses')
    outcome={'status':'PASS','comparisons':comparisons,'readbacks_independently_checked':len(records)+len(extras),
      'declared_tower_cases':len(records),'additional_point_search_cases':len(extras),'trace_steps_checked':trace_count,
      'six_controls_replayed':control_ids,'new_mutation_campaign':False,
      'additional_torsion_corollary':{'evidence_kind':'NEW_IN_THIS_REVIEW_STANDARD_THEOREM_APPLICATION',
        'curve':'y^2=x^3-25x','discriminant':delta,'good_prime_counts':counts,
        'theorem':'Milne, Elliptic Curves (2006), II Corollary 5.7, printed p.66: rational torsion injects under good reduction at odd p.',
        'source':'https://www.jmilne.org/math/Books/ectext6.pdf#page=74',
        'proof':'Good reduction at 3 and #E(F3)=4 bound total rational torsion by 4. The four displayed 2-torsion points attain the bound.',
        'torsion_points':{'O':'infinity','T0':['0','0'],'Tplus':['5','0'],'Tminus':['-5','0']},
        'conclusion':'E(Q)_tors = E(Q)[2] = (Z/2)^2; exactly four rational torsion points.',
        'not_concluded':'P is an integral generator; full Sha; full BSD coefficient formula'},
      'scope':'Fresh execution comparison plus independently checked recorded arithmetic; no independent worker-context claim'}
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(outcome,indent=2)+'\n');print(json.dumps({'status':'PASS','readbacks':len(records)+len(extras),'trace_steps':trace_count,'torsion_order':4}))
if __name__=='__main__':main()
