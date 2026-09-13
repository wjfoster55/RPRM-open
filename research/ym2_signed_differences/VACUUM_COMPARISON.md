# Explicit finite-graph vacuum comparison

12 September 2026. New written derivation on the accepted two-square source.
This closes a quantitative sufficient bound on its actual conditional-variance
constant. It does not determine the best constant, solve the vacuum
eigenfunction, or establish a uniform graph-family bound.

## Contract and result

Retain [GAP_BRIDGE.md](accepted_sources/ym2_global_phase_joint/GAP_BRIDGE.md):
`Q=SU(2)^7`, normalized product Haar probability `mu`, full gauge invariance
at all six vertices, generators `i sigma_k`, and

```text
kappa = alpha hbar^2/2 > 0,
H = -kappa sum_e Delta_e + V,
V = beta(2-a-b),    beta >= 0,    0 <= V <= 4 beta,
r = beta/(alpha hbar^2).
```

The self-adjoint domain is the accepted source Laplacian domain. Its unique
normalized positive ground state `psi_0` is smooth, gauge invariant and
strictly positive on the connected compact source. Write

```text
rho = psi_0^2,    dnu = rho dmu,
m_0 = min_Q rho > 0,    M_0 = max_Q rho,
R_actual = M_0/m_0,
R_bar(r) = exp(16r) (5/3)^14.                              (V1)
```

Retaining the joint vertex-gauge constraint in the heat kernel improves
this explicit bound to

```text
R_actual <= R_gauge(r),
R_gauge(r) = exp(32r/3) (104207/52043)^2 < R_bar(r).       (V1a)
```

Section 2a proves (V1a) by a complete analytic character-tail bound and
the graph's four possible nonempty supports without a leaf. Every
fixed-two-square comparison inequality below using `R_bar` also holds with
the smaller `R_gauge`. In particular, the strongest new comparison bound is

```text
gamma >= 6 alpha hbar^2 exp(-32r/3) (52043/104207)^2 > 0.  (V1b)
```

Supply the seven singleton patch occurrences `{e}`, each once. Their
sigma algebras, integrated conditional variances `v_e^nu`, and receiver
are exactly those of [NEXT_GLUE_LEMMA.md](accepted_sources/ym2_global_phase_joint/NEXT_GLUE_LEMMA.md).
The outside variables are the actual other six links; conditionals are
under the full joint vacuum `nu`.

For every finite admitted parameter choice,

```text
R_actual <= R_bar(r),
Var_nu(f) <= [R_bar(r)/4] sum_e v_e^nu(f)  for physical f,
v_e^nu(f) <= [R_bar(r)/3] integral sum_k |D_(e,k)f|^2 dnu,
patch overlap multiplicity = 1.                           (V2)
```

Thus one may supply `C_mix=R_bar/4`, `C_loc=R_bar/3`, `m=1`
to that sufficient lemma. It yields

```text
gamma >= 6 alpha hbar^2 / R_bar(r)^2 > 0.                  (V3)
```

Transferring the accepted physical Haar Poincare inequality directly gives
the stronger bound

```text
gamma >= 6 alpha hbar^2 / R_bar(r)
      = 6 alpha hbar^2 exp(-16r) (3/5)^14 > 0.             (V4)
```

The comparison also supplies `C_mix=R_bar` for arbitrary source functions.
The factor `1/4` in (V2) requires the physical function class and this
graph's gauge and shortest-cycle contract. These are sufficient constants;
no claim of optimality is made.

## 1. A complete heat-series bound at one time

Let `q_s(g)` be the Haar kernel of `exp(s Delta)` on one `SU(2)` factor.
With `n=2j+1`, the accepted all-spin Casimir is `n^2-1`, so Peter--Weyl
expansion gives

```text
q_s(g) = sum_(n>=1) n exp[-s(n^2-1)] chi_((n-1)/2)(g).
```

The Riemannian kernel and the equivalent Chebyshev expansion are recorded
in [Baudoin and Bonnefont, Section 3.2](https://arxiv.org/pdf/0802.3320).
Here `s` is dimensionless heat time in our stated Laplacian convention;
the subelliptic kernel in that paper is a different kernel.

Every representation is unitary, hence `|chi_((n-1)/2)(g)|<=n`.
At the single declared time `s=1`, the entire nonconstant tail obeys

```text
|q_1(g)-1| <= sum_(n>=2) n^2 exp[-(n^2-1)].                (V5)
```

For all integers `n>=2`,
`n^2-1-3(n-1)=(n-1)(n-2)>=0`. The positive Taylor series proves
`exp(3)>sum_(k=0)^8 3^k/k!>20`. Therefore the complete infinite tail is
bounded by a differentiated geometric series:

```text
sum_(n>=2) n^2 exp[-(n^2-1)]
 <= sum_(n>=2) n^2 (1/20)^(n-1)
  = (1+1/20)/(1-1/20)^3 - 1
  = 1541/6859 < 1/4.
```

No omitted spin is assigned zero weight: the infinite remainder is bounded
analytically. Absolute uniform convergence at this time justifies the
pointwise estimate and yields

```text
3/4 <= q_1(g) <= 5/4 for every g in SU(2).                (V6)
```

The heat kernel `K_t(x,y)` of `exp(t kappa sum_e Delta_e)` is the product
of seven copies of `q_(kappa t)`. At `t_*=1/kappa`,

```text
(3/4)^7 <= K_(t_*)(x,y) <= (5/4)^7,
sup_(x,y) K_(t_*)(x,y)/inf_(x,y) K_(t_*)(x,y) <= (5/3)^7.  (V7)
```

The auxiliary semigroup time `t_*` has inverse-energy units. It is not
the real Schrödinger time, and no extra factor of `hbar` belongs in
`exp(-t_* H)`.

## 2. Ground-state oscillation with the energy canceled

For a nonnegative function `u` and `P_t=exp(t kappa sum_e Delta_e)`,
the bounded-potential Feynman--Kac formula gives

```text
exp(-t max V) P_t u <= exp(-tH)u <= exp(-t min V) P_t u.
```

This is the scalar compact-manifold specialization of the standard formula
described in [Boldt and Güneysu, introduction and Theorem 2.2](https://arxiv.org/pdf/2012.15551).
In this bounded case it also follows by applying these order bounds to
each positive heat/multiplication factor in the Trotter product and
passing to the semigroup limit.

Apply the inequality to `u=psi_0`. Since
`exp(-tH)psi_0=exp(-tE_0)psi_0`, for every `x,y` at `t=t_*`,

```text
psi_0(x)/psi_0(y)
 <= exp[t_*(max V-min V)]
    [sup K_(t_*) integral psi_0 dmu]
    /[inf K_(t_*) integral psi_0 dmu]
 <= exp(4 beta/kappa) (5/3)^7
  = exp(8r) (5/3)^7.                                     (V8)
```

Both the common eigenvalue factor and the positive common integral cancel.
Squaring (V8) proves (V1). This bounds the quantum vacuum density itself;
it never identifies that density with a classical Gibbs law `exp(-V)`.

## 2a. Refine the bound by joint gauge averaging

The preceding product estimate bounded seven independent heat factors
before using gauge invariance. The same source heat semigroup admits a
sharper bound on its physical function class. For dimensionless `s>0`,
define

```text
d_s = sum_(n>=2) n^2 exp[-s(n^2-1)],
K_phys,s(x,y) = integral_(g in SU(2)^6) K_(s/kappa)(g.x,y) dg,
```

with normalized product Haar measure on the vertex gauges. This kernel
is nonnegative and integrates to one in `y`, because it averages genuine
source heat kernels. If `u` is gauge invariant, commutation of gauge
transformations with the heat semigroup gives

```text
P_(s/kappa)u(x) = integral K_phys,s(x,y)u(y) dmu(y).       (V8a)
```

Subtract the uniform Haar kernel as a signed difference:

```text
h_s(z) = q_s(z)-1,    integral h_s(z) dmu_SU2(z) = 0,
|h_s(z)| <= d_s.
```

The integral identity is heat-kernel normalization. On edge `e=(v,w)`,
the gauge-transformed heat factor is
`1+h_s(g_v x_e g_w^(-1) y_e^(-1))`, with the fixed edge orientation.
Expand the product of these seven factors into its `2^7` finite support
terms. For a support `S`, the active factors are precisely its `h_s`
occurrences; all remaining factors are one. If `S` has a degree-one
vertex, only its one incident active factor depends on that vertex
gauge. Haar invariance and `integral h_s=0` make that integral vanish.
This includes either endpoint orientation because Haar inversion and
left/right translations preserve normalized Haar measure.

Each surviving support term has absolute gauge average at most
`d_s^|S|`. Thus subtracting the uniform reference, retaining the actual
edge residuals, and joining them through the full vertex-gauge integral
leaves only supports without a leaf. This is a finite product expansion;
it makes no claim that physical eigenbasis functions are uniformly
bounded by one and requires no exchange of a multi-spin series with
the gauge integral. The single-factor character expansion is used only
to bound `|h_s|` by its complete tail `d_s`.

Here the undirected graph consists of three paths between `B` and `E`:
the length-three path through `a,l,c`, the central edge `s`, and the
length-three path through `b,r,d`. Each internal path vertex has degree
two. A support without a leaf must include an entire path if it includes
any of that path's edges, and it must include at least two paths to avoid
a leaf at `B` or `E`. Its four nonempty possibilities therefore have
sizes `4,4,6,7`: the left square, right square, outer cycle, and all seven
edges. This is the accepted support list in
[RESULTS_QUANTUM.json](accepted_sources/ym2_global_phase_joint/RESULTS_QUANTUM.json),
with its coverage explained directly here; the old checker is not rerun.
Passing this necessary support condition need not give a nonzero term.
Retaining all four supports is valid for an upper bound.

The empty support contributes precisely one, and the triangle inequality
after gauge integration yields

```text
|K_phys,s(x,y)-1| <= eta(d_s),
eta(d) = 2 d^4 + d^6 + d^7.                              (V8b)
```

To obtain a fixed explicit constant, choose `s=2/3`. Finite positive
Taylor sums through degree 16 prove

```text
exp(2) > 73/10,
exp(16/3) > 200,
exp(14/3) > 100.
```

The first tail term, at `n=2`, is less than `40/73`. The term at `n=3`
is less than `9/200`. For `n>=3`, the ratio of successive positive
terms `a_n=n^2 exp[-(2/3)(n^2-1)]` satisfies

```text
a_(n+1)/a_n
 = [(n+1)/n]^2 exp[-(2/3)(2n+1)]
 <= (16/9) exp(-14/3) < 4/225.
```

Thus the full infinite remainder, with no spin cutoff, satisfies

```text
d_(2/3) < 40/73 + (9/200)/(1-4/225) < 3/5.
```

This proves the finite value and complete coverage of the character-tail
majorant used for each residual. The support expansion itself is finite.
Since `eta` increases for nonnegative arguments,

```text
eta(d_(2/3)) < eta(3/5) = 26082/78125 < 1,
1-26082/78125 <= K_phys,2/3(x,y) <= 1+26082/78125,
sup K_phys,2/3 / inf K_phys,2/3 <= 104207/52043.          (V8c)
```

Use (V8a) with the actual invariant `psi_0` in the bounded-potential
semigroup comparison of Section 2. The positive common integral and
ground-energy factors cancel exactly as before. At
`t=s/kappa=4/(3 alpha hbar^2)`, this gives

```text
max psi_0/min psi_0
 <= exp[t osc(V)] (104207/52043)
 <= exp(16r/3) (104207/52043).
```

Squaring proves (V1a). Its rational prefactor is smaller than the coarse
one and its exponential coefficient is `32/3<16`, so it improves (V1)
for every `r>=0`. It keeps the actual link occurrences and joint Gauss
constraints; it does not replace the vacuum by a product of loop states.

## 3. Transfer the conditional-variance constant

For a probability `eta`, write

```text
Var_eta(f) = inf_(c in C) integral |f-c|^2 deta,
v_e^eta(f) = inf_(g measurable outside e) integral |f-g|^2 deta.
```

These are orthogonal-projection variational formulas. The spaces of
admissible square-integrable functions for `mu` and `nu` coincide because
`m_0<=rho<=M_0`. Consequently

```text
Var_nu(f) <= M_0 Var_mu(f),
v_e^mu(f) <= (1/m_0) v_e^nu(f).                           (V9)
```

To retain the physical improvement, let `P_e^mu` integrate out edge `e`
against Haar and let `A_mu=sum_e(I-P_e^mu)`. The projections commute,
preserve the invariant subspace, and satisfy

```text
sum_e v_e^mu(f) = <f,A_mu f>_mu.
```

On each product Peter--Weyl component, `I-P_e^mu` is zero if `j_e=0`
and the identity if `j_e>0`. Thus `A_mu` has eigenvalue equal to the
number of nontrivially labeled edge occurrences. Full gauge invariance
requires a singlet at each vertex. As proved at all spins in the accepted
gap bridge, a nonempty support cannot have a degree-one vertex; it
contains a cycle, and every cycle here has at least four edges. Every
nonconstant physical component therefore has `A_mu` eigenvalue at least
four. Peter--Weyl completeness gives

```text
Var_mu(f) <= (1/4) sum_e v_e^mu(f) for physical f.         (V10)
```

Combining (V9)--(V10) proves
`Var_nu(f)<=(R_actual/4) sum_e v_e^nu(f)`, then (V2).
On the unrestricted source the same diagonal argument uses the minimum
nonempty support size one and yields the stated `R_actual` comparison.
No independence is assumed under `nu`, and the optimizing conditional
means under `mu` and `nu` are not equated.

For `beta=0`, the accepted constant ground state gives `R_actual=1`.
Then `C_mix=1/4` is sharp on physical functions: the left plaquette half
trace has nonzero support on exactly its four edges and attains (V10).
The convenient upper bound `R_bar(0)>1` is deliberately loose and need
not replace this known exact value.

## 4. Local and direct spectral transfer

Fix the six outside links. The conditional vacuum density with respect
to Haar on the remaining edge is
`rho(link,outside)/integral rho(link,outside) dmu_edge`.
Its maximum-to-minimum ratio is at most `R_actual` because the
normalizing denominator cancels. One-edge Haar Poincare has constant
`1/3` in the accepted metric. The same variational comparison as (V9),
followed by this Haar inequality and the reverse density bound on the
Dirichlet integral, gives conditional Poincare constant
`R_actual/3`. Integrating in the actual exterior marginal proves the
local inequality in (V2).

For the stronger direct route, the accepted physical Haar inequality is
`Var_mu(f)<=(1/12) integral sum_(e,k)|D_(e,k)f|^2 dmu`.
It and (V9) give

```text
Var_nu(f)
 <= (M_0/12) integral sum_(e,k)|D_(e,k)f|^2 dmu
 <= (R_actual/12) integral sum_(e,k)|D_(e,k)f|^2 dnu.
```

The source ground-state transform then proves (V4). Smooth positive
`psi_0` and its reciprocal are bounded with bounded derivatives on this
compact source. Multiplication and division by `psi_0` preserve the
inherited `H^1` form domain and physical subspace. Thus these inequalities
extend from smooth invariant functions by form closure and concern the
original physical spectrum, including the inherited singular-quotient
boundary domain. They do not select a new boundary condition.

## 5. Coverage and hostile limits

For this fixed graph the estimate is positive at every finite
`r>=0`, including beyond the accepted variational estimate's `r<3`
positivity region. It may be extremely small. Combining existing and new
valid lower bounds is allowed, for example

```text
gamma >= alpha hbar^2 max{6-2r,
                         6 exp(-32r/3)(52043/104207)^2}.
```

Its positive second term is an actual fixed-source bound, not evidence
of a useful uniform continuum bound. For a finite open square-lattice
graph with `N_e` links, `N_p` plaquettes, shortest cycle four and the
same coefficients, this particular derivation replaces `R_bar` by

```text
R_bar,G = exp(8 r N_p) (5/3)^(2 N_e).                     (V11)
```

The resulting coarse direct lower bound `6 alpha hbar^2/R_bar,G` tends to
zero as the volume grows at fixed positive coefficients. This proves
failure of uniform positivity for this bound, not vanishing of the
actual gap. At fixed graph, `r` tending to infinity also drives its
normalized lower bound to zero. Physical-unit rescaling must still be
carried through the full ratio. The exact `beta=0` solution is a
distinguishing control: there `R_actual=1` at every graph size and the
true free physical gap remains `6 alpha hbar^2` under this girth contract,
even though (V11)'s crude heat comparison deteriorates with `N_e`.
The refined support polynomial `2d^4+d^6+d^7` is specific to the fixed
two-square graph; a larger graph has additional support occurrences and
requires its own count and bound. Neither its small polynomial nor the
fixed numerical ratio in (V8c) has been supplied for a growing family.

The unresolved family obligation is a bound on the actual family
vacuum conditionals or a different global Poincare argument whose full
physical-energy ratio stays uniformly positive. Continuum construction
and the preservation of the required quantum observables also remain
OPEN. No exact interacting eigenfunction or complete spectral fiber is
returned by a sufficient inequality.

## Evidence and replay boundary

The analytic evidence is the written derivation above, using the accepted
all-spin invariant support argument, compact-source ground state and
form domain, standard heat-kernel spectral expansion, and bounded-potential
semigroup comparison. It is not a proof-assistant certificate.

[check_vacuum_comparison.py](check_vacuum_comparison.py) uses only Python
standard-library exact rationals to recompute the finite Taylor lower
bound, generating-function value, rational interval, and constants in
the seven-factor estimate. It also checks the three refined Taylor
lower bounds, the complete-tail geometric-majorant value, and the
evaluation of the accepted support polynomial at `3/5`. The receipt is
[RESULTS_VACUUM_COMPARISON.json](RESULTS_VACUUM_COMPARISON.json).
The infinite-tail coverage is the general inequality and geometric-series
identity written above; the finite checker does not itself prove
Peter--Weyl completeness, Feynman--Kac, operator-domain statements, or
the general soundness of this argument.

```powershell
python -I -B research/ym2_signed_differences/check_vacuum_comparison.py
python -I -O -B research/ym2_signed_differences/check_vacuum_comparison.py
```

Default mode recomputes and compares the saved receipt without writing;
`--write-results` explicitly creates or replaces only that adjacent receipt.
No accepted-source checks are rerun, no spin cutoff is used as a theorem,
and no numerical eigenvalue or simulation is supplied.
