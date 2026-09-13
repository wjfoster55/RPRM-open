"""Exact checks supporting VACUUM_SEPARATING_WITNESS.md; no simulation.

Python standard library, 3.10+. Default compares the existing receipt.
The analytic proof and all-real interval are in the Markdown derivation.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
from hashlib import sha256
import json
from math import comb
from pathlib import Path

HERE = Path(__file__).resolve().parent
Poly = dict[tuple[int, int, int], F]


def require(test, name):
    if not test:
        raise RuntimeError(name)


def add(*polys):
    ans = {}
    for p in polys:
        for key, val in p.items():
            ans[key] = ans.get(key, F(0)) + val
    return {key: val for key, val in ans.items() if val}


def scale(c, p):
    return {key: F(c) * val for key, val in p.items() if c * val}


def mul(p, q):
    out = {}
    for i, c in p.items():
        for j, d in q.items():
            key = tuple(x + y for x, y in zip(i, j))
            out[key] = out.get(key, F(0)) + c * d
    return {key: val for key, val in out.items() if val}


def coord_moment(n):
    # Uniform S^3 coordinate: Catalan(m)/4^m for n=2m.
    if n % 2:
        return F(0)
    m = n // 2
    return F(comb(2 * m, m), (m + 1) * 4**m)


def radial_moment(n, power):
    return sum(((-1)**i * comb(power, i) * coord_moment(n + 2*i)
                for i in range(power + 1)), F(0))


def moment(i, j, k):
    # w=ab+D; E[D^(2m)|a,b]=[(1-a²)(1-b²)]^m/(2m+1).
    return sum((F(comb(k, 2*m), 2*m+1)
                * radial_moment(i+k-2*m, m)
                * radial_moment(j+k-2*m, m)
                for m in range(k//2+1)), F(0))


def mean(p):
    return sum((c * moment(*key) for key, c in p.items()), F(0))


def value(p, a, b, w):
    return sum((c * a**i * b**j * w**k
                for (i, j, k), c in p.items()), F(0))


def compute():
    one = {(0, 0, 0): F(1)}
    a, b, w = ({(1, 0, 0): F(1)}, {(0, 1, 0): F(1)}, {(0, 0, 1): F(1)})
    ab = mul(a, b)
    a2, b2 = mul(a, a), mul(b, b)
    D = add(w, scale(-1, ab))
    u1 = scale(F(1, 6), add(a, b))
    u2 = add(scale(F(1, 96), add(a2, b2, scale(F(-1, 2), one))),
             scale(F(1, 39), ab), scale(F(1, 351), w))
    log2 = add(scale(2, u2), scale(-1, mul(u1, u1)))
    require(mean(u1) == mean(u2) == mean(D) == 0, 'Haar mean conventions')
    require(mean(mul(D, D)) == F(3, 16), 'D norm')
    require(mean(mul(D, w)) == F(3, 16), 'D-w contraction')
    orthogonal_controls = 0
    for i in range(9):
        for j in range(9-i):
            require(mean(mul(D, {(i, j, 0): F(1)})) == 0,
                    f'conditional orthogonality control {i},{j}')
            orthogonal_controls += 1
    require(mean(mul(D, u1)) == 0, 'first-order annihilation')
    require(mean(mul(D, log2)) == F(1, 936), 'second-order signed readout')
    # UV is Haar as well. This supplies independent convolution-marginal controls.
    convolution_controls = 0
    for k in range(13):
        require(moment(0, 0, k) == coord_moment(k), f'UV Haar marginal {k}')
        convolution_controls += 1
    require(mean(mul(u1, u1)) == F(1, 72), 'density normalizer coefficient')
    normalized_log2 = add(log2, scale(F(-1, 72), one))
    require(normalized_log2[(0, 0, 0)] == F(-7, 288), 'normalized log constant')
    require(mean(mul(D, normalized_log2)) == F(1, 936), 'normalization cancels')

    delta = add(one, scale(-1, a2), scale(-1, b2), scale(-1, mul(w, w)),
                scale(2, mul(ab, w)))
    pair = [(F(0), F(0), F(3, 5)), (F(0), F(0), F(-3, 5))]
    require(all(value(delta, *p) == F(16, 25) for p in pair), 'interior hostile pair')
    require(value(log2, *pair[0]) - value(log2, *pair[1]) == F(4, 585),
            'hostile jet separation only')

    K0 = F(104207, 52043)
    require(K0 < F(7, 3), 'accepted ratio simplification')
    require(F(16, 3) * F(1, 10) == F(8, 15) < 1, 'exponent interval')
    u2_bound = F(1, 64) + F(1, 39) + F(1, 351)
    require(u2_bound < F(1, 20), 'u2 uniform bound')
    p2_lower = 1-F(1, 30)-F(1, 2000)
    require(p2_lower > F(9, 10) > F(1, 7), 'positive polynomial approximant')
    require(625 < 648, '5/(9 sqrt(2)) < 2/5 after positive squaring')
    require(F(1, 3)+F(1, 10)*F(1, 20) < F(7, 20), 'z coefficient')
    require(F(7, 20)*F(1, 10) < F(1, 10), 'log-series domain')
    scalar_log_tail = F(343, 21600)+F(1, 60)+F(1, 3200)
    require(scalar_log_tail < F(1, 25), 'full scalar logarithm suffix bound')
    require(7*F(2, 5)+F(1, 25) < 3, 'full L2 logarithm error')
    require(4*F(3, 16) < 1, '2||D||_2 < 1 after squaring')
    rmax = F(1, 3000)
    require(0 < rmax < F(1, 10), 'coupling domain')
    require(3*rmax == F(1, 1000), 'all-interval cubic error coefficient')
    require(F(1, 936)-F(1, 1000) == F(4, 58500) > 0, 'strict separating margin')
    require(value(log2, 0, 0, 0) == F(-1, 96), 'unnormalized log convention')

    return {
        'schema': 'ym2-connected-vacuum-witness-v1',
        'status': 'PASS',
        'evidence_grade': 'exact finite checks supporting the linked written proof',
        'checker_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
        'orthogonality_monomial_controls': orthogonal_controls,
        'convolution_haar_marginal_controls': convolution_controls,
        'D_norm_squared': '3/16',
        'J_second_order_coefficient': '1/936',
        'normalized_log_second_order_constant': '-7/288',
        'u2_sup_majorant': str(u2_bound),
        'p2_lower_majorant_at_r_1_10': str(p2_lower),
        'scalar_log_tail_coefficient': str(scalar_log_tail),
        'full_log_phi_L2_error_bound': '< 3 r^3 for 0<r<=1/10',
        'J_full_remainder_bound': '|J-r^2/936| < 3r^3 for 0<r<=1/10',
        'certified_interval': '0<r<=1/3000',
        'strict_lower_bound': 'J(r) > (4/58500)r^2',
        'hostile_pair': ['(0,0,3/5)', '(0,0,-3/5)'],
        'hostile_pair_second_order_difference': '4/585 (jet only)',
        'boundary': ('All-real quantifiers, conditional moments, analytic perturbation '
                     'and the accepted vacuum lower bound use written proofs. '
                     'No numerical eigenvalue, simulation or old source test is run.')
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--write-results', action='store_true')
    args = parser.parse_args()
    result = compute()
    target = HERE / 'RESULTS_WITNESS.json'
    if args.write_results:
        target.write_text(json.dumps(result, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
    else:
        require(json.loads(target.read_text(encoding='utf-8')) == result,
                'saved receipt differs from current exact computation')
    print('PASS: actual-vacuum witness rational checks; '
          f"{result['orthogonality_monomial_controls']} orthogonality and "
          f"{result['convolution_haar_marginal_controls']} Haar controls")


if __name__ == '__main__':
    main()
