# IF-j result

Written after `CENSUS-JOINT.json`. Nulls were frozen in
[NULL-JOINT.md](NULL-JOINT.md) at commit `bd28533`. Replay:

```powershell
python -I -B research/inverse-fiber-2026-09-17/verify_joint.py
```

Evidence grade: **finite exhaustive check** of the IF-k named fibers
against the products of their one-port marginals. All eight frozen
surviving names matched. Not Lean. Not a physics law.

## Dispositions

| Question | Frozen surviving-null | Result |
|---|---|---|
| QJ1. XOR=1 equals product? | `N_xor1_joint` | **NONE** of equality |
| QJ2. XOR=1 extras | `N_xor1_extra_eq` | **MANY(((0,0),(1,1)))** — the XOR=0 fiber |
| QJ3. C=(0,0) equals product? | `N_c00_joint` | **NONE** of equality |
| QJ4. C=(0,0) extras | `N_c00_extra6` | **MANY(6)** of the other triples |
| QJ5. C=(1,1) equals product? | `N_c11_joint` | **NONE** of equality |
| QJ6. Product admits `(1,1)`? | `N_xor1_admits_11` | **ONE(yes)** |
| QJ7. AND=1 equals product? | `N_and1_equals` | **ONE(yes)** — `{1}×{1}` |
| QJ8. XOR=0 and XOR=1 same product? | `N_xor_same_prod` | **ONE(yes)** — both are `X2` |

## Hostile cases

Reconstructing XOR=1 by choosing each bit from `{0,1}` independently
adds `(0,0)` and `(1,1)`, which XOR maps to 0. Reconstructing C=(0,0)
or C=(1,1) from three `{0,1}` marginals adds six illegal triples.

The product does not name the law: XOR=0 and XOR=1 share one product.
A singleton **does** factor (QJ7). “No fiber equals its product” is
dead.

## What remains OPEN

Discriminating-view selection (which extra readout splits a MANY fiber
to ONE) is the next cut, not this one. Certified approximate families
and larger grids remain OPEN.
