"""Fresh exact split 2-descent certificate for y^2 = x^3 - 1156*x.

Standard library only. No saved receipts, curve databases, or rank backends
are read. ARITHMETIC_PROOF.md supplies the written coverage arguments and
the explicitly cited standard theorems; this script checks their finite data.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
import json
from math import gcd, isqrt, lcm
from pathlib import Path
import platform


N = 34
ROOTS = (0, N, -N)
D = (-34, -17, -2, -1, 1, 2, 17, 34)
O = None
K = (O, (F(0), F(0)), (F(N), F(0)), (F(-N), F(0)))
K_NAMES = ('O', 'T0', 'Tplus', 'Tminus')
P = (F(-2), F(48))
IDENTITY = (1, 1, 1)


def require(statement, message):
    if not statement:
        raise AssertionError(message)


def admit(point):
    if point is None:
        return
    if not (isinstance(point, tuple) and len(point) == 2
            and all(isinstance(a, F) for a in point)):
        raise ValueError('Admission error: point must be O or a pair of Fractions')
    x, y = point
    if y*y != x*x*x - N*N*x:
        raise ValueError('Admission error: point is off E34')


def add(left, right):
    admit(left)
    admit(right)
    if left is None or right is None:
        return right if left is None else left
    x, y = left
    z, w = right
    if x == z and y == -w:
        return O
    slope = (3*x*x-N*N)/(2*y) if left == right else (w-y)/(z-x)
    xx = slope*slope-x-z
    answer = (xx, slope*(x-xx)-y)
    admit(answer)
    return answer


def sqrt_q(value):
    value = F(value)
    if value < 0:
        return None
    a, b = isqrt(value.numerator), isqrt(value.denominator)
    return F(a, b) if a*a == value.numerator and b*b == value.denominator else None


def squareclass(value):
    value = F(value)
    if not value:
        raise ValueError('Admission error: zero has no multiplicative squareclass')
    matches = [d for d in D if sqrt_q(value/d) is not None]
    if len(matches) != 1:
        raise ValueError('Admission error: unsupported or nonunique squareclass')
    return matches[0]


def multiply_classes(left, right):
    return tuple(squareclass(a*b) for a, b in zip(left, right))


def signature(point):
    admit(point)
    if point is None:
        return IDENTITY
    result = []
    for e in ROOTS:
        q = point[0]-e
        if not q:
            other = [r for r in ROOTS if r != e]
            q = (e-other[0])*(e-other[1])
        result.append(squareclass(q))
    return tuple(result)


def covering_residuals(d, v):
    u1, u2, u3, t = v
    return (d[0]*u1*u1-d[1]*u2*u2-N*t*t,
            d[2]*u3*u3-d[0]*u1*u1-N*t*t)


def homogeneous_witness(point, d):
    if point is None:
        return (1, 1, 1, 0)
    roots = [sqrt_q((point[0]-e)/a) for e, a in zip(ROOTS, d)]
    require(all(r is not None for r in roots), 'Missing rational covering coordinate')
    scale = lcm(*(r.denominator for r in roots))
    v = tuple(int(r*scale) for r in roots)+(scale,)
    common = gcd(*v)
    return tuple(a//common for a in v)


def residue_filter(d, prime, modulus):
    """Flat exhaustive primitive projective-coordinate residue enumeration.

    Each tuple in {0,...,modulus-1}^4 is visited exactly once. Primitivity
    means some coordinate is a prime-adic unit; no projective quotient or
    lifting assumption can accidentally drop a candidate.
    """
    count, first = 0, None
    for v in product(range(modulus), repeat=4):
        if not any(a % prime for a in v):
            continue
        if all(r % modulus == 0 for r in covering_residuals(d, v)):
            count += 1
            if first is None:
                first = v
    return {'prime': prime, 'modulus': modulus,
            'primitive_solution_count': count, 'first_witness': first,
            'ambient_tuple_count': modulus**4}


def encode(point):
    return 'O' if point is None else {'x': str(point[0]), 'y': str(point[1])}


def finite_curve(prime):
    points = [(x, y) for x, y in product(range(prime), repeat=2)
              if (y*y-x*x*x+N*N*x) % prime == 0]
    discriminant = 64*N**6
    require(discriminant % prime != 0, 'Torsion reduction prime is not good')
    return {'prime': prime, 'discriminant_residue': discriminant % prime,
            'affine_points': points, 'projective_point_count': len(points)+1}


def run():
    admit(P)
    torsion_sigs = [signature(t) for t in K]
    require(len(set(torsion_sigs)) == 4, 'Two-torsion Kummer signatures collide')
    require(all(add(t, t) is None for t in K), 'Wrong two-torsion list')
    first_orbit = {signature(add(p, t)) for p, t in product((O, P), K)}
    require(len(first_orbit) == 8, 'P does not provide a non-torsion quotient direction')

    # Complete only within this disclosed integer-x search, not all rational points.
    searched = []
    for x in range(-34, 10001):
        y = sqrt_q(x*x*x-N*N*x)
        if y is not None:
            searched.append((F(x), y))
    q_candidates = [r for r in searched if signature(r) not in first_orbit]
    require(q_candidates, 'Search did not find a second quotient direction')
    Q = q_candidates[0]
    require(Q == (F(-16), F(120)), 'Unexpected deterministic search result')

    records, point_reps = [], []
    for epsilon, eta, torsion_index in product((0, 1), (0, 1), range(4)):
        point = add(add(P if epsilon else O, Q if eta else O), K[torsion_index])
        d = signature(point)
        witness = homogeneous_witness(point, d)
        require(covering_residuals(d, witness) == (0, 0), 'Covering witness is false')
        require(gcd(*witness) == 1, 'Covering witness was not primitive')
        records.append({'P_coefficient': epsilon, 'Q_coefficient': eta,
                        'torsion': K_NAMES[torsion_index], 'point': encode(point),
                        'signature': d, 'homogeneous_witness': witness})
        point_reps.append(point)
    H = {r['signature'] for r in records}
    require(len(H) == 16, 'Sixteen rational witnesses do not have distinct signatures')
    for a, b in product(point_reps, repeat=2):
        require(signature(add(a, b)) == multiply_classes(signature(a), signature(b)),
                'Exact finite Kummer homomorphism check failed')
    require(all(multiply_classes(a, b) in H for a, b in product(H, repeat=2)),
            'Witnessed signature set is not a subgroup')

    supported = {(a, b, squareclass(a*b)) for a, b in product(D, repeat=2)}
    V = {d for d in supported if d[0]*d[1] > 0 and d[2] > 0}
    require(len(supported) == 64 and len(V) == 32, 'Support and real class counts')
    filters = {d: {str(m): residue_filter(d, 2, m) for m in (2, 4, 8)}
               for d in sorted(V)}
    survivors = {d for d in V if filters[d]['8']['primitive_solution_count']}
    require(survivors == H, 'Local upper bound differs from global witnesses')

    # The mod-17 scan is diagnostic, not a claim that residues prove Q17 solubility.
    local17 = {d: residue_filter(d, 17, 17) for d in sorted(V)}
    require((6*6-2) % 17 == 0 and gcd(12, 17) == 1,
            'Hensel root or derivative condition failed')
    require(all(r['primitive_solution_count'] for r in local17.values()),
            'Unexpected mod17 diagnostic exclusion')
    require(all(local17[d]['primitive_solution_count'] for d in H),
            'Rational witness contradicts the mod-17 necessary test')
    A = (1, 2, 2)
    AH = {multiply_classes(A, h) for h in H}
    require(H.isdisjoint(AH) and H | AH == V, 'Two-coset coverage failed')
    require(filters[A]['8']['primitive_solution_count'] == 0,
            'Excluded coset representative survives mod8')

    reductions = [finite_curve(p) for p in (3, 5)]
    require([r['projective_point_count'] for r in reductions] == [4, 8],
            'Good-reduction torsion point counts changed')
    require(gcd(*(r['projective_point_count'] for r in reductions)) == 4,
            'Torsion size bound is not four')
    for t in K[1:]:
        require(signature(t) != IDENTITY, 'A nonzero two-torsion point is a double')

    rejections = []
    for point in ((F(0), F(1)), (F(-16), F(121))):
        try:
            signature(point)
        except ValueError as error:
            rejections.append({'input': encode(point), 'result': str(error)})
        else:
            raise AssertionError('Off-curve hostile input was admitted')
    repeated_direction = {signature(add(add(a, b), t))
                          for a, b, t in product((O, P), (O, P), K)}
    require(len(repeated_direction) == 8, 'Repeated-point independence control failed')

    return {
        'status': 'PASS',
        'evidence_grade': 'FRESH_EXACT_FINITE_CERTIFICATE_PLUS_WRITTEN_PROOF_AND_CITED_THEOREMS',
        'utc': datetime.now(timezone.utc).isoformat(),
        'python': platform.python_version(),
        'source_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
        'curve': {'field': 'Q', 'a_invariants': [0, 0, 0, -1156, 0],
                  'root_order': ROOTS, 'discriminant': 64*N**6,
                  'squareclass_support': [-1, 2, 17], 'representatives': D},
        'dependency_policy': {'reads_saved_receipts': False, 'uses_rank_backend': False,
                              'uses_curve_database': False, 'imports_old_checker': False},
        'conclusions': {'rank': 2, 'selmer_2_order': 16, 'selmer_2_dimension': 4,
                        'sha_2_order': 1, 'sha_2_primary': 'ZERO',
                        'sha_all_2_power_torsion': 'Sha[2^n]=0 for every n>=1',
                        'rational_torsion_order': 4,
                        'rational_torsion_structure': '(Z/2Z)^2',
                        'P_Q_independent': True,
                        'P_Q_free_subgroup_index': 'FINITE_ODD_NOT_DETERMINED',
                        'odd_prime_saturation': 'NOT_PERFORMED'},
        'P': encode(P), 'Q': encode(Q),
        'generator_signatures': {'P': signature(P), 'Q': signature(Q),
                                 'T0': torsion_sigs[1], 'Tplus': torsion_sigs[2]},
        'candidate_counts': {'supported': 64, 'real': 32,
                             **{'mod'+str(m): sum(bool(filters[d][str(m)]['primitive_solution_count'])
                                                for d in V) for m in (2, 4, 8)},
                             'mod17': sum(bool(r['primitive_solution_count']) for r in local17.values()),
                             'rationally_witnessed': 16},
        'representatives': records,
        'modular_filters': [{'signature': d, **filters[d], '17': local17[d]} for d in sorted(V)],
        'cosets': [{'representative': IDENTITY, 'members': sorted(H)},
                   {'representative': A, 'members': sorted(AH), 'obstruction_modulus': 8}],
        'rational_search': {'carrier': 'integer x in [-34,10000], nonnegative rational y',
                            'integer_abscissas_tested': 10035,
                            'points_found': [encode(r) for r in searched],
                            'second_direction_selection': 'first point outside delta(<P,E[2]>)'},
        'torsion_good_reductions': reductions,
        'finite_kummer_homomorphism_pairs': 256,
        'local17_hensel_certificate': {'polynomial': 'z^2-2', 'prime': 17,
                                       'residue_root': 6, 'polynomial_residue': 0,
                                       'derivative_residue': 12,
                                       'consequence': '2 is square in Q17; A is locally trivial'},
        'hostile_controls': {'off_curve_rejected': rejections,
                             'repeating_P_instead_of_Q_gives_only_classes': len(repeated_direction),
                             'residue_lift_loss': {'signature': A,
                                'mod4_count': filters[A]['4']['primitive_solution_count'],
                                'mod8_count': filters[A]['8']['primitive_solution_count']}},
        'sources': [
            {'id': 'S_KUMMER', 'url': 'https://www.jmilne.org/math/Books/ectext6.pdf',
             'locator': 'IV section3 Remark3.7, printed p113 / PDF page121; preceding cohomology identification',
             'status': 'THEOREM_CITED', 'hypotheses': 'characteristic zero; distinct rational roots0,34,-34; all E[2] rational'},
            {'id': 'S_MW', 'url': 'https://www.jmilne.org/math/Books/ectext6.pdf',
             'locator': 'IV opening finite basis theorem, printed p101 / PDF page109',
             'status': 'THEOREM_CITED', 'hypotheses': 'nonsingular elliptic curve over number field Q'},
            {'id': 'S_SELMER', 'url': 'https://arxiv.org/pdf/math/0611694',
             'locator': 'section1.1 pp2-3, Kummer map, all-place image definition, Selmer/Sha exact sequence',
             'status': 'THEOREM_CITED', 'hypotheses': 'Q number field; E34 elliptic; n=2^k>1'},
            {'id': 'S_TORSION_REDUCTION', 'url': 'https://www.jmilne.org/math/Books/ectext6.pdf',
             'locator': 'II section5 Corollary5.7, printed p66 / PDF page74',
             'status': 'THEOREM_CITED', 'hypotheses': 'good odd primes3,5; curve over Q'},
            {'id': 'S_HENSEL', 'url': 'https://www.jmilne.org/math/Books/ectext6.pdf',
             'locator': 'I section2 Theorem2.12, printed p24 / PDF page32',
             'status': 'THEOREM_CITED', 'hypotheses': 'z^2-2 has simple root6 modulo17'}],
        'not_established': ['full integral generator saturation at odd primes',
                            'odd-primary Sha or total Sha order',
                            'analytic rank or analytic leading coefficient', 'general BSD theorem'],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = run()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({'status': result['status'], 'counts': result['candidate_counts'],
                      'P': result['P'], 'Q': result['Q'], 'conclusions': result['conclusions'],
                      'output': str(args.output)}, indent=2))


if __name__ == '__main__':
    main()
