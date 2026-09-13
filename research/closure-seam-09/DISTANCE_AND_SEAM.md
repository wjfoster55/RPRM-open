# Distance, pairing and the relation neither side fixes alone

Evidence: elementary written deductions, primary-source height theory and fresh exact rational interval computation. This instantiates the user's relational-seam proposal in a finite matching carrier and in the established arithmetic height geometry. It does not identify an additional unproved BSD factor by naming a new object.

## 1. What the seam could supply

Suppose two observations L(h),R(h) come from the same admitted source h, and the question is Q(h). A seam datum is needed by those observations exactly when two compatible sources can have the same retained pair `(L,R)` but different Q. Then no decoder of that retained pair alone can give the correct answer for both. Conversely, if Q is constant on every reached complete fiber, it is determined by the pair.

Not being determined by either side separately is a weaker condition. For example, two full point coordinates in a fixed metric frame together determine their distance. If only their lengths remain, relative alignment can be missing. If unpaired occurrence lists remain, matching can be missing. If each point uses a different coordinate frame, the map relating the frames can be missing. If no metric is supplied, the distance law itself is missing. These are distinct contracts.

The [finite joint-relation proof](agents/JOINT_RELATION.md) fixes both side records to `(0,1)` with named occurrences. Identity matching gives total squared pair distance zero; swapped matching gives two. The complete fiber consists of exactly those two matchings. One binary distinction is necessary and sufficient for this readout. Equal coordinate values remain distinct occurrences. A different receiver, such as minimum over matchings, has a different answer and does not ask for the actual matching.

The general expansion is

\[
\sum_i(x_i-y_{\pi(i)})^2
=\sum_i x_i^2+\sum_j y_j^2-2\sum_i x_i y_{\pi(i)}.
\tag{1}
\]

The last cross term can change while the individual records stay fixed. It is relational information. It is not necessarily a new independent variable if the full matching is already supplied.

## 2. The actual arithmetic metric and its normalization

Retain the previous curve `E: y^2=x^3-1156x` and the full logarithmic canonical height

\[
H(P)=\lim_{k\to\infty}4^{-k}\log H_x(2^kP).
\]

The established height theorem makes H a nonnegative quadratic form, zero precisely on torsion. It induces a positive-definite inner product on the finite-dimensional real vector space obtained from `E(Q)/torsion`. Our pairing convention is

\[
\beta(P,Q)=\tfrac12\bigl(H(P+Q)-H(P)-H(Q)\bigr).
\tag{2}
\]

This gives `beta(P,P)=H(P)`. The convention matches the existing E34 calculation. Milne's notation for the unhalved polarization differs by two; that factor is explicitly adapted in the [geometry audit](agents/GEOMETRY.md). The quadratic-height facts and their conditions are the published dependency, not conclusions inferred from our decimal enclosures. [Milne, IV §§4 and 6](https://www.jmilne.org/math/Books/ectext6.pdf), [Cremona, §3.4](https://johncremona.github.io/book/fulltext/chapter3.pdf)

Write `p=H(P)`, `q=H(Q)`, `s=H(P+Q)`, and

\[
D=H(P-Q).
\]

D is **squared arithmetic distance**. The actual metric distance is `sqrt(D)`, on rational points modulo torsion. On the original point group it is only a pseudometric, because points differing by torsion have distance zero. This is not Euclidean distance between plotted x,y coordinates.

The parallelogram law gives

\[
s+D=2p+2q,\qquad
\boxed{\beta=\frac{p+q-D}{2}.}\tag{3}
\]

Thus two separate lengths leave their alignment open, while the squared distance determines the pairing once those lengths are known. For the established integral basis, the regulator is

\[
\boxed{\mathcal R=pq-\beta^2
=pq-\frac{(p+q-D)^2}{4}.}\tag{4}
\]

The metric parallelogram spanned by P,Q has area `sqrt(R)`; R is its area squared. This is a useful joint object for the user's coin analogy, at a specified arithmetic receiver. The usual vector-space area interpretation does not make a new physical surface or a new arithmetic theorem.

## 3. What is and is not determined by the sides

For fixed real `p,q>=0`, all positive-semidefinite two-by-two Gram matrices

\[
G=\begin{pmatrix}p&\beta\\\beta&q\end{pmatrix}
\]

are parametrized by `-sqrt(pq)<=beta<=sqrt(pq)`. Equivalently,

\[
(\sqrt p-\sqrt q)^2\le D\le(\sqrt p+\sqrt q)^2.
\tag{5}
\]

Necessity is the determinant condition and (3). Sufficiency follows, for p>0, by choosing vectors `(sqrt(p),0)` and `(beta/sqrt(p),sqrt(q-beta^2/p))`; the p=0 case forces beta=0 and is handled directly. This is the **complete real Gram relaxation**, not a claim that every such value occurs among rational points on the fixed elliptic curve. That lattice has additional constraints.

For fixed p,q and regulator r with `0<=r<=pq`, the Gram relaxation instead leaves

\[
\beta=\pm\sqrt{pq-r},\qquad
D=p+q\mp2\sqrt{pq-r}.
\tag{6}
\]

The branches coincide at r=pq. Therefore a regulator receiver only needs beta squared, while an oriented-pairing or distance receiver may need its sign. We should not retain or demand an extra distinction without checking which question it serves.

Degeneracy is also precise. D=0 means P and Q agree modulo torsion. R=0 means their images are linearly dependent; it need not mean D=0. For example, vectors of lengths two and one in the same direction have D=1 and R=0. Positive separation does not by itself establish two independent directions.

## 4. Fresh source-generated E34 calculation

Use the actual points `P=(-2,48)`, `Q=(-16,120)`. Subtract Q by adding its group inverse. The chord slope is 12, giving

\[
P-Q=(162,-2016),\qquad (-2016)^2=162^3-1156\cdot162=4064256.
\]

The rational group calculation also checks `(P-Q)+Q=P`. The source computes P+Q independently, rather than importing a saved height. Eight exact projective doublings of each point give the following outward intervals in the fixed full-height convention:

| Quantity | Certified interval |
|---|---|
| H(P) | `[2.5128778330, 2.5130283810]` |
| H(Q) | `[3.0185865641, 3.0187371120]` |
| H(P+Q) | `[6.9259970420, 6.9261475899]` |
| H(P-Q), squared distance | `[4.1371018983, 4.1372524462]` |
| sqrt(H(P-Q)), distance | `[2.0339867006, 2.0340237084]` |
| beta, using the two proved polarization forms | `[0.6971157745, 0.6973317973]` |
| regulator | `[7.0990676287, 7.1002016338]` |
| parallelogram area | `[2.6644075568, 2.6646203546]` |

These are fresh arithmetic enclosures. No analytic L-value, five-adic coefficient, saved PASS file, expected BSD ratio or database rank generated them. In particular the numerical value of the distance is not being selected as a safe digit or a carry threshold.

The source also encloses zero for O and all three two-torsion points. Their exact zero canonical heights follow from the torsion theorem and projective duplication; a small interval alone would not prove exact zero. Early doublings are checked independently by the rational chord law. Every projective update retains the removed gcd and verifies the bounds described below.

## 5. Why the interval is rigorous

For primitive x-coordinates `(a:b)`, write

\[
F=(a^2+1156b^2)^2,\quad G=4ab(a^2-1156b^2),\quad g=\gcd(F,G).
\]

The earlier written all-point bound gives `g|C0=5345344` and
`1<=max(F,|G|)/H_x^4<=C1=1338649`, with projective/torsion exceptions included. Therefore after depth k,

\[
-\frac{\log C0}{3\cdot4^k}
\le H(P)-4^{-k}\log H_x(2^kP)
\le\frac{\log C1}{3\cdot4^k}.
\tag{7}
\]

The constant and proof are an explicit dependency of [the prior height-series note](../bsd-identity-01/EXPLICIT_IDENTITY_TARGET.md). Fresh checks of finitely many gcds do not establish that uniform theorem.

For a positive integer h, write `h=2^e r` with `e=bit_length(h)-1`, so `1<=r<2`. If e>96, the retained top bits give

`floor(r*2^96)/2^96 <= r < (floor(r*2^96)+1)/2^96`.

For e<=96, r is retained exactly. For either endpoint t in `[1,2]`, set `z=(t-1)/(t+1)`, so `0<=z<=1/3`. With K=48,

\[
S_K=2\sum_{j=0}^{K-1}\frac{z^{2j+1}}{2j+1},\qquad
S_K\le\log t\le S_K+
\frac{2z^{2K+1}}{(2K+1)(1-z^2)}.
\tag{8}
\]

This follows by integrating the geometric series for `1/(1-z^2)`; the positive remaining terms are bounded by replacing their denominators by `2K+1` and summing the geometric powers. It covers z=0. Monotonicity and `log h=e log 2+log r` produce a rational enclosure. Both correction constants in (7) use upper logarithm endpoints in the outward direction. All subsequent interval additions, products, squares and square roots retain rational bounds; decimal endpoints use integer floor/ceiling operations. The full certificate source is [check_distance.py](work/check_distance.py).

The two pairing intervals may be intersected because the height theorem proves their exact values equal. Their overlap is not itself the proof of that theorem. Likewise the parallelogram residual enclosure is a consistency control, not a decimal substitute for an identity.

## 6. A carry criterion must retain its basis and scale

Replacing Q by -Q is a basis reversal. It preserves p,q and R, changes beta to -beta, and swaps D with H(P+Q). In our fresh enclosures, D is below 5 while the reversed distance squared is above 5. Thus the illustrative criterion `D>5` changes its answer under a basis reversal of the same arithmetic lattice. It cannot be an intrinsic closure criterion with that meaning. This tests one precisely stated threshold, not every possible interpretation of a distance-based handoff.

More generally, replace Q by `Q+nP`, an integral change of basis of determinant one. The exact rules are

\[
q_n=q+2n\beta+n^2p,\quad
\beta_n=\beta+np,\quad
\mathcal R_n=\mathcal R,
\]
\[
D_n=q+(n-1)^2p+2(n-1)\beta.\tag{9}
\]

The distance grows without bound as |n| grows for p>0, while the regulator stays fixed. A specified basis-dependent distance remains a valid readout; its basis must be part of the contract. Transporting the lattice regulator instead has the general law

\[
\det(M^TGM)=\det(M)^2\det(G).
\tag{10}
\]

The fresh finite check covers all 625 integer two-by-two matrices with entries -2 through 2, including 104 unimodular ones. The unrestricted identity follows from the determinant product law. Singular matrices are retained and give zero; a nonunit determinant represents an index change rather than the same integral basis.

Rescaling the height convention by lambda>0 scales p,q,beta,D by lambda, distance by sqrt(lambda), and the regulator by lambda squared. This is a mathematical normalization change, not an inferred physical dimensionality. The analytic BSD formula must retain its corresponding convention factors.

## 7. The remaining seam

This pass realizes a precise meaning of the user's proposal: a relational readout can contain information absent from the two individual summaries, and a distance can recover a pairing. In the actual BSD calculation that structure is already supplied by canonical-height geometry. It sharpens how to retain and compare the arithmetic side.

The open target remains the equality between the independently defined analytic leading coefficient and `Omega * regulator * sigma`, followed separately by identifying finite sigma with the actual Sha order. Calling the pairing or area a seam does not produce this equality. A source-derived analytic-to-arithmetic law and its boundary conditions are still required. The useful next candidate must respect (3), (4), basis transport and the previous mixed-refinement obstruction simultaneously.
