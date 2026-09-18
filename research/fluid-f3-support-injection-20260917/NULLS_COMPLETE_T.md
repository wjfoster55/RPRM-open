# Frozen nulls — complete T on horizon-pay ledges (2026-09-17)

Written **before** the complete / constructive T search on
`D_ledge_end28`, `D_ledge_end30`, `D_sill_end25`. Do not edit
hypotheses after looking. Outcomes go in `CLAIM.md` and `results/`.

Previous cut (`NULLS.md`) stays: 50000-state T is not a cheap NO on
these rows. This cut asks the leftover fiber: if T is run to
**completion** (a witness in the same occupancy-count graph, or
exhaustion of that graph), does it MEET `R_catwalk` or EXHAUST?

Layer B stays refuted. Official static stays Layer A + n=1 isolation.
Not BSD. Hostile pair must not become a T-NO.

## Class T (unchanged)

Exactly `n` occupied cells. One token relocates along an
occupancy-respecting model-B move. Frame / `vx` / `vy` / stamp
ignored. MEETS iff some reachable occupancy intersects `R_catwalk`.
EXHAUSTS iff the reachable set is finite-enumerated with empty
intersection. A constructive legal T-path is enough for MEETS; it
answers what a complete search would find.

## Hypotheses (frozen)

| ID | Hypothesis | Falsified if |
|---|---|---|
| T-C1 | Complete T on `D_ledge_end28` MEETS `R_catwalk`. | Exhausts with no meet, or cannot finish. |
| T-C2 | Complete T on `D_ledge_end30` MEETS `R_catwalk`. | Exhausts with no meet, or cannot finish. |
| T-C3 | Complete T on `D_sill_end25` MEETS `R_catwalk`. | Exhausts with no meet, or cannot finish. |
| T-C4 | Hostile pair still MEETS (not a T-NO). | T exhausts with no meet on the hostile scene. |

Packed-column YES stays OPEN (no cheap lemma claimed).
