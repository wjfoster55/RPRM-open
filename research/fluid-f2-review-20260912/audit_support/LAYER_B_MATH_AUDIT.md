# F2 Layer B audit — two-cell support injection

**Verdict: the general Layer B CERTIFIED_NO guarantee is refuted in the stated model-B contract.** The witness uses the original 64x48 container, unit masses, normalization to zero velocity, frame 0 initialization, no sand, no inflow, H=300 and strict theta=0.5. It adds two allowed ledge wall cells. This is an exact counterexample to the proposed rule, reproduced with the unchanged exported implementation and pinned simulator. It is not an estimate of failure frequency.

## Exact claim and code

- `input/fluid_dynamic_frontier_02/proof/DERIVATION.md:104–110` treats the number of cells from a fringe position down to the next wall as a lower bound on the mass needed to create support. The assertion that stacking in one column is cheapest is the failed step.
- `input/fluid_dynamic_frontier_02/src/bound.py:177` implements `sill_need`; lines 281–282 certify NO when `V < need`. `official_static_verdict` at line 308 admits that result to the official routing path.
- `input/fluid_dynamic_frontier_02/pinned/models.js:106–108` allows a diagonal move to inject water below a later cell, followed by that later cell's horizontal move.
- `input/fluid_dynamic_frontier_02/pinned/grid.js:140–153` supplies the actual scan order. On even frame 2, x=30 is processed before x=31 within their common chunk. The stamp prevents a water occurrence from moving twice; it does not prevent a moved occurrence from supporting another occurrence.

## Witness

Use `scenes.make_container(64, 48, 10, extra_walls=[(29,36),(30,36)])`. The divider is x=32 starting at y=36. The monitor is the complete right compartment, x>32. Put exactly one water cell at each of `(30,34)` and `(31,34)`; all other non-wall cells start empty.

The unchanged bound reports:

- A: UNRESOLVED;
- water in R_catwalk: 0;
- V: 2;
- sill_need: 12;
- B and official static result: CERTIFIED_NO, reason `no_catwalk_and_V_lt_sill_need`.

The unchanged full oracle reports Q=1, first breach at frame 3, maximum monitored mass 1, final total water mass 2, after all 300 frames.

| Frame | Water positions | Mechanism |
|---|---|---|
| 0 | (30,34), (31,34) | Normalized start. |
| 1 | (30,35), (31,35) | Both fall one cell; neither splashes in a frame in which it fell. |
| 2 | (31,36), (32,35) | The x=30 cell has a wall below and moves diagonally into (31,36). It now supports the x=31 cell. Both diagonal destinations of that second cell are walls, so it moves horizontally into the divider gap (32,35). |
| 3 | (31,37), (33,36) | The gap cell moves diagonally right into the monitor; mass 1 exceeds 0.5. |

There is no filled twelve-cell tower. Two cells suffice because support arrives diagonally from an adjacent ledge before the supported cell is processed. The derivation's later discussion of same-row injection as an open interaction also applies to Layer B itself.

## Surviving scope and correction

Layer A remains sound for normalized unit-occupancy model B with static walls, no sand, no inflow, and the stated summed-region receiver: its optimistic graph includes every actual move, so water outside the reverse reachable set cannot subsequently reach the monitor. Ignoring time enlarges that set and can reduce certification coverage without creating a false NO. Unit-mass conservation follows from normalization and relocation at mass 1; this argument is not an assertion about arbitrary pre-normalization fractional masses.

The full-state limited exact path also remains sound under that contract: check actual monitored mass for YES, apply Layer A to the current field for early NO, otherwise run through the finite horizon. It evolves incoming support and scheduler state across the entire grid. This witness does not challenge that path; the unsound static B result prevents the original combined router from reaching it.

Withdraw the general Layer B guarantee and route its present NO branch as UNRESOLVED until a new proof with a defensible admission guard or a different bound is supplied. Retain the original panel and this counterexample as separate evidence. A zero-error result on the 53-scene panel cannot preserve the refuted guarantee. Any narrower result must explicitly cover or exclude transient support injection and must be re-evaluated under its changed routing contract.

## Reproduction and artifacts

Run:

```powershell
python -I -B C:\github\RPRM-open\research\fluid-f2-review-20260912\audit_support\check_layer_b_support_injection.py
```

The script imports the unchanged exported `bound.py` and `scenes.py`, then calls the unchanged `oracle.js` for this single constructed scene. It asserts the false NO and records complete input plus oracle output under `audit_support`:

- `layer_b_support_injection_spec.json`: full walls, initial field and monitor;
- `layer_b_support_injection_oracle.json`: 301 monitored observations and frame 0–3 snapshots;
- `layer_b_support_injection_result.json`: contract, layer outputs, concise trace and mismatch.

Checked with Python 3.14.5 and Node 24.18.0. Input payload files were not edited.

SHA-256 at review execution:

| Artifact | SHA-256 |
|---|---|
| check_layer_b_support_injection.py | `1ea72bb8044b34187baa1540a9af95d21f5f274997b6cf7dd4233a5f3eea45eb` |
| layer_b_support_injection_spec.json | `f2909d598b62408d5b1bdd51c84a2eaab250a0e4ce0dc64e9322eef5f6aca78a` |
| layer_b_support_injection_result.json | `99aa162bd2c6f05747b0f68558577c8592d1daacf43a37acfa2efc2e15f88f08` |
