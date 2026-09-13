# Independent mathematical review of the spatial joint packet

12 September 2026. Review by the agent deriving the separate seven-link
force witness. Reviewed `STATIC_JOIN.md`, `RELATIONAL_SCALING.md`, and
`PHASE_CLOSURE.md` in this new folder. No earlier YM2 tests were rerun and
no other author's files were edited by this reviewer.

**Assessment:** the static algebraic proofs, complete fibers, parameter
normalization and regular two-plaquette Hamiltonian are mathematically
consistent with the declared plus-i convention and finite-graph source.
The force witness and the reduced cometric were derived independently.
The clarifications below concern naming, endpoint quantifiers, literal loop
ordering, and one short omitted rank argument; none changes the main result.

## Static joint: signs and complete fibers

The Pauli identity gives

`(a,u)(b,v)=(ab-u.v, a v+b u-u cross v)`

for `U=aI+i u.sigma`. The sign is essential and is consistently used in
the static note. Expanding a third product gives

`Sc(Q1 Q2 Q3)=a1 a2 a3-a3 G12-a1 G23-a2 G13+tau123`.

Thus the orthogonal rational triple has the asserted values `91/125` and
`-37/125`, with `tau=+64/125` and `-64/125`. These are distinct proper-
rotation classes despite identical pair Gram data.

For product replacement, independently expanding the new vector
`z=a_i v_j+a_j v_i-v_i cross v_j` gives

`z.v_l=a_i G_jl+a_j G_il-tau_ijl`,

`z.(v_l cross v_m)=a_i tau_jlm+a_j tau_ilm-G_il G_jm+G_im G_jl`.

These agree with (S7), including signs. The restriction to unchanged other
slots and simultaneous use of the old tuple makes replacement valid when
the replaced slot also supplies one or both input factors. Symmetry,
alternation and the separately reset diagonal cover the remaining entries.

The pair image condition and representative prove both necessity and
sufficiency, including central endpoints. The common `SO(3)` orbit is the
complete raw pair fiber: its span has dimension at most two, so an
orthogonal extension can always be chosen proper. This justifies the ONE
physical class result, not merely a collection of representatives.

For arbitrary finite tuples, the Gram factor plus one common determinant
orientation gives the complete `SO(3)` orbit. The mixed-minor equations
`tau_I tau_J=det G[I,J]` are sufficient with PSD, rank and diagonal constraints:
a nonzero principal triple fixes orientation and every other triple; at
rank at most two all triple squares vanish. No unmentioned third orientation
branch or independent choice of triple signs survives these identities.
The explicit full-tuple carrier and warning about graph word relations
prevent an unsupported image claim for dependent loop choices.

For a fixed full outer matrix `W=(c,w)`, the raw split fiber
`(U,U^-1 W)` for arbitrary `U in SU(2)` is complete. Its magnetic shape sum is
the linear functional

`B_fine=2-[(1+c)a+u.w]` on `(a,u) in S^3`.

The coefficient vector has length `sqrt(2+2c)`. Both extrema and every
intermediate value occur, giving the exact interval in (S10). At `W=-I`
the readout is uniquely 2 while the raw split fiber remains nonunique.
The two displayed noncommuting split witnesses give exactly `26/25` and
`18/25`. Keeping the full outer matrix is therefore still insufficient for
the fine magnetic sum. The claim is at the tuple level and is not extended
to arbitrary fine electric or internal-link configurations.

## Scaling and threshold questions

For `H=alpha/2 sum|E|^2+beta V`, direct differentiation verifies

`P=sqrt(alpha/beta)E`, `tau=sqrt(alpha beta)t`,

`dQ/dtau=P Q`, `dP/dtau=-grad V`, `H/beta=|P|^2/2+V`.

At zero electric field, the distinction between the dimensionless shape
and magnetic energy is

`V''(0)=-alpha beta sum|grad V|^2`,

`(beta V)''(0)=-alpha beta^2 sum|grad V|^2`.

The scaling note has the latter coefficient correctly. All positive uniform
coefficients preserve a strict witness difference. The exclusion of zero
or negative coefficients, the retained nonuniform ratios, and the warning
that momentum scaling alone is not canonical are appropriate.

**Clarification requested from the author:** in the coarse-energy section,
the displayed `B=2-a-v0` and its interval should be called the dimensionless
magnetic shape sum, or explicitly restricted to unit magnetic coefficient.
For physical magnetic energy `beta B`, multiply the entire interval by
`beta`. Any threshold must specify which of these two quantities it tests.

For a supplied complete interval `[L,U]` and threshold question `B<=b*`,
the exact quantifiers and endpoints are:

- Every split answers yes iff `U<=b*`.
- Every split answers no iff `L>b*`.
- The actual split's answer is unresolved iff `L<=b*<U`.
- Some split answers yes iff `L<=b*`.

**Clarification requested from the author:** use these inequalities instead
of only "below" or "straddles". In particular, `b*=L<U` is ambiguous for
the actual split even though the threshold lies at an endpoint. If `L=U`,
the first two cases already determine the answer, including equality.

The trigonometric control rejects the specific inherited cubic-force
amplitude/time map: `sin(lambda theta)=lambda^3 sin theta` fails at
`theta=pi/2, lambda=2`. It does not exclude every possible changed-parameter
transport. Likewise `U^2 V^2 != (UV)^2` rejects the stated power-map
homomorphism without asserting that no other coarse map could work.
These scopes are correctly distinguished from resolution changes and
continuum limits.

## Regular phase chart: independent cometric and closure audit

Use the exact graph and tree in `DYNAMICS.md`, with common-base pair
`L=U`, `R=V`, scalar parts `a,b`, vector parts `u,v`, and
`w=Sc(VU)=Sc(UV)`. For an explicit independent all-link calculation define

`q=Vec(VU)=b u+a v+u cross v`,

`h=Vec(UV)=b u+a v-u cross v`.

In edge order `(a,b,c,d,l,s,r)` from the graph, the three scalar gradients
in tree gauge are

```text
grad Sc(U) = (-u,  0, +u,  0, +u, -u,  0),
grad Sc(V) = ( 0, -v,  0, +v,  0, +v, -v),
grad w     = (-q, -q, +q, +h, +q,  0, -q).
```

The labels `a,b` in this edge list are graph-edge names, distinct from the
scalar ports. Contracting over all seven unit-metric links gives exactly
(P3): diagonal entries `4(1-a^2),4(1-b^2),6(1-w^2)`, and off-diagonal
entries `w-ab,3(b-aw),3(a-bw)`. In particular the kinetic metric was not
replaced by a two-chord product metric. The all-link force witness is the
contraction `-(1,1,0)M(1,1,0)^T` at zero momentum and reproduces both exact
accelerations in `DYNAMICS.md`.

On the regular domain the effective vertex action is free. The trace map
has rank three and its kernel is the 18-dimensional gauge tangent space.
Zero Gauss is exactly annihilation of that space. Thus every constrained
covector is uniquely a pullback of one `p in T*D`. This establishes the
physical ONE fiber and canonical symplectic reduction claimed in (P1)--(P2).
No extra unconstrained chord momenta are being assumed. The representative
formula for `V` has squared norm `b^2+(d^2+Delta)/(1-a^2)=1`, as required.

Differentiating `(1/2)p^T M p+2-a-b` reproduces every sign and coefficient
in (P6). Because the source canonical form and Hamiltonian descend,
ordinary ODE uniqueness supplies the stated full continuation while the
configuration remains regular. This argument is stronger than agreement
of a few derivatives. The chart is a partial continuation contract, and
the text correctly does not assert invariance of its regular domain.

**Ordering clarification sent to the author:** under the common-base words
in `DYNAMICS.md`, `VU=RL` is the product with literal shared-edge cancellation.
`UV=LR` has the same trace and represents a cyclically rebased perimeter;
the full matrices need not coincide. This affects a prose description of
the product, not the cometric or any trace formula. Naming the word and the
trace equality explicitly prevents an accidental stronger matrix claim.

The claimed boundary rank is correct. To complete its short proof, on
`Delta=0` with both factors noncentral, the leading 2-by-2 minor is

`16(1-a^2)(1-b^2)-(w-ab)^2 = 15(1-a^2)(1-b^2)>0`.

If `a=+/-1` and `b` is noncentral, the `(b,w)` principal minor equals
`15(1-b^2)^2>0`; the other case is symmetric. Thus rank is exactly two
away from the central corners and zero at those corners. This supplementary
argument was sent to the phase author. The nonzero electric circulation at
the all-identity configuration is a valid Gauss-constrained state, and `J=0`
there excludes it from every finite canonical `p` in this chart. It is a
real coverage boundary rather than a defect in the source equations.

## Review evidence and limits

This is an independent written mathematical audit and exact algebraic
cross-check, not a formal proof-assistant verification. The force/cometric
derivation above was sent to the phase author separately before reviewing
their final formulas. The new force checker's rational matrix, gauge and
Gauss checks remain documented in `RESULTS_DYNAMICS.json`; this review did
not rerun older suites or conduct numerical trajectory simulations.

No blocking mathematical error was found in the reviewed derivations. The
listed prose clarifications were sent to the owning authors for resolution.
No assertion of global singular-phase closure, larger-lattice aggregation,
continuum control, quantum construction, mass gap, minimal storage or
measured performance follows from the reviewed results.

**Resolved disposition:** the owning authors applied all four requested
clarifications, and this reviewer reread the changed passages.
`RELATIONAL_SCALING.md` now explicitly distinguishes dimensionless `B` from
physical `beta B`, scales the interval by `beta`, and states the exact
universal, actual-split and existential threshold inequalities.
`PHASE_CLOSURE.md` now names the literal outer word `VU=RL`, states
`Tr(UV)=Tr(VU)`, and includes the principal-minor proof of boundary rank two.
Its added reverse decoder `p=M^-1 J E=M^-1 dot x` also follows directly
from `E=J^T p` on the regular domain. No requested correction remains open
from this review; the historical requests above are retained as the audit
trail. The receipt `RESULTS_PHASE.json` was inspected as recorded finite
execution evidence without rerunning any older suite.
