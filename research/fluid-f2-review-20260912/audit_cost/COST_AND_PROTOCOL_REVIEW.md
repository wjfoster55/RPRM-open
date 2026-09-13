# F2 cost and protocol review

Read-only source: `../input/fluid_dynamic_frontier_02/`. This review aggregates the supplied scored rows, identifies exact duplicate simulator inputs, and runs only six bounded controls. Reproduce with `python -I -B research/fluid-f2-review-20260912/audit_cost/audit_cost.py` from the repository root. `audit_cost_results.json` contains the numbers and full control outputs. Source files were not modified.

## Findings

### 1. The recorded implementation reduces simulator steps but takes more measured time

The stored rows sum to:

| Measurement | Seconds |
|---|---:|
| Candidate static preparation (`t_prepare_s`) | 1.936694 |
| Candidate fallback (`cand_fallback_wall_s`) | 2.443805 |
| Candidate timed pipeline, sum of the preceding two | 4.380499 |
| Reference timed pipeline (`t_ref_s`) | 1.479860 |
| Reference process-only (`ref_wall_s`) | 1.448973 |

The comparable wrapper timing ratio is **2.9601 candidate/reference**, despite 1771/10125 model-B steps. This is one recorded harness execution, including process/I/O overhead and static diagnostics, not a robust engine runtime ranking. It nevertheless rules out describing the supplied measurement as an observed wall-clock speedup. The return note correctly calls its ratio executed steps; it should also state the adverse measured time result.

`t_graph_s` (1.926656 s summed) is nested inside `t_prepare_s`, so adding both would double count. Evidence: `src/run_f2.py:95-105`, `109-116`, `172`, `186`, `193-195`. Candidate fallback timing and reference `t_ref_s` both surround the entire `run_oracle` wrapper; reference `ref_wall_s` surrounds only `subprocess.run` (`src/run_f2.py:36-49`). The protocol's "no overlapping totals" wording at `PROTOCOL.md:45-55` should explicitly declare this nesting.

The candidate recomputes an invariant wall/monitor graph on every frame check (`src/oracle.js:130-135`), producing 1794 graph evaluations. `reverseROpt` depends on fixed walls, dimensions, monitor and maximum fall, not evolving occupancy (`src/oracle.js:33-80`). Cache it once per scene, then check current water mass in that cached set. Charge initialization, graph construction, monitoring, allocation and serialization in an end-to-end comparison. `sumActive` does not include this graph work.

### 2. The reachability baseline omits the candidate's ordinary dynamic reachability stopping rule

`reachability_A` stops only when A decides initially; otherwise it borrows the reference's yes-only exit rollout (`PROTOCOL.md:37-40`; `src/run_f2.py:151-157`). Candidate fallback reevaluates the same A condition after each frame. Thus the large 8625-to-1771 step reduction relative to the declared A baseline conflates B with repeated A monitoring.

A conventional **dynamic A + yes exit** comparator uses the same cached reverse reachability set, checking whether remaining reachable water can still exceed the threshold after each actual model-B update. No new physical prediction is required. On all non-B-static paths the supplied candidate already runs exactly this comparator. Only the five B-only scenes require new controls:

| Scene | Dynamic A steps | Stop |
|---|---:|---|
| D_shelf_isolated | 300 | horizon |
| E_adjcell_y1 | 13 | no_trapped |
| E_adjcell_y35 | 1 | no_trapped |
| E_stack10_adj | 7 | no_trapped |
| E_blob9_far | 13 | no_trapped |

The resulting dynamic-A comparator takes **2105** total steps; AB takes **1771**, a **334-step (15.87%) reduction** attributable to B on this development panel. The stated 1500 steps avoided by B is correct relative to *static* A followed by yes-exit, but not relative to the stronger dynamic A comparator. Full runtime superiority over dynamic A remains unmeasured. The separate `../audit_support/LAYER_B_MATH_AUDIT.md` finds a unit-mass counterexample to B; accordingly, these 334 steps are a panel observation, not a sound algorithmic gain. Dynamic A remains the relevant surviving comparator.

### 3. The static wrapper does not apply the declared model-B normalization

`MODEL_CONTRACT.md:19,37` requires model-B normalization before frame zero. The contract excludes fractional mass *remaining after* normalization (`MODEL_CONTRACT.md:52`), without explicitly prohibiting positive fractional raw input. The actual oracle converts every positive input mass to WATER and then normalizes (`src/oracle.js:82-89`); the pinned normalizer sets its mass to 1 (`pinned/models.js:957-961`). Static evaluation instead sums raw input mass (`src/bound.py:139-147`, `238-242`, `260-269`; invocation `src/run_f2.py:98-101`).

Exact hostile control: copy `C_right_one`, replace its sole mass 1 with 0.25, retain the same walls/monitor/H/theta. Static official verdict is **CERTIFIED_NO** from A, but pinned `yes_exit` returns **Q=1 at frame 0**, with normalized mass 1. This control changes only pre-normalization mass and leaves no fractional mass after normalization. The frozen panel uses only raw 0/1 masses, so it cannot expose the discrepancy.

Repair options: apply a shared model-B admission/normalization map before static and exact paths, or explicitly restrict and validate raw input masses to {0,1}. Until then, distinguish the passing generated panel from the broader normalization contract; do not advertise a total static certificate on all accepted raw inputs.

### 4. The named panel has duplicate inputs and six mislabeled volumes

There are 53 scene labels but **50 distinct simulator inputs** (all physics inputs canonicalized, excluding descriptive metadata). Duplicate pairs:

- `f1_tall` and `A_w6_x26_V180`.
- `A_w4_x1_V180` and `C_far4_V180`.
- `A_w4_x28_V180` and `C_adj4_V180`.

All six `A_w2_*_V180` scenes contain **92**, not 180, water cells. A two-column generator supplies only 2×46 positions (`src/scenes.py:69-74`); `fill_cells` silently exhausts them (`src/scenes.py:57-66`), while the calling family and IDs promise V180 (`src/scenes.py:134-149`). `results/rows.jsonl:3-8` records the true V=92, so outcome rows themselves are not numerically falsified. Correct the family description/IDs or the generator in a separately versioned repair; assert the number placed for intended-volume generators. Preserve the original frozen panel and its rows.

Report denominators as 53 labeled runs / 50 distinct inputs, and do not interpret the panel as a clean fixed-volume placement comparison across every width. Duplicate weighting affects aggregate workload totals and collision-class frequencies.

## What the protocol supports

The protocol explicitly calls this a development panel, not held-out confirmation (`PROTOCOL.md:3-5`); uses the same receiver, pinned updater and horizon for both executed paths; separates candidate execution from the reference label (`src/run_f2.py:109-118`); and records the failed ablation rather than routing official output through it. These are useful controls. Final byte hashes establish transfer integrity; the delivered package alone does not independently establish when the panel/protocol was frozen relative to previous development observations.

The justified empirical report is finite panel agreement and a reduction in actual model-B steps on the supplied weighted panel. It is not proof of Layer B soundness, a measured speedup, a held-out generalization result, or evidence about continuum fluid dynamics. Dynamic A, shared normalization, corrected panel metadata and separate full-cost reporting are the next concrete evaluation repairs.
