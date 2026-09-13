# Dynamic-frontier insufficiency: C_body is NOT sufficient for Q_dyn

Grid 48x64. Continuation model = B (momentum). Horizon H = 300 frames. Breach threshold THETA = 0.5 cell-mass past the crest.

## 1. Witness pair (concrete numbers)

Container: closed box, central divider rising 10 cells from the floor (crest row 36); monitored region = the entire RIGHT compartment.
Both states: identical container, identical volume V = 180 (TALL sum=180, FLAT sum=180) => identical C_body.

- STATIC receiver Q_hydro (independent QUASISTATIC oracle): the resting distribution it assigns each state is IDENTICAL — right-compartment mass TALL=0.000, FLAT=0.000, TV(tall,flat) = 0.000. So both states share one Q_hydro answer — **C_body IS sufficient for the quasistatic receiver**, as `SUFFICIENCY_TEST.md` certified.
- DYNAMIC receiver Q_dyn (actual model-B rollout, H=300): **TALL Q_dyn = 1** (peak right-mass 22.0, first breach at frame 11); **FLAT Q_dyn = 0** (peak right-mass 0.0).

=> C_body(TALL) = C_body(FLAT) but Q_dyn(TALL)=1 != Q_dyn(FLAT)=0. **C_body is INSUFFICIENT for Q_dyn** (Prop-1 refutation for this receiver). This is insufficiency of THIS summary, not a universal lower bound.

**The sharp version (read this):** the quasistatic oracle *assigns the tall column the same resting-left answer as the flat one* — but the model-B rollout shows the tall column's momentum actually carries ~22 cell-mass over the crest, which the one-way crest then TRAPS on the right. That path-dependent, momentum-driven deposit is a real dynamic outcome the quasistatic summary (and C_body) provably cannot represent — the two states are Q_hydro-indistinguishable yet Q_dyn-distinct. That gap IS the insufficiency.

![witness pair](dynamic_frontier_witness.png)

## 2. Summary-collision disagreement rate (scene suite)

For each (container, V) CLASS all arrangements share C_body. We roll out K per class and count how often equal-summary states DISAGREE on Q_dyn. We also verify the static truth is identical within each class (so the disagreement is purely dynamic).

| container crest_h | V | arrangements | Q_dyn=1 | Q_dyn=0 | pairwise disagreement | static TV (within class) | mixed? |
|---|---|---|---|---|---|---|---|
| 8 | 140 | 7 | 3 | 4 | 57.1% | 0.000 | YES |
| 8 | 180 | 7 | 3 | 4 | 57.1% | 0.000 | YES |
| 8 | 220 | 4 | 2 | 2 | 66.7% | 0.000 | YES |
| 10 | 140 | 7 | 3 | 4 | 57.1% | 0.000 | YES |
| 10 | 180 | 7 | 3 | 4 | 57.1% | 0.000 | YES |
| 10 | 220 | 4 | 2 | 2 | 66.7% | 0.000 | YES |
| 12 | 140 | 7 | 3 | 4 | 57.1% | 0.000 | YES |
| 12 | 180 | 7 | 3 | 4 | 57.1% | 0.000 | YES |
| 12 | 220 | 4 | 2 | 2 | 66.7% | 0.000 | YES |

**Summary-collision disagreement rate: 84/144 equal-C_body pairs (58.3%) disagree on Q_dyn.** 9/9 equal-summary classes are 'mixed' (contain both a spill and a no-spill state). Within every class the static truth is identical (max static TV = 0.000), so the disagreement is entirely dynamic: C_body determines the static answer but not Q_dyn.

## 3. The minimal RPRM repair (Prop-1: C' = (C_body, extra))

A cheap summary S is INSUFFICIENT for Q_dyn if two states with equal S disagree on Q_dyn (a collision). C_body's own coordinate is V; a natural 'obvious fix' is to also retain the highest occupied row (D's `top`). Both still collide:

- **V  (== C_body)**: 9 colliding summary-classes => still **INSUFFICIENT**. e.g. crest_h=8 V=140, equal summary (140.0,): [('flat', 0), ('col_adj_w4', 1), ('col_adj_w6', 1), ('col_mid_w4', 0), ('col_far_w4', 0), ('two_col_w3', 1), ('ramp', 0)] (position of an equal-height column decides spill).
- **V + top row**: 6 colliding summary-classes => still **INSUFFICIENT**. e.g. crest_h=8 V=140, equal summary (140.0, 1): [('col_adj_w4', 1), ('col_adj_w6', 1), ('col_mid_w4', 0), ('col_far_w4', 0), ('two_col_w3', 1)] (position of an equal-height column decides spill).

So even C_body augmented with the surface height (`top`) does not decide Q_dyn: two equal-volume columns of the same height but different horizontal position disagree on whether their collapse overtops the crest. The exact Prop-1 repair is `C'(x) = (C_body(x), Q_dyn(x))` — cache the answer, the least informative refinement. The minimal *physical* state that restores sufficiency is the full **dynamic field** (the in-flight water distribution / arrangement, and under a momentum model the velocity field): with it, rolling the dynamics forward reproduces Q_dyn exactly, BY CONSTRUCTION. This is precisely RPRM_FLUIDS.md §3.3's forced fallback `C' = (C_body, velocity field)`: retaining it reintroduces the dynamic cost. So 'dynamic is expensive' is reframed honestly as 'this cheap summary is insufficient; here is the minimal add-back, and it is exactly the dynamic state we tried to discard.'

## Honest scope

This refutes sufficiency of the SPECIFIC summary C_body = (V, container geometry) for the SPECIFIC dynamic receiver Q_dyn. It is **not** a universal lower bound and **not** a claim that no local representation can answer Q_dyn (consistent with RPRM_FLUIDS.md §3.1's insufficiency *conjecture*, which we do not upgrade to a theorem). The static receiver Q_hydro remains sufficient for C_body — verified here by identical within-class static truth.
