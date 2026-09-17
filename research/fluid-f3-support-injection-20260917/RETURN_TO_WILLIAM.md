# Return to William — F3 V≥2 freeze

F1 stays closed. Layer B stays refuted. No paper.

## Theorem on a stated domain

**Carrier:** pinned model B, unit occupancy, static walls, no sand/inflow,
F2 64×48 divider container (and the 96×64 scale pair).  
**Cheap certificate class:** occupancy-ignoring cell graphs using catwalk
moves plus same-frame injection, with or without water-as-floor, ignoring
how many tokens actually exist.

On that class there is **no** static NO for n≥2 that is both sound on
packed-column YES and useful on isolated Q=0 scenes while leaving the
original hostile pair uncertified-NO.

- Full soup (water floors on) meets `R_catwalk` on every n≥2 A-unresolved
  frozen-panel row and on the hostile / midair / shelf two-cell probes.
  Never CERTIFIED_NO.
- Wall-only soup leaves the hostile pair UNRESOLVED, but false-NOs
  `A_w4_x26_V180` and `C_adj4_V60` (oracle Q=1).

Official F3 rule: Layer A, then isolation NO at n=1, else UNRESOLVED and
limited exact. Isolation is still the only new static NO.

## Distinguishing case

Extra walls `(29,36),(30,36)`, water `(30,34),(31,34)`: Layer B still says
NO; F3 stays UNRESOLVED; oracle YES at frame 3.

## Replay

```
python -I -B tests/test_f3.py
```
