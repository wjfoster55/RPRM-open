"""Exact four-state projection checks; Python standard library only.

Default execution recomputes and compares the deterministic receipt.
--write-results explicitly writes the receipt. Conditions use no asserts.
This finite checker does not verify the general Hilbert-space or SU(2) proofs.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
import hashlib
import itertools
import json
from pathlib import Path


STATES = list(itertools.product((-1, 1), repeat=2))
N = len(STATES)


def require(condition, label):
    if not condition:
        raise RuntimeError(label)


def eye():
    return [[F(i == j) for j in range(N)] for i in range(N)]


def add(a, b):
    return [[x + y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def scale(c, a):
    return [[c * x for x in ar] for ar in a]


def sub(a, b):
    return add(a, scale(-1, b))


def transpose(a):
    return [list(row) for row in zip(*a)]


def mul(a, b):
    bt = transpose(b)
    return [[sum((x*y for x, y in zip(ar, bc)), F(0))
             for bc in bt] for ar in a]


def mv(a, v):
    return [sum((x*y for x, y in zip(row, v)), F(0)) for row in a]


def power(a, n):
    out = eye()
    for _ in range(n):
        out = mul(out, a)
    return out


def determinant(a):
    b = [row[:] for row in a]
    out = F(1)
    for j in range(N):
        pivots = [i for i in range(j, N) if b[i][j]]
        if not pivots:
            return F(0)
        p = pivots[0]
        if p != j:
            b[p], b[j] = b[j], b[p]
            out = -out
        pivot = b[j][j]
        out *= pivot
        for i in range(j + 1, N):
            factor = b[i][j] / pivot
            b[i] = [x - factor*y for x, y in zip(b[i], b[j])]
    return out


def conditional(weights, retained_values):
    """Rows act on observables; condition on equality of the retained port."""
    return [[weights[j] / sum(weights[k] for k in range(N)
                             if retained_values[k] == retained_values[i])
             if retained_values[j] == retained_values[i] else F(0)
             for j in range(N)] for i in range(N)]


def edge_form(weights, p):
    """Matrix of (1/2) E[(f(Q)-f(Q'))^2] for a conditional refresh."""
    out = [[F(0) for _ in range(N)] for _ in range(N)]
    for i in range(N):
        for j in range(N):
            c = weights[i]*p[i][j]/2
            out[i][i] += c
            out[j][j] += c
            out[i][j] -= c
            out[j][i] -= c
    return out


def weighted_inner(weights, u, v):
    return sum((p*x*y for p, x, y in zip(weights, u, v)), F(0))


def variance(weights, v):
    mean = sum((p*x for p, x in zip(weights, v)), F(0))
    return weighted_inner(weights, v, v)-mean**2


def vvadd(a, b):
    return [x+y for x, y in zip(a, b)]


def vvscale(c, a):
    return [c*x for x in a]


def serial(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {str(k): serial(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [serial(x) for x in value]
    return value


def check_rho(rho):
    require(-1 < rho < 1, "rho admission")
    weights = [(1+rho*x*y)/4 for x, y in STATES]
    w = [[weights[i] if i == j else F(0) for j in range(N)]
         for i in range(N)]
    ident = eye()
    zero = scale(0, ident)
    one = [F(1)]*N
    x = [F(s[0]) for s in STATES]
    y = [F(s[1]) for s in STATES]
    plus, minus = vvadd(x, y), vvadd(x, vvscale(-1, y))
    interaction = [a*b-rho for a, b in STATES]
    px, py = conditional(weights, y), conditional(weights, x)
    rx, ry = sub(ident, px), sub(ident, py)
    a = add(rx, ry)
    j = [weights[:] for _ in range(N)]
    center = sub(ident, j)
    k = scale(F(1, 2), add(px, py))
    sweep = mul(px, py)
    sweep0 = sub(sweep, j)
    basis = transpose([one, plus, minus, interaction])
    eigs = [F(0), 1-rho, 1+rho, F(2)]
    checks = []

    def eq(left, right, label):
        require(left == right, f"rho={rho}: {label}")
        checks.append(label)

    eq(sum(weights), F(1), "probability normalization")
    require(all(p > 0 for p in weights), "strict full support")
    for label, p, r in (("x", px, rx), ("y", py, ry)):
        eq(mv(p, one), one, label+": preserves constants")
        eq(mul(p, p), p, label+": conditional projection idempotent")
        eq(mul(transpose(p), w), mul(w, p), label+": weighted self-adjoint")
        eq(mul(r, r), r, label+": residual projection idempotent")
        eq(mul(p, r), zero, label+": expectation residual orthogonal")
        eq(mul(transpose(r), mul(w, r)), mul(w, r),
           label+": residual squared norm equals quadratic form")
        eq(edge_form(weights, p), mul(w, r),
           label+": pairwise signed difference form")
        eq(mul(r, center), r, label+": centering leaves residual unchanged")
        eq(mul(r, j), zero, label+": constant offsets killed")
        require(r != ident, label+": residual is not identity")
    eq(mul(w, a), add(mul(transpose(rx), mul(w, rx)),
                     mul(transpose(ry), mul(w, ry))),
       "stacked residual Gram matrix equals weighted A")
    require(determinant(basis) != 0, "complete eigenbasis")
    gram = mul(transpose(basis), mul(w, basis))
    expected_norms = [F(1), 2*(1+rho), 2*(1-rho), 1-rho**2]
    eq(gram, [[expected_norms[i] if i == z else F(0)
               for z in range(N)] for i in range(N)],
       "complete weighted orthogonal eigenbasis")
    for v, eigen in zip(transpose(basis), eigs):
        eq(mv(a, v), vvscale(eigen, v), f"A eigenvector at {eigen}")
        eq(mv(k, v), vvscale(1-eigen/2, v), f"K eigenvector from A at {eigen}")
    eq(k, sub(ident, scale(F(1, 2), a)), "K=I-A/2")
    delta = 1-abs(rho)
    sharp_vector = plus if rho >= 0 else minus
    energy = weighted_inner(weights, sharp_vector, mv(a, sharp_vector))
    eq(variance(weights, sharp_vector)/energy, 1/delta,
       "sharp variance-to-residual ratio attained")
    eq(variance(weights, plus), 2*(1+rho), "joint sum variance")
    eq(weighted_inner(weights, plus, mv(a, plus)), 2*(1-rho**2),
       "joint sum residual energy")
    eq(variance(weights, plus), variance(weights, vvscale(-1, plus)),
       "negation preserves variance")
    eq(weighted_inner(weights, plus, mv(a, plus)),
       weighted_inner(weights, vvscale(-1, plus), mv(a, vvscale(-1, plus))),
       "negation preserves residual energy")
    shifted = vvadd(plus, [F(7, 3)]*N)
    eq(variance(weights, plus), variance(weights, shifted),
       "affine centering preserves variance")
    eq(mv(a, plus), mv(a, shifted), "affine centering preserves A readout")
    eq(mul(scale(-1, ident), scale(-1, ident)), ident,
       "double negation is identity unlike residual idempotence")
    eq(mul(sweep0, sweep0), scale(rho**2, sweep0),
       "centered systematic sweep minimal identity")
    eq(mul(transpose(sweep0), mul(w, sweep0)),
       mul(w, scale(rho**2, sub(py, j))),
       "sweep adjoint product gives exact norm abs(rho)")
    for n in (1, 2, 3, 5):
        eq(sub(power(sweep, n), j), scale(rho**(2*(n-1)), sweep0),
           f"systematic sweep exact power n={n}")
        expected = mul(basis, [[(1-eigs[i]/2)**n if i == z else F(0)
                               for z in range(N)] for i in range(N)])
        eq(mul(power(k, n), basis), expected, f"random refresh exact power n={n}")
    eq(mv(mul(rx, ry), interaction), interaction,
       "alternating residuals retain interaction rather than mix all modes")
    commutator = sub(mul(rx, ry), mul(ry, rx))
    eq(commutator == zero, rho == 0, "residual order commutes exactly at rho=0")

    # Exact source coordinate change is invertible, but the new coordinate
    # refresh rule is a different operation and has a nonconstant invariant.
    sd = [(p, d) for p, d in zip(plus, minus)]
    eq([((s+d)/2, (s-d)/2) for s, d in sd], STATES,
       "sum-difference coordinate change exact inverse")
    require(minus[0] == minus[3] and plus[0] != plus[3],
            "difference alone loses joint-sum receiver")
    ps = conditional(weights, minus)  # refresh s, hold d
    pd = conditional(weights, plus)   # refresh d, hold s
    anew = sub(scale(2, ident), add(ps, pd))
    component = [F(s == 0) for s in plus]
    component_mean = sum(p*v for p, v in zip(weights, component))
    component0 = [v-component_mean for v in component]
    require(variance(weights, component0) > 0, "new update invariant nonconstant")
    eq(mv(anew, component0), [F(0)]*N,
       "new coordinate refresh disconnects sum/difference carrier")
    require(anew != a, "new refresh is not conjugated old refresh")
    return serial({
        "rho": rho, "weights": weights,
        "matrices": {"W": w, "P_x": px, "P_y": py, "R_x": rx,
                     "R_y": ry, "A": a, "J": j, "K": k,
                     "systematic_sweep": sweep, "residual_commutator": commutator,
                     "new_coordinate_P_s": ps, "new_coordinate_P_d": pd,
                     "new_coordinate_A": anew},
        "eigenbasis_columns": basis, "eigenbasis_gram": gram,
        "A_spectrum": eigs, "sharp_C_mix": 1/delta,
        "random_refresh_mean_zero_norm": (1+abs(rho))/2,
        "sweep_mean_zero_norm": abs(rho),
        "sweep_mean_zero_spectral_radius": rho**2,
        "new_coordinate_invariant_mean_zero": component0,
        "checks": checks, "check_count": len(checks),
    })


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-results", action="store_true")
    args = parser.parse_args()
    this = Path(__file__).resolve()
    target = this.with_name("RESULTS_DIFFERENCES.json")
    values = [F(-99, 100), F(-3, 4), F(-1, 2), F(0),
              F(1, 2), F(3, 4), F(99, 100)]
    rows = [check_rho(rho) for rho in values]
    binary = [F(0), F(1)]
    centered = [v-F(1, 2) for v in binary]
    twice_centered = [v-F(1, 2) for v in centered]
    require(centered == [F(-1, 2), F(1, 2)], "binary half centering")
    require(twice_centered != binary, "repeated centering is not double negation")
    require((centered[0], centered[0]) == (F(-1, 2), F(-1, 2)),
            "equal half coordinates remain two occurrences")
    result = {
        "schema": "ym2-signed-differences-exact-v1",
        "evidence_grade": "exact rational finite matrix checks; analytic proofs separate",
        "source_sha256": hashlib.sha256(this.read_bytes()).hexdigest(),
        "states": STATES,
        "rho_contract": "-1 < rho < 1; seven exact rational instances, no sampling",
        "rows": rows,
        "centering_controls": serial({"binary": binary, "centered": centered,
                                       "twice_centered": twice_centered,
                                       "equal_occurrences": [centered[0], centered[0]]}),
        "analytic_claims_not_checked": ["gauge equivariance on SU(2) links",
                                        "general two-projection norm theorem",
                                        "actual vacuum correlation or uniform gap"],
    }
    result = serial(result)
    if args.write_results:
        target.write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
        print(f"Wrote {target.name}: {len(rows)} rational four-state models.")
    else:
        saved = json.loads(target.read_text(encoding="utf-8"))
        require(result == saved, "receipt mismatch; inspect changes before replacing")
        print(f"PASS: {len(rows)} rational four-state models; "
              f"{sum(r['check_count'] for r in rows)} matrix/control checks; "
              "half-centering controls; receipt exact.")


if __name__ == "__main__":
    main()
