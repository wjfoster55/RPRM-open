# Making model D cheap — D_fast (E_exact and variant F)

**For William.** Model D fixed the hydrostatics (U-tube Δh→0, mass 0.000%) but was
expensive: every frame it ran a full connected-components flood + cavity flood per
active body, peaking at ~1.3× the whole grid on a dam-break (`PROBLEMS.md` §1★).
This document is the "make it cheap" track. It uses the RPRM sufficiency
certificate (`js/certificate.js`, `design/SUFFICIENCY_TEST.md`) as the **license to
skip the expensive recompute**, and reports the real speedup — including where it
does *not* help, and where a claim from the first draft did not survive audit.

Everything is reproducible and measured against the exact `js/` physics the demo
runs (driven headlessly through node). See **§6 How to run**.

> **Audit correction (read this first).** The first draft of this document
> claimed a single model **E** was *both* bit-for-bit identical to D *and* cheap.
> That is not true, and the two properties are in tension. Reproducing D's global
> relabel bit-for-bit requires re-flooding every awake body in the same row-major
> order D uses, which is exactly the work the cache is trying to skip. So the code
> is now split into two honestly-separated models:
>
> - **E = E_exact** — the cache/skip machinery constrained to reproduce D's global
>   relabel **exactly**. Verified frame-for-frame identical to D across
>   basin/utube/dam/stress (`experiments/test_frame_equality.js`, max per-cell
>   deviation `0.0`). Because frame-identity forces the full relabel each frame,
>   **E_exact does essentially D's flood work — it is a faithful mirror, not a
>   speedup** (see §3: `E avg flood ÷ D ≈ 1.00×`).
> - **F = D_fast** — the certificate-gated variant that actually skips work
>   (certificate-moving-skip + orphan adoption + per-body gate). **This is where
>   the speedup lives**, and it is **NOT** frame-identical to D: it reaches a
>   hydrostatically equivalent result but with small deviations on fragmenting
>   scenes (U-tube Δh 0.054 vs D's 0.066). The speedups below are F's.

---

## 1. What the two models keep and change

Both E_exact and F keep model D's physics ingredients: the same incompressible
local advection, the same body+cavity flood, the same bottom-up read-off, and the
same mass-conserving matched relaxation. They differ only in *how often* the
expensive flood runs and *whether* they match D cell-for-cell.

**E_exact (`stepE` / `relaxLevelsFast(..., exact=true)`).** Each relabel frame it
clears the body cache and re-floods every awake water cell in strict row-major
seed order — literally D's global relabel, expressed through the cache
bookkeeping. The only work it can skip vs D is fully-asleep chunks, which D skips
too (`forEachActiveRow`). Hence it is provably frame-identical to D and provides no
meaningful speedup. It exists to prove the relaxation rules are D's, exactly.

**F = D_fast (`stepF` / `relaxLevelsFast(..., exact=false)`).** This is the cheap
variant:

1. **Certificate-gated recompute (the #2→#1 payoff).** Each body carries a cached
   summary — its cells, its cavity, its target level, and its RPRM certificate
   verdict `P_geo = C1∧C3∧C4`. When `P_geo` holds, the read-off `(V, cavity,
   target)` is treated as invariant under the body's *own* motion, so a **certified
   moving body reuses the cache and just relaxes — no flood.** Only bodies that are
   **uncertified** (splashing, perched, mid-merge) are re-flooded. *This skip is
   exactly what breaks frame-identity with D* (it reorders shared-cavity
   first-claim; see §5.4), which is why it lives in F and not in E_exact.
2. **Incremental / dirty-region tracking.** Connected-body labels (`_bodyId`)
   persist across frames. Only bodies disturbed this frame or whose topology
   changed are relabelled; a **settled, undisturbed body costs O(1)**.
3. **Per-body disturbance gate.** F gates each body by *its own* recently-moved
   mass (D, and therefore E_exact, use a single scene-wide gate). A still pool next
   to a splash equalizes at full speed — a deliberate behavior change, hence not
   bit-identical.

Guardrails that keep F correct:

- **Volume-drift check.** Before trusting a cached target, F sums the body's volume
  over its cached cavity in the same pass as the relaxation; if it drifted (a
  stream poured in, a brush edit, a merge) it re-floods and re-targets.
- **Eager edit invalidation (`grid.set`).** A brush paint/erase records the edited
  cell; the level solve invalidates the owning + 4-neighbour body and re-floods it
  (split/merge/mass-change). See `PROBLEMS.md` and the trust audit, Finding #4.
- **Orphan adoption.** Advection spreading a body's own water into an adjacent
  cavity cell is recognised as internal instead of forcing a re-flood.
- **TTL backstop.** A certified *moving* body re-floods at least every
  `CacheTTL=128` frames; a **settled** body re-verifies its cavity volume at least
  that often too (the settled backstop added in Finding #4).

---

## 2. Results — correctness

E_exact is verified **frame-for-frame identical** to D; F reaches a
hydrostatically equivalent settled state but is *not* cell-identical.

| scenario | model | mass err % | U-tube Δh | frame-identical to D? |
|---|---|---|---|---|
| U-tube | D | 0.000 | 0.066 | — |
| U-tube | **E_exact** | 0.000 | **0.066** | **yes (0.0)** |
| U-tube | **F** | 0.000 | **0.054** | no (hydrostatically equiv.) |
| dam | D | 0.000 | — | — |
| dam | **E_exact** | 0.000 | — | **yes (0.0)** |
| dam | **F** | 0.000 | — | no |
| basin | **E_exact** | 0.000 | — | **yes (0.0)** |
| basin | **F** | 0.000 | — | no |

Frame-identity is checked by `experiments/test_frame_equality.js` (max per-cell
mass deviation E-vs-D = `0.0` on all four scenarios; F is shown diverging to
confirm the exactness claim is specific to E).

## 3. Results — cost

`flood cells/step` = connected-component + cavity cells visited by the level solve.
`cache-relax` = cavity cells F touches while relaxing off a cached target (no
flood). `skip%` = body-processings that skipped the flood.

| scenario | model | peak flood | avg flood | avg cache-relax | skip % | avg ms/step |
|---|---|---|---|---|---|---|
| basin | D | 6226 | 64.1 | 0.0 | 0.0 | 0.030 |
| basin | **E_exact** | 6226 | 64.3 | 0.0 | 0.0 | 0.040 |
| basin | **F** | 6226 | **29.3** | 5.8 | 96.9 | 0.028 |
| U-tube | D | 1477 | 6.9 | 0.0 | 0.0 | 0.012 |
| U-tube | **E_exact** | 1408 | 6.8 | 0.0 | 0.0 | 0.013 |
| U-tube | **F** | 1369 | **0.6** | 8.8 | 99.9 | 0.011 |
| dam | D | 8361 | 176.8 | 0.0 | 0.0 | 0.046 |
| dam | **E_exact** | 8356 | 176.2 | 0.0 | 0.0 | 0.058 |
| dam | **F** | 8356 | **8.0** | 81.5 | 99.9 | 0.026 |
| stress | D | 4889 | 109.5 | 0.0 | 0.0 | 0.034 |
| stress | **E_exact** | 4889 | 109.5 | 0.0 | 0.0 | 0.041 |
| stress | **F** | 4703 | **5.0** | 49.2 | 99.8 | 0.023 |

**Headline:**

| scenario | E_exact avg flood ÷ D | F avg flood ↓ vs D | F peak flood ↓ | F avg ms ↓ |
|---|---|---|---|---|
| basin | 1.00× | 2.2× | 1.00× | 1.18× |
| U-tube | 0.99× | 11.9× | 1.08× | 1.15× |
| dam | 1.00× | **22.2×** | 1.00× | **1.94×** |
| stress | 1.00× | 21.7× | 1.04× | 1.54× |

Read this honestly:

- **E_exact reads ~1.00× — it is not a speedup.** It does D's flood work every
  frame (that is the price of frame-identity). Its value is as the *reference* that
  proves the relaxation rules are D's, not as an optimization.
- **F's average / sustained flood cost drops 2–22×**, biggest on the dam-break
  (177 → 8 cells/step) and stress (110 → 5). Wall-clock ms/step drops up to
  **~1.9×** on the dam-break.
- **F's peak flood cost is essentially unchanged (1.00–1.08×).** F must label the
  scene at least once, and the single most expensive frame is a full flood. The win
  is that F pays that peak on *a handful of frames* then rides the certificate cache
  (`artifacts/perf_cost_dam.png`).
- **basin shows almost no ms win** because a wide basin flattens slowly: the body
  stays *active* many frames, so F's cost shifts from flooding to cache-relaxation
  (O(cavity) per frame). Honest.

<img src="../artifacts/perf_cost_dam.png" alt="dam: D floods every step, F floods once" width="640" />
<img src="../artifacts/perf_flood_bars.png" alt="avg and peak flood cells per scenario, D vs E_exact vs F" width="640" />

## 4. Did the certificate actually pay off? — yes, measured on F

The worry: maybe **dirty-region tracking alone** (skip settled bodies, re-flood
every moving one) gets all the savings and the certificate adds nothing. We test
this with an ablation `F_noCert` (`D.CertGate=false`): the certificate-moving-skip
is disabled, so every MOVING body is re-flooded and only SETTLED undisturbed bodies
are skipped (pure incremental tracking + quiescence).

| scenario | D avg flood | F_noCert avg flood | F avg flood | dirty-track ↓ (D→noCert) | **certificate ↓ (noCert→F)** |
|---|---|---|---|---|---|
| basin | 64.1 | 38.5 | 29.3 | 1.7× | **1.3×** |
| U-tube | 6.9 | 4.7 | 0.6 | 1.5× | **8.1×** |
| dam | 176.8 | 54.3 | 8.0 | 3.3× | **6.8×** |
| stress | 109.5 | 43.7 | 5.0 | 2.5× | **8.7×** |

The certificate is **load-bearing** for F: on the dam-break, stress, and U-tube it
buys an extra **6.8–8.7×** on top of plain dirty-tracking. The reason is exactly
the certificate's advertised strength: a body can be **moving yet have a stable
read-off** — a quiescence-only scheme re-floods it every frame; the certificate
lets it ride the cache. Note this is the same skip that makes F diverge from D
cell-for-cell (§5.4): the speedup and the loss of bit-identity are the *same*
mechanism, which is precisely why "bit-identical AND cheap" was not achievable.

On the **basin** the certificate adds only 1.3×, because the basin settles fast and
most savings come from settled-skip (dirty-tracking). Also honest.

## 5. New failure modes / where it breaks (honest)

1. **E_exact is not cheap.** Frame-identity with D costs D's flood every frame.
2. **Peak is not reduced (F).** The worst single frame is still a full flood; F only
   amortizes it. A scene that never settles and keeps *all* water moving
   uncertifiably sees little benefit.
3. **Fast split/merge → full-flood fallback (F).** A continuously fragmenting splash
   scene can drive F's fallback every frame, at which point F costs ≈ D. Our
   scenarios stay mostly one connected body per container. Treat "22× on dam" as
   *this* dam-break, not a universal claim.
4. **Shared-cavity first-claim differs from D (F).** D labels all bodies in one
   global pass, fixing cross-body cavity first-claim order within a frame. F labels
   incrementally and skips certified bodies, so two bodies sharing a cavity that are
   re-flooded on *different* frames claim it in a different order than D would.
   **This is the specific reason F is not frame-identical to D**, and it is why the
   exact variant (E_exact) has to fall back to a full row-major relabel. On
   fragmenting scenes this produces small deviations that can chaotically amplify
   (basin diverged from D by ~1.5 cell-masses over 1500 steps in testing) while
   staying hydrostatically equivalent.
5. **Interactive edits (F).** Brush edits now flow through eager `grid.set`
   invalidation (Finding #4) plus the volume-drift check and the settled backstop,
   so a body changed by a paint/erase is re-flooded rather than stranded.

## 6. How to run

```bash
# D vs E_exact vs F cost comparison + certificate ablation + plots:
/workspace/.venv/bin/python noita_lab/experiments/perf_experiment.py

# frame-for-frame equality check (E_exact must match D; F is shown diverging):
node noita_lab/experiments/test_frame_equality.js 1500

# cache-invalidation mutation tests (paint/split/merge/mass-preserving-move):
node noita_lab/experiments/test_cache_invalidation.js

# full model comparison incl. E and the multi-body stress scene (refreshes GIFs):
/workspace/.venv/bin/python noita_lab/experiments/run_experiments.py
```

Outputs: `artifacts/perf_table.md`, `artifacts/perf_cost_{dam,utube}.png`,
`artifacts/perf_flood_bars.png` — all mirrored to `/cursor/stores/self/artifacts/`.
