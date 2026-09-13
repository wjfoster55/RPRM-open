# Open problems & trade-offs — mini-Noita liquid lab

For William. These are the problems I actually hit while building and measuring the
three liquid models, ordered with the **liquid** problems first. Every number
below comes from `experiments/run_experiments.py` (see `artifacts/metrics_table.md`
and the plots). I have tried to be honest about what does **not** work.

The single most important finding, up front:

> **Cheap cellular water equalizes surfaces by letting water run *downhill along
> the surface*, not by transmitting *pressure through the fluid body*. Every
> "level equalization" win in models A/B/C is really surface flow. The moment
> water must be pushed *up* through a barrier (a U-tube), all three fail — C
> merely fails *slowly and partially* instead of instantly.**
>
> **Model D breaks this by *changing the representation*: it retains a per-body
> level field and reads the answer off it (U-tube Δh 35 → 0.07, mass 0.000%),
> instead of diffusing pressure one cell per frame. The catch is that the fix is
> non-local by construction — see §1★ for the win *and* its cost/failure modes.**

---

## 1. Hydrostatic pressure is not transmitted through the fluid body (U-tube never equalizes) — THE big one

**What happens.** In the connected-vessels test (`utube_*.gif`, `utube_equalization.png`)
the left shaft is filled and the right shaft should rise to the same level.
- Models **A (binary)** and **B (momentum)**: water fills the left shaft and the
  bottom pipe, and then *freezes* with the right shaft **empty**. The height
  difference `Δh` drops from 35 to ~26.6 in the first ~200 steps and then
  **flatlines forever** — a completely static, physically impossible state
  (a 28-cell water column standing next to an empty connected shaft).
- Model **C (mass-level)**: `Δh` decreases *continuously* (35 → ~18 at 6000 steps)
  and is still going, but it plateaus (long runs settle at `Δh ≈ 9` for this tall
  tube, never 0).

**Why (hypothesis).** Horizontal flow in all three models is driven by a *local*
quantity. In C it is the mass difference between two horizontally-adjacent cells,
`(m_i − m_j)/4`. Between two **full** cells (both `m ≈ 1`) that difference is ~0,
so a tall column exerts **no** sideways push through the row of full cells at the
bottom pipe. The only thing that leaks pressure sideways is the tiny
*compressibility* term (cells allowed to hold `1 + MaxCompress`), and that
information propagates at best ~`MaxCompress` per step. Pressure is therefore *diffused*
extremely slowly instead of transmitted, and for a tall tube the deadband (see #3)
stops it before it finishes.

**How cheap fixes fail.** Raising `MaxCompress` is the obvious lever and it *does*
help monotonically (`compress_sweep.png`: final `Δh` 26.8 → 13.9 as
`MaxCompress` 0.02 → 0.4), but (a) it never reaches 0, (b) it makes the free
surface bounce/overshoot, and (c) it only rescales the timescale — convergence is
still ~O(height) or worse. It is a band-aid on a diffusion process, not a pressure
solve.

**What a good solution needs.** A genuine pressure/level field that is *non-local*:
e.g. flood-fill each connected water body (union-find) once per frame, compute a
single target surface level per body from `volume / footprint`, and move water
toward that level; or a lightweight height-field / 1-D "pipe" pressure Poisson
solve. All of these break the "purely local, one-cell-neighborhood" rule and cost
more (a connected-components pass, or an iterative solve), which is exactly the
cheap-vs-correct tension at the heart of this demo.

**➡ This is now implemented as model D — see §1★ below.**

---

## 1★. Model D — a connected-body level field that actually fixes #1 (the RPRM change of representation)

This is the fix proposed in #1, built and measured. The RPRM move is literal: a
purely local rule *cannot see* the quantity that decides the answer — a connected
body's target free-surface level — so instead of trying to propagate that signal
one cell per frame (C's slow compressibility diffusion), model **D** *changes the
representation* to retain that quantity explicitly, then reads the answer off it.

**How it works (`js/models.js` `stepD` / `relaxLevels`).** Each relabel step:
1. **Label** contiguous water bodies by flood fill (4-connectivity over water cells),
   seeded only from cells in *awake* chunks so settled/asleep pools cost nothing.
2. **Flood the containing cavity** (air+water bounded by walls), *bounded above by
   the body's own topmost water cell* — equilibrium can never rise above that, so
   we never flood the open sky and (verified) never teleport water up over a
   barrier into a disconnected basin.
3. **Read the target level straight off:** fill the cavity bottom-up with the
   body's volume `V`. Deep cells target `MaxMass`, the surface row a partial fill,
   cells above the level target `0`. Both shafts of a U-tube share one body → one
   level → equal fill.
4. **Relax** toward the target with a **mass-conserving matched transfer**: drain
   over-full cells top-down, fill deficit cells bottom-up, by the *same* amount.
   Because target and current mass both sum to `V` over the body, *any* partial
   relaxation conserves mass **exactly** (measured 0.000%).

Local advection (incompressible down-fill + horizontal spread) still runs every
step for lively splashes; a **disturbance gate** (`1/(1+moved·scale)`) throttles
the non-local solve while gravity is actively moving mass (dam-break splash) and
opens up once local flow stalls (U-tube frozen) so the level field finishes the job.

**What it fixes (measured, grid 100×64; see `artifacts/metrics_table.md`).**

| metric | A binary | B momentum | C mass-level | **D level-aware** |
|---|---|---|---|---|
| U-tube final Δh (0 = level) | 26.6 | 26.8 | 17.9 | **0.07** |
| comes to rest? | never | never | never | **yes (17/39/54 steps)** |
| basin surface std (flat=0) | 1.32 | 0.96 | 0.97 | **0.00** |
| dam surface std | 2.36 | 0.84 | 6.55 | **0.00** |
| mass error (final) | 0.000% | 0.000% | 0.000% | **0.000%** |
| avg active % (basin/utube/dam) | 22/29/39 | 25/28/42 | 25/23/43 | **0.8/0.1/1.4** |

- **The U-tube equalizes** (Δh 35 → 0.07 in ~15 steps, vs C still at 17.9 after
  6000). `artifacts/utube_equalization_ABCD.png` and `..._zoom.png`.
- **D is the only model that comes to rest** and the only one that leaves a
  *perfectly flat* surface (std 0.00). It fixes #2, #3 and #4 as a side effect,
  because "at rest" is now "body is within `LevelEps` of its read-off target."
- **Amortized cost is *lower*, not higher:** because D settles and then sleeps,
  its average active fraction is 0.1–1.4% vs C's 23–43%.

**What it costs (measured honestly).** The average is cheap *only because D stops*.
The *instantaneous* cost during the active phase is real: each relabel runs a full
connected-components + cavity pass over every active body.

- Peak labeling cost: **~1,500 cells/step (U-tube)** to **~8,400 cells/step
  (dam)** — the dam figure is ~1.3× the whole 6,400-cell grid (body cells once +
  cavity cells once). That is the price of the change of representation; it is not
  a one-cell-neighborhood rule anymore.
- Amortizing helps and is safe (`relabel_sweep.png`): `RelabelEvery` k = 1→16
  halves average label cost (dam 589→281 cells/step) and still reaches Δh≈0 with
  **0.000% mass error** — each relabel is recomputed from scratch, so staleness
  can never leak mass or corrupt a split/merged body; it only *slows* the
  equalization response into a visible staircase (k=16 U-tube: ~200 steps vs ~15).

**New failure modes (the honest tension).**
1. **It looks non-local, because it is.** On the U-tube the far shaft fills from
   the bottom while the near shaft drains from the top *without water visibly
   flowing through the pipe* — the level is read off, not carried. The disturbance
   gate hides this during violent transients (the dam collapses as a natural wave,
   `dam_D.gif`), but a slow-motion U-tube fill (`utube_D.gif`) reveals the
   "teleport." This is the representation trade, not a bug: you buy O(1)-pass
   equalization by giving up strict local causality.
2. **The disturbance gate is global.** It sums the whole step's local movement, so
   one splashing body throttles the level solve for *every* body in the scene. A
   per-body gate (recent per-body movement) would be more correct; not implemented.
3. **Shared-cavity bodies are resolved by first-claim.** If two water-disconnected
   bodies share one air cavity *below* both their surfaces, the first-labeled body
   claims the shared cells; the other is under-allocated. The surface-height bound
   makes this correct for the standard cases (verified: an isolated basin next to a
   deeper empty basin keeps 100% of its water; a ledge puddle correctly spills into
   a lower basin), but pathological multi-puddle layouts can mis-level.
4. **Sleeping still needs the labeling pass to notice a body is level.** A pool
   with one jittering surface cell wakes its chunk and forces a full body+cavity
   flood that step even though relaxation then finds `E < LevelEps` and does
   nothing — inherited from #6.
5. **Trapped pocket behind a lip — D drains water it should retain (found by the
   falsification harness, `design/SUFFICIENCY_TEST.md`).** D fills the cavity
   *globally bottom-up* with the body's volume `V`, which implicitly assumes the
   cavity is a single monotone basin. On `ledge`/staircase geometries a connected
   body can have a *higher* sub-pocket held up by an internal lip that does not
   drain to the global bottom. D's bottom-up fill puts that water at the low
   global surface instead of leaving it perched behind the lip, so the read-off is
   **wrong** (measured: 43/1100 scenes, `ledge` family, TV up to ~99 cell-masses;
   `artifacts/case_trap_c4_catch.png`). This is *distinct* from mode 3 (shared
   cavity): here it is one body, one cavity, but a non-monotone floor. The cheap
   detector is a monotone-drainage BFS from the filled region (the certificate's
   **C4**, a Prop-2 enabledness check); geometric checks that only test
   connectivity of the fill (C1) and no-shared-cavity (C3) do **not** catch it.
   Note these are all **non-quiescent** states — a genuinely settled D body cannot
   have such a pocket because the `top` bound tracks its true surface — so the
   failure is invisible to a quiescence test but real for D's *instantaneous*
   read-off. Not fixed in D itself; only detected by the certificate.

**➡ Failure modes 2 and 4 are now fixed, and D's per-frame cost is amortized 2–22×,
by the D_fast variant **F** — see §1★★ below.**

---

## 1★★. D_fast: making D cheap with the sufficiency certificate

D was correct but expensive: a full connected-components + cavity flood per active
body *every frame*, peaking ~1.3× the whole grid on a dam-break (§1★).

> **Audit note (Finding #2).** The first draft claimed a single model **E** was
> *both* bit-for-bit identical to D *and* cheap. It isn't — the two are in tension.
> The code now separates them: **E = E_exact** reproduces D **frame-for-frame**
> (verified, `test_frame_equality.js`) but, because frame-identity forces the full
> relabel each frame, is **not** cheaper than D. **F = D_fast** is the cheap variant
> below; it is **not** bit-identical to D (U-tube Δh 0.054 vs 0.066, a *similar
> hydrostatic outcome*). The speedups here are **F's**.

Variant **F** (`js/models.js` `stepF` / `relaxLevelsFast(..., exact=false)`; full
write-up in `design/PERF.md`) reaches a similar hydrostatic result to D (U-tube
Δh≈0.05, mass 0.000%, flat surfaces) but makes the flood *rare* by using the RPRM
certificate as the license to skip it:

- **Certificate-gated recompute.** Each body caches its `(cells, cavity, target,
  P_geo verdict)` across frames. A body whose certificate `P_geo=C1∧C3∧C4` holds
  has a read-off that is invariant under its own motion, so it **reuses the cache
  and just relaxes — no flood**. Only *uncertified* (splashing/perched/merging)
  bodies re-flood every frame. This is the literal #2→#1 link: the certificate's
  "safe while moving" certification rate becomes skipped work. (It is *also* what
  makes F diverge from D cell-for-cell — see failure mode 4.)
- **Incremental body tracking** (fixes the spirit of §6): labels persist; a
  settled, undisturbed body costs O(1); only externally-disturbed or
  topology-changed components are relabelled. Whole-grid disturbance degrades to
  D's full flood — the honest fallback.
- **Per-body disturbance gate** (fixes §1★ mode 2): each body is gated by its own
  recently-moved mass, so one splash no longer throttles every other body.
- Fixes §1★ mode 4 (flood-a-whole-pool-to-notice-it's-level): a settled body is
  skipped in O(1); surface jitter no longer forces a full flood.

**Measured (grid 100×64, `experiments/perf_experiment.py`).**

| scenario | avg flood cells/step D → F | peak flood D → F | avg ms/step ↓ | mass err | U-tube Δh |
|---|---|---|---|---|---|
| U-tube | 6.9 → **0.6** (11.9×) | 1477 → 1369 (1.08×) | 1.16× | 0.000% | **0.05** |
| dam | 176.8 → **8.0** (22.2×) | 8361 → 8356 (**1.00×**) | **1.82×** | 0.000% | — |
| basin | 64.1 → **29.3** (2.2×) | 6226 → 6226 (1.00×) | 1.00× | 0.000% | — |
| multi-body stress | 109.5 → **5.0** (21.7×) | 4889 → 4703 (1.04×) | 1.59× | 0.000% | — |

**Did the certificate itself pay off? Yes.** Ablating the certificate-moving-skip
(pure dirty-tracking + quiescence) still re-floods every moving body: the
certificate buys an **extra 6.8–8.7×** on dam/stress/U-tube on top of dirty-tracking
(only 1.3× on the fast-settling basin). See `design/PERF.md` §4.

**New failure modes (honest).**
1. **Peak is NOT reduced** — the worst single frame is still a full flood; F only
   amortizes it. The dam-break's violent phase is uncertifiable, so the certificate
   saves nothing *during* it (only after it calms). If a scene never settles and
   keeps all water moving uncertifiably, F ≈ D.
2. **Fast split/merge triggers the full-flood fallback** (re-flood the whole
   affected component that frame). A continuously fragmenting splash could drive it
   every frame; our benchmark scenes stay ~one body per container, so it fires only
   in the opening frames. The "22× on dam" is *this* dam-break, not a universal claim.
3. **Cache-relax is O(cavity)/frame**, so slow-flattening wide surfaces (basin,
   #4) get the flood-cell reduction but little wall-clock win — the cost just moves
   from flooding to relaxing.
4. **F is not frame-identical to D.** F's incremental, certificate-skipping flood
   claims shared cavities in a different order than D's single global pass, so on
   fragmenting scenes F diverges from D cell-for-cell (hydrostatically equivalent,
   but ~1.5 cell-masses over 1500 steps on basin). This is *the* reason the exact
   reference (E_exact) has to fall back to a full row-major relabel and thus cannot
   be cheaper than D (Finding #2).
5. **Interactive brush / sand↔water** changes now flow through eager `grid.set`
   cache invalidation (Finding #4) plus the volume-drift check and a settled-record
   `CacheTTL`≤128 backstop, so an edited body is re-flooded rather than left stale;
   no effect on the headless numbers. See `experiments/test_cache_invalidation.js`.

---

## 2. Binary models never come to rest (update-order limit cycle)

**What happens.** A and B **never quiesce** on any scenario (`settle` = "jitter
(never)" in the table; residual 44–90 changed cells/step *forever*, see
`settle_*.png`). Watch `basin_A.gif`: the pool keeps shuffling cells sideways
indefinitely even though it looks settled.

**Why.** Binary water is one-cell-per-parcel with a horizontal "spread" rule. On a
flat surface a cell sees an equal-height neighbor, moves into it, the neighbor
moves back next scan, etc. — a 2-cycle. Because we scan the grid in an order, the
choice of who-moves-first also injects a directional bias.

**How cheap fixes fail.** We already alternate the horizontal scan direction each
frame (`Grid.frame & 1`), which cancels the *gross* left/right drift but not the
local 2-cycle. Randomizing the scan removes bias in expectation but replaces it
with noise and destroys determinism (bad for reproducibility). There is no clean
"is this parcel at rest?" test for a binary cell because rest is a property of the
*continuous* height field it is only crudely sampling.

**What a good solution needs.** A continuous per-cell amount (model C) so "at rest"
becomes "net flow < ε", or explicit velocity with a static-friction threshold.

---

## 3. Surface limit-cycle / checkerboard jitter in the mass model (and the deadband that hides it)

**What happens.** Even model C does not fully settle: ~60–80 cells keep exchanging
tiny amounts of mass at the free surface indefinitely, and the surface renders
slightly "foamy" (speckled partial-mass cells — visible in `utube_C.gif`).

**Why.** The down-flow (which over-fills a cell) and the up-pressure flow (which
empties it) can form a small 2-cycle at the surface, and horizontal equalization
between near-equal partial cells oscillates around the mean.

**How cheap fixes fail / the trade-off we chose.** We added a **flow deadband**
(`MinFlowCutoff`: flows below it are zeroed) plus a **sleep threshold**
(`SleepEps`). This lets cells actually go to sleep (the whole active-cell scheme
depends on it) but at a cost:
- too small → nothing ever sleeps, cost stays high;
- too large → water freezes with a **permanent** neighbor imbalance (visible
  stair-steps) and the U-tube plateaus *further* from level (deadband is a second,
  independent cause of the #1 plateau).
This is a direct instance of the RPRM "how economical can the retained state be
before the answer degrades" question — the deadband is the economy knob and it
trades equalization accuracy for the ability to stop computing.

**What a good solution needs.** Semi-implicit / averaged updates (solve the local
exchange to its fixed point instead of iterating toward it), or a proper rest
detector decoupled from the flow magnitude.

---

## 4. Wide free surfaces flatten *very* slowly and transiently "mound"

**What happens.** Drop a column into a wide basin (`basin_C.gif`) and C first
builds a **mound** in the middle that only relaxes to flat over thousands of
steps. (`surface std` at the measured step is comparable to A/B precisely because
C has not finished flattening.)

**Why.** Same root as #1: flattening is driven by surface water trickling down the
slope, not by pressure at the base pushing the mound outward. Two full cells at
the bottom of the mound don't exchange, so the base of the pile is "load-bearing"
and slow to spread.

**How cheap fixes fail.** Increasing the horizontal flow constant speeds spreading
but overshoots and adds surface waves. **What a good solution needs:** the same
level-field idea as #1.

---

## 5. Mass leaks at active-sleeping boundaries (a real bug I hit — and fixed)

**What happens (before fix).** Model C lost **up to ~2.5%** of its water in the
violent scenarios (dam, U-tube). Mass is supposed to be conserved *exactly*.

**Why.** The active-cell scheme only copied/committed the double-buffer for cells
in *awake* chunks. When an awake cell pushed flow into a **sleeping** neighbor, the
outflow was committed (source lost mass) but the inflow into the sleeping cell was
never committed (it was dropped). Every awake/asleep boundary leaked.

**Fix + lesson.** Dilate the awake set by one chunk (a **halo**) for the copy and
commit passes, while still *emitting* flow only from awake cells (`Grid.computeHalo`,
`forEachHaloRow`). Mass error went to **0.000%** everywhere. The lesson generalizes:
*any* sleeping/active scheme with cell-to-cell exchange must retain a one-cell halo
or it silently violates conservation. In RPRM terms, the halo is the *minimal
sufficient* extra state — retain less and the invariant (mass) breaks.

---

## 6. Chunk-granular sleeping keeps a whole pool awake

**What happens.** The active-cell scheme is a big win for *idle/empty* regions
(basin active-cell cost falls from 100% to ~22–25%, `active_cost.png`), but a
*settled pool* stays partly awake: one jittering surface cell (see #3) wakes its
whole 8×8 chunk plus 8 neighbors.

**Why / trade-off.** Coarse chunks amortize bookkeeping but have poor granularity;
we moved 16→8 to let a deep pool's still interior sleep. Smaller chunks = finer
sleeping but more per-chunk overhead; true per-cell sleeping needs a per-cell wake
set/queue.

**What a good solution needs.** Per-cell or per-column sleep flags, or a "settled
body" merge that treats a quiescent connected pool as a single sleeping object.

---

## 7. Evaporation threshold leaks mass; lowering it leaves foam

Cells below `MinMass` are zeroed (treated as dry). In violent scenes this created a
slow mass drain (part of the pre-fix #5 numbers). Lowering `MinMass` (1e-4 → 1e-5)
cut the drain but leaves near-invisible films of water lingering (foam-like specks).
There is no free lunch: a hard cutoff either loses mass or accumulates dust.

---

## 8. No viscosity, surface tension, or cohesion → "teleporting" water

Model A's horizontal spread scans up to `A_FLOW` (=4) cells and moves a parcel there
in a single step — water visibly *teleports* sideways to find a hole. None of the
models bead droplets, resist shear, or form a meniscus. Cheap viscosity (blend
velocity with neighbors) is easy for B but fights its splashiness; surface tension
needs a curvature estimate (non-local).

## 9. Sand↔water coupling is a crude swap (no real buoyancy)

Sand sinks by *swapping* with the water cell below it; water is teleported up one
cell with zero momentum. It looks plausible but there is no density-driven pressure
coupling, no drag, no settling velocity — drop a lot of sand into deep water and the
lack of momentum shows.

## 10. Determinism vs symmetry

We chose deterministic alternating scan order. It is reproducible (good for a
research harness and for netcode) but not perfectly left-right symmetric on any
single frame. Random tie-breaking would be symmetric in expectation but
nondeterministic. You cannot have all three of {cheap, deterministic, symmetric}
with a sequential scan.

## 11. Performance cliff when everything moves at once

The active-cell scheme gives ~free idle regions, but a full-grid disturbance
(dam break) pushes the active fraction toward 100% *and* model C does 3 passes per
step (copy / flow / commit) plus the halo, so its worst-case per-cell cost is ~3–4×
A's. Dam-break residual activity for C is ~370 cells/step vs ~90 for A. There is no
level-of-detail fallback (e.g. coarsen deep still water) to cap the worst case.

---

## If I had one more work-block, in priority order
1. ~~**A connected-component level field for #1/#4**~~ — **DONE (model D, §1★).**
   It is the direct analogue of RPRM's "change representation to expose the
   question you actually need to answer" (the question is *what is this body's
   target level?*, which the local rule can't see). It fixed #1/#2/#3/#4 at once;
   the remaining work is making the fix *local-looking* again (§1★ failure mode 1).
2. **Per-body disturbance gate** (§1★ failure mode 2) so multi-body scenes don't
   let one splash freeze every other body's leveling.
3. **Route the level correction through the connection graph** so the U-tube far
   shaft visibly fills through the pipe instead of teleporting (trade some of D's
   O(1)-pass speed back for local causality / naturalness).
4. Per-column sleep for #6 (also cuts D's "flood a whole pool to notice it's
   already level" cost, §1★ failure mode 4).
