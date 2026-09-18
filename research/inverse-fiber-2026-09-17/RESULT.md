# IF-k result

Written after `CENSUS.json`. Nulls were frozen in [NULL.md](NULL.md) at
commit `3127680`. Replay:

```powershell
python -I -B research/inverse-fiber-2026-09-17/verify_if.py
```

Evidence grade: **finite exhaustive check** of Bits2 (4 ordered pairs),
Bits3 (8 ordered triples), and Add3 (`{0,1,2}`²). Exact integer
arithmetic. Not Lean. Not inverse graphics. Not a physics law. Eleven
frozen surviving names matched. Q11's frozen `N_add4_none` died.

## Dispositions

| Question | Frozen surviving-null | Result |
|---|---|---|
| Q1. AND⁻¹(1) | `N_and1_one` | **ONE((1,1))** |
| Q2. AND⁻¹(0) | `N_and0_many3` | **MANY((0,0),(0,1),(1,0))** |
| Q3. XOR⁻¹(1) | `N_xor1_many` | **MANY((0,1),(1,0))** |
| Q4. NAND⁻¹(0) | `N_nand0_one` | **ONE((1,1))** |
| Q5. CONST0⁻¹(1) | `N_c0_none` | **NONE** |
| Q6. AND=0 joint vs product | `N_and0_joint` | **NONE** of equality — product adds `(1,1)` |
| Q7. C⁻¹(0,0) | `N_c00_many` | **MANY((0,0,0),(1,1,1))** |
| Q8. C⁻¹(1,1) | `N_c11_many` | **MANY((0,1,1),(1,0,0))** |
| Q9. AND=0 stopped after two | `N_partial_open` | **OPEN** — scanned 2 of 4, no coverage |
| Q10. Add3, c=2 | `N_add2_many` | **MANY((0,2),(1,1),(2,0))** |
| Q11. Add3, integer sum 4 | `N_add4_none` **died** | **ONE((2,2))** |
| Q12. XOR⁻¹(0) | `N_xor0_many` | **MANY((0,0),(1,1))** |

## Hostile cases

**Two solutions reported as one.** Q2 rejects `ONE((0,0))`. Q3 rejects
`ONE((0,1))` and the unordered support `{0,1}`. Q7 rejects `ONE((0,0,0))`.
Q8 rejects `ONE((1,0,0))`. Q10 rejects `ONE((1,1))`. Q12 rejects the
class label `"equal"`.

**Product of marginals is not the fiber.** Q6: AND=0 marginals are both
`{0,1}`; their product includes `(1,1)`, which AND maps to 1.

**Incomplete search is OPEN.** Q9 found `((0,0),(0,1))` and stopped.
That subset is not `MANY(2)` and not `ONE` of a representative.

## Q11 death

The frozen **NONE** for integer sum 4 did not survive. Ordinary addition
on Add3² gives `2+2=4`, so the complete fiber is **ONE((2,2))**. The
guess “4 is not a sum in `{0,1,2}`” mixed “4 ∉ Add3” with emptiness. If
the aperture requires the supplied port `c` to inhabit Add3, the input
is an admission error, still not NONE. `NULL.md` is not rewritten.
Replay refuses to revive `N_add4_none`. Genuine NONE on this cut is Q5.

## What remains OPEN

Rank-7 certified approximate families, discriminating-view selection,
grids larger than these named maps, SAT/SMT, Lean. A stopped search
stays OPEN. This packet does not establish its own general soundness
beyond the named maps.
