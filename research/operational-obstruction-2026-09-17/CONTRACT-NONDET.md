# Contract NONDET-LTS-01 — finite labeled transition obstruction

17 September 2026. New required type. The PARTIAL O05 oracle on
`rprm.futures.Machine` does not stretch. FIVE.future is not this contract.

This supersedes the §14 total-table probe: that probe had no enabledness
port and could not host deadlock versus disabled.

## 1. Task record

1. **Carrier, types, equality, admitted context.** Finite labeled
   transition systems. States are exact atoms; actions are distinct
   nonempty names; observation is a total table. Each action is a
   *partial* function from states to frozensets of states.
   - Absent source: **disabled**.
   - Present empty set: **deadlock** (enabled, no successors).
   - Present nonempty set: **live branching**.
   Live edges are partial functions into nonempty subsets. Deadlock is an
   explicit empty value in the domain, not a missing port. Bool/float
   atoms are admission errors. A proposed summary `C` is a total map from
   states to exact atoms. Equality is the declared state equality.
2. **Supplied ports, missing ports, requested readout.** Supplied: the
   nondet machine and `C`. Missing: the complete obstruction of `C` against
   this contract. Readout: each unordered merged pair labelled by its
   earliest clause `observation`, `enabledness`, or `successor_blocks`, or
   `pass`.
3. **Operation kind, direction, enabledness.** `NONDET`. Diagnostic.
   Enabledness is membership in an action's domain. Deadlock is a
   successor-set value, not enabledness.
4. **Receiver.** Observation, enabledness, and successor *sets of
   C-blocks*. Not FIVE.future. Not PARTIAL one-step state labels. Not
   kernel pushforward mass.
5. **Inverse / complete fiber.** The obstruction fiber is the complete
   set of merged pairs whose earliest clause is not `pass`. NONE, ONE, or
   MANY only after that enumeration. The bounded n=2,3 one-action census
   is closed. The 845 PARTIAL lift remains OPEN.
6. **Coverage, hostile, evidence grade.** Coverage: written trichotomy on
   this carrier; named hostiles in `verify.py`; complete census of the
   declared 2- and 3-state one-action family (successor sets of size
   0, 1, or 2, plus disabled). Hostile: deadlock versus disabled on a
   two-state merged pair. Grade: written trichotomy; finite tests; finite
   census. The 845-family PARTIAL census does **not** lift; that claim
   stays OPEN. Unbounded carriers and `KERNEL` remain OPEN.

## 2. Closed claim

**Definition.** For states `x ≠ y` with `C(x) = C(y)`, the earliest
NONDET-LTS clause is:

1. `observation` if `O(x) ≠ O(y)`;
2. else `enabledness` if some action is defined at exactly one of `x, y`;
3. else `successor_blocks` if some action defined at both has
   `C[N_a(x)] ≠ C[N_a(y)]`;
4. else `pass`.

`C[S]` is the set of `C`-labels of members of `S`. In particular
`C[∅] = ∅`, so deadlock versus a nonempty landing is
`successor_blocks` when both sources are enabled.

**Proposition (trichotomy).** These four labels partition the merged-pair
carrier. Proof: the clauses are checked in order; each is a decidable
equality or domain membership on a finite table; exactly one label is
returned.

**Proposition (deadlock is not disabled).** If `a` is defined at `x` with
`N_a(x) = ∅` and undefined at `y`, the clause is `enabledness`. If `a`
is defined at both, `N_a(x) = ∅`, and `N_a(y) ≠ ∅`, the clause is
`successor_blocks` once observation agrees. Grade: written from the
definition.

**Proposition (PARTIAL oracle does not admit this carrier).**
`obstruction_fiber` requires `Machine`. `Machine` targets are single
states. `shortest_witness` requires `Machine`. Grade: written.

## 3. Nulls, frozen before the hostiles

> Deadlock (empty successor set in the domain) and disabled (absent from
> the domain) receive the same earliest clause on a two-state merged pair
> with equal observation.

> The 845-family PARTIAL ghost-fold occupancy lifts unchanged to this
> NONDET-LTS contract.

The first null is decided by the named hostiles. The second is **not
run** this cut: no 845 NONDET census is claimed or performed.

## 4. What this does not claim

Not the 845 PARTIAL lift. Not FIVE.future. Not Lean. Not that empty-set
deadlock is a nonempty subset. Not that the PARTIAL 2×2 or residue
types classify nondet machines. Not n≥4 or two actions.

Oracle: [nondet.py](nondet.py). Tests: `verify.py` `check_nondet`,
`check_nondet_census`. Receipt: [NONDET_CENSUS.json](NONDET_CENSUS.json).
