# Hamming / teacher 28/35 cut

17 September 2026. First-party next-paper cut, not BSD, not fluid, not O05.

Read in this order:

1. [NULL.md](NULL.md) — named nulls, frozen before the enumerator ran
2. [CLAIM.md](CLAIM.md) — carrier, ports, receiver, hostile case
3. [RESULT.md](RESULT.md) — written after `CENSUS.json` exists
4. [CENSUS.json](CENSUS.json) — exact receipt

Replay:

```powershell
python -I -B research/hamming-teacher-2026-09-17/verify_ht28.py
```

Does not import `research/liar-teacher-formalization-2026-09-12/verify_panels.py`.
Does not run the SAT pilot.

**Result:** Q1 is **ONE(28)**. The historical “any of those seven” null is
**NONE**. The seven failures are the Hamming lines `{a,b,a⊕b}`.
