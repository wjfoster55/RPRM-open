"""Obstruction oracle as one Tile; a tiny three-cell Board.

A Tile is the oracle on a declared (machine, summary) pair. A Board here is
three named hostiles with withheld versus revealed ports. This is not an
eight-Tile Board and not an Atlas. Generality is OPEN.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from rprm.futures import Machine, future_quotient, shortest_witness
from obstruction import (
    GHOST_SHAPES,
    block_profile,
    distinguishing_witness_fiber,
    ghost_fiber,
    ghost_shape,
    is_ghost_fold,
    is_operational_fold,
    is_typed_residue,
    least_stable_repair,
    lifted_ghost_type,
    merged_pairs,
    obstruction_fiber,
    profile_kind,
    repaired_kernel_matches,
    set_partitions,
    unique_pair_witness_set,
)


TILE_PORTS = (
    "machine",
    "summary",
    "obstruction",
    "ghost",
    "lift_type",
    "profile_kind",
    "five_future",
    "o05_witness",
    "o09_matches",
    "o09_classes",
)

# Locked withheld-summary occupancy. Finite-test readout, not a premise.
MANIFESTO_WITHHELD = {"status": "ONE", "ghost_folds": 1, "lift_counts": {"sink_self": 1}}
SINK_SELF_WITHHELD = {"status": "ONE", "ghost_folds": 1, "lift_counts": {"sink_self": 1}}
SPLIT_WITHHELD = {
    "status": "MANY",
    "ghost_folds": 6,
    "lift_counts": {"crowd": 2, "split": 1, "multi": 1, "sink_self": 2},
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def manifesto_pqr_machine():
    return Machine(("p", "q", "r"), ("a",), {"p": 0, "q": 0, "r": 0},
                   {"a": {"p": "p", "q": "r", "r": "r"}})


def manifesto_pqr_summary():
    return {"p": 0, "q": 0, "r": 1}


def sink_self_2x2_machine():
    return Machine((0, 1, 2), ("a",), {0: 0, 1: 0, 2: 0}, {"a": {0: 0, 1: 2, 2: 2}})


def sink_self_2x2_summary():
    return {0: 0, 1: 0, 2: 1}


def unique_pair_split_machine():
    return Machine((0, 1, 2, 3), ("a",), {0: 0, 1: 0, 2: 0, 3: 0},
                   {"a": {0: 2, 1: 3, 2: 2, 3: 3}})


def unique_pair_split_summary():
    return {0: 0, 1: 0, 2: 1, 3: 2}


def compact_machine(machine):
    return {
        "states": list(machine.states),
        "actions": list(machine.actions),
        "observation": [machine.observation[state] for state in machine.states],
        "next": {
            action: [machine.transitions[action][state] if state in machine.transitions[action] else -1
                     for state in machine.states]
            for action in machine.actions
        },
    }


def compact_witness_row(row):
    return {
        "left": row["left"],
        "right": row["right"],
        "clause": row["clause"],
        "words": [list(word) for word in row["words"]],
        "word_status": row["word_status"],
        "length": row["length"],
        "least": list(row["least"]),
        "five_future": row["five_future"],
        "five_word": None if row["five_word"] is None else list(row["five_word"]),
        "five_word_is_o05_witness": row["five_word_is_o05_witness"],
    }


def compact_witness_fiber(fiber):
    return {
        "status": fiber["status"],
        "pairs": [compact_witness_row(row) for row in fiber["pairs"]],
        "by_clause": dict(fiber["by_clause"]),
        "ghost_pairs": fiber["ghost_pairs"],
        "five_visible_pairs": fiber["five_visible_pairs"],
        "five_word_differs": fiber["five_word_differs"],
    }


def closed_tile(machine, summary):
    """Fill every Tile readout port from the obstruction oracle.

    Carrier: one declared (machine, summary). Vacancy: the classified
    obstruction, ghost fiber, lift type, and O05 witness fiber. The
    commuting receipt is that these functions of (machine, summary)
    reproduce the closed artifact.
    """
    fiber = obstruction_fiber(machine, summary)
    ghosts = ghost_fiber(machine, summary)
    witness = distinguishing_witness_fiber(machine, summary)
    five = []
    for left, right in merged_pairs(machine, summary):
        word = shortest_witness(machine, left, right)
        five.append({"left": left, "right": right, "status": word["status"]})
    repaired = least_stable_repair(machine, summary)
    return {
        "summary": [summary[state] for state in machine.states],
        "profile": list(block_profile(summary, machine.states)),
        "obstruction": {
            "status": fiber["status"],
            "pairs": [dict(row) for row in fiber["pairs"]],
            "by_clause": dict(fiber["by_clause"]),
        },
        "ghost": {
            "status": ghosts["status"],
            "pairs": [dict(row) for row in ghosts["pairs"]],
        },
        "lift_type": lifted_ghost_type(machine, summary),
        "n3_shape": ghost_shape(machine, summary),
        "profile_kind": profile_kind(summary, machine.states),
        "five_future": five,
        "o05_witness": compact_witness_fiber(witness),
        "o09_matches": repaired_kernel_matches(machine, summary),
        "o09_classes": len(repaired["classes"]),
        "future_classes": len(future_quotient(machine)["classes"]),
    }


def withhold_summary_fiber(machine):
    """Complete ghost-fold fiber of set-partitions of the machine.

    Revealed: the machine. Withheld: the summary. NONE/ONE/MANY is used only
    after that enumeration.
    """
    tiles = []
    for summary in set_partitions(machine.states):
        if is_ghost_fold(machine, summary):
            tiles.append(closed_tile(machine, summary))
    lift_counts = {}
    for tile in tiles:
        name = tile["lift_type"]
        lift_counts[name] = lift_counts.get(name, 0) + 1
    if not tiles:
        status = "NONE"
    elif len(tiles) == 1:
        status = "ONE"
    else:
        status = "MANY"
    return {
        "status": status,
        "ghost_folds": len(tiles),
        "lift_counts": lift_counts,
        "tiles": tiles,
        "partition_count": sum(1 for _ in set_partitions(machine.states)),
    }


def _compact_withheld(fiber):
    return {
        "status": fiber["status"],
        "ghost_folds": fiber["ghost_folds"],
        "lift_counts": fiber["lift_counts"],
        "partition_count": fiber["partition_count"],
    }


def _require_ghost_tile(tile, lift_type, pair, n_states):
    require(tile["obstruction"]["status"] == "ONE", "Named hostile obstruction should be ONE pair")
    require(tile["obstruction"]["pairs"] == [
        {"left": pair[0], "right": pair[1], "clause": "successor"}
    ], "Named hostile pair is successor")
    require(tile["ghost"]["status"] == "ONE", "Named hostile is a ghost fold")
    require(tile["lift_type"] == lift_type, "Named hostile lift type")
    require(tile["profile_kind"] == "unique_pair", "Named hostile is unique-pair")
    require(tile["five_future"] == [{"left": pair[0], "right": pair[1], "status": "NONE"}],
            "Named hostile FIVE.future is NONE")
    require(tile["o05_witness"]["status"] == "ONE", "Named hostile O05 witness fiber is ONE")
    require(tile["o05_witness"]["pairs"] == [{
        "left": pair[0],
        "right": pair[1],
        "clause": "successor",
        "words": [["a"]],
        "word_status": "ONE",
        "length": 1,
        "least": ["a"],
        "five_future": "NONE",
        "five_word": None,
        "five_word_is_o05_witness": False,
    }], "Named hostile O05 witness is the successor word (a,), not FIVE.future NONE")
    require(tile["o05_witness"]["ghost_pairs"] == 1, "Named hostile ghost pair still has an O05 word")
    require(tile["o05_witness"]["five_word_differs"] == 1,
            "FIVE.future NONE must not be counted as an O05 witness")
    require(tile["o09_matches"] is False, "O09 must split the ghost pair")
    require(tile["o09_classes"] == n_states, "Least stable repair is discrete")
    require(tile["future_classes"] == 1, "Canonical future quotient is indiscrete")


def check_board():
    """Finite checks for the three-cell Board. Not an Atlas theorem."""
    manifesto_m = manifesto_pqr_machine()
    manifesto_c = manifesto_pqr_summary()
    sink_m = sink_self_2x2_machine()
    sink_c = sink_self_2x2_summary()
    split_m = unique_pair_split_machine()
    split_c = unique_pair_split_summary()

    manifesto_tile = closed_tile(manifesto_m, manifesto_c)
    sink_tile = closed_tile(sink_m, sink_c)
    split_tile = closed_tile(split_m, split_c)

    _require_ghost_tile(manifesto_tile, "sink_self", ("p", "q"), 3)
    require(manifesto_tile["n3_shape"] == "sink_self", "Manifesto {p,q,r} is the 2x2 sink_self")
    require(not is_typed_residue(manifesto_m, manifesto_c, "split"),
            "Manifesto 2x2 is not unique-pair split")

    _require_ghost_tile(sink_tile, "sink_self", (0, 1), 3)
    require(sink_tile["n3_shape"] == "sink_self", "Numeric 2x2 is sink_self")
    require(sink_tile["lift_type"] == manifesto_tile["lift_type"],
            "Equal type on Manifesto {p,q,r} and 0,1,2 sink_self")
    require(manifesto_tile["obstruction"]["pairs"] != sink_tile["obstruction"]["pairs"],
            "Equal type is not equal occurrence: pair names differ")

    _require_ghost_tile(split_tile, "split", (0, 1), 4)
    require(split_tile["n3_shape"] == "unclassified",
            "The n=3 2x2 classifier does not name n=4 split")
    require(is_typed_residue(split_m, split_c, "split"), "Declared unique-pair split")
    require(unique_pair_witness_set(split_m, split_c) == frozenset(["split"]),
            "Declared split has witness set {split}")
    require(split_tile["profile"] == [1, 1, 2], "Declared split is unique-pair")

    manifesto_withheld = withhold_summary_fiber(manifesto_m)
    sink_withheld = withhold_summary_fiber(sink_m)
    split_withheld = withhold_summary_fiber(split_m)

    require(_compact_withheld(manifesto_withheld)["status"] == MANIFESTO_WITHHELD["status"]
            and manifesto_withheld["ghost_folds"] == MANIFESTO_WITHHELD["ghost_folds"]
            and manifesto_withheld["lift_counts"] == MANIFESTO_WITHHELD["lift_counts"],
            "Manifesto withheld-summary fiber changed")
    require(manifesto_withheld["partition_count"] == 5, "Bell(3) is 5")
    require(manifesto_withheld["tiles"] == [manifesto_tile],
            "Filling the Manifesto vacancy must recover the declared Tile")

    require(_compact_withheld(sink_withheld)["status"] == SINK_SELF_WITHHELD["status"]
            and sink_withheld["ghost_folds"] == SINK_SELF_WITHHELD["ghost_folds"]
            and sink_withheld["lift_counts"] == SINK_SELF_WITHHELD["lift_counts"],
            "2x2 sink_self withheld-summary fiber changed")
    require(sink_withheld["tiles"] == [sink_tile],
            "Filling the 2x2 vacancy must recover the declared Tile")

    require(split_withheld["status"] == SPLIT_WITHHELD["status"]
            and split_withheld["ghost_folds"] == SPLIT_WITHHELD["ghost_folds"]
            and split_withheld["lift_counts"] == SPLIT_WITHHELD["lift_counts"],
            "Split-machine withheld-summary fiber changed")
    require(split_withheld["partition_count"] == 15, "Bell(4) is 15")
    require(split_tile in split_withheld["tiles"],
            "Declared split Tile must lie in the withheld-summary fiber")
    split_named = [tile for tile in split_withheld["tiles"] if tile["lift_type"] == "split"]
    require(len(split_named) == 1 and split_named[0] == split_tile,
            "On the split machine, type split still selects ONE summary")
    require(sum(1 for tile in split_withheld["tiles"] if tile["lift_type"] == "sink_self") == 2,
            "The split machine also hosts 2x2 sink_self summaries")
    require(any(tile["lift_type"] in GHOST_SHAPES for tile in split_withheld["tiles"])
            and any(tile["lift_type"] == "split" for tile in split_withheld["tiles"]),
            "Unique-pair ghost does not force a 2x2 name, even on one machine")

    # Commuting receipt: every withheld-summary completion is a closed Tile
    # of the oracle, and operational partitions are not ghosts.
    for machine in (manifesto_m, sink_m, split_m):
        rebuilt = []
        operational = 0
        for summary in set_partitions(machine.states):
            if is_operational_fold(machine, summary):
                operational += 1
                require(not is_ghost_fold(machine, summary),
                        "Operational fold cannot be a ghost Tile")
            if is_ghost_fold(machine, summary):
                rebuilt.append(closed_tile(machine, summary))
        fiber = withhold_summary_fiber(machine)
        require(rebuilt == fiber["tiles"], "Withheld-summary fiber disagrees with closed Tiles")
        require(operational + fiber["ghost_folds"] <= fiber["partition_count"],
                "Ghost and operational counts escaped the partition carrier")

    cells = (
        {"name": "manifesto_pqr", "tile": manifesto_tile},
        {"name": "unique_pair_split", "tile": split_tile},
        {"name": "sink_self_2x2", "tile": sink_tile},
    )
    by_type = {}
    for cell in cells:
        by_type.setdefault(cell["tile"]["lift_type"], []).append(cell["name"])
    require(sorted(by_type["sink_self"]) == ["manifesto_pqr", "sink_self_2x2"],
            "Type sink_self occupies two cells")
    require(by_type["split"] == ["unique_pair_split"],
            "Type split occupies one cell")
    type_fiber = {
        name: {
            "status": "ONE" if len(hits) == 1 else "MANY",
            "count": len(hits),
            "cells": hits,
        }
        for name, hits in by_type.items()
    }
    require(type_fiber["sink_self"]["status"] == "MANY",
            "Revealing lift type sink_self does not select a unique cell")
    require(type_fiber["split"]["status"] == "ONE",
            "Revealing lift type split selects the unique-pair split cell")

    return {
        "schema": "rprm-operational-obstruction-board/v1",
        "status": "PASS",
        "evidence_grade": "finite_test",
        "generality": "OPEN",
        "eight_tile_board": False,
        "atlas": False,
        "tile": {
            "capability": "O05 obstruction oracle on a declared machine and summary",
            "ports": list(TILE_PORTS),
            "vacancy": "classified obstruction, ghost fiber, lift type, and O05 witness fiber",
            "receipt": "closed_tile(machine, summary) agrees with the oracle functions",
        },
        "board": {
            "cells": 3,
            "names": [cell["name"] for cell in cells],
            "withheld_question": (
                "Whether a ghost-fold diagnosis is determined by a proper "
                "subset of the Tile ports. Not a preinstalled eighth Tile."
            ),
            "cells_detail": [
                {
                    "name": "manifesto_pqr",
                    "machine": compact_machine(manifesto_m),
                    "declared": manifesto_tile,
                    "withhold_summary": _compact_withheld(manifesto_withheld),
                },
                {
                    "name": "unique_pair_split",
                    "machine": compact_machine(split_m),
                    "declared": split_tile,
                    "withhold_summary": {
                        **_compact_withheld(split_withheld),
                        "tiles": split_withheld["tiles"],
                    },
                },
                {
                    "name": "sink_self_2x2",
                    "machine": compact_machine(sink_m),
                    "declared": sink_tile,
                    "withhold_summary": _compact_withheld(sink_withheld),
                },
            ],
            "type_fiber_among_cells": type_fiber,
        },
        "coverage": (
            "Three named hostiles as Tile instances, plus every set-partition "
            "of each host machine as the withheld-summary aperture. Not a "
            "theorem about eight-Tile Boards, Atlases, or arbitrary machines."
        ),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(check_board(), indent=2))
