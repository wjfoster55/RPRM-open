# Trust audit of PR #9 (model E "D_fast" + RPRM sufficiency certificate + oracle)

**For William.** This is not a feature push. A sharp external review of PR #9
(commit `f57f3e0`) raised five concerns about the fluid-simulation work. This
document reproduces each concern, fixes what was broken, **re-validates every
affected number honestly**, and states plainly which published claims **changed**.
Intellectual honesty is the whole point: where a fix weakens a prior headline, the
weaker number is reported here, in bold, up front.

## Claims that CHANGED (read this first)

1. **"Model E is bit-identical to D *and* cheap" — RETRACTED.** These two
   properties are in tension and cannot both hold for the cache/skip design. The
   code is now split: **E_exact** is verified frame-for-frame identical to D but is
   **not cheaper than D**; **F** is the cheap variant (2.2–22× less flood) but is
   **not bit-identical** to D (U-tube Δh 0.054 vs D's 0.066 — a *similar hydrostatic
   outcome*, not equality). See Finding #2.
2. **Ground-truth exact-read-off rate dropped 835/1100 → 816/1100** (75.9% → 74.2%)
   under the corrected spill oracle. **The decisive certificate number survives:
   `P_geo` still has FP = 0**, now at a 46.8% certification rate. See Finding #1.
3. **"Decidable certificate" → "sound-but-incomplete acceptance predicate."** The
   predicate does not *decide* sufficiency; it is a conservative sufficient
   condition that rejects 320 within-tolerance scenes. "Exact" everywhere means
   *agreement within a 1 cell-mass total-variation tolerance* (`TV < 1.0`), not
   bit-equality. See Finding #3.
4. **"C4 is proven necessary" → "removing C4 admits false positives in the tested
   geometries."** Not a universal necessity claim. See Finding #3.
5. **Dynamic-frontier claim softened** from a proved necessity to a *defensible
   insufficiency conjecture*. See Finding #5.

Nothing below is hidden: the falsification harness, the oracle self-test, the
frame-equality check, and the mutation tests all run from the commands in each
section.

---

## Finding #1 (most important): the oracle had a spill/redistribution bug

**Concern.** `truth_solver.py` — the *independent* ground-truth against which D's
read-off is judged — found a single water height whose reachable region holds the
body volume, then rescaled to conserve mass. But reachable capacity **jumps
discontinuously** when the level crosses a divider into another basin, so the
rescale becomes a large, physically wrong redistribution. Mass stays exact, so
mass-conservation does **not** catch it — a silent oracle error that would
mis-grade the entire sufficiency experiment.

**Reproduction (confirmed).** Two-compartment container: left compartment holds 6
units to the divider crest; right compartment wider and empty; 8 units placed in
the left. Correct quasistatic answer: **6 left / 2 right**. The PR#9 oracle found a
single global height, saw reachable capacity jump 6 → 18 as the level cleared the
crest, and filled ×8/18 → **≈2.667 left / 5.333 right** (total mass 8.000, so
mass-conservation passed while the distribution was wrong). Encoded as the headline
case in `experiments/test_spill_regression.py`.

**Fix.** `truth_solver.py` now implements an explicit quasistatic spill/retention
contract (`_solve_level` / `_fill_region`): fill the lowest reachable basin to its
crest, then spill **only the excess** into connected lower basins, iterating with a
min-heap frontier ordered by bottom-height. A sub-basin that fills to its own crest
merges back and the pool keeps rising. Retention (a lip that should hold water) and
spill (excess crossing a crest) are both handled explicitly, so capacity no longer
jumps.

**Regression suite** (`experiments/test_spill_regression.py`, all PASS):

| scene | expectation | result |
|---|---|---|
| two_compartment | 6 left / 2 right | **6.000 / 2.000** |
| cascade_nested (3 basins) | 6 / 6 / 2 | 6.000 / 6.000 / 2.000 |
| utube | \|lh−rh\| = 0 | 0.000 |
| tilted_terraces | 6 retained / 6 spilled | 6.000 / 6.000 |
| retention_no_spill | right stays dry | 0.000 |

The oracle's own analytic self-test (`truth_solver.py`) still prints **ALL PASS**.

**Re-validation (the honest part).** Re-ran the full 1100-scene falsification with
the corrected oracle (`experiments/sufficiency_test.py 110`):

- Ground truth: **816/1100 (74.2%)** within-tolerance D read-offs — **down from
  835/1100 (75.9%)**. The corrected oracle reclassifies 19 spill scenes (mostly
  `ledge`/`multipocket`) as *not* exact.
- **`P_geo` still certifies none of those 19**, so its **false-positive count is
  unchanged at 0**. The zero-FP headline holds.

New confusion matrix (corrected oracle):

| verdict | cert% | **FP** | FPrate% | recall% | TP | FN | TN |
|---|---|---|---|---|---|---|---|
| **P_geo = C1∧C3∧C4** | **46.8** | **0** | 0.00 | 63.1 | 515 | 301 | 284 |
| P_full = C1∧C2∧C3 | 1.7 | 0 | 0.00 | 2.3 | 19 | 797 | 284 |
| P_noC2 = C1∧C3 | 50.7 | 43 | 7.71 | 63.1 | 515 | 301 | 241 |
| C3 alone | 66.5 | 216 | 29.55 | 63.1 | 515 | 301 | 68 |
| C4 alone | 62.5 | 173 | 25.15 | 63.1 | 515 | 301 | 111 |
| baseline quiescent (`active≤4`) | 3.4 | 0 | 0.00 | 4.5 | 37 | 779 | 284 |

**Net:** the oracle bug was real and is fixed; the exact-rate headline dropped by
19 scenes; the certificate's decisive property (0 false positives, ~14× the
certification rate of naive quiescence) **survived the correction**.

```bash
/workspace/.venv/bin/python noita_lab/experiments/truth_solver.py           # self-test
/workspace/.venv/bin/python noita_lab/experiments/test_spill_regression.py  # regression
/workspace/.venv/bin/python noita_lab/experiments/sufficiency_test.py 110   # re-validate
```

---

## Finding #2: model E was not bit-identical to D

**Concern.** D throttles relaxation by a **scene-wide** moved-cell count; PR#9's E
used **per-body** moved-mass on rebuilt bodies and relaxed cached bodies with the
full parameter **without the disturbance gate**. Hence the U-tube Δh differed
(D≈0.066 vs E≈0.054) — E was a *behavior change*, not an accelerator of the same
computation.

**What we found (and the honest tension).** Making the gate scene-wide was
necessary but **not sufficient** for frame-identity. The deeper issue: D relabels
**all** bodies in one global row-major pass, fixing the cross-body cavity
first-claim order within a frame. Any cache that **skips** re-flooding some bodies
(the certificate-moving-skip that makes D_fast cheap) floods the remaining bodies
in a **different order**, so a shared cavity is claimed differently and the states
diverge and chaotically amplify on fragmenting scenes. **You cannot have both
frame-identity to D and the incremental-skip speedup in general.**

**Resolution — two honestly separated models:**

- **E = E_exact** (`stepE` / `relaxLevelsFast(..., exact=true)`). Reproduces D's
  global relabel exactly: each relabel frame it re-floods every awake water cell in
  strict row-major seed order (D's `forEachActiveRow` scan). The only work it skips
  is fully-asleep chunks — which D skips too. **Verified frame-for-frame identical
  to D** across basin/utube/dam/stress (max per-cell mass deviation **0.0**).
  Consequence: E_exact does D's flood work every frame and is **not a speedup**
  (avg-flood ÷ D ≈ **1.00×**).
- **F = D_fast** (`stepF` / `exact=false`). The certificate-cached variant: per-body
  gate, certificate-moving-skip, orphan adoption. **This is where the speedup lives
  (2.2–22×)** and it is **not** frame-identical to D.

**Frame-equality evidence** (`experiments/test_frame_equality.js 1500`):

| scenario | max \|mass_E − mass_D\| | type-mismatch cells | max \|mass_F − mass_D\| |
|---|---|---|---|
| basin | 0.0 | 0 | 1.459 (F diverges, expected) |
| utube | 0.0 | 0 | 1.000 |
| dam | 0.0 | 0 | 1.715 |
| stress | 0.0 | 0 | 1.637 |

**Redone certificate cost ablation** (`experiments/perf_experiment.py`, D vs
E_exact vs F). E_exact confirms it is not a speedup; F carries it; the certificate's
own contribution is measured on F:

| scenario | E_exact avg flood ÷ D | F avg flood ↓ vs D | dirty-track ↓ (D→F_noCert) | **certificate ↓ (F_noCert→F)** |
|---|---|---|---|---|
| basin | 1.00× | 2.2× | 1.7× | **1.3×** |
| utube | 0.99× | 11.9× | 1.5× | **8.1×** |
| dam | 1.00× | 22.2× | 3.3× | **6.8×** |
| stress | 1.00× | 21.7× | 2.5× | **8.7×** |

The certificate's 6.8–8.7× contribution (the PR#9 headline) is **real, but it
belongs to F, not to a bit-identical model.** The per-body-gate faster-settling
behavior is preserved intact as variant F, deliberately renamed so the exactness
claim (E) is never conflated with the speed change (F).

```bash
node noita_lab/experiments/test_frame_equality.js 1500
/workspace/.venv/bin/python noita_lab/experiments/perf_experiment.py
```

---

## Finding #3: over-strong wording, tightened to what is measured

| was | now |
|---|---|
| "exact" / "exactly sufficient" | "agree within a **1 cell-mass total-variation** tolerance" (`TV < 1.0`) |
| "bit-identical" / "bit-for-bit" (of the cheap model) | reserved for **E_exact** with **verified frame equality**; F is a "**similar hydrostatic outcome**" |
| "decidable certificate" / "decide exactly" | "a proposed **sound but incomplete** acceptance predicate (misses **320** harness-acceptable scenes), computable and terminating" |
| "C4 proven necessary" | "**removing C4 admits false positives in the tested geometries**" (not universal) |
| "coverage" (accept-fraction) | "**certification rate**" (William's framework reserves *coverage* for audit obligation-coverage) |

Edited in `SUFFICIENCY_TEST.md`, `PERF.md`, `PROBLEMS.md`, `RPRM_FLUIDS.md`,
`README.md`, and the harness display strings (`sufficiency_test.py`), so the
regenerated `artifacts/sufficiency_results.md` and plots use *certification rate*.

---

## Finding #4: cache-invalidation hole on settled bodies

**Concern.** The `≤128-frame refresh` backstop applied only to **active** records; a
**settled** (non-dirty) record skipped the volume check entirely, so a settled body
edited by a brush could never invalidate. `grid.set()` woke the chunk but did **not**
touch the body cache.

**Fix.**
- `grid.set()` now records each edited cell (`_editList`). The level solve
  invalidates the **owning body and its 4-neighbour bodies** of every edit (covers
  split, merge, and mass-preserving shape change) and queues freshly-painted orphan
  water for flooding.
- **Settled records** now re-verify their cavity volume at least every `CacheTTL`
  frames (the settled backstop), so any edit that somehow escapes the eager path is
  caught within 128 frames rather than never.

**Mutation tests** (`experiments/test_cache_invalidation.js`) — F must converge to D
(the cacheless oracle) after each edit. All **PASS** (per-column water-mass match;
tolerance 0.75 cell-mass):

| mutation | max per-column \|F − D\| | verdict |
|---|---|---|
| paint_into_settled | 0.056 | PASS |
| split_wall | 0.032 | PASS |
| merge_pools | 0.062 | PASS |
| mass_preserving_move | 0.054 | PASS |

**Honest nuance.** These four also pass with the eager fix *disabled*, because the
pre-existing machinery (advection touch-tracking + awake-chunk scan + the
volume-drift check on every non-settled relaxation) already self-heals any edit
that **moves water** — and every one of these mutations moves water. The residual
hole the fix uniquely closes is narrow: a **constant-cavity-volume topology change**
(e.g. a wall inserted mid-body that displaces exactly its own volume) applied while
a body is dirty, where the volume-drift check would not fire. The fix makes
invalidation **eager and explicit** and bounds staleness for settled records; it is
correct and defensive, but the review's implication that the hole silently produces
wrong *simulation output* today is not borne out by the tests — the drift check was
already guarding the output. We report this rather than overselling the fix.

```bash
node noita_lab/experiments/test_cache_invalidation.js
```

---

## Finding #5: the dynamic-frontier claim, softened

**Concern.** `RPRM_FLUIDS.md` asserted that dynamic incompressible questions
*necessarily require* a global solve — an impossibility claim we have not proved.

**Fix.** §3.1 and the H5 hypothesis now frame it as a **defensible insufficiency
conjecture**: *no known purely-local representation is exactly sufficient for the
dynamic incompressible receiver* (every surveyed local method is secretly
compressible; the exact methods all pay a global elliptic solve). We explicitly do
**not** claim to have proved necessity, and we keep it falsifiable: exhibiting an
exactly-incompressible, purely-local dynamic scheme would refute the conjecture.

---

## Reproduce everything

```bash
# Finding #1 — oracle + regression + re-validated sufficiency
/workspace/.venv/bin/python noita_lab/experiments/truth_solver.py
/workspace/.venv/bin/python noita_lab/experiments/test_spill_regression.py
/workspace/.venv/bin/python noita_lab/experiments/sufficiency_test.py 110

# Finding #2 — frame equality + redone cost ablation
node noita_lab/experiments/test_frame_equality.js 1500
/workspace/.venv/bin/python noita_lab/experiments/perf_experiment.py

# Finding #4 — cache-invalidation mutation tests
node noita_lab/experiments/test_cache_invalidation.js
```

Artifacts land in `noita_lab/artifacts/` and are mirrored to
`/cursor/stores/self/artifacts/`. No raw corpus is committed.
