# Inverse design with complete ambiguity families

17 September 2026. Independent-math Rank 7. Not BSD, not fluid, not
Hamming, not O05, not observability, not Markov padding. Not a physics
law.

Read in this order:

1. [NULL.md](NULL.md) — IF-k frozen before the enumerator (`3127680`)
2. [CLAIM.md](CLAIM.md) / [RESULT.md](RESULT.md) / [CENSUS.json](CENSUS.json)
3. [NULL-JOINT.md](NULL-JOINT.md) — IF-j frozen at `bd28533`
4. [CLAIM-JOINT.md](CLAIM-JOINT.md) / [RESULT-JOINT.md](RESULT-JOINT.md) /
   [CENSUS-JOINT.json](CENSUS-JOINT.json)
5. [NULL-VIEW.md](NULL-VIEW.md) — IF-v frozen at `14c5b8a`
6. [CLAIM-VIEW.md](CLAIM-VIEW.md) / [RESULT-VIEW.md](RESULT-VIEW.md) /
   [CENSUS-VIEW.json](CENSUS-VIEW.json)
7. [INVERSE-FIBER-NOTE.md](INVERSE-FIBER-NOTE.md) — standalone for tomorrow

Replay:

```powershell
python -I -B research/inverse-fiber-2026-09-17/verify_if.py
python -I -B research/inverse-fiber-2026-09-17/verify_joint.py
python -I -B research/inverse-fiber-2026-09-17/verify_view.py
```

Does not import `rprm` or the other tonight trees.

**IF-k.** Complete joint preimages. Representative ≠ fiber. Stopped
search OPEN. Frozen NONE for sum 4 died as **ONE((2,2))**.

**IF-j.** XOR=1 is not `{0,1}×{0,1}`: extras are the XOR=0 fiber.
C=(0,0) and C=(1,1) each add six illegal triples. Complementary XOR
fibers share one product. AND=1 **does** equal `{1}×{1}`. All eight
names matched.

**IF-v.** On XOR=1, exactly `FST` and `SND` split to ONE; AND/OR/EQ
do not. `FST=0` leaves **ONE((0,1))**. On C=(0,0), exactly
`X,Y,Z,PARITY,AND3` split to ONE; already-supplied `C0` does not.
`X=0` leaves **ONE((0,0,0))**. All eight names matched.

Certified approximate families and a min-view search over all Boolean
functions remain OPEN. Discrete census on these menus stops here.
