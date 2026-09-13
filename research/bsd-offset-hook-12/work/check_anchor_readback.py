"""Exact reference-assisted readback of the old bound in two decimal frames."""
from fractions import Fraction as F
from pathlib import Path
import argparse,json,hashlib

root=Path(__file__).resolve().parents[1]
ap=argparse.ArgumentParser(description=__doc__)
ap.add_argument('--input',type=Path,default=root/'evidence/hooks.json')
ap.add_argument('--output',type=Path,required=True)
args=ap.parse_args()
if args.output.exists():raise FileExistsError('Preserve prior evidence')
data=json.loads(args.input.read_text())
rows=[]
for row in data['fresh_distance_rows']:
    for side,shown in enumerate(row['distance_display10']):
        for width,prefix,key in ((3,'2.034','after_three_place_anchor'),(4,'2.0340','after_four_place_anchor')):
            suffix=row[key][side]
            value=F(prefix)+F(int(suffix),10**(width+len(suffix)))
            assert value==F(shown)
            rows.append({'depth':row['depth'],'side':side,'prefix':prefix,'prefix_width':width,
                         'suffix':suffix,'suffix_width':len(suffix),'recovered_value':str(value)})
target=[]
for row in rows:
    if row['depth']!=9 or row['side']!=0:continue
    suffix=row['suffix'];matches=[]
    for record in data['records']:
        for left in range(1,4):
            for right in range(1,4):
                if '0'*left+record['code']+'0'*right==suffix:
                    matches.append((record,left,right))
    assert len(matches)==1
    record,left,right=matches[0]
    packet={'prefix':row['prefix'],'prefix_width':row['prefix_width'],
            'hook':record['half_gap_hook'],'reference_A':record['A'],
            'left_frame':left,'right_frame':right,'decoder':'seven-state direct-code/half-gap'}
    delta=int(packet['hook'][1]);a=packet['reference_A']
    assert delta>=1 and a>=0 and 2*a+3*delta<=9
    recovered='0'*left+f'{delta}{2*delta}{a}'+'0'*right
    assert recovered==suffix
    recovered_value=F(packet['prefix'])+F(int(recovered),10**(packet['prefix_width']+len(recovered)))
    assert recovered_value==F('2.0340012300')
    target.append({'packet':packet,'recovered_suffix':recovered,'recovered_bound':str(recovered_value)})
assert len(target)==2
assert target[0]['packet']['hook']==target[1]['packet']['hook']=='010'
assert target[0]['packet']['left_frame']==target[1]['packet']['left_frame']+1
result={'status':'REFERENCE_AND_FRAME_READBACK_VERIFIED','all_offset_frames':rows,
        'two_lossless_packets_for_same_old_lower_bound':target,
        'visible_hook_alone_recovers_bound':False,'full_BSD_comparison':'OPEN',
        'input_sha256':hashlib.sha256(args.input.read_bytes()).hexdigest(),
        'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
args.output.parent.mkdir(parents=True,exist_ok=True)
args.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,indent=2))
