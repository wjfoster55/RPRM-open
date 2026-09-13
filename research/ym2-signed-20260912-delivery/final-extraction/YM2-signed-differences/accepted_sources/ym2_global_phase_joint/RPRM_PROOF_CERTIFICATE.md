# Proof-donut certificate for the dynamical joint

12 September 2026. This is a written mathematical certificate, not output
from a proof assistant or from the finite-table proof-donut implementation.
Its task is to say exactly which missing ports have now been filled, by
which proofs, and which ports remain open.

## 1. The RPRM connection and its limits

The project [proof-donut source](accepted_sources/rprm/proof-donut.md)
asks for types, coverage, transport, seams, continuation, and landing
around a specified question. It does not infer an interior from its
surroundings without a law covering that interior. Its executable finite
tables do not themselves certify an arbitrary continuous dynamical system.

The relevant project operations are question descent, operational descent,
all-future preservation, and LIFT–SPIN–LAND in
[operations.md](accepted_sources/rprm/operations.md). A lift and inverse
alone do not show that the operation survives the trip: the evolution must
commute with that representation. This packet supplies those equations
separately for a classical and a quantum carrier.

The historical Prestige/number-operation sources describe a compound
relationship becoming a usable unit while retaining its context and
ancestry. They do not restrict the broader concept to a Gram matrix,
invariant quotient, integer arity, or this physical model. Here the
sixteen-scalar joint is one concrete realization: a complete physical
state of a specified finite graph becomes a reusable input to a proved
updater. Calling it a joint does not add a physical law.

Likewise, absolute distinction is not being redefined as ordinary orbit
equivalence. We specify which distinctions this particular receiver keeps:
every gauge-invariant classical phase observation and its future under the
declared Hamiltonian. Equality of occurrences is still stronger than equal
values: the central edge is one shared edge in both loops, including in the
kinetic energy and Gauss constraints.

## 2. Classical aperture and enclosure

**Given:** the open two-square, seven-link graph, SU(2), all-vertex zero
Gauss, the source Hamiltonian, an admissible phase state, and elapsed real
time. **Question:** can a finite relational joint preserve the state and
all its allowed continuations even where the earlier trace chart fails?

| Obligation | Supplied certificate | Coverage and status |
|---|---|---|
| Types and equality | `T*SU(2)^7` at zero Gauss modulo six vertex gauges; tree target `(U,V,P,Q)` at residual Gauss modulo common conjugation | Written contract; real exact states, fixed graph |
| Coverage | Unique based tree gauge, explicit electric reconstruction, complete residual orbit fiber | Every source, including central/collinear configurations and singular phase orbits |
| Transport | Equality of canonical one-forms and full seven-link Hamiltonian | Preserves the actual source kinetic coupling, not a guessed two-link metric |
| Joint seams | Four color vectors `u,v,P,Q` share one Gram matrix and one coherent orientation table; squared residual Gauss is zero | Complete common SO(3) fiber, not independent pair completions |
| Continuation | Dot/cross compiler, product rule, source coercivity and ODE uniqueness | One polynomial invariant vector field, all ranks, every real continuation time |
| Landing | Recover electric energy, magnetic energy, signed transfer, outer trace, and every gauge-invariant phase readout from the joint | ONE physical gauge class per admitted joint; raw gauge representatives remain a complete orbit family |

The proofs are in [GLOBAL_TREE_PHASE.md](GLOBAL_TREE_PHASE.md) and
[GLOBAL_INVARIANT_JOINT.md](GLOBAL_INVARIANT_JOINT.md). Here is the logical
core, with maps made explicit. Let `Z0` be the global tree zero-Gauss source,
`C:Z0 -> J` the invariant joint, `F` the source vector field, and `F_J` the
polynomial updater. The construction proves

```text
C(z)=C(z')  iff  z and z' have the same simultaneous SU(2) orbit,
dC_z F(z) = F_J(C(z)),
C(Flow_t(z)) = FlowJ_t(C(z))   for every real t.
```

The last line is a theorem, not the definition of a tested trajectory.
For each admitted joint, any lift supplies a global solution. Smooth
polynomial local uniqueness makes its projected solution independent of
the lift. Time reversal supplies the inverse. Consequently every finite
sequence of allowed continuations also commutes, by composition. This is
the legitimate “prove the rule once, reuse it on the covered class” step.
It does not claim a finite list of examples proves unbounded coverage or
that one fixed graph covers all spatial refinements.

The scalar compiler has a separate structural-induction proof. Every
expression formed by the declared finite grammar of addition,
multiplication, vector scaling, dot and cross products reduces to the
retained data. This proves all finite expressions in that grammar, not
arbitrary new operations or closed-form solutions of the ODE.

## 3. Hostile cases that changed the answer

**The old coordinate hole is actually reachable.** At `U=V=I`,
`P=e1,Q=e2`, the exact source gives

```text
u(t) cross v(t) = 15 e3 t^2 + O(t^3),
Delta(t) = 225 t^4 + O(t^5).
```

Regular configurations on either side of zero reach the central
configuration in finite time. A proof restricted to `Delta>0` therefore
does not cover all continuations from that domain. This is failure of a
configuration chart, not a claim that a Hamiltonian flow crosses full
phase-orbit strata. The new joint works on both and needs no inverse
angle or discriminant.

**Lengths and pairwise angles still forget orientation.** At `a=b=0`,
`u=e1,v=e2`, compare `(P,Q)=(e3,-e3)` with `(-e3,e3)`. They satisfy
Gauss and have identical complete Gram data and energy. Their future
outer trace starts with derivatives `+6` and `-6`. Coherent triple
products distinguish the two. This hostile case establishes a need for
orientation for this all-observable receiver; it does not prove that
every proposed energy-only receiver needs all sixteen scalar entries.

**The coarse spatial seam remains open.** The accepted prior static
result exhibits equal coarse holonomy with unequal fine magnetic energy.
Completing the global fixed-graph phase joint does not make that energy
constant on a coarsening fiber. A refinement adapter must supply the
additional joint content or change and justify its receiver.

## 4. The quantum aperture is a new contract

The quantum carrier is `L²(SU(2)^7, Haar)^SU(2)^6`, all spins admitted,
with the source Laplacian, bounded plaquette potential, and an explicit
self-adjoint domain. A classical phase point is not identified with a
wavefunction. Quantization is supplied here as a physical modeling choice.

For the complete configuration quotient `x=(a,b,w)`, the Haar measure
becomes the uniform density `2/pi²` on `Delta>=0`. Pullback `W` is unitary.
Transport of the entire operator domain, not just the regular differential
expression, gives

```text
H W = W H_J,
exp(-itH/hbar) W = W exp(-itH_J/hbar)   for every real t.
```

The domain is inherited from the compact source. No arbitrary boundary
condition at an aligned or central configuration is used to manufacture a
gap. This is the quantum transport and continuation certificate in
[GAP_BRIDGE.md](GAP_BRIDGE.md).

Complete spin-network coverage plus the graph's girth proves the exact
free electric gap `6 alpha hbar²`. A nonnegative magnetic potential and
a constant trial state then prove the interacting estimate

```text
E1-E0 >= 6 alpha hbar² - 2 beta.
```

This lands at a bound for the chosen finite graph. It leaves the exact
interacting spectrum OPEN. Compactness/positivity gives an isolated simple
vacuum for each fixed finite parameter choice, but does not supply the
uniform estimate needed in the limit.

## 5. The still-open central port: scaling of the vacuum

The quantum ratio `r=beta/(alpha hbar²)` survives a change of energy unit.
It must travel with the receiver; fixing it silently would hide a physical
change. The normalized bound is `gamma/(alpha hbar²)>=6-2r`.
Changing the number of plaquettes, their spacing, or the coupling creates
a family contract beyond coordinate re-expression of this graph.

For the true vacuum `psi0`, the exact spectral question becomes a weighted
Poincaré inequality for `nu=psi0² Haar`. On the trace quotient its best
constant satisfies

```text
gamma = (alpha hbar²/2)
        inf_{mean_nu(f)=0} integral(grad f · M grad f) dnu
                          / integral |f|² dnu.
```

The infimum uses nonzero functions in the transported form domain. This
is a precise new aperture, not a solution for `psi0`. The patch criterion
and exact correlation control in [NEXT_GLUE_LEMMA.md](NEXT_GLUE_LEMMA.md)
expose what a scalable joint proof must provide. Local spectral estimates
must be combined with a uniform control on correlations of the same
vacuum and the same shared link occurrences.

## 6. Evidence grade

The continuous results here are written proofs, independently reviewed
within the declared model. The three new exact checkers corroborate finite
algebraic and combinatorial steps. Their receipts do not prove the
checkers' general soundness or the analytic theorems they use.

The repository has general Lean declarations for fiber and operational
preservation, as documented in the included formal-proofs source. No new
SU(2) theorem was instantiated or checked in Lean in this task. No compiler
was installed. Hashes bind the exported files; they are not mathematical
certification. Publication remains on hold.
