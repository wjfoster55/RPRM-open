"""Exact conditional equality gate; it never assumes a denominator bound.

Inputs are newly executed E34 interval/height/period receipts. Their written
proofs remain dependencies. The new checks concern what these bounds can
and cannot conclude about exact equality, and the user's level-of-readout
proposal. Python standard library only.
"""
import argparse
from fractions import Fraction as F
from hashlib import sha256
import json
from pathlib import Path


def floor(x):
    x = F(x)
    return x.numerator // x.denominator


def ceil(x):
    return -floor(-F(x))


def squared_interval(pair):
    a, b = pair
    return (F(0) if a <= 0 <= b else min(a*a, b*b), max(a*a, b*b))


def whole_and_remainder(x, level=0):
    x = F(x)
    if x < 0 or not isinstance(level, int) or level < 0:
        raise ValueError('This contract admits nonnegative rationals and integer levels >=0')
    scaled = 10**level * x
    n = floor(scaled)
    return n, scaled - n


def retained_add(first, second):
    n, r = first
    m, s = second
    if not (isinstance(n, int) and isinstance(m, int) and
            n >= 0 and m >= 0 and 0 <= r < 1 and 0 <= s < 1):
        raise ValueError('Nonnegative normalized states required')
    carry = floor(r+s)
    return n+m+carry, r+s-carry


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError('Choose a fresh evidence path')
    record = json.loads((args.run/'RUN.json').read_text(encoding='utf-8'))
    if record['status'] != 'FRESH_REPLAY_AND_CONSISTENCY_CHECKS_COMPLETED':
        raise ValueError('A completed fresh computational run is required')
    files = {}
    receipts = {}
    for name in ('interval', 'generator', 'factor_frontier'):
        path = args.run/'evidence'/(name+'.json')
        data = path.read_bytes()
        receipts[name] = json.loads(data)
        files[name] = sha256(data).hexdigest()
        stage = next(x for x in record['stages'] if x['stage'] == name)
        assert files[name] == stage['receipt_sha256']
        assert receipts[name]['source_sha256'] == sha256(
            (args.run/'work'/(name+'.py')).read_bytes()).hexdigest()

    i, g, f = (receipts[n] for n in ('interval', 'generator', 'factor_frontier'))
    assert i['model'] == f['model'] == [0, 0, 0, -1156, 0]
    assert g['conclusion']['free_index'] == 1
    assert f['period']['real_components'] == 2
    assert f['local_product'] == f['torsion_order']**2 == 16
    assert f['sha_order'] == f['full_BSD_identity'] == 'NOT_ESTABLISHED'
    p, q, b = [tuple(map(F, g['gram'][k])) for k in
               ('diagonal_P', 'diagonal_Q', 'off_diagonal_B')]
    blo, bhi = squared_interval(b)
    reg = p[0]*q[0]-bhi, p[1]*q[1]-blo
    omega = tuple(map(F, f['period']['omega']))
    c2 = tuple(map(F, i['alpha_times_lambda2_interval']))
    assert reg[0] > 0 and omega[0] > 0 and c2[0] > 0
    ratio = c2[0]/(omega[1]*reg[1]), c2[1]/(omega[0]*reg[0])
    outer = tuple(map(F, f['bsd_quotient']))
    assert outer[0] <= ratio[0] < 1 < ratio[1] <= outer[1]

    # For a/q != 1, |a/q-1| >= 1/q. This conditional arithmetic theorem
    # says nothing about the actual real quotient's denominator by itself.
    epsilon = max(1-ratio[0], ratio[1]-1)
    maximum_admissible_denominator = ceil(1/epsilon)-1
    clean_bound = 10000
    assert clean_bound <= maximum_admissible_denominator
    assert epsilon < F(1, clean_bound)
    only_candidate = set()
    for denominator in range(1, clean_bound+1):
        low_n = ceil(ratio[0]*denominator)
        high_n = floor(ratio[1]*denominator)
        assert low_n == high_n == denominator
        only_candidate.add(F(low_n, denominator))
    assert only_candidate == {F(1)}
    first_above_q = ceil(1/(ratio[1]-1))
    first_below_q = ceil(1/(1-ratio[0]))
    side = 'above' if first_above_q <= first_below_q else 'below'
    first_q = min(first_above_q, first_below_q)
    closest_breaker = F(first_q+(1 if side == 'above' else -1), first_q)
    assert first_q == maximum_admissible_denominator+1
    assert ratio[0] <= closest_breaker <= ratio[1] and closest_breaker != 1
    fine_counterexample = F(1)+F(1, 10**12)
    assert ratio[0] < fine_counterexample < ratio[1] and fine_counterexample != 1

    grid = [F(j, 10) for j in range(21)]
    checks = 0
    for level in range(4):
        scale = 10**level
        for x in grid:
            n, r = whole_and_remainder(x, level)
            assert F(n+r, scale) == x
            for y in grid:
                state = retained_add((n, r), whole_and_remainder(y, level))
                assert state == whole_and_remainder(x+y, level)
                checks += 1
    six_tenths = whole_and_remainder(F(3, 5))
    joined = retained_add(six_tenths, six_tenths)
    assert six_tenths == (0, F(3, 5)) and joined == (1, F(1, 5))
    # Two pairs with identical coarse input readings have different sums.
    assert floor(F(3, 5)) == floor(F(1, 5)) == 0
    assert floor(F(3, 5)+F(3, 5)) == 1
    assert floor(F(1, 5)+F(1, 5)) == 0
    finite_depth_controls = []
    for depth in range(10):
        hidden = F(1, 10**(depth+1))
        assert all(whole_and_remainder(hidden, k)[0] == 0 for k in range(depth+1))
        assert whole_and_remainder(hidden, depth+1)[0] == 1
        finite_depth_controls.append({'last_zero_level': depth, 'nonzero_value': str(hidden),
                                      'first_visible_level': depth+1})
    negative = F(-3, 5)
    signed_options = {'value': str(negative), 'floor': floor(negative),
                      'truncate_toward_zero': -floor(abs(negative)),
                      'status': 'Distinct analyst-defined extensions; user rule unspecified'}
    assert signed_options['floor'] == -1 and signed_options['truncate_toward_zero'] == 0

    # A separate, genuinely additive quotient used by the admitted p=5
    # trace criterion. This enumerates possible residues, not the trace.
    admitted_trace_residues = [t for t in range(125) if t % 25 == 0]
    valuation_two_residues = [t for t in admitted_trace_residues if t != 0]
    assert admitted_trace_residues == [0, 25, 50, 75, 100]
    assert valuation_two_residues == [25, 50, 75, 100]
    for t in range(-250, 251):
        assert (t % 125 in valuation_two_residues) == (t % 25 == 0 and t % 125 != 0)
    assert 25 % 25 == 125 % 25 == 0
    assert 25 % 125 == 25 and 125 % 125 == 0

    result = {
        'status': 'CONDITIONAL_EQUALITY_GATE_AND_READOUT_CONTROLS_COMPLETED',
        'model': i['model'], 'input_receipt_sha256': files,
        'source_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
        'ratio_interval': list(map(str, ratio)), 'absolute_distance_from_one_bound': str(epsilon),
        'conditional_rational_gate': {
            'premise': 'The actual quotient is rational with reduced positive denominator <=10000',
            'consequence': 'The actual quotient equals1',
            'proof': '|a/q-1|>=1/q for a!=q; exact interval lies within distance1/10000',
            'checked_denominators': clean_bound, 'complete_candidate_fiber': ['1'],
            'largest_bound_admitted_by_current_interval': maximum_admissible_denominator,
            'premise_for_actual_quotient': 'NOT_ESTABLISHED'},
        'controls': {
            'rationality_without_denominator_bound': str(fine_counterexample),
            'first_denominator_admitting_another_value': first_q,
            'boundary_counterexample': str(closest_breaker),
            'scope': 'Possible real-number inputs, not claimed alternate elliptic-curve L-values'},
        'readout_levels': {
            'carrier': 'nonnegative rational values; level k>=0; exact equality retained',
            'decode': 'x=(whole+remainder)/10^k, 0<=remainder<1',
            'six_tenths_state': list(map(str, six_tenths)),
            'two_six_tenths_sum_state': list(map(str, joined)),
            'addition_grid_pairs_and_levels_checked': checks,
            'finite_depth_controls': finite_depth_controls,
            'negative_extension_options': signed_options,
            'all_levels_zero_lemma': 'For one fixed x, all-level zero implies x=0; written proof required',
            'all_levels_zero_for_BSD_discrepancy': 'NOT_ESTABLISHED'},
        'separate_five_adic_trace_readout': {
            'carrier': 'Z/125Z projected to Z/25Z; conditions justified in ODD_PRIME_ATTEMPT.md',
            'complete_fiber_over_coarse_zero': admitted_trace_residues,
            'residues_sufficient_for_the_5_primary_vanishing_theorem': valuation_two_residues,
            'zero_residue': 'This valuation-two criterion is inconclusive; nontrivial Sha is NOT inferred',
            'actual_trace_mod125': None,
            'status': 'ACTUAL_RESIDUE_NOT_COMPUTED'},
        'actual_quotient_rationality': 'NOT_ESTABLISHED',
        'actual_exact_analytic_identity': 'NOT_ESTABLISHED',
        'total_Sha': 'NOT_ESTABLISHED', 'full_BSD': 'NOT_ESTABLISHED',
        'evidence_grade': 'WRITTEN_CONDITIONAL_REDUCTION_PLUS_EXACT_FINITE_CHECKS',
        'formal_verification': 'NOT_RUN'}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({'status': result['status'],
                      'largest_conditional_denominator_bound': maximum_admissible_denominator,
                      'boundary_counterexample': str(closest_breaker),
                      'addition_checks': checks,
                      'actual_identity': 'NOT_ESTABLISHED'}, indent=2))


if __name__ == '__main__':
    main()
