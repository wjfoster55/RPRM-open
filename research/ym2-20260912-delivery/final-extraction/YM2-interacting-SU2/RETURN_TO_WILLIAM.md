# YM2 result and the issues it exposes

**The signed-transfer repair from YM1 does not close this interacting SU(2)
sector.** I derived an exact homogeneous reduction of the classical field
equations, kept Gauss's constraint, and found an exact separating pair. I then
tested one physically motivated refinement and found a further exact
obstruction. YM2's bounded research question is answered; a fully sufficient
reduced description remains an open research problem.

## What was tested

Think of `U_B(t)` as a curve showing magnetic energy over time. The proposed
summary remembers its present height `U_B`, its present slope `J`, and the
electric energy available in the same system. In YM1's fixed Maxwell mode,
the supplied equations let those quantities determine the curve's subsequent
motion. Here the magnetic potential contains actual products of noncommuting
SU(2) field components. The way the field is moving through that potential
matters in addition to the total amounts and the current transfer.

In a fixed box with `g=V=1` in stated reference units, the diagonal gauge
fields are `A_i=q_i T_i` and their electric velocities are `p_i T_i`. They obey

\[
 U_E=\tfrac12\sum_i p_i^2,\qquad
 U_B=\tfrac12(q_1^2q_2^2+q_1^2q_3^2+q_2^2q_3^2),\qquad
 \ddot q_i=-q_i\sum_{j\ne i}q_j^2.
\]

This is an exact invariant slice of the homogeneous SU(2) equations, with
Gauss zero. The broader bounded test carrier admits homogeneous constrained
states beyond this slice; a failure inside this slice is
enough to refute sufficiency on that carrier.

## The first issue: same transfer, different curvature

Take the same initial `q=(1,1,0)` and either
`p_A=(0,0,1)` or `p_B=(2/3,−2/3,1/3)`. Both give

`(electric energy, magnetic energy, signed transfer)=(1/2,1/2,0)`.

Nevertheless their magnetic-energy accelerations are `0` and `−8/3`.
Their future magnetic energies differ by
`U_B,A(t)−U_B,B(t)=(4/3)t²+o(t²)`, positive for all sufficiently small
positive times. All equalities at the starting instant are exact rationals.

Why can this happen? Imagine moving sideways along a contour of equal height
on a curved surface. Two directions can both give zero initial change in
height, yet the surface bends differently along those directions. Here the
surface is the magnetic interaction energy as a function of field components.
Equal electric energy fixes the speed, and zero transfer fixes one projection
of the direction. Those facts still leave different ways to move through the
curvature. The algebra pinpoints the missing contraction as `pᵀ(∇²W)p`.

This is not a failure of deterministic evolution. Each complete source state
has one lawful evolution. It is a failure of a description that merges those
states before asking for the evolution.

## The refinement: acceleration helps, then another distinction appears

I retained `K=d²U_B/dt²`. That separates the original pair and supplies the
quadratic Taylor data of the magnetic-energy curve. It is a derived dynamical
property of the original dynamics, not an added energy penalty.

But consider the same initial `q=(1,1,1)` with velocities
`p_+=(1,1,−2)` and `p_−=(−1,−1,2)`. Every pair of spatial components now has
a nonzero commutator. Both states give

`(U_E,U_B,J,K)=(3,3/2,0,−12)`.

Their third magnetic-energy derivatives are **+36 and −36**. The curves share
their height, slope and curvature, then separate at the next order:
`U_B,+(t)−U_B,−(t)=12t³+o(t³)`.

These two states run the same classical motion in opposite time directions.
At this instant the retained slope vanishes and the retained curvature is
unchanged by time reversal. The first remaining directional distinction lies
in the cubic interaction term. Asking both states for the same positive time
exposes it. Time reversal is not a gauge transformation.

There is more than an isolated pair here. Holding this initial `q` fixed,
every velocity on the circle `p_1+p_2+p_3=0`, `|p|²=6` gives those same four
numbers. Across that **complete conditioned circle**, the next derivative
ranges continuously from `−36` to `+36`. The retained summary loses a whole
family of interaction directions. A separate pair at unequal amplitudes
`q=(1,2,0)` confirms that the problem is not confined to equal initial fields.

## What still needs to be figured out

The immediate mathematical issue is to find a joint description that retains
the necessary interaction geometry **and can update itself**. Adding one
derivative solves one distinction but creates the obligation to update that
derivative. Here the exact next expression is

`dot K = V(∇³W[v,v,v] − 4 vᵀ(∇²W)∇W)`.

Any successful continuation of this particular refinement must distinguish
states for which that expression differs. Retaining it would be a possible
next step, but this work does not establish whether it closes, whether a
different set of invariants works better, or whether a short derivative list
eventually suffices. Two failed summaries are not a proof that every reduced
description fails. The standard full constrained field state already works;
the open question is what useful structure can be retained without repeatedly
reopening all of it.

There is also a separate scale-of-physics issue. We have tested spatially
homogeneous classical fields in a fixed periodic box. Their non-Abelian
interaction is real within the theory, but the omitted spatial modes,
quantization and limiting quantum theory have not been supplied. Solving the
retained-state problem here would still leave those bridges to establish.

## What was checked, and the mass-gap boundary

Exact rational calculations agree through independent Hessian and full
color-vector ODE-series methods. An independent reviewer used a separate
scalar-series recurrence. Gauss and total energy are proved conserved, six
states were transported consistently by an actual color gauge rotation, and
commuting and initially-flat controls were checked.

A small illustration at `t=0.01`, with 100 and 200 RK4 steps, gives:

| Pair | First magnetic energy | Second magnetic energy |
|---|---:|---:|
| Original summary | 0.499999991668 | 0.499866679814 |
| Acceleration refinement | 1.499406164319 | 1.499394165639 |

The largest observed absolute energy drift was about `7.11×10⁻¹⁵`; the largest
step-comparison difference was about `7.33×10⁻¹⁵`, below the declared `10⁻¹⁰`
diagnostic tolerance. These illustrate the exact argument and are not rigorous
numerical error bounds. All rows are included in `RESULTS.json`.

**No quantum mass-gap bound follows.** The result identifies information that
a classical description loses; it says nothing about the existence or absence
of a positive quantum vacuum excitation gap. The missing broader bridge is a
controlled quantum construction with a positive spectral bound that survives
the omitted modes, continuum limit and infinite-volume limit. The accepted
YM1 `1/L` finite-box caution remains intact. See `PROBLEM_BRIDGE.md` for the
precise obligation.

The action and homogeneous mechanics are established literature. The displayed
witnesses, contraction audit and conditioned fiber were derived in this run;
no claim is made that they are new to the literature. Original RPRM meanings
remain broader than this realization: acquired usable relationships,
construction and reopening access are not reduced to a tuple or a file hash.

The portable package contains the derivation, checker, full rows, sources,
reviews and manifests. Final replay evidence is deliberately outside the
already-hashed ZIP. Publication remains on hold; no paper, installation,
commit, push, merge, paid compute or other-lane work was performed.
