"""NONDET-LTS-01 obstruction oracle and the bounded n=2,3 family.

New required type: finite labeled transition systems as partial functions
into nonempty successor sets, plus an explicit empty-set deadlock value.
The PARTIAL oracle on rprm.futures.Machine does not stretch. FIVE.future
is not this instrument.

Contract: CONTRACT-NONDET.md
"""
from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType

import itertools as it

from rprm.core import AdmissionError, atom, carrier, require, total_table
from rprm.futures import Machine

CONTRACT = "NONDET-LTS-01"
NONDET_CLAUSES = ("observation", "enabledness", "successor_blocks")
PAIR_KINDS = (
    "observation",
    "deadlock_disabled",
    "disabled_live",
    "both_disabled",
    "both_deadlock",
    "deadlock_live",
    "branching",
    "singletons",
    "pass",
)
DISABLED = None


@dataclass(frozen=True)
class NondetMachine:
    """Finite LTS. Observation is total. Each action is a partial set table.

    Absent source: disabled. Present empty set: deadlock. Present nonempty
    set: live branching.
    """

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
            frozen = {}
            for source, successors in table.items():
                atom(source)
                require(source in self.states, "Source leaves the carrier")
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


def action_defined(machine, action, state):
    require_nondet_machine(machine)
    require(action in machine.actions, "Unadmitted action")
    return state in machine.transitions[action]


def successors(machine, action, state):
    require(action_defined(machine, action, state), "Action is disabled at this state")
    return machine.transitions[action][state]


def block_image(summary, landing):
    return frozenset(summary[state] for state in landing)


def pair_clause_nondet(machine, left, right, summary):
    """Earliest NONDET-LTS failure for one unordered C-pair, or 'pass'."""
    require_nondet_summary(machine, summary)
    atom(left)
    atom(right)
    require(left in machine.states and right in machine.states, "Unadmitted pair")
    if machine.observation[left] != machine.observation[right]:
        return "observation"
    for action in machine.actions:
        left_on = action_defined(machine, action, left)
        right_on = action_defined(machine, action, right)
        if left_on != right_on:
            return "enabledness"
        if left_on:
            left_blocks = block_image(summary, successors(machine, action, left))
            right_blocks = block_image(summary, successors(machine, action, right))
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
    """Complete NONDET-LTS obstruction of a proposed summary.

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
        "contract": CONTRACT,
        "five_future": "OPEN_NEW_CARRIER",
    }


def is_operational_fold_nondet(machine, summary):
    return obstruction_fiber_nondet(machine, summary)["status"] == "NONE"


def as_partial_machine(machine):
    """Singleton-valued live edges, or admission error.

    Missing sources become PARTIAL domain holes (disabled). Empty sets and
    branching sets are not partial maps: deadlock is not a missing port.
    """
    require_nondet_machine(machine)
    tables = {}
    for action in machine.actions:
        table = {}
        for state, landing in machine.transitions[action].items():
            if len(landing) != 1:
                raise AdmissionError("Successor set is not a singleton; not a PARTIAL map")
            table[state] = next(iter(landing))
        tables[action] = table
    return Machine(machine.states, machine.actions, dict(machine.observation), tables)


def encodes_as_partial(machine):
    try:
        as_partial_machine(machine)
    except AdmissionError:
        return False
    return True


def as_nondet_machine(machine):
    """Embedding: partial function to singleton-or-absent LTS.

    Defined sources become singleton successor sets. Absent sources stay
    disabled. Not a claim that this is the 845 lift until the image fiber
    is compared.
    """
    require(type(machine) is Machine, "Machine required")
    tables = {}
    for action in machine.actions:
        table = {}
        for source, target in machine.transitions[action].items():
            table[source] = frozenset({target})
        tables[action] = table
    return NondetMachine(machine.states, machine.actions, dict(machine.observation), tables)


def case_key_nondet(machine, summary):
    """Exact identity of one (NondetMachine, C) pair."""
    require_nondet_summary(machine, summary)
    tables = []
    for action in machine.actions:
        rows = tuple(sorted(
            (source, frozenset(landing))
            for source, landing in machine.transitions[action].items()
        ))
        tables.append((action, rows))
    observation = tuple(machine.observation[state] for state in machine.states)
    labels = tuple(summary[state] for state in machine.states)
    return (machine.states, machine.actions, observation, tuple(tables), labels)


def machine_key_nondet(key):
    return key[:-1]


def partition_shape(states, summary):
    """Block-size profile of C, largest part first. Not a 2x2 ghost type."""
    require(type(states) is tuple, "Carrier enumeration must be a tuple")
    require(type(summary) is dict and set(summary) == set(states), "Summary misses the carrier")
    sizes = {}
    for state in states:
        label = summary[state]
        sizes[label] = sizes.get(label, 0) + 1
    return "+".join(str(size) for size in sorted(sizes.values(), reverse=True))


def successor_choices(states, max_size=2):
    """Disabled, deadlock, then nonempty subsets of size 1..max_size."""
    choices = [DISABLED, frozenset()]
    for size in range(1, max_size + 1):
        for combo in it.combinations(states, size):
            choices.append(frozenset(combo))
    return tuple(choices)


def nondet_family(n, actions=("a",), max_size=2, observations=(0, 1)):
    """Bounded NONDET-LTS family. Not the 845 PARTIAL family."""
    require(type(n) is int and n >= 0, "State count must be a finite integer")
    states = tuple(range(n))
    choices = successor_choices(states, max_size)
    machines = []
    for obs in it.product(observations, repeat=n):
        observation = dict(zip(states, obs))
        for flat in it.product(choices, repeat=n * len(actions)):
            tables = {}
            for j, action in enumerate(actions):
                table = {}
                for i, state in enumerate(states):
                    landing = flat[j * n + i]
                    if landing is not DISABLED:
                        table[state] = landing
                tables[action] = table
            machines.append(NondetMachine(states, actions, observation, tables))
    return tuple(machines)


def landing_kind(machine, left, right, action):
    """How two sources sit on one action, ignoring observation."""
    left_on = action_defined(machine, action, left)
    right_on = action_defined(machine, action, right)
    if not left_on and not right_on:
        return "both_disabled"
    if left_on != right_on:
        live = left if left_on else right
        if len(successors(machine, action, live)) == 0:
            return "deadlock_disabled"
        return "disabled_live"
    left_set = successors(machine, action, left)
    right_set = successors(machine, action, right)
    left_dead = len(left_set) == 0
    right_dead = len(right_set) == 0
    if left_dead and right_dead:
        return "both_deadlock"
    if left_dead or right_dead:
        return "deadlock_live"
    if len(left_set) > 1 or len(right_set) > 1:
        return "branching"
    return "singletons"


def pair_kind_nondet(machine, left, right, summary):
    """Kind of the witnessing action for the earliest NONDET-LTS clause."""
    clause = pair_clause_nondet(machine, left, right, summary)
    if clause == "observation":
        return "observation"
    if clause == "pass":
        return "pass"
    for action in machine.actions:
        left_on = action_defined(machine, action, left)
        right_on = action_defined(machine, action, right)
        if clause == "enabledness" and left_on != right_on:
            return landing_kind(machine, left, right, action)
        if clause == "successor_blocks" and left_on and right_on:
            if block_image(summary, successors(machine, action, left)) != block_image(
                    summary, successors(machine, action, right)):
                return landing_kind(machine, left, right, action)
    raise AdmissionError("Earliest clause has no witnessing action")


def obstruction_class(fiber):
    if fiber["status"] == "NONE":
        return "NONE"
    occupied = "+".join(clause for clause in NONDET_CLAUSES if fiber["by_clause"][clause])
    return fiber["status"] + ":" + occupied
