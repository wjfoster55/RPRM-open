# Finite-budget observability / sensor selection

17 September 2026. Independent-math Rank 2, not BSD, not fluid, not
Hamming, not n=4 obstruction padding.

Read in this order:

1. [NULL.md](NULL.md) — OB-k nulls, frozen before the enumerator ran
   (commit `e758dd3`)
2. [CLAIM.md](CLAIM.md) / [RESULT.md](RESULT.md) / [CENSUS.json](CENSUS.json)

Replay:

```powershell
python -I -B research/observability-budget-2026-09-17/verify_ob.py
```

Does not import `rprm`, AD-R3 code, or the obstruction/fluid/Hamming trees.

**Q1.** Budget-1 panels for `Q=h` are **ONE(`{H}`)**.

**Q2.** Hostile extra sensors `{R,R2,Z}` are **NONE**. Both `r`-fibers
still split `h` (**MANY(2)** ghost pairs). “More sensors help” is
`N_more_helps`, rejected.

**Q3.** Extra tick-time with only `R` is **NONE** (`N_layer`).

**Q4.** Budget-2 panels are **MANY(6)**. `{R,X}` completes; `{R,R2}`
does not.

**Q5.** Keep port `{R}` and admit `reveal`: **ONE(yes)**. The
intervention family changed; the sensor count did not.

Adjacent written source: `docs/relational-layer.md` four-state example.
AD-R3 remains the linear row-space ancestry, not this census.
