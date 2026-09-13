"""Exact bounded hook decoders, anchor offsets and fresh height refinement."""
from fractions import Fraction as F
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,importlib.util,json

def overlap(a,b):
    for k in range(min(len(a),len(b)),-1,-1):
        if k==0 or a[-k:]==b[:k]:return a+b[k:],k
    raise AssertionError('Unreachable empty overlap')

def framed_core_matches(word,records):
    return [{'code':r['code'],'left_zeros':l,'right_zeros':z}
            for r in records for l in range(1,4) for z in range(1,4)
            if '0'*l+r['code']+'0'*z==word]

def phases(word,query,orientation=1):
    return [p for p in range(len(word))
            if all(word[(p+orientation*j)%len(word)]==c for j,c in enumerate(query))]

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args()
    if args.output.exists():raise FileExistsError('Use a new evidence path')
    root=Path(__file__).resolve().parents[1]
    kernel_path=root/'work/height_kernel.py'
    spec=importlib.util.spec_from_file_location('height_kernel',kernel_path)
    h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
    records=[]
    for delta in range(1,4):
        for a in range(10):
            if 2*a+3*delta>9:continue
            code=f'{delta}{2*delta}{a}'
            residual=a-2*delta
            residual_word='0'+str(residual)
            first,k1=overlap('0',residual_word)
            hook,k2=overlap(first,'0')
            records.append({'A':a,'B':a+2*delta,'delta':delta,'midpoint':a+delta,
                            'code':code,'residual':residual,'residual_word':residual_word,
                            'half_gap_hook':f'0{delta}0','residual_overlap_hook':hook,
                            'overlaps':[k1,k2]})
    assert len(records)==7
    midpoint_fibers={str(m):[r['code'] for r in records if r['midpoint']==m] for m in range(1,5)}
    delta_fibers={str(k):[r['code'] for r in records if r['delta']==k] for k in range(1,4)}
    residual_fibers={r['residual_overlap_hook']:[s['code'] for s in records if s['residual_overlap_hook']==r['residual_overlap_hook']] for r in records}
    assert all(len(v)==1 for v in residual_fibers.values())
    fixed_anchor=[r['code'] for r in records if r['delta']==1 and r['A']==3]
    assert fixed_anchor==['123']
    roundtrips=[]
    for r in records:
        for l in range(1,4):
            for z in range(1,4):
                original='0'*l+r['code']+'0'*z
                # Full frame+anchor packet, not just its visible three-character hook.
                packet={'anchor_A':r['A'],'half_gap_hook':r['half_gap_hook'],'left_zeros':l,'right_zeros':z}
                dd=int(packet['half_gap_hook'][1]); aa=packet['anchor_A']
                recovered_code=f'{dd}{2*dd}{aa}'
                recovered='0'*l+recovered_code+'0'*z
                assert recovered==original
                roundtrips.append({'source':original,'packet':packet,'recovered':recovered})
    assert len(roundtrips)==63
    target_words={w:framed_core_matches(w,records) for w in ('0012300','01230','010','01200')}
    assert len(target_words['0012300'])==len(target_words['01230'])==1
    assert not target_words['010']
    # '01200' has direct core120; greedy zero stripping would wrongly give12.
    assert target_words['01200'][0]['code']=='120'
    p=(F(-2),F(48));q=(F(-16),F(120));r=h.add(p,h.negate(q))
    assert r==(F(162),F(-2016))
    anchor=F('2.0340');distance_rows=[]
    for depth in (9,10):
        h.DEPTH=depth
        D,ledger=h.height(r); d=h.sqrt_interval(D,12)
        a4=tuple(10000*(x-anchor) for x in d)
        a3=tuple(1000*(x-anchor) for x in d)
        assert a4==tuple(10*x for x in a3)
        assert tuple(anchor+x/F(10000) for x in a4)==d
        display=h.decimal_interval(d,10)
        assert all(s.startswith('2.0340') for s in display)
        after3=[s[len('2.034'):] for s in display]
        after4=[s[len('2.0340'):] for s in display]
        assert all(a=='0'+b for a,b in zip(after3,after4))
        distance_rows.append({'depth':depth,'distance':list(map(str,d)),
             'distance_display12':h.decimal_interval(d,12),'distance_display10':display,
             'offset3':list(map(str,a3)),'offset4':list(map(str,a4)),
             'offset3_decimal':h.decimal_interval(a3,9),'offset4_decimal':h.decimal_interval(a4,8),
             'after_three_place_anchor':after3,'after_four_place_anchor':after4,
             'fixed_123_occurrences':[[(i,i+3) for i in range(len(s)-2) if s[i:i+3]=='123'] for s in after3],
             'framed_core_matches':[framed_core_matches(s,records) for s in after3],
             'ledger':ledger})
        print('height depth'+str(depth)+' completed',flush=True)
    circular=[]
    for word in ('31415926535','0012300','01230','0104820','010'):
        stabilizer=[p for p in range(len(word)) if word[p:]+word[:p]==word]
        circular.append({'word':word,'artificial_wrap':True,'stabilizer':stabilizer,
                         'queries':{s:{'forward':phases(word,s,1),'backward':phases(word,s,-1)}
                                    for s in ('3','5','35','53','123','01230','010')}})
    w='31415926535'
    semantic_endpoints={'A':{'index':0,'value':w[0]},'B':{'index':10,'value':w[10]}}
    assert phases(w,'35',1)==[9]
    assert phases(w,'35',-1)==[0,9]
    result={'status':'BOUNDED_HOOK_MODELS_AND_OFFSETS_TESTED','created_utc':datetime.now(timezone.utc).isoformat(),
      'records':records,'midpoint_fibers':midpoint_fibers,'half_gap_fibers':delta_fibers,
      'residual_overlap_fibers':residual_fibers,'anchor_A3_half_gap1_fiber':fixed_anchor,
      'frame_carrier':'left and right counts1..3; seven directcodes;63states',
      'framed_roundtrips':roundtrips,'literal_word_parses':target_words,
      'fresh_distance_rows':distance_rows,'circular_phase_tables':circular,
      'pi_semantic_endpoints':semantic_endpoints,
      'two_models_for010':['half-gap projection plus frame; requires A for code recovery',
                           'signed residual view plus maximal overlap; code recovery already unique on sevenstates'],
      'full_user_operation':'OPEN_MULTIPLE_COMPATIBLE_GRAMMARS',
      'independent_real_BSD_multiplier':'OPEN',
      'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
      'height_kernel_sha256':hashlib.sha256(kernel_path.read_bytes()).hexdigest()}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:result[k] for k in ('status','midpoint_fibers','half_gap_fibers','anchor_A3_half_gap1_fiber','literal_word_parses','full_user_operation')},indent=2))
    print(json.dumps([{k:r[k] for k in ('depth','distance_display12','after_three_place_anchor','after_four_place_anchor','fixed_123_occurrences','offset3_decimal','offset4_decimal')} for r in distance_rows],indent=2))

if __name__=='__main__':main()
