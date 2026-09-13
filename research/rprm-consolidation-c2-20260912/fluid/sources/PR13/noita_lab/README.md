# mini-Noita liquid lab

A tiny, dependency-free **falling-sand / liquid** sandbox whose real purpose is to
**compare three cheap water models** and surface the hard problems in cheap liquid
simulation. Built as a proof-of-concept: the liquid is the star; sand/stone exist
only to make the liquid demo compelling.

Everything is self-contained in this folder. No build step, no npm, no external JS
deps. The interactive demo is vanilla browser JS (Canvas2D, one pixel per cell).
The experiment harness is Python + numpy + Pillow and drives the **exact same
JavaScript physics** through node, so the measured numbers describe the code the
demo runs.

> **Read [`PROBLEMS.md`](PROBLEMS.md) next** — that is the main deliverable: a
> sharp, numbered list of the open liquid problems and trade-offs, backed by the
> measurements below.

---

## Run the interactive demo

```bash
cd noita_lab
/workspace/.venv/bin/python -m http.server 8000
# open http://localhost:8000/  (any Python or static server works)
```

Controls: paint with the mouse; switch **water model A/B/C/D/E/F live** (E = D_fast
frame-identical to D, F = D_fast cheap variant); switch brush
(water / sand / stone / erase); load a scenario (Column→basin / U-tube / Dam-break);
pause, change speed, and toggle a **"show awake chunks"** overlay. The HUD shows
**FPS, active-cell count / %, cells moved, and total water mass**.

Try this: load **U-tube**, watch model **A** freeze with the right shaft empty,
switch to **C** live and watch it slowly push water partway up the right shaft,
then switch to **D** and watch both shafts snap level (Δh → ~0) in a few steps.

## Run the experiments (headless, reproducible)

```bash
cd noita_lab/experiments
/workspace/.venv/bin/python run_experiments.py        # ~15 s; writes table + artifacts
node smoke_demo.js                                    # headless sanity check of the demo JS
```

`run_experiments.py` runs each model on three scenarios, prints the comparison
table (also written to `artifacts/metrics_table.md`), and regenerates all GIFs and
plots into both `artifacts/` (committed) and `/cursor/stores/self/artifacts/`.

## The four liquid models (swappable live)

- **A — Binary (classic Noita).** Each water cell is full; tries down, then a
  down-diagonal, then spreads horizontally to the nearest hole. Fast; cannot climb;
  surface stays stepped; never truly rests.
- **B — Momentum.** Each cell carries a velocity; gravity accelerates it and
  impacts become horizontal splashes. Lively, but oscillates and won't flatten.
- **C — Mass / level-equalizing.** Each cell holds a *continuous* amount of water
  and exchanges it with down/left/right/**up** neighbors, with a small
  compressibility so connected columns build pressure. Flattens free surfaces,
  represents sub-cell depth, conserves mass exactly, and is the only model that
  pushes water *upward* at all. **The strongest purely-local candidate — but it
  still does not fully equalize a tall U-tube (see PROBLEMS.md #1).**
- **D — Level-aware (connected-body level field).** C's continuous mass plus a
  *non-local change of representation* (the RPRM move for #1): each step it labels
  connected water bodies, reads each body's target free-surface level straight off
  (`volume / footprint`), and relaxes toward it with a mass-conserving matched
  transfer. **Equalizes a tall U-tube to Δh ≈ 0.07, leaves a perfectly flat
  surface (std 0.00), is the only model that comes to rest, and stays exactly
  mass-conserving (0.000%)** — at the cost of a per-body flood-fill each step and a
  non-local "teleporty" look that a disturbance gate hides during splashes. This
  is the headline result; see PROBLEMS.md §1★ for the full win/cost/failure-mode.

## Results (grid 100×64; see `artifacts/metrics_table.md` for the full table)

| scenario | model | mass err % | rests? | residual moved/step | surface std | U-tube Δh | avg active % |
|---|---|---|---|---|---|---|---|
| basin | A binary | 0.000 | no (jitter) | 62 | 1.32 | – | 22 |
| basin | B momentum | 0.000 | no (jitter) | 47 | 0.96 | – | 25 |
| basin | C mass-level | 0.000 | no (jitter) | 79 | 0.97 | – | 25 |
| basin | **D level-aware** | 0.000 | **yes (39)** | **0** | **0.00** | – | **0.8** |
| utube | A binary | 0.000 | freezes wrong | 44 | – | **26.6** | 29 |
| utube | B momentum | 0.000 | freezes wrong | 22 | – | **26.7** | 28 |
| utube | C mass-level | 0.000 | slowly closing | 63 | – | **17.9** | 23 |
| utube | **D level-aware** | 0.000 | **yes (17)** | **0** | – | **0.07** | **0.1** |
| dam | A binary | 0.000 | no (jitter) | 90 | 2.36 | – | 39 |
| dam | B momentum | 0.000 | no (jitter) | 43 | 0.84 | – | 42 |
| dam | C mass-level | 0.000 | no (jitter) | 370 | 6.55 | – | 43 |
| dam | **D level-aware** | 0.000 | **yes (54)** | **0** | **0.00** | – | **1.4** |

`Δh` = |left − right| shaft fill after the run; **0 = perfectly level**. A/B freeze
at Δh≈26.6 (right shaft empty, physically impossible); C keeps closing (still
descending at the end of the run) but plateaus above 0; **D reads the level off a
per-body field and reaches Δh≈0.07 in ~15 steps** (see PROBLEMS.md §1★). D's low
`avg active %` is because it actually *settles and sleeps*; its instantaneous cost
during the active phase includes a per-body labeling pass (peak ~1.5k–8.4k
cells/step — measured in `metrics_table.md`). Compressibility trades
equalization speed for calm (model C only):

| MaxCompress | 0.02 | 0.05 | 0.1 | 0.2 (default) | 0.4 |
|---|---|---|---|---|---|
| final U-tube Δh | 26.8 | 24.2 | 21.9 | 17.9 | 13.9 |

### Headline takeaways
- **All four conserve mass** (0.000% after the active/sleeping halo fix, PROBLEMS #5;
  D's matched-transfer relaxation is mass-conserving by construction).
- **Only C flattens surfaces and pushes water up** among the *purely local* models
  — but its "equalization" is surface-flow, not pressure, so a tall U-tube never
  fully levels (PROBLEMS #1). **Model D fixes this by changing representation
  (per-body level field): U-tube Δh → 0.07, perfectly flat surfaces (std 0.00).**
- **Only D comes to rest.** A/B shuffle forever (update-order limit cycle), C keeps
  a low surface jitter tamed by a deadband at the cost of tiny permanent imbalance
  (PROBLEMS #2, #3); D stops once each body is within `LevelEps` of its target.
- **D's fix is non-local, and that is the trade** — it costs a connected-components
  + cavity flood over every active body each step and looks "teleporty" (PROBLEMS §1★).
- **The active-cell scheme works**: idle regions sleep, dropping cost to ~22–25%
  of the grid on the basin — but a live pool's surface never fully sleeps
  (PROBLEMS #6), and a full-grid disturbance erases the savings (PROBLEMS #11).

## Artifacts

In `artifacts/` (and mirrored to `/cursor/stores/self/artifacts/`):
- `basin_{A,B,C,D}.gif`, `utube_{A,B,C,D}.gif`, `dam_{A,B,C,D}.gif` — scenario × model
- `settle_{basin,utube,dam}.png` — cells-changed-per-step (settling)
- `utube_equalization_ABCD.png` — Δh vs step for **all four models** (the headline
  figure: D drops to ~0, C crawls, A/B freeze); `..._ABCD_zoom.png` is the first-400-step view
- `utube_equalization.png` — same, kept for backward compatibility
- `compress_sweep.png` — model C compressibility vs equalization speed
- `relabel_sweep.png` — model D `RelabelEvery` amortization vs equalization speed
- `active_cost.png` — active-cell % over time
- `mass_conservation.png` — mass error over time
- `metrics_table.md` — the full generated table (incl. D's labeling cost columns)

## Files

```
index.html            demo page + controls
js/constants.js       elements, tunables, stableBottom() pressure function
js/grid.js            cell storage, chunk/dirty-rect active-cell scheme, sand
js/scenarios.js       basin / U-tube / dam builders (shared with the harness)
js/models.js          water models A/B/C/D + D_fast (E_exact and F) + live switching
                      (D = level-aware: connected-body level field + relaxation;
                       E_exact = frame-identical to D; F = certificate-cached D_fast,
                       the cheap-but-not-bit-identical variant — see design/PERF.md)
js/renderer.js        Canvas2D ImageData pixel blit
js/main.js            input, loop, HUD
experiments/run_sim.js         node driver: runs the js/ physics headlessly -> JSON
experiments/run_experiments.py metrics + GIFs + plots (drives run_sim.js)
experiments/smoke_demo.js      headless load+run of all demo scripts (stubbed DOM)
```

## RPRM connection (light)

The researcher's [RPRM-open](https://github.com/wjfoster55/RPRM-open) frames RPRM as
a *Relational Pressure Retention Model* — "retain only what must be retained to
continue," change representation to expose the question you actually need, and
choose the next observation economically. Two concrete bridges show up in this
code:

1. **Active-cell / dirty-rect simulation = economical retention.** We only simulate
   cells that can still change; sleeping cells are exactly the state we choose *not*
   to keep observing. The `SleepEps`/`MinFlowCutoff` deadband is the literal
   "how economical can the retained set be before the answer degrades" knob — and
   PROBLEMS #3 shows it degrading the answer, which is the RPRM trade-off made
   measurable.
2. **The halo bug (PROBLEMS #5) is an RPRM "minimal *sufficient* representation"
   lesson.** Retaining only awake cells was *too* economical: it broke mass
   conservation. The one-chunk halo is the minimal extra state that makes the
   retained representation sufficient again.
3. **Problem #1 is a "change of representation" problem — and model D is that change.**
   The local rule literally cannot see the quantity that matters (a connected body's
   target level), so **model D changes the representation**: it flood-fills a
   per-body level field and reads the equilibrium off it instead of diffusing
   pressure one cell per frame. This is the most direct RPRM bridge in the code —
   *retain the minimal sufficient extra state (a per-body level) that makes the
   question answerable* — and PROBLEMS.md §1★ measures both the win (Δh → ~0) and
   the price (a non-local flood-fill per active body; a "teleporty" look).

This is a light, honest analogy, not a claim that the demo implements RPRM.
