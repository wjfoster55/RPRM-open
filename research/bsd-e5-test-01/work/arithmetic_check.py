#!/usr/bin/env python3
"""Independent, standard-library E5 arithmetic checks; never imports supplied code.

Run from any directory: python -I -B arithmetic_check.py --output arithmetic.json
This executable establishes finite facts. ARITHMETIC_PROOF.md supplies coverage
and explicitly cited Kummer/Selmer/Mordell-Weil dependencies.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from fractions import Fraction as F
from functools import reduce
from hashlib import sha256
from itertools import product
import json
from math import gcd, isqrt, lcm
from pathlib import Path
import platform

ROOTS = (0, 5, -5)
D = (-10, -5, -2, -1, 1, 2, 5, 10)
O = None
P = (F(-4), F(6))
K = (O, (F(0), F(0)), (F(5), F(0)), (F(-5), F(0)))
K_NAMES = ('O', 'T0', 'Tplus', 'Tminus')
BIT_CAP = 4096
MAX_BITS = 0


def check(condition, message):
    if not condition:
        raise AssertionError(message)


def admit(point):
    global MAX_BITS
    if point is None:
        return
    if not isinstance(point, tuple) or len(point) != 2 or not all(isinstance(q, F) for q in point):
        raise ValueError('Admission error: expected O or two exact Fraction coordinates')
    x, y = point
    if y*y != x*x*x-25*x:
        raise ValueError('Admission error: point is off E5')
    size = max(abs(q.numerator).bit_length() for q in point)
    size = max(size, *(q.denominator.bit_length() for q in point))
    MAX_BITS = max(MAX_BITS, size)
    check(size <= BIT_CAP, 'Declared point-coordinate bit cap exceeded')


def negate(point):
    admit(point)
    return None if point is None else (point[0], -point[1])


def plus(left, right):
    """Intersect a chord/tangent with the cubic, then negate its third point."""
    admit(left)
    admit(right)
    if left is None or right is None:
        return right if left is None else left
    x, y = left
    z, w = right
    if x == z and y == -w:
        return None
    slope = (3*x*x-25)/(2*y) if left == right else (w-y)/(z-x)
    intercept = y-slope*x
    third_x = slope*slope-x-z
    result = (third_x, -(slope*third_x+intercept))
    admit(result)
    return result


def times(integer, point):
    """Small repeated addition deliberately differs from source binary powering."""
    admit(point)
    if integer < 0:
        integer, point = -integer, negate(point)
    total = None
    for _ in range(integer):
        total = plus(total, point)
    return total


def sqrt_q(value):
    value = F(value)
    if value < 0:
        return None
    a, b = isqrt(value.numerator), isqrt(value.denominator)
    return F(a, b) if a*a == value.numerator and b*b == value.denominator else None


def squareclass(value):
    """Identify by exact square tests against all eight supported representatives.

    This uses no factor stripping, factorization, or source checker. If the
    support contract fails there is no match and an admission error is raised.
    """
    value = F(value)
    if not value:
        raise ValueError('Admission error: zero is not a multiplicative squareclass')
    matches = [d for d in D if sqrt_q(value/d) is not None]
    if len(matches) != 1:
        raise ValueError('Admission error: nonunique or unsupported squareclass')
    return matches[0]


def signature(point):
    admit(point)
    if point is None:
        return (1, 1, 1)
    x = point[0]
    answers = []
    for root in ROOTS:
        value = x-root
        if value == 0:
            value = reduce(lambda a, b: a*b, (root-other for other in ROOTS if other != root), 1)
        answers.append(squareclass(value))
    return tuple(answers)


def compose(a, b):
    return tuple(squareclass(x*y) for x, y in zip(a, b))


def homogeneous(point, sig):
    if point is None:
        return (1, 1, 1, 0)
    roots = [sqrt_q((point[0]-e)/d) for e, d in zip(ROOTS, sig)]
    check(all(r is not None for r in roots), 'Covering square root missing')
    scale = lcm(*(r.denominator for r in roots))
    values = tuple(int(r*scale) for r in roots)+(scale,)
    common = gcd(*values)
    return tuple(a//common for a in values)


def cover_equations(d, values, modulus=None):
    a, b, c, t = values
    errors = (d[0]*a*a-d[1]*b*b-5*t*t, d[2]*c*c-d[0]*a*a-5*t*t)
    return all(v == 0 for v in errors) if modulus is None else all(v % modulus == 0 for v in errors)


def lift_filter(d):
    """Enumerate the complete primitive binary residue tree, one lift at a time.

    At level k+1 every solution uniquely reduces to a solution at level k;
    its four new high bits are exhausted. An odd coordinate remains odd.
    No compressed weighted-square buckets or flat mod-8 scan is used.
    """
    frontier = [v for v in product((0, 1), repeat=4) if any(v) and cover_equations(d, v, 2)]
    result = {'2': {'count': len(frontier), 'first': frontier[0] if frontier else None}}
    for old_modulus in (2, 4):
        frontier = [tuple(x+old_modulus*bit for x, bit in zip(v, high))
                    for v in frontier for high in product((0, 1), repeat=4)
                    if cover_equations(d, tuple(x+old_modulus*bit for x, bit in zip(v, high)), 2*old_modulus)]
        check(len(frontier) == len(set(frontier)), 'Residue lifting duplicated a leaf')
        result[str(2*old_modulus)] = {'count': len(frontier), 'first': frontier[0] if frontier else None}
    return result


def halves(target):
    """Use half abscissas, then independently solve the curve for +/- ordinate.

    All eight root signs give four abscissas; both square-root ordinates are
    tried against the chord law. No supplied half ordinates/sign selector.
    """
    admit(target)
    if target is None:
        return K
    if signature(target) != (1, 1, 1):
        raise ValueError('Admission error: rational halving is not enabled')
    x, _ = target
    roots = [sqrt_q(x-e) for e in ROOTS]
    check(all(r is not None for r in roots), 'Half abscissa root missing')
    possible_x = set()
    for signs in product((-1, 1), repeat=3):
        a, b, c = (r*s for r, s in zip(roots, signs))
        possible_x.add(x+a*b+a*c+b*c)
    answers = set()
    for abscissa in possible_x:
        ordinate = sqrt_q(abscissa**3-25*abscissa)
        check(ordinate is not None, 'Half candidate has irrational ordinate')
        for yy in (ordinate, -ordinate):
            candidate = (abscissa, yy)
            if plus(candidate, candidate) == target:
                answers.add(candidate)
    check(len(answers) == 4, 'The halving fiber should have exactly four points')
    # Choose the smallest-height branch, an explicit finite deterministic policy.
    return tuple(sorted(answers, key=lambda q: (max(abs(z.numerator) for z in q)+max(z.denominator for z in q), q)))


def encode(point):
    return 'O' if point is None else {'x': str(point[0]), 'y': str(point[1])}


def decode(point, level, representatives):
    admit(point)
    if type(level) is not int or level < 1:
        raise ValueError('Admission error: level must be a positive integer')
    state, coefficient, first_torsion, trace = point, 0, None, []
    for digit in range(level):
        epsilon, torsion = representatives[signature(state)]
        if digit == 0:
            first_torsion = torsion
        coefficient += (2**digit)*epsilon
        even = plus(state, negate(plus(times(epsilon, P), K[torsion])))
        next_state = halves(even)[0]
        check(plus(plus(times(epsilon, P), K[torsion]), times(2, next_state)) == state, 'Step readback')
        trace.append({'bit': epsilon, 'torsion': K_NAMES[torsion], 'remainder': encode(next_state)})
        state = next_state
    check(plus(plus(times(coefficient, P), K[first_torsion]), times(2**level, state)) == point, 'Exact full readback')
    return {'m': coefficient, 'torsion': K_NAMES[first_torsion], 'remainder': encode(state), 'trace': trace}


def bits(integer):
    return [(integer >> bit) & 1 for bit in range(5)]


def frame(integer):
    """Involution: b3'=b3 XOR b0, b2'=b2 XOR b4; others fixed."""
    return integer ^ (((integer >> 0) & 1) << 3) ^ (((integer >> 4) & 1) << 2)


def indicator(integer):
    b = bits(integer)
    return (1-b[3])*(1-b[4])


def run():
    all_triples = {(a, b, squareclass(a*b)) for a, b in product(D, repeat=2)}
    candidates = {d for d in all_triples if d[0]*d[1] > 0 and d[2] > 0}
    check(len(all_triples) == 64 and len(candidates) == 32, 'Support/sign cardinality')
    filters = {d: lift_filter(d) for d in sorted(candidates)}
    survivors = {d for d in candidates if filters[d]['8']['count']}
    reps, index = [], {}
    for epsilon, torsion in product((0, 1), range(4)):
        point = plus(times(epsilon, P), K[torsion])
        sig = signature(point)
        quad = homogeneous(point, sig)
        check(cover_equations(sig, quad), 'Exact homogeneous witness failed')
        check(sig not in index, 'Rational signatures collide')
        index[sig] = (epsilon, torsion)
        reps.append({'epsilon': epsilon, 'torsion': K_NAMES[torsion], 'point': encode(point), 'signature': sig, 'homogeneous_witness': quad})
    H = set(index)
    check(H == survivors, 'Locally surviving set differs from witnessed set')
    coset_representatives = ((1, 1, 1), (2, 2, 1), (1, 2, 2), (2, 1, 2))
    blocks = [{compose(h, c) for h in H} for c in coset_representatives]
    check(set.union(*blocks) == candidates and sum(map(len, blocks)) == len(candidates), 'Coset partition')
    exclusions = []
    for sig, modulus in (((2, 2, 1), 4), ((1, 2, 2), 8), ((2, 1, 2), 4)):
        check(filters[sig][str(modulus)]['count'] == 0, 'Coset representative is not excluded')
        exclusions.append({'signature': sig, 'modulus': modulus, 'primitive_count': 0})
    point_reps = [plus(times(e, P), K[t]) for e, t in product((0, 1), range(4))]
    for a, b in product(point_reps, repeat=2):
        check(signature(plus(a, b)) == compose(signature(a), signature(b)), 'Finite Kummer homomorphism check')

    # A separate rational abscissa search is a spot check, not new curve work.
    searched = set()
    abscissas = {F(numerator, denominator*denominator) for denominator in range(1, 5) for numerator in range(-80, 201)}
    for x in sorted(abscissas):
        y = sqrt_q(x*x*x-25*x)
        if y is not None:
            searched.update(((x, y), (x, -y)))
    for point in searched:
        check(signature(point) in H, 'Abscissa search found an unaccounted class')
    search_spots = []
    for point in sorted(searched)[:6]:
        search_spots.append({'point': encode(point), 'level4': decode(point, 4, index)})

    tower = []
    selection = (-3, -1, 0, 1, 2, 3, 5)
    for m, t, level in product(selection, range(4), range(1, 5)):
        point = plus(times(m, P), K[t])
        got = decode(point, level, index)
        check((got['m'], got['torsion']) == (m % 2**level, K_NAMES[t]), 'Tower coordinates')
        if level > 1:
            previous = decode(point, level-1, index)
            check((got['m'] % 2**(level-1), got['torsion']) == (previous['m'], previous['torsion']), 'Tower transition')
        tower.append({'source_m': m, 'source_torsion': K_NAMES[t], 'level': level, 'point': encode(point), **got})

    q = times(2, P)
    check(q == (F(1681, 144), F(-62279, 1728)), 'Double arithmetic')
    half_q = halves(q)
    check(set(half_q) == {plus(P, t) for t in K}, 'Halves differ from torsion orbit')
    check(all(signature(h) != (1, 1, 1) for h in half_q), 'Unexpected rational quarter of Q')
    check(all(signature(t) != (1, 1, 1) for t in K[1:]), 'Unexpected rational order-four torsion')
    inverse = {'P_level1': decode(P, 1, index), 'minus_P_level1': decode(negate(P), 1, index), 'P_level2': decode(P, 2, index), 'minus_P_level2': decode(negate(P), 2, index)}
    check((inverse['P_level1']['m'], inverse['P_level1']['torsion']) == (inverse['minus_P_level1']['m'], inverse['minus_P_level1']['torsion']) == (1, 'O'), 'Inverse coarse identity')
    check((inverse['P_level2']['m'], inverse['P_level2']['torsion']) == (1, 'O') and (inverse['minus_P_level2']['m'], inverse['minus_P_level2']['torsion']) == (3, 'O'), 'Inverse finer distinction')

    generators = (signature(P), signature(K[1]), signature(K[2]), (2, 2, 1), (1, 2, 2))
    cube = {}
    for label in range(32):
        sig = (1, 1, 1)
        for enabled, generator in zip(bits(label), generators):
            if enabled:
                sig = compose(sig, generator)
        cube[label] = sig
    check(len(set(cube.values())) == 32 and set(cube.values()) == candidates, 'Cube bijection')
    for a, b in product(range(32), repeat=2):
        check(cube[a ^ b] == compose(cube[a], cube[b]), 'Cube multiplication transport')
        check(frame(a ^ b) == frame(a) ^ frame(b), 'Frame linearity')
        check(cube[frame(a ^ b)] == compose(cube[frame(a)], cube[frame(b)]), 'New basis group transport')
    for label in range(32):
        check(indicator(label) == int(cube[label] in survivors), 'Indicator was not reconstructed from descent')
        check(frame(frame(label)) == label, 'Frame inverse')
        check(indicator(frame(frame(label))) == int(cube[label] in survivors), 'Coherent readout transport')
    mismatches = [{'source_bits': bits(label), 'new_bits': bits(frame(label)), 'signature': cube[label], 'transported_readout': indicator(frame(frame(label))), 'untransported_readout': indicator(frame(label))} for label in range(32) if indicator(frame(label)) != indicator(label)]
    check(mismatches, 'Wrong frame control did not change a real readout')

    rejections = []
    operations = {'group': lambda: plus((F(0), F(1)), P), 'signature': lambda: signature((F(0), F(1)))}
    for name, operation in operations.items():
        try:
            operation()
        except ValueError as error:
            rejections.append({'path': name, 'error': str(error)})
        else:
            raise AssertionError('Off-curve input was accepted')
    lost = {'O_level1': decode(O, 1, index), 'Q_level1': decode(q, 1, index), 'O_level2': decode(O, 2, index), 'Q_level2': decode(q, 2, index), 'Q': encode(q), 'all_Q_halves': [{'point': encode(h), 'signature': signature(h)} for h in half_q]}
    check((lost['O_level1']['m'], lost['O_level1']['torsion']) == (lost['Q_level1']['m'], lost['Q_level1']['torsion']) == (0, 'O'), 'Lost remainder coarse collision')
    check((lost['O_level2']['m'], lost['O_level2']['torsion']) == (0, 'O') and (lost['Q_level2']['m'], lost['Q_level2']['torsion']) == (2, 'O'), 'Lost remainder finer witness')
    sources = [
        {'id': 'S_KUMMER', 'url': 'https://www.jmilne.org/math/Books/ectext6.pdf', 'locator': 'IV section 3, Remark 3.7, printed p.113 / PDF page 121; preceding split-2-torsion cohomology identification', 'status': 'THEOREM_CITED', 'checked_hypotheses': ['Q has characteristic zero', 'roots 0,5,-5 are distinct rational integers', 'discriminant 1000000 is nonzero', 'E[2] is rational']},
        {'id': 'S_SELMER', 'url': 'https://arxiv.org/pdf/math/0611694', 'locator': 'section 1.1, printed pp.2-3 / PDF pages 2-3, Kummer and Selmer exact sequences and all-place local-image definition', 'status': 'THEOREM_CITED', 'checked_hypotheses': ['Q is a number field', 'E5 is an elliptic curve', 'n=2^k is an integer greater than one', 'all places are retained in Selmer definition']},
        {'id': 'S_MW', 'url': 'https://www.jmilne.org/math/Books/ectext6.pdf', 'locator': 'Chapter IV opening, finite-basis theorem, printed p.101 / PDF page 109', 'status': 'THEOREM_CITED', 'checked_hypotheses': ['E5 is an elliptic curve over number field Q']},
        {'id': 'S_HALF', 'url': 'https://arxiv.org/html/1702.02255v2', 'locator': 'section 2, Theorem 2.1 and equations (3)-(6), plus Example 2.2 for a two-torsion target', 'status': 'THEOREM_CITED', 'checked_hypotheses': ['characteristic of Q is not 2', 'all three roots belong to Q and are distinct', 'non-O target is admitted on E5', 'all three differences are rational squares on enabled path', 'O handled separately as fiber E[2]']},
    ]
    controls = [
        {'id': 'K01_OFF_CURVE', 'status': 'CONFIRMED', 'outcome': 'ADMISSION_REJECTED', 'input': {'x': '0', 'y': '1'}, 'residual_y2_minus_rhs': '1', 'observations': rejections},
        {'id': 'K05_LOST_REMAINDER', 'status': 'CONFIRMED', 'outcome': 'NON_IDENTIFIABLE_FROM_COARSE_LABEL', 'fiber': 'MANY: the two finer quotient lifts (0,O) and (2,O); source-specific choice OPEN after backing is removed', 'observations': lost},
        {'id': 'K06_FRAME_TRANSPORT', 'status': 'CONFIRMED', 'outcome': 'COHERENT_TRANSPORT_CONFIRMED_AND_STALE_READOUT_REFUTED', 'frame': 'b3 ^= b0; b2 ^= b4; self-inverse', 'positive_cases': 32, 'negative_mismatch_count': len(mismatches), 'witness': mismatches[0]},
    ]
    return {
        'status': 'PASS', 'evidence_kind': 'INDEPENDENT_FINITE_TESTS_PLUS_WRITTEN_PROOF_WITH_CITED_THEOREMS',
        'utc': datetime.now(timezone.utc).isoformat(), 'python': platform.python_version(),
        'source_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
        'source_contract': {'field': 'Q', 'a_invariants': [0, 0, 0, -25, 0], 'no_supplied_imports_or_receipt_reads': True},
        'tasks': [{'id': 'A01', 'status': 'CONFIRMED', 'conclusion': 'Sel_2=delta(E(Q)) has eight classes; rank=1; Sha[2^n]=0 for all n>=1', 'evidence': ['independent residue lifting', 'exact rational witnesses', 'ARITHMETIC_PROOF.md'], 'sources': ['S_KUMMER', 'S_SELMER', 'S_MW']}, {'id': 'A02', 'status': 'CONFIRMED', 'conclusion': 'compatible 2-power quotient coordinates and exact finite readback; no odd-prime saturation conclusion', 'evidence': ['112 finite tower cases at levels1..4', 'six rational-x-search spot cases', 'ARITHMETIC_PROOF.md'], 'sources': ['S_HALF', 'S_KUMMER', 'S_MW', 'S_SELMER']}, {'id': 'C01', 'status': 'CONFIRMED', 'conclusion': 'five-bit bijection transports XOR to squareclass multiplication; coherent frame/readout transport passes', 'evidence': ['all 1024 pairs', '32 transported readouts', 'ARITHMETIC_PROOF.md'], 'sources': []}],
        'sources': sources, 'controls': controls,
        'candidate_counts': {'supported': len(all_triples), 'real': len(candidates), 'mod2': sum(bool(f['2']['count']) for f in filters.values()), 'mod4': sum(bool(f['4']['count']) for f in filters.values()), 'mod8': len(survivors)},
        'modular_filter_route': 'Complete binary lifting tree from primitive mod2 leaves to mod4 then mod8; parity preserved under lifts',
        'modular_filters': [{'signature': d, **filters[d]} for d in sorted(candidates)],
        'representatives': reps, 'cosets': [{'representative': c, 'members': sorted(block)} for c, block in zip(coset_representatives, blocks)], 'exclusions': exclusions,
        'rational_x_search': {'bounds': 'x=a/b^2, -80<=a<=200, 1<=b<=4; both rational y signs', 'unique_x_tested': len(abscissas), 'affine_points_found': len(searched), 'points': [encode(q) for q in sorted(searched)], 'decoded_spots': search_spots},
        'tower_tests': {'count': len(tower), 'm_selection': selection, 'levels': [1, 2, 3, 4], 'records': tower, 'inverse_distinction': inverse, 'declared_point_coordinate_bit_cap': BIT_CAP, 'observed_max_point_coordinate_bits': MAX_BITS},
        'cube': {'bit_order': ['P', 'T0', 'Tplus', 'A', 'B'], 'generators': generators, 'group_pair_count': 1024, 'mapping': [{'bits': bits(label), 'signature': cube[label], 'arithmetic_admissible': cube[label] in survivors} for label in range(32)]},
        'not_established': ['P generates the full free integral lattice', 'odd-primary Sha or total Sha order', 'a general BSD theorem', 'analytic claims', 'general RPRM performance advantage'],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = run()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({'status': result['status'], 'counts': result['candidate_counts'], 'tower_cases': result['tower_tests']['count'], 'max_coordinate_bits': MAX_BITS, 'cube_pairs': 1024, 'task_ids': [r['id'] for r in result['tasks']], 'control_ids': [r['id'] for r in result['controls']], 'output': str(args.output)}, indent=2))


if __name__ == '__main__':
    main()
