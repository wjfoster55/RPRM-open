# Sliding the three hoops: independent geometry audit

Date: 2026-09-12. Evidence: **written proofs for the declared family**, plus numerical evaluation of the displayed margins. No formal proof, numeric-label decoder, or BSD identity is supplied.

The three small hoops can move closer along their shared connector without changing the link. A small hoop can then cross both other small-hoop traces in a projected view. The connector nevertheless remains the unique component *linked* to three others. The stronger projection claim in [view 14](../../bsd-keyring-view-14/README.md) used the original equal spacing and does not extend to this family.

## Contract and moving family

Take `R=3`, `r=3/4`, `ez=(0,0,1)`, and `e(theta)=(cos theta,sin theta,0)`. Define

\[
C(t)=R e(t),\qquad
S_j(u;a,\phi)=(R+r\cos u)e(\phi+ja)+r\sin u\,e_z,
\quad j\in\{-1,0,+1\}.
\]

The parameters `t,u,phi` are angles modulo `2pi`; the slider has the closed range `pi/15 <= a <= 2pi/3`, or 12 to 120 degrees. `a=120 degrees` recovers the original equally spaced shape up to phase and labels. Reducing `a` actually moves the outer two hoops toward the middle hoop. Changing `phi` slides the group around the connector. A further `Q in SO(3)` rigidly rotates every point, or equivalently changes the camera relative to the object.

The carrier consists of these labelled four-circle states with parameters `(a,phi,Q)`. Spatial point equality tests collision; equal component occurrences retain their labels. Supplied ports are this geometry and these operations. The requested receivers are (i) disjointness and linking, (ii) projected trace intersection. They are different receivers. All centerline points stay inside the ball of radius `R+r=15/4`.

Sliding along an admitted path is reversible by reversing that path. A rigid rotation has inverse `Q^-1`. Orthographic projection forgets depth and generally has no inverse. The complete parameter-state fiber of the linking-matrix readout is the whole declared carrier, because the proof below gives the same matrix at every state. This does not claim to classify every spatial link with that matrix.

## Exact separation, including overlapping enclosing balls

For two distinct angular positions `theta,psi`, put `Delta=theta-psi`, `rho_u=R+r cos u`, and `z_u=r sin u`. Since `rho_u >= R-r > 0`,

\[
\begin{aligned}
\|S_\theta(u)-S_\psi(v)\|^2
&=(\rho_u-\rho_v)^2
  +2\rho_u\rho_v(1-\cos\Delta)+(z_u-z_v)^2\\
&\ge 2(R-r)^2(1-\cos\Delta).
\end{aligned}
\]

Equality is attained at `u=v=pi`, so the exact minimum is

\[
\operatorname{dist}(S_\theta,S_\psi)
=2(R-r)|\sin(\Delta/2)|.
\]

Thus distinct angular positions give disjoint small circles even when their radius-`r` enclosing balls overlap. Each small-circle point is still exactly distance `r` from `C`: the nearest connector point has its horizontal angle, and the squared distance is `(r cos u)^2+(r sin u)^2`.

In the chosen slider range the smallest circular separation among `-a,0,a` is `a`, including the endpoint `a=120 degrees`. Therefore the global small-circle separation is at least

\[
2(R-r)\sin(6^\circ)=0.4703780847044405\ldots.
\]

For geometric tubes of small-hoop radius `0.075` and connector radius `0.055`, the guaranteed inter-tube margins are therefore at least `0.4703780847-0.15 > 0.3203780847` between small hoops and `0.75-0.075-0.055=0.62` from a small hoop to the connector. Each individual tube radius is below its circle radius, so its own standard round tube is embedded. These physical radii are distinct from a renderer's screen-space stroke width.

The adjacent small tubes would first touch at `a=2 arcsin(1/30)`, approximately `3.8204263434 degrees`, below the permitted minimum. Zero-width centerlines can approach arbitrarily closely as `a` tends to zero, but `a=0` makes the three circles coincide. Extending the symmetric family to `a=pi` makes the two outer circles coincide. Those endpoints are admission failures for four disjoint labelled circles.

## Continuous motion and preserved links

There is an explicit ambient isotopy, rather than only a succession of unrelated pictures. First set `phi=0` and let `a_s` be any continuous slider path from `a_0` to `a_1`. On `[-pi,pi]`, let `h_s` be the piecewise linear increasing map sending the five knots

\[
(-\pi,-a_0,0,a_0,\pi)\quad\hbox{to}\quad
(-\pi,-a_s,0,a_s,\pi).
\]

All segment slopes are positive because `0<a_s<pi`, and `h_0` is the identity. Extend modulo `2pi`. In cylindrical coordinates, the maps

\[
H_s(\rho\cos\theta,\rho\sin\theta,z)
=(\rho\cos h_s(\theta),\rho\sin h_s(\theta),z)
\]

are homeomorphisms for `rho>0` and extend continuously by the identity on the vertical axis. Their inverses use `h_s^-1` and also vary continuously. Thus `H_s` is an ambient isotopy. It preserves the connector circle as a set and sends each initial small hoop to its assigned moving hoop. Phase changes and spatial rotations can be composed with it. This explicit construction establishes topological isotopy; its piecewise linear angle map is not being claimed to be a smooth ambient diffeomorphism.

The original [keyring audit](../../bsd-keyring-13/agents/KEYRING_AUDIT.md) computes each connector/satellite linking number as `-1` for increasing parameters. Its proof works unchanged at every `theta`: the satellite meets the connector's planar spanning disk exactly once, at `(R-r)e(theta)`, transversely with negative vertical velocity.

For completeness, the small hoop's spanning disk consists of

\[
(R+b)e(\theta)+c e_z,\qquad b^2+c^2\le r^2.
\]

Every disk point has strictly positive horizontal radius and the unique angle `theta`. Distinct-angle disks are consequently pairwise disjoint, whether or not their enclosing balls overlap. They prove that the satellite sublink remains an unlink. In component order `(C,S_-1,S_0,S_+1)`, the absolute linking matrix is everywhere

\[
\begin{pmatrix}
0&1&1&1\\1&0&0&0\\1&0&0&0\\1&0&0&0
\end{pmatrix}.
\]

The union still has four connected components. Its linking-incidence graph is the connected star with degree sequence `(3,1,1,1)`. Sliding, group phase, and rigid view rotation preserve this receiver.

## An explicit clustered counterview

Take `phi=0`, `a=pi/6` (30 degrees). Look along the unit vector

\[
n=(0,\sqrt{99}/10,1/10),
\]

with orthonormal screen coordinates

\[
P(x,y,z)=(X,Y)=\left(x,\frac{\sqrt{99}z-y}{10}\right).
\]

This view is tilted out of the connector plane, so the connector projects to a nondegenerate ellipse. All three small hoops also project to nondegenerate ellipses. Put `c=cos a`. The filled projected disk of either outer small hoop is exactly `F_+(X,Y)<=1` or `F_-(X,Y)<=1`, where

\[
F_\pm(X,Y)=
\left(\frac{X/c-R}{r}\right)^2+
\left(\frac{10Y\pm X\tan a}{\sqrt{99}\,r}\right)^2.
\]

The middle small hoop contains the two projected points `p_in=(R-r,0)=(9/4,0)` and `p_out=(R+r,0)=(15/4,0)`. For each outer ellipse,

\[
F_\pm(p_{\rm in})=(2\sqrt3-4)^2+\frac1{33}
=0.3174901092\ldots<1,
\]

while at `p_out` the first squared term alone exceeds one because

\[
\frac{(15/4)/c-R}{r}=\frac{10\sqrt3}{3}-4>1.
\]

Each of the middle hoop's two arcs from `p_in` to `p_out` therefore crosses the boundary of each outer ellipse, by continuity. Consequently the middle small-hoop trace intersects **both** other small-hoop traces in this explicit orthographic view. These are projection intersections between spatially disjoint, pairwise unlinked small hoops. The strict inside/outside inequalities also make the existence of these intersections persist under sufficiently small changes of view.

The same overlap is easy to see in the exactly horizontal limiting view `P(x,y,z)=(x,z)`: the outer traces coincide with each other, and the middle trace intersects them at `cos u=-4 tan^2(15 degrees)`, with nonzero sine and cosine. Those pairwise intersections are transverse. The tilted witness above avoids relying on the edge-on collapse to establish the requested overlap.

## Boundary of the correction

View 14's equal-spacing estimate remains valid for that embedding. The newly permitted slide changes its center distances and invalidates reuse of that estimate. The explicit witness proves that the middle satellite can meet both other satellite traces in projection after sliding; therefore the earlier universal exclusion of that visual behavior cannot be applied here.

The topological hub is still unique. Projected intersection, depth order, visible centrality, and linking are separate questions. This audit does not classify every camera direction or calculate a complete projected-crossing diagram, and it does not supply a law transporting this geometry into the analytic/arithmetic BSD readouts.

Verification performed: direct algebraic derivation of the exact minimum-distance formula, explicit ambient isotopy, disjoint spanning disks, and exact ellipse inside/outside witnesses. Python 3 standard-library evaluation independently recomputed the displayed finite margins and witness decimals. No height computation or prior-lane replay was run.
