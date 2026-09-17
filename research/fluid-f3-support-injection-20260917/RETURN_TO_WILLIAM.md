# Return to William — F3 unit isolation

F1 stays closed. Layer B stays refuted. No paper.

## What continued

The live fluid thread was F2 dynamic-breach prediction, not a separate
"fluent" project. "Fluent" did not name an artifact; it reads as the fluid
adjacency / F2 lane.

F3 takes the review's required correction and adds one sound static NO:

- Do not accept B-only `V < sill_need` NO.
- If after unit normalization there is exactly one water cell, and that
  cell is not on the wall-supported catwalk `R_catwalk`, the breach bit is 0.
- Otherwise use Layer A and limited exact, as before.

The two-cell ledge scene still breaches at frame 3. F3 leaves it UNRESOLVED
and lets the pinned oracle say YES. That counterexample is kept beside the
surviving certificates.

## One success

Frozen panel `E_adjcell_y1` and `E_adjcell_y35`: unique gap-adjacent drips,
not on `R_catwalk`. F3 certifies NO with no rollout. Oracle Q=0.

Same rule also certifies a single cell on the isolated D-shelf geometry.

## One non-success (preserved)

`D_shelf_isolated` (nine cells) was a Layer B static NO. Isolation does not
apply at n=9. Official F3 is UNRESOLVED; limited exact still returns Q=0.
That is coverage loss, not a restored theorem.

## Still OPEN

A static NO for two or more cells that survives support injection. Finite
two-cell probes (`results/two_cell_travel.json`):

- Hostile pair beside a two-cell ledge: Q=1 at frame 3.
- Same pair with no extra ledge: Q=0 (they fall into the left basin).
- Two cells on a far isolated shelf: Q=0.
- Two cells at the tip of a crest-height ledge ending at x=30 or x=28: Q=0.

Injection can breach, but not from every two-cell placement. That is a
five-row family, not a V=2 theorem.

## Replay

```
python -I -B tests/test_f3.py
```
