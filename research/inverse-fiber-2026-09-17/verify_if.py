"""Exact tests of complete preimage fibers on named finite forward maps.

Does not import rprm, obstruction, fluid, Hamming, observability, Markov,
or BSD. Null names are those frozen in NULL.md at commit 3127680. This
script enumerates declared domains; it does not choose a predicted name
after seeing a representative.
"""
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
NULL_COMMIT = "3127680b33e65f1b825b3e690791621f91a5cf7a"

X2 = ((0, 0), (0, 1), (1, 0), (1, 1))
X3 = tuple((x, y, z) for x in (0, 1) for y in (0, 1) for z in (0, 1))
ADD3 = (0, 1, 2)


def AND(ab):
    a, b = ab
    return 1 if a == 1 and b == 1 else 0


def XOR(ab):
    a, b = ab
    return 1 if a != b else 0


def NAND(ab):
    return 1 - AND(ab)


def CONST0(ab):
    return 0


def C(xyz):
    x, y, z = xyz
    return (x ^ y, x ^ z)


def fiber(domain, fn, target):
    return tuple(x for x in domain if fn(x) == target)


def add3_fiber(c):
    return tuple((a, b) for a in ADD3 for b in ADD3 if a + b == c)


def product_of_marginals(pairs):
    first = tuple(sorted({a for a, _ in pairs}))
    second = tuple(sorted({b for _, b in pairs}))
    return tuple((a, b) for a in first for b in second)


def product_of_bit_marginals(triples):
    xs = tuple(sorted({x for x, _, _ in triples}))
    ys = tuple(sorted({y for _, y, _ in triples}))
    zs = tuple(sorted({z for _, _, z in triples}))
    return tuple((x, y, z) for x in xs for y in ys for z in zs)


def stopped_and0(limit):
    found = []
    scanned = 0
    complete = True
    for ab in X2:
        scanned += 1
        if AND(ab) == 0:
            found.append(ab)
            if len(found) == limit:
                complete = scanned == len(X2)
                break
    else:
        complete = True
    return tuple(found), complete, scanned


def classify_complete(family):
    if len(family) == 0:
        return "NONE", family
    if len(family) == 1:
        return "ONE", family
    return "MANY", family


def main():
    and1 = fiber(X2, AND, 1)
    and0 = fiber(X2, AND, 0)
    xor1 = fiber(X2, XOR, 1)
    xor0 = fiber(X2, XOR, 0)
    nand0 = fiber(X2, NAND, 0)
    const0_1 = fiber(X2, CONST0, 1)
    c00 = fiber(X3, C, (0, 0))
    c11 = fiber(X3, C, (1, 1))
    add2 = add3_fiber(2)
    add4 = add3_fiber(4)
    and0_product = product_of_marginals(and0)
    c00_product = product_of_bit_marginals(c00)
    partial, partial_complete, partial_scanned = stopped_and0(2)

    if partial_complete:
        raise SystemExit("partial_search_was_complete")
    if set(X2) != {(0, 0), (0, 1), (1, 0), (1, 1)}:
        raise SystemExit("bits2_not_ordered_pairs")
    if 2 + 2 != 4:
        raise SystemExit("add3_wrap_detected")

    names = {}

    names["Q1"] = "N_and1_one" if and1 == ((1, 1),) else "N_and1_many"
    if and0 == ((0, 0), (0, 1), (1, 0)):
        names["Q2"] = "N_and0_many3"
    elif and0 == ((0, 0),):
        names["Q2"] = "N_and0_rep"
    elif and0 == X2:
        names["Q2"] = "N_and0_product4"
    else:
        names["Q2"] = "N_and0_unexpected"

    if xor1 == ((0, 1), (1, 0)):
        names["Q3"] = "N_xor1_many"
    elif xor1 == ((0, 1),):
        names["Q3"] = "N_xor1_rep"
    elif set(xor1) == {(0, 1), (1, 0)} and len(xor1) == 1:
        names["Q3"] = "N_xor1_set"
    else:
        names["Q3"] = "N_xor1_unexpected"

    names["Q4"] = "N_nand0_one" if nand0 == ((1, 1),) else "N_nand0_none"
    names["Q5"] = "N_c0_none" if const0_1 == () else "N_c0_open"
    names["Q6"] = "N_and0_joint" if and0 != and0_product else "N_and0_factor"

    if c00 == ((0, 0, 0), (1, 1, 1)):
        names["Q7"] = "N_c00_many"
    elif c00 == ((0, 0, 0),):
        names["Q7"] = "N_c00_rep"
    elif c00 == X3:
        names["Q7"] = "N_c00_prod8"
    else:
        names["Q7"] = "N_c00_unexpected"

    if c11 == ((0, 1, 1), (1, 0, 0)):
        names["Q8"] = "N_c11_many"
    elif c11 == ((1, 0, 0),):
        names["Q8"] = "N_c11_rep"
    else:
        names["Q8"] = "N_c11_unexpected"

    if not partial_complete:
        names["Q9"] = "N_partial_open"
    elif partial == ((0, 0), (0, 1)):
        names["Q9"] = "N_partial_many2"
    elif partial == ((0, 0),):
        names["Q9"] = "N_partial_one"
    else:
        names["Q9"] = "N_partial_unexpected"

    if add2 == ((0, 2), (1, 1), (2, 0)):
        names["Q10"] = "N_add2_many"
    elif add2 == ((1, 1),):
        names["Q10"] = "N_add2_rep"
    elif add2 == ():
        names["Q10"] = "N_add2_none"
    else:
        names["Q10"] = "N_add2_unexpected"

    if add4 == ():
        names["Q11"] = "N_add4_none"
    elif add4 == ((2, 2),):
        names["Q11"] = "N_add4_one"
    else:
        names["Q11"] = "N_add4_open"

    if xor0 == ((0, 0), (1, 1)):
        names["Q12"] = "N_xor0_many"
    else:
        names["Q12"] = "N_xor0_class"

    frozen = {
        "Q1": "N_and1_one",
        "Q2": "N_and0_many3",
        "Q3": "N_xor1_many",
        "Q4": "N_nand0_one",
        "Q5": "N_c0_none",
        "Q6": "N_and0_joint",
        "Q7": "N_c00_many",
        "Q8": "N_c11_many",
        "Q9": "N_partial_open",
        "Q10": "N_add2_many",
        "Q11": "N_add4_none",
        "Q12": "N_xor0_many",
    }
    # Q11's frozen survivor died on the first census: 2+2=4, so
    # Add3² targeting integer 4 is ONE((2,2)), not NONE. NULL.md is
    # not edited. Replay must keep this death.
    documented_dead = {
        "Q11": {"wanted": "N_add4_none", "got": "N_add4_one"},
    }
    surviving = dict(frozen)
    surviving["Q11"] = "N_add4_one"

    dispositions = {
        "Q1": classify_complete(and1),
        "Q2": classify_complete(and0),
        "Q3": classify_complete(xor1),
        "Q4": classify_complete(nand0),
        "Q5": classify_complete(const0_1),
        "Q7": classify_complete(c00),
        "Q8": classify_complete(c11),
        "Q9": ("OPEN", partial),
        "Q10": classify_complete(add2),
        "Q11": classify_complete(add4),
        "Q12": classify_complete(xor0),
    }

    census = {
        "null_commit": NULL_COMMIT,
        "names": names,
        "frozen": frozen,
        "surviving": surviving,
        "documented_dead": documented_dead,
        "match": names == frozen,
        "match_surviving": names == surviving,
        "X2": [list(p) for p in X2],
        "X3": [list(p) for p in X3],
        "and1": [list(p) for p in and1],
        "and0": [list(p) for p in and0],
        "and0_product": [list(p) for p in and0_product],
        "xor1": [list(p) for p in xor1],
        "xor0": [list(p) for p in xor0],
        "nand0": [list(p) for p in nand0],
        "const0_1": [list(p) for p in const0_1],
        "c00": [list(p) for p in c00],
        "c00_product": [list(p) for p in c00_product],
        "c11": [list(p) for p in c11],
        "add2": [list(p) for p in add2],
        "add4": [list(p) for p in add4],
        "partial": [list(p) for p in partial],
        "partial_complete": partial_complete,
        "partial_scanned": partial_scanned,
        "dispositions": {
            q: {"kind": kind, "family": [list(p) for p in family]}
            for q, (kind, family) in dispositions.items()
        },
        "Q6_joint_equals_product": and0 == and0_product,
        "hostile_representative_rejected": {
            "Q2": names["Q2"] != "N_and0_rep",
            "Q3": names["Q3"] != "N_xor1_rep",
            "Q7": names["Q7"] != "N_c00_rep",
            "Q8": names["Q8"] != "N_c11_rep",
            "Q9": names["Q9"] != "N_partial_one",
            "Q10": names["Q10"] != "N_add2_rep",
            "Q12": names["Q12"] != "N_xor0_class",
        },
    }

    path = HERE / "CENSUS.json"
    path.write_text(json.dumps(census, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    unexpected = {
        q: {"got": names[q], "wanted": surviving[q]}
        for q in surviving
        if names[q] != surviving[q]
    }
    if unexpected:
        raise SystemExit("frozen_null_miss: " + json.dumps(unexpected, sort_keys=True))
    if names["Q11"] != "N_add4_one" or add4 != ((2, 2),):
        raise SystemExit("q11_death_not_held")
    if names["Q11"] == frozen["Q11"]:
        raise SystemExit("q11_death_silently_revived")

    print("PASS")
    print("null_commit", NULL_COMMIT)
    for q in ("Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "Q8", "Q9", "Q10", "Q11", "Q12"):
        extra = ""
        if q in dispositions:
            kind, family = dispositions[q]
            extra = " " + kind + " " + str(family)
        print(q, names[q] + extra)


if __name__ == "__main__":
    main()
