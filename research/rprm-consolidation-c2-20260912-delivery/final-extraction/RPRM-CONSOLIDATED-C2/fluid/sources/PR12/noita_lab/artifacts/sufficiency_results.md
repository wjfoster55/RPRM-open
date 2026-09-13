# Sufficiency-certificate falsification results (auto-generated)

Grid 40x52. Scenes evaluated: 1100. Exact D read-offs: 816 (74.2%).
EXACT means TV(D read-off, independent truth) < 1.0 cell-masses (agreement within a 1 cell-mass total-variation tolerance).
Baselines tuned for max certification rate at FP=0: quiescent active<= 4, speed maxFlow<= 0.0.

```
verdict            cert%   FP  FPrate%  recall%   TP   FN   TN
--------------------------------------------------------------
P_geo               46.8    0     0.00     63.1  515  301  284
P_full               1.7    0     0.00      2.3   19  797  284
P_noC2              50.7   43     7.71     63.1  515  301  241
P_C1only            70.5   43     5.54     89.8  733   83  241
C1                  70.5   43     5.54     89.8  733   83  241
C2                   1.7    0     0.00      2.3   19  797  284
C3                  66.5  216    29.55     63.1  515  301   68
C4                  62.5  173    25.15     63.1  515  301  111
base_quiescent       3.4    0     0.00      4.5   37  779  284
base_speed           0.0    0     0.00      0.0    0  816  284

== DECISIVE DIAGNOSTIC ==
D-wrong scenes: 284. Their activeWaterCells: min=5 median=73 max=164
QUIESCENT-but-D-WRONG (active<= 4): 0  (these are where naive quiescence would FALSE-POSITIVE)
  ...of those, RPRM P (C1&C3) correctly REJECTS: 0 (RPRM's potential soundness win over quiescence)
MOVING-but-exact that RPRM P_geo certifies and quiescence misses: 478 (RPRM's certification-rate win over quiescence)

Per-family (exact / total, and P_noC2 FP):
  closed_tank          exact 110/110  P_geo cert=110 FP=0  quiescent FP=0
  flat_basin           exact 110/110  P_geo cert=110 FP=0  quiescent FP=0
  ledge                exact  67/110  P_geo cert= 31 FP=0  quiescent FP=0
  midsplash            exact  64/110  P_geo cert=  3 FP=0  quiescent FP=0
  multipocket          exact  86/110  P_geo cert= 40 FP=0  quiescent FP=0
  tilted               exact  49/110  P_geo cert= 49 FP=0  quiescent FP=0
  trap_perched         exact   0/110  P_geo cert=  0 FP=0  quiescent FP=0
  trap_shared_cavity   exact 110/110  P_geo cert=  0 FP=0  quiescent FP=0
  trapped_air          exact 110/110  P_geo cert=110 FP=0  quiescent FP=0
  utube                exact 110/110  P_geo cert= 62 FP=0  quiescent FP=0
```

Illustrative TRAP (D drains a pocket it should keep): family `ledge`, TV=217.00. C1&C3 alone certify it (wrong); the drainage guard C4 rejects it (C4=False).

Illustrative CERTIFICATION-RATE win: family `multipocket`, exact read-off with activeWaterCells=123 (NOT quiescent); RPRM P_geo certifies it, naive quiescence cannot.

