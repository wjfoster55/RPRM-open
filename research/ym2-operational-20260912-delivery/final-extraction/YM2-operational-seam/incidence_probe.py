"""New local incidence census, no prior verifier import."""
from itertools import combinations, product
import json

def add(a,b): return tuple(x+y for x,y in zip(a,b))
def unit(d,k): return tuple(int(i==k) for i in range(d))
def square(x,i,j):
    d=len(x); ei=unit(d,i); ej=unit(d,j)
    return frozenset(((x,add(x,ei)),(x,add(x,ej)),
                      (add(x,ei),add(add(x,ei),ej)),
                      (add(x,ej),add(add(x,ej),ei))))

def star(edge):
    x,y=edge; d=len(x); i=next(k for k in range(d) if x[k]!=y[k])
    return {square(add(x,tuple(-int(k==j)*s for k in range(d))),i,j)
            for j in range(d) if j!=i for s in (0,1)}

def pair_kind(p,q,shared):
    edges=p|q
    pure=0
    for v in shared:
        ins=sum(v==b for a,b in edges); outs=sum(v==a for a,b in edges)
        assert ins+outs==3
        pure+=int(ins==0 or outs==0)
    assert pure in (0,1)
    return 'same' if pure else 'opposite'

def census(d,k):
    anchor=(tuple(0 for _ in range(d)),unit(d,k))
    pairs=set()
    for p in star(anchor):
        for e in p:
            for q in star(e)-{p}:
                pairs.add(frozenset((p,q)))
    counts={a:{b:0 for b in ('same','opposite')} for a in ('shared','outside')}
    for pair in pairs:
        p,q=tuple(pair); common=p&q
        assert len(common)==1
        e=next(iter(common)); assert anchor in p|q
        counts['shared' if anchor==e else 'outside'][pair_kind(p,q,e)]+=1
    return {'dimension':d,'axis':k,'plaquettes':len(star(anchor)),
            'pair_count':len(pairs),'counts':counts}

if __name__=='__main__':
    print(json.dumps([census(d,k) for d in (2,3) for k in range(d)],indent=2))
