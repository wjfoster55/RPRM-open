"""Fresh exact interval, decimal-format and finite RPRM chart checks."""
from fractions import Fraction as F
from pathlib import Path
from collections import Counter
import argparse
import hashlib
import importlib.util
import json

OLD_LO='2.0339867006'
OLD_HI='2.0340237084'
ZIP_PAIRS=((0,2),(0,4),(0,6),(1,3),(1,5),(2,4),(3,5))
P={0:5,1:9,2:8,3:3,4:6,5:0,6:4,7:7,8:2,9:1}
N={d:-d%10 for d in range(10)}
T={d:P[N[d]] for d in range(10)}
M={d:9-d for d in range(10)}
MAPS={'I':{d:d for d in range(10)},'P':P,'N':N,'T':T,'M':M}

def atan_bound(x,terms=24):
    assert 0<x<1
    s=sum(((-1)**j*x**(2*j+1)/F(2*j+1) for j in range(terms)),F(0))
    next_term=(-1)**terms*x**(2*terms+1)/F(2*terms+1)
    return min(s,s+next_term),max(s,s+next_term)

def pi_bound():
    # tan(4atan(1/5)-atan(1/239))=1 on the principal first-quadrant branch.
    a=F(1,5); twice=2*a/(1-a*a); four=2*twice/(1-twice*twice)
    assert (four-F(1,239))/(1+four/F(239))==1
    lo,hi=atan_bound(a); ll,uu=atan_bound(F(1,239))
    return 16*lo-4*uu,16*hi-4*ll

def disjoint(a,b): return a[1]<b[0] or b[1]<a[0]
def shift(interval,k): return tuple(x*F(10)**k for x in interval)
def fixed(n,digits):
    return str(n//10**digits)+'.'+str(n%10**digits).zfill(digits)
def nearest_range(interval,digits):
    # Positive real values: nearest, ties upward. Our admitted interval avoids ties.
    vals=[(x*10**digits+F(1,2)).numerator//(x*10**digits+F(1,2)).denominator for x in interval]
    return [fixed(x,digits) for x in vals]
def digits(s): return ''.join(c for c in s if c.isdigit())

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args()
    if args.output.exists(): raise FileExistsError('Preserve evidence; use new output')
    root=Path(__file__).resolve().parents[1]
    kernel_path=root/'work/height_kernel.py'
    spec=importlib.util.spec_from_file_location('height_kernel',kernel_path)
    h=importlib.util.module_from_spec(spec); spec.loader.exec_module(h)
    p=(F(-2),F(48));q=(F(-16),F(120))
    r=h.add(p,h.negate(q)); assert r==(F(162),F(-2016))
    rows=[]
    for depth in (8,9):
        h.DEPTH=depth
        D,ledger=h.height(r); distance=h.sqrt_interval(D,digits=12)
        rows.append({'depth':depth,'height_interval':h.decimal_interval(D,12),
                     'distance_interval':h.decimal_interval(distance,12),
                     'distance_rational':list(map(str,distance)),
                     'ledger':ledger,
                     'rounding':{str(k):nearest_range(distance,k) for k in (3,4,5,6)},
                     'zero_counts':{str(k):[digits(w).count('0') for w in h.decimal_interval(distance,k)] for k in (4,6,10,12)}})
        print('fresh height depth'+str(depth)+' completed',flush=True)
    old=(F(OLD_LO),F(OLD_HI))
    fresh8=tuple(map(F,rows[0]['distance_rational']))
    assert old[0]<=fresh8[0]<=fresh8[1]<=old[1]
    pi=pi_bound(); other=(4-pi[1],4-pi[0])
    assert F(314,100)<pi[0]<pi[1]<F(315,100)
    numeric=[]
    for name,source in (('pi',pi),('4-pi',other)):
        for k in range(-6,7):
            target=shift(source,k)
            numeric.append({'claim':f'd=10^{k}*({name})','compatible_with_original_distance':not disjoint(old,target)})
    square_minus_one=(old[0]**2-1,old[1]**2-1)
    pi_window_l=(pi[0]*10**10).numerator//(pi[0]*10**10).denominator
    pi_window_u=(pi[1]*10**10).numerator//(pi[1]*10**10).denominator
    assert pi_window_l==pi_window_u
    piword=str(pi_window_l)
    charts=[]
    for a,b in ZIP_PAIRS:
        middle=F(a+b,2); delta=F(b-a,2)
        assert middle.denominator==delta.denominator==1
        middle=int(middle);delta=int(delta)
        assert (a,2*middle-a)==(a,b)
        grid=[[delta,a+delta,delta],[a+2*delta,2*a+3*delta,2*delta],[a+3*delta,a+2*delta,a]]
        assert all(0<=v<=9 for row in grid for v in row)
        word=str(a)+''.join(str(v) for row in grid for v in row)+str(b)
        charts.append({'endpoints':[a,b],'endpoint_midpoint':[a,middle],
                      'delta':delta,'reconstructed_right':2*middle-a,
                      'grid':grid,'word':word,'is_initial_pi_window':word==piword})
    complete=[(a,a+2*delta) for a in range(10) for delta in range(1,10) if 2*a+3*delta<=9]
    assert sorted(complete)==sorted(ZIP_PAIRS)
    endpoint_midpoint=[r for r in charts if r['endpoint_midpoint']==[3,4]]
    endpoint_endpoint=[r for r in charts if r['endpoints']==[3,4]]
    assert len(endpoint_midpoint)==1 and not endpoint_endpoint
    assert endpoint_midpoint[0]['word']==piword
    wordtests=[]
    for original in (OLD_LO,OLD_HI):
        word=digits(original); cases=[]
        for name,mapping in MAPS.items():
            mapped=''.join(str(mapping[int(c)]) for c in word)
            for reverse in (False,True):
                w=mapped[::-1] if reverse else mapped
                for rotate in range(len(w)):
                    out=w[rotate:]+w[:rotate]
                    cases.append({'map':name,'reverse':reverse,'left_rotation':rotate,'output':out,'equals_pi_prefix':out==piword})
        wordtests.append({'original':original,'word':word,'digit_counts':dict(Counter(word)),
                          'tested_operations':len(cases),'matches':[r for r in cases if r['equals_pi_prefix']],
                          'all_outputs':cases})
    # Equal endpoint zero counts depend on representation: append a valid zero.
    zero_control={'original_counts':[digits(s).count('0') for s in (OLD_LO,OLD_HI)],
                  'same_value_padded_counts':[digits(s+'0').count('0') for s in (OLD_LO,OLD_HI)]}
    for s in (OLD_LO,OLD_HI): assert F(s)==F(s+'0')
    result={'status':'BOUNDED_RPRM_PI_READING_TESTED','old_bounds':[OLD_LO,OLD_HI],
      'fresh_distance':rows,'pi_interval':h.decimal_interval(pi,24),'pi_definition':'16atan(1/5)-4atan(1/239), alternating tails24terms',
      'certified_pi_window':piword,'rounding_of_entire_original_interval':nearest_range(old,4),
      'old_zero_observation':zero_control,'decimal_shift_tests':numeric,
      'squared_distance_minus_unit_pi':{'compatible':not disjoint(square_minus_one,pi),'interval':h.decimal_interval(square_minus_one,12)},
      'zip_chart_full_carrier':charts,'34_endpoint_midpoint_fiber':endpoint_midpoint,
      '34_endpoint_endpoint_fiber':endpoint_endpoint,'word_tests':wordtests,
      'conclusions':{'four_decimal_rounding':'ONE(2.0340)','endpoint_midpoint34':'ONE(35) in the historical seven-record chart',
       'full_user_zip_grammar':'OPEN_NOT_SPECIFIED','distance_to_pi_identity':'OPEN_NO_SOURCE_DERIVED_ADAPTER',
       'real_BSD_comparison':'OPEN','pi_map_output_ceiling':'finite certified prefix selector, no new full-pi generator'},
      'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
      'height_kernel_sha256':hashlib.sha256(kernel_path.read_bytes()).hexdigest()}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:result[k] for k in ('status','rounding_of_entire_original_interval','old_zero_observation','34_endpoint_midpoint_fiber','conclusions')},indent=2))
    print(json.dumps([{k:r[k] for k in ('depth','height_interval','distance_interval','rounding','zero_counts')} for r in rows],indent=2))

if __name__=='__main__':main()
