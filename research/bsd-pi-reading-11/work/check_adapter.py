"""Read a fresh distance enclosure through the explicitly declared digit chart."""
from fractions import Fraction as F
from pathlib import Path
import argparse
import json
import hashlib

root=Path(__file__).resolve().parents[1]
ap=argparse.ArgumentParser(description=__doc__)
ap.add_argument('--input',type=Path,default=root/'evidence/reading.json')
ap.add_argument('--output',type=Path,default=root/'evidence/adapter.json')
args=ap.parse_args()
source=args.input
out=args.output
if out.exists():raise FileExistsError('Preserve the earlier adapter evidence')
data=json.loads(source.read_text())
interval=tuple(map(F,data['fresh_distance'][-1]['distance_rational']))
def floor(x):return x.numerator//x.denominator
def extract(x):
    if not F(2)<=x<F(21,10):raise ValueError('Outside declared real carrier')
    return floor(100*x)%10,floor(1000*x)%10
table={tuple(r['endpoint_midpoint']):r['word'] for r in data['zip_chart_full_carrier']}
def decode(x):
    key=extract(x)
    if key not in table:raise ValueError('Digit pair outside admitted seven-state chart')
    return table[key]
assert F('2.0340')<interval[0]<=interval[1]<F('2.0341')
assert floor(interval[0]*10000)==floor(interval[1]*10000)==20340
assert extract(interval[0])==extract(interval[1])==(3,4)
assert decode(interval[0])==decode(interval[1])==data['certified_pi_window']
assert len(table)==len(set(table.values()))==7
grid=[]
for h in range(10):
    for k in range(10):
        lo=F(2)+F(h,100)+F(k,1000);hi=lo+F(1,1000)
        assert extract(lo)==extract((lo+hi)/2)==(h,k)
        grid.append({'key':[h,k],'fiber_half_open':[str(lo),str(hi)],'word':table.get((h,k)),
                     'disposition':'ONE_WORD' if (h,k) in table else 'ADMISSION_ERROR'})
hits=[r for r in grid if r['word']==data['certified_pi_window']]
assert len(hits)==1 and tuple(map(F,hits[0]['fiber_half_open']))==(F('2.034'),F('2.035'))
counterexamples=[F('2.0342'),F('2.0348')]
assert counterexamples[0]!=counterexamples[1]
assert all(decode(x)==data['certified_pi_window'] for x in counterexamples)
assert all(x>interval[1] for x in counterexamples)
admission_count=sum(r['disposition']=='ADMISSION_ERROR' for r in grid)
assert admission_count==93
result={'status':'EXACT_DECLARED_ADAPTER_AND_COMPLETE_FIBER','carrier':'real interval[2,2.1), infinite',
 'receiver':'hundredths/thousandths pair;100 states','admitted_decoder_states':7,'inadmissible_decoder_states':93,
 'actual_distance_interval':list(map(str,interval)),'certified_leading_fractional_digits':'0340',
 'actual_distance_key':[3,4],'decoder_output':data['certified_pi_window'],
 'decoder_pi_window_fiber':{'kind':'MANY','half_open_interval':['2.034','2.035']},
 'distinct_values_outside_actual_distance_interval_with_same_word':list(map(str,counterexamples)),
 'complete_receiver_table':grid,'root_input_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
 'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'preserves_full_real_value':False,'predicts_pi_beyond_given_finite_window':False,
 'role_choice':'explicit proposed adapter, not mathematically forced by glyphs',
 'full_BSD_comparison':'OPEN'}
out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:result[k] for k in ('status','actual_distance_key','decoder_output','decoder_pi_window_fiber','full_BSD_comparison')},indent=2))
