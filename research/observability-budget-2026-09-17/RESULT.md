# OB-k result

Written after `CENSUS.json`. Nulls were frozen in [NULL.md](NULL.md) at
commit `e758dd3`. Replay:

```powershell
python -I -B research/observability-budget-2026-09-17/verify_ob.py
```

Evidence grade: **finite exhaustive census** of five named ports on the
four-state relational-layer machine. Not Lean. Not AD-R3. Not a Kalman
or Petreczky theorem. Not n=4 obstruction padding.

## Dispositions

| Question | Frozen surviving-null test | Result |
|---|---|---|
| Q1. Which 1-port panels make `Q=h` constant? | `N_H` = 1 vs `N_all5`, `N_HX`, `N_none` | **ONE(`{H}`)** |
| Q2. Does `HOSTILE_MORE={R,R2,Z}` separate `h`? | `N_redundant` vs `N_more_helps` | **NONE** |
| Q2 ghost pair | `N_ghost_00_01` vs `N_ghost_other` | **MANY(2)** — `N_ghost_other` |
| Q3. Does `{R}` with tick-only horizon 3 determine `h`? | `N_layer` vs `N_time_helps` | **NONE** |
| Q4. Which 2-port panels make `Q=h` constant? | `N_pairs_HX` = 6 vs `N_pairs_all`, `N_pairs_H`, `N_pairs_5` | **MANY(6)** |
| Q5. Does `{R}` with `{tick,reveal}` horizon 1 determine `h`? | `N_reveal_separates` vs `N_still_hidden` | **ONE(yes)** |

The historical guess “more sensors help” is **NONE** on this carrier:
`{R,R2,Z}` is three ports and still lives inside the `r`-fibers. Extra
tick-time with only `R` is the same **NONE**. The `reveal` action, not
another copy of `R`, is what makes the existing port read `h`.

## Hostile case

`HOSTILE_MORE = {R, R2, Z}` has two occupied answers:

| Answer `R,R2,Z` | Sources | `Q=h` |
|---|---|---|
| 000 | `(0,0)`, `(0,1)` | 0 and 1 |
| 110 | `(1,0)`, `(1,1)` | 0 and 1 |

The frozen ghost guess `N_ghost_00_01` named only the first pair. Both
`r`-fibers split `Q`, so the complete splitting family is **MANY(2)**.
That does not revive `N_more_helps`. `R` and `R2` are distinct
occurrences with equal values; collapsing them by map-equality would
hide that the extra sensor added no coordinate.

## Completing second port, not a third copy of `R`

Budget 2 is **MANY(6)**:

```text
{H,R}  {H,R2}  {H,X}  {H,Z}  {R,X}  {R2,X}
```

`{R,X}` works because `h = r XOR (r XOR h)` on every source. `{R,R2}`
does not: it is two readings of the same visible bit. `{X,Z}` does not:
XOR alone still mixes `(0,0)` with `(1,1)`.

Tick-only traces of `R` through horizon 3:

| Start | Readings after `ε, tick, tick², tick³` |
|---|---|
| `(0,0)` | 0,1,0,1 |
| `(0,1)` | 0,1,0,1 |
| `(1,0)` | 1,0,1,0 |
| `(1,1)` | 1,0,1,0 |

This is the written relational-layer sequence, not a sampled window.

With `reveal` admitted, the horizon-1 `R`-trace separates all four
sources, so `Q` is constant on each fiber. Sensor count stayed 1; the
intervention family changed.

## Sequel — value-copies (Q6–Q8)

Frozen after this census, in [NULL-DUP.md](NULL-DUP.md) at `f535cd0`.
A value-copy never repaired an insufficient L-panel (**NONE** of 80).
That is a [restricted theorem](THEOREM-DUP.md), not a new control law.
Hostile machine M: `{A,A2}` still splits on `{0,1}`; `{A,B}` does not,
because `B` is not a duplicate. See [RESULT-DUP.md](RESULT-DUP.md). Extra time versus an independent
port is [RESULT-TIME.md](RESULT-TIME.md): all 31 L-panels descend;
horizon 3 never refines; `{R,X}` does; hostile shift `{Y}` does not
descend and horizon 2 repairs.

## What remains OPEN

Linear AD-R3 repair rank, switched systems over `Q` or a finite field,
noisy sensors, infinite carriers, and any advantage claim against
Kalman/Petreczky placement. This packet does not establish its own
general soundness beyond the enumerated four-state menu.
