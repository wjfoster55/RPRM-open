"""Bounded exact checks of centered coordinates, retained carries and stopping."""
from fractions import Fraction as F
from collections import defaultdict
from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import argparse,json

ap=argparse.ArgumentParser(description=__doc__)
ap.add_argument('--output',required=True,type=Path)
args=ap.parse_args()
if args.output.exists():raise FileExistsError('Use a fresh evidence path')

# C1: original rail and the explicitly enlarged digit carrier.
rail=[{'raw':x,'z':5-x,'tau':str(F(6-x,2))} for x in (6,5,4)]
assert [r['z'] for r in rail]==[-1,0,1]
assert [r['tau'] for r in rail]==['0','1/2','1']
digits=range(10)
center_rows=[{'raw':x,'z':5-x,'reconstructed':5-(5-x)} for x in digits]
assert len({r['z'] for r in center_rows})==10
center_pair_count=0
for a in digits:
    for b in digits:
        za,zb=5-a,5-b
        assert za-zb==-(a-b)
        assert (za==zb)==(a==b)
        assert (a+F(0,1))-(b+F(0,1))==a-b
        assert (a+1)-(b+1)==a-b
        # Independently selected origins hide difference unless retained.
        oa,ob=a,b
        assert a-oa==b-ob==0
        assert ((a-oa)+oa)-((b-ob)+ob)==a-b
        if b!=0:
            assert F(5-za,5-zb)==F(a,b)
        center_pair_count+=1
assert F(5,9)!=F(0,-4)  # Ratio does not transport by dividing new coordinates.

# C2: pairs are (digit, carry_row), with ordinary integer readout.
states=[(d,q) for q in digits for d in digits]
def value(s):return 10*s[1]+s[0]
def encode(n):
    if not 0<=n<=99:raise ValueError('OPEN_NEW_CARRIER')
    q,d=divmod(n,10)
    return d,q
def increment(s):
    if s==(9,9):raise ValueError('OPEN_NEW_CARRIER')
    return encode(value(s)+1)
assert all(encode(value(s))==s for s in states)
projection_fibers=defaultdict(list)
steps=[]
for s in states:
    projection_fibers[s[0]].append(list(s))
    if s==(9,9):continue
    t=increment(s)
    assert value(t)==value(s)+1
    assert encode(value(t)-1)==s
    steps.append({'before':list(s),'after':list(t),
                  'value_before':value(s),'value_after':value(t)})
assert len(steps)==99 and all(len(f)==10 for f in projection_fibers.values())
assert increment((9,0))==(0,1) and value((0,1))==10 and F(0,1)==0
assert (0,0)!=(0,1) and value((0,0))==0
for d in digits:
    for q in range(9):
        assert value((d,q+1))-value((d,q))==10
assert increment((9,8))==(0,9)
try:increment((9,9))
except ValueError as e:assert str(e)=='OPEN_NEW_CARRIER'
else:raise AssertionError('Missing top-boundary guard')

# C3: exact conditional lattice stop, plus an admitted nonlattice control.
D=(F(-507394,10**9),F(592595,10**9))
delta=F(1,1000)
assert -delta<D[0]<=D[1]<delta
lattice_in_interval=[]
for k in range(-10,11):
    d=k*delta
    if D[0]<=d<=D[1]:lattice_in_interval.append({'k':k,'D':str(d)})
    if abs(d)<delta:assert k==0 and d==0
assert lattice_in_interval==[{'k':0,'D':'0'}]
control=F(1,10000)
assert D[0]<=control<=D[1] and control!=0 and control/delta==F(1,10)
display_scales=[]
for n in (4,5,6,9,12):
    numerator=control*10**n
    assert numerator.denominator==1 and F(int(numerator),10**n)==control
    display_scales.append({'numerator':int(numerator),'denominator':10**n,'D':str(control)})
# Fine-grid equality is not forced by the mere presence of decimal denominators.
fine_in_interval=[k for k in range(-10,11) if D[0]<=F(k,10000)<=D[1]]
assert fine_in_interval==list(range(-5,6))

report={'status':'BOUNDED_CENTER_CARRY_AND_CONDITIONAL_STOP_CHECKED',
 'created_utc':datetime.now(timezone.utc).isoformat(),
 'source_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
 'original_seam_zero_rail':rail,'extended_digit_center_rows':center_rows,
 'center_and_common_addition_pairs_checked':center_pair_count,
 'target_5_9':{'raw':[5,9],'z':[0,-4],'raw_difference':-4,'z_difference':4,
               'transported_ratio':'5/9','naive_new_coordinate_ratio':'0'},
 'carry_steps':steps,'digit_only_complete_fibers':dict(projection_fibers),
 'zero_one':{'candidate_state':[0,1],'integer_readout':10,'ordinary_fraction':'0'},
 'hostile_equal_digit_states':{'enabled':[9,8],'disabled':[9,9]},
 'attributed_D_interval':list(map(str,D)),
 'candidate_lattice_delta':str(delta),'lattice_fiber_within_interval':lattice_in_interval,
 'lattice_premise_established_for_actual_BSD':False,
 'nonzero_control':{'D':str(control),'D_over_delta':str(control/delta)},
 'same_nonzero_control_at_finer_scales':display_scales,
 'fine_grid_delta':'1/10000','fine_grid_possible_k':fine_in_interval,
 'claim_ceiling':'Finite exact models and a conditional stopping law; no new BSD identity or Sha result'}
args.output.parent.mkdir(parents=True,exist_ok=True)
args.output.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:report[k] for k in ('status','center_and_common_addition_pairs_checked',
 'target_5_9','zero_one','lattice_premise_established_for_actual_BSD','nonzero_control')},indent=2))
