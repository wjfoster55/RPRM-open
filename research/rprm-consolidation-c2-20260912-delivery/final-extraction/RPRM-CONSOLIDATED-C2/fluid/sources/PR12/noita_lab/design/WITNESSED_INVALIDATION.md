# Witnessed cache invalidation for F (D_fast)

**For William.** This closes the highest-ranked "unused corpus concept" from
`design/RPRM_CORPUS_MAP.md` §3.1: replace F's *heuristic* cache guards — a fixed
`CacheTTL = 128` timer plus a volume-drift threshold — with **witnessed, minimal**
refresh triggers grounded in the will-corpus's `Fold → FutureTest → Five → Refold`
loop and its `successor_defect` / backward-localization discipline
(`RPRM-CORE-FORMALIZATION-01/fold.py`, `five.five`).

Read the honest verdict first: **this is not a speedup.** F's per-frame volume
check already catches every real invalidation, so the dominant flood cost is
unchanged. What changes is that invalidation becomes *principled* — every forced
re-flood now points at the exact cell that forced it, and the unprincipled
128-frame magic constant is gone. The measured payoff is the removal of **490
blind timer operations** that changed nothing, and a modest cut to the (small)
cache-relax term. It is a correctness/clarity result, not a performance one.

Everything is reproducible against the exact `js/` physics the demo runs
(`experiments/witnessed_invalidation.py`, driven headlessly through node). It is a
*mode* of F, not a replacement: `js/constants.js` `D.Invalidation` selects
`'heuristic'` (default, unchanged) or `'witnessed'`.

---

## 1. What F's heuristic guards were, and why they are heuristic

F (`D_fast`) skips model D's per-frame global flood by caching each certified
body's cavity + target levels and only *relaxing* off that cache. To stay correct
it must notice when a cached read-off has gone stale. The original (heuristic)
guards, from `design/PERF.md` / `TRUST_AUDIT.md` Finding #4, were:

- **`CacheTTL = 128` timer.** An active certified body is force-re-flooded at least
  every 128 frames; a settled/undisturbed body re-verifies its cavity volume every
  128 frames — *whether or not anything changed*. `128` is a magic constant chosen
  to bound "a brush edit we somehow missed"; it has no proof obligation behind it.
- **Volume-drift check.** Each frame, the O(cavity) cache-relax pass re-sums the
  body's mass and re-floods if it drifted (this catches external inflow/outflow,
  merges, and edits that touch the cavity).
- **Eager `grid.set()` edit list + orphan adoption** (already witnessed by
  construction — an edit *is* the witness).

The volume-drift check is already essentially witnessed. The **timer is the purely
heuristic part**: it does work on a clock, not on evidence.

## 2. The witnessed trigger (`successor_defect`)

Corpus map §3.1: *Fold* = our `C_body` cache; *FutureTest* = the refinement check;
*Refold* = the re-flood. The missing stage is the **witness**: when a fold would go
wrong, emit a *minimal witness* naming the coordinate that forces reopening
(`five.five` backward-localization).

In `js/models.js` the witnessed mode (`D.Invalidation === 'witnessed'`):

1. **Drops the timer entirely.** No active-body `CacheTTL` re-flood; no settled-body
   periodic re-verify. A settled undisturbed body is skipped in **O(1) forever** —
   it cannot change without a touch or edit, both of which fire a witness.
2. **Keeps the per-frame O(cavity) volume check** as the FutureTest. When it fires
   (drift detected), `recordSuccessorDefect()` backward-localizes the cause: it
   scans the body's cavity for the cell touched *this* frame (`_touchStamp === _touchGen`)
   carrying the largest mass delta (`_delta`), and emits a `successor_defect`:
   `{ frame, body id, cell (x, y), quantity: 'volume', delta }`. **That named cell
   is the witness** that the cached body-level read-off must be re-derived.
3. **Counts an honest completeness gap.** If the volume drifted but no touched
   cavity cell is found (a drift with no cell witness), it increments an
   `unwitnessed` counter rather than pretending the witness set was complete. On
   this suite `unwitnessed = 0` everywhere (see §4), i.e. the volume witness is
   complete: the only two ways the grid changes are `grid.set()` (→ edit list, a
   witness) and advection (→ touch list, from which the defect is localized).

## 3. Correctness (must be preserved — and is)

Same `js/` physics, only the guard differs. Both modes pass the mutation suite
identically (`node experiments/test_cache_invalidation.js` — 4 mutations ×
{heuristic, witnessed}, all `PASS`, max per-column |F−D| ≤ 0.062, mass |F−D| ≤
3e-2), and the scenario metrics match:

| scenario | mode | mass err % | U-tube Δh | avg flood | peak flood | avg cache-relax | skip % |
|---|---|---|---|---|---|---|---|
| basin | heuristic | 0.000 | – | 29.3 | 6226 | 5.8 | 96.9 |
| basin | witnessed | 0.000 | – | 29.3 | 6226 | 3.6 | 96.9 |
| utube | heuristic | 0.000 | 0.054 | 0.6 | 1369 | 8.8 | 99.9 |
| utube | witnessed | 0.000 | 0.054 | 0.6 | 1369 | 3.3 | 99.9 |
| dam | heuristic | 0.000 | – | 8.0 | 8356 | 81.5 | 99.9 |
| dam | witnessed | 0.000 | – | 8.0 | 8356 | 43.3 | 99.9 |
| stress | heuristic | 0.000 | – | 3.4 | 4703 | 39.4 | 99.9 |
| stress | witnessed | 0.000 | – | 3.4 | 4703 | 20.5 | 99.9 |

Mass error, U-tube Δh, and — critically — the dominant **flood** cost are
identical. Witnessed invalidation invalidates exactly as correctly as the
heuristic.

## 4. Invalidation accounting (the point)

The heuristic spends **blind timer work** — re-floods/re-verifies forced purely by
the 128-frame clock, changing nothing. The witnessed policy spends **zero** blind
work; every re-flood it does carries a **named cell**.

| scenario | heuristic timer re-floods | heuristic timer re-verifies | witnessed re-floods (all named) | unwitnessed drift |
|---|---|---|---|---|
| basin | 0 | 15 | 5 | 0 |
| utube | 0 | 46 | 1 | 0 |
| dam | 0 | 15 | 0 | 0 |
| stress | 0 | 414 | 0 | 0 |

Totals: heuristic **490** blind timer operations across the suite; witnessed **0**,
with **0** unwitnessed drift (witness set complete). A concrete
`successor_defect`: on `basin`, frame 4, body 5, **cell (x=61, y=62)** changed by
Δmass = 0.295 — that cell *is* the witness that forced the re-flood. The heuristic
cannot point at a cell; it re-floods on a clock.

Note the blind work here is entirely the *settled re-verify*; the active-body
`CacheTTL` re-flood never fired on these scenes because bodies settle in fewer than
128 active frames. That is itself evidence the timer is doing nothing useful.

![witnessed vs heuristic](../artifacts/witnessed_invalidation.png)

## 5. Honest verdict

- **Correctness preserved.** Witnessed matches heuristic on mass error, U-tube Δh,
  the mutation suite (both modes), and — the dominant term — flood cost. `0`
  unwitnessed drift: the volume witness set is complete on this suite.
- **Blind work removed, not flood work.** The heuristic's **490** timer-driven
  operations that changed nothing become **0**. But F's per-frame volume check
  already caught the real invalidations (`TRUST_AUDIT.md` predicted this), so
  witnessed does **not** beat heuristic on average/peak flood cost — the expensive
  term is identical. It does cut the cheaper *cache-relax* work by dropping the
  blind settled re-verify (dam 81.5→43.3, stress ≈2×), but that term is small and
  wall-clock barely moves. **We do not sell this as a speedup.**
- **The value is principled, not cheaper.** Invalidation is now *minimal and
  witnessed*: every re-flood names the exact cell that forced it (a
  `successor_defect`), and the unprincipled 128-frame magic constant is gone. This
  is the corpus's `Fold → FutureTest → Five → Refold` discipline — name the
  witness, backward-localize — applied to F's cheapest, most heuristic component.
  It also converts a "we think the cache is stale" timer into "here is the minimal
  witness that it is."

## 6. How to run

```
node    experiments/test_cache_invalidation.js          # both modes, mutation suite
node    experiments/test_cache_invalidation.js heuristic # heuristic only
.venv/bin/python experiments/witnessed_invalidation.py   # table + figure (this doc)
```

`D.Invalidation` in `js/constants.js` selects the mode for the demo/harness;
`'heuristic'` remains the default so nothing downstream changes unless opted in.
