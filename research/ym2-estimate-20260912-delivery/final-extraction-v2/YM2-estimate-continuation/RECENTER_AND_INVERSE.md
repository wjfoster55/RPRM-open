# Recentered vacuum equation, inverse scope, and the closed endpoint

12 September 2026. A bounded written continuation of the accepted proof in
[DIRECT_COVER_ATTEMPT.md](accepted/DIRECT_COVER_ATTEMPT.md)
and the certificate boundary in
[NEXT_OBLIGATION.md](accepted/NEXT_OBLIGATION.md).
No old proof or test suite is reopened. The calculations below are new
written derivations, not a formal certificate or numerical experiment.

## 1. Contract and the question being continued

The carrier is the same finite open square or cubic lattice graph `G`,
with full, untruncated `SU(2)` link variables, distinct square plaquette
occurrences, product normalized Haar measure `mu`, and unit-round-`S^3`
metric. In the accepted normalization,

```text
T = -(1/2) Delta,       S = sum_p (1/2) Tr(U_p),
A(r) = T-rS,           m = 2(d-1),
Qf = f-mu(f),          a = T^-1 S,
B(f,g) = T^-1 Q <grad f,grad g>,
b = 8/3,              ||a||_* <= 8m,
||B(f,g)||_* <= b ||f||_* ||g||_*.
```

`T^-1` removes the scalar mode. `X_G` is the accepted Haar-mean-zero,
energy-weighted anchored Fourier space: for
`f_J=Tr(B_J pi_J)`, `lambda_J=sum_e 2j_e(j_e+1)`,

```text
||f||_* = max_e sum_(J:e in supp J) lambda_J ||B_J||_1.
```

Functions are equal as their Haar-almost-everywhere equivalence classes;
the continuous representatives furnished by this space may be used in
the equations. A log vacuum uses the normalization `mu(u)=0`; adding a
constant changes the normalization of its wavefunction, not its physical
ground-state line.

The supplied ports are an actual log vacuum `u0` at `r0`, a certified bound
`y0=||u0||_* <= Y0 < 1/b`, and an increment `delta r`. The missing port is
the response `v=u(r0+delta r)-u0` in this same normalization. The requested
receiver is a construction of the actual vacuum together with a lower
bound on the complete excited-state energy form. A local fixed-point
uniqueness assertion means uniqueness in its declared ball; it does not
enumerate every algebraic solution of the log-vacuum equation outside it.

## 2. Exact recentering and the old estimate's maximum increment

The accepted vacuum equation is `u=ra+B(u,u)/2`. Symmetry and bilinearity
give the exact subtraction identity

```text
v = (delta r)a+B(u0,v)+(1/2)B(v,v).                       (RI1)
```

Put `h=8m|delta r|`. On a closed `X_G` ball of radius `Z`, the old estimates
give a self-map and contraction whenever

```text
h+bY0 Z+(b/2)Z^2 <= Z,
b(Y0+Z) < 1.                                             (RI2)
```

For the first line, the largest allowed forcing according to this
quadratic bound is

```text
q_(Y0)(Z) = (1-bY0)Z-(b/2)Z^2,
Z_* = (1-bY0)/b,
max_(Z>=0) q_(Y0)(Z)
  = h_* = (1-bY0)^2/(2b)
  = [1-(8/3)Y0]^2/(16/3).                                (RI3)
```

At `Z=Z_*`, the second line of (RI2) is an equality, so Banach contraction
does not follow. Thus `h_*` is the exact maximum of the radius-admissibility
quadratic and the supremum, not an attained positive endpoint, of the
strict-contraction forcing increments established by (RI2).
For `0<=h<h_*`, the smaller radius

```text
Z_- = [(1-bY0)-sqrt((1-bY0)^2-2bh)]/b                     (RI4)
```

satisfies both conditions. Its contraction multiplier is
`1-sqrt((1-bY0)^2-2bh)<1`. This constructs the response of the actual
vacuum: the new fixed point produces a positive eigenfunction, and the
accepted ground-state form identity identifies its eigenvalue as the
simple bottom eigenvalue.

Now let `t0=8mr0`, and suppose the available bound is exactly the old
smaller-root majorant, so that

```text
t0 = Y0-(b/2)Y0^2,       0<=Y0<1/b.
```

For continuation toward increasing `r`, (RI3) then gives the cancellation

```text
t0+h_*
 = Y0-(b/2)Y0^2 + (1-2bY0+b^2Y0^2)/(2b)
 = 1/(2b)
 = 3/16.                                                  (RI5)
```

More strongly, substituting this identity into (RI4) gives

```text
Y0+Z_- = [1-sqrt(1-2b(t0+h))]/b.                         (RI6)
```

That is exactly the original smaller-root radius at total forcing
`t0+h`. Restarting at an intermediate point with only this old majorant
reproduces the same majorant at the next point. Repeating that operation
cannot carry its strict contraction certificate beyond
`8mr<3/16`, equivalently `r<3/(128m)`.

This is a limitation of those supplied estimates. It is not an assertion
that the actual norm equals its majorant, that every use of `X_G` must
stop there, or that the actual vacuum stops existing. In particular, an
independently proved smaller bound on `y0`, a smaller source estimate,
or a sharper estimate of the actual linearized operation is new input
and can change (RI5). Mere recentering supplies none of those improvements.

## 3. Applying the old Neumann inverse yields the same envelope

Define the derivative of the fixed-point residual by

```text
K0 = I-B(u0, .) : X_G -> X_G.
```

Since `||B(u0, .)|| <= bY0<1`, the operator has a genuine Neumann inverse
on `X_G`, with

```text
K0^-1 = sum_(n>=0) B(u0, .)^n,
||K0^-1|| <= M0 = 1/(1-bY0).                             (RI7)
```

Applying this inverse to (RI1) gives the exact equation

```text
v = (delta r)K0^-1 a+(1/2)K0^-1 B(v,v).                  (RI8)
```

Using only (RI7) and the old bilinear estimate, a radius must satisfy

```text
Z >= M0 h+(M0 b/2)Z^2,       M0 b Z<1.
```

The resulting increment condition is
`h<1/(2M0^2 b)=(1-bY0)^2/(2b)`, precisely (RI3). Calling the operation
an inverse has not changed the estimate that controls it.

A concrete sharper inverse route would instead prove, uniformly in the
admitted graphs and centers, usable constants

```text
||K0^-1 a||_* <= A0,
||K0^-1 B(f,g)||_* <= C0 ||f||_* ||g||_*.
```

Then the inverse-first construction permits
`2 C0 A0 |delta r|<1`, with the corresponding smaller-root radius, for
positive `A0,C0`. These are directional source and nonlinear inverse
estimates. The bound on the complete energy form must still be carried
through the new vacuum, for example by controlling `||u0+v||_*` in the
accepted Hessian argument. The displayed targets identify what must be
proved; this note does not claim such improved constants.

## 4. The actual weighted Poisson inverse is a different norm question

Let `nu0` be the probability measure proportional to `exp(2u0)mu`, and set

```text
L0 = Delta+2 grad u0 dot grad,
P0 = -(1/2)L0 = T-grad u0 dot grad.
```

On smooth Haar-mean-zero functions, the exact relation is

```text
K0 = T^-1 Q P0.                                          (RI9)
```

`P0` is nonnegative and self-adjoint in `L^2(nu0)`; its kernel consists
of constants. Its inverse on the `nu0`-mean-zero subspace is the actual
weighted Poisson inverse. The accepted gap bound gives

```text
gap(P0) >= gamma0 = 1-2Y0,
||P0^-1||_(L^2_0(nu0) -> L^2_0(nu0)) <= 1/gamma0.        (RI10)
```

This upper bound tends to `4` as the old majorant `Y0` tends to `3/8`.
By contrast, the Neumann upper bound `1/(1-bY0)` tends to infinity.
The divergence of the latter bound does not establish divergence or
nonexistence of the actual inverse.

The projections and function spaces in (RI9) matter. For a smooth
Haar-mean-zero source `g`, solving `K0 v=g`, with `mu(v)=0`, is equivalent
to

```text
P0 v = Tg-nu0(Tg),
w = P0^-1 [Tg-nu0(Tg)],
v = w-mu(w).                                             (RI11)
```

Indeed `Q P0 v=Tg` determines `P0v` up to a scalar; invariance of `nu0`
determines that scalar by `nu0(P0v)=0`. The last line fixes the log-vacuum
normalization. A smooth source has a unique smooth normalized solution
by this compact elliptic Poisson problem. Equation (RI11) is a genuine
inverse representation on that smooth carrier, not permission to use
an `L^2` estimate as an `X_G` estimate. Sources such as `a` and
`B(f,g)` also carry their own derivative and projection structure, which
an improved estimate may exploit.

The target of (RI10) is only `L^2(nu0)`. The target needed in (RI8) sums
trace norms of all Fourier blocks touching each anchor and weights
their energies. No graph-uniform comparison from the former target to
the latter was supplied. In (RI11), applying `T`, subtracting a `nu0`
mean and recovering the anchored Fourier norm all need their own
mapping estimates. For fixed `G`, smooth elliptic regularity is
available; its constants and the constants comparing Haar and `nu0`
norms cannot silently become uniform in the number of links.

There is a hostile case even at the free vacuum. Take a one-square graph,
`u0=0`, and the gauge-invariant spin-`j` character of its holonomy,

```text
f_j(U) = chi_j(U_p),       j>0.
```

Haar integration of any one link makes the holonomy Haar distributed,
so character orthogonality gives `mu(f_j)=0` and `||f_j||_2=1`. Every
Fourier component has spin `j` on all four links, hence
`T f_j=Lambda_j f_j` with `Lambda_j=8j(j+1)`. The Fourier-algebra norm
dominates the supremum norm, and at identity holonomy
`f_j=2j+1`. Consequently

```text
||T^-1 f_j||_*
 = ||f_j||_A
 >= 2j+1 -> infinity.                                    (RI12)
```

Thus even the free Poisson inverse, which is bounded on mean-zero
`L^2`, has no bounded map from the `L^2` unit ball into `X_G` on this
fixed graph. This does not refute an `X_G -> X_G` estimate for `K0^-1`:
at this very center `K0=I`. It exactly refutes the shortcut that a
spectral-gap bound alone supplies the required Fourier target control.
It retains high spins and is already gauge invariant.

## 5. A new closed-endpoint gap statement from continuity alone

The old strict interval can be closed for the spectral lower bound,
without proving any endpoint log-vacuum norm estimate. Define

```text
r_* = 3/(128m).
```

Fix one admitted finite graph. Because each half trace is between `-1`
and `1`, `||S||_infinity<=N_p`. The operators have a common domain and
differ by a bounded multiplication operator, so

```text
||A(r)-A(s)|| <= N_p |r-s|.
```

Here the norm denotes the bounded difference, not either unbounded
operator separately. The min-max principle applied to their compact
resolvents yields, for each ordered eigenvalue counted with multiplicity,

```text
|E_k(r)-E_k(s)| <= N_p |r-s|.                            (RI13)
```

For every `r<r_*`, the accepted proof gives

```text
E_1(r)-E_0(r) >= 1-2R_-(r),
R_-(r) = (3/8)[1-sqrt(1-128mr/3)].
```

Taking `r` upward to `r_*` in this fixed graph, (RI13) proves

```text
gap(A(r_*)) >= 1/4.                                      (RI14)
```

In particular, the ground eigenvalue at the endpoint remains simple.
The continuity constant `N_p` is graph dependent; this causes no loss
of uniformity in (RI14). The limit is taken separately for every finite
graph, and the resulting lower bound is the same `1/4` for all graphs.
No joint volume/coupling limit is being interchanged. Altogether,

```text
0<=r<=3/(128m)
  ==> gap(A(r)) >= 1/4                                  (RI15)
```

on the full-link carrier. The interior retains its stronger explicit
bound `1-2R_-(r)`.

The endpoint vacuum is gauge invariant as well. For example, its
isolated rank-one spectral projection is the norm limit of the interior
ground-state projections under this bounded perturbation; their ranges
lie in the closed gauge-invariant subspace. The full-space gap bound
therefore restricts to the physical subspace, with the accepted proviso
that an empty excited complement yields a vacuous form inequality.

The proof of (RI14) does not assert that `u(r_*)` was constructed by the
endpoint Banach map, does not use `||u(r_*)||_*<=3/8`, and does not provide
a graph-uniform positive amount of continuation beyond `r_*`. Continuity
on any one finite graph may use its own `N_p`; that argument alone gives
no positive common extension in `r` for graphs of unbounded size.

## 6. What is closed and what remains open

The recentering and Neumann-inverse calculations close a specific
method question: restarting with exactly the old scalar-majorant data
reproduces its envelope. The weighted Poisson calculation identifies
an actual inverse and the missing graph-uniform mapping estimate.
The spectral continuity calculation closes the finite-graph endpoint
bound `gap>=1/4` uniformly over the admitted graph family.

An improved inverse estimate is **OPEN within this recentering route**.
The other notes in this continuation supply sharper source and bilinear
estimates and therefore enlarge the interval by new input; see
[RESULT.md](RESULT.md). Recentring alone has not supplied a stronger
inverse or alternative reference estimate preserving the complete
energy-form receiver. The repeated positive
lower bound shows that this particular vacuum-construction certificate
expires before its curvature estimate reaches zero. It supplies no
evidence that the physical gap vanishes there.

These statements are at the fixed lattice energy scale. Multiplication
by `E_el=alpha hbar^2` gives a bound in the original energy units for
the same admitted ratios. Refining the lattice while changing those
coefficients requires its declared physical scaling and convergence
contracts; neither the endpoint argument nor a local inverse alone
closes that further question.
