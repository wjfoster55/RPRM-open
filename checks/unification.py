"""Bounded independent semantic checks for U01/U02/U04; not their general proof.

Direct source term evaluation is compared with evaluation of translated,
function-free formulas on larger relational target carriers. All computations
are exact, offline, and use only adjacent committed bytes plus Python stdlib.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools as it
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def term_value(term, env, function, constant):
    kind = term[0]
    if kind == "var":
        return env[term[1]]
    if kind == "constant":
        return constant
    if kind == "function":
        return function[term_value(term[1], env, function, constant)]
    raise ValueError(("source term", term))


def source_value(formula, env, universe, function, predicate, constant, flag):
    kind = formula[0]
    if kind == "eq":
        return term_value(formula[1], env, function, constant) == term_value(
            formula[2], env, function, constant)
    if kind == "pred":
        return term_value(formula[1], env, function, constant) in predicate
    if kind == "flag":
        return flag
    if kind == "not":
        return not source_value(formula[1], env, universe, function, predicate, constant, flag)
    if kind == "and":
        return all(source_value(f, env, universe, function, predicate, constant, flag)
                   for f in formula[1:])
    if kind == "or":
        return any(source_value(f, env, universe, function, predicate, constant, flag)
                   for f in formula[1:])
    if kind in ("exists", "forall"):
        values = (source_value(formula[2], env | {formula[1]: x}, universe,
                               function, predicate, constant, flag) for x in universe)
        return any(values) if kind == "exists" else all(values)
    raise ValueError(("source formula", formula))


class Translator:
    """Build an explicit relational AST, without calling either evaluator."""

    def __init__(self):
        self.next_id = 0

    def fresh(self):
        self.next_id += 1
        # Source syntax below admits only x,y; generated names are disjoint.
        return "w" + str(self.next_id)

    def value(self, term, result):
        if term[0] == "var":
            return ("eqvars", result, term[1])
        if term[0] == "constant":
            return ("relation", "constant", (result,))
        if term[0] == "function":
            middle = self.fresh()
            return ("exists", middle, ("and",
                    ("relation", "image", (middle,)),
                    self.value(term[1], middle),
                    ("relation", "function", (middle, result))))
        raise ValueError(term)

    def formula(self, formula):
        kind = formula[0]
        if kind == "eq":
            left, right = self.fresh(), self.fresh()
            return ("exists", left, ("exists", right, ("and",
                    ("relation", "image", (left,)),
                    ("relation", "image", (right,)),
                    self.value(formula[1], left), self.value(formula[2], right),
                    ("eqvars", left, right))))
        if kind == "pred":
            result = self.fresh()
            return ("exists", result, ("and",
                    ("relation", "image", (result,)),
                    self.value(formula[1], result),
                    ("relation", "predicate", (result,))))
        if kind == "flag":
            return ("relation", "flag", ())
        if kind in ("not", "and", "or"):
            return (kind, *(self.formula(f) for f in formula[1:]))
        if kind == "exists":
            return ("exists", formula[1], ("and",
                    ("relation", "image", (formula[1],)), self.formula(formula[2])))
        if kind == "forall":
            return ("forall", formula[1], ("or",
                    ("not", ("relation", "image", (formula[1],))),
                    self.formula(formula[2])))
        raise ValueError(formula)


def target_value(formula, env, universe, relations):
    kind = formula[0]
    if kind == "eqvars":
        return env[formula[1]] == env[formula[2]]
    if kind == "relation":
        return tuple(env[v] for v in formula[2]) in relations[formula[1]]
    if kind == "not":
        return not target_value(formula[1], env, universe, relations)
    if kind == "and":
        return all(target_value(f, env, universe, relations) for f in formula[1:])
    if kind == "or":
        return any(target_value(f, env, universe, relations) for f in formula[1:])
    if kind in ("exists", "forall"):
        values = [target_value(formula[2], env | {formula[1]: value}, universe, relations)
                  for value in universe]
        return any(values) if kind == "exists" else all(values)
    raise ValueError(("target formula", formula))


def free_variables(formula):
    def term_vars(term):
        return ({term[1]} if term[0] == "var" else
                term_vars(term[1]) if term[0] == "function" else set())
    if formula[0] == "eq":
        return term_vars(formula[1]) | term_vars(formula[2])
    if formula[0] == "pred":
        return term_vars(formula[1])
    if formula[0] == "flag":
        return set()
    if formula[0] in ("forall", "exists"):
        return free_variables(formula[2]) - {formula[1]}
    return set().union(*(free_variables(f) for f in formula[1:]))


def formula_suite(nonempty):
    x, y = ("var", "x"), ("var", "y")
    terms = [x, y, ("function", x), ("function", y),
             ("function", ("function", x))]
    if nonempty:
        terms.append(("constant",))
    atoms = [("eq", a, b) for a in terms for b in terms]
    atoms += [("pred", t) for t in terms] + [("flag",)]
    formulas = list(atoms)
    formulas += [("not", a) for a in atoms]
    # Every atom under each of these exact binder patterns.
    for a in atoms:
        formulas.extend([("forall", "x", a), ("exists", "x", a),
                         ("forall", "x", ("exists", "y", a)),
                         ("exists", "x", ("forall", "y", a))])
    p, q = ("pred", x), ("pred", ("function", x))
    formulas.extend([("forall", "x", ("or", ("not", p), q)),
                     ("exists", "x", ("and", p, ("not", q))),
                     # Shadowing of an outer source variable tests capture hygiene.
                     ("forall", "x", ("exists", "x", ("eq", x, x)))])
    return formulas


def check_translation():
    cases = models = 0
    per_size = {}
    for n in range(3):
        source = tuple(range(n))
        target = tuple("t" + str(i) for i in range(n + 1))
        formulas = formula_suite(bool(n))
        translated = [(f, Translator().formula(f), sorted(free_variables(f)))
                      for f in formulas]
        count_before, model_before = cases, models
        functions = it.product(source, repeat=n)
        for values in functions:
            function = dict(zip(source, values))
            for bits in it.product((False, True), repeat=n):
                predicate = {x for x, bit in zip(source, bits) if bit}
                for constant in (source if n else (None,)):
                    for flag in (False, True):
                        for encoded in it.permutations(target, n):
                            encoding = dict(zip(source, encoded))
                            relations = {
                                "image": {(x,) for x in encoded},
                                "function": {(encoding[x], encoding[function[x]]) for x in source},
                                "predicate": {(encoding[x],) for x in predicate},
                                "constant": {(encoding[constant],)} if n else set(),
                                "flag": {()} if flag else set(),
                            }
                            models += 1
                            for original, transformed, variables in translated:
                                for assignment in it.product(source, repeat=len(variables)):
                                    env = dict(zip(variables, assignment))
                                    expected = source_value(original, env, source, function,
                                                            predicate, constant, flag)
                                    observed = target_value(transformed,
                                                            {v: encoding[x] for v, x in env.items()},
                                                            target, relations)
                                    require(expected == observed,
                                            ("truth mismatch", n, function, predicate, original, env))
                                    cases += 1
        per_size[str(n)] = {"models": models-model_before, "formula_count": len(formulas),
                            "formula_assignments": cases-count_before}
    return {"models": models, "formula_assignments": cases, "by_source_size": per_size,
            "boundary": "One sort of size 0..2; all unary functions/predicates, constants when nonempty, "
                        "nullary predicate truth values, injections into n+1 target points; "
                        "the explicit finite formula_suite only. Not exhaustive over formulas/signatures."}


def check_bridge_fibers():
    cases = 0
    source = (0, 1)
    target = ("a", "b", "extra")
    rows = tuple(it.product(source, repeat=2))
    for encoded in it.permutations(target, 2):
        e = dict(zip(source, encoded))
        for bits in it.product((False, True), repeat=4):
            relation = {r for r, bit in zip(rows, bits) if bit}
            image_relation = {tuple(e[x] for x in r) for r in relation}
            for known_mask in it.product((False, True), repeat=2):
                known = [i for i, bit in enumerate(known_mask) if bit]
                missing = [i for i, bit in enumerate(known_mask) if not bit]
                for values in it.product(source, repeat=len(known)):
                    env = dict(zip(known, values))
                    expected = {tuple(e[r[i]] for i in missing) for r in relation
                                if all(r[i] == x for i, x in env.items())}
                    observed = {tuple(r[i] for i in missing) for r in image_relation
                                if all(r[i] == e[x] for i, x in env.items())}
                    require(expected == observed, "fiber transport")
                    cases += 1
    return {"fiber_comparisons": cases, "injections": 6, "source_relations": 16,
            "scope": "One shared injection applied to both binary ports; not all independent port-map pairs."}


def check_shared_interface():
    labels = ("ab", "bc", "cd", "da")
    cases = 0
    for length in range(9):
        for word in it.product((1, -1), repeat=length):
            for a in range(4):
                for b in range(4):
                    if a % 2 != b % 2:
                        continue
                    source_one = a
                    source_two = labels[b]
                    shared = a % 2
                    for step in word:
                        source_one = (source_one + step) % 4
                        source_two = labels[(labels.index(source_two) + step) % 4]
                        shared = 1-shared
                        require(source_one % 2 == labels.index(source_two) % 2 == shared,
                                "shared interface step")
                    cases += 1
    return {"word_initial_pairs": cases, "max_word_length": 8,
            "scope": "Both four-state U04 examples and every word through length 8."}


def hostile_controls():
    # Each hostile countermodel violates a different theorem hypothesis. Require disagreement
    # with an exact source result, rather than reporting a preselected count.
    results = {}
    results["noninjective_equality"] = ((0 == 1) != ("merged" == "merged"))
    results["missing_predicate_reflection"] = ((0 in set()) != ("a" in {"a"}))
    formula = ("forall", "x", ("eq", ("var", "x"), ("constant",)))
    exact = Translator().formula(formula)
    # Remove only the universal image guard.
    unguarded = ("forall", exact[1], exact[2][2])
    relations = {"image": {("a",)}, "constant": {("a",)},
                 "function": {("a", "a")}, "predicate": set(), "flag": set()}
    results["unrestricted_quantifier"] = (
        target_value(exact, {}, ("a", "b"), relations)
        and not target_value(unguarded, {}, ("a", "b"), relations))
    source_paths = {(x, z) for x, y in set() for middle, z in set() if y == middle}
    target_r, target_s = {("a", "outside")}, {("outside", "c")}
    target_paths = {(x, z) for x, y in target_r for middle, z in target_s if y == middle}
    results["unrestricted_middle_witness"] = source_paths != target_paths
    witnesses = {("a", "left", "c"), ("a", "right", "c")}
    results["endpoint_projection_claimed_injective"] = (
        len({(x, z) for x, _, z in witnesses}) < len(witnesses))
    results["marginals_claimed_joint"] = (
        set(it.product((0, 1), repeat=2)) != {(0, 0), (1, 1)})
    require(all(results.values()), ("missed hostile control", results))
    return {"counterexample_checks": len(results), "controls": results,
            "scope": "Exact hostile mathematical countermodels; universal guard control mutates the translated AST. "
                     "These are not six implementation mutation tests."}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = {"schema": "rprm-v02-unification-conformance/v1",
              "translation": check_translation(), "fibers": check_bridge_fibers(),
              "shared_interface": check_shared_interface(), "hostile": hostile_controls(),
              "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "status": "PASS", "claim_ceiling": "Bounded exact semantic conformance; written general proofs separate."}
    serialized = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(serialized, encoding="utf-8", newline="\n")
    print(serialized)


if __name__ == "__main__":
    main()
