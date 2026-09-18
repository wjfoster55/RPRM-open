"""Independent census of budget-k observation panels on the four-state layer.

Does not import rprm, AD-R3, obstruction, fluid, Hamming, or BSD trees.
Null names are those frozen in NULL.md. This script computes the fibers;
it does not choose a predicted count after seeing them.
"""
from itertools import combinations, product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

STATES = ((0, 0), (1, 0), (0, 1), (1, 1))
PORT_NAMES = ("H", "R", "R2", "X", "Z")
HOSTILE_MORE = ("R", "R2", "Z")
TICK_WORDS = ((), ("tick",), ("tick", "tick"), ("tick", "tick", "tick"))
REVEAL_WORDS = ((), ("reveal",), ("tick",))


def q_hidden(state):
    r, h = state
    return h


def port_value(name, state):
    r, h = state
    if name == "H":
        return h
    if name == "R" or name == "R2":
        return r
    if name == "X":
        return r ^ h
    if name == "Z":
        return 0
    raise ValueError("unknown_port")


def tick(state):
    r, h = state
    return (1 - r, 1 - h)


def reveal(state):
    r, h = state
    return (h, h)


def step(state, action):
    if action == "tick":
        return tick(state)
    if action == "reveal":
        return reveal(state)
    raise ValueError("unknown_action")


def execute(state, word):
    current = state
    for action in word:
        current = step(current, action)
    return current


def static_code(panel, state):
    return tuple(port_value(name, state) for name in panel)


def trace_code(panel, state, words):
    return tuple(static_code(panel, execute(state, word)) for word in words)


def fibers(panel, coder):
    buckets = {}
    for state in STATES:
        key = coder(panel, state)
        buckets.setdefault(key, []).append(state)
    return buckets


def sufficient(family):
    for members in family.values():
        answers = {q_hidden(state) for state in members}
        if len(answers) > 1:
            return False
    return True


def splitting_pairs(family):
    pairs = []
    for members in family.values():
        for i, left in enumerate(members):
            for right in members[i + 1:]:
                if q_hidden(left) != q_hidden(right):
                    pairs.append((left, right))
    return tuple(pairs)


def require(condition, name):
    if not condition:
        raise AssertionError(name)


def classify_singleton_count(count):
    names = {5: "N_all5", 2: "N_HX", 1: "N_H", 0: "N_none"}
    return names.get(count, "UNNAMED_COUNT")


def classify_pair_count(count):
    names = {10: "N_pairs_all", 4: "N_pairs_H", 6: "N_pairs_HX", 5: "N_pairs_5"}
    return names.get(count, "UNNAMED_COUNT")


def panel_key(panel):
    return tuple(sorted(panel, key=PORT_NAMES.index))


def main():
    require("rprm" not in globals(), "no_rprm_import")
    require(len(PORT_NAMES) == 5, "five_named_ports")
    require(len(STATES) == 4, "four_states")
    require(PORT_NAMES.index("R") != PORT_NAMES.index("R2"), "R_and_R2_are_distinct_occurrences")
    require(all(port_value("R", s) == port_value("R2", s) for s in STATES), "R_and_R2_agree_in_value")
    require(not all(port_value("R", s) == port_value("H", s) for s in STATES), "R_is_not_H")

    singletons = [panel_key((name,)) for name in PORT_NAMES]
    require(len(singletons) == 5, "complete_singleton_carrier")
    pairs = [panel_key(panel) for panel in combinations(PORT_NAMES, 2)]
    require(len(pairs) == 10, "complete_pair_carrier")

    singleton_records = []
    for panel in singletons:
        family = fibers(panel, static_code)
        singleton_records.append({
            "panel": list(panel),
            "sufficient": sufficient(family),
            "splitting_pairs": [[list(a), list(b)] for a, b in splitting_pairs(family)],
            "fibers": {"".join(str(bit) for bit in key): [list(s) for s in members]
                       for key, members in family.items()},
        })
    sufficient_singletons = [tuple(record["panel"]) for record in singleton_records if record["sufficient"]]
    q1_count = len(sufficient_singletons)
    q1_null = classify_singleton_count(q1_count)

    hostile_panel = panel_key(HOSTILE_MORE)
    hostile_family = fibers(hostile_panel, static_code)
    hostile_ok = sufficient(hostile_family)
    hostile_pairs = splitting_pairs(hostile_family)
    q2_null = "N_more_helps" if hostile_ok else "N_redundant"
    ghost_null = "N_ghost_00_01" if hostile_pairs == (((0, 0), (0, 1)),) else "N_ghost_other"

    tick_family = fibers(("R",), lambda panel, state: trace_code(panel, state, TICK_WORDS))
    tick_ok = sufficient(tick_family)
    q3_null = "N_time_helps" if tick_ok else "N_layer"
    tick_pairs = splitting_pairs(tick_family)

    pair_records = []
    for panel in pairs:
        family = fibers(panel, static_code)
        pair_records.append({
            "panel": list(panel),
            "sufficient": sufficient(family),
            "contains_H": "H" in panel,
            "splitting_pairs": [[list(a), list(b)] for a, b in splitting_pairs(family)],
        })
    sufficient_pairs = [tuple(record["panel"]) for record in pair_records if record["sufficient"]]
    q4_count = len(sufficient_pairs)
    q4_null = classify_pair_count(q4_count)

    reveal_family = fibers(("R",), lambda panel, state: trace_code(panel, state, REVEAL_WORDS))
    reveal_ok = sufficient(reveal_family)
    q5_null = "N_reveal_separates" if reveal_ok else "N_still_hidden"

    require(all(len(word) <= 3 and set(word) <= {"tick"} for word in TICK_WORDS), "q3_tick_only")
    require(any("reveal" in word for word in REVEAL_WORDS), "q5_has_reveal")
    require(("reveal",) not in TICK_WORDS, "q3_has_no_reveal")
    for state in STATES:
        require(port_value("H", state) == q_hidden(state), "H_is_Q")
        require(q_hidden(state) == (port_value("R", state) ^ port_value("X", state)), "h_equals_R_XOR_X")
    for record in singleton_records:
        family = fibers(tuple(record["panel"]), static_code)
        require(sorted(state for members in family.values() for state in members) == sorted(STATES),
                "each_singleton_covers_all_sources")
        require(record["sufficient"] == (not record["splitting_pairs"]), "sufficient_iff_no_split")

    receipt = {
        "status": "PASS",
        "evidence_grade": "FINITE_EXHAUSTIVE_CENSUS",
        "claim": "OB-k",
        "null_commit": "e758dd33b25384d9b7eaa13a57127c619b3f6256",
        "Q1": {
            "question": "how many of 5 singletons are sufficient for Q=h",
            "count": q1_count,
            "sufficient_panels": [list(panel) for panel in sufficient_singletons],
            "surviving_null": q1_null,
            "rejected_nulls": [name for name in ("N_all5", "N_HX", "N_H", "N_none") if name != q1_null],
            "count_disposition": f"ONE({q1_count})" if q1_count else "NONE",
            "selection_disposition": ("NONE", "ONE", "MANY")[min(q1_count, 2)],
            "records": singleton_records,
        },
        "Q2": {
            "question": "is HOSTILE_MORE={R,R2,Z} sufficient",
            "panel": list(hostile_panel),
            "sufficient": hostile_ok,
            "surviving_null": q2_null,
            "ghost_null": ghost_null,
            "disposition": "ONE(yes)" if hostile_ok else "NONE",
            "splitting_pairs": [[list(a), list(b)] for a, b in hostile_pairs],
            "fibers": {"".join(str(bit) for bit in key): [list(s) for s in members]
                       for key, members in hostile_family.items()},
        },
        "Q3": {
            "question": "does {R} with tick-only horizon 3 determine h",
            "sufficient": tick_ok,
            "surviving_null": q3_null,
            "disposition": "ONE(yes)" if tick_ok else "NONE",
            "splitting_pairs": [[list(a), list(b)] for a, b in tick_pairs],
            "traces": [
                {
                    "state": list(state),
                    "readings": [port_value("R", execute(state, word)) for word in TICK_WORDS],
                }
                for state in STATES
            ],
        },
        "Q4": {
            "question": "how many of 10 pairs are sufficient for Q=h",
            "count": q4_count,
            "sufficient_panels": [list(panel) for panel in sufficient_pairs],
            "surviving_null": q4_null,
            "rejected_nulls": [name for name in ("N_pairs_all", "N_pairs_H", "N_pairs_HX", "N_pairs_5")
                               if name != q4_null],
            "count_disposition": f"ONE({q4_count})" if q4_count else "NONE",
            "selection_disposition": ("NONE", "ONE", "MANY")[min(q4_count, 2)],
            "records": pair_records,
        },
        "Q5": {
            "question": "does {R} with tick+reveal horizon 1 determine h",
            "sufficient": reveal_ok,
            "surviving_null": q5_null,
            "disposition": "ONE(yes)" if reveal_ok else "NONE",
            "splitting_pairs": [[list(a), list(b)] for a, b in splitting_pairs(reveal_family)],
            "fibers": {str(key): [list(s) for s in members] for key, members in reveal_family.items()},
        },
        "limits": (
            "Complete census of five named ports on the four-state relational-layer "
            "machine only. Not AD-R3, not Kalman rank, not a general soundness proof "
            "of this script."
        ),
    }
    (HERE / "CENSUS.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    return receipt


if __name__ == "__main__":
    print(json.dumps(main(), indent=2))
