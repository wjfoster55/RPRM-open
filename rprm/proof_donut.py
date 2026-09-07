"""Finite proof-certificate checks over supplied exact tables (0BSD).

The checker knows the enumerated carriers, not whether they cover an external
problem. It imports no RPRM core implementation or proof-status metadata.
Malformed data raises AdmissionError; a well-typed failed certificate REJECTs.
All carriers must be finite built-in containers; they are copied on admission.
"""

from __future__ import annotations


class AdmissionError(ValueError):
    """The request does not satisfy the documented finite input contract."""


def _require(condition, message):
    if not condition:
        raise AdmissionError(message)


def _atom(value):
    if type(value) in (int, str, type(None)):
        return
    if type(value) in (tuple, frozenset):
        for part in value:
            _atom(part)
        return
    raise AdmissionError("State atoms must be int/string/None/tuple/frozenset; no bool or float")


def _carrier(values, name):
    _require(type(values) in (tuple, list, range, set, frozenset),
             name + " must be an explicit finite built-in container")
    result = tuple(values)
    for value in result:
        _atom(value)
    _require(len(set(result)) == len(result), name + " contains duplicate atoms")
    return result


def _subset(values, universe, name):
    result = set(_carrier(values, name))
    _require(result <= set(universe), name + " contains an out-of-carrier atom")
    return result


def _map(table, domain, codomain, name, total=True):
    _require(type(table) is dict, name + " must be a finite dict")
    result = dict(table)
    for key, value in result.items():
        _atom(key)
        _atom(value)
    _require(set(result) <= set(domain), name + " has an out-of-carrier key")
    if total:
        _require(set(result) == set(domain), name + " must cover its entire domain")
    _require(set(result.values()) <= set(codomain), name + " leaves its codomain")
    return result


def _observation(table, domain, name):
    _require(type(table) is dict, name + " must be a dict")
    result = dict(table)
    for key in result:
        _atom(key)
    _require(set(result) == set(domain), name + " must cover its entire domain")
    for value in result.values():
        if type(value) is not bool:
            _atom(value)
    return result


def _answer_key(value):
    # A Boolean answer and an integer answer are different typed readouts.
    return (type(value).__name__, value)


def _relation(rows, left, right, name):
    result = _carrier(rows, name)
    _require(all(type(row) is tuple and len(row) == 2 for row in result),
             name + " needs distinct ordered pairs")
    _require(all(x in left and y in right for x, y in result),
             name + " has an out-of-sort pair")
    return set(result)


def _audit(violations):
    return {"status": "REJECT" if violations else "ACCEPT",
            "errors": sorted({v["code"] for v in violations}),
            "witnesses": violations}


def fiber_disposition(hypotheses, compatible, readout):
    """Complete fiber from a Boolean admission table and total readout table.

    The result retains every member and distinct typed answer. Empty fibers
    have decided=False. ONE denotes one member of this supplied carrier.
    """
    hypotheses = _carrier(hypotheses, "Hypotheses")
    compatible = _observation(compatible, hypotheses, "Compatibility")
    _require(all(type(v) is bool for v in compatible.values()),
             "Compatibility entries must be exact Booleans")
    readout = _observation(readout, hypotheses, "Readout")
    members = tuple(h for h in hypotheses if compatible[h])
    answers = {}
    for h in members:
        answers.setdefault(_answer_key(readout[h]), readout[h])
    decided = len(answers) == 1
    return {"fiber": "NONE" if not members else "ONE" if len(members) == 1 else "MANY",
            "count": len(members), "members": members, "answers": tuple(answers.values()),
            "decided": decided, "decision": next(iter(answers.values())) if decided else None}


def audit_finite_aperture(givens, witnesses, relation, abstract_givens,
                          abstract_witnesses, abstract_relation, alpha, beta):
    """Check F'(alpha(g)) = {beta(g,w): w in F(g)} for every given input.

    Relations are complete finite sets of pairs. alpha is total G -> G';
    beta is total G x W -> W'. A common witness carrier W is used; relation
    membership carries any per-given restrictions. No callback is trusted.
    """
    givens = _carrier(givens, "Givens")
    witnesses = _carrier(witnesses, "Witnesses")
    abstract_givens = _carrier(abstract_givens, "Abstract givens")
    abstract_witnesses = _carrier(abstract_witnesses, "Abstract witnesses")
    relation = _relation(relation, givens, witnesses, "Concrete relation")
    abstract_relation = _relation(abstract_relation, abstract_givens,
                                  abstract_witnesses, "Abstract relation")
    alpha = _map(alpha, givens, abstract_givens, "Given map")
    beta = _map(beta, tuple((g, w) for g in givens for w in witnesses),
                abstract_witnesses, "Witness map")
    violations = []
    for g in givens:
        image = {beta[g, w] for w in witnesses if (g, w) in relation}
        abstract = {v for v in abstract_witnesses if (alpha[g], v) in abstract_relation}
        for v in abstract_witnesses:
            if v in image - abstract:
                violations.append({"code": "FORWARD_COVERAGE", "at": (g, v)})
            if v in abstract - image:
                violations.append({"code": "WITNESS_LIFTING", "at": (g, v)})
    return _audit(violations)


def audit_finite_induction(states, seeds, transitions, safe, bad):
    """Check abstract seed/closure/separation obligations on finite tables.

    A partial transition is a well-typed but rejected total-transition
    certificate. A successor outside the carrier is an admission error.
    Source coverage and concrete-to-abstract soundness are separate premises.
    """
    states = _carrier(states, "States")
    seeds = _subset(seeds, states, "Seeds")
    safe = _subset(safe, states, "Safe")
    bad = _subset(bad, states, "Bad")
    _require(type(transitions) in (tuple, list), "Transitions must be a tuple/list of maps")
    transitions = tuple(_map(op, states, states, "Transition", total=False) for op in transitions)
    violations = []
    for x in states:
        if x in seeds - safe:
            violations.append({"code": "SEED", "at": x})
        if x in safe & bad:
            violations.append({"code": "SEPARATION", "at": x})
        for i, op in enumerate(transitions):
            if x not in op:
                violations.append({"code": "TOTAL_TRANSITION", "at": (i, x)})
            if x in safe and (x not in op or op[x] not in safe):
                violations.append({"code": "CLOSURE", "at": (i, x)})
    return _audit(violations)


def audit_finite_descent(states, core, bad, rank, step):
    """Check finite bad-case returns with a nonnegative integer rank.

    This tests a supplied certificate. It cannot discover a uniform return
    rule for an unspecified source family.
    """
    states = _carrier(states, "States")
    core = _subset(core, states, "Core")
    bad = _subset(bad, states, "Bad")
    _require(type(rank) is dict, "Rank must be a dict")
    rank = dict(rank)
    for key in rank:
        _atom(key)
    _require(set(rank) == set(states), "Rank must cover the entire carrier")
    _require(all(type(v) is int and v >= 0 for v in rank.values()),
             "Ranks must be nonnegative integers, excluding bool")
    step = _map(step, states, states, "Return map", total=False)
    violations = []
    for x in states:
        if x in core & bad:
            violations.append({"code": "BASE", "at": x})
        if x in bad - core:
            if x not in step:
                violations.append({"code": "RETURN", "at": x})
                continue
            y = step[x]
            if y not in bad:
                violations.append({"code": "PRESERVATION", "at": (x, y)})
            if rank[y] >= rank[x]:
                violations.append({"code": "DECREASE", "at": (x, y)})
    return _audit(violations)


def audit_finite_path(states, transition, path, *, cycle=False):
    """Check every edge in an explicit path, optionally a positive closed walk.

    Repeated states in a path are allowed. A cycle needs at least one edge
    and equality of the complete first/last state. Minimal period is not asked.
    """
    states = _carrier(states, "States")
    transition = _map(transition, states, states, "Transition", total=False)
    _require(type(path) in (tuple, list), "Path must be a tuple/list")
    path = tuple(path)
    _require(bool(path), "Path must contain an initial state")
    _require(type(cycle) is bool, "cycle must be Boolean")
    for x in path:
        _atom(x)
        _require(x in states, "Path leaves the state carrier")
    violations = []
    if cycle and len(path) < 2:
        violations.append({"code": "ZERO_LENGTH_CYCLE", "at": path[0]})
    if cycle and path[-1] != path[0]:
        violations.append({"code": "NOT_CLOSED", "at": (path[0], path[-1])})
    for i, (x, y) in enumerate(zip(path, path[1:])):
        if x not in transition:
            violations.append({"code": "UNDEFINED_STEP", "at": (i, x)})
        elif transition[x] != y:
            violations.append({"code": "WRONG_STEP", "at": (i, x, y)})
    return _audit(violations)


def audit_finite_quotient(states, summary, observation, transition):
    """Independent pairwise deterministic quotient audit.

    Every pair with equal summaries must agree on current observation,
    transition enabledness and the successor summary. Finite partial maps
    are supported, with undefinedness retained as an observable distinction.
    """
    states = _carrier(states, "States")
    summary = _observation(summary, states, "Summary")
    _require(all(type(v) is not bool for v in summary.values()), "Summary labels are state atoms")
    observation = _observation(observation, states, "Observation")
    transition = _map(transition, states, states, "Transition", total=False)
    violations = []
    for i, x in enumerate(states):
        for y in states[i + 1:]:
            if summary[x] != summary[y]:
                continue
            if _answer_key(observation[x]) != _answer_key(observation[y]):
                violations.append({"code": "OBSERVATION", "at": (x, y)})
            if (x in transition) != (y in transition):
                violations.append({"code": "ENABLEDNESS", "at": (x, y)})
            elif x in transition and summary[transition[x]] != summary[transition[y]]:
                violations.append({"code": "SUCCESSOR", "at": (x, y)})
    return _audit(violations)
