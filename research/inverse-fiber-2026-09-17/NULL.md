# Frozen nulls — inverse design with complete ambiguity families

Written **before** this packet's enumerator was run. Do not edit after
`CENSUS.json` exists except to record that a later task superseded it.

Independent-math Rank 7 from
`rprm-corpus-2026-09-17/03-independent-math-reading.md`: inverse design
with complete ambiguity families. This cut is the smallest typed
preimage census, not the Rank-7 novelty target (certified approximate
families, discriminating-view selection, or a grid larger than these
named maps). Adjacent written sources: AGENT_HANDBOOK §3 joint
completions; README `a+b=c` table; docs/core.md §5 joint correlation and
unfinished search. Not BSD. Not fluid. Not Hamming. Not O05. Not
observability-budget. Not Markov lumping.

## Carrier (frozen)

**Bits2.** Domain `X2 = {(0,0),(0,1),(1,0),(1,1)}` with ordered-pair
equality. `(0,1)` is not `(1,0)`. Bits are exact integers `0` and `1`,
not booleans-as-ints and not floats.

Named total forward maps `X2 → {0,1}`:

```text
AND(a,b)  = 1 iff a=1 and b=1
XOR(a,b)  = 1 iff a≠b
NAND(a,b) = 0 iff a=1 and b=1
CONST0(a,b) = 0
```

**Bits3.** Domain `X3 = {0,1}^3` with ordered-triple equality. Named
total readout `C:X3 → {0,1}^2`,

```text
C(x,y,z) = (x XOR y, x XOR z)
```

**Add3.** Carrier `{0,1,2}` with ordinary addition and no wrap. Relation
`R = {(a,b,c): a,b,c in {0,1,2} and a+b=c}`. Aperture supplies `c` and
requests the joint pair `(a,b)`.

A **preimage fiber** of a total map `f:X→Z` at `z` is
`{x in X: f(x)=z}`, listed in lexicographic order of tuples. Missing
ports stay joint: the fiber is a set of tuples, not a product of
marginals.

Dispositions, only after a complete census of the declared domain:

- empty complete fiber → `NONE`
- singleton complete fiber → `ONE(value)`
- complete fiber of size `n>1` → `MANY(family)` with every member
- unfinished scan of the declared domain → `OPEN`, never `NONE`,
  never `ONE` of a found witness, never `MANY` of a found subset

Picking one member of a two-or-more fiber and calling it `ONE` is the
named hostile. That is not a complete fiber.

## Q1 — AND fiber of 1

Complete preimage of `AND=1` on Bits2?

| Name | Predicted | Source of the guess |
|---|---|---|
| `N_and1_one` | `ONE((1,1))` | both bits must be 1 |
| `N_and1_many` | `MANY` | two input ports, so two answers |

## Q2 — AND fiber of 0 (hostile representative)

Complete preimage of `AND=0` on Bits2?

| Name | Predicted | Source of the guess |
|---|---|---|
| `N_and0_many3` | `MANY((0,0),(0,1),(1,0))` | three failing pairs |
| `N_and0_rep` | `ONE((0,0))` | pick the zero pair as “the” solution |
| `N_and0_product4` | `MANY` of all four pairs | `{0,1}×{0,1}` from the two marginals |

## Q3 — XOR fiber of 1 (hostile ordered-pair collapse)

Complete preimage of `XOR=1` on Bits2?

| Name | Predicted | Source of the guess |
|---|---|---|
| `N_xor1_many` | `MANY((0,1),(1,0))` | two ordered disagreements |
| `N_xor1_rep` | `ONE((0,1))` | pick a representative disagreement |
| `N_xor1_set` | `ONE({0,1})` | forget order, keep the unordered support |

## Q4 — NAND fiber of 0

Complete preimage of `NAND=0` on Bits2?

| Name | Predicted | Source of the guess |
|---|---|---|
| `N_nand0_one` | `ONE((1,1))` | NAND is 0 only on the AND-1 pair |
| `N_nand0_none` | `NONE` | confuse NAND=0 with AND=0 |

## Q5 — CONST0 fiber of 1

Complete preimage of `CONST0=1` on Bits2?

| Name | Predicted | Source of the guess |
|---|---|---|
| `N_c0_none` | `NONE` | 1 is not in the image |
| `N_c0_open` | `OPEN` | maybe a larger gate family would hit 1 |

## Q6 — AND=0 joint versus product of marginals

Does the complete `AND=0` fiber equal the product of its one-bit
marginals?

| Name | Predicted | Source of the guess |
|---|---|---|
| `N_and0_joint` | no | product adds `(1,1)`, which AND maps to 1 |
| `N_and0_factor` | yes | each bit separately can be 0 or 1 |

## Q7 — C fiber of (0,0) (hostile representative)

Complete preimage of `C=(0,0)` on Bits3?

| Name | Predicted | Source of the guess |
|---|---|---|
| `N_c00_many` | `MANY((0,0,0),(1,1,1))` | kernel of the two XOR readouts |
| `N_c00_rep` | `ONE((0,0,0))` | pick the zero word |
| `N_c00_prod8` | `MANY` of all eight triples | each bit-marginal is `{0,1}` |

## Q8 — C fiber of (1,1)

Complete preimage of `C=(1,1)` on Bits3?

| Name | Predicted | Source of the guess |
|---|---|---|
| `N_c11_many` | `MANY((0,1,1),(1,0,0))` | y=z=1-x |
| `N_c11_rep` | `ONE((1,0,0))` | pick one of the two |

## Q9 — incomplete AND=0 scan (OPEN, not MANY of found witnesses)

Scan Bits2 for `AND=0` in lexicographic order and stop after two
witnesses, with no coverage argument for the rest of the domain. What
disposition?

| Name | Predicted | Source of the guess |
|---|---|---|
| `N_partial_open` | `OPEN` | unfinished search is not a complete fiber |
| `N_partial_many2` | `MANY((0,0),(0,1))` | report the found subset as MANY |
| `N_partial_one` | `ONE((0,0))` | pick a representative of the found subset |

## Q10 — Add3, supplied c=2

Complete `(a,b)` fiber of `a+b=2` on Add3?

| Name | Predicted | Source of the guess |
|---|---|---|
| `N_add2_many` | `MANY((0,2),(1,1),(2,0))` | three joint pairs, no wrap |
| `N_add2_rep` | `ONE((1,1))` | pick the balanced pair |
| `N_add2_none` | `NONE` | 2+0 would wrap off the carrier |

## Q11 — Add3, supplied c=4

Complete `(a,b)` fiber of `a+b=4` on Add3?

| Name | Predicted | Source of the guess |
|---|---|---|
| `N_add4_none` | `NONE` | 4 is not a sum in `{0,1,2}` |
| `N_add4_open` | `OPEN` | maybe admit `{0,1,2,3,4}` |

## Q12 — XOR fiber of 0

Complete preimage of `XOR=0` on Bits2?

| Name | Predicted | Source of the guess |
|---|---|---|
| `N_xor0_many` | `MANY((0,0),(1,1))` | two equal-bit pairs |
| `N_xor0_class` | `ONE("equal")` | collapse the fiber to a class label |

## Surviving-null test (frozen)

The enumerator must return the named prediction below, or the claim is
restricted / the surviving name is recorded as dead. Attractive errors
are the rejected siblings.

| Q | Surviving name | Rejected sibling(s) |
|---|---|---|
| Q1 | `N_and1_one` | `N_and1_many` |
| Q2 | `N_and0_many3` | `N_and0_rep`, `N_and0_product4` |
| Q3 | `N_xor1_many` | `N_xor1_rep`, `N_xor1_set` |
| Q4 | `N_nand0_one` | `N_nand0_none` |
| Q5 | `N_c0_none` | `N_c0_open` |
| Q6 | `N_and0_joint` | `N_and0_factor` |
| Q7 | `N_c00_many` | `N_c00_rep`, `N_c00_prod8` |
| Q8 | `N_c11_many` | `N_c11_rep` |
| Q9 | `N_partial_open` | `N_partial_many2`, `N_partial_one` |
| Q10 | `N_add2_many` | `N_add2_rep`, `N_add2_none` |
| Q11 | `N_add4_none` | `N_add4_open` |
| Q12 | `N_xor0_many` | `N_xor0_class` |

## Out of scope

Inverse graphics, continuous geometry, certified outer bounds on an
infinite or large grid, SAT/SMT solving, circuit synthesis beyond these
named maps, Lean, a new physics law, treating a picked representative as
the design.

## What would make this run OPEN

If the enumerator imports `rprm` or another research tree, if Bits2 is
scanned as unordered pairs, if Add3 silently wraps, if Q9's stopped
search is labelled `MANY` or `ONE`, if a prediction is edited after
`CENSUS.json` exists, or if any named fiber is reported without listing
every remaining domain point, the result is OPEN, not a complete
NONE/ONE/MANY.
