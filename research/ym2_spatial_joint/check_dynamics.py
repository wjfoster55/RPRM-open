#!/usr/bin/env python3
"""Exact finite checks for DYNAMICS.md; standard library only, no integration.

Run: python -I -B research/ym2_spatial_joint/check_dynamics.py
Add --write-results to refresh adjacent RESULTS_DYNAMICS.json.
Quaternion convention: Q(q)=q0 I + i(q1 sigma1+q2 sigma2+q3 sigma3).
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
import json
from pathlib import Path


ZERO = F(0)
ONE = F(1)
I = (ONE, ZERO, ZERO, ZERO)
QZERO = (ZERO,) * 4
BASIS = tuple(tuple(F(int(i == j + 1)) for i in range(4)) for j in range(3))
EDGES = {
    "a": ("A", "B"), "b": ("B", "C"),
    "c": ("D", "E"), "d": ("E", "F"),
    "l": ("A", "D"), "s": ("B", "E"), "r": ("C", "F"),
}
LEFT = (("a", 1), ("s", 1), ("c", -1), ("l", -1))
RIGHT = (("b", 1), ("r", 1), ("d", -1), ("s", -1))
LEFT_AT_B = (("s", 1), ("c", -1), ("l", -1), ("a", 1))
OUTER_AT_B = (("b", 1), ("r", 1), ("d", -1), ("c", -1), ("l", -1), ("a", 1))
PLAQUETTES = (LEFT, RIGHT)


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def neg(a):
    return tuple(-x for x in a)


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), ZERO)


def cross(a, b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])


def mul(a, b):
    # The MINUS cross product is essential for Q=q0 I+i q.sigma.
    av, bv = a[1:], b[1:]
    cv = cross(av, bv)
    return (a[0]*b[0]-dot(av, bv),) + tuple(
        a[0]*bv[j]+b[0]*av[j]-cv[j] for j in range(3)
    )


def inv(q):
    return (q[0],) + neg(q[1:])


def product(qs):
    out = I
    for q in qs:
        out = mul(out, q)
    return out


def loop(links, path):
    return product(links[e] if s == 1 else inv(links[e]) for e, s in path)


def tangent(links, path, edge, axis):
    """d product for the actual full-link path exp(eps*T_axis) U_edge."""
    out = QZERO
    for index, (e, sign) in enumerate(path):
        if e != edge:
            continue
        factors = [links[k] if direction == 1 else inv(links[k]) for k, direction in path]
        factors[index] = (mul(BASIS[axis], links[e]) if sign == 1
                          else neg(mul(inv(links[e]), BASIS[axis])))
        out = add(out, product(factors))
    return out


def gradient(links, plaquettes=PLAQUETTES):
    return {e: tuple(-sum((tangent(links, p, e, j)[0] for p in plaquettes), ZERO)
                     for j in range(3)) for e in EDGES}


def adjoint(q, v):
    result = mul(mul(q, (ZERO,) + tuple(v)), inv(q))
    assert result[0] == 0
    return result[1:]


def gauss(links, electric):
    result = {v: (ZERO,) * 3 for v in "ABCDEF"}
    for e, (source, target) in EDGES.items():
        result[source] = add(result[source], electric[e])
        result[target] = add(result[target], neg(adjoint(inv(links[e]), electric[e])))
    return result


def gauge_transform(links, gauge):
    return {e: mul(mul(gauge[s], links[e]), inv(gauge[t])) for e, (s, t) in EDGES.items()}


def tree_state(u, v):
    result = {e: I for e in EDGES}
    result["c"], result["d"] = inv(u), inv(v)
    return result


# An exact, independent 2x2 complex-matrix implementation. A complex number
# is a pair of Fractions; there is no float or Python complex arithmetic.
CZ = (ZERO, ZERO)
CO = (ONE, ZERO)
MI = ((CO, CZ), (CZ, CO))
MZ = ((CZ, CZ), (CZ, CZ))


def cmul(a, b):
    return (a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0])


def madd(a, b):
    return tuple(tuple(add(a[i][j], b[i][j]) for j in range(2)) for i in range(2))


def mneg(a):
    return tuple(tuple(neg(z) for z in row) for row in a)


def mmul(a, b):
    return tuple(tuple(add(cmul(a[i][0], b[0][j]), cmul(a[i][1], b[1][j]))
                       for j in range(2)) for i in range(2))


def dagger(a):
    return tuple(tuple((a[j][i][0], -a[j][i][1]) for j in range(2)) for i in range(2))


def matrix(q):
    w, x, y, z = q
    return (((w, z), (y, x)), ((-y, x), (w, -z)))


def mproduct(mats):
    out = MI
    for m in mats:
        out = mmul(out, m)
    return out


def matrix_gradient(links, plaquettes=PLAQUETTES):
    mats = {e: matrix(q) for e, q in links.items()}
    result = {}
    for edge in EDGES:
        coords = []
        for axis in range(3):
            total = MZ
            for path in plaquettes:
                for index, (e, sign) in enumerate(path):
                    if e != edge:
                        continue
                    factors = [mats[k] if direction == 1 else dagger(mats[k]) for k, direction in path]
                    factors[index] = (mmul(matrix(BASIS[axis]), mats[e]) if sign == 1
                                      else mneg(mmul(dagger(mats[e]), matrix(BASIS[axis]))))
                    total = madd(total, mproduct(factors))
            trace = add(total[0][0], total[1][1])
            assert trace[1] == 0
            coords.append(-trace[0]/2)
        result[edge] = tuple(coords)
    return result


def state_record(links):
    for q in links.values():
        assert dot(q, q) == 1
        assert mmul(matrix(q), dagger(matrix(q))) == MI
    grad = gradient(links)
    assert grad == matrix_gradient(links)
    assert all(v == (ZERO,) * 3 for v in gauss(links, grad).values())
    u, v = loop(links, LEFT_AT_B), loop(links, RIGHT)
    perimeter = loop(links, OUTER_AT_B)
    assert perimeter == mul(v, u)
    force2 = sum((dot(value, value) for value in grad.values()), ZERO)
    expected = 4*(dot(u[1:], u[1:])+dot(v[1:], v[1:]))-2*dot(u[1:], v[1:])
    assert force2 == expected
    assert grad["s"] == add(u[1:], neg(v[1:]))
    assert force2 == 8-4*u[0]**2-4*v[0]**2-2*u[0]*v[0]+2*perimeter[0]
    return {
        "plaquette_half_traces": [loop(links, p)[0] for p in PLAQUETTES],
        "common_base_dot": dot(u[1:], v[1:]),
        "perimeter_half_trace": perimeter[0],
        "B_initial": 2-u[0]-v[0],
        "B_prime_initial": ZERO,
        "B_second_initial": -force2,
        "gradient_norm_squared": force2,
        "shared_gradient_norm_squared": dot(grad["s"], grad["s"]),
        "per_edge_gradients": grad,
    }


def stringify(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {k: stringify(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [stringify(v) for v in value]
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-results", action="store_true")
    args = parser.parse_args()
    u = (F(3, 5), F(4, 5), ZERO, ZERO)
    va = (F(3, 5), ZERO, F(4, 5), ZERO)
    vb = (F(3, 5), F(12, 25), F(16, 25), ZERO)
    gauge = dict(zip("ABCDEF", (
        u, (F(5, 13), ZERO, F(12, 13), ZERO),
        (F(8, 17), ZERO, ZERO, F(15, 17)), (F(1, 2),)*4,
        (F(7, 25), F(24, 25), ZERO, ZERO), va,
    )))
    assert mmul(matrix(BASIS[0]), matrix(BASIS[1])) == matrix(neg(BASIS[2]))
    states = {"A": tree_state(u, va), "B": tree_state(u, vb)}
    records = {name: state_record(links) for name, links in states.items()}
    assert records["A"]["plaquette_half_traces"] == records["B"]["plaquette_half_traces"]
    assert records["A"]["B_initial"] == records["B"]["B_initial"] == F(4, 5)
    assert records["A"]["B_second_initial"] == F(-128, 25)
    assert records["B"]["B_second_initial"] == F(-544, 125)
    assert records["B"]["B_second_initial"]-records["A"]["B_second_initial"] == F(96, 125)
    assert mul(u, va) != mul(va, u) and mul(u, vb) != mul(vb, u)
    for name, links in states.items():
        reversed_right = tuple((e, -s) for e, s in reversed(RIGHT))
        assert gradient(links, (LEFT, reversed_right)) == gradient(links)
        assert matrix_gradient(links, (LEFT, reversed_right)) == gradient(links)
        moved = gauge_transform(links, gauge)
        moved_record = state_record(moved)
        original_grad, moved_grad = gradient(links), gradient(moved)
        for e, (source, _) in EDGES.items():
            assert moved_grad[e] == adjoint(gauge[source], original_grad[e])
        for field in records[name]:
            if field != "per_edge_gradients":
                assert moved_record[field] == records[name][field]

    # Hostile controls: a central plaquette; aligned and antialigned forces;
    # and a fully three-dimensional quaternion vector at the second loop.
    controls = {
        "central_left": tree_state(I, va),
        "aligned": tree_state(u, u),
        "antialigned": tree_state(u, inv(u)),
        "three_vector_components": tree_state(u, (F(1, 2),)*4),
    }
    control_records = {name: state_record(links) for name, links in controls.items()}
    assert control_records["aligned"]["shared_gradient_norm_squared"] == 0
    assert control_records["antialigned"]["shared_gradient_norm_squared"] == F(64, 25)
    # Deleting tree-link contributions and imposing a naive product kinetic
    # metric on the two chords falsely gives the same curvature for A and B.
    wrong_chord_force2 = dot(u[1:], u[1:])+dot(va[1:], va[1:])
    assert wrong_chord_force2 == dot(u[1:], u[1:])+dot(vb[1:], vb[1:]) == F(32, 25)
    assert wrong_chord_force2 != records["A"]["gradient_norm_squared"]
    output = stringify({
        "status": "PASS",
        "scope": "Exact rational finite lattice derivative checks; no trajectory integration or continuum claim.",
        "convention": "Q=q0 I+i q.sigma; T=i sigma; <X,Y>=-Tr(XY)/2; H=sum|E|^2/2+B",
        "graph": {"vertices": 6, "links": 7, "plaquettes": 2, "boundary": "open/free"},
        "witnesses": {"U": u, "V_A": va, "V_B": vb},
        "results": records,
        "B_second_B_minus_A": F(96, 125),
        "gauge_covariance": {"nonconstant_vertex_transformations": 1, "transformed_witnesses": 2, "all_21_gradient_components_per_state": "PASS"},
        "controls": control_records,
        "checks": [
            "Unit quaternions and exact complex-matrix unitarity for all eight checked configurations",
            "Full seven-link quaternion derivatives equal independent exact 2x2 complex-matrix derivatives",
            "Gauge force obeys the Gauss identity at every vertex for all eight configurations",
            "Common-base shared force difference and all-link norm formula for all eight configurations",
            "Two noncommuting witnesses have equal individual classes and unequal actual initial B second derivative",
            "Nonconstant independent vertex gauge changes preserve observables and transform each link gradient covariantly",
            "Reversing the right plaquette orientation leaves its trace potential and every actual force unchanged",
            "Central, aligned, antialigned, and three-component-vector controls",
            "Naive two-chord unit kinetic metric rejects the required seven-link force norm",
        ],
        "proof_boundary": "The accompanying written derivation proves the finite-model formula. These finite executable checks do not prove their own general soundness, dynamical closure, a continuum limit, or a mass gap.",
    })
    payload = json.dumps(output, indent=2) + "\n"
    if args.write_results:
        Path(__file__).with_name("RESULTS_DYNAMICS.json").write_text(payload, encoding="utf-8")
    print(payload, end="")


if __name__ == "__main__":
    main()
