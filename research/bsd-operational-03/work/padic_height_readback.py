"""Independent E34 rational-duplication and 5-adic-height residue readback.

This imports no computation from the main height implementation. The witness
provides values to check; its status and theorem conclusions are never inputs.
The p-adic interpretation is a written theorem dependency, not inferred by
this finite arithmetic verifier.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
from math import gcd, isqrt
from pathlib import Path


D = 1156


def require(condition, message):
    if not condition:
        raise ValueError(message)


def on_curve(point):
    x, y = point
    return y*y == x*x*x-D*x


def duplicate(point):
    """Closed duplication polynomials, without a secant/tangent slope."""
    x, y = point
    require(on_curve(point), 'duplication input is off curve')
    require(y != 0, 'this readback admits only nontorsion affine inputs')
    next_x = (x*x+D)**2/(4*y*y)
    next_y = (x**6-5*D*x**4-5*D*D*x*x+D**3)/(8*y**3)
    result = next_x, next_y
    require(on_curve(result), 'duplication output is off curve')
    return result


def five_valuation(value):
    numerator, denominator = value.numerator, value.denominator
    require(numerator != 0, 'zero has infinite rather than finite valuation')
    result = 0
    while numerator % 5 == 0:
        numerator //= 5
        result += 1
    while denominator % 5 == 0:
        denominator //= 5
        result -= 1
    return result


def primitive(point):
    x, y = point
    denominator = isqrt(x.denominator)
    require(denominator*denominator == x.denominator,
            'abscissa denominator is not a square')
    ordinate = y*denominator**3
    require(ordinate.denominator == 1, 'ordinate denominator is not compatible')
    a, b, d = x.numerator, ordinate.numerator, denominator
    require(gcd(a, d) == gcd(b, d) == 1, 'nonprimitive integral coordinates')
    require(b*b == a*a*a-D*a*d**4, 'integral curve equation fails')
    return a, b, d


def local_component(a, b, d, prime):
    if d % prime == 0:
        return {'prime': prime, 'reduction': 'O', 'nonsingular': True}
    x = a*pow(d, -2, prime) % prime
    y = b*pow(d, -3, prime) % prime
    require((y*y-x*x*x+D*x) % prime == 0, 'bad-prime reduction off curve')
    gradient = [(-3*x*x+D) % prime, 2*y % prime]
    require(gradient != [0, 0], 'point is outside identity component')
    return {'prime': prime, 'reduction': [x, y], 'gradient': gradient,
            'nonsingular': True}


def row(point):
    doubled = point
    for _ in range(3):
        doubled = duplicate(doubled)
    a, b, d = primitive(doubled)
    t = -doubled[0]/doubled[1]
    require(five_valuation(t) >= 1, 'eightfold point is outside the formal group')
    unit = Fraction(-a, b)
    require(t/d == unit and five_valuation(unit) == 0, 'incorrect unit extraction')
    residue = unit.numerator*pow(unit.denominator, -1, 25) % 25
    fourth = residue**4 % 25
    require(fourth % 5 == 1, 'fourth power of unit must be one mod five')
    h = ((fourth-1)//5)*pow(256, -1, 5) % 5
    return {
        'point': [str(coordinate) for coordinate in point],
        'eight_times_point': [str(coordinate) for coordinate in doubled],
        'integral_coordinates': {'a': str(a), 'b': str(b), 'd': str(d)},
        't': str(t), 'v5_t': five_valuation(t),
        'unit_t_over_d_mod25': residue, 'u_fourth_mod25': fourth,
        'h_MST_mod5': h,
        'bad_prime_connected_component_checks': [local_component(a, b, d, p)
                                                   for p in (2, 17)],
    }


def point_count(prime):
    affine = [[x, y] for x in range(prime) for y in range(prime)
              if (y*y-x*x*x+D*x) % prime == 0]
    return {'prime': prime, 'affine_points': affine, 'count': len(affine)+1,
            'trace': prime-len(affine)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--witness', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    require(not arguments.output.exists(), 'preserve earlier evidence')
    witness_bytes = arguments.witness.read_bytes()
    witness = json.loads(witness_bytes)
    # Fixed input sources are admitted independently of the stored witness.
    P = Fraction(-2), Fraction(48)
    Q = Fraction(-16), Fraction(120)
    require(on_curve(P) and on_curve(Q), 'base inputs off curve')
    slope = (Q[1]-P[1])/(Q[0]-P[0])
    sum_x = slope*slope-P[0]-Q[0]
    S = sum_x, slope*(P[0]-sum_x)-P[1]
    require(on_curve(S), 'independently constructed sum is off curve')
    computations = {}
    for label, point in [('P', P), ('Q', Q), ('P+Q', S)]:
        fresh = row(point)
        stored = witness['heights'][label]
        for key, value in fresh.items():
            require(stored[key] == value, f'witness mismatch for {label}: {key}')
        computations[label] = fresh
    a = computations['P']['h_MST_mod5']
    c = computations['Q']['h_MST_mod5']
    mixed = (computations['P+Q']['h_MST_mod5']-a-c)*3 % 5
    polar = [[a, mixed], [mixed, c]]
    gram = [[3*entry % 5 for entry in entries] for entries in polar]
    determinant = (gram[0][0]*gram[1][1]-gram[0][1]*gram[1][0]) % 5
    require(witness['MST_pairing_matrix_mod5'] == gram, 'stored Gram matrix differs')
    require(witness['MST_determinant_mod5'] == determinant, 'stored determinant differs')
    require(determinant != 0, 'regulator residue does not certify nonvanishing')

    at_three = point_count(3)
    at_five = point_count(5)
    require((64*34**6) % 3 != 0, 'three is not a good-reduction prime')
    require(at_three['trace'] == 0, 'the irreducibility test has a different trace')
    discriminant_mod5 = (at_three['trace']**2-4*3) % 5
    squares_mod5 = sorted({x*x % 5 for x in range(5)})
    frobenius_roots = [x for x in range(5)
                       if (x*x-at_three['trace']*x+3) % 5 == 0]
    require(discriminant_mod5 not in squares_mod5 and not frobenius_roots,
            'the Frobenius polynomial is reducible over F5')
    require(at_five['count'] == 8 and at_five['trace'] % 5 != 0,
            'five is not admitted as the stated ordinary prime')
    output = {
        'created_utc': datetime.now(timezone.utc).isoformat(),
        'status': 'INDEPENDENT_RATIONAL_AND_HEIGHT_RESIDUE_READBACK_PASSED',
        'main_math_imported': False, 'stored_status_read': False,
        'duplication_method': 'closed x/y duplication polynomials',
        'heights': computations, 'polar_half_h_matrix_mod5': polar,
        'MST_pairing_matrix_mod5': gram, 'MST_determinant_mod5': determinant,
        'point_count_mod3': at_three, 'point_count_mod5': at_five,
        'frobenius_mod5_test': {'polynomial': 'X^2+3',
                               'discriminant_mod5': discriminant_mod5,
                               'squares_mod5': squares_mod5,
                               'roots': frobenius_roots,
                               'irreducible': True},
        'evidence_boundary': ('Finite rational and residue arithmetic; p-adic sigma, '
                             'height, Frobenius and Bockstein meanings require the '
                             'written domain-theorem audit.'),
        'witness_sha256': hashlib.sha256(witness_bytes).hexdigest(),
        'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(output, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({key: output[key] for key in (
        'status', 'MST_pairing_matrix_mod5', 'MST_determinant_mod5',
        'frobenius_mod5_test')}, indent=2))


if __name__ == '__main__':
    main()
