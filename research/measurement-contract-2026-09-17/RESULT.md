# MC-k result

Written after `CENSUS.json`. Nulls were frozen in [NULL.md](NULL.md) at
commit `0256331`. Replay:

```powershell
python -I -B research/measurement-contract-2026-09-17/verify_mc.py
```

Evidence grade: **finite exhaustive check** of Bits2 (4 ordered pairs)
under Count2, Mean2, and FourState. Exact integer and `Fraction`
arithmetic. Not Lean. Not a laboratory calibration. Not a physics law.
All twelve frozen surviving names matched. None died.

## Dispositions

| Question | Frozen surviving-null | Result |
|---|---|---|
| Q1. XOR constant on Count2 | `N_xor_const` | **ONE(yes)** — decoder `h(0)=0`, `h(1)=1`, `h(2)=0` |
| Q2. Mean2 numeral equals XOR | `N_mean_not_xor` | **NONE** — `(1,1)` has mean `1` and XOR `0`; `(0,1)` has mean `1/2` and XOR `1` |
| Q3. PAIR fiber of count `1` | `N_sum1_many` | **MANY((0,1),(1,0))** |
| Q4. Count-1 joint vs product | `N_sum1_joint` | **NONE** of equality — product is all four pairs |
| Q5. FST constant on Count2 | `N_fst_split` | **NONE** — fiber of 1 has `FST=0` and `FST=1` |
| Q6. FourState fiber of `1` | `N_c4_1_one` | **ONE((1,0))** |
| Q7. FourState fiber of `2` | `N_c4_2_one` | **ONE((0,1))** |
| Q8. PAIR fiber of count `0` | `N_sum0_one` | **ONE((0,0))** |
| Q9. Count2/Mean2 same kernel | `N_same_kernel` | **ONE(yes)** |
| Q10. Mean2 is a sure Bernoulli of XOR | `N_unit_count` | **NONE** — image is `{0, 1/2, 1}` |
| Q11. Mean2 with only `a=1` | `N_en_disabled` | **DISABLED** |
| Q12. Count2 is a CAR onto its image | `N_count_fold` | **NONE** — count `1` is MANY |

AND is constant on Count2 (control, not a scored null): AND is `1`
exactly at count `2`. FourState is a CAR: each code `0,1,2,3` has a
singleton pair-fiber.

## Hostile cases

**Looks identified, fiber is MANY.** Q3 rejects `ONE((0,1))`. Q12
rejects treating Count2 as a CAR because three of four codes are
unique. The remaining code is `MANY((0,1),(1,0))`.

**Missing ports treated as independent.** Q4: both bit-marginals of
count `1` are `{0,1}`; their product adds `(0,0)` and `(1,1)`.

**Estimator-as-display / units / receiver unstated.** Q2: the Mean2
numeral is not XOR. Q10: occupancy of `[0,1]` is not a probability
law of XOR; `1/2` is in the image. Q5: the mean does not identify the
first bit.

**Enabledness unstated.** Q11: a missing `b` disables Mean2; it is not
a one-sample mean of the visible bit.

## What remains OPEN

Rank-8 machine-readable units/calibration/source-identity contracts,
prospective use on a real pipeline, Lean. This packet does not
establish its own general soundness beyond Count2, Mean2, and
FourState on Bits2.
