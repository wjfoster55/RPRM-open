# Fluid simulation through the RPRM lens

**An accuracy-first design analysis.**

*Author's note on stance.* This document is written for William, who built RPRM
and explicitly wants it *not to be BS*. The whole value of the exercise depends
on separating two things:

- **(a) Real design commitments** — places where taking RPRM seriously forces a
  specific, non-obvious choice that a default fluids engineer would *not* make,
  or would only make after a lot of tacit reasoning.
- **(b) Rename-jobs** — places where "the RPRM design" is a well-known standard
  technique wearing new vocabulary.

I flag (b) aggressively and in its own section (§6). Where I think RPRM adds
genuine value it is **not** a new algorithm; it is a **discipline for choosing
which representation to use, plus a sound-but-incomplete acceptance predicate for
when a cheap one is sufficient (to a stated tolerance) versus when you must
refine.** That is a real and useful thing, but it is smaller and more honest than
"RPRM invents a new fluid solver."

I prioritize *accuracy/realism* first, per the brief, on the theory that
understanding the accurate RPRM-native design informs the cheap one later (§7).

Primary RPRM sources are cited by repo path from
[`wjfoster55/RPRM-open`](https://github.com/wjfoster55/RPRM-open). The two papers
William mentioned are present: the *Manifesto* (`MANIFESTO.md` /
`RPRM-Manifesto.pdf`, DOI 10.5281/zenodo.22650748) and the newer Process
Mechanics working paper *The Right Answer Is Not Enough*
(`papers/process-mechanics/MANUSCRIPT.md`, DOI 10.5281/zenodo.22709682). The
second is the more directly relevant of the two for simulation.

---

## 1. What RPRM actually commits to (cited)

RPRM = **Relational Pressure Retention Model**. Two things must be said up front,
because both are stated by the author and both matter for intellectual honesty:

1. **The name's "Pressure" is *not* a physics primitive you get for free.**
   `docs/core.md` §15 is explicit: *"**Pressure** has no universal scalar
   definition in this core. A model may define a constraint count, residual norm,
   live-fiber cardinality, resource deficit or another quantity, with units and
   intended use... No pressure minimization law is inferred for every RPRM
   construction."* So RPRM does **not** hand us a notion of hydrostatic pressure.
   "Pressure" in "RPRM" is a *motivating* physics word (`README.md` lines 6–9;
   `docs/relational-layer.md` lines 1–7), and any pressure we use in a fluid model
   we must define ourselves in the ordinary way. This is the single most important
   guardrail against self-deception here: **RPRM will not tell us what pressure
   is; it will only discipline how we *represent and retain* whatever pressure we
   define.**

2. **The author pre-empts the rename problem himself.** `AGENT_HANDBOOK.md`
   line 46: *"Do not assume a concept is new because its RPRM name is new. Give
   ordinary mathematical names and attribution where applicable."* Process
   Mechanics §7 then explicitly maps its own results onto **abstract
   interpretation, CEGAR, Kalman filtering, equivalence-class determination
   (EC²), self-adjusting computation, and strong lumpability of Markov chains**
   (`MANUSCRIPT.md` §7). This is unusually candid and it means my §6 is not an
   attack on RPRM — it is finishing a job the author started.

With those guardrails, here are RPRM's actual, load-bearing commitments, in
precise language, each with a citation and each stated as an *operational test*
rather than a slogan.

### 1.1 Carrier / ports / aperture — a question is a choice of what is supplied
A **carrier** is the admitted set of objects with their equality, units, bounds
(`AGENT_HANDBOOK.md` §2; `docs/core.md` §2). A **port** is a typed role. An
**aperture** chooses which ports are supplied and which are requested. *Changing
the aperture changes the question, not the law* (`README.md` "One law, several
questions"; `docs/core.md` §6). The **fiber** is the complete set of compatible
completions, with dispositions `NONE / ONE / MANY / OPEN` (`AGENT_HANDBOOK.md`
§3). **Design consequence for us:** before touching a solver, name the *receiver
question* precisely, because a fluid field that answers one aperture ("velocity
everywhere now") is not automatically sufficient for another ("resting surface
height here").

### 1.2 The receiver — the thing that must be preserved
A **receiver** is the declared family of questions/behaviors a representation
must preserve (`docs/core.md` §8; `AGENT_HANDBOOK.md` §4). This is the pivot of
the whole framework: *sufficiency is always relative to a stated receiver.*
`LAYPERSON_GUIDE.md` lines 48–56: *"A summary is exact for a receiver when every
original situation that it merges has the same answer to those questions."*

### 1.3 Question factorization — the exact sufficiency test (Prop 1)
For a representation `C: X → Z` and a question `Q: X → B`, an exact decoder
`Q = h∘C` exists **iff** `C(x)=C(y) ⇒ Q(x)=Q(y)` (`docs/core.md` §8, the boxed
theorem; Process Mechanics Prop 1, `MANUSCRIPT.md` §3.1). Equivalently: you may
throw away any distinction that never changes the receiver's answer. The exact
repair when it fails is `C'(x) = (C(x), Q(x))` — the *least* informative
refinement that restores sufficiency (`docs/core.md` §10; `AGENT_HANDBOOK.md`
§4). **This is the mathematical content of "retain only the minimal sufficient
state."**

### 1.4 Operational factorization — sufficiency to *continue*, not just answer once (Prop 2)
To use a summary `C` as a *state* through updates `T_a` with observation `O`, you
need for every `C(x)=C(y)`: (1) `O(x)=O(y)`; (2) each `T_a` enabled at both or
neither; (3) `C(T_a(x)) = C(T_a(y))` (`AGENT_HANDBOOK.md` §5; Process Mechanics
Prop 2, `MANUSCRIPT.md` §3.2; `docs/relational-layer.md` "Closed observations").
This is strictly stronger than answering the present question — it is a
**congruence / bisimulation / strong-lumpability** condition, and the author says
so (§6). **Design consequence:** a cheap fluid representation can be exactly right
for a *static* question and still be unusable as a *dynamical state*; Prop 2 is
the test that tells you which.

### 1.5 Change of representation to expose the question
*"An explicit change of representation can expose a different question, explain
why information was lost, or show exactly what must be retained to continue"*
(`README.md` lines 22–27). A **CAR** is an invertible re-coordinatization; a
**FOLD/ADAPTER** is a lossy map that provably preserves a named receiver
(`docs/core.md` §9). **Design consequence:** the central RPRM move is not "solve
harder" but "re-coordinatize so the receiver's question becomes a read-off."

### 1.6 Relational vs absolute quantities; keep the joint fiber
RPRM repeatedly prefers *relational* (difference/ratio) coordinates to *absolute*
ones and warns against destroying correlations by marginalizing. The gravity
chapter retains the **radial receiver `(r, u, j)`** — separation, radial
velocity, squared specific angular momentum — and deliberately *forgets absolute
spatial orientation* because the receiver does not need it (`docs/relational-layer.md`
"Gravity"; `AGENT_HANDBOOK.md` §12). The abduction example infers `z−x=5` from
`y−x=2, z−y=3` while the absolute offset `a` stays free and undetermined — *"a
compatibility law, not an observation of an absolute origin"*
(`docs/relational-layer.md` "What abduction can establish"). **Keep missing ports
joint**: from `{(0,0),(1,1)}` the marginals are each `{0,1}` but their product
falsely admits `(0,1),(1,0)` (`docs/core.md` §5; `AGENT_HANDBOOK.md` §3).

### 1.7 Observation economy — choose the next observation, and don't observe what can't change the answer
The context/communication pack formalizes **one-step minimax question
selection**: pick the probe that minimizes the largest surviving-hypothesis
bucket, *before reading its outcome* (`AGENT_HANDBOOK.md` §13, "one-step minimax
query"). And an **unvisited value is known when every remaining possibility gives
it the same value** (`LAYPERSON_GUIDE.md` lines 120–125). **Design consequence:**
you should only *update* (observe/advance) the cells/bodies whose state can still
change the receiver's answer; the rest are dormant. (This is real but it is also
exactly where the rename risk is highest — see §6.)

### 1.8 Minimal *sufficient* — economy has a floor set by an invariant
Economy is bounded below by whatever invariant the receiver needs.
`AGENT_HANDBOOK.md`'s worked line example and the Manifesto's conservation
discussions insist that a summary retain *enough* to keep its invariant. The
prototype already learned this the hard way: dropping the one-cell halo made the
retained set "too economical" and silently broke mass conservation
(`noita_lab/PROBLEMS.md` #5). RPRM's phrase for the halo is *the minimal
sufficient extra state.*

> **One-paragraph summary of RPRM's real content.** RPRM is a disciplined
> vocabulary + two theorems (question factorization and operational
> factorization) for deciding **what to retain** and **what to observe next**,
> *relative to an explicitly named receiver*, plus a strong preference for
> **changing representation** (often to relational coordinates) so the receiver's
> question becomes a read-off. It deliberately does **not** supply physics (not
> even "pressure"), and it explicitly warns that its named constructions are
> often standard methods.

---

## 2. How accurate fluid simulation works today, decomposed RPRM-style

For each family: **retained state**, the **real question answered per step**, and
the **irreducible cost**. The recurring punchline is set up here and paid off in
§3: *every accurate method enforces incompressibility with a global, non-local
coupling, and that coupling is the industrial-scale version of our U-tube's "a
local cell cannot see its connected body's target level."*

### 2.0 The shared physics
Incompressible Navier–Stokes: `∂u/∂t + (u·∇)u = −(1/ρ)∇p + ν∇²u + g`, subject to
`∇·u = 0`. Pressure `p` is **not** a dynamical variable with its own time
evolution; it is a Lagrange multiplier whose only job is to enforce `∇·u=0`.
Taking the divergence of the momentum equation gives a **pressure Poisson
equation** `∇²p = (…)` that determines `p` from `u` *at the same instant*. Because
that PDE is **elliptic**, *"a change in the velocity field near one spatial point
instantly affects the pressure, and therefore the acceleration of the fluid,
everywhere else... the incompressible limit in which the sound speed becomes
infinite"* (Hunter, *Intro to the Incompressible Euler Equations*, §3). Hold onto
that sentence; it is the crux.

### 2.1 Eulerian grid + pressure projection (Stam, *Stable Fluids*, SIGGRAPH 1999; Chorin projection 1968)
- **Retained state:** a velocity field `u` on a fixed grid (MAC/staggered), plus
  advected scalars. Pressure is *not* retained between steps — it is recomputed.
- **Real question per step:** "Given the post-advection, post-force velocity `w`
  (which is not divergence-free), what is the *nearest* divergence-free field?"
  This is the Helmholtz–Hodge projection `u = w − ∇q`, and `q` solves
  `∇²q = ∇·w` with Neumann BC `∂q/∂n = 0` at walls (Stam §; verified). RPRM
  reading: the step's aperture is *"supplied: `w`; requested: the divergence-free
  representative of `w`'s equivalence class."*
- **Irreducible cost:** the **global sparse elliptic solve** (Jacobi/Gauss–Seidel,
  CG, or multigrid). Everything else (semi-Lagrangian advection, forces) is local
  and cheap. The solve is the whole ballgame and it is non-local by construction.

### 2.2 SPH (Smoothed Particle Hydrodynamics)
- **Retained state:** per-particle position, velocity, mass; density `ρ_i =
  Σ_j m_j W(x_i−x_j, h)` is a *kernel sum over neighbors*.
- **Real question per step:** classic WCSPH asks "what pressure force does a local
  equation of state `p = k((ρ/ρ₀)ⁿ − 1)` produce?" — this is **weakly
  compressible**: it fakes incompressibility with a stiff local EOS and pays with
  tiny density fluctuations and small time steps. PCISPH/IISPH instead ask "what
  pressure field makes the *predicted* density return to `ρ₀`?" — which is again a
  **global** (iterated) solve, just phrased on particles.
- **Irreducible cost:** neighbor search + either stiffness (WCSPH: small `dt`) or
  a global pressure iteration (PCISPH/IISPH). RPRM reading: WCSPH *chose a local
  representation of a non-local constraint and paid in stiffness* — this is
  exactly our Model C's "compressibility term diffuses pressure slowly"
  (`PROBLEMS.md` #1), at research grade.

### 2.3 Hybrid PIC / FLIP / APIC
- **Retained state:** particles carry mass/velocity (and, in APIC, an affine
  velocity matrix `C_p` that preserves angular momentum across the transfer); a
  background grid is scratch space each step.
- **Real question per step:** transfer particles→grid, **do the incompressible
  pressure projection on the grid** (same Poisson solve as §2.1), transfer
  grid→particles. PIC is dissipative; FLIP transfers only the *delta* and is
  lively; APIC (Jiang et al. 2015) fixes FLIP's noise/angular-momentum loss with
  the affine term.
- **Irreducible cost:** the same grid Poisson solve, plus transfer overhead. The
  particle/grid split is an accuracy/energy-preservation choice; **the
  non-locality is unchanged.**

### 2.4 Position-Based Fluids (PBF; Macklin & Müller 2013)
- **Retained state:** particle positions; one **density constraint per particle**
  `C_i(x) = ρ_i/ρ₀ − 1 = 0`.
- **Real question per step:** "what position correction `Δx_i` drives every
  particle's density back to `ρ₀`?" solved by a few (≈2–6) Jacobi iterations of
  the constraint system with per-particle Lagrange multipliers `λ_i`. Crucially,
  PBF **does not iterate to convergence** — it runs a *fixed, small* number of
  iterations for stability + speed and accepts residual compressibility.
- **Irreducible cost:** neighbor search + constraint iterations. RPRM reading:
  PBF is the honest admission that the global solve is expensive, so it
  *truncates* it and accepts a bounded receiver error. That truncation is a FOLD
  with a tolerance contract — and Process Mechanics has exactly the machinery for
  "approximate retention with a TV/error bound" (`MANUSCRIPT.md` §11, the
  `min(1, t·ε)` bound). This is a place RPRM's vocabulary *fits* real practice.

### 2.5 Lattice-Boltzmann (LBM)
- **Retained state:** per-cell particle-distribution functions `f_i` along a
  fixed velocity stencil (e.g. D2Q9). Density and momentum are *low moments* of
  `f`.
- **Real question per step:** local **collide** (relax `f` toward equilibrium
  `f^eq`) + **stream** (shift `f_i` to neighbors). Incompressibility is recovered
  only in the low-Mach limit; pressure ≈ `c_s²ρ` locally.
- **Irreducible cost:** memory bandwidth for `f` (many numbers per cell), and the
  method is again **weakly compressible** — it trades the global solve for a
  local relaxation but only approximates `∇·u=0`, with acoustic/compressibility
  error the price. RPRM reading: LBM is a *different representation* (velocity
  moments) in which one step is fully local — but it does not answer the exact
  incompressible aperture; it answers a nearby compressible one.

### 2.6 The pattern
| Method | Retained state | Real question / step | Irreducible cost | How it treats incompressibility |
|---|---|---|---|---|
| Stable Fluids | grid `u` | nearest div-free field | **global elliptic solve** | exact, non-local |
| SPH (WC) | particles, `ρ=Σ W` | local EOS force | stiffness / small `dt` | approx, local, stiff |
| SPH (PCI/II) | particles | pressure to restore `ρ₀` | global iteration | exact-ish, non-local |
| PIC/FLIP/APIC | particles + grid | grid projection | **global elliptic solve** | exact, non-local |
| PBF | particles, `C_i` | fixed-iter density constraint | neighbor + k iters | approx (truncated), semi-non-local |
| LBM | per-cell `f_i` | collide+stream | bandwidth | approx, local, weakly-compressible |

**Two clean buckets.** Either you enforce incompressibility *exactly* and pay a
**global, non-local coupling** (Stable Fluids, PIC/FLIP/APIC, PCISPH/IISPH), or
you enforce it *approximately and locally* and pay in **stiffness / finite
propagation speed / compressibility error** (WCSPH, LBM, PBF-truncated, and our
Model C). **There is no known method that is simultaneously exactly incompressible
and purely local, and §3 argues that is not an accident.**

---

## 3. The crux: is incompressibility's non-locality fundamental, or a representation artifact?

William's intuition, verbatim from the brief: *"it should just work — you
shouldn't need to propagate a level signal; I wish it just fell instead of us
simulating it."* This is the right question to interrogate, and the honest answer
is **it splits cleanly in two**, and the split is the most valuable single result
in this document.

### 3.1 First, name what is actually non-local
Gravity is **local** — it is a body force, every parcel just falls. What is
non-local is the **incompressibility constraint response**: the pressure/normal
force by which the rest of the fluid and the container push back to prevent
interpenetration and overfilling. In a truly incompressible medium this response
is *instantaneous and global* because the medium is infinitely stiff — the same
reason a **rigid rod transmits force from end to end with no travel time**, and
the same reason a rigid-body constraint solver is a global linear solve. So "I
wish it just fell" is half-granted: it *does* just fall; the cost is not the
falling, it is the **push-back that makes a U-tube's far column rise against
gravity.** You cannot get "rise on the far side" from purely local rules because
that water must be pushed *up*, and the only thing that can push it up is a force
transmitted *through* the connected body. Transmitting a force through an
incompressible body is intrinsically non-local. (This is precisely why our Model
C fails: horizontal flow is `(m_i − m_j)/4`, which is ~0 between two full cells,
so a tall column exerts no sideways push through the bottom pipe —
`js/models.js` LEFT/RIGHT branches; `PROBLEMS.md` #1.)

**Verdict on the *dynamic* case (stated as a conjecture, not a theorem).** For a
receiver that asks dynamical questions (waves, splashes, momentum, "where is the
shock at time t"), we could not find — and are not aware of — a change of
representation that answers them *exactly* without some instantaneous global
coupling: every "local" method surveyed above is secretly answering a
*compressible* aperture and accepting acoustic/stiffness error, and the exactly
incompressible methods all pay a global elliptic solve (§2.3 table). We therefore
treat non-locality here as a **defensible insufficiency conjecture**: *no known
purely-local representation is exactly sufficient for the dynamic incompressible
receiver.* We do **not** claim to have *proved* that a global solve is necessary —
that would be a strong impossibility result we have not established, and "changing
representation cannot possibly help" is exactly the kind of overclaim William wants
avoided. What we can say plainly is falsifiable (see H3, §5): exhibiting an
exactly-incompressible, purely-local dynamic scheme would refute the conjecture.

### 3.2 But the *hydrostatic* receiver is different
Now restrict the receiver to the **quasi-static** questions the U-tube and the
Noita lab actually care about: *"what is the resting free-surface height here?",
"will this vessel overflow?", "which cells are underwater at equilibrium?"* For
these, the answer is **not** obtained by watching a dynamic process reach a fixed
point. Equilibrium of a connected incompressible body under gravity is a
**potential-minimizer**: the resting state is the unique one in which each
connected body's free surface is a single horizontal **equipotential** (one level
per body), subject to the body's conserved volume. That level is a *closed-form
read-off* from two pieces of data:

- the body's **conserved volume** `V` (an invariant of the carrier), and
- the container's **area-vs-height (hypsometric) function** `A(z)` — geometry
  that is *static and knowable in advance*.

The level is `z*` such that `∫ A(z) dz = V` up to `z*`. **No Poisson iteration is
needed to find the equilibrium** — you need connectivity and volume. Standard
sims iterate a global solve only because they insist on computing equilibrium as
the *fixed point of a dynamical process expressed in an absolute Eulerian field*.

![Two representations of the same U-tube state: the absolute Eulerian field (left) needs a global elliptic solve to push the far column up against gravity, while the body/level representation (right) reads the equalized level off the body's conserved volume and container geometry — intrinsic, no iteration.](figures/utube_representations.svg)

**Verdict on the *static* case: the non-locality is (mostly) a REPRESENTATION
ARTIFACT.** In a **body/level representation** the hydrostatic answer is intrinsic
— read off, not iterated to. The *irreducible* residue of non-locality is small
and exactly identifiable: it is the **connectivity** relation (which cells belong
to the same body), because "same body" is genuinely a global property (two cells
can be adjacent yet in different bodies, or far apart yet connected through a
pipe). Connectivity is `O(N)` per frame (union-find / flood fill), not an elliptic
solve, and it is the **minimal non-local structure** that makes level intrinsic.

### 3.3 The precise statement RPRM lets us make
Put §3.1 and §3.2 together with the two factorization theorems:

- For the **hydrostatic receiver** `Q_hydro` = {resting surface height per point,
  overflow, underwater-mask}, the representation
  `C_body(state) = (per-body volume, connectivity graph, container geometry)`
  **satisfies question factorization (Prop 1)**: any two microstates with the same
  bodies+volumes have the same resting levels. So `C_body` is an *exact sufficient
  FOLD for `Q_hydro`*, and the velocity/pressure field is discardable.
- The moment the receiver adds a **dynamic** question (a wave arrival time, a
  splash, a pressure transient), `C_body` **fails operational factorization
  (Prop 2)**: two states with equal bodies+volumes but different velocity fields
  have different futures under the "advance dynamics" operation, so condition (3)
  `C(T(x))=C(T(y))` breaks. RPRM's repair rule then tells you *exactly* the least
  extra state to add back: `C'(x) = (C_body(x), velocity-field(x))` — i.e. you are
  forced back to a full solver, and RPRM *names why*.

**This is the genuine, non-obvious RPRM design commitment (category (a)):** not a
new solver, but a **crisp criterion for the boundary** between "a cheap intrinsic
read-off is exactly correct" and "you must pay for the global dynamic solve,"
expressed as a checkable congruence condition rather than as folklore. A default
engineer knows "use shallow water when you can"; RPRM turns that instinct into a
*test you can actually run on a receiver* (§5, H2).

---

## 4. An RPRM-native, accuracy-first water architecture

The design principle: **represent water as the receiver requires, and no more —
but keep a proof obligation that tells you when to refine.** Concretely, a
*two-representation* system with an explicit FOLD between them and a Prop-2 trigger
that decides which is live per region.

### 4.1 The two representations
1. **Body/level (relational, intrinsic-hydrostatic).** Water is a set of **labeled
   connected bodies**. Each body retains its **conserved volume** `V_b` and a
   pointer into precomputed **container geometry** `A_b(z)`. The receiver question
   "surface height here" is answered by the read-off `level(b)`; "overflow" is
   `V_b > capacity_b`. This is the RPRM "change representation so the question is
   intrinsic" move (§1.5), using relational level rather than an absolute pressure
   field (§1.6). Non-locality is confined to the `O(N)` connectivity pass.
2. **Field (absolute, dynamic).** Standard incompressible solver (grid projection
   or APIC) — retained *only in regions where the receiver has live dynamic
   questions* (an active splash, a moving front, an object impact).

### 4.2 The FOLD and the refinement trigger
- **field → body (coarsen):** when a region goes quiescent (velocities below `ε`
  for `k` steps), flood-fill it into bodies, integrate volume, **drop the velocity
  field**. Justified by Prop 1 for `Q_hydro`.
- **body → field (refine):** when a dynamic event touches a body (object enters,
  a wall opens, two bodies merge with a height mismatch that would splash),
  re-instantiate a velocity field seeded from the hydrostatic state. Triggered by
  the Prop-2 failure test: *the pending operation is one whose successor is not a
  function of `C_body` alone.*
- This is **observation economy** (§1.7) made physical: only field-region cells
  are "observed" (advanced) each step; body regions are dormant and answer by
  read-off.

### 4.3 Pseudocode (accuracy-first; the cheap version is §7)

```text
STATE:
  bodies: list of { cells: set, V: float, geom: A(z), level: float }
  field:  { u: velocity grid, solid mask }   # only over "active" cells
  active_mask: bool grid                      # where dynamic receiver questions live

# --- container geometry is precomputed once (static) ---
precompute A_b(z) for every potential vessel   # area-vs-height per connected region

step(dt, receiver):
  # 1. OBSERVATION ECONOMY: which cells can still change the receiver's answer?
  active_mask = cells within reach of {moving fluid, moved walls, object contacts,
                                       body-merge height-mismatches}
  # everything else is dormant this step (RPRM: don't observe what can't change Q)

  # 2. FIELD REGION: pay the fundamental non-local cost ONLY here (§3.1)
  if any(active_mask):
      w = advect(field.u) + forces(dt)          # local
      # exact incompressibility = global elliptic solve, restricted to active cells
      q = solve_pressure_poisson(div(w), neumann_at(solid|dormant_boundary))
      field.u = w - grad(q)                      # Helmholtz-Hodge projection
      move_water(field.u, dt)

  # 3. CONNECTIVITY: the minimal non-local structure for intrinsic level (§3.2)
  bodies = union_find(all_water_cells)           # O(N) label pass
  for b in bodies:
      b.V = sum(mass in b.cells)                 # conserved invariant
      b.level = invert(  ∫_z0^z A_b(z) dz = b.V ) # INTRINSIC read-off, no iteration

  # 4. HYDROSTATIC RECEIVER answers are now read off, not solved:
  #    height_at(p)   = bodies[label(p)].level
  #    overflow(b)    = b.V > capacity(b)
  #    underwater(p)  = elevation(p) < bodies[label(p)].level

  # 5. FOLD MANAGEMENT (Prop1 coarsen / Prop2 refine)
  for region in quiescent_regions(field.u, eps, k):
      drop_field(region)                         # justified by Prop 1 for Q_hydro
  for b in bodies touched_by_dynamic_event():
      instantiate_field(b, seed=hydrostatic(b))  # forced by Prop 2 failure

  # 6. MINIMAL SUFFICIENT halo (Prop-sufficiency floor, §1.8; PROBLEMS #5)
  reconcile field/body boundary with a one-cell halo   # or mass leaks
```

### 4.4 Why this is the *accurate* design, not a shortcut
- The **field region is a full, exact incompressible solver** — no accuracy is
  sacrificed where dynamics live. We do not approximate the elliptic solve away;
  §3.1 says we cannot.
- The **body region is exactly correct for its receiver** (hydrostatic
  equilibrium is genuinely a flat equipotential per body). It is not a visual
  approximation; for the static receiver it is the *ground truth*.
- The two are stitched by an **explicit FOLD with a stated preservation
  contract** and a **refinement trigger derived from Prop 2**, so the system knows
  where it is exact and where it must spend.

The honest cost: managing the FOLD boundary, connectivity per frame, and the
seeding transfer. This is more machinery than a monolithic solver; its payoff is
that the enormous quiescent majority of a typical scene costs `O(N)` connectivity
+ read-off instead of a global solve.

---

## 5. Falsifiable / testable hypotheses that distinguish the RPRM design

Each is stated so a "no" is possible and informative.

- **H1 (intrinsic level is exact for statics).** For any connected vessel network,
  the body/level read-off `level(b) = invert(∫A_b dz = V_b)` matches the converged
  equilibrium surface of a reference incompressible solver to within
  discretization error, in **one connectivity pass** — no iteration, and in
  particular **U-tube `Δh → 0` exactly** (contrast Model C's plateau at
  `Δh≈9–18`, `noita_lab/README.md` results table). *Falsified if* any static
  configuration equilibrates to a non-flat or wrong level under the read-off.
- **H2 (the Prop-2 boundary is real and checkable).** There exists a cheap,
  terminating predicate on the *receiver* — "does the pending operation's successor
  depend on more than `C_body`?" — that is **sound** (when it accepts, the cheap
  read-off matches a reference to tolerance) even if **incomplete** (it may reject
  cases that are in fact fine). *Falsified if* the predicate is *unsound* (accepts a
  case a reference solver contradicts). **Result (`SUFFICIENCY_TEST.md`):** the
  geometric form `P_geo` is empirically sound (0 false positives / 1100 scenes) but
  incomplete (rejects 320 within-tolerance scenes) — so it is a *sufficient
  condition*, not a full decision procedure. That still shows RPRM adds something a
  plain "use shallow water when quiescent" heuristic does not (it certifies 14× more
  scenes at the same zero-FP soundness): a *test*, not a vibe. We deliberately no
  longer call it "decidable" — it decides *acceptance*, not *sufficiency*.
- **H3 (observation economy beats geometric sleeping on connected pools).** Waking
  only cells whose state can change the receiver's answer (RPRM §1.7) strictly
  dominates chunk-granular sleeping on a *settled connected pool with one
  jittering surface cell* — the exact failure in `PROBLEMS.md` #6 — because a
  surface ripple that cannot change any body's `level` need not wake the pool.
  *Falsified if* the RPRM active set is not smaller than the chunk active set on
  that scenario.
- **H4 (relational level removes the compressibility knob's tyranny).** The
  body/level representation makes `MaxCompress` (`js/constants.js`) irrelevant to
  equalization: U-tube equalization time becomes `O(1)` connectivity passes,
  independent of column height, versus Model C's `O(height)`-or-worse diffusion
  (`compress_sweep.png`; `PROBLEMS.md` #1). *Falsified if* equalization time still
  scales with height under the body representation.
- **H5 (the split is defensible — conjectured no free lunch).** For a receiver
  containing a genuine dynamic question (measured wave arrival time), we *conjecture*
  that no purely local / intrinsic representation matches a reference incompressible
  solver exactly, so some global coupling (elliptic solve or its equivalent) is
  needed. This is a **defensible insufficiency conjecture, not a proved necessity**
  (see §3.1): known methods all pay it, but we have not established an impossibility
  theorem. *Falsified if* someone exhibits an exactly-incompressible, purely-local
  dynamic scheme — which would be a major result and would also refute §3.1's
  reframed claim. (I expect H5 holds; stating it as falsifiable is the point.)

---

## 6. Where this is just standard method X renamed (the honest section)

This is the section William asked me not to soften. For each RPRM ingredient
above, the standard name and the verdict.

| RPRM framing used here | Standard name it (mostly) is | Rename, or real? |
|---|---|---|
| "Intrinsic hydrostatic level from column volume; `P=ρgh`" | **Height-field / water-column / virtual-pipes methods** (Kass & Miller 1990; O'Brien & Hodgins 1995; shallow-water) | **Rename.** Making hydrostatic pressure a read-off from column height is a 30+ year-old standard technique. RPRM did not invent it. |
| "Labeled connected bodies with one level each" | **Connected-component / flood-fill "equilibrium water"** (common in games; union-find) | **Rename.** The data structure and the flat-equipotential fact are classical. |
| "Retain only the minimal sufficient state / question factorization" | **Observability reduction; bisimulation/quotient; strong lumpability** of Markov chains; abstract interpretation | **Mostly rename** — and the author says so (`MANUSCRIPT.md` §7; `AGENT_HANDBOOK.md` §5–6). |
| "Operational factorization (Prop 2)" | **Strong lumpability / bisimulation congruence** | **Rename of the theorem**, but see below for the real part. |
| "Observation economy / don't update dormant cells" | **Adaptive mesh refinement, sparse/`VDB` grids, sleeping rigid bodies, LOD, active-set/dirty-rect** | **Rename.** The prototype's own dirty-rect scheme is already this (`js/grid.js`). |
| "Approximate retention with a bound" (PBF truncation) | **Truncated iterative solver + error analysis** | **Rename**, though the TV bound framing (`MANUSCRIPT.md` §11) is a tidy way to state it. |
| "Relational vs absolute coordinates" | **Reduced/relative coordinates; gauge/potential formulations** | **Rename** of a standard modeling instinct. |

**So what, if anything, is category (a) — genuinely non-obvious?** After being
this harsh, three things survive as *real*, and they are all *meta* (about
choosing/justifying representations), not new physics or new solvers:

1. **A single receiver-relative decision procedure that spans the whole
   pipeline.** The individual pieces are all standard, but RPRM's insistence that
   you *first name the receiver*, then apply *one* sufficiency test (Prop 1) and
   *one* continuation test (Prop 2) to decide **every** representation choice —
   grid vs particles vs bodies, what to store, what to observe — is a genuinely
   useful unifying discipline. Its value is *methodological*, and Process
   Mechanics is honest that this is the claim (`MANUSCRIPT.md` §7 close: *"Its
   usefulness as a method still needs comparison against ordinary practice"*).
2. **Turning "use the cheap model when you can" into a checkable boundary.** H2/§3.3:
   the Prop-2 congruence gives an *operational* answer to *when* the intrinsic
   representation is exact versus lossy, and *exactly what to add back* when it
   fails (`C' = (C_body, velocity)`). Practitioners do this by experience; RPRM
   makes it a test. That is a real, if modest, contribution.
3. **A crisp diagnosis of the non-locality itself (§3).** The clean statement
   "instantaneous global coupling is fundamental for the *dynamic* receiver (the
   elliptic limit) but a representation artifact for the *static* receiver" is
   correct, clarifying, and not how the folklore usually phrases it. But note: the
   underlying facts (elliptic limit = infinite sound speed; hydrostatic
   equilibrium = flat equipotential) are **classical physics**. RPRM organizes
   them; it does not discover them.

**Net honest verdict.** RPRM here is **~80% re-labeling of height-field +
connected-components + model-reduction + adaptivity**, plus **~20% genuine value
as a receiver-relative decision/justification discipline.** That 20% is real and
worth keeping, *provided* it is sold as a method for choosing and proving
representations — never as a new simulator or as new physics. Selling it as the
latter would be the BS William is trying to avoid.

---

## 7. Payoff for the cheap version (fixing our U-tube)

The accuracy-first analysis pays off directly for the cheap Noita lab, because
§3.2 says the expensive part (dynamics) is exactly the part the demo does **not**
need for its headline failure. The U-tube plateau (`PROBLEMS.md` #1) is a
*hydrostatic* question, and hydrostatics is the cheap, intrinsic case.

**Concrete cheap fix, derived from the accurate design (drop-in for Model C):**
1. **Once per frame, union-find the water cells** into connected bodies
   (`js/grid.js` already visits active cells; add a label pass over them). Cost
   `O(active cells)`.
2. **Per body, compute `V_b = Σ mass` and `footprint`**, then the target level
   `z*_b` (for uniform-width columns this is just `V_b / footprint`, exactly the
   `volume/footprint` the prototype's own `PROBLEMS.md` #1 already proposed).
3. **Nudge each body's cells toward `z*_b`** instead of relying on the
   `(m_i−m_j)/4` horizontal term and the `MaxCompress` diffusion. Cells below
   `z*_b` fill to full, cells above drain — *the level is read off, not diffused.*

This replaces the two mechanisms that cause the plateau — the ~0 horizontal push
between full cells and the `MaxCompress`-limited slow pressure diffusion
(`js/models.js` LEFT/RIGHT/UP branches; `js/constants.js` `MaxCompress`) — with a
single `O(N)` non-local structure (connectivity) plus an `O(1)` read-off. Predicted
effect: **U-tube `Δh → 0` regardless of tube height**, killing both the A/B freeze
(`Δh≈26.6`) and the C plateau (`Δh≈9–18`), and making `MaxCompress` irrelevant to
equalization (H4).

What it deliberately does **not** buy (honest scope, from §3.1): correct *wave
dynamics, splashes, or transients*. Those need the field representation. But the
demo's stated open problem is level equalization, and that is precisely the
intrinsic-hydrostatic case — so the cheap fix is not a hack, it is the accurate
design with the (unneeded) dynamic half deleted. The RPRM framing earns its keep
here as the thing that told us *which half we could delete and still be exact.*

The two honest caveats to carry into implementation: (i) connectivity is a real
non-local cost (you cannot avoid *some* global structure — that is §3.1's residue,
not a failure); (ii) the one-cell **halo** discipline from `PROBLEMS.md` #5 still
applies at the body/field boundary or mass will leak — the "minimal sufficient
extra state" (§1.8) does not go away just because the representation changed.

---

## 8. Bottom line and confidence

- **Fundamental vs artifact (conjecture for dynamics, high confidence for
  statics):** incompressibility's instantaneous global coupling is *conjectured*
  fundamental for dynamic receivers (elliptic limit / infinite sound speed; §3.1
  states this as a defensible insufficiency conjecture, not a proved impossibility)
  and is demonstrably a **representation artifact** for hydrostatic receivers
  (equilibrium is an intrinsic flat equipotential per connected body). William's "I
  wish it just fell" is right for *statics*; for *dynamics* we expect it is too
  optimistic but have not proved so.
- **Strongest RPRM-native idea (medium confidence it's *useful*, high confidence
  it's *not novel*):** represent water as labeled connected bodies whose level is
  *read off* from conserved volume + container geometry, so hydrostatic pressure
  is intrinsic. As an *object*, this is height-field + connected-components water,
  decades old. As an *RPRM result*, the non-obvious part is the **Prop-1/Prop-2
  boundary test** — a sound-but-incomplete acceptance predicate that says when this
  read-off is sufficient (to tolerance) and what to add back when it is not.
- **Biggest rename risk (high confidence):** almost every concrete ingredient is a
  standard technique (height-field, union-find water, strong lumpability, AMR /
  sleeping). RPRM's honest contribution is a *receiver-relative decision and
  justification discipline*, which the author's own Process Mechanics paper frames
  correctly and modestly.

*Confidence notes.* The physics of §2–§3 is verified against primary literature
(Stam 1999; Hunter's Euler notes for the elliptic/infinite-sound-speed claim;
Macklin & Müller 2013 for PBF; O'Brien & Hodgins 1995 / Kass & Miller 1990 for
height-field). The RPRM readings of §1 are grounded in direct quotes from the
repo. The one thing I have *not* done is *implement* the body/level fix and
measure H1–H5; those are stated as falsifiable precisely because they remain to
be run in the lab.
