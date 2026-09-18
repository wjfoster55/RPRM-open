# OB-iff result

Nulls frozen in [NULL-IFF.md](NULL-IFF.md) at `4aa1c13`. Replay:

```powershell
python -I -B research/observability-budget-2026-09-17/verify_ob.py
```

| Question | Frozen test | Result |
|---|---|---|
| Q14. L tick-horizon 3 refine-Q count | `N_l_none` vs `N_l_some` | **NONE** |
| Q15. M identity on `{A}` | `N_m_id_none` vs yes | **NONE** |
| Q16. Hostile `{Y}` h1 refine-Q / h2 repair | `N_y_delay` vs immediate / never | **ONE(`N_y_immediate`)** |

`N_y_delay` is **NONE**. The named pair `(000),(001)` still agrees on
`Y` after one shift (`0,0`) and splits after two (`0,1`). Another
Q-ghost, `(000),(011)`, already splits at horizon 1 (`Y: 0→0` vs
`0→1`). Descent failure is not the same event as “the pair you named.”

No further budget-k family. Standalone note:
[OBSERVABILITY-NOTE.md](OBSERVABILITY-NOTE.md).
