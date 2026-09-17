"""Complete O05 obstruction fibers for finite deterministic partial machines.

`rprm.core.deterministic_quotient` returns the first failing pair.
`rprm.futures.shortest_witness` cannot see a successor-update failure that
leaves every tagged future observation equal. This module returns the
complete classified pair fiber, then NONE/ONE/MANY.
"""
from __future__ import annotations

from rprm.core import atom, require, total_table
from rprm.futures import Machine, shortest_witness, stable_refinement

CLAUSES = ("observation", "enabledness", "successor")


def require_machine(machine):
    require(type(machine) is Machine, "Machine required")


def require_summary(machine, summary):
    require_machine(machine)
    total_table(machine.states, summary, "Summary")
    for value in summary.values():
        atom(value)


def pair_clause(machine, left, right, summary):
    """Earliest O05 failure for one unordered C-pair, or 'pass'.

    Order is load-bearing: present observation, then enabledness, then
    retained successor. A pair may fail later clauses as well; those are
    not reported once an earlier clause already fails.
    """
    require_summary(machine, summary)
    atom(left)
    atom(right)
    require(left in machine.states and right in machine.states, "Unadmitted pair")
    if machine.observation[left] != machine.observation[right]:
        return "observation"
    for action in machine.actions:
        enabled_left = left in machine.transitions[action]
        enabled_right = right in machine.transitions[action]
        if enabled_left != enabled_right:
            return "enabledness"
        if enabled_left:
            next_left = machine.transitions[action][left]
            next_right = machine.transitions[action][right]
            if summary[next_left] != summary[next_right]:
                return "successor"
    return "pass"


def merged_pairs(machine, summary):
    require_summary(machine, summary)
    pairs = []
    states = machine.states
    for i, left in enumerate(states):
        for right in states[i + 1:]:
            if summary[left] == summary[right]:
                pairs.append((left, right))
    return tuple(pairs)


def obstruction_fiber(machine, summary):
    """Complete O05 obstruction of a proposed summary.

    Carrier of the fiber: unordered merged pairs. Readout: earliest clause.
    NONE means the admitted obstruction is empty, i.e. an operational fold.
    """
    failures = []
    passed = 0
    for left, right in merged_pairs(machine, summary):
        clause = pair_clause(machine, left, right, summary)
        if clause == "pass":
            passed += 1
        else:
            failures.append({"left": left, "right": right, "clause": clause})
    failures = tuple(failures)
    if not failures:
        status = "NONE"
    elif len(failures) == 1:
        status = "ONE"
    else:
        status = "MANY"
    by_clause = {clause: 0 for clause in CLAUSES}
    for row in failures:
        by_clause[row["clause"]] += 1
    return {
        "status": status,
        "pairs": failures,
        "merged": passed + len(failures),
        "passed": passed,
        "by_clause": by_clause,
    }


def is_operational_fold(machine, summary):
    return obstruction_fiber(machine, summary)["status"] == "NONE"


def same_kernel(left_summary, right_summary, states):
    total_table(states, left_summary, "Left summary")
    total_table(states, right_summary, "Right summary")
    for i, a in enumerate(states):
        for b in states[i + 1:]:
            if (left_summary[a] == left_summary[b]) != (right_summary[a] == right_summary[b]):
                return False
    return True


def least_stable_repair(machine, summary):
    """O09: coarsest operational fold refining the proposed summary."""
    require_summary(machine, summary)
    return stable_refinement(machine, summary)


def repaired_kernel_matches(machine, summary):
    repaired = least_stable_repair(machine, summary)
    return same_kernel(summary, {state: repaired["encoding"][state] for state in machine.states},
                       machine.states)


def ghost_fiber(machine, summary):
    """Merged pairs that are future-equivalent but fail one-step O05.

    FIVE.future returns NONE exactly when every tagged word observation
    agrees, including failure. Enabledness mismatches produce a FAIL vs OK
    word, so they never appear here. A one-step `pass` pair need not be
    future-equivalent unless every merged pair passes.
    """
    require_summary(machine, summary)
    ghosts = []
    for left, right in merged_pairs(machine, summary):
        clause = pair_clause(machine, left, right, summary)
        word = shortest_witness(machine, left, right)
        require(word["status"] in ("ONE", "NONE"), "Pair witness must be complete")
        if word["status"] == "NONE" and clause != "pass":
            require(clause == "successor", "Future-equivalent obstruction must be successor")
            ghosts.append({"left": left, "right": right, "clause": clause})
    ghosts = tuple(ghosts)
    if not ghosts:
        status = "NONE"
    elif len(ghosts) == 1:
        status = "ONE"
    else:
        status = "MANY"
    return {"status": status, "pairs": ghosts}


def is_future_sufficient(machine, summary):
    """Every merged pair has FIVE.future NONE."""
    require_summary(machine, summary)
    return all(shortest_witness(machine, left, right)["status"] == "NONE"
               for left, right in merged_pairs(machine, summary))


def is_ghost_fold(machine, summary):
    """Future-sufficient strict compression that still fails O05."""
    return is_future_sufficient(machine, summary) and not is_operational_fold(machine, summary)


def min_repair_alphabet(states, summary, question):
    """O08R: smallest tag alphabet repairing Q relative to C."""
    total_table(states, summary, "Summary")
    total_table(states, question, "Question")
    if not states:
        return 0
    blocks = {}
    for state in states:
        atom(summary[state])
        atom(question[state])
        blocks.setdefault(summary[state], set()).add(question[state])
    return max(len(values) for values in blocks.values())


def set_partitions(states):
    """All partitions of a finite tuple, each as a state-to-block-index map."""
    require(type(states) is tuple, "Carrier enumeration must be a tuple")
    n = len(states)
    if n == 0:
        yield {}
        return
    codes = [0] * n

    def walk(index, used):
        if index == n:
            yield {states[i]: codes[i] for i in range(n)}
            return
        for label in range(used):
            codes[index] = label
            yield from walk(index + 1, used)
        codes[index] = used
        yield from walk(index + 1, used + 1)

    yield from walk(0, 0)
