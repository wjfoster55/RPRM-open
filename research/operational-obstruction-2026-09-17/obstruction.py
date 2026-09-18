"""Complete O05 obstruction fibers for finite deterministic partial machines.

`rprm.core.deterministic_quotient` returns the first failing pair.
`rprm.futures.shortest_witness` cannot see a successor-update failure that
leaves every tagged future observation equal. This module returns the
complete classified pair fiber, then NONE/ONE/MANY.
"""
from __future__ import annotations

from rprm.core import atom, require, total_table
from rprm.futures import Machine, shortest_witness, stable_refinement

CLAUSES = ("observation", "enabledness", "successor")
GHOST_SHAPES = ("sink_self", "sink_partner", "return_self", "return_partner")
# Occupied residue types of a ghost fold. Occupancy is a census readout, not
# a premise. Each name has an independent typed flag in structural_lift_flags.
RESIDUE_TYPES = ("split", "escape", "crowd", "multi", "mixed")
# A priori lift vocabulary. Occupancy is a census readout, not a premise.
LIFT_TYPES = GHOST_SHAPES + RESIDUE_TYPES + (
    "partial_land",
    "wide_landing",
    "unclassified",
)
PROFILE_KINDS = ("crowd", "multi", "unique_pair", "other")


def require_machine(machine):
    require(type(machine) is Machine, "Machine required")


def require_summary(machine, summary):
    require_machine(machine)
    total_table(machine.states, summary, "Summary")
    for value in summary.values():
        atom(value)


def pair_clause(machine, left, right, summary):
    """Earliest O05 failure for one unordered C-pair, or 'pass'.

    Order is load-bearing: present observation, then enabledness, then
    retained successor. A pair may fail later clauses as well; those are
    not reported once an earlier clause already fails.
    """
    require_summary(machine, summary)
    atom(left)
    atom(right)
    require(left in machine.states and right in machine.states, "Unadmitted pair")
    if machine.observation[left] != machine.observation[right]:
        return "observation"
    for action in machine.actions:
        enabled_left = left in machine.transitions[action]
        enabled_right = right in machine.transitions[action]
        if enabled_left != enabled_right:
            return "enabledness"
        if enabled_left:
            next_left = machine.transitions[action][left]
            next_right = machine.transitions[action][right]
            if summary[next_left] != summary[next_right]:
                return "successor"
    return "pass"


def merged_pairs(machine, summary):
    require_summary(machine, summary)
    pairs = []
    states = machine.states
    for i, left in enumerate(states):
        for right in states[i + 1:]:
            if summary[left] == summary[right]:
                pairs.append((left, right))
    return tuple(pairs)


def obstruction_fiber(machine, summary):
    """Complete O05 obstruction of a proposed summary.

    Carrier of the fiber: unordered merged pairs. Readout: earliest clause.
    NONE means the admitted obstruction is empty, i.e. an operational fold.
    """
    failures = []
    passed = 0
    for left, right in merged_pairs(machine, summary):
        clause = pair_clause(machine, left, right, summary)
        if clause == "pass":
            passed += 1
        else:
            failures.append({"left": left, "right": right, "clause": clause})
    failures = tuple(failures)
    if not failures:
        status = "NONE"
    elif len(failures) == 1:
        status = "ONE"
    else:
        status = "MANY"
    by_clause = {clause: 0 for clause in CLAUSES}
    for row in failures:
        by_clause[row["clause"]] += 1
    return {
        "status": status,
        "pairs": failures,
        "merged": passed + len(failures),
        "passed": passed,
        "by_clause": by_clause,
    }


def is_operational_fold(machine, summary):
    return obstruction_fiber(machine, summary)["status"] == "NONE"


def same_kernel(left_summary, right_summary, states):
    total_table(states, left_summary, "Left summary")
    total_table(states, right_summary, "Right summary")
    for i, a in enumerate(states):
        for b in states[i + 1:]:
            if (left_summary[a] == left_summary[b]) != (right_summary[a] == right_summary[b]):
                return False
    return True


def least_stable_repair(machine, summary):
    """O09: coarsest operational fold refining the proposed summary."""
    require_summary(machine, summary)
    return stable_refinement(machine, summary)


def repaired_kernel_matches(machine, summary):
    repaired = least_stable_repair(machine, summary)
    return same_kernel(summary, {state: repaired["encoding"][state] for state in machine.states},
                       machine.states)


def ghost_fiber(machine, summary):
    """Merged pairs that are future-equivalent but fail one-step O05.

    FIVE.future returns NONE exactly when every tagged word observation
    agrees, including failure. Enabledness mismatches produce a FAIL vs OK
    word, so they never appear here. A one-step `pass` pair need not be
    future-equivalent unless every merged pair passes.
    """
    require_summary(machine, summary)
    ghosts = []
    for left, right in merged_pairs(machine, summary):
        clause = pair_clause(machine, left, right, summary)
        word = shortest_witness(machine, left, right)
        require(word["status"] in ("ONE", "NONE"), "Pair witness must be complete")
        if word["status"] == "NONE" and clause != "pass":
            require(clause == "successor", "Future-equivalent obstruction must be successor")
            ghosts.append({"left": left, "right": right, "clause": clause})
    ghosts = tuple(ghosts)
    if not ghosts:
        status = "NONE"
    elif len(ghosts) == 1:
        status = "ONE"
    else:
        status = "MANY"
    return {"status": status, "pairs": ghosts}


def is_future_sufficient(machine, summary):
    """Every merged pair has FIVE.future NONE."""
    require_summary(machine, summary)
    return all(shortest_witness(machine, left, right)["status"] == "NONE"
               for left, right in merged_pairs(machine, summary))


def is_ghost_fold(machine, summary):
    """Future-sufficient strict compression that still fails O05."""
    return is_future_sufficient(machine, summary) and not is_operational_fold(machine, summary)


def _blocks(summary, states):
    blocks = {}
    for state in states:
        blocks.setdefault(summary[state], []).append(state)
    return tuple(tuple(block) for block in blocks.values())


def ghost_shape(machine, summary):
    """2×2 block-dynamics type of a ghost fold, or unclassified.

    On a one-action total (2,1) ghost fold the merged pair has exactly one
    stayer (image in the merged class) and one jumper (image the singleton).
    The stayer is a self-loop or maps to its partner. The singleton is a
    sink or returns into the merged class. Those two binary choices name
    four ordinary types. Anything else, including a non-ghost, is
    unclassified. No prestige vocabulary is used.
    """
    if not is_ghost_fold(machine, summary):
        return "unclassified"
    if len(machine.states) != 3 or len(machine.actions) != 1:
        return "unclassified"
    table = machine.transitions[machine.actions[0]]
    if set(table) != set(machine.states):
        return "unclassified"
    parts = _blocks(summary, machine.states)
    sizes = sorted(len(part) for part in parts)
    if sizes != [1, 2]:
        return "unclassified"
    merged = next(part for part in parts if len(part) == 2)
    singleton = next(part for part in parts if len(part) == 1)[0]
    stayers = [state for state in merged if table[state] in merged]
    jumpers = [state for state in merged if table[state] == singleton]
    if len(stayers) != 1 or len(jumpers) != 1:
        return "unclassified"
    stayer = stayers[0]
    if table[stayer] == stayer:
        stay = "self"
    elif table[stayer] in merged:
        stay = "partner"
    else:
        return "unclassified"
    if table[singleton] == singleton:
        land = "sink"
    elif table[singleton] in merged:
        land = "return"
    else:
        return "unclassified"
    return land + "_" + stay


def block_profile(summary, states):
    return tuple(sorted(len(part) for part in _blocks(summary, states)))


def profile_kind(summary, states):
    """Partition of block-size profiles. Independent of occupancy.

    crowd: some block has size ≥3.
    multi: no such block, and at least two blocks of size 2.
    unique_pair: exactly one block of size 2, and no larger block.
    other: no merged pair of size 2 or more that those three names cover.
    """
    sizes = block_profile(summary, states)
    if any(size >= 3 for size in sizes):
        return "crowd"
    twos = sum(1 for size in sizes if size == 2)
    if twos >= 2:
        return "multi"
    if twos == 1:
        return "unique_pair"
    return "other"


def unique_pair_block(summary, states):
    if profile_kind(summary, states) != "unique_pair":
        return None
    return next(part for part in _blocks(summary, states) if len(part) == 2)


def _local_action_shape(machine, merged, summary, action):
    """Stay-jump readout of one action on one size-2 block, or a residue tag.

    `agree` means the action is enabled at both points and preserves C-blocks.
    `not_successor` means it cannot be an O05 successor witness.
    """
    table = machine.transitions[action]
    left, right = merged
    enabled_left = left in table
    enabled_right = right in table
    if enabled_left != enabled_right or not enabled_left:
        return "not_successor"
    if summary[table[left]] == summary[table[right]]:
        return "agree"
    stayers = [state for state in merged if table[state] in merged]
    jumpers = [state for state in merged if table[state] not in merged]
    if len(jumpers) == 2:
        return "split"
    if len(stayers) != 1 or len(jumpers) != 1:
        return "unclassified"
    stayer = stayers[0]
    jumper = jumpers[0]
    if table[stayer] == stayer:
        stay = "self"
    elif table[stayer] in merged:
        stay = "partner"
    else:
        return "unclassified"
    land = table[jumper]
    land_size = sum(1 for state in machine.states if summary[state] == summary[land])
    if land_size != 1:
        return "wide_landing"
    if land not in table:
        return "partial_land"
    if table[land] == land:
        kind = "sink"
    elif table[land] in merged:
        kind = "return"
    else:
        return "escape"
    return kind + "_" + stay


def unique_pair_witness_set(machine, summary):
    """Set of local witnessing names on the unique size-2 block, or None.

    None means the profile is not unique-pair. The empty set means unique-pair
    with no successor-witnessing action.
    """
    require_summary(machine, summary)
    merged = unique_pair_block(summary, machine.states)
    if merged is None:
        return None
    labels = []
    for action in machine.actions:
        tag = _local_action_shape(machine, merged, summary, action)
        if tag not in ("agree", "not_successor"):
            labels.append(tag)
    return frozenset(labels)


def classify_ghost_fold(machine, summary):
    """Lift type of a known ghost fold. Not a name for a non-ghost.

    Profile is first: a block of size ≥3 is `crowd`; two or more size-2
    blocks is `multi`. On a unique size-2 block the original 2×2 is tried
    on every successor-witnessing action. Split, escape, partial landing,
    and wide landing are the one-pair residues. Distinct witnessing names
    across actions are `mixed`.
    """
    require_summary(machine, summary)
    parts = _blocks(summary, machine.states)
    sizes = sorted(len(part) for part in parts)
    if any(size >= 3 for size in sizes):
        return "crowd"
    twos = sum(1 for size in sizes if size == 2)
    if twos >= 2:
        return "multi"
    if twos != 1:
        return "unclassified"
    merged = next(part for part in parts if len(part) == 2)
    labels = []
    for action in machine.actions:
        tag = _local_action_shape(machine, merged, summary, action)
        if tag in ("agree", "not_successor"):
            continue
        labels.append(tag)
    if not labels:
        return "unclassified"
    uniq = set(labels)
    if len(uniq) > 1:
        return "mixed"
    name = next(iter(uniq))
    if name in LIFT_TYPES:
        return name
    return "unclassified"


def structural_lift_flags(machine, summary):
    """Independent typed flags for the lift vocabulary. Not occupancy buckets.

    Exactly one flag must hold on a classified ghost fold. Crowd and multi
    are profile types. Split, escape, mixed, the 2×2, partial_land, and
    wide_landing are unique-pair witness-set types. Mixed is a set of size
    at least two; it is not a split or escape flag.
    """
    require_summary(machine, summary)
    flags = {name: False for name in LIFT_TYPES if name != "unclassified"}
    kind = profile_kind(summary, machine.states)
    flags["crowd"] = kind == "crowd"
    flags["multi"] = kind == "multi"
    witnesses = unique_pair_witness_set(machine, summary)
    if kind == "unique_pair" and witnesses is not None:
        flags["mixed"] = len(witnesses) > 1
        if len(witnesses) == 1:
            only = next(iter(witnesses))
            if only in flags:
                flags[only] = True
    return flags


def structural_lift_type(machine, summary):
    """Name from the typed flags, or unclassified if none or several fire."""
    hits = [name for name, bit in structural_lift_flags(machine, summary).items() if bit]
    if len(hits) == 1:
        return hits[0]
    return "unclassified"


def is_typed_residue(machine, summary, name):
    """True iff this is a ghost fold of the named residue type."""
    require(name in RESIDUE_TYPES, "Residue type required")
    if not is_ghost_fold(machine, summary):
        return False
    return structural_lift_type(machine, summary) == name


def lifted_ghost_type(machine, summary):
    """2×2 name or lift residue of a ghost fold; unclassified if not a ghost."""
    if not is_ghost_fold(machine, summary):
        return "unclassified"
    return classify_ghost_fold(machine, summary)


def ghost_fold_detail(machine, summary, lift_type):
    """Occupancy subtype inside crowd/multi. Not a replacement invariant."""
    parts = _blocks(summary, machine.states)
    if lift_type == "crowd":
        triple = next(part for part in parts if len(part) == 3)
        tags = []
        for action in machine.actions:
            table = machine.transitions[action]
            if any(state not in table for state in triple):
                tags.append("crowd_partial")
                continue
            jumpers = sum(1 for state in triple if table[state] not in triple)
            if jumpers == 1:
                tags.append("crowd_one_jumper")
            elif jumpers == 2:
                tags.append("crowd_two_jumpers")
            else:
                tags.append("crowd_other")
        if len(set(tags)) == 1:
            return tags[0]
        return "crowd_mixed"
    if lift_type == "multi":
        pairs = [part for part in parts if len(part) == 2]
        witnessed = 0
        for part in pairs:
            if any(_local_action_shape(machine, part, summary, action)
                   not in ("agree", "not_successor") for action in machine.actions):
                witnessed += 1
        if witnessed >= 2:
            return "multi_both"
        if witnessed == 1:
            return "multi_one"
        return "multi_other"
    return lift_type


def min_repair_alphabet(states, summary, question):
    """O08R: smallest tag alphabet repairing Q relative to C."""
    total_table(states, summary, "Summary")
    total_table(states, question, "Question")
    if not states:
        return 0
    blocks = {}
    for state in states:
        atom(summary[state])
        atom(question[state])
        blocks.setdefault(summary[state], set()).add(question[state])
    return max(len(values) for values in blocks.values())


def set_partitions(states):
    """All partitions of a finite tuple, each as a state-to-block-index map."""
    require(type(states) is tuple, "Carrier enumeration must be a tuple")
    n = len(states)
    if n == 0:
        yield {}
        return
    codes = [0] * n

    def walk(index, used):
        if index == n:
            yield {states[i]: codes[i] for i in range(n)}
            return
        for label in range(used):
            codes[index] = label
            yield from walk(index + 1, used)
        codes[index] = used
        yield from walk(index + 1, used + 1)

    yield from walk(0, 0)
