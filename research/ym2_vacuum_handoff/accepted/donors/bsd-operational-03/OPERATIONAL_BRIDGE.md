# Implementing the operational relation on E34

The recovered definition treats an object's operational profile as the
evaluations and relations it already possesses in the stated structure.
An operational state retains enough of that profile for the requested
observations and future operations. This experiment implements such a state
on an actual elliptic-curve carrier, then makes a new arithmetic comparison
vector concrete. It does not assume the desired BSD equality as a rule.

## A shadow with a genuinely missing continuation

On E: Y²=X³−1156X define r(P)=Y/(2X), where finite and nonzero. Let
T0=(0,0). Exactly two point occurrences give each generic shadow:

    P, tau(P)=−P+T0.

The curve equation gives X²−4r²X−1156=0 and Y=2rX. The two roots
are the two occurrences. Both have the same r, and hence the same pair
(r,−r) if a deterministic mirror is appended. That extra mirror does not
separate them. In contrast, doubling gives

    2 tau(P)=−2P,    r(2 tau(P))=−r(2P).

For example,

| Point | Present shadow | Shadow after doubling |
|---|---:|---:|
| P=(−2,48) | −12 | 20447/3480 |
| tau(P)=(578,−13872) | −12 | −20447/3480 |

Thus the present shadow cannot specify its own next value. There is a
precise repair. With r1=r(P) and r2=r(2P), put

    V=(r1^4−289)/(2 r1 r2),
    X=2(V+r1²),  Y=2r1X.                              (1)

The curve equation gives r1²=X/4−289/X and
V=X/4+289/X, hence V²=r1^4+289. Substitution of the duplication
formula gives r2=(r1^4−289)/(2r1V). These identities prove (1)
where its denominators are nonzero. One extra continuation observation
separates the two occurrences and reconstructs the original point.

The single-read formula excludes the four-torsion exceptional locus.
That complement is not doubling-closed over every field: an order-eight
point can leave it. The finite implementation instead uses exactly the4096
points in E[68] whose component at17 is primitive over Z[i]/17. This
carrier is closed under doubling and tau, and never meets the poles or
four-torsion. It has16 possible four-parts and256 primitive seventeen-parts.

The implementation starts from a newly constructed primitive68 seed in the
certified unramified ring (Z/125)[z]/(z^16−2). Each Gaussian coefficient
a+bi modulo68 with a²+b² nonzero modulo17 gives one carrier point.
The executable checks4096 distinct points, all transitions and all4096
inverse evaluations. Partition refinement gives

    present r:                       2048 classes of size2;
    present r plus deterministic −r: 2048 classes of size2;
    present r plus r after doubling:4096 singleton classes.

Singletons are stable under every further admitted operation. The written
inverse explains why this holds; the complete finite census is its fresh
test. The field backend is copied unchanged from the earlier trace source,
but no old trace or PASS record is an input. The new seed and carrier are
constructed afresh.

## What must be preserved for a regulator

Individual canonical height satisfies q(tau(P))=q(P), since sign and
torsion translation preserve it. That equality persists through every pure
doubling continuation. Therefore the stronger two-shadow state is needed
for point recovery and raw-shadow updating; the original shadow already
preserves that height-only observation. This distinction corrects any
overbroad assertion that the first shadow loses every height question.

The regulator also uses mixed relations. Add the same Q=(−16,120) to
the two occurrences above. The new exact height calculation gives, in the
MST quadratic normalization,

    h5(P+Q)=4 mod5,    h5(tau(P)+Q)=3 mod5.

Thus identical separate shadows do not determine how the points combine.
The repaired state recovers the orientation needed for this operation.
The paired heights retain a cross term that cannot be recovered from two
unrelated scalar magnitudes. These rational-point checks have their own
carrier; adding Q to the finite torsion carrier would require an explicitly
larger carrier and is not silently included in its4096-state census.

All points in that finite trace carrier are torsion, and their canonical
heights are zero. Recovering them exactly does not construct the free
rational basis. The rational witnesses and the finite torsion census test
the same rational formulas at different admitted inputs; this is not an
unproved identification of their arithmetic roles.

## A concrete arithmetic vector for the third-relation route

For the actual free basis P,Q, let G be the MST cyclotomic 5-adic pairing
matrix and let ell=(log_omega(P),log_omega(Q))^t. These objects are
defined independently of the complex leading coefficient. Define

    W=adj(G) ell in Q5 tensor E(Q).                   (2)

The new exact residue calculation gives

    G=[[1,2],[2,2]] mod5,  det(G)=3 mod5,
    ell/5=(2,2)^t mod5,
    W/5=(0,3)^t mod5.                                (3)

These are congruences: the P-coordinate of W is not proved to be exactly
zero. The calculation shows W is nonzero. Because G is invertible, (2)
is the unique vector satisfying

    B_MST(x,W)=log_omega(x) det(G) for every x.        (4)

This uniqueness is earned from the nonzero determinant. It is not inserted
as an axiom to force the analytic answer. The exact matrix identity
G adj(G)=det(G)I proves (4).

The vector is invariant under an integral change of basis. For a basis
matrix U, G'=U^t G U and ell'=U^t ell. The represented vector transforms
as U adj(G')ell'=det(U)^2 adj(G)ell. Thus GL2(Z) changes leave W
unchanged, while a finite-index sublattice retains the required index-square
factor. The executable checks this polynomial identity for all nonsingular
integer2-by2 matrices with entries between−3 and3, alongside its written
general proof.

The [height and theorem audit](PADIC_HEIGHT_AUDIT.md) explains the scalar
normalization and the transport to the nonzero BKS Bockstein regulator.
Its augmentation-valued tensor is not literally the scalar residue3 or
the coordinate pair in (3). BKS Theorems5.6 and6.2 provide actual
comparison laws on the 5-adic side under the hypotheses now checked for
this curve. In particular the canonical derived Kato class is collinear
with that regulator; this includes the possibility of the zero class.

What remains is the exact multiplier linking this arithmetic relation to
the **real** leading coefficient. The required formula is still the
rank-two comparison in BKS Proposition4.14, equivalently the scalar
formula in Corollary6.7 once regulator nonvanishing is known. Those are
not proved by the residue (3). The new result replaces an unspecified
third-object suggestion with an actual arithmetic construction, a nonzero
readout, and a precisely isolated remaining comparison obligation.
