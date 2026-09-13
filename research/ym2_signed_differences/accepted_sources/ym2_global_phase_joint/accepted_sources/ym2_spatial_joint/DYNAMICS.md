# Shared-edge dynamics of two adjacent SU(2) plaquettes

12 September 2026. Bounded spatial continuation of
[the homogeneous joint/scaling note](../ym2_joint_scaling/JOINT_AND_SCALING.md).
This new carrier is a classical finite lattice regulator with open boundary.
It is not an exact spatial truncation theorem for continuum Yang--Mills.

**Result.** Two noncommuting configurations have the same individual
plaquette conjugacy classes and zero electric field, but different initial
magnetic-energy acceleration under the actual seven-link Hamiltonian. The
shared link feels the difference of two color forces brought to the same
vertex. Their relative orientation supplies a cross term which independent
plaquette classes discard.

## Contract and conventions

Use six vertices and seven oriented links:

```text
D ----c----> E ----d----> F
^           ^           ^
l           s           r
|           |           |
A ----a----> B ----b----> C
```

Every link carries `U_e in SU(2)` and a left-trivialized electric momentum
`E_e in su(2)`. Let the usual Pauli matrices be `sigma_a` and fix

`T_a=i sigma_a`, `[T_a,T_b]=-2 epsilon_abc T_c`,

`<X,Y>=-Tr(XY)/2`, so `<T_a,T_b>=delta_ab`.

Thus `E_e=sum_a E_e^a T_a` has squared norm `sum_a (E_e^a)^2`. All quantities
and time below are dimensionless reference variables. Using `i sigma/2`
while keeping the same coefficient vector norm would change the kinetic
normalization and its numerical accelerations. There is no unstated factor
of two convention.

Write `U=u0 I+i u.sigma`, equivalently a unit quaternion `(u0,u)`. Its product
has scalar part `u0 v0-u.v` and vector part `u0 v+v0 u-u cross v`.
The minus sign of that cross product matches this `+i sigma` convention.
For `X=x.T`, `ReTr(XU)/2=-x.u`.

Both plaquettes are counterclockwise:

`P_L=a s c^{-1} l^{-1}` based at A,

`P_R=b r d^{-1} s^{-1}` based at B.

Here the letters also denote their link matrices. Define

\[
 B(U)=\sum_{p=L,R}\left(1-\tfrac12\operatorname{ReTr}P_p\right),
 \qquad H(U,E)=\tfrac12\sum_{e=a,b,c,d,l,s,r}|E_e|^2+B(U).
 \tag{1}
\]

The phase carrier is `T*SU(2)^7` with its canonical cotangent symplectic
structure, subject to zero Gauss moment map at each vertex, modulo all
vertex gauge transformations. No boundary link is frozen and no exterior
plaquette is included. This is the open two-square graph, not a periodic
lattice with its wraparound identifications. Physical equality uses the
full `SU(2)^6` vertex gauge action.

The supplied ports are this graph, Hamiltonian, conventions, zero initial
electric fields, and the two individual plaquette classes. The missing port
is their relative color orientation after a specified transport. The first
requested readout is `B''(0)`, a necessary discriminator for the receiver
consisting of `B(t)` at all times in a supplied finite horizon `0<=t<=T`.
For a bounded operational enclosure also fix finite `H_max`; energy bounds
all electric momenta, and the link configuration space is compact.

## Gauge covariance and the actual equations

For one group element `g_v` at every vertex, independently,

`U_e -> g_source U_e g_target^{-1}`,

`E_e -> Ad(g_source) E_e`.

Every based plaquette transforms by conjugation at its base. The Hamiltonian
is invariant. Define the left gradient `G_e` by

`d/d epsilon B(...,exp(epsilon X)U_e,...)|0=<G_e,X>`.

It transforms as `G_e -> Ad(g_source)G_e`; its norm is gauge invariant.
The canonical equations in this trivialization are

\[
 \dot U_e=E_eU_e,\qquad \dot E_e=-G_e(U).
 \tag{2}
\]

The possible Lie-algebra coadjoint contribution from the isotropic kinetic
term vanishes: it is proportional to `[E_e,E_e]=0`.
The Gauss constraint at a vertex is

\[
 \Gamma_v=\sum_{s(e)=v} E_e
 -\sum_{t(e)=v}\operatorname{Ad}(U_e^{-1})E_e=0.
 \tag{3}
\]

It is automatic for `E=0`. Gauge invariance preserves it under (2).
Infinitesimal gauge invariance also gives the identity obtained by replacing
every `E_e` in (3) with `G_e`, which is an exact force-sign check.

At zero initial momentum, all configuration velocities and `B'(0)` vanish.
Differentiate `B'=sum_e<G_e,E_e>` and use (2):

\[
 \boxed{B''(0)=-\sum_e|G_e(U(0))|^2.}
 \tag{4}
\]

There is no directional Hessian term at this zero-velocity initial slice.
All seven terms use the kinetic metric of (1). Gauge-fixing a tree is
permitted to calculate them; deleting tree-link kinetic terms is not.
The reduced quotient metric generally couples the loop variables.

Smoothness on the compact link configuration manifold and energy control
of the electric momenta give complete finite-time evolution. Hence the
nonzero second-derivative separation below implies unequal magnetic-energy
functions on every sufficiently short positive interval. It is an actual
dynamical separation, not a straight-line probe of the potential.

## The common-base force and its sign

Use the source B of the shared link as the common base. Set

\[
 L=s c^{-1}l^{-1}a=a^{-1}P_La=l_0I+i\ell\cdot\sigma,
 \qquad R=P_R=r_0I+i r\cdot\sigma.
 \tag{5}
\]

Both now transform by `Ad(g_B)`, so `ell.r` is gauge invariant. Equivalently
one can transport the right loop to A using `a`; declaring the path is
essential. Directly pairing vectors at their original different bases
without transport does not have this invariance.

Vary the shared link by `s -> exp(epsilon X)s`. Cyclic trace invariance
turns the left contribution into `Tr(exp(epsilon X)L)` and the right into
`Tr(exp(-epsilon X)R)`. The latter sign comes from the inverse shared link.
Therefore

\[
 G_s=\ell-r,\qquad |G_s|^2=|\ell|^2+|r|^2-2\ell\cdot r.
 \tag{6}
\]

Each plaquette has three other links. Moving the varying factor around its
trace conjugates its vector and may reverse its sign. Conjugation preserves
the norm, so each outer link of the left face contributes `|ell|^2`, and
each outer link of the right contributes `|r|^2`. No other face acts on these
links in this open graph. Thus, for every admitted link configuration,

\[
 \boxed{\sum_e|G_e|^2
 =3|\ell|^2+3|r|^2+|\ell-r|^2
 =4(|\ell|^2+|r|^2)-2\ell\cdot r.}
 \tag{7}
\]

Individual classes fix `l0,r0`, hence `|ell|^2=1-l0^2` and
`|r|^2=1-r0^2`. They do not fix `ell.r`. In gauge-invariant loop language,
let

`w=ReTr(RL)/2=l0 r0-ell.r`.

The product `RL=b r d^{-1} c^{-1} l^{-1} a` is the perimeter loop based at B.
Here the italicized edge letter `r` in the path and the vector `r` in (5)
have different declared types. Equations (4) and (7) become

\[
 B''(0)=-8+4l_0^2+4r_0^2+2l_0r_0-2w.
 \tag{8}
\]

This is an explicit relational gluing term: the combined boundary loop
distinguishes configurations that the two separate face classes merge.

## Rational noncommuting witness

The five links `{a,b,l,s,r}` form a spanning tree. Set them all to identity
and choose `c=U^{-1}`, `d=V^{-1}`, so `L=U`, `R=V` in the common tree gauge.
In quaternion coordinates use

\[
 U=(3/5,4/5,0,0),\quad
 V_A=(3/5,0,4/5,0),\quad
 V_B=(3/5,12/25,16/25,0).
 \tag{9}
\]

All are unit quaternions; both `(U,V_A)` and `(U,V_B)` are noncommuting.
Both states have the same pair of individual classes, since both half
traces equal `3/5`; all electric fields vanish. Their exact values are:

| Readout | State A | State B |
|---|---:|---:|
| `|ell|^2=|r|^2` | `16/25` | `16/25` |
| `ell.r` | `0` | `48/125` |
| Perimeter half trace `w` | `9/25` | `-3/125` |
| `B(0)=H(0)` | `4/5` | `4/5` |
| `B'(0)` | `0` | `0` |
| Shared-link `|G_s|^2` | `32/25` | `64/125` |
| Full seven-link `sum |G_e|^2` | `128/25` | `544/125` |
| **`B''(0)`** | **`-128/25`** | **`-544/125`** |

For an explicit sign audit in this tree gauge, the gradients in edge order
`(a,b,c,d,l,s,r)` are

`(ell, r, -ell, -r, -ell, ell-r, r)`.

The six boundary-link contributions agree between the states; the shared
term differs. The acceleration difference is exactly `96/125` and the
small-time energy difference is `(48/125)t^2+o(t^2)`. Distinct perimeter
traces prove these states are not related by any vertex gauge transformation.

## Complete initial readout fiber and the evolving-state boundary

For fixed admitted individual half traces `l0,r0 in [-1,1]`, set
`a=sqrt(1-l0^2)`, `b=sqrt(1-r0^2)` and `d=ell.r`. Every value in
`[-ab,ab]` occurs: if `a,b>0`, take two vectors of lengths `a,b` with any
angle from zero to pi; if either length is zero, only `d=0` occurs.
Conversely Cauchy--Schwarz excludes every value outside this interval.
The complete initial-acceleration answer from these marginal classes and
`E=0` is therefore

\[
 B''(0)\in[-4(a^2+b^2)-2ab,\;-4(a^2+b^2)+2ab].
 \tag{10}
\]

It is `ONE(-4(a^2+b^2))` if `ab=0`, and `MANY(the entire interval)` if
`ab>0`. Inputs outside the half-trace domain are admission errors.
This is a complete readout fiber, not an exhaustive claim about continuum
field configurations. Supplying `d` repairs this readout by (7).

For this graph, a spanning tree identifies configuration gauge orbits with
pairs `(L,R)` modulo simultaneous conjugation. Their scalar parts and dot
product determine that joint orbit: any two vector pairs with equal lengths
and dot product have an isometry on their spans, extensible to `SO(3)` by
choosing the unused normal orientation. `SU(2)` covers this `SO(3)` action.
Thus the triple `(l0,r0,d)`, **together with the stipulated initial `E=0`**,
determines the whole initial phase-space gauge orbit and consequently its
future under the supplied Hamiltonian. This existence of a source decoder
does not itself give a closed evolving equation in the three static traces.
The slice `E=0` is not invariant, and later electric data are additional ports.
Do not assert autonomous spatial dynamics from static loop-trace closure.

Nor does (7) prove that one perimeter trace closes larger lattices. More
faces, independent loop vectors, transported electric momenta and Gauss
compatibilities introduce additional relationships. Exact dynamic spatial
aggregation and resolution-change laws remain OPEN beyond this declared
two-face result.

## Parameter transport and relation to earlier scaling

The homogeneous quartic amplitude scaling does not carry over unchanged to
compact group-valued links with the cosine-like plaquette potential.
For a declared finite-lattice family one can nevertheless prove a parameter
transport once and reuse it. Let

`H_{alpha,beta}=alpha/2 sum |E_e|^2+beta B`, with `alpha,beta>0`.

Define `tau=sqrt(alpha beta)t` and `P=sqrt(alpha/beta)E`. Then the equations
in `(U,P,tau)` are precisely (2) with unit coefficients. Gauss scales by the
same positive electric factor. At `E=0`,

`d^2 B/dt^2=-alpha beta sum |G_e|^2`.

This is a clock/momentum transport across a specified coupling family. It
preserves the witness separation with the same positive multiplier and
transports horizons and energy caps. It is not a spatial coarse-graining
theorem, a continuum limit, or an amplitude power law for the links.

## Evidence and reproduction

Equations (4)--(10), their gauge argument and parameter transport are written
derivations for this finite classical model. The numerical values are exact
rational checks, independently evaluated through quaternion derivatives and
2x2 complex matrices with rational real/imaginary components. There is no
floating-point time integration or simulation campaign.

Run from the repository root:

```powershell
python -I -B research/ym2_spatial_joint/check_dynamics.py
```

To refresh only this note's local receipt, append `--write-results`.
[The checker](check_dynamics.py) tests both noncommuting witnesses, a
nonconstant independent vertex gauge transformation of each, and central,
aligned, antialigned and three-component-vector controls. It checks every
link gradient against matrix differentiation, verifies the Gauss force
identity, checks force invariance when a plaquette orientation is reversed,
and rejects a naive two-chord unit kinetic metric. The recorded
[result](RESULTS_DYNAMICS.json) is finite execution evidence; it is not a
formal proof or a proof of the checker itself.

The strongest supported conclusion is that independent local plaquette
classes do not preserve even the initial magnetic-energy acceleration of
this actual constrained Hamiltonian when the faces share a link. The
common-base joint repairs this first seam exactly. There is no claim here
of a continuum Yang--Mills theorem, mass gap, quantum construction, minimal
storage, performance gain, or novelty over established lattice methods.
