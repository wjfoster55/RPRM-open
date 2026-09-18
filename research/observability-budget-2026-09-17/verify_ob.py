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
FRESH_COPY = {"H": "H2", "R": "R3", "R2": "R3", "X": "X2", "Z": "Z2"}
COPY_BASE = {"H2": "H", "R3": "R", "X2": "X", "Z2": "Z"}
M_STATES = (0, 1, 2)
M_TABLE = {"A": (0, 0, 1), "A2": (0, 0, 1), "B": (0, 1, 1)}
DUP_NULL_COMMIT = "f535cd051d814613f0f4e7530fe8b099e7f6c111"
TIME_NULL_COMMIT = "784f27a72929b924324c04027407a58d069e32ed"
N_STATES = tuple((a, b, c) for a in (0, 1) for b in (0, 1) for c in (0, 1))
SHIFT_WORDS = ((), ("shift",), ("shift", "shift"))


def q_hidden(state):
    r, h = state
    return h


def port_value(name, state):
    r, h = state
    base = COPY_BASE.get(name, name)
    if base == "H":
        return h
    if base in ("R", "R2"):
        return r
    if base == "X":
        return r ^ h
    if base == "Z":
        return 0
    raise ValueError("unknown_port")


def m_question(state):
    return 1 if state == 1 else 0


def m_port(name, state):
    if name not in M_TABLE:
        raise ValueError("unknown_m_port")
    return M_TABLE[name][state]


def coded_fibers(states, panel, value_fn):
    buckets = {}
    for state in states:
        key = tuple(value_fn(name, state) for name in panel)
        buckets.setdefault(key, []).append(state)
    return buckets


def question_constant(family, question):
    for members in family.values():
        if len({question(state) for state in members}) > 1:
            return False
    return True


def n_question(state):
    return state[2]


def n_port(name, state):
    if name != "Y":
        raise ValueError("unknown_n_port")
    return state[0]


def n_shift(state):
    a, b, c = state
    return (b, c, 0)


def n_execute(state, word):
    current = state
    for action in word:
        require(action == "shift", "n_shift_only")
        current = n_shift(current)
    return current


def descends(states, panel, value_fn, act):
    successor = {}
    for state in states:
        code = tuple(value_fn(name, state) for name in panel)
        nxt = tuple(value_fn(name, act(state)) for name in panel)
        if code in successor and successor[code] != nxt:
            return False
        successor[code] = nxt
    return True


def function_of(states, panel, value_fn, query):
    seen = {}
    for state in states:
        code = tuple(value_fn(name, state) for name in panel)
        value = query(state)
        if code in seen and seen[code] != value:
            return False
        seen[code] = value
    return True


def same_partition(states, left_code, right_code):
    for i, x in enumerate(states):
        for y in states[i + 1:]:
            if (left_code(x) == left_code(y)) != (right_code(x) == right_code(y)):
                return False
    return True


def question_splits(family, question):
    pairs = []
    for members in family.values():
        for i, left in enumerate(members):
            for right in members[i + 1:]:
                if question(left) != question(right):
                    pairs.append((left, right))
    return tuple(pairs)


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


def port_order(name):
    if name in PORT_NAMES:
        return (0, PORT_NAMES.index(name))
    return (1, name)


def panel_key(panel):
    return tuple(sorted(panel, key=port_order))


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

    nonempty = [panel_key(panel) for n in range(1, 6) for panel in combinations(PORT_NAMES, n)]
    require(len(nonempty) == 31, "complete_nonempty_L_panels")
    dup_trials = []
    repairs = []
    for panel in nonempty:
        before = question_constant(coded_fibers(STATES, panel, port_value), q_hidden)
        for source_port in panel:
            fresh = FRESH_COPY[source_port]
            require(fresh not in panel, "fresh_copy_not_already_in_S")
            require(all(port_value(fresh, state) == port_value(source_port, state) for state in STATES),
                    "fresh_copy_agrees_everywhere")
            enlarged = panel_key(panel + (fresh,))
            after = question_constant(coded_fibers(STATES, enlarged, port_value), q_hidden)
            trial = {
                "panel": list(panel),
                "copied": source_port,
                "fresh": fresh,
                "before": before,
                "after": after,
            }
            dup_trials.append(trial)
            if after and not before:
                repairs.append(trial)
            require(after == before, "duplicate_changes_sufficiency")
    require(len(dup_trials) == 80, "eighty_L_duplication_trials")
    q6_null = "N_dup_repairs" if repairs else "N_dup_never"

    m_panels = {
        "A": ("A",),
        "A_A2": ("A", "A2"),
        "A_B": ("A", "B"),
    }
    m_ok = {
        name: question_constant(coded_fibers(M_STATES, panel, m_port), m_question)
        for name, panel in m_panels.items()
    }
    require(m_port("A", 0) == m_port("A2", 0) and m_port("A", 1) == m_port("A2", 1)
            and m_port("A", 2) == m_port("A2", 2), "A2_duplicates_A")
    require(m_port("B", 1) != m_port("A", 1), "B_differs_on_live_ghost")
    if (not m_ok["A"]) and (not m_ok["A_A2"]) and m_ok["A_B"]:
        q7_null = "N_look_copy"
    elif (not m_ok["A"]) and m_ok["A_A2"] and m_ok["A_B"]:
        q7_null = "N_look_any_second"
    elif (not m_ok["A"]) and (not m_ok["A_A2"]) and (not m_ok["A_B"]):
        q7_null = "N_look_none"
    else:
        q7_null = "UNNAMED_LOOK"

    r_trace = question_constant(
        fibers(("R",), lambda panel, state: trace_code(panel, state, TICK_WORDS)), q_hidden)
    r_r2_trace = question_constant(
        fibers(("R", "R2"), lambda panel, state: trace_code(panel, state, TICK_WORDS)), q_hidden)
    require(r_trace == tick_ok, "q8_r_trace_matches_q3")
    q8_null = "N_trace_copy_helps" if (r_r2_trace and not r_trace) else "N_trace_copy_never"
    require(r_trace == r_r2_trace, "trace_duplicate_changes_sufficiency")

    require(q1_null == "N_H" and q1_count == 1, "q1_disposition_unchanged")
    require(q2_null == "N_redundant" and not hostile_ok, "q2_disposition_unchanged")
    require(q3_null == "N_layer" and not tick_ok, "q3_disposition_unchanged")
    require(q4_null == "N_pairs_HX" and q4_count == 6, "q4_disposition_unchanged")
    require(q5_null == "N_reveal_separates" and reveal_ok, "q5_disposition_unchanged")
    require(q6_null == "N_dup_never" and not repairs, "q6_disposition_unchanged")
    require(q7_null == "N_look_copy", "q7_disposition_unchanged")
    require(q8_null == "N_trace_copy_never" and not r_r2_trace, "q8_disposition_unchanged")

    descending = []
    time_refinements = []
    for panel in nonempty:
        closed = descends(STATES, panel, port_value, tick)
        if closed:
            descending.append(panel)
        static_ok = question_constant(coded_fibers(STATES, panel, port_value), q_hidden)
        trace_ok = question_constant(
            fibers(panel, lambda current, state: trace_code(current, state, TICK_WORDS)), q_hidden)
        same = same_partition(
            STATES,
            lambda state, current=panel: static_code(current, state),
            lambda state, current=panel: trace_code(current, state, TICK_WORDS),
        )
        if closed:
            require(same, "descending_panel_time_refined_kernel")
            if (not static_ok) and (not same or trace_ok != static_ok):
                time_refinements.append(list(panel))
        require("reveal" not in "".join(action for word in TICK_WORDS for action in word),
                "q9_tick_only")
    q9_count = len(descending)
    q9_null = {31: "N_all31", 5: "N_sing5", 0: "N_none"}.get(q9_count, "UNNAMED_COUNT")
    q10_null = "N_time_closed_sometimes" if time_refinements else "N_time_closed_never"

    x_of_r = function_of(STATES, ("R",), port_value, lambda state: port_value("X", state))
    rx_ok = question_constant(coded_fibers(STATES, ("R", "X"), port_value), q_hidden)
    if (not x_of_r) and rx_ok:
        q11_null = "N_port_indep"
    elif x_of_r and rx_ok:
        q11_null = "N_port_dep"
    elif (not x_of_r) and (not rx_ok):
        q11_null = "N_port_fail"
    else:
        q11_null = "UNNAMED_PORT"

    require(len(N_STATES) == 8, "eight_shift_states")
    n_static = question_constant(coded_fibers(N_STATES, ("Y",), n_port), n_question)
    n_trace_family = {}
    for state in N_STATES:
        key = tuple(n_port("Y", n_execute(state, word)) for word in SHIFT_WORDS)
        n_trace_family.setdefault(key, []).append(state)
    n_trace_ok = question_constant(n_trace_family, n_question)
    if (not n_static) and n_trace_ok:
        q12_null = "N_shift_time"
    elif (not n_static) and (not n_trace_ok):
        q12_null = "N_shift_none"
    elif n_static and n_trace_ok:
        q12_null = "N_shift_already"
    else:
        q12_null = "UNNAMED_SHIFT"
    n_closed = descends(N_STATES, ("Y",), n_port, n_shift)
    q13_null = "N_shift_closed" if n_closed else "N_shift_open"

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
        "Q6": {
            "question": "does a value-copy ever repair an insufficient L panel",
            "trials": 80,
            "repairs": repairs,
            "surviving_null": q6_null,
            "disposition": "NONE" if not repairs else f"ONE({len(repairs)})",
            "grade": "THEOREM_RESTRICTED" if q6_null == "N_dup_never" else "COUNTEREXAMPLE",
            "dup_null_commit": DUP_NULL_COMMIT,
        },
        "Q7": {
            "question": "lookalike machine M: {A} vs {A,A2} vs {A,B}",
            "A": m_ok["A"],
            "A_A2": m_ok["A_A2"],
            "A_B": m_ok["A_B"],
            "surviving_null": q7_null,
            "disposition": "ONE(N_look_copy)" if q7_null == "N_look_copy" else f"ONE({q7_null})",
            "splitting_A": [[a, b] for a, b in question_splits(
                coded_fibers(M_STATES, ("A",), m_port), m_question)],
            "splitting_A_A2": [[a, b] for a, b in question_splits(
                coded_fibers(M_STATES, ("A", "A2"), m_port), m_question)],
            "splitting_A_B": [[a, b] for a, b in question_splits(
                coded_fibers(M_STATES, ("A", "B"), m_port), m_question)],
        },
        "Q8": {
            "question": "does {R,R2} tick-horizon 3 determine h if {R} does not",
            "R_sufficient": r_trace,
            "R_R2_sufficient": r_r2_trace,
            "surviving_null": q8_null,
            "disposition": "NONE" if not r_r2_trace else "ONE(yes)",
        },
        "Q9": {
            "question": "how many of 31 nonempty L-panels descend under tick",
            "count": q9_count,
            "surviving_null": q9_null,
            "disposition": f"ONE({q9_count})" if q9_count else "NONE",
            "time_null_commit": TIME_NULL_COMMIT,
        },
        "Q10": {
            "question": "does horizon-3 refine ker C_S for any descending insufficient L-panel",
            "refinements": time_refinements,
            "surviving_null": q10_null,
            "disposition": "NONE" if not time_refinements else f"ONE({len(time_refinements)})",
            "grade": "THEOREM_RESTRICTED" if q10_null == "N_time_closed_never" and q9_null == "N_all31" else "FINITE_CHECK",
        },
        "Q11": {
            "question": "is X a function of {R}, and is {R,X} sufficient",
            "X_of_R": x_of_r,
            "RX_sufficient": rx_ok,
            "surviving_null": q11_null,
            "disposition": "ONE(N_port_indep)" if q11_null == "N_port_indep" else f"ONE({q11_null})",
        },
        "Q12": {
            "question": "shift machine N: static {Y} vs horizon-2 {Y}",
            "static_sufficient": n_static,
            "horizon2_sufficient": n_trace_ok,
            "surviving_null": q12_null,
            "disposition": "ONE(N_shift_time)" if q12_null == "N_shift_time" else f"ONE({q12_null})",
            "splitting_static": [[list(a), list(b)] for a, b in question_splits(
                coded_fibers(N_STATES, ("Y",), n_port), n_question)],
        },
        "Q13": {
            "question": "does {Y} descend under shift",
            "descends": n_closed,
            "surviving_null": q13_null,
            "disposition": "NONE" if n_closed else "ONE(open)",
        },
        "limits": (
            "Complete census of five named ports on the four-state relational-layer "
            "machine, plus 80 value-copy trials, one three-state lookalike, and one "
            "eight-state shift. Not AD-R3, not Kalman rank, not a general soundness "
            "proof of this script."
        ),
    }
    (HERE / "CENSUS.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    return receipt


if __name__ == "__main__":
    print(json.dumps(main(), indent=2))
