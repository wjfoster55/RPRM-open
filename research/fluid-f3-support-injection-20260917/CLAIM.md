# F3 — unit-isolation NO; no cheap V≥2 static NO; cycle exact on ledges

**Date:** 2026-09-17  
**Carrier pin:** PR12 `91d74b77bde86251468f0d3758f8e84125792677`, frozen under `research/fluid-f2-review-20260912/input/fluid_dynamic_frontier_02/`  
**Does not restore F2 Layer B.** The two-cell support-injection hostile case remains a refutation of `sill_need` CERTIFIED_NO.

## Problem record

1. **Carrier, types, equality, context.** Finite static-wall grids as in F2 `MODEL_CONTRACT.md`. Cell types empty/water/wall. After the pinned `normalizeForModel(B)` map, every positive-mass non-wall cell has occupancy 1 and `vx=vy=0`. No sand, no inflow, no edits. Equality of states retains type, unit occupancy, velocities, stamp, frame, and dirty chunks. This is a discrete simulator carrier, not continuum fluid.

2. **Ports.** Supplied: initial walls and raw mass, W, H, monitor index list, H=300, theta=0.5, pinned `stepB`. Missing: the future breach bit. Requested readout: `Q_300` = 1 iff monitored unit-mass sum `> 0.5` at any sampled frame 0..300.

3. **Operation.** Deterministic forward `stepB`. Direction: time-forward only. Enabledness: water cells in awake chunks; a cell that falls this frame does not splash this frame; stamp blocks a second move of the same occurrence.

4. **Receiver.** The breach bit only. Not the full trajectory, not Navier–Stokes, not F2's combined AB router.

5. **Fiber.** A fully supplied admitted state has ONE trajectory and ONE bit. A partial occupancy summary is useful only when that bit is constant on the merged family.

6. **Coverage, hostile case, evidence.**
   - Hostile case (preserved): extra walls `(29,36),(30,36)`, water `(30,34),(31,34)`. Frozen Layer B says NO; oracle YES at frame 3. F3 must stay UNRESOLVED then exact YES.
   - Static NO: unique unit cell not on `R_catwalk`.
   - Cheap V≥2 cell-graph NO: none. Official n≥2 after Layer A is UNRESOLVED *statically*.
   - Token-aware class T: occupancy-count over-approx, budgeted, not static.
   - Class E: pinned `stepB` with token-state cycle exit, still exact.

## Claims

| ID | Claim | Grade | Status |
|---|---|---|---|
| F3-A | Unit-normalized Layer A is a sound YES/NO certificate for this receiver (F2 review, reused). | Written proof + finite replay | LIVE |
| F3-ISO | If after unit normalization there is exactly one water cell and it is not in `R_catwalk`, then `Q_H = 0`. | Written proof + finite tests | LIVE |
| F3-ROUTE | Official *static* routing may use A and F3-ISO only. The F2 B `sill_need` NO branch is not an official certificate. n≥2 after A is statically UNRESOLVED. Limited exact may use F3-E cycle exit. | Definition / correction | LIVE |
| F3-HOSTILE | The two-cell support-injection scene is Q=1 at frame 3 under the pinned oracle. | Finite test | LIVE (counterexample) |
| F3-V2-CHEAP | On this admitted container, no occupancy-ignoring cell-graph certificate (catwalk + injection, with or without water floors, ignoring token count) is both sound on packed-column YES and useful as a V≥2 NO while leaving the hostile pair uncertified-NO. | Written proof + finite tests | LIVE |
| F3-T | Class T (exactly n occupied cells, occupancy-respecting one-token moves, ignore frame/`vx`/`vy`/stamp): NO only on exhaustion inside `MAX_N=32`, `MAX_STATES=50000`. Hostile pair meets `R_catwalk` (not T-NO). Isolated n=2 shelf and midair exhaust as T-NO. Packed YES rows are skipped (`n>MAX_N`) and are not T-NO. | Finite tests after frozen nulls | LIVE |
| F3-T-LEDGE | On `D_ledge_end28`, `D_ledge_end30`, `D_sill_end25`, class T neither meets `R_catwalk` nor exhausts inside 50000 expansions (budget hit). No cheap T-NO on those horizon-pay rows. | Finite tests after frozen nulls | LIVE |
| F3-T-COMPLETE | Complete T on those three rows **MEETS** `R_catwalk`: legal occupancy-count paths of length 48/24/49, each replayed on the T graph. Hostile pair still MEETS (not T-NO). So a finished T search would not EXHAUST and cannot certify NO here. | Finite tests after `NULLS_COMPLETE_T.md` | LIVE |
| F3-E | Pinned `stepB` with a hash of occupancy, milli `vx,vy`, frame parity, and `dirtyNext`: the three horizon-pay ledges cycle-exit with `stepsRun` 111/99/52, `Qdyn=0`. Hostile YES at frame 3. `D_ledge_end31` and `A_w4_x26_V180` YES before cycle. | Finite tests after frozen nulls | LIVE |
| F2-B | General Layer B CERTIFIED_NO via `V < sill_need`. | — | **REFUTED** (keep beside survivors) |

F3-V2 as “a cheap static NO for some n≥2 family” is closed as NONE for the occupancy-ignoring cell-graph class. Class T is not that class and is not official static. Class E is exact evolution with an early stop, not a free static NO.

Frozen nulls: `NULLS.md`, `NULLS_COMPLETE_T.md`. Outcomes: `results/token_aware_ledges.json`, `results/cycle_exact_ledges.json`, `results/complete_t_ledges.json`.

## What this is not

Not BSD. Not a T(X,P) monoid paper. Not a new physical fluid law. Not a runtime-win claim. Not a restoration of Layer B.
