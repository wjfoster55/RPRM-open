"""Check the existing P involution against reverse-overlap and retained carry."""
from itertools import product
from fractions import Fraction
from pathlib import Path
from hashlib import sha256
import argparse,json

ap=argparse.ArgumentParser(description=__doc__)
ap.add_argument('--output',type=Path,required=True)
args=ap.parse_args()
if args.output.exists():raise FileExistsError('Use a fresh evidence path')
P=(5,9,8,3,6,0,4,7,2,1)
assert sorted(P)==list(range(10)) and all(P[P[d]]==d for d in range(10))
def pword(w):return ''.join(str(P[int(d)]) for d in w)
def hinge(w):
    rev=w[::-1]
    for k in range(len(w),-1,-1):
        if k==0 or w[-k:]==rev[:k]:return w+rev[k:]
    raise AssertionError('Unreachable')
rows=[]
for a,b in product('0123456789',repeat=2):
    w=a+b
    assert pword(pword(w))==w
    assert pword(hinge(w))==hinge(pword(w))
    rows.append({'word':w,'P_word':pword(w),'F_word':hinge(w),
                 'P_after_F':pword(hinge(w)),'F_after_P':hinge(pword(w))})
assert pword('59')=='01' and pword('595')=='010'
assert pword('55')=='00' and hinge('00')=='00'
assert pword('592595')=='018010'
typed_certificate={'source':pword('59'),'opcode':'2','output':pword('595')}
assert '|'.join(typed_certificate.values())=='01|2|010'

# Conjugate the same cyclic successor; ordinary +1 is not preserved by P.
conjugate_successor=[P[(P[d]+1)%10] for d in range(10)]
assert conjugate_successor[0]==4 and conjugate_successor[1]==5
carry_rows=[]
for n in range(99):
    q,d=divmod(n,10);q1,d1=divmod(n+1,10)
    chart_before=(P[d],q);chart_after=(P[d1],q1)
    assert 10*chart_before[1]+P[chart_before[0]]==n
    assert 10*chart_after[1]+P[chart_after[0]]==n+1
    carry_rows.append({'raw_before':[d,q],'raw_after':[d1,q1],
                      'P_chart_before':chart_before,'P_chart_after':chart_after})
assert carry_rows[9]['P_chart_before']==(1,0)
assert carry_rows[9]['P_chart_after']==(5,1)
assert Fraction(5,9)!=Fraction(0,1)
ratio_example={'raw':'5/9','naive_ratio_after_P':'0',
 'preserved_readout':'P_inverse(0)/P_inverse(1) = 5/9'}
report={'status':'P_HINGE_COMMUTATION_AND_CARRY_CONJUGATION_CHECKED',
 'source_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
 'existing_P_images':P,'all_100_word_rows':rows,'target':next(r for r in rows if r['word']=='59'),
 'typed_certificate_after_payload_P':typed_certificate,
 'untyped_full_word_after_P':'018010',
 'conjugate_cyclic_successor':conjugate_successor,'all_99_retained_carry_steps':carry_rows,
 'ratio_countercase':ratio_example,
 'claim_ceiling':'Exact equivariance of a declared word operation; no BSD scalar relation or universal numeral meaning'}
args.output.parent.mkdir(parents=True,exist_ok=True)
args.output.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:report[k] for k in ('status','target','typed_certificate_after_payload_P',
 'conjugate_cyclic_successor','ratio_countercase')},indent=2))
