"""Exact E5 coordinate checks and the user's bounded ordered-pair trace.

The proposed carry/swap trace is retained as a partial map, not identified
with elliptic-curve division or promoted to a universal recurrence.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import json
from math import isqrt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
P = (F(-4), F(6))


def point_json(point):
    return 'O' if point is None else [str(v) for v in point]


def on_e5(point):
    return point is None or point[1]**2 == point[0]**3-25*point[0]


def add(a, b):
    if not on_e5(a) or not on_e5(b):
        raise ValueError('Curve-point admission error')
    if a is None or b is None:
        return b if a is None else a
    x, y = a
    u, v = b
    if x == u and y == -v:
        return None
    slope = (3*x*x-25)/(2*y) if a == b else (v-y)/(u-x)
    xx = slope*slope-x-u
    out = (xx, slope*(x-xx)-y)
    assert on_e5(out)
    return out


def normalized(point):
    return None if point is None else (point[0]/5, point[1]/25)


def unnormalized(point):
    return None if point is None else (5*point[0], 25*point[1])


def y_fiber(x, normalized_model=False):
    value = (x*x*x-x)/5 if normalized_model else x*x*x-25*x
    if value < 0:
        return {'status': 'NONE', 'rhs_y_squared': str(value), 'reason': 'Negative square required over Q.'}
    a, b = isqrt(value.numerator), isqrt(value.denominator)
    if a*a != value.numerator or b*b != value.denominator:
        return {'status': 'NONE', 'rhs_y_squared': str(value),
                'reason': 'Reduced rational has numerator or denominator that is not an integer square.'}
    values = sorted({F(a,b), -F(a,b)})
    return {'status': 'ONE' if len(values) == 1 else 'MANY', 'rhs_y_squared': str(value),
            'values': [str(v) for v in values]}


def translated_add(left, right, coefficients):
    """Direct chord/tangent law on Y²+a3Y=X³+a2X²+a4X+a6."""
    a2, a3, a4, a6 = coefficients
    def admitted(point):
        if point is not None:
            x,y = point
            assert y*y+a3*y == x**3+a2*x*x+a4*x+a6
    admitted(left)
    admitted(right)
    if left is None or right is None:
        return right if left is None else left
    x,y = left
    u,v = right
    if x == u and y+v == -a3:
        return None
    slope = (3*x*x+2*a2*x+a4)/(2*y+a3) if left==right else (v-y)/(u-x)
    intercept = y-slope*x
    xx = slope*slope-a2-x-u
    answer = (xx, -slope*xx-intercept-a3)
    admitted(answer)
    return answer


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT/'evidence/coordinates.json')
    args = parser.parse_args()
    K = [None, (F(0), F(0)), (F(5), F(0)), (F(-5), F(0))]
    points = K+[P, (P[0],-P[1]), add(P,P)]
    for point in points:
        q = normalized(point)
        assert unnormalized(q) == point
        assert q is None or 5*q[1]**2 == q[0]**3-q[0]
    # Transport addition by the inverse map; no claim that raw slot swapping
    # automatically preserves the old cubic.
    for a in points:
        for b in points:
            qa, qb = normalized(a), normalized(b)
            transported = normalized(add(unnormalized(qa), unnormalized(qb)))
            assert transported == normalized(add(a,b))
    translation_cars = []
    for shift_x,shift_y in [(3,-6),(4,-5)]:
        coefficients = (-3*shift_x,-2*shift_y,3*shift_x**2-25,
                        -shift_x**3+25*shift_x-shift_y**2)
        encode = lambda p: None if p is None else (p[0]+shift_x,p[1]+shift_y)
        decode = lambda p: None if p is None else (p[0]-shift_x,p[1]-shift_y)
        for point in points:
            assert decode(encode(point)) == point
        for a in points:
            for b in points:
                assert translated_add(encode(a),encode(b),coefficients) == encode(add(a,b))
        p_image = encode(P)
        inverse_image = encode((P[0],-P[1]))
        assert p_image != inverse_image
        translation_cars.append({'shift':[shift_x,shift_y],
            'forward':'(X,Y)=(x+s,y+t)', 'inverse':'(x,y)=(X-s,Y-t)',
            'a_invariants':[0,*coefficients], 'P_image':point_json(p_image),
            'minus_P_image':point_json(inverse_image), 'identity_image':'O',
            'group_pairs_checked':len(points)**2,
            'meaning':'Same curve in new coordinates; P remains primitive. Zero Y alone no longer characterizes two-torsion because the Y-linear coefficient changes.'})
    tests = [(6,4),(-6,4),(3,5),(3,4),(1,2),(-1,0),(0,1)]
    literal_checks = [{'pair': pair,
        'interpretation': 'Only the literal x,y interpretation on the unchanged E5 equation',
        'residual': str(F(pair[1])**2-F(pair[0])**3+25*pair[0]),
        'on_e5': on_e5(tuple(map(F,pair)))} for pair in tests]
    trace = [(0,1),(2,1),(3,4),(6,4)]
    forward = dict(zip(trace[:-1], trace[1:]))
    inverse = {b:a for a,b in forward.items()}
    assert len(forward) == len(inverse) == 3
    assert all(inverse[forward[a]] == a for a in forward)
    # Test two literal, fully stated interpretations, without attributing them
    # to William's as-yet incompletely specified carry/phase operation.
    carry_then_swap = lambda a,b: (b,a+1)
    swap_then_carry = lambda a,b: (b+1,a)
    candidate_tests = []
    for name, operation in [('increment_first_then_swap',carry_then_swap),
                            ('swap_then_increment_first',swap_then_carry)]:
        rows = [{'from': a, 'required': b, 'computed': operation(*a),
                 'matches': operation(*a)==b} for a,b in forward.items()]
        candidate_tests.append({'candidate': name, 'edges': rows,
            'status': 'CONFIRMED_ON_TRACE' if all(r['matches'] for r in rows) else 'REFUTED_AS_A_COMPLETE_DESCRIPTION_OF_THIS_TRACE'})
    assert F(6,4) == F(3,2) and (6,4) != (3,2)
    assert add((F(-5),F(0)),(F(-5),F(0))) is None
    result = {
        'status': 'CONFIRMED_AT_DECLARED_SCOPES', 'utc': datetime.now(timezone.utc).isoformat(),
        'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'exact_curve_isomorphism': {'source': 'y^2=x^3-25x', 'target': '5v^2=u^3-u',
            'forward': '(u,v)=(x/5,y/25)', 'inverse': '(x,y)=(5u,25v)',
            'P_image': point_json(normalized(P)), 'O_image': 'O',
            'minus_one_zero_preimage': ['-5','0'], 'minus_one_zero_order': 2,
            'finite_retraction_checks': len(points), 'transported_addition_pairs': len(points)**2,
            'universal_support': 'Exact substitution; origin-preserving curve isomorphism transports the elliptic group law.'},
        'literal_pair_checks': literal_checks,
        'explicit_generator_relabelings': translation_cars,
        'partial_coordinate_queries': {
            'E5_x_zero': y_fiber(F(0)), 'E5_x_minus_one_fifth': y_fiber(F(-1,5)),
            'normalized_u_minus_one_fifth': y_fiber(F(-1,5),True)},
        'user_trace': {'carrier': 'ordered integer pairs, preserving both slots and their occurrences',
            'ascending': trace, 'descending': list(reversed(trace)),
            'forward_edges': [{'from':a,'to':b} for a,b in forward.items()],
            'exact_inverse_on_observed_image': True,
            'base_symbol': '--0 retained as the user\'s symbol; no arithmetic or orientation identification assumed',
            'general_carry_sign_phase_rule': 'OPEN: the finite trace and verbal description do not yet specify which slot changes, carry state, sign state and branch at all other inputs.',
            'elliptic_curve_adapter': 'OPEN: no map from this complete ordered-pair carrier to E(Q) and transported addition has yet been specified.'},
        'two_literal_candidate_rules': candidate_tests,
        'ratio_fold': {'inputs': [[6,4],[3,2]], 'equal_rational_value': '3/2',
            'different_slot_states': True, 'meaning': 'Reducing a slash label to a rational number can discard slot/carry information.'},
        'claim_boundary': 'A failed literal affine-point test does not refute an RPRM coordinate change. A genuine isomorphism preserves identity, element order and primitivity; a lossy fold requires its receiver/fiber contract.'
    }
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'status':result['status'],'partial_trace_edges':3,'normalized_P':result['exact_curve_isomorphism']['P_image'],
                      'normalized_minus_one_zero_order':2,'carry_law_status':'OPEN'}))


if __name__ == '__main__':
    main()
