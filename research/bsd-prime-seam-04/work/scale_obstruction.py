"""Exact prime-seam scale obstruction and auxiliary-Euler leading factor.

The alternative scalars are countermodels to INSUFFICIENT CONSTRAINTS, not
assertions about the actual BSD quotient. All arithmetic is rational.
"""
import argparse
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import json

def fraction(q):return [q.numerator,q.denominator]
def valuation(q,p):
    if q==0:raise ValueError('infinite valuation needs separate type')
    a=abs(q.numerator);b=q.denominator;v=0
    while a%p==0:a//=p;v+=1
    while b%p==0:b//=p;v-=1
    return v

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',required=True,type=Path)
    args=parser.parse_args()
    if args.output.exists():raise FileExistsError('Use a fresh output path')
    # This admitted earlier interval is used only as a receiver constraint;
    # its derivation is in dependencies/FACTOR_COMPARISON.md.
    lower=F(999920542,10**9);upper=F(1000092816,10**9)
    primes=(2,5,13);precision=8
    modulus=1
    for p in primes:modulus*=p**precision
    denominator=modulus*10**8+1
    u=F(denominator+modulus,denominator);alternate=u*u
    assert 1<alternate<upper and lower<1
    assert all(valuation(u,p)==valuation(alternate,p)==0 for p in primes)
    assert all(valuation(alternate-1,p)>=precision for p in primes)
    # Independent cross-multiplication of the strict real bound.
    assert alternate.numerator*upper.denominator<upper.numerator*alternate.denominator
    auxiliary=F(1)+F(6,13)+F(1,13)
    assert auxiliary==F(20,13) and valuation(auxiliary,5)==1
    # Normalized ratio is unchanged when both independently normalized sides
    # acquire the same nonzero auxiliary Euler factor.
    assert auxiliary*alternate/(auxiliary*F(1))==alternate
    # Rank-two leading-term transport: E(T)*A(T), mod T^3, with A0=A1=0.
    leading_samples=[]
    for a2,e1,e2 in ((F(0),F(1),F(2)),(F(7,11),F(-5,3),F(8)),
                     (F(-13,2),F(20),F(-9,5))):
        a=[F(0),F(0),a2];e=[auxiliary,e1,e2]
        product=[sum(e[j]*a[k-j] for j in range(k+1)) for k in range(3)]
        assert product==[0,0,auxiliary*a2]
        leading_samples.append({'a2':fraction(a2),'T2_product':fraction(product[2])})
    # A failed admission witness: without order>=2, higher E coefficients mix.
    wrong_a=[F(1),F(0),F(0)];e=[auxiliary,F(0),F(1)]
    wrong_T2=sum(e[j]*wrong_a[2-j] for j in range(3))
    assert wrong_T2==1 and wrong_T2!=auxiliary*wrong_a[2]
    report={'status':'EXACT_SCALE_OBSTRUCTION_AND_EULER_FACTOR_VERIFIED',
            'source_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
            'real_interval':[fraction(lower),fraction(upper)],
            'tested_primes':primes,'congruence_precision':precision,
            'modulus':modulus,'alternate_square_root':fraction(u),
            'alternate_positive_rational_square':fraction(alternate),
            'alternate_is_not_one':alternate!=1,
            'alternate_in_real_interval':lower<alternate<upper,
            'alternate_valuations':{str(p):valuation(alternate,p) for p in primes},
            'alternate_minus_one_valuations':{str(p):valuation(alternate-1,p) for p in primes},
            'auxiliary_13_Euler_factor_at_1':fraction(auxiliary),
            'auxiliary_13_v5':valuation(auxiliary,5),
            'rank2_leading_transport_samples':leading_samples,
            'order_admission_hostile_T2':fraction(wrong_T2),
            'global_BSD_quotient_congruences_actually_computed':False,
            'actual_analytic_augmentation_coefficient':'OPEN_NOT_COMPUTED',
            'countermodel_scope':'finite local congruences, positive rational square, real interval',
            'not_a_counterexample_to_BSD':True}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
