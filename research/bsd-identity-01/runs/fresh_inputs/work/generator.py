"""Complete bounded generator certificate for E34 and P=(-2,48), Q=(-16,120).

The rational logarithm helpers are adapted from this repository's
research/bsd-e5-completion/work/bsd_factors.py (down, up,
log_unit_interval, log_integer_interval). They are copied here so this
certificate never imports old code or reads old results. All E34 heights,
the cutoff, the point search, and membership witnesses are fresh.
Mathematical coverage and dependencies: ../GENERATOR_PROOF.md.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
import json
from math import gcd, isqrt
from pathlib import Path
import platform


N = 34
C0 = 4*N**4
C1 = (1+N*N)**2
BITS = 100
DEN = 1 << BITS
STEPS = 8
HEIGHT_CAP = 5000
RAW_PAIR_CAP = 1000000
P = (F(-2), F(48))
Q = (F(-16), F(120))
K = (None, (F(0), F(0)), (F(N), F(0)), (F(-N), F(0)))
K_NAMES = ('O', 'T0', 'Tplus', 'Tminus')


def require(statement, message):
    if not statement:
        raise AssertionError(message)


def down(x, den=DEN):
    x = F(x)
    return F(x.numerator*den//x.denominator, den)


def up(x, den=DEN):
    return -down(-F(x), den)


def serial(interval):
    return [str(v) for v in interval]


def readable(interval, places=9):
    return serial((down(interval[0], 10**places), up(interval[1], 10**places)))


def log_unit_interval(r, terms=96):
    """Positive atanh series and a geometric all-term remainder bound."""
    r = F(r)
    require(1 <= r <= 2, 'Logarithm mantissa outside [1,2]')
    z = (r-1)/(r+1)
    z2, power, total = z*z, z, F(0)
    for j in range(terms):
        total += 2*power/(2*j+1)
        power *= z2
    tail = 2*power/((2*terms+1)*(1-z2))
    return down(total), up(total+tail)


def log_integer_interval(integer):
    require(type(integer) is int and integer >= 1, 'Positive integer logarithm required')
    k = integer.bit_length()-1
    if k <= BITS:
        rlo = rhi = F(integer, 1 << k)
    else:
        shift = k-BITS
        top = integer >> shift
        rlo, rhi = F(top, DEN), F(top+1, DEN)
        require(rlo*(1 << k) <= integer < rhi*(1 << k), 'Log mantissa enclosure failed')
    ln2 = log_unit_interval(F(2))
    lo, hi = log_unit_interval(rlo)[0], log_unit_interval(rhi)[1]
    return down(k*ln2[0]+lo), up(k*ln2[1]+hi)


def admit(point):
    if point is None:
        return
    if not (isinstance(point, tuple) and len(point) == 2
            and all(isinstance(v, F) for v in point)):
        raise ValueError('Admission error: expected a pair of Fractions or O')
    x, y = point
    if y*y != x*x*x-N*N*x:
        raise ValueError('Admission error: off E34')


def add(left, right):
    admit(left)
    admit(right)
    if left is None or right is None:
        return right if left is None else left
    x, y = left
    z, w = right
    if x == z and y == -w:
        return None
    slope = (3*x*x-N*N)/(2*y) if left == right else (w-y)/(z-x)
    xx = slope*slope-x-z
    result = (xx, slope*(x-xx)-y)
    admit(result)
    return result


def negate(point):
    admit(point)
    return None if point is None else (point[0], -point[1])


def encode(point):
    return 'O' if point is None else {'x': str(point[0]), 'y': str(point[1])}


def duplicate_x(a, b):
    require(gcd(a, b) == 1, 'Primitive x coordinates required')
    height = max(abs(a), abs(b))
    num = (a*a+N*N*b*b)**2
    den = 4*a*b*(a*a-N*N*b*b)
    common = gcd(num, den)
    require(common > 0 and C0 % common == 0, 'Universal gcd bound failed on this input')
    require(height**4 <= max(abs(num), abs(den)) <= C1*height**4,
            'Universal raw-height bound failed on this input')
    aa, bb = num//common, den//common
    if bb < 0:
        aa, bb = -aa, -bb
    require(bb >= 0 and gcd(aa, bb) == 1, 'Output x is not normalized')
    return aa, bb, common


def canonical_height(point):
    admit(point)
    a, b = (1, 0) if point is None else (point[0].numerator, point[0].denominator)
    rows = []
    for j in range(STEPS):
        a, b, common = duplicate_x(a, b)
        rows.append({'doubling': j+1, 'gcd_removed': common,
                     'numerator_bits': abs(a).bit_length(), 'denominator_bits': b.bit_length()})
    height = max(abs(a), b)
    log_h = log_integer_interval(height)
    log_c0, log_c1 = log_integer_interval(C0), log_integer_interval(C1)
    scale = 4**STEPS
    enclosure = (down(log_h[0]/scale-log_c0[1]/(3*scale)),
                 up(log_h[1]/scale+log_c1[1]/(3*scale)))
    return enclosure, {'point': encode(point), 'doublings': STEPS,
                       'duplication_ledger': rows,
                       'last_x_numerator_hex': hex(a), 'last_x_denominator_hex': hex(b),
                       'last_height_hex': hex(height), 'log_last_height': serial(log_h),
                       'enclosure': serial(enclosure), 'readable': readable(enclosure)}


def find_height_cutoff(log_upper):
    """Search only within the explicitly authorized integer-height budget."""
    if log_integer_interval(HEIGHT_CAP+1)[0] <= log_upper:
        return None
    left, right = 1, HEIGHT_CAP+1
    while left < right:
        middle = (left+right)//2
        if log_integer_interval(middle)[0] > log_upper:
            right = middle
        else:
            left = middle+1
    return left-1


def enumerate_points(bound):
    raw_count = (2*bound+1)*isqrt(bound)
    require(raw_count <= RAW_PAIR_CAP, 'Raw enumeration cap exceeded')
    counts, found, digest = [], [], sha256()
    for c in range(1, isqrt(bound)+1):
        candidates, squares = 0, 0
        for a in range(-bound, bound+1):
            if gcd(a, c) != 1:
                continue
            candidates += 1
            radicand = a*(a*a-N*N*c**4)
            root = isqrt(radicand) if radicand >= 0 else None
            square = root is not None and root*root == radicand
            digest.update((f'{a},{c},{radicand},{root},{int(square)}\n').encode('ascii'))
            if not square:
                continue
            squares += 1
            ordinates = (F(root, c**3),) if root == 0 else (F(root, c**3), F(-root, c**3))
            for y in ordinates:
                point = (F(a, c*c), y)
                admit(point)
                require(max(abs(point[0].numerator), point[0].denominator) <= bound,
                        'Enumerated point outside height bound')
                found.append(point)
        counts.append({'c': c, 'denominator': c*c, 'reduced_abscissas': candidates,
                       'square_radicands': squares})
    require(len(found) == len(set(found)), 'Search duplicated a rational point')
    return found, {'bound': bound, 'c_max': isqrt(bound), 'raw_pair_count': raw_count,
                    'reduced_abscissa_count': sum(row['reduced_abscissas'] for row in counts),
                    'affine_point_count': len(found), 'by_denominator': counts,
                    'all_candidate_digest_sha256': digest.hexdigest(),
                    'digest_row_contract': 'a,c,radicand,floor_sqrt_or_None,is_square followed by newline; increasing c then a'}


def run():
    require(C0 == 5345344 and C1 == 1338649, 'Height constants changed')
    sum_point = add(P, Q)
    require(sum_point == (F(2178, 49), F(65472, 343)), 'P+Q arithmetic mismatch')
    hp, p_data = canonical_height(P)
    hq, q_data = canonical_height(Q)
    hs, sum_data = canonical_height(sum_point)
    pairing = (down((hs[0]-hp[1]-hq[1])/2), up((hs[1]-hp[0]-hq[0])/2))
    require(hp[0] > 0 and hq[0] > 0 and pairing[0] > 0, 'Positive Gram conditions failed')
    determinant = (down(hp[0]*hq[0]-max(abs(pairing[0]), abs(pairing[1]))**2),
                   up(hp[1]*hq[1]-min(abs(pairing[0]), abs(pairing[1]))**2))
    require(determinant[0] > 0, 'Gram positive definiteness not certified')
    box_q_upper = up((hp[1]+hq[1]+2*max(abs(pairing[0]), abs(pairing[1])))/4)
    log_c0, log_c1 = log_integer_interval(C0), log_integer_interval(C1)
    naive_log_upper = up(box_q_upper+log_c0[1]/3)
    cutoff = find_height_cutoff(naive_log_upper)
    if cutoff is None:
        return {'status': 'OPEN', 'reason': 'Certified cutoff exceeds height budget',
                'height_cap': HEIGHT_CAP, 'naive_log_upper': str(naive_log_upper)}
    require(cutoff == 987, 'Fresh cutoff differs from documented value')
    log_next = log_integer_interval(cutoff+1)
    require(naive_log_upper < log_next[0], 'Height cutoff is not strict')
    points, search_data = enumerate_points(cutoff)

    # Membership requires a witness only. This small search is not claimed
    # to enumerate all possible coefficients or to prove nonmembership.
    p_multiples, q_multiples = {-1: negate(P), 0: None, 1: P}, {-1: negate(Q), 0: None, 1: Q}
    membership = {}
    for i, j, torsion_index in product((-1, 0, 1), (-1, 0, 1), range(4)):
        candidate = add(add(p_multiples[i], q_multiples[j]), K[torsion_index])
        require(candidate not in membership, 'Known independent basis classes collided')
        membership[candidate] = (i, j, torsion_index)
    all_points = [None]+points
    missing = [r for r in all_points if r not in membership]
    if missing:
        return {'status': 'OPEN', 'reason': 'Some small points lack membership witnesses',
                'missing_points': [encode(r) for r in missing], 'search': search_data}
    witnesses = []
    for point in all_points:
        i, j, torsion_index = membership[point]
        reconstructed = add(add(p_multiples[i], q_multiples[j]), K[torsion_index])
        require(reconstructed == point, 'Membership witness readback failed')
        a, b = (1, 0) if point is None else (point[0].numerator, point[0].denominator)
        aa, bb, common = duplicate_x(a, b)
        doubled = add(point, point)
        require((bb == 0 and doubled is None) or
                (bb != 0 and doubled is not None and doubled[0] == F(aa, bb)),
                'Projective duplication differs from independent chord law')
        witnesses.append({'point': encode(point), 'P_coefficient': i, 'Q_coefficient': j,
                          'torsion': K_NAMES[torsion_index], 'duplication_gcd': common})
    require(len(points) == 25 and search_data['reduced_abscissa_count'] == 38205,
            'Completed search count differs from documented enumeration')
    _, _, sharp_gcd = duplicate_x(N, 1)
    wrong_gcd_bound = 4*17**4
    require(sharp_gcd == C0 and sharp_gcd > wrong_gcd_bound, 'Wrong 2-adic cancellation control failed')
    try:
        add((F(-16), F(121)), P)
    except ValueError as error:
        rejection = str(error)
    else:
        raise AssertionError('Off-curve hostile point was accepted')

    return {'status': 'PASS', 'utc': datetime.now(timezone.utc).isoformat(),
            'python': platform.python_version(),
            'source_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
            'evidence_grade': 'EXACT_FINITE_CERTIFICATE_PLUS_WRITTEN_HEIGHT_LATTICE_PROOF',
            'conclusion': {'P': encode(P), 'Q': encode(Q), 'free_index': 1,
                           'group': 'E34(Q)=Z*P direct_sum Z*Q direct_sum (Z/2Z)^2',
                           'odd_saturation': 'COMPLETE_BY_ALL_INDEX_HEIGHT_ARGUMENT'},
            'accepted_arithmetic_dependencies': {'source': '../ARITHMETIC_PROOF.md',
                'rank': 2, 'torsion': 'K=E[2](Q)', 'P_Q_independent': True,
                'saved_arithmetic_json_read': False},
            'height_normalization': 'q(R)=lim 4^-n log H_x(2^n R), full x-height',
            'rounding': {'dyadic_bits': BITS, 'log_series_terms': 96},
            'constants': {'C0_gcd_bound': C0, 'C1_raw_height_bound': C1,
                           'log_C0': serial(log_c0), 'log_C1': serial(log_c1)},
            'heights': {'P': p_data, 'Q': q_data, 'P_plus_Q': sum_data},
            'gram': {'diagonal_P': serial(hp), 'diagonal_Q': serial(hq),
                     'off_diagonal_B': serial(pairing), 'B_readable': readable(pairing),
                     'determinant_positive_lower_bound': str(determinant[0]),
                     'regulator_interval': serial(determinant),
                     'regulator_readable': readable(determinant),
                     'regulator_normalization': 'Gram diagonal q(R)=lim 4^-n log H_x(2^n R); B=(q(P+Q)-q(P)-q(Q))/2',
                     'regulator_basis_status': 'FULL_INTEGRAL_BASIS_PROVED_IN_THIS_CERTIFICATE'},
            'cutoff_certificate': {'centered_basis_coefficient_bounds': ['-1/2', '1/2'],
                'box_q_upper': str(box_q_upper), 'naive_log_upper': str(naive_log_upper),
                'naive_log_upper_readable': str(up(naive_log_upper, 10**9)),
                'log_next_integer_interval': serial(log_next),
                'strict_log_margin': str(log_next[0]-naive_log_upper),
                'height_at_most': cutoff, 'height_cap': HEIGHT_CAP,
                'raw_pair_cap': RAW_PAIR_CAP},
            'search': search_data, 'membership_coefficient_search': [-1, 0, 1],
            'all_small_points_with_membership': witnesses,
            'controls': {'wrong_two_adic_gcd_bound': {'point': encode(K[2]),
                    'actual_gcd': sharp_gcd, 'wrong_bound': wrong_gcd_bound,
                    'result': 'REJECTED'},
                'off_curve': {'point': {'x': '-16', 'y': '121'}, 'result': rejection},
                'duplication_vs_chord_law_points': len(all_points),
                'finite_membership_requires_no_nonmembership_inference': True},
            'sources': [{'id': 'S_HEIGHT', 'url': 'https://www.jmilne.org/math/Books/ectext6.pdf',
                'locator': 'IV section4, printed pp120-124 / PDF pp128-132: Lemma4.6, Theorem4.7, Proposition4.9, Lemma4.11',
                'status': 'THEOREM_CITED', 'hypotheses': 'nonsingular rational Weierstrass curve'}],
            'helper_attribution': 'rational log helpers adapted from research/bsd-e5-completion/work/bsd_factors.py',
            'not_established': ['analytic order of vanishing', 'BSD leading-coefficient identity',
                                'odd-primary Sha or total Sha order']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = run()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    if result['status'] == 'PASS':
        print(json.dumps({'status': result['status'], 'free_index': 1,
            'height_bound': result['cutoff_certificate']['height_at_most'],
            'raw_pairs': result['search']['raw_pair_count'],
            'reduced_abscissas': result['search']['reduced_abscissa_count'],
            'affine_points': result['search']['affine_point_count'],
            'all_points_have_exact_membership_witnesses': True,
            'P_height': result['heights']['P']['readable'],
            'Q_height': result['heights']['Q']['readable'],
            'B_pairing': result['gram']['B_readable'],
            'regulator_interval': result['gram']['regulator_readable'],
            'output': str(args.output)}, indent=2))
    else:
        print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
