# YM2 and the mass-gap ambition

YM2 establishes a concrete limitation on **classical observable preservation**:
even with non-Abelian interaction and Gauss enforced, `(U_E,U_B,dU_B/dt)` can
merge states with different future magnetic energy. Adding `d²U_B/dt²` still
merges such states. The first missing term is velocity relative to interaction
curvature; the next includes a cubic directional interaction contraction.
These are derived counterexamples in an exact homogeneous classical sector.

This supplies **no nontrivial quantum spectral bound**. We constructed no
quantum Hilbert space, vacuum, self-adjoint quantum Hamiltonian, continuum limit
or inequality excluding excitations near the vacuum. The Hamiltonian used in
YM2 is a classical energy function. Its Hessian and energy-transfer derivatives
are not the quantum excitation spectrum. A classical trajectory falling in
magnetic energy is also not losing total energy: its electric energy rises by
the same amount.

The official broader target requires existence of a nontrivial quantum
Yang–Mills theory on four-dimensional unbounded spacetime with a positive
vacuum excitation gap; finite-volume constructions need control of the limiting
theory. See [Jaffe–Witten, §4 and §§5–6](https://www.claymath.org/wp-content/uploads/2022/06/yangmills.pdf).
Its definitions are established literature; YM2's counterexamples do not come
from that source.

**One precise bridge still missing:** construct a controlled quantum
description retaining the relevant interacting, gauge-invariant structure and
prove a vacuum spectral inequality that survives restoring the omitted spatial
modes and taking the continuum and infinite-volume limits. In a regulated
Hamiltonian formulation, the intended form is

\[
 \langle\psi,(\widehat H_{a,L}-E_{0,a,L})\psi\rangle
 \ge \Delta\|\psi\|^2,\qquad
 \psi\perp\mathcal V_{a,L},\quad \Delta>0,
\]

where `ψ` belongs to the physical quadratic-form domain (the left side denotes
the energy quadratic form), and `𝒱_{a,L}` is the entire vacuum eigenspace.
The requirement is a common positive bound for suitable normalized approximants and a
proved nontrivial physical limit to which that bound transfers. This statement
is an obligation, not a claim that such approximants or their limit were
constructed here. Restoring the omitted field modes is part of that bridge,
not something secured by the exact classical homogeneous ansatz. The fixed
classical `g` used in YM2 is not a proposed prescription for renormalized
quantum cutoff dependence.

The accepted YM1 `1/L` lesson is unchanged: a positive free-mode spacing in
one finite box is compatible with spacings tending to zero as the box grows.
We neither reran that result nor transplanted its formula to interacting SU(2).
Likewise, quantizing homogeneous Yang–Mills mechanics would not by itself
provide the full field-theory inequality. It removes degrees of freedom whose
effect on the limiting spectrum has not been controlled here.

Classically, scaling diagonal initial data as `q→εq`, `p→ε²p` sends the
quartic-plus-kinetic energy to `ε⁴H`, while nonzero commutators remain nonzero
for every `ε>0`. This is a derived elementary classical observation, not a
quantum no-gap argument. Quantum uncertainty, the vacuum, and spectral
normalization are separate structures. Conversely, classical nonlinearity
alone supplies none of them.

The useful progress toward the ambition is therefore diagnostic and specific:
we now know two ways a candidate retained description can discard lawful
interaction information before a quantum bridge is even attempted. That helps
formulate a better mathematical state-description problem. It proves neither
the existence nor the absence of a mass gap and is not yet a quantitative
bound toward one.
