# A larger actual-vacuum and uniform physical-gap interval

12 September 2026. This continuation combines two independently derived
improvements in the accepted anchored Fourier norm. It changes no
Hamiltonian, gauge constraint, lattice spacing convention, or earlier
packet. Publication remains on hold. The result is a written theorem with
independent agent review and exact finite controls, not a formal proof-
assistant certificate or a literature-priority claim.

## 1. Precise result

Let G be any admitted finite open square/cubic lattice graph, with all
SU(2) link variables, every vertex gauge constraint, distinct elementary
plaquettes, no boundary charges and no spin cutoff. Put

```text
d in {2,3},       m=2(d-1),
T=-Delta/2,       S=sum_p Tr(U_p)/2,
A(r)=T-rS,       H/E_el=A(r)+r N_p,       E_el>0.
```

The metric on each SU(2) is the unit-round S^3 metric, with single-link
Casimir lambda_j=2j(j+1). Equality in Hilbert spaces is Haar almost
everywhere; the constructed vacuum and conditional densities have smooth
representatives at every configuration.

**Theorem.** For every such graph and

```text
0 <= r <= 1/(3m),
```

there is a convergent construction of the actual positive normalized
vacuum, and its physical excited complement obeys

```text
gap_phys(H)/E_el >= [d/(7(d-1))] exp(-32/63) > 0.       (C1)
```

The same constant holds for every graph size. If the physical sector has
no excited complement, the corresponding quadratic-form inequality is
vacuous there rather than asserting an excited eigenvalue exists.
In three spatial dimensions this gives r<=1/12 and bound
(3/14)exp(-32/63), approximately 0.129. In two dimensions it gives
r<=1/6 and (2/7)exp(-32/63), approximately 0.172.

The earlier accepted entire uniform-gap interval was r<=9/(128m).
The new endpoint is larger by exactly 128/27, approximately 4.741.
For d=3, the old endpoint was 9/512, approximately 0.01758; the new one
is 1/12, approximately 0.08333. These compare sufficient bounds in the
same dimensionless coupling, not different physical energy units.

A stronger bound on the smaller interior interval is also available:

```text
r<=1/(4m)
  ==> gap_phys(H)/E_el >= [3d/(4(d-1))] exp(-7/24).      (C2)
```

All statements concern the retained finite-lattice Hamiltonian. They do
not construct an infinite-volume representation or continuum theory.

## 2. The norm and why the new restrictions are legitimate

Retain the accepted Fourier expansion and anchored norm:

```text
u=sum_(J!=0) Tr(B_J pi_J),
lambda_J=sum_i 2j_i(j_i+1),
||u||_* = max_e sum_(J:e in supp J) lambda_J ||B_J||_1.
```

Work in its closed real gauge-invariant subspace, with Haar mean zero.
This is a restriction on the unknown log vacuum, not a truncation of
admitted SU(2) representations. Gauge transformations commute with
isotypic projections, T, its mean-zero inverse and Q. Since the metric
is gauge invariant, the contracted derivative Gamma(u,v)=grad u.grad v
preserves invariance. The source S is invariant. Thus the whole
fixed-point construction remains in this subspace.

The [gauge estimate](GAUGE_NORM_GAIN.md), especially its final section8,
proves for the same bilinear map

```text
B(u,v)=T^(-1)Q Gamma(u,v),
||B(u,v)||_* <= K ||u||_* ||v||_*,       K=1/3.          (C3)
```

The preceding accepted value was 16/9 without exploiting invariance.
There are two load-bearing new inputs. First, gauge balance at vertices
of a simple triangle-free lattice forces a spin-l link to be supported
by other spins, giving lambda_J>=l(2l+11), and hence lambda_J>=6 for
any nonzero invariant block. Second, coefficient gauge intertwiners make
the averaged one-link singular-vector density matrices maximally mixed.
The contracted fundamental-pair constant becomes 3/2 rather than 2.
The written proof treats the nonfundamental half-spin pairs as well;
it does not assume individual singular vectors are invariant.

The inverse output Casimir is used exactly once, to cancel the norm's
output energy weight. An additional factor 1/6 is not appended. The
new gain arises in the input estimate and its anchored summation.

## 3. Resolve the first generated joint term before bounding the tail

The actual log-vacuum equation, modulo its additive normalization, is

```text
u = r T^(-1)S + (1/2)B(u,u).
```

Set u0=rS/6 and u=u0+v. The source norm remains the accepted exact
orientation-sensitive bound ||T^(-1)S||_*<=4m, so with x=mr,
||u0||_*<=4x. The equation becomes

```text
v = h + B(u0,v)+(1/2)B(v,v),
h=(1/2)B(u0,u0).                                      (C4)
```

The source h is evaluated using the actual plaquette pattern before
applying a generic bound. Edge-disjoint plaquette pairs have zero cross
gradient. For one square Q Gamma(a_p,a_p)=-chi_1(U_p), with Fourier norm
27 in the retained orientation, giving 3m/8 in the coefficient of r^2.
For two squares sharing an edge, the final gauge bound makes the local
cross-gradient norm at most 24. At most (7/2)m(m-1) unordered adjacent
pairs can touch a fixed output anchor. The [local derivation](LOCAL_VACUUM_ROUTE.md)
therefore proves

```text
||h||_* <= kappa_m r^2,
kappa_m = (3/8)m+(7/3)m(m-1),
kappa_2=65/12,     kappa_4=59/2,
kappa_m/m^2 <= 59/32.                                 (C5)
```

On two adjacent squares the new joint trace c already appears in this
first correction. Its explicit coefficient and full reduced operator
are in [the joint geometry](TWO_SQUARE_GEOMETRY.md). The further tail v
is not discarded: C4 sums it by contraction with all generated spins
and supports admitted.

## 4. A closed ball with strict slack at the new endpoint

For any radius Z, C3–C5 give

```text
||right side of C4||_* <= (59/32)x^2+(4/3)x Z+Z^2/6,
Lipschitz constant <= (4x+Z)/3.                        (C6)
```

Both quantities increase with nonnegative x,Z. At the worst allowed
x=1/3, choose Z=3/7. Exact rational arithmetic gives

```text
Z - [(59/32)(1/3)^2+(4/3)(1/3)(3/7)+(3/7)^2/6]
  = 37/14112 > 0,
(4/3+3/7)/3 = 37/63 < 1.                              (C7)
```

Thus C4 maps the closed radius-3/7 ball into itself and is a strict
contraction, uniformly for 0<=x<=1/3. Banach's fixed-point theorem
constructs one v in that ball. This is an all-spin convergent series in
the accepted Banach space, not a finite Taylor approximation.

The accepted fixed-graph regularity argument applies unchanged: the
finite-graph weighted Fourier summability gives C1 control and the
distributional elliptic equation, followed by elliptic bootstrap.
Consequently u is smooth. Its normalized exponential psi is strictly
positive and solves A psi=E psi. The exact ground-state form identity
proves it is the actual unique positive vacuum. No assumed spectral gap
was used to construct it. C7 has strict slack at the closed endpoint,
so no limiting argument is required for that endpoint.

## 5. The actual conditional bounds, including every exterior

Write the actual density as nu=psi^2 mu, with

```text
log(dnu/dmu) = rS/3+2v+constant.
```

The explicit source rS/3 has one-link oscillation at most 2mr/3 and
mixed-oscillation row budget at most 4mr. For the invariant correction,
lambda_J>=6 and |v_J|<=||B_J||_1 imply

```text
d_v=max_i osc_i(2v) <= 4 max_i sum_(J:i in supp J)||B_J||_1
                    <= (2/3)Z.                       (C8)
```

For mixed replacement differences, each coefficient contributes at
most 8||B_J||_1 to D_ij(2v). Using
lambda_J>=(3/2)|supp J| yields the accepted bound

```text
b_v=max_i sum_(j!=i)D_ij(2v) <= (16/3)Z.               (C9)
```

All suprema admit every link value and exterior configuration.
The total-variation tilt inequality then bounds the actual influence
matrix by its actual mixed log density, giving

```text
q=max_i sum_j c_ij <= x+(4/3)Z <= 19/21 < 1,
D=max_i osc_i log(dnu_i/dmu_i)
  <= (2/3)(x+Z) <= 32/63.                             (C10)
```

Each actual one-link conditional therefore has gradient Poincare
constant at most exp(D)/3. The accepted continuous conditional-update
proof gives all conditional blocks constant at most exp(D)/[3(1-q)].
The accepted gauge/forest-complement identity then yields

```text
gap_phys(A) >= [d/(d-1)](3/2)(1-q) exp(-D),
```

which at C10 is exactly C1. This is the gap of the retained physical
Hamiltonian because the density was constructed from its actual vacuum.
The reference residual has not been omitted.

For C2 choose x<=1/4 and Z=3/16 in C6. The radius margin is 1/256,
the Lipschitz factor is 19/48, q<=1/2 and D<=7/24. The same formula
proves C2. These checks also use the final K=1/3 and final source C5.

## 6. Three conditions from the preceding rail packet are now met here

The conditional law is obtained from an actual positive joint density,
so all coordinate update rectangles close exactly and gauge covariance
holds. The fixed-point equation makes its local-energy ratio constant,
so it meets the actual-vacuum requirement. C10 supplies the graph-uniform
conditional controls. Thus the previous conditional certificate has
been supplied with its missing inputs on this larger coupling domain.

This does not say those requirements hold for arbitrary compatible
conditional laws or for every coupling. The earlier incompatible local
rules, compatible wrong-vacuum example, and slow collective auxiliary
family remain valid separating cases.

## 7. Where these estimates stop, and what the next step would need

The centered construction majorant itself has a smaller positive fixed
point while

```text
x < 12/(16+sqrt(177)), approximately 0.410.             (C11)
```

This is only a sufficient construction threshold. It uses the strict
condition (1-4x/3)^2>(59/48)x^2. A root at the edge of that condition
would exhaust the contraction proof, not prove a singular vacuum.

The current influence bound needs Z<(3/4)(1-x). Substituting this
threshold into C6 reduces the available strict slack to

```text
30x^2+50x-21 < 0,
x < (sqrt(1255)-25)/30, approximately 0.348.            (C12)
```

For every fixed x below C12's positive root, the smaller scalar fixed
point lies below that influence threshold. A slightly larger radius
still gives contraction and a positive q margin. C1 deliberately uses
the simpler closed interval x<=1/3 with explicit uniform constants.
No positive endpoint gap is inferred from C12 at equality.

Here the collective comparison runs out before the construction
majorant. This is an estimate boundary, not evidence that the actual
gap closes. A next useful improvement must control the actual mixed
responses more tightly, or estimate their spectrum with a weighted
matrix/block argument, or use a different physical quadratic-form
comparison. Repeating coordinate handoffs alone does not change C12.

The outer-loop trace resolves the first missing joint degree of freedom
on two squares. Larger connected clusters generate more such relations.
The present proof controls their whole tail in one norm on a finite
coupling interval. To continue much further, one needs their support,
sign, or response structure to improve that uniform bound. The proof
does not assert a fixed finite list of local traces suffices on every graph.

Finally, the accepted standard lattice convention gives r=8/g_b^4.
The weak-bare-coupling continuum direction takes r toward infinity,
well outside C1, C11, and C12. A dimensionless gap in E_el units must
also be matched to a defined physical scale in the limit. No change of
units can turn this bounded r interval into that limit. Infinite-volume
construction, continuum convergence, and a positive continuum physical
mass gap remain OPEN.

## 8. Evidence grade

The source/Gamma algebra, all-spin inequalities, fixed-point argument,
and conditional gap transfer are written proofs using the stated
accepted analytic dependencies. Independent agents reviewed the gauge
intertwiner step, source counting, scalar inequalities and composition.
[The review](CONSTRUCTION_REVIEW.md) records exact reviewed source hashes.

The new [checker](check_construction.py) verifies complete polynomial
identities, direct seven-link quaternion derivatives on rational SU(2)
configurations, finite spin-pair arithmetic and the exact radius/gap
constants. Its [receipt](RESULTS.json) is a bounded corroboration, not
a substitute for the all-spin proof. Earlier checkers are not rerun.
Established representation theory, character coordinates, Banach
contraction, and the prior analytic results remain separately attributed.
No claim is made that this numerical bound has priority in the literature.
