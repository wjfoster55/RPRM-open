"""Exact finite controls for STATIC_JOIN.md; Python standard library only."""

from fractions import Fraction as F
from itertools import combinations, product
import argparse
import json
from pathlib import Path


def q(*xs):
    return tuple(F(x) for x in xs)


def dot(x, y):
    return sum((a * b for a, b in zip(x, y)), F(0))


def cross(x, y):
    return (x[1] * y[2] - x[2] * y[1],
            x[2] * y[0] - x[0] * y[2],
            x[0] * y[1] - x[1] * y[0])


def mul(x, y):
    """Plus-i Pauli convention: the vector cross term has a minus sign."""
    a, u, b, v = x[0], x[1:], y[0], y[1:]
    uv = cross(u, v)
    return (a * b - dot(u, v),) + tuple(
        a * v[i] + b * u[i] - uv[i] for i in range(3))


def inv(x):
    return (x[0],) + tuple(-t for t in x[1:])


def ca(z, w):
    return z[0] + w[0], z[1] + w[1]


def cm(z, w):
    return z[0] * w[0] - z[1] * w[1], z[0] * w[1] + z[1] * w[0]


def matrix(x):
    """Direct a I + i(x sigma1 + y sigma2 + z sigma3), exact complex pairs."""
    a, b, c, d = x
    return (((a, d), (c, b)), ((-c, b), (a, -d)))


def mm(a, b):
    return tuple(tuple(ca(cm(a[i][0], b[0][j]), cm(a[i][1], b[1][j]))
                       for j in range(2)) for i in range(2))


def matrix_scalar(a):
    t = ca(a[0][0], a[1][1])
    assert t[1] == 0
    return t[0] / 2


def invariants(xs):
    v = [x[1:] for x in xs]
    a = tuple(x[0] for x in xs)
    g = tuple(tuple(dot(x, y) for y in v) for x in v)
    t = tuple(tuple(tuple(dot(cross(x, y), z) for z in v) for y in v)
              for x in v)
    return a, g, t


def joint_product(old, i, j, k):
    """S7 computed only from old joint, replacing named occurrence k by i*j."""
    a, g, t = old
    n = len(a)
    b = list(a)
    b[k] = a[i] * a[j] - g[i][j]

    def entry(r, s):
        if r == k and s == k:
            return 1 - b[k] ** 2
        if r == k or s == k:
            ell = s if r == k else r
            return a[i] * g[j][ell] + a[j] * g[i][ell] - t[i][j][ell]
        return g[r][s]

    def triple(r, s, p):
        indices = (r, s, p)
        if len(set(indices)) < 3:
            return F(0)
        if k not in indices:
            return t[r][s][p]
        pos = indices.index(k)
        ell, m = indices[(pos + 1) % 3], indices[(pos + 2) % 3]
        return (a[i] * t[j][ell][m] + a[j] * t[i][ell][m]
                - g[i][ell] * g[j][m] + g[i][m] * g[j][ell])

    return (tuple(b), tuple(tuple(entry(r, s) for s in range(n))
                           for r in range(n)),
            tuple(tuple(tuple(triple(r, s, p) for p in range(n))
                        for s in range(n)) for r in range(n)))


def det3(m):
    return dot(m[0], cross(m[1], m[2]))


def pair_image(a, b, d):
    return abs(a) <= 1 and abs(b) <= 1 and d * d <= (1-a*a) * (1-b*b)


def serial(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {k: serial(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [serial(v) for v in value]
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-results", action="store_true",
                        help="replace the saved receipt; default only recomputes and compares it")
    args = parser.parse_args()
    identity = q(1, 0, 0, 0)
    i, j, k = q(0, 1, 0, 0), q(0, 0, 1, 0), q(0, 0, 0, 1)
    u = q("3/5", "4/5", 0, 0)
    v = q("3/5", 0, "4/5", 0)
    z = q("3/5", 0, 0, "4/5")
    minus_z = q("3/5", 0, 0, "-4/5")
    seeds = [identity, q(-1, 0, 0, 0), i, j, k, u,
             q("1/2", "1/2", "1/2", "1/2")]
    assert all(dot(x, x) == 1 for x in seeds)

    for x, y in product(seeds, repeat=2):
        assert matrix(mul(x, y)) == mm(matrix(x), matrix(y))
        assert dot(mul(x, y), mul(x, y)) == 1
        assert mul(x, inv(x)) == identity
    for x, y, zz in product(seeds, repeat=3):
        lhs, rhs = mul(mul(x, y), zz), mul(x, mul(y, zz))
        assert lhs == rhs
        assert matrix(lhs) == mm(mm(matrix(x), matrix(y)), matrix(zz))

    w_low, w_high = mul(u, u)[0], mul(u, inv(u))[0]
    assert (w_low, w_high) == (F(-7, 25), F(1))
    assert pair_image(F(3, 5), F(3, 5), F(16, 25))
    assert not pair_image(F(3, 5), F(3, 5), F(17, 25))
    assert pair_image(F(1), F(3, 5), F(0))
    assert not pair_image(F(1), F(3, 5), F(1, 100))
    assert not pair_image(F(6, 5), F(3, 5), F(0))

    plus, minus = [u, v, z], [u, v, minus_z]
    ap, gp, tp = invariants(plus)
    am, gm, tm = invariants(minus)
    assert (ap, gp) == (am, gm)
    assert tp[0][1][2] == -tm[0][1][2] == F(64, 125)
    triple_plus = matrix_scalar(mm(mm(matrix(u), matrix(v)), matrix(z)))
    triple_minus = matrix_scalar(mm(mm(matrix(u), matrix(v)), matrix(minus_z)))
    assert (triple_plus, triple_minus) == (F(91, 125), F(-37, 125))
    assert det3(gp) == tp[0][1][2] ** 2
    pairs_plus = [mul(plus[r], plus[s])[0] for r, s in combinations(range(3), 2)]
    pairs_minus = [mul(minus[r], minus[s])[0] for r, s in combinations(range(3), 2)]
    assert pairs_plus == pairs_minus == [F(9, 25)] * 3

    # Rank 0, 1, 2, and 3 controls, including mixed/repeated factor replacements.
    states = [[identity] * 4, [u, inv(u), i, identity],
              [u, v, i, j], [u, v, z, seeds[-1]]]
    update_count = 0
    minor_count = 0
    for xs in states:
        old = invariants(xs)
        a, g, t = old
        for ix, jx in product(combinations(range(4), 3), repeat=2):
            minor = det3(tuple(tuple(g[r][s] for s in jx) for r in ix))
            assert t[ix[0]][ix[1]][ix[2]] * t[jx[0]][jx[1]][jx[2]] == minor
            minor_count += 1
        for r, s, target in product(range(4), repeat=3):
            ys = list(xs)
            ys[target] = mul(xs[r], xs[s])
            assert joint_product(old, r, s, target) == invariants(ys)
            update_count += 1

    rotated = [(x[0], -x[1], -x[2], x[3]) for x in plus]
    assert invariants(rotated) == invariants(plus)
    for xs in [plus, minus, rotated]:
        a, g, t = invariants(xs)
        formula = a[0]*a[1]*a[2]-a[2]*g[0][1]-a[0]*g[1][2]-a[1]*g[0][2]+t[0][1][2]
        assert formula == matrix_scalar(mm(mm(matrix(xs[0]), matrix(xs[1])), matrix(xs[2])))

    outer = z
    ua, ub = u, q("4/5", "3/5", 0, 0)
    va, vb = mul(inv(ua), outer), mul(inv(ub), outer)
    assert va == q("9/25", "-12/25", "-16/25", "12/25")
    assert vb == q("12/25", "-9/25", "-12/25", "16/25")
    assert mul(ua, va) == mul(ub, vb) == outer
    assert mm(matrix(ua), matrix(va)) == mm(matrix(ub), matrix(vb)) == matrix(outer)
    assert mul(ua, va) != mul(va, ua) and mul(ub, vb) != mul(vb, ub)
    fine_a, fine_b = 2-ua[0]-va[0], 2-ub[0]-vb[0]
    assert (fine_a, fine_b) == (F(26, 25), F(18, 25))
    # The exact squared bound avoids approximate square-root comparisons.
    for split, w in product(seeds + [ua, ub], seeds + [outer]):
        other = mul(inv(split), w)
        assert mul(split, other) == w
        total_scalar = split[0] + other[0]
        assert total_scalar == (1+w[0])*split[0] + dot(split[1:], w[1:])
        assert total_scalar ** 2 <= 2+2*w[0]
        if w == q(-1, 0, 0, 0):
            assert 2-total_scalar == 2

    powers_first = mul(mul(i, i), mul(j, j))
    product_first = mul(mul(i, j), mul(i, j))
    assert powers_first == identity and product_first == q(-1, 0, 0, 0)
    assert mm(mm(matrix(i), matrix(i)), mm(matrix(j), matrix(j))) == matrix(identity)
    assert mm(mm(matrix(i), matrix(j)), mm(matrix(i), matrix(j))) == matrix(product_first)

    result = {
        "status": "PASS",
        "arithmetic": "fractions.Fraction; independent exact complex Pauli matrices",
        "claim_grade": "Finite exact controls; continuous-fiber coverage is a written proof in STATIC_JOIN.md",
        "scope": "Static finite SU(2) tuples; no dynamics, RG, or continuum/quantum assertion",
        "counts": {"rational_seeds": len(seeds), "matrix_product_comparisons": len(seeds)**2,
                   "associativity_and_matrix_triples": len(seeds)**3,
                   "joint_product_updates": update_count, "cross_Gram_minor_identities": minor_count,
                   "coarse_fiber_recovery_and_energy_controls": (len(seeds)+2)*(len(seeds)+1)},
        "pair_local_trace_obstruction": {"individual_scalars": [u[0], u[0]],
                                         "joined_scalar_endpoints": [w_low, w_high]},
        "triple_orientation_obstruction": {"plus": plus, "minus": minus, "scalars": ap,
                                           "Gram": gp, "pair_product_scalars": pairs_plus,
                                           "oriented_triples": [tp[0][1][2], tm[0][1][2]],
                                           "ordered_product_scalars": [triple_plus, triple_minus]},
        "coarse_energy_obstruction": {"outer": outer, "U_A": ua, "V_A": va,
                                      "U_B": ub, "V_B": vb,
                                      "fine_shape_sum": [fine_a, fine_b],
                                      "coarse_shape_term": 1-outer[0],
                                      "both_pairs_noncommuting": True,
                                      "complete_fine_sum_fiber": "[2-sqrt(2+2*w0),2+sqrt(2+2*w0)]"},
        "integer_power_not_join_homomorphism": {"U": i, "V": j,
                                                "U_squared_V_squared": powers_first,
                                                "UV_squared": product_first},
        "hostile_controls": ["out-of-image pair dot rejected", "central endpoint forces zero dot",
                             "out-of-domain scalar rejected", "improper reflection preserves pairs but changes triples",
                             "rank-zero through rank-three product replacements checked",
                             "full outer holonomy does not determine fine magnetic sum",
                             "W=-I fixes fine sum while source pair remains nonunique"],
    }
    target = Path(__file__).with_name("RESULTS_STATIC.json")
    payload = json.dumps(serial(result), indent=2) + "\n"
    if args.write_results:
        target.write_text(payload, encoding="utf-8")
    else:
        assert target.read_text(encoding="utf-8") == payload, "Saved static receipt differs from recomputed results"
    print(json.dumps({"status": "PASS", "receipt": str(target),
                      "receipt_action": "written" if args.write_results else "compared_without_writing",
                      "counts": result["counts"]}, indent=2))


if __name__ == "__main__":
    main()
