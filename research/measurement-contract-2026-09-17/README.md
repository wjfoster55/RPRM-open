# Scientific measurement-contract auditing

17 September 2026. Independent-math Rank 8, smallest typed toy cut.
Not BSD, not fluid, not Hamming, not O05, not observability, not
Markov, not inverse-fiber 4-bit padding. Not a physics law.

Read in this order:

1. [NULL.md](NULL.md) — frozen before the enumerator (commit `0256331`)
2. [CLAIM.md](CLAIM.md) / [RESULT.md](RESULT.md) / [CENSUS.json](CENSUS.json)
3. [MEASUREMENT-CONTRACT-NOTE.md](MEASUREMENT-CONTRACT-NOTE.md) — standalone for tomorrow

Replay:

```powershell
python -I -B research/measurement-contract-2026-09-17/verify_mc.py
```

Does not import `rprm` or the other tonight trees.

**Q1.** XOR is constant on Count2 fibers: **ONE(yes)**. Decoder
`h(0)=0`, `h(1)=1`, `h(2)=0`.

**Q2.** Mean2 numeral equals XOR: **NONE**. Sample mean of two bits
does not estimate XOR as a number.

**Q3–Q4.** Count `1` is **MANY((0,1),(1,0))**; the product of
bit-marginals is all four pairs.

**Q5.** First bit is not constant on Count2.

**Q6–Q7.** FourState codes `1` and `2` are **ONE((1,0))** and
**ONE((0,1))**.

**Q8.** Count `0` is **ONE((0,0))**.

**Q9–Q10.** Count2 and Mean2 share a kernel. Mean2 is not a sure
Bernoulli of XOR (`1/2` is in the image).

**Q11.** Missing port `b`: **DISABLED**, not a one-sample mean.

**Q12.** Count2 is not a CAR. The contract that looks identified has
fiber **MANY** at count `1`.

Adjacent written source: Manifesto III.7 count/density and Proposition
III.7.2. Discrete census stops here.
