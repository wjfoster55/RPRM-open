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

## Remaining question (still OPEN)

Can two or more cells walk toward a gap by repeated same-row injection
without a wall catwalk, and can that travel be bounded before height is
lost? The hostile scene shows that injection can create a one-cell bridge
into the divider gap in three frames. A general V≥2 static NO is therefore
a new proof obligation, not a corollary of isolation. Finite two-cell
probes are recorded in `results/two_cell_travel.json` when tests run; they
do not close F3-V2.

## Failed candidates kept

- F2 `failed_gap_adjacent` — unsound (F2 panel false NOs). Not used.
- F2 Layer B `V < sill_need` — refuted by the two-cell scene. Not used.
