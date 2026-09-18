# OB-time result

Written after `CENSUS.json` gained Q9–Q13. Nulls were frozen in
[NULL-TIME.md](NULL-TIME.md) at commit `784f27a`. Replay:

```powershell
python -I -B research/observability-budget-2026-09-17/verify_ob.py
```

Q1–Q8 dispositions are unchanged. Duplicate-function proof:
[THEOREM-DUP.md](THEOREM-DUP.md) (20 lines). Time proof:
[THEOREM-TIME.md](THEOREM-TIME.md).

## Dispositions

| Question | Frozen surviving-null test | Result |
|---|---|---|
| Q9. How many of 31 L-panels descend under `tick`? | `N_all31` vs `N_sing5`, `N_none` | **ONE(31)** |
| Q10. Does horizon-3 refine any descending insufficient panel? | `N_time_closed_never` vs sometimes | **NONE** |
| Q11. `X` of `{R}` / `{R,X}` sufficient? | `N_port_indep` vs dep / fail | **ONE(`N_port_indep`)** |
| Q12. Shift `{Y}` static vs horizon 2 | `N_shift_time` vs none / already | **ONE(`N_shift_time`)** |
| Q13. Does `{Y}` descend under `shift`? | `N_shift_open` vs closed | **ONE(open)** |

## Grade

**THEOREM restricted:** if `C_S ∘ T` is a function of `C_S`, extra time
cannot refine `ker C_S`. On L the hypothesis holds for every nonempty
panel. Hostile N fails the hypothesis, and extra time repairs. An
independent port is a different repair (`{R,X}`).
