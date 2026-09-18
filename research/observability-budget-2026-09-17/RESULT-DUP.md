# OB-dup result

Written after `CENSUS.json` gained Q6–Q8. Nulls were frozen in
[NULL-DUP.md](NULL-DUP.md) at commit `f535cd0`. Replay:

```powershell
python -I -B research/observability-budget-2026-09-17/verify_ob.py
```

Q1–Q5 dispositions are unchanged. Evidence grade for Q6: **restricted
theorem** plus 80 exact trials. Not Lean. Not AD-R3.

## Dispositions

| Question | Frozen surviving-null test | Result |
|---|---|---|
| Q6. Does a value-copy repair any insufficient L-panel? | `N_dup_never` vs `N_dup_repairs` | **NONE** (0 of 80) |
| Q7. Machine M `{A}` / `{A,A2}` / `{A,B}` | `N_look_copy` vs any-second / none | **ONE(`N_look_copy`)** |
| Q8. `{R,R2}` tick-horizon 3 | `N_trace_copy_never` vs helps | **NONE** |

## Hostile machine M

`{A}` and `{A,A2}` both leave `{0,1}` joined with `Q` unequal. `{A,B}`
separates that pair because `B` differs at state `1`. A lookalike is
not a duplicate; the identical-map hypothesis is load-bearing.

## Grade

**THEOREM restricted** to total named ports, value-tuple or word-trace
representations, and state-only `Q`. Written proof:
[THEOREM-DUP.md](THEOREM-DUP.md).
