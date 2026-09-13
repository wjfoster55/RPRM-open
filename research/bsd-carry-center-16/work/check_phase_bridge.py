"""Exact finite Fourier checks and bounds for a conditional BSD phase bridge."""
from fractions import Fraction as F
from itertools import product
from hashlib import sha256
from pathlib import Path
import argparse,json

ap=argparse.ArgumentParser(description=__doc__)
ap.add_argument('--output',type=Path,required=True)
args=ap.parse_args()
if args.output.exists():raise FileExistsError('Use a new evidence path')
N=(-2,-1,0,1,2)
modes=[{'n':n,'density':1,'winding':n,'energy':n*n} for n in N]
rows=[]
# Written orthogonality proof supplies the norm and energy formulas.
for coeffs in product((-1,0,1),repeat=5):
    norm=sum(c*c for c in coeffs)
    energy=sum(n*n*c*c for n,c in zip(N,coeffs))
    mean=coeffs[2]
    assert energy>=norm-mean*mean
    if mean==0:assert energy>=norm
    rows.append({'coefficients':coeffs,'norm_squared':norm,'energy':energy,'mean':mean})
assert len(rows)==243
small=[]
for eps in (F(1),F(1,2),F(1,10),F(1,100),F(1,1000)):
    energy=eps*eps;norm=1+energy
    small.append({'epsilon':str(eps),'energy_over_norm_squared':str(energy/norm)})

A=(F('6.38511803'),F('6.38518585'))
B=(F('6.384593255'),F('6.385625424'))
assert 0<B[0]<=B[1]
Q=(A[0]/B[1],A[1]/B[0])
K=(Q[0]-1,Q[1]-1)
assert -F(1,2)<K[0]<0<K[1]<F(1,2)
# Complete integer fiber: outside [-2,2] also outside (-1/2,1/2).
assert [n for n in N if K[0]<=n<=K[1]]==[0]
a=F('6.38515');b=F('6.38505')
assert A[0]<=a<=A[1] and B[0]<=b<=B[1]
q=a/b;k=q-1
assert k==F(2,127701) and k.denominator!=1
# Algebraic boundary test for exp(i*k*theta): periodic iff k is integer.
ordinary_periodic=k.denominator==1
assert not ordinary_periodic
# A small twisted boundary can admit a fractional parameter in the same interval.
twist=F(1,100000)
assert K[0]<twist<K[1] and twist.denominator!=1
assert (twist-twist).denominator==1
report={'status':'FINITE_FOURIER_AND_CONDITIONAL_PHASE_BRIDGE_CHECKED',
 'source_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
 'five_modes':modes,'coefficient_carrier':'{-1,0,1}^5','all_243_coefficient_rows':rows,
 'nonconstant_small_energy_controls':small,
 'attributed_A_interval':list(map(str,A)),'attributed_B1_interval':list(map(str,B)),
 'derived_Q_interval':list(map(str,Q)),'derived_Q_minus_one_interval':list(map(str,K)),
 'complete_integer_fiber_in_K_interval':[0],
 'nonzero_control':{'A':str(a),'B1':str(b),'Q':str(q),'K':str(k),
                   'ordinary_periodic':ordinary_periodic},
 'twisted_boundary_control':{'twist':str(twist),'K':str(twist),'ordinary_periodic':False},
 'analytic_exponential_equivalence':'Written proof: exp(2*pi*i*K)=1 iff K is integer',
 'periodicity_established_for_actual_BSD':False,
 'claim_ceiling':'Finite tests plus conditional implication; periodicity is an open premise, not a BSD proof'}
args.output.parent.mkdir(parents=True,exist_ok=True)
args.output.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:report[k] for k in ('status','complete_integer_fiber_in_K_interval',
 'nonzero_control','twisted_boundary_control','periodicity_established_for_actual_BSD')},indent=2))
