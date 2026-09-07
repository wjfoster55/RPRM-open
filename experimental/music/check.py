"""Independent assignment DP and exhaustive bounded symbolic checks."""
import argparse
from collections import deque
import hashlib
import importlib.util
from itertools import combinations, combinations_with_replacement, product
import json
import os
from uuid import uuid4
from math import gcd
from pathlib import Path

HERE=Path(__file__).resolve().parent


def _run_checks(args):
    spec=importlib.util.spec_from_file_location("music_model",HERE/"model.py")
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    counts={"assertions":0,"matching_pairs":0,"triangle_inequalities":0,"simultaneous_actions":0,"event_contexts":0,"event_conjugacy_states":0,"wave_inputs":0,"rejections":0}
    def require(ok,why):
        counts["assertions"]+=1
        if not ok:raise RuntimeError(why)
    def rejects(fn):
        try:fn()
        except ValueError:counts["rejections"]+=1
        else:raise RuntimeError("malformed input admitted")
    # An independent graph shortest-path oracle for the 12-cycle metric.
    distances=[]
    for start in range(12):
        d={start:0};queue=deque([start])
        while queue:
            v=queue.popleft()
            for w in ((v-1)%12,(v+1)%12):
                if w not in d:d[w]=d[v]+1;queue.append(w)
        distances.append(d)
        for end in range(12):require(m.circular_distance(start,end)==d[end],"cycle distance differs from BFS")
    def assignment_dp(left,right):
        best={0:0};paths={0:[()]}
        for used in range(7):
            i=used.bit_count()
            for j in range(3):
                if not used&(1<<j):
                    next_mask=used|(1<<j);cost=best[used]+distances[left[i]][right[j]]
                    if cost < best.get(next_mask,100):
                        best[next_mask]=cost;paths[next_mask]=[p+(j,) for p in paths[used]]
                    elif cost == best[next_mask]:
                        paths[next_mask].extend(p+(j,) for p in paths[used])
        return best[7],sorted(paths[7])
    labelled=list(product(range(12),repeat=3));carrier=list(combinations_with_replacement(range(12),3));index={x:i for i,x in enumerate(carrier)}
    require(len(labelled)==1728 and len(carrier)==364 and len(list(combinations(range(12),3)))==220,"carrier counts")
    folds={x:[] for x in carrier}
    for x in labelled:folds[tuple(sorted(x))].append(x)
    for x in carrier:
        fiber=m.labelled_fiber(x)
        require({tuple(v) for v in fiber["values"]}==set(folds[x]),"labelled inverse fiber incomplete")
        require(fiber["disposition"]==("ONE" if len(folds[x])==1 else "MANY"),"labelled fiber disposition")
    table=[]
    for x in carrier:
        row=[]
        for y in carrier:
            result=m.matching(x,y);cost,paths=assignment_dp(x,y)
            require(result["distance"]==cost,"matching differs from independent subset DP")
            require(result["assignment_fiber"]["values"]==[list(p) for p in paths],"minimum assignment fiber incomplete")
            require(result["assignment_fiber"]["disposition"]==("ONE" if len(paths)==1 else "MANY"),"assignment fiber disposition")
            require((cost==0)==(x==y),"metric zero identity")
            for p in result["assignment_fiber"]["values"]:
                require(sorted(p)==[0,1,2] and sum(distances[x[i]][y[p[i]]] for i in range(3))==cost,"minimum assignment witness")
            row.append(cost);counts["matching_pairs"]+=1
        table.append(row)
    for i,row in enumerate(table):
        for j,ij in enumerate(row):
            require(ij==table[j][i],"metric symmetry")
            middle=table[j]
            for k,ik in enumerate(row):
                if ik>ij+middle[k]:raise RuntimeError("triangle inequality failed")
            counts["triangle_inequalities"]+=len(row)
    for anchor in range(12):
        for sign in (-1,1):
            for x in labelled:
                g=m.action(x,anchor,sign)
                require(m.action(g,(-sign*anchor)%12,sign)==x,"dihedral inverse")
            transported=[index[tuple(sorted(m.action(x,anchor,sign)))] for x in carrier]
            for i,row in enumerate(table):
                image=table[transported[i]]
                for j,cost in enumerate(row):
                    if image[transported[j]]!=cost:raise RuntimeError("simultaneous action did not preserve matching")
                counts["simultaneous_actions"]+=len(row)
            for x in range(12):
                for k in range(12):
                    require(m.action(((x+k)%12,),anchor,sign)[0]==(m.action((x,),anchor,sign)[0]+sign*k)%12,"orientation-aware equivariance")
    # Multiplicity, voice, register, adjacency and interval-histogram controls.
    require(m.multiset((0,4,7))==m.multiset((7,4,0)) and (0,4,7)!=(7,4,0),"voice order control")
    require(m.distinct_set((0,0,7))==m.distinct_set((0,7,7)) and m.matching((0,0,7),(0,7,7))["distance"]==5,"multiplicity control")
    require(60%12==72%12 and 60!=72,"register erasure control")
    require(m.circular_distance(0,1)==1 and m.circular_distance(0,5)==5,"non-isometric relabeling control")
    require(m.circular_distance(0,1)!=m.circular_distance(0,(7*1)%12),"fifths and chromatic metrics")
    a=(0,1,3,7);b=(0,1,4,6)
    require(m.interval_histogram(a)==m.interval_histogram(b) and b not in m.orbit(a),"histogram does not determine arrangement")
    require(m.action((1,),0,-1)[0]!=(m.action((0,),0,-1)[0]+1)%12,"wrong orientation control")
    # All small integer sample arrays; positive/negative and cyclic operations
    # remain algebraic, with no inference about physical sound or perception.
    for n in range(1,6):
        for wave in product((-1,0,1),repeat=n):
            counts["wave_inputs"]+=1
            require(m.sum_waves(wave,m.negate(wave))==(0,)*n,"additive cancellation")
            for k in range(n):
                want=wave[k:]+wave[:k]
                require(m.shift(wave,k)==want and m.shift(want,-k)==wave,"phase inverse")
    hostile=(4,0,-2,0,-2,0)
    require(all(m.shift(hostile,k)!=m.negate(hostile) for k in range(6)),"universal sign/phase claim survived hostile wave")
    require(m.shift((0,1,0,-1),2)==m.negate((0,1,0,-1)),"lawful half-period example")
    # Build permutation cycles independently as edges on finite state sets.
    for p in range(1,7):
        masks=list(product((0,1),repeat=p))
        for q in range(1,7):
            for events in masks:
                counts["event_contexts"]+=1;states=set(product(range(p),range(q)))
                expected=[];edges={(f,h):((f+1)%p,(h+events[f])%q) for f,h in states}
                while states:
                    at=min(states);cycle=[]
                    while at not in cycle:cycle.append(at);states.remove(at);at=edges[at]
                    expected.append(cycle)
                actual=m.event_cycles(events,q)
                require(actual==expected,"event orbit census")
                divisor=gcd(sum(events),q)
                require(len(actual)==divisor and {len(c) for c in actual}=={p*q//divisor},"event cycle formula")
                for state,next_state in edges.items():
                    require(m.event_step(events,q,state)==next_state,"event forward map")
                    require(m.event_step(events,q,next_state,inverse=True)==state,"event inverse map")
                    require(m.event_invariant(events,q,state)==m.event_invariant(events,q,next_state),"event invariant")
                target=tuple(reversed(events))
                for state in edges:
                    left=m.timing_adapter(events,target,q,edges[state])
                    right=m.event_step(target,q,m.timing_adapter(events,target,q,state))
                    require(left==right,"timing conjugacy")
                    require(m.timing_adapter(target,events,q,m.timing_adapter(events,target,q,state))==state,"timing adapter inverse")
                    counts["event_conjugacy_states"]+=1
    require(m.event_step((1,0),3,(0,0))!=m.event_step((0,1),3,(0,0)),"same total does not mean equal temporal readout")
    for bad in (True,1.0,"1",None,-1,12):rejects(lambda b=bad:m.pitches((b,)))
    for bad in (True,0,2,1.0):rejects(lambda b=bad:m.action((0,),0,b))
    rejects(lambda:m.matching((0,1),(0,1)))
    rejects(lambda:m.pitches((0,),size=True))
    rejects(lambda:m.interval_histogram((0,0,1)))
    rejects(lambda:m.wave((True,)))
    rejects(lambda:m.sum_waves((0,),(0,0)))
    rejects(lambda:m.event_context((True,),2))
    rejects(lambda:m.event_context((0,),True))
    rejects(lambda:m.event_context((0,)*17,2))
    rejects(lambda:m.event_step((1,0),3,(0,3)))
    rejects(lambda:m.timing_adapter((1,0),(1,1),3,(0,0)))
    result={"status":"PASS","evidence":"exhaustive tests at the bounds below; no perceptual experiment", "counts":counts,
        "bounds":{"labelled_triples":1728,"multisets":364,"distinct_trichords":220,"dihedral_maps":24,"event_periods":"1..6","event_moduli":"1..6","wave_inputs":"all {-1,0,1} arrays of lengths1..5, plus frozen six-sample hostile wave"},
        "cost_model":{"matching_assignments_per_query":6,"baseline":"independent subset-assignment dynamic programming over 8 masks","claim":"No optimization or human similarity claim"},
        "source_hashes":{p.relative_to(HERE.parents[1]).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted([HERE/name for name in ("README.md","model.py","example.py","check.py")])}}
    payload=json.dumps(result,indent=2)+"\n"
    _publish(args.output, result)
    print(payload)


def _publish(path, result):
    if path is None:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + "." + uuid4().hex + ".tmp")
    temporary.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="optional absolute JSON receipt path")
    args = parser.parse_args()
    if args.output is not None:
        if not args.output.is_absolute():
            parser.error("--output requires an absolute path")
        args.output = args.output.resolve()
        source_files = {(HERE / name).resolve() for name in ("README.md", "model.py", "example.py", "check.py")}
        if args.output in source_files:
            parser.error("--output cannot overwrite this pack's source files")
    _publish(args.output, {"status": "PENDING"})
    try:
        return _run_checks(args)
    except Exception as exc:
        _publish(args.output, {"status": "FAIL", "error": f"{type(exc).__name__}: {exc}"})
        raise


if __name__=="__main__":main()
