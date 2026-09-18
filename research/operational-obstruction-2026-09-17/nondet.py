"""First probe of NONDET obstruction fibers.

The PARTIAL oracle in obstruction.py admits only rprm.futures.Machine:
deterministic partial maps. A successor-set table is a new carrier.
FIVE.future is not this instrument and is not defined on that carrier.

Deadlock is the empty successor set. It is not a separate enabledness port.
"""
from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType

from rprm.core import AdmissionError, atom, carrier, require, total_table
from rprm.futures import Machine

NONDET_CLAUSES = ("observation", "successor_blocks")


@dataclass(frozen=True)
class NondetMachine:
    """Finite total nondeterministic machine. Every state has a successor set."""

    states: tuple
    actions: tuple
    observation: object
    transitions: object

    def __post_init__(self):
        carrier(self.states)
        require(type(self.actions) is tuple and all(type(a) is str and a for a in self.actions)
                and len(set(self.actions)) == len(self.actions), "Actions need distinct nonempty names")
        total_table(self.states, self.observation, "Observation")
        require(type(self.transitions) is dict
                and all(type(a) is str for a in self.transitions)
                and set(self.transitions) == set(self.actions),
                "Every action needs exactly one successor-set table")
        tables = {}
        for action, table in self.transitions.items():
            require(type(table) is dict, "Successor-set table must be a dictionary")
            total_table(self.states, table, "Successor sets for " + action)
            frozen = {}
            for source, successors in table.items():
                require(type(successors) is frozenset, "Successors must be an exact set")
                for target in successors:
                    atom(target)
                    require(target in self.states, "Successor leaves the carrier")
                frozen[source] = frozenset(successors)
            tables[action] = MappingProxyType(frozen)
        object.__setattr__(self, "observation", MappingProxyType(dict(self.observation)))
        object.__setattr__(self, "transitions", MappingProxyType(tables))


def require_nondet_machine(machine):
    require(type(machine) is NondetMachine, "NondetMachine required")


def require_nondet_summary(machine, summary):
    require_nondet_machine(machine)
    total_table(machine.states, summary, "Summary")
    for value in summary.values():
        atom(value)


def block_image(summary, successors):
    return frozenset(summary[state] for state in successors)


def pair_clause_nondet(machine, left, right, summary):
    """Earliest NONDET failure for one unordered C-pair, or 'pass'.

    Observation first. Then successor-block sets. There is no enabledness
    clause: the successor table is total, and deadlock is the empty set.
    """
    require_nondet_summary(machine, summary)
    atom(left)
    atom(right)
    require(left in machine.states and right in machine.states, "Unadmitted pair")
    if machine.observation[left] != machine.observation[right]:
        return "observation"
    for action in machine.actions:
        left_blocks = block_image(summary, machine.transitions[action][left])
        right_blocks = block_image(summary, machine.transitions[action][right])
        if left_blocks != right_blocks:
            return "successor_blocks"
    return "pass"


def merged_pairs_nondet(machine, summary):
    require_nondet_summary(machine, summary)
    pairs = []
    states = machine.states
    for i, left in enumerate(states):
        for right in states[i + 1:]:
            if summary[left] == summary[right]:
                pairs.append((left, right))
    return tuple(pairs)


def obstruction_fiber_nondet(machine, summary):
    """Complete NONDET obstruction of a proposed summary.

    OPEN_NEW_CARRIER relative to the PARTIAL oracle: this function does not
    accept rprm.futures.Machine, and obstruction_fiber does not accept
    NondetMachine.
    """
    require_nondet_summary(machine, summary)
    failures = []
    passed = 0
    for left, right in merged_pairs_nondet(machine, summary):
        clause = pair_clause_nondet(machine, left, right, summary)
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
    by_clause = {clause: 0 for clause in NONDET_CLAUSES}
    for row in failures:
        by_clause[row["clause"]] += 1
    return {
        "status": status,
        "pairs": failures,
        "merged": passed + len(failures),
        "passed": passed,
        "by_clause": by_clause,
        "kind": "NONDET",
        "five_future": "OPEN_NEW_CARRIER",
    }


def is_operational_fold_nondet(machine, summary):
    return obstruction_fiber_nondet(machine, summary)["status"] == "NONE"


def as_partial_machine(machine):
    """Singleton-valued encoding, or admission error if some set is not a singleton.

    Empty sets and branching sets are not partial maps. That is the point
    of OPEN_NEW_CARRIER: deadlock and branching do not become enabledness.
    """
    require_nondet_machine(machine)
    tables = {}
    for action in machine.actions:
        table = {}
        for state in machine.states:
            successors = machine.transitions[action][state]
            if len(successors) != 1:
                raise AdmissionError("Successor set is not a singleton; not a PARTIAL map")
            table[state] = next(iter(successors))
        tables[action] = table
    return Machine(machine.states, machine.actions, dict(machine.observation), tables)
