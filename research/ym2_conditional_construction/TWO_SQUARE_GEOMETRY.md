# The joint geometry and exact reduced Hamiltonian of two squares

12 September 2026. New derivation using the accepted finite SU(2) lattice
Hamiltonian. No spin truncation or simulated dynamics is introduced.

## 1. Carrier, equality, and complete joint coordinate

Take two elementary squares sharing one edge, with seven links, six
vertices, and gauge transformations at every vertex. Let the shared-edge
matrix be e and the remaining three-link paths be A and B, oriented so
the based elementary holonomies are P=eA and Q=Be^(-1). Their outer
six-edge loop has trace Tr(PQ)=Tr(AB). Define half traces

```text
a=Tr(P)/2,     b=Tr(Q)/2,     c=Tr(PQ)/2.
```

The exact physical configuration quotient is

```text
Omega = {(a,b,c) in [-1,1]^3 : D(a,b,c)>=0},
D = 1-a^2-b^2-c^2+2abc.
```

This is a complete coordinate for gauge orbits on this graph. It is not
a coordinate for the original seven link occurrences before quotienting,
and it is not a three-variable encoding of arbitrary larger lattices.

**Proof.** Gauge fix a spanning tree, leaving two independent holonomies
up to simultaneous conjugation. Write P=aI+i p.sigma and Q=bI+i q.sigma.
Their vector lengths are sqrt(1-a^2), sqrt(1-b^2), and c=ab-p.q. A pair
of vectors up to simultaneous SO(3) rotation is determined by these two
lengths and their dot product. Equal Gram matrices of two vectors are
related by an SO(3) rotation, including rank-deficient pairs: an unused
orthogonal direction lets one choose determinant +1. The SU(2) adjoint
action supplies that rotation. Existence is exactly the Cauchy-Schwarz
inequality (c-ab)^2<=(1-a^2)(1-b^2), equivalent to D>=0.

Thus the completion fiber for c at supplied (a,b) is exactly

```text
[ab-sqrt((1-a^2)(1-b^2)), ab+sqrt((1-a^2)(1-b^2))].
```

It is ONE at a collapsed interval and MANY otherwise, at gauge-orbit
equality. An inadmissible a or b is an admission error. This keeps the
missing joint relation joint; the product of separate trace records
would forget it. The [obstruction proof](CONDITIONAL_OBSTRUCTION.md)
shows that forgetting c cannot preserve any nonzero interacting
eigenfunction depending only on a and b when r is nonzero.

## 2. The measure is simple; the kinetic geometry is not flat

Product Haar measure pushes forward to

```text
dmu_Omega = (2/pi^2) da db dc on Omega.
```

Indeed, conditional on e the disjoint paths make P and Q independent
Haar matrices. Each half trace has density (2/pi)sqrt(1-a^2). Their
independent axes have dot cosine uniform on [-1,1]. Changing this cosine
to c supplies Jacobian 1/sqrt((1-a^2)(1-b^2)); the factors cancel.
The boundary has measure zero. This derivation also normalizes the
constant: the c-interval has length 2sqrt((1-a^2)(1-b^2)), giving
volume pi^2/2.

For invariant functions F(a,b,c), define Gamma(F,H)=sum_e grad_e F.grad_e H
using the original seven unit-round SU(2) metrics. Its coefficient matrix is

```text
G = [[4(1-a^2), c-ab,       3(b-ac)],
     [c-ab,      4(1-b^2),  3(a-bc)],
     [3(b-ac),   3(a-bc),   6(1-c^2)]],

Gamma(F,H) = (partial F)^T G (partial H).
```

For a one-link change of a loop trace, the Pauli product rule gives
Gamma_edge(a,a)=1-a^2. There are four edges for a,b and six for c.
The common edge is traversed oppositely by P and Q, giving c-ab.
Each of the three edges shared by P and PQ gives b-ac; each of the
three shared by Q and PQ gives a-bc. This proves every entry, with
orientations fixed by the displayed loop words. Inverting an edge is a
metric/Haar isometry here; no Fourier-norm orientation invariance is assumed.

The accepted Casimir convention gives Ta=6a, Tb=6b and Tc=9c. Therefore
the exact reduced kinetic operator on smooth invariant functions is

```text
T_Omega F = 6a F_a+6b F_b+9c F_c
             -(1/2) sum_ij G_ij F_ij
           = -(1/2) sum_ij partial_i(G_ij partial_j F).

A_Omega(r)=T_Omega-r(a+b).
```

The divergence identity is checked directly: div G=(-12a,-12b,-18c).
Its quadratic form is (1/2) integral (partial F)^*G(partial F) dmu_Omega.
The self-adjoint realization and admissible regularity at the boundary
are inherited from smooth gauge-invariant functions on SU(2)^7 and
closure of that form. We do not impose arbitrary flat-coordinate
Dirichlet or Neumann data on the curved quotient boundary.

Two useful exact geometric identities are

```text
G grad D = -D (8a,8b,12c)^T,
det G = 6D (16-6a^2-6b^2-c^2-3abc).
```

In particular the boundary normal has zero quadratic cost in these
coordinates on D=0. That degeneracy records the quotient geometry;
it does not prove a small physical spectral gap. At r=0 the physical
free gap on this graph is 6, despite the same boundary degeneracy.
The inherited gauge constraints require every nontrivial spin support
to contain a cycle; the shortest is a four-edge fundamental cycle,
whose kinetic eigenvalue is 4*(3/2)=6 and is attained by a or b.

## 3. The next joint term is forced at second order

The mean-zero log vacuum has the weak-coupling expansion, on each fixed
graph and within its proved analytic construction neighborhood,

```text
w = r w1+r^2 w2+O(r^3),
w1=(a+b)/6,
w2=-(a^2+b^2-1/2)/288 -ab/468+c/351.
```

The terms are obtained from the actual equation
Tw-(1/2)Gamma(w,w)-r(a+b)=E. First, Tw1=a+b. Next,

```text
Gamma(a+b,a+b)=8-4a^2-4b^2+2c-2ab,
T(a^2-1/4)=16(a^2-1/4),
T(ab)=13ab-c,             Tc=9c,
T^(-1)(c-ab)=-ab/13+4c/39.
```

Since Haar expectations are a^2=b^2=1/4 and ab=c=0, these imply
Tw2=(1/72)Q Gamma(a+b,a+b) and E2=-1/12. The coefficient c/351
is nonzero: the new joint variable appears in the first correction
generated by overlap, rather than being an optional descriptive tag.
For this finite graph, w2 is the Taylor coefficient of the actual
locally constructed log vacuum. The truncated polynomial alone is not
asserted to be the exact vacuum.

The residual of its positive exponential is exactly

```text
(A exp(rw1+r^2w2))/exp(rw1+r^2w2)
 = -r^2/12-r^3 Gamma(w1,w2)-(r^4/2)Gamma(w2,w2).
```

This exposes the next obligation: retaining c closes the two-square
configuration quotient and its exact differential operator, but the
vacuum is still a nontrivial function on that quotient. On larger graphs,
overlapping corrections generate larger joint supports. The new
[local construction estimate](LOCAL_VACUUM_ROUTE.md) addresses their
summation in a graph-uniform norm; coordinate completeness alone cannot
supply the analytic bound.

## 4. Literature and evidence scope

Trace coordinates for the rank-two SU(2) character variety are established
mathematics. A directly inspected primary exposition is Forni, Goldman,
Lawton and Matheus, *Non-ergodicity on SU(2) and SU(3) character varieties
of the once-punctured torus*, Annales Henri Lebesgue 7 (2024), section2.2,
printed page1102. It identifies the three trace generators and compact
three-dimensional character body. Our half-trace signs, seven-edge
kinetic coefficients and perturbative calculation are derived explicitly
above; no priority claim is made for the character coordinates.
[Primary article](https://www.numdam.org/item/10.5802/ahl.216.pdf).

The written derivation covers the full continuous gauge quotient of this
particular graph, without a spin cutoff. New exact controls compare its
metric with direct quaternion link derivatives and verify the displayed
polynomial identities. Those finite controls do not replace the general
proof or establish a continuum/infinite-volume limit.
