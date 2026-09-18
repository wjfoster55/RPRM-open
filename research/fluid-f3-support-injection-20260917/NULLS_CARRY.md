# Frozen nulls — static injection-carry lemma (2026-09-17)

Written **before** the 1-high / cheap-class carry checks below. Do not
edit hypotheses after looking. Outcomes go in `CLAIM.md` and `results/`.

Layer B stays refuted. Not BSD. Hostile pair must not become a false NO.
Packed-column YES (`A_w4_x26_V180`, `C_adj4_V60`) is the soundness
hostile for “must allow water-as-floor.”

## Cheap class (scan-order ignored)

Static rules that over-approximate `stepB` by cells or n-token
occupancy, using fall/splash shapes, **without** scan order, stamp, or
“fell this frame ⇒ no splash.”

## Restricted class (1-high)

Domain: after unit normalize, **every** water cell is wall-supported
(WALL immediately below). Outside: packed columns, stacks, midair
pairs, the original hostile pair.

Rule: if the catwalk forward closure of the occupied cells misses
`R_catwalk`, CERTIFIED_NO. Coverage boundary: 1-high Q=1 rows whose
wall walk already meets `R_catwalk` stay UNRESOLVED.

## Hypotheses (frozen)

| ID | Hypothesis | Falsified if |
|---|---|---|
| C-H1 | No cheap (scan-order-ignoring) carry lemma is sound on packed-column YES, useful as NO on `D_ledge_end28/30` and `D_sill_end25`, and not a false NO on the hostile pair. | An exhibited cheap rule does all three. |
| C-H2 | Restricted 1-high: all wall-supported and `Cat(S) ∩ R_catwalk = ∅` implies `Q_H = 0`. | Any 1-high panel/probe with Cat-miss and oracle Q=1, or a false NO on hostile/packed YES (those must stay outside the domain). |
| C-H3 | 1-high Q=1 rows `D_ledge_end31`, `D_sill_end31`, `D_ledge_to_gap` have `Cat(S)` meeting `R_catwalk` (hypothesis of C-H2 fails; not a false NO). | Cat-miss on any of those Q=1 rows. |
