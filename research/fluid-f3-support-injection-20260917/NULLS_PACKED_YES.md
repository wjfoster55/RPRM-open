# Frozen nulls — packed-column static YES (2026-09-17)

Written **before** the V=60 far-edge probe and the predicate scan.
Do not edit hypotheses after looking. Outcomes go in `CLAIM.md` and
`results/`.

1-high NO is already official (`4350188`). Layer B stays refuted. Not
BSD. The extra-walls hostile pair must not become a static YES.

## Domain

Pinned model B, unit occupancy, 64×48 container, `dx=32`, `crest_h=10`,
`crest_y=36`, `floor=46`. No sand, no inflow.

## Predicate Y1 (frozen)

A scene **matches Y1** iff after unit normalize the occupied cells are
exactly a hole-free rectangle of width `w ≥ 4` whose bottom row sits on
the container floor (`y = floor`), right edge `x_r ≥ 29` (`dx-3`), and
`V ≥ 60`.

**Claim:** match ⇒ `Q_300 = 1`.

Hostile extra walls `(29,36),(30,36)` with two midair cells does not
match (not a floor rectangle of width ≥ 4). Packed-looking Q=0 rows
with `V < 60` (`C_adj4_V20`, `C_adj4_V40`) or `x_r < 29` (`A_w4_x24`)
or `w = 2` do not match and are not counterexamples.

## Kill probe (frozen before execution)

`probe_w4_x26_V60`: same container, column `x0=26`, `w=4`, `V=60`
(hole-free, floor-sitting). This is the cheapest Y1 match at the
farthest allowed right edge. If the oracle returns `Q=0`, Y1 is false.

## Hypotheses

| ID | Hypothesis | Falsified if |
|---|---|---|
| Y1-H1 | Every frozen-panel scene that matches Y1 has stored `Q_ref = 1`. | A matching panel row with Q=0. |
| Y1-H2 | `probe_w4_x26_V60` has oracle `Qdyn = 1`. | Oracle Q=0 (Y1 dies). |
| Y1-H3 | Hostile pair does not match Y1; official F3 static is not CERTIFIED_YES. | Y1 match or official YES on the hostile scene. |

## Predicate Y2 (frozen after Y1 died, before the hang probe)

Y1 died: `probe_w4_x26_V60` floor-sitting matches Y1 and the oracle is
`Qdyn=0`. Floor-sitting is not the panel packed-column shape (those
are top-filled from `y=1`). A replacement occupancy predicate that
does match `A_w4_x26_V180` / `C_adj4_V60`:

A scene **matches Y2** iff after unit normalize the occupied cells are
exactly a hole-free rectangle of width `w ≥ 4` whose **top row is the
ceiling row** (`y_top = 1`), right edge `x_r ≥ 29`, `V ≥ 60`, and
`x_r < dx`, on the 64×48 container.

**Claim:** match ⇒ `Q_300 = 1`.

Hostile pair does not match. `C_adj4_V20/V40` (`V<60`) and `A_w4_x24`
(`x_r=27`) do not match.

## Kill probe Y2 (frozen before execution)

`probe_hang_w4_x26_V60`: same container, `column_cells` from `y=1`
down, `x0=26`, `w=4`, `V=60` (hole-free, ceiling-hanging). Cheapest
Y2 match at the farthest allowed right edge. If the oracle returns
`Q=0`, Y2 is false.

## Hypotheses Y2

| ID | Hypothesis | Falsified if |
|---|---|---|
| Y2-H1 | Every frozen 64×48 panel scene that matches Y2 has stored `Q_ref = 1`. | A matching panel row with Q=0. |
| Y2-H2 | `probe_hang_w4_x26_V60` has oracle `Qdyn = 1`. | Oracle Q=0 (Y2 dies). |
| Y2-H3 | Hostile pair does not match Y2; official F3 static is not CERTIFIED_YES. | Y2 match or official YES on the hostile scene. |
