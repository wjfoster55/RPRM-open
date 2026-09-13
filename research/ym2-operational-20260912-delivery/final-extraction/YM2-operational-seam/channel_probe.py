"""New exact finite source-channel check; no old checker or spin truncation.

Run: python -B research/ym2_operational_seam/channel_probe.py
Requires the already-installed numpy. All matrix assertions use integers.
"""

from itertools import product
from fractions import Fraction
import numpy as np


def add(x, y):
    return tuple(a + b for a, b in zip(x, y))


def loop_signs(vertices):
    result = []
    for a, b in zip(vertices, vertices[1:] + vertices[:1]):
        delta = tuple(y - x for x, y in zip(a, b))
        nonzero = [d for d in delta if d]
        assert len(nonzero) == 1 and abs(nonzero[0]) == 1
        result.append(nonzero[0])
    return result


def trace_indices(indices, signs):
    rows, columns = [], []
    for k, sign in enumerate(signs):
        a, b = indices[k], indices[(k + 1) % 4]
        row, column = (a, b) if sign > 0 else (b, a)
        rows.append(row)
        columns.append(column)
    return rows, columns


def encode(bits):
    result = 0
    for bit in bits:
        result = 2 * result + bit
    return result


def product_coefficient_times_four(delta_p, delta_q):
    v, w = (0, 0, 0), (1, 0, 0)
    signs_p = loop_signs([v, w, add(w, delta_p), add(v, delta_p)])
    signs_q = loop_signs([w, v, add(v, delta_q), add(w, delta_q)])
    assert signs_p[0] == 1 and signs_q[0] == -1
    matrix = np.zeros((256, 256), dtype=np.int64)
    for ip, iq in product(product(range(2), repeat=4), repeat=2):
        rp, cp = trace_indices(ip, signs_p)
        rq, cq = trace_indices(iq, signs_q)
        # Shared U tensor conjugate(U), then the six exterior factors.
        rows = [rp[0], rq[0]] + rp[1:] + rq[1:]
        columns = [cp[0], cq[0]] + cp[1:] + cq[1:]
        # Tr(B pi): B row is pi column.
        matrix[encode(columns), encode(rows)] += 1
    return matrix


def channels(delta_p, delta_q, expected):
    b4 = product_coefficient_times_four(delta_p, delta_q)
    twice_p0 = np.array([[1, 0, 0, 1], [0, 0, 0, 0],
                         [0, 0, 0, 0], [1, 0, 0, 1]], dtype=np.int64)
    twice_p1 = 2 * np.eye(4, dtype=np.int64) - twice_p0
    result = []
    for ell, twice_projector in enumerate([twice_p0, twice_p1]):
        p = np.kron(twice_projector, np.eye(64, dtype=np.int64))
        coefficient16 = p @ b4 @ p
        gram = coefficient16.T @ coefficient16
        rank, eigenvalue, hs_squared = expected[ell]
        assert np.array_equal(gram @ gram, eigenvalue * gram)
        assert int(np.trace(gram)) == 256 * hs_squared
        assert Fraction(int(np.trace(gram)), eigenvalue) == rank
        result.append({"spin": ell, "rank": rank,
                       "nonzero_singular_value_squared":
                           str(Fraction(eigenvalue, 256)),
                       "HS_squared": hs_squared})
    print(delta_p, delta_q, result)


channels((0, 1, 0), (0, -1, 0), [(16, 16, 1), (16, 144, 9)])
channels((0, 1, 0), (0, 0, -1), [(16, 16, 1), (16, 144, 9)])
channels((0, 1, 0), (0, 0, 1), [(4, 64, 1), (12, 192, 9)])
channels((0, -1, 0), (0, 0, -1), [(4, 64, 1), (12, 192, 9)])

# The complete spin-one character coefficient for one square.
n = 3
basis = list(product(range(n), repeat=4))
index = {value: k for k, value in enumerate(basis)}
character = np.zeros((n**4, n**4), dtype=np.int64)
for a, b, c, d in basis:
    character[index[b, c, c, d], index[a, b, d, a]] += 1
gram = character.T @ character
assert np.array_equal(gram @ gram, 9 * gram)
assert int(np.trace(gram)) == 81
print("same-square Q Gamma: rank9, singular value3, exact A norm27")

for m in (2, 4):
    shared_same = m * (m - 2) // 4
    shared_opposite = m * m // 4
    exterior_same = 3 * m * (m - 2) // 2
    exterior_opposite = 3 * m * m // 2
    assert shared_same + shared_opposite == m * (m - 1) // 2
    assert exterior_same + exterior_opposite == 3 * m * (m - 1)
    rational = (Fraction(3*m, 8) + Fraction(shared_opposite, 3)
                + Fraction(exterior_same, 6)
                + Fraction(2 * exterior_opposite, 3))
    radical = Fraction(shared_same + exterior_same, 6)
    assert rational == Fraction(4*m*m, 3) - Fraction(m, 8)
    assert radical == Fraction(7*m*(m-2), 24)
    print("m", m, "orientation-count source kappa =", rational,
          "+", radical, "sqrt(3)")
print("PASS: all exact integer-matrix and rational source-count assertions")
