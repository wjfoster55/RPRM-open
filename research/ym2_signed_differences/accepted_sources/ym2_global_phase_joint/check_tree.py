"""Exact finite full-graph checks for the global tree phase carrier.

Independent standard-library implementation; imports no adjacent checker.
Default recomputes and compares the receipt without writing it. No integration.
"""

from fractions import Fraction as F
from pathlib import Path
import argparse
import json

if not __debug__:
    raise RuntimeError("This checker requires assertions; run without -O or -OO.")

Z3 = (F(0),) * 3
Z4 = (F(0),) * 4
I = (F(1), F(0), F(0), F(0))
AXES = tuple(tuple(F(i == j) for i in range(3)) for j in range(3))
EDGES = ("a", "b", "c", "d", "l", "s", "r")
ENDS = {"a": ("A", "B"), "b": ("B", "C"), "c": ("D", "E"),
        "d": ("E", "F"), "l": ("A", "D"), "s": ("B", "E"),
        "r": ("C", "F")}
WORDS = ((("s", 1), ("c", -1), ("l", -1), ("a", 1)),
         (("b", 1), ("r", 1), ("d", -1), ("s", -1)),
         (("b", 1), ("r", 1), ("d", -1), ("c", -1), ("l", -1), ("a", 1)))


def add(a, b):
    return tuple(x+y for x, y in zip(a, b))


def scale(a, s):
    return tuple(s*x for x in a)


def sub(a, b):
    return add(a, scale(b, -1))


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def cross(a, b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])


def bracket(a, b):
    return scale(cross(a, b), -2)


def alg(v):
    return (F(0),)+tuple(v)


def mul(q, r):
    a, b, u, v = q[0], r[0], q[1:], r[1:]
    return (a*b-dot(u, v),)+sub(add(scale(v, a), scale(u, b)), cross(u, v))


def inv(q):
    return (q[0],)+scale(q[1:], -1)


def adj(q, v):
    return mul(mul(q, alg(v)), inv(q))[1:]


def stereo(v):
    v = tuple(F(x) for x in v)
    s = dot(v, v)
    return ((1-s)/(1+s),)+scale(v, 2/(1+s))


def jm(q, r):
    """First jets (value, derivative); no finite differences."""
    return (mul(q[0], r[0]), add(mul(q[1], r[0]), mul(q[0], r[1])))


def ji(q):
    return (inv(q[0]), inv(q[1]))


def ja(q, e):
    out = jm(jm(q, (alg(e[0]), alg(e[1]))), ji(q))
    return (out[0][1:], out[1][1:])


def word(links, path):
    value = (I, Z4)
    for edge, sign in path:
        value = jm(value, links[edge] if sign == 1 else ji(links[edge]))
    return value


def tree(u, v):
    links = dict.fromkeys(EDGES, I)
    links.update(c=inv(u), d=inv(v))
    return links


def lift(u, v, p, q):
    s, r = adj(inv(u), p), adj(inv(v), q)
    return {"a": s, "b": q, "c": scale(s, -1), "d": scale(r, -1),
            "l": scale(s, -1), "s": sub(p, r), "r": q}


def gauss(links, electric):
    out = dict.fromkeys("ABCDEF", Z3)
    for edge, (source, target) in ENDS.items():
        out[source] = add(out[source], electric[edge])
        out[target] = sub(out[target], adj(inv(links[edge]), electric[edge]))
    return out


def gamma(u, v, p, q):
    return add(sub(p, adj(inv(u), p)), sub(q, adj(inv(v), q)))


def fix_tree(links, electric):
    """General source-to-tree map, acting on first jets with B fixed.

    Works directly with arbitrary link representatives. Its differentiated
    form supplies a separate full-graph test of the reduced vector field.
    """
    h = {"B": (I, Z4), "A": ji(links["a"]), "C": links["b"], "E": links["s"]}
    h["D"], h["F"] = jm(h["A"], links["l"]), jm(h["C"], links["r"])
    fixed = {e: jm(jm(h[s], links[e]), ji(h[t])) for e, (s, t) in ENDS.items()}
    ef = {e: ja(h[s], electric[e]) for e, (s, _) in ENDS.items()}
    u, v = ji(fixed["c"]), ji(fixed["d"])
    p, q = ja(u, ef["c"]), ja(v, ef["d"])
    p, q = tuple(scale(x, -1) for x in p), tuple(scale(x, -1) for x in q)
    assert all(fixed[e] == (I, Z4) for e in ("a", "b", "l", "s", "r"))
    return u, v, p, q


def jacobian(links):
    rows = []
    for path in WORDS:
        row = []
        for edge in EDGES:
            for axis in AXES:
                jets = {e: (links[e], mul(alg(axis), links[e]) if e == edge else Z4) for e in EDGES}
                row.append(word(jets, path)[1][0])
        rows.append(tuple(row))
    return tuple(rows)


def source_field(links, electric):
    j = jacobian(links)
    dq = {e: mul(alg(electric[e]), links[e]) for e in EDGES}
    de = {e: tuple(j[0][3*k+i]+j[1][3*k+i] for i in range(3)) for k, e in enumerate(EDGES)}
    return dq, de


def reduced_field(u, v, p, q):
    a = sub(scale(p, 4), adj(inv(v), q))
    b = sub(scale(q, 4), adj(v, p))
    return mul(alg(a), u), mul(alg(b), v), sub(bracket(a, p), u[1:]), scale(v[1:], -1)


def hamiltonian(u, v, p, q):
    return 2*(dot(p, p)+dot(q, q))-dot(p, adj(inv(v), q))+2-u[0]-v[0]


def jet_hamiltonian(u, v, p, q):
    r = ja(ji(v), q)
    return (4*(dot(p[0], p[1])+dot(q[0], q[1]))
            -dot(p[1], r[0])-dot(p[0], r[1])-u[1][0]-v[1][0])


def gauge(links, electric, h):
    return ({e: mul(mul(h[s], links[e]), inv(h[t])) for e, (s, t) in ENDS.items()},
            {e: adj(h[s], electric[e]) for e, (s, _) in ENDS.items()})


def bridge(u, v, p):
    r, s, t = p
    return (sub(scale(u[1:], -r), scale(mul(u, v)[1:], t)),
            sub(scale(v[1:], -s), scale(mul(v, u)[1:], t)))


def check_case(name, u, v, p, q):
    assert dot(u, u) == dot(v, v) == 1
    assert gamma(u, v, p, q) == Z3
    links, electric = tree(u, v), lift(u, v, p, q)
    h = {vertex: stereo((F(k+1, 9), F(2-k, 7), F(k-3, 11))) for k, vertex in enumerate("ABCDEF")}
    source_rows = []
    for label, (lk, el) in (("tree", (links, electric)), ("independent_vertex_gauge", gauge(links, electric, h))):
        assert all(g == Z3 for g in gauss(lk, el).values())
        decoded = fix_tree({e: (lk[e], Z4) for e in EDGES}, {e: (el[e], Z3) for e in EDGES})
        uu, vv, pp, qq = (z[0] for z in decoded)
        if label == "tree":
            assert (uu, vv, pp, qq) == (u, v, p, q)
        else:
            assert (uu, vv, pp, qq) == (mul(mul(h["B"], u), inv(h["B"])),
                                      mul(mul(h["B"], v), inv(h["B"])), adj(h["B"], p), adj(h["B"], q))
        dq, de = source_field(lk, el)
        decoded_jets = fix_tree({e: (lk[e], dq[e]) for e in EDGES}, {e: (el[e], de[e]) for e in EDGES})
        actual = tuple(z[1] for z in decoded_jets)
        predicted = reduced_field(uu, vv, pp, qq)
        assert actual == predicted, (name, label, "full-graph vector field")
        assert jet_hamiltonian(*decoded_jets) == 0, (name, label, "energy derivative")
        # Differentiate the residual momentum map independently with jets.
        ub, vb = ja(ji(decoded_jets[0]), decoded_jets[2]), ja(ji(decoded_jets[1]), decoded_jets[3])
        assert add(sub(actual[2], ub[1]), sub(actual[3], vb[1])) == Z3
        kinetic = sum(dot(el[e], el[e]) for e in EDGES)/2
        assert kinetic+2-uu[0]-vv[0] == hamiltonian(uu, vv, pp, qq)
        assert kinetic >= F(3, 2)*(dot(pp, pp)+dot(qq, qq))
        source_rows.append({"representative": label, "vector_field_all_14_components": True,
                            "energy_derivative_zero": True, "gauss_derivative_zero": True})
    # Pull back the full canonical one-form along arbitrary tree tangents
    # and arbitrary infinitesimal vertex gauge tangents.
    x, y = (F(2, 3), F(-3, 5), F(5, 7)), (F(-7, 11), F(11, 13), F(13, 17))
    omega = {vertex: tuple(F((k+1)*(j+2), 7+j+k) for j in range(3)) for k, vertex in enumerate("ABCDEF")}
    tangent = dict.fromkeys(EDGES, Z3)
    tangent["c"], tangent["d"] = scale(adj(inv(u), x), -1), scale(adj(inv(v), y), -1)
    theta = sum(dot(electric[e], tangent[e]) for e in EDGES)
    assert theta == dot(p, x)+dot(q, y)
    for e, (s, t) in ENDS.items():
        tangent[e] = add(tangent[e], sub(omega[s], adj(links[e], omega[t])))
    assert sum(dot(electric[e], tangent[e]) for e in EDGES) == theta
    # The chord definition plus the five non-root Gauss equations uniquely
    # reconstructs every edge. Test that the extraction reverses a lift.
    assert lift(*tuple(z[0] for z in fix_tree({e: (links[e], Z4) for e in EDGES},
                                           {e: (electric[e], Z3) for e in EDGES}))) == electric
    return {"name": name, "traces": (u[0], v[0], mul(u, v)[0]),
            "kinetic": sum(dot(e, e) for e in electric.values())/2,
            "source_checks": source_rows, "canonical_one_form": True, "round_trip": True}


def check_bridge(u, v, oldp):
    p, q = bridge(u, v, oldp)
    links = tree(u, v)
    j = jacobian(links)
    lifted = {e: tuple(sum(oldp[i]*j[i][3*k+n] for i in range(3)) for n in range(3)) for k, e in enumerate(EDGES)}
    assert lifted == lift(u, v, p, q)
    a, b, w = u[0], v[0], mul(u, v)[0]
    m = ((4*(1-a*a), w-a*b, 3*(b-a*w)),
         (w-a*b, 4*(1-b*b), 3*(a-b*w)),
         (3*(b-a*w), 3*(a-b*w), 6*(1-w*w)))
    assert sum(dot(e, e) for e in lifted.values()) == dot(oldp, tuple(dot(row, oldp) for row in m))
    return {"old_p": oldp, "full_link_lift_matches": True, "old_cometric_matches": True}


def serial(obj):
    if isinstance(obj, F):
        return str(obj)
    if isinstance(obj, dict):
        return {k: serial(v) for k, v in obj.items()}
    if isinstance(obj, (tuple, list)):
        return [serial(v) for v in obj]
    return obj


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-results", action="store_true")
    args = parser.parse_args()
    u = (F(3, 5), F(4, 5), F(0), F(0))
    v = (F(3, 5), F(0), F(4, 5), F(0))
    arbitrary = (F(1), F(2), F(3))
    pairs = ((u, v), (stereo((F(1, 2), F(1, 3), F(1, 4))), stereo((F(2, 3), F(-1, 5), F(1, 7)))))
    oldmomenta = (Z3, (F(1), F(-2), F(3)), (F(1, 3), F(2, 5), F(-1, 7)))
    cases, bridges = [], []
    for i, (uu, vv) in enumerate(pairs):
        for k, oldp in enumerate(oldmomenta):
            p, q = bridge(uu, vv, oldp)
            cases.append(check_case(f"regular_{i}_{k}", uu, vv, p, q))
            bridges.append(check_bridge(uu, vv, oldp))
    boundary = (("aligned_transverse_electric", u, u, arbitrary, (F(4), F(-2), F(-3))),
                ("antialigned_transverse_electric", u, inv(u), arbitrary, adj(inv(u), arbitrary)),
                ("central_U", I, v, arbitrary, scale(v[1:], 2)),
                ("central_V", u, I, scale(u[1:], 3), arbitrary),
                ("central_single_circulation", I, I, AXES[0], Z3),
                ("central_two_circulations", I, I, AXES[0], AXES[1]),
                ("negative_central", scale(I, -1), scale(I, -1), arbitrary, AXES[1]),
                ("all_zero_equilibrium", I, I, Z3, Z3))
    cases.extend(check_case(*row) for row in boundary)
    du, dv, dp, dq = reduced_field(I, I, AXES[0], AXES[1])
    cross_coefficient = cross(du[1:], dv[1:])
    assert cross_coefficient == scale(AXES[2], 15)
    assert dot(cross_coefficient, cross_coefficient) == 225
    # The naive two-loop unit kinetic energy demonstrably changes the flow.
    assert reduced_field(I, I, AXES[0], Z3)[0] != mul(alg(AXES[0]), I)
    result = {"scope": "finite exact source vector-field and one-form checks; no time integration",
              "conventions": {"pauli": "+i sigma, minus cross", "tree": ["a", "b", "l", "s", "r"],
                              "root": "B", "kinetic_source": "sum E_e^2 / 2"},
              "cases": cases, "regular_bridge_cases": bridges,
              "central_exit": {"P": AXES[0], "Q": AXES[1], "cross_t2": cross_coefficient,
                               "Delta_t4": 225, "energy": 4},
              "naive_two_chord_metric_rejected": True, "all_passed": True}
    target = Path(__file__).with_name("RESULTS_TREE.json")
    payload = json.dumps(serial(result), indent=2)+"\n"
    if args.write_results:
        target.write_text(payload, encoding="utf-8")
    else:
        assert target.read_text(encoding="utf-8") == payload, "Tree receipt differs from recomputation"
    print(f"PASS: {len(cases)} phase cases in 2 representatives each; {len(bridges)} regular bridges; "
          "central exit coefficient 225; naive metric rejected.\n"
          f"Receipt {'written' if args.write_results else 'compared_without_writing'}: {target}")


if __name__ == "__main__":
    main()
