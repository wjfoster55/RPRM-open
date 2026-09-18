"""Exact tests of named extra readouts that split MANY fibers to ONE.

Does not import rprm or the other tonight trees. Null names are those
frozen in NULL-VIEW.md at commit 14c5b8a. This script evaluates named
views on complete fibers; it does not choose a predicted name after
seeing a representative split.
"""
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
NULL_COMMIT = "14c5b8a60584897ccb07e5642b34edddb05f2e69"

XOR1 = ((0, 1), (1, 0))
C00 = ((0, 0, 0), (1, 1, 1))

BITS2_VIEWS = {
    "FST": lambda ab: ab[0],
    "SND": lambda ab: ab[1],
    "AND": lambda ab: 1 if ab[0] == 1 and ab[1] == 1 else 0,
    "OR": lambda ab: 1 if ab[0] == 1 or ab[1] == 1 else 0,
    "EQ": lambda ab: 1 if ab[0] == ab[1] else 0,
    "CONST0": lambda ab: 0,
}
BITS2_ORDER = ("FST", "SND", "AND", "OR", "EQ", "CONST0")

BITS3_VIEWS = {
    "X": lambda xyz: xyz[0],
    "Y": lambda xyz: xyz[1],
    "Z": lambda xyz: xyz[2],
    "PARITY": lambda xyz: xyz[0] ^ xyz[1] ^ xyz[2],
    "AND3": lambda xyz: 1 if xyz == (1, 1, 1) else 0,
    "C0": lambda xyz: xyz[0] ^ xyz[1],
}
BITS3_ORDER = ("X", "Y", "Z", "PARITY", "AND3", "C0")


def values_on(fiber, fn):
    return tuple(fn(p) for p in fiber)


def splits(fiber, fn):
    vals = values_on(fiber, fn)
    return len(set(vals)) > 1


def splits_to_one(fiber, fn):
    vals = values_on(fiber, fn)
    if len(set(vals)) != len(vals):
        return False
    return len(vals) > 1


def refined(fiber, fn, value):
    return tuple(p for p in fiber if fn(p) == value)


def splitting_family(fiber, menu, order):
    return tuple(name for name in order if splits_to_one(fiber, menu[name]))


def main():
    xor1_splitters = splitting_family(XOR1, BITS2_VIEWS, BITS2_ORDER)
    c00_splitters = splitting_family(C00, BITS3_VIEWS, BITS3_ORDER)
    and_splits = splits(XOR1, BITS2_VIEWS["AND"])
    or_splits = splits(XOR1, BITS2_VIEWS["OR"])
    fst_to_one = splits_to_one(XOR1, BITS2_VIEWS["FST"])
    fst0 = refined(XOR1, BITS2_VIEWS["FST"], 0)
    c0_splits = splits(C00, BITS3_VIEWS["C0"])
    x0 = refined(C00, BITS3_VIEWS["X"], 0)

    names = {}
    if xor1_splitters == ("FST", "SND"):
        names["QV1"] = "N_xor1_fst_snd"
    elif xor1_splitters == BITS2_ORDER:
        names["QV1"] = "N_xor1_all6"
    elif xor1_splitters == ("AND",):
        names["QV1"] = "N_xor1_and"
    elif xor1_splitters == ():
        names["QV1"] = "N_xor1_none"
    else:
        names["QV1"] = "N_xor1_unexpected"

    names["QV2"] = "N_and_splits" if and_splits else "N_and_const"
    names["QV3"] = "N_or_splits" if or_splits else "N_or_const"
    names["QV4"] = "N_fst_one" if fst_to_one else "N_fst_many"

    if fst0 == ((0, 1),):
        names["QV5"] = "N_fst0_one"
    elif fst0 == XOR1:
        names["QV5"] = "N_fst0_many"
    elif fst0 == ():
        names["QV5"] = "N_fst0_none"
    else:
        names["QV5"] = "N_fst0_unexpected"

    if c00_splitters == ("X", "Y", "Z", "PARITY", "AND3"):
        names["QV6"] = "N_c00_xyzpa"
    elif c00_splitters == ("X",):
        names["QV6"] = "N_c00_x_only"
    elif c00_splitters == BITS3_ORDER:
        names["QV6"] = "N_c00_all6"
    elif c00_splitters == ():
        names["QV6"] = "N_c00_none"
    else:
        names["QV6"] = "N_c00_unexpected"

    names["QV7"] = "N_c0_splits" if c0_splits else "N_c0_const"

    if x0 == ((0, 0, 0),):
        names["QV8"] = "N_x0_one"
    elif x0 == C00:
        names["QV8"] = "N_x0_many"
    elif x0 == ():
        names["QV8"] = "N_x0_none"
    else:
        names["QV8"] = "N_x0_unexpected"

    frozen = {
        "QV1": "N_xor1_fst_snd",
        "QV2": "N_and_const",
        "QV3": "N_or_const",
        "QV4": "N_fst_one",
        "QV5": "N_fst0_one",
        "QV6": "N_c00_xyzpa",
        "QV7": "N_c0_const",
        "QV8": "N_x0_one",
    }

    census = {
        "null_commit": NULL_COMMIT,
        "names": names,
        "frozen": frozen,
        "match": names == frozen,
        "xor1_splitters": list(xor1_splitters),
        "c00_splitters": list(c00_splitters),
        "xor1_values": {name: list(values_on(XOR1, BITS2_VIEWS[name])) for name in BITS2_ORDER},
        "c00_values": {name: list(values_on(C00, BITS3_VIEWS[name])) for name in BITS3_ORDER},
        "fst0": [list(p) for p in fst0],
        "x0": [list(p) for p in x0],
        "and_constant_on_xor1": not and_splits,
        "or_constant_on_xor1": not or_splits,
        "c0_constant_on_c00": not c0_splits,
        "eq_constant_on_xor1": not splits(XOR1, BITS2_VIEWS["EQ"]),
        "const0_constant_on_xor1": not splits(XOR1, BITS2_VIEWS["CONST0"]),
    }

    path = HERE / "CENSUS-VIEW.json"
    path.write_text(json.dumps(census, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    if names != frozen:
        dead = {q: {"got": names[q], "wanted": frozen[q]} for q in frozen if names[q] != frozen[q]}
        raise SystemExit("frozen_null_miss: " + json.dumps(dead, sort_keys=True))

    print("PASS")
    print("null_commit", NULL_COMMIT)
    for q in ("QV1", "QV2", "QV3", "QV4", "QV5", "QV6", "QV7", "QV8"):
        print(q, names[q])
    print("xor1_splitters", xor1_splitters)
    print("c00_splitters", c00_splitters)
    print("fst0", fst0)
    print("x0", x0)


if __name__ == "__main__":
    main()
