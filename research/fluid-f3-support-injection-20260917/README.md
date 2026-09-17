# Fluid F3 — support-injection continuation

Continuation of Cursor Fluid F2 after the independent 2026-09-12 review.
Does not restart F1, does not restore Layer B, does not start BSD.

## Run

```
python -I -B tests/test_f3.py
```

Requires Python 3 and Node (pinned oracle). Frozen F2 bytes stay read-only
under `../fluid-f2-review-20260912/input/fluid_dynamic_frontier_02/`.

## Layout

| Path | Role |
|---|---|
| `CLAIM.md` | Typed claims, grades, hostile case |
| `DERIVATION.md` | Unit-isolation argument |
| `src/bound_f3.py` | Official static routing: A + isolation, never B sill_need |
| `src/oracle_driver.py` | Frozen `oracle.js` wrapper |
| `tests/test_f3.py` | Exact checks |
| `RETURN_TO_WILLIAM.md` | Short return |

## Official static rule

1. Unit-normalize occupancy (same map as `normalizeForModel(B)`).
2. Layer A YES or NO decides.
3. Else if exactly one water cell is not on `R_catwalk`: CERTIFIED_NO.
4. Else UNRESOLVED → existing limited exact (`cut_exit`).

## Inventory pointer

Cloud / local fluid-adjacency threads this continues:

- Cloud `bc-3b46431e-0f52-5e44-8779-6de70c8fcd52` — F2 crest-cut / dynamic breach
- Cloud `bc-602dc8d4-8dc8-48e5-b10a-60bde3892054` — noita_lab from-scratch (PR6–13)
- Local `C:\Users\bkbee\rprm-fluid-adjacency` — transport PR1–4
- Review authority: `research/fluid-f2-review-20260912/REVIEW.md`
