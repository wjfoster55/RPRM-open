# A global phase joint with polynomial invariant continuation

12 September 2026. This note extends the regular phase result to **every
zero-Gauss phase state of the fixed two-square graph**, including central
holonomies and nonzero electric circulation. It uses the global tree
reduction in [GLOBAL_TREE_PHASE.md](GLOBAL_TREE_PHASE.md). Its new coordinates
are redundant invariants of the entire phase tuple; they are not a smooth
canonical chart at every singular point. All general claims below have
written algebraic or ordinary differential-equation proofs. The adjacent
exact checker supplies bounded implementation controls, not formal proofs.

## 1. Source, ports, equality, and operations

Keep exactly the seven named links, root, tree, metric, dimensionless
Hamiltonian, and plus-i Pauli convention of the adjacent tree derivation.
Its globally reduced intermediate source is

```text
S = {(U,V,P,Q) in SU(2)^2 x (R^3)^2 : Gamma=0},
Gamma = P-Ad_(U^-1) P + Q-Ad_(V^-1) Q.
```

Here `P,Q` are the right-trivialized canonical cotangent vectors: the
canonical one-form is `P·(dU U^-1)+Q·(dV V^-1)`. They are not velocities or
the regular trace momenta. Residual gauge equality is simultaneous SU(2)
conjugation of both group elements and both Lie-algebra vectors. Under
`i x·sigma <-> x`, this is a common **proper** rotation of all color vectors.
The tree theorem identifies these residual gauge classes with the complete
physical gauge classes of the original zero-Gauss seven-link source.

Write `U=(a,u), V=(b,v)` and name the four ordered vector occurrences
`X_1=u, X_2=v, X_3=P, X_4=Q`. The proposed retained joint is

```text
C = (a,b,G_ij,tau_ijk),
G_ij = X_i·X_j,             1 <= i <= j <= 4,
tau_ijk = (X_i x X_j)·X_k,  1 <= i < j < k <= 4.           (G1)
```

The supplied ports are this one compatible joint and a requested finite
real time, with a finite initial-energy bound `E` if a bounded operational
enclosure is desired. No color orientation frame is supplied or needed by
the updater. The receiver includes physical gauge-invariant observables,
fine electric and magnetic energies, signed transfer, the outer trace,
and Hamiltonian continuations of this fixed graph. Readout of a
gauge-dependent individual color component is outside this receiver.

Finite algebraic readouts built from the retained group elements and phase
vectors are also admitted. Adding a new independent link, loop, or vector
requires its joint relations and a new explicit carrier. Forward time and
negative time are both enabled at every source point. An imposed energy
bound is preserved. No discretized time step or numerical time simulation
is used in the result or checker.

## 2. Exact reached image and complete fibers, at every rank

Extend `G` symmetrically and `tau` by alternation, with zero on repeated
indices. The following are necessary and sufficient for a real joint (G1)
to come from `S`:

1. `G` is positive semidefinite and has rank at most three;
   `G_11=1-a^2`, `G_22=1-b^2`.
2. For each two increasing triples `I,J` drawn from `{1,2,3,4}`,
   `tau_I tau_J = det G[I,J]`.
3. The invariant polynomial `N_Gamma(C)` defined in section 3 is zero.

For a supplied bound `E`, also require `H(C)<=E`. The first item already
forces `|a|,|b|<=1`. These are a mathematical exact-real admission criterion,
not a claim to decide arbitrary encoded real numbers effectively.

**Existence proof.** Positive semidefiniteness and the rank bound give a
real factor `G=X^T X` with three rows. If its rank is at most two, the
diagonal minor identities force all triples to vanish. At rank three,
choose an increasing triple `I` with positive principal minor. Its retained
triple has either square root of that minor. Orient a Gram factor to match
that triple. Every cross-minor identity then forces all its other triples
to match. The first item supplies the two unit group elements. The vector
expression for `Gamma` uses only equivariant sums, crosses, and dot products;
section 3 computes its squared Euclidean norm exactly as `N_Gamma(C)`.
Therefore item 3 is equivalent to zero Gauss in this factor. This proves
existence even at central holonomies and every rank.

**Complete fiber proof.** Equal Gram matrices give an isometry of vector
spans and an extension in `O(3)`. At rank three, a nonzero equal retained
triple forces that extension to have determinant `+1`. At rank at most two,
one can choose its action on the orthogonal complement to make it proper
without changing the given vectors. Consequently equal joints are exactly
common `SO(3)` orbits, which are exactly residual SU(2) conjugacy classes.
Gauss and energy are constant on such an orbit.

Thus each valid joint has **ONE physical gauge class**. Its complete raw
intermediate source fiber is

```text
{(a,Ru,b,Rv,RP,RQ) : R in SO(3)}.                         (G2)
```

This is ONE raw point at rank zero and MANY otherwise. The stabilizer is
`SO(2)` at rank one and trivial at rank at least two; at rank zero it is
all `SO(3)`. Applying the tree inverse and arbitrary vertex gauge changes
gives the complete original seven-link phase fiber. A well-typed candidate
failing the displayed image conditions has NONE sources. Malformed ports
are admission errors. This fiber proof does not use `Delta^-1` or choose
an orientation frame as part of the forward update.

## 3. A finite compiler for invariant vector arithmetic

Use a module of ten named formal vector expressions

```text
e_i = X_i       (four expressions),
f_ij = X_i x X_j, i<j  (six expressions).                 (G3)
```

Represent a vector expression by ten scalar coefficients. The coefficients
are polynomials in `a,b,G,tau`; they need not be unique at singular rank.
Nonuniqueness causes no division or ambiguity because each expression is
evaluated by the identities below. Addition and scalar multiplication act
on coefficients. Dot and cross products act bilinearly using

```text
e_i·e_j = G_ij,
e_i·f_jk = tau_ijk,
f_ij·f_kl = G_ik G_jl-G_il G_jk,

e_i x e_j = f_ij  (with the ordered sign),
e_i x f_jk = G_ik e_j-G_ij e_k,
f_ij x e_k = G_ik e_j-G_jk e_i,
f_ij x f_kl = tau_ijl e_k-tau_ijk e_l.                    (G4)
```

The second and third cross identities are the ordinary vector triple
product identities. The last follows by applying the second one to
`(X_i x X_j) x (X_k x X_l)`. The cross-dot identity is the two-by-two Gram
determinant identity. Every identity holds at every rank, including when
some vectors vanish. A scalar triple expression is the dot product of a
compiled cross with a compiled vector.

**Finite expression closure.** Structural induction on expressions formed
from scalar constants, `a,b`, the named vectors, scalar sums/products,
vector sums, scalar multiplication, dots and crosses proves that every
scalar expression has an invariant polynomial value and every vector
expression has a representation (G3). The base and each constructor are
provided by (G4). This is a proof for every finite expression in that
grammar, rather than an enumeration of a few expression depths.

For example the plus-i adjoint is compiled as

```text
Ad_(c,z) Y = (c^2-z·z)Y+2(z·Y)z-2c(z x Y),
Ad_((c,z)^-1) Y = (c^2-z·z)Y+2(z·Y)z+2c(z x Y).          (G5)
```

Define the compiled vector
`gamma=e_3-Ad_(U^-1)e_3+e_4-Ad_(V^-1)e_4`, using (G5), and set
`N_Gamma(C)=gamma·gamma` using (G4). This gives the polynomial in the image
criterion without reconstructing a Gram factor. On a reached Gram/triple
joint it is nonnegative and vanishes exactly when the vector Gauss law
holds. It is not necessary to expand this polynomial into one long list
of monomials to specify it unambiguously.

Quaternion multiplication is also in this grammar:
`(c,z)(d,y)=(cd-z·y, c y+d z-z x y)`. Ordered word scalars, vector inner
products with phase vectors, and all their finite algebraic combinations
therefore have exact readouts from the same joint. An algebraic replacement
of source slots is an operation on this physical phase carrier only if
it preserves its unit and Gauss conditions; expression closure alone does
not declare an arbitrary replacement symplectic or physically admissible.

## 4. The closed invariant vector field

The global tree Hamiltonian and source equations are

```text
K = 2(P·P+Q·Q)-P·Ad_(V^-1)Q,
H = K+2-a-b,
A = 4P-Ad_(V^-1)Q,          B = 4Q-Ad_V P,

dot a = -A·u,              dot u = a A-A x u,
dot b = -B·v,              dot v = b B-B x v,
dot P = -2 A x P-u,        dot Q = -v.                    (G6)
```

The bracket is `[r,s]=-2(r × s)` in the plus-i identification, where `×`
denotes the ordinary vector cross product.
Equivalently `dot P=[A,P]-u`. The source derivation uses the right Maurer
one-form; changing trivializations without changing the momenta would
change these equations.

Let `F_i` be the four compiled right-hand sides for `u,v,P,Q` in (G6).
The complete invariant updater is the following finite program:

```text
dot a = -A·e_1,                    dot b = -B·e_2,
dot G_ij = F_i·e_j+e_i·F_j,
dot tau_ijk = (F_i x e_j)·e_k
              +(e_i x F_j)·e_k+(e_i x e_j)·F_k.           (G7)
```

Every operation on the right is performed on the ten coefficients using
(G4)-(G5). Thus (G7) is a specified polynomial vector field on the sixteen
ambient real scalar coordinates. Its evaluation neither extracts an
orientation frame nor selects a square-root branch, inverts a matrix,
divides by a minor, or tests a rank. Product differentiation proves
`dC·F_source=F_invariant·C` on every source point. This is a symbolic
identity from the displayed algebra, with no regular-rank qualification.

Useful closed scalar readouts are

```text
U_E = K(C),                 U_B = 2-a-b,
signed transfer = -dot a-dot b,
w = ab-G_12,
dot w = b dot a+a dot b-dot G_12.                         (G8)
```

The compiler is a polynomial arithmetic evaluator and derivative updater.
It is not a claim that the finite-time flow itself is a finite polynomial
formula or that explicit Euler stepping preserves constraints.

## 5. Global continuation and the exact operational quotient

The source vector field is smooth on `SU(2)^2 x R^6`, tangent to its unit
constraints, Hamiltonian, and equivariant under the residual gauge group.
The tree derivation supplies preservation of Gauss and energy. One can
also differentiate `Gamma` and `H` directly in (G6), using invariance of
the Lie-algebra inner product, to obtain `dot Gamma=0` and `dot H=0`.

Adjoint rotations preserve norms. Hence

```text
K >= 2(|P|^2+|Q|^2)-|P||Q|
  >= (3/2)(|P|^2+|Q|^2),    0 <= 2-a-b <= 4.             (G9)
```

A solution of finite initial energy `E` therefore remains in the compact
set of unit configurations and `|P|^2+|Q|^2<=2E/3`. The smooth vector
field and the ordinary compact-set continuation theorem exclude a
finite-time endpoint in either time direction. Every source solution
exists for all real times, stays at zero Gauss if initially there, and
stays inside any admitted energy sublevel.

Lift any valid joint using the existence proof in section 2 and apply
this global source flow. Its joint solves the polynomial ODE (G7).
Polynomial vector fields are locally Lipschitz in the ambient coordinates,
so the initial-value solution of (G7) is unique. Equivalently, source
equivariance and the complete orbit-fiber theorem show independence of
the chosen lift. This supplies a global invariant flow `Psi_t` on the
reached image, even where that image is singular, and proves

```text
C(Phi_t(s)) = Psi_t(C(s))       for every s in S, t in R. (G10)
```

The lift proves image preservation, rather than assuming that arbitrary
ambient points with selected minors zero remain physical. The ordinary
inverse is `Psi_(-t)`. All physical continuations and the readouts (G8)
are constant on complete fibers; their enabledness is constant because
every finite real time is enabled. This proves an exact operational
quotient of the declared finite classical source. It does not infer a
smooth symplectic coordinate chart across every orbit type.

## 6. Agreement with the old regular chart

On the overlap `Delta=(1-a^2)(1-b^2)-G_12^2>0`, define
`x=(a,b,ab-G_12)` and take `dot x` from (G7)-(G8). The old cometric is

```text
       [4(1-a^2)  w-ab       3(b-aw)]
M(x) = [w-ab      4(1-b^2)   3(a-bw)] .
       [3(b-aw)   3(a-bw)    6(1-w^2)]
```

The exact regular decoder is `p=M(x)^-1 dot x`. It uses only retained
invariants and is enabled only for `Delta>0`, where the old proof shows
positive definiteness. In the reverse direction, if `p=(r,s,t)`, put

```text
z = vec(UV)=b u+a v-u x v,
z' = vec(VU)=b u+a v+u x v,
P = -r u-t z,                Q = -s v-t z'.              (G11)
```

To prove (G11), vary `U` and `V` with right velocities independently in
`p·d(a,b,w)`. Their coefficients are precisely the displayed `P,Q`.
The old cotangent reduction proves uniqueness of this zero-Gauss lift on
the overlap. Equality of the canonical one-forms and the source Hamiltonian
therefore proves equality with all six old canonical Hamilton equations,
not just the three initial trace derivatives. In particular derivatives
of the decoder give the old momentum derivatives along every regular
segment. The checker tests that derivative identity with exact dual
rational arithmetic on its bounded regular examples.

At `Delta=0` this decoder is not used. The global joint still retains the
phase state and continues it by (G7). Singular configuration does not mean
zero momentum, and singular rank of the invariant tables does not mean
an undefined vector field.

## 7. Distinguishing controls and scope

At `U=V=I`, let `P=e_1,Q=0`. Then `Gamma=0`, `K=2`, and the tree inverse
gives a nonzero electric circulation. The joint retains `G_33=1`; the
zero-electric state has `G_33=0` and `K=0`. Both have the same three
configuration traces `(1,1,1)`, whose differentials vanish there.
The new source and updater represent both and their different
continuations. This resolves the old chart's specific missing singular
circulation port within this fixed graph.

There is also an exact chart-boundary crossing control. At `U=V=I`, take
`P=e_1,Q=e_2`. Then `Gamma=0`, `K=4`, `dot u=4e_1-e_2` and
`dot v=-e_1+4e_2`. Smoothness of the source flow gives

```text
u(t) × v(t) = 15e_3 t^2+O(t^3),
Delta(t) = |u(t) × v(t)|^2 = 225t^4+O(t^5).
```

Thus the configuration is regular at sufficiently small nonzero positive
and negative times, while singular at time zero. The global joint crosses
this state with no change of formula. The old regular configuration domain
is consequently not invariant under the global flow: starting at a nearby
negative regular time reaches this singular point in finite time. This
argument uses exact derivatives and their nonzero leading term, not a
numerical trajectory.

The phase triples cannot generally be discarded even when all Gram data
and energy are retained. An exact pair of zero-Gauss witnesses is

```text
a=b=0, u=e_1, v=e_2,
P=+e_3,Q=-e_3       versus       P=-e_3,Q=+e_3.           (G12)
```

Both have the same full Gram matrix, `K=3`, `w=0`, and regular
configuration `Delta=1`. Their `tau_123` values are `+1` and `-1`.
Equation (G6) gives `dot w=+6` and `dot w=-6`. The improper reflection
fixing `e_1,e_2` exchanges them; no proper rotation fixing both can do so.
Thus the Gram-only phase summary has an immediate successor-derivative
collision in the actual zero-Gauss source. The retained triples distinguish
it. Lower-rank tuples have vanishing triples but remain covered by the
same formulas.

This is a global solution of one fixed finite classical reduction and
its invariant continuation. It does not establish continuum Yang-Mills
existence, a refinement-compatible coarse Hamiltonian, quantization, a
spectral gap, or a mass-gap theorem. The earlier coarse-fiber magnetic
energy obstruction survives. These different ports require their own
carriers, laws, and proofs.

## 8. Reproduction and evidence

From the repository root:

```powershell
python -I -B research/ym2_global_phase_joint/check_invariants.py
```

The standard-library checker compares an explicit quaternion source route
against the invariant coefficient compiler using exact rational arithmetic.
Its named states include ranks zero through three, central and commuting
configurations, regular lifts, gauge rotations, and the pair (G12). It also
checks unit/Gauss/energy tangency and the regular decoder derivatives.
These checks are evaluations and exact differential identities, not
time trajectories. [RESULTS_INVARIANTS.json](RESULTS_INVARIANTS.json)
records the exact bounded controls. The default command recomputes and
compares the receipt without changing it; `--write-results` deliberately
replaces it. The universal claims rely on the written proofs above and
the adjacent source reduction, rather than extrapolation from these tests
or a claim that the checker establishes its own general soundness.
