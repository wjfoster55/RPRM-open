"""Finite checks for complete O05 obstruction fibers.

The census null is declared and recorded before any enumeration of the
845-machine family. Counts are not premises; they are the readout.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools as it
import json
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from rprm.core import AdmissionError, deterministic_quotient, stochastic_quotient
from rprm.futures import Machine, future_quotient, shortest_witness
from obstruction import (
    CLAUSES,
    ghost_fiber,
    is_ghost_fold,
    is_operational_fold,
    least_stable_repair,
    merged_pairs,
    min_repair_alphabet,
    obstruction_fiber,
    pair_clause,
    repaired_kernel_matches,
    set_partitions,
)

HERE = Path(__file__).resolve().parent
NULL = (
    "In the checks/futures.py 845-machine family, every partition that is "
    "future-sufficient on its merged pairs is an operational fold, except "
    "the Manifesto three-state example (constant observation, a: 0->0, "
    "1->2, 2->2) and its state relabelings."
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def manifesto_machine():
    return Machine((0, 1, 2), ("a",), {0: 0, 1: 0, 2: 0}, {"a": {0: 0, 1: 2, 2: 2}})


def manifesto_summary():
    return {0: 0, 1: 0, 2: 1}


def is_manifesto_relabeling(machine, summary):
    if machine.states != (0, 1, 2) or machine.actions != ("a",):
        return False
    if len(set(machine.observation.values())) != 1:
        return False
    blocks = {}
    for state, label in summary.items():
        blocks.setdefault(label, []).append(state)
    sizes = sorted(len(block) for block in blocks.values())
    if sizes != [1, 2]:
        return False
    merged = next(block for block in blocks.values() if len(block) == 2)
    singleton = next(block for block in blocks.values() if len(block) == 1)[0]
    table = machine.transitions["a"]
    if set(table) != {0, 1, 2}:
        return False
    a, b = merged
    # Self-loop on one merged state, jump from the other onto the singleton,
    # singleton stays.
    if table[singleton] != singleton:
        return False
    jumps = (table[a] == singleton and table[b] == b) or (table[b] == singleton and table[a] == a)
    return jumps


def check_named_hostiles():
    machine = manifesto_machine()
    summary = manifesto_summary()
    fiber = obstruction_fiber(machine, summary)
    require(fiber["status"] == "ONE", "Manifesto obstruction should be ONE pair")
    require(fiber["pairs"][0] == {"left": 0, "right": 1, "clause": "successor"},
            "Manifesto pair is successor, not observation or enabledness")
    require(shortest_witness(machine, 0, 1)["status"] == "NONE",
            "Manifesto pair must be future-equivalent")
    ghosts = ghost_fiber(machine, summary)
    require(ghosts["status"] == "ONE" and ghosts["pairs"][0]["clause"] == "successor",
            "Manifesto is the ghost-fold exhibit")
    require(not is_operational_fold(machine, summary), "Ghost fold is not operational")
    require(not repaired_kernel_matches(machine, summary), "O09 must split the ghost pair")
    repaired = least_stable_repair(machine, summary)
    require(len(repaired["classes"]) == 3, "Least stable repair of the ghost is discrete")
    require(future_quotient(machine)["classes"] == ((0, 1, 2),),
            "Canonical future quotient is indiscrete")

    # First-witness core hides a second failing pair.
    two = Machine((0, 1, 2, 3), ("a",), {0: 0, 1: 1, 2: 0, 3: 1},
                  {"a": {0: 0, 1: 1, 2: 2, 3: 3}})
    collapsed = {0: 0, 1: 0, 2: 1, 3: 1}
    many = obstruction_fiber(two, collapsed)
    require(many["status"] == "MANY" and many["by_clause"]["observation"] == 2,
            "Two observation failures must be MANY, not the first witness")
    core = deterministic_quotient(two.states, collapsed, dict(two.observation), dict(two.transitions["a"]))
    require(core["status"] == "REJECT" and core["reason"] == "observation",
            "Core first-witness still rejects")
    require(len(core["witness"]) == 2, "Core returns one pair")
    witnessed = tuple(sorted(core["witness"]))
    require(any(tuple(sorted((row["left"], row["right"]))) == witnessed for row in many["pairs"]),
            "Core witness must lie in the complete fiber")

    # n=2 indiscrete: successor is automatic; remaining failures are FIVE-visible.
    binary = Machine((0, 1), ("a",), {0: 0, 1: 0}, {"a": {0: 0}})
    indiscrete = {0: 0, 1: 0}
    require(obstruction_fiber(binary, indiscrete)["status"] == "ONE",
            "Enabledness mismatch on n=2 is an obstruction")
    require(obstruction_fiber(binary, indiscrete)["pairs"][0]["clause"] == "enabledness",
            "n=2 failure is enabledness")
    require(ghost_fiber(binary, indiscrete)["status"] == "NONE",
            "Enabledness is visible to FIVE.future; not a ghost")
    require(shortest_witness(binary, 0, 1)["status"] == "ONE",
            "Enabledness mismatch has a distinguishing word")

    one_block = Machine((0, 1, 2), ("a",), {0: 0, 1: 0, 2: 0}, {"a": {0: 1, 1: 2, 2: 0}})
    require(ghost_fiber(one_block, {0: 0, 1: 0, 2: 0})["status"] == "NONE",
            "A single block cannot ghost-fold: successor is automatic")
    require(is_operational_fold(one_block, {0: 0, 1: 0, 2: 0}),
            "Indiscrete constant-obs total map is operational")

    # O08R repairs the present question while operational obstruction remains.
    five = Machine(("p", "q", "u", "v", "r"), ("a",),
                   {"p": 0, "q": 0, "u": 0, "v": 0, "r": 1},
                   {"a": {"p": "u", "q": "v", "u": "r", "v": "v", "r": "r"}})
    question = dict(five.observation)
    present_only = {state: 0 for state in five.states}
    require(min_repair_alphabet(five.states, present_only, question) == 2,
            "O08R lower bound is the two observation values")
    repaired_tags = {state: (five.observation[state],
                             five.observation[five.transitions["a"][state]])
                     for state in five.states}
    require(min_repair_alphabet(five.states, repaired_tags, question) == 1,
            "Pairing O with O after T already decodes O")
    five_obs = obstruction_fiber(five, repaired_tags)
    require(five_obs["status"] == "MANY" and five_obs["by_clause"]["successor"] >= 1,
            "Question repair is not operational repair")
    require(shortest_witness(five, "p", "q")["word"] == ("a", "a"),
            "Five-state example is FIVE-visible, not a ghost")

    # Empty carrier: O08R is 0; obstruction NONE.
    empty = Machine((), (), {}, {})
    require(min_repair_alphabet((), {}, {}) == 0, "Empty O08R")
    require(obstruction_fiber(empty, {})["status"] == "NONE", "Empty obstruction")
    require(list(set_partitions(())) == [{}], "Empty partition family")

    # KERNEL equal support is not this module's PARTIAL trichotomy.
    # One block cannot witness it: every row pushes mass 1 into the unique
    # class. Need a merged pair and a second class.
    kernel_states = (0, 1, 2)
    equal_support = {
        0: {0: Fraction(1, 2), 1: Fraction(0), 2: Fraction(1, 2)},
        1: {0: Fraction(1, 4), 1: Fraction(0), 2: Fraction(3, 4)},
        2: {0: Fraction(0), 1: Fraction(0), 2: Fraction(1)},
    }
    stochastic = stochastic_quotient(
        kernel_states, {0: 0, 1: 0, 2: 1}, {0: 0, 1: 0, 2: 0}, equal_support)
    require(stochastic["status"] == "REJECT" and stochastic["reason"] == "pushforward_mass",
            "Kernel hostile remains outside PARTIAL obstruction")
    try:
        Machine((0,), ("a",), {False: 0}, {"a": {0: 0}})
    except AdmissionError:
        pass
    else:
        raise RuntimeError("Bool observation key must remain an admission error")
    return {"named_hostiles": 8, "clauses": list(CLAUSES)}


def family_machines():
    machines = []
    for n, actions in ((0, ("a",)), (1, ("a", "b")), (2, ("a", "b")), (3, ("a",))):
        states = tuple(range(n))
        for observations in it.product((0, 1), repeat=n):
            observation = dict(zip(states, observations))
            for flat in it.product(tuple(range(-1, n)), repeat=n * len(actions)):
                tables = {a: {x: flat[j * n + x] for x in states if flat[j * n + x] != -1}
                          for j, a in enumerate(actions)}
                machines.append(Machine(states, actions, observation, tables))
    return machines


def ghost_record(machine, summary):
    table = machine.transitions[machine.actions[0]] if machine.actions else {}
    merged = [state for state in machine.states
              if sum(1 for other in machine.states if summary[other] == summary[state]) > 1]
    singleton = [state for state in machine.states if state not in merged]
    action = machine.actions[0] if machine.actions else None
    total = action is not None and set(table) == set(machine.states)
    constant_obs = len(set(machine.observation.values())) == 1
    singleton_fixed = bool(singleton) and singleton[0] in table and table[singleton[0]] == singleton[0]
    merged_self_loop = any(state in table and table[state] == state for state in merged)
    return {
        "observation": [machine.observation[state] for state in machine.states],
        "next": [table[state] if state in table else -1 for state in machine.states],
        "merged": merged,
        "total": total,
        "constant_observation": constant_obs,
        "singleton_fixed": singleton_fixed,
        "merged_self_loop": merged_self_loop,
        "manifesto_relabeling": is_manifesto_relabeling(machine, summary),
        "pairs": list(ghost_fiber(machine, summary)["pairs"]),
    }


def check_census(null_text):
    machines = family_machines()
    require(len(machines) == 845, "Futures family size changed")
    cases = 0
    folds = 0
    ghosts = []
    ghosts_one_block = 0
    ghosts_two_states = 0
    clause_hits = {clause: 0 for clause in CLAUSES}
    ghost_successor_pairs = 0
    for machine in machines:
        for summary in set_partitions(machine.states):
            cases += 1
            fiber = obstruction_fiber(machine, summary)
            if fiber["status"] == "NONE":
                folds += 1
                require(repaired_kernel_matches(machine, summary),
                        "Empty obstruction must already be O09-stable")
            else:
                require(not repaired_kernel_matches(machine, summary),
                        "Nonempty obstruction must be split by O09")
                for row in fiber["pairs"]:
                    clause_hits[row["clause"]] += 1
            for left, right in merged_pairs(machine, summary):
                clause = pair_clause(machine, left, right, summary)
                word = shortest_witness(machine, left, right)
                if clause in ("observation", "enabledness"):
                    require(word["status"] == "ONE", "Present/enabledness failure is FIVE-visible")
                if fiber["status"] == "NONE":
                    require(word["status"] == "NONE", "Operational fold pairs are future-equivalent")
            require(is_ghost_fold(machine, summary) == (
                fiber["status"] != "NONE" and all(
                    shortest_witness(machine, left, right)["status"] == "NONE"
                    for left, right in merged_pairs(machine, summary))),
                    "Ghost-fold flag disagrees with future-sufficiency plus obstruction")
            if is_ghost_fold(machine, summary):
                record = ghost_record(machine, summary)
                ghosts.append(record)
                ghost_successor_pairs += len(record["pairs"])
                if len(set(summary.values())) == 1:
                    ghosts_one_block += 1
                if len(machine.states) <= 2:
                    ghosts_two_states += 1
                require(machine.states == (0, 1, 2) and machine.actions == ("a",),
                        "Ghost fold escaped the three-state one-action slice")
                require(record["total"], "Ghost fold with a partial merged action")
    require(ghosts_one_block == 0, "Single-block ghost fold appeared")
    require(ghosts_two_states == 0, "n<=2 ghost fold appeared")
    require(all(row["constant_observation"] for row in ghosts),
            "Ghost fold with non-constant observation in this family")
    relabelings = sum(1 for row in ghosts if row["manifesto_relabeling"])
    null_holds = len(ghosts) == relabelings
    return {
        "machines": len(machines),
        "machine_partition_cases": cases,
        "operational_folds": folds,
        "ghost_folds": len(ghosts),
        "ghost_manifesto_relabelings": relabelings,
        "ghost_unexpected_count": len(ghosts) - relabelings,
        "ghost_successor_pairs": ghost_successor_pairs,
        "five_visible_successor_pairs": clause_hits["successor"] - ghost_successor_pairs,
        "ghost_family": ghosts,
        "ghost_shape_counts": {
            "total_maps": sum(1 for row in ghosts if row["total"]),
            "constant_observation": sum(1 for row in ghosts if row["constant_observation"]),
            "singleton_fixed": sum(1 for row in ghosts if row["singleton_fixed"]),
            "merged_self_loop": sum(1 for row in ghosts if row["merged_self_loop"]),
            "singleton_fixed_and_merged_self_loop": sum(
                1 for row in ghosts if row["singleton_fixed"] and row["merged_self_loop"]),
        },
        "failing_pairs_by_clause": clause_hits,
        "null": null_text,
        "null_holds": null_holds,
    }


def source_hashes():
    names = (
        "research/operational-obstruction-2026-09-17/obstruction.py",
        "research/operational-obstruction-2026-09-17/verify.py",
        "rprm/core.py",
        "rprm/futures.py",
        "checks/futures.py",
    )
    return {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in names}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=HERE / "CENSUS.json")
    args = parser.parse_args()
    named = check_named_hostiles()
    census = check_census(NULL)
    result = {
        "schema": "rprm-operational-obstruction/v1",
        "status": "PASS",
        "null_declared_before_census": NULL,
        "named": named,
        "census": census,
        "source_hashes": source_hashes(),
        "coverage": (
            "Named hostiles plus every partition of every machine in the "
            "checks/futures.py 845-machine family. Not a theorem about arbitrary "
            "infinite carriers, nondeterministic operations, or kernels."
        ),
    }
    payload = json.dumps(result, indent=2) + "\n"
    args.output.write_text(payload, encoding="utf-8")
    print(payload)


if __name__ == "__main__":
    main()
