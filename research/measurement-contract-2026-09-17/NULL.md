# Frozen nulls — scientific measurement-contract auditing

Written **before** this packet's enumerator was run. Do not edit after
`CENSUS.json` exists except to record that a later task superseded it.

Independent-math Rank 8 from
`rprm-corpus-2026-09-17/03-independent-math-reading.md`: measurement-contract
auditing for scientific pipelines. This cut is the smallest typed toy
contract, not Rank-8's machine-readable provenance/units interchange or
a real reproducibility audit. Adjacent written sources: Manifesto
III.7 count/density of a binary block and Proposition III.7.2 four-state
`a+2b`; Process Mechanics measurement-admission flags (arithmetic vs
calibration vs estimator equivalence); AGENT_HANDBOOK §2 units and
occurrences. Not a paper scrape. Not BSD. Not fluid. Not Hamming. Not
O05. Not observability. Not Markov. Not inverse-fiber 4-bit padding.

## Carrier (frozen)

**Bits2.** Domain `X = {(0,0),(0,1),(1,0),(1,1)}` with ordered-pair
equality. `(0,1)` is not `(1,0)`. Bits are exact integers `0` and `1`,
not booleans-as-ints and not floats.

Named source questions `X → {0,1}`:

```text
XOR(a,b) = 1 iff a≠b
AND(a,b) = 1 iff a=1 and b=1
FST(a,b) = a
```

The pair readout `PAIR(a,b)=(a,b)` requests the source itself.

**Count2.** Manifesto III.7 count of a length-2 binary block:

```text
C_sum(a,b) = a+b ∈ {0,1,2}
```

Unit: bit-count. Kind: total function on `X`. Enabled iff both ports
`a` and `b` are supplied. A missing port is disabled, not a one-sample
mean of the visible bit.

**Mean2.** Manifesto density: divide the count by known `n=2`.

```text
C_mean(a,b) = (a+b)/2 ∈ {0, 1/2, 1}
```

Values are exact `Fraction`. Occupancy of `[0,1]` is not a probability
law. No Bernoulli model is supplied.

**FourState.** Manifesto Proposition III.7.2 instrument:

```text
C4(a,b) = a+2b ∈ {0,1,2,3}
```

with the written inverse `a = z mod 2`, `b = floor(z/2)`.

A **representation fiber** of `C` at display `z` is `{x in X: C(x)=z}`,
listed lexicographically. `Q` is **identified** by `C` iff `Q` is
constant on every nonempty fiber (Manifesto II.2 / factorization). Then
a unique decoder `h` on the reached image satisfies `Q = h ∘ C`.
Numerical equality `C(x)=Q(x)` is a different contract (estimator
equivalence to the display numeral).

Missing ports stay joint. The product of one-bit marginals of a fiber
is not the fiber.

Dispositions for a complete pair-fiber:

- empty → `NONE`
- singleton → `ONE(value)`
- size `n>1` → `MANY(family)`
- unfinished scan → `OPEN`

Picking one member of a two-or-more fiber and calling the pair
identified is the named hostile. A contract that looks identified
because three of four Count2 codes are unique still has `MANY` at
count `1`.

The Count2/Mean2 instrument is not a physical detector. FourState is
not a laboratory voltmeter. No physics law is claimed.

## Q1 — XOR constant on Count2 fibers

Is `XOR` constant on every nonempty `C_sum` fiber?

| Name | Predicted | Source of the guess |
|---|---|---|
| `N_xor_const` | yes | Manifesto: parity is determined by count |
| `N_xor_split` | no | a mean cannot see an exclusive-or |

## Q2 — display mean equals XOR as numbers (estimator-as-display)

Does `C_mean(x) = XOR(x)` hold for every `x` in `X` (integer `XOR`
compared with `Fraction` mean)?

| Name | Predicted | Source of the guess |
|---|---|---|
| `N_mean_is_xor` | yes | sample mean of two bits estimates XOR |
| `N_mean_not_xor` | no | `(1,1)` has mean `1` and XOR `0` |

## Q3 — Count2 fiber of 1 (hostile identified-looking pair)

Complete `PAIR` fiber of `C_sum=1`?

| Name | Predicted | Source of the guess |
|---|---|---|
| `N_sum1_many` | `MANY((0,1),(1,0))` | `binom(2,1)=2` |
| `N_sum1_rep` | `ONE((0,1))` | pick a representative; the count looks like a measurement of the pair |

## Q4 — independent missing ports at Count2=1

Does that fiber equal the product of its one-bit marginals?

| Name | Predicted | Source of the guess |
|---|---|---|
| `N_sum1_joint` | no | product adds `(0,0)` and `(1,1)` |
| `N_sum1_factor` | yes | each bit-marginal is `{0,1}` |

## Q5 — FST constant on Count2 fibers

Is `FST` constant on every nonempty `C_sum` fiber?

| Name | Predicted | Source of the guess |
|---|---|---|
| `N_fst_const` | yes | the mean is an estimate of the first bit |
| `N_fst_split` | no | fiber of 1 has `FST=0` and `FST=1` |

## Q6 — FourState fiber of code 1

Complete `PAIR` fiber of `C4=1`?

| Name | Predicted | Source of the guess |
|---|---|---|
| `N_c4_1_one` | `ONE((1,0))` | Manifesto inverse `a=z mod 2`, `b=floor(z/2)` |
| `N_c4_1_many` | `MANY` | two bits, so two preimages |

## Q7 — FourState fiber of code 2

Complete `PAIR` fiber of `C4=2`?

| Name | Predicted | Source of the guess |
|---|---|---|
| `N_c4_2_one` | `ONE((0,1))` | written inverse |
| `N_c4_2_sum` | `ONE((1,0))` | confuse `a+2b=2` with `a+b=1` |

## Q8 — Count2 fiber of 0

Complete `PAIR` fiber of `C_sum=0`?

| Name | Predicted | Source of the guess |
|---|---|---|
| `N_sum0_one` | `ONE((0,0))` | only the zero pair has count 0 |
| `N_sum0_none` | `NONE` | empty-looking display |

## Q9 — Count2 and Mean2 have the same fibers (units vs kernel)

Do `C_sum` and `C_mean` have equal nonempty fibers (same kernel)?

| Name | Predicted | Source of the guess |
|---|---|---|
| `N_same_kernel` | yes | Manifesto: density has the same fibers as count |
| `N_diff_kernel` | no | integer `{0,1,2}` is a different instrument from `{0,1/2,1}` |

## Q10 — Mean2 is a probability of XOR without a stated law (units/receiver)

Without a probability law, does occupancy of `[0,1]` make `C_mean` a
probability of `XOR`?

Exact predicate used by the enumerator: `C_mean(x)` equals the
`Fraction` of the integer `XOR(x)` for every `x` (the realized-XOR
Bernoulli reading of the display).

| Name | Predicted | Source of the guess |
|---|---|---|
| `N_unit_prob` | yes | values lie in `[0,1]` |
| `N_unit_count` | no | `[0,1]` occupancy is not a probability law; the predicate fails at `(0,1)` |

## Q11 — enabledness: Mean2 with only port `a=1` supplied

Both-port Mean2, environment `{a:1}`, `b` missing. What does the
instrument return?

| Name | Predicted | Source of the guess |
|---|---|---|
| `N_en_one` | `ONE(1)` | one-sample mean of the visible bit |
| `N_en_disabled` | disabled | Count2/Mean2 is enabled iff both ports are supplied |

## Q12 — Count2 identifies the pair (hostile CAR)

Is `C_sum` a CAR onto its image (every reached display has a singleton
pair-fiber)?

| Name | Predicted | Source of the guess |
|---|---|---|
| `N_count_car` | yes | three of four codes are unique, so the pair looks identified |
| `N_count_fold` | no | fiber of count `1` is `MANY` |

## Surviving-null test (frozen)

The enumerator must return the named prediction below, or the claim is
restricted / the surviving name is recorded as dead. Attractive errors
are the rejected siblings.

| Q | Surviving name | Rejected sibling |
|---|---|---|
| Q1 | `N_xor_const` | `N_xor_split` |
| Q2 | `N_mean_not_xor` | `N_mean_is_xor` |
| Q3 | `N_sum1_many` | `N_sum1_rep` |
| Q4 | `N_sum1_joint` | `N_sum1_factor` |
| Q5 | `N_fst_split` | `N_fst_const` |
| Q6 | `N_c4_1_one` | `N_c4_1_many` |
| Q7 | `N_c4_2_one` | `N_c4_2_sum` |
| Q8 | `N_sum0_one` | `N_sum0_none` |
| Q9 | `N_same_kernel` | `N_diff_kernel` |
| Q10 | `N_unit_count` | `N_unit_prob` |
| Q11 | `N_en_disabled` | `N_en_one` |
| Q12 | `N_count_fold` | `N_count_car` |

## Out of scope

Scraping papers, BRCA1, protein folding, laboratory calibration traces,
`rprm.process_mechanics.measurement` flag summarizer as an oracle,
Lean, a new physics law, inverse-fiber 4-bit tables, Rank-8 workflow
standards.

## What would make this run OPEN

If the enumerator imports `rprm` or another research tree, if bits are
floats or booleans-as-ints, if Mean2 uses binary `/` floats, if a
missing port is silently filled, if FourState wraps modulo 4, if a
prediction is edited after `CENSUS.json` exists, or if `MANY` is
issued for an unfinished scan, the result is OPEN, not a complete
NONE/ONE/MANY.
