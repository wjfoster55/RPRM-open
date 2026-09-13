"""Alternative CM-character orbit, with independently implemented E' group law.

The optional numerical replay imports trace125.py's finite-ring arithmetic only.
It does not import that program's CM orbit, elliptic-curve group law, or trace.
See DIVISION_ORBIT.md for the proof that the weights describe the conjugates.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys


def gaussian_mul(z, w, modulus):
    a, b = z
    c, d = w
    return ((a*c-b*d) % modulus, (a*d+b*c) % modulus)


def legendre17(n):
    r = pow(n % 17, 8, 17)
    assert r in (0, 1, 16)
    return -1 if r == 16 else r


def finite_admission():
    units = [(a, b) for a in range(17) for b in range(17)
             if (a*a+b*b) % 17]
    primary68 = [(a, b) for a in range(68) for b in range(68)
                 if a % 2 == 1 and b % 2 == 0 and (a+b) % 4 == 1
                 and (a*a+b*b) % 17]
    fibers = {u: [] for u in units}
    for a, b in primary68:
        fibers[a % 17, b % 17].append((a, b))
    assert len(units) == 256
    assert len(primary68) == 512
    assert {len(v) for v in fibers.values()} == {2}
    weights = {z: legendre17(z[0]**2+z[1]**2) for z in units}
    for z in units:
        for w in units:
            assert weights[gaussian_mul(z, w, 17)] == weights[z]*weights[w]
    assert sum(weights.values()) == 0
    # R is primitive precisely when neither split Gaussian prime kills R.
    assert (4*4+1) == 17
    assert [a for a in range(17) if (a*a+1) % 17 == 0] == [4, 13]
    return {
        "gaussian_units_mod17": len(units),
        "primary_ray_representatives_mod68": len(primary68),
        "lifts_per_mod17_unit": 2,
        "positive_character_weights": sum(w == 1 for w in weights.values()),
        "negative_character_weights": sum(w == -1 for w in weights.values()),
        "character_multiplicativity_pairs": len(units)**2,
        "split_prime_norms": [17, 17],
        "conjugates": 256,
    }


class Curve289:
    """Affine E': y²=x³+289x. Every used inverse must be a ring unit."""

    def __init__(self, sqrt_minus_one):
        self.i = sqrt_minus_one

    @staticmethod
    def neg(P):
        return None if P is None else (P[0], -P[1])

    def add(self, P, Q):
        if P is None:
            return Q
        if Q is None:
            return P
        x, y = P
        u, v = Q
        if x == u:
            if y == -v:
                return None
            assert y == v
            m = (3*x*x+289)/(2*y)
        else:
            m = (v-y)/(u-x)
        z = m*m-x-u
        return (z, m*(x-z)-y)

    def mul(self, n, P):
        if n < 0:
            return self.mul(-n, self.neg(P))
        Q = None
        while n:
            if n & 1:
                Q = self.add(Q, P)
            n >>= 1
            if n:
                P = self.add(P, P)
        return Q

    def cm(self, a, b, P):
        if P is None:
            return None
        iP = (-P[0], self.i*P[1])
        return self.add(self.mul(a, P), self.mul(b, iP))

    @staticmethod
    def on_curve(P):
        return P is None or P[1]*P[1] == P[0]**3+289*P[0]

    @staticmethod
    def intercept(P, Q):
        assert P is not None and Q is not None and P[0] != Q[0]
        return (P[1]*Q[0]-Q[1]*P[0])/(Q[0]-P[0])

    def g(self, T, R):
        U = self.add(T, R)
        return self.intercept(U, R)/self.intercept(T, R)


def chord_trace(curve, T, R, sqrt17):
    """Return the 256-conjugate trace plus all exact orbit checks."""
    assert sqrt17*sqrt17 == 17
    assert curve.on_curve(T) and curve.on_curve(R)
    assert T[0] == 17
    assert curve.mul(4, T) is None and curve.mul(2, T) is not None
    assert curve.mul(17, R) is None
    assert curve.cm(4, 1, R) is not None
    assert curve.cm(4, -1, R) is not None
    multiples = [curve.mul(j, R) for j in range(17)]
    i_multiples = [curve.cm(0, 1, S) for S in multiples]
    total = 0*sqrt17
    conjugates = []
    primitive_points = []
    chord_checks = 0
    for a in range(17):
        for b in range(17):
            weight = legendre17(a*a+b*b)
            if not weight:
                continue
            S = curve.add(multiples[a], i_multiples[b])
            assert S is not None and curve.on_curve(S)
            primitive_points.append(S)
            g = curve.g(T, S)
            rho = weight*sqrt17*g
            Q = curve.add(T, curve.mul(2, S))
            assert Q is not None and rho*rho == Q[0]
            assert curve.g(curve.neg(T), curve.neg(S)) == g
            chord_checks += 1
            conjugates.append(rho)
            total += 2*rho**5+289*rho
    # The assertions below compare exact finite-ring values, not decimals.
    encode = lambda z: repr(z)
    assert len({(encode(P[0]), encode(P[1])) for P in primitive_points}) == 256
    assert len({encode(z*z) for z in conjugates}) == 256
    return total, {
        "primitive_points_checked": len(primitive_points),
        "distinct_squared_conjugates": len(conjugates),
        "chord_square_and_simultaneous_negation_checks": chord_checks,
    }


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def field_admission(F):
    """Rabin irreducibility, rechecked without reading a saved certificate."""
    def trim(a):
        while a and a[-1] == 0:
            a.pop()
        return a

    def remainder(a, b):
        a = trim(a[:])
        b = trim(b[:])
        assert b
        while len(a) >= len(b):
            shift = len(a)-len(b)
            c = a[-1]*pow(b[-1], -1, 5) % 5
            for j, v in enumerate(b):
                a[j+shift] = (a[j+shift]-c*v) % 5
            trim(a)
        return a

    z = F([0, 1], 5)
    assert z**(5**16) == z
    p = [3]+[0]*15+[1]
    q = list((z**(5**8)-z).c)
    while trim(q):
        p, q = q, remainder(p, q)
    assert len(trim(p)) == 1
    return {"polynomial": "z^16-2", "coefficient_prime": 5,
            "rabin_degree": 16, "z_to_5_power_16_equals_z": True,
            "gcd_degree_at_5_power_8": 0,
            "saved_certificate_used": False}


def numerical_replay(root):
    """Use input point as a witness, never trust the input's PASS or trace."""
    backend_path = root/"work"/"trace125.py"
    action_path = root/"work"/"cm_action.py"
    input_path = root/"evidence"/"trace125.json"
    # trace125 imports cm_action, but this replay calls neither its CM action
    # nor its group law. Only the exact F coefficient arithmetic is shared.
    load_module("cm_action", action_path)
    backend = load_module("division_orbit_field_backend", backend_path)
    F = backend.F
    field_checks = field_admission(F)
    witness = json.loads(input_path.read_text(encoding="utf-8"))
    X, Y = [F(c, 125) for c in witness["lifted_point"]]
    assert Y*Y == X**3-1156*X
    i = F(57)
    assert i*i == -1
    curve = Curve289(i)
    # Dual two-isogeny, followed by scaling the +4624 model by (4,8).
    P = ((X-1156/X)/4, Y*(1+1156/(X*X))/8)
    assert curve.on_curve(P)
    T = curve.mul(17, P)
    assert T is not None and T[0] in (F(17), F(-17))
    normalized_by_i = T[0] == -17
    if normalized_by_i:
        P = curve.cm(0, 1, P)
        T = curve.mul(17, P)
    assert T[0] == 17
    R = curve.mul(9, curve.add(P, curve.neg(T)))
    assert curve.add(T, curve.mul(2, R)) == P
    s = F([0]*8+[1])  # z^8 squares to 2, congruent to 17 modulo 5.
    for _ in range(2):
        s = s+(17-s*s)/(2*s)
    assert s*s == 17
    value, checks = chord_trace(curve, T, R, s)
    assert not any(value.c[1:]), "Trace must lie in the selected base K completion"
    residue = value.c[0]
    valuation = 0
    remaining = residue
    while remaining and remaining % 5 == 0:
        valuation += 1
        remaining //= 5
    assert residue % 25 == 0 and residue % 125 != 0
    assert valuation == 2
    return {
        "numerical_trace_status": "EXACT_CHARACTER_ORBIT_TRACE_RESIDUE_COMPUTED",
        "trace_mod125_up_to_global_sign": residue,
        "trace_coefficients": list(value.c),
        "v5_trace": valuation,
        "fresh_field_certificate": field_checks,
        "normalized_input_by_cm_i": normalized_by_i,
        "sqrt17_coefficients": list(s.c),
        "lambda3_component": [list(c.c) for c in T],
        "primitive17_component": [list(c.c) for c in R],
        "checks": checks,
        "attributed_shared_arithmetic": {
            "path": "work/trace125.py",
            "sha256": sha256(backend_path),
            "used_api": "F coefficient arithmetic only",
            "group_law_and_trace_independent": True,
            "field_arithmetic_independent": False,
        },
        "point_witness_input": {
            "path": "evidence/trace125.json",
            "sha256": sha256(input_path),
            "used_fields": ["lifted_point"],
            "saved_status_and_trace_used": False,
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--admission-only", action="store_true")
    parser.add_argument("--output", type=Path,
                        default=Path(__file__).resolve().parents[1]/"evidence"/"division_orbit.json")
    args = parser.parse_args()
    result = {
        "scope": "E34 p=5, alternative character-weighted CM division orbit",
        "finite_admission": finite_admission(),
        "written_proof": "../DIVISION_ORBIT.md",
        "numerical_trace_status": "OPEN: finite-ring replay not yet attached",
        "trace_mod125_up_to_global_sign": None,
        "v5_trace": None,
        "source_sha256": sha256(Path(__file__)),
    }
    if not args.admission_only:
        result.update(numerical_replay(Path(__file__).resolve().parents[1]))
    args.output.write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
