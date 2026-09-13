# Poincare as a closure reference

Date: 2026-09-12. Evidence: primary-source theorem audit plus explicitly identified deductions; no new Millennium-problem proof. Scope: the finite-extinction route to Poincare, and three further problem contracts. Clay currently lists Poincare as solved and RH, Navier–Stokes, and Hodge as unsolved. [Clay status](https://www.claymath.org/millennium-problems/)

## Contract and distinct proof obligations

The Poincare input is a closed, connected, simply connected smooth three-manifold with an arbitrary initial Riemannian metric. Pointwise metric equality, diffeomorphism, and homeomorphism are distinct relations. The requested readout is its homeomorphism type, with the stronger smooth classification available in dimension three. The operation is forward Ricci flow, `∂t g = -2 Ric`, extended by a prescribed surgery procedure. Surgery changes the underlying manifold and requires a topology ledger; it is not an invertible coordinate change. The target readout can close without recovering a unique initial metric or a complete family of surgery histories.

**1. Monotonicity produces geometric control through an additional argument.** Perelman's entropy functional satisfies an identity with a nonnegative squared-tensor integral as its derivative. For a smooth flow on a closed manifold over a finite time interval, a hypothetical sequence of collapsing, curvature-controlled balls would force the entropy infimum to approach negative infinity; monotonicity transports this contradiction to the fixed initial metric. The resulting noncollapsing estimate has the form `Vol B(x,r) ≥ κ r^n` under the specified curvature and scale conditions. In three dimensions, noncollapsing plus almost-nonnegative curvature yields rescaled high-curvature neighborhoods modeled by ancient solutions. Neither statement says curvature stays globally bounded through a singularity. [Perelman, entropy paper, §§3–4, 8, 12](https://arxiv.org/pdf/math/0211159)

**2. Continuation through singularities must be justified.** With normalized initial data (sectional curvature bounded in absolute value by one; every unit ball has at least half the Euclidean unit-ball volume), sufficiently small surgery cutoffs admit flows with pinching, noncollapsing, and canonical-neighborhood estimates on every finite time interval. Canonical neck/cap models license controlled surgery; the cutoff scales are bounded away from zero on fixed finite intervals. The bounds may deteriorate as the time horizon increases. Surgery removes a controlled positive volume, preventing an accumulation of surgery times there. These are analytic and construction estimates, not consequences of a diagram's finite number of labels. Extinct flows reconstruct connected sums of spherical space forms and `S² × S¹`. Simply connectedness eliminates nontrivial fundamental-group factors, leaving `S³`. [Perelman, surgery paper, §§1, 4–6, 8](https://arxiv.org/pdf/math/0303109)

The final sentence uses the standard connected-sum fundamental-group calculation after the cited surgery classification. A metric rescaling accommodates arbitrary smooth initial metrics; normalization is an analytic setup condition, not a restriction to already-round manifolds.

## What forces finite extinction

**Perelman's original route.** Theorem 1.1 assumes a closed oriented three-manifold whose prime decomposition has no aspherical factors, and permits every initial metric. An aspherical factor has vanishing higher homotopy groups. For the irreducible case, choose a nontrivial relative homotopy class in the space of contractible loops relative to constant loops. Define `A(t)=inf_Γ sup_(c∈Γ) inf_(disks spanning c) area`, with `Γ` representing that class. Topology supplies the nontrivial family; curve shortening and Gauss–Bonnet give

```text
D⁺A ≤ -2π - (1/2) R_min A,
R_min ≥ -3 / [2(t+C)],                 C > 0.
```

For `B=A/(t+C)`, therefore,

```text
D⁺B ≤ -2π/(t+C) - A/[4(t+C)²] ≤ -2π/(t+C),
B(T) ≤ A(0)/C - 2π log((T+C)/C).
```

The right side eventually becomes negative, whereas `A≥0`. Almost distance-nonincreasing surgery maps preserve the comparison on surviving relevant components. Kneser finiteness and prime decomposition extend the argument beyond the irreducible case; the homotopy-sphere case also has a direct tracking argument. This excludes perpetual survival, rather than asserting that one fixed disk remains smoothly minimal throughout. [Perelman, finite extinction, §§1.1–1.5, 3](https://arxiv.org/pdf/math/0307245)

**The sphere-width route is distinct.** Colding–Minicozzi's Theorem 1.1 starts with a closed orientable prime non-aspherical three-manifold. A nontrivial sphere sweepout class defines width `W(t)` by minimizing the maximal sphere-map energy. Minmax analysis supplies minimal-sphere limits and control of near-maximal slices. With `D⁺` denoting the upper forward Dini derivative, their comparison is

```text
D⁺W ≤ -4π + 3W/[4(t+C)],
D⁺[(t+C)^(-3/4) W] ≤ -4π(t+C)^(-3/4),
(T+C)^(-3/4)W(T)
  ≤ C^(-3/4)W(0) - 16π[(T+C)^(1/4)-C^(1/4)].
```

Gauss–Bonnet supplies `4π`; the scalar-curvature bound supplies `3/4`. Nonnegativity contradicts indefinite existence. Their Corollary 1.2 extends extinction to closed orientable manifolds without aspherical prime factors, with surgery. The width argument does not require the limiting minimal spheres to be embedded. [Colding–Minicozzi, §§1–4](https://arxiv.org/pdf/math/0308090)

**Correction retained.** Morgan–Tian corrected their exposition's curve-curvature evolution calculation: an omitted term changes the total-curvature estimate's dependence to include initial length. Compact initial curve families bound both needed quantities, so their extinction application survives. Their note explicitly identifies Perelman's original bound as having the correct term. The correction illustrates why the uniform-family estimate is a genuine obligation. [Morgan–Tian correction, opening discussion](https://arxiv.org/pdf/1512.00699)

## The transferable lemma and its boundary

**Elementary deduction.** Suppose a nonnegative quantity `B` exists whenever a process survives, is continuous between locally finite jumps, has no upward jumps, and satisfies `D⁺B(t)≤-q(t)` between jumps for a continuous `q≥0`. Scalar comparison gives `B(T)≤B(0)-∫₀ᵀq(t)dt`. If that integral is unbounded, survival cannot continue for all time. For a nonsmooth candidate, proving the comparison regularity and jump behavior is part of the contract.

Four ingredients are separate: a persistent witness, a lower bound, quantitatively sufficient accumulated decrease, and preservation through allowed transitions. A coercive estimate has the further job of controlling a dangerous state norm or escape mode; a monotone label does not automatically do so. Here noncollapsing and canonical-neighborhood bounds support the geometric construction, while the area/width comparison forces extinction.

**Hostile controls.** `B(t)=exp(-t)` is strictly decreasing and nonnegative forever: its total decrease is finite. A flat three-torus has `Ric=0`, hence a stationary Ricci flow; it is aspherical and excluded from the extinction theorem. Removing the topological condition would make the proposed theorem false.

For the task's supplied carry lift `L_k=F_k+10C_k=F_0+121k`, strict growth makes distinct times distinct in the lifted readout. It supplies no upper budget, so unlimited progression is compatible with the formula. Restricting `k≤K` stops at an imposed carrier boundary. To infer geometric extinction, a physical spectral gap, or regularity, one must construct an adapter preserving the target law and readout, and prove the corresponding bound independently. This audit does not certify the carry formula's implementation.

## Further problem obligations

The first column below gives official mathematical targets; the last column is this audit's proposed test of an RPRM adapter, not a claimed equivalence or established solution method.

| Problem and official target | Missing port / proposed closure obligation |
|---|---|
| **RH — OPEN.** For the meromorphic continuation of `ζ(s)=Σ n^(-s)` from `Re(s)>1`, every nontrivial zero must have real part `1/2`. [Bombieri, §I](https://www.claymath.org/wp-content/uploads/2022/05/riemann.pdf) | Account for every zero at unbounded height. A carry encoding must preserve this analytic zero condition and exclude off-line zeros globally. A finite digit cycle, a finite zero computation, or reflection symmetry alone does not do that. |
| **Navier–Stokes — OPEN.** In three dimensions, `ν>0`, prove one of Fefferman's alternatives A–D: global smooth unforced solutions for every admitted smooth divergence-free datum on `R³` (rapid spatial decay, bounded energy) or the periodic domain; alternatively exhibit admitted smooth data and force for which the corresponding global solution does not exist. Forces in the breakdown alternatives obey the stated decay/periodicity conditions. [Fefferman, pp.1–2](https://www.claymath.org/wp-content/uploads/2022/06/navierstokes.pdf) | A positive approach must supply enough uniform control to continue the actual PDE solution at every finite time; a negative approach must certify breakdown with the admitted data. Preserving total energy or proving a lattice trace terminates leaves uncontrolled spatial concentration and the passage to the PDE limit as separate obligations. |
| **Hodge — OPEN.** For every smooth projective complex variety and every rational class in `H^(2p)(X,Q) ∩ H^(p,p)(X)`, produce a rational linear combination of codimension-`p` algebraic-cycle classes. The integral or merely Kähler versions are different, false generalizations. [Deligne, §§1–2](https://www.claymath.org/wp-content/uploads/2022/06/hodge.pdf) | The joint completion is actual cycles with rational coefficients and the required cohomology equality. A diagonal-shaped representation must preserve algebraicity, rather than just a vector-space decomposition. Deligne's §4 already distinguishes the algebraic diagonal of `X×X` from the unresolved general algebraicity of its individual Künneth components. |

Disposition: the cited Poincare machinery provides an established reference theorem and a reproducible logical comparison. The proposed transfers from carry/sawtooth/diagonal operations remain **OPEN** until their typed adapters and domain-specific closure estimates are supplied. No complete completion fiber for RH, Navier–Stokes, or Hodge is claimed.
