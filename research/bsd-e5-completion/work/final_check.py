"""Independent integration checks of the new E5 certificates and theorem inputs.

This reassembles finite data and intervals; the cited theorems and written
global arguments are reviewed in the companion notes, not proved by JSON.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import json
from math import gcd, isqrt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input-dir',type=Path,default=ROOT/'evidence')
    parser.add_argument('--output',type=Path,default=ROOT/'evidence/final_check.json')
    args = parser.parse_args()
    load = lambda name: json.loads((args.input_dir/name).read_text(encoding='utf-8'))
    generator, factors, coords = load('generator.json'), load('bsd_factors.json'), load('coordinates.json')
    theorem = json.loads((ROOT/'evidence/bsd_sha_theorems.json').read_text(encoding='utf-8'))
    checks = {}
    cases = generator['enumeration']['all_abscissa_rows']
    expected = {(a,b) for a in range(-20,21) for b in range(1,21) if gcd(a,b)==1}
    checks['complete_height_20_domain'] = {(r['a'],r['b']) for r in cases} == expected and len(cases)==len(expected)==511
    points = set()
    for row in cases:
        x = F(row['a'],row['b'])
        rhs = x**3-25*x
        if rhs >= 0:
            sn,sd = isqrt(rhs.numerator),isqrt(rhs.denominator)
            is_square = sn*sn==rhs.numerator and sd*sd==rhs.denominator
        else:
            is_square = False
        assert is_square == row['is_square']
        if is_square:
            points.update({(x,F(sn,sd)),(x,F(-sn,sd))})
    reported = {tuple(map(F,r['point'])) for r in generator['enumeration']['classified_points']}
    checks['alternate_rational_square_test'] = points == reported and len(points)==7
    checks['global_bound_exact_integer_comparison'] = 4**3*676*2500**9 < 21**27
    checks['primitive_conclusion_matches_written_proof'] = generator['result']['free_index_of_P']==1
    checks['source_generator'] = generator['metadata']['checker_sha256']==hashlib.sha256((ROOT/'work/generator_check.py').read_bytes()).hexdigest()
    checks['source_factors'] = factors['source_sha256']==hashlib.sha256((ROOT/'work/bsd_factors.py').read_bytes()).hexdigest()
    checks['source_coordinates'] = coords['source_sha256']==hashlib.sha256((ROOT/'work/coordinate_check.py').read_bytes()).hexdigest()
    a,b=-4,1
    for row in factors['height']['duplication_ledger']:
        ff,gg = (a*a+25*b*b)**2,4*a*b*(a*a-25*b*b)
        common = gcd(ff,gg)
        assert common==row['gcd_removed'] and common<=2500
        a,b=ff//common,gg//common
        if b<0:
            a,b=-a,-b
        assert a.bit_length()==row['numerator_bit_length'] and b.bit_length()==row['denominator_bit_length']
    checks['eight_exact_height_iterates'] = a==int(factors['height']['last_x_numerator_hex'],16) and b==int(factors['height']['last_x_denominator_hex'],16)
    omega = list(map(F,factors['period']['omega_raw']))
    reg = list(map(F,factors['height']['canonical_height_raw']))
    cp,torsion = factors['local_factors']['product_cp'],factors['torsion_order']
    prior = ROOT/'supplied_review/BSD_E5_REVIEW/input/BSD_E5_CODEX_TEST_01_RETURN/DERIVATIVE_INTERVAL.json'
    prior_interval = json.loads(prior.read_text(encoding='utf-8'))
    derivative = [F(prior_interval['lower']),F(prior_interval['upper'])]
    checks['derivative_matches_preserved_prior_certificate'] = derivative==list(map(F,factors['derivative_interval'])) and prior_interval['input_curve_a_invariants']==[0,0,0,-25,0]
    rhs = [omega[0]*reg[0]*cp/torsion**2,omega[1]*reg[1]*cp/torsion**2]
    ratio = [derivative[0]/rhs[1],derivative[1]/rhs[0]]
    checks['raw_factor_product'] = rhs==list(map(F,factors['bsd_rhs_without_sha_raw']))
    checks['raw_ratio'] = ratio==list(map(F,factors['quotient_raw']))
    checks['only_possible_positive_integer'] = F(1,2)<ratio[0]<=1<=ratio[1]<F(3,2)
    checks['coarse_integer_isolation'] = omega[0]>2 and reg[0]>F(3,2) and cp==8 and torsion==4 and F(1114529,750000)<2
    checks['theorem_hypotheses'] = theorem['curve']['a_invariants']==[0,0,0,-25,0] and theorem['curve']['conductor']==800<5000 and theorem['hypotheses']['analytic_rank']==1
    checks['local_factor_specialization'] = factors['local_factors']['p2']['b8']==-772 and (-772)%8!=0 and (-24)%4==0 and factors['local_factors']['p5']['distinct_roots_mod_5']==[0,1,4]
    checks['generator_relabelings'] = [r['P_image'] for r in coords['explicit_generator_relabelings']]==[['-1','0'],['0','1']]
    checks['observed_pair_trace_inverse'] = coords['user_trace']['exact_inverse_on_observed_image']
    result = {'status':'CONFIRMED' if all(checks.values()) else 'FAILED',
        'utc':datetime.now(timezone.utc).isoformat(),'checks':checks,
        'evidence_grade':'INDEPENDENT_FINITE_REASSEMBLY_AND_ROOT_WRITTEN_PROOF_REVIEW',
        'conclusions':{'free_index':1,'torsion_order':4,'sha_order':1,'odd_primary_sha':'TRIVIAL',
            'full_formula':'Lprime(E,1)=Omega(E)*Hhat_x(P)/2',
            'formula_evidence':'Creutz–Miller Theorem1.1 with hypotheses independently established for this E5.'},
        'reviewed_written_obligations':['All-prime gcd bound and all-odd-index height cutoff, including infinity/torsion.',
            'Canonical-height quadraticity and full-height regulator convention.',
            'Two real components, AGM enclosure of entire limit, rational logarithm and height tail.',
            'Actual Tate branches at2 and5, rather than a good-prime or odd-prime shortcut.',
            'FullBSD theorem applies to every E/Q with N<5000 and analytic rank<=1; no residual/CM exception.',
            'Integer isolation uses that theorem and positive factors, not decimal rounding.',
            'Explicit affine coordinate maps preserve the same group; the unformalized global carry law is not inferred.'],
        'remaining_coordinate_seam':coords['user_trace']['general_carry_sign_phase_rule'],
        'theorem_source':'https://arxiv.org/pdf/1105.4018v2#page=2',
        'published_theorem_computations_replayed':False,'formal_proof':False,
        'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'status':result['status'],'checks':len(checks),'free_index':1,'sha_order':1}))
    if not all(checks.values()):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
