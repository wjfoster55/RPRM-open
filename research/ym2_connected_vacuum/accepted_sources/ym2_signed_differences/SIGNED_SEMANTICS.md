# Signed differences: retained references, stacking, and reversal

Date: 2026-09-12. Evidence grade: self-contained written elementary proofs and
exact counterexamples. This note contains no formal proof, numerical experiment,
Yang–Mills dynamics calculation, or quantum mass-gap theorem.

The useful candidate in the present question is that signed differences and
retained offsets may expose a simpler construction, especially when a completed
object provides a reference from which to work backwards. Several exact versions
of that candidate survive below. Its unrestricted forms require corrections:
changing signs does not itself remove nonlinear interactions, restore forgotten
data, or enlarge a spectral gap.

## Source context and contract

The source context is the active task's signed-difference proposal, together with
the following local distinctions:

- [Recovered number operations, U25](accepted_sources/rprm/PRESTIGE-AND-NUMBER-OPERATIONS.md#u25--correction-same-landing-different-construction-route)
  at source lines 120–124 preserves equal useful landings reached by different
  constructions. The quotation is evidence of that distinction, not a new task
  instruction or a definition of all the operations below.
- [Core, section 15](accepted_sources/rprm/core.md#15-residual-balance-pressure-and-negative-views)
  distinguishes negative coordinates, residuals, complements, reciprocals and
  reversals, and keeps equal-valued coordinate occurrences separate.
- [Core, section 19](accepted_sources/rprm/core.md#19-the-affine-aperture-chart) makes an
  origin and endpoint chart explicit and restricts inverses to admitted images.
- [Operations, section 4](accepted_sources/rprm/operations.md#4-observe-project-car-and-adapter)
  transports both a query and an operation through an invertible representation;
  [section 6](accepted_sources/rprm/operations.md#6-fivefuture-and-traceback) distinguishes predecessor compatibility
  from the actual historical predecessor.

All scalar examples use exact rational or real arithmetic on explicitly bounded
input sets, with the bounded reached image declared as output. No wrap,
saturation, rounding, or extension of an output to an input carrier is implicit.
The probabilistic carriers are finite. The Hamiltonian example has two real
coordinates, bounded input, and a fixed finite time horizon. These are separate
contracts; shared minus signs do not identify their operations.

The supplied ports are the named expression or map, its parameters, and its
input data. Requested readouts are its value, inverse fiber, retained variance,
or conditioning as explicitly named below. A proposed application to a new
quantum carrier remains OPEN until its operator, measure or inner product,
domain, and retained receiver are supplied.

## 1. Addition can be written with subtraction, with nesting retained

For `x,y` in the admitted interval `[-R,R]`, `R>0`, the exact identity is

```text
x + y = x - (0 - y).
```

Both expressions reach `[-2R,2R]`. Thus subtraction and the constant zero form
an adequate expression language for addition. The parentheses preserve the
operation tree; they are mathematical data.

The proposed flat expression, in ordinary arithmetic, instead gives

```text
1 + x - y - 1 = x - y.
```

For example, with `R>=3`, `x=2,y=3` gives `-1`, whereas `x+y=5`. The source idea can be
retained by repairing the inner sign:

```text
1 + x - (0 - y) - 1 = x + y.
```

This correction fixes that scalar identity. It does not claim that an
occurrence, retained route, higher-level constructor, or contextual operation
is exhausted by its scalar value.

Unary negation `N(x)=0-x` is an involution on `[-R,R]`: `N(N(x))=x`.
A stack of `k` copies of this same unary operation therefore depends only on
the parity of `k`. Binary subtraction has two ordered ports and a different
fiber. For the relation `z=x-y`, with `x,y in [-R,R]`, the complete joint fiber
at admitted `z in [-2R,2R]` is

```text
{(z+t,t) : t in [-R,R] intersect [-R-z,R-z]}.
```

Every listed pair subtracts to `z`, and every lawful pair appears by taking
`t=y`; this proves coverage. At `z=2R` or `z=-2R` it is ONE. At every interior
`z` it is MANY, with the displayed family as the complete answer. An external
request outside the declared output carrier is an admission error. If the
same equation is instead posed with any real target admitted, `|z|>2R` gives
NONE in the declared input carrier. Supplying `y` fixes a unique candidate
`x=z+y`, whose membership still has to be checked.

There is a stronger positive reading of stacked minuses. Let

```text
J_a(x) = a - x.
J_b(J_a(x)) = x + (b-a).
```

Each `J_a` reflects about `a/2`; for composition, use its reached image as
the next input. Two reflections with different retained references produce a
translation. Taking `a=0,b=y` gives `y-(0-x)=x+y`. Thus changing references
between sign reversals carries information that a mere parity count loses.
This is an exact mechanism worth preserving from the intuition.

## 2. The expressive boundary is affine, until another operation is admitted

Fix a finite expression tree whose leaves are variables `x_1,...,x_d` and
fixed real constants, and whose only internal operation is binary subtraction.
On any admitted bounded box of variable values, its result has the form

```text
c + n_1*x_1 + ... + n_d*x_d,   each n_i an integer.
```

Here `c` is an integer linear combination of the supplied constants; it need
not itself be an integer. Every intermediate expression has a bounded reached
image because the expression is finite and the input box is bounded.

**Proof.** A variable leaf has one coefficient 1 and all others 0; a constant
leaf has no variable contribution. Subtracting two such forms subtracts their
constant terms and integer coefficient vectors. Structural induction covers
every expression in this syntax. Conversely, repeated copies and subtraction
can express every integer coefficient, with constants supplied as needed.

Therefore a fixed subtraction-only expression does not compute a general
variable product `x*y`. On the four admitted inputs `{0,1}^2`, any affine
function has zero mixed difference

```text
f(1,1)-f(1,0)-f(0,1)+f(0,0) = 0,
```

whereas `x*y` has mixed difference 1. This is a finite hostile case.
Similarly, on `[1,2]`, a reciprocal cannot be affine: an affine function
matching `1/x` at 1 and 2 would take value `3/4` at `3/2`, while the required
value is `2/3`. These counterexamples address this precise fixed-expression
claim. They do not rule out a richer algorithm or a restricted special case.

Multiplication by an integer count `n in {0,...,N}` can be executed by a
loop that repeatedly adds `x`, with each addition compiled as subtraction.
Variable `n` requires a loop/control state or a family of expression trees;
those are additional supplied operations, and the reached values lie in
`[-NR,NR]` for `x in [-R,R]`. A negative integer count additionally uses its
sign. This does not give real multiplication for a non-integer count through
an unexplained finite repetition rule.

Division likewise names a relation and a domain. For `a=b*q`, if `b != 0`
the sole algebraic candidate is `q=a/b`, intersected with the admitted
quotient carrier. If `b=0,a!=0` the fiber is NONE. If `b=0,a=0`, every
admitted `q` belongs to the fiber; its cardinality determines NONE, ONE, or
MANY. A bounded repeated-subtraction algorithm for positive integers can
instead return quotient and remainder. That distinct output does not define
a reciprocal at zero or exact division on arbitrary real inputs.

## 3. The -0.6 and +0.4 offsets give a centered, unequal-probability pair

Let `B` take values 0 and 1, with `P(B=1)=p=3/5`. Define `Z=B-p`.
The exact finite probability table is

| B | Z | Probability |
|---|---|---|
| 0 | -3/5 | 2/5 |
| 1 | +2/5 | 3/5 |

The map `B -> Z` is invertible on these two-point carriers, with inverse
`B=Z+3/5`. Its mean and variance are

```text
E[Z] = (-3/5)*(2/5) + (2/5)*(3/5) = 0,
Var(Z) = (9/25)*(2/5) + (4/25)*(3/5) = 6/25.
```

The two signed values do not sum to zero: their unweighted sum is `-1/5`.
Their probability-weighted mean is zero. The signs are coordinates;
the probabilities are nonnegative weights. Assigning probability `1/2` to
each offset changes the law and gives mean `-1/10`.

For a fixed positive integer `n`, retain separate occurrences
`Z_1,...,Z_n`, then explicitly supply the sum readout `S_n=sum_i Z_i`.
Its reached values lie in `[-3n/5,2n/5]`, and

```text
Var(S_n) = sum_i Var(Z_i) + 2*sum_{i<j} Cov(Z_i,Z_j).
```

With independent copies, this is `6n/25`; the averaged readout `S_n/n`
has variance `6/(25n)`. With the same bit copied into all `n` occurrences,
it is `6n^2/25`. For `n=2` the variances are respectively `12/25` and
`24/25`, despite identical one-coordinate marginal distributions. The
coupling between occurrences is therefore a concrete place to test the
stacking intuition. The unequal offsets alone do not specify that coupling.

## 4. Moving an origin, reversing a direction, and reversing time differ

For a physical scalar `X in [-R,R]` and a supplied fixed origin `a`, let
`xi=X-a`. Changing to a supplied origin `b` gives

```text
eta = X-b = xi+(a-b).
```

This leaves differences between two physical points unchanged. Reflection
`eta=b-X` reverses those differences. Neither operation by itself changes
the time order of a trajectory.

A moving reference can be useful, but its evolution is part of the law.
For a finite sequence `x_k` and supplied references `a_k`, define
`d_k=x_k-a_k`; then

```text
d_(k+1)-d_k = (x_(k+1)-x_k) - (a_(k+1)-a_k).
```

For example, if both trajectories obey `F(x)=x^2`, their difference obeys

```text
F(a+d)-F(a) = 2*a*d + d^2.
```

Taking admitted `|a|,|d|<=R` gives a bounded one-step example. Centering
reveals a linear term and a residual quadratic term; it does not erase the
quadratic interaction. Retaining only `d` also loses the coefficient `a`
unless it is known from the retained reference trajectory. A useful local
approximation can arise for small `d`, but that is an approximation with a
bound on `d^2`, rather than an exact removal of the interaction.

## 5. Exact sign and origin changes preserve the relevant gap quotient

First fix a finite probability space `(Omega,mu)` with positive masses and
a real, self-adjoint nonnegative operator `A` on `L^2(mu)` satisfying
`A*1=0`. Define the Dirichlet form and the centered Rayleigh quotient by

```text
E_mu(f) = <f,A*f>_mu,
Q_mu(f) = E_mu(f)/Var_mu(f),   Var_mu(f)>0.
```

For `g=s*f+c`, with nonzero supplied real `s` and constant `c`,

```text
Var_mu(g) = s^2*Var_mu(f),
E_mu(g) = s^2*E_mu(f),
Q_mu(g) = Q_mu(f).
```

**Proof.** Subtracting the mean gives
`g-E[g]=s*(f-E[f])`. Since `A*1=0`, the constant term and cross terms in
the energy vanish; self-adjointness removes the remaining cross term.
Thus for translation or negation (`s=+1` or `s=-1`) the variance itself
is unchanged. An arbitrary scaling changes variance but not this quotient.
The infimum of `Q_mu` over nonconstant observables is therefore unchanged
under these invertible reparametrizations. If the kernel contains additional
nonconstant functions, this infimum is zero; no positive gap is assumed.

This statement concerns the centered quotient. Translating `f` generally
changes the uncentered denominator `||f||^2`; silently exchanging that
denominator for variance would change the question.

For a bijective state-coordinate map `T:Omega -> Omega'`, retain the
pushforward law `mu'=T_*mu` and define

```text
U:g -> g o T,
A' = U^(-1) A U.
```

Then `U` is unitary, `U*1=1`, and direct substitution preserves variance,
Dirichlet energy, and their quotient. In particular the entire spectrum of
these finite-dimensional operators and every spectral gap are unchanged.
Changing the coordinates while leaving an incompatible measure or operator
in place defines a different model.

As a complete finite check, take `A=I-P`, where `P f=E_mu[f]*1`.
Then `E_mu(f)=Var_mu(f)` by expansion, so `Q_mu(f)=1` for every
nonconstant `f`. The two-state Bernoulli law above has gap 1 under this
specified operator, before and after centering. Its variance `6/25` is
therefore not itself a gap. Different transition rates would specify a
different operator and could produce another gap.

For a quantum Hamiltonian the corresponding finite-dimensional statement
uses unitary conjugation: `H'=V H V^(-1)` preserves eigenvalues and gaps.
Subtracting a scalar `E_0 I` changes the energy origin and preserves all
energy differences. A general unbounded Hamiltonian requires its operator
domain to be transported as well; the finite proof here does not establish
that domain or a continuum limit for a separate model.

## 6. An exact reversible system can be equally unstable backwards

Fix `lambda>0`, `R>0` and a finite horizon `T>0`. On two real canonical
coordinates use the Hamiltonian

```text
H(q,p) = lambda*q*p,
q_dot = lambda*q,
p_dot = -lambda*p,
Phi_t(q,p) = (exp(lambda*t)*q, exp(-lambda*t)*p).
```

Start in `K=[-R,R]^2`; for `|t|<=T` the whole trajectory lies in the
explicit bounded enclosure `[-R*exp(lambda*T),R*exp(lambda*T)]^2`.
At a selected time the map is a bijection from `K` onto `Phi_t(K)`, with
inverse `Phi_(-t)` restricted to that reached image. There is ONE exact
predecessor for a fully specified reached endpoint and specified time.

The involution `J(q,p)=(p,q)` is antisymplectic, preserves `H`, and satisfies

```text
J o Phi_t o J = Phi_(-t).
```

Thus this example has an explicit Hamiltonian time-reversal symmetry.
Nevertheless, for `t=T`, Euclidean perturbation amplification obeys

```text
||D Phi_T||_2 = exp(lambda*T),
||D Phi_T^(-1)||_2 = exp(lambda*T),
condition_2(D Phi_T) = exp(2*lambda*T).
```

Forward evolution expands a small `q` error. Backward evolution expands a
small `p` error by the same factor. Restricting perturbations to an interior
neighborhood of the admitted image keeps this a valid local conditioning
comparison. Both maps are cheap to evaluate by the displayed formula, so
inverse existence, expression size, computational cost, and sensitivity to
input error must be assessed separately.

Backward inference can still be easier for a particular supplied terminal
condition, retained history, stable direction, or chosen receiver. The
counterexample refutes a universal implication from reversibility to better
backward conditioning. This linear hyperbolic system is not evidence of
chaos, is not claimed to model SU(2) Yang–Mills dynamics, and supplies no
vacuum or quantum spectral-gap conclusion.

## What this contributes to the open quantum obligation

The signed-difference proposal now has three concrete uses: compile additive
expressions into one primitive with its references retained; expose the
covariances that make repeated offsets accumulate; and choose reference
coordinates that display the linear and residual terms of an interaction.
Those are useful operations with exact scope and hostile controls above.

To obtain new spectral information, the next construction must do more than
invertibly recode the same quadratic form. It must provide an estimate for
the actual target energy or Dirichlet form relative to the actual target
variance or ground-state orthogonal norm. A favorable reference might make
that estimate accessible; the needed comparison constants must be bounded
in the stated regulator, volume, coupling, and limiting regime. Establishing
that comparison and the applicable vacuum/domain remains OPEN here.

Verification for this note consists of the written induction, complete
subtraction-fiber argument, exact rational calculations, direct conjugation
identities, and the explicitly solved finite-time Hamiltonian example.
No executable test suite was run for this document-only contribution.
