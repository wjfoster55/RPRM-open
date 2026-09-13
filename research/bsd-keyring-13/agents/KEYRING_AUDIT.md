# Four-component keyring: independent written audit

Date: 2026-09-12. Evidence grade: **elementary written proof for the explicitly supplied embedding**, using the standard linking-number/intersection theorem. No formal proof or general link-classification result is claimed.

The construction realizes three separate hoops threaded by a fourth hoop. Its union has **four connected components**; its linking-incidence graph is the connected star with three leaves. It supplies a precise model of the clarified shape. The numerical suffixes have not themselves been shown to generate this embedding, and the shape has not been shown to imply a BSD identity.

This clarification changes the model from the two complementary arcs discussed in [experiment12](../../bsd-offset-hook-12/TWO_HALVES.md). That earlier result remains valid for its own two-arc contract; it does not decide the present four-loop proposal.

## Contract

| Item | Declared scope |
|---|---|
| Carrier | Four labelled smooth circles in the bounded region of Euclidean three-space containing the formulas below. Parameters are in the compact circle `ℝ/(2πℤ)`. |
| Equality | Exact equality of spatial points for intersection tests; the four component occurrences keep their identities. Ambient deformation without intersection is a separate equivalence. |
| Supplied ports | Connector `C`, satellites `S0,S1,S2`, the exact constants `R=3,r=3/4`, their formulas, and the role assignment below. |
| Requested readout | Disjointness; number of components; pairwise linking; the connector-incidence graph. |
| Operations | Parameter traversal and label replacement are defined below. No arithmetic operation is inferred from a geometric traversal. |
| Missing ports | A numeric-label-to-geometry law, a value decoder, and any operation that compares the actual analytic and arithmetic BSD objects. |
| Receiver | The fixed labelled arrangement and its pairwise linking data. Exact numerical reconstruction is an additional receiver. |
| Inverse/fiber | Fixed geometry forgets arbitrary annotations. On any supplied complete finite annotation family `Λ`, its complete annotation fiber is `Λ`. No numeric inverse exists when `Λ` contains different requested values. |

The proposed role assignment is `S0 ↔ "2."`, `S1 ↔ "0340"`, `S2 ↔ the joint lower/upper suffix record`, and `C ↔ the fourth connecting/reference role`. The lower and upper suffixes are paired annotations on the third hoop in this model; they are not silently split into two extra components.

Calling the fourth role a “number line” does not yet identify the circle with a linearly ordered number carrier. A traversal parameter on `C` is cyclic. An ordered numerical readout needs its own cut, frame, bounded domain, and decoder; endpoint identification or wrapping must be explicit.

## Exact embedding and disjointness

Write `ez=(0,0,1)`, `θj=2πj/3`, and `ej=(cos θj,sin θj,0)` for `j=0,1,2`. Define

\[
C(t)=(R\cos t,R\sin t,0),\qquad
S_j(u)=(R+r\cos u)e_j+r\sin u\,e_z,
\quad R=3,\quad r=\frac34.
\]

`C` is a circle of radius `R`. Each `Sj` is a circle of radius `r` centered at `qj=R ej`, in the plane spanned by `ej,ez`. In each formula, equal points force equality of both sine and cosine of the parameter, hence equality modulo `2π`; each is an embedded circle. All points lie within the closed ball of radius `R+r=15/4` centered at the origin.

For any point `p=Sj(u)`, its horizontal radius is `R+r cos u>0`. The nearest point of `C` has the same horizontal direction `ej`. Consequently

\[
\operatorname{dist}(S_j(u),C)^2
=(r\cos u)^2+(r\sin u)^2=r^2.
\]

Thus every satellite point is exactly distance `3/4` from the connector, and no satellite meets it. Equivalently, intersection would require `sin u=0`, but the two resulting horizontal radii `R±r` are both different from `R`.

For `j≠k`, `ej·ek=-1/2`, so

\[
\lVert q_j-q_k\rVert=R\sqrt3=3\sqrt3>2r=\frac32.
\]

Every satellite lies on the boundary of its radius-`r` ball centered at `qj`; these three closed balls are pairwise disjoint. The distance between any two satellites is at least `3√3-3/2>0`. These inequalities prove pairwise disjointness of all four circles without relying on a projection or sampled rendering.

## Each satellite threads the connector once

Orient `C` by increasing `t`; its planar spanning disk

\[
D_C=\{(x,y,0):x^2+y^2\le R^2\}
\]

has positive normal `ez`. The standard linking-number theorem computes the oriented linking number as the signed intersections of the other component with a spanning surface. This theorem and its orientation interpretation were checked in [Joan E. Licata, *Beginning Course, Lecture 3*, §2.3, Theorem 3, p.3 (2012)](https://www.math.ias.edu/files/wam/LicataLecture3.pdf).

For `Sj`, the only points in the plane `z=0` occur at `u=0,π`. At `u=0`, its horizontal radius is `R+r>R`, outside `DC`. At `u=π`, the point is `(R-r)ej`, strictly inside `DC`. The latter crossing is transverse because

\[
\frac{d}{du}(S_j(u)\cdot e_z)\bigg|_{u=\pi}=-r\ne0.
\]

There is therefore exactly one interior crossing, of negative sign under the increasing-`u` orientation:

\[
\operatorname{lk}(C,S_j)=-1,\qquad
|\operatorname{lk}(C,S_j)|=1.
\]

Reversing the satellite orientation changes the sign to `+1`; the unoriented statement “threaded once” is unchanged. This establishes nontrivial pairwise linking in this model. It does not infer a sign from the numeral labels.

The same threading can be seen directly from the satellite's spanning disk

\[
D_j=\{q_j+a e_j+b e_z:a^2+b^2\le r^2\}.
\]

`C` meets the plane of `Dj` only at `qj` and `-qj`. The first is the center of `Dj`; the second is distance `2R=6>r` from that center. Thus `C` crosses each hoop's disk precisely once. A disk crossing is not an intersection of the wire boundaries.

## The satellites form an unlink, while the whole arrangement is linked

Each disk `Dj` lies in its satellite's radius-`r` ball. If strict interior containment is desired, use balls of radius `1`: they still remain pairwise disjoint because `2<3√3`. Each satellite is a round unknot inside its own ball, and the three disjoint balls separate them. Hence the satellite-only three-component sublink is an unlink, a stronger conclusion than merely having three zero pairwise linking numbers.

In particular, `lk(Sj,Sk)=0` for `j≠k`. For arbitrary links, zero pairwise linking numbers alone do not establish unlinking; here the disjoint balls and disks supply that additional proof.

With order `(C,S0,S1,S2)`, the absolute pairwise linking matrix is

\[
\begin{pmatrix}
0&1&1&1\\
1&0&0&0\\
1&0&0&0\\
1&0&0&0
\end{pmatrix}.
\]

The associated graph has four vertices and the three edges `C—Sj`. It is connected. The actual union of the four wires has four connected components, because the circles are connected, mutually disjoint, and separated by positive distances. “One connected linkage” is therefore a statement about this relation graph, not a claim that the material is one continuous circle. No continuous path lying only in the four wires can switch from one component to another.

## What persists when a suffix changes

Let `Λ` be any explicitly supplied finite family of joint label records, and let `G` be this fixed labelled geometric embedding. A decorated source state is `(G,λ)`. The shape-only representation is

\[
\pi(G,\lambda)=G.
\]

For this carrier, `π⁻¹(G)={(G,λ):λ∈Λ}` is the complete fiber. Every component count, pairwise linking number, and incidence-graph question above is constant on the fiber. A numerical question that differs between two records is not constant and cannot be recovered from `G` alone. For example, substituting a different same-width suffix annotation changes no point of any curve. If the exact annotation is also retained, a declared positional decoder can read it; that is a stronger representation.

The depth-9 and depth-10 enclosures in [experiment12's readout](../../bsd-offset-hook-12/README.md) provide a relevant kind of label update: lower and upper endpoint suffixes change while the proposed role assignment can remain intact. Assigning both stages to `G` proves the stability of the chosen geometric representation under that assignment. It does not prove that the topology generated the new digits or selected the enclosed height value.

If suffixes are intended to move seams, alter radii, change embeddings, or trigger an operation, the rule must be supplied. Then preservation becomes a check on that rule. Keeping a joint lower/upper annotation also does not authorize replacing its actual compatibility relation by the Cartesian product of two independent suffix sets.

## The additional operation required for BSD

The two endpoint suffixes concern bounds for one arithmetic quantity. They do not by themselves name BSD's analytic and arithmetic sides. The previous lane states its fixed-normalization target and outstanding comparison in [its BSD section](../../bsd-offset-hook-12/TWO_HALVES.md#what-remains-for-bsd); this audit supplies no new value for that target.

A useful next bridge would name source states `XA` and `XB` for the actual analytic and arithmetic objects, a correspondence `f:XA→XB`, their scalar readouts `qA,qB`, and then prove

\[
q_A(x)=q_B(f(x))
\]

on the covered domain for the same curve and normalization. If operations are claimed, each operation must have matching enabledness and a commuting successor rule. If a return operation `g` is offered, `g(f(x))=x` must be proved on its admitted domain, while the readout equation remains a separate obligation.

Even a perfectly closed operational loop does not force arbitrary readouts to agree: on the finite carrier `X={1,2}`, take `f=g=id`, `qA(x)=x`, and `qB(x)=2x`. Every loop closes, but the two readouts disagree at every state. The four-hoop shape alone cannot exclude this hostile case because it supplies none of those readout laws.

## Coverage boundary and disposition

The proofs above cover exactly the supplied embedding and role assignment. They remain algebraic arguments rather than claims inferred from visual similarity or finite samples. Relevant hostile cases are explicit:

- Collapsing `r` to zero destroys the satellite circles and is outside the admitted embedding carrier.
- Replacing each center `3ej` by `4ej` while keeping `r=3/4` gives four separate circles with no satellite crossing the connector disk: the smallest satellite horizontal radius becomes `13/4>3`. Hoop counts alone therefore do not force threading.
- Joining or welding the components changes the carrier and component count; it is not an allowed deformation of this disjoint link.
- Refreshing numeric suffixes while leaving all formulas fixed changes labels without changing linking; shape alone cannot determine that numerical update.

The geometric readout is completely determined: four disjoint components, three unit-magnitude connector links, and a satellite unlink. Recovery of arbitrary suffix values from the bare shape fails on the stated multi-value annotation fiber. A law deriving the embedding from the user's numerical records, and an operational comparison that closes the actual BSD target, remain **OPEN**. Neither openness is a refutation of the clarified shape proposal.
