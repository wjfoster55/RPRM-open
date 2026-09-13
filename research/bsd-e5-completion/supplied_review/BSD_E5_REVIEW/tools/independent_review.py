"""Independent exact review of the E5 return. No submitted implementation imports.

The integral check uses three-point Simpson panels with a conservative error
bound derived directly from cubic Taylor remainders, not the submitted midpoint
quadrature. Exponentials use reciprocals of positive Taylor-series bounds.
See INDEPENDENT_METHOD.md for the analytic justification.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
from fractions import Fraction as Q
from functools import lru_cache
from itertools import product
from math import isqrt, prod
from pathlib import Path
import hashlib, json, platform, sys, zipfile

SCALE=10**36

def require(condition: bool, message: str) -> None:
    if not condition: raise ValueError(message)

def floorq(x: Q, d: int=SCALE) -> Q:
    return Q(x.numerator*d//x.denominator,d)

def ceilq(x: Q, d: int=SCALE) -> Q:
    return -floorq(-x,d)

def put(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')

def sha(p: Path) -> str: return hashlib.sha256(p.read_bytes()).hexdigest()

def atan_recip(d: int, terms: int=80) -> tuple[Q,Q]:
    z=Q(1,d); term=z; s=Q(0)
    for k in range(terms):
        s+=term/(2*k+1); term*=-z*z
    other=s+term/(2*terms+1)
    return min(s,other),max(s,other)

def alpha_bounds() -> tuple[Q,Q,dict]:
    # atan(1/2)+atan(1/3)=pi/4: tan addition =1, angle in first quadrant.
    a,b=atan_recip(2),atan_recip(3)
    pilo,pihi=4*(a[0]+b[0]),4*(a[1]+b[1])
    r=isqrt(2*SCALE*SCALE)
    require(r*r<2*SCALE*SCALE<(r+1)**2,'sqrt2 bracket')
    slo,shi=Q(r,SCALE),Q(r+1,SCALE)
    lo,hi=floorq(pilo/(10*shi)),ceilq(pihi/(10*slo))
    require(Q(1,5)<lo<hi<Q(1,4),'alpha bounds')
    return lo,hi,{'method':'pi=4(atan(1/2)+atan(1/3)); 80 alternating terms each; integer sqrt2',
      'pi_interval':[str(pilo),str(pihi)],'sqrt2_interval':[str(slo),str(shi)],'alpha_interval':[str(lo),str(hi)]}

@lru_cache(maxsize=None)
def exp_minus(x: Q) -> tuple[Q,Q]:
    """Bound exp(-x) via positive exp(z) sums, reciprocal, then powering."""
    require(x>=0,'exp domain')
    z=x; k=0
    while z>1:
        z/=2; k+=1
    term=s=Q(1)
    degree=40
    for j in range(1,degree+1):
        term*=z/j; s+=term
    next_term=term*z/(degree+1)
    upper=s+next_term/(1-z/(degree+2))
    # For all following terms, consecutive ratio <= z/(degree+2).
    lo,hi=floorq(1/upper),ceilq(1/s)
    require(0<=lo<=hi<=1,'positive reciprocal exp enclosure')
    for _ in range(k):
        lo,hi=floorq(lo*lo),ceilq(hi*hi)
    return lo,hi

def e1_simpson(xlo: Q,xhi: Q,k: int=16) -> tuple[Q,Q,dict]:
    require(0<xlo<=xhi<32,'E1 domain for this review')
    lower=upper=error=Q(0); left=xlo; count=0
    while left<32:
        right=min(2*left,Q(32)); width=(right-left)/k
        for j in range(k):
            a=left+j*width; b=a+width; m=(a+b)/2
            al,au=exp_minus(a); ml,mu=exp_minus(m); bl,bu=exp_minus(b)
            sl=width*(al/a+4*ml/m+bl/b)/6
            su=width*(au/a+4*mu/m+bu/b)/6
            # f''''(a) bounds |f''''| on [a,b]; conservative Taylor bound
            # |integral - Simpson| <= (b-a)^5 * sup |f''''| / 720.
            f4=au*(1/a+4/a**2+12/a**3+24/a**4+24/a**5)
            err=ceilq(width**5*f4/720)
            lower+=floorq(sl)-err; upper+=ceilq(su)+err
            error+=err; count+=1
        left=right
    argument_loss=ceilq((xhi-xlo)/xlo)
    integral_tail=ceilq(exp_minus(Q(32))[1]/32)
    lower-=argument_loss; upper+=integral_tail
    return lower,upper,{'panels':count,'integral_interval':[str(lower),str(upper)],
          'symmetric_quadrature_radius':str(error),'argument_loss':str(argument_loss),
          'integral_tail':str(integral_tail)}

def isprime(n:int)->bool:
    return n>=2 and all(n%d for d in range(2,isqrt(n)+1))

def coefficients(M:int)->tuple[dict,dict]:
    counts={p:1+sum((y*y-x*x*x+25*x)%p==0 for x in range(p) for y in range(p))
            for p in range(2,M+1) if isprime(p)}
    traces={p:p+1-c for p,c in counts.items()}
    coefficients={1:1}
    for n in range(2,M+1):
        if n%2==0 or n%5==0:
            coefficients[n]=0; continue
        m=n; factors=[]
        for p in range(2,n+1):
            if m%p: continue
            k=0
            while m%p==0: m//=p; k+=1
            seq=[1,traces[p]]
            for j in range(2,k+1): seq.append(traces[p]*seq[-1]-p*seq[-2])
            factors.append(seq[k])
        require(m==1,'factor coverage'); coefficients[n]=prod(factors)
    return coefficients,counts

def squarefree(q:Q|int)->int:
    q=Q(q); require(q!=0,'squareclass nonzero')
    n=abs(q.numerator*q.denominator); result=-1 if q<0 else 1
    p=2
    while p*p<=n:
        parity=0
        while n%p==0:n//=p; parity^=1
        if parity:result*=p
        p+=1
    return result*n

def compose(a,b):return tuple(squarefree(x*y) for x,y in zip(a,b))

def finite_arithmetic()->dict:
    D=(-10,-5,-2,-1,1,2,5,10)
    V=sorted({(a,b,squarefree(a*b)) for a in D for b in D if a*b>0})
    bins={}
    witnesses={}
    for mod in (2,4,8):
        primitive=[v for v in product(range(mod),repeat=4) if any(t%2 for t in v)]
        survivors=[]
        for d in V:
            found=next((v for v in primitive if
                (d[0]*v[0]**2-d[1]*v[1]**2-5*v[3]**2)%mod==0 and
                (d[2]*v[2]**2-d[0]*v[0]**2-5*v[3]**2)%mod==0),None)
            if found is not None:
                survivors.append(d);witnesses[str((mod,d))]=found
        bins[str(mod)]=survivors
    require([len(bins[str(m)]) for m in (2,4,8)]==[32,16,8],'local census')
    points=[None,(Q(0),Q(0)),(Q(5),Q(0)),(Q(-5),Q(0)),(Q(-4),Q(6)),
            (Q(25,4),Q(75,8)),(Q(-5,9),Q(-100,27)),(Q(45),Q(-300))]
    signatures=[]
    roots=(0,5,-5)
    for pt in points:
        if pt is None: signatures.append((1,1,1));continue
        x,y=pt;require(y*y==x*x*x-25*x,'rational witness off curve')
        signatures.append(tuple(squarefree(x-e if x!=e else prod(e-f for f in roots if f!=e)) for e in roots))
    require(set(signatures)==set(bins['8']),'witness saturation')
    basis=[(-1,-1,1),(-1,-5,5),(5,2,10),(2,2,1),(1,2,2)]
    cube={}
    for bits in product((0,1),repeat=5):
        value=(1,1,1)
        for bit,generator in zip(bits,basis):
            if bit:value=compose(value,generator)
        cube[bits]=value
        require((value in signatures)==(bits[3]==0 and bits[4]==0),'cube indicator')
    require(set(cube.values())==set(V),'cube bijection')
    for b1,c1 in cube.items():
        for b2,c2 in cube.items():
            require(cube[tuple(a^b for a,b in zip(b1,b2))]==compose(c1,c2),'cube group operation')
    return {'method':'direct primitive mod-2/4/8 quadruple census; exact rational membership; squarefree factoring; cube group check',
            'candidate_count':len(V),'local_survivor_counts':{m:len(v) for m,v in bins.items()},
            'eight_rational_witness_signatures':signatures,'cube_vertices':len(cube),'cube_pair_checks':len(cube)**2,
            'scope':'finite arithmetic; universal Selmer/rank claims require the written coverage proof and Kummer/Mordell-Weil theorems'}

def integrity(root:Path,archive:Path|None)->dict:
    manifest=json.loads((root/'DELIVERY_INVENTORY.json').read_text())
    seen=set();mismatches=[]
    for row in manifest['files']:
        path=root/row['path'];require(row['path'] not in seen,'duplicate inventory entry');seen.add(row['path'])
        if not path.is_file() or path.stat().st_size!=row['size'] or sha(path)!=row['sha256']:
            mismatches.append(row['path'])
    actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
    originals=[]
    if archive is not None and archive.exists():
        with zipfile.ZipFile(archive) as z:
            for info in z.infolist():
                if info.is_dir():continue
                path=root/'supplied'/info.filename
                require(path.is_file() and path.read_bytes()==z.read(info),f'original mismatch {info.filename}')
                originals.append(info.filename)
    require(not mismatches,'inventory mismatches')
    require(actual-seen=={'DELIVERY_INVENTORY.json'},'unlisted payload')
    return {'inventory_members':len(seen),'payload_members':len(actual),'inventory_mismatches':mismatches,
            'unlisted_payload':sorted(actual-seen),'original_archive_members_identical':len(originals),
            'original_archive_checked':str(archive) if originals else None}

def main()->None:
    ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--original',type=Path)
    args=ap.parse_args();root=args.root.resolve();out=args.out.resolve();out.mkdir(parents=True,exist_ok=True)
    before=integrity(root,args.original);put(out/'INTEGRITY.json',before)
    finite=finite_arithmetic();put(out/'FINITE_ARITHMETIC.json',finite)
    submitted=json.loads((root/'DERIVATIVE_INTERVAL.json').read_text())
    coef,counts=coefficients(40)
    require({str(n):a for n,a in coef.items()}==submitted['finite_coefficient_data']['all_coefficients'],'independent coefficients differ')
    alo,ahi,constants=alpha_bounds()
    lo=hi=Q(0);rows=[]
    delivered={r['n']:r for r in submitted['attempts'][0]['retained_e1']}
    for n,a in coef.items():
        if not a:continue
        el,eu,record=e1_simpson(n*alo,n*ahi)
        w=Q(2*a,n);tl,tu=sorted((w*el,w*eu));lo+=tl;hi+=tu
        dl,du=Q(delivered[n]['lower']),Q(delivered[n]['upper'])
        contained=(dl<=el<=eu<=du)
        require(contained,f'independent E1 bounds not contained at {n}')
        record.update({'n':n,'a_n':a,'signed_term_interval':[str(tl),str(tu)],'inside_submitted_e1':contained})
        rows.append(record)
    tail=Q(120,41)*Q(5,6)**41
    final_lo,final_hi=floorq(lo-tail,10**9),ceilq(hi+tail,10**9)
    dl,du=Q(submitted['lower']),Q(submitted['upper'])
    require(dl<=final_lo<final_hi<=du,'review enclosure not inside submitted result')
    require(du-dl==Q(submitted['width'])==sum(Q(v) for v in submitted['error_ledger'].values()),'submitted ledger assembly')
    report={'status':'PASS','generated_utc':datetime.now(timezone.utc).isoformat(),'python':sys.version,'platform':platform.platform(),
      'source_sha256':sha(Path(__file__)),'method':'independently written rational Simpson/Taylor enclosure and reciprocal-positive-series exponentials; no submitted implementation imports',
      'prime_counts':counts,'coefficients':coef,'constants':constants,'retained_terms':rows,
      'head_interval':[str(lo),str(hi)],'all_uncomputed_coefficient_tail_radius':str(tail),
      'independent_interval':[str(final_lo),str(final_hi)],'independent_interval_decimal':[float(final_lo),float(final_hi)],
      'submitted_interval':[str(dl),str(du)],'independent_interval_inside_submitted':True,
      'submitted_width':str(du-dl),'submitted_exact_error_ledger_reassembles':True,
      'scope':'independent algorithmic cross-check of the same fixed-curve Mellin formula and cited Hasse-derived tail theorem; not new modularity proof, rank computation, different-L backend, or full BSD verification'}
    put(out/'INDEPENDENT_INTERVAL.json',report)
    require(before==integrity(root,args.original),'input changed during review')
    print(json.dumps({'status':'PASS','inventory':before,'finite_arithmetic':finite,
       'independent_interval_decimal':report['independent_interval_decimal'],'inside_codex_interval':True},indent=2))

if __name__=='__main__':main()
