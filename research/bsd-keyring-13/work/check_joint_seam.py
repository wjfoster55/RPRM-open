"""Check when a shared middle block fails during joint interval carry."""
from fractions import Fraction as F
from hashlib import sha256
import argparse, importlib.util, json
from pathlib import Path

root=Path(__file__).resolve().parents[1]
source=root/'work/check_keyring.py'
spec=importlib.util.spec_from_file_location('keyring',source)
k=importlib.util.module_from_spec(spec);spec.loader.exec_module(k)
ap=argparse.ArgumentParser(description=__doc__)
ap.add_argument('--output',type=Path,required=True)
args=ap.parse_args()
if args.output.exists():raise FileExistsError('Use a new evidence path')
same=split=0
for p in range(10):
    for a in range(20):
        for b in range(a,20):
            low,_=k.carry(2,p,a,1,1);high,_=k.carry(2,p,b,1,1)
            assert k.value(*low,1,1)<=k.value(*high,1,1)
            different=low[:2]!=high[:2]
            assert different==(a<10<=b)
            if different:split+=1
            else:same+=1
assert (same,split)==(1100,1000)
actual=[]
for t in (10**8-1,10**8):
    normalized,tags=k.carry(2,340,t,4,8)
    x=k.value(*normalized,4,8)
    assert x==k.value(2,340,t,4,8)
    actual.append({'raw_tail':t,'normalized':normalized,'tags':tags,'value':str(x),
                   'fixed_width_readout':k.recover(x,4,8)})
assert actual[0]['fixed_width_readout'][1]=='0340'
assert actual[1]['fixed_width_readout'][1]=='0341'
result={'status':'JOINT_CARRY_BOUNDARY_EXCEPTION_VERIFIED','carrier':'I=2,P=0..9,0<=a<=b<20,w=m=1',
        'same_prefix_cases':same,'split_prefix_cases':split,
        'actual_width_control':actual,
        'obligation':'At a straddled carry boundary, retain endpoint-specific prefixes or an extended common-frame offset. A single normalized middle word is insufficient.',
        'source_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
        'dependency_sha256':sha256(source.read_bytes()).hexdigest()}
args.output.parent.mkdir(parents=True,exist_ok=True)
args.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,indent=2))
