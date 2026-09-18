# Return to William — F3 token-aware cut

F1 stays closed. Layer B stays refuted. No paper. Isolation is still the
only new *static* NO.

Token-aware occupancy counts (class T, budget 50000 configs) give a
cheap NO on isolated two-cell shelf/midair probes and do **not** give a
cheap NO on `D_ledge_end28/30` or `D_sill_end25` (cap hit, hostile pair
still not T-NO). Cycle exact (class E) stops those three ledges at 111,
99, and 52 frames with Q=0, cheaper than paying H=300; hostile YES at
frame 3.

OPEN: whether a complete T search on the n=15/25 ledges would meet
`R_catwalk` or exhaust; packed-column YES still needs exact; no static
injection-carry lemma.

## Replay

```
python -I -B tests/test_f3.py
```
