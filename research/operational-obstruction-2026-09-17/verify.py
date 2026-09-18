"""Finite checks for complete O05 obstruction fibers.

The census null is declared and recorded before any enumeration of the
845-machine family. The 2×2 lift nulls are declared before the four-state
and two-action families are enumerated. The O05 witness null is declared
before the three Board cells' witness fibers are read. Counts are not
premises; they are the readout.
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

from rprm.core import AdmissionError, deterministic_quotient, nondeterministic_quotient, stochastic_quotient
from rprm.futures import Machine, future_quotient, shortest_witness
from nondet import (
    CONTRACT as NONDET_CONTRACT,
    NONDET_CLAUSES,
    PAIR_KINDS,
    NondetMachine,
    as_partial_machine,
    encodes_as_partial,
    is_operational_fold_nondet,
    nondet_family,
    obstruction_class,
    obstruction_fiber_nondet,
    pair_clause_nondet,
    pair_kind_nondet,
)
from board import (
    check_board,
    compact_witness_fiber,
    manifesto_pqr_machine,
    manifesto_pqr_summary,
    sink_self_2x2_machine,
    sink_self_2x2_summary,
    unique_pair_split_machine,
    unique_pair_split_summary,
)
from obstruction import (
    CLAUSES,
    GHOST_SHAPES,
    LIFT_TYPES,
    RESIDUE_TYPES,
    block_profile,
    classify_ghost_fold,
    DELAY_REASONS,
    distinguishing_witness_fiber,
    delayed_pair_record,
    ghost_fiber,
    is_delayed_five_successor,
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
    pair_witness_words,
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
WITNESS_NULL = (
    "On Manifesto {p,q,r}, unique-pair split, and numeric 2x2 sink_self, "
    "FIVE.future is NONE on the declared merged pair, therefore the O05 "
    "distinguishing-witness fiber of each declared C is also NONE."
)
FIVE_COINCIDES_NULL = (
    "On the checks/futures.py 845-machine family, for every failing merged "
    "pair with FIVE.future ONE, the FIVE.future word equals the shortlex-least "
    "O05 clause-witness."
)
DELAY_NULL = (
    "The 24 FIVE.future/O05 disagreements on the checks/futures.py "
    "845-machine family are all successor-class ghost folds of one 2x2 type "
    "sink_self, sink_partner, return_self, or return_partner."
)
DELAY_MATCH_NULL = (
    "On the 845-machine family, every delayed FIVE successor pair has "
    "obstruction class successor, is not a ghost fold, has unique-pair "
    "local name partial_land, and has FIVE delay late_enabledness. "
    "Unclassified delay is NONE."
)
NONDET_NULL = (
    "The existing PARTIAL obstruction oracle already classifies finite "
    "nondeterministic machines: empty successor sets are enabledness, "
    "and FIVE.future decides every successor_blocks failure."
)
DEADLOCK_DISABLED_NULL = (
    "Deadlock (empty successor set in the domain) and disabled (absent from "
    "the domain) receive the same earliest clause on a two-state merged pair "
    "with equal observation."
)
NONDET_CENSUS_LIFT_NULL = (
    "The 845-family PARTIAL ghost-fold occupancy lifts unchanged to this "
    "NONDET-LTS contract."
)
# Frozen before the n=2,3 one-action census is enumerated. Not the 845 lift.
NONDET_COLLISION_NULL = (
    "On the declared 2- and 3-state one-action NONDET family with successor "
    "sets of size 0, 1, or 2 (plus disabled), deadlock/disabled collisions "
    "are unoccupied as an earliest clause."
)
NONDET_FIVE_AGREE_NULL = (
    "FIVE.future would agree with the NONDET obstruction disposition on "
    "every machine-partition pair in that family."
)
NONDET_FAMILY_SLICES = (
    {"name": "two_state_one_action", "n": 2, "machines": 100, "cases": 200},
    {"name": "three_state_one_action", "n": 3, "machines": 4096, "cases": 20480},
)
NONDET_FAMILY_MACHINES = 4196
NONDET_FAMILY_CASES = 20680
# Occupancy readout, locked after the first enumeration. Not a premise of the nulls.
NONDET_STATUS_READOUT = {"NONE": 6190, "ONE": 10830, "MANY": 3660}
NONDET_COLLISION_READOUT = 388
NONDET_FIVE_GHOSTS_READOUT = 72
NONDET_CLASS_READOUT = {
    "NONE": 6190,
    "ONE:observation": 6194,
    "ONE:enabledness": 1360,
    "ONE:successor_blocks": 3276,
    "MANY:observation": 1824,
    "MANY:enabledness": 264,
    "MANY:successor_blocks": 252,
    "MANY:observation+enabledness": 672,
    "MANY:observation+successor_blocks": 576,
    "MANY:enabledness+successor_blocks": 72,
}
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
# 845-family readout: FIVE.future ONE words that are not the O05 witness.
FIVE_DIFFERS_READOUT = 24
# Locked after the first delayed-pair classification. Not a premise of DELAY_NULL.
DELAY_LOCAL_READOUT = {"partial_land": 24}
DELAY_REASON_READOUT = {
    "late_enabledness": 24,
    "late_observation": 0,
    "late_other": 0,
}


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
    manifesto_w = distinguishing_witness_fiber(machine, summary)
    require(manifesto_w["status"] == "ONE" and manifesto_w["pairs"][0]["least"] == ("a",),
            "Manifesto O05 witness is the successor word (a,), not FIVE.future NONE")
    require(manifesto_w["pairs"][0]["five_future"] == "NONE",
            "Manifesto FIVE.future stays NONE")
    require(not manifesto_w["pairs"][0]["five_word_is_o05_witness"],
            "FIVE.future NONE must not be treated as the O05 witness")
    require(not is_delayed_five_successor(machine, 0, 1, summary),
            "Manifesto ghost is FIVE.future NONE, not a delayed FIVE pair")

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
    mixed_w = pair_witness_words(mixed_m, 0, 1, mixed_c)
    require(mixed_w["status"] == "MANY" and mixed_w["words"] == (("a",), ("b",)),
            "mixed successor pair has two one-letter O05 words")
    require(distinguishing_witness_fiber(mixed_m, mixed_c)["pairs"][0]["five_future"] == "NONE",
            "mixed is still a ghost: FIVE.future NONE with a nonempty O05 word set")

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
    partial_w = distinguishing_witness_fiber(partial_m, partial_c)
    require(partial_w["status"] == "ONE" and partial_w["pairs"][0]["least"] == ("a",),
            "partial_land O05 witness is the successor letter (a,)")
    require(partial_w["pairs"][0]["five_word"] == ("a", "a"),
            "partial_land FIVE.future is (a,a), a different receiver")
    require(not partial_w["pairs"][0]["five_word_is_o05_witness"],
            "Must not pretend FIVE.future (a,a) is the O05 successor witness")
    require(is_delayed_five_successor(partial_m, 0, 1, partial_c),
            "partial_land is the definitional delayed FIVE successor")
    partial_delay = delayed_pair_record(partial_m, 0, 1, partial_c)
    require(partial_delay["clause"] == "successor", "partial_land obstruction class is successor")
    require(partial_delay["ghost_fold"] is False and partial_delay["ghost_shape"] == "unclassified",
            "partial_land is not a 2x2 ghost fold")
    require(partial_delay["local_name"] == "partial_land", "Definitional local name is partial_land")
    require(partial_delay["delay"] == "late_enabledness",
            "Definitional delay is FAIL vs OK after the O05 letter")

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
    two_w = distinguishing_witness_fiber(two, collapsed)
    require(two_w["status"] == "MANY" and two_w["by_clause"]["observation"] == 2,
            "Two observation failures have two empty-word O05 witnesses")
    require(all(row["least"] == () and row["five_word"] == () for row in two_w["pairs"]),
            "Observation O05 witness is the empty word and coincides with FIVE.future")

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
    binary_w = distinguishing_witness_fiber(binary, indiscrete)
    require(binary_w["status"] == "ONE" and binary_w["pairs"][0]["least"] == ("a",),
            "Enabledness O05 witness is the mismatched one-letter word")
    require(binary_w["pairs"][0]["five_word"] == ("a",),
            "Enabledness FIVE.future word coincides with the O05 witness")

    one_block = Machine((0, 1, 2), ("a",), {0: 0, 1: 0, 2: 0}, {"a": {0: 1, 1: 2, 2: 0}})
    require(ghost_fiber(one_block, {0: 0, 1: 0, 2: 0})["status"] == "NONE",
            "A single block cannot ghost-fold: successor is automatic")
    require(is_operational_fold(one_block, {0: 0, 1: 0, 2: 0}),
            "Indiscrete constant-obs total map is operational")
    require(distinguishing_witness_fiber(one_block, {0: 0, 1: 0, 2: 0})["status"] == "NONE",
            "Operational fold has empty O05 witness fiber")

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
    five_w = distinguishing_witness_fiber(five, repaired_tags)
    require(five_w["status"] == "MANY" and five_w["by_clause"]["successor"] >= 1,
            "Five-state O05 witness fiber is the successor pairs, not the future word")
    pq = next(row for row in five_w["pairs"] if {row["left"], row["right"]} == {"p", "q"})
    require(pq["least"] == ("a",) and pq["five_word"] == ("a", "a"),
            "Five-state O05 witness is (a,), FIVE.future is (a,a)")
    require(not pq["five_word_is_o05_witness"],
            "Must not pretend the FIVE.future word (a,a) is the O05 successor witness")
    require(is_delayed_five_successor(five, "p", "q", repaired_tags),
            "Five-state pair is delayed FIVE, not a ghost")
    five_delay = delayed_pair_record(five, "p", "q", repaired_tags)
    require(five_delay["delay"] == "late_observation",
            "Five-state delay is OK(1) vs OK(0), not FAIL vs OK")
    require(five_delay["ghost_fold"] is False,
            "Five-state delayed pair is not a ghost fold")
    require(five_delay["local_name"] != "partial_land",
            "late_observation hostile is not the 845 partial_land type")

    # Empty carrier: O08R is 0; obstruction NONE.
    empty = Machine((), (), {}, {})
    require(min_repair_alphabet((), {}, {}) == 0, "Empty O08R")
    require(obstruction_fiber(empty, {})["status"] == "NONE", "Empty obstruction")
    require(distinguishing_witness_fiber(empty, {})["status"] == "NONE",
            "Empty O05 witness fiber")
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
        "witness_null": WITNESS_NULL,
        "delay_reasons": list(DELAY_REASONS),
    }


def check_witnesses():
    """Finite O05 witness checks. Nulls are recorded before the readout."""
    cells = (
        ("manifesto_pqr", manifesto_pqr_machine(), manifesto_pqr_summary(), "p", "q"),
        ("unique_pair_split", unique_pair_split_machine(), unique_pair_split_summary(), 0, 1),
        ("sink_self_2x2", sink_self_2x2_machine(), sink_self_2x2_summary(), 0, 1),
    )
    declared = {}
    for name, machine, summary, left, right in cells:
        fiber = distinguishing_witness_fiber(machine, summary)
        five = shortest_witness(machine, left, right)
        require(five["status"] == "NONE", name + ": FIVE.future must stay NONE")
        require(fiber["status"] != "NONE", name + ": O05 witness fiber is not NONE")
        require(fiber["status"] == "ONE", name + ": declared cell should be ONE pair")
        row = fiber["pairs"][0]
        require(row["clause"] == "successor" and row["least"] == ("a",),
                name + ": O05 witness is the successor word (a,)")
        require(row["five_future"] == "NONE" and row["five_word"] is None,
                name + ": FIVE.future word is NONE")
        require(not row["five_word_is_o05_witness"],
                name + ": must not pretend FIVE.future NONE is the O05 witness")
        declared[name] = compact_witness_fiber(fiber)
    witness_null_holds = all(row["status"] == "NONE" for row in declared.values())
    require(not witness_null_holds,
            "Witness null was supposed to be the false FIVE.future identification")
    return {
        "witness_null": WITNESS_NULL,
        "witness_null_holds": witness_null_holds,
        "five_coincides_null": FIVE_COINCIDES_NULL,
        "cells": declared,
        "coverage": (
            "Declared Board cells plus the named hostiles in check_named_hostiles. "
            "Not a theorem about arbitrary machines."
        ),
    }


def expect_admission_error(call, message):
    try:
        call()
    except AdmissionError:
        return
    raise RuntimeError(message)


def check_nondet():
    """NONDET-LTS-01 oracle. Nulls are recorded before the hostiles are read."""
    expect_admission_error(
        lambda: Machine((0, 1), ("a",), {0: 0, 1: 0}, {"a": {0: frozenset({1}), 1: frozenset({1})}}),
        "Successor sets must not be PARTIAL Machine targets")
    expect_admission_error(
        lambda: obstruction_fiber(
            NondetMachine((0, 1), ("a",), {0: 0, 1: 0},
                          {"a": {0: frozenset({0}), 1: frozenset({1})}}),
            {0: 0, 1: 0}),
        "PARTIAL oracle must reject NondetMachine: OPEN_NEW_CARRIER")

    manifesto = NondetMachine(
        (0, 1, 2), ("a",), {0: 0, 1: 0, 2: 0},
        {"a": {0: frozenset({0}), 1: frozenset({2}), 2: frozenset({2})}})
    summary = {0: 0, 1: 0, 2: 1}
    fiber = obstruction_fiber_nondet(manifesto, summary)
    require(fiber["status"] == "ONE" and fiber["pairs"][0]["clause"] == "successor_blocks",
            "Manifesto-as-nondet is ONE successor_blocks, not NONE")
    require(fiber["contract"] == NONDET_CONTRACT and fiber["five_future"] == "OPEN_NEW_CARRIER",
            "FIVE.future does not cover NONDET-LTS-01")
    expect_admission_error(
        lambda: shortest_witness(manifesto, 0, 1),
        "FIVE.future shortest_witness is not defined on NondetMachine")
    partial = as_partial_machine(manifesto)
    require(obstruction_fiber(partial, summary)["pairs"][0]["clause"] == "successor",
            "Singleton encoding recovers the PARTIAL successor clause")
    require(pair_clause_nondet(manifesto, 0, 1, summary) == "successor_blocks",
            "Manifesto pair is successor_blocks, not enabledness")

    deadlock = NondetMachine(
        (0, 1), ("a",), {0: 0, 1: 0},
        {"a": {0: frozenset(), 1: frozenset({1})}})
    dead_c = {0: 0, 1: 0}
    dead = obstruction_fiber_nondet(deadlock, dead_c)
    require(dead["status"] == "ONE" and dead["pairs"][0]["clause"] == "successor_blocks",
            "Deadlock versus a singleton is successor_blocks, not enabledness")
    expect_admission_error(
        lambda: as_partial_machine(deadlock),
        "Empty successor set is not a PARTIAL domain hole")
    both_dead = NondetMachine(
        (0, 1), ("a",), {0: 0, 1: 0},
        {"a": {0: frozenset(), 1: frozenset()}})
    require(is_operational_fold_nondet(both_dead, dead_c),
            "Equal empty successor sets agree")

    disabled = NondetMachine(
        (0, 1), ("a",), {0: 0, 1: 0},
        {"a": {0: frozenset()}})
    disable_c = {0: 0, 1: 0}
    dead_vs_off = obstruction_fiber_nondet(disabled, disable_c)
    require(dead_vs_off["status"] == "ONE" and dead_vs_off["pairs"][0]["clause"] == "enabledness",
            "Deadlock versus disabled is enabledness, not successor_blocks")
    expect_admission_error(
        lambda: as_partial_machine(disabled),
        "Deadlock cannot be rewritten as a PARTIAL hole")
    off_vs_live = NondetMachine(
        (0, 1), ("a",), {0: 0, 1: 0},
        {"a": {1: frozenset({1})}})
    off_fiber = obstruction_fiber_nondet(off_vs_live, disable_c)
    require(off_fiber["status"] == "ONE" and off_fiber["pairs"][0]["clause"] == "enabledness",
            "Disabled versus a singleton is enabledness")
    partial_off = as_partial_machine(off_vs_live)
    require(pair_clause(partial_off, 0, 1, disable_c) == "enabledness",
            "Singleton live edges recover PARTIAL enabledness")
    both_off = NondetMachine(
        (0, 1), ("a",), {0: 0, 1: 0},
        {"a": {}})
    require(is_operational_fold_nondet(both_off, disable_c),
            "Equal disabled sources agree")

    order = NondetMachine(
        (0, 1), ("a", "b"), {0: 0, 1: 0},
        {"a": {0: frozenset()},
         "b": {0: frozenset({0}), 1: frozenset({1})}})
    require(pair_clause_nondet(order, 0, 1, disable_c) == "enabledness",
            "Enabledness precedes successor_blocks")

    branch = NondetMachine(
        (0, 1, 2), ("a",), {0: 0, 1: 0, 2: 0},
        {"a": {0: frozenset({0, 2}), 1: frozenset({2}), 2: frozenset({2})}})
    branch_c = {0: 0, 1: 0, 2: 1}
    require(obstruction_fiber_nondet(branch, branch_c)["status"] == "ONE",
            "Branching versus a singleton landing is successor_blocks")
    expect_admission_error(
        lambda: as_partial_machine(branch),
        "Branching sets are not PARTIAL maps")

    two = NondetMachine(
        (0, 1, 2, 3), ("a",), {0: 0, 1: 1, 2: 0, 3: 1},
        {"a": {0: frozenset({0}), 1: frozenset({1}), 2: frozenset({2}), 3: frozenset({3})}})
    collapsed = {0: 0, 1: 0, 2: 1, 3: 1}
    many = obstruction_fiber_nondet(two, collapsed)
    require(many["status"] == "MANY" and many["by_clause"]["observation"] == 2,
            "Two observation failures remain MANY")
    core = nondeterministic_quotient(
        two.states, collapsed, dict(two.observation),
        {state: two.transitions["a"][state] for state in two.states})
    require(core["status"] == "REJECT" and core["reason"] == "observation",
            "Core first-witness still rejects")

    empty = NondetMachine((), (), {}, {})
    require(obstruction_fiber_nondet(empty, {})["status"] == "NONE", "Empty NONDET obstruction")

    deadlock_clause = pair_clause_nondet(deadlock, 0, 1, dead_c)
    disabled_clause = pair_clause_nondet(disabled, 0, 1, disable_c)
    deadlock_disabled_null_holds = deadlock_clause == disabled_clause
    require(deadlock_clause == "successor_blocks" and disabled_clause == "enabledness",
            "Deadlock versus live and deadlock versus disabled must split")

    return {
        "contract": NONDET_CONTRACT,
        "nondet_null": NONDET_NULL,
        "nondet_null_holds": False,
        "deadlock_disabled_null": DEADLOCK_DISABLED_NULL,
        "deadlock_disabled_null_holds": deadlock_disabled_null_holds,
        "census_lift_null": NONDET_CENSUS_LIFT_NULL,
        "census_lift_null_holds": "OPEN",
        "kind": "NONDET",
        "clauses": list(NONDET_CLAUSES),
        "five_future": "OPEN_NEW_CARRIER",
        "named_hostiles": 12,
        "coverage": (
            "Named hostiles. The 845-family PARTIAL occupancy is not "
            "lifted. The bounded n=2,3 census is a separate fiber."
        ),
    }


def check_nondet_census():
    """Complete NONDET-LTS obstruction on the bounded n=2,3 family.

    Nulls are the constants above. This is not the 845 PARTIAL lift.
    """
    collision = NondetMachine(
        (0, 1), ("a",), {0: 0, 1: 0},
        {"a": {0: frozenset()}})
    collision_c = {0: 0, 1: 0}
    require(pair_clause_nondet(collision, 0, 1, collision_c) == "enabledness",
            "Named hostile: deadlock versus disabled is enabledness")
    require(pair_kind_nondet(collision, 0, 1, collision_c) == "deadlock_disabled",
            "Named hostile kind is deadlock_disabled")
    require(not encodes_as_partial(collision),
            "Deadlock/disabled collision is not a PARTIAL encoding")

    manifesto = NondetMachine(
        (0, 1, 2), ("a",), {0: 0, 1: 0, 2: 0},
        {"a": {0: frozenset({0}), 1: frozenset({2}), 2: frozenset({2})}})
    manifesto_c = {0: 0, 1: 0, 2: 1}
    require(encodes_as_partial(manifesto), "Manifesto-as-nondet encodes as PARTIAL")
    require(obstruction_fiber_nondet(manifesto, manifesto_c)["status"] == "ONE",
            "Manifesto-as-nondet is ONE successor_blocks")
    require(is_future_sufficient(as_partial_machine(manifesto), manifesto_c),
            "Manifesto remains FIVE-future-sufficient: FIVE would agree is false")

    status_counts = {"NONE": 0, "ONE": 0, "MANY": 0}
    class_counts = {}
    clause_pairs = {clause: 0 for clause in NONDET_CLAUSES}
    kind_pairs = {kind: 0 for kind in PAIR_KINDS}
    five_unadmitted = 0
    five_agree = 0
    five_disagree = 0
    five_ghosts = 0
    collision_pairs = 0
    slices = []
    seen_collision = False
    seen_manifesto = False
    total_machines = 0
    total_cases = 0

    for spec in NONDET_FAMILY_SLICES:
        machines = nondet_family(spec["n"])
        require(len(machines) == spec["machines"],
                "NONDET family size changed for " + spec["name"])
        require(len(machines) != 845, "This census must not be the 845 family")
        slice_status = {"NONE": 0, "ONE": 0, "MANY": 0}
        slice_classes = {}
        slice_kinds = {kind: 0 for kind in PAIR_KINDS}
        slice_collisions = 0
        slice_five_unadmitted = 0
        slice_five_disagree = 0
        slice_cases = 0
        for machine in machines:
            if (machine.states == collision.states
                    and dict(machine.observation) == dict(collision.observation)
                    and {action: dict(table) for action, table in machine.transitions.items()}
                    == {action: dict(table) for action, table in collision.transitions.items()}):
                seen_collision = True
            if (machine.states == manifesto.states
                    and dict(machine.observation) == dict(manifesto.observation)
                    and {action: dict(table) for action, table in machine.transitions.items()}
                    == {action: dict(table) for action, table in manifesto.transitions.items()}):
                seen_manifesto = True
            partial = as_partial_machine(machine) if encodes_as_partial(machine) else None
            for summary in set_partitions(machine.states):
                slice_cases += 1
                fiber = obstruction_fiber_nondet(machine, summary)
                status_counts[fiber["status"]] += 1
                slice_status[fiber["status"]] += 1
                name = obstruction_class(fiber)
                class_counts[name] = class_counts.get(name, 0) + 1
                slice_classes[name] = slice_classes.get(name, 0) + 1
                for row in fiber["pairs"]:
                    clause_pairs[row["clause"]] += 1
                    kind = pair_kind_nondet(machine, row["left"], row["right"], summary)
                    kind_pairs[kind] += 1
                    slice_kinds[kind] += 1
                    if kind == "deadlock_disabled":
                        collision_pairs += 1
                        slice_collisions += 1
                if partial is None:
                    five_unadmitted += 1
                    slice_five_unadmitted += 1
                else:
                    five_ok = is_future_sufficient(partial, summary)
                    nondet_ok = fiber["status"] == "NONE"
                    if five_ok == nondet_ok:
                        five_agree += 1
                    else:
                        five_disagree += 1
                        slice_five_disagree += 1
                        if five_ok and not nondet_ok:
                            five_ghosts += 1
        require(slice_cases == spec["cases"],
                "NONDET case count changed for " + spec["name"])
        slices.append({
            "name": spec["name"],
            "n": spec["n"],
            "machines": spec["machines"],
            "cases": slice_cases,
            "status_counts": slice_status,
            "class_counts": slice_classes,
            "kind_pairs": slice_kinds,
            "deadlock_disabled_pairs": slice_collisions,
            "five_unadmitted": slice_five_unadmitted,
            "five_disagree": slice_five_disagree,
        })
        total_machines += spec["machines"]
        total_cases += slice_cases

    require(seen_collision, "Named deadlock/disabled hostile left the family")
    require(seen_manifesto, "Named Manifesto-as-nondet hostile left the family")
    require(total_machines == NONDET_FAMILY_MACHINES, "NONDET family size changed")
    require(total_cases == NONDET_FAMILY_CASES, "NONDET case count changed")
    require(sum(status_counts.values()) == total_cases, "Status counts miss cases")
    require(sum(class_counts.values()) == total_cases, "Class counts miss cases")
    require(collision_pairs > 0, "Deadlock/disabled collisions vanished")
    require(five_unadmitted > 0, "Every machine encoded as PARTIAL")
    require(five_disagree > 0, "FIVE.future agreed on every PARTIAL encoding")
    require(status_counts == NONDET_STATUS_READOUT, "NONDET status occupancy changed")
    require(class_counts == NONDET_CLASS_READOUT, "NONDET class occupancy changed")
    require(collision_pairs == NONDET_COLLISION_READOUT,
            "Deadlock/disabled collision count changed")
    require(five_ghosts == NONDET_FIVE_GHOSTS_READOUT, "NONDET FIVE-ghost count changed")

    collision_null_holds = collision_pairs == 0
    five_agree_null_holds = five_unadmitted == 0 and five_disagree == 0
    require(not collision_null_holds, "Collision null should be occupied")
    require(not five_agree_null_holds, "FIVE-agree null should fail")

    return {
        "schema": "rprm-operational-obstruction-nondet/v1",
        "status": "PASS",
        "contract": NONDET_CONTRACT,
        "evidence_grade": "finite_test",
        "family": (
            "2- and 3-state one-action machines, binary observation, "
            "each source disabled or a successor set of size 0, 1, or 2"
        ),
        "collision_null": NONDET_COLLISION_NULL,
        "collision_null_holds": collision_null_holds,
        "five_agree_null": NONDET_FIVE_AGREE_NULL,
        "five_agree_null_holds": five_agree_null_holds,
        "census_lift_null": NONDET_CENSUS_LIFT_NULL,
        "census_lift_null_holds": "OPEN",
        "named_hostile": (
            "Two-state constant-observation deadlock versus disabled is "
            "ONE enabledness, kind deadlock_disabled. Manifesto-as-nondet "
            "is ONE successor_blocks and FIVE-future-sufficient."
        ),
        "machines": total_machines,
        "cases": total_cases,
        "status_counts": status_counts,
        "class_counts": class_counts,
        "clause_pairs": clause_pairs,
        "kind_pairs": kind_pairs,
        "deadlock_disabled_pairs": collision_pairs,
        "five_unadmitted": five_unadmitted,
        "five_agree": five_agree,
        "five_disagree": five_disagree,
        "five_ghosts": five_ghosts,
        "slices": slices,
        "coverage": (
            "Every partition of every machine in the declared n=2,3 "
            "one-action family. Not the 845-family PARTIAL lift. Not "
            "n>=4, not two actions, not KERNEL."
        ),
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
    five_one_equals_o05 = 0
    five_one_differs_from_o05 = 0
    o05_witnessed_pairs = 0
    delayed = []
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
                witness = pair_witness_words(machine, left, right, summary)
                if clause in ("observation", "enabledness"):
                    require(word["status"] == "ONE", "Present/enabledness failure is FIVE-visible")
                if fiber["status"] == "NONE":
                    require(word["status"] == "NONE", "Operational fold pairs are future-equivalent")
                    require(witness["status"] == "NONE", "Operational fold pairs have no O05 word")
                if clause != "pass":
                    o05_witnessed_pairs += 1
                    require(witness["status"] != "NONE" and witness["words"],
                            "Failing pair must have a nonempty O05 word set")
                    require(witness["clause"] == clause, "O05 word clause must match the pair clause")
                    if word["status"] == "ONE":
                        if word["word"] in witness["words"]:
                            five_one_equals_o05 += 1
                        else:
                            five_one_differs_from_o05 += 1
                            delayed.append(delayed_pair_record(machine, left, right, summary))
                    else:
                        require(clause == "successor", "FIVE.future NONE on a failing pair is successor")
                        require(witness["words"], "Ghost pair still has an O05 successor word")
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
    require(o05_witnessed_pairs == sum(clause_hits.values()),
            "Every failing pair must contribute exactly one O05 word set")
    require(five_one_differs_from_o05 == FIVE_DIFFERS_READOUT,
            "845 FIVE.future/O05 disagreement count changed")
    five_coincides_null_holds = five_one_differs_from_o05 == 0
    require(len(delayed) == FIVE_DIFFERS_READOUT, "Delayed pair fiber size changed")
    delay_counts = {name: 0 for name in DELAY_REASONS}
    local_counts = {}
    ghost_shape_on_delayed = {name: 0 for name in GHOST_SHAPES}
    ghost_shape_on_delayed["unclassified"] = 0
    delayed_ghost_folds = 0
    delayed_clauses = {clause: 0 for clause in CLAUSES}
    for row in delayed:
        require(row["clause"] == "successor", "Delayed pair escaped successor")
        require(row["ghost_pair"] is False, "Delayed pair cannot be a ghost pair")
        require(row["delay"] in delay_counts, "Unknown delay reason")
        delay_counts[row["delay"]] += 1
        local_counts[row["local_name"]] = local_counts.get(row["local_name"], 0) + 1
        ghost_shape_on_delayed[row["ghost_shape"]] = ghost_shape_on_delayed.get(row["ghost_shape"], 0) + 1
        delayed_clauses[row["clause"]] += 1
        if row["ghost_fold"]:
            delayed_ghost_folds += 1
    occupied_two_by_two = sum(1 for name in GHOST_SHAPES if ghost_shape_on_delayed[name])
    delay_null_holds = (
        delayed_ghost_folds == len(delayed)
        and occupied_two_by_two == 1
        and ghost_shape_on_delayed["unclassified"] == 0
    )
    delay_match_ok = (
        delayed_ghost_folds == 0
        and all(row["local_name"] == "partial_land" for row in delayed)
        and delay_counts["late_enabledness"] == len(delayed)
        and delay_counts["late_other"] == 0
    )
    require(not delay_null_holds, "Delay null should be the false 2x2-ghost identification")
    require(delay_match_ok, "Delayed pairs escaped the typed partial_land/late_enabledness fiber")
    require(local_counts == DELAY_LOCAL_READOUT, "Delayed local-name occupancy changed")
    require(delay_counts == DELAY_REASON_READOUT, "Delayed FIVE-reason occupancy changed")
    compact_delayed = []
    for row in delayed:
        compact_delayed.append({
            "states": list(row["states"]),
            "observation": list(row["observation"]),
            "next": {action: list(images) for action, images in row["next"].items()},
            "summary": list(row["summary"]),
            "left": row["left"],
            "right": row["right"],
            "clause": row["clause"],
            "ghost_fold": row["ghost_fold"],
            "ghost_shape": row["ghost_shape"],
            "profile_kind": row["profile_kind"],
            "local_name": row["local_name"],
            "structural_name": row["structural_name"],
            "delay": row["delay"],
            "o05_word": list(row["o05_word"]),
            "five_word": list(row["five_word"]),
            "n": row["n"],
            "actions": list(row["actions"]),
        })
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
        "five_coincides_null": FIVE_COINCIDES_NULL,
        "five_coincides_null_holds": five_coincides_null_holds,
        "o05_witnessed_pairs": o05_witnessed_pairs,
        "five_one_equals_o05": five_one_equals_o05,
        "five_one_differs_from_o05": five_one_differs_from_o05,
        "delay_null": DELAY_NULL,
        "delay_null_holds": delay_null_holds,
        "delay_match_null": DELAY_MATCH_NULL,
        "delay_match_null_holds": delay_match_ok,
        "delayed_pairs": compact_delayed,
        "delayed_count": len(delayed),
        "delayed_ghost_folds": delayed_ghost_folds,
        "delayed_clauses": delayed_clauses,
        "delay_counts": delay_counts,
        "delayed_local_counts": local_counts,
        "delayed_ghost_shapes": ghost_shape_on_delayed,
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
        "research/operational-obstruction-2026-09-17/board.py",
        "research/operational-obstruction-2026-09-17/nondet.py",
        "research/operational-obstruction-2026-09-17/CONTRACT-NONDET.md",
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
    parser.add_argument("--board-output", type=Path, default=HERE / "BOARD.json")
    parser.add_argument("--witness-output", type=Path, default=HERE / "WITNESS.json")
    parser.add_argument("--delayed-output", type=Path, default=HERE / "DELAYED.json")
    parser.add_argument("--nondet-output", type=Path, default=HERE / "NONDET_CENSUS.json")
    args = parser.parse_args()
    named = check_named_hostiles()
    board = check_board()
    witnesses = check_witnesses()
    nondet = check_nondet()
    nondet_census = check_nondet_census()
    census = check_census(NULL)
    lift = check_lift_census()
    result = {
        "schema": "rprm-operational-obstruction/v9",
        "status": "PASS",
        "null_declared_before_census": NULL,
        "shape_null_declared_before_shape_census": SHAPE_NULL,
        "lift_null_declared_before_census": LIFT_NULL,
        "slice_null_declared_before_census": SLICE_NULL,
        "lift_exhaustion_null_declared_before_census": LIFT_EXHAUSTION_NULL,
        "match_null_declared_before_census": MATCH_NULL,
        "witness_null_declared_before_looking": WITNESS_NULL,
        "five_coincides_null_declared_before_census": FIVE_COINCIDES_NULL,
        "delay_null_declared_before_census": DELAY_NULL,
        "delay_match_null_declared_before_census": DELAY_MATCH_NULL,
        "nondet_null_declared_before_looking": NONDET_NULL,
        "deadlock_disabled_null_declared_before_looking": DEADLOCK_DISABLED_NULL,
        "nondet_census_lift_null_declared_before_looking": NONDET_CENSUS_LIFT_NULL,
        "nondet_collision_null_declared_before_census": NONDET_COLLISION_NULL,
        "nondet_five_agree_null_declared_before_census": NONDET_FIVE_AGREE_NULL,
        "named": named,
        "board": {
            "schema": board["schema"],
            "status": board["status"],
            "evidence_grade": board["evidence_grade"],
            "generality": board["generality"],
            "eight_tile_board": board["eight_tile_board"],
            "atlas": board["atlas"],
            "cells": board["board"]["names"],
            "type_fiber_among_cells": board["board"]["type_fiber_among_cells"],
            "withhold_summary": {
                cell["name"]: {
                    "status": cell["withhold_summary"]["status"],
                    "ghost_folds": cell["withhold_summary"]["ghost_folds"],
                    "lift_counts": cell["withhold_summary"]["lift_counts"],
                }
                for cell in board["board"]["cells_detail"]
            },
        },
        "witness": {
            "witness_null": witnesses["witness_null"],
            "witness_null_holds": witnesses["witness_null_holds"],
            "five_coincides_null": witnesses["five_coincides_null"],
            "five_coincides_null_holds": census["five_coincides_null_holds"],
            "cells": witnesses["cells"],
            "o05_witnessed_pairs": census["o05_witnessed_pairs"],
            "five_one_equals_o05": census["five_one_equals_o05"],
            "five_one_differs_from_o05": census["five_one_differs_from_o05"],
            "delay_null_holds": census["delay_null_holds"],
            "delay_match_null_holds": census["delay_match_null_holds"],
            "delayed_local_counts": census["delayed_local_counts"],
            "delay_counts": census["delay_counts"],
        },
        "nondet": nondet,
        "nondet_census": {
            "schema": nondet_census["schema"],
            "status": nondet_census["status"],
            "machines": nondet_census["machines"],
            "cases": nondet_census["cases"],
            "collision_null_holds": nondet_census["collision_null_holds"],
            "five_agree_null_holds": nondet_census["five_agree_null_holds"],
            "census_lift_null_holds": nondet_census["census_lift_null_holds"],
            "status_counts": nondet_census["status_counts"],
            "class_counts": nondet_census["class_counts"],
            "kind_pairs": nondet_census["kind_pairs"],
            "deadlock_disabled_pairs": nondet_census["deadlock_disabled_pairs"],
            "five_unadmitted": nondet_census["five_unadmitted"],
            "five_disagree": nondet_census["five_disagree"],
            "five_ghosts": nondet_census["five_ghosts"],
        },
        "census": census,
        "lift_census": lift,
        "source_hashes": source_hashes(),
        "coverage": (
            "Named hostiles plus every partition of every machine in the "
            "checks/futures.py 845-machine family, plus the four-state "
            "one-action family and the three-state two-action family with "
            "the same constructor, plus the three-cell Board that uses the "
            "oracle as a Tile, plus the O05 distinguishing-witness fiber, "
            "plus the bounded n=2,3 one-action NONDET-LTS census. "
            "Not a theorem about arbitrary infinite carriers, "
            "the 845 PARTIAL occupancy lifting, kernels, eight-Tile Boards, "
            "or Atlases."
        ),
    }
    payload = json.dumps(result, indent=2) + "\n"
    args.output.write_text(payload, encoding="utf-8")
    args.lift_output.write_text(json.dumps(lift, indent=2) + "\n", encoding="utf-8")
    args.board_output.write_text(json.dumps(board, indent=2) + "\n", encoding="utf-8")
    args.witness_output.write_text(json.dumps({
        "schema": "rprm-operational-obstruction-witness/v1",
        "status": "PASS",
        "evidence_grade": "finite_test",
        **witnesses,
        "five_coincides_null_holds": census["five_coincides_null_holds"],
        "o05_witnessed_pairs": census["o05_witnessed_pairs"],
        "five_one_equals_o05": census["five_one_equals_o05"],
        "five_one_differs_from_o05": census["five_one_differs_from_o05"],
    }, indent=2) + "\n", encoding="utf-8")
    args.delayed_output.write_text(json.dumps({
        "schema": "rprm-operational-obstruction-delayed/v1",
        "status": "PASS",
        "evidence_grade": "finite_test",
        "delay_null": census["delay_null"],
        "delay_null_holds": census["delay_null_holds"],
        "delay_match_null": census["delay_match_null"],
        "delay_match_null_holds": census["delay_match_null_holds"],
        "delayed_count": census["delayed_count"],
        "delayed_ghost_folds": census["delayed_ghost_folds"],
        "delayed_clauses": census["delayed_clauses"],
        "delay_counts": census["delay_counts"],
        "delayed_local_counts": census["delayed_local_counts"],
        "delayed_ghost_shapes": census["delayed_ghost_shapes"],
        "pairs": census["delayed_pairs"],
        "coverage": (
            "Complete delayed FIVE successor fiber on the 845-machine family. "
            "Not a theorem about n>=4 or two-action machines."
        ),
    }, indent=2) + "\n", encoding="utf-8")
    args.nondet_output.write_text(json.dumps(nondet_census, indent=2) + "\n", encoding="utf-8")
    summary = {
        "status": "PASS",
        "ghost_folds_845": census["ghost_folds"],
        "witness_null_holds": witnesses["witness_null_holds"],
        "five_coincides_null_holds": census["five_coincides_null_holds"],
        "five_one_differs_from_o05": census["five_one_differs_from_o05"],
        "delay_null_holds": census["delay_null_holds"],
        "delay_match_null_holds": census["delay_match_null_holds"],
        "delayed_local_counts": census["delayed_local_counts"],
        "delay_counts": census["delay_counts"],
        "nondet_null_holds": nondet["nondet_null_holds"],
        "deadlock_disabled_null_holds": nondet["deadlock_disabled_null_holds"],
        "nondet_census_lift_null_holds": nondet["census_lift_null_holds"],
        "nondet_contract": nondet["contract"],
        "nondet_five_future": nondet["five_future"],
        "nondet_census_cases": nondet_census["cases"],
        "nondet_status_counts": nondet_census["status_counts"],
        "nondet_class_counts": nondet_census["class_counts"],
        "nondet_collision_null_holds": nondet_census["collision_null_holds"],
        "nondet_five_agree_null_holds": nondet_census["five_agree_null_holds"],
        "nondet_deadlock_disabled_pairs": nondet_census["deadlock_disabled_pairs"],
        "nondet_five_ghosts": nondet_census["five_ghosts"],
        "board_cells": board["board"]["names"],
        "board_generality": board["generality"],
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
