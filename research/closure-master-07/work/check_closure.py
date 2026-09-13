"""Exact carry lifts, finite cycle obstruction, and bounded stopping controls."""
import argparse
from collections import Counter
from datetime import datetime,timezone
from fractions import Fraction
from hashlib import sha256
from itertools import product
import json
from pathlib import Path


def cycles_of(T):
    cycles=set()
    for start in range(len(T)):
        seen={};path=[];x=start
        while x not in seen:
            seen[x]=len(path);path.append(x);x=T[x]
        cyc=path[seen[x]:]
        least=cyc.index(min(cyc));canonical=tuple(cyc[least:]+cyc[:least])
        cycles.add(canonical)
    return sorted(cycles)


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args()
    if args.output.exists():raise FileExistsError('Choose a new evidence path')
    cases=[];state_count=0;transition_checks=0
    for base,weights in [(3,(1,1)),(5,(1,5,5)),(7,(1,7,7)),(10,(100,10,10,1))]:
        count=0;A=sum(weights)
        for initial in product(range(base),repeat=len(weights)):
            d=list(initial);C=0;F0=sum(w*x for w,x in zip(weights,d))
            for k in range(2*base+1):
                F=sum(w*x for w,x in zip(weights,d))
                directC=sum(w*((x+k)//base) for w,x in zip(weights,initial))
                assert C==directC
                assert F+base*C==F0+A*k
                if k==base:
                    assert tuple(d)==initial and C==A
                wraps=sum(w for w,x in zip(weights,d) if x==base-1)
                nxt=[(x+1)%base for x in d]
                assert sum(w*x for w,x in zip(weights,nxt))-F==A-base*wraps
                C+=wraps;d=nxt;transition_checks+=1
            count+=1
        state_count+=count
        cases.append({'base':base,'weights':weights,'states':count,'horizon':2*base})
    d0=(5,4,2,6);weights=(100,10,10,1);path=[]
    for k in range(21):
        d=[(x+k)%10 for x in d0]
        F=sum(w*x for w,x in zip(weights,d))
        C=sum(w*((x+k)//10) for w,x in zip(weights,d0))
        path.append({'k':k,'source_word':''.join(map(str,d)),'wrapped':F,
                     'weighted_wraps':C,'lifted':F+10*C})

    # Exhaustive functional graphs on three states, with integer edge costs -1,0,1.
    counts=Counter();examples={}
    for T in product(range(3),repeat=3):
        cycles=cycles_of(T)
        for h in product((-1,0,1),repeat=3):
            sums=[sum(h[x] for x in cyc) for cyc in cycles]
            cycle_test=all(s==0 for s in sums)
            potentials=[g for g in product(range(-2,3),repeat=3)
                        if all(h[x]==g[x]-g[T[x]] for x in range(3))]
            assert cycle_test==bool(potentials)
            counts['zero_cycle_sums' if cycle_test else 'nonzero_cycle_sum']+=1
            examples.setdefault('solvable' if cycle_test else 'obstructed',
                {'T':T,'h':h,'cycles':cycles,'cycle_sums':sums,
                 'one_potential':potentials[0] if potentials else None})
    assert sum(counts.values())==729

    # Complete cube patterns, including arbitrary free coordinates, on each parity boundary.
    parity=[]
    for b in range(3,9):
        mono=Counter();patterns=0
        for cube in product((-1,0,1),repeat=b):
            free=[i for i,c in enumerate(cube) if c==-1]
            parities=set()
            for filling in product((0,1),repeat=len(free)):
                assignment=list(cube)
                for i,v in zip(free,filling):assignment[i]=v
                parities.add(sum(assignment)%2)
            if len(parities)==1:mono[len(free)]+=1
            patterns+=1
        assert dict(mono)=={0:2**b}
        parity.append({'boundary_bits':b,'all_cube_patterns':patterns,
                       'monochromatic_cubes':mono[0],'maximum_free_bits':0,
                       'compact_opposite_parity_CNF_clause_count':8*(b-2),
                       'required_block_certified_cube_exclusions':2**b})

    # Known numerator height plus divisibility really can close an exact rational zero.
    height=100;modulus=125
    zero_candidates=[a for a in range(-height,height+1) if a%modulus==0]
    assert zero_candidates==[0]
    contraction=[Fraction(1,2**k) for k in range(21)]
    assert all(x>0 for x in contraction)
    assert all(contraction[k+1]==contraction[k]/2 for k in range(20))
    shrinking_gaps=[Fraction(1,2**n) for n in range(1,21)]
    result={
        'created_utc':datetime.now(timezone.utc).isoformat(),
        'status':'EXACT_CARRY_CYCLE_AND_STOPPING_CONTROLS_COMPLETED',
        'source_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
        'carry':{'cases':cases,'total_states':state_count,'transition_checks':transition_checks,
                 'current_path':path,'one_cycle_projected_return':path[10]['wrapped'],
                 'one_cycle_lift_drift':path[10]['lifted']-path[0]['lifted']},
        'cycle_potential':{'complete_family_size':729,'counts':dict(counts),
                           'examples':examples,'equation':'h(x)=g(x)-g(Tx)',
                           'scope':'n=3 functional graphs, edge costs -1,0,1; written theorem covers arbitrary supplied finite graph'},
        'parity_cubes':parity,
        'stop_controls':{'numerator_bound':height,'divisibility_modulus':modulus,
                         'complete_compatible_numerators':zero_candidates,
                         'without_height_bound_nonzero_witness':modulus,
                         'strict_contraction_nonzero_at_every_recorded_step':True,
                         'contraction_samples':[str(x) for x in contraction],
                         'positive_finite_gaps_with_zero_limit':[str(x) for x in shrinking_gaps]},
        'Millennium_problem_solved':False,
        'claim_ceiling':'Fresh finite tests plus separate written proofs; no domain bridge is inferred from shared notation.'
    }
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'status':result['status'],'source_states':state_count,
                      'transition_checks':transition_checks,'cycle_models':729,
                      'one_cycle_drift':result['carry']['one_cycle_lift_drift']},indent=2))


if __name__=='__main__':main()
