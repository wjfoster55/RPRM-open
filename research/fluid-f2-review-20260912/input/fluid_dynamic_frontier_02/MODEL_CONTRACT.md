# MODEL_CONTRACT — F2 discrete model-B breach

**Not a continuum-fluid theorem. Discrete simulator question only.**

## Receiver

    Q_H(x) = 1 iff summed water mass in the declared monitored region
             exceeds theta at any frame t = 0..H
             under the model's actual update, gravity, and no new inflow;
             else 0.

Primary parameters, frozen before scored execution:

- model = `B` (pinned `pinned/models.js` `stepB`)
- H = 300
- theta = 0.5
- no new inflow
- no sand in admitted scenes
- `normalizeForModel(grid, 'B')` runs before step 0 and **zeroes** `vx` and `vy` on every water cell
- `grid.wakeAll()` after normalize
- each frame: `beginFrame`, `stepSand` (no-op if no sand), `stepWater(grid, 'B')`
- monitor mass sums `grid.mass[c]` over monitor cells with `type === WATER`
- comparison is `mm > theta` (strict), matching `dynamic_frontier_sim.js`

Source identity for a scene includes: initial `walls` and `mass` fields, W, H, monitor index list, model, scheduler/scan state implied by `Grid.frame` starting at 0, H, theta, and the pinned JS bytes. No randomness is admitted; splash sign uses `(frame + x) & 1`.

## Pinned implementation facts used by every argument

From `pinned/models.js` `stepB` and `pinned/grid.js` `forEachActiveRow`:

1. After gravity, `vy = min(vy + 0.4, 6)`. Fall distance this frame is `max(1, round(vy))` cells, stopping at the first non-empty cell. `B.maxV = 6`, `B.gravity = 0.4`.
2. If **any** fall occurs, the cell relocates and **does not splash this frame**, even if it stopped because the next cell was blocked.
3. If it cannot fall, it converts `vy` into a horizontal splash, then tries, in order: down-diagonal with `hdir`, down-diagonal against `hdir`, horizontal with `hdir`, horizontal against `hdir`. Then `vy = 0`.
4. `hdir` is `sign(vx)` after that conversion. If `|vx| < 0.1`, the sign is `((frame + x) & 1) ? 1 : -1`.
5. There is **no** move with negative `dy`. Increasing `y` is down. This is not an upward splash and not a measured physical velocity law.
6. `forEachActiveRow` is **bottom-to-top**, left-to-right on even frames and right-to-left on odd frames. `stamp` prevents a cell from moving twice in one frame. Bottom-to-top plus stamp is a **cascade**: lower water can vacate a cell before the cell above is processed, so a packed column can drop in one frame without the top cell ever taking the splash branch.
7. Occupancy is at most one water cell. Mass for model B is `C.MaxMass = 1` after normalize.
8. Empty chunks sleep after the first frame unless `wake` is called. `wakeAll` is used at t=0, so frame 1 visits the whole grid; later frames visit dirty chunks only.

## Admitted state that a proof must account for

- `type`, `mass`, `vx`, `vy`, `stamp`, `frame`, `dirty` / `dirtyNext`
- wall geometry, including extra ledges in Family D
- scan direction `(frame & 1)`

A proof that ignores cascade, stamp, or `(frame+x)&1` is not a proof about this updater.

## What is out of contract

- Models A, C, D, E, F
- Sand–water swaps (those can raise water)
- Inflow, brush edits, fractional mass remaining after normalize
- Continuum Euler/Navier–Stokes, Noita-the-game, or production engines
- Changing H or theta after seeing failures
- Rigid-body broadphase (closed F1 counterexample; not this task)

## Source pin

PR12 tree used as the F1 baseline: `91d74b77bde86251468f0d3758f8e84125792677`.
Copied JS SHA-256:

| file | SHA-256 |
|---|---|
| constants.js | `14f3a5c88f5f73ad30f1898eaa96c437ee315aa69d591fee03f409476ad35380` |
| grid.js | `3ec221be5e0ce86ea0ca676f379f63cd14be6b339594a09cb2f671889c2984a3` |
| models.js | `7f20984990f71157ca64c1279b87de27dc39688b5f1bbf684451102c1f79d17f` |
| scenarios.js | `e689ae50e2f3b1d8b1e8986c36203c74f0e27a677d8c3cb371421e65369a4f2a` |

PR13 copies of these three physics files are byte-identical; PR12 is the named pin.
