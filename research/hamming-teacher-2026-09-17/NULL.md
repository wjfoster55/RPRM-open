# Frozen nulls — Hamming / teacher 28/35 cut

Written **before** this packet's enumerator was run. Do not edit after
`CENSUS.json` exists except to record that a later task superseded it.

This cut tests one finite claim already stated in the recovered-concepts
backlog and in `research/liar-teacher-formalization-2026-09-12/THEORY.md`
P5–P6 / P9. It does not rerun the SAT pilot, fluid, BSD, or O05 work.

## Question Q1

Carrier: `V = F₂³`, equality of 3-bit vectors, encoded as integers `0..7`
with XOR. Checks: the seven nonzero linear functionals `ℓ_u(x) = popcount(u & x) mod 2`
for `u ∈ {1,…,7}`. Objects: the `C(7,3) = 35` unordered triples of distinct
checks. Readout: the joint map `C_τ : V → {0,1}³` is injective iff every
nonempty fiber is a singleton (equivalently, the three labels have rank 3).

**Q1.** How many of the 35 triples have injective joint readout?

Named nulls, frozen here:

| Name | Predicted | Q1 | Source of the guess |
|---|---:|---|---|
| `N_any` | 35 | every triple works | historical “any of those seven” reduction |
| `N_lines` | 7 | only the Fano lines work | confusing the failure set with the success set |
| `N_pairs` | 21 | one per ordered pair | `7·6/2` without dividing by the 3 pairs in a line |
| `N_p5` | 28 | independent triples work | THEORY P5 prediction |

A later enumerator may confirm at most one of these counts. Confirming a
count is a **finite test** of this carrier, not a Lean proof and not a
theorem about other alphabets.

## Question Q2 — hostile identification

**Q2.** Let `Fail` be the set of non-injective triples. Is
`Fail = { {a,b,a⊕b} : a ≠ b, both nonzero }`?

Named nulls:

| Name | Predicted | Source of the guess |
|---|---|---|
| `N_q2_yes` | yes, and that set has size 7 | THEORY P5 / P6 |
| `N_q2_no` | `Fail` is some other set | “any three” is only off by a few random triples |

## Question Q3 — named swap exhibits (outcomes not inspected yet)

Freeze the start panel and two replacements. Do not rename them after
seeing fibers.

- Start basis `B = {1, 2, 4}` (standard basis of `F₂³`).
- `SWAP_XOR` replaces `4` by `1 ⊕ 4 = 5`, so `{1, 2, 5}`.
- `SWAP_SUM` replaces `4` by `1 ⊕ 2 = 3`, so `{1, 2, 3}`.
- `HOSTILE_LINE = {1, 2, 3}` is the same triple as `SWAP_SUM`.

Named nulls for injectivity of `{SWAP_XOR, SWAP_SUM}`:

| Name | `SWAP_XOR` | `SWAP_SUM` | Source of the guess |
|---|---|---|---|
| `N_both` | injective | injective | any replacement of the third check works |
| `N_neither` | not | not | two checks never determine a unique third |
| `N_p6` | injective | not | THEORY P6: third check must leave `span{1,2}` |

## Question Q4 — Hamming support adapter

Let `H` be the `3×7` matrix whose columns are the nonzero vectors `1..7`
in that order. Hamming-7 is `ker H ⊂ F₂⁷`. Weight-three codewords have
supports that are 3-subsets of `{1,…,7}`.

**Q4.** Does `Fail` equal the set of those weight-three supports?

| Name | Predicted |
|---|---|
| `N_q4_yes` | yes (THEORY P9) |
| `N_q4_no` | the teacher failures and Hamming lines are different 3-subsets |

Cube vertices, dual checks, and error-position labels remain different
types even if the underlying 3-bit words coincide.

## Out of scope

k=4 check panels, Hamming-8 double-error fibers, free-toggle 4→8 source
roles, SAT/P versus NP, BSD, fluid, O05. Those have other packets.

## What would make this run OPEN

If the enumerator is not exhaustive on the 35 triples, if it imports
`verify_panels.py`, or if a type other than linear `F₂` checks is silently
substituted, the result is OPEN, not a count.
