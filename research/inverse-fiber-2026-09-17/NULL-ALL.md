# Frozen nulls — all Boolean extras on two named two-point fibers

Written **before** this packet's all-function enumerator was run. Do
not edit after `CENSUS-ALL.json` exists except to record that a later
task superseded it.

Independent-math Rank 7: min-view search over all Boolean functions on
the IF-v fibers. Adjacent written source: [NULL-VIEW.md](NULL-VIEW.md)
two-point split/split-to-ONE coincidence; IF-v named-menu census.
Not BSD. Not a physics law. Not a 4-bit lift.

## Carrier (frozen)

```text
XOR1 = ((0,1),(1,0))
C00  = ((0,0,0),(1,1,1))
```

A **Boolean readout** on Bits2 is any total map `{0,1}^2 → {0,1}`.
There are `2^4 = 16`, listed as truth tables
`(D(0,0), D(0,1), D(1,0), D(1,1))` in that domain order.

A Boolean readout on Bits3 is any total map `{0,1}^3 → {0,1}`. There
are `2^8 = 256`. Domain order is lexicographic triples
`(000,001,010,011,100,101,110,111)`.

`D` **splits `F` to ONE** iff `D` is injective on `F`. On these
two-point fibers that is `D(p) ≠ D(q)`. A readout constant on `F` is
not discriminating.

Linear functionals are `F_2`-linear maps (no constant term). Affine
maps are linear plus a constant. The **linear duals of the fiber
direction** are the linear `L` with `L(p+q) = 1` (`p+q` is `(1,1)` on
XOR1 and `(1,1,1)` on C00).

Coverage: every one of the 16, and every one of the 256. 256 is
admitted as fast exact enumeration, not a sample.

## QA1 — how many of the 16 split XOR=1 to ONE?

| Name | Predicted | Source of the guess |
|---:|---:|---|
| `N_xor1_8` | 8 | two-point: half the tables have `D(0,1) ≠ D(1,0)` |
| `N_xor1_2` | 2 | only FST and SND (IF-v menu) |
| `N_xor1_3` | 3 | only a coordinate or parity |
| `N_xor1_4` | 4 | only affine duals |

## QA2 — is the XOR=1 splitting family exactly the linear duals of `(1,1)`?

| Name | Predicted | Source of the guess |
|---|---|---|
| `N_xor1_not_lin` | no | linear duals are `x` and `y` only |
| `N_xor1_just_lin` | yes | “min-view is the dual space” |

## QA3 — does 2-bit parity (XOR) split XOR=1?

| Name | Predicted | Source of the guess |
|---|---|---|
| `N_par2_const` | no | XOR=1 on both members |
| `N_par2_splits` | yes | coordinate-or-parity guess includes it |

## QA4 — how many of the 256 split C=(0,0) to ONE?

| Name | Predicted | Source of the guess |
|---:|---:|---|
| `N_c00_128` | 128 | two-point: half of `2^8` |
| `N_c00_5` | 5 | IF-v menu `X,Y,Z,PARITY,AND3` |
| `N_c00_4` | 4 | only a coordinate or parity |
| `N_c00_8` | 8 | only affine odd-weight |

## QA5 — is the C=(0,0) splitting family exactly the linear duals of `(1,1,1)`?

| Name | Predicted | Source of the guess |
|---|---|---|
| `N_c00_not_lin` | no | those are the four odd-weight linear forms |
| `N_c00_just_lin` | yes | dual space of the fiber direction |

## QA6 — XOR=1 splitting truth tables, domain order `(00,01,10,11)`

| Name | Predicted family |
|---|---|
| `N_xor1_tables8` | `((0,0,1,0),(0,0,1,1),(0,1,0,0),(0,1,0,1),(1,0,1,0),(1,0,1,1),(1,1,0,0),(1,1,0,1))` |
| `N_xor1_xy_only` | `((0,0,1,1),(0,1,0,1))` — FST and SND |
| `N_xor1_coord_par` | FST, SND, and XOR `(0,1,1,0)` |

## QA7 — how many extras are constant on each fiber? (hostile)

| Name | Predicted |
|---|---|
| `N_const_half` | 8 of 16 and 128 of 256 |
| `N_const_none` | 0 — every extra readout discriminates |

## QA8 — which affine maps split XOR=1?

| Name | Predicted |
|---|---|
| `N_aff_xy_flips` | `x, y, x+1, y+1` |
| `N_aff_xy_only` | `x, y` |
| `N_aff_all8` | every affine map |

## Surviving-null test (frozen)

| Q | Surviving name | Rejected sibling(s) |
|---|---|---|
| QA1 | `N_xor1_8` | `N_xor1_2`, `N_xor1_3`, `N_xor1_4` |
| QA2 | `N_xor1_not_lin` | `N_xor1_just_lin` |
| QA3 | `N_par2_const` | `N_par2_splits` |
| QA4 | `N_c00_128` | `N_c00_5`, `N_c00_4`, `N_c00_8` |
| QA5 | `N_c00_not_lin` | `N_c00_just_lin` |
| QA6 | `N_xor1_tables8` | `N_xor1_xy_only`, `N_xor1_coord_par` |
| QA7 | `N_const_half` | `N_const_none` |
| QA8 | `N_aff_xy_flips` | `N_aff_xy_only`, `N_aff_all8` |

## Out of scope

4-bit maps (`2^{16}` tables), min-cardinality among nonlinear
splitters, a general theorem for `|F|>2`, Lean, a physics law,
rewriting IF-v's named menu as this cut.

## What would make this run OPEN

If the enumerator samples 256 instead of listing all 256, if it
imports `rprm`, if a constant-on-fiber table is labelled a splitter,
or if these predictions are edited after `CENSUS-ALL.json` exists,
the result is OPEN.
