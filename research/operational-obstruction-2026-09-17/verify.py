"""Finite checks for complete O05 obstruction fibers.

The census null is declared and recorded before any enumeration of the
845-machine family. The 2×2 lift nulls are declared before the four-state
and two-action families are enumerated. Counts are not premises; they are
the readout.
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
    GHOST_SHAPES,
    LIFT_TYPES,
    RESIDUE_TYPES,
    block_profile,
    classify_ghost_fold,
    ghost_fiber,
    ghost_fold_detail,
    ghost_shape,
    is_future_sufficient,
    is_ghost_fold,
    is_operational_fold,
    is_typed_residue,
    least_stable_repair,
    lifted_ghost_type,
    merged_pairs,
    min_repair_alphabet,
    obstruction_fiber,
    pair_clause,
    profile_kind,
    repaired_kernel_matches,
    set_partitions,
    structural_lift_flags,
    structural_lift_type,
    unique_pair_witness_set,
)

HERE = Path(__file__).resolve().parent
NULL = (
    "In the checks/futures.py 845-machine family, every partition that is "
    "future-sufficient on its merged pairs is an operational fold, except "
    "the Manifesto three-state example (constant observation, a: 0->0, "
    "1->2, 2->2) and its state relabelings."
)
SHAPE_NULL = (
    "After removing sink_self (the Manifesto sink/self-loop/jump pattern), "
    "the remaining ghost folds in the 845-machine family occupy exactly one "
    "of the leftover named types sink_partner, return_self, return_partner."
)
LISTING = {
    "sink_self": 12,
    "sink_partner": 12,
    "return_self": 24,
    "return_partner": 24,
    "unclassified": 0,
}
LIFT_NULL = (
    "On the four-state one-action family and the three-state two-action "
    "family (binary observations, all partial maps, all set-partitions; the "
    "same constructor as the 845-machine futures family), every ghost fold "
    "still receives one of the four names sink_self, sink_partner, "
    "return_self, return_partner."
)
LIFT_EXHAUSTION_NULL = (
    "On those two families, every ghost fold receives a name in the a priori "
    "lift vocabulary {sink_self, sink_partner, return_self, return_partner, "
    "split, escape, crowd, multi, mixed, partial_land, wide_landing}; "
    "unclassified is NONE."
)
SLICE_NULL = (
    "On the four-state one-action family and the three-state two-action "
    "family, every ghost fold whose block profile has exactly one size-2 "
    "class and no larger class still receives one of the four names "
    "sink_self, sink_partner, return_self, return_partner."
)
MATCH_NULL = (
    "On the four-state one-action family and the three-state two-action "
    "family, every ghost fold named split, escape, crowd, multi, or mixed "
    "satisfies the typed definition of that name, and every ghost fold "
    "satisfying one of those five definitions receives that name. The five "
    "definitions are pairwise exclusive. Unclassified is NONE."
)
LIFT_SLICES = (
    {"name": "four_state_one_action", "n": 4, "actions": ("a",)},
    {"name": "three_state_two_action", "n": 3, "actions": ("a", "b")},
)
# Census readout, locked after the first lift enumeration. Not a premise of the nulls.
FOUR_STATE_READOUT = {
    "sink_self": 480,
    "sink_partner": 480,
    "return_self": 960,
    "return_partner": 960,
    "split": 624,
    "escape": 384,
    "crowd": 1152,
    "multi": 1152,
    "mixed": 0,
    "partial_land": 0,
    "wide_landing": 0,
    "unclassified": 0,
}
TWO_ACTION_READOUT = {
    "sink_self": 408,
    "sink_partner": 408,
    "return_self": 864,
    "return_partner": 864,
    "split": 0,
    "escape": 0,
    "crowd": 0,
    "multi": 0,
    "mixed": 624,
    "partial_land": 0,
    "wide_landing": 0,
    "unclassified": 0,
}
# Unique-pair hostile readout: split+escape+mixed on the unique-pair slice.
UNIQUE_PAIR_RESIDUE_READOUT = 1632


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def require_structural_name(machine, summary, name):
    """Classifier and typed flags name the same unique lift type."""
    require(classify_ghost_fold(machine, summary) == name,
            "Classifier missed " + name)
    require(structural_lift_type(machine, summary) == name,
            "Typed flags missed " + name)
    flags = structural_lift_flags(machine, summary)
    require(sum(1 for bit in flags.values() if bit) == 1,
            "Typed flags must be pairwise exclusive on " + name)
    require(flags[name], "Typed flag " + name + " must fire")


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
    require(ghost_shape(machine, summary) == "sink_self",
            "Manifesto example is sink_self")
    require_structural_name(machine, summary, "sink_self")
    require(all(not is_typed_residue(machine, summary, name) for name in RESIDUE_TYPES),
            "Manifesto 2x2 is not a residue type")

    # Three leftover types, built from the 2×2 definition, not from the census.
    sink_partner = Machine((0, 1, 2), ("a",), {0: 0, 1: 0, 2: 0},
                           {"a": {0: 1, 1: 2, 2: 2}})
    require(is_ghost_fold(sink_partner, summary), "sink_partner must be a ghost fold")
    require(ghost_shape(sink_partner, summary) == "sink_partner", "Named sink_partner")
    require_structural_name(sink_partner, summary, "sink_partner")
    require(not is_manifesto_relabeling(sink_partner, summary),
            "sink_partner is not the Manifesto relabeling")

    return_self = Machine((0, 1, 2), ("a",), {0: 0, 1: 0, 2: 0},
                          {"a": {0: 0, 1: 2, 2: 0}})
    require(is_ghost_fold(return_self, summary), "return_self must be a ghost fold")
    require(ghost_shape(return_self, summary) == "return_self", "Named return_self")
    require_structural_name(return_self, summary, "return_self")

    return_partner = Machine((0, 1, 2), ("a",), {0: 0, 1: 0, 2: 0},
                             {"a": {0: 1, 1: 2, 2: 0}})
    require(is_ghost_fold(return_partner, summary), "return_partner must be a ghost fold")
    require(ghost_shape(return_partner, summary) == "return_partner", "Named return_partner")
    require_structural_name(return_partner, summary, "return_partner")

    # Lift hostiles. Built from the 2×2 failure modes, not from a census.
    idle = Machine((0, 1, 2, 3), ("a",), {0: 0, 1: 0, 2: 0, 3: 0},
                   {"a": {0: 0, 1: 2, 2: 2, 3: 3}})
    idle_c = {0: 0, 1: 0, 2: 1, 3: 2}
    require(is_ghost_fold(idle, idle_c), "Idle extra singleton is still a ghost fold")
    require(ghost_shape(idle, idle_c) == "unclassified",
            "The n=3 2x2 classifier does not name n=4")
    require(lifted_ghost_type(idle, idle_c) == "sink_self",
            "Lift recovers sink_self on a unique size-2 block at n=4")
    require_structural_name(idle, idle_c, "sink_self")
    require(profile_kind(idle_c, idle.states) == "unique_pair",
            "Idle extra singleton is unique-pair")

    split_m = Machine((0, 1, 2, 3), ("a",), {0: 0, 1: 0, 2: 0, 3: 0},
                      {"a": {0: 2, 1: 3, 2: 2, 3: 3}})
    split_c = {0: 0, 1: 0, 2: 1, 3: 2}
    require(is_ghost_fold(split_m, split_c), "split must be a ghost fold")
    require(lifted_ghost_type(split_m, split_c) == "split", "Named split")
    require_structural_name(split_m, split_c, "split")
    require(is_typed_residue(split_m, split_c, "split"), "Typed split")
    require(unique_pair_witness_set(split_m, split_c) == frozenset(["split"]),
            "split is the singleton witness set {split}")
    require(all(not is_typed_residue(split_m, split_c, name)
                for name in RESIDUE_TYPES if name != "split"),
            "split is not escape/crowd/multi/mixed")

    escape_m = Machine((0, 1, 2, 3), ("a",), {0: 0, 1: 0, 2: 0, 3: 0},
                       {"a": {0: 0, 1: 2, 2: 3, 3: 3}})
    escape_c = {0: 0, 1: 0, 2: 1, 3: 2}
    require(is_ghost_fold(escape_m, escape_c), "escape must be a ghost fold")
    require(lifted_ghost_type(escape_m, escape_c) == "escape", "Named escape")
    require_structural_name(escape_m, escape_c, "escape")
    require(is_typed_residue(escape_m, escape_c, "escape"), "Typed escape")
    require(unique_pair_witness_set(escape_m, escape_c) == frozenset(["escape"]),
            "escape is the singleton witness set {escape}")

    crowd_m = Machine((0, 1, 2, 3), ("a",), {0: 0, 1: 0, 2: 0, 3: 0},
                      {"a": {0: 0, 1: 0, 2: 3, 3: 3}})
    crowd_c = {0: 0, 1: 0, 2: 0, 3: 1}
    require(is_ghost_fold(crowd_m, crowd_c), "crowd must be a ghost fold")
    require(lifted_ghost_type(crowd_m, crowd_c) == "crowd", "Named crowd")
    require_structural_name(crowd_m, crowd_c, "crowd")
    require(is_typed_residue(crowd_m, crowd_c, "crowd"), "Typed crowd")
    require(ghost_fold_detail(crowd_m, crowd_c, "crowd") == "crowd_one_jumper",
            "Definitional crowd has one jumper out of the triple")
    require(unique_pair_witness_set(crowd_m, crowd_c) is None,
            "crowd is not a unique-pair type")
    require(not is_typed_residue(crowd_m, crowd_c, "split"),
            "A merged triple is crowd, not split")

    crowd_two = Machine((0, 1, 2, 3), ("a",), {0: 0, 1: 0, 2: 0, 3: 0},
                        {"a": {0: 3, 1: 3, 2: 2, 3: 3}})
    require(is_ghost_fold(crowd_two, crowd_c), "two-jumper crowd must be a ghost fold")
    require_structural_name(crowd_two, crowd_c, "crowd")
    require(is_typed_residue(crowd_two, crowd_c, "crowd"), "Typed two-jumper crowd")
    require(ghost_fold_detail(crowd_two, crowd_c, "crowd") == "crowd_two_jumpers",
            "Two jumpers out of the triple is still crowd")
    require(not is_typed_residue(crowd_two, crowd_c, "split"),
            "Two jumpers from a triple are not unique-pair split")

    multi_m = Machine((0, 1, 2, 3), ("a",), {0: 0, 1: 0, 2: 0, 3: 0},
                      {"a": {0: 0, 1: 2, 2: 2, 3: 3}})
    multi_c = {0: 0, 1: 0, 2: 1, 3: 1}
    require(is_ghost_fold(multi_m, multi_c), "multi must be a ghost fold")
    require(lifted_ghost_type(multi_m, multi_c) == "multi", "Named multi")
    require_structural_name(multi_m, multi_c, "multi")
    require(is_typed_residue(multi_m, multi_c, "multi"), "Typed multi")
    require(ghost_fold_detail(multi_m, multi_c, "multi") == "multi_one",
            "Definitional multi has one witnessing pair")
    require(not is_typed_residue(multi_m, multi_c, "mixed"),
            "Two merged pairs are multi, not mixed")

    multi_both = Machine((0, 1, 2, 3), ("a",), {0: 0, 1: 0, 2: 0, 3: 0},
                         {"a": {0: 0, 1: 2, 2: 2, 3: 0}})
    require(is_ghost_fold(multi_both, multi_c), "both-pair multi must be a ghost fold")
    require_structural_name(multi_both, multi_c, "multi")
    require(is_typed_residue(multi_both, multi_c, "multi"), "Typed both-pair multi")
    require(ghost_fold_detail(multi_both, multi_c, "multi") == "multi_both",
            "Two witnessing pairs is still multi")
    require(not is_typed_residue(multi_both, multi_c, "mixed"),
            "Two witnessing pairs are not unique-pair mixed")

    mixed_m = Machine((0, 1, 2), ("a", "b"), {0: 0, 1: 0, 2: 0},
                      {"a": {0: 0, 1: 2, 2: 2}, "b": {0: 0, 1: 2, 2: 0}})
    mixed_c = {0: 0, 1: 0, 2: 1}
    require(is_ghost_fold(mixed_m, mixed_c), "mixed must be a ghost fold")
    require(lifted_ghost_type(mixed_m, mixed_c) == "mixed", "Named mixed")
    require_structural_name(mixed_m, mixed_c, "mixed")
    require(is_typed_residue(mixed_m, mixed_c, "mixed"), "Typed mixed")
    require(ghost_shape(mixed_m, mixed_c) == "unclassified",
            "The one-action 2x2 classifier does not name two actions")
    require(len(unique_pair_witness_set(mixed_m, mixed_c)) > 1,
            "mixed is a unique-pair witness set of size at least two")
    require(not is_typed_residue(mixed_m, mixed_c, "split"),
            "mixed is not split")

    partial_m = Machine((0, 1, 2), ("a",), {0: 0, 1: 0, 2: 0},
                        {"a": {0: 0, 1: 2}})
    partial_c = {0: 0, 1: 0, 2: 1}
    require(not is_ghost_fold(partial_m, partial_c),
            "partial_land is FIVE-visible FAIL vs OK, not a ghost")
    require(classify_ghost_fold(partial_m, partial_c) == "partial_land",
            "Named partial_land")
    require_structural_name(partial_m, partial_c, "partial_land")
    require(shortest_witness(partial_m, 0, 1)["status"] == "ONE",
            "partial_land has a distinguishing word")
    require(not is_typed_residue(partial_m, partial_c, "escape"),
            "FAIL-vs-OK landing is not a ghost residue")

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
    require(ghost_shape(binary, indiscrete) == "unclassified",
            "Non-ghost enabledness failure is unclassified")

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
    return {
        "named_hostiles": 21,
        "clauses": list(CLAUSES),
        "shapes": list(GHOST_SHAPES),
        "residue_types": list(RESIDUE_TYPES),
        "lift_types": list(LIFT_TYPES),
    }


def slice_machines(n, actions):
    """Same constructor as checks/futures.py: binary observations, all partial maps."""
    states = tuple(range(n))
    machines = []
    for observations in it.product((0, 1), repeat=n):
        observation = dict(zip(states, observations))
        for flat in it.product(tuple(range(-1, n)), repeat=n * len(actions)):
            tables = {a: {x: flat[j * n + x] for x in states if flat[j * n + x] != -1}
                      for j, a in enumerate(actions)}
            machines.append(Machine(states, actions, observation, tables))
    return machines


def family_machines():
    machines = []
    for n, actions in ((0, ("a",)), (1, ("a", "b")), (2, ("a", "b")), (3, ("a",))):
        machines.extend(slice_machines(n, actions))
    return machines


def compact_ghost(machine, summary, lift_type):
    tables = {
        action: [machine.transitions[action][state] if state in machine.transitions[action] else -1
                 for state in machine.states]
        for action in machine.actions
    }
    return {
        "states": list(machine.states),
        "actions": list(machine.actions),
        "observation": [machine.observation[state] for state in machine.states],
        "next": tables,
        "summary": [summary[state] for state in machine.states],
        "profile": list(block_profile(summary, machine.states)),
        "lift_type": lift_type,
        "detail": ghost_fold_detail(machine, summary, lift_type),
    }


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
        "shape": ghost_shape(machine, summary),
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
                require((record["shape"] == "sink_self") == record["manifesto_relabeling"],
                        "sink_self must match the Manifesto relabeling predicate")
                require(lifted_ghost_type(machine, summary) == record["shape"],
                        "Lift type must recover the 2x2 on the 845 slice")
                require(structural_lift_type(machine, summary) == record["shape"],
                        "Typed flags must recover the 2x2 on the 845 slice")
    require(ghosts_one_block == 0, "Single-block ghost fold appeared")
    require(ghosts_two_states == 0, "n<=2 ghost fold appeared")
    require(all(row["constant_observation"] for row in ghosts),
            "Ghost fold with non-constant observation in this family")
    relabelings = sum(1 for row in ghosts if row["manifesto_relabeling"])
    null_holds = len(ghosts) == relabelings
    shape_counts = {name: 0 for name in GHOST_SHAPES}
    shape_counts["unclassified"] = 0
    for row in ghosts:
        shape = row["shape"]
        require(shape in shape_counts, "Unknown shape label")
        shape_counts[shape] += 1
    leftover = {name: shape_counts[name] for name in GHOST_SHAPES if name != "sink_self"}
    leftover_occupied = sum(1 for count in leftover.values() if count)
    shape_null_holds = leftover_occupied == 1
    require(shape_counts == LISTING, "Census disagrees with the written 2×2 listing")
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
        "shape_null": SHAPE_NULL,
        "shape_null_holds": shape_null_holds,
        "shape_listing": LISTING,
        "shape_counts": shape_counts,
        "leftover_occupied_types": leftover_occupied,
    }


def check_one_lift_slice(spec):
    n = spec["n"]
    actions = spec["actions"]
    expected = (2 ** n) * ((n + 1) ** (n * len(actions)))
    machines = slice_machines(n, actions)
    require(len(machines) == expected, spec["name"] + " family size changed")
    partitions = tuple(set_partitions(tuple(range(n))))
    counts = {name: 0 for name in LIFT_TYPES}
    details = {}
    profiles = {}
    examples = {}
    cases = 0
    folds = 0
    ghosts = 0
    ghosts_one_block = 0
    unique_pair_ghosts = 0
    unique_pair_two_by_two = 0
    unique_pair_residues = 0
    match_ok = True
    total = len(machines)
    for index, machine in enumerate(machines):
        if index % 2000 == 0:
            print(f"{spec['name']} {index}/{total} ghosts={ghosts}", file=sys.stderr)
        for summary in partitions:
            cases += 1
            fiber = obstruction_fiber(machine, summary)
            if fiber["status"] == "NONE":
                folds += 1
                continue
            if fiber["by_clause"]["observation"] or fiber["by_clause"]["enabledness"]:
                continue
            if not is_future_sufficient(machine, summary):
                continue
            require(fiber["by_clause"]["successor"] >= 1,
                    "Ghost fold with no successor failure")
            ghosts += 1
            if len(set(summary.values())) == 1:
                ghosts_one_block += 1
            name = classify_ghost_fold(machine, summary)
            typed = structural_lift_type(machine, summary)
            flags = structural_lift_flags(machine, summary)
            if name != typed or sum(1 for bit in flags.values() if bit) != 1:
                match_ok = False
            require(name == typed, spec["name"] + ": classifier disagrees with typed definition")
            require(sum(1 for bit in flags.values() if bit) == 1,
                    spec["name"] + ": typed flags were not exclusive")
            require(name in counts, "Unknown lift label")
            counts[name] += 1
            detail = ghost_fold_detail(machine, summary, name)
            details[detail] = details.get(detail, 0) + 1
            profile = "+".join(str(size) for size in block_profile(summary, machine.states))
            profiles[profile] = profiles.get(profile, 0) + 1
            kind = profile_kind(summary, machine.states)
            if kind == "crowd":
                require(name == "crowd", spec["name"] + ": crowd profile was not named crowd")
            elif kind == "multi":
                require(name == "multi", spec["name"] + ": multi profile was not named multi")
            elif kind == "unique_pair":
                witnesses = unique_pair_witness_set(machine, summary)
                require(witnesses is not None and len(witnesses) >= 1,
                        spec["name"] + ": unique-pair ghost had an empty witness set")
                if name in GHOST_SHAPES:
                    require(witnesses == frozenset([name]),
                            spec["name"] + ": 2x2 name disagrees with witness set")
                elif name == "split":
                    require(witnesses == frozenset(["split"]),
                            spec["name"] + ": split name disagrees with witness set")
                elif name == "escape":
                    require(witnesses == frozenset(["escape"]),
                            spec["name"] + ": escape name disagrees with witness set")
                elif name == "mixed":
                    require(len(witnesses) > 1,
                            spec["name"] + ": mixed name has a singleton witness set")
            unique_pair = kind == "unique_pair"
            if unique_pair:
                unique_pair_ghosts += 1
                if name in GHOST_SHAPES:
                    unique_pair_two_by_two += 1
                elif name in ("split", "escape", "mixed"):
                    unique_pair_residues += 1
            if name not in examples:
                examples[name] = compact_ghost(machine, summary, name)
    print(f"{spec['name']} {total}/{total} ghosts={ghosts}", file=sys.stderr)
    require(ghosts_one_block == 0, spec["name"] + ": one-block ghost fold appeared")
    two_by_two = sum(counts[name] for name in GHOST_SHAPES)
    if spec["n"] == 4:
        require(details.get("crowd_one_jumper", 0) + details.get("crowd_two_jumpers", 0)
                == counts["crowd"],
                "n=4 crowd ghosts must have jumper count 1 or 2")
        require(details.get("multi_one", 0) + details.get("multi_both", 0) == counts["multi"],
                "n=4 multi ghosts must have one or both pairs witnessing")
        require(details.get("crowd_other", 0) == 0 and details.get("multi_other", 0) == 0,
                "n=4 crowd/multi corollary leftover appeared")
    return {
        "name": spec["name"],
        "n": n,
        "actions": list(actions),
        "machines": len(machines),
        "machine_partition_cases": cases,
        "operational_folds": folds,
        "ghost_folds": ghosts,
        "lift_counts": counts,
        "detail_counts": details,
        "profile_counts": profiles,
        "two_by_two_ghosts": two_by_two,
        "residue_ghosts": ghosts - two_by_two,
        "unclassified": counts["unclassified"],
        "unique_pair_ghosts": unique_pair_ghosts,
        "unique_pair_two_by_two": unique_pair_two_by_two,
        "unique_pair_residues": unique_pair_residues,
        "lift_null_holds": two_by_two == ghosts,
        "slice_null_holds": unique_pair_ghosts == unique_pair_two_by_two,
        "exhaustion_null_holds": counts["unclassified"] == 0,
        "match_null_holds": match_ok and counts["unclassified"] == 0,
        "examples": examples,
    }


def check_lift_census():
    slices = [check_one_lift_slice(spec) for spec in LIFT_SLICES]
    totals = {name: 0 for name in LIFT_TYPES}
    ghosts = 0
    unique_pair_ghosts = 0
    unique_pair_two_by_two = 0
    unique_pair_residues = 0
    match_ok = True
    for row in slices:
        ghosts += row["ghost_folds"]
        unique_pair_ghosts += row["unique_pair_ghosts"]
        unique_pair_two_by_two += row["unique_pair_two_by_two"]
        unique_pair_residues += row["unique_pair_residues"]
        match_ok = match_ok and row["match_null_holds"]
        for name, count in row["lift_counts"].items():
            totals[name] += count
    two_by_two = sum(totals[name] for name in GHOST_SHAPES)
    residue_from_names = sum(totals[name] for name in RESIDUE_TYPES)
    unique_pair_from_names = totals["split"] + totals["escape"] + totals["mixed"]
    require(slices[0]["lift_counts"] == FOUR_STATE_READOUT,
            "Four-state lift census disagrees with the locked readout")
    require(slices[1]["lift_counts"] == TWO_ACTION_READOUT,
            "Two-action lift census disagrees with the locked readout")
    require(slices[0]["profile_counts"] == {"1+1+2": 3888, "1+3": 1152, "2+2": 1152},
            "Four-state ghost profiles changed")
    require(slices[1]["profile_counts"] == {"1+2": 3168},
            "Two-action ghost profiles changed")
    require(unique_pair_residues == UNIQUE_PAIR_RESIDUE_READOUT,
            "Unique-pair residue hostile count changed")
    require(unique_pair_from_names == UNIQUE_PAIR_RESIDUE_READOUT,
            "split+escape+mixed is not the unique-pair residue fiber")
    require(unique_pair_ghosts - unique_pair_two_by_two == UNIQUE_PAIR_RESIDUE_READOUT,
            "Unique-pair ghosts minus 2x2 is not the residue hostile")
    require(residue_from_names == ghosts - two_by_two,
            "Residue occupancy is not the five typed fibers")
    require(match_ok and totals["unclassified"] == 0,
            "Typed definitions failed to match the classifier")
    return {
        "lift_null": LIFT_NULL,
        "lift_null_holds": two_by_two == ghosts,
        "slice_null": SLICE_NULL,
        "slice_null_holds": unique_pair_ghosts == unique_pair_two_by_two,
        "exhaustion_null": LIFT_EXHAUSTION_NULL,
        "exhaustion_null_holds": totals["unclassified"] == 0,
        "match_null": MATCH_NULL,
        "match_null_holds": match_ok and totals["unclassified"] == 0,
        "ghost_folds": ghosts,
        "two_by_two_ghosts": two_by_two,
        "residue_ghosts": ghosts - two_by_two,
        "unclassified": totals["unclassified"],
        "unique_pair_ghosts": unique_pair_ghosts,
        "unique_pair_two_by_two": unique_pair_two_by_two,
        "unique_pair_residues": unique_pair_residues,
        "lift_counts": totals,
        "slices": slices,
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
    parser.add_argument("--lift-output", type=Path, default=HERE / "LIFT_CENSUS.json")
    args = parser.parse_args()
    named = check_named_hostiles()
    census = check_census(NULL)
    lift = check_lift_census()
    result = {
        "schema": "rprm-operational-obstruction/v3",
        "status": "PASS",
        "null_declared_before_census": NULL,
        "shape_null_declared_before_shape_census": SHAPE_NULL,
        "lift_null_declared_before_census": LIFT_NULL,
        "slice_null_declared_before_census": SLICE_NULL,
        "lift_exhaustion_null_declared_before_census": LIFT_EXHAUSTION_NULL,
        "match_null_declared_before_census": MATCH_NULL,
        "named": named,
        "census": census,
        "lift_census": lift,
        "source_hashes": source_hashes(),
        "coverage": (
            "Named hostiles plus every partition of every machine in the "
            "checks/futures.py 845-machine family, plus the four-state "
            "one-action family and the three-state two-action family with "
            "the same constructor. Not a theorem about arbitrary infinite "
            "carriers, nondeterministic operations, or kernels."
        ),
    }
    payload = json.dumps(result, indent=2) + "\n"
    args.output.write_text(payload, encoding="utf-8")
    args.lift_output.write_text(json.dumps(lift, indent=2) + "\n", encoding="utf-8")
    summary = {
        "status": "PASS",
        "ghost_folds_845": census["ghost_folds"],
        "shape_counts_845": census["shape_counts"],
        "lift_null_holds": lift["lift_null_holds"],
        "slice_null_holds": lift["slice_null_holds"],
        "exhaustion_null_holds": lift["exhaustion_null_holds"],
        "match_null_holds": lift["match_null_holds"],
        "lift_ghost_folds": lift["ghost_folds"],
        "lift_counts": lift["lift_counts"],
        "unique_pair_residues": lift["unique_pair_residues"],
        "slices": [
            {
                "name": row["name"],
                "machines": row["machines"],
                "ghost_folds": row["ghost_folds"],
                "lift_counts": row["lift_counts"],
                "profile_counts": row["profile_counts"],
                "lift_null_holds": row["lift_null_holds"],
                "slice_null_holds": row["slice_null_holds"],
                "exhaustion_null_holds": row["exhaustion_null_holds"],
                "match_null_holds": row["match_null_holds"],
                "unique_pair_residues": row["unique_pair_residues"],
            }
            for row in lift["slices"]
        ],
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
