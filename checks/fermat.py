"""Exact finite premises for docs/fermat.md. Code: 0BSD.

This is an arithmetic certificate checker, not a proof assistant for the
written arguments or a new unrestricted proof of Fermat's Last Theorem.
All certificate data are ordinary integer pairs; only the standard library
is used. Run with --output followed by an absolute JSON path.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
from math import comb, gcd, isqrt
import json
import os
from pathlib import Path
import sys
from uuid import uuid4


# (odd prime exponent, auxiliary prime). The full nonzero power image is
# reconstructed below; neither a supplied generator nor a PASS label is used.
AUXILIARIES = (
    (3, 7), (5, 11), (7, 29), (11, 23), (13, 53), (17, 137),
    (19, 191), (23, 47), (29, 59), (31, 311), (37, 149), (41, 83),
    (43, 173), (47, 659), (53, 107), (59, 827), (61, 977), (67, 269),
    (71, 569), (73, 293), (79, 317), (83, 167), (89, 179), (97, 389),
    (101, 809), (103, 1031), (107, 857), (109, 1091), (113, 227), (127, 509),
    (131, 263), (137, 1097), (139, 557), (149, 1193), (151, 1511), (157, 1571),
    (163, 653), (167, 2339), (173, 347), (179, 359), (181, 1811), (191, 383),
    (193, 773), (197, 7487), (199, 797), (211, 2111), (223, 7583), (227, 5903),
    (229, 5039), (233, 467), (239, 479), (241, 2411), (251, 503), (257, 9767),
    (263, 5261), (269, 2153), (271, 2711), (277, 1109), (281, 563), (283, 9623),
    (293, 587), (307, 1229), (311, 6221), (313, 5009), (317, 8243), (331, 5297),
    (337, 3371), (347, 2777), (349, 3491), (353, 4943), (359, 719), (367, 3671),
    (373, 1493), (379, 10613), (383, 23747), (389, 14783), (397, 6353), (401, 3209),
    (409, 1637), (419, 839), (421, 4211), (431, 863), (433, 1733), (439, 4391),
    (443, 887), (449, 3593), (457, 21023), (461, 9221), (463, 18521), (467, 9341),
    (479, 3833), (487, 1949), (491, 983), (499, 1997), (503, 7043), (509, 1019),
    (521, 16673), (523, 5231), (541, 11903), (547, 5471), (557, 4457), (563, 7883),
    (569, 25037), (571, 5711), (577, 2309), (587, 8219), (593, 1187), (599, 4793),
    (601, 6011), (607, 20639), (613, 6131), (617, 4937), (619, 2477), (631, 6311),
    (641, 1283), (643, 10289), (647, 9059), (653, 1307), (659, 1319), (661, 14543),
    (673, 2693), (677, 5417), (683, 1367), (691, 6911), (701, 22433), (709, 2837),
    (719, 1439), (727, 2909), (733, 7331), (739, 2957), (743, 1487), (751, 52571),
    (757, 12113), (761, 1523), (769, 7691), (773, 15461), (787, 22037), (797, 11159),
    (809, 1619), (811, 8111), (821, 6569), (823, 8231), (827, 11579), (829, 8291),
    (839, 26849), (853, 3413), (857, 6857), (859, 18899), (863, 27617), (877, 14033),
    (881, 22907), (883, 3533), (887, 23063), (907, 30839), (911, 1823), (919, 3677),
    (929, 7433), (937, 9371), (941, 7529), (947, 7577), (953, 1907), (967, 15473),
    (971, 19421), (977, 7817), (983, 13763), (991, 21803), (997, 3989), (1009, 10091),
    (1013, 2027), (1019, 2039), (1021, 10211), (1031, 2063), (1033, 4133), (1039, 4157),
    (1049, 2099), (1051, 29429), (1061, 21221), (1063, 4253), (1069, 10691), (1087, 4349),
    (1091, 21821), (1093, 4373), (1097, 15359), (1103, 2207), (1109, 15527), (1117, 11171),
    (1123, 4493), (1129, 4517), (1151, 9209), (1153, 25367), (1163, 37217), (1171, 25763),
    (1181, 30707), (1187, 9497), (1193, 16703), (1201, 12011), (1213, 26687), (1217, 31643),
    (1223, 2447), (1229, 2459), (1231, 19697), (1237, 19793), (1249, 12491), (1259, 17627),
    (1277, 25541), (1279, 12791), (1283, 33359), (1289, 2579), (1291, 12911), (1297, 5189),
    (1301, 26021), (1303, 20849), (1307, 10457), (1319, 42209), (1321, 29063), (1327, 5309),
    (1361, 10889), (1367, 10937), (1373, 60413), (1381, 38669), (1399, 97931), (1409, 2819),
    (1423, 5693), (1427, 19979), (1429, 5717), (1433, 20063), (1439, 2879), (1447, 49199),
    (1451, 2903), (1453, 5813), (1459, 14591), (1471, 23537), (1481, 2963), (1483, 14831),
    (1487, 11897), (1489, 14891), (1493, 20903), (1499, 2999), (1511, 3023), (1523, 21323),
    (1531, 79613), (1543, 6173), (1549, 6197), (1553, 49697), (1559, 3119), (1567, 6269),
    (1571, 12569), (1579, 6317), (1583, 3167), (1597, 6389), (1601, 3203), (1607, 32141),
    (1609, 16091), (1613, 32261), (1619, 12953), (1621, 45389), (1627, 45557), (1637, 62207),
    (1657, 26513), (1663, 6653), (1667, 13337), (1669, 16691), (1693, 16931), (1697, 13577),
    (1699, 37379), (1709, 85451), (1721, 34421), (1723, 17231), (1733, 3467), (1741, 38303),
    (1747, 17471), (1753, 7013), (1759, 38699), (1777, 7109), (1783, 39227), (1787, 185849),
    (1789, 17891), (1801, 28817), (1811, 3623), (1823, 25523), (1831, 18311), (1847, 48023),
    (1861, 74441), (1867, 18671), (1871, 14969), (1873, 18731), (1877, 15017), (1879, 7517),
    (1889, 3779), (1901, 3803), (1907, 26699), (1913, 26783), (1931, 3863), (1933, 88919),
    (1949, 132533), (1951, 42923), (1973, 3947), (1979, 39581), (1987, 7949), (1993, 67763),
    (1997, 87869), (1999, 19991),
)


def integer(value, minimum, name):
    if type(value) is not int or value < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")
    return value


def is_prime(n):
    integer(n, 0, "n")
    return n >= 2 and all(n % d for d in range(2, isqrt(n) + 1))


def auxiliary(p, q):
    """Validate one sufficient first-case certificate using the full image."""
    integer(p, 3, "p")
    integer(q, 2, "q")
    if not is_prime(p) or p % 2 == 0:
        raise ValueError("p must be an odd prime")
    if not is_prime(q) or q == p or (q - 1) % (2 * p):
        raise ValueError("q must be a prime of the form 2*k*p+1, k >= 1")
    residues = {pow(a, p, q) for a in range(1, q)}
    if len(residues) != (q - 1) // p or 0 in residues:
        raise ValueError("power image has the wrong size")
    if any((1 - r) % q in residues for r in residues):
        raise ValueError("power image contains two elements summing to one")
    if p % q in residues:
        raise ValueError("p is a nonzero pth power modulo q")
    return {"p": p, "q": q, "source_powers": q - 1,
            "residues": len(residues)}


def verify_auxiliaries(records):
    """Require exactly one certificate for every odd prime through 1999."""
    if type(records) not in (tuple, list):
        raise ValueError("records must be a complete materialized tuple or list")
    pairs = []
    for row in records:
        if type(row) not in (tuple, list) or len(row) != 2:
            raise ValueError("each record must be a pair")
        p, q = row
        pairs.append((integer(p, 3, "p"), integer(q, 2, "q")))
    expected = tuple(p for p in range(3, 2000, 2) if is_prime(p))
    if tuple(p for p, _ in pairs) != expected:
        raise ValueError("exponent census must be the ordered odd primes through 1999")
    checked = [auxiliary(p, q) for p, q in pairs]
    return {"certificates": len(checked), "largest_p": expected[-1],
            "largest_q": max(row["q"] for row in checked),
            "source_powers": sum(row["source_powers"] for row in checked),
            "distinct_residues_per_modulus": sum(row["residues"] for row in checked)}


def residual(a, b, c, n):
    for name, value in (("a", a), ("b", b), ("c", c)):
        integer(value, 1, name)
    integer(n, 1, "n")
    return a**n + b**n - c**n


def valuation(n, p):
    integer(n, 1, "n")
    if not is_prime(p):
        raise ValueError("valuation base must be prime")
    exponent = 0
    while n % p == 0:
        n //= p
        exponent += 1
    return exponent


def exponent_census():
    """Check every exponent allowed by the written a >= 2*n lemma."""
    counts = Counter()
    covered_primes = {p for p, _ in AUXILIARIES}
    remaining = []
    for n in range(3, 2001):
        if n % 3 == 0:
            counts["cubic_descent"] += 1
            continue
        if n % 4 == 0:
            counts["quartic_descent"] += 1
            continue
        m = n if n % 2 else n // 2
        p = next(p for p in range(5, m + 1) if m % p == 0 and is_prime(p))
        if p not in covered_primes or gcd(m, p - 1) != 1:
            raise RuntimeError("missing auxiliary or noninjective least-prime map")
        if n in (5, 10):
            remaining.append(n)
            counts["exceptional_fifth_or_tenth"] += 1
            continue
        ceiling = 26000 if n % 2 else 1100000000
        floor = p ** (n - valuation(m, p))
        if floor <= ceiling:
            raise RuntimeError(f"valuation comparison failed at exponent {n}")
        counts["linear_valuation" if n % 2 else "quadratic_valuation"] += 1
    if remaining != [5, 10] or sum(counts.values()) != 1998:
        raise RuntimeError("incomplete exponent census")
    return dict(counts)


def fifth_residual(a, gap, seam, kind):
    integer(a, 1, "a")
    integer(gap, 1, "gap")
    integer(seam, 1, "seam")
    if kind == "difference":
        return residual(a, a + seam - gap, a + seam, 5)
    if kind == "sum":
        return residual(a, seam - a, seam - a + gap, 5)
    raise ValueError("kind must be difference or sum")


def factor_pairs(total):
    """Complete positive (d,s), d<s, d*s=total carrier."""
    integer(total, 1, "total")
    return tuple((d, total // d) for d in range(1, isqrt(total) + 1)
                 if total % d == 0 and d < total // d)


def tenth_factor_candidates():
    """Enumerate the two proved gap forms under the tenth-power bounds."""
    output = {}
    examined = 0
    for kind in ("ordinary", "five_divides_a"):
        multiplier = 1 if kind == "ordinary" else 5**9
        pairs = []
        t = 1
        while multiplier * t**10 < 6560000:
            for d, s in factor_pairs(multiplier * t**10):
                examined += 1
                if d >= 400 or s >= 16400 or (s - d) % 2:
                    continue
                b, c = (s - d) // 2, (s + d) // 2
                if b > 0 and gcd(b, c) == 1:
                    pairs.append((b, c))
            t += 1
        output[kind] = sorted(set(pairs))
    if output != {"ordinary": [(255, 257)], "five_divides_a": []}:
        raise RuntimeError("unexpected tenth-power factor fiber")
    if not 257**2 < 5**9:
        raise RuntimeError("last quadratic seam was not excluded")
    return {"factor_pairs_examined": examined, "fibers": output,
            "surviving_fermat_solutions": 0}


def run():
    named = 0
    def require(condition, label):
        nonlocal named
        if not condition:
            raise RuntimeError(label)
        named += 1

    auxiliary_counts = verify_auxiliaries(AUXILIARIES)
    require(auxiliary_counts["certificates"] == 302, "auxiliary census")
    require(auxiliary_counts["source_powers"] == 4052680, "complete source powers")
    require(auxiliary_counts["distinct_residues_per_modulus"] == 3936, "residue census")
    require(4000**5 < 5 * 22000**4, "fifth shell bound")
    require(22800**2 + 22000**2 < 1100000000, "quadratic seam ceiling")
    require(7**6 > 26000 and 5**20 > 26000, "odd valuation floors")
    require(7**13 > 1100000000 and 5**45 > 1100000000, "even valuation floors")
    require(4000**10 < 10 * 8000**9, "tenth shell bound")
    require(5**9 < 6560000 < 5**9 * 2**10, "exceptional tenth gap")

    # A single rational certificate supports the separate symbolic monotonicity
    # proof for every n >= 100. This is not sampling that unbounded range.
    kappa, n = Fraction(81, 40), 100
    lower = sum(Fraction(comb(n, j), 1) / (kappa * n + 1)**j for j in range(4))
    require(lower == Fraction(9991013, 6129013) and lower > Fraction(13, 8), "slope certificate")
    require(Fraction(8, 13)**2 + Fraction(8, 13) - 1 == -Fraction(1, 169), "slope residual")

    require(4626**5 - 4001**5 - 4000**5 == 69217768803909375, "five divides smaller root")
    require(24000**5 - 23999**5 - 4000**5 == 634741765759880001, "large difference seam")
    brackets = (
        ("difference", 625, 1, 335, -18753691826, 26900909375),
        ("difference", 625, 32, 1028, -1142821221024, 1641632904757),
        ("difference", 625, 243, 2523, -35451102937500, 32297263771651),
        ("sum", 625, 1, 181, -926025000, 6250588651),
        ("sum", 625, 32, 296, -4201942176, 60664215625),
        ("sum", 20000, 1, 3296, -329671369090625, 353993777122976),
    )
    for kind, seam, gap, a, lo, hi in brackets:
        require(fifth_residual(a, gap, seam, kind) == lo < 0, "negative bracket")
        require(fifth_residual(a + 1, gap, seam, kind) == hi > 0, "positive bracket")
    require(fifth_residual(4000, 32, 20000, "sum") == -9503787009999634432, "sum endpoint 32")
    require(fifth_residual(4000, 243, 20000, "sum") == -81057900031960689443, "sum endpoint 243")
    gaps = tuple(t**5 for t in range(1, 4) if t**5 < 800)
    seams = tuple(625 * t**5 for t in range(1, 3) if 625 * t**5 < 26000)
    require(gaps == (1, 32, 243) and 4**5 >= 800, "complete fifth gaps")
    require(seams == (625, 20000) and 625 * 3**5 >= 26000, "complete exceptional seams")
    # Independent direct check of every integer in every derived branch.
    fifth_inputs = 0
    fifth_branches = Counter()
    for kind in ("difference", "sum"):
        for seam in seams:
            for gap in gaps:
                for a in range(1, 4001):
                    b = a + seam - gap if kind == "difference" else seam - a
                    c = b + gap
                    if a < b < c and 5 * gap < a:
                        if residual(a, b, c, 5) == 0:
                            raise RuntimeError("fifth-power branch has an integer zero")
                        fifth_inputs += 1
                        fifth_branches[f"{kind}:{seam}:{gap}"] += 1

    # Controls retain valid outside-premise equalities and failed shortcuts.
    require(residual(3, 4, 5, 2) == 0, "square equality retained")
    require(residual(6, 8, 9, 3) == -1, "near cube is not equality")
    require(residual(5, 6, 7, 3) == -2 and residual(6, 7, 8, 3) == 47, "upward shell sign shortcut refuted")
    require(3**3 + 4**3 + 5**3 == 6**3, "three summands change the target")
    require(1**2 + 7**2 == 5**2 + 5**2 and 1**3 + 7**3 != 2 * 5**3, "one depth does not determine the next")
    admission_controls = 0
    bad_calls = (
        lambda: verify_auxiliaries(AUXILIARIES[:-1]),
        lambda: verify_auxiliaries(AUXILIARIES + AUXILIARIES[:1]),
        lambda: verify_auxiliaries(iter(AUXILIARIES)),
        lambda: verify_auxiliaries(((True, 7),)),
        lambda: verify_auxiliaries(((3, 7, 9),)),
        lambda: auxiliary(4, 17), lambda: auxiliary(3, 3),
        lambda: auxiliary(3, 25), lambda: auxiliary(3, 19),
        lambda: auxiliary(13, 443),
        lambda: auxiliary(True, 7), lambda: auxiliary(3, 7.0),
        lambda: residual(0, 1, 1, 3), lambda: residual(1, 1, 1, True),
        lambda: factor_pairs(0), lambda: valuation(10, 4),
        lambda: fifth_residual(1, 1, 625, "unknown"),
    )
    for call in bad_calls:
        try:
            call()
        except ValueError:
            admission_controls += 1
        else:
            raise RuntimeError("malformed or invalid certificate was accepted")
    return {"status": "PASS", "scope": "exact finite premises of the written smaller-root <= 4000 proof",
            "formal_proof_of_prose": False, "full_fermat_proof": False,
            "auxiliaries": auxiliary_counts, "exponents": exponent_census(),
            "fifth_branch_integer_inputs": fifth_inputs, "fifth_branches": dict(fifth_branches),
            "tenth": tenth_factor_candidates(), "named_checks": named,
            "admission_controls": admission_controls,
            "slope_certificate": {"kappa": "81/40", "from_exponent": 100,
                                  "lower_bound": str(lower)}}


def write_result(path, result):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + "." + uuid4().hex + ".tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    if not args.output.is_absolute():
        parser.error("--output must be an absolute JSON path")
    write_result(args.output, {"status": "PENDING"})
    try:
        result = run()
    except Exception as exc:
        write_result(args.output, {"status": "FAIL", "error": f"{type(exc).__name__}: {exc}"})
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    write_result(args.output, result)
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
