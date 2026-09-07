"""Replay square-frontier expansion, finite donut audits and the Fermat bridge.

Code: 0BSD. Complete arithmetic census through 390625; finite certificates do
not prove an unrestricted Fermat theorem. All requirements survive Python -O.
"""

import argparse
import hashlib
import importlib.util
import json
from math import isqrt
import os
from pathlib import Path
import sys
from time import perf_counter
from uuid import uuid4


ROOT = Path(__file__).resolve().parents[1]
SOURCES = ("experimental/primes/square_frontier.py", "checks/prime_frontier.py",
           "rprm/proof_donut.py", "checks/fermat.py")
SCHEMA = "rprm-square-frontier-checks/v1"
LABELS = ("PRIME", "COMPOSITE")


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load(name, relative_path):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(",", ":")).encode()).hexdigest()


def source_hashes():
    return {path: hashlib.sha256((ROOT / path).read_bytes()).hexdigest() for path in SOURCES}


def oracle_factor(n):
    """Independent oracle: try every integer divisor, without a prime list."""
    for divisor in range(2, isqrt(n) + 1):
        if n % divisor == 0:
            return divisor
    return 0


def aperture(pd, givens, expected, observed):
    """Complete two-witness classification relation, with total identity maps."""
    return pd.audit_finite_aperture(
        givens, LABELS, expected, givens, LABELS, observed,
        {n: n for n in givens}, {(n, label): label for n in givens for label in LABELS})


def audit_expansion(pd, source, target, answers, factors, chunk_size=256):
    require(all(type(state) is tuple and len(state) == 2 for state in (source, target)),
            "stage states must be exact bound/list pairs")
    bound, primes = source
    next_bound, next_primes = target
    require(type(bound) is int and bound >= 2, "invalid source bound")
    require(type(next_bound) is int and next_bound == bound * bound, "wrong square successor")
    require(all(type(values) is tuple and all(type(p) is int and p >= 2 for p in values)
                for values in (primes, next_primes)), "prime states need exact integer tuples")
    require(type(chunk_size) is int and chunk_size > 0, "chunk size must be a positive integer")
    require(next_bound < len(factors), "oracle does not cover the successor")
    require(primes == tuple(n for n in range(2, bound + 1) if factors[n] == 0),
            "source prime list is incomplete or corrupt")
    require(next_primes == tuple(n for n in range(2, next_bound + 1) if factors[n] == 0),
            "successor prime list is incomplete or corrupt")
    require(type(answers) is tuple and len(answers) == next_bound - 1,
            "classification must cover every candidate exactly once")
    composite_count = 0
    for n, answer in enumerate(answers, 2):
        require(type(answer) is tuple and len(answer) == 2 and type(answer[0]) is bool
                and type(answer[1]) is int, "malformed classification or factor")
        prime, factor = answer
        require((prime and factor == 0) or
                (not prime and 2 <= factor < n and n % factor == 0),
                "invalid factor witness at " + str(n))
        require(factor == factors[n], "wrong smallest factor at " + str(n))
        composite_count += not prime
    chunks = 0
    covered = 0
    for first in range(2, next_bound + 1, chunk_size):
        givens = tuple(range(first, min(first + chunk_size, next_bound + 1)))
        expected = tuple((n, LABELS[factors[n] != 0]) for n in givens)
        observed = tuple((n, LABELS[not answers[n - 2][0]]) for n in givens)
        result = aperture(pd, givens, expected, observed)
        require(result["status"] == "ACCEPT", "classification aperture rejected: " + str(result))
        chunks += 1
        covered += len(givens)
    require(covered == next_bound - 1, "aperture chunks missed candidates")
    return {"source_bound": bound, "target_bound": next_bound,
            "classifications": covered, "composite_factor_witnesses": composite_count,
            "aperture_chunks": chunks, "prime_count": len(next_primes),
            "prime_list_sha256": digest(next_primes), "answers_sha256": digest(answers)}


def auxiliary_bridge(records, final_frontier, fermat):
    require(type(records) in (tuple, list), "auxiliary records must be materialized")
    require(all(type(row) in (tuple, list) and len(row) == 2
                and all(type(value) is int for value in row) for row in records),
            "malformed auxiliary pair")
    primes = set(final_frontier.primes)
    expected = tuple(p for p in final_frontier.primes if 3 <= p <= 1999)
    require(tuple(p for p, _ in records) == expected, "incomplete or duplicate exponent census")
    checked = []
    for p, q in records:
        require(p in primes and q in primes, "auxiliary primality missing from frontier")
        # Frontier certificates gate the existing checker, whose independent
        # primality checks and complete residue reconstruction remain active.
        checked.append(fermat.auxiliary(p, q))
    return {"certificates": len(checked), "frontier_primality_ports": 2 * len(checked),
            "exponent_census": len(expected), "largest_p": max(expected),
            "largest_q": max(q for _, q in records),
            "source_powers": sum(row["source_powers"] for row in checked),
            "distinct_residues_per_modulus": sum(row["residues"] for row in checked)}


def run():
    started = perf_counter()
    before = source_hashes()
    model = load("square_frontier", SOURCES[0])
    pd = load("frontier_proof_donut", SOURCES[2])
    fermat = load("frontier_fermat", SOURCES[3])
    # The two leading placeholders are outside the classified carrier.
    factors = (0, 0) + tuple(oracle_factor(n) for n in range(2, 390626))
    frontier = model.Frontier(5, (2, 3, 5))
    states, stages, expansions = [frontier.state], [], []
    for expected_bound in (25, 625, 390625):
        successor, answers = frontier.expand()
        require(successor.bound == expected_bound, "unexpected frontier sequence")
        stages.append(audit_expansion(pd, frontier.state, successor.state, answers, factors))
        expansions.append((frontier, successor, answers))
        states.append(successor.state)
        frontier = successor
    transition = dict(zip(states, states[1:]))
    path = pd.audit_finite_path(tuple(states), transition, tuple(states))
    require(path["status"] == "ACCEPT", "complete-state stage path rejected")
    auxiliaries = auxiliary_bridge(fermat.AUXILIARIES, frontier, fermat)
    require(auxiliaries["certificates"] == 302 and auxiliaries["source_powers"] == 4052680
            and auxiliaries["distinct_residues_per_modulus"] == 3936, "Fermat census changed")

    controls = []

    def rejected(label, call, exception=ValueError):
        try:
            call()
        except exception:
            controls.append(label)
        else:
            raise RuntimeError("hostile input accepted: " + label)

    def reject_aperture(label, n, expected, observed):
        result = aperture(pd, (n,), ((n, expected),), observed)
        require(result["status"] == "REJECT", "hostile aperture accepted: " + label)
        controls.append(label)

    seed, first, first_answers = expansions[0]
    for label, call in (
        ("missing_seed_prime_5", lambda: model.Frontier(5, (2, 3))),
        ("duplicate_prime", lambda: model.Frontier(5, (2, 3, 3, 5))),
        ("unordered_primes", lambda: model.Frontier(5, (3, 2, 5))),
        ("composite_in_prime_list", lambda: model.Frontier(5, (2, 3, 4, 5))),
        ("boolean_bound", lambda: model.Frontier(True, (2,))),
        ("float_prime", lambda: model.Frontier(5, (2, 3, 5.0))),
        ("one_shot_prime_list", lambda: model.Frontier(5, iter((2, 3, 5)))),
        ("below_minimum_bound", lambda: model.Frontier(1, ())),
        ("out_of_region_49", lambda: seed.classify(49)),
        ("candidate_below_two", lambda: seed.classify(1)),
        ("boolean_candidate", lambda: seed.classify(True)),
        ("float_candidate", lambda: seed.classify(2.0)),
    ):
        rejected(label, call)
    require(seed.classify(2) == (True, 0) and seed.classify(5) == (True, 0),
            "prime must not divide itself before the square test")
    require(seed.classify(25) == (False, 5), "perfect square endpoint must remain composite")
    require(first.classify(601) == (True, 0), "exhaustion must return prime")
    require(first.classify(49) == (False, 7), "expanded frontier must catch 49")
    reject_aperture("prime_self_divisor_mutation", 5, "PRIME", ((5, "COMPOSITE"),))
    reject_aperture("square_off_by_one_mutation", 25, "COMPOSITE", ((25, "PRIME"),))
    reject_aperture("unchecked_missing_5_mutation", 25, "COMPOSITE", ((25, "PRIME"),))
    reject_aperture("wrong_exhaustion_mutation", 601, "PRIME", ())
    corrupt_factor = tuple((False, 4) if n == 15 else answer
                           for n, answer in enumerate(first_answers, 2))
    for label, source, target, answers in (
        ("corrupt_source_stage", (5, (2, 3)), first.state, first_answers),
        ("float_source_prime", (5, (2, 3, 5.0)), first.state, first_answers),
        ("float_successor_prime", seed.state, (25, first.primes[:-1] + (23.0,)), first_answers),
        ("corrupt_successor_list", seed.state, (25, first.primes + (25,)), first_answers),
        ("corrupt_factor", seed.state, first.state, corrupt_factor),
        ("missing_classification", seed.state, first.state, first_answers[:-1]),
        ("wrong_successor_bound", seed.state, (26, first.primes), first_answers),
    ):
        rejected(label, lambda s=source, t=target, a=answers:
                 audit_expansion(pd, s, t, a, factors), RuntimeError)
    hostile_path = pd.audit_finite_path(tuple(states), transition, (states[0], states[2]))
    require("WRONG_STEP" in hostile_path["errors"], "skipped stage accepted")
    controls.append("skipped_full_state_successor")
    rejected("missing_auxiliary_exponent", lambda:
             auxiliary_bridge(fermat.AUXILIARIES[:-1], frontier, fermat), RuntimeError)
    rejected("duplicate_auxiliary_exponent", lambda:
             auxiliary_bridge(fermat.AUXILIARIES + fermat.AUXILIARIES[:1], frontier, fermat), RuntimeError)
    residue_controls = []
    for p, q in ((3, 19), (13, 443)):
        require(p in frontier.primes and q in frontier.primes, "hostile pair must have prime inputs")
        residues = {pow(a, p, q) for a in range(1, q)}
        intersection = sorted(residues & {(1 - r) % q for r in residues})
        p_in_residues = p % q in residues
        require((p, intersection, p_in_residues) in ((3, [8, 12], False), (13, [], True)),
                "hostile residue witness changed")
        rejected("residue_failure_" + str(p) + "_" + str(q), lambda p=p, q=q: fermat.auxiliary(p, q))
        residue_controls.append({"p": p, "q": q, "both_prime": True,
                                 "intersection": intersection, "p_in_residues": p_in_residues})
    require(source_hashes() == before, "source bytes changed during replay")
    return {"schema": SCHEMA, "status": "PASS", "source_sha256": before,
            "bounds": [state[0] for state in states], "stages": stages,
            "seed_prime_count": 3, "seed_candidates": 4,
            "unique_candidates": len(factors) - 2,
            "stage_classifications": sum(stage["classifications"] for stage in stages),
            "aperture_chunks": sum(stage["aperture_chunks"] for stage in stages),
            "path": {"status": path["status"], "complete_states": len(states), "edges": len(transition)},
            "auxiliaries": auxiliaries, "hostile_controls": controls,
            "hostile_control_count": len(controls), "residue_controls": residue_controls,
            "elapsed_seconds": round(perf_counter() - started, 6),
            "scope": "Complete finite prime classifications and stage path; primality feeds all 302 existing first-case residue certificates.",
            "general_square_frontier_rule": "Written factor-bound proof supplies the parameterized continuation; finite checks audit its instances.",
            "unrestricted_fermat": "OPEN: uniform zero-exclusion or an integer, equation-preserving strict descent remains unsupplied.",
            "formal_proof_of_prose": False, "full_fermat_proof": False}


def write_result(path, result):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + "." + uuid4().hex + ".tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Optional absolute JSON receipt path")
    args = parser.parse_args()
    if args.output is not None and not args.output.is_absolute():
        parser.error("--output must be an absolute JSON path")
    # When requested, this receipt precedes every model/checker import.
    if args.output is not None:
        write_result(args.output, {"schema": SCHEMA, "status": "PENDING"})
    try:
        result = run()
    except Exception as exc:
        if args.output is not None:
            write_result(args.output, {"schema": SCHEMA, "status": "FAIL",
                                       "error": f"{type(exc).__name__}: {exc}"})
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    if args.output is not None:
        write_result(args.output, result)
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
