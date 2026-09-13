"""Exact bounded controls for floating loss, prestige summaries and BSD rounding."""
from fractions import Fraction as F
from itertools import product
from collections import defaultdict
from hashlib import sha256
from datetime import datetime, timezone
from pathlib import Path
import argparse,json,sys

ap=argparse.ArgumentParser(description=__doc__)
ap.add_argument('--output',type=Path,required=True)
args=ap.parse_args()
if args.output.exists():raise FileExistsError('Use a new evidence path')
assert sys.float_info.radix==2 and sys.float_info.mant_dig==53

n=2**53
floating_rows=[]
for i in range(n-2,n+5):
    f=float(i)
    floating_rows.append({'integer':i,'binary64_exact_value':str(F.from_float(f)),
                         'error':str(F.from_float(f)-i)})
assert float(n+1)==float(n) and F(n+1)-F(n)==1

Atext=('6.38511803','6.38518585')
Btext=('6.384593255','6.385625424')
A=tuple(map(F,Atext));B=tuple(map(F,Btext))
D=(A[0]-B[1],A[1]-B[0])
width_A=A[1]-A[0];width_B=B[1]-B[0];width_D=D[1]-D[0]
assert width_A+width_B==width_D
assert D==(F(-507394,10**9),F(592595,10**9))
float_D=(float(Atext[0])-float(Btext[1]),float(Atext[1])-float(Btext[0]))
last_step_errors=[abs(F.from_float(f)-d) for f,d in zip(float_D,D)]
assert max(last_step_errors)<F(1,10**15)
assert width_D>10**12*max(last_step_errors)

# Seven-site summary from the existing three-cube envelope.
fibers=defaultdict(list)
for table in product((0,1),repeat=8):fibers[table[:7]].append(table)
assert len(fibers)==128 and all(len(v)==2 for v in fibers.values())
zero=(0,)*8;hidden=(0,)*7+(1,)
assert fibers[(0,)*7]==[zero,hidden]
assert zero[:7]==hidden[:7] and zero!=hidden
# The h-flip at mask 6 asks for old mask 7, exposing the retained-summary loss.
def flip_h(table):return tuple(table[s^1] for s in range(8))
assert flip_h(zero)[6]==0 and flip_h(hidden)[6]==1
# For a fixed seven-site question, knowing those seven entries is sufficient.
assert all(all(v[:7]==summary for v in vals) for summary,vals in fibers.items())

assert 0<B[0]<=B[1]
Q=(A[0]/B[1],A[1]/B[0])
def rounded_integer(x,places):
    y=x*10**places+F(1,2)
    return y.numerator//y.denominator
roundings=[]
for p in range(7):
    lo=rounded_integer(Q[0],p);hi=rounded_integer(Q[1],p)
    roundings.append({'decimal_places':p,'lower_rounded_scaled_integer':lo,
                     'upper_rounded_scaled_integer':hi,'scale':10**p,
                     'unique_rounded_value':str(F(lo,10**p)) if lo==hi else None})
assert [r['decimal_places'] for r in roundings if r['unique_rounded_value'] is not None]==[0,1,2,3]
assert all(roundings[p]['unique_rounded_value']=='1' for p in range(4))
assert roundings[4]['lower_rounded_scaled_integer']==9999
assert roundings[4]['upper_rounded_scaled_integer']==10001
a=F('6.38515')
witnesses=[]
for d in (F(0),F(1,10000)):
    b=a-d
    assert A[0]<=a<=A[1] and B[0]<=b<=B[1]
    q=a/b
    assert rounded_integer(q,3)==1000
    witnesses.append({'A':str(a),'B1':str(b),'Q':str(q),'D':str(d),'rounded_3dp':'1.000'})

d=F(1,10000)
scales=[]
for s in (1,10,10000):
    a=F('6.38515');b=a-d
    ds=a/s-b/s
    assert ds==d/s and ds!=0 and ds*s==d
    scales.append({'scale':s,'normalized_D':str(ds),'reconstructed_D':str(ds*s)})

result={'status':'BOUNDED_FLOAT_PRESTIGE_AND_ROUNDING_CONTROLS_CHECKED',
 'created_utc':datetime.now(timezone.utc).isoformat(),
 'source_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
 'binary64_control_rows':floating_rows,
 'attributed_A_interval':list(map(str,A)),'attributed_B1_interval':list(map(str,B)),
 'derived_D_interval':list(map(str,D)),
 'widths':{'A':str(width_A),'B1':str(width_B),'D':str(width_D),
           'B1_share_of_D_width':str(width_B/width_D)},
 'last_subtraction_binary64_absolute_errors':list(map(str,last_step_errors)),
 'last_subtraction_errors_less_than':'1/1000000000000000',
 'binary64_scope':'Only a demonstration of the final displayed-endpoint subtraction; actual producer arithmetic audited separately',
 'cube_carrier_count':256,'summary_count':128,'complete_fiber_size':2,
 'zero_summary_complete_fiber':[zero,hidden],
 'h_flip_distinguishing_site':6,
 'Q_interval':list(map(str,Q)),'nearest_half_up_roundings':roundings,
 'same_rounded_different_exact_witnesses':witnesses,
 'retained_scalings':scales,
 'claim_ceiling':'Exact finite models and rounded readout of attributed bounds; no new BSD enclosure or exact identity'}
args.output.parent.mkdir(parents=True,exist_ok=True)
args.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:result[k] for k in ('status','widths','last_subtraction_binary64_absolute_errors',
 'nearest_half_up_roundings','same_rounded_different_exact_witnesses')},indent=2))
