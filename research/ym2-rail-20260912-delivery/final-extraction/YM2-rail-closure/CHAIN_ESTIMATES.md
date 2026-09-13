# A chain certificate for reference handoffs

12 September 2026. Bounded continuation of the accepted
[vacuum-chart identities](accepted/handoff/VACUUM_ATLAS.md),
[trial-reference calculation](accepted/handoff/TRIAL_REFERENCE.md), and
[returned result](accepted/handoff/RESULT.md). Their existing checks are
accepted evidence and were not rerun. This note gives written derivations
and a four-state exact example. It changes neither the accepted YM coupling
window nor the physical Hamiltonian.

The useful distinction is between **exact transport of a shared state**,
**accumulation of an approximation defect**, and **a uniform estimate for
the actual conditional law**. The first has a telescoping certificate. The
second needs control of signed partial sums or a proved contraction. The
third needs a collective estimate as well as one-coordinate control.

## 1. Contract and supplied ports

The primary carrier is each admitted finite open lattice graph `G` with
configuration manifold `SU(2)^E`, all spins, product Haar probability `mu`,
the accepted link metrics, and gauge constraints at every vertex. A chain
has a declared finite length `L`; a claim uniform in chain length or graph
volume quantifies over a specified family of these finite objects. Graphs
are fixed within each chain. The handoff index is an ordering coordinate,
not a physical time variable.

Fix one dimensionless physical Hamiltonian `A=T-rS` and its accepted
positive normalized vacuum `psi`. References `phi_k` are smooth, strictly
positive, normalized, and gauge invariant. Function equality is almost
everywhere; displayed derivatives use smooth representatives. The receiver
retains the shared physical state, Hilbert norm, full transported operator,
conditional laws, and their quantitative estimates. Reference-diffusion
gaps and full-Hamiltonian gaps are different readouts.

The supplied ports are `A`, the references and their exact ratios. Where
approximations are used, their update defects must also be supplied as
functions or proved bounds in the declared receiver. The missing analytic
port is a graph-uniform estimate for the actual correction or actual
conditional influences. The inverse of a normalized exact chart transition
is **ONE**. A complete actual-correction estimate beyond the accepted
window remains **OPEN**. A finite reference list or a closed loop does not
enumerate the completion fiber of that analytic problem.

Write, modulo additive constants where appropriate,

```text
ell_k = 2 log phi_k,
h_k = log(phi_(k+1)/phi_k),
v_k = log(psi/phi_k),
H_n = sum_(k=0)^(n-1) h_k.
```

For real `g`, use the accepted all-exterior seminorms

```text
d(g) = max_i osc_i(g),
D_ij(g) = sup |g(x_i,x_j,z)-g(y_i,x_j,z)
                -g(x_i,y_j,z)+g(y_i,y_j,z)|,
b(g) = max_i sum_(j!=i) D_ij(g).
```

The supremum admits every displayed coordinate choice and exterior `z`.
These are seminorms, constants vanish, and `D_ij=D_ji`. The correction
budgets called `d_v,b_v` in the accepted packet are `d(2v),b(2v)` here.

## 2. Exact composition cancels reference drift

**Proposition C1: exact telescoping.** For every prefix of an exact chain,

```text
H_n = log(phi_n/phi_0),
v_n = v_0-H_n,
ell_n+2v_n = 2 log psi.                                (C1)
```

If log coordinates were independently centered, the second and third
equalities hold modulo the corresponding scalar. The equality of
normalized densities is exact.

**Proof.** Multiply consecutive reference ratios. Their numerator and
denominator occurrences cancel. Substitution of the definitions gives
the other identities. In particular, for every ordered coordinate pair,

```text
Delta_i Delta_j(ell_n+2v_n)
 = Delta_i Delta_j(ell_0+2v_0).                         (C2)
```

Here `Delta_i` is a coordinate replacement difference with all other
coordinates retained. Cancellation happens before absolute values or
suprema. Consequently a certificate for the total mixed log density
should estimate the left side directly whenever its signs are known.
Replacing it by `D_ij(ell_n)+D_ij(2v_n)` is sufficient but can lose the
whole cancellation. The same applies to one-coordinate oscillations.

There is an equally exact operator certificate. Define

```text
U_k f = phi_k f,
J_(k+1,k) = U_(k+1)^(-1) U_k,
K_k = T-grad(log phi_k) dot grad,
R_k = (A phi_k)/phi_k.
```

Then

```text
J_(n,n-1) ... J_(1,0) f = exp(-H_n) f,
||exp(-H_n)f||_(L2(phi_n^2 mu)) = ||f||_(L2(phi_0^2 mu)),
K_n+R_n = J_(n,0)(K_0+R_0)J_(0,n).                    (C3)
```

An exact loop with `phi_L=phi_0` has `H_L=0` and total transition `I`.
Every prefix still has to carry its residual `R_k`. These equalities
certify fixed-Hamiltonian transport; they cannot certify an independently
changed Hamiltonian or the gap of `K_k` alone.

Square roots introduce no loss. The transition multiplier is
`sqrt(dnu_0/dnu_n)` and intermediate square-root ratios telescope. Its
operator norm between its stated weighted Hilbert spaces is exactly one.
For unnormalized `exp(w_k)`, the scalar
`(1/2)log(Z_k/Z_(k+1))` belongs in `h_k`; these scalars telescope too.
Dropping them can break norm preservation, although `d` and `b` cannot
detect that scalar error.

## 3. Approximate transport: retain the signed defect

Let `vhat_k` be a proposed correction. Define its handoff defect by the
relation

```text
e_k = vhat_(k+1)-vhat_k+h_k          modulo constants,
E_n = sum_(k=0)^(n-1) e_k,
delta_k = v_k-vhat_k.
```

**Proposition C2: complete defect accounting.**

```text
vhat_n = vhat_0-H_n+E_n,
delta_n = delta_0-E_n,
ell_n+2vhat_n = ell_0+2vhat_0+2E_n.                    (C4)
```

**Proof.** Sum the defining differences. This is exact algebra and does
not require the errors to be independent, random, or small.

Thus the exact calibration budget at prefix `n` is
`d(2delta_0-2E_n), b(2delta_0-2E_n)`. A convenient sufficient certificate
is a proved common bound for `d(2E_n),b(2E_n)` over **every required
prefix**, followed by one triangle inequality against the initial error.
Adding the separate positive norms of all step defects is a weaker
certificate. A bound only on the final loop sum controls that endpoint;
it says nothing about an intermediate prefix.

Three distinct sufficient mechanisms illustrate the difference:

1. **Exact handoffs:** `e_k=0`. The initial calibration error is carried
   unchanged, regardless of reference drift.
2. **Bounded primitive:** `e_k=B_(k+1)-B_k`, with independently proved
   `d(2B_k)<=D_B` and `b(2B_k)<=B_B` at every prefix. Then
   `E_n=B_n-B_0`, giving `d(2E_n)<=2D_B` and
   `b(2E_n)<=2B_B`, independent of chain length. The functions `B_k`
   must be supplied or constructed; defining them as uncontrolled partial
   sums does not establish the bounds.
3. **Summable increments:** `sum_k d(2e_k)<=D_E` and
   `sum_k b(2e_k)<=B_E`, uniformly over the admitted family. Then the
   same two bounds hold for every `E_n`.

Merely asserting `d(2e_k)<=epsilon` and `b(2e_k)<=epsilon` gives at most
`n epsilon`. Alternating equal and opposite defects have zero two-step
sum; equal-signed defects grow. A closed final sum cannot distinguish
those possibilities at all the intermediate prefixes.

This certificate controls calibration relative to the **complete proposed
density** `phi_k^2 exp(2vhat_k)` after normalization. It does not by itself
bound the raw correction `v_k` relative to a freely wandering `phi_k`.
For the latter readout the exact necessary object is
`v_0-H_k`, and it too needs uniform local and mixed bounds. A poor chart
can make that correction large while leaving the actual measure unchanged.

## 4. A quantitative surrounding-relation certificate

The following matrix calculation is a possible analytic port, not a claim
that its hypotheses have been proved for the YM correction.

Let a finite nonnegative vector `x` contain the required error readouts,
for example all `osc_i(2delta)` and all `D_ij(2delta)`. Suppose independent
local-response estimates establish

```text
x <= a+A x,
A >= 0,  a >= 0,
A s <= rho s,       s>0,       rho<1.                 (C5)
```

The inequality is componentwise. The source `a`, response matrix `A`,
positive weights `s`, and common strict margin must be derived from the
equation and the admitted neighborhood of states. They cannot be inferred
from the desired gap or merely from the existence of an exact chart.

**Proposition C3: weighted comparison.** Under (C5),

```text
x <= (I-A)^(-1)a = sum_(j>=0) A^j a.
```

In particular, if `a<=eta s`, then `x<=eta s/(1-rho)`.

**Proof.** Iterate the inequality `m` times:
`x<=sum_(j=0)^(m-1) A^j a+A^m x`. In the weighted maximum norm
`||y||_s=max_i |y_i|/s_i`, positivity gives `||A||_s<=rho`.
The final term tends to zero; the geometric series converges. This is a
written comparison theorem on each finite vector carrier. Uniform
one-link and mixed-row budgets additionally require that the resulting
weights have uniformly bounded components in the one-link slots and
uniformly bounded row sums in the pair slots. A small spectral radius
alone does not bound an arbitrary forcing vector in an arbitrary receiver.

For actual approximate updates, a more general independently proved
recurrence is

```text
x_(k+1) <= A_k x_k+a_k.
```

For a declared period of `p` updates, put

```text
M = A_(p-1) ... A_0,
c = sum_(j=0)^(p-1) A_(p-1) ... A_(j+1) a_j,           (C6)
```

where the empty matrix product is `I`. If `M s<=rho s`, `c<=eta s`, and
`rho<1`, then at complete periods

```text
x_(np) <= [rho^n ||x_0||_s+eta(1-rho^n)/(1-rho)] s.    (C7)
```

The intermediate matrix products and partial forcing sums also need
uniform bounds to certify all prefixes. Formula (C7) follows by the same
iteration. A closed chart loop says its **exact Hilbert-space transition**
is `I`. It says nothing about `M`, which describes propagation of an
approximation estimate in another receiver. Conversely, exact transport
alone preserves the calibration error in (C4); it supplies no strict
contraction. A strict inequality in (C5) or (C7) must come from an actual
analytic correction mechanism.

For the present YM route the missing source law remains the accepted
equation

```text
K_phi v = -Q_phi R_phi+(1/2)Q_phi |grad v|^2.
```

A useful new estimate would derive (C5), a controlled update recurrence,
or bounded signed primitives from this equation with constants uniform in
volume. An `L2` Poisson inverse alone does not establish a mixed-oscillation
estimate for its nonlinear right-hand side.

## 5. A weighted collective certificate can improve a row-sum test

This section gives a second matrix receiver, for **spatial conditional
influence**, distinct from the update-error matrices above. Let `L` be
the actual normalized log density, and let `C_ij` be the supremum over
exteriors differing only at `j` of the total-variation distance between
their actual one-link conditional laws at `i`. An independently proved
majorant `C<=B`, with zero diagonal and nonnegative entries, suffices.
One available bound is

```text
B_ij = tanh(D_ij(L)/4).                                (C8)
```

If only a calibrated decomposition `L=Lhat+2delta+constant` is known,
replace `D_ij(L)` in (C8) by
`D_ij(Lhat)+D_ij(2delta)`. If signed mixed differences are available,
combine them before taking the supremum, as in (C2).

**Proposition C4: weighted influence certificate.** Suppose for every
admitted graph one supplies finite positive weights `s_i` such that

```text
B s <= q s,                  q <= q_* < 1,             (C9)
```

with a common strict margin. Suppose every actual one-link conditional
law has gradient Poincare constant at most `c_*`, uniformly over all
exteriors. Then every conditional block has gradient Poincare constant
at most `c_* /(1-q_*)`. The accepted physical forest cover consequently
gives

```text
gap_phys(A) >= [W/(2 Lambda c_*)](1-q_*).               (C10)
```

**Proof.** The accepted heat-bath oscillation estimate evolves the
coordinate-oscillation column vector under `C^T-I`. Its weighted sum
obeys

```text
s^T (C^T-I) delta = (Cs-s)^T delta
                 <= -(1-q_*) s^T delta.
```

Hence the heat-bath semigroup contracts this seminorm at rate `1-q_*`.
At each finite graph `min_i s_i>0`, so total oscillation and the supremum
norm of a centered function are bounded by a finite constant times that
weighted seminorm. For a bounded centered `f`, this gives
`<f,P_t f><=K_f exp(-(1-q_*)t)`. By reversibility the left side is the
Laplace transform of a positive spectral measure. Any mass strictly below
`1-q_*` would contradict that decay as `t` increases. Thus the heat-bath
gap is at least `1-q_*`, equivalently

```text
Var(f) <= (1-q_*)^(-1) sum_i E[Var_i(f)].               (C11)
```

Bounded functions are dense in `L2`; extend the form inequality there.
Insert the one-link gradient bounds. For a conditional block restrict
`B` and `s` to its coordinates: deleting nonnegative terms preserves
(C9), and the original all-exterior bounds still apply. Finally apply the
accepted gauge/forest identity and form factor `1/2`, proving (C10).

No graph-uniform weight ratio is needed in this spectral argument:
the norm-comparison prefactor is used at fixed graph before the spectral
decay rate is identified. A uniform norm-contraction statement in an
unweighted norm would require a separate uniform comparison of weights.

The ordinary row-sum criterion is `s_i=1`. A weighted criterion may work
when a few large row sums conceal an asymmetric or inhomogeneous influence
pattern. For an exact finite matrix illustration, take

```text
B = [[0,3/5,3/5],[3/5,0,0],[3/5,0,0]],
s = (3/2,1,1),                     q=9/10.
```

Its maximum row sum is `6/5`, but `Bs=(6/5,9/10,9/10)<=q s`.
This illustrates a stronger comparison criterion; it is not an asserted
influence matrix for the unknown YM vacuum. The criterion cannot hide a
genuinely large spectral radius. For example,
if `B_ij>=c>0` for all distinct coordinates of an `n`-site subset, then
`rho(B)>=(n-1)c`; no weights satisfy (C9) when that lower bound is at least
one. Thus this improvement is concrete and testable, not a way to remove
the collective hypothesis.

Using the accepted plaquette reference and unweighted split bounds gives
back precisely

```text
gap_phys(A) >= [d/(d-1)](3/2)(1-mr-b_v/4)
                            exp(-2mr/3-d_v),           (C12)
```

provided `d_v` is uniformly bounded and `mr+b_v/4` has a uniform strict
margin below one. Here `d` in `d/(d-1)` is spatial dimension, while
`d_v=d(2v)` is an oscillation budget. The chain certificate tells us how
to transport and audit these quantities; it has not supplied their
missing actual-vacuum estimate.

## 6. Exact hostile loop with arbitrarily small valid steps

First, a four-state calculation isolates the failure. This auxiliary
carrier is `{(-1,-1),(-1,+1),(+1,-1),(+1,+1)}` with uniform reference
measure. It is declared separately from the SU(2) carrier. For `a>=0`,
let

```text
p_a(x,y) = exp(a x y)/cosh(a),
phi_a = sqrt(p_a).
```

Here `p_a` is a density relative to the uniform four-state measure.
The heat-bath generator refreshes each coordinate at rate one. Its
conditional means are `E[x|y]=y tanh(a)` and
`E[y|x]=x tanh(a)`. Therefore

```text
G(x+y)=-(1-tanh(a))(x+y),
G(x-y)=-(1+tanh(a))(x-y),
G(xy-tanh(a))=-2(xy-tanh(a)).                           (C13)
```

Together with the constant eigenfunction these span all four states.
The exact gap is `1-tanh(a)`.

Take the reference loop
`0,epsilon,2epsilon,...,M epsilon,(M-1)epsilon,...,0`.
Every normalized transition is exact and their product is `I`. At every
step

```text
d(2h_k)=2epsilon,      b(2h_k)=4epsilon.
```

These can be made arbitrarily small. At the midpoint the diffusion gap
is exactly `1-tanh(M epsilon)`, which tends to zero as `M` increases.
The final cocycle is closed; the worst intermediate collective budget
was not controlled. For an entirely rational finite instance use
`a=log(2)`: equal-sign states each have probability `2/5`, opposite-sign
states each have probability `1/10`, `tanh(a)=3/5`, and the gap is `2/5`.
At the midpoint `a=log(4)`, the gap is `2/17`. These are exact algebraic
values, not simulation estimates.

The accepted SU(2) mixture gives a stronger graph-volume witness, with
even the endpoint one-link density ratios uniformly bounded. Reuse the
`N` edge-disjoint squares joined by tree paths from
[VACUUM_ATLAS.md, section 8](accepted/handoff/VACUUM_ATLAS.md).
For `0<=s<=t`, set

```text
ell_(s,N) = log cosh(s S_N)-N log z(s),
phi_(s,N) = exp(ell_(s,N)/2).
```

The accepted endpoint identities give

```text
d(ell_(t,N)) <= 2t,
b(ell_(t,N)) >= 8(N-1) log cosh(2t),
gap_phys(K_(t,N)) <= 2/[N m(t)^2].                     (C14)
```

This family also admits uniformly small **mixed-budget increments**.
Indeed

```text
partial_s ell_(s,N) = S_N tanh(s S_N)-N m(s).
```

The derivative of `u tanh(su)` in `u` has absolute value at most two:
`|tanh(su)|<=1` and `|su| sech^2(su)<=1`. One link changes `S_N` by
at most two. The normalization term is constant in configuration, so

```text
d(ell_(s+Delta,N)-ell_(s,N)) <= 4 Delta,
b(ell_(s+Delta,N)-ell_(s,N)) <= 8(4N-1) Delta.         (C15)
```

For the second bound each mixed oscillation is at most twice the
one-link oscillation, and only the `4N` square links can contribute.
Choose a uniform partition into `L` intervals with
`L>=8(4N-1)t/epsilon`. Every step then has both budgets at most
`epsilon`. Reverse that partition to make an exact closed loop. At its
midpoint (C14) still forces the auxiliary diffusion gap to zero with
volume. Every step is legal, arbitrarily small in both declared
seminorms, and exactly reversible; the total collective budget remains
uncontrolled. This extends the accepted separating witness by a written
small-step chain construction, without replaying its old checker.

There is no contradiction with (C3). The operators in (C13)-(C14) are
reference diffusions whose measures change along the path. If one fixes
one `A` and transports its full `K_k+R_k`, its spectrum is invariant
along that chart chain. The mixture is not asserted to be the actual
vacuum of the retained local plaquette Hamiltonian. It refutes a generic
inference from locally valid handoffs and closed cocycles to a uniform
diffusion gap; it does not refute the accepted YM gap.

## 7. What a committed handoff would have to retain

A mathematical handoff can retain the preceding normalized reference,
the exact transition, the proposed next correction, the full residual
operator, the defect in (C4), and a certificate covering its admitted
exteriors and prefixes. The next state is accepted only when these
relations are mutually compatible and its required quantitative bound
is independently established. An atomic commit can keep this tuple
consistent; it does not prove the mathematical bound recorded in it.

The past record and prepared continuation thus supply a useful operational
organization: each candidate is checked through its relations to retained
inputs and permitted successors. No object self-certifies by its name,
normalization, hash, or cocycle alone. A closed loop checks a particular
transport relation; (C5), (C9), or a stronger replacement must still
control the analytic receiver. This organization carries no security,
causality, or physical-time theorem.

**Evidence and endpoint.** C1-C4 and the hostile chains are written
derivations on their stated carriers, using the accepted finite-volume
YM and conditional-update ingredients where explicitly identified.
C13 is a complete four-state spectral calculation. A new in-memory
Python `Fraction` check passed 38 exact assertions: 32 eigenvector
component identities for `a=log(2),log(4)`, their two gap values, the
three weighted star inequalities, and its maximum row sum. That bounded
check corroborates the displayed arithmetic; it proves no general
analytic hypothesis and wrote no separate checker in this lane.
No formal proof,
old verifier rerun, coupling-window enlargement, infinite-volume
construction, or continuum mass-gap proof is claimed. The new useful
port is precise: derive a volume-uniform local-response comparison or
bounded signed error primitive for the **actual** correction, then
evaluate the resulting actual mixed conditional influence with its
strict margin. Exact chart compatibility supplies the transport that
makes such an estimate reusable; it does not supply that estimate.
