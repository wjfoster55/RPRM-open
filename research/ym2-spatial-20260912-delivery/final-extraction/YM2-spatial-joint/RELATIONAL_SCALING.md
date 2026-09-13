# What relational scaling means in this attempt

The working principle is to transport the defining relationships along with
the scale change. That principle becomes a mathematical statement only after
the change and its preserved receiver are specified. The results below are
written algebraic derivations, not a claim that every physical constant varies
with viewpoint.

## Three different changes

1. A common color-frame rotation is gauge: rotate both vectors and their
   transport together. Dot products and loop traces stay fixed. No observable
   constant changes merely because we chose another gauge or drawing angle.
2. Changing the *relative* color angle changes the state. The magnetic energy
   of each separate cell can stay fixed while their joined behavior changes.
   The shared-edge force contains the exact contraction u·v.
3. Grouping cells changes the question and representation. The outer loop
   product W=UV is a valid new readout, but its fiber can contain different
   internal magnetic energies. A coarse description needs a retained split,
   a complete conditional fiber, or a justified effective law for its receiver.

The same multiplication law operates at every finite level of an ordered
path. This proves compositional reuse. It does not prove that the Hamiltonian
has the same functional form after interior links have been eliminated.

## Removing uniform unit factors without hardcoding them

Let the classical graph Hamiltonian be

    H = α/2 Σ_e |E_e|² + β V(Q),       α>0, β>0,
    V(Q) = Σ_faces (1 − 1/2 Tr Q_face).

All links use the same kinetic coefficient and faces the same magnetic
coefficient in this paragraph. With left electric coordinates and the
bi-invariant metric, the equations are

    dQ_e/dt = α E_e Q_e,
    dE_e/dt = −β grad_e V.

The electric self-bracket contributes zero because the kinetic norm is
adjoint invariant. Set

    P_e = sqrt(α/β) E_e,       τ = sqrt(αβ) t.

Direct substitution gives

    dQ_e/dτ = P_e Q_e,
    dP_e/dτ = −grad_e V,       H/β = 1/2 Σ |P|² + V.

Gauss is homogeneous in electric fields, so its zero constraint survives.
This is covariance between equations with rescaled units; the momentum
rescaling by itself is not a canonical transformation of the original fixed
symplectic form. The α=β=1 witness is therefore a representative of an
explicit positive-coefficient family. For initial E=0,

    d²(βV)/dt² = −αβ² Σ_e |grad_e V|².

Every strict separating witness remains separating for all α,β>0. We have
not selected new numerical constants at every level. Nonuniform link and
face weights leave relative ratios after normalization; these are additional
geometry/parameter ports. This calculation does not identify arbitrary changes
in coupling, shape or resolution with changes of units.

## Why the previous amplitude law needs a new check here

The accepted homogeneous continuum system has a cubic force, giving
A_λ(t)=λ A(λt), E_λ(t)=λ² E(λt). Compact group links do not obey that law
under arbitrary rescaling of a logarithm. Already along one SU(2) subgroup,
the plaquette potential contains 1−cos θ and its derivative sin θ. The
previous cubic-force transformation would require

    sin(λθ) = λ³ sin θ

at every θ. At θ=π/2, λ=2 the two sides are 0 and 8. Thus that *specified*
amplitude/time map is not a symmetry of this fixed-lattice potential. This
does not exclude other transformations with explicitly changed parameters.

The continuum-to-link relationship also retains the dimensionless
combination g a A for a short link (convention and path ordering specified).
Changing field amplitude, lattice spacing a, region size, and blocking are
different operations. Their continuum correspondence is an asymptotic
statement, not an exact identity for every coarse lattice. See SOURCES.md.

## Exact coarse-energy obstruction

At fixed exact outer matrix W=UV=(c,w), the complete split is

    U arbitrary in SU(2),     V=U⁻¹W.

Writing U=(a,u), the fine magnetic sum is

    B = 2−a−v0 = 2−[(1+c)a + u·w].

The four-vector (a,u) is a unit vector and the coefficient vector (1+c,w)
has length sqrt(2+2c). The Cauchy–Schwarz bound is attained and every
intermediate value is attained on the unit 3-sphere. Consequently the
*complete* magnetic-energy fiber at this supplied W is

    [2−sqrt(2+2c), 2+sqrt(2+2c)].

Here B is the dimensionless shape sum; physical magnetic energy is βB,
whose complete interval is multiplied by β. This is both an exclusion
theorem and a realization theorem. At W=−I the
interval collapses to {2}; otherwise it has positive width. The larger loop
can therefore support an exact energy range before its split is reopened.
It cannot generally support one exact fine energy from W alone. Neither
using a different label nor changing an overall coefficient removes that
fiber ambiguity. STATIC_JOIN.md gives noncommuting rational witnesses and
the reconstruction map.

Writing the interval [L,U], the threshold question B≤b* is yes for every
split exactly when U≤b*, and no for every split exactly when L>b*.
If L≤b*<U, the supplied data do not decide the actual split's answer. For
the distinct question whether *some* split meets the threshold, the answer
is yes exactly when L≤b*. The user’s backward/negative-question
idea helps precisely because the requested quantifier changes what must
be resolved.

## Next obligation

A reusable dynamical block must explain how its retained interface and
internal energy evolve when attached to another block. The composition must
preserve transport, shared-edge electric flux and Gauss matching; it must
also avoid counting a shared edge's kinetic energy twice. At any fixed finite
graph the full constrained link state provides such a source description.
An efficient smaller description with uniform control as blocks and
resolution grow has not been established by the two-cell construction.

This is the precise open scale question: can the extra relationships forced
by each join be generated and updated by a manageable law? It is more
informative than stipulating that every apparent constant must change, and
it makes the next counterexample or positive closure test concrete.
