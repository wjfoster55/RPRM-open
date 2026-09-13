# Frozen F2 development protocol

Frozen before the scored execution of `src/run_f2.py`. This is a
development panel, not a held-out confirmation cohort. Do not retune
theta, H, move sets, Layer B, or the scene list after seeing scored Q.

## Receiver (unchanged after freeze)

`MODEL_CONTRACT.md`. H=300, theta=0.5, model B, strict `>`.

## Scene panel

`src/scenes.py` `build_panel()`, at most 60 scenes. Families:

- `f1_regression`: original tall/flat
- `placement_V180`: columns at declared (width, x0), ramp, two-col
- `crest_volume`: crest_h in {8,12} × {flat180, far4-140, adj4-140}
- `threshold`: empty, one-on-right, gap cells y in {1,20,35}, adj4 V in
  {20,40,60,180}, far4 V in {20,180}
- `ledge`: isolated shelf; ledge to gap; ledge ends 28/30/31; sills
- `small`: single gap-adjacent cells; 10-stack; 9-blob
- `fill`: flat V=400
- `scale`: 96×64 far and adj, same H and theta

Generators are deterministic. No seeds. No scene added because a previous
run was favorable.

## Methods (declared)

Official candidate: `crest_cut_AB` static, then limited exact `cut_exit`
if UNRESOLVED.

Baselines:

1. `volume_height`: record `(V, top, W, H, crest_h)`; not a certificate;
   count colliding classes on this panel only.
2. `reachability_A`: Layer A only. If UNRESOLVED, fall back to the same
   yes-exit rollout as the reference (cost charged).
3. `early_exit_yes`: pinned model B, stop on first monitor `> theta`,
   else run all H. This is the competent reference.

Ablation (not official): `failed_gap_adjacent`. Count false NO. Do not
route fallback through it.

## Cost fields (no overlapping totals)

Per scene, separately:

- `t_prepare_s`, `t_graph_s` (static BFS)
- `cand_steps`, `cand_sum_active`, `cand_graph_evals`, `cand_fallback_wall_s`
- `ref_steps`, `ref_sum_active`, `ref_wall_s`
- `reach_steps` (0 if A decides, else equal to `ref_steps`)

Do not add candidate graph time into `ref_wall_s`. Do not report
certification-rate ratios as speedups.

## Scoring

- false NO / false YES of the official candidate must be 0 (harness
  exits nonzero otherwise)
- coverage denominators stated (n scenes)
- F1 tall/flat must replay Q=1/0; tall first breach 11 is checked in
  `src/check_f1_regression.py` after the panel, using the same oracle

## Separation

Static evaluation runs before any oracle call. Candidate `cut_exit` does
not read `Q_ref`. Reference `yes_exit` is a separate process.

## What this protocol is not

Not a large benchmark, not a paper, not a broadphase repair, not a
reopening of F1 claims, not a runtime ranking of engines.
