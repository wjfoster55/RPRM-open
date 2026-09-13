# An all-state gap from the actual conditional laws

12 September 2026. A new written proof using the actual log vacuum from
the Fourier construction. It supplies the spectral implication that
[CONDITIONAL_REFINEMENT.md](accepted/CONDITIONAL_REFINEMENT.md)
explicitly left separate from its conditional estimates. The old packet
and its tests are unchanged.

## 1. Result and precise dependency ports

Keep the finite open square/cubic graph, full `SU(2)` link variables,
product Haar measure `mu`, unit-round-`S^3` metric, operator
`A(r)=T-rS`, `T=-Delta/2`, and anchored energy norm `||.||_*` of the
accepted [direct proof](accepted/DIRECT_COVER_ATTEMPT.md).
Let `N=|E_G|>=1`. Suppose the supplied actual log vacuum is smooth and
satisfies

```text
psi_hat = exp(u)/||exp(u)||_2,
A(r)psi_hat = E psi_hat,
dnu = psi_hat^2 dmu,
||u||_* <= Y < 3/4.                                      (CG1)
```

Then the complete, untruncated excited-state form has the bound

```text
gap(A(r)) >= (3/2)(1-4Y/3) exp(-8Y/3).                   (CG2)
```

This implication only requires the vacuum and norm ports in (CG1).
It does not require `Y<1/2`, which was needed for a positive lower bound
from the earlier curvature estimate. No assumed heat-bath theorem is
hidden in (CG2): sections 2--5 prove the needed implication on this
continuous compact product space.

For the improved source and bilinear inputs of this continuation,

```text
||T^-1 S||_* <= 4m,
||B(f,g)||_* <= (16/9)||f||_* ||g||_*,
m=2(d-1),
```

the inherited fixed-point construction supplies

```text
Y(r) = (9/16)[1-sqrt(1-128mr/9)],
||u||_* <= Y(r),          0<=r<r_*:=9/(128m).             (CG3)
```

The bilinear input is proved in
[SIGNED_AND_CONTRACTED_AUDIT.md](SIGNED_AND_CONTRACTED_AUDIT.md), and
the source input in
[SOURCE_NORM_REFINEMENT.md](SOURCE_NORM_REFINEMENT.md).
Equation (CG2) itself is independent of those construction inputs.
With both supplied, (CG2) and fixed-graph spectral continuity give

```text
0<=r<=9/(128m)
  ==> gap(A(r)) >= (3/8)exp(-3/2) > 0.                   (CG4)
```

This is a bound for every admitted finite graph with one common
constant, at the stated lattice energy scale. The interior retains
the stronger `Y(r)`-dependent expression in (CG2).

The missing port addressed here is a lower bound for all functions
orthogonal to the actual vacuum. It is not an enumeration of the
interacting eigenfunctions. All conditional kernels use the actual
measure `nu`, with smooth positive conditional densities defined at
every exterior configuration. Equality of spectral vectors is
`nu`-almost everywhere, while pointwise oscillation estimates below
use continuous representatives on the compact configuration space.

## 2. Conditional influence and the oscillation matrix

For a link `i`, let `nu_i(.|x_-i)` be its actual conditional law and
let `P_i f` be integration against this law with all other links held
fixed. On `L^2(nu)`, `P_i` is the orthogonal conditional-expectation
projection. Set, for `i!=j`,

```text
c_ij = sup_(x,y differing only at j)
       TV(nu_i(.|x_-i),nu_i(.|y_-i)),
c_ii = 0,
C = (c_ij),       q = max_i sum_j c_ij.
```

`TV` is the probability convention `sup_A |p(A)-q(A)|`, equivalently
one half of the `L^1` difference of densities. The accepted support
calculation (CR10)--(CR12), applied to the full `u`, gives

```text
c_ij <= 2 sum_(J:i,j in supp J) ||u_J||_A,
q <= (4/3)||u||_* <= 4Y/3 < 1.                           (CG5)
```

Only its final substitution of an older radius restricted (CR12) to
`Y<=1/4`. The displayed support estimate uses absolute convergence,
`lambda_J>=(3/2)|supp J|`, and
`TV<=tanh(osc(log tilt)/4)<=osc(log tilt)/4`. These steps remain valid
for any finite `||u||_*`; thus (CG5) uses that same proved estimate at
the larger supplied radius without importing the old radius restriction.

For a self-contained reminder of the retained tilt inequality, let the
new law have density R relative to the old law, with a<=R<=b,
E[R]=1, and b/a=exp(D). The chord bound for |R-1| gives
TV<=((1-a)(b-1))/(b-a). Maximizing over a with b=exp(D)a gives
TV<=(exp(D/2)-1)/(exp(D/2)+1)=tanh(D/4); D=0 gives zero directly.
This recalls the accepted bounded-tilt lemma, not a newly claimed result.

For real continuous `f`, define the one-link oscillations by

```text
delta_j(f) = sup_(x,y differing only at j) |f(x)-f(y)|.
```

They are finite. Replacing the coordinates one at a time gives
`osc(f)<=sum_j delta_j(f)`. Integration at site `i` removes all
dependence on that site's input, so `delta_i(P_i f)=0`. For `j!=i`,
add and subtract the integral of the same integrand under the other
conditional law. Changing the integrand costs at most `delta_j(f)`;
changing its law costs at most `c_ij delta_i(f)`. Thus

```text
delta_j(P_i f) <= delta_j(f)+c_ij delta_i(f),   j!=i.     (CG6)
```

The coefficient is `c_ij`, not `c_ji`: it measures how outside site
`j` changes the update of site `i`. This fixes the transpose needed
in the next calculation.

## 3. Continuous-time heat bath and its complete spectral gap

Define the auxiliary bounded generator and semigroup on `L^2(nu)` by

```text
L_hb = sum_i(P_i-I),
H_hb = -L_hb = sum_i(I-P_i),
T_t = exp(tL_hb).
```

Each site updates at rate one. Since the `P_i` are orthogonal
projections, `H_hb` is bounded, self-adjoint and nonnegative. Constants
are fixed and `nu` is invariant. The operators preserve continuous
functions: the conditional densities are smooth positive functions
on a compact product.

Let `P=N^-1 sum_i P_i`. Regarding `delta(f)` as a column vector,
averaging (CG6) and the zero diagonal update yields

```text
delta(Pf) <= M delta(f),
M = (1-1/N)I+C^T/N.                                     (CG7)
```

All entries of `M` are nonnegative. Iteration, subadditivity of
oscillations, and the uniformly convergent Poisson expansion

```text
T_t = exp[-Nt] sum_(k>=0) (Nt)^k P^k/k!
```

give componentwise

```text
delta(T_t f) <= exp[t(C^T-I)] delta(f).
```

The maximum column sum of `C^T` is the maximum row sum `q` of `C`.
Consequently its induced `l^1` norm is at most `q`, and its nonnegative
matrix exponential satisfies

```text
sum_j delta_j(T_t f)
 <= exp[-(1-q)t] sum_j delta_j(f).                       (CG8)
```

If `nu(f)=0`, then `nu(T_t f)=0`, so

```text
||T_t f||_2 <= ||T_t f||_infinity
 <= osc(T_t f)
 <= D_f exp[-(1-q)t],
D_f = sum_j delta_j(f) < infinity.                       (CG9)
```

The prefactor `D_f` can depend on the number of links. This does not
weaken the spectral exponent. To check that assertion explicitly, let
`sigma_f` be the spectral measure of `H_hb` for such an `f`. The
self-adjoint spectral theorem gives

```text
||T_t f||_2^2 = integral exp(-2st) d sigma_f(s).
```

If `sigma_f([0,a])>0` for any `a<1-q`, its right side is at least
`exp(-2at) sigma_f([0,a])`, contradicting (CG9) as `t` tends to
infinity. Taking a countable increasing sequence of such `a` shows
that the spectral projection of `f` onto `[0,1-q)` is zero.

Centered real continuous functions are dense in the real centered
`L^2(nu)` space on this compact manifold. A spectral projection is
bounded, so the same zero projection holds for every centered `L^2`
function. Complex functions follow by real and imaginary parts.
This proves, with no discrete-state or compact-resolvent assumption
for the heat bath,

```text
Var_nu(f) <= [1/(1-q)] <f,H_hb f>
          = [1/(1-q)] sum_i nu[Var_(nu_i)(f)].            (CG10)
```

The equality follows from conditional expectation:
`<f,(I-P_i)f>=||f-P_i f||_2^2=nu[Var_(nu_i)(f)]`.
Equation (CG10) covers every `L^2` state and rules out additional
zero modes on the centered subspace. The argument uses finite `N`
throughout, but the resulting constant depends only on `q`.

## 4. Single-link conditional gradient comparison

Fix an exterior configuration at link `i`. Fourier terms whose
support omits `i` are constant under changes of `U_i`. Since
`|u_J|<=||u_J||_A`, the oscillation of the conditional log density is
bounded by

```text
D_i := osc_(U_i) log[dnu_i/dmu_i]
     = osc_(U_i) [2u(U_i,x_-i)]
    <= 4 sum_(J:i in supp J) ||u_J||_A
    <= (8/3)||u||_*
    <= 8Y/3.                                             (CG11)
```

The penultimate step only needs `lambda_J>=3/2` for a component
containing `i`. The conditional normalizing constant disappears
from this oscillation.

Haar measure on unit-round `S^3` has the exact inequality

```text
Var_(mu_i)(g) <= (1/3) integral |grad_i g|^2 dmu_i.
```

Its first nonzero `-Delta` eigenvalue is `3`, already fixed by the
accepted all-spin Casimir normalization. To transfer it, put
`p=dnu_i/dmu_i`, `a=min p>0`, and `b=max p`. For a real smooth `g`,

```text
Var_(nu_i)(g)
 = inf_c integral |g-c|^2 p dmu_i
 <= b Var_(mu_i)(g)
 <= (b/3) integral |grad_i g|^2 dmu_i
 <= [b/(3a)] integral |grad_i g|^2 dnu_i.
```

Since `b/a=exp(D_i)`, this proves the uniform-in-exterior estimate

```text
Var_(nu_i)(g)
 <= [exp(8Y/3)/3] integral |grad_i g|^2 dnu_i.            (CG12)
```

There is one tilt-oscillation factor, not its square. Normalization
does not alter the ratio `b/a`.

## 5. Return to the actual quantum form

Integrating (CG12) over all exteriors and using (CG10) gives, first
for smooth functions,

```text
Var_nu(f)
 <= exp(8Y/3)/[3(1-q)] integral |grad f|^2 dnu.
```

Smooth functions are dense in the weighted `H^1` form domain on
each fixed compact graph, because the actual density is smooth and
strictly positive. Form closure extends the inequality to that
complete domain. Combining it with (CG5) yields

```text
(1/2) integral |grad f|^2 dnu
 >= (3/2)(1-4Y/3) exp(-8Y/3) Var_nu(f).                  (CG13)
```

The accepted ground-state transform `U f=psi_hat f` is unitary from
`L^2(nu)` to `L^2(mu)` and identifies its inherited form domains, with

```text
q_(A(r)-E)[Uf] = (1/2) integral |grad f|^2 dnu,
Var_nu(f) = ||Uf||_2^2-|<psi_hat,Uf>|^2.
```

This proves (CG2) on the entire excited complement.
Here q denotes the closed quadratic form, so the displayed identity
does not require an operator-domain vector. Applying
conditional expectations did not assume a tensor-product structure
for the gauge-invariant subspace: the proof was on the full product
space, and its final inequality can be restricted to invariant states.
The actual positive vacuum is invariant by the accepted uniqueness
argument. An invariant sector with no excited complement retains
the accepted vacuous-form qualification.

## 6. Coupling extension and closed endpoint

For clarity, the scalar equation arising from the two improved inputs
is

```text
Y = 4mr+(8/9)Y^2.
```

Its smaller root is exactly (CG3), and the contraction factor
`(16/9)Y` stays below one for `r<9/(128m)`. As `r` approaches that
endpoint, `Y(r)` increases to `9/16`, so throughout the open interval

```text
1-4Y(r)/3 >= 1/4,
exp[-8Y(r)/3] >= exp(-3/2).
```

Equation (CG2) therefore has the positive lower bound in (CG4),
even beyond `5/(72m)`, where the earlier expression `1-2Y(r)`
reaches zero. This replaces that geometric comparison; it does not
infer that its exhausted lower bound was the actual gap.

Two interior values make the improvement easy to compare:

```text
r<=7/(144m)  ==> Y(r)<=1/4
             ==> gap(A(r)) >= exp(-2/3) > 1/2,

r<=1/(16m)   ==> Y(r)<=3/8
             ==> gap(A(r)) >= 3/(4 exp(1)) > 1/4.         (CG14)
```

The latter bound is about `0.2759`, compared with `1/4` from the
curvature argument at `Y=3/8`. The former retains a simple half-gap
statement on the enlarged interval, with a slightly stronger actual
certificate of about `0.5134`.

At `r_*=9/(128m)`, fix one finite graph. The common-domain operators
satisfy the bounded-difference estimate
`||A(r)-A(s)||<=N_p|r-s|`. Min-max continuity of the first two ordered
eigenvalues therefore passes the same bound to `r=r_*`, exactly as
in [RECENTER_AND_INVERSE.md](RECENTER_AND_INVERSE.md), section 5.
The limit is taken separately for each finite graph. Its final
constant remains graph independent even though `N_p` in the
continuity estimate is not. No endpoint `X_G` construction or
endpoint `||u||_*` assumption is required.

## 7. Hostile cases and evidence ceiling

- A row bound for a formal polynomial approximation to `log nu`
  cannot replace (CG5). Every influence coefficient here belongs to
  the actual conditional law, including every exterior configuration
  and every generated Fourier support.
- Transposing the influence indices incorrectly would use column
  sums that were not supplied. Equations (CG6)--(CG8) retain the
  actual orientation and the appropriate `l^1` matrix norm.
- A nonreversible semigroup with an oscillation decay estimate cannot
  be passed through this self-adjoint spectral-measure argument without
  a separate theorem. Here reversibility is proved by the conditional
  expectation projections.
- At `Y=3/4`, the sufficient influence bound reaches `q=1`, and
  this argument gives no positive heat-bath constant. This is another
  certificate boundary, not a proof of vanishing physical gap.
- At the free vacuum `Y=0`, (CG2) gives `3/2`, agreeing with the full
  free-link spectral gap in the declared metric and providing a
  normalization control on the factors `1/2` and `1/3`.

The new evidence is a written derivation of the continuous-state
heat-bath spectral step, the local gradient comparison, and their
all-state transfer. It depends on the accepted actual-vacuum support
estimate, the supplied improved construction estimates, and standard
self-adjoint spectral and compact elliptic form facts used explicitly
above. No finite-state approximation, numerical experiment, old test
rerun, or proof-assistant certificate is asserted. Uniform finite-graph
coverage is closed on (CG4); an infinite-volume representation,
continuum scaling, and a continuum physical mass gap remain **OPEN**.
