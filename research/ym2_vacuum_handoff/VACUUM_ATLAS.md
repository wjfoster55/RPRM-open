# Positive vacuum charts and the estimate needed for a handoff

12 September 2026. Written mathematical continuation on the accepted finite
lattice carrier. This note reuses the accepted results without rerunning
their verifiers. The chart identities, conditional implication, and hostile
cases below are written derivations, not formal proofs or numerical evidence.

Changing to a useful positive reference is an exact operation. It can expose
a better estimate even when an earlier construction runs out of room. The
operation alone does not supply that estimate: its complete transported
operator includes the reference's energy residual. This note identifies a
local conditional estimate that would make a new chart useful for the
physical gap without requiring the earlier bound on the total log vacuum.

## 1. Carrier, ports, and retained receiver

The carrier is each finite open nearest-neighbor subgraph of `Z^d`, `d=2,3`,
with configuration manifold `M_G=SU(2)^E`, normalized product Haar measure
`mu`, the accepted unit-round link metrics, and no spin cutoff. Gauge
transformations act at every vertex. There are no external charges or
periodic identifications. Function equality is almost everywhere; smooth
positive representatives are used for the displayed differential identities.

Keep the dimensionless physical Hamiltonian

```text
H_r = T+r V,          T=-(1/2) sum_e Delta_e,
V = sum_p(1-a_p),     a_p=(1/2)Tr(U_boundary(p)).       (VA1)
```

Multiplication by `E_el>0` restores physical energy units. Its actual positive
normalized vacuum is `psi_r`, with energy `E_r` and measure
`dnu_r=psi_r^2 dmu`. Finite-volume existence, smoothness, uniqueness, gauge
invariance, and the actual-vacuum form identity are accepted dependencies.

Supplied ports are the graph, Hamiltonian, and one or more smooth strictly
positive gauge-invariant reference functions. A reference need not solve
the vacuum equation. The missing quantitative port is an all-graph estimate
for the actual vacuum relative to a selected reference. The receiver retains
the full physical Hilbert norm, Hamiltonian form, and spectral gap, together
with the conditional laws needed for the forest-complement argument.

The chart operations below are invertible at every fixed graph. Their
inverse fibers are **ONE** once normalization is fixed. A volume-uniform
estimate, or an enlarged coupling interval, does not follow from that
fixed-graph invertibility. Those quantitative ports are **OPEN** here.

Dependencies are [the accepted overlap result](accepted/overlap/RESULT.md),
[the normalized inverse analysis](accepted/overlap/OVERLAP_INVERSE.md),
and the accepted conditional argument linked in section 5. Here “atlas” means
an ordinary family of compatible positive-function charts; it does not assert
the separate eight-Board abduction construction from RPRM math-lenses.

## 2. Two actual positive vacua of one Hamiltonian give the same chart

Suppose `phi_a,phi_b` are strictly positive normalized eigenfunctions of the
same `H_r`, with eigenvalues `E_a,E_b`. Self-adjointness gives

```text
(E_a-E_b) <phi_b,phi_a> = 0.
```

The overlap is positive, so `E_a=E_b`. Applying the ground-state form identity
based at `phi_a` to `phi_b=phi_a q` gives

```text
0 = (1/2) integral |grad q|^2 phi_a^2 dmu.
```

The product manifold is connected, hence `q` is constant. Positivity and unit
norm give `q=1`. Equivalently one may invoke the accepted uniqueness theorem.
Thus there are no distinct normalized strictly positive ground states of this
same finite Hamiltonian to choose between. A useful new chart must mean a
different positive reference, a different construction of the same vacuum,
or a reference at a different Hamiltonian parameter. Those are distinct
operations with the explicit transitions below.

## 3. Exact transitions for arbitrary positive references

Normalize each reference by `mu(phi_a^2)=1`. Put

```text
u_a = log phi_a,                dnu_a = phi_a^2 dmu,
h_ba = log(phi_b/phi_a),         dnu_b/dnu_a = exp(2h_ba),
U_a f = phi_a f,                J_ba = U_b^-1 U_a,
J_ba f = exp(-h_ba) f.                                   (VA2)
```

`U_a:L2(nu_a)->L2(mu)` and `J_ba:L2(nu_a)->L2(nu_b)` are unitaries. They
also preserve the physical gauge-invariant subspaces. On triple overlaps,

```text
h_ca = h_cb+h_ba,
J_ca = J_cb J_ba,      J_ab=J_ba^-1,      J_aa=I.        (VA3)
```

For initially unnormalized references `exp(w_a)`, write
`Z_a=mu(exp(2w_a))` and `phi_a=exp(w_a)/sqrt(Z_a)`. Then
`h_ba=w_b-w_a+(1/2)log(Z_a/Z_b)`. The normalization term is required in the
unitary multiplier; it disappears from oscillations and gradients.

For fixed `r`, define the reference diffusion and residual potential

```text
P_a = T-grad u_a dot grad,
W_a(r) = (H_r phi_a)/phi_a
       = rV+T u_a-(1/2)|grad u_a|^2,
R_a(r) = U_a^-1 H_r U_a = P_a+W_a(r).                   (VA4)
```

`P_a` is nonnegative and self-adjoint in `L2(nu_a)` with constants in its
kernel. It has the quadratic form `(1/2)integral|grad f|^2 dnu_a`. The full
transported Hamiltonian is `R_a`, with its specified residual multiplication
operator. Direct use of the product rule proves

```text
P_b = P_a-grad h_ba dot grad,
W_b-W_a = P_a h_ba-(1/2)|grad h_ba|^2,
R_b = J_ba R_a J_ab,
J_ba P_a J_ab = P_b+(W_b-W_a).                          (VA5)
```

These identities hold first on smooth functions and then for the operators
and closed forms by the smooth positive multiplication maps. At each fixed
compact graph their coefficients and reciprocal reference functions are
bounded. No volume-uniform bound on these ordinary multiplication maps is
being inferred. Dropping `W_b-W_a` in the last identity changes the operator.

For a physical state `F=phi_a f_a=phi_b f_b`, including complex states,

```text
f_b=J_ba f_a,
<F,H_r F> = (1/2) integral |grad f_a|^2 dnu_a
                         +integral W_a |f_a|^2 dnu_a.   (VA6)
```

The complete right-hand side is chart invariant. Its two separate terms need
not be. Constants in a reference chart represent the reference function;
they represent the actual vacuum only when that reference is the vacuum.

For references associated with different parameters, the extra Hamiltonian
change must also remain visible:

```text
R_b(r_b) = J_ba R_a(r_a) J_ab+(r_b-r_a)V.                (VA7)
```

In particular, if the references are the actual vacua at `r_a,r_b`, then

```text
P_a h_ba-(1/2)|grad h_ba|^2+(r_b-r_a)V = E_b-E_a.
```

The weighted diffusions at different couplings are not asserted to be
unitarily equivalent. A chart composition transports states exactly; a
coupling change adds the displayed physical interaction.

## 4. Coordinates of the same actual vacuum in every chart

At a fixed `r`, define `q_a=psi_r/phi_a>0`. Then

```text
nu_a(q_a^2)=1,         q_b=exp(-h_ba)q_a,
dnu_r=q_a^2 dnu_a=q_b^2 dnu_b,
(P_a+W_a)q_a=E_r q_a.                                 (VA8)
```

One may instead use a log coordinate `v_a`, modulo constants, by

```text
q_a = exp(v_a)/sqrt[nu_a(exp(2v_a))],
Q_mu v_b = Q_mu(v_a-h_ba),        Q_mu f=f-mu(f).        (VA9)
```

The transition is affine and has the exact inverse obtained by exchanging
`a,b`. The two occurrences of the actual vacuum in (VA8) are one shared
state. They are not independent compatible choices to be summed.

Writing `v=log q_a` with its fixed normalization, the exact missing equation
is

```text
P_a v-(1/2)|grad v|^2+W_a = E_r,
P_a v = -Q_nu_a W_a+(1/2)Q_nu_a |grad v|^2,
E_r = nu_a(W_a)-(1/2)nu_a(|grad v|^2).                  (VA10)
```

All displayed equations for gradients also hold for a constant-shifted `v`.
Solving this equation with uniform bounds is a substantive possible handoff.
Merely renaming its unknown does not solve it. In particular, the `L2`
Poisson inverse of `P_a` and its anchored Fourier inverse estimates are
different receiver requirements, as the accepted overlap-inverse hostile
case already demonstrates.

## 5. A sufficient all-volume conditional handoff theorem

This theorem uses the actual log correction `v=log(psi_r/phi_a)`; it does not
replace it by a formal or truncated series. Define the one-link oscillation
and mixed oscillation, for a real function `g`, by

```text
osc_i g = sup_(x_-i) [sup_(x_i)g(x)-inf_(x_i)g(x)],
D_ij(g) = sup_(x_-i,y_-i differing only at j)
          osc_(x_i)[g(x_i,x_-i)-g(x_i,y_-i)],   i!=j.
```

The outer supremum in `osc_i` includes every exterior. Constants are
irrelevant. Define `ell_a=log(dnu_a/dmu)=2u_a`. The following bounds suffice,
uniformly over the admitted graphs, parameter values, and selected charts:

1. Every reference one-link conditional law has gradient Poincare constant
   at most `c_*<infinity`, for every exterior.
2. `d_v := sup_i osc_i(2v)` has a finite common upper bound.
3. The direct mixed-log-density bound obeys

```text
q_* := sup_i sum_(j!=i)
       tanh([D_ij(ell_a)+D_ij(2v)]/4) < 1.             (VA11)
```

Here `q_*` denotes a proved common bound strictly below one, not just a
number below one on each separate finite graph. Under these hypotheses the
actual conditional measure on every block `B`, for every exterior `z`, obeys

```text
Var_(nu_r,B(.|z))(f)
 <= C_* integral sum_(i in B)|grad_i f|^2 dnu_r,B(.|z),
C_* = c_* exp(d_v)/(1-q_*).                            (VA12)
```

Consequently any accepted forest-complement cover with total weight `W`
and maximum link load `Lambda` gives

```text
gap_phys(H_r) >= W(1-q_*)/[2 Lambda c_* exp(d_v)].      (VA13)
```

The physical energy gap is `E_el` times this bound. For the direction cover,
`W/Lambda=d/(d-1)`.

**Proof.** At fixed exterior the exact conditional density ratio is

```text
dnu_r,i/dnu_a,i = exp(2v)/nu_a,i(exp(2v)).              (VA14)
```

Its maximum divided by its minimum is at most `exp(d_v)`. If this normalized
density lies between `m_i` and `M_i`, the variational characterization
`Var(f)=inf_c integral|f-c|^2` gives

```text
Var_(nu_r,i)(f)
 <= M_i c_* integral|grad_i f|^2 dnu_a,i
 <= (M_i/m_i)c_* integral|grad_i f|^2 dnu_r,i.
```

This uses one density-range factor, not its square. Changing exterior link
`j` changes the log of the actual conditional density by an `i`-dependent
term with oscillation at most `D_ij(ell_a)+D_ij(2v)`. Conditional normalizers
are constant in `i` and disappear. The accepted bounded-tilt inequality
therefore gives actual total-variation influence at most the summand in
(VA11). This is a direct estimate of actual log conditional densities. It
does not assume that influence coefficients add when a measure is tilted.

The accepted conditional heat-bath proof then gives approximate
tensorization of variance with constant `1/(1-q_*)`: its oscillation vector
evolves under `C^T-I`, where `C` is the actual influence matrix, and the
maximum row sum of `C` controls the induced column sum of `C^T`. Reversibility
and the spectral theorem yield the `L2` variance inequality. The full proof
is [CONDITIONAL_GAP_EXTENSION.md, sections 2-3](accepted/overlap/accepted/estimate/CONDITIONAL_GAP_EXTENSION.md).
For a conditional block the internal influences form a submatrix of this
same actual matrix and have no larger row bound. The one-link conditionals
are also these same laws with more exterior coordinates fixed. Thus the
same proof applies to every block, proving (VA12).

Gauge invariance and a forest exterior give the accepted exact identity
`E_nu_r[f|outside B]=nu_r(f)` for physical `f`. Integrate (VA12), sum the
weighted covers, and charge each edge at most `Lambda`. This gives
`W Var_nu_r(f)<=Lambda C_* integral|grad f|^2 dnu_r`. The actual-vacuum form
has the factor `1/2`, proving (VA13) on the full physical form domain.

This theorem supplies a different possible quantitative receiver from the
earlier small total Fourier norm. It is noncircular as a conditional
implication: proving its actual-correction bounds does not require assuming
the desired spectral gap. The bounds themselves remain an independent
obligation; asserting that an unknown vacuum has them would not close it.

## 6. Explicit target for the first plaquette reference

Set `S=sum_p a_p`, `m=2(d-1)`, and choose the explicit positive reference

```text
phi = exp(cS)/sqrt[mu(exp(2cS))],       c=r/6.
```

At most `m` retained elementary plaquettes contain a link. If `n_ij` is the
number containing both links, `sum_(j!=i)n_ij<=3m`. Since `a_p` lies in
`[-1,1]`, its one-link oscillation is at most `2` and its mixed oscillation
at most `4`. Hence

```text
osc_i(log dnu_phi/dmu) <= 4cm = 2mr/3,
D_ij(log dnu_phi/dmu) <= 8c n_ij,
c_* = exp(2mr/3)/3,
sup_i sum_(j!=i) D_ij(log dnu_phi/dmu)/4 <= mr.          (VA15)
```

The constant `1/3` is the accepted Haar gradient Poincare constant on the
unit-round `SU(2)=S^3`. These are direct local reference estimates and do
not impose a small anchored norm on the complete reference logarithm.

For the **actual** correction `v=log(psi_r/phi)`, put

```text
d_v = sup_i osc_i(2v),
b_v = sup_i sum_(j!=i) D_ij(2v).
```

Using `tanh t<=t`, the exact sufficient continuation target becomes

```text
d_v < infinity,              mr+b_v/4 < 1,

gap_phys(H_r)
 >= [d/(d-1)] (3/2) [1-mr-b_v/4]
                         exp[-2mr/3-d_v].             (VA16)
```

The two displayed correction bounds must hold uniformly in graph volume,
all exterior configurations, and the claimed coupling set. A uniform strict
margin in the second bound is needed for a positive uniform lower bound.
They could, if proved at a coupling larger than `9/(128m)`, add physical
gap scope beyond the earlier constructed window. This note does not prove
such a correction estimate or enlarge that window.

The target distinguishes three useful possibilities: a better estimate for
this explicit reference's correction, another independently controlled
reference chart, or a different collective conditional comparison that
replaces (VA11). Exact chart algebra permits all three. Reusing exactly the
old scalar inverse majorant after the chart change does not automatically
produce a stronger theorem.

## 7. What gluing costs, and what it does not control

For any block `B` and pair of references, the conditional version of (VA2) is

```text
dnu_b,B(.|z)/dnu_a,B(.|z)
 = exp(2h_ba)/nu_a,B(exp(2h_ba)|z).                    (VA17)
```

If `osc_B h_ba<=D` uniformly, comparison transfers the complete block
Poincare inequality at cost at most `exp(2D)`. Global comparison is the
special case `B=E`. If `h_ba` is a sum of uniformly bounded local terms, its
global oscillation can still grow proportionally to the number of terms.
Finiteness on each fixed graph then gives no uniform transfer constant.

The conditional route avoids comparing the entire density by requiring
single-link control together with a collective influence bound. Single-link
ratios alone cannot be multiplied together and declared uniform: section 8
provides a physical gauge-invariant control where they are uniformly bounded
but the associated diffusion gap vanishes with volume.

For a chain of charts, exact log ratios add by (VA3). Any bounds obtained
only by the triangle inequality also add: one-link oscillations and mixed
row sums can accumulate along the path. Exact cocycle compatibility alone
does not prevent that accumulation. To cover a new coupling set uniformly,
one must either supply a uniform finite set of independently certified
charts, or prove uniform control of the complete transition path. For each
parameter one may select any chart whose correction certificate holds; no
partition of unity or added localization energy is needed.

The target in section 5 gives a physical gap when its hypotheses hold. It
does not by itself give the anchored Fourier inverse needed by the earlier
nonlinear construction. Conversely, an anchored correction construction
can supply the conditional bounds, but would need its own uniform estimates.
Those two receivers must not be identified by the existence of the unitary
map (VA2).

## 8. Two exact all-volume controls

Take `N` edge-disjoint elementary squares connected by retained tree paths,
with no additional retained plaquettes. Such connected finite open lattice
subgraphs are admitted. Write their traces as `a_1,...,a_N`, and
`S_N=sum_k a_k`. The square variables are independent under product Haar;
tree links carry their usual Haar measure. Each trace has a symmetric,
nonconstant distribution, and the accepted metric identity is

```text
sum_(e in square k)|grad_e a_k|^2 = 4(1-a_k^2).          (VA18)
```

Fix `t>0` and define `z(t)=mu(exp(t a_1))` and
`m(t)=z'(t)/z(t)>0`. Positivity follows from symmetry and
`z'(t)=mu[a_1 sinh(t a_1)]>0`.

**Independent tilt: extensive global oscillation need not spoil the gap.**
The density `exp(tS_N)/z(t)^N` is a product over the disjoint four-link
squares, with independent Haar tree links. Its global log-density
oscillation is `2tN`. Each square factor has gradient Poincare constant at
most `exp(2t)/3` by comparison with the four-link Haar product. Ordinary
product variance tensorization therefore gives this same constant for
every `N`. Thus the elementary global density comparison deteriorates
exponentially even though a uniform conditional/block proof is available.

**Correlated mixture: bounded single-link ratios need not preserve a gap.**
Now choose the smooth positive gauge-invariant density

```text
p_N = cosh(tS_N)/z(t)^N
    = (1/2) product_k [exp(t a_k)/z(t)]
      +(1/2) product_k [exp(-t a_k)/z(t)],
phi_N = sqrt(p_N),       dnu_N=p_N dmu.                 (VA19)
```

It is exactly normalized. Changing one link changes only one `a_k` by at
most `2`. Because `log cosh` is `1`-Lipschitz,
`osc_i(log p_N)<=2t` for every `N` and every exterior. Thus every one-link
conditional density relative to Haar has maximum/minimum ratio at most
`exp(2t)`, and conditional gradient constant at most `exp(2t)/3`.

Nevertheless the gauge-invariant function `F_N=S_N/N` has mean zero and

```text
Var_nu_N(F_N) >= m(t)^2,
integral |grad F_N|^2 dnu_N <= 4/N.
```

The first inequality is the variance of the two conditional component means
`+m(t),-m(t)` in (VA19). The second follows directly from (VA18) and disjoint
edge supports. Therefore the weighted physical diffusion has

```text
gap_phys(P_phi_N) <= 2/[N m(t)^2] -> 0.                 (VA20)
```

The omitted collective control can be seen directly. For a link in one
square and a link in a different square, set every other square trace to
zero. Let the two relevant traces independently take the endpoint values
`+1,-1`. The resulting mixed log-density oscillation is at least
`2 log cosh(2t)>0`. There are four links in each of the other squares, so

```text
sup_i sum_(j!=i) D_ij(log p_N)
 >= 8(N-1) log cosh(2t).                                (VA21)
```

This is an exact smooth, full-gauge, all-spin control against a generic
single-link-density-only handoff theorem. The measure (VA19) is not asserted
to be the actual vacuum measure of the specific plaquette Hamiltonian
(VA1). Accordingly (VA20) is not a counterexample to its physical gap.
It proves why one cannot infer that gap from local density ratios alone.

## 9. Supported endpoint

The positive-reference transitions, their normalization, inverse,
composition, Hamiltonian residual, and actual-vacuum correction equation are
exactly determined at each admitted finite graph. The conditional handoff
theorem proves that uniform actual-correction bounds of the form (VA11), or
the explicit target (VA16), would carry the complete physical gap receiver.

What remains **OPEN** is a proof of those actual-correction bounds on a
coupling domain extending the accepted one, or another independent estimate
with the same all-volume physical consequence. The known gap, a new chart
name, or finite-volume uniqueness supplies none of this missing estimate.
No infinite-volume representation, continuum limit, or continuum mass gap
is established here. Only this note was written in this lane; no old verifier,
simulation, installation, publication, or repository-wide check was run.
