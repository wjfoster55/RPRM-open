"""Exact origin, widening and ambiguity checks for the discrepancy digit words."""
from fractions import Fraction as F
from pathlib import Path
from hashlib import sha256
from datetime import datetime,timezone
import argparse,json

root=Path(__file__).resolve().parents[1]
ap=argparse.ArgumentParser(description=__doc__)
ap.add_argument('--output',type=Path,required=True)
args=ap.parse_args()
if args.output.exists():raise FileExistsError('Use a new evidence path')
scale=10**9
A=(F('6.38511803'),F('6.38518585'))
B=(F('6.384593255'),F('6.385625424'))
D=(A[0]-B[1],A[1]-B[0])
assert D==(F(-507394,scale),F(592595,scale))
assert A[1]*scale-B[0]*scale==592595
assert B[1]*scale-A[0]*scale==507394
assert '507394'[-4:]=='7394' and '507394'[:-4]=='50'

def joint(w):
    v=w[::-1]
    for k in range(len(w),-1,-1):
        if k==0 or w[-k:]==v[:k]:return w+v[k:]
    raise AssertionError('unreachable')
def certificate(w):return w+'2'+joint(w)
assert certificate('59')=='592595'
assert certificate('58')=='582585'
assert certificate('55')=='55255'
words=[str(i).zfill(2) for i in range(100)]
all_rows=[{'source':w,'reversed':w[::-1],'joined':joint(w),'certificate':certificate(w)} for w in words]
assert len({r['certificate'] for r in all_rows})==100
assert all(r['certificate'][:2]==r['source'] for r in all_rows)
assert sum(joint(w)==w for w in words)==10

widened=(D[0]-F(1,scale),D[1]+F(1,scale))
assert widened[0]<D[0]<=D[1]<widened[1]
assert widened==(F(-507395,scale),F(592596,scale))
assert '592596'!=certificate('59')
assert F(592595,scale)==F(5925950,10*scale)

examples=[]
for defect in (F(0),F(1,10000)):
    a=F('6.38515');b=a-defect
    assert A[0]<=a<=A[1] and B[0]<=b<=B[1]
    assert a-b==defect
    examples.append({'hypothetical_A':str(a),'hypothetical_B1':str(b),'D':str(defect)})

result={'status':'BOUNDED_DISPLAY_AND_GRAMMAR_CHECKS_PASS','created_utc':datetime.now(timezone.utc).isoformat(),
    'attributed_prior_inputs':{'A':list(map(str,A)),'B1':list(map(str,B))},
    'integer_origin':{'upper_subtraction':[int(A[1]*scale),int(B[0]*scale),592595],
                      'lower_magnitude_subtraction':[int(B[1]*scale),int(A[0]*scale),507394],
                      'scale':scale,'lower_suffix':'7394','omitted_lower_prefix':'50'},
    'fresh_L_or_height_run':False,'all_100_word_cases':all_rows,
    'literal_doubling_59':118,'literal_duplication_59':'5959',
    'candidate_is_post_target':True,'max_overlap_fixed_words':[w for w in words if joint(w)==w],
    'widened_bound_numerators':[-507395,592596],
    'same_value_rescaled_record':[5925950,10*scale],
    'both_consistent_with_supplied_intervals':examples,
    'example_scope':'Interval-level ambiguity only, not alternate actual BSD values',
    'user_grammar':'OPEN: multiple possible rules; this candidate is not independently selected',
    'BSD_zero_defect':'OPEN: no new equation from the L-function and regulator definitions',
    'source_sha256':sha256(Path(__file__).read_bytes()).hexdigest()}
args.output.parent.mkdir(parents=True,exist_ok=True)
args.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:result[k] for k in ('status','integer_origin','max_overlap_fixed_words','both_consistent_with_supplied_intervals','user_grammar')},indent=2))
