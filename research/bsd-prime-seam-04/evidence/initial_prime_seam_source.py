"""Exact local BSD-factor seams and a bounded prime/lucky scout for E34.

Standard library only. No saved numerical evidence or database input.
The Gaussian Frobenius interpretation uses the written CM theorem audit.
This program does NOT evaluate a p-adic L-series or the global BSD scalar.
"""
import argparse
from collections import deque
from fractions import Fraction as F
from hashlib import sha256
from math import gcd, isqrt
from pathlib import Path
import json

ONE=(F(1),F(0))

def add(z,w): return (z[0]+w[0],z[1]+w[1])
def neg(z): return (-z[0],-z[1])
def sub(z,w): return add(z,neg(w))
def mul(z,w): return (z[0]*w[0]-z[1]*w[1],z[0]*w[1]+z[1]*w[0])
def conj(z): return (z[0],-z[1])
def norm(z): return z[0]*z[0]+z[1]*z[1]
def div(z,w):
    n=norm(w)
    if not n: raise ZeroDivisionError('zero Gaussian denominator')
    v=mul(z,conj(w))
    return (v[0]/n,v[1]/n)
def power(z,n):
    out=ONE
    while n:
        if n&1: out=mul(out,z)
        z=mul(z,z); n//=2
    return out
def enc(z):
    return {k:[v.numerator,v.denominator] for k,v in zip(('real','imag'),z)}

def primes_to(bound):
    sieve=[True]*(bound+1)
    sieve[:2]=[False,False]
    for p in range(2,isqrt(bound)+1):
        if sieve[p]:
            for n in range(p*p,bound+1,p): sieve[n]=False
    return [n for n,yes in enumerate(sieve) if yes]

def lucky_to(bound):
    # After the first pass, every second positive integer has been deleted.
    values=list(range(1,bound+1,2)); index=1; stages=[]
    while index < len(values):
        step=values[index]
        if step>len(values): break
        before=len(values)
        values=[n for position,n in enumerate(values,1) if position%step]
        stages.append({'step':step,'before':before,'after':len(values)})
        index+=1
    return values,stages

def count_points(p):
    # Euler's criterion, independently checked at 5 and 13 by full (x,y) enumeration.
    return 1+sum(1 if (r:=(x*x*x-1156*x)%p)==0
                 else 2 if pow(r,(p-1)//2,p)==1 else 0 for x in range(p))

def factors(n):
    out={}; d=2
    while d*d<=n:
        while n%d==0: out[str(d)]=out.get(str(d),0)+1; n//=d
        d+=1
    if n>1: out[str(n)]=out.get(str(n),0)+1
    return out

def factor_at(p):
    if p in (2,17) or p%4!=1: raise ValueError('requires good split odd prime')
    count=count_points(p); trace=p+1-count
    assert trace%2==0
    a=trace//2; b=isqrt(p-a*a)
    assert b>0 and a*a+b*b==p
    pi=(F(a),F(b)); bar=conj(pi)
    # C_pi=(p-pi)/(p-bar_pi), algebraically equivalent to original BKS factor.
    c=div(sub((F(p),F(0)),pi),sub((F(p),F(0)),bar))
    assert norm(c)==1 and c!=ONE
    d=p-a
    assert d*d+b*b==p*count
    assert c==(F(d*d-b*b,d*d+b*b),F(-2*d*b,d*d+b*b))
    assert (p*count)%c[0].denominator==0
    assert (p*count)%c[1].denominator==0
    assert count%4==0
    return c, {'prime':p,'point_count':count,'a_prime':trace,
               'pi':[a,b],'pi_minus_one_norm':count,'factor':enc(c),
               'point_count_factors':factors(count)}

def ec_add(p,q,modulus):
    if p is None:return q
    if q is None:return p
    x,y=p; u,v=q
    if x==u and (y+v)%modulus==0:return None
    slope=((3*x*x-1156)*pow(2*y,-1,modulus) if p==q
           else (v-y)*pow(u-x,-1,modulus))%modulus
    xx=(slope*slope-x-u)%modulus
    return (xx,(slope*(x-xx)-y)%modulus)

def ec_times(p,n,modulus):
    out=None
    while n:
        if n&1:out=ec_add(out,p,modulus)
        p=ec_add(p,p,modulus);n//=2
    return out

def ray_mul(z,w):
    return ((z[0]*w[0]-z[1]*w[1])%68,(z[0]*w[1]+z[1]*w[0])%68)

def ray_group(gens):
    found={(1,0)};todo=deque(found)
    while todo:
        x=todo.popleft()
        for g in gens:
            y=ray_mul(x,g)
            if y not in found:found.add(y);todo.append(y)
    return found

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--bound',type=int,default=1000)
    args=parser.parse_args()
    if args.output.exists():raise FileExistsError('Use a fresh witness path')
    if not 31<=args.bound<=10000:raise ValueError('frozen scout admits bounds 31..10000')
    ps=primes_to(args.bound); ls,stages=lucky_to(args.bound); lucky=set(ls)
    # Extending the ambient bound must not change the retained prefix.
    extended,_=lucky_to(2*args.bound)
    assert [v for v in extended if v<=args.bound]==ls
    rows=[]; local={}
    for p in ps:
        if p%4==1 and p!=17:
            c,row=factor_at(p);row['lucky']=p in lucky
            rows.append(row);local[p]=c
    c5=local[5];c13=local[13];ratio=div(c13,c5)
    a5=(F(-1),F(2));a13=(F(-3),F(2));ii=(F(0),F(1))
    assert sub(a13,ONE)==mul((F(0),F(-2)),conj(a5))
    assert sub(conj(a13),ONE)==mul((F(0),F(2)),a5)
    assert c5==mul(ii,div(a5,conj(a5)))
    assert ratio==mul(ii,div(a13,conj(a13)))
    assert ratio==(F(12,13),F(5,13))
    assert c5==(F(4,5),F(-3,5)) and c13==(F(63,65),F(-16,65))
    # A concrete order-five point supplied by reduction at 13.
    torsion5=[]
    for x in range(13):
        for y in range(13):
            if (y*y-x*x*x+1156*x)%13==0 and ec_times((x,y),5,13) is None:
                torsion5.append([x,y])
    assert len(torsion5)==4
    ray5=(67,2);value=(1,0);order=0
    while True:
        value=ray_mul(value,ray5);order+=1
        if value==(1,0):break
        assert order<2049
    loop_factor=power(c5,order)
    assert order==16 and loop_factor!=ONE and norm(loop_factor)==1
    gens5=[(67,2),(67,66)];gens13=[(65,2),(65,66)]
    groups=[len(ray_group(gens5)),len(ray_group(gens5+gens13))]
    assert groups==[256,512]
    # Four-code support receiver, with locations retained in addition to counts.
    prime_set=set(ps)
    codes={code:[] for code in ('00','01','10','11')}
    for n in range(1,args.bound+1):
        x=int(n in prime_set);y=int(n in lucky)
        s=x+y-1;d=x-y
        assert F(s+d+1,2)==x and F(s-d+1,2)==y
        codes[f'{x}{y}'].append(n)
    assert 13 in codes['11'] and 5 in codes['10'] and 9 in codes['01']
    assert 31 in codes['11'] and count_points(31)==32 # lucky prime, supersingular at31
    edges=[{'source':row['prime'],'target':int(q),'exponent':e}
           for row in rows for q,e in row['point_count_factors'].items()]
    assert all(edge['target']<edge['source'] for edge in edges)
    same_5_support=[r['prime'] for r in rows if r['point_count']%5==0]
    report={
        'status':'EXACT_LOCAL_SEAM_AND_BOUNDED_SCOUT_COMPLETED',
        'model':[0,0,0,-1156,0],'bound':args.bound,
        'source_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
        'local_factors':{str(p):enc(local[p]) for p in (5,13)},
        'ratio_13_over_5':enc(ratio),'ordinary_prime_rows':rows,
        'good_ordinary_prime_count':len(rows),'point_count_divisibility_edges':edges,
        'ordinary_primes_with_5_dividing_point_count':same_5_support,
        'lucky_members_in_that_list':[p for p in same_5_support if p in lucky],
        'E_F13_nonzero_order5_points':torsion5,
        'prime_lucky_counts':{k:len(v) for k,v in codes.items()},
        'prime_lucky_address_lists':codes,'lucky_sieve_stages':stages,
        'lucky_bound_extension_prefix_verified':True,
        'ray_group_orders':groups,
        'ray_loop':{'generator':[67,2],'order':order,'endpoint':[1,0],
                    'exact_accumulated_factor':enc(loop_factor),
                    'same_as_empty_path_factor':False,'norm':1,
                    'interpretation':'ASSIGNED_LOCAL_FACTOR_TRANSPORT_NOT_A_KATO_NORM_LAW'},
        'global_BSD_scalar':'OPEN_NOT_COMPUTED',
        'p13_height_and_BKS_hypotheses':'NOT_AUDITED_HERE',
        'lucky_to_global_multiplier_adapter':'OPEN',
        'evidence_grade':'EXACT_FINITE_ARITHMETIC_AND_WRITTEN_ALGEBRA'}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:report[k] for k in ('status','local_factors','ratio_13_over_5',
        'good_ordinary_prime_count','prime_lucky_counts','ordinary_primes_with_5_dividing_point_count',
        'lucky_members_in_that_list','E_F13_nonzero_order5_points','ray_group_orders',
        'global_BSD_scalar')},indent=2))

if __name__=='__main__':main()
