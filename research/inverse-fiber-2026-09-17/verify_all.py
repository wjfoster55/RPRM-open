"""Exact census of every Boolean extra on XOR=1 and C=(0,0).

Does not import rprm or the other tonight trees. Null names are those
frozen in NULL-ALL.md at commit 2069b6f. This script lists all 16 and
all 256 tables; it does not sample.
"""
from pathlib import Path
import itertools
import json

HERE = Path(__file__).resolve().parent
NULL_COMMIT = "2069b6f6293c33923a28a4fa44d83a32c3c3d5c3"

XOR1 = ((0, 1), (1, 0))
C00 = ((0, 0, 0), (1, 1, 1))
X2 = ((0, 0), (0, 1), (1, 0), (1, 1))
X3 = tuple(itertools.product((0, 1), repeat=3))

EXPECTED_XOR1_TABLES = (
    (0, 0, 1, 0),
    (0, 0, 1, 1),
    (0, 1, 0, 0),
    (0, 1, 0, 1),
    (1, 0, 1, 0),
    (1, 0, 1, 1),
    (1, 1, 0, 0),
    (1, 1, 0, 1),
)


def table_of(domain, bits):
    if len(bits) != len(domain):
        raise ValueError("table_width")
    return dict(zip(domain, bits))


def apply_table(tab, point):
    return tab[point]


def splits_to_one(fiber, tab):
    vals = tuple(apply_table(tab, p) for p in fiber)
    return len(set(vals)) == len(fiber) and len(fiber) > 1


def all_tables(domain):
    width = len(domain)
    for bits in itertools.product((0, 1), repeat=width):
        yield bits, table_of(domain, bits)


def linear_form(weights, point):
    return sum((w * x for w, x in zip(weights, point)), 0) % 2


def affine_table(domain, weights, const):
    return tuple((linear_form(weights, p) + const) % 2 for p in domain)


def main():
    xor1_split = []
    xor1_const = []
    for bits, tab in all_tables(X2):
        if splits_to_one(XOR1, tab):
            xor1_split.append(bits)
        else:
            xor1_const.append(bits)

    c00_split_n = 0
    c00_const_n = 0
    for bits, tab in all_tables(X3):
        if splits_to_one(C00, tab):
            c00_split_n += 1
        else:
            c00_const_n += 1

    if len(xor1_split) + len(xor1_const) != 16:
        raise SystemExit("bits2_not_16")
    if c00_split_n + c00_const_n != 256:
        raise SystemExit("bits3_not_256")

    xor_table = (0, 1, 1, 0)
    xor_splits = splits_to_one(XOR1, table_of(X2, xor_table))

    lin2 = {(1, 0), (0, 1)}
    affine_xor1 = []
    for weights in itertools.product((0, 1), repeat=2):
        for const in (0, 1):
            bits = affine_table(X2, weights, const)
            if splits_to_one(XOR1, table_of(X2, bits)):
                affine_xor1.append((weights, const, bits))

    lin2_split_tables = tuple(
        affine_table(X2, w, 0) for w in sorted(lin2)
    )
    xor1_is_just_lin = tuple(xor1_split) == tuple(sorted(lin2_split_tables))

    lin3_odd = []
    for weights in itertools.product((0, 1), repeat=3):
        if sum(weights) % 2 == 1:
            lin3_odd.append(weights)
    lin3_split_n = 0
    for weights in lin3_odd:
        bits = affine_table(X3, weights, 0)
        if splits_to_one(C00, table_of(X3, bits)):
            lin3_split_n += 1
    c00_is_just_lin = c00_split_n == lin3_split_n

    aff_names = []
    for weights, const, bits in affine_xor1:
        label = []
        if weights == (1, 0):
            label.append("x")
        elif weights == (0, 1):
            label.append("y")
        elif weights == (1, 1):
            label.append("x+y")
        elif weights == (0, 0):
            label.append("0")
        if const:
            label.append("1")
        aff_names.append("+".join(label) if label else "0")

    names = {}
    n16 = len(xor1_split)
    if n16 == 8:
        names["QA1"] = "N_xor1_8"
    elif n16 == 2:
        names["QA1"] = "N_xor1_2"
    elif n16 == 3:
        names["QA1"] = "N_xor1_3"
    elif n16 == 4:
        names["QA1"] = "N_xor1_4"
    else:
        names["QA1"] = "N_xor1_unexpected"

    names["QA2"] = "N_xor1_just_lin" if xor1_is_just_lin else "N_xor1_not_lin"
    names["QA3"] = "N_par2_splits" if xor_splits else "N_par2_const"

    if c00_split_n == 128:
        names["QA4"] = "N_c00_128"
    elif c00_split_n == 5:
        names["QA4"] = "N_c00_5"
    elif c00_split_n == 4:
        names["QA4"] = "N_c00_4"
    elif c00_split_n == 8:
        names["QA4"] = "N_c00_8"
    else:
        names["QA4"] = "N_c00_unexpected"

    names["QA5"] = "N_c00_just_lin" if c00_is_just_lin else "N_c00_not_lin"

    xor1_tuple = tuple(xor1_split)
    if xor1_tuple == EXPECTED_XOR1_TABLES:
        names["QA6"] = "N_xor1_tables8"
    elif xor1_tuple == ((0, 0, 1, 1), (0, 1, 0, 1)):
        names["QA6"] = "N_xor1_xy_only"
    elif xor_table in xor1_tuple and (0, 0, 1, 1) in xor1_tuple:
        names["QA6"] = "N_xor1_coord_par"
    else:
        names["QA6"] = "N_xor1_tables_unexpected"

    if len(xor1_const) == 8 and c00_const_n == 128:
        names["QA7"] = "N_const_half"
    elif len(xor1_const) == 0 and c00_const_n == 0:
        names["QA7"] = "N_const_none"
    else:
        names["QA7"] = "N_const_unexpected"

    aff_set = set(aff_names)
    if aff_set == {"x", "y", "x+1", "y+1"}:
        names["QA8"] = "N_aff_xy_flips"
    elif aff_set == {"x", "y"}:
        names["QA8"] = "N_aff_xy_only"
    elif len(affine_xor1) == 8:
        names["QA8"] = "N_aff_all8"
    else:
        names["QA8"] = "N_aff_unexpected"

    frozen = {
        "QA1": "N_xor1_8",
        "QA2": "N_xor1_not_lin",
        "QA3": "N_par2_const",
        "QA4": "N_c00_128",
        "QA5": "N_c00_not_lin",
        "QA6": "N_xor1_tables8",
        "QA7": "N_const_half",
        "QA8": "N_aff_xy_flips",
    }

    census = {
        "null_commit": NULL_COMMIT,
        "names": names,
        "frozen": frozen,
        "match": names == frozen,
        "xor1_split_count": n16,
        "xor1_const_count": len(xor1_const),
        "xor1_split_tables": [list(t) for t in xor1_split],
        "xor1_const_tables": [list(t) for t in xor1_const],
        "c00_split_count": c00_split_n,
        "c00_const_count": c00_const_n,
        "bits2_total": 16,
        "bits3_total": 256,
        "xor_table": list(xor_table),
        "xor_splits_xor1": xor_splits,
        "linear_duals_xor1": [[1, 0], [0, 1]],
        "linear_duals_c00_count": len(lin3_odd),
        "xor1_equals_linear_duals": xor1_is_just_lin,
        "c00_equals_linear_duals": c00_is_just_lin,
        "affine_xor1_splitters": aff_names,
        "criterion": "D_splits_to_ONE_iff_D_differs_on_the_two_members",
    }

    path = HERE / "CENSUS-ALL.json"
    path.write_text(json.dumps(census, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    if names != frozen:
        dead = {q: {"got": names[q], "wanted": frozen[q]} for q in frozen if names[q] != frozen[q]}
        raise SystemExit("frozen_null_miss: " + json.dumps(dead, sort_keys=True))

    print("PASS")
    print("null_commit", NULL_COMMIT)
    for q in ("QA1", "QA2", "QA3", "QA4", "QA5", "QA6", "QA7", "QA8"):
        print(q, names[q])
    print("xor1_split", n16, "of 16")
    print("c00_split", c00_split_n, "of 256")
    print("affine_xor1", aff_names)


if __name__ == "__main__":
    main()
