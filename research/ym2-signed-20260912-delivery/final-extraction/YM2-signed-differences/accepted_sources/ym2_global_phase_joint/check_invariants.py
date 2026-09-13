"""Exact bounded controls for GLOBAL_INVARIANT_JOINT.md; no time stepping.

Only Python's standard library is used. The source route uses explicit
quaternion products. The invariant route carries ten formal coefficients
and uses Gram/triple identities, without reconstructing Cartesian vectors.
Default: recompute and compare the adjacent receipt. --write-results writes it.
"""

from dataclasses import dataclass
from fractions import Fraction as F
from itertools import combinations, permutations
from pathlib import Path
import argparse
import json


@dataclass(frozen=True)
class Dual:
    value: object
    tangent: object = F(0)

    @staticmethod
    def of(x):
        return x if isinstance(x, Dual) else Dual(x)

    def __add__(self, other):
        other = self.of(other)
        return Dual(self.value + other.value, self.tangent + other.tangent)

    __radd__ = __add__

    def __neg__(self):
        return Dual(-self.value, -self.tangent)

    def __sub__(self, other):
        return self + -self.of(other)

    def __rsub__(self, other):
        return self.of(other) + -self

    def __mul__(self, other):
        other = self.of(other)
        return Dual(self.value * other.value,
                    self.tangent * other.value + self.value * other.tangent)

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = self.of(other)
        return Dual(self.value / other.value,
                    (self.tangent * other.value - self.value * other.tangent)
                    / (other.value * other.value))

    def __rtruediv__(self, other):
        return self.of(other) / self


def add(x, y):
    return tuple(a + b for a, b in zip(x, y))


def scale(c, x):
    return tuple(c * a for a in x)


def sub(x, y):
    return add(x, scale(-1, y))


def dot(x, y):
    return sum(a * b for a, b in zip(x, y))


def cross(x, y):
    return (x[1] * y[2] - x[2] * y[1],
            x[2] * y[0] - x[0] * y[2],
            x[0] * y[1] - x[1] * y[0])


def qmul(x, y):
    """Explicit plus-i quaternion product, independent of the compiler."""
    a, b, c, d = x
    e, f, g, h = y
    return (a * e - b * f - c * g - d * h,
            a * f + b * e - c * h + d * g,
            a * g + c * e - d * f + b * h,
            a * h + d * e - b * g + c * f)


def qconj(x):
    return (x[0], -x[1], -x[2], -x[3])


def pure(x):
    return (0,) + tuple(x)


def qadj(q, x):
    return qmul(qmul(q, pure(x)), qconj(q))[1:]


def source_rhs(state):
    U, V, P, Q = state
    A = sub(scale(4, P), qadj(qconj(V), Q))
    B = sub(scale(4, Q), qadj(V, P))
    bracket = sub(qmul(pure(A), pure(P)), qmul(pure(P), pure(A)))[1:]
    return (qmul(pure(A), U), qmul(pure(B), V),
            sub(bracket, U[1:]), scale(-1, V[1:]))


def source_gauss(state):
    U, V, P, Q = state
    return add(sub(P, qadj(qconj(U), P)), sub(Q, qadj(qconj(V), Q)))


def source_energy(state):
    U, V, P, Q = state
    return 2 * (dot(P, P) + dot(Q, Q)) - dot(P, qadj(qconj(V), Q)) + 2 - U[0] - V[0]


TRIPLES = tuple(combinations(range(4), 3))
PAIRS = tuple(combinations(range(4), 2))
BASIS = tuple((i,) for i in range(4)) + PAIRS
BASIS_INDEX = {key: i for i, key in enumerate(BASIS)}


def summarize(state):
    U, V, P, Q = state
    X = (U[1:], V[1:], P, Q)
    return {"a": U[0], "b": V[0],
            "G": tuple(tuple(dot(x, y) for y in X) for x in X),
            "tau": {ijk: dot(cross(X[ijk[0]], X[ijk[1]]), X[ijk[2]])
                    for ijk in TRIPLES}}


def flat(joint):
    return ((joint["a"], joint["b"])
            + tuple(joint["G"][i][j] for i in range(4) for j in range(i, 4))
            + tuple(joint["tau"][ijk] for ijk in TRIPLES))


def unit_coefficient(index):
    return tuple(F(int(i == index)) for i in range(10))


class Compiler:
    """No Cartesian components, ranks, square roots or matrix inverses."""

    def __init__(self, joint):
        self.joint = joint
        self.G = joint["G"]
        self.X = tuple(unit_coefficient(i) for i in range(4))

    def tau(self, i, j, k):
        indices = (i, j, k)
        if len(set(indices)) != 3:
            return F(0)
        inversions = sum(indices[a] > indices[b] for a in range(3) for b in range(a + 1, 3))
        return (-1 if inversions % 2 else 1) * self.joint["tau"][tuple(sorted(indices))]

    def basis_dot(self, left, right):
        if len(left) == len(right) == 1:
            return self.G[left[0]][right[0]]
        if len(left) == 1:
            return self.tau(left[0], *right)
        if len(right) == 1:
            return self.tau(*left, right[0])
        i, j = left
        k, l = right
        return self.G[i][k] * self.G[j][l] - self.G[i][l] * self.G[j][k]

    def basis_cross(self, left, right):
        if len(left) == len(right) == 1:
            i, j = left[0], right[0]
            if i == j:
                return (F(0),) * 10
            return scale(1 if i < j else -1,
                         unit_coefficient(BASIS_INDEX[tuple(sorted((i, j)))]))
        if len(left) == 1:
            i, (j, k) = left[0], right
            return sub(scale(self.G[i][k], self.X[j]), scale(self.G[i][j], self.X[k]))
        if len(right) == 1:
            (i, j), k = left, right[0]
            return sub(scale(self.G[i][k], self.X[j]), scale(self.G[j][k], self.X[i]))
        i, j = left
        k, l = right
        return sub(scale(self.tau(i, j, l), self.X[k]), scale(self.tau(i, j, k), self.X[l]))

    @staticmethod
    def is_zero(x):
        return ((x.value == 0 and x.tangent == 0) if isinstance(x, Dual) else x == 0)

    def dot(self, x, y):
        return sum(a * b * self.basis_dot(BASIS[i], BASIS[j])
                   for i, a in enumerate(x) if not self.is_zero(a)
                   for j, b in enumerate(y) if not self.is_zero(b))

    def cross(self, x, y):
        result = (F(0),) * 10
        for i, a in enumerate(x):
            if self.is_zero(a):
                continue
            for j, b in enumerate(y):
                if not self.is_zero(b):
                    result = add(result, scale(a * b, self.basis_cross(BASIS[i], BASIS[j])))
        return result

    def adj(self, scalar, vector, value, inverse=False):
        return add(add(scale(scalar * scalar - self.dot(vector, vector), value),
                       scale(2 * self.dot(vector, value), vector)),
                   scale((2 if inverse else -2) * scalar, self.cross(vector, value)))

    def gauss(self):
        u, v, P, Q = self.X
        return add(sub(P, self.adj(self.joint["a"], u, P, inverse=True)),
                   sub(Q, self.adj(self.joint["b"], v, Q, inverse=True)))

    def gauss_norm(self):
        gamma = self.gauss()
        return self.dot(gamma, gamma)

    def energy(self):
        _, v, P, Q = self.X
        a, b = self.joint["a"], self.joint["b"]
        return (2 * (self.dot(P, P) + self.dot(Q, Q))
                - self.dot(P, self.adj(b, v, Q, inverse=True)) + 2 - a - b)

    def rhs(self):
        u, v, P, Q = self.X
        a, b = self.joint["a"], self.joint["b"]
        A = sub(scale(4, P), self.adj(b, v, Q, inverse=True))
        B = sub(scale(4, Q), self.adj(b, v, P))
        fields = (sub(scale(a, A), self.cross(A, u)),
                  sub(scale(b, B), self.cross(B, v)),
                  sub(scale(-2, self.cross(A, P)), u), scale(-1, v))
        return {"a": -self.dot(A, u), "b": -self.dot(B, v),
                "G": tuple(tuple(self.dot(fields[i], self.X[j]) + self.dot(self.X[i], fields[j])
                                 for j in range(4)) for i in range(4)),
                "tau": {ijk: (self.dot(self.cross(fields[ijk[0]], self.X[ijk[1]]), self.X[ijk[2]])
                              + self.dot(self.cross(self.X[ijk[0]], fields[ijk[1]]), self.X[ijk[2]])
                              + self.dot(self.cross(self.X[ijk[0]], self.X[ijk[1]]), fields[ijk[2]]))
                        for ijk in TRIPLES}}


def determinant(matrix):
    n = len(matrix)
    result = 0
    for permutation in permutations(range(n)):
        inversions = sum(permutation[i] > permutation[j] for i in range(n) for j in range(i + 1, n))
        term = -1 if inversions % 2 else 1
        for i in range(n):
            term = term * matrix[i][permutation[i]]
        result = result + term
    return result


def minor(G, rows, columns):
    return determinant(tuple(tuple(G[i][j] for j in columns) for i in rows))


def image_failures(joint):
    """Exact rational evaluation of the written real-image criterion."""
    G = joint["G"]
    failures = []
    if any(G[i][j] != G[j][i] for i in range(4) for j in range(4)):
        failures.append("symmetry")
    if any(minor(G, I, I) < 0 for n in range(1, 5) for I in combinations(range(4), n)):
        failures.append("positive_semidefinite")
    if determinant(G) != 0:
        failures.append("rank_at_most_three")
    if G[0][0] + joint["a"] * joint["a"] != 1 or G[1][1] + joint["b"] * joint["b"] != 1:
        failures.append("unit")
    if any(joint["tau"][I] * joint["tau"][J] != minor(G, I, J) for I in TRIPLES for J in TRIPLES):
        failures.append("triple_minor_compatibility")
    if Compiler(joint).gauss_norm() != 0:
        failures.append("zero_gauss")
    return failures


def phase_rank(state):
    X = (state[0][1:], state[1][1:], state[2], state[3])
    if any(dot(cross(X[i], X[j]), X[k]) != 0 for i, j, k in TRIPLES):
        return 3
    if any(dot(cross(X[i], X[j]), cross(X[i], X[j])) != 0 for i, j in PAIRS):
        return 2
    return 1 if any(dot(x, x) != 0 for x in X) else 0


def dual_state(state, tangent):
    return tuple(tuple(Dual(a, b) for a, b in zip(x, y)) for x, y in zip(state, tangent))


def regular_lift(U, V, p):
    r, s, t = p
    return (U, V, sub(scale(-r, U[1:]), scale(t, qmul(U, V)[1:])),
            sub(scale(-s, V[1:]), scale(t, qmul(V, U)[1:])))


def regular_decode(joint):
    a, b = joint["a"], joint["b"]
    w = a * b - joint["G"][0][1]
    rhs = Compiler(joint).rhs()
    velocity = (rhs["a"], rhs["b"], b * rhs["a"] + a * rhs["b"] - rhs["G"][0][1])
    M = ((4 * (1 - a * a), w - a * b, 3 * (b - a * w)),
         (w - a * b, 4 * (1 - b * b), 3 * (a - b * w)),
         (3 * (b - a * w), 3 * (a - b * w), 6 * (1 - w * w)))
    denominator = determinant(M)
    momenta = tuple(determinant(tuple(tuple(velocity[i] if j == k else M[i][j]
                                              for j in range(3)) for i in range(3))) / denominator
                    for k in range(3))
    return (a, b, w), momenta, velocity


def canonical_p_rhs(x, p):
    a, b, w = x
    r, s, t = p
    return (4 * a * r * r + b * r * s + 3 * w * r * t - 3 * s * t + 1,
            4 * b * s * s + a * r * s - 3 * r * t + 3 * w * s * t + 1,
            6 * w * t * t - r * s + 3 * a * r * t + 3 * b * s * t)


def rotate_state(state, rotation):
    U, V, P, Q = state
    return ((U[0],) + qadj(rotation, U[1:]), (V[0],) + qadj(rotation, V[1:]),
            qadj(rotation, P), qadj(rotation, Q))


def rationalize(state):
    return tuple(tuple(F(x) for x in part) for part in state)


def samples():
    I, minusI = (1, 0, 0, 0), (-1, 0, 0, 0)
    zero, e1, e2, e3 = (0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)
    U, V = (F(3, 5), F(4, 5), 0, 0), (F(5, 13), 0, F(12, 13), 0)
    states = [
        ("central_zero_rank0", (I, I, zero, zero), None),
        ("central_circulation_rank1", (I, I, e1, zero), None),
        ("central_two_circulations_rank2", (I, I, e1, e2), None),
        ("central_signs_rank2", (minusI, I, (1, 2, 3), (-2, 0, 1)), None),
        ("commuting_axial_rank1", (U, U, (2, 0, 0), (-3, 0, 0)), None),
        ("commuting_transverse_rank2", (U, U, e2, (0, -1, 0)), None),
        ("one_central_rank2", (I, V, e1, (0, 2, 0)), None),
        ("mirror_plus_rank3", ((0, 1, 0, 0), (0, 0, 1, 0), e3, (0, 0, -1)), (0, 0, 1)),
        ("mirror_minus_rank3", ((0, 1, 0, 0), (0, 0, 1, 0), (0, 0, -1), e3), (0, 0, -1)),
    ]
    for name, U0, V0, p in [
        ("regular_plane_rank2", U, V, (2, -1, 0)),
        ("regular_oriented_rank3", U, V, (2, -1, 3)),
        ("regular_mixed_rank3", U, (F(1, 2),) * 4, (F(1, 2), F(-2, 3), F(5, 7))),
        ("regular_negative_scalar_rank3", (F(-3, 5), F(4, 5), 0, 0), V, (-2, 3, -1)),
    ]:
        states.append((name, regular_lift(U0, V0, p), p))
    return [(name, rationalize(state), None if p is None else tuple(F(v) for v in p))
            for name, state, p in states]


def encode(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {str(key): encode(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [encode(item) for item in value]
    return value


def run():
    counts = {"checks": 0, "source_invariant_rhs_comparisons": 0,
              "proper_rotation_controls": 0, "regular_decoder_derivative_controls": 0,
              "basis_dot_cross_controls": 0}

    def require(condition, message):
        counts["checks"] += 1
        if not condition:
            raise RuntimeError(message)

    rows = []
    data = samples()
    rotations = ((F(3, 5), 0, 0, F(4, 5)), (F(1, 2),) * 4)
    for name, original, expected_p in data:
        row = {"name": name, "phase_rank": phase_rank(original), "energy": source_energy(original)}
        for state in (original,) + tuple(rotate_state(original, r) for r in rotations):
            joint = summarize(state)
            compiler = Compiler(joint)
            require(not image_failures(joint), name + ": reached image")
            require(source_gauss(state) == (0, 0, 0), name + ": source zero Gauss")
            require(compiler.energy() == source_energy(state), name + ": energy decoder")
            require(source_energy(state) >= F(3, 2) * (dot(state[2], state[2]) + dot(state[3], state[3])),
                    name + ": compact energy bound")
            tangent = source_rhs(state)
            dual = dual_state(state, tangent)
            joint_dual = summarize(dual)
            invariant_rhs = compiler.rhs()
            require(tuple(value.tangent for value in flat(joint_dual)) == flat(invariant_rhs),
                    name + ": source differential equals invariant compiler")
            counts["source_invariant_rhs_comparisons"] += 1
            require(all(value.tangent == 0 for value in source_gauss(dual)), name + ": Gauss tangency")
            require(source_energy(dual).tangent == 0, name + ": energy tangency")
            require(dot(dual[0], dual[0]).tangent == 0 and dot(dual[1], dual[1]).tangent == 0,
                    name + ": unit tangency")
            if state != original:
                require(flat(joint) == flat(summarize(original)), name + ": proper-rotation invariant joint")
                require(flat(invariant_rhs) == flat(Compiler(summarize(original)).rhs()),
                        name + ": proper-rotation invariant continuation")
                counts["proper_rotation_controls"] += 1
            if expected_p is not None:
                x, p, _ = regular_decode(joint)
                require(p == expected_p, name + ": regular inverse momenta")
                _, p_dual, _ = regular_decode(joint_dual)
                require(tuple(value.tangent for value in p_dual) == canonical_p_rhs(x, p),
                        name + ": old canonical momentum derivatives")
                counts["regular_decoder_derivative_controls"] += 1

        # Exhaust every one of the finite 10-by-10 primitive compiler pairs
        # on this named source, evaluating compiled results only in this test.
        joint = summarize(original)
        compiler = Compiler(joint)
        X = (original[0][1:], original[1][1:], original[2], original[3])
        concrete_basis = X + tuple(cross(X[i], X[j]) for i, j in PAIRS)
        for i, j in ((i, j) for i in range(10) for j in range(10)):
            require(compiler.basis_dot(BASIS[i], BASIS[j]) == dot(concrete_basis[i], concrete_basis[j]),
                    name + ": basis dot")
            coefficients = compiler.basis_cross(BASIS[i], BASIS[j])
            evaluated = tuple(sum(coefficients[k] * concrete_basis[k][axis] for k in range(10)) for axis in range(3))
            require(evaluated == cross(concrete_basis[i], concrete_basis[j]), name + ": basis cross")
            counts["basis_dot_cross_controls"] += 2
        rows.append(row)

    require({row["phase_rank"] for row in rows} == {0, 1, 2, 3}, "all phase ranks represented")
    plus, minus = data[7][1], data[8][1]
    jplus, jminus = summarize(plus), summarize(minus)
    require(jplus["G"] == jminus["G"], "mirror equal full Gram")
    require(source_energy(plus) == source_energy(minus) == 5, "mirror equal total energy")
    _, pplus, vplus = regular_decode(jplus)
    _, pminus, vminus = regular_decode(jminus)
    require(vplus[2] == 6 and vminus[2] == -6, "mirror derivative separation")
    require(jplus["tau"][(0, 1, 2)] == 1 and jminus["tau"][(0, 1, 2)] == -1,
            "mirror triple separation")

    central = data[2][1]
    central_rhs = source_rhs(central)
    central_cross = cross(central_rhs[0][1:], central_rhs[1][1:])
    require(central_cross == (0, 0, 15), "central crossing leading vector coefficient")
    require(dot(central_cross, central_cross) == 225, "Delta fourth-order leading coefficient")
    require(source_energy(data[1][1]) == 2 and source_energy(data[0][1]) == 0,
            "singular circulation retained energy")

    invalid = []
    candidate = dict(jplus, a=F(1))
    invalid.append(("unit_mismatch", candidate, "unit"))
    candidate = dict(jplus, tau=dict(jplus["tau"]))
    candidate["tau"][(0, 1, 2)] *= -1
    invalid.append(("independently_flipped_triple", candidate, "triple_minor_compatibility"))
    candidate = summarize(rationalize(((0, 1, 0, 0), (1, 0, 0, 0), (0, 1, 0), (0, 0, 0))))
    invalid.append(("nonzero_gauss", candidate, "zero_gauss"))
    candidate = {"a": F(0), "b": F(0),
                 "G": tuple(tuple(F(int(i == j)) for j in range(4)) for i in range(4)),
                 "tau": {ijk: F(0) for ijk in TRIPLES}}
    invalid.append(("rank_four_Gram", candidate, "rank_at_most_three"))
    rejected = []
    for name, candidate, expected in invalid:
        failures = image_failures(candidate)
        require(expected in failures, name + ": rejected by exact image criterion")
        rejected.append({"name": name, "failed_conditions": failures})

    return encode({
        "schema": "ym2_global_phase_joint.invariants.v1",
        "evidence_grade": "bounded exact rational checks; written general proofs in GLOBAL_INVARIANT_JOINT.md",
        "method": "quaternion source differential versus ten-coefficient Gram/triple compiler; exact dual derivatives; no time integration",
        "scope": "fixed seven-link two-square classical zero-Gauss source; ranks zero through three; no continuum or quantum assertion",
        "counts": counts,
        "states": rows,
        "mirror_hostile": {"same_full_Gram": True, "kinetic_energy_each": F(3),
                           "total_energy_each": F(5), "tau_123": (F(1), F(-1)),
                           "outer_trace_velocity": (vplus[2], vminus[2]),
                           "regular_p_w": (pplus[2], pminus[2])},
        "central_crossing": {"initial_phase_rank": 2, "initial_energy": F(4),
                             "u_cross_v_t_squared_coefficient": central_cross,
                             "Delta_t_fourth_coefficient": F(225)},
        "image_rejections": rejected,
        "status": "PASS",
    })


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-results", action="store_true")
    args = parser.parse_args()
    result = run()
    receipt = Path(__file__).resolve().with_name("RESULTS_INVARIANTS.json")
    if args.write_results:
        receipt.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print("PASS: wrote " + str(receipt))
    else:
        expected = json.loads(receipt.read_text(encoding="utf-8"))
        if expected != result:
            raise RuntimeError("Recomputed invariants differ from RESULTS_INVARIANTS.json")
        print("PASS: invariant controls match RESULTS_INVARIANTS.json")
    print(json.dumps(result["counts"], sort_keys=True))


if __name__ == "__main__":
    main()
