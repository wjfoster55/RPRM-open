# Receiver-specific Markov-state coarse graining

17 September 2026. Independent-math Rank 3, smallest typed cut. Not BSD,
not fluid, not Hamming, not O05, not observability-budget padding.

Read in this order:

1. [NULL.md](NULL.md) — frozen before the enumerator (commit `f191077`)
2. [CLAIM.md](CLAIM.md) / [RESULT.md](RESULT.md) / [CENSUS.json](CENSUS.json)
3. [MARKOV-LUMPING-NOTE.md](MARKOV-LUMPING-NOTE.md) — standalone for tomorrow

Replay:

```powershell
python -I -B research/markov-lumping-2026-09-17/verify_ml.py
```

Does not import `rprm` or the other tonight trees.

**Q1.** FairTwo merge, constant `Q`: **ONE(yes)**.

**Q2.** Same merge, identity `Q`: **NONE**. Lumpable is not enough.

**Q3–Q4.** AbsorbingTwo merge, constant `Q`: **NONE** on named port
`enter_L` (`1/2` vs `0`). One-block lumpability is vacuous; the frozen
mass-reason is corrected in RESULT.

**Q5.** ManifestoFour-P, `C_AB`, `Q_color`: **ONE(yes)**.

**Q6 / Q8.** `C_AB` with `Q_split`, and `C_diag` with `Q_color`: **NONE**.
Both partitions are lumpable on `P`; `Q` is not constant.

**Q7 / Q9.** `C_fine` on `P`, and `C_AB` on Ptilde: **NONE**. `Q_color`
is constant; block masses are not.

**Q11–Q12.** Skew three-state: `enter_B` enabledness **ONE(yes)**;
operational **NONE**. Equal supports are not equal laws.

Adjacent written source: Manifesto IV.1.2 and handbook §11. Not a new
physics law. Discrete census stops here.
