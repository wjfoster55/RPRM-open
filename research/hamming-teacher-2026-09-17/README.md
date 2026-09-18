# Hamming / teacher 28/35 cut

17 September 2026. First-party next-paper cut, not BSD, not fluid, not O05.

Read in this order:

1. [NULL.md](NULL.md) — HT-28 nulls, frozen before that enumerator ran
2. [CLAIM.md](CLAIM.md) / [RESULT.md](RESULT.md) / [CENSUS.json](CENSUS.json)
3. [LEMMA.md](LEMMA.md) — injectivity-vs-line is immediate from rank; do not pad
4. [NULL-78.md](NULL-78.md) — HT-78 nulls, frozen before that enumerator ran
5. [CLAIM-78.md](CLAIM-78.md) / [RESULT-78.md](RESULT-78.md) / [CENSUS-78.json](CENSUS-78.json)

Replay:

```powershell
python -I -B research/hamming-teacher-2026-09-17/verify_ht28.py
python -I -B research/hamming-teacher-2026-09-17/verify_ht78.py
```

Does not import `research/liar-teacher-formalization-2026-09-12/verify_panels.py`.
Does not run the SAT pilot.

**HT-28:** Q1 is **ONE(28)**. “Any of those seven” is **NONE**. Failures
are the lines `{a,b,a⊕b}`. The iff with dependence is the rank lemma,
not a second census.

**HT-78:** seven-teacher words **ONE(8)** and dual to Hamming-7
**ONE(yes)**; Hamming-8 messages **ONE(16)**; free toggle 4→8 only for
`c ∉ U`. Collapsing those eights is **NONE**.
