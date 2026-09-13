# A spatial joint with an exact static continuation law

12 September 2026. A bounded continuation of
[the homogeneous joint/scaling result](../ym2_joint_scaling/JOINT_AND_SCALING.md).
This note derives a static SU(2) holonomy join. It does not supply a reduced
Hamiltonian, a renormalization map, or a continuum/quantum limit.

**Result:** two local loop traces need one transported relative alignment to
determine their joined trace. For three loops, even every pair trace can
miss an oriented triple product. Retaining scalar parts, a common Gram
matrix, and oriented triple products determines the complete simultaneous
conjugacy class and supports ordered multiplication exactly. The same rule
works for every admitted finite tuple; it is proved algebraically, not fitted
separately at each size. An exact outer product still leaves a complete family
of fine interiors, including different fine magnetic energies.

## 1. Carrier, interface and receiver

Fix a finite oriented graph, named loop occurrences, their traversal order,
and connector paths to one named root. For the complete image/fiber claims,
admit the full tuple carrier `SU(2)^n`, with `n<=N` and `N` a supplied positive
finite integer. Independent graph cycle generators realize this carrier;
the two plaquettes of the open two-cell graph are one such example. A choice
of graph loops with additional word relations requires imposing those
relations and intersecting the fibers below; it cannot inherit the full
image claim without that check. Coordinates are real and dimensionless;
each group element lies on
the compact unit 3-sphere. The derivation is uniform in each such `N`; the
exact checker uses the finite rational states listed in its receipt.

The source for this static algebraic contract is the tuple of based
holonomies. Raw equality means equality of every matrix at every named
occurrence. Gauge equality here is **simultaneous conjugacy** of that tuple.
This is not asserted to classify all link fields, electric fields, or
continuum fields realizing it. Such realizations can have further fibers.

For a loop `V_y` based at another vertex, retain the declared transporter
`P_xy` and use `V=P_xy V_y P_xy^-1` at the root `x`. With the convention

`P_xy -> g_x P_xy g_y^-1`, `V_y -> g_y V_y g_y^-1`,

the transported `V` transforms as `g_x V g_x^-1`, just like a loop `U` at
`x`. The connector is part of the interface. Changing it can change a joined
loop; it is not merely changing coordinates. `UV` describes the declared
ordered concatenation. It describes a two-cell outer boundary when the
chosen orientations and connector make the corresponding edge word cancel
the shared interior traversal. Arbitrary loop products are not automatically
outer boundaries of a geometric union.

The first supplied ports are `a=Tr(U)/2`, `b=Tr(V)/2`; the missing port is
their relative color alignment. The requested readout is `w=Tr(UV)/2`.
The stronger receiver also admits traces of ordered words, inverses, and
replacement of a retained factor by an ordered product of retained factors.
These operations are total on a fixed tuple; adding a new external factor
requires its joint relations to the old factors and an available named slot.
An operation that exceeds the supplied cap or changes the graph/interface
has a new contract, rather than silently extending this one.

## 2. Two-cell join: exact image and complete fibers

Use the standard Pauli matrices with
`sigma_i sigma_j=delta_ij I+i epsilon_ijk sigma_k`, and write

`U=a I+i u·sigma`, `V=b I+i v·sigma`,

where `a^2+|u|^2=b^2+|v|^2=1`. In this **plus-i convention**, multiplication is

```text
(a,u)(b,v) = (ab-u·v, a v+b u-u×v).                 (S1)
```

The minus sign on the cross product is essential. An alternative quaternion
convention can use a plus sign, but must change its Pauli identification
consistently. Direct multiplication of the displayed Pauli matrices proves
(S1); the checker independently uses exact complex 2-by-2 matrices.

Retain `d=u·v`. Then

```text
w=ab-d.                                           (S2)
```

The exact reached image of `C_2(U,V)=(a,b,d)` is

```text
|a|<=1, |b|<=1, d^2 <= (1-a^2)(1-b^2).             (S3)
```

Necessity is the unit-sphere condition and Cauchy--Schwarz. For sufficiency,
put `r=sqrt(1-a^2)`, `s=sqrt(1-b^2)`. If `r>0`, a representative is

```text
u=(r,0,0),  v=(d/r, sqrt(s^2-d^2/r^2), 0).
```

If `r=0`, (S3) forces `d=0`; take `u=0`, `v=(s,0,0)`.
These give every admitted tuple. The complete raw fiber is the common
`SO(3)` rotation orbit of this representative pair. Equality of the two-vector
Gram matrix gives an isometry between their spans; extending that isometry
to three dimensions can always have determinant `+1`, since the span has
dimension at most two. SU(2) conjugation supplies precisely these proper
rotations. Consequently each reached `(a,b,d)` has **ONE simultaneous
conjugacy class**, although its raw representatives are generally MANY.
Only when both vector parts vanish is its raw fiber also ONE; otherwise the
whole rotation orbit is the complete MANY family.

Supplying only `(a,b)` gives the complete joined-readout fiber

```text
w in [ab-rs, ab+rs].                              (S4)
```

Every point occurs by the representative above, so this is a complete
interval, not a few witnesses. It is ONE when `rs=0`, and MANY otherwise.
Equivalently, the complete simultaneous-conjugacy source fiber over `(a,b)`
is indexed by `d in [-rs,rs]`. A proposed well-typed `(a,b,d)` outside (S3)
has NONE compatible sources. A non-unit proposed source matrix or malformed
port is an admission error. With `(a,b,d)` supplied, (S2) gives ONE joined
trace.

For a rational hostile pair, fix `a=b=3/5`, `u=(4/5,0,0)` and choose
`v=+(4/5,0,0)` or `v=-(4/5,0,0)`. The local traces agree, but the normalized
joined traces are respectively `-7/25` and `1`, the endpoints of (S4).
Thus a pair of independent local trace summaries is insufficient.

## 3. The third-cell obstruction is orientation

For `Q_i=(a_i,v_i)`, write `G_ij=v_i·v_j` and
`tau_ijk=(v_i×v_j)·v_k`. Repeated use of (S1) gives

```text
Tr(Q_1 Q_2 Q_3)/2
 = a_1 a_2 a_3-a_3 G_12-a_1 G_23-a_2 G_13+tau_123. (S5)
```

Choose

```text
Q_1=(3/5, 4/5,0,0),  Q_2=(3/5, 0,4/5,0),
Q_3^+=(3/5, 0,0,4/5),  Q_3^-=(3/5, 0,0,-4/5).
```

The two triples have every individual normalized trace `3/5`, every
distinct-pair normalized product trace `9/25`, and the same full Gram matrix
`(16/25) I`. Their oriented triple products are `+64/125` and `-64/125`,
and their ordered triple normalized traces are `91/125` and `-37/125`.
An improper reflection exchanges the two triples. It is not simultaneous
SU(2) conjugation. Pair relationships determine an `O(3)` orbit; at rank
three that orbit has two `SO(3)` branches.

For three factors with fixed valid scalars and Gram matrix, the complete
trace fiber in (S5) is the two values obtained using
`tau_123=+sqrt(det G)` and `-sqrt(det G)` when `rank G=3`. At rank at most
two, `tau_123=0` and the trace fiber is ONE. Here the two-point answer is
complete because Gram factorization gives exactly those orientation branches.
This does not contradict the accepted homogeneous Gram closure: its declared
magnetic-energy receiver was insensitive to that model's mirror branches.
Ordered loop multiplication is a different receiver and operation.

## 4. A sufficient joint for finite ordered continuation

For a tuple of `n<=N` based holonomies, retain

```text
C_n = (all a_i, all G_ij, all tau_ijk).             (S6)
```

The scalar, pair and triple coordinates are one constrained joint. They are
not independently selectable tables. Here is an exact description of its
image, including singular cases:

1. `|a_i|<=1`; `G` is symmetric positive semidefinite of rank at most three,
   with `G_ii=1-a_i^2`.
2. Choose a real `3 by n` factor `X` with `G=X^T X`. If the rank is at most
   two, every `tau` is zero. If the rank is three, the array `tau` is either
   the array of all ordered column determinants of `X` or its common negative.

The criterion is independent of the chosen factor. Equivalently, require an
alternating triple array and, for every pair `I,J` of increasing index
triples, `tau_I tau_J=det G[I,J]`. Together with condition 1 these polynomial
identities are sufficient: in rank three choose `I` with `det G[I,I]>0`,
orient a Gram factor to match `tau_I`, then the cross-minor identities force
every other triple to match; in rank at most two the diagonal identities
force every triple to be zero. This is an exact image characterization, not
a claim that testing arbitrary real inputs is an effective algorithm.

**Complete fiber proof.** Equality of Gram matrices gives a common `O(3)`
map between the vector factors. At rank three a nonzero retained determinant
forces its determinant to be `+1`. At lower rank, its extension can be made
proper without changing any vector. Hence equality of (S6) is equivalent to
simultaneous SU(2) conjugacy. Each valid joint has ONE conjugacy-class source;
its complete raw source fiber is the common proper-rotation orbit. The
statement is about the tuple source defined in section 1, not all fine link
fields realizing that tuple.

**Explicit closure.** If a named factor `k` is replaced by the product of
old factors `i,j`, its new scalar and relationships to unchanged factors
`ell,m` are

```text
a_k = a_i a_j-G_ij,
G_k,ell = a_i G_j,ell+a_j G_i,ell-tau_i,j,ell,
tau_k,ell,m = a_i tau_j,ell,m+a_j tau_i,ell,m
              -G_i,ell G_j,m+G_i,m G_j,ell.         (S7)
```

Use symmetry/alternation for permuted slots, zero for repeated triple slots,
and `G_kk=1-a_k^2`. All unaffected entries remain unchanged. These are
simultaneous formulas from the old tuple, also when `k` equals `i` or `j`.
The last line follows from
`(v_i×v_j)·(v_ell×v_m)=G_i,ell G_j,m-G_i,m G_j,ell`.
Inversion preserves `a_i` and negates `v_i`, so it changes every involving
pair/triple entry by the appropriate number of signs. These formulas preserve
the exact reached image because they are computed from valid group products;
fiber independence follows either from the formulas or conjugation covariance.

All ordered word traces are therefore determined by the joint, and every
admitted finite sequence of these replacements/inversions has a well-defined
joint continuation. Associativity comes from matrix multiplication through
(S1), so different parenthesizations yield the same product; exchanging
factor order is a different operation and generally changes the result.
This is an exact quotient for the declared **static algebraic operations**.
It is not a time-evolution theorem. All triples may be redundant: at rank
three, the Gram matrix plus one nonzero orientation sign determines them.
No minimal storage or computational speed claim is made.

To join an external region, retain its connector and the new cross pairs
and cross triples. Two separately complete internal joints alone lack these
relative data. Local completeness does not imply compatible joint gluing.

## 5. Coarse-to-fine recovery and a surviving energy obstruction

Let `W=UV` be a supplied **full** based SU(2) product, rather than merely
its trace. The complete raw fine-pair fiber is

```text
{(U, U^-1 W) : U in SU(2)}.                        (S8)
```

Every member multiplies to `W`; every solution must have `V=U^-1 W`, proving
both directions. Thus it is MANY, even when the full outer transporter is
known. Retaining the split factor gives the bijective coordinate change

```text
(U,V) -> (W=UV, U),       (W,U) -> (U,U^-1 W).      (S9)
```

This is exact recovery at the tuple level. Forgetting `U` is the lossy step.
A finer region's internal edge fields need their own witnesses and constraints;
(S9) does not invent the internal links or electric data.

There is a useful quantitative obstruction even before dynamics. Define the
dimensionless two-plaquette magnetic shape sum

`B_fine=(1-a)+(1-b)=2-a-b`,

with any physical common prefactor kept separately. Write `W=(w_0,w)`.
On (S8), (S1) gives `b=a w_0+u·w`, and therefore

```text
a+b=(1+w_0)a+u·w.
```

This is a linear functional on the full unit 3-sphere `(a,u)`. Its coefficient
vector has squared norm
`(1+w_0)^2+|w|^2=2+2w_0`. Every value between the extrema occurs (the sphere
has enough orthogonal directions). The complete fine-energy readout fiber is

```text
B_fine in [2-sqrt(2+2w_0), 2+sqrt(2+2w_0)].        (S10)
```

It is ONE(`2`) at `W=-I`, and MANY otherwise, including at `W=I`. This
degenerate readout does not make the source fiber in (S8) unique. Conversely,
the coarse shape term `1-w_0` is constant on that fiber and cannot recover
the generally varying fine sum. A scale-dependent coefficient alone cannot
remove this within-fiber variation.

An exact noncommuting witness fixes `W=(3/5,0,0,4/5)`. Use

```text
U_A=(3/5,4/5,0,0),    V_A=(9/25,-12/25,-16/25,12/25),
U_B=(4/5,3/5,0,0),    V_B=(12/25,-9/25,-12/25,16/25).
```

Both have `U V=W`, but `B_fine,A=26/25` and `B_fine,B=18/25`. Neither pair
commutes. The common coarse shape term is `2/5`. Thus preserving exact
outer holonomy is not sufficient to replace the fine Wilson magnetic sum.
One can retain enough interior data to recover it, supply a conditional
distribution and integrate over interiors, or prove a different effective
law. None follows from the product identity alone.

For a truly open path `h_xy`, gauge transformation is
`h_xy -> g_x h_xy g_y^-1`. Its trace generally changes because the endpoint
gauges are independent. Path composition `h_xy h_yz` works because the same
middle-frame transformation cancels. The complete left-right gauge orbit of
one open transporter is all of SU(2), so quotienting each open path by its
two endpoint gauges independently discards exactly the interface needed for
later composition. Retained boundary frames/transporters, or an equivalent
shared boundary representation, are the positive repair. A closed-loop trace
cannot silently stand in for that open boundary object.

## 6. Which scaling question has been answered?

The homogeneous law `A_lambda(t)=lambda A(lambda t)` at fixed `g,L` changes
field amplitude and clock. It does not change spatial resolution or the
number of cells. The static law here covers ordered concatenation at each
finite supplied size, retaining its joint interface. Refinement reverses a
concatenation by selecting or retaining members of its correlated fiber;
the product does not choose a unique fine interior.

Physical lattice spacing, path lengths, volume, coupling, and Hamiltonian
coefficients are separate context ports. They must travel with any physical
scale change. A unit holonomy cannot generally be multiplied by an amplitude
factor and remain in SU(2). Defining a scaling through a matrix logarithm
also requires branches and does not preserve multiplication in general.
For a concrete branch-free integer control, take `U=i sigma_1`,
`V=i sigma_2`: `U^2 V^2=I` but `(UV)^2=-I`. Thus even the everywhere-defined
power map `Q->Q^2` is not a homomorphism of this join. The checker verifies
this independently from matrices.

The exact new result is static compatible joining plus a recoverable fine
fiber. Closure of a proposed reduced spatial dynamics, a Hamiltonian through
coarsening, a refinement-compatible probability law, and a continuum/quantum
limit remain separate obligations. Equations (S8)--(S10) locate a specific
next obstruction: outer agreement alone leaves fine magnetic energy free.
No renormalization-group closure or mass-gap conclusion is claimed.

## 7. Evidence and reproduction

The universal statements above are written algebraic proofs for the declared
classical SU(2) tuple carrier. They are derived here using ordinary matrix and
Gram algebra, without a claim of first discovery. They are not formal proofs.
The prior homogeneous theorem is reused at its original stated scope and is
not rerun by this checker.

From the repository root run:

```powershell
python -I -B research/ym2_spatial_joint/check_static_join.py
```

The standard-library checker recomputes its results and compares them with
[RESULTS_STATIC.json](RESULTS_STATIC.json), leaving the saved receipt unchanged.
Pass `--write-results` explicitly when intentionally replacing that receipt.
It compares the quaternion route against exact complex Pauli-matrix products,
checks rational pair/triple witnesses and product updates, and verifies the
coarse-fiber energy and recovery controls. Those finite checks detect errors
in these examples and implementations; coverage of the real continuous
fibers comes from the proofs, not enumeration or a self-test soundness claim.
