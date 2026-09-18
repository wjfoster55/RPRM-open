# Hamming / teacher 28/35 cut

17 September 2026. First-party next-paper cut, not BSD, not fluid, not O05.

Read in this order:

1. [NULL.md](NULL.md) — HT-28 nulls, frozen before that enumerator ran
2. [CLAIM.md](CLAIM.md) / [RESULT.md](RESULT.md) / [CENSUS.json](CENSUS.json)
3. [LEMMA.md](LEMMA.md) — injectivity-vs-line is immediate from rank; do not pad
4. [NULL-78.md](NULL-78.md) — HT-78 nulls, frozen before that enumerator ran
5. [CLAIM-78.md](CLAIM-78.md) — HT-78 task record; result files after the enumerator

Replay (HT-28 now; HT-78 after its census commit):

```powershell
python -I -B research/hamming-teacher-2026-09-17/verify_ht28.py
```

Does not import `research/liar-teacher-formalization-2026-09-12/verify_panels.py`.
Does not run the SAT pilot.

**HT-28:** Q1 is **ONE(28)**. The historical “any of those seven” null is
**NONE**. The seven failures are the Hamming lines `{a,b,a⊕b}`.
The iff with linear dependence is the rank lemma, not a second census.
