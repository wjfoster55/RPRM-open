# IF-a result

Written after `CENSUS-ALL.json`. Nulls were frozen in
[NULL-ALL.md](NULL-ALL.md) at commit `2069b6f`. Replay:

```powershell
python -I -B research/inverse-fiber-2026-09-17/verify_all.py
```

Evidence grade: **finite exhaustive check** of all 16 Bits2 tables and
all 256 Bits3 tables. All eight frozen surviving names matched. Not
Lean. Not a theorem for `|F|>2`. Not a physics law.

## Dispositions

| Question | Frozen surviving-null | Result |
|---|---|---|
| QA1. XOR=1 splitters among 16 | `N_xor1_8` | **ONE(8)** |
| QA2. Equals linear duals of `(1,1)`? | `N_xor1_not_lin` | **NONE** — those are `x,y` only |
| QA3. 2-bit parity splits XOR=1? | `N_par2_const` | **NONE** — XOR=1 on both |
| QA4. C=(0,0) splitters among 256 | `N_c00_128` | **ONE(128)** |
| QA5. Equals linear duals of `(1,1,1)`? | `N_c00_not_lin` | **NONE** — four odd-weight linear forms |
| QA6. XOR=1 truth tables | `N_xor1_tables8` | **MANY(8)** listed in CENSUS |
| QA7. Constant-on-fiber extras | `N_const_half` | 8 of 16 and 128 of 256 |
| QA8. Affine XOR=1 splitters | `N_aff_xy_flips` | `x, y, x+1, y+1` |

## Criterion

On these two-point fibers, `D` splits to ONE iff `D(p)≠D(q)`. That is
half of all Boolean extras. The linear duals of the fiber direction
are a proper subset. “Only a coordinate or parity” is dead: 2-bit
parity is constant on XOR=1, and 8 > 2, 128 > 4.

This is not “just linear functionals dual to the fiber.” Stop
padding. No 4-bit lift. No min-cardinality among the nonlinear
splitters.

## What remains OPEN

Certified approximate families. Fibers with more than two members.
A general statement beyond these two named fibers is not this census.
