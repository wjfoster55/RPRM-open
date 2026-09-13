"""Exact finite checks for the midpoint/reflection bridge; no L-value estimate.

Run from the repository root:
python -I -B research/bsd-rank-two-01/work/midpoint.py --output research/bsd-rank-two-01/evidence/midpoint.json
"""

import argparse
from fractions import Fraction as Q
import json
from pathlib import Path


def centered(a, b):
    return (a+b)/2, (a-b)/2


def uncentered(m, d):
    return m+d, m-d


def interpolate_pair(a, b, tau):
    """Explicit analyst candidate: move BOTH slots linearly; not an inferred user recurrence."""
    return (1-tau)*a+tau*b, tau*a+(1-tau)*b


def value(coefficients, x):
    return sum((c*x**k for k, c in enumerate(coefficients)), Q(0))


def reflection(coefficients):
    return tuple((-1)**k*c for k, c in enumerate(coefficients))


def order(coefficients):
    return next((k for k, c in enumerate(coefficients) if c), None)


def multiply(coefficients, scalar):
    return tuple(scalar*c for c in coefficients)


def preserves_measure_and_cancels(points, permutation, masses, h):
    assert set(permutation) == set(points)
    assert set(permutation.values()) == set(points)
    for x in points:
        assert permutation[permutation[x]] == x
        assert masses[permutation[x]] == masses[x]
        assert h[permutation[x]] == -h[x]
    integral = sum((masses[x]*h[x] for x in points), Q(0))
    assert integral == 0
    return integral


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    a, b = Q(3, 5), Q(2, 5)
    m, d = centered(a, b)
    assert (m, d) == (Q(1, 2), Q(1, 10))
    assert uncentered(m, d) == (a, b)
    assert centered(b, a) == (m, -d)
    assert centered(-a, -b) == (-m, -d)
    assert centered(b, a) != centered(-a, -b)
    assert centered(Q(7, 10), Q(3, 10))[0] == m
    assert centered(Q(7, 10), Q(3, 10))[1] != d
    assert 2*m-a == b
    assert centered(a, -a) == (Q(0), a)
    gap = b-a
    assert gap == Q(-1, 5)
    assert gap/2 == Q(-1, 10)
    assert a+gap == b and a+gap/2 == m
    assert a+gap/2 > b  # The half-step has stopped at the center, before the target.
    assert (m-gap/2, m+gap/2) == (a, b)
    assert a-b == -gap  # Exchanging the slots reverses the directed gap.
    assert interpolate_pair(a, b, Q(0)) == (a, b)
    assert interpolate_pair(a, b, Q(1)) == (b, a)
    assert interpolate_pair(a, b, Q(1, 2)) == (m, m)
    assert interpolate_pair(Q(7, 10), Q(3, 10), Q(1, 2)) == (m, m)
    # If only the first slot moves and the second is kept, information is retained.
    first_slot_half_step = (m, b)
    assert (2*first_slot_half_step[0]-first_slot_half_step[1], first_slot_half_step[1]) == (a, b)

    # Bounded complete replay of coordinate identities; proof is in the note.
    grid = [Q(j, 10) for j in range(-10, 11)]
    for aa in grid:
        for bb in grid:
            mm, dd = centered(aa, bb)
            assert uncentered(mm, dd) == (aa, bb)
            assert centered(bb, aa) == (mm, -dd)
            assert centered(-aa, -bb) == (-mm, -dd)
            for tau in (Q(0), Q(1, 4), Q(1, 2), Q(3, 4), Q(1)):
                moved = interpolate_pair(aa, bb, tau)
                assert centered(*moved) == (mm, (1-2*tau)*dd)
                if tau != Q(1, 2):
                    moved_m, moved_d = centered(*moved)
                    assert uncentered(moved_m, moved_d/(1-2*tau)) == (aa, bb)

    # Coefficients of Lambda(1+t) and F(1/2+d)=Lambda(1+2d).
    source_coefficients = (Q(3), Q(-2), Q(5), Q(7), Q(-11))
    midpoint_coefficients = tuple(2**k*c for k, c in enumerate(source_coefficients))
    for dd in grid:
        assert value(midpoint_coefficients, dd) == value(source_coefficients, 2*dd)
        z = Q(1, 2)+dd
        assert 2*(1-z) == 2-2*z

    even = (Q(0), Q(0), Q(3), Q(0), Q(1))
    odd = (Q(0), Q(5), Q(0), Q(-2), Q(0))
    assert reflection(even) == even
    assert reflection(odd) == multiply(odd, -1)
    for k, c in enumerate(even):
        assert ((-1)**k-1)*c == 0
    for k, c in enumerate(odd):
        assert ((-1)**k+1)*c == 0

    # Same +1 reflection symmetry and quartic coefficient, different zero order.
    epsilon = Q(1, 10**12)
    quartic = (Q(0), Q(0), Q(0), Q(0), Q(1))
    perturbed = (Q(0), Q(0), epsilon, Q(0), Q(1))
    assert reflection(quartic) == quartic
    assert reflection(perturbed) == perturbed
    assert order(quartic) == 4 and order(perturbed) == 2
    assert quartic[4] == perturbed[4] == 1
    for dd in grid:
        assert value(quartic, dd) >= 0 and value(perturbed, dd) >= 0
        assert value(perturbed, dd)-value(quartic, dd) == epsilon*dd*dd

    # Finite signed measure; each T orbit has equal masses, opposite h values.
    points = (0, 1, 2, 3)
    involution = {0: 1, 1: 0, 2: 3, 3: 2}
    masses = {0: Q(2), 1: Q(2), 2: Q(-3), 3: Q(-3)}
    h = {0: Q(7, 5), 1: Q(-7, 5), 2: Q(4, 9), 3: Q(-4, 9)}
    cancellation = preserves_measure_and_cancels(points, involution, masses, h)
    # Breaking either premise removes the inference: these examples do not cancel.
    wrong_masses = dict(masses)
    wrong_masses[1] = Q(1)
    wrong_mass_sum = sum((wrong_masses[x]*h[x] for x in points), Q(0))
    assert wrong_mass_sum != 0
    wrong_h = dict(h)
    wrong_h[1] = h[0]
    wrong_sign_sum = sum((masses[x]*wrong_h[x] for x in points), Q(0))
    assert wrong_sign_sum != 0

    result = {
        "status": "PASS",
        "arithmetic": "fractions.Fraction, exact rational arithmetic",
        "coordinate_example": {"a": a, "b": b, "m": m, "d": d,
                               "recovered": uncentered(m, d),
                               "swap_coordinates": centered(b, a),
                               "negate_both_coordinates": centered(-a, -b)},
        "coordinate_grid": {"a_and_b": "j/10, -10 <= j <= 10", "pairs": len(grid)**2},
        "directed_step_correction": {"from": a, "to": b, "full_gap": gap,
                                    "half_gap": gap/2, "half_step_endpoint": a+gap/2,
                                    "retained_midpoint_and_gap_recovery": (m-gap/2, m+gap/2),
                                    "first_slot_only_half_step": first_slot_half_step},
        "whole_pair_interpolation_candidate": {"status": "Analyst-defined comparison; not a user-supplied recurrence",
                                               "tau_0": interpolate_pair(a, b, Q(0)),
                                               "tau_half": interpolate_pair(a, b, Q(1, 2)),
                                               "tau_1": interpolate_pair(a, b, Q(1)),
                                               "offset_rule": "d_tau=(1-2*tau)d"},
        "analytic_coordinate_change": {"s": "2z", "z": "1/2+d", "t": "2d",
                                       "source_coefficients": source_coefficients,
                                       "midpoint_coefficients": midpoint_coefficients},
        "reflection_checks": {"w_plus": even, "w_minus": odd},
        "same_parity_negative_control": {"epsilon": epsilon,
                                        "quartic_coefficients": quartic,
                                        "perturbed_coefficients": perturbed,
                                        "orders": [order(quartic), order(perturbed)]},
        "cancellation_check": {"signed_masses": masses, "involution": involution,
                               "h": h, "sum": cancellation,
                               "broken_measure_sum": wrong_mass_sum,
                               "broken_sign_sum": wrong_sign_sum},
        "evidence_ceiling": "Finite exact identity checks and analytic-germ controls; no elliptic-curve rank or L-value calculation",
    }
    output = json.dumps(result, default=str, indent=2)+"\n"
    if args.output:
        args.output.write_text(output, encoding="utf-8")
        print(json.dumps({"status": "PASS", "output": str(args.output), "exact_grid_pairs": 441}, indent=2))
    else:
        print(output, end="")


if __name__ == "__main__":
    main()
