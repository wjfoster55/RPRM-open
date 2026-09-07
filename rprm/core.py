"""Small exact finite reference semantics for RPRM; standard library only.

This supplies finite tables, not an arbitrary theorem prover or serializer.
AdmissionError means malformed/out-of-carrier input. A valid empty fiber is
NONE; an incompatible quotient is REJECT. Neither is an implementation error.
State values use immutable int/string/None/tuple/frozenset atoms (not floats or
bools); equality is their exact Python equality within a nominal declared sort.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from threading import Lock


class AdmissionError(ValueError):
    pass


class ValidatorError(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise AdmissionError(message)


def atom(value):
    if type(value) in (int, str, type(None)):
        return
    if type(value) in (tuple, frozenset):
        for item in value:
            atom(item)
        return
    raise AdmissionError("Only exact immutable atoms are admitted; bool/float are not atoms")


def carrier(values):
    require(type(values) is tuple, "Carrier enumeration must be a tuple")
    for value in values:
        atom(value)
    require(len(set(values)) == len(values), "Carrier enumeration has duplicates")
    return values


@dataclass(frozen=True)
class Sort:
    name: str
    values: tuple

    def __post_init__(self):
        require(type(self.name) is str and bool(self.name), "Sort needs a name")
        carrier(self.values)


@dataclass(frozen=True)
class Port:
    name: str
    sort: Sort

    def __post_init__(self):
        require(type(self.name) is str and bool(self.name), "Port needs a name")
        require(type(self.sort) is Sort, "Port needs a declared sort")


@dataclass(frozen=True)
class Value:
    sort: Sort
    value: object

    def __post_init__(self):
        require(type(self.sort) is Sort, "Value needs a declared sort")
        atom(self.value)
        require(self.value in self.sort.values, "Value is outside its sort")


@dataclass(frozen=True)
class Relation:
    ports: tuple
    rows: frozenset

    def __post_init__(self):
        require(type(self.ports) is tuple and all(type(p) is Port for p in self.ports),
                "Relation ports must be a tuple of Ports")
        require(len({p.name for p in self.ports}) == len(self.ports), "Duplicate port name")
        # A nominal sort name cannot have contradictory definitions in one signature.
        sorts = {}
        for port in self.ports:
            require(port.sort.name not in sorts or sorts[port.sort.name] == port.sort,
                    "Conflicting declarations of the same nominal sort")
            sorts[port.sort.name] = port.sort
        require(type(self.rows) is frozenset, "Relation rows must be a frozenset")
        for row in self.rows:
            require(type(row) is tuple and len(row) == len(self.ports), "Wrong row arity")
            for port, value in zip(self.ports, row):
                atom(value)
                require(value in port.sort.values, "Out-of-sort relation row")


@dataclass(frozen=True)
class Fiber:
    ports: tuple
    members: frozenset

    def __post_init__(self):
        require(type(self.ports) is tuple and all(type(p) is str and p for p in self.ports)
                and len(set(self.ports)) == len(self.ports), "Fiber needs distinct named output ports")
        require(type(self.members) is frozenset, "Fiber members must be a frozenset")
        for member in self.members:
            require(type(member) is tuple and len(member) == len(self.ports), "Wrong fiber member arity")
            for value in member:
                atom(value)

    @property
    def disposition(self):
        return "NONE" if not self.members else "ONE" if len(self.members) == 1 else "MANY"


def solve(relation, supplied):
    require(type(relation) is Relation and type(supplied) is dict, "Invalid aperture request")
    by_name = {p.name: (i, p) for i, p in enumerate(relation.ports)}
    require(set(supplied) <= set(by_name), "Unknown supplied port")
    fixed = {}
    for name, value in supplied.items():
        require(type(value) is Value and value.sort == by_name[name][1].sort, "Wrong supplied sort")
        fixed[by_name[name][0]] = value.value
    missing = tuple(i for i in range(len(relation.ports)) if i not in fixed)
    rows = frozenset(tuple(row[i] for i in missing) for row in relation.rows
                     if all(row[i] == value for i, value in fixed.items()))
    return Fiber(tuple(relation.ports[i].name for i in missing), rows)


def binary(relation):
    require(type(relation) is Relation and len(relation.ports) == 2, "Binary relation required")


def converse(relation):
    binary(relation)
    a, b = relation.ports
    return Relation((Port("source", b.sort), Port("target", a.sort)),
                    frozenset((y, x) for x, y in relation.rows))


def witnesses(first, second, middle_guard=None):
    binary(first)
    binary(second)
    require(first.ports[1].sort == second.ports[0].sort, "Middle interface mismatch")
    allowed = frozenset(first.ports[1].sort.values)
    if middle_guard is not None:
        require(type(middle_guard) is frozenset, "Invalid middle guard")
        for value in middle_guard:
            atom(value)
        require(middle_guard <= allowed, "Invalid middle guard")
        allowed = middle_guard
    return frozenset((x, y, z) for x, y in first.rows for yy, z in second.rows
                     if y == yy and y in allowed)


def compose(first, second, middle_guard=None):
    joined = witnesses(first, second, middle_guard)
    return Relation((Port("source", first.ports[0].sort), Port("target", second.ports[1].sort)),
                    frozenset((x, z) for x, _, z in joined))


@dataclass(frozen=True)
class Occurrence:
    context: str
    identifier: str
    sort: str
    payload: object

    def __post_init__(self):
        require(all(type(x) is str and x for x in (self.context, self.identifier, self.sort)),
                "Occurrence context, identifier, and sort must be nonempty strings")
        atom(self.payload)


def attach_occurrences(left, right):
    """Exact payload matching in one context/sort, retaining the ordered seam pair."""
    require(type(left) is tuple and type(right) is tuple, "Occurrence carriers must be tuples")
    seen = {}
    for occurrence in left + right:
        require(type(occurrence) is Occurrence, "Occurrence required")
        key = (occurrence.context, occurrence.identifier)
        require(key not in seen or seen[key] == occurrence, "Conflicting occurrence identity")
        seen[key] = occurrence
    require(len(set(left)) == len(left) and len(set(right)) == len(right), "Duplicate occurrence row")
    return frozenset((a, b) for a in left for b in right
                     if (a.context, a.sort, a.payload) == (b.context, b.sort, b.payload))


def total_table(states, table, name):
    require(type(table) is dict and set(table) == set(states), name + " must cover exactly the carrier")
    for key in table:
        atom(key)
    for value in table.values():
        atom(value)


def groups(states, summary, observation):
    carrier(states)
    total_table(states, summary, "Summary")
    total_table(states, observation, "Observation")
    result = {}
    for state in states:
        result.setdefault(summary[state], []).append(state)
    return result


def descend(states, summary, observation, profiles, mismatch):
    blocks = groups(states, summary, observation)
    out, answers = {}, {}
    for label, block in blocks.items():
        first = block[0]
        for other in block[1:]:
            if observation[first] != observation[other]:
                return {"status": "REJECT", "reason": "observation", "witness": (first, other)}
            if profiles[first] != profiles[other]:
                return {"status": "REJECT", "reason": mismatch(first, other), "witness": (first, other)}
        answers[label], out[label] = observation[first], profiles[first]
    return {"status": "ACCEPT", "observation": answers, "transition": out}


def deterministic_quotient(states, summary, observation, transition):
    groups(states, summary, observation)
    require(type(transition) is dict and set(transition) <= set(states), "Invalid partial-map domain")
    for key in transition:
        atom(key)
    for value in transition.values():
        atom(value)
        require(value in states, "Transition leaves the carrier")
    profiles = {x: ("OK", summary[transition[x]]) if x in transition else ("FAIL",) for x in states}
    return descend(states, summary, observation, profiles,
                   lambda x, y: "enabledness" if (x in transition) != (y in transition) else "successor")


def nondeterministic_quotient(states, summary, observation, transition):
    groups(states, summary, observation)
    require(type(transition) is dict and set(transition) == set(states), "Successor table must be total")
    for key in transition:
        atom(key)
    for successors in transition.values():
        require(type(successors) is frozenset, "Successors must be an exact set")
        for successor in successors:
            atom(successor)
        require(successors <= set(states), "Successor leaves the carrier")
    profiles = {x: frozenset(summary[y] for y in transition[x]) for x in states}
    return descend(states, summary, observation, profiles, lambda _x, _y: "successor_blocks")


def stochastic_quotient(states, summary, observation, kernel):
    blocks = groups(states, summary, observation)
    require(type(kernel) is dict and set(kernel) == set(states), "Kernel must have one row per state")
    for key in kernel:
        atom(key)
    for row in kernel.values():
        require(type(row) is dict and set(row) == set(states), "Kernel row must retain every mass, including zero")
        for key in row:
            atom(key)
        require(all(type(mass) is Fraction and mass >= 0 for mass in row.values()), "Exact nonnegative Fraction masses required")
        require(sum(row.values(), Fraction(0)) == 1, "Kernel row is not normalized")
    profiles = {x: tuple((label, sum((kernel[x][y] for y in block), Fraction(0)))
                         for label, block in blocks.items()) for x in states}
    return descend(states, summary, observation, profiles, lambda _x, _y: "pushforward_mass")


def refine_question(states, summary, question):
    groups(states, summary, question)
    return {x: (summary[x], question[x]) for x in states}


def land(states, richer, embedding, retraction, motion):
    carrier(states)
    carrier(richer)
    total_table(states, embedding, "Embedding")
    total_table(richer, retraction, "Retraction")
    total_table(richer, motion, "Motion")
    require(set(embedding.values()) <= set(richer) and set(retraction.values()) <= set(states)
            and set(motion.values()) <= set(richer), "Landing map type mismatch")
    require(all(retraction[embedding[x]] == x for x in states), "Retraction equation fails")
    return {x: retraction[motion[embedding[x]]] for x in states}


def swap_vacancy(state, edge):
    require(type(state) is tuple and len(state) == 4 and state.count(None) == 1
            and all(x is None or type(x) is int and x in (0, 1) for x in state), "Expected four sites with one vacancy and binary payloads")
    require(type(edge) is int and 0 <= edge < 3, "Edge index must be 0, 1, or 2")
    if state[edge] is not None and state[edge + 1] is not None:
        return ("FAIL",)
    next_state = list(state)
    next_state[edge], next_state[edge + 1] = next_state[edge + 1], next_state[edge]
    return ("OK", tuple(next_state))


@dataclass(frozen=True)
class Snapshot:
    store_id: object
    version: int
    payload: object

    def __post_init__(self):
        require(type(self.store_id) is object, "Snapshot needs an opaque in-memory store identity")
        require(type(self.version) is int and self.version >= 0, "Snapshot needs a nonnegative integer version")
        atom(self.payload)


class StateStore:
    """An in-memory linearizable compare-and-swap store; no durability claim.

    Immutable snapshots, opaque per-store identity, and monotone versions prevent
    ABA in this process. Snapshots are live process objects, not durable tickets.
    A supplied validator is a gate, not an automatically proved theorem.
    """

    def __init__(self, payload):
        atom(payload)
        self._lock = Lock()
        self._state = Snapshot(object(), 0, payload)

    def snapshot(self):
        with self._lock:
            return self._state

    def flick(self, parent, candidate, validator):
        require(type(parent) is Snapshot, "Expected an exact parent snapshot")
        atom(candidate)
        require(callable(validator), "Validator must be callable")
        with self._lock:
            if parent != self._state:
                return "REJECT_STALE"
        try:
            valid = validator(parent.payload, candidate)
        except Exception as error:
            raise ValidatorError("Validator failed; candidate not installed") from error
        if type(valid) is not bool:
            raise ValidatorError("Validator must return an exact Boolean")
        if not valid:
            return "REJECT_INVALID"
        with self._lock:
            if parent != self._state:
                return "REJECT_STALE"
            self._state = Snapshot(parent.store_id, parent.version + 1, candidate)
            return "COMMITTED"
