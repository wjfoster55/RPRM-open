# Retained output support improves the actual-vacuum certificate

12 September 2026. Written finite-lattice result using accepted all-spin
construction and conditional-cover theorems. Publication remains on hold.

## Contract and dependency boundary

Use the carrier, positive-coordinate orientation, Fourier trace norm and
gauge constraints in [CANDIDATES.md](CANDIDATES.md). Write

```
T=-Delta/2, A=T-rS, S=sum_p a_p, a_p=Tr(U_p)/2,
B(f,g)=T^-1 Q Gamma(f,g),  m=2(d-1), x=mr, d=2 or 3.
```

The accepted all-spin gauge estimate is ||B(f,g)||_* <= ||f||_*||g||_*/3.
The source u0=rS/6 has norm at most 4x. The unknown mean-zero log vacuum
is u=u0+v. Its exact fixed-point equation is

```
v = h+B(u0,v)+(1/2)B(v,v),    h=(1/2)B(u0,u0).
```

The prior proofs provide the Banach-space closure, regularity, positivity,
uniqueness of the vacuum ray, and conditional/forest-cover transfer. They
are reused, not re-proved by the finite controls in this packet. The
new input below is a smaller bound on this exact h, obtained by retaining
its output channel and support. No term in the actual equation is dropped.

## New local source bound

The coefficient proof is [CHANNEL_SOURCE.md](CHANNEL_SOURCE.md). For two
adjacent squares put a=a_p, b=a_q, c=the merged-loop half-trace, and
h13=ab-c/4. The shared link has spin zero in c, spin one in h13:

```
Gamma(a,b) = 3c/4-h13,   Tc=9c,   T h13=13 h13.
```

The anchored norm counts an output only at its nontrivial link supports.
Thus the c channel contributes nothing when the anchor is the common link.
The inverse's output energy cancels the anchored energy weight exactly
once. The remaining weights, in the actual coordinate orientation, are:

| Pair type at its common link | Common-link anchor | Exterior-link anchor |
|---|---:|---:|
| No pure trivalent endpoint | 12 | 24 |
| One pure trivalent endpoint | 6 sqrt(3) | 6+6 sqrt(3) |

Here pure means all three positive-coordinate arrows enter the vertex, or
all three leave it. It is a coefficient-matrix partition property, not a
new physical orientation of the gauge field. The norm has retained its
original coordinate convention. Opposite signs in distinct channels
never cancel in this norm.

For an anchor in a full square lattice there is one common-link pair and
six exterior-link pairs, all of the first type. In a full cubic lattice
there are four first-type and two second-type common-link pairs, and
24 first-type and 12 second-type exterior-link pairs. To see completeness,
list the m squares through the anchor. A pair either shares the anchor,
or is specified uniquely by that square, one of its three other edges,
and one of the m-1 other squares through that edge. The latter description
never double counts: two elementary squares cannot share two distinct edges.
At an edge in three dimensions the four sides are +j,-j,+k,-k. Two equal
signs on distinct transverse axes give the second type (two of six pairs).
For a fixed square side, exactly one of the other three choices has its
sign and two have the opposite sign. This also gives the exterior census.
Deleting plaquettes for an open subgraph only removes nonnegative terms.

Each unordered adjacent pair enters h with coefficient r^2/36; each
self-square contributes 3r^2/8 to any of its anchors. Therefore

```
||h||_* <= kappa_d r^2,
kappa_2 = 3/4 + (12+6*24)/36 = 61/12,
kappa_3 = 3/2 + [4*12+2*6sqrt(3)+24*24+12*(6+6sqrt(3))]/36
        = 125/6 + 7sqrt(3)/3.
```

This improves the preceding coefficients 65/12 and 59/2. For both d,

```
kappa_d/m^2 <= 25/16,     so ||h||_* <= (25/16)x^2.       (OC1)
```

For d=2 compare 61/48 < 25/16. For d=3,
(125+14sqrt(3))/96 < 150/96 because 588<625. These are exact inequalities.
The local census is exhaustively recomputed by incidence_probe.py; its
general use on every admitted graph rests on the deletion and local-star
argument, not extrapolation from a large simulation.

## Actual construction and two explicit physical-gap certificates

For a closed ball ||v||_*<=Z, the exact map and its Lipschitz constant obey

```
M_x(Z) = (25/16)x^2 + (4/3)xZ + Z^2/6,
L_x(Z) = (4x+Z)/3.
```

If M_x(Z)<Z and L_x(Z)<1, the accepted fixed-point/elliptic argument gives
the smooth positive actual vacuum. The actual probability density is
proportional to exp(2u), with the accepted conditional bounds

```
q <= x+4Z/3,    D <= 2(x+Z)/3,
gap_phys(A) >= [3d/(2(d-1))](1-q) exp(-D).               (OC2)
```

These estimates hold for every exterior configuration and uniformly in
graph size. The physical excited complement is assumed nonempty; on a
tree the corresponding form inequality is vacuous. The potential has
its original sign. An additive energy constant does not alter this gap.

At the preceding reported window x<=1/3, take Z=7/20. Then

```
Z-M_x(Z) >= 1/2400,   L_x(Z)<=101/180,
q<=4/5,             D<=41/90,
gap_phys(A) >= [3d/(10(d-1))] exp(-41/90).              (OC3)
```

At the enlarged window x<=7/20, take Z=5/12. Then

```
Z-M_x(Z) >= 13/6912, L_x(Z)<=109/180,
q<=163/180,          D<=23/45,
gap_phys(A) >= [17d/(120(d-1))] exp(-23/45).            (OC4)
```

All inequalities are strict in the fixed-point ports at the displayed
endpoints, so these are closed intervals. Monotonicity in nonnegative x
extends each endpoint check to the entire interval. For d=3, OC3 supplies
about 0.2853 in electric-energy units through r=1/12; OC4 supplies about
0.1275 through r=7/80. The latter coupling window is 5% larger than the
previous simple endpoint r=1/12. These are sufficient bounds, not optimal
thresholds or measurements of a physical phase transition.

## What still fails, and why

The positive fixed-point root is available up to

```
x < 1/[4/3+5/sqrt(24)].
```

This statement constructs the vacuum; it does not automatically make
OC2 positive. The permitted conditional radius requires Z<3(1-x)/4.
Substitution into M_x(Z)-Z gives

```
32[M_x(3(1-x)/4)-3(1-x)/4] = 21x^2+50x-21.
```

Thus this scalar certificate loses its simultaneous strictly positive
conditional margin at x=(sqrt(1066)-25)/21, about 0.3643, before the
construction root disappears near 0.4248. Neither event proves a gap
closes. They identify different limitations of this estimate.

The companion [SPECTRAL_CHANNEL.md](SPECTRAL_CHANNEL.md) proves a sharper
obstruction to one attractive shortcut: a fixed positive resolvent shift
improves each finite pair of channels, but gives no uniform strict norm
factor over all spins, even on a single square and on genuine bilinear
source terms. Modes with arbitrarily large kinetic energy make that
factor tend to one. A new moving reference therefore needs a tail or
relative-scale estimate; changing the coordinate by itself supplies none.

In physical units multiply OC3/OC4 by E_el. In the inherited lattice
normalization r=8/g_b^4 and E_el=g_b^2/(4a). The small-bare-coupling
continuum route requires r to grow without bound; these finite r windows
do not reach it. Continuum existence, a nontrivial limiting theory and a
positive excitation scale after the limits remain OPEN. This is useful
local progress on an interacting lattice problem, with no quantum
Yang-Mills continuum mass-gap claim or literature-priority claim.
