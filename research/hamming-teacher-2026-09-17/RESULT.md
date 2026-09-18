# HT-28 result

Written after `CENSUS.json`. Nulls were frozen in [NULL.md](NULL.md) at
commit `0e9168d`. Replay:

```powershell
python -I -B research/hamming-teacher-2026-09-17/verify_ht28.py
```

Evidence grade: **finite exhaustive census** of linear checks on `F₂³`.
Not Lean. Not a Manifesto theorem. Not a SAT or Hamming-8 result.

## Dispositions

| Question | Frozen surviving-null test | Result |
|---|---|---|
| Q1. How many of 35 triples inject? | `N_p5` = 28 vs `N_any` = 35, `N_lines` = 7, `N_pairs` = 21 | **ONE(28)** |
| Q2. Fail = `{{a,b,a⊕b}}`? | `N_q2_yes` vs `N_q2_no` | **ONE(yes)** |
| Q3. Named swaps | `N_p6` (XOR works, sum fails) vs both/neither | **ONE(N_p6)** |
| Q4. Fail = Hamming-7 weight-3 supports? | `N_q4_yes` vs `N_q4_no` | **ONE(yes)** |

The historical universal “any of those seven” is **NONE** on this carrier:
seven triples fail. Those seven failures are **MANY(7)**, listed below, and
are exactly the Hamming lines.

## Successful swap and failing swap

Start panel `B = {1,2,4}`.

- `SWAP_XOR = {1,2,5}` (replace `4` by `1⊕4`): injective, eight singleton
  fibers. This is a justified third-check handoff.
- `SWAP_SUM = {1,2,3}` (replace `4` by `1⊕2`): rank 2. Answer `000` is
  **MANY({0,4})**. The third answer is determined by the first two, so the
  panel cannot recover the missing bit.

## Hostile case

`HOSTILE_LINE = {1,2,3}` is the failing swap. Occupied answers and fibers:

| Answer | Sources |
|---|---|
| 000 | 0, 4 |
| 101 | 1, 5 |
| 011 | 2, 6 |
| 110 | 3, 7 |

The four unoccupied answers are empty, not source states. THEORY P6's
example `{4,2,6}` is another of the same seven lines (it appears in the
census as `(2,4,6)`). Cube vertices, check labels, and Hamming positions
remain different types.

## The seven failing triples

```text
(1,2,3)  (1,4,5)  (1,6,7)  (2,4,6)  (2,5,7)  (3,4,7)  (3,5,6)
```

Each is `{a,b,a⊕b}`. Each is a weight-three Hamming-7 support under the
column labeling `1..7`. Hamming-7 itself has 16 codewords; that count is a
consistency check, not a second claim.

## What remains OPEN

k>3, nonlinear checks, Hamming-8 double-error location (MANY per syndrome
in THEORY P9, not rerun here), free-toggle 4→8 source roles, general SAT.
This packet does not establish its own general soundness beyond the
enumerated carrier.
