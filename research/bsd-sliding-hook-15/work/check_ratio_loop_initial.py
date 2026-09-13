"""Exact two-ratio reading of a mirrored hinge path, including zero guards."""
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import argparse,json

ap=argparse.ArgumentParser(description=__doc__)
ap.add_argument('--output',type=Path,required=True)
args=ap.parse_args()
if args.output.exists():raise FileExistsError('Use a new evidence path')
rows=[];excluded=[]
for a in range(10):
    for b in range(10):
        if a==0 or b==0:
            excluded.append({'word':f'{a}{b}','reason':'one or both required ratio denominators are zero'})
            continue
        out,back=F(a,b),F(b,a)
        assert out*back==1
        assert (out==1)==(a==b)
        rows.append({'word':f'{a}{b}','path':[a,b,a],'out':str(out),'back':str(back),'product':'1'})
assert len(rows)==81 and len(excluded)==19
target=next(r for r in rows if r['word']=='59')
assert target['out']=='5/9' and target['back']=='9/5'
a=F('6.38515');b=F('6.38505')
assert a-b==F(1,10000) and (a/b)*(b/a)==1 and a/b!=1
result={'status':'RATIO_ROUNDTRIP_AND_COUNTERCASE_VERIFIED','all_81_admitted_rows':rows,
        'all_19_excluded_words':excluded,'product_one_fiber':{'kind':'MANY','size':81},
        'target_59':target,'unit_first_leg_words':[r['word'] for r in rows if r['out']=='1'],
        'interval_compatible_nonzero_defect_control':{'A':str(a),'B1':str(b),
            'D':str(a-b),'A_over_B1':str(a/b),'roundtrip_product':'1'},
        'claim_ceiling':'A ratio roundtrip equals one for unequal inputs too; no BSD equality follows',
        'source_sha256':sha256(Path(__file__).read_bytes()).hexdigest()}
args.output.parent.mkdir(parents=True,exist_ok=True)
args.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:result[k] for k in ('status','product_one_fiber','target_59','interval_compatible_nonzero_defect_control')},indent=2))
