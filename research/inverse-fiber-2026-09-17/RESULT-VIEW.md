# IF-v result

Written after `CENSUS-VIEW.json`. Nulls were frozen in
[NULL-VIEW.md](NULL-VIEW.md) at commit `14c5b8a`. Replay:

```powershell
python -I -B research/inverse-fiber-2026-09-17/verify_view.py
```

Evidence grade: **finite exhaustive check** of two named menus on two
named MANY fibers. All eight frozen surviving names matched. Not Lean.
Not a minimum-view theorem. Not a physics law.

## Dispositions

| Question | Frozen surviving-null | Result |
|---|---|---|
| QV1. Bits2 splitters of XOR=1 | `N_xor1_fst_snd` | **ONE((FST,SND))** |
| QV2. AND splits XOR=1? | `N_and_const` | **NONE** — AND=0 on both |
| QV3. OR splits XOR=1? | `N_or_const` | **NONE** — OR=1 on both |
| QV4. FST splits XOR=1 to ONE? | `N_fst_one` | **ONE(yes)** |
| QV5. XOR=1 after FST=0 | `N_fst0_one` | **ONE((0,1))** |
| QV6. Bits3 splitters of C=(0,0) | `N_c00_xyzpa` | **ONE((X,Y,Z,PARITY,AND3))** |
| QV7. C0 splits C=(0,0)? | `N_c0_const` | **NONE** — both have C0=0 |
| QV8. C=(0,0) after X=0 | `N_x0_one` | **ONE((0,0,0))** |

## Hostile cases

AND, OR, EQ, and CONST0 are extra-looking Bits2 readouts that stay
constant on XOR=1. Already-supplied `C0` stays constant on C=(0,0).
Those are not discriminating views. “Any extra gate helps” is dead.

## What remains OPEN

Minimum-view search over all Boolean functions, certified approximate
families, larger grids. Discrete census on these two menus stops here.
