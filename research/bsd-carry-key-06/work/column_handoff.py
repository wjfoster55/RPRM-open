"""Exact audit of the user's 5426 -> 566 compression and shadow handoff."""
import argparse
from collections import defaultdict
from datetime import datetime,timezone
from hashlib import sha256
import json
from pathlib import Path


def fold(n):
    return 10*(n//100)+n%100


def shift_digits(n,width=4):
    return int(''.join(str((int(d)+1)%10) for d in str(n).zfill(width)))


def weighted_marks(n):
    marks=[0]*10
    for weight,digit in zip((100,10,10,1),str(n).zfill(4)):
        marks[int(digit)]+=weight
    return tuple(marks)


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args()
    if args.output.exists(): raise FileExistsError('Use a new evidence file')
    a,m=2301,3125
    assert a+m==5426
    assert fold(a)==231 and fold(m)==335 and fold(a+m)==566
    # All local carry pairs: incoming ones carries are already in each remainder.
    for r in range(100):
        for s in range(100):
            k=(r+s)//100
            assert fold(r+s)==fold(r)+fold(s)-90*k
    # All canonical coefficient candidates with this fixed precision modulus.
    for b in range(m):
        k=((b%100)+(m%100))//100
        assert fold(b+m)==fold(b)+fold(m)-90*k
    image_fiber=[n for n in range(10000) if fold(n)==566]
    coefficients=[b for b in range(m) if fold(b+m)==566]
    zero_mask=[b for b in coefficients if (b//10)%10==0]
    old_residue=[b for b in coefficients if b%625==426]
    assert zero_mask==old_residue==[2301]
    next_lifts=[426+625*t for t in range(5)]
    assert [b for b in next_lifts if (b//10)%10==0]==[2301]

    # Transport M through the fold at the declared width, retaining its true range.
    fibers=defaultdict(list)
    for n in range(10000):
        y=fold(n);fibers[y].append(n)
        assert fold(9999-n)==1089-y
    ambiguous=[]
    for y,preimages in fibers.items():
        targets={fold(shift_digits(n)) for n in preimages}
        if len(targets)>1: ambiguous.append(y)
    assert fold(4796)==fold(5426)==566
    assert fold(shift_digits(4796))==587
    assert fold(shift_digits(5426))==687
    assert shift_digits(566,3)==677
    # Complete stable carrier for the admitted uniform digit maps S and M.
    mark_classes=set();future_classes=set()
    for n in range(10000):
        w=weighted_marks(n);mark_classes.add(w)
        assert sum(w)==121 and sum(j*w[j] for j in range(10))==fold(n)
        shifted=weighted_marks(shift_digits(n))
        assert shifted==tuple(w[(j-1)%10] for j in range(10))
        assert weighted_marks(9999-n)==tuple(w[9-j] for j in range(10))
        assert fold(shift_digits(n))==fold(n)+121-10*w[9]
        x=n;future=[]
        for k in range(10):
            future.append(fold(x));x=shift_digits(x)
        assert x==n
        future_classes.add(tuple(future))
    assert len(mark_classes)==len(future_classes)==5500
    path=[];x=5426
    for k in range(11):
        path.append({'step':k,'source_word':str(x).zfill(4),'compressed':fold(x),
                     'next_wrap_weight':weighted_marks(x)[9]})
        x=shift_digits(x)
    safe_source={0,5}
    safe_shadow={(d+1)%10 for d in safe_source}
    assert safe_shadow=={1,6}
    source=Path(__file__)
    report={
        'created_utc':datetime.now(timezone.utc).isoformat(),
        'source_sha256':sha256(source.read_bytes()).hexdigest(),
        'status':'COMPRESSION_CARRY_AND_CONDITIONAL_HANDOFF_AUDITED',
        'user_supplied_stage':'566 IS INTERMEDIATE; terminal readout is not selected',
        'source_example':{'coefficient':a,'modulus':m,'sum':a+m,
                          'folded_terms':[fold(a),fold(m)],'folded_sum':fold(a+m)},
        'fold':{'domain':[0,9999],'range':[0,1089],
                'formula':'F(n)=10*floor(n/100)+(n mod100)',
                'addition_defect':'F(n+m)=F(n)+F(m)-90*k; k=floor(((n mod100)+(m mod100))/100)',
                'local_carry_pairs_checked':10000,'fixed_modulus_candidates_checked':3125,
                'failed_additivity_control':{'inputs':[99,1],'sum_after_fold':100,'fold_after_sum':10},
                'all_total_preimages_of566':image_fiber,
                'all_coefficient_preimages_with_modulus3125':coefficients,
                'inverse_with_tens_zero':zero_mask,'inverse_with_old_residue':old_residue,
                'next_lifts_and_folded_sums':[{'coefficient':b,'compressed_sum':fold(b+m)} for b in next_lifts]},
        'shadow':{'maps':'M(d)=9-d; N(d)=(-d) mod10; S=N after M',
                  'digit5_path':[5,4,6],
                  'transported_checkpoint_set':{'source':sorted(safe_source),'image':sorted(safe_shadow),
                     'scope':'Illustrative transport of the historical checkpoint guard; no universal safety claim'},
                  'exact_M_transport':'M_F(y)=1089-y',
                  'M_transport_example':{'source':5426,'source_shadow':4573,'folded_shadow':523,
                                         'naive_three_digit_shadow':433,'difference':90},
                  'S_descent_ambiguous_output_count':len(ambiguous),
                  'S_descent_total_output_count':len(fibers),
                  'S_descent_witness':[{'source':n,'fold':fold(n),'shadow':shift_digits(n),'fold_after_shadow':fold(shift_digits(n))} for n in (4796,5426)],
                  'conditional_handoff_with_old_residue':{'compressed_input':566,'recovered_sum':5426,
                     'source_shadow':6537,'compressed_shadow':687,'operation_status':'CANDIDATE S, not uniquely identified as user intended'},
                  'different_operation_on_three_digit_word':{'input':566,'output':677}},
        'retained_shadow_carrier':{'marks':'W[j]=weighted count of source digit j with weights(100,10,10,1)',
                                  'source_states':10000,'complete_operational_classes':len(mark_classes),
                                  'S_update':'W_next[j]=W[(j-1) mod10]',
                                  'M_update':'W_next[j]=W[9-j]',
                                  'readout':'sum(j*W[j])',
                                  'next_readout':'F_next=F+121-10*W[9]',
                                  'ten_step_path':path,
                                  'preserved_operations':'uniform S and M on every source digit; observing F',
                                  'forgotten':'order of the two middle source digits; other positional operations require a new audit'},
        'claim_ceiling':'Exact finite operations and inverse repair. The zero mask or compressed value is observed data, not an independent prediction of the analytic coefficient. BSD comparison remains OPEN.'
    }
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'status':report['status'],'total_fiber':image_fiber,
                      'repaired_coefficient':zero_mask,'shadow_ambiguous_fibers':len(ambiguous),
                      'conditional_candidate_handoff':687},indent=2))


if __name__=='__main__':main()
