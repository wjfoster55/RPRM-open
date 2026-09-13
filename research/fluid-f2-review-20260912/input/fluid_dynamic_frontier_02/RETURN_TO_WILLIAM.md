# Return to William — F2 crest-cut

Publication still on hold. F1 stays closed. No paper.

## Proposed summary

**Crest-cut:** the occupancy-ignoring model-B move graph `R_opt` (Layer A), plus a wall-supported catwalk `R_catwalk` and a conservative sill-fill need (Layer B). If those are UNRESOLVED, run the pinned `stepB` until A becomes decisive or H=300 (limited exact).

This is not `C_body`, not velocity-only, and not a certification-rate speedup.

## Derived rule

- **CERTIFIED_YES:** monitor mass `> 0.5` now, or during limited exact.
- **CERTIFIED_NO:** no water remains on `R_opt` (static A, or after exact evolution), **or** no water on `R_catwalk` and `V < sill_need` (static B).
- **UNRESOLVED** is not a final official output: fallback always finishes.

Evidence kind: A/B are proofs on the declared move graph; YES and trapped-NO from limited exact are the actual updater.

## One success

`D_shelf_isolated`: nine cells on a wall shelf that does not meet the gap. Layer A is UNRESOLVED (optimistic walk). Layer B certifies NO with **0** model-B steps. The yes-exit reference still runs 300 frames of shelf slosh. Truth Q=0.

Same pattern: `E_blob9_far`, `E_stack10_adj`, single gap-adjacent drips with V < 12.

## One failure / refinement

`D_ledge_end28` / `D_ledge_end30` / `D_sill_end25`: water stays on a disconnected ledge, `V >= sill_need`, so B will not say NO, and A never becomes empty because optimistic `R_opt` still allows horizontal walks without a floor. Limited exact pays the full 300 frames; truth is 0. The missing interaction is same-row down-diagonal injection versus “empty below ⇒ fall this frame,” which we did not prove as a global bound.

The ablation `failed_gap_adjacent` is **unsound** on this panel: 6 false NOs, including `A_w4_x26_V180` (2-cell creep, first breach 31) and `D_ledge_to_gap` (wall walk from x=20). Official verdicts do not use it.

## Reference comparison (53 frozen scenes)

| method | model-B steps | sumActive | static decides | false NO/YES |
|---|---|---|---|---|
| yes-exit only (competent rollout) | 10125 | 7041664 | 0 | 0 (exact) |
| reachability_A then yes-exit | 8625 | (A-decided scenes skip) | 6 | 0 |
| **crest_cut_AB + limited exact** | **1771** | 2049408 | 11 | **0 / 0** |
| failed_gap_adjacent (ablation) | n/a static | — | — | **6 false NO** |

Step ratio 1771/10125 = 0.175 is **executed steps**, not a certification-rate ratio. Versus the baseline that already owns Layer A, the new work is Layer B (5 extra static NO, 1500 reference steps avoided) and trapped-NO (20 scenes, 646 vs 6000 steps). 19 YES match yes-exit (same first-breach stop). 3 scenes still tie the horizon.

F1 pair full replay: tall Q=1 first 11 peak 22; flat Q=0 peak 0. Both initial velocities zero.

Volume+height: 6 colliding multi-member classes on this panel (placement still decides).

## Single remaining question

Can one prove that a cell with non-wall empty below always falls this frame unless a same-row already-processed neighbour injects a floor, and that this injection cannot carry mass arbitrarily far toward a gap before height is lost? If yes, the three horizon-pay ledges become static or early NO. If not, those scenes stay limited-exact-to-H.

## How to replay

From this directory:

```
python -I -B src/run_f2.py --output-dir /tmp/f2_replay_out
python -I -B src/check_f1_regression.py --rows /tmp/f2_replay_out/rows.jsonl
```
