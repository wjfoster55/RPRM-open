# DERIVATION — unit isolation

F2 asked whether a cell with non-wall empty below always falls this frame
unless a same-row already-processed neighbour injects a floor
(`RETURN_TO_WILLIAM.md`, single remaining question). The F2 review answered
the second clause with a counterexample: injection happens, and it already
false-NOs Layer B. This note answers a narrower, proved restriction of the
first clause: when there is **no** other water occurrence, injection is
impossible, so actual motion lies on the wall-supported catwalk graph.

Frozen F2 files are not edited. Layer B's stack lower bound stays refuted.

## Unit occupancy

Pinned `normalizeForModel(B)` sets every WATER cell's mass to `C.MaxMass = 1`
and zeroes `vx`, `vy` before frame 0. F3 applies the same map to raw mass
before any certificate: each non-wall cell with mass `> 0` becomes occupancy
1. Fractional raw mass is not a second carrier; it is admitted only through
this map. That removes the F2 static/oracle normalization split on
`C_right_one` with raw mass 0.25.

Water-cell count `n` is the integer number of occupied cells after that map.

## Layer A (reused, not re-litigated)

`R_opt` is reverse reachability on occupancy-ignoring model-B moves: fall
1..6, down-diagonal, horizontal; never up; walls block. Every actual `stepB`
move is one of those edges. If no unit mass remains on `R_opt`, none can
arrive at the monitor. If monitor mass `> 0.5` now, YES. Proof and panel
replay: F2 `DERIVATION.md` and `REVIEW.md`. F3 evaluates A on unit-normalized
occupancy.

## Unique cell: actual moves are catwalk moves

Assume `n = 1`. Let `w` be the unique water occurrence.

Pinned `stepB`:

1. If `isEmpty` immediately below, the cell falls (at least one cell; up to
   `max(1, round(vy))`, stopping at the first non-empty). A cell that falls
   does not splash this frame.
2. If it cannot fall, it splashes into empty down-diagonal or horizontal
   neighbours.
3. `isEmpty(x,y)` is true only for an in-bounds EMPTY cell.
4. Sand is excluded. The only other occupancy would be another WATER cell.

Therefore, with `n = 1`, "cannot fall" means the cell immediately below is a
WALL (or out of bounds, treated as blocked). Splash therefore occurs only from
a wall-supported cell. Fall occurs only through EMPTY cells. Those are exactly
`forward_moves_catwalk` in frozen `bound.py`.

Scan order, stamp, and cascade do not create a second occurrence. They cannot
inject a floor under `w`.

Hence every reachable location of `w` lies in the forward catwalk closure of
its start cell. `R_catwalk` is the reverse reachable set of the monitor on
that graph. If the start cell is not in `R_catwalk`, the monitor is never
occupied, so `Q_H = 0` for the declared H (and for any larger horizon on this
updater).

This certificate never says YES. Occupying `R_catwalk` does not force a
breach: splash sign `((frame + x) & 1)` and "fell this frame ⇒ no splash"
can send the unique cell into the left pit. Those scenes stay UNRESOLVED
and use limited exact. Frozen examples: `C_gap_y1` (Q=0) and `C_gap_y20`
(Q=1).

## Why this does not restore Layer B

Layer B certified NO whenever `n ≥ 1`, no water occupied `R_catwalk`, and
`V < sill_need`, treating a full column as a lower bound on the mass needed
to create support. The hostile scene has `n = 2`, `V = 2`, `sill_need = 12`,
and Q=1 at frame 3 because one occurrence moves diagonally into a supporting
cell before the other is processed. Stamping prevents a double move of one
occurrence; it does not prevent the moved occurrence from supporting the
next. The stack lemma is false. F3 isolation applies only at `n = 1`.

The five original B-only panel successes included `D_shelf_isolated` (V=9),
`E_blob9_far` (V=9), `E_stack10_adj` (V=10), and two genuine V=1 drips.
F3 keeps the two V=1 NOs and returns the multi-cell rows to UNRESOLVED plus
limited exact. Their Q=0 observations remain; they are not a general V≥2
certificate.

## Why V≥2 has no cheap static NO

A cheap certificate here means a cell-graph over-approximation: cells, not
n-tuples of simultaneous occurrences. Two natural graphs were checked.

**Full soup.** Close catwalk travel under wall-supported injection *and*
water-as-floor (one soup cell standing on another). Token count is ignored,
so two start cells generate the same stacking laterals as an unbounded
column. On the admitted 64×48 divider container this soup meets `R_catwalk`
for every frozen-panel scene with n≥2 and Layer A UNRESOLVED, and for the
hostile pair, the midair pair, and the far-shelf pair. It is sound as a
“might reach” test and therefore never yields CERTIFIED_NO. It is not a
useful V≥2 bound.

**Wall-only soup.** Same closure, but the injector must be wall-supported.
The hostile pair still meets `R_catwalk` (distinguishing case stays
UNRESOLVED). Isolated shelves miss `R_catwalk` and would look like NOs.
Packed-column YES scenes miss it too: `A_w4_x26_V180` and `C_adj4_V60`
have oracle Q=1, first breaches 31 and 15, and wall-only `meets=false`.
Using that graph as CERTIFIED_NO is a false NO. Packed-column creep is
water-as-floor, which this graph refuses to admit.

Those two graphs exhaust the cheap occupancy-ignoring options that stay
inside F2’s move set. Including water floors makes the soup too large to
NO; excluding them makes it too small to be sound on the YES columns that
already refute “gap-adjacent” and that Layer B never decided.

Class T below tracks the actual token count as an occupancy over-approx
(not exact `stepB`). Exhaustion can NO isolated n=2 probes; it does not
cheaply decide the n=15/25 horizon-pay ledges. Class E is limited exact
with a token-state cycle stop.

Therefore official F3 *static* routing after A and isolation uses the
1-high rule below, then UNRESOLVED. The hostile extra-walls/water pair
stays outside that domain (UNRESOLVED-then-exact-YES).

## Cheap carry is empty; 1-high carry is a theorem

Nulls: `NULLS_CARRY.md`, frozen before these checks.

**Cheap class.** Scan-order-ignoring over-approx (cell graphs or n-token
occupancy, fall/splash shapes only). Packed-column YES
(`A_w4_x26_V180`, `C_adj4_V60`) uses water-as-floor: wall-only soup
misses `R_catwalk` while the oracle is Q=1, so any cheap rule that
forbids water floors is a false NO. Any cheap rule that *allows* water
floors contains the T graph (or full soup). Complete T already MEETS
`R_catwalk` on `D_ledge_end28/30` and `D_sill_end25`, so that class
cannot NO those rows. The hostile pair also MEETS. There is therefore
no cheap static injection-carry lemma that is sound, useful on the
horizon-pay ledges, and not a false NO on the hostile pair.

**Restricted 1-high.** Assume every water cell is wall-supported, and
let `Cat(S)` be the catwalk forward closure of the occupied set. If
`Cat(S)` meets `R_catwalk`, stop (UNRESOLVED): a wall-supported splash
into the gap is already a catwalk edge (`D_ledge_end31`, `D_sill_end31`,
`D_ledge_to_gap`).

If `Cat(S)` misses `R_catwalk`, then `Q_H = 0`.

Proof. Splash from a wall-supported cell is a catwalk edge, so no
wall-supported cell can splash directly into `R_catwalk`. A token
leaves the wall only into the one-move fringe. That fringe cell is not
in `R_catwalk` (else `Cat(S)` would meet). From a midair fringe cell,
`stepB` falls if the cell below is empty and does not splash that
frame. Fall dests are catwalk edges, hence also miss `R_catwalk`.

A partner can use a newly planted midair floor in the *same* frame
(bottom-to-top: the planter moves first from the wall row; a later
same-row cell can splash onto or beside that floor). Stamp then blocks
a second move. The next frame processes the lower midair floor first;
it falls; the cell above now has empty below and falls. Midair
water-as-floor does not persist. Chaining a second air column while
staying high would need that second splash after the floor is gone, or
a double move in one frame, both forbidden.

Packed columns and the original hostile pair have a cell that is not
wall-supported, so they are outside the domain. Hostile YES uses
same-frame injection from a *non*-1-high start already adjacent to the
gap; the 1-high miss hypothesis does not apply.

This is not `sill_need` and not occupancy-ignoring soup. It NOs the
three horizon-pay ledges and `D_shelf_isolated`.

## Token-aware occupancy (class T)

Nulls were frozen in `NULLS.md` before this search.

State: exactly `n` occupied cells. One token relocates per edge along an
occupancy-respecting model-B move (fall if empty below; else splash).
Frame, velocity, stamp, and scan order are ignored, so the graph
over-approximates `stepB`. CERTIFIED_NO only if the graph is exhausted
inside `MAX_STATES=50000` with no intersection with `R_catwalk`. A meet,
a cap hit, or `n>32` is UNRESOLVED. Never YES.

- Hostile pair: meets `R_catwalk` (T-H1). Not a false NO.
- `D_ledge_end31`: already on `R_catwalk` at t=0 (T-H5).
- Isolated n=2 shelf and midair: exhaust, T-NO (T-H4, extra midair).
- Packed YES `A_w4_x26_V180`, `C_adj4_V60`: `n>MAX_N`, skipped (T-H3).
- Horizon-pay `D_ledge_end28/30`, `D_sill_end25`: 50000 expansions, no
  meet, not exhausted (T-H2). A **complete** T search **MEETS**:
  constructive occupancy-count paths of length 48/24/49 into the gap
  column, replayed on the T graph (`NULLS_COMPLETE_T.md` T-C1–C3).
  The 50k cap missed those paths because it wandered the ledge
  rearrangements. T is therefore too coarse to NO these rows (same
  usefulness failure as full soup, with token count enforced). Actual
  `stepB` still has Q=0; the T path uses scan-order/phase freedom that
  the updater does not grant.

Official static routing does not use T. This is not `sill_need`.

## Token-state cycle exact (class E)

Same pinned `stepB` bytes, F3 driver. After each frame hash occupancy,
milli-quantized `vx,vy`, frame parity, and `dirtyNext`. Stop on monitor
YES, Layer-A empty, exact token-state repeat, or `t=H`. A repeat with no
prior breach is `Q=0` for this updater.

On the three horizon-pay rows this is cheaper than paying H=300:

| scene | stepsRun | stop | Q |
|---|---|---|---|
| `D_ledge_end28` | 111 | occ_cycle | 0 |
| `D_ledge_end30` | 99 | occ_cycle | 0 |
| `D_sill_end25` | 52 | occ_cycle | 0 |

Hostile YES at frame 3; `D_ledge_end31` and `A_w4_x26_V180` YES before
any cycle. E is the official F3 *continuation* after A+isolation, not a
static certificate.

## Failed candidates kept

- F2 `failed_gap_adjacent` — unsound (F2 panel false NOs). Not used.
- F2 Layer B `V < sill_need` — refuted by the two-cell scene. Not used.
- F3 full injection soup — sound, never NOs on this container. Not official.
- F3 wall-only injection soup — useful on shelves, false-NO on packed YES.
  Not official.
- F3 class T on n=15/25 horizon-pay ledges — 50000-state search hits
  the cap; complete T MEETS `R_catwalk`. Not a cheap or complete NO
  on those rows.
