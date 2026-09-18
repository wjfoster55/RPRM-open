# Measurement contracts, in one sitting

17 September 2026. Standalone note for tomorrow. Not BSD. Not a
laboratory calibration. Not a physical law.

Branch `research/measurement-contract-2026-09-17` in worktree
`C:\github\RPRM-open-measurement-contract`. Replay:

```powershell
python -I -B research/measurement-contract-2026-09-17/verify_mc.py
```

Nulls were frozen at `0256331` before the enumerator. Evidence grade is
Manifesto II.2 factorization plus an exact census of Bits2 under the
named instruments Count2, Mean2, and FourState. Lean was not run. The
independent-math Rank 8 prompt was measurement-contract auditing. This
cut is the smallest toy contract, not a paper scrape and not Rank-8's
workflow standard.

---

## 1. What is being asked

A published or toy measurement claims a quantity `Q` from ports. Audit:

1. Is `Q` constant on each representation fiber?
2. Were missing ports treated as independent (product of marginals)?
3. Were enabledness, units, and receiver stated?

Identified means a decoder `h` exists with `Q = h ∘ C`. It does not
mean the display numeral equals `Q`, and it does not mean the source
pair is recovered.

---

## 2. Named instruments

**Count2.** Manifesto III.7 count of a length-2 binary block:
`C_sum(a,b)=a+b`. Unit: bit-count. Enabled iff both ports are supplied.

**Mean2.** Density: `C_mean=(a+b)/2` as `Fraction`. Same fibers as
count. Occupancy of `[0,1]` is not a probability law.

**FourState.** Manifesto III.7.2: `C4=a+2b`, inverse `a=z mod 2`,
`b=floor(z/2)`.

---

## 3. What the census did

| Cut | Result |
|---|---|
| XOR on Count2 | **ONE(yes)** — `h(0)=0`, `h(1)=1`, `h(2)=0` |
| Mean2 numeral equals XOR | **NONE** — `(1,1)` is mean `1`, XOR `0` |
| PAIR at count `1` | **MANY((0,1),(1,0))** |
| Count-1 vs product of bit-marginals | **NONE** — product adds `(0,0)` and `(1,1)` |
| FST on Count2 | **NONE** — count `1` splits the first bit |
| FourState codes `1` and `2` | **ONE((1,0))** and **ONE((0,1))** |
| PAIR at count `0` | **ONE((0,0))** |
| Count2/Mean2 same kernel | **ONE(yes)** |
| Mean2 sure Bernoulli of XOR | **NONE** — image `{0, 1/2, 1}` |
| Mean2 with only `a=1` | **DISABLED** |
| Count2 is a CAR | **NONE** — count `1` is MANY |

Hostile: Count2 looks identified (three singleton codes) and the pair
fiber at count `1` is still MANY. Independent bits reconstruct the
wrong pairs. The slogan “sample mean of two bits estimates XOR” fails
as a numeral and succeeds as a nonlinear decoder.

---

## 4. Stop

No paper scrape. No BRCA1. No inverse-fiber 4-bit lift. Rank-8
machine-readable provenance/units interchange remains OPEN and is not
this cut.
