"""Exact tests of a toy measurement contract on Count2, Mean2, and FourState.

Does not import rprm, obstruction, fluid, Hamming, observability, Markov,
inverse-fiber, or BSD. Null names are those frozen in NULL.md at commit
0256331. This script enumerates declared domains; it does not choose a
predicted name after seeing a representative.
"""
from fractions import Fraction
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
NULL_COMMIT = "0256331836de226ae5b5e6534c462e45e128403c"

X = ((0, 0), (0, 1), (1, 0), (1, 1))
DISABLED = "disabled"
F = Fraction


def XOR(ab):
    a, b = ab
    return 1 if a != b else 0


def AND(ab):
    a, b = ab
    return 1 if a == 1 and b == 1 else 0


def FST(ab):
    return ab[0]


def C_sum(ab):
    a, b = ab
    return a + b


def C_mean(ab):
    a, b = ab
    return F(a + b, 2)


def C4(ab):
    a, b = ab
    return a + 2 * b


def fiber(domain, fn, target):
    return tuple(x for x in domain if fn(x) == target)


def partition_sets(domain, fn):
    buckets = {}
    for x in domain:
        buckets.setdefault(fn(x), []).append(x)
    return {frozenset(members) for members in buckets.values()}


def constant_on_fibers(domain, display, question):
    seen = {}
    for x in domain:
        z = display(x)
        q = question(x)
        if z in seen and seen[z] != q:
            return False
        seen[z] = q
    return True


def product_of_marginals(pairs):
    first = tuple(sorted({a for a, _ in pairs}))
    second = tuple(sorted({b for _, b in pairs}))
    return tuple((a, b) for a in first for b in second)


def classify_complete(family):
    if len(family) == 0:
        return "NONE", family
    if len(family) == 1:
        return "ONE", family
    return "MANY", family


def mean2_instrument(ports):
    if "a" not in ports or "b" not in ports:
        return DISABLED
    if ports["a"] not in (0, 1) or ports["b"] not in (0, 1):
        raise ValueError("bit_out_of_carrier")
    return F(ports["a"] + ports["b"], 2)


def decoder_on_image(domain, display, question):
    table = {}
    for x in domain:
        z = display(x)
        q = question(x)
        if z in table and table[z] != q:
            return None
        table[z] = q
    return {str(z): q for z, q in sorted(table.items(), key=lambda item: (float(item[0]), item[1]))}


def main():
    if set(X) != {(0, 0), (0, 1), (1, 0), (1, 1)}:
        raise SystemExit("bits2_not_ordered_pairs")
    if any(isinstance(bit, bool) for pair in X for bit in pair):
        raise SystemExit("booleans_as_ints")
    if C_mean((0, 1)) != F(1, 2) or type(C_mean((0, 1))) is not F:
        raise SystemExit("mean2_not_fraction")
    if C4((1, 1)) == (1 + 2 * 1) % 4 and C4((1, 1)) != 3:
        raise SystemExit("fourstate_wrap")

    xor_const = constant_on_fibers(X, C_sum, XOR)
    mean_eq_xor = all(C_mean(x) == XOR(x) for x in X)
    sum1 = fiber(X, C_sum, 1)
    sum0 = fiber(X, C_sum, 0)
    sum2 = fiber(X, C_sum, 2)
    sum1_product = product_of_marginals(sum1)
    fst_const = constant_on_fibers(X, C_sum, FST)
    c4_1 = fiber(X, C4, 1)
    c4_2 = fiber(X, C4, 2)
    c4_0 = fiber(X, C4, 0)
    c4_3 = fiber(X, C4, 3)
    same_kernel = partition_sets(X, C_sum) == partition_sets(X, C_mean)
    mean_image = tuple(sorted({C_mean(x) for x in X}))
    xor_as_fraction_image = {F(0), F(1)}
    mean_is_sure_bernoulli = set(mean_image) <= xor_as_fraction_image
    missing_b = mean2_instrument({"a": 1})
    both_ports = mean2_instrument({"a": 1, "b": 0})
    count_is_car = all(len(fiber(X, C_sum, z)) == 1 for z in (0, 1, 2) if fiber(X, C_sum, z))
    four_is_car = all(len(fiber(X, C4, z)) == 1 for z in (0, 1, 2, 3))
    and_const = constant_on_fibers(X, C_sum, AND)
    xor_decoder = decoder_on_image(X, C_sum, XOR)
    xor_mean_decoder = decoder_on_image(X, C_mean, XOR)

    names = {
        "Q1": "N_xor_const" if xor_const else "N_xor_split",
        "Q2": "N_mean_is_xor" if mean_eq_xor else "N_mean_not_xor",
        "Q3": "N_sum1_many" if sum1 == ((0, 1), (1, 0)) else "N_sum1_rep" if sum1 == ((0, 1),) else "N_sum1_unexpected",
        "Q4": "N_sum1_joint" if sum1 != sum1_product else "N_sum1_factor",
        "Q5": "N_fst_const" if fst_const else "N_fst_split",
        "Q6": "N_c4_1_one" if c4_1 == ((1, 0),) else "N_c4_1_many",
        "Q7": "N_c4_2_one" if c4_2 == ((0, 1),) else "N_c4_2_sum" if c4_2 == ((1, 0),) else "N_c4_2_unexpected",
        "Q8": "N_sum0_one" if sum0 == ((0, 0),) else "N_sum0_none",
        "Q9": "N_same_kernel" if same_kernel else "N_diff_kernel",
        "Q10": "N_unit_prob" if mean_is_sure_bernoulli else "N_unit_count",
        "Q11": "N_en_disabled" if missing_b == DISABLED else "N_en_one",
        "Q12": "N_count_car" if count_is_car else "N_count_fold",
    }

    frozen = {
        "Q1": "N_xor_const",
        "Q2": "N_mean_not_xor",
        "Q3": "N_sum1_many",
        "Q4": "N_sum1_joint",
        "Q5": "N_fst_split",
        "Q6": "N_c4_1_one",
        "Q7": "N_c4_2_one",
        "Q8": "N_sum0_one",
        "Q9": "N_same_kernel",
        "Q10": "N_unit_count",
        "Q11": "N_en_disabled",
        "Q12": "N_count_fold",
    }

    if both_ports != F(1, 2):
        raise SystemExit("enabled_mean_wrong")
    if four_is_car is not True:
        raise SystemExit("fourstate_not_car")
    if and_const is not True:
        raise SystemExit("and_not_constant_on_count2")

    dispositions = {
        "Q3": classify_complete(sum1),
        "Q6": classify_complete(c4_1),
        "Q7": classify_complete(c4_2),
        "Q8": classify_complete(sum0),
        "Q11": ("DISABLED", ()),
        "Q12": classify_complete(sum1),
    }

    census = {
        "null_commit": NULL_COMMIT,
        "names": names,
        "frozen": frozen,
        "match": names == frozen,
        "X": [list(p) for p in X],
        "xor_const": xor_const,
        "mean_eq_xor": mean_eq_xor,
        "xor_decoder_on_count2": xor_decoder,
        "xor_decoder_on_mean2": xor_mean_decoder,
        "sum0": [list(p) for p in sum0],
        "sum1": [list(p) for p in sum1],
        "sum2": [list(p) for p in sum2],
        "sum1_product": [list(p) for p in sum1_product],
        "fst_const": fst_const,
        "and_const": and_const,
        "c4_0": [list(p) for p in c4_0],
        "c4_1": [list(p) for p in c4_1],
        "c4_2": [list(p) for p in c4_2],
        "c4_3": [list(p) for p in c4_3],
        "same_kernel": same_kernel,
        "mean_image": [str(v) for v in mean_image],
        "mean_is_sure_bernoulli": mean_is_sure_bernoulli,
        "missing_b": missing_b,
        "both_ports": str(both_ports),
        "count_is_car": count_is_car,
        "four_is_car": four_is_car,
        "pointwise_mean_vs_xor": {
            str(list(x)): {"mean": str(C_mean(x)), "xor": XOR(x)} for x in X
        },
        "dispositions": {
            q: {"kind": kind, "family": [list(p) for p in family]}
            for q, (kind, family) in dispositions.items()
        },
        "hostile_rejected": {
            "Q2": names["Q2"] != "N_mean_is_xor",
            "Q3": names["Q3"] != "N_sum1_rep",
            "Q4": names["Q4"] != "N_sum1_factor",
            "Q5": names["Q5"] != "N_fst_const",
            "Q10": names["Q10"] != "N_unit_prob",
            "Q11": names["Q11"] != "N_en_one",
            "Q12": names["Q12"] != "N_count_car",
        },
    }

    path = HERE / "CENSUS.json"
    path.write_text(json.dumps(census, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    if names != frozen:
        dead = {q: {"got": names[q], "wanted": frozen[q]} for q in frozen if names[q] != frozen[q]}
        raise SystemExit("frozen_null_miss: " + json.dumps(dead, sort_keys=True))

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
