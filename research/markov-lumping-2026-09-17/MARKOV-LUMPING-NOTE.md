# Receiver-specific Markov lumping, in one sitting

17 September 2026. Standalone note for tomorrow. Not BSD. Not a new
lumpability theorem. Not a physical law.

Branch `research/markov-lumping-2026-09-17` in worktree
`C:\github\RPRM-open-markov-lumping`. Replay:

```powershell
python -I -B research/markov-lumping-2026-09-17/verify_ml.py
```

Nulls were frozen at `f191077` before the enumerator. Evidence grade is
the written Kemeny–Snell / Manifesto IV.1.2 criterion plus an exact
`Fraction` check on five named 2–4 state chains. Lean was not run. The
independent-math Rank 3 prompt was Markov-state coarse graining for a
fixed receiver. This cut is the smallest conjunction, not the Rank-3
hitting/path/intervention construction.

---

## 1. What is being asked

A finite homogeneous kernel `P` and a partition `C` with block map `r`.
Receiver `Q` is a function on states. `C` is an **operational quotient
for `Q`** iff

1. `Q` is constant on each block,
2. states in one block have equal mass into every block (strong
   lumpability),
3. every named zero-rate port is enabled in the whole block or in none
   of it.

(1) is Manifesto II.2. (2) is Proposition IV.1.2. Equal supports are a
lossy view of (2). The lumped matrix, when it exists, is not a molecular
or physical law.

---

## 2. Named chains

**FairTwo.** `{H,T}`, both rows `(1/2,1/2)`. **AbsorbingTwo.** `{L,D}`,
live `(1/2,1/2)`, dead `(0,1)`, extra port `enter_L`. **ManifestoFour-P**
and **Ptilde.** `{a,b,c,d}` as in Manifesto IV.1. **HandbookThreeSkew.**
`{a,b,c}` with `K_a(B)=1/4` and `K_b(B)=3/4`.

---

## 3. What the census did

| Cut | Result |
|---|---|
| FairTwo merge, constant `Q` | **ONE(yes)** |
| FairTwo merge, identity `Q` | **NONE** — lumpable, `Q` splits |
| AbsorbingTwo merge, constant `Q` | **NONE** — `enter_L` is `1/2` vs `0` |
| ManifestoFour-P, `C_AB={{a,b},{c,d}}`, `Q_color` | **ONE(yes)** |
| Same `C_AB`, `Q_split` | **NONE** — lumpable, `Q` splits `a` from `b` |
| `C_fine={{a},{b},{c,d}}`, `Q_color` | **NONE** — `Q` constant, `K_c({a})=1/4≠0=K_d({a})` |
| `C_diag={{a,c},{b,d}}`, `Q_color` | **NONE** — lumpable, `Q` splits `a` from `c` |
| Ptilde, `C_AB`, `Q_color` | **NONE** — `K_a(B)=1/4`, `K_b(B)=0` |
| Skew, `enter_B` | **ONE(yes)** both positive |
| Skew, operational | **NONE** — supports match, masses do not |

Hostile: Q7/Q9/Q12 keep `Q` and fail lumping. Q2/Q6/Q8 lump and fail
`Q`. Q12 additionally kills “equal support is enough.”

One-block lumpability on AbsorbingTwo is vacuous. The frozen NONE
survived on enabledness, not on a mass disagreement about a state that
is not a block.

---

## 4. Stop

No Bell-number padding of four-state partitions. No approximate
lumpability. No MSM comparison. Rank-3 coarsest hitting receivers remain
OPEN and are not this cut.
