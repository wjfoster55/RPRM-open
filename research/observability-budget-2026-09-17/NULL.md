# Frozen nulls — finite-budget observability / sensor selection

Written **before** this packet's enumerator was run. Do not edit after
`CENSUS.json` exists except to record that a later task superseded it.

Independent-math Rank 2 from
`rprm-corpus-2026-09-17/03-independent-math-reading.md`: given a finite
machine, a budget `k`, and a question `Q`, which `k` observation ports
make `Q` constant on the representation fiber. Adjacent written source:
the four-state example in `docs/relational-layer.md`. Not AD-R3 linear
row-space closure. Not n=4 obstruction padding. Not fluid, Hamming, BSD,
or O05.

## Carrier (frozen)

Source states `X = {(r,h): r,h in {0,1}}` with pair equality.
Question `Q(r,h) = h`.
Total action `tick(r,h) = (1-r, 1-h)`.
Optional total action `reveal(r,h) = (h,h)`.
Observation-port menu, five named occurrences:

| Port | Map |
|---|---|
| `H` | `(r,h) ↦ h` |
| `R` | `(r,h) ↦ r` |
| `R2` | `(r,h) ↦ r` (distinct occurrence, equal values) |
| `X` | `(r,h) ↦ r XOR h` |
| `Z` | `(r,h) ↦ 0` |

A size-`k` panel `S` is an unordered `k`-subset of `{H,R,R2,X,Z}`.
Horizon-`0` representation: `C_S(x) = (p(x) : p in S)` in port-name order.
A panel is **sufficient** iff `C_S(x)=C_S(y)` implies `Q(x)=Q(y)`.
Horizon-`b` representation along an action alphabet `A` records, in
shortlex word order, either `FAIL` or the same port tuple after the
executed word. Enabledness is total on both named actions.

Named hostile panel: `HOSTILE_MORE = {R, R2, Z}`.

## Q1 — budget 1, horizon 0

How many of the five singletons are sufficient for `Q`?

| Name | Predicted | Source of the guess |
|---|---:|---|
| `N_all5` | 5 | every named sensor sees `h` |
| `N_HX` | 2 | `H` and the XOR port both hide `h` |
| `N_H` | 1 | only the port that *is* `Q` |
| `N_none` | 0 | this menu cannot answer `h` |

## Q2 — more sensors that still do not separate

Is `HOSTILE_MORE` sufficient for `Q` at horizon 0?

| Name | Predicted | Source of the guess |
|---|---|---|
| `N_more_helps` | yes | three ports beat one |
| `N_redundant` | no | copies of `R` plus a constant stay in the `r`-fiber |

If insufficient, which source pair shares the hostile readout and splits
`Q`?

| Name | Predicted pair |
|---|---|
| `N_ghost_00_01` | `(0,0)` and `(0,1)` |
| `N_ghost_other` | some other pair |

## Q3 — more time with only `R`

With panel `{R}`, alphabet `{tick}`, horizon 3: is `Q` constant on the
trace fiber?

| Name | Predicted | Source of the guess |
|---|---|---|
| `N_time_helps` | yes | four observations beat one |
| `N_layer` | no | relational-layer: `(0,0)` and `(0,1)` share `0,1,0,1` for every finite `k` |

## Q4 — budget 2, horizon 0

How many of the `C(5,2)=10` pairs are sufficient?

| Name | Predicted | Source of the guess |
|---|---:|---|
| `N_pairs_all` | 10 | any two ports work |
| `N_pairs_H` | 4 | only pairs that contain `H` |
| `N_pairs_HX` | 6 | every pair containing `H`, plus `{R,X}` and `{R2,X}` |
| `N_pairs_5` | 5 | forget that `R2` is a second `R`-occurrence |

## Q5 — intervention family, not extra sensors

With panel `{R}`, alphabet `{tick, reveal}`, horizon 1: is `Q` constant
on the trace fiber?

| Name | Predicted | Source of the guess |
|---|---|---|
| `N_reveal_separates` | yes | `reveal` makes the existing `R` port read `h` |
| `N_still_hidden` | no | one sensor cannot see two bits |

## Out of scope

AD-R3 row-space recurrence, switched linear systems over `Q`, n=4
operational obstruction, Hamming/teacher panels, BSD, fluid, sensor
placement on infinite or noisy plants, a general advantage theorem
against Kalman rank or Petreczky observability.

## What would make this run OPEN

If the enumerator is not exhaustive on the five ports and ten pairs, if
it imports another research tree, if `R` and `R2` are collapsed by
value-equality of maps before the fiber is formed, or if `reveal` is
silently added to Q3, the result is OPEN, not a count.
