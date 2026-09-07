"""Independent bounded conformance for RPRM reference semantics.

Run with python -I -B. The checker enumerates assignments and candidate quotient
tables independently of runtime row filtering and representative signatures.
Only these two adjacent Python source files are loaded; no old census imported.
"""

from __future__ import annotations

import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import importlib.util
from itertools import product
import json
from pathlib import Path
import sys
from threading import Barrier


HERE = Path(__file__).resolve().parent


class ConformanceFailure(Exception):
    pass


def check(condition, message):
    if not condition:
        raise ConformanceFailure(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def subsets(values):
    values = tuple(values)
    for mask in range(1 << len(values)):
        yield frozenset(values[i] for i in range(len(values)) if mask & (1 << i))


def partitions(n, prefix=()):
    if len(prefix) == n:
        yield prefix
    else:
        for label in range(max(prefix, default=-1) + 2):
            yield from partitions(n, prefix + (label,))


def compositions(total, size):
    if size == 0:
        if total == 0:
            yield ()
    elif size == 1:
        yield (total,)
    else:
        for first in range(total + 1):
            for tail in compositions(total - first, size - 1):
                yield (first,) + tail


def oracle_fiber(domains, rows, known):
    missing = tuple(i for i in range(len(domains)) if i not in known)
    completions = set()
    for candidate in product(*(domains[i] for i in missing)):
        assignment = dict(known)
        assignment.update(zip(missing, candidate))
        if tuple(assignment[i] for i in range(len(domains))) in rows:
            completions.add(candidate)
    return frozenset(completions)


def oracle_quotient(states, labels, observation, transition, kind, denominator=2):
    """Enumerate possible retained outputs and test their defining equations.

    For kernels transition contains integer row counts, not runtime Fractions.
    No runtime quotient function, partition refiner, or helper is used here.
    """
    image = tuple(dict.fromkeys(labels[x] for x in states))
    if kind == "det":
        candidates = [("FAIL",)] + [("OK", z) for z in image]
    elif kind == "nondet":
        candidates = list(subsets(image))
    else:
        candidates = [tuple(zip(image, counts)) for counts in compositions(denominator, len(image))]
    answers, induced = {}, {}
    for z in image:
        sources = [x for x in states if labels[x] == z]
        answer_options = [bit for bit in (0, 1) if all(observation[x] == bit for x in sources)]
        if not answer_options:
            return None
        possible = []
        for candidate in candidates:
            valid = True
            for x in sources:
                if kind == "det":
                    valid = valid and ((x not in transition) if candidate[0] == "FAIL"
                                       else x in transition and labels[transition[x]] == candidate[1])
                elif kind == "nondet":
                    valid = valid and all((q in candidate) == any(labels[y] == q for y in transition[x])
                                          for q in image)
                else:
                    valid = valid and all(count == sum(transition[x][y] for y in states if labels[y] == q)
                                          for q, count in candidate)
            if valid:
                possible.append(candidate)
        if not possible:
            return None
        check(len(possible) == 1 and len(answer_options) == 1, "Oracle quotient is unexpectedly nonunique")
        answers[z] = answer_options[0]
        induced[z] = (tuple((q, Fraction(count, denominator)) for q, count in possible[0])
                      if kind == "stoch" else possible[0])
    return {"status": "ACCEPT", "observation": answers, "transition": induced}


def binary_relation(rt, source, target, rows):
    return rt.Relation((rt.Port("source", source), rt.Port("target", target)), frozenset(rows))


class Suite:
    def __init__(self, rt):
        self.rt = rt
        self.counts = Counter()
        self.controls = []

    def admission(self, name, action):
        try:
            action()
        except self.rt.AdmissionError:
            self.counts["admission_rejections"] += 1
            return
        raise ConformanceFailure("Invalid input was not rejected: " + name)

    def hostile_control(self, name, proposed, oracle):
        check(proposed != oracle, "Hostile output incorrectly passed the exact oracle: " + name)
        self.controls.append(name)

    def relations(self):
        rt = self.rt
        missing_marker = object()
        for arity in range(4):
            for sizes in product(range(3), repeat=arity):
                domains = tuple(tuple(range(size)) for size in sizes)
                sorts = tuple(rt.Sort("sort" + str(i), domain) for i, domain in enumerate(domains))
                ports = tuple(rt.Port("p" + str(i), sort) for i, sort in enumerate(sorts))
                for rows in subsets(product(*domains)):
                    relation = rt.Relation(ports, rows)
                    for values in product(*((missing_marker,) + domain for domain in domains)):
                        known = {i: value for i, value in enumerate(values) if value is not missing_marker}
                        supplied = {"p" + str(i): rt.Value(sorts[i], value) for i, value in known.items()}
                        expected = oracle_fiber(domains, rows, known)
                        actual = rt.solve(relation, supplied)
                        expected_ports = tuple("p" + str(i) for i in range(arity) if i not in known)
                        status = "NONE" if not expected else "ONE" if len(expected) == 1 else "MANY"
                        check((actual.ports, actual.members, actual.disposition) == (expected_ports, expected, status),
                              f"Aperture mismatch: {sizes}, {rows}, {known}")
                        self.counts["aperture_queries"] += 1
                        self.counts["fiber_" + status.lower()] += 1
        bit = rt.Sort("bit", (0, 1))
        diag = binary_relation(rt, bit, bit, ((0, 0), (1, 1)))
        check(rt.solve(diag, {}).members == frozenset(((0, 0), (1, 1))), "Joint correlation lost")
        self.hostile_control("independent_marginals_invent_joint_rows", frozenset(product((0, 1), repeat=2)), diag.rows)
        self.hostile_control("NONE_for_valid_zero_port_row", frozenset(), oracle_fiber((), frozenset({()}), {}))
        empty_value = rt.Sort("set_value", (frozenset(),))
        query = rt.Relation((rt.Port("answer", empty_value),), frozenset({(frozenset(),)}))
        check(rt.solve(query, {}).disposition == "ONE", "Successful empty-set payload confused with no completion")
        self.hostile_control("NONE_for_successful_empty_payload", "NONE", rt.solve(query, {}).disposition)
        self.admission("wrong nominal sort", lambda: rt.solve(diag, {"source": rt.Value(rt.Sort("other", (0, 1)), 0)}))
        self.admission("unknown port", lambda: rt.solve(diag, {"unknown": rt.Value(bit, 0)}))
        self.admission("duplicate ports", lambda: rt.Relation((rt.Port("x", bit), rt.Port("x", bit)), frozenset()))
        self.admission("wrong row arity", lambda: rt.Relation(diag.ports, frozenset({(0,)})))
        self.admission("out of carrier", lambda: rt.Value(bit, 2))
        self.admission("Boolean aliases an integer", lambda: rt.Value(bit, False))
        self.admission("nested Boolean atom", lambda: rt.Sort("nested", ((0, (False,)),)))
        self.admission("conflicting nominal sort", lambda: rt.Relation((rt.Port("x", bit), rt.Port("y", rt.Sort("bit", (0,)))), frozenset()))
        self.admission("empty sort cannot admit a value", lambda: rt.Value(rt.Sort("empty", ()), 0))
        self.admission("duplicate fiber ports", lambda: rt.Fiber(("x", "x"), frozenset()))
        self.admission("wrong fiber tuple arity", lambda: rt.Fiber(("x",), frozenset({()})))
        self.admission("Boolean fiber payload", lambda: rt.Fiber(("x",), frozenset({(False,)})))
        relations = [binary_relation(rt, bit, bit, rows) for rows in subsets(product((0, 1), repeat=2))]
        for first in relations:
            check(rt.converse(rt.converse(first)).rows == first.rows, "Converse involution failed")
            for second in relations:
                expected_witnesses = frozenset((x, y, z) for x, y, z in product((0, 1), repeat=3)
                                               if (x, y) in first.rows and (y, z) in second.rows)
                expected = frozenset((x, z) for x, _, z in expected_witnesses)
                check(rt.witnesses(first, second) == expected_witnesses, "Witness composition mismatch")
                check(rt.compose(first, second).rows == expected, "Relation composition mismatch")
                check(rt.converse(rt.compose(first, second)).rows ==
                      rt.compose(rt.converse(second), rt.converse(first)).rows, "Converse order mismatch")
                self.counts["binary_relation_pairs"] += 1
                for third in relations:
                    left = rt.compose(rt.compose(first, second), third).rows
                    right = rt.compose(first, rt.compose(second, third)).rows
                    # Direct four-coordinate compatibility, independently of either bracketing.
                    direct = frozenset((a, d) for a, b, c, d in product((0, 1), repeat=4)
                                       if (a, b) in first.rows and (b, c) in second.rows and (c, d) in third.rows)
                    check(left == right == direct, "Composition associativity/direct witness mismatch")
                    self.counts["binary_relation_triples"] += 1
        full = relations[-1]
        self.hostile_control("converse_is_always_inverse", rt.compose(full, rt.converse(full)).rows,
                    frozenset({(0, 0), (1, 1)}))
        singleton = rt.Sort("singleton", (0,))
        first = binary_relation(rt, singleton, bit, ((0, 0), (0, 1)))
        second = binary_relation(rt, bit, singleton, ((0, 0), (1, 0)))
        check(len(rt.witnesses(first, second)) == 2 and len(rt.compose(first, second).rows) == 1,
              "Terminal ONE must coexist with MANY middle witnesses")
        self.hostile_control("terminal_output_counts_paths", len(rt.compose(first, second).rows), len(rt.witnesses(first, second)))

    def quotient_censuses(self):
        rt = self.rt
        for kind in ("det", "nondet", "stoch"):
            for n in range(4):
                states = tuple(range(n))
                if kind == "det":
                    options = tuple(range(-1, n))
                elif kind == "nondet":
                    options = tuple(subsets(states))
                else:
                    options = tuple(compositions(2, n))
                for encoded in product(options, repeat=n):
                    if kind == "det":
                        oracle_input = {x: y for x, y in enumerate(encoded) if y >= 0}
                        runtime_input = oracle_input.copy()
                        function = rt.deterministic_quotient
                    elif kind == "nondet":
                        oracle_input = dict(enumerate(encoded))
                        runtime_input = oracle_input.copy()
                        function = rt.nondeterministic_quotient
                    else:
                        oracle_input = {x: dict(enumerate(row)) for x, row in enumerate(encoded)}
                        runtime_input = {x: {y: Fraction(count, 2) for y, count in row.items()}
                                         for x, row in oracle_input.items()}
                        function = rt.stochastic_quotient
                    for partition in partitions(n):
                        summary = dict(enumerate(partition))
                        for obs in product((0, 1), repeat=n):
                            observation = dict(enumerate(obs))
                            expected = oracle_quotient(states, summary, observation, oracle_input, kind)
                            actual = function(states, summary, observation, runtime_input)
                            check((actual["status"] == "ACCEPT") == (expected is not None), f"{kind} acceptance mismatch")
                            if expected is not None:
                                check(actual == expected, f"{kind} quotient table mismatch")
                            self.counts[kind + "_quotient_cases"] += 1
                            self.counts[kind + "_" + actual["status"].lower()] += 1
        states, c, o = (0, 1), {0: 0, 1: 0}, {0: 0, 1: 0}
        rejected = rt.deterministic_quotient(states, c, o, {0: 0})
        check(rejected["reason"] == "enabledness", "Enabledness witness not identified")
        self.hostile_control("ignore_partial_enabledness", "ACCEPT", rejected["status"])
        self.admission("transition exits carrier", lambda: rt.deterministic_quotient(states, c, o, {0: 2}))
        self.admission("summary not total", lambda: rt.deterministic_quotient(states, {0: 0}, o, {}))
        self.admission("missing nondeterministic row", lambda: rt.nondeterministic_quotient(states, c, o, {0: frozenset()}))
        self.admission("Boolean summary key", lambda: rt.deterministic_quotient(states, {False: 0, 1: 0}, o, {}))
        self.admission("Boolean transition key", lambda: rt.deterministic_quotient(states, c, o, {False: 0}))
        self.admission("Boolean nondeterministic key", lambda: rt.nondeterministic_quotient(states, c, o, {False: frozenset(), 1: frozenset()}))
        states, c, o = (0, 1, 2, 3), {0: 0, 1: 0, 2: 1, 3: 2}, dict.fromkeys(range(4), 0)
        n = {0: frozenset({2}), 1: frozenset({3}), 2: frozenset({2}), 3: frozenset({3})}
        rejected = rt.nondeterministic_quotient(states, c, o, n)
        self.hostile_control("same_observations_replace_successor_blocks", "ACCEPT", rejected["status"])
        k = {x: {y: Fraction(int(x == y)) for y in states} for x in states}
        k[0] = {0: Fraction(0), 1: Fraction(0), 2: Fraction(1, 2), 3: Fraction(1, 2)}
        k[1] = {0: Fraction(0), 1: Fraction(0), 2: Fraction(1, 4), 3: Fraction(3, 4)}
        rejected = rt.stochastic_quotient(states, c, o, k)
        integer_kernel = {x: {y: int(4 * mass) for y, mass in row.items()} for x, row in k.items()}
        check(oracle_quotient(states, c, o, integer_kernel, "stoch", 4) is None, "Independent equal-support law control failed")
        check(rejected["reason"] == "pushforward_mass", "Equal-support unequal-law control failed")
        self.hostile_control("support_equality_replaces_mass_equality", "ACCEPT", rejected["status"])
        bad = {x: row.copy() for x, row in k.items()}
        bad[0][2] = 0.5
        self.admission("inexact float probability", lambda: rt.stochastic_quotient(states, c, o, bad))
        bad[0][2] = Fraction(-1, 2)
        self.admission("negative probability", lambda: rt.stochastic_quotient(states, c, o, bad))
        bad[0][2] = Fraction(0)
        self.admission("unnormalized probability", lambda: rt.stochastic_quotient(states, c, o, bad))
        del bad[0][0]
        self.admission("omitted zero mass", lambda: rt.stochastic_quotient(states, c, o, bad))
        boolean_key_kernel = {x: row.copy() for x, row in k.items()}
        boolean_key_kernel[0] = {False: Fraction(0), 1: Fraction(0), 2: Fraction(1, 2), 3: Fraction(1, 2)}
        self.admission("Boolean probability destination key", lambda: rt.stochastic_quotient(states, c, o, boolean_key_kernel))
        boolean_outer_kernel = {False: k[0], 1: k[1], 2: k[2], 3: k[3]}
        self.admission("Boolean probability source key", lambda: rt.stochastic_quotient(states, c, o, boolean_outer_kernel))

    def examples(self):
        rt = self.rt
        a = rt.Occurrence("ctx", "o1", "digit", 5)
        b = rt.Occurrence("ctx", "o2", "digit", 5)
        c = rt.Occurrence("ctx", "right", "digit", 5)
        seams = rt.attach_occurrences((a, b), (c,))
        check(seams == frozenset({(a, c), (b, c)}), "Equal-valued occurrence identity was lost")
        self.hostile_control("value_projection_is_occurrence_identity", 1, len(seams))
        self.admission("conflicting occurrence payload", lambda: rt.attach_occurrences((a,), (rt.Occurrence("ctx", "o1", "digit", 6),)))
        states = tuple("pquvr")
        o = {x: int(x == "r") for x in states}
        t = {"p": "u", "q": "v", "u": "r", "v": "v", "r": "r"}
        question = {x: o[t[x]] for x in states}
        refined = rt.refine_question(states, o, question)
        check(refined["u"] != refined["v"] and refined["p"] == refined["q"], "Wrong question refinement")
        rejected = rt.deterministic_quotient(states, refined, o, t)
        check(rejected["status"] == "REJECT" and o[t[t["p"]]] != o[t[t["q"]]], "Refinement hostile control failed")
        self.hostile_control("one_witness_refinement_already_closed", "ACCEPT", rejected["status"])
        edge = rt.Sort("edge", (0,))
        middle = rt.Sort("middle", (0, 1))
        first = binary_relation(rt, edge, middle, ((0, 1),))
        second = binary_relation(rt, middle, edge, ((1, 0),))
        guarded = rt.compose(first, second, frozenset({0})).rows
        check(guarded == frozenset(), "Guarded bridge introduced an extra intermediate")
        self.hostile_control("unguarded_target_composition", rt.compose(first, second).rows, guarded)
        self.admission("out-of-carrier guard", lambda: rt.compose(first, second, frozenset({2})))
        self.admission("Boolean middle guard", lambda: rt.compose(first, second, frozenset({False})))
        other_middle = rt.Sort("other_middle", (0, 1))
        mismatched_second = binary_relation(rt, other_middle, edge, ((1, 0),))
        self.admission("matching values but wrong middle sort", lambda: rt.compose(first, mismatched_second))
        source, rich = (0, 1), tuple(product((0, 1), repeat=2))
        embedding = {x: (x, 0) for x in source}
        retract = {z: z[0] for z in rich}
        # Reversible swap of (1,0) with (0,1); the two embedded inputs land at 0.
        motion = dict(zip(rich, rich))
        motion[(1, 0)], motion[(0, 1)] = (0, 1), (1, 0)
        landed = rt.land(source, rich, embedding, retract, motion)
        check(len(set(motion.values())) == len(rich) and landed == {0: 0, 1: 0}, "Landing countermodel incorrect")
        self.hostile_control("retraction_and_reversible_motion_imply_injective_landing", True, len(set(landed.values())) == len(source))
        self.counts["named_interface_examples"] += 4

    def vacancy(self):
        rt = self.rt
        states = tuple(row for row in product((None, 0, 1), repeat=4) if row.count(None) == 1)
        check(len(states) == 32, "Wrong declared vacancy carrier")
        count = {x: x.count(1) for x in states}
        with_position = {x: (x.count(1), x.index(None)) for x in states}
        for edge in range(3):
            transitions = {}
            moved_question = {}
            for state in states:
                actual = rt.swap_vacancy(state, edge)
                vacancy = state.index(None)
                enabled = vacancy in (edge, edge + 1)
                if enabled:
                    occupied = edge + 1 if vacancy == edge else edge
                    expected = tuple(state[occupied] if j == vacancy else None if j == occupied else state[j]
                                     for j in range(4))
                    check(actual == ("OK", expected), "Swap differs from coordinate assignment oracle")
                    check(expected in states and expected.count(1) == state.count(1), "Swap conservation failed")
                    check(rt.swap_vacancy(expected, edge) == ("OK", state), "Swap inverse failed")
                    transitions[state] = expected
                    moved_question[state] = ("OK", state[occupied])
                    self.counts["vacancy_enabled_moves"] += 1
                else:
                    check(actual == ("FAIL",), "Disabled swap accepted")
                    moved_question[state] = ("FAIL",)
                self.counts["vacancy_edge_queries"] += 1
            check(rt.deterministic_quotient(states, count, count, transitions)["status"] == "REJECT", "Count-only summary decided location")
            check(rt.deterministic_quotient(states, with_position, count, transitions)["status"] == "ACCEPT", "Count+position should support swaps")
            # At least one same summary has different moved-payload answers.
            check(any(with_position[x] == with_position[y] and moved_question[x] != moved_question[y]
                      for x in states for y in states), "Position summary unexpectedly recovers every moving payload")
        self.counts["vacancy_states"] = len(states)
        self.admission("creates second vacancy", lambda: rt.swap_vacancy((None, None, 0, 1), 0))
        self.admission("invalid edge", lambda: rt.swap_vacancy(states[0], 3))
        self.hostile_control("creation_preserves_one_vacancy", (None, None, 0, 1).count(None), 1)

    def flick(self):
        rt = self.rt
        # Two clients start with the same snapshot. Each action is a whole
        # refresh or candidate validation/commit; callbacks are deterministic.
        actions = tuple(("refresh", who, None) for who in range(2)) + tuple(
            (mode, who, value) for who in range(2) for mode, value in (("valid", "A"), ("valid", "B"), ("invalid", "A")))
        for word in product(actions, repeat=4):
            store = rt.StateStore("A")
            actual_saved = [store.snapshot(), store.snapshot()]
            expected_saved = [(0, "A"), (0, "A")]
            version, payload = 0, "A"
            for mode, who, value in word:
                if mode == "refresh":
                    actual_saved[who] = store.snapshot()
                    expected_saved[who] = (version, payload)
                else:
                    expected = ("REJECT_STALE" if expected_saved[who] != (version, payload)
                                else "REJECT_INVALID" if mode == "invalid" else "COMMITTED")
                    actual = store.flick(actual_saved[who], value, lambda _p, _c, m=mode: m == "valid")
                    check(actual == expected, "FLICK schedule disagrees with monotone-version reference")
                    if expected == "COMMITTED":
                        version, payload = version + 1, value
                snap = store.snapshot()
                check((snap.version, snap.payload) == (version, payload), "FLICK store state mismatch")
                self.counts["flick_schedule_steps"] += 1
            self.counts["flick_schedules"] += 1
        store = rt.StateStore("A")
        old = store.snapshot()
        check(store.flick(old, "B", lambda *_: True) == "COMMITTED", "ABA first leg failed")
        check(store.flick(store.snapshot(), "A", lambda *_: True) == "COMMITTED", "ABA return leg failed")
        result = store.flick(old, "B", lambda *_: True)
        check(result == "REJECT_STALE" and store.snapshot().version == 2, "ABA stale commit accepted")
        self.hostile_control("content_only_ABA_parent_match", "COMMITTED", result)
        other = rt.StateStore("A")
        check(other.flick(rt.StateStore("A").snapshot(), "B", lambda *_: True) == "REJECT_STALE", "Cross-store parent accepted")
        parent = other.snapshot()
        invalid_result = other.flick(parent, "B", lambda *_: False)
        check(invalid_result == "REJECT_INVALID" and other.snapshot() == parent, "Invalid candidate mutated state")
        self.hostile_control("validation_gate_ignored", "COMMITTED", invalid_result)
        self.admission("Boolean snapshot version", lambda: rt.Snapshot(parent.store_id, False, "A"))
        self.admission("mutable store payload", lambda: rt.StateStore(["A"]))
        for validator in (lambda *_: 1, lambda *_: (_ for _ in ()).throw(ValueError("failure"))):
            try:
                other.flick(parent, "B", validator)
            except rt.ValidatorError:
                check(other.snapshot() == parent, "Validator error changed state")
                self.counts["validator_errors_rejected"] += 1
            else:
                raise ConformanceFailure("Validator error was not reported")
        race_store = rt.StateStore("A")
        race_parent = race_store.snapshot()
        barrier = Barrier(2)
        def validate(_parent, _candidate):
            barrier.wait(timeout=5)
            return True
        with ThreadPoolExecutor(max_workers=2) as pool:
            futures = [pool.submit(race_store.flick, race_parent, value, validate) for value in ("A", "B")]
            outcomes = [future.result(timeout=10) for future in futures]
        check(sorted(outcomes) == ["COMMITTED", "REJECT_STALE"] and race_store.snapshot().version == 1,
              "Concurrent candidates both installed or neither installed")
        self.counts["forced_concurrent_races"] += 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Absolute JSON output path")
    args = parser.parse_args()
    output = args.output or HERE.parent / ".artifacts/core.json"
    check(args.output is None or args.output.is_absolute(), "Output override must be absolute")
    check(not output.resolve().is_relative_to(HERE), "Outputs may not overwrite public source files")
    output.parent.mkdir(parents=True, exist_ok=True)
    runtime_path, verifier_path = HERE.parent / "rprm/core.py", Path(__file__).resolve()
    hashes = {path.relative_to(HERE.parent).as_posix(): digest(path) for path in (runtime_path, verifier_path)}
    receipt = {"schema": "rprm-core-conformance-v1", "status": "FAIL_IMPLEMENTATION",
               "started_utc": datetime.now(timezone.utc).isoformat(), "source_sha256": hashes,
               "evidence_grade": "finite_test", "prior_censuses_imported": False}
    suite = None
    try:
        spec = importlib.util.spec_from_file_location("rprm_checked_runtime", runtime_path)
        check(spec is not None and spec.loader is not None, "Cannot load repository runtime")
        rt = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = rt
        spec.loader.exec_module(rt)
        suite = Suite(rt)
        for task in (suite.relations, suite.quotient_censuses, suite.examples, suite.vacancy, suite.flick):
            task()
        check(hashes == {path.relative_to(HERE.parent).as_posix(): digest(path) for path in (runtime_path, verifier_path)}, "Sources changed during replay")
        receipt["status"] = "PASS"
    except Exception as error:
        receipt["error_type"], receipt["error"] = type(error).__name__, str(error)
    if suite is not None:
        receipt["counts"] = dict(sorted(suite.counts.items()))
        receipt["hostile_controls_rejected"] = suite.controls
        receipt["hostile_control_count"] = len(suite.controls)
    receipt["finished_utc"] = datetime.now(timezone.utc).isoformat()
    output.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2))
    return 0 if receipt["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
