# ML-k result

Written after `CENSUS.json`. Nulls were frozen in [NULL.md](NULL.md) at
commit `f191077`. Replay:

```powershell
python -I -B research/markov-lumping-2026-09-17/verify_ml.py
```

Evidence grade: **finite exhaustive check** of five named 2–4 state
kernels with exact `Fraction` rows. Not Lean. Not Manifesto IV.1.3. Not
a molecular MSM. Not a physics law. All twelve frozen surviving names
matched.

## Dispositions

| Question | Frozen surviving-null | Result |
|---|---|---|
| Q1. FairTwo `C_merge`, `Q_const` | `N_fair_yes` | **ONE(yes)** |
| Q2. FairTwo `C_merge`, `Q_id` | `N_fair_qfail` | **NONE** — `q_not_constant` |
| Q3. AbsorbingTwo `C_merge`, `Q_const` | `N_abs_mass` | **NONE** — `enabledness` |
| Q4. AbsorbingTwo `enter_L` | `N_abs_en_no` | **NONE** — rates `1/2` vs `0` |
| Q5. ManifestoFour-P `C_AB`, `Q_color` | `N_p_yes` | **ONE(yes)** |
| Q6. ManifestoFour-P `C_AB`, `Q_split` | `N_p_qfail` | **NONE** — `q_not_constant` |
| Q7. ManifestoFour-P `C_fine`, `Q_color` | `N_fine_mass` | **NONE** — `not_lumpable` |
| Q8. ManifestoFour-P `C_diag`, `Q_color` | `N_diag_qfail` | **NONE** — `q_not_constant` |
| Q9. ManifestoFour-Ptilde `C_AB`, `Q_color` | `N_pt_mass` | **NONE** — `not_lumpable` |
| Q10. Ptilde `enter_B` on `{a,b}` | `N_pt_en_no` | **NONE** — `1/4` vs `0` |
| Q11. Skew `enter_B` on `{a,b}` | `N_sk_en_yes` | **ONE(yes)** — `1/4>0` and `3/4>0` |
| Q12. Skew `C_AB`, `Q_color` | `N_sk_mass` | **NONE** — `not_lumpable` |

## Hostile cases

**Q preserves, lumping fails.** Q7: `C_fine={{a},{b},{c,d}}` keeps
`Q_color` constant, but `K_c({a})=1/4` and `K_d({a})=0`. Q9: the
Manifesto failed matrix, `K_a(B)=1/4` and `K_b(B)=0`. Q12: equal
supports of `enter_B` (`N_sk_support` rejected); masses `1/4` vs `3/4`.

**Lumping holds, Q fails.** Q2: FairTwo is strongly lumpable and
`Q_id` splits the block. Q6: `C_AB` is lumpable on `P` and
`Q_split(a)=0≠1=Q_split(b)`. Q8: `C_diag` is lumpable on `P` and
`Q_color(a)=0≠1=Q_color(c)`.

## Q3 reason correction

The frozen **NONE** for Q3 survived. The written reason did not. Under
`C_merge={{L,D}}` there is one block, so strong lumpability is
vacuous (`K=1` for both rows). The failing conjunct is the named
zero-rate port `enter_L`: `P[L,L]=1/2` and `P[D,L]=0`. That is Q4.
`N_abs_qenough` stays dead. Do not treat one-block lumpability as a
mass disagreement about a state that is not a block.

## What remains OPEN

Rank-3 coarsest hitting / path / intervention receivers, approximate
lumpability, continuous-time generators as a separate type, molecular
comparison, Lean. This packet does not establish its own general
soundness beyond the named chains.
