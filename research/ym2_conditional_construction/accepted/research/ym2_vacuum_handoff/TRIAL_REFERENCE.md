# An explicit new reference and the correction it must carry

12 September 2026. New written derivation using the accepted finite-lattice
YM model. It tests the proposed handoff without assuming a new actual
vacuum has already been constructed.

## 1. Carrier and exact transformed operator

Let G be a finite open square/cubic graph, with full SU(2) link variables,
all vertex gauge constraints and no boundary charges. Work in the physical
subspace of L2 of product Haar measure mu. Keep the accepted unit-round
link metric, T=-Delta/2, S=sum_p a_p, a_p=Tr(U_p)/2 and

```text
A(r)=T-rS,          H/E_el=A(r)+r N_p.
```

The additive scalar does not affect the excitation gap. The accepted
plaquette identity is T a_p=6 a_p. The actual ground state of each fixed
finite Hamiltonian is unique, smooth, positive and gauge invariant.
Here phi is an arbitrary smooth, positive, normalized, gauge-invariant
reference, which need not be that ground state. Set

```text
w=log phi,       dnu_phi=phi^2 dmu,
K_phi=T-grad w dot grad,
R_phi=(A phi)/phi=Tw-(1/2)|grad w|^2-rS.
```

Multiplication U_phi f=phi f is unitary from L2(nu_phi) to L2(mu),
preserves physical vectors, and gives the exact operator/form transport

```text
U_phi^-1 A U_phi=K_phi+R_phi,
<f,K_phi f>_(nu_phi)=(1/2) integral |grad f|^2 dnu_phi.   (TR1)
```

The displayed operator identity holds on smooth functions and extends
to the corresponding self-adjoint realization and closed form. Positivity
on a fixed compact manifold makes the multiplication maps and inverses
bounded on the needed Sobolev spaces. This statement makes no graph-uniform
bound on those multiplication norms.

A change of reference is therefore legitimate. The residual R_phi must
travel with it. Dropping R_phi changes the physical operator unless it is
constant. If it is constant, positivity makes phi the actual ground state;
its normalization selects the same unique vacuum as any other exact chart
of this Hamiltonian. The missing inverse fiber is thus a change of
representation or a new construction at another parameter, not an
additional positive physical vacuum at the same finite Hamiltonian.

## 2. A gap theorem that does not require an exact reference vacuum

Suppose the physical excited complement is nonempty and K_phi has a
proved physical gap g_phi>0 above its constant eigenfunction. Let E0,E1
be the first two eigenvalues of A restricted to the physical space.
Boundedness of R_phi and min-max give

```text
E1 >= g_phi + inf R_phi.
```

The normalized test vector 1 in L2(nu_phi) corresponds to phi in L2(mu).
Its Rayleigh quotient gives E0<=nu_phi(R_phi). Hence

```text
gap_phys(A) >= g_phi - [nu_phi(R_phi)-inf R_phi]
            >= g_phi - osc R_phi.                       (TR2)
```

This is a direct proof for the actual operator through an approximate
positive reference. It does not solve the nonlinear vacuum equation.
It shows that the user is right about a possible alternative route: the
original vacuum construction need not be the only route to a gap bound.
The reference gap and the residual comparison are its explicit ports.

This is a min-max and variational comparison, not a new attribution of
the min-max principle. It is a sufficient certificate and may be weak.
For example, even at phi=1 the direct bounded-potential estimate on a
small graph can outperform the oscillation-only version of TR2.

## 3. Construct a reference for every coupling

Choose a real c>=0 and normalize

```text
phi_c=exp(cS)/||exp(cS)||_2.
```

This is an explicit positive gauge-invariant function on the full link
space for every finite G and every c. From T S=6S,

```text
R_c=(6c-r)S-(c^2/2)|grad S|^2.
```

Choosing c=r/6 cancels the first-order source exactly:

```text
phi_r=exp(rS/6)/||exp(rS/6)||_2,
R_r=-(r^2/72)|grad S|^2.                                (TR3)
```

The reference exists at arbitrary coupling. It is generally not the
actual vacuum: its residual is not constant. This is a retained
separating witness, not a reason to discard the reference.

Its reference measure is explicit: log density is (r/3)S plus a constant.
Each edge meets at most m=2(d-1) plaquettes, and each plaquette has four
distinct edges. Let n_ij count plaquettes containing both i and j. Since
|a_p|<=1, one-link log-density oscillation and four-point mixed oscillation
are bounded by

```text
D_i <= (2r/3)m,
D_ij <= (4r/3)n_ij,
sum_(j!=i) n_ij <= 3m.
```

Changing the exterior only at j changes the conditional law at i by at
most tanh(D_ij/4)<=D_ij/4 in probability total variation. Therefore

```text
q=max_i sum_j c_ij <= mr.
```

For mr<1, the accepted continuous conditional-update proof and the
one-link Haar gradient constant 1/3 apply directly. They do not require
constructing an actual vacuum or estimating its Fourier norm. They give
the common, exterior-uniform block constant

```text
C_ref(r)=exp(2mr/3)/[3(1-mr)].
```

The reference measure is gauge invariant, so the accepted
forest-complement identity holds for it. Its direction cover therefore
proves

```text
g_phi >= [d/(d-1)] (3/2)(1-mr) exp(-2mr/3),
0<=r<1/m.                                               (TR4)
```

This reference-gap window is strictly larger than the previous actual
vacuum construction window 0<=r<9/(128m). The distinction is essential:
TR4 is a theorem about K_phi. Only TR1–TR2, or another proved residual
transfer, would turn it into a bound for A. It is not a newly enlarged
actual YM coupling window.

## 4. An exact extensive residual obstruction

Use N elementary squares with disjoint edge sets, joined into one
connected open lattice subgraph by paths that are bridges and create
no additional plaquette. For example, place square k at x=3k,3k+1 and
y=0,1, and connect the bottom corners of successive squares along y=0.
All these graphs belong to the admitted carrier. Their distinct square
edge variables are independent in product Haar measure; their bridge
variables do not enter S.

The accepted metric identity |grad a_p|^2=4(1-a_p^2), together with
disjoint edge supports, gives the exact relation

```text
|grad S|^2=4 sum_(p=1)^N (1-a_p^2),
R_r=-(r^2/18) sum_(p=1)^N (1-a_p^2),
inf R_r=-Nr^2/18,       sup R_r=0,
osc R_r=Nr^2/18.                                       (TR5)
```

Both extrema are attained: each plaquette holonomy can independently
have trace coordinate zero or absolute trace coordinate one. Bridge
values can be chosen arbitrarily. The witness is exact on SU(2), not
a spin cutoff or simulation.

The sharper loss in TR2 is extensive as well. Under this explicit
reference, each a_p has the tilted Haar trace law proportional to
exp((r/3)a) times its symmetric Haar law. Consequently

```text
nu_phi(R_r)-inf R_r
 = (Nr^2/18) E_tilt[a^2] >= Nr^2/72.                    (TR6)
```

For the last inequality, Haar has E[a^2]=1/4. Symmetry replaces the
tilt by cosh((r/3)a). Both a^2 and cosh((r/3)a) increase with |a|.
Their covariance is nonnegative, as follows by averaging the product
(x^2-y^2)(cosh(rx/3)-cosh(ry/3)) over two independent Haar trace values.
Division by the positive mean of cosh proves the claim.

Thus a fixed positive lower certificate from TR4 minus this bulk loss
eventually becomes inconclusive at every fixed r>0. The displayed bound
is what fails; TR5–TR6 do not show that the actual gap vanishes. Local
energy contributions may change ground and excited energies together,
and a bulk oscillation estimate throws that cancellation away.

This is a concrete next requirement for a direct reference route: control
the residual's effect on excitation energy uniformly in volume, rather
than charge its entire accumulated variation against one excitation.

## 5. Alternatively, calibrate the actual correction locally

Write the actual vacuum as psi=phi_r exp(v) up to a normalizing scalar.
The product rule in TR1 gives

```text
R_r+K_phi v-(1/2)|grad v|^2=E0.
```

The scalar is not missing information: integrating with respect to the
reference measure gives

```text
E0=nu_phi(R_r)-(1/2)nu_phi(|grad v|^2),
K_phi v=-Q_phi R_r+(1/2)Q_phi |grad v|^2,
Q_phi h=h-nu_phi(h).                                   (TR7)
```

This is the exact equation the newcomer reference must learn. The
positive gap of K_phi provides an L2 Poisson inverse, but the conditional
readout requires stronger, local control. Define

```text
d_v=max_i osc_i(2v),
b_v=max_i sum_(j!=i) mixedosc_ij(2v).
```

Here mixedosc_ij is the supremum of the four-point difference obtained
by independently replacing coordinates i and j. Direct conditional
log-density comparison gives

```text
D_actual <= 2mr/3+d_v,
q_actual <= mr+b_v/4.
```

If actual corrections satisfy d_v<=D and b_v<=B uniformly in G, with
mr+B/4<1, then the conditional proof and forest cover yield

```text
gap_phys(A)
 >= [d/(d-1)](3/2)(1-mr-B/4) exp(-2mr/3-D).             (TR8)
```

This conditional theorem allows a new reference to carry the main
variation. It does not require the *total* actual log vacuum to fit the
old anchored-norm ball. The all-volume bounds on the *actual* v solving
TR7 are OPEN. An approximate residual or a trial correction cannot be
substituted for those ports without an error estimate. The general
transition law and a collective-dependence counterexample are in
[VACUUM_ATLAS.md](VACUUM_ATLAS.md).

## 6. Why applying the same old estimate to the new chart is insufficient

There is an exact control against a cosmetic restart. In the accepted
anchored norm let t=4mr bound ||r T^-1 S||_*, and write b=8/9 for
half the accepted bilinear constant. The first-order reference is
w=r T^-1 S=rS/6. Expanding the old fixed-point equation u=w+(1/2)B(u,u)
at u=w+v gives the sufficient scalar majorant

```text
Z = b t^2 + 2bt Z + b Z^2,       Z bounds ||v||_*.
```

Put Y=t+Z. The equation becomes exactly

```text
Y=t+bY^2.
```

Thus the same absolute norm estimates reproduce the same discriminant
condition t<1/(4b)=9/32, equivalent to r<9/(128m). A new name for the
reference does not improve those estimates. The conditional ports TR8
or a sharper excitation comparison in TR2 provide genuinely different
ways to seek an improvement.

## 7. Result and limits

The user-proposed handoff is a valid mathematical route. This note
constructs an explicit reference, proves its larger-window reference
gap, carries its exact operator residual, and exhibits the all-volume
obstruction to the first residual-transfer estimate. It also identifies
an alternative local calibration theorem and the exact equation whose
solution must supply its missing bounds.

All general claims above are written proofs using accepted YM/conditional
identities, elementary product rules and min-max. New finite rational
checks corroborate their constants and separating cases; they do not
establish the general theorems by sampling. No actual YM coupling-window
extension, infinite-volume construction or continuum mass-gap result is
claimed. The previous 3/2 cover result and its frozen archive are unchanged.
