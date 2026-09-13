# DERIVATION — crest-cut bound and the occupancy interaction

## Question restated

Can a justified geometry/motion-aware partial description certify some
`Q_300` answers, or route limited exact work, more selectively than rolling
every scene for 300 frames?

The volume/container summary is already known to be insufficient (F1; not
re-litigated). Volume+height still collides. This note does not restore a
velocity-only story: both F1 witnesses start at `vx=vy=0`.

## Move graph (from the code, not from a continuum picture)

A non-wall cell may send a water cell to:

- `(x, y+k)` for `k = 1..6` if the path is non-wall (`B.maxV`)
- `(x±1, y+1)` or `(x±1, y)` if the destination is non-wall

Never `(x, y-1)`. Time is ignored in the static graphs on the admitted
grids because the move-graph diameter is < 300; a nonempty path of any
length still only *prevents* a NO certificate, it does not create a false NO.

## Layer A — occupancy-ignoring reachability `R_opt`

Reverse-BFS from the monitor on the move graph above, treating other water
as absent. Let `W_opt` be the current water mass on `R_opt`.

- If current monitor mass `> theta`: **CERTIFIED_YES** (exact, t=0).
- If `W_opt <= theta`: **CERTIFIED_NO**. Proof: every model-B move that
  exists in some occupancy configuration is an edge of `R_opt`. If no
  water occupies a cell with a path to the monitor, none can arrive. The
  divider occupying `x = dx` for `y >= crest_y` is the usual cut: left
  water with `y >= crest_y` cannot go up to the gap.

This is the **trivial barrier / no-upward / reachability** baseline. It
already decides F1-flat, empty, and any puddle trapped below the crest.
It must not be sold as the new result.

It **does not** decide F1-tall, far columns, or a disconnected high shelf:
those occupy `R_opt` while still possibly never crossing.

## Why a tighter static NO is not just “gap-adjacent”

Development (not the scored panel) showed:

| arrangement | starts gap-adjacent? | Q |
|---|---|---|
| width-4 column, right edge at x=29 (2 cells from x=31) | no | **1** (first 31) |
| width-4 column, right edge at x=28 | no | 0 |
| width-2 column against the divider | yes | 0 |
| adj4 V=20 or 40 | yes | 0 |
| adj4 V>=60 | yes | 1 |
| one cell in the gap at y=1 | yes (in the gap) | **0** |
| one cell in the gap at y=20 | yes | **1** |

So “must start next to the gap” is **not necessary** for YES (2-cell
creep during collapse), and “is next to the gap / in the gap” is **not
sufficient** (skinny stacks slump; gap water may splash *left* on the
divider top).

The ablation `failed_gap_adjacent` certifies NO when no water currently
occupies `{dx-1, dx, dx+1}` at `y < crest_y` and `V` does not exceed the
left below-crest capacity. That rule is **unsound**. The scored panel
is required to exhibit at least one false NO for it (the near-2 column).

### Interaction that produces the 2-cell YES

`stepB` prefers falling. A packed column sitting on the floor is
processed bottom-to-top: the base splashes sideways, the cell above
then often *falls into the vacated cell* instead of walking. Most of
the lateral motion is therefore at the **floor**, below the crest, and
cannot climb. That is why a mid-box column of equal height does not spill.

Near the divider, a 4-wide packed body can keep a water floor under the
crest-height row long enough for **one or two** splash steps toward the
gap before the slump wins. That is new support created by occupancy, not
present as a wall-catwalk and not present as initial gap-adjacency.
A 2-cell halo “repair” of the failed candidate would only be an observed
margin on some columns, not a lemma: fill-overflow and wall ledges are
different mechanisms, and a 3-cell creep is not proved impossible.

### Interaction that produces gap_y1 = NO and gap_y20 = YES

Water in the gap falls until `x=dx, y=crest_y-1` (divider top). If it
fell this frame, it does not splash until a later frame (`if (fell)
relocate; continue`). Splash sign is `((frame + x) & 1)`. One arrival
phase goes right into the monitor; the opposite phase goes left into the
left pit and is then trapped below the crest. Starting height changes
the arrival frame. **Gap occupancy is not a forced YES.**

## Layer B — wall-supported catwalk plus sill-fill need

`R_catwalk`: same fall edges as `R_opt`, but lateral/down-diag edges
only from cells whose immediate below cell is **WALL** (a ledge). This
is the lasting support the code actually uses when no other water is
present.

If some water already occupies `R_catwalk` (monitor, divider-top landing,
or a wall shelf that walks into those), Layer B stays UNRESOLVED.

Otherwise a one-move fringe of `R_catwalk` can still be reached if water
**stacks** from an existing wall up to a cell that can splash into
`R_catwalk`. `sill_need` is the minimum number of non-wall cells in one
column from that fringe cell down to the next wall. If `V < sill_need`,
even a maximally stacked tower cannot occupy a fringe cell.

Then **CERTIFIED_NO**. Assumptions: no sand, no inflow, no upward move,
and stacking in a single column is the cheapest way to build new support
(so using it as a *lower bound on the mass required* is conservative).
Spreading, which the real updater prefers, only makes filling the sill
harder.

This is the **new static content**. It decides small isolated blobs and
high shelves whose wall path does not meet the gap, without a rollout.
It does **not** decide V=180 far/mid columns (`V >= sill_need`).

## Limited exact query (Layer C)

If A and B are UNRESOLVED, run the pinned `stepB` on the **full admitted
state**. After each frame, re-evaluate Layer A on the *current* field
(cheap BFS). Stop with:

- **CERTIFIED_YES** if monitor mass `> theta`
- **CERTIFIED_NO** if `W_opt <= theta` (all remaining water is now behind the
  geometric cut)
- else at t=H: **CERTIFIED_NO** because the receiver is a finite horizon
  (the bit is 0; this is exact for that H, not a physical “never”)

Incoming influence: this is not a spatial crop. Occupancy anywhere that
can become support for a crossing cell is admitted by evolving the whole
grid. Chunk sleeping already skips empty right-hand chunks after frame 1;
that is charged in `sumActive`, not claimed as a separate algorithm.

A spatial crop that deleted the left basin would be **unsound**: the basin
is the support that makes adjacent packed columns spill after they land.

## Where the bound still pays the horizon

If water remains on `R_opt` for all 300 frames without crossing — typical
disconnected ledge with `V >= sill_need` — Layer C cannot early-exit NO.
Optimistic `R_opt` still thinks the water might walk horizontally without a
floor. The missing lemma is: *a cell with empty-and-not-wall below will
fall this frame unless a same-row down-diagonal injects a new floor
before it is processed.* Proving that injection cannot extend arbitrarily
toward the gap is the remaining interaction. We do not fake that lemma.

## Failed attempt (kept)

`failed_gap_adjacent`: NO if not currently in the three-column gap band
and `V <=` left below-crest capacity. Refuted by a packed column whose
right edge is two cells from the divider: collapse creates the missing
floors. Official verdicts do not use it.

## What would look like a speedup and is not claimed

Certification-rate ratios are not runtime. “Would skip 70%” is not a
speed ratio. A runtime claim here requires executed `stepsRun` /
`sumActive` / wall time of candidate **including** certification and
fallback versus the matched yes-exit reference. Ties and losses are
reported as such.
