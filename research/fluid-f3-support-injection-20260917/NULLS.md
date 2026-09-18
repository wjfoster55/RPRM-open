# Frozen nulls — token-aware F3 cut (2026-09-17)

Written **before** the occupancy-count search and cycle-detect exact
were run. Do not edit hypotheses after looking. Outcomes go in
`CLAIM.md` and `results/`.

Layer B stays refuted. Occupancy-ignoring cell-graph NO stays NONE.
Official static routing stays Layer A + n=1 isolation. This cut is not
BSD and is not a free static NO.

## Carrier (unchanged)

Pinned model B, unit occupancy after `normalizeForModel(B)`, static
walls, no sand, no inflow. 64×48 divider container (and the 96×64
scale pair). Receiver `Q_300`. Hostile extra walls `(29,36),(30,36)`,
water `(30,34),(31,34)` must not become a false NO.

## Certificate class T — n-token occupancy over-approx

**State:** exactly `n` occupied non-wall cells (the actual token count).
**Transition:** one token relocates along an occupancy-respecting
model-B move: fall `1..6` through empty cells if the cell immediately
below is empty; otherwise splash to an empty down-diagonal or
horizontal neighbour. Frame, `vx`, `vy`, stamp, and scan order are
ignored, so one-token transitions over-approximate actual `stepB`.
**NO:** no reachable state intersects `R_catwalk`, and the search
**exhausts** inside the budget.
**UNRESOLVED:** a reached state meets `R_catwalk`, or the budget is
hit, or `n` exceeds `MAX_N`.
**Never YES.** Budget: `MAX_N = 32`, `MAX_STATES = 50000` expanded
configurations. Hitting the cap is not a NO.

This is cheaper than 300-frame exact only when a witness or exhaustion
occurs inside the cap. It is not a cell-graph soup: token count is
enforced.

## Certificate class E — token-state cycle exact

Pinned `stepB` (F3 driver, frozen JS bytes unchanged). After each
frame hash occupancy, milli-quantized `vx,vy`, frame parity, and
`dirtyNext` chunks. Stop on monitor YES, Layer-A empty, exact token-
state repeat, or `t=H`. A repeat with no prior breach is `Q=0` for
this updater (periodic continuation). Budget `H=300`. Cheaper than
horizon-pay iff `stepsRun < 300`.

## Hypotheses (frozen)

| ID | Hypothesis | Falsified if |
|---|---|---|
| T-H1 | Hostile pair: T meets `R_catwalk` inside budget (not T-NO). | T exhausts with no meet, or T-NO. |
| T-H2 | `D_ledge_end28`, `D_ledge_end30`, `D_sill_end25`: T meets `R_catwalk` **or** hits the cap — no cheap T-NO on these horizon-pay rows. | T exhausts with no meet (then T-NO is live on those rows). |
| T-H3 | Packed YES `A_w4_x26_V180` and `C_adj4_V60`: T does not T-NO (n>MAX_N skip, cap, or meet). | T-NO on either. |
| T-H4 | `shelf_two_far` (n=2): T exhausts with no meet — a cheap T-NO exists for that isolated pair. | T meets or hits cap. |
| T-H5 | `D_ledge_end31` (actual Q=1): T meets `R_catwalk`. | T-NO. |
| E-H1 | The three horizon-pay ledges cycle-exit with `stepsRun < 300` and `Qdyn=0`. | Any of the three still pays H or reports Q=1. |
| E-H2 | Hostile pair: E reports YES at frame 3; not a cycle-NO. | Cycle-NO or wrong first breach. |
| E-H3 | `D_ledge_end31` and `A_w4_x26_V180`: E reports YES before cycle. | Cycle-NO on a Q=1 row. |

## Official routing after this cut

Unchanged unless a hypothesis earns a **budgeted** (not static)
certificate that is sound on the hostile pair and the packed YES
rows. T-NO, if any, is labeled budgeted occupancy-count, never
`sill_need`.
