# What the discrepancy measures; what a change of view preserves

This is a bounded clarification of the existing E34 and keyring models.
The letters A and B used for the BSD comparison are not the A/B hoop
labels in the figure. The former are whole numerical readouts; the latter
label the integer and middle blocks of one distance representation.

## The actual numerical discrepancy

For E: y²=x³-1156x, with the previously fixed minimal differential,
full-height regulator and real period over both components, define

\[
A=\frac{L''(E,1)}2,\qquad B_\sigma=\Omega\,\mathcal R\,\sigma,
\qquad D_\sigma=A-B_\sigma.
\]

A is the leading analytic coefficient of the curve's L-function at 1.
The regulator R uses the integral rational-point basis and its height
pairings. Omega is the real period. Sigma is a specified positive integer
candidate for the order of Sha; naming it does not establish that order
or finiteness. The local/Tamagawa and torsion factors cancel for this
curve under the retained conventions.

These definitions are retained from the
[explicit identity target](../bsd-identity-01/EXPLICIT_IDENTITY_TARGET.md).
For sigma=1, the earlier
[two-scale enclosures](../bsd-coefficient-05/TWO_SCALES.md) were

| Readout | Earlier certified enclosure |
|---|---|
| A | [6.38511803, 6.38518585] |
| B1 | [6.384593255, 6.385625424] |

Fresh exact subtraction of those input intervals gives

\[
-0.000507394\le D_1\le0.000592595.
\]

This enclosure includes zero and nonzero values. It does not determine
the sign or prove equality. It is not claimed to be the latest or tightest
possible enclosure: no new L-function or height calculation was run.
Using previously attributed enclosures to explain the quantity is distinct
from accepting an old success flag as proof of an identity.

The two values near 2.034 enclose d=sqrt(H(P-Q)), a different quantity.
Their difference is the width of that distance enclosure. The distance
contributes to the regulator through
R=p*q-(p+q-d²)²/4, where p=H(P), q=H(Q). It is not by itself the whole
arithmetic prediction B1. The symbol D in older height-geometry notes
sometimes denoted d²; this note uses D_sigma exclusively for BSD's defect.

## The viewpoint observation has an exact surviving form

In the supplied keyring, the same connector remains linked to all three
satellites after any rigid rotation. Relative orientation and projected
crossing locations can change; the pairwise linking numbers do not.
In every regular link diagram, the signed crossing sum of the connector
with each satellite is twice their linking number, hence plus or minus 2.
At least two mixed crossings remain for each such pair. The
[standard linking-number definition and surface theorem](https://www.math.ias.edu/files/wam/LicataLecture3.pdf)
support this statement, with the actual circle geometry proved in
[the keyring audit](../bsd-keyring-13/agents/KEYRING_AUDIT.md).

An exactly edge-on view is exceptional as a diagram: viewing along y
maps C(t)=(3 cos t,3 sin t,0) to (3 cos t,0). The circle projects to a
line segment, and t and -t generally have the same image. For example,
(0,3,0) and (0,-3,0) become the same projected point. The source loop
remains closed and linked; the projection loses depth and occurrence
information. Visible uninterrupted tracing can also be hidden by occlusion.

The correct persistent claim concerns the same three-dimensional
connector, including portions hidden in a particular picture.

## Choosing a reference versus changing the linking hub

The absolute linking matrix has degree sequence (3,1,1,1). The connector
is uniquely the component linked to three others; each satellite is linked
only to it. Therefore a rigid rotation cannot swap the topological hub
role with a satellite. Choosing a different hoop as a coordinate reference
is allowed, but is a different operation from changing its physical links.

All 24 component permutations were checked. Exactly six preserve the
linking matrix, and every one fixes the connector while permuting the
three satellites. The degree proof covers why no hub swap can occur.

There is a stronger result for the **specific orthographic construction**.
Its satellite centers are distance 3*sqrt(3) apart, with enclosing-ball
radii 3/4. If two satellite projections overlap, their projected centers
must be at distance at most 3/2. Thus a unit viewing direction v and the
unit center-chord direction u must satisfy |v·u|² >= 11/12.

The two chord axes from any one satellite make 60 degrees. For their
unit representatives u1,u2, |u1·u2|=1/2. The largest eigenvalue of
u1*u1^T+u2*u2^T is 1+|u1·u2|=3/2, so
(v·u1)²+(v·u2)² <= 3/2. Simultaneous overlap with both other satellite
balls would instead require this sum to be at least 11/6, a contradiction.
Therefore a satellite cannot cross both other satellite traces in any
orthographic view of this embedding. In every regular orthographic
diagram, the connector is consequently also the unique trace crossing
all three others. This stronger conclusion uses the actual separation
geometry; the abstract linking matrix alone is insufficient to prove it.

## What this suggests for BSD

The useful candidate is that the analytic and arithmetic calculations
might be rigorously identified as two readouts of one common invariant.
To prove their equality, both readout maps and their preservation law
must be established for the actual curve. The topological invariant of
our drawing has not been identified with that BSD invariant. All labels
in the drawing can still vary without changing its linking matrix.

Thus the viewpoint observation yields a proved geometric invariance
statement at its stated scope. D_sigma=0 and identification of sigma
with the finite Sha order remain OPEN.

Replay the small exact checks with Python 3.10+:

```powershell
python -I -B check.py --output my-checks.json
```

The [fresh checks](checks.json) record interval subtraction, all component
permutations and an exact noninjective edge-on projection. The viewpoint
proof was independently checked by a read-only subagent. No old packet,
other research lane or live task was modified.
