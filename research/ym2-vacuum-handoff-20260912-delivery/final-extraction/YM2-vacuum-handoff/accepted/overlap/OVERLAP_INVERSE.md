# Overlapping blocks and the actual-vacuum inverse

12 September 2026. Bounded written continuation. The calculations below
use the accepted full-link Fourier carrier; they run no simulation or
previous verifier and change no accepted result. Ordinary coordinate
blocks, conditional inverses and additive preconditioners are established
mathematical constructions. This note makes no novelty claim for them.

The useful outcome is precise: overlapping blocks reconstruct the free
inverse when they retain each Fourier mode's complete kinetic energy.
Adding partial kinetic inverses does not do so. A positive sum of those
partial inverses fails the required general local-norm preconditioner
bound even on a fixed graph. This leaves a concrete, narrower obligation
for using an interacting overlapping construction.

## 1. Contract and inherited target

The carrier is a finite admitted square or cubic lattice graph `G`, with
link set `E`, full `SU(2)^E`, product normalized Haar measure `mu`, and the
accepted unit-round metric. Spins have no cutoff. Link occurrences shared
by blocks remain the same variables. Equality is Haar almost everywhere.
All displayed algebraic identities first hold on finite Peter-Weyl sums;
extensions are stated separately. The gauge-invariant examples below use
the same vertex gauge action as the accepted theory.

Write

```text
T = sum_e T_e,             T_e = -(1/2) Delta_e,
c_j = 2j(j+1),             lambda_J = sum_e c_(j_e),
supp J = {e : j_e > 0},    Q_mu f = f-mu(f),
f_J = Tr(B_J pi_J),
||f||_* = max_e sum_(J:e in supp J) lambda_J ||B_J||_1.
```

The source norm used only in this note is

```text
||h||_diamond = max_e sum_(J:e in supp J) ||B_J(h)||_1.
```

On mean-zero sources of finite diamond norm the free inverse is exactly
an isometry into the accepted space `X_G`:

```text
||T^-1 h||_* = ||h||_diamond.                            (OI1)
```

This follows block by block from cancellation of `lambda_J`; it is not
an `L2 -> X_G` estimate. Constants are the kernel of `T`; Haar mean zero
selects its unique inverse. Equation (OI1) covers every spin and support
for the fixed graph, with constant one independent of the graph.

For the actual vacuum `u0` at a center `r0`, the inherited inverse target
is

```text
B(f,g) = T^-1 Q_mu <grad f,grad g>,
K0 = I-B(u0,.),            a = T^-1 S,
||K0^-1 a||_* <= A0,
||K0^-1 B(f,g)||_* <= C0 ||f||_* ||g||_* .               (OI2)
```

These directional estimates would admit increments
`2 A0 C0 |delta r| < 1` in the recentered equation, when `A0,C0>0`.
The current accepted bounds are `||a||_* <= 4m` and bilinear constant
`16/9`, giving the strict construction interval `r<9/(128m)`.
The closed endpoint spectral bound is already supplied by the previous
continuation. This note does not enlarge either interval.

Dependencies: [RESULT.md](accepted/estimate/RESULT.md) and
[RECENTER_AND_INVERSE.md](accepted/estimate/RECENTER_AND_INVERSE.md).
The latter records older constants as part of its restart calculation;
the newer `4m,16/9` constants are used for the present target.

## 2. Two genuinely different local inverse proposals

Let `mathcal B` be a finite family of nonempty link subsets covering `E`.
Allow overlaps. Give each block a positive scalar weight `theta_B`.
Let `E_B` denote integration over the links in `B`, retaining all exterior
variables, and set `Q_B=I-E_B`. Define the partial kinetic operator and
its conditional inverse by

```text
T_B = sum_(e in B) T_e,
lambda_B(J) = sum_(e in B) c_(j_e),
R_B = T_B^-1 Q_B.
```

The inverse is conditional: for each exterior configuration its output
has zero Haar mean over `B`. Its exact Fourier multiplier is

```text
R_B(J) = 1/lambda_B(J)   if supp J intersects B,
       = 0               otherwise.                    (OI3)
```

The exterior Fourier factors remain present. Consequently, for the
positive additive candidate `M=sum_B theta_B R_B`,

```text
(MT)(J) = q(J),
q(J) = lambda_J sum_(B:lambda_B(J)>0)
                         theta_B/lambda_B(J).           (OI4)
```

Coverage does not make this multiplier one. For a mode supported at one
edge `e`, it equals `sum_(B:e in B) theta_B`. Balancing these singleton
coverage counts can repair those particular modes. It does not repair
joint modes with support across several blocks.

A different proposal retains only functions depending entirely on a
block. Let `F_B=E_(E\B)` integrate the exterior, and define

```text
R_tilde_B = T_B^-1 Q_mu F_B.
```

Its multiplier is `1/lambda_J` when `empty != supp J subset B` and zero
otherwise. Therefore

```text
(sum_B theta_B R_tilde_B) T (J)
   = sum_(B:supp J subset B) theta_B.                   (OI5)
```

Every mode whose complete support fits in no block lies in this
candidate's kernel. Overlap of link sets alone does not restore the
discarded joint sector. A source decomposition supported only in the
individual blocks would require an additional completeness argument.

## 3. Exact hostile cases

### A. A long gauge-invariant loop

Let `C` be a simple lattice cycle of `k` links and let
`f_C,j = chi_j(U_C)`, for `j>0`. A graph containing this cycle and an
elementary square is admitted; a rectangular grid is one choice.
Character orthogonality after integrating one cycle link gives
`mu(f_C,j)=0` and `||f_C,j||_2=1`. Every Fourier component has spin `j`
on each cycle link and zero elsewhere, so `lambda_J=k c_j`.

For singleton blocks with weight one, (OI4) gives

```text
MT f_C,j = k^2 f_C,j.                                    (OI6)
```

The cover has multiplicity one. Its failure therefore cannot be blamed
on excessive geometric overlap. If every chosen block misses at least
one edge of `C`, (OI5) instead annihilates the same mode. These are two
distinct failures: excessive partial-inverse weight versus lost support.
Dividing the first candidate by the number of active singleton blocks
only changes `k^2` to `k`; ordinary overlap counting is insufficient.

### B. High spin outside a proper block, on a fixed graph

Suppose the positive additive candidate includes a proper nonempty
block `B`, and choose `e in B`, `f outside B`. Take a nonzero Fourier
mode with spin `1/2` on `e`, spin `j` on `f`, and spin zero elsewhere.
Then `lambda_B=3/2` and

```text
q(J) >= theta_B [3/2+2j(j+1)]/(3/2) -> infinity.         (OI7)
```

Normalizing this mode to have `||g_J||_*=1` leaves
`||MT g_J||_*=q(J)`. Thus `MT` has no bounded extension `X_G -> X_G`
on this fixed full-link graph. Equivalently, `M` has no bounded map
from the diamond source space into `X_G`. Adding more positive block
inverses cannot cancel this lower bound. Each individual `R_B` remains
bounded `X_G -> X_G`; it is its composition with `T`, or its use with
the weaker source norm, that fails.

There is also a gauge-invariant version whenever a block contains all
links of a plaquette `p` and none of an edge-disjoint plaquette `q`.
Use

```text
g_j = chi_(1/2)(U_p) chi_j(U_q).
```

These factors can live on two squares joined by a path or sharing only
a vertex. They are separately gauge invariant. Their product has total
kinetic energy `6+8j(j+1)` and block energy `6`, hence
`q(J) >= theta_B [6+8j(j+1)]/6`. The same fixed-graph divergence follows.
For arbitrary covers the ambient witness (OI7) always applies; this
particular physical witness requires the stated two-loop placement.

This refutes the general `X_G` preconditioner bound for the stated
positive partial-inverse candidate. It does not refute every additive
Schwarz method, every frequency-weighted construction, or separate
estimates restricted to the particular source and nonlinear ranges in
(OI2). Those have different obligations.

## 4. Exact repairs that retain the missing energy information

One diagonal repair of (OI4) is explicit. Let `D` have multiplier `q(J)`
on nonconstant modes. Since the cover is complete,

```text
q(J) >= c_min > 0,
c_min = min_e sum_(B:e in B) theta_B.
```

To prove the inequality, pick an edge in `supp J`, retain just its
containing blocks, and use `lambda_J/lambda_B(J)>=1`. Thus `D^-1` is
bounded on `X_G` by `1/c_min`, and blockwise

```text
D^-1 M = T^-1 Q_mu.                                     (OI8)
```

The formula extends from Fourier polynomials by (OI1). Its normalizer
depends on the energies of the complete mode in every intersected
block. It is not a geometry-only overlap count. The repaired operator
is exactly the original free inverse, with no improved constant or
new interacting estimate claimed.

There is another useful exact assembly that uses block heat operators.
Choose nonnegative occurrence weights `w_(B,e)`, zero outside `B`, with
`sum_B w_(B,e)=1` for every link. For example, divide each link equally
among all of its containing blocks. Put

```text
T_B^w = sum_e w_(B,e) T_e,        sum_B T_B^w = T.
```

The link Casimirs commute, so all these block operators commute. Hence

```text
product_B exp(-t T_B^w) = exp(-t T),
T^-1 Q_mu = integral_(0 to infinity)
                     [product_B exp(-t T_B^w)] Q_mu dt. (OI9)
```

For a nonconstant Fourier mode the integrand multiplier is exactly
`exp(-t sum_B lambda_B^w(J))=exp(-t lambda_J)`, whose integral is
`1/lambda_J`. This proves the identity directly, without a time-step
approximation, a spin truncation, or independent copies of overlaps.
It extends in `L2` on mean-zero inputs and from the diamond space into
`X_G` by (OI1).

The common integration parameter matters. Integrating each block first
and adding its inverse gives (OI4), a different operation. The successful
assembly preserves the joint mode through all blocks at the same `t`.
Every component here is gauge equivariant. Nothing in this free identity
constructs an interacting reference vacuum.

## 5. What the actual weighted operator would need

For an actual smooth log vacuum `u0`, set

```text
d nu0 = Z0^-1 exp(2u0) d mu,
P0 = T-grad u0 dot grad,       Q_nu0 h = h-nu0(h).
```

The exact normalized inverse relation remains

```text
K0^-1 g = Q_mu P0^-1 Q_nu0 T g.                         (OI10)
```

The weighted Poisson inverse in this expression is taken on the
`nu0`-mean-zero space. The extra `T`, the two mean conventions and the
final `X_G` readout are essential.

An overlapping partial weighted generator can be defined without
changing the joint measure:

```text
P_(0,B)^w = sum_e w_(B,e)
                      [T_e-grad_e u0 dot grad_e],
sum_B P_(0,B)^w = P0.
```

Its conditional measure retains the exterior configuration and every
interaction crossing the block boundary. For unweighted blocks the
conditional Poisson inverse `R_(0,B)` obeys

```text
P_(0,B) R_(0,B) = R_(0,B) P_(0,B) = I-E_B^(nu0),
```

on the appropriate smooth conditional carrier. Existence of conditional
inverses on each fixed compact fiber follows from the positive smooth
density; any uniform estimates over exterior data and graphs are extra
requirements. In general overlapping weighted generators and their
conditional projections do not commute. Thus the finite product in
(OI9) is not automatically the interacting heat semigroup. An ordered
limit or a commutator-controlled approximation needs its own proof and
its own norm estimates.

Here is a precise sufficient continuation target for any proposed
weighted assembly `M0`, whether additive or corrected. Define initially
on smooth Haar-mean-zero functions

```text
N0 = Q_mu M0 Q_nu0 T,       E0 = I-N0 K0.                (OI11)
```

Prove that `N0` extends boundedly on `X_G` and, uniformly in the
admitted graphs and centers, establish

```text
||E0||_(X_G -> X_G) <= rho < 1,
||N0 a||_* <= A_pre,
||N0 B(f,g)||_* <= C_pre ||f||_* ||g||_* .              (OI12)
```

For a fixed graph smooth elliptic solvability gives the actual inverse
on smooth sources. There `sum_(n>=0) E0^n N0` equals that inverse,
because `N0 K0=I-E0`. Fourier polynomials are dense in `X_G`, `K0` is
bounded by the accepted bilinear estimate, and the bounded extension
of this series therefore gives a two-sided inverse on `X_G`. It yields

```text
A0 <= A_pre/(1-rho),     C0 <= C_pre/(1-rho),
2 A_pre C_pre |delta r| < (1-rho)^2.                    (OI13)
```

The directional sources in (OI12) retain helpful structure:

```text
N0 a = Q_mu M0 Q_nu0 S,
N0 B(f,g) = Q_mu M0 Q_nu0 <grad f,grad g>.
```

They need not be bounded by discarding that structure. Equations
(OI11)-(OI13) are a sufficient target, not a claim that every successful
continuation must use a bounded preconditioner of this form.

The naive positive sum of conditional partial inverses does not meet
this target even at `u0=0`: then `K0=I`, `N0=MT`, and (OI7) makes both
`N0` and its defect unbounded. A different source-specific argument
would have to address the relevant joint sectors directly. An `L2`
conditional gap alone supplies none of the missing Fourier estimates.

## 6. Closure and remaining seam

The free normalized inverse fiber is **ONE**, explicitly (OI8) or
(OI9), for each admitted mean-zero source in the stated spaces. The
unconditional additive proposal is exactly rejected at its claimed
general norm scope by (OI7); the fully block-supported proposal loses
the modes identified in (OI5). These are written proofs over all
spins, with exact gauge-invariant hostile cases, not finite-test evidence.

The useful next obligation is **OPEN**: construct a weighted assembly
whose retained boundary interactions and full-support energy treatment
give stronger graph-uniform bounds of the kind (OI2) or (OI12). Such a
bound must control the continued actual vacuum and then carry the
complete physical energy-form receiver. This note supplies neither a
larger coupling interval nor continuum existence. It supplies the exact
free comparison and a discriminating test that any proposed overlap
inverse can be checked against before making either claim.
