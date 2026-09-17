# F3 — unit-isolation NO after Layer B refutation

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
   - New static NO: unique unit cell not on `R_catwalk`.
   - V ≥ 2 static NO: OPEN.

## Claims

| ID | Claim | Grade | Status |
|---|---|---|---|
| F3-A | Unit-normalized Layer A is a sound YES/NO certificate for this receiver (F2 review, reused). | Written proof + finite replay | LIVE |
| F3-ISO | If after unit normalization there is exactly one water cell and it is not in `R_catwalk`, then `Q_H = 0`. | Written proof + finite tests | LIVE |
| F3-ROUTE | Official static routing may use A and F3-ISO only. The F2 B `sill_need` NO branch is not an official certificate. | Definition / correction | LIVE |
| F3-HOSTILE | The two-cell support-injection scene is Q=1 at frame 3 under the pinned oracle. | Finite test | LIVE (counterexample) |
| F2-B | General Layer B CERTIFIED_NO via `V < sill_need`. | — | **REFUTED** (keep beside survivors) |
| F3-V2 | A static NO bound for two or more cells that survives injection. | — | **OPEN** |

NONE/ONE/MANY are not returned for F3-V2. That search is unfinished.

## What this is not

Not BSD. Not a T(X,P) monoid paper. Not a new physical fluid law. Not a runtime-win claim. Not a restoration of the five original multi-cell B-only panel NOs as a theorem.
