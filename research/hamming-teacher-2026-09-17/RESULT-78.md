# HT-78 result

Written after `CENSUS-78.json`. Nulls were frozen in [NULL-78.md](NULL-78.md)
at commit `7a868a8`. The injectivity-vs-line request is the rank lemma in
[LEMMA.md](LEMMA.md), not this census. Replay:

```powershell
python -I -B research/hamming-teacher-2026-09-17/verify_ht28.py
python -I -B research/hamming-teacher-2026-09-17/verify_ht78.py
```

Evidence grade: **finite exhaustive census** of `E`, `ker H`, and two
named source toggles. Written duality is THEORY P9a. Not Lean. Not SAT.

## Dispositions

| Question | Frozen surviving-null test | Result |
|---|---|---|
| Q1. `|S|` | `N_s8` = 8 vs 7 or 16 | **ONE(8)** |
| Q2. `S = C⊥` | `N_dual_yes` vs not-dual / `S = C` | **ONE(yes)** |
| Q3. `|C8|` | `N_ext16` = 16 vs 8 positions or 32 free bits | **ONE(16)** |
| Q4. free `c=4` vs hostile `c=3` | `N_p9b` | **ONE(N_p9b)** |
| Q5. one typed eight? | `N_three_eights` vs `N_one_eight` | **NONE** |

Hamming-8 does **not** double messages. Hostile source toggle `c = 3`
does **not** expand `U`. The historical collapse “seven plus one is the
same eight as Hamming-8 or as four-plus-four roles” is **NONE**.

## Hostile `{1,2,3}`

As **checks**, `{1,2,3}` is the HT-28 line: not injective, answer `000`
is MANY({0,4}).

As a **source toggle**, `c = 1⊕2 = 3` lies in `U = {0,1,2,3}`. Then
`U ∪ (3+U) = U`, still four roles.

Same glyphs, two types. They are not one teacher panel.

## The three eights

| Object | What was counted | Size |
|---|---|---:|
| Simplex response words `S = E(V)` | 7-bit teacher answers | 8 |
| Hamming-8 code `C8` | messages after determined parity | 16 |
| Hamming-8 block | coordinate positions | 8 |
| Free toggle `U ∪ (4+U)` | source roles | 8 |

Nonzero words of `S` have weight 4. `|C| = 16`. Matching an 8 with an 8
does not identify the carrier.

## What remains OPEN

Unique location of Hamming-8 double errors (MANY per syndrome, THEORY P9,
not rerun), silent ninth position, general SAT, nonlinear teachers.
