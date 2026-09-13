# The actual vacuum through second order, with a convergent remainder

12 September 2026. This is a new fixed-graph calculation using the accepted
[quantum bridge](accepted_sources/ym2_global_phase_joint/GAP_BRIDGE.md), and a bounded
continuation of the [connected-response obligation](accepted_sources/ym2_signed_differences/NEXT_CONNECTED_OBLIGATION.md).
The ground state is obtained from its eigenvalue equation. No classical
Gibbs density is substituted for the quantum vacuum.

**Result.** For the open two-square SU(2) graph, the Haar-mean-one ground
state has the convergent expansion

```text
psi(r) = 1 + r(a+b)/6
           + r^2 [(a^2+b^2-1/2)/96 + ab/39 + w/351] + R_3(r),

||R_3(r)||_2 <= |r|^3/[2 sqrt(2)(1-|r|)],       |r|<1.       (CV1)
```

The eigenvector branch is analytic in `L^2` on the larger complex disk
`|r|<3/2`. The bound in (CV1) is one explicit Cauchy estimate within that
disk. The second-order logarithm contains the connected pair interaction

```text
C_pair(a,b,w) = (4w-3ab)/702.                              (CV2)
```

For edge-disjoint square plaquettes, the corresponding cross term cancels
at second order. These are exact Taylor coefficients, with a convergent
fixed-graph remainder, not an assertion that higher coefficients vanish.

## 1. Carrier, supplied ports and receiver

Retain all seven link occurrences, gauge invariance at all six vertices,
open boundary conditions, and generators `i sigma_k`. The source carrier
is `H_phys` inside `L^2(SU(2)^7, product Haar)`, with almost-everywhere
equality. There is no spin cutoff. The equivalent trace carrier is

```text
K = {(a,b,w) in [-1,1]^3: 1-a^2-b^2-w^2+2abw >= 0},
dmu_K = (2/pi^2) da db dw.
```

The operator domain is inherited from the source compact manifold as in
the accepted bridge; the singular trace boundary receives no extra boundary
condition. Let `T0=-(1/2)div(M grad)` on that domain, with

```text
       [ 4(1-a^2)   w-ab       3(b-aw)  ]
M(x) = [ w-ab        4(1-b^2)  3(a-bw)  ].
       [ 3(b-aw)     3(a-bw)   6(1-w^2) ]
```

The supplied kinetic facts are `T0 1=0`, a simple zero eigenvalue, and
`spec(T0)\{0} subset [6,infinity)`. Put

```text
S=a+b,     A(r)=T0-rS,
H/(alpha hbar^2)=A(r)+2r,     r=beta/(alpha hbar^2).
```

Physical couplings are real `r>=0`; complex `r` is only the analytic
continuation variable. The exact positive physical ground state is
normalized here by `integral psi(r) dmu_K=1`, not by unit `L^2` norm.
Its probability density is
`rho(r)=psi(r)^2/integral psi(r)^2 dmu_K` for real `r`.

The requested readouts are the ground-state energy, its first two
wavefunction coefficients, and the first two log-density coefficients.
The Taylor coefficient equations below have unique mean-zero solutions
because `T0` is invertible on mean-zero functions. This solves those
coefficient ports; the complete interacting eigenfunction remains given by
an analytic branch with a bounded remainder. A uniform connected expansion
over growing graphs remains **OPEN**.

## 2. Direct convergence proof and normalization

This is a direct application of the resolvent construction underlying
analytic perturbation theory; see
[Kato, *Perturbation Theory for Linear Operators*, Chapter VII](https://link.springer.com/book/10.1007/978-3-642-66282-9).
The quantitative constants are derived here.

On the circle `|z|=3`, the distance to the free spectrum is at least `3`.
Since `||S||_infinity=2`, the Neumann series for the resolvent of `A(r)`
converges there whenever `2|r|/3<1`. Its contour integral is an analytic
Riesz projection of constant rank one on `|r|<3/2`. Denote the enclosed
eigenvalue by `e(r)`; it is simple, with `e(0)=0`.

The resolvent Neumann test also places the perturbed spectrum within
distance `2|r|` of the free spectrum. The enclosed eigenvalue has `|e|<3`,
while every nonzero free eigenvalue is at least `6`, so its nearest free
spectral point must be zero. Consequently

```text
|e(r)| <= 2|r|.                                           (CV3)
```

Let `P0 f=(integral f)1` and `Q0=I-P0`. On `Q0 H_phys`, the operator

```text
C(r)=Q0 T0 Q0-r Q0 S Q0-e(r)
```

has a bounded inverse, with
`||C(r)^-1|| <= 1/(6-2|r|-|e(r)|) <= 1/(6-4|r|)`.
This follows by the free reduced resolvent and a second Neumann series.
An eigenvector in the enclosed eigenline cannot have zero Haar mean:
otherwise it would lie in `Q0 H_phys` and in the kernel of `C(r)`.
Local analytic eigenvectors can therefore be divided by their nonzero
means. These normalizations agree on overlaps, giving a unique analytic
`psi(r)` on the whole disk `|r|<3/2`.

For real `r` in this disk, the rest of the spectrum is at least
`6-2|r|>3`, while `e(r)` is inside the contour. Thus this branch is the
ground state. Its positive representative agrees with the accepted
compact-source positivity result.

Write `psi=1+v`, with mean-zero `v`. Its projected eigenvalue equation is

```text
C(r)v = r Q0 S1 = rS.
```

The two plaquette half traces are independent Haar half traces in the
accepted tree variables. Therefore
`integral a=integral b=integral ab=0`, `integral a^2=integral b^2=1/4`,
and `||S||_2=1/sqrt(2)`. It follows that

```text
||psi(r)-1||_2 <= |r|/[sqrt(2)(6-4|r|)].                  (CV4)
```

For any `0<R<3/2`, let `C_R=R/[sqrt(2)(6-4R)]`.
The Banach-valued Cauchy formula gives, if
`psi=1+sum_(n>=1) r^n u_n`,

```text
||u_n||_2 <= C_R/R^n,
||sum_(n>=3) r^n u_n||_2
   <= C_R (|r|/R)^3/(1-|r|/R),             |r|<R.         (CV5)
```

Taking `R=1` proves (CV1). No pointwise or conditional-density estimate is
inferred from this `L^2` estimate by itself.

## 3. Solving the first two coefficient equations

Set `psi=1+r u1+r^2 u2+...`, `e=r e1+r^2 e2+...`, and require every
`u_n` to have Haar mean zero. Comparing powers in `A(r)psi=e psi` gives

```text
e1=0,       T0 u1=S,
e2=-integral S u1,       T0 u2=S u1+e2.                  (CV6)
```

Direct differentiation of the accepted cometric gives

```text
T0 a=6a,                   T0 b=6b,
T0(a^2-1/4)=16(a^2-1/4),   T0(b^2-1/4)=16(b^2-1/4),
T0(ab)=13ab-w,              T0 w=9w.                    (CV7)
```

The cross identity contains the shared edge contribution. In particular,
`T0(ab)` is not `12ab` on this graph. Equations (CV6)-(CV7) give

```text
u1=(a+b)/6,
e2=-1/12,
T0 u2=[(a^2-1/4)+(b^2-1/4)]/6+ab/3,
u2=(a^2+b^2-1/2)/96+ab/39+w/351.                         (CV8)
```

Every displayed term has zero mean. Since the mean-zero inverse of `T0`
is unique, checking its image proves uniqueness without a search cutoff.
The source Haar moments also give `integral S u2=0`. The mean part of the
exact eigenvalue equation is `e=-r integral S psi`, hence

```text
E_0/(alpha hbar^2)=2r-r^2/12+R_E(r),
|R_E(r)| <= |r|^4/[4(1-|r|)],                |r|<1.       (CV9)
```

Here the order-three energy coefficient vanishes exactly. The bound uses
`||S||_2=1/sqrt(2)` and (CV1), not an assumption that the remaining energy
series is zero.

## 4. The logarithm and the connected term

The exact second-order jet of the unnormalized log density is

```text
log psi^2 = 2r u1+r^2(2u2-u1^2)+O(r^3)
         = r(a+b)/3
           +r^2[-(a^2+b^2)/144-1/96+(4w-3ab)/702]
           +O(r^3).                                    (CV10)
```

The mean normalization of `psi` matters only to a scalar in this formula.
Since `integral psi^2=1+r^2/72+O(r^3)`, the probability-normalized density
obeys

```text
log rho = r(a+b)/3
          +r^2[-(a^2+b^2-1/2)/144-1/36+C_pair(a,b,w)]
          +O(r^3).                                     (CV11)
```

An additive scalar cancels from normalized conditional laws. The retained
pair term `C_pair` is not a multiple of `ab+w`: its separate coefficients are
`-1/234` on `ab` and `2/351` on `w`.

For clarity about the meaning of the log remainder, the following
fixed-graph regularity argument is available independently of (CV1).
On the smooth compact source `Q=SU(2)^7`, `(T0+1)^-1` maps `H^s` boundedly
to `H^(s+2)`, and multiplication by the fixed smooth `S` preserves every
`H^s`. The elliptic regularity and Sobolev mapping facts are standard;
see [Taylor, *Short Course on Pseudodifferential Operators*, I.3, I.4 and I.8](https://mtaylor.web.unc.edu/wp-content/uploads/sites/16915/2022/05/psidolect.pdf).
The equation

```text
psi=(T0+1)^-1[(1+e+rS)psi]
```

bootstraps the proved `L^2` holomorphy into every `H^s`. Sobolev embedding
then gives holomorphy into each fixed `C^k(Q)` on the same disk. Near
`r=0`, `psi` is uniformly near `1`, so the logarithm is analytic in `C^k`
on a possibly smaller disk. Thus the `O(r^3)` in (CV10)-(CV11) can be
taken in `C^k(Q)` for each fixed `k`, with a graph-dependent radius and
constant. This is a written regularity argument; no explicit `C^k`
constant or volume-uniform log remainder is supplied here. It does not
assume regular trace-coordinate charts at the singular boundary.

The adjacent coefficient itself has an exact global bound:
`||C_pair||_infinity=2/351` and `osc C_pair=4/351` on `K`. Indeed,
`w=ab-sqrt(1-a^2)sqrt(1-b^2)z`, `|z|<=1`, so
`|4w-3ab|<=|ab|+4sqrt(1-a^2)sqrt(1-b^2)<=4` by Cauchy-Schwarz.
Both signs are attained at `a=b=0,w=+-1`.

A separate [vacuum separating witness](VACUUM_SEPARATING_WITNESS.md)
uses (CV1) together with an explicitly proved positive lower bound on
`psi` to control an actual log-vacuum observation on a numerical coupling
interval. That additional argument does not follow from the polynomial
jet alone.

## 5. What survives on a finite square or cubic lattice graph

This section changes the graph port explicitly. Supply a finite open
square or cubic lattice graph, the full product-link kinetic operator,
gauge invariance at every vertex, and a finite set of `N` distinct simple
elementary square plaquettes, with `N>=1`. There are no duplicated plaquette
occurrences or short periodic identifications. Distinct elementary
plaquettes share either one edge or no edges. An adjacent union has the
ordinary simple outer six-edge loop. Use the same generators, link metric,
and uniform plaquette coefficient `r`.

Write `a_p` for each half trace and `w_pq` for the outer-loop half trace
for an unordered adjacent pair, with loop words chosen as in the
two-square bridge. Products are functions of the joint source links.
Let `p~q` mean that the plaquettes share an edge. If they share only a
vertex, they are edge-disjoint for this calculation.

Distinct plaquettes have `integral a_p a_q=0`, by integrating an edge
present in only one plaquette. Each has `integral a_p^2=1/4`. The local
kinetic differentiation is unaffected by additional edges. Therefore

```text
T0(a_p a_q)=12 a_p a_q                 if p is not adjacent to q,
T0(a_p a_q)=13 a_p a_q-w_pq           if p~q,
T0 w_pq=9 w_pq.                                          (CV12)
```

For the first case, the mixed product-rule term is zero because no
derivative acts on the same edge occurrence in both factors. For the
second case, the union is precisely the shared-edge calculation (CV7).
The global inverse need not be assumed local: the displayed local
polynomial has the required image, and uniqueness of the mean-zero
inverse certifies that it is the full coefficient.

For the energy after subtracting the constant `Nr`, these facts give

```text
u1=(sum_p a_p)/6,     e2=-N/24,
u2=sum_p (a_p^2-1/4)/96
   +sum_(p<q, p not~q) a_p a_q/36
   +sum_(p<q, p~q) [a_p a_q/39+w_pq/351].                (CV13)
```

The cross term of `u1^2` for each unordered pair is `a_p a_q/18`.
For every edge-disjoint pair it equals twice the corresponding `u2`
coefficient and cancels exactly. For an adjacent pair the surviving
coefficient is `(4w_pq-3a_p a_q)/702`. The result is

```text
log psi^2 = (r/3)sum_p a_p
  +r^2[-sum_p a_p^2/144-N/192
        +sum_(p<q, p~q)(4w_pq-3a_p a_q)/702]+O_G(r^3),

log rho = (r/3)sum_p a_p
  +r^2[-sum_p(a_p^2-1/4)/144-N/72
        +sum_(p<q, p~q)(4w_pq-3a_p a_q)/702]+O_G(r^3).    (CV14)
```

This is a written coefficient theorem for the declared finite graph
class. It shows connected support through second order. It does not
exclude connected chains through other plaquettes at later orders.

For each fixed graph the same free-gap proof applies. The elementary
analytic argument above has `||sum_p a_p||_infinity<=N` and yields only
the disk `|r|<3/N`, with

```text
||psi(r)-1||_2 <= |r| sqrt(N)/[2(6-2N|r|)].               (CV15)
```

Its shrinking radius exposes the remaining limitation: cancellation of
every disconnected pair at order two is not a uniform cluster-convergence
theorem. The required graph-uniform conditional response estimate and a
spectral estimate that survives physical continuum scaling remain OPEN.

## 6. Verification and hostile controls

The new standard-library checker differentiates `M` using exact rational
polynomials, verifies the coefficient equations and Haar means, computes
the second-order log polynomial, and checks the edge-disjoint cancellation.
It also retains the nonzero residual produced by incorrectly using that
disconnected coefficient on adjacent plaquettes. It computes Haar moments
by the exact conditional `w` law, without numerical quadrature.

```powershell
python -I -B check_connected.py
```

Run from this packet's directory. Default execution is read-only and
compares the complete recomputed receipt with the saved receipt, including
relative source paths and their hashes. To intentionally regenerate the
adjacent receipt after a reviewed source change, use
`python -I -B check_connected.py --write-results`.

The receipt is [RESULTS_CONNECTED.json](RESULTS_CONNECTED.json). The finite
checks do not verify the spectral projection theorem, elliptic regularity,
or the arbitrary-graph proof by exhausting graph instances. Those are
written arguments using their stated established mathematical inputs.
The source spectrum/domain and cometric are reused at their accepted
scope; no old verification suite is rerun by this command. Source hashes
bind the exact reused files and new checked bytes, and do not prove them.
