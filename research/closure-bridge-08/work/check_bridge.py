"""Exact bounded rise/fall and forward/backward seam tests; no external libraries."""
import argparse
from datetime import datetime, timezone
from hashlib import sha256
from itertools import product
import json
from pathlib import Path


def require(test, label):
    if not test:
        raise AssertionError(label)


def image(states, edges):
    return {y for x,y in edges if x in states}


def preimage(states, edges):
    return {x for x,y in edges if y in states}


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',required=True,type=Path)
    args=ap.parse_args()
    if args.output.exists():
        raise FileExistsError('Choose a new output path')
    carry_states=0;enabled_edges=0;by_base=[]
    for base in range(2,11):
        lo=-2*base;hi=3*base-1
        states=range(lo,hi+1)
        def reflect(z): return base-1-z
        for z in states:
            q,d=divmod(z,base)
            require(-2<=q<=2 and 0<=d<base,'admitted state')
            reflected=reflect(z)
            require(divmod(reflected,base)==(-q,base-1-d),'reflection keeps row')
            require(reflect(reflected)==z,'involution')
            require(z+reflected==base-1,'paired invariant')
            require((z<hi)==(reflected>lo),'transported enabledness')
            if z<hi:
                nq,nd=divmod(z+1,base)
                require(nq==q+(d==base-1) and nd==(d+1)%base,'forward carry')
                require(reflect(z+1)==reflected-1,'rise/fall conjugacy')
                require(reflect(reflected-1)==z+1,'inverse conjugacy')
                enabled_edges+=1
            carry_states+=1
        by_base.append({'base':base,'states':5*base,'forward_edges':5*base-1,
                        'outer_boundary':[lo,hi]})

    # Exhaust all three-state transition relations; compare against complete paths.
    possible=list(product(range(3),repeat=2))
    relations=0;seam_checks=0;matched_paths=0
    for mask in range(1<<len(possible)):
        edges={edge for j,edge in enumerate(possible) if mask>>j&1}
        relations+=1
        for start in range(3):
            for target in range(3):
                paths=[(start,)]
                F=[{start}]
                B=[{target}]
                for n in range(1,5):
                    F.append(image(F[-1],edges))
                    B.append(preimage(B[-1],edges))
                for n in range(5):
                    good=[p for p in paths if p[-1]==target]
                    for k in range(n+1):
                        seam=F[k]&B[n-k]
                        witnessed={p[k] for p in good}
                        require(seam==witnessed,'complete joint seam')
                        require(bool(seam)==bool(good),'existence iff seam inhabited')
                        seam_checks+=1
                    matched_paths+=len(good)
                    paths=[p+(v,) for p in paths for v in range(3) if (p[-1],v) in edges]

    start=7;split=2;horizon=5
    forward=start+split
    negative_target=2;backward=negative_target-(horizon-split)
    positive_target=12;positive_back=positive_target-(horizon-split)
    require(forward%10==backward%10 and forward!=backward,'false displayed meeting')
    require(forward==positive_back,'true full-state meeting')
    # Nonempty seam does not imply a unique source or a universally fixed readout.
    left={(0,0),(1,1)};right={(0,0),(1,1)}
    triples=sorted((x,y,z) for x,y in left for y2,z in right if y==y2)
    require(triples==[(0,0,0),(1,1,1)],'joint witness identity')
    require({x for x,y,z in triples}=={0,1},'variable readout remains unresolved')
    path=[{'k':k,'rise':7+k,'fall':2-k,'rise_state':divmod(7+k,10),
           'fall_state':divmod(2-k,10),'sum':9} for k in range(6)]
    result={'created_utc':datetime.now(timezone.utc).isoformat(),
        'status':'EXACT_BOUNDED_RISE_FALL_AND_SEAMS_CHECKED',
        'source_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
        'rise_fall':{'cases':by_base,'states':carry_states,'enabled_edges':enabled_edges,
                     'example_path':path,'unbounded_continuation':'Written family z=7+k, reflected=2-k for any separately admitted integer k; no terminal predicate follows'},
        'bidirectional':{'relations':relations,'states_per_relation':3,'horizons':[0,1,2,3,4],
                         'seam_checks':seam_checks,'successful_path_occurrences':matched_paths},
        'hostile_meeting':{'start':start,'target':negative_target,'horizon':horizon,'split':split,
                           'forward_state':divmod(forward,10),'backward_state':divmod(backward,10),
                           'same_digit':True,'joint_seam_empty':True,
                           'projected_route':[v%10 for v in range(7,13)]},
        'positive_meeting':{'start':start,'target':positive_target,'horizon':horizon,
                            'joint_seam':[forward],'path':list(range(7,13))},
        'existence_not_forced_readout':{'complete_triples':triples,'readout_values':[0,1]},
        'general_BSD_or_other_Millennium_proof':False}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'status':result['status'],'carry_states':carry_states,
                      'enabled_edges':enabled_edges,'relations':relations,
                      'seam_checks':seam_checks,'false_display_meeting_retained':True}))


if __name__=='__main__':main()
