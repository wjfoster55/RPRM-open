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
7. [NULL-ALL.md](NULL-ALL.md) — IF-a frozen at `2069b6f`
8. [CLAIM-ALL.md](CLAIM-ALL.md) / [RESULT-ALL.md](RESULT-ALL.md) /
   [CENSUS-ALL.json](CENSUS-ALL.json)
9. [INVERSE-FIBER-NOTE.md](INVERSE-FIBER-NOTE.md) — standalone for tomorrow

On Bits2, XOR=1 is Count2⁻¹(1). That identification is `verify_id.py`
in the measurement worktree, not a new inverse census. This census
stays STOP.

Replay:

```powershell
python -I -B research/inverse-fiber-2026-09-17/verify_if.py
python -I -B research/inverse-fiber-2026-09-17/verify_joint.py
python -I -B research/inverse-fiber-2026-09-17/verify_view.py
python -I -B research/inverse-fiber-2026-09-17/verify_all.py
```

Does not import `rprm` or the other tonight trees.

**IF-k.** Complete joint preimages. Representative ≠ fiber. Stopped
search OPEN. Frozen NONE for sum 4 died as **ONE((2,2))**.

**IF-j.** XOR=1 is not `{0,1}×{0,1}`: extras are the XOR=0 fiber.
C=(0,0) and C=(1,1) each add six illegal triples. Complementary XOR
fibers share one product. AND=1 **does** equal `{1}×{1}`.

**IF-v.** Named menus: `FST,SND` on XOR=1; `X,Y,Z,PARITY,AND3` on
C=(0,0). AND/OR/EQ and already-supplied `C0` do not split.

**IF-a.** All 16 and all 256 Boolean extras. Split-to-ONE iff `D`
differs on the two members: **8 of 16** and **128 of 256**. Not the
linear duals of the fiber direction. 2-bit parity does not split
XOR=1. 8/8 names matched. Stop. No 4-bit lift.

Certified approximate families remain OPEN.
