# Inverse design with complete ambiguity families

17 September 2026. Independent-math Rank 7, smallest typed cut. Not BSD,
not fluid, not Hamming, not O05, not observability, not Markov padding.

Read in this order:

1. [NULL.md](NULL.md) — frozen before the enumerator (commit `3127680`)
2. [CLAIM.md](CLAIM.md) / [RESULT.md](RESULT.md) / [CENSUS.json](CENSUS.json)
3. [INVERSE-FIBER-NOTE.md](INVERSE-FIBER-NOTE.md) — standalone for tomorrow

Replay:

```powershell
python -I -B research/inverse-fiber-2026-09-17/verify_if.py
```

Does not import `rprm` or the other tonight trees.

**Q1.** AND=1: **ONE((1,1))**.

**Q2.** AND=0: **MANY((0,0),(0,1),(1,0))**. A representative is not a
fiber.

**Q3.** XOR=1: **MANY((0,1),(1,0))**. Order is load-bearing.

**Q4.** NAND=0: **ONE((1,1))**.

**Q5.** CONST0=1: **NONE**.

**Q6.** AND=0 product of marginals: **NONE** of equality.

**Q7–Q8.** 3-to-2 readout `C(x,y,z)=(x⊕y,x⊕z)`: **MANY(2)** at `(0,0)`
and at `(1,1)`.

**Q9.** Stopped AND=0 scan: **OPEN**, not `MANY` of the found pair.

**Q10.** Add3, `c=2`: **MANY((0,2),(1,1),(2,0))**.

**Q11.** Frozen NONE for sum 4 **died**: complete fiber **ONE((2,2))**.

**Q12.** XOR=0: **MANY((0,0),(1,1))**.

Adjacent written source: handbook §3; README `a+b=c` table; core.md §5.
Not a new physics law. Discrete census stops here.
