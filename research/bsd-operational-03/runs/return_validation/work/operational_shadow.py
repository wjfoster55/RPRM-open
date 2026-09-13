"""A faithful two-observation RPRM adapter for an actual E34 shadow.

The finite carrier is the 4096 points in E[68] whose17-component is a
generator over Z[i]/17. Doubling is closed on this carrier. The two raw
observations r(P)=Y/(2X),r(2P) recover P exactly; r alone does not update
under doubling. Canonical-height-only observations have a different quotient.
"""
import argparse
from collections import Counter,defaultdict
from datetime import datetime,timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import time
from rational_ec import Q,point,add,mul,neg,encode
from padic_height import height_mod5


def load_module(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec)
    sys.modules[name]=module
    spec.loader.exec_module(module)
    return module


def restore(r,s):
    V=(r**4-289)/(2*r*s)
    X=2*(V+r*r)
    return X,2*r*X


def rational_witness():
    P=point(-2,48); R=point(-16,120); T=point(0,0)
    twin=add(neg(P),T)
    shadow=lambda A:A[1]/(2*A[0])
    r=shadow(P);rt=shadow(twin)
    s=shadow(mul(2,P));st=shadow(mul(2,twin))
    assert P!=twin and r==rt and s==-st and s!=st
    assert restore(r,s)==P and restore(rt,st)==twin
    value1,check1=height_mod5(add(P,R))
    value2,check2=height_mod5(add(twin,R))
    assert value1!=value2
    return {'P':encode(P),'twin_minus_P_plus_T0':encode(twin),
            'common_shadow_r':str(r),'r_after_double':[str(s),str(st)],
            'both_explicit_inverses_recover_source':True,
            'same_deterministic_mirror_pair':[str(r),str(-r)],
            'h5_after_add_Q_mod5':[value1,value2],
            'height_checks':[check1,check2],
            'height_only_correction':'q(P)=q(twin), and equality persists under pure doubling; loss is raw-shadow update or mixed addition/pairing, not the pure canonical-height receiver'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    if args.output.exists():raise FileExistsError('Preserve earlier evidence')
    start=time.monotonic()
    root=Path(__file__).resolve().parents[1]
    inputs=root/'input_source'
    load_module('cm_action',inputs/'cm_action.py')
    backend=load_module('bsd_operational_finite_ring',inputs/'trace125.py')
    F=backend.F
    field=backend.field_certificate()
    residue,search=backend.find_seed(3403)
    P,lifting=backend.lift_point(residue,125)
    multipliers=[None]
    for _ in range(1,68):multipliers.append(backend.add(multipliers[-1],P))
    imaginary=[backend.cm_i(S) for S in multipliers]
    coordinates=[(a,b) for a in range(68) for b in range(68) if (a*a+b*b)%17]
    assert len(coordinates)==16*256
    points={};shadows={};fibers=defaultdict(list)
    for a,b in coordinates:
        A=backend.add(multipliers[a],imaginary[b])
        assert A is not None and backend.on_curve(A)
        points[a,b]=A
        r=A[1]/(2*A[0])
        shadows[a,b]=r
        fibers[r.c].append((a,b))
    assert len({tuple(tuple(c.c) for c in A) for A in points.values()})==4096
    assert len(fibers)==2048 and set(map(len,fibers.values()))=={2}
    pairs=set();mirrors=set();trace=hashlib.sha256();successor_pairs=[]
    for a,b in coordinates:
        r=shadows[a,b]
        next_key=(2*a%68,2*b%68)
        assert next_key in points
        s=shadows[next_key]
        assert restore(r,s)==points[a,b]
        X,Y=points[a,b]
        V=(X*X+1156)/(4*X)
        assert V*V==r**4+289
        assert s==(r**4-289)/(2*r*V)
        twin=((34-a)%68,(34-b)%68)
        assert twin in points and twin!=(a,b)
        assert shadows[twin]==r
        twin_next=(2*twin[0]%68,2*twin[1]%68)
        assert shadows[twin_next]==-s and s!=-s
        pairs.add((r.c,s.c))
        mirrors.add((r.c,(-r).c))
        trace.update(json.dumps([a,b,list(r.c),list(s.c)],separators=(',',':')).encode())
    assert len(pairs)==4096 and len(mirrors)==2048
    # Partition refinement for the actual finite operation table: first the
    # present raw shadow; then its shadow after one doubling. The latter is
    # already discrete and therefore stable for every later doubling word.
    partition0={key:r.c for key,r in shadows.items()}
    partition1={key:(partition0[key],partition0[(2*key[0]%68,2*key[1]%68)])
                for key in coordinates}
    assert len(set(partition1.values()))==4096
    witness=rational_witness()
    result={'created_utc':datetime.now(timezone.utc).isoformat(),
            'status':'EXACT_OPERATIONAL_ADAPTER_AND_HOSTILE_CONTROL_VERIFIED',
            'carrier':'E34[68] with primitive Gaussian17-component',
            'field_certificate':field,'seed_search':search,
            'residue_seed':backend.encode_point(residue),
            'lifted_seed':backend.encode_point(P),'lifting':lifting,
            'carrier_size':4096,'raw_shadow_classes':2048,
            'raw_shadow_fiber_size':2,'mirror_pair_classes':len(mirrors),
            'shadow_plus_doubling_classes':len(pairs),
            'partition_refinement_class_counts':[2048,4096,4096],
            'shortest_separating_operation':'DOUBLE, length1',
            'explicit_recoveries_checked':4096,'all_doubling_targets_admitted':True,
            'complete_new_row_stream_sha256':trace.hexdigest(),
            'rational_witness':witness,
            'trace_to_real_height_or_BSD_identity':'OPEN_NO_SUCH_COMPARISON_ASSERTED',
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'dependency_sha256':{str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest()
                                 for p in [inputs/'trace125.py',inputs/'cm_action.py',
                                           root/'work/rational_ec.py',root/'work/padic_height.py']},
            'elapsed_seconds':time.monotonic()-start}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:result[k] for k in ('status','carrier_size','raw_shadow_classes',
                              'shadow_plus_doubling_classes','elapsed_seconds')},indent=2))


if __name__=='__main__':main()
