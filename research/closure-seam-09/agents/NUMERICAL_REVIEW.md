# Independent review of Seam 09 distance enclosures

Date: 2026-09-12 America/Denver. Reviewed
[check_distance.py](../work/check_distance.py) and
[distance.json](../evidence/distance.json). The source SHA-256
`d1ab3943932a25bd8bce023eebb405d138957c339e5c9640640e6490d4ab7cf0`
matched the receipt at review time. This is source inspection and a written
rounding argument, not a second execution of the height campaign or a
formal proof of the Python runtime.

**Finding:** the stated canonical-height, distance, pairing, regulator,
and transported-basis intervals have valid outward enclosure logic under
the attributed uniform height-tail theorem. No numerical defect requiring
a rerun was found.

## Logarithm and canonical tail

For `ln_small(r)`, \(1\le r\le2\) gives
\(z=(r-1)/(r+1)\in[0,1/3]\). The first T terms of
\(\log r=2\sum_{j\ge0}z^{2j+1}/(2j+1)\) form a lower bound. After the
loop, `term` is \(z^{2T+1}\), and the remaining positive series is at most

\[
\frac{2z^{2T+1}}{(2T+1)(1-z^2)}.
\]

The code adds exactly this bound. It covers r=1 with zero remainder and
r=2 without a boundary exception.

For positive integer h, \(e=\lfloor\log_2h\rfloor\) is obtained exactly
from bit length. When the mantissa is truncated, its floor m gives
\(m/2^{96}\le h/2^e<(m+1)/2^{96}\). Both endpoints remain in [1,2].
Monotonicity of log and the positive integer e justify summing the lower
mantissa/LN2 endpoints and the upper endpoints. No floating point is used.

The inherited tail is
\(-\log C_0/(3\cdot4^k)\le H-s_k\le\log C_1/(3\cdot4^k)\).
The implementation subtracts an **upper** bound for \(\log C_0\) from the
lower endpoint of \(s_k\), and adds an **upper** bound for \(\log C_1\) to
its upper endpoint. Both directions are correct. Clipping the lower result
at zero uses the stated nonnegativity theorem. The finite checks on sampled
gcds and raw heights corroborate source calculations; they do not replace
the inherited all-future tail theorem.

## Interval operations and display

Addition, subtraction, signed scaling, and the four endpoint products
enclose their corresponding operations. `square` correctly treats an
interval crossing zero separately. The two pairing intervals enclose the
same B by the established polarization identities, so intersecting them
is valid even though their inputs share p and q. Subsequent interval
arithmetic allows a larger independent box and remains conservative.

For a nonnegative rational x and decimal unit U, the identity
\(\lfloor\sqrt{\lfloor xU^2\rfloor}\rfloor
=\lfloor U\sqrt x\rfloor\) justifies the integer-square-root lower
endpoint. The upper endpoint is incremented exactly when its square is
too small, giving a ceiling. `decimal_interval` uses integer floor for the
lower endpoint and integer ceiling for the upper, including negative
inputs. Its conversion of an already outward-rounded square-root interval
does not narrow that interval.

## Basis and exceptional controls

The 625 integer-matrix checks, including 104 unimodular matrices, are exact
tests in one declared rational Gram model. Their general justification is
the written identity \(\det(M^{\mathsf T}GM)=\det(M)^2\det G\), not finite
enumeration. The E34 shear intervals use the correct transported quadratic
and bilinear forms. Repeated occurrences enlarge their widths but do not
invalidate them; for example the n=1 difference is exactly -Q and its
canonical height is exactly q.

Projective duplication covers O and all three rational two-torsion points.
The first three duplications per source are cross-checked through the chord
law; the remaining five use the stated projective duplication formula.
The torsion outputs [0, 0.0000717528] are conservative enclosures of exact
zero. Their positive upper endpoint is not positive torsion height.

The receipt's field `arithmetic_seam.area` is \(\sqrt{\mathcal R}\), the
**parallelogram** area. The area of the triangle with vertices 0,P,Q is
half that value. This is a labeling distinction to preserve in explanation,
not an enclosure defect.

## Result and scope

The receipt encloses

| Readout | Certified outward decimal interval |
|---|---|
| \(H(P-Q)\) | [4.1371018983, 4.1372524462] |
| \(\sqrt{H(P-Q)}\) | [2.0339867006, 2.0340237084] |
| B | [0.6971157745, 0.6973317973] |
| \(\mathcal R\) | [7.0990676287, 7.1002016338] |

B is strictly positive, so the orientation test in
[GEOMETRY.md](GEOMETRY.md) is decisive for its stated invariance claim.
There is also a concrete fixed-threshold example: at \(\tau=4\), the basis
(P,Q) has difference height above 4, while the unimodularly equivalent
basis (P,Q+P) has difference height q in
[3.0185865641, 3.0187371120], below 4. This rejects that threshold as a
basis-independent event; it permits a statistic with a declared basis.

The parallelogram residual interval contains zero, as expected from the
height theorem. That overlap is a consistency check. The run computes no
analytic coefficient, Sha order, or exact BSD identity, and this review
does not promote interval overlap to such a result.
