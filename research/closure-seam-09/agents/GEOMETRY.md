# Seam 09: canonical-height distance and the two orientation branches

Date: 2026-09-12 America/Denver. This bounded audit adds this file only.
Evidence consists of attributed height theorems, written deductions below,
and a fresh exact rational group calculation. It does not rerun an earlier
campaign or supply a new analytic precision calculation.

The proposed distance has an exact arithmetic realization. If the seam
retains the two individual heights and the height of the difference point,
it retains the entire two-point Gram matrix. The resulting determinant is
the existing regulator readout. This gives a concrete geometry for the
joint port identified in [Bridge 08](../../closure-bridge-08/agents/BSD_SEAM.md).
An identity connecting that arithmetic determinant to the analytic leading
coefficient remains a separate missing law.

## 1. Contract and normalization

The arithmetic carrier is the fixed elliptic curve

\[
E/\mathbb Q:\quad y^2=x^3-1156x,
\qquad P=(-2,48),\quad Q=(-16,120).
\]

Equality in this source carrier is equality of rational projective points.
The metric receiver passes to the quotient
\(L=E(\mathbb Q)/E(\mathbb Q)_{\mathrm{tors}}\); this quotient intentionally
forgets which torsion translate supplied a class. The Euclidean carrier is
\(V=L\otimes_{\mathbb Z}\mathbb R\). Equal metric classes do not identify
distinct source-point occurrences.

Use natural logarithms and the **full** canonical x-height

\[
H(R)=\lim_{n\to\infty}4^{-n}\log H_x(2^nR),\qquad
\langle U,V\rangle=\frac{H(U+V)-H(U)-H(V)}2.
\tag{1}
\]

Here \(H_x\) denotes multiplicative primitive x-height, whereas \(H\)
denotes its canonical logarithmic limit. The pairing has diagonal
\(\langle R,R\rangle=H(R)\). This is the convention of
[Cremona, §3.4, printed pp. 71–72](https://johncremona.github.io/book/fulltext/chapter3.pdf#page=10).
[Milne, IV §4 and §6](https://www.jmilne.org/math/Books/ectext6.pdf#page=129)
supplies the canonical-limit, quadraticity, torsion, and real-positivity
theorems. Milne names the *unhalved* polarization his pairing; his pairing
is twice (1), and positivity survives this positive factor.

The operations used here are rational point addition/subtraction, followed
by the height readout, and algebraic changes among the real Gram coordinates.
Point subtraction is enabled for all projective source points, including
the identity and torsion exceptions. No rational halving is assumed.

The supplied ports are \(E,P,Q\) and the height convention. For the geometry
apertures below, the ports are explicitly either \((p,q,D)\) or
\((p,q,\mathcal R)\). The receiver asks for the pairing, determinant, or
orientation branches; it does not recover an arbitrary rational point
from a real height value. The inherited source note supplies the rank and
integral-basis status of \(P,Q\); this audit does not re-prove those facts.

## 2. The exact difference point

Subtracting Q adds \(-Q=(-16,-120)\). The chord slope is

\[
m=\frac{-120-48}{-16-(-2)}=12,
\quad x(P-Q)=12^2-(-2)-(-16)=162,
\]
\[
y(P-Q)=12(-2-162)-48=-2016.
\]

Thus

\[
\boxed{P-Q=(162,-2016).}
\tag{2}
\]

Both sides of its curve equation equal \(4\,064\,256\). A fresh Python
`fractions.Fraction` chord-law calculation also checked

\[
(P-Q)+Q=P,\qquad (P-Q)-P=-Q,
\quad P+Q=(2178/49,65472/343).
\]

This is an independently generated arithmetic source point for measuring
the difference height. The number 162 is its x-coordinate; it is neither
the canonical height nor the metric distance.

## 3. The distance law and regulator

Write

\[
p=H(P),\quad q=H(Q),\quad B=\langle P,Q\rangle,
\quad s=H(P+Q),\quad D=H(P-Q).
\]

Bilinearity and the parallelogram identity give

\[
s=p+q+2B,\qquad D=p+q-2B,\qquad s+D=2(p+q),
\]
\[
\boxed{B=\frac{p+q-D}{2}},\qquad
\boxed{\mathcal R=pq-\frac{(p+q-D)^2}{4}}.
\tag{3}
\]

For fixed \(p,q\), changing from s to D is an exact involution
\(D=2(p+q)-s\); neither description adds an independent theorem. Measuring
the actual difference point can nevertheless provide a separate numerical
consistency check on computations of the sum-point height.

The **metric distance** is
\(d(P,Q)=\sqrt{H(P-Q)}=\sqrt D\). The quantity D is squared distance.
The square root is a translation-invariant pseudometric on source points
and a metric on L. D itself fails the triangle inequality: for a nontorsion
T, \(D(O,2T)=4H(T)>H(T)+H(T)=D(O,T)+D(T,2T)\).

In V, the triangle with vertices \(0,P,Q\) has side lengths
\(\sqrt p,\sqrt q,\sqrt D\). Its area is \(\sqrt{\mathcal R}/2\).
The regulator is the squared area of the corresponding parallelogram,
provided the chosen points form the inherited integral basis.

The geometry uses all three sides. Squared distance D alone cannot decode
the determinant: in the abstract Gram carrier, \((p,q,D)=(1,1,2)\) gives
\(\mathcal R=1\), while \((2,2,2)\) gives \(\mathcal R=3\). These are
explicit Euclidean witnesses, not claimed realizations by E34 rational
points.

## 4. Complete Gram fibers and the two sides

Fix real \(p,q\ge0\). The complete positive-semidefinite Gram family is

\[
G_B=\begin{pmatrix}p&B\\B&q\end{pmatrix},\qquad
-\sqrt{pq}\le B\le\sqrt{pq}.
\tag{4}
\]

Equivalently its full squared-distance interval is

\[
\boxed{(\sqrt p-\sqrt q)^2\le D\le(\sqrt p+\sqrt q)^2.}
\tag{5}
\]

Necessity follows from \(\det G_B\ge0\). For sufficiency when \(p>0\),
the vectors
\((\sqrt p,0)\) and \((B/\sqrt p,\sqrt{q-B^2/p})\) realize every matrix
in (4) in \(\mathbb R^2\). If \(p=0\), positivity forces \(B=0,D=q\);
use vectors 0 and \((\sqrt q,0)\). The case \(q=0\) is symmetric.
Negative p or q is an admission error for squared-norm ports.

These constructions prove coverage of the **abstract Gram carrier**.
They do not prove that every real matrix in (4) is realized by rational
points of a fixed elliptic curve. On the fixed Mordell–Weil lattice,
bounded height admits finitely many rational points, hence fixed p,q admit
only finitely many ordered source pairs. Their arithmetic realization fiber
requires the lattice and point constraints. It is not replaced by the
continuous interval (5). For already fixed P,Q, their exact height data
determine one actual Gram matrix, even while numerical evaluation is open.

At fixed p,q, the determinant has the factored form

\[
\mathcal R=\frac14
\left((\sqrt p+\sqrt q)^2-D\right)
\left(D-(\sqrt p-\sqrt q)^2\right).
\tag{6}
\]

Now supply a candidate determinant r as the missing-port aperture.
Within the abstract Gram carrier, its complete fiber is empty when
\(r<0\) or \(r>pq\). When \(0\le r\le pq\), it is precisely

\[
\boxed{B=\pm\sqrt{pq-r},\qquad
D=p+q\mp2\sqrt{pq-r}.}
\tag{7}
\]

At \(r=pq\) the branches coincide: ONE with \(B=0,D=p+q\).
For \(0\le r<pq\) there are exactly two Gram completions: MANY of the
two displayed branches. Equation (7) records the correlation between sign
and distance; their independent Cartesian product would add false rows.
For \(p=q=0\), and more generally \(pq=0,r=0\), only the coincident branch
remains.

This supplies a precise interpretation of “two sides of the coin”: the
determinant forgets the sign of the cross-pairing. Replacing Q with -Q
exchanges those signs and exchanges D with s while preserving p,q and
\(\mathcal R\). It does not assert two separately measured physical objects
or an analytic/arithmetic duality.

The determinant is largest at the center \(D=p+q\), where the vectors are
orthogonal. Its derivative with respect to D at fixed p,q is B. Therefore
moving the points closer does not have one global monotone effect on the
regulator: the two sides of the center have opposite derivative signs.

## 5. Degeneracy and retained source distinctions

\(D=0\) means \(P-Q\) is torsion. It means equality in L, not necessarily
equality of rational points. Distinct torsion points already give a hostile
case to a claimed metric on all of \(E(\mathbb Q)\).

For \(p,q>0\), the endpoint values in (5) give \(\mathcal R=0\): the two
vectors are collinear, with equal or opposite direction. On the rational
Mordell–Weil lattice, this means some nonzero integer combination of P,Q is
torsion. It does not require either P or Q to be torsion. For example Q=2P
has \(q=4p,B=2p,D=p\), positive separation and zero determinant.

If \(P=Q\) is nontorsion, then \(D=0,s=4p,B=p\). If \(Q=-P\), then
\(D=4p,s=0,B=-p\). Both have zero determinant. Adding arbitrary torsion to
either input changes the source occurrence but leaves all these height
readouts unchanged. The inherited independence of the actual E34 basis
puts its Gram matrix strictly inside the nondegenerate region.

Finite asynchronous naive-height approximants from Bridge 08 need not be
positive-semidefinite and need not obey (5). The metric and Gram statements
apply to canonical limits, or to certified enclosures that establish their
properties. A failed Gram inequality for a coarse approximant alone does
not refute the canonical source.

## 6. Orientation, basis, and coordinate scales

Swapping P,Q preserves B and D. Negating both preserves B and D. Negating
only Q changes \(B\mapsto-B\) and \(D\mapsto2(p+q)-D\), preserving the
determinant. These operations must retain which source port was changed.

With the basis-column convention, a generator change by an integer matrix
M gives \(G'=M^{\mathsf T}GM\), hence

\[
\det G'=(\det M)^2\det G.
\tag{8}
\]

Unimodular M preserves the regulator. An index-d sublattice has determinant
\(d^2\mathcal R\). A dependent pair has determinant zero and is not a basis.
Individual heights and pair distances need not survive a unimodular change.
For the explicit shear \((P,Q)\mapsto(P,Q+kP)\),

\[
D_k=H((1-k)P-Q)=(1-k)^2p+q-2(1-k)B.
\tag{9}
\]

All these ordered pairs generate the same free lattice; their regulator is
unchanged. Since \(p>0\), the squared distances are unbounded as \(|k|\)
increases. Each numerical threshold test still uses a finite selected k;
the unbounded statement follows from the displayed quadratic.

A change of height convention \(H'=\lambda H\), \(\lambda>0\), sends
\((p,q,B,D)\) to \(\lambda(p,q,B,D)\), sends d to \(\sqrt\lambda d\), and
sends \(\mathcal R\) to \(\lambda^2\mathcal R\). The half-height convention
has \(\lambda=1/2\), so its rank-two determinant is one quarter. Using
\(\log_b\), \(b>1\), instead of \(\log\) has \(\lambda=1/\log b\).
A dimensional numerical threshold needs the corresponding conversion.

This differs from changing Weierstrass coordinates. For nonzero rational u,
\((X,Y)=(u^2x,u^3y)\) gives the isomorphic equation
\(Y^2=X^3-1156u^4X\). The raw affine plot stretches its axes differently.
For u=2, the displayed P,Q become \((-8,384),(-64,960)\); this visibly
changes affine coordinate distances. The canonical height stays unchanged:
the x-coordinate change alters naive logarithmic height by a uniform
bounded amount, and multiplication by \(4^{-n}\) removes that difference
in the canonical limit. This also follows from
[Milne, IV Proposition 4.1](https://www.jmilne.org/math/Books/ectext6.pdf#page=126)
applied to the degree-one x-coordinate map.

The differential must be transported separately:
\(dX/(2Y)=u^{-1}dx/(2y)\). The integral of its absolute value scales by
\(|u|^{-1}\). Returning to the chosen minimal differential, and retaining
the convention of integrating over both real components, is essential
before comparing to the analytic coefficient. Model-coordinate scaling
does not authorize an unrecorded height or period factor.

## 7. A precise falsifier for a universal distance carry

No numerical carry threshold is inferred from the picture. A testable
candidate must name the carrier, ordered source ports, event C, threshold
and equality convention, enabled update, and transformation behavior.
For example, freeze

\[
C_\tau(P,Q)=\mathbf 1\{H(P-Q)>\tau\}.
\tag{10}
\]

If C is claimed to be a property of the elliptic curve or free lattice
independent of its chosen integral basis, the following is a direct
falsifier. For any specified \(\tau>q\), compare the basis
\((P,Q+P)\), whose difference height is q, with
\((P,Q+kP)\), choosing a finite k for which a certified lower bound from
(9) exceeds \(\tau\). The first candidate output is 0 and the second is 1,
but the source lattice and regulator are unchanged. No Sha computation or
analytic coefficient is needed for this contradiction.

There is an even smaller orientation test for a centered threshold:
if \(B\ne0\), the bases \((P,Q)\) and \((P,-Q)\) have equal p,q and
regulator, while their D values lie strictly on opposite sides of p+q.
Thus \(\mathbf 1\{D>p+q\}\), or equivalently
\(\mathbf 1\{D/(p+q)>1\}\), measures a selected orientation branch and
cannot be a basis-orientation-independent event. A certified interval
excluding zero for B makes this a finite E34 test.

For a *fixed* threshold lying below every attained nonzero lattice
distance, (10) may simply be constant; the shear argument does not pretend
to refute that case. A threshold tied to a declared oriented basis can also
be a valid statistic. Its mathematical role then includes that basis, and
a law relating its update to the requested BSD readout remains to be
provided. Changing the threshold together with its units is a valid
adapter; changing units while holding a purported universal bare numeral
fixed is not.

## 8. Arithmetic closure and the analytic seam

The identities (3), (6), and (7) are complete algebraic consequences of the
canonical-height pairing in their stated carriers. They sharpen the
meaning of the arithmetic joint port. They also show exactly what the
regulator forgets: an orientation sign at fixed diagonal heights.

The missing analytic/arithmetic bridge remains

\[
c_2^{\mathrm{an}}
=\Omega\sigma\left[pq-\frac{(p+q-D)^2}{4}\right].
\tag{11}
\]

Neither polarization nor the change s↔D proves (11), because both are
internal arithmetic identities and introduce no constraint on
\(c_2^{\mathrm{an}}\). Bridge 08's matching-edge condition and its required
initial/terminal compatibility still apply after this coordinate change.
Fresh interval comparisons can reject a candidate equality or certify
finite consistency; intervals containing zero at finite precision do not
prove exact equality. Identifying a positive candidate integer sigma with
the finite cohomological Sha order is a further separate obligation.

**Closed:** the distance/pairing/determinant identities; complete abstract
Gram fibers; the two orientation branches; the declared transformation
laws; the exact source-point calculation (2); and the conditional threshold
falsifiers for the precisely stated invariance claims.

**Open:** a source-derived law connecting this arithmetic geometry to the
analytic coefficient with the required boundary conditions, its unbounded
continuation, and total Sha identification. The source-point computation
is a finite test, not a general group-law or height-theory formal proof.

## 9. Exact arithmetic replay

The fresh check used Python's standard-library rational arithmetic. The
following code is sufficient to replay its exact point assertions; run it
through `python -I -B -` from the repository root. No old campaign is invoked.

```python
from fractions import Fraction as F
A = -1156
P, Q = (F(-2), F(48)), (F(-16), F(120))

def neg(T):
    return None if T is None else (T[0], -T[1])

def add(U, V):
    if U is None:
        return V
    if V is None:
        return U
    x, y = U
    u, v = V
    if x == u and y == -v:
        return None
    m = (3*x*x + A)/(2*y) if U == V else (v-y)/(u-x)
    z = m*m - x - u
    return z, m*(x-z) - y

def admitted(T):
    return T is None or T[1]**2 == T[0]**3 + A*T[0]

R, S = add(P, neg(Q)), add(P, Q)
assert R == (F(162), F(-2016))
assert S == (F(2178, 49), F(65472, 343))
assert all(admitted(T) for T in (P, Q, R, S))
assert R[1]**2 == R[0]**3 + A*R[0] == 4064256
assert add(R, Q) == P
assert add(R, neg(P)) == neg(Q)
print("PASS: rational admission, subtraction and inverse continuation")
```
