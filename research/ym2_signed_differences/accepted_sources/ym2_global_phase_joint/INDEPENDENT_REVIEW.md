# Independent review of the global invariant and quantum bridge proofs

12 September 2026. Reviewed [GLOBAL_INVARIANT_JOINT.md](GLOBAL_INVARIANT_JOINT.md)
and [GAP_BRIDGE.md](GAP_BRIDGE.md) against their displayed definitions and
derivations. The reviewer separately derived the source tree reduction in
[GLOBAL_TREE_PHASE.md](GLOBAL_TREE_PHASE.md), so this is independent review
of the invariant and quantum arguments, not an independent review of that
reviewer's own tree note.

**Disposition:** no substantive mathematical defect found in either written
argument within its stated carrier. The invariant result has written proof
coverage at every rank and for every finite continuation time. The quantum
result has a written finite-graph operator construction and gap estimate,
conditional on its explicitly supplied quantization and normalization.
Neither is a proof-assistant result or a continuum Yang--Mills theorem.

## 1. Invariant joint: coverage and continuation

The admission and complete-fiber proof survives the singular ranks. Given
a positive semidefinite rank-at-most-three Gram matrix, a real three-row
Gram factor exists. At rank below three all principal triple minors vanish,
forcing every retained triple to be zero. At rank three, selecting one
nonzero triple fixes the orientation of a factor; the mixed-minor
identities fix every other triple. There is no further omitted orientation
compatibility condition for a four-vector tuple. Conversely, equal Gram
and triple data give the same SO(3) orbit. In rank at most two, the unused
orthogonal direction permits adjustment to a proper rotation. This proves
the entire orbit fiber rather than just separating generic examples.

The squared-Gauss admission polynomial is sufficient because it is used
after the Gram/triple conditions have established an actual real vector
realization. On that realization it is the squared Euclidean norm of the
correct tree moment map. Its zero condition therefore cannot silently
admit a nonzero Gauss vector. This ordering avoids treating an arbitrary
formal polynomial zero as a physical phase state.

All six displayed dot/cross rules were checked against vector identities.
In particular

```text
(X_i cross X_j) cross (X_k cross X_l)
 = tau_ijl X_k-tau_ijk X_l.
```

The ten-expression vector module is closed under the stated grammar.
Its coefficient nonuniqueness at lower rank does not affect its evaluated
vector or any scalar readout. The updater is a specified finite polynomial
program on the sixteen scalar coordinates; it is not being confused with
a finite polynomial formula for elapsed-time flow.

The global continuation proof uses the right order of implications:

1. The full tree vector field has global solutions by energy coercivity
   and compact configuration space.
2. Differentiation of the invariant map gives the displayed polynomial
   updater identically on source points, at every rank.
3. A lift of any admitted initial joint supplies an all-time solution
   that stays in the reached image.
4. Local uniqueness for the ambient polynomial ODE makes that solution
   unique and independent of the chosen source lift.

This proves invariant-image preservation; it does not assume preservation
from selected vanishing minors. The negative-time map supplies the inverse.
The regular decoder is restricted to Delta>0, and its singular failure is
not imported into the global updater.

The Gram-only hostile pair was recalculated directly. For
`a=b=0,u=e1,v=e2,P=e3,Q=-e3`, the true velocities give
`dot u=-3e2,dot v=-3e1`, hence `dot w=6`. Reversing the two momenta gives
`dot w=-6`. Both have the stated common Gram matrix, zero Gauss and kinetic
energy 3. Thus the orientation triples retain an actual continuation
distinction even within the zero-Gauss source.

One notation-only suggestion was sent to the invariant author and is now
corrected: the bracket is written with an explicit cross-product symbol.
This changes no formula or proof.

## 2. Quantum measure and operator domain

The Haar pushforward was recomputed from two independent Haar quaternions.
The product scalar density is

```text
(4/pi^2) sqrt(1-a^2) sqrt(1-b^2),
```

and the conditional cosine density is `1/2`. The change
`w=ab-sqrt(1-a^2)sqrt(1-b^2)z` therefore gives the stated constant density
`2/pi^2`. Integrating the allowed w interval gives
`Vol(K)=2(pi/2)^2=pi^2/2`, checking normalization independently.

The complete compact-group configuration quotient makes the pullback W
unitary onto the physical invariant subspace. The pointwise singular
boundary has measure zero, while operator behavior there is supplied by
the inherited source domain. The note correctly distinguishes those two
facts: a null boundary does not by itself license arbitrary boundary
conditions for a degenerate differential expression.

Direct differentiation of the three columns of M gives

```text
div_column(M)=(-12a,-12b,-18w).
```

This matches the source chain rule, where each edge in a simple fundamental
trace loop contributes eigenvalue -3 and the loop lengths are 4,4,6.
The source domain is the Sobolev domain of the elliptic Laplacian on the
closed compact product group. Adding a bounded smooth potential preserves
that domain; restriction to a reducing invariant subspace preserves
self-adjointness and compact resolvent. Transporting the entire domain by
W defines one operator at all quotient strata. The ensuing functional
calculus intertwining is therefore stronger than equality of differential
expressions on the regular interior.

## 3. All-spin free gap and the interacting estimate

The support proof is valid without a spin cutoff. In the complete
spin-network decomposition, a vertex incident to exactly one nontrivial
irreducible edge has no invariant tensor. Every nonempty support hence
contains a cycle. Girth four forces at least four positive-spin edges, each
with Casimir at least 3 in the declared generator norm. This gives
`lambda_1(T)>=6 alpha hbar^2`. A fundamental plaquette trace attains the
bound and is orthogonal to the constant, proving equality. The all-trivial
sector has exactly one vector, so there is no extra zero-energy sector
omitted by the support argument.

The cited complete fixed-graph decomposition is supported directly by
[Baez, Section 2, Lemma 3](https://arxiv.org/pdf/gr-qc/9411007). Its graph
orientation convention differs from the source presentation, but incoming
versus outgoing dual representations leave the no-single-edge invariant
argument unchanged. The normalization `4j(j+1)` agrees with the unit-S3
Laplacian and is explicitly reconciled with the usual spin convention in
[Jakobs et al., equation (42)](https://arxiv.org/html/2304.02322v2#S3.SS4).

The variational subtraction is correct. Nonnegative potential gives
`E_1(H)>=lambda_1(T)` with eigenvalues ordered by multiplicity. The
normalized constant gives the distinct trial bound `E_0(H)<=2 beta`.
Together they prove

```text
E_1-E_0 >= 6 alpha hbar^2-2 beta.
```

No step assumes that the interacting vacuum is constant or that the
mean-zero subspace is orthogonal to that unknown vacuum. Positivity
improvement on the connected compact source also gives a simple positive
ground state for every fixed finite beta. Gauge invariance then places
that state in the physical Hilbert space. Compact resolvent gives an
isolated physical ground eigenvalue even when the displayed quantitative
estimate becomes inconclusive.

The weighted ground-state Poincare formula has the correct measure,
orthogonality condition and coefficient `alpha hbar^2/2`. The source form
domain controls the meaning of the gradient expression on the quotient.
The surviving quantum ratio `beta/(alpha hbar^2)` is correctly retained;
the classical momentum rescaling changes the commutation scale and does
not remove that ratio.

## 4. Scope and execution evidence

The graph-family extension of the same trial argument loses positivity as
`6 alpha hbar^2-N_p beta`; it does not assert a vanishing true gap.
The note's limit boundary is consistent with the official problem's
requirement for a four-dimensional nontrivial quantum theory and a
positive vacuum gap, and with its discussion of uniform finite-volume
control. [Jaffe and Witten, Sections 4-6](https://www.claymath.org/wp-content/uploads/2022/06/yangmills.pdf)
supplies that distinction. The finite-graph estimate does not solve the
continuum vacuum or gap fiber.

No old checker, eigensolver, trajectory integrator, spin truncation or proof
assistant was run as part of this review. The new tree checker was executed
separately by its author and passed, as recorded in its own receipt. The
implementation addendum below records the subsequent independent audit and
default-mode execution of the completed invariant and quantum checkers.

## 5. Implementation addendum

The completed [invariant checker](check_invariants.py) and
[quantum checker](check_quantum.py) were inspected and each was executed
once in default mode. Both passed their saved-receipt comparisons without
writing the receipts. No implementation-to-claim mismatch was found in
their declared bounded checks.

For the invariant checker, the concrete source route uses componentwise
quaternion multiplication and a quaternion commutator. The retained route
uses the ten formal vector coefficients with Gram/triple bilinear rules.
The code implements the displayed dot, cross, adjoint and derivative signs.
Exact dual arithmetic differentiates the sixteen invariants and, on the
regular overlap, the decoded momenta. Its sparse coefficient zero test
keeps a coefficient with zero value but nonzero tangent, avoiding loss of
first-order information at singular states. The image evaluator uses all
principal minors for positive semidefiniteness, the determinant for the
four-by-four rank bound, all mixed triple minors, and the squared-Gauss
condition. The regular inverse is a test helper invoked on regular data;
it is absent from the global compiler and is not a general admission API.

The observed invariant receipt counts are 3,008 checks: 39 comparisons of
the source differential with the invariant updater, 24 proper-rotation
controls, 18 regular-decoder derivative controls, and 2,600 primitive
basis dot/cross controls, with additional image and hostile-state checks.
These counts describe exact evaluations on thirteen named states and their
specified rotations. They do not constitute an exhaustive test of all
real phase points or the infinite expression grammar; those claims retain
their written proofs. Default comparison parses JSON and compares the
recomputed structured result, so harmless receipt formatting differences
are intentionally ignored.

For the quantum checker, all 128 edge subsets are enumerated directly
from the graph endpoints. The four nonempty supports passing the necessary
no-leaf condition have edge counts 4,4,6,7. A separate all-fundamental
seven-edge control correctly distinguishes that necessary support condition
from singlet sufficiency at the two trivalent vertices. Gaussian-integer
Pauli products check the metric and fundamental Casimir. Sparse integer
polynomial differentiation checks the three cometric column divergences
against the independently checked simple loop walks of lengths 4,4,6.
Default comparison is an exact serialized-text comparison with the saved
quantum receipt.

Both checkers use explicit failure exceptions for their new verification
conditions, so those conditions are not disabled by Python optimization.
The quantum result explicitly lists its analytic inputs and exclusions:
support enumeration does not enumerate all spins, prove Peter--Weyl
completeness, choose an operator domain, or establish the interacting
spectral theorem. Its conditional coefficient 6 is consistent with its
computed minimum support 4, fundamental Casimir 3 and prefactor 1/2.
The executed commands were:

```powershell
python -I -B research/ym2_global_phase_joint/check_invariants.py
python -I -B research/ym2_global_phase_joint/check_quantum.py
```
