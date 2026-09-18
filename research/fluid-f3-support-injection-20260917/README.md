# Fluid F3 — support-injection continuation

Continuation of Cursor Fluid F2 after the independent 2026-09-12 review.
Does not restart F1, does not restore Layer B, does not start BSD.

## Run

```
python -I -B tests/test_f3.py
```

Requires Python 3 and Node (pinned oracle). Frozen F2 bytes stay read-only
under `../fluid-f2-review-20260912/input/fluid_dynamic_frontier_02/`.

## Official static rule

1. Unit-normalize occupancy (same map as `normalizeForModel(B)`).
2. Layer A YES or NO decides.
3. Else if exactly one water cell is not on `R_catwalk`: CERTIFIED_NO.
4. Else UNRESOLVED → F3 cycle exact (`cycle_exit`), not F2 Layer B.

n≥2 has no cheap occupancy-ignoring cell-graph NO on this container.
Token-aware class T is budgeted, not static; see CLAIM.md F3-T / F3-T-LEDGE.
Class E cycle-exits the three horizon-pay ledges before H=300.

## Layout

| Path | Role |
|---|---|
| `CLAIM.md` | Typed claims, grades, hostile case |
| `NULLS.md` | Frozen token-aware / cycle hypotheses |
| `DERIVATION.md` | Isolation argument + V≥2 dichotomy + T/E |
| `src/bound_f3.py` | Official routing + soup audits |
| `src/token_aware.py` | Class T occupancy-count search |
| `src/oracle_cycle.js` | Class E cycle exact (pinned JS unchanged) |
| `src/oracle_driver.py` | Frozen `oracle.js` plus `cycle_exit` |
| `tests/test_f3.py` | Exact checks |
| `RETURN_TO_WILLIAM.md` | Short return |
