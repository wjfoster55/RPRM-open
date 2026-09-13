# The general mechanism behind the fluid result: receiver-relative reuse certificates

**For William. Written to survive the same honesty filter as `RPRM_FLUIDS.md`.**

*Stance.* In the fluids lab we found something that felt bigger than fluids: a
cheap water summary whose level you *read off*, a **decidable certificate** that
says the read-off is exact *right now* (even while the water is still moving), and
a cash-out where "certified ⇒ skip the recompute" bought a measured 2–22× with a
bit-identical result (`design/SUFFICIENCY_TEST.md`, `design/PERF.md`). This note
asks whether that is a *general mechanism* and formalizes it domain-agnostically.

Two hard commitments, both inherited from RPRM and from `RPRM_FLUIDS.md` §6:

- I state the mechanism in **William's own formal objects** (retained
  representation `r`/`C`, receiver question `q_K`/`Q`, and the two factorization
  propositions), citing `RPRM-CORE-FORMALIZATION-01/` (hereafter **RCF01**), so
  this is *RPRM*, not a parallel invention.
- I separate **genuine contribution** from **relabeling of existing results** as
  aggressively as §6 did. Spoiler, up front: the mechanism is **mostly a
  synthesis** of certifying algorithms, sound approximation, strong lumpability,
  and self-adjusting computation. The one defensible novelty is a *framing* — the
  **coverage-over-soundness, certify-under-motion** axis tied to a named receiver,
  plus **RPRM as the discipline that tells you which `(C, P)` to go looking for.**
  I will not oversell it past that.

All corpus references are by relative path; per the private-corpus rule I cite and
summarize William's material rather than pasting it.

---

## 1. The general mechanism, stated precisely

### 1.1 The abstract objects (grounded in RCF01)

RCF01's `FORMAL_BRIDGE_NOTE.md` §2 already fixes the vocabulary. I reuse it verbatim
in spirit and only rename where a domain-neutral word helps.

- **Carrier / state family `X`.** The admitted set of micro-states with their
  equality (RCF01 `CONCEPT_REGISTER.md`; `RPRM_FLUIDS.md` §1.1). Fluids: grid
  mass/velocity states. Cube: rational tables on `{0,1}^3` (`check_bridge.py`).
- **Receiver / question `Q : X → B`.** The declared family of questions a
  representation must preserve — RCF01's `q_K(·,π)` (`FORMAL_BRIDGE_NOTE.md` §2).
  *Sufficiency is always relative to a stated `Q`.* Fluids: `R_static` = resting
  surface level / underwater-mask (`SUFFICIENCY_TEST.md` §1).
- **Representation / summary `C : X → Z`.** The retained description — RCF01's
  `r` / `C_S` (restrict-to-`S`). Fluids: `C_body = (per-body volume, cavity
  geometry)`. The *point* of a good `C` is that it makes `Q` **intrinsic**: `Q`
  becomes a cheap read-off `h∘C` instead of a simulation.
- **Operations `T_a : X ⇀ X` with observation `O`.** Partial successors used to
  advance state; RCF01 `FORMAL_BRIDGE_NOTE.md` §2 and the Double-Stamp dwell graph
  (`check_bridge.py` CB11). Fluids: one settling/advection step.
- **Decoder `h`.** The read-off map with `Q = h∘C` when it exists.

### 1.2 The two propositions the mechanism stands on (cited, not re-derived)

Both are already proved/checked in RCF01 and in the Process Mechanics paper; I am
*using* them, claiming no new theorem here.

- **Prop 1 (question factorization).** A decoder `h` with `Q = h∘C` exists **iff**
  `C(x)=C(y) ⇒ Q(x)=Q(y)` (RCF01 `FORMAL_BRIDGE_NOTE.md` §2; `SUFFICIENCY_TEST.md`
  §2). "Two states with equal descriptions and different answers refute
  sufficiency."
- **Prop 2 (operational factorization).** To reuse `C` **as a state** through
  `T_a` with observation `O`, need for every `C(x)=C(y)`: (1) `O(x)=O(y)`; (2)
  `T_a` enabled at `x` iff at `y`; (3) `C(T_a(x)) = C(T_a(y))` (RCF01
  `FORMAL_BRIDGE_NOTE.md` §2; `SUFFICIENCY_TEST.md` §2). This is strictly stronger
  than Prop 1 — a **congruence / bisimulation / strong-lumpability** condition.
- **Repair when it fails.** `C'(x) = (C(x), Q(x))`, the least informative
  refinement (RCF01 §2; `SUFFICIENCY_TEST.md` §2). Fluids' forced fallback
  `C' = (C_body, velocity field)` is exactly this (`RPRM_FLUIDS.md` §3.3).

RCF01 also supplies the object that answers *"which representation change should I
seek?"*: the **least forward-closed retained set `S*`** — the smallest `C` that
survives a whole family of admitted operations/view-changes
(`FORMAL_BRIDGE_NOTE.md` §6 Proposition; `check_bridge.py` CB09). That proposition
is the design-search target the general mechanism inherits.

### 1.3 The new object: a runtime certificate `P`

Prop 1 and Prop 2 are **quantified over all pairs `x,y`** — they are properties of
the *design* `(C, Q, T)`, checked once (exhaustively, in RCF01's cube:
`check_bridge.py` runs all 65,536 law pairs). The fluid result adds something the
propositions do not directly give: a **decidable predicate on a single state**.

> **Definition (reuse certificate).** A **certificate** for `(C, Q)` is a
> predicate `P : X → {0,1}`, cheaply computable from the instantaneous state,
> such that `P(x) = 1` **implies** the read-off is exact at `x`, i.e.
> `Q(x) = h(C(x))` — and, for reuse, that `C` behaves as a state across the
> operations enabled at `x` (the local, this-state instance of Prop 2's clauses).

`P` is a *sound under-approximation* of the (generally undecidable or expensive)
predicate "`C` is sufficient at `x`." Fluids: `P_geo = C1 ∧ C3 ∧ C4` — single
equipotential (Prop 1), no shared cavity and no trapped pocket (Prop 2
enabledness) — each clause `O(cavity)` (`SUFFICIENCY_TEST.md` §3). Crucially `P`
is *local and cheap* where re-deriving `Q` from scratch is *global and expensive*.

### 1.4 The mechanism as a claim/theorem-shape

Putting the pieces together, the general claim is a three-part conjunction:

> **General mechanism (informal).** Given a receiver `Q` on a carrier `X`, seek a
> representation `C` making `Q` intrinsic and a certificate `P` such that:
>
> 1. **(Soundness)** `P(x)=1 ⇒ Q(x) = h(C(x))` — a certified read-off is exact.
> 2. **(Cheapness)** `P` and `h∘C` are computable in cost `≪` the cost of
>    computing `Q` by the reference method.
> 3. **(Exact reuse)** while `P` holds along a trajectory `x, T(x), T²(x), …`, the
>    cached `C` may be *reused* (recompute skipped) with a result **bit-identical**
>    to recomputing, because the local Prop-2 clauses hold at each step.

*Proof sketch.* (1) is Prop 1 restricted to the fiber of `x` under `C`, witnessed
by `P`'s clauses (fluids: C1 forces one level ⇒ the read-off's single-equipotential
answer is the true one; C3/C4 rule out the enabledness/mislevel counterexamples).
(3) is induction using Prop 2: if `P` certifies the local clauses at each visited
state, then `C(T(x))` equals what a full recompute would produce, so reusing the
cache cannot differ from recomputing — this is precisely the "descent to a
well-defined operation on retained states" argument of RCF01 `FORMAL_BRIDGE_NOTE.md`
§2, applied per-step at runtime instead of once over all pairs. (2) is an
empirical property of the chosen `(C, P)`, not a theorem; it is what makes the
mechanism *pay*, and it is exactly what `design/PERF.md` measures. ∎(sketch)

### 1.5 The cost model, grounded in Prestige One

The cash-out is not incidental; it is RCF01's **Prestige One** made operational.
`CONCEPT_REGISTER.md` RCF-P1: *a completed relational course can appear as one
while retaining a route to its construction; established relationships make lower
work unnecessary.* Model it as a **promoted envelope**: a hot summary `C` plus a
cold reconstruction route (the full recompute), with a verdict from the outcome
set RCF01 proposes (`CURSOR_START_HERE.md` §4: `EXACT / REOPEN_REQUIRED /
UNRESOLVED / INVALID_DEPENDENCY`).

> **Cost model.** Per step, per unit: check `P`. If `P` holds → `EXACT`: reuse the
> hot summary (cost `= cost(P) + cost(read-off)`). If `P` fails → `REOPEN_REQUIRED`:
> pay the cold recompute and refresh `C`. Total work `= Σ_certified cost(P) +
> Σ_uncertified cost(recompute)`.

This is exactly D_fast (`design/PERF.md` §1): `P_geo` is the *license to skip the
recompute*; a certified body rides its cache; an uncertified one re-floods; a TTL
backstop bounds drift (the "reopen at least every N" of a promoted envelope). The
measured payoff (avg flood 2–22×, bit-identical) is the Prestige-One promise —
"lower work unnecessary" — with the certificate as the thing that *earns* the
promotion honestly (it retains the reopen route and refuses when insufficient).

### 1.6 The two separable quality axes

The fluid experiment's most transferable finding is that certificate quality
splits into **two independent axes**, and RPRM's value lives on the second.

- **SOUNDNESS** — *never certify a wrong read-off*: `P(x)=1 ⇒ exact`, i.e. zero
  false positives. This is the classic soundness of any sound approximation. In
  fluids it was perfect (0 FP / 1100 scenes, `SUFFICIENCY_TEST.md` §5).
- **COVERAGE** — *how many truly-exact states can `P` certify*, especially **under
  change**. Measured against a **quiescence baseline** ("wait until the unit stops
  moving, then trust the read-off").

The sharp, generalizable hypothesis:

> **Coverage-over-soundness hypothesis.** For a receiver-relative exactness
> certificate, **soundness is usually free** — a conservative "unit is quiescent /
> inputs unchanged" predicate already achieves zero false positives. The RPRM
> certificate's *value* is therefore almost entirely **coverage**: certifying
> exactness *while the unit is still changing*, because Prop 2 clause (3)
> `C(T(x)) = C(x)` can hold even when `x ≠ T(x)`. That is strictly more than
> "the operation is a no-op," and it is the headroom a quiescence baseline leaves
> on the table.

Fluids confirmed both halves cleanly: on soundness, `P_geo` merely **tied**
quiescence (no still-but-wrong state exists for model D, so quiescence is already
sound — `SUFFICIENCY_TEST.md` §5.1); on coverage, `P_geo` **beat** quiescence
**~14×** (46.8% vs 3.4% certified at equal 0 FP), by certifying 478
moving-but-exact states (§5.2). The compute cash-out inherits the same split:
the certificate bought **6.8–8.7×** *over* pure quiescence/dirty-tracking
precisely on the moving-but-exact bodies (`design/PERF.md` §4). Soundness pays the
rent; **coverage is the profit.**

A discipline note this axis forces: a "coverage win" is only genuine if it is not
a *relabeling*. RCF01's coherent-transport control (`check_bridge.py` CB12) is the
razor: transporting *both* the view and the receiver `S_new = map⁻¹(S_old)` creates
**no** information and must not be scored as coverage; only certifying a state the
baseline rejects *for the same fixed receiver* (the CB06 setting) counts. I carry
that razor into every application below.

---

## 2. Honest placement in known math

Per `RPRM_FLUIDS.md` §6 and RCF01's own instruction to *"give ordinary
mathematical names and attribution"* (`AGENT_HANDBOOK.md` line 46, quoted in
`RPRM_FLUIDS.md` §1). For each ingredient: the standard name, and the verdict.

| Mechanism ingredient | Standard name it (mostly) is | Rename, or real? |
|---|---|---|
| `P(x)` = checkable witness that the cheap read-off is exact here | **Certifying algorithms** (Mehlhorn & McConnell, *A Certifying Algorithm…*, 2011): output + a witness a cheap checker verifies | **Mostly rename**, with a twist (below). |
| `P` sound, never over-certifies | **Abstract interpretation / sound approximation** (Cousot & Cousot 1977): soundness = no false claim; coverage = precision/completeness | **Rename.** Soundness-vs-coverage *is* soundness-vs-precision. |
| Prop 2 congruence enabling exact reuse of `C` | **Strong lumpability / bisimulation** (Kemeny–Snell; Milner, Park 1981; Buchholz 1994) | **Rename of the theorem** (RCF01 says so). |
| "certified ⇒ skip recompute, reuse cache" | **Self-adjusting computation / incremental computation / memoization / materialized-view maintenance** (Acar 2005; Ramalingam & Reps 1993) | **Mostly rename** — but see the delta. |
| baseline = "unit is quiescent, let it sleep" | **Sleeping / islands + wake conditions** in physics engines (Baraff; Box2D, Bullet); dirty-rects; **a posteriori error estimation** for solvers | **Rename** of the baseline the certificate must beat. |
| "retain only the interface the receiver touches" | **Kron reduction / Schur complement / model-order reduction** — William himself makes this exact identification in the corpus | **Rename**, and a candid one — his own analogy. |

**The twist worth stating precisely.** Certifying algorithms classically emit a
witness that *an exact algorithm's output is correct*. Here `P` certifies that a
**cheaper, generally-inexact** computation (the read-off) is **exact for this
input** — a *per-instance exactness certificate for an approximation*, tied to a
**named receiver**. That specific combination — (approximation) × (per-instance) ×
(receiver-relative) × (used as a reuse license under motion) — is not, as far as I
can find, a standard named pattern, even though each factor is standard. That is
the whole of the candidate novelty, and it is a **framing**, not a theorem.

**Where the reuse delta is real.** Plain memoization/self-adjusting computation
invalidates a cache when its **inputs change** (dependency-dirtiness). The
certificate keeps the cache valid *despite input change*, whenever a
**receiver-relative invariant** (Prop 2 clause 3) survives the change. That is
literally the fluid ablation: dirty-tracking alone re-floods every moving body;
the certificate rides the cache and buys an extra 6.8–8.7× (`design/PERF.md` §4).
So the delta over incremental computation is **exactly the coverage axis** — not a
new mechanism, but a sharper *invalidation predicate* derived from a sufficiency
argument rather than from input-equality.

**Blunt novelty verdict.**

- **~80–85% synthesis.** Prop 1 = factorization through a quotient / observability
  reduction. Prop 2 = strong lumpability = bisimulation congruence. `P` = a
  certifying-algorithm witness. The cache = self-adjusting computation. The
  baseline = engine sleeping / a posteriori error control. Each is decades old and
  RCF01/`RPRM_FLUIDS.md` say so.
- **~15–20% genuine, and it is *methodological/framing*, not mathematical:**
  1. **The coverage-over-soundness / certify-under-motion framing tied to a
     receiver** (§1.6). The empirical claim "the certificate's value is coverage,
     soundness is usually free" is crisp, falsifiable, and generalizable, and I
     have not found it stated this way. **Strongest novelty candidate.**
  2. **RPRM as the *search discipline*** — the standard techniques don't tell you
     *which* representation change to make or *which* certificate to seek; RCF01's
     recipe (name the receiver `Q` ⇒ find `C` making `Q` intrinsic ⇒ derive `P`
     from Prop 1/Prop 2 ⇒ locate the least forward-closed `S*` for the operation
     family) is a genuine, if modest, unifying *method*. Process Mechanics is
     honest that this is the claim, not a solver.

If someone insists "this is just certifying algorithms + memoization + lumpability,"
**they are ~80% right, and I will not pretend otherwise.** The defense is that the
synthesis is *useful*: it converts folklore ("use the cheap model when you can")
into a receiver-relative, decidable, measurable procedure, and it names a quality
axis (coverage under motion) that the constituent techniques do not foreground.

---

## 3. Cross-domain applications

For each candidate: the receiver `Q`, the intrinsic summary `C`, the certificate
`P`, and the quiescence-style baseline `P` must beat. The razor from §1.6 applies:
a win counts only if `P` certifies **motion** the baseline rejects for the **same
fixed receiver**.

| Domain | Receiver `Q` | Summary `C` (makes `Q` intrinsic) | Certificate `P` | Baseline to beat |
|---|---|---|---|---|
| **Physics broadphase / collision sleeping** | "Does the contact set (which pairs touch/penetrate) change next step?" | cached contact manifold + per-body AABBs + resting-force graph | AABB conservative-advancement margin proves no separated pair can close, **and** resting contacts stay in force balance ⇒ reuse cached manifold | velocity-threshold sleeping `‖v‖<τ` |
| **Incremental SAT / constraint / DB view** | the materialized view / model / solution value | cached answer + its support set (base tuples / clause frontier it depends on) | the incoming delta provably misses the support (or unit-propagation frontier unchanged) ⇒ reuse answer | "recompute on any base change" |
| **Rendering temporal / occlusion reuse** | final shaded/visible pixel this frame | cached shading + reprojection + occluder set | no disocclusion, material/light unchanged in-tolerance, motion within reprojection bound ⇒ reuse sample exactly | "invalidate on any camera motion" |
| **Multigrid / multiresolution solver** | fine-grid functional (flux, drag) on a region | coarse-grid solution on that region | a posteriori residual/error indicator below the receiver tolerance ⇒ skip fine relaxation there | uniform fine relaxation everywhere |
| **Groundwater dual-domain transport (this repo)** | `outlet_exceedance`: does outlet mobile conc. exceed `C*` over `[t0,t1]`? (`src/rprm_transport/receiver.py`) | mobile-domain conc. field + a **lumped** immobile total mass (drop the resolved immobile profile) | exchange flux `ζ·(c_m−c_im)` over `[t0,t1]` is below what could flip the threshold, **or** local equilibrium `c_im≈c_m` holds ⇒ read off from a single-porosity model | "always run the full dual-domain (IST) solve" |

Notes on the razor: the rendering and multigrid rows are the **weakest** — their
"certificates" collapse most readily into existing named techniques (reprojection
validity heuristics; a posteriori error estimators / adaptive mesh refinement). I
flag them as *likely relabels*, not clean wins. The SAT/view row and the
groundwater row have genuine receiver structure. The broadphase row is the
**tightest structural mirror of the fluid result** (its baseline literally *is*
"sleeping + wake conditions," the §2 baseline), so I develop it as the experiment.

### 3.1 Worked falsification experiment: a wake-certificate for broadphase sleeping

**Why this one.** It reproduces every feature of the fluid experiment: a cheap
summary (cached contact manifold), an intrinsic receiver (the contact *set*), a
decidable certificate (conservative-advancement margin + resting balance), and a
**quiescence baseline built into every real engine** (velocity-threshold sleeping).
If the coverage-over-soundness story is general, it should reappear here; if it
collapses to a known technique, this is where we will catch it (see §4).

**Setup (minimal, runnable).** 2-D rigid disks/boxes in a bin. Scene families
mirroring the fluid suite's spirit: (a) settled stacks; (b) **slow uniform
drift** (a block translating under weak damping / on a slow conveyor) — the
"moving-but-exact" analog; (c) near-miss fly-bys (separated, fast); (d) genuine
impacts; (e) resting stacks with one jittering top body (the `PROBLEMS.md` #6
analog). ~1000 randomized instances.

**Ground truth.** Run full broadphase every step; record, per step per island,
whether the **contact set changed**. "Reuse is exact this step" ⟺ contact set
unchanged (and manifold identical).

**Certificate `P`.** For a sleeping island: (C1) every currently-separated AABB
pair `(i,j)` has gap `> (‖v_i‖+‖v_j‖)·Δt + slack` (conservative advancement — no
new contact can form before next broadphase); (C3/C4 analog) existing resting
contacts remain in force balance (net force within the friction cone), so no
contact is *lost*. `P = C1 ∧ (resting-balance)`. Cost `O(island boundary)`.

**Baselines.** (i) velocity-threshold sleeping `‖v‖<τ`; (ii) "dirty on any
motion." Each given its best zero-FP threshold, exactly as `SUFFICIENCY_TEST.md`
§5 does.

**Metrics (identical shape to the fluid confusion matrix).**
- Confusion matrix `{P says reuse} × {contact set actually unchanged}`; the
  decisive number is the **false-positive rate** (certified-but-changed).
- **Coverage** = fraction of body-steps certified; compare `P` vs
  velocity-threshold at **equal (zero) FP**. The hypothesis predicts `P` certifies
  the *slow-drift* family (contact set invariant though bodies move) that
  velocity-threshold must wake — a coverage gap analogous to the fluid 478.
- **Compute saved** = broadphase pairs skipped while certified, bit-identical
  manifold.

**Falsification conditions (a "no" is informative).** `P` is refuted as *sound* if
any certified step's contact set actually changed (FP `> 0`). `P` is refuted as
*valuable* if its coverage does **not** exceed velocity-threshold sleeping at equal
FP — i.e. if there is no "moving-but-exact" headroom in rigid contact the way there
was in fluids. **I expect a weaker win here than 14×**, and §4 says why; running it
is how we find out, and a null result is a perfectly good, publishable answer
(RCF01 `CURSOR_START_HERE.md` §5: "a correct null … is a valid outcome").

**Preliminary run (single-step, throwaway harness — treat as a sanity check, not
the full study).** A minimal 1540-scene version of exactly this protocol was run
while writing this note (7 families incl. slow-drift, closing, and separating
pairs; ground truth = full broadphase next step). Findings, at face value:

- With a **well-posed** reach bound (one that includes the in-step gravity impulse
  `g·Δt`, not just current velocity), `P` was **sound: 0 false positives / 1540**,
  coverage **60.4%** vs naive velocity-threshold quiescence **18.6%** — a **~3.3×**
  coverage win, certifying **770** moving-but-exact states quiescence rejects. The
  contact-changing families (`closing`, `separating`) were correctly refused
  (true negatives), so soundness was actually stressed, not vacuous.
- The win is **markedly smaller than the fluid 14×**, as predicted, and it is
  against a *naive* baseline (§4).
- The instructive failure: an *earlier* reach bound using current velocity alone
  produced a false positive on a near-still body accelerating under gravity —
  concretely demonstrating §4's "soundness rides on a well-posed bound." Adding the
  `g·Δt` term removed it. (Amusingly, naive velocity-threshold quiescence stayed
  *unsound* on that same scene — a still-looking body still falls — so here the
  receiver-derived certificate beat the naive baseline on *both* axes; I do not
  generalize that past this toy, since a gravity-aware quiescence guard would also
  be sound.)

This is a one-step, low-fidelity harness (no persistent islands, no engine-grade
conservative advancement), so it validates that the experiment is *well-posed and
sound*, not that the win survives against mature engines — which is the real test
§4 flags.

---

## 4. Honest risks and limits

**Where the generalization likely fails.**

- **The peak is never reduced, only amortized.** As in `design/PERF.md` §5, a unit
  whose receiver-answer *keeps* changing is uncertifiable and costs the full
  recompute. Domains where everything is always changing in a receiver-relevant
  way (turbulent dynamics, chaotic constraint churn) get ~nothing. The mechanism
  is a tax on **quiescent-or-invariant majorities**, not a universal speedup.
- **`P`'s soundness rides on a well-posed bound.** In fluids, model D bounded
  every cavity by the body's `top`, which is what made "still-but-wrong" states
  *non-existent* and the certificate well-defined (`SUFFICIENCY_TEST.md` §5.1).
  Domains lacking such clean structure (unbounded velocities, force spikes) can
  break the conservative bound and produce false positives — the broadphase C1
  margin fails exactly when an unmodeled impulse exceeds `‖v‖·Δt`.

**Where "certificate" collapses to a known technique.**

- If `P` reduces to "**inputs unchanged**," it *is* plain memoization /
  dirty-tracking — the fluid `E_noCert` baseline, which the certificate beat only
  because a receiver-relative invariant survived input change. **No invariant ⇒ no
  delta over incremental computation.**
- **Broadphase is the sharpest risk of collapse.** Conservative advancement,
  speculative contacts, and temporal coherence are *already standard* in mature
  engines (Box2D speculative contacts, Bullet). So the broadphase certificate may
  add **little or nothing** over an engine that already does this — its "quiescence
  baseline" is not naive. The fluid 14× exploited a *naive* quiescence baseline;
  where the incumbent baseline is already sophisticated, the coverage headroom may
  be near zero. This is the **single biggest honest risk** to the whole thesis:
  the coverage win may be large only against strawman baselines and shrink to
  nothing against the best existing practice.
- Multigrid/rendering rows (§3): the certificate is an a posteriori error
  estimator / reprojection-validity test with a new label — expect **relabel, not
  win**, per the CB12 coherent-transport razor.

**What RCF01's formalization would still need to prove.** RCF01 rigorously
establishes Prop 1/Prop 2, the least forward-closed `S*` (exhaustively on the cube,
`check_bridge.py` CB09), and its control validator (omit/duplicate/unexpected fail,
reorder passes — `results/aggregate_controls.json`). It does **not** yet establish
the three things the general mechanism needs:

1. **Existence/soundness of a *runtime* certificate.** RCF01 checks the
   *design-level* propositions over all pairs; it has no theorem that a decidable,
   cheap **per-state** `P` soundly under-approximating sufficiency exists for a
   given `(C, Q, T)`. Fluids found one by hand; the general existence question is
   open. (`P` may not exist, or may be as expensive as the recompute.)
2. **Any coverage guarantee.** The coverage-over-soundness claim is **empirical**
   in fluids and **unproven** in general. There is no theorem bounding coverage
   below, nor characterizing which `(C, Q, T)` admit a certify-under-motion `P`.
   This is the crux novelty and it is currently a *hypothesis with one data point*.
3. **A net cost model that counts everything.** RCF01 is explicit
   (`CURSOR_START_HERE.md` §5): *"Any efficiency claim must include construction,
   checking, storage, lookup, reopening, invalidation."* The fluid `design/PERF.md`
   honors this (peak not reduced; cache-relax not free), but the general claim
   "certified reuse pays" needs a cost theorem that `cost(P) + amortized
   reopen ≪ cost(recompute)` — which fails whenever `P` is as global as the thing
   it guards.

---

## 5. Bottom line and confidence

- **Mechanism (high confidence it's well-posed):** change representation so the
  receiver `Q` is intrinsic to a cheap summary `C`; derive a decidable certificate
  `P` from Prop 1/Prop 2 that soundly says "read-off is exact *now*"; cash `P` as a
  license to skip recompute (Prestige One), with bit-identical results while
  certified. Two axes: **soundness** (no false certifications — usually free) and
  **coverage** (certify under motion — where the value is).
- **Novelty (high confidence it's *mostly synthesis*):** ~80–85% relabeling of
  certifying algorithms, sound approximation, strong lumpability, and self-adjusting
  computation. The defensible ~15–20% is a **framing**: coverage-over-soundness /
  certify-under-motion tied to a receiver, plus RPRM as the *search discipline* for
  `(C, P)`. **Not a new theorem. Not a new solver.**
- **Best non-fluid domain (medium confidence):** broadphase sleeping with a
  wake-certificate — tightest mirror, cleanest experiment — **with the explicit
  caveat** that mature engines already do conservative advancement, so the honest
  expected result is a *smaller* coverage win than fluids, possibly a null against
  best practice. That risk is the most important thing to test, not hide.
- **Biggest honest risk (high confidence it matters):** the coverage win may exist
  only against **naive** quiescence baselines and collapse against sophisticated
  incumbents; and where no receiver-relative invariant survives input change, `P`
  degenerates to ordinary memoization with no delta.

**Confidence, blunt.** High that the mechanism is a correct, useful *synthesis* and
that the fluid result is a real instance of it. Medium that the coverage-over-
soundness framing is genuinely new rather than folklore I haven't found the name
for. Low-to-medium that it transfers with fluid-sized wins to any domain whose
incumbent baseline is already better than naive quiescence. The one experiment in
§3.1 is designed to move that last number in either direction, and I'd trust its
answer over this document's optimism.
