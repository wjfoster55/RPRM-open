"""Exhaustive finite and hostile checks for proof_donut.py (0BSD)."""

from __future__ import annotations

import argparse
from itertools import product
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from rprm import proof_donut as pd
from rprm.core import deterministic_quotient


def run():
    counts = {"named_contract_checks": 0, "admission_controls": 0,
              "aperture_certificates": 0, "induction_certificates": 0,
              "descent_certificates": 0, "quotient_comparisons": 0}

    def expect(condition, label):
        if not condition:
            raise RuntimeError(label)
        counts["named_contract_checks"] += 1

    def accepted(result):
        return result["status"] == "ACCEPT"

    def malformed(call):
        try:
            call()
        except pd.AdmissionError:
            counts["admission_controls"] += 1
            return
        raise RuntimeError("Malformed input was admitted")

    hypotheses = (0, 1, 2, 3)
    parity = {h: h % 2 == 0 for h in hypotheses}
    many = pd.fiber_disposition(hypotheses, parity, parity)
    expect(many["fiber"] == "MANY" and many["count"] == 2 and many["decision"] is True, "homogeneous fiber")
    mixed = pd.fiber_disposition(hypotheses, {h: True for h in hypotheses}, parity)
    expect(not mixed["decided"] and len(mixed["answers"]) == 2, "mixed fiber")
    empty = pd.fiber_disposition(hypotheses, {h: False for h in hypotheses}, parity)
    expect(empty["fiber"] == "NONE" and not empty["decided"], "empty fiber is not a vacuous decision")
    unique = pd.fiber_disposition(hypotheses, {h: h == 2 for h in hypotheses}, parity)
    expect(unique["fiber"] == "ONE" and unique["members"] == (2,), "unique fiber")
    typed = pd.fiber_disposition((0, 1), {0: True, 1: True}, {0: True, 1: 1})
    expect(not typed["decided"], "Boolean and integer answer sorts remain distinct")
    none_answer = pd.fiber_disposition((0,), {0: True}, {0: None})
    expect(none_answer["decided"] and none_answer["decision"] is None, "None answer distinguished from undecided")

    # A bitmask oracle compares existential signatures. The implementation
    # instead forms typed witness-image sets for every original given input.
    givens = (0, 1)
    witnesses = (0, 1)
    beta = {(g, w): "v" for g in givens for w in witnesses}
    for concrete_mask in range(16):
        concrete = tuple((g, w) for g in givens for w in witnesses if concrete_mask & (1 << (2*g+w)))
        for abstract_mask in range(4):
            abstract = tuple((g, "v") for g in givens if abstract_mask & (1 << g))
            for alpha_values in product(givens, repeat=2):
                alpha = dict(zip(givens, alpha_values))
                expected = all(bool(concrete_mask & (3 << (2*g))) == bool(abstract_mask & (1 << alpha[g])) for g in givens)
                actual = pd.audit_finite_aperture(givens, witnesses, concrete, givens, ("v",), abstract, alpha, beta)
                if accepted(actual) != expected:
                    raise RuntimeError("Aperture differs from existential-signature oracle")
                counts["aperture_certificates"] += 1

    # Path enumeration from every safe state is an independent finite oracle
    # for invariant closure of each total two-state transition.
    states2 = (0, 1)
    subsets = [tuple(x for x in states2 if mask & (1 << x)) for mask in range(4)]
    for targets in product(states2, repeat=2):
        op = dict(zip(states2, targets))
        for seeds, safe, bad in product(subsets, repeat=3):
            visited = set()
            for start in safe:
                x = start
                for _ in range(3):
                    visited.add(x)
                    x = op[x]
            expected = set(seeds) <= set(safe) and not set(safe) & set(bad) and visited <= set(safe)
            actual = pd.audit_finite_induction(states2, seeds, (op,), safe, bad)
            if accepted(actual) != bool(expected):
                raise RuntimeError("Induction differs from bounded-path oracle")
            counts["induction_certificates"] += 1
    expect("TOTAL_TRANSITION" in pd.audit_finite_induction(states2, (0,), ({0: 1},), states2, ())["errors"], "partial induction table")

    # Under this complete finite carrier/rank, a nonempty bad set cannot
    # satisfy descent. The oracle uses that theorem, not the checker's steps.
    states3 = (0, 1, 2)
    for mask in range(8):
        bad = tuple(i for i in states3 if mask & (1 << i))
        for targets in product((None, 0, 1, 2), repeat=3):
            step = {i: t for i, t in enumerate(targets) if t is not None}
            result = pd.audit_finite_descent(states3, (0,), bad, {0: 0, 1: 1, 2: 2}, step)
            if accepted(result) != (mask == 0):
                raise RuntimeError("Invalid finite descent certificate accepted")
            counts["descent_certificates"] += 1

    # Independent pairwise auditing is compared with the core's block/profile
    # construction. Neither implementation imports the other.
    for labels in product((0, 1), repeat=3):
        summary = dict(zip(states3, labels))
        for outputs in product((0, 1), repeat=3):
            observation = dict(zip(states3, outputs))
            for targets in product((None, 0, 1, 2), repeat=3):
                transition = {x: y for x, y in zip(states3, targets) if y is not None}
                core = deterministic_quotient(states3, summary, observation, transition)
                independent = pd.audit_finite_quotient(states3, summary, observation, transition)
                if accepted(core) != accepted(independent):
                    raise RuntimeError("Core and independent quotient audit disagree")
                counts["quotient_comparisons"] += 1

    cycle_states = ((0, 1), (1, 2), (2, 3), (3, 0))
    cycle_map = {s: cycle_states[(i+1) % 4] for i, s in enumerate(cycle_states)}
    expect(accepted(pd.audit_finite_path(cycle_states, cycle_map, cycle_states + cycle_states[:1], cycle=True)), "full pair cycle")
    expect("NOT_CLOSED" in pd.audit_finite_path(cycle_states, cycle_map, cycle_states, cycle=True)["errors"], "incomplete cycle")
    expect("ZERO_LENGTH_CYCLE" in pd.audit_finite_path((0,), {0: 0}, (0,), cycle=True)["errors"], "positive period required")
    expect("WRONG_STEP" in pd.audit_finite_path((0, 1), {0: 1, 1: 0}, (0, 0))["errors"], "wrong route edge")
    expect("UNDEFINED_STEP" in pd.audit_finite_path((0, 1), {0: 1}, (1, 0))["errors"], "disabled route edge")
    expect(accepted(pd.audit_finite_path((0,), {}, (0,))), "zero-edge path is valid when cycle not requested")

    # A relation-join control must retain the shared root, not only its square.
    roots = tuple(range(1, 6))
    direct = {(w, w**3) for w in roots}
    joined = {(w, u*w) for w in roots for u in (w*w,)}
    forgotten = {w1*w1*w2 for w1 in roots for w2 in roots}
    expect(joined == direct and 2 in forgotten and 2 not in {v for _, v in direct}, "shared witness control")

    states4 = (0, 1, 2, 3)
    summary4 = {x: x % 2 for x in states4}
    op4 = {0: 1, 1: 0, 2: 3, 3: 2}
    expect(accepted(pd.audit_finite_quotient(states4, summary4, summary4, op4)) and
           accepted(deterministic_quotient(states4, summary4, summary4, op4)) and
           accepted(pd.audit_finite_induction(states4, (0,), (op4,), (0, 1), (2, 3))), "finite mutual-use model")
    hostile = dict(op4)
    hostile[2] = 2
    expect("SUCCESSOR" in pd.audit_finite_quotient(states4, summary4, summary4, hostile)["errors"], "present output does not certify future quotient")

    malformed(lambda: pd.fiber_disposition(iter((0,)), {0: True}, {0: 0}))
    malformed(lambda: pd.fiber_disposition((0, 0), {0: True}, {0: 0}))
    malformed(lambda: pd.fiber_disposition((False,), {False: True}, {False: 0}))
    malformed(lambda: pd.fiber_disposition((0,), {0: 1}, {0: 0}))
    malformed(lambda: pd.fiber_disposition((0,), {}, {0: 0}))
    malformed(lambda: pd.fiber_disposition((0,), {0: True}, {0: 0.0}))
    malformed(lambda: pd.audit_finite_induction((0,), (1,), ({0: 0},), (0,), ()))
    malformed(lambda: pd.audit_finite_induction((0,), (0,), ({0: 1},), (0,), ()))
    malformed(lambda: pd.audit_finite_descent((0,), (), (), {0: -1}, {}))
    malformed(lambda: pd.audit_finite_descent((0,), (), (), {0: False}, {}))
    malformed(lambda: pd.audit_finite_descent((0,), (), (), {}, {}))
    malformed(lambda: pd.audit_finite_path((0,), {0: 0}, ()))
    malformed(lambda: pd.audit_finite_path((0,), {0: 0}, (1,)))
    malformed(lambda: pd.audit_finite_path((0,), {0: 0}, (0,), cycle=1))
    malformed(lambda: pd.audit_finite_quotient((0,), {0: False}, {0: 0}, {0: 0}))
    malformed(lambda: pd.audit_finite_aperture((0,), (0,), ((0, 0),), (0,), (0,), ((0, 0),), {0: 0}, {}))
    malformed(lambda: pd.audit_finite_aperture((0,), (0,), ((0, 1),), (0,), (0,), ((0, 0),), {0: 0}, {(0, 0): 0}))

    return {"schema": "rprm-proof-donut-checks/v1", "status": "PASS", "counts": counts,
            "scope": "Finite certificate checks and core comparison; not a proof of arbitrary theory consistency, source coverage, or physical origins."}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Absolute JSON output path")
    args = parser.parse_args()
    if args.output is not None and not args.output.is_absolute():
        parser.error("--output must be an absolute path")
    result = run()
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
