# A global tree phase carrier for the two-plaquette graph

12 September 2026. This is a continuation of the fixed classical open graph
in [DYNAMICS.md](accepted_sources/ym2_spatial_joint/DYNAMICS.md) and the regular trace chart
in [PHASE_CLOSURE.md](accepted_sources/ym2_spatial_joint/PHASE_CLOSURE.md). Those files remain
unchanged. The new result closes their global-coverage obligation for this
graph by retaining two group elements and their electric momenta, with one
residual Gauss constraint and simultaneous conjugation equality. No inverse
trace discriminant is used.

## 1. The new contract

The source is the same seven-link cotangent Hamiltonian system on
`T*SU(2)^7`, at zero Gauss, modulo the full six-vertex gauge group. Its edge
occurrences, orientations and reference normalization are unchanged:

```text
D ----c----> E ----d----> F
^           ^           ^
l           s           r
|           |           |
A ----a----> B ----b----> C

H_source = (1/2) sum_e |E_e|^2 + 2-Sc(L)-Sc(R),
L=s c^-1 l^-1 a, R=b r d^-1 s^-1.
```

Here `Sc` is normalized trace. Edge names and half-trace coordinates below
have separate declared types even where the same letter is used. Use
`T_i=i sigma_i`, `<X,Y>=-Tr(XY)/2`, and `[X,Y]=-2 X cross Y` in vector
coordinates. A quaternion product has the **minus** vector cross term:

```text
(a,u)(b,v) = (ab-u·v, a v+b u-u cross v).
```

The intermediate, globally smooth carrier is

```text
Z = T*SU(2)^2 = {(U,V,P,Q): |U|=|V|=1, P,Q in R^3}.
```

Its canonical one-form is
`theta=P·(dU U^-1)+Q·(dV V^-1)`; momenta use the same vector norm as the
source. Put `S=Ad_(U^-1)P` and `R_e=Ad_(V^-1)Q`. The subscript distinguishes
the electric vector `R_e` from the named right loop. The physical target is

```text
Z_phys = {z in Z: Gamma(z)=P-S+Q-R_e=0} / SU(2),           (G1)
```

where the residual action conjugates `U,V` and applies the same adjoint
rotation to `P,Q`. Physical equality is exactly this orbit equality. Thus
the target can have singular quotient strata; it is not asserted to be one
global six-coordinate Darboux chart.

The supplied ports are a lawful phase state, this graph and Hamiltonian,
and an elapsed time. The operation is Hamiltonian continuation, enabled for
every real elapsed time. Its receiver retains every gauge-invariant phase
observable and subsequent Hamiltonian continuation of this graph. A bounded
operational request may fix finite energy `H<=H_max` and a finite horizon
`|t|<=T`; the theorem does not replace those bounds by a simulation.
Malformed quaternions or a nonzero residual Gauss value are admission errors
for `Z_phys`. A complete admitted target orbit has **ONE physical source
gauge class**. The full raw source fiber is described in section 3.

## 2. Global tree gauge and the canonical momentum definitions

Root the spanning tree `{a,b,l,s,r}` at B. Gauge transformations act by

```text
U_e -> h_source U_e h_target^-1,
E_e -> Ad_(h_source) E_e.
```

For any source configuration, the unique tree gauge transformation with
`h_B=I` is

```text
h_A=a^-1, h_C=b, h_D=a^-1 l, h_E=s, h_F=b r.            (G2)
```

These formulas are global: they involve products and inverses of group
elements, with no alignment test or division by a trace coordinate. They
make the five tree links identity and give

```text
c'=a^-1 l c s^-1=U^-1, d'=s d r^-1 b^-1=V^-1,
U=L, V=R.
```

A gauge transformation between two tree configurations must be constant
at every vertex, because its endpoint values agree on every tree edge.
The only remaining configuration action is simultaneous conjugation.

On the tree slice the original one-form has only chord terms. The identity

```text
d(U^-1) U = -Ad_(U^-1)(dU U^-1)
```

therefore fixes the canonical momenta, including their signs:

```text
P = -Ad_U E_c', Q = -Ad_V E_d'.                       (G3)
```

Here primes mean that (G2) has already acted on the source electric fields.
In particular these are not the bare electric vectors of the two chord
links. In arbitrary source coordinates a direct global decoder is

```text
U=s c^-1 l^-1 a, V=b r d^-1 s^-1,
P=-Ad_U Ad_(a^-1 l)E_c,
Q=-Ad_V Ad_s E_d.                                    (G4)
```

## 3. All seven electric fields, all Gauss constraints, and the full fiber

In the tree gauge (G3) gives `E_c=-S`, `E_d=-R_e`. The five Gauss equations
at vertices other than B now solve successively without an inverse matrix:

```text
A: E_a+E_l=0;       D: E_c-E_l=0;
C: E_r-E_b=0;       F: -Ad_V E_d-E_r=0;
E: E_d-Ad_U E_c-E_s=0.
```

Consequently the unique reconstructed fields are

```text
E_a=S, E_b=Q, E_c=-S, E_d=-R_e,
E_l=-S, E_s=P-R_e, E_r=Q.                             (G5)
```

The last constraint, at B, is exactly
`E_b+E_s-E_a=P-S+Q-R_e=Gamma`. This proves both directions:

1. Every zero-Gauss source state gives an admitted `(U,V,P,Q)` by (G4).
2. Every admitted `(U,V,P,Q)` reconstructs a zero-Gauss source by the tree
   links and (G5).

The constructions are inverse on their physical orbits. If two source
states give the same target orbit, apply their based tree gauges and then
the residual constant gauge transformation relating the two target
representatives. Equation (G5) relates every electric field as well. The
original source states are therefore gauge equivalent. Conversely every
source gauge transformation changes its decoded representative only by
the constant transformation at B.

For a supplied target orbit `[z]`, the complete raw fiber is

```text
{g · reconstruction(z): g in SU(2)^6}.                (G6)
```

Changing the representative of `[z]` leaves this set unchanged. Stabilizers
can give repeated parameters in (G6); they do not create extra physical
classes. Thus the fiber is ONE at the physical equality declared in section
1, including aligned, antialigned and central configurations. There is no
unclassified mirror branch.

There is also a direct symplectic argument. Based gauge transformations
`h_B=I` act freely at every configuration: a transformation fixing all
links is forced to be identity by the tree. Zero Gauss at the five non-root
vertices says exactly that the canonical one-form annihilates these gauge
directions. Equations (G2) and (G5) give a global section of this reduction,
and its one-form is the canonical form in section 1. Taking its exterior
derivative identifies the reduced symplectic form with that of `Z`.
The remaining B gauge action has moment map (G1). This separates a smooth
global tree reduction from the final possibly singular residual quotient;
no assertion about a smooth quotient at every orbit is needed.

## 4. Hamiltonian and signs of the complete global vector field

Substituting **all seven** fields of (G5) into the kinetic energy gives

```text
2 K = 3|S|^2+|R_e|^2+2|Q|^2+|P-R_e|^2,

K = 2(|P|^2+|Q|^2)-P·Ad_(V^-1)Q,
H_tree = K+2-a-b, a=Sc(U), b=Sc(V).                  (G7)
```

The tree links retain their kinetic contributions. For example, a single
central left circulation `P=e1,Q=0` has `K=2`, not the `1/2` supplied by a
naive two-chord kinetic metric.

Let

```text
A_e=4P-Ad_(V^-1)Q,
B_e=4Q-Ad_V P.                                      (G8)
```

The subscript distinguishes Lie-algebra velocities from graph vertices.
For the right Maurer velocity `X=dot U U^-1`, variation of the canonical
action gives

```text
dot U=(partial_P H) U,
dot P=[partial_P H,P]-grad_U H,                      (G9)
```

with the same formula for V,Q. To audit the Euler sign directly, put
`eta=delta U U^-1`; then `delta X=dot eta+[eta,X]`. Integration by parts
in `P·X-H` gives `dot P=[X,P]-grad_U H`. The magnetic gradient of `-Sc(U)`
is `u=Vec(U)` since `Sc(eta U)=-eta·u`.

The kinetic term is independent of U. Under `delta V=eta V`,

```text
delta(Ad_(V^-1)Q)=Ad_(V^-1)[Q,eta],
grad_V K = [Q,Ad_V P] = [B_e,Q].
```

The Q Euler term thus cancels its kinetic configuration gradient, yielding
the global equations

```text
dot U=A_e U,               dot V=B_e V,
dot P=[A_e,P]-u,           dot Q=-v.                 (G10)
```

These formulas apply on all of `Z`; physical source states additionally
satisfy Gamma=0 and residual orbit equality. Their quaternion version is
polynomial on the unit-quaternion submanifold:

```text
dot a=-A_e·u, dot u=a A_e-A_e cross u,
dot b=-B_e·v, dot v=b B_e-B_e cross v,
dot P=-2 A_e cross P-u, dot Q=-v,

Ad_(a,u)z=(a^2-u·u)z+2(u·z)u-2a(u cross z).          (G11)
```

No expression divides by `Delta=|u cross v|^2` or by a vector length.

A second sign derivation uses the full graph dynamics. At a tree
representative, impose a compensating time-dependent gauge transformation
with infinitesimal value `omega_B=0` to keep the tree links identity:

```text
omega_A=-S, omega_C=Q, omega_D=-2S,
omega_E=P-R_e, omega_F=2Q.
```

Then the transformed chord velocity is
`E_c+omega_D-Ad_(U^-1)omega_E=-Ad_(U^-1)A_e`, with the analogous d result
`-Ad_(V^-1)B_e`. Differentiating (G3), while using the source electric
equation and its gauge correction `[omega_source,E_e]`, gives exactly
(G10). The checker instead differentiates the general formulas (G2)-(G4)
on arbitrary source representatives, so it does not reuse these
compensating-gauge formulas as its source calculation.

## 5. Global preservation, inverse flow, and boundedness

The Hamiltonian and canonical form in sections 2-4 are obtained by an
invertible smooth based reduction. Therefore the full Hamiltonian vector
field projects to (G10). This is equality of vector fields on the whole
tree carrier after based reduction, not an inference from a few matching
initial derivatives.

The remaining Hamiltonian is invariant under simultaneous conjugation.
Its moment map Gamma is conserved, so its zero level is invariant; the
flow is equivariant and gives a unique projected continuation on every
residual orbit. These statements hold even where the quotient is singular.

For global existence, Cauchy--Schwarz gives

```text
K >= (3/2)(|P|^2+|Q|^2), 2-a-b >= 0.                (G12)
```

Conservation of H bounds the momenta on every finite-energy trajectory,
and `SU(2)^2` is compact. The smooth vector field thus cannot escape every
compact subset in finite time, in either direction. Standard local ODE
existence and uniqueness extend it for all real time. Projection through
the quotient preserves that unique orbit evolution; this is not a claim
of an ordinary smooth ODE chart on every quotient stratum.

Let `C` be the source-to-target orbit map just proved bijective, `Phi_t`
the physical source flow, and `Psi_t` the orbit flow of (G10). Then

```text
C(Phi_t(s))=Psi_t(C(s)) for every admitted s and t in R. (G13)
```

The inverse operation is `Psi_(-t)`. All gauge-invariant source readouts
factor through this map. In particular

```text
electric energy=K,
magnetic energy=2-a-b,
signed magnetic transfer=dot(2-a-b)=A_e·u+B_e·v,
outer Wilson half trace=w=Sc(VU)=Sc(UV).
```

The carrier preserves the all-time source continuation receiver for this
graph. It does not claim a smaller generic physical dimension than six.

## 6. Exact bridge to the frozen regular chart

On the old domain `Delta=|u cross v|^2>0`, let
`x=(a,b,w)` and let `(p_a,p_b,p_w)` be its canonical trace momenta. For
`delta U=XU`, `delta V=YV`, cyclicity gives

```text
delta a=-u·X, delta b=-v·Y,
delta w=-Vec(UV)·X-Vec(VU)·Y.
```

The canonical one-form equality `p·delta x=P·X+Q·Y` therefore gives

```text
P=-p_a u-p_w Vec(UV),
Q=-p_b v-p_w Vec(VU).                               (G14)
```

This agrees with the frozen full-link lift `E=J^T p` after (G5), so (G7)
pulls back to its `(1/2)p^T M(x)p+2-a-b`. On Delta>0 the old cotangent
fiber proof supplies the inverse uniquely, up to the already-declared
residual conjugation. Equation (G14) can be evaluated at Delta=0 but need
not be onto the available phase states there. The new construction does
not try to repair that failure by inverting the old singular cometric.

At `U=V=I`, all finite old momenta give `P=Q=0` through (G14). The source
circulation `P=e1,Q=0`, reconstructed by (G5), has nonzero kinetic energy
2 and zero Gauss. It belongs to the new carrier. This recovers the exact
hostile state already identified as outside the old chart.

## 7. An exact trajectory crosses the old configuration boundary

Take the additional lawful state

```text
U=V=I, P=e1, Q=e2; Gamma=0, K=H=4.                  (G15)
```

Equations (G10)-(G11) give, at time zero,

```text
dot u=4e1-e2, dot v=-e1+4e2,
dot P=-2e3, dot Q=0.
```

Smoothness gives `u(t)=(4e1-e2)t+O(t^2)` and
`v(t)=(-e1+4e2)t+O(t^2)`. Consequently

```text
u(t) cross v(t)=15 e3 t^2+O(t^3),
Delta(t)=225 t^4+O(t^5).                             (G16)
```

Thus Delta is positive for every sufficiently small nonzero time, on both
sides of zero, while Delta(0)=0. Starting on either nearby regular
configuration and following toward zero reaches the old chart boundary
in finite time; (G10) continues uniquely through it. This proves that the
old regular configuration domain is not invariant under the full flow.
It is a Taylor consequence of the exact vector field, not a trajectory
simulation or a claim based on sampling a few times.

A distinction matters here: central **configuration** does not force a
singular **phase orbit**. At (G15), P and Q are independent, so their common
SO(3) stabilizer is trivial. The phase reduction is on its regular orbit
stratum while its old configuration chart fails. The new carrier also
includes actual singular phase strata, such as `U=V=I,P=Q=0`, without
requiring a local manifold chart there.

## 8. Evidence, reproduction, and coverage ceiling

Sections 2-7 are written mathematical derivations for the explicitly
declared finite classical graph. They are not proof-assistant results.
The adjacent [checker](check_tree.py) is an independent standard-library
implementation of exact rational quaternion first jets. It does not import
the earlier checkers and does not integrate a trajectory.

The [receipt](RESULTS_TREE.json) records 14 phase cases: six regular
configuration/momentum pairs, aligned and antialigned transverse-electric
states, one-central-factor states, two different central circulations,
negative central holonomies, and the zero equilibrium. Each is checked in
both the tree representative and a nonconstant independent vertex gauge.
For each it differentiates full seven-link loop words to obtain the source
force, differentiates the general tree decoder, and compares every one of
the 14 quaternion/momentum derivative components against (G10). It also
checks Gauss, energy and residual-Gauss derivatives, the energy bound, the
one-form with added gauge tangents, and the reconstruction round trip.
Six exact regular bridges compare (G14)-(G5) with the full-link trace
Jacobian lift and the old cometric. The central-exit coefficient 225 and
failure of the naive independent two-chord kinetic metric are separate
controls.

```powershell
python -I -B research/ym2_global_phase_joint/check_tree.py
```

The default command recomputes and byte-compares the stored receipt without
writing files. Add `--write-results` only to replace this new receipt.
It explicitly rejects optimized Python (`-O` or `-OO`) because its
verification conditions use assertions. The normal command above keeps
every condition active.
Finite checks corroborate the written derivations; they do not prove
universal soundness of the implementation or replace the coverage proof.

The previously OPEN singular-configuration continuation obligation is
closed for this exact seven-link graph by (G1)-(G13), including its actual
singular phase orbits. Extension to different graphs, spatial refinement,
continuum limits, quantization, and a quantum Yang--Mills mass gap remains
outside this carrier and is not established here.
