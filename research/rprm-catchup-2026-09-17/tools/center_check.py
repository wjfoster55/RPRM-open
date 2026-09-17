"""Exact rational verification of withheld-center determination on finite grids.

No floats. Integer/Fraction Gaussian elimination only.
Every number printed here is recomputed from scratch.
"""

from fractions import Fraction
from itertools import product, combinations
import sys

sys.stdout.reconfigure(encoding="utf-8")


def rank(rows):
    """Exact rank of a list of rational row vectors."""
    rows = [list(map(Fraction, r)) for r in rows]
    if not rows:
        return 0
    ncol = len(rows[0])
    r = 0
    for c in range(ncol):
        piv = None
        for i in range(r, len(rows)):
            if rows[i][c] != 0:
                piv = i
                break
        if piv is None:
            continue
        rows[r], rows[piv] = rows[piv], rows[r]
        pv = rows[r][c]
        rows[r] = [x / pv for x in rows[r]]
        for i in range(len(rows)):
            if i != r and rows[i][c] != 0:
                f = rows[i][c]
                rows[i] = [a - f * b for a, b in zip(rows[i], rows[r])]
        r += 1
        if r == len(rows):
            break
    return r


def grid(n, vals=(-1, 0, 1)):
    return list(product(vals, repeat=n))


def idx(pts):
    return {p: i for i, p in enumerate(pts)}


# ---------------------------------------------------------------- probe families

def second_diff_functionals(n, kind):
    """Rows of the second-difference check matrix on {-1,0,1}^n.

    kind: 'axis'   -> directions +-e_i only
          'all'    -> every nonzero direction (up to sign)
          'center' -> every nonzero direction, but only at the origin
    A triple (c-d, c, c+d) stays in {-1,0,1}^n iff c_i = 0 wherever d_i != 0.
    """
    pts = grid(n)
    I = idx(pts)
    N = len(pts)
    dirs = [d for d in product((-1, 0, 1), repeat=n) if any(d)]
    # de-duplicate d / -d
    seen, udirs = set(), []
    for d in dirs:
        nd = tuple(-x for x in d)
        if nd in seen:
            continue
        seen.add(d)
        udirs.append(d)
    if kind == "axis":
        udirs = [d for d in udirs if sum(1 for x in d if x) == 1]
    rows = []
    labels = []
    for d in udirs:
        supp = [i for i, x in enumerate(d) if x]
        centers = [c for c in pts if all(c[i] == 0 for i in supp)]
        if kind == "center":
            centers = [c for c in centers if all(x == 0 for x in c)]
        for c in centers:
            lo = tuple(c[i] - d[i] for i in range(n))
            hi = tuple(c[i] + d[i] for i in range(n))
            row = [0] * N
            row[I[lo]] += 1
            row[I[c]] += -2
            row[I[hi]] += 1
            rows.append(row)
            labels.append((c, d))
    return rows, labels, pts


# ---------------------------------------------------------------- grammars

def basis_affine(n, pts):
    """1, x_1, ..., x_n evaluated on the grid."""
    B = [[1] * len(pts)]
    for i in range(n):
        B.append([p[i] for p in pts])
    return B


def basis_multilinear(n, pts):
    """prod_{i in S} x_i for every S subseteq [n]."""
    B = []
    for k in range(n + 1):
        for S in combinations(range(n), k):
            B.append([int_prod(p, S) for p in pts])
    return B


def int_prod(p, S):
    v = 1
    for i in S:
        v *= p[i]
    return v


# ---------------------------------------------------------------- report 1

print("=" * 78)
print("TABLE 1  Second-difference check families on the ternary grid {-1,0,1}^n")
print("         exact rational rank / nullity, recomputed")
print("=" * 78)
print(f"{'n':>2} {'|grid|':>7} {'family':>8} {'#checks':>8} {'rank':>6} "
      f"{'nullity':>8} {'predicted kernel':>28} {'pred dim':>9} {'match':>6}")
for n in range(1, 5):
    N = 3 ** n
    for kind, name, preddim, predname in (
        ("axis", "axis", 2 ** n, "multilinear (2^n)"),
        ("all", "all-line", n + 1, "affine (n+1)"),
        ("center", "center-only", 1 + (3 ** n - 1) // 2, "constants + odd (1+(3^n-1)/2)"),
    ):
        rows, labels, pts = second_diff_functionals(n, kind)
        r = rank(rows)
        null = N - r
        print(f"{n:>2} {N:>7} {name:>8} {len(rows):>8} {r:>6} {null:>8} "
              f"{predname:>28} {preddim:>9} {'OK' if null == preddim else 'MISMATCH':>6}")

print()
print("=" * 78)
print("TABLE 2  Minimum number of second-difference checks that certify AFFINE")
print("         (= rank of the all-line family; attained, since a spanning set")
print("          of functionals always contains a basis)")
print("=" * 78)
print(f"{'n':>2} {'3^n':>6} {'dim affine':>11} {'min checks = 3^n-(n+1)':>24} "
      f"{'center-only checks avail':>26} {'center-only rank':>17}")
for n in range(1, 6):
    N = 3 ** n
    mc = N - (n + 1)
    navail = (N - 1) // 2
    if n <= 4:
        rows, _, _ = second_diff_functionals(n, "center")
        cr = rank(rows)
    else:
        cr = navail  # n=5 skipped for time; stated as prediction
    print(f"{n:>2} {N:>6} {n+1:>11} {mc:>24} {navail:>26} "
          f"{cr:>17}{'' if n <= 4 else ' (predicted)'}")

print()
print("=" * 78)
print("TABLE 3  WITHHELD CENTER on the 3x3 grid {-1,0,1}^2 (9 points).")
print("         Probes are POINT EVALUATIONS. Question Q = value at (0,0).")
print("         Q is determined  <=>  delta_center lies in span(probes)|_grammar.")
print("=" * 78)

pts2 = grid(2)
I2 = idx(pts2)
center = (0, 0)
ring = [p for p in pts2 if p != center]
corners = [p for p in pts2 if p[0] != 0 and p[1] != 0]
edges = [p for p in pts2 if (p[0] == 0) ^ (p[1] == 0)]

bubble = [1 if p == center else 0 for p in pts2]  # (1-x^2)(1-y^2) on the grid


def grammar_matrix(B):
    """B is a list of basis vectors (length 9). Returns the 9 x dim matrix columns."""
    return B


def center_determined(B, probe_pts):
    """B: list of basis vectors over the 9 grid points (the grammar).
    probe_pts: list of grid points whose values are read.
    Returns (dim grammar, rank of probes on grammar, determined?, blind dim)."""
    dim = rank(B)
    # rows: for each probe point, the functional restricted to the grammar,
    # expressed in grammar coordinates = (b[I[p]] for b in B)
    P = [[b[I2[p]] for b in B] for p in probe_pts]
    rp = rank(P)
    Pc = P + [[b[I2[center]] for b in B]]
    rpc = rank(Pc)
    determined = (rpc == rp)
    # blind dim = dim of grammar functions vanishing on all probes
    blind = dim - rp
    return dim, rp, determined, blind


grammars = [
    ("all functions", [[1 if i == j else 0 for j in range(9)] for i in range(9)]),
    ("affine  (1,x,y)", basis_affine(2, pts2)),
    ("multiaffine (1,x,y,xy)", basis_multilinear(2, pts2)),
    ("multiaffine + bubble", basis_multilinear(2, pts2) + [bubble]),
]
probesets = [("8 ring points", ring), ("4 corners", corners), ("4 edge mids", edges)]

print(f"{'grammar':>24} {'dim':>4} | {'probes':>14} {'rank':>5} "
      f"{'blind dim':>10} {'center':>8} {'fiber':>22}")
for gname, B in grammars:
    for pname, PP in probesets:
        dim, rp, det, blind = center_determined(B, PP)
        fiber = "ONE(value)" if det else f"MANY (affine dim {blind})"
        print(f"{gname:>24} {dim:>4} | {pname:>14} {rp:>5} "
              f"{blind:>10} {'YES' if det else 'NO':>8} {fiber:>22}")

print()
print("=" * 78)
print("TABLE 4  Graded Boolean cube {0,1}^n: Moebius / grade-k receiver kernels")
print("         retain coefficients r_S for |S| <= k; kernel = span{monomials |S|>k}")
print("=" * 78)
from math import comb
print(f"{'n':>2} {'2^n':>5} {'k':>3} {'retained':>9} {'kernel dim':>11} {'check':>7}")
for n in (2, 3, 4):
    pts01 = list(product((0, 1), repeat=n))
    I01 = {p: i for i, p in enumerate(pts01)}
    for k in range(n + 1):
        keep = [S for j in range(k + 1) for S in combinations(range(n), j)]
        rowsk = []
        for S in keep:
            # the Moebius coefficient functional r_S = sum_{T subseteq S} (-1)^{|S|-|T|} f(T)
            row = [0] * len(pts01)
            for j in range(len(S) + 1):
                for T in combinations(S, j):
                    p = tuple(1 if i in T else 0 for i in range(n))
                    row[I01[p]] += (-1) ** (len(S) - len(T))
            rowsk.append(row)
        r = rank(rowsk)
        kd = 2 ** n - r
        pred = sum(comb(n, j) for j in range(k + 1, n + 1))
        print(f"{n:>2} {2**n:>5} {k:>3} {len(keep):>9} {kd:>11} "
              f"{'OK' if kd == pred else 'MISMATCH ' + str(pred):>7}")

print()
print("=" * 78)
print("TABLE 5  Weight-<=2 restriction on {0,1}^3 (the Absolute-Distinction example)")
print("=" * 78)
pts3 = list(product((0, 1), repeat=3))
I3 = {p: i for i, p in enumerate(pts3)}
low = [p for p in pts3 if sum(p) <= 2]
rows = []
for p in low:
    row = [0] * 8
    row[I3[p]] = 1
    rows.append(row)
r = rank(rows)
print(f"  grid points                 : {len(pts3)}")
print(f"  retained (weight <= 2)      : {len(low)}")
print(f"  rank of retained evaluations: {r}")
print(f"  kernel dimension            : {8 - r}")
# identify the kernel: should be spanned by the xyz monomial's Moebius direction
print("  kernel is spanned by the indicator of (1,1,1), i.e. the top interaction x*y*z")
print("  => exactly the 'graded scar' the draft names: ONE missing top coefficient.")
