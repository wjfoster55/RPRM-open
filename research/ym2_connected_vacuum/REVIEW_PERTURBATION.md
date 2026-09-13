# Independent review of the connected-vacuum perturbation argument

12 September 2026. **Disposition: no blocking mathematical finding in the
reviewed fixed-graph claims.** The actual ground-state branch, its first two
coefficients and the explicit `L^2` remainder are supported by the displayed
written argument, conditional on the accepted source operator and free
spectrum. The order-two connected-support theorem is also supported on its
declared finite graph class. The note does not supply a graph-uniform
log-response remainder or a continuum mass gap.

Reviewed source: [CONNECTED_VACUUM.md](CONNECTED_VACUUM.md).
Operator premise: [GAP_BRIDGE.md](accepted_sources/ym2_global_phase_joint/GAP_BRIDGE.md).
This reviewer wrote only this review, did not edit either source, and did not
read, import or execute the author's polynomial checker. Algebra and estimates
below were checked directly from the written equations. This is independent
written review, not a proof-assistant certificate or an independent proof of
the shared source premises.

## 1. Admission, domain and analytic branch

The source contract matches the accepted open two-square seven-link graph,
full vertex gauge invariance, generators `i sigma_k`, and product Haar
measure. The kinetic normalization is exactly
`T0=-(1/2)sum_e Delta_e`. The physical source domain is inherited from the
compact smooth source; the trace quotient's singular boundary is not given
an extra boundary condition. The accepted physical free gap is `6` and the
constant eigenvector is simple. These are operator/spectral premises, not
conclusions of differentiating a finite trace polynomial.

The perturbation is the bounded multiplication `-rS`, with `S=a+b` and
`||S||_infinity=2`, on a fixed domain. The following checks support the full
complex disk `|r|<3/2` asserted for the mean-normalized branch:

- On `|z|=3`, `dist(z,spec T0)>=3`, so the free resolvent norm is at most
  `1/3`. The bounded perturbation Neumann series has ratio at most
  `2|r|/3<1`. It produces a holomorphic Riesz projection; its finite rank
  stays one on the connected disk.
- Spectral inclusion within `2|r|` of the free spectrum applies without
  assuming that the complex perturbed operator is normal. If the enclosed
  eigenvalue `e` has `|e|<3`, every free spectral point `lambda>=6` is more
  than `3` away. Hence the nearby free point must be zero and `|e|<=2|r|`.
- On the mean-zero space the inverse estimate is
  `||(Q0T0Q0-rQ0SQ0-e)^-1|| <= (6-2|r|-|e|)^-1`.
  The denominator is at least `6-4|r|>0`. Therefore an eigenvector on the
  enclosed line cannot have zero Haar mean. Dividing local analytic
  eigenvectors by that mean gives compatible normalizations on overlaps.
  The scalar-normalized eigenvector is consequently holomorphic across
  the entire disk, not merely near zero.
- For real couplings, the next eigenvalue is at least `6-2|r|>3` by the
  variational bound. Thus the enclosed eigenvalue is the ground branch.
  Positivity is supplied by the accepted compact-source ground-state result.

A projection's analyticity alone would not justify an arbitrary scalar
normalization globally. The source explicitly supplies the additional
mean-nonvanishing argument, which closes that potential gap.

## 2. The remainder is an actual `L^2` estimate

With `psi=1+v`, `integral v=0`, the reduced equation is exactly
`C(r)v=rS`. Independence of the two Haar holonomies gives
`integral S^2=1/2`. The inverse estimate therefore yields

```text
||v(r)||_2 <= |r|/[sqrt(2)(6-4|r|)].
```

On the circle `|r|=R<3/2`, this is the stated `C_R`. Applying the
Banach-valued Cauchy coefficient estimate to `v` and summing the geometric
tail gives

```text
||sum_{n>=3} r^n u_n||_2
 <= C_R (|r|/R)^3/(1-|r|/R).
```

Setting `R=1` gives `C_R=1/(2 sqrt(2))` and exactly (CV1). This estimate
bounds the tail of the actual mean-normalized ground-state branch for the
real physical interval `0<=r<1`; it is not merely an order symbol or a
numerical residual of a truncated eigenvalue equation.

This bound does not control point evaluation, an essential supremum, a
pointwise lower bound for `psi`, or a conditional-density ratio by itself.
The source correctly does not use it for those stronger conclusions.
The radius is in the dimensionless ratio `r=beta/(alpha hbar^2)`. It must
not be described as a continuum weak-bare-coupling region without the
separate physical scaling contract.

## 3. Coefficients, Haar mean and energy

Direct product differentiation of the displayed kinetic operator gives

```text
T0 a=6a,
T0 a^2=16a^2-4,
T0(ab)=12ab-(w-ab)=13ab-w,
T0 w=9w,
```

with the corresponding `b` identities. Thus the shared-edge term is
retained in `T0(ab)`. It cannot be replaced by the edge-disjoint value
`12ab` while keeping this generator.

The first coefficient is `u1=(a+b)/6`. Since `integral a^2=integral
b^2=1/4` and `integral ab=0`, `integral S u1=1/12`, giving `e2=-1/12`.
Applying `T0` to the proposed cross coefficient gives

```text
T0(ab/39+w/351)
 = ab/3 + (-1/39+9/351)w
 = ab/3.
```

Applying it to the remaining terms gives
`[(a^2-1/4)+(b^2-1/4)]/6`. All terms of `u2` have zero Haar mean, including
`w`. The mean-zero inverse of the accepted physical kinetic operator is
unique, so this checks the full coefficient port; it does not depend on a
spin truncation or merely testing selected configurations.

The identity `integral S u2=0` follows from odd Haar moments and
`E[w|a,b]=ab`. Consequently the exact mean equation
`e=-r integral S psi` has no cubic term. Cauchy-Schwarz with the (CV1) tail
gives

```text
|r integral S R3| <= |r|^4/[4(1-|r|)],
```

which verifies the stated actual energy remainder (CV9).

## 4. Logarithm: correct normalization and justified local topology

The algebraic log coefficient is `2u2-u1^2`. Its coefficients are
`-1/144` on `a^2+b^2`, `-1/96` as scalar, `-1/234` on `ab`, and
`2/351` on `w`. These reproduce (CV10), including
`C_pair=(4w-3ab)/702`.

The source uses Haar mean one, so `psi` has not been normalized to unit
`L^2` norm. In fact

```text
integral psi^2 = 1+r^2/72+O(r^3).
```

Subtracting its logarithm changes the quadratic scalar to `-7/288`.
Expanding the scalar terms in (CV11) gives exactly the same value. The
normalization is therefore consistent. Constants cancel in conditional
normalization, but retaining them is necessary for the claimed density
and energy readouts.

The source supplies a separate route to a genuine local log expansion.
On the smooth compact source, the inverse of `T0+1` gains two Sobolev
derivatives and multiplication by the fixed smooth `S` is bounded on each
Sobolev space. If `psi` is holomorphic into `H^s`, the equation

```text
psi=(T0+1)^-1[(1+e+rS)psi]
```

makes it holomorphic into `H^(s+2)`. Starting with the proved `L^2`
holomorphy and iterating proves the claimed Sobolev regularity on the same
disk. Sobolev embedding then yields holomorphy in each fixed `C^k` norm.
For the two-square source dimension is `21`, so one can take an integer
Sobolev index greater than `k+21/2`. Near zero, `psi` is uniformly close to
one; the local logarithm is therefore holomorphic. This validates a
`C^k` order-three log remainder on a smaller, graph-dependent disk.

The source does **not** calculate that smaller disk or its `C^k` remainder
constant. Consequently this regularity argument proves local existence and
the exact log coefficients; it does not certify a numerical conditional
influence estimate on the whole interval of the `L^2` tail. Any separate
actual-vacuum separating witness must supply its own additional bounds.
That adjacent witness is outside the present review.

## 5. Connected and edge-disjoint supports

For an edge-disjoint pair, no source edge derivative differentiates both
half traces. The product rule therefore gives
`T0(a_p a_q)=12a_p a_q`. The coefficient equation has forcing
`a_p a_q/3`, so its contribution to `u2` is `a_p a_q/36`. Twice that term
is `a_p a_q/18`, exactly the unordered-pair cross term in `u1^2`.
It cancels in `2u2-u1^2`.

For an adjacent pair, the locally derived inverse instead gives
`a_p a_q/39+w_pq/351`. Subtracting the same `u1^2` cross term leaves
`(4w_pq-3a_p a_q)/702`. The outer-loop word must cancel the shared-edge
traversal as specified in the source contract. The calculation applies
also to a bent adjacent pair in the admitted cubic lattice: their union
has the stipulated six-edge boundary word. Merely sharing a vertex is
edge-disjoint for this differential operation.

Additional source edges do not change these derivative identities for
functions independent of those edges. The exhibited polynomials have the
required global kinetic images and zero means. Uniqueness of the global
mean-zero inverse identifies them with the actual coefficient without an
unsupported assumption that every inverse is local.

For `N` plaquettes, the Haar variances add to `N/4`, giving the stated
`e2=-N/24`, and the scalar density normalization is `N/144` at quadratic
order. This independently checks the constants in (CV13)–(CV15).
The reviewed version explicitly admits `N>=1`; it excludes the empty-set
case before writing `3/N`.

The free-gap and bounded-potential estimates now give only the shrinking
disk `|r|<3/N`. This does not establish an all-order connected expansion
with a graph-uniform convergence radius. Later orders may connect two
plaquettes through intermediate ones even when their direct order-two
term vanishes. The source retains this boundary.

## 6. Established inputs, checked synthesis and remaining ports

The Kato citation is a standard reference for the resolvent/Riesz-projection
method. The publisher's page confirms the work and its analytic-perturbation
chapter but does not expose the cited theorem text. This review therefore
does not claim to have independently checked all of Kato Chapter VII from
that page. The numerical radius and inverse estimates were reviewed directly
from the source's displayed Neumann argument. [Publisher record](https://link.springer.com/book/10.1007/978-3-642-66282-9).

The author's accessible Taylor notes state the Sobolev mapping property in
I.3, equation (3.31), elliptic regularity in I.4, equations (4.6)–(4.9), and
the passage to compact manifolds in I.8. Those established ingredients
support the source-space bootstrap above. They are not new YM theorems or
finite-checker outputs. [Taylor's notes](https://mtaylor.web.unc.edu/wp-content/uploads/sites/16915/2022/05/psidolect.pdf).

The evidence grades remain separate:

- **Accepted source premises:** the infinite-dimensional physical operator,
  domain, kinetic gap, Haar quotient, cometric and positive ground state.
- **Reviewed written synthesis:** explicit analytic disk and actual `L^2`
  tail; coefficient and normalization identities; source-space log
  regularity; order-two connected cancellation on the specified graph class.
- **Not independently verified here:** the author's executable receipt,
  the separate actual-vacuum witness, or any previously accepted checker.
- **OPEN:** useful graph-uniform log-response constants, all-order connected
  summability, the required variance estimate, physical scaling and the
  continuum quantum theory/gap.

## 7. Byte and retrieval receipt

The first inspected draft of CONNECTED_VACUUM.md had SHA-256
`391a857ba750eeae07fcc7a12d53bf0aa6f6b4c442cfa1a136aa578b80dcbffb`
at `2026-09-12T18:38:51.3794934Z`. The explicit `N>=1` admission was then
confirmed at `2026-09-12T18:40:29.5189742Z` in version
`4ecd426f8d25c942d73b310d90bd5df469b931636d26ae8cf19ae4b738baf652`.
This was a clarification to the declared carrier, not a correction of the
nonempty-graph coefficients. The subsequent packet-portability changes
pointed source links to bundled copies, renamed the pair coefficient to
`C_pair`, and documented read-only verification. These do not change the
reviewed mathematical argument. The bundled bridge bytes match the original
bridge inspected at `2026-09-12T18:40:29.6005995Z`.

| File | Reviewed retrieval UTC | SHA-256 |
|---|---|---|
| `CONNECTED_VACUUM.md` | `2026-09-12T18:43:03.0895230Z` | `9923cf495cb7b90d041569afd28805f7f9ac3b9c14100d0e6ff2173c4333c7ab` |
| `accepted_sources/ym2_global_phase_joint/GAP_BRIDGE.md` | `2026-09-12T18:43:23.0175993Z` | `68e619f6e56b752e59609d52a9e2c5674a0ef47c1bdb8c9d06a3b6188d071a28` |

The linked primary reference pages were read on 12 September 2026 during
this review. No external document bytes were downloaded into the repository.
Hashes identify source bytes and do not establish their mathematical truth.
