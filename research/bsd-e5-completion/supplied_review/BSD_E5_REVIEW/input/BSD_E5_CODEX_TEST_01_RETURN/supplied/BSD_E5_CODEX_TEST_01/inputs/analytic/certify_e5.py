#!/usr/bin/env python3
"""A finite, exact nonvanishing certificate for L'(E,1), E: y^2=x^3-25x.

The mathematical implications use explicitly cited standard inputs (modularity,
N=800, root number -1, Euler recurrences, and the Mellin/E1 identity).
This executable checks their finite arithmetic specialization and the rational
inequality; it does not re-prove those theorems or use a rank/database oracle.

Run: python -B certify_e5.py --output CERTIFICATE.json
Only the optional decimal illustration uses mpmath; the certificate is Fraction-only.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import platform
from fractions import Fraction as F
from itertools import product
from pathlib import Path


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ArithmeticError(message)


def primes_upto(k: int) -> list[int]:
    return [p for p in range(2, k+1)
            if all(p % d for d in range(2, math.isqrt(p)+1))]


def count_pairs(p: int) -> int:
    return 1 + sum((y*y-x*x*x+25*x) % p == 0
                   for x in range(p) for y in range(p))


def count_roots(p: int) -> int:
    roots = [0]*p
    for y in range(p):
        roots[y*y % p] += 1
    return 1 + sum(roots[(x*x*x-25*x) % p] for x in range(p))


def coefficients(k: int) -> tuple[list[int], list[dict]]:
    ps = primes_upto(k)
    ap = {}
    table = []
    for p in ps:
        n = count_pairs(p)
        require(n == count_roots(p), f'point count mismatch at {p}')
        ap[p] = p+1-n
        if p in (2,5):
            require(ap[p] == 0, f'bad-prime coefficient at {p}')
            kind = 'additive bad reduction; local Euler factor 1'
        else:
            require(ap[p]**2 <= 4*p, f'Hasse bound at {p}')
            kind = 'good reduction'
        table.append({'p':p,'projective_model_points':n,'a_p':ap[p],
                      'local_factor_type':kind})
    a=[0]*(k+1)
    a[1]=1
    for n in range(2,k+1):
        p=next(p for p in ps if n%p==0)
        d=n;e=0
        while d%p==0:
            d//=p;e+=1
        if p in (2,5):
            a[n]=0
            continue
        last,cur=1,ap[p]
        for _ in range(2,e+1):
            last,cur=cur,ap[p]*cur-p*last
        a[n]=a[d]*cur
    return a,table


def atan_interval(x:F,terms:int=8)->tuple[F,F]:
    require(0 < x < 1, 'arctan domain')
    s=sum(((-1)**k)*x**(2*k+1)/F(2*k+1) for k in range(terms))
    nxt=((-1)**terms)*x**(2*terms+1)/F(2*terms+1)
    return min(s,s+nxt),max(s,s+nxt)


def sf(n:int)->int:
    require(n!=0,'zero is not a squareclass')
    sign=-1 if n<0 else 1
    n=abs(n);out=1;d=2
    while d*d<=n:
        odd=0
        while n%d==0:n//=d;odd^=1
        if odd:out*=d
        d+=1
    return sign*out*n


def smul(a:tuple[int,...],b:tuple[int,...])->tuple[int,...]:
    return tuple(sf(x*y) for x,y in zip(a,b))


def cube_check()->dict:
    # These generators and arithmetic exclusions are inherited from E5_DESCENT_NOTE.
    generators=[(-1,-1,1),(-1,-5,5),(5,2,10),(2,2,1),(1,2,2)]
    labels={}
    for bits in product((0,1),repeat=5):
        value=(1,1,1)
        for bit,g in zip(bits,generators):
            if bit:value=smul(value,g)
        require(value not in labels,'five-bit map not injective')
        labels[value]=bits
    D=(-10,-5,-2,-1,1,2,5,10)
    V={(a,b,sf(a*b)) for a in D for b in D if a*b>0}
    require(set(labels)==V, 'cube does not cover candidate set')
    H={value for value,bits in labels.items() if bits[-2:]==(0,0)}
    blocks={str((u,v)):sum(bits[-2:]==(u,v) for bits in labels.values())
            for u,v in product((0,1),repeat=2)}
    require(len(H)==8 and set(blocks.values())=={8},'incorrect block sizes')
    for value,bits in labels.items():
        indicator=(1-bits[3])*(1-bits[4])
        require(indicator==int(value in H),'indicator mismatch')
    return {'candidate_vertices':len(labels),'realized_class_vertices':len(H),
            'group_sizes_by_outer_bits':blocks,
            'basis_order':['delta(P)','delta(T0)','delta(Tplus)','A','B'],
            'validity_indicator_given_previous_descent':'(1-u)*(1-v)',
            'scope':'Exact recoding of accepted finite descent structure. '
                    'Local exclusions are inherited, not proved by the cube alone.',
            'class_count_including_identity':8,'wrapper_is_a_new_group_element':False}


def as_record(x:F)->dict:
    return {'numerator':str(x.numerator),'denominator':str(x.denominator),
            'float_for_display_only':float(x)}


def certificate()->dict:
    a,pt=coefficients(20)
    nz=[(n,a[n]) for n in range(1,21) if a[n]]
    require(nz==[(1,1),(9,-3),(13,-6),(17,-2)], 'unexpected Fourier coefficients')
    # Machin's exact identity and alternating remainder give an enclosure for pi.
    a5,b5=atan_interval(F(1,5))
    a239,b239=atan_interval(F(1,239))
    pi_low,pi_high=16*a5-4*b239,16*b5-4*a239
    require(3 < pi_low < pi_high < F(22,7),'pi bounds')
    require(F(7,5)**2 < 2 < F(3,2)**2,'sqrt2 bounds')
    # alpha = pi / (10*sqrt2); no floating arithmetic in these inequalities.
    require(pi_low/15 > F(1,5),'lower alpha bound')
    require(pi_high/14 < F(1,4),'upper alpha bound')
    q=F(5,6)
    # e^{-alpha}<q from alpha>1/5 and exp(x)>1+x.
    negative=sum(F(10*abs(an),n*n)*q**n for n,an in nz if an<0)
    # |a_n| <= d(n)*sqrt(n) <= 2n and E1(x)<=exp(-x)/x.
    # Therefore the omitted tail after n=20 is bounded by:
    tail=F(120,21)*q**21
    # E1(alpha) > e^{-1}log4 > (1/3)*(4/3)=4/9.
    # e<3 and log2>2/3 have elementary series proofs in the note.
    positive=F(8,9)
    lower=positive-negative-tail
    require(negative<F(109,1000),'negative bound insufficient')
    require(tail<F(1,8),'tail bound insufficient')
    require(lower>F(65,100),'nonvanishing inequality failed')
    return {
        'status':'PASS',
        'equation':'y^2=x^3-25*x',
        'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'python':platform.python_version(),
        'theorem_inputs':[
            'Modularity, analytic continuation, and completed functional equation.',
            'Congruent-number family: conductor N=32*5^2=800; sign epsilon=-1.',
            'Local Euler factors; multiplicativity and prime-power recurrence.',
            'Hasse bound implies |a_n| <= d(n)*sqrt(n) <= 2n.',
            "L'(E,1)=2 sum_{n>=1} (a_n/n) E1(2*pi*n/sqrt(N)) for sign -1.",
            'Elementary integral definition of E1 and elementary exponential/logarithm inequalities.',
            "Prior exact arithmetic descent: rank(E(Q))=1. Not used in the derivative computation."
        ],
        'point_counts':pt,
        'nonzero_coefficients_through_20':nz,
        'alpha_enclosure':{'lower':'1/5','upper':'1/4'},
        'positive_first_term_lower_bound':as_record(positive),
        'retained_negative_magnitude_upper_bound':as_record(negative),
        'entire_omitted_tail_magnitude_upper_bound':as_record(tail),
        'Lprime_lower_bound':as_record(lower),
        'certified_conclusion':"L(E,1)=0 and L'(E,1)>65/100; analytic order exactly 1.",
        'BSD_rank_equality_for_this_curve':'1=1 after adjoining previous arithmetic descent',
        'full_BSD_leading_coefficient_formula':'NOT_ESTABLISHED_BY_THIS_CERTIFICATE',
        'generator_odd_saturation':'NOT_PERFORMED',
        'general_BSD':'NOT_ESTABLISHED_BY_THIS_CERTIFICATE',
        'finite_cube_recoding':cube_check(),
        'roundoff_used_in_certificate':False,
        'numerical_display':None
    }


def illustration()->dict:
    try:
        import mpmath as mp
    except ImportError:
        return {'status':'NOT_RUN','reason':'mpmath unavailable; exact certificate unaffected'}
    mp.mp.dps=60
    a,_=coefficients(100)
    alpha=2*mp.pi/mp.sqrt(800)
    s=2*mp.fsum(mp.mpf(a[n])/n*mp.e1(alpha*n)
                for n in range(1,101) if a[n])
    tail=4/(alpha*101)*mp.exp(-alpha*101)/(1-mp.exp(-alpha))
    require(s>mp.mpf('0.65'),'numerical illustration disagrees')
    return {'status':'NUMERICAL_ILLUSTRATION_ONLY',
            'partial_sum_n_le_100':mp.nstr(s,40),
            'analytic_tail_bound_evaluated_numerically':mp.nstr(tail,12),
            'arbitrary_precision_decimal_digits':60,
            'rounding_error_certified':False,
            'note':'Not needed for, and not promoted into, the exact sign proof.'}


def main()->None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=Path('CERTIFICATE.json'))
    args=parser.parse_args()
    result=certificate()
    result['numerical_display']=illustration()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'status':result['status'],
                      'conclusion':result['certified_conclusion'],
                      'lower_bound':result['Lprime_lower_bound'],
                      'illustration':result['numerical_display']},indent=2))

if __name__=='__main__':
    main()
