"""Exact finite full-link checks for the regular two-square phase chart.

Standard library only; no numerical integration or external installations.
This checker is independent of the adjacent dynamics/static checker modules.
"""

from fractions import Fraction as F
from pathlib import Path
import argparse
import json


ZERO = (F(0),) * 4
ONE = (F(1), F(0), F(0), F(0))
AXES = tuple(tuple(F(int(i == j)) for i in range(4)) for j in (1, 2, 3))
EDGES = ("a", "b", "c", "d", "l", "s", "r")
ENDS = {"a": ("A", "B"), "b": ("B", "C"), "c": ("D", "E"),
        "d": ("E", "F"), "l": ("A", "D"), "s": ("B", "E"),
        "r": ("C", "F")}
WORDS = (
    (("s", 1), ("c", -1), ("l", -1), ("a", 1)),
    (("b", 1), ("r", 1), ("d", -1), ("s", -1)),
    (("b", 1), ("r", 1), ("d", -1), ("c", -1), ("l", -1), ("a", 1)),
)


def add(*qs):
    return tuple(sum(q[k] for q in qs) for k in range(4))


def scale(q, c):
    return tuple(c * z for z in q)


def dot(u, v):
    return sum(x * y for x, y in zip(u, v))


def cross(u, v):
    return (u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0])


def mul(q, r):
    a, u, b, v = q[0], q[1:], r[0], r[1:]
    c = cross(u, v)
    return (a*b-dot(u, v),) + tuple(a*v[k]+b*u[k]-c[k] for k in range(3))


def conj(q):
    return (q[0],) + tuple(-z for z in q[1:])


def adj(q, e):
    return mul(mul(q, (F(0),)+tuple(e)), conj(q))[1:]


def stereographic(v):
    v = tuple(F(z) for z in v)
    n = dot(v, v)
    return ((1-n)/(1+n),) + tuple(2*z/(1+n) for z in v)


def jmul(q, r):
    return tuple(add(*(mul(q[j], r[k-j]) for j in range(k+1))) for k in range(3))


def word_jet(links, word, first=None, second=None):
    first, second = first or {}, second or {}
    result = (ONE, ZERO, ZERO)
    for edge, sign in word:
        factor = (links[edge], first.get(edge, ZERO), second.get(edge, ZERO))
        if sign == -1:
            factor = tuple(conj(q) for q in factor)
        result = jmul(result, factor)
    return tuple(q[0] for q in result)


def readout(links):
    return tuple(word_jet(links, word)[0] for word in WORDS)


def jacobian(links):
    return tuple(tuple(word_jet(links, word, {e: mul(axis, links[e])})[1]
                       for e in EDGES for axis in AXES) for word in WORDS)


def transpose_product(j):
    return tuple(tuple(dot(row, other) for other in j) for row in j)


def metric(x):
    a, b, w = x
    return ((4*(1-a*a), w-a*b, 3*(b-a*w)),
            (w-a*b, 4*(1-b*b), 3*(a-b*w)),
            (3*(b-a*w), 3*(a-b*w), 6*(1-w*w)))


def delta(x):
    a, b, w = x
    return 1-a*a-b*b-w*w+2*a*b*w


def matvec(m, v):
    return tuple(dot(row, v) for row in m)


def determinant(m):
    return (m[0][0]*(m[1][1]*m[2][2]-m[1][2]*m[2][1])
            -m[0][1]*(m[1][0]*m[2][2]-m[1][2]*m[2][0])
            +m[0][2]*(m[1][0]*m[2][1]-m[1][1]*m[2][0]))


def metric_rate(x, dx):
    a, b, w = x
    da, db, dw = dx
    ab = dw-da*b-a*db
    aw = 3*(db-da*w-a*dw)
    bw = 3*(da-db*w-b*dw)
    return ((-8*a*da, ab, aw), (ab, -8*b*db, bw), (aw, bw, -12*w*dw))


def momentum_rate(x, p):
    a, b, w = x
    r, s, t = p
    return (4*a*r*r+b*r*s+3*w*r*t-3*s*t+1,
            4*b*s*s+a*r*s-3*r*t+3*w*s*t+1,
            6*w*t*t-r*s+3*a*r*t+3*b*s*t)


def lift(j, p):
    flat = tuple(sum(j[i][k]*p[i] for i in range(3)) for k in range(21))
    return {e: flat[3*k:3*k+3] for k, e in enumerate(EDGES)}


def gauss(links, electric):
    g = {v: [F(0)]*3 for v in "ABCDEF"}
    for e, (source, target) in ENDS.items():
        back = adj(conj(links[e]), electric[e])
        for k in range(3):
            g[source][k] += electric[e][k]
            g[target][k] -= back[k]
    return g


def gauge_links(links, h):
    return {e: mul(mul(h[s], links[e]), conj(h[t])) for e, (s, t) in ENDS.items()}


def tree_links(u, v):
    links = dict.fromkeys(EDGES, ONE)
    links["c"], links["d"] = conj(u), conj(v)
    return links


def regular_check(name, links, p):
    assert all(dot(q, q) == 1 for q in links.values())
    x, j = readout(links), jacobian(links)
    assert delta(x) > 0
    m = metric(x)
    assert transpose_product(j) == m, (name, "cometric")
    a, b, w = x
    assert determinant(m) == 6*delta(x)*(16-6*a*a-6*b*b-w*w-3*a*b*w)
    electric = lift(j, p)
    assert all(z == 0 for row in gauss(links, electric).values() for z in row)
    flat = tuple(z for e in EDGES for z in electric[e])
    kinetic = dot(flat, flat)/2
    assert kinetic == dot(p, matvec(m, p))/2
    dq = {e: mul((F(0),)+electric[e], links[e]) for e in EDGES}
    # H=E^2/2+2-a-b: left-trivial E_dot=grad a+grad b.
    de = lift(j, (F(1), F(1), F(0)))
    ddq_half = {e: scale(add(mul((F(0),)+de[e], links[e]),
                              mul((F(0),)+electric[e], dq[e])), F(1, 2)) for e in EDGES}
    source_jets = tuple(word_jet(links, word, dq, ddq_half) for word in WORDS)
    dx = matvec(m, p)
    assert tuple(jet[1] for jet in source_jets) == dx
    dp = momentum_rate(x, p)
    acceleration = tuple(a+b for a, b in zip(matvec(metric_rate(x, dx), p), matvec(m, dp)))
    assert tuple(2*jet[2] for jet in source_jets) == acceleration, (name, "acceleration")
    return {"name": name, "x": x, "p": p, "delta": delta(x), "kinetic": kinetic,
            "velocity": dx, "acceleration": acceleration, "passed": True}


class Poly:
    """Tiny exact sparse polynomial ring for an identity, independent of samples."""
    def __init__(self, value=0):
        self.terms = value if isinstance(value, dict) else ({(0, 0, 0): F(value)} if value else {})

    def __add__(self, other):
        other = other if isinstance(other, Poly) else Poly(other)
        terms = dict(self.terms)
        for k, v in other.terms.items():
            terms[k] = terms.get(k, 0)+v
        return Poly({k: v for k, v in terms.items() if v})

    __radd__ = __add__

    def __neg__(self):
        return Poly({k: -v for k, v in self.terms.items()})

    def __sub__(self, other):
        return self+-other if isinstance(other, Poly) else self+(-F(other))

    def __rsub__(self, other):
        return -self+other

    def __mul__(self, other):
        other = other if isinstance(other, Poly) else Poly(other)
        result = Poly()
        for ka, va in self.terms.items():
            for kb, vb in other.terms.items():
                result += Poly({tuple(a+b for a, b in zip(ka, kb)): va*vb})
        return result

    __rmul__ = __mul__


def polynomial_check():
    a, b, w = (Poly({tuple(int(i == k) for i in range(3)): F(1)}) for k in range(3))
    det = determinant(metric((a, b, w)))
    factored = 6*delta((a, b, w))*(16-6*a*a-6*b*b-w*w-3*a*b*w)
    assert not (det-factored).terms
    return {"method": "exact sparse polynomial expansion", "expanded_terms": len(det.terms), "passed": True}


def singular_check():
    links = dict.fromkeys(EDGES, ONE)
    j = jacobian(links)
    assert all(z == 0 for row in j for z in row)
    circulation = {e: (F(0), F(0), F(0)) for e in EDGES}
    for e, sign in (("a", 1), ("s", 1), ("c", -1), ("l", -1)):
        circulation[e] = (F(sign), F(0), F(0))
    assert all(z == 0 for row in gauss(links, circulation).values() for z in row)
    energy = sum(dot(e, e) for e in circulation.values())/2
    assert energy == 2
    assert readout(links) == (F(1),)*3
    assert all(z == 0 for e in lift(j, (F(1), F(2), F(3))).values() for z in e)
    return {"x": (1, 1, 1), "nonzero_gauss_zero_circulation_kinetic": energy,
            "jacobian_rank": 0, "finite_p_lift_misses_state": True, "passed": True}


def boundary_checks():
    u = (F(3, 5), F(4, 5), F(0), F(0))
    cases = (("parallel", u, u), ("antiparallel", u, conj(u)), ("central_left", ONE, u))
    rows = []
    for name, u, v in cases:
        links = tree_links(u, v)
        x, j = readout(links), jacobian(links)
        m = metric(x)
        assert delta(x) == determinant(m) == 0
        assert transpose_product(j) == m
        minors = [m[i][i]*m[k][k]-m[i][k]*m[k][i] for i, k in ((0, 1), (0, 2), (1, 2))]
        assert any(z > 0 for z in minors)
        rows.append({"name": name, "x": x, "cometric_rank": 2, "passed": True})
    return rows


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
    pairs = (
        ((F(3, 5), F(4, 5), F(0), F(0)), (F(3, 5), F(0), F(4, 5), F(0))),
        (stereographic((F(1, 2), F(1, 3), F(1, 4))), stereographic((F(2, 3), F(-1, 5), F(1, 7)))),
    )
    momenta = ((F(0), F(0), F(0)), (F(1), F(-2), F(3)), (F(1, 3), F(2, 5), F(-1, 7)))
    h = {v: stereographic((F(k+1, 9), F(2-k, 7), F(k-3, 11))) for k, v in enumerate("ABCDEF")}
    rows, covariances = [], []
    for index, (u, v) in enumerate(pairs):
        base = tree_links(u, v)
        gauged = gauge_links(base, h)
        assert readout(gauged) == readout(base)
        for k, p in enumerate(momenta):
            e, eg = lift(jacobian(base), p), lift(jacobian(gauged), p)
            assert all(eg[edge] == adj(h[ENDS[edge][0]], e[edge]) for edge in EDGES)
            covariances.append({"configuration": index, "momentum": k, "passed": True})
            for label, links in (("tree", base), ("gauge_transformed", gauged)):
                rows.append(regular_check(f"pair_{index}_momentum_{k}_{label}", links, p))
    result = {"scope": "finite exact full-seven-link tests and one polynomial identity; no trajectory simulation",
              "conventions": {"pauli": "+i, minus cross", "edge_order": EDGES,
                              "words": WORDS, "kinetic": "sum E_edge_alpha^2 / 2"},
              "polynomial_determinant": polynomial_check(), "regular_cases": rows,
              "gauge_covariance_cases": covariances, "boundary_cases": boundary_checks(),
              "singular_hostile_case": singular_check(), "all_passed": True}
    target = Path(__file__).with_name("RESULTS_PHASE.json")
    payload = json.dumps(serial(result), indent=2)+"\n"
    if args.write_results:
        target.write_text(payload, encoding="utf-8")
    else:
        assert target.read_text(encoding="utf-8") == payload, "Saved phase receipt differs from recomputed results"
    action = "written" if args.write_results else "compared_without_writing"
    print(f"PASS: {len(rows)} regular full-link cases, {len(covariances)} gauge-covariance cases, "
          f"3 rank-two boundary cases, singular hostile case, exact polynomial determinant identity.\n"
          f"Receipt {action}: {target}")


if __name__ == "__main__":
    main()
