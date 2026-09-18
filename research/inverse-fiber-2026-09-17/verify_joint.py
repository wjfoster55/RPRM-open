"""Exact tests that XOR/C fibers are not products of their marginals.

Does not import rprm or the other tonight trees. Null names are those
frozen in NULL-JOINT.md at commit bd28533. This script lists complete
products and extras; it does not choose a predicted name after seeing
a representative extra.
"""
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
NULL_COMMIT = "bd28533e315c8a9416eafdfedb7982e33acbacd5"

XOR1 = ((0, 1), (1, 0))
XOR0 = ((0, 0), (1, 1))
AND1 = ((1, 1),)
C00 = ((0, 0, 0), (1, 1, 1))
C11 = ((0, 1, 1), (1, 0, 0))
X2 = ((0, 0), (0, 1), (1, 0), (1, 1))
X3 = tuple((x, y, z) for x in (0, 1) for y in (0, 1) for z in (0, 1))


def pair_marginals(pairs):
    first = tuple(sorted({a for a, _ in pairs}))
    second = tuple(sorted({b for _, b in pairs}))
    return first, second


def pair_product(pairs):
    first, second = pair_marginals(pairs)
    return tuple((a, b) for a in first for b in second)


def triple_marginals(triples):
    xs = tuple(sorted({x for x, _, _ in triples}))
    ys = tuple(sorted({y for _, y, _ in triples}))
    zs = tuple(sorted({z for _, _, z in triples}))
    return xs, ys, zs


def triple_product(triples):
    xs, ys, zs = triple_marginals(triples)
    return tuple((x, y, z) for x in xs for y in ys for z in zs)


def extras(product, fiber):
    fiber_set = set(fiber)
    return tuple(p for p in product if p not in fiber_set)


def main():
    xor1_prod = pair_product(XOR1)
    xor0_prod = pair_product(XOR0)
    and1_prod = pair_product(AND1)
    c00_prod = triple_product(C00)
    c11_prod = triple_product(C11)
    xor1_extra = extras(xor1_prod, XOR1)
    c00_extra = extras(c00_prod, C00)
    c11_extra = extras(c11_prod, C11)

    names = {}
    names["QJ1"] = "N_xor1_joint" if XOR1 != xor1_prod else "N_xor1_factor"
    if xor1_extra == ((0, 0), (1, 1)):
        names["QJ2"] = "N_xor1_extra_eq"
    elif xor1_extra == ((1, 1),):
        names["QJ2"] = "N_xor1_extra_and"
    elif xor1_extra == ():
        names["QJ2"] = "N_xor1_extra_none"
    else:
        names["QJ2"] = "N_xor1_extra_unexpected"

    names["QJ3"] = "N_c00_joint" if C00 != c00_prod else "N_c00_factor"
    expected_c00_extra = tuple(p for p in X3 if p not in set(C00))
    if c00_extra == expected_c00_extra and len(c00_extra) == 6:
        names["QJ4"] = "N_c00_extra6"
    elif c00_extra == ():
        names["QJ4"] = "N_c00_extra_none"
    elif c00_extra == ((0, 0, 1),):
        names["QJ4"] = "N_c00_extra_rep"
    else:
        names["QJ4"] = "N_c00_extra_unexpected"

    names["QJ5"] = "N_c11_joint" if C11 != c11_prod else "N_c11_factor"
    names["QJ6"] = "N_xor1_admits_11" if (1, 1) in xor1_prod else "N_xor1_blocks_11"
    names["QJ7"] = "N_and1_equals" if AND1 == and1_prod else "N_and1_never"
    names["QJ8"] = "N_xor_same_prod" if xor1_prod == xor0_prod else "N_xor_diff_prod"

    frozen = {
        "QJ1": "N_xor1_joint",
        "QJ2": "N_xor1_extra_eq",
        "QJ3": "N_c00_joint",
        "QJ4": "N_c00_extra6",
        "QJ5": "N_c11_joint",
        "QJ6": "N_xor1_admits_11",
        "QJ7": "N_and1_equals",
        "QJ8": "N_xor_same_prod",
    }

    census = {
        "null_commit": NULL_COMMIT,
        "names": names,
        "frozen": frozen,
        "match": names == frozen,
        "XOR1": [list(p) for p in XOR1],
        "XOR0": [list(p) for p in XOR0],
        "AND1": [list(p) for p in AND1],
        "C00": [list(p) for p in C00],
        "C11": [list(p) for p in C11],
        "xor1_prod": [list(p) for p in xor1_prod],
        "xor0_prod": [list(p) for p in xor0_prod],
        "and1_prod": [list(p) for p in and1_prod],
        "c00_prod": [list(p) for p in c00_prod],
        "c11_prod": [list(p) for p in c11_prod],
        "xor1_extra": [list(p) for p in xor1_extra],
        "c00_extra": [list(p) for p in c00_extra],
        "c11_extra": [list(p) for p in c11_extra],
        "xor1_equals_prod": XOR1 == xor1_prod,
        "c00_equals_prod": C00 == c00_prod,
        "c11_equals_prod": C11 == c11_prod,
        "and1_equals_prod": AND1 == and1_prod,
        "xor_products_equal": xor1_prod == xor0_prod,
        "xor1_prod_is_X2": xor1_prod == X2,
        "c00_prod_is_X3": c00_prod == X3,
        "c11_prod_is_X3": c11_prod == X3,
        "hostile_admits_11": (1, 1) in xor1_prod and (1, 1) not in XOR1,
    }

    path = HERE / "CENSUS-JOINT.json"
    path.write_text(json.dumps(census, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    if names != frozen:
        dead = {q: {"got": names[q], "wanted": frozen[q]} for q in frozen if names[q] != frozen[q]}
        raise SystemExit("frozen_null_miss: " + json.dumps(dead, sort_keys=True))

    print("PASS")
    print("null_commit", NULL_COMMIT)
    for q in ("QJ1", "QJ2", "QJ3", "QJ4", "QJ5", "QJ6", "QJ7", "QJ8"):
        print(q, names[q])
    print("xor1_extra", xor1_extra)
    print("c00_extra", c00_extra)
    print("c11_extra", c11_extra)


if __name__ == "__main__":
    main()
