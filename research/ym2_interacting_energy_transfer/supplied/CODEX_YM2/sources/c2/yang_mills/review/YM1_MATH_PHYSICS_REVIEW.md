# YM1 independent mathematics and physics review

Date: 2026-09-12. Reviewer: independent YM1 math-review agent.

## Disposition and inspected scope

**PASS at the stated single-mode classical scope.** Inspected the actual
`../YM1_BRIDGE.md`, `../check_ym1.py`, and initial `../YM1_CHECK.json` after
the independent derivation below. No required mathematical or physical
correction was found. The bridge explicitly separates this receiver result
from the quantum negative control and from interacting Yang–Mills.
No simulation, historical suite, or independent code campaign was run by
this reviewer. The checker and receipt were inspected, not independently
executed: the recorded PASS covers five exact amplitude cases, four field
sampling cases at 16 periodic nodes, and four finite-box calibration
entries. These are calibrations rather than proof of untested general
claims. The written derivation supplies the general one-mode claim.

One minor citation-label correction was sent to the author: the precise
Jaffe–Witten existence/mass-gap statement is in section 4, with relevant
volume-uniform discussion in sections 5–6, rather than sections 1–3.
The zero-mode, flat-component, and homogeneous-quadratic distinctions
below were supplied as wording guards; the inspected bridge does not
assert triviality of every Wilson loop, recovery of linear signs, or a
gap between every pair of excited quantum levels.

Inspected repository instructions, `README.md`, `AGENT_HANDBOOK.md`, the YM1
task, the prior-owner card, and the supplied
`check_yang_mills_connections.py` / `YANG_MILLS_CONNECTION_CHECKS.json`.
Those inherited checks concern finite cubes and a two-photon calibration;
their evidence does not supply a Yang–Mills calculation.

The source Maxwell action, gauge invariance, Coulomb-gauge wave equation,
energy, and free quantum radiation Hamiltonian were checked in
[Tong, section 6, equations 6.493–6.524](https://www.damtp.cam.ac.uk/user/tong/qft/qfthtml/S6.html).
The periodic-box momentum convention was checked in
[Tong, section 2, equations 2.99–2.104](https://www.damtp.cam.ac.uk/user/tong/qft/qfthtml/S2.html).
The distinct non-Abelian quantum target and volume-uniform gap obligation
were checked in [Jaffe–Witten, sections 4–6](https://www.claymath.org/wp-content/uploads/2022/06/yangmills.pdf).
The calculations below are the reviewer's derivations from these supplied
physical laws, not new results asserted by those sources.

## Carrier, physical states, and normalization

Fix a spatial origin and mode basis on the periodic cubic three-torus with
side `L>0`, volume `V=L^3`, and `k=2π/L`. Use natural electromagnetic units.
The carrier is the continuous bounded ellipse
`X={(Q,P) in R² : (P²+k²Q²)/2 <= Emax}`, with fixed finite `Emax>0`.
Equality means equality of the physical initial fields in this fixed mode
sector; time shifts and spatial translations are physical operations, not
gauge identifications.

For `α=sqrt(2/V)`, the proposed fields are
`A_y=αQ cos(kx)`, `E_y=-αP cos(kx)`, `B_z=-αkQ sin(kx)`.
They obey the Coulomb condition and both divergence constraints. The
periodic integrals of the squared sine and cosine are `V/2`, so substitution
into the Maxwell Lagrangian gives `(Qdot²-k²Q²)/2`. Therefore the reduced
canonical momentum is `P=Qdot`; the minus sign in `E_y` is correct. The
Hamiltonian is exactly `(P²+k²Q²)/2`, with no added mass or energy term.

`Pdot=-k²Q` also satisfies both curl evolution equations. The resulting flow
`Q'=Qc+(P/k)s`, `P'=Pc-kQs`, where `c=cos(kt)` and `s=sin(kt)`, conserves
the Hamiltonian. It is total on `X` for every real finite time and invertible
by `t -> -t`. Thus the energy bound does not introduce hidden stopping
behavior, and the classical single-mode truncation is invariant under the
declared linear Maxwell dynamics.

The zero-mode restriction must mean vanishing harmonic electric mode,
vanishing flux sector, and a fixed trivial harmonic/flat component. It
must not mean that every Wilson loop of a radiative connection is trivial:
`A_y=αQ cos(kx)` can give nontrivial loops around the y-cycle at fixed x.
This sector restriction and fixed mode basis are physical coverage
assumptions, not conclusions of gauge fixing alone.

## Exact loss, repair, and complete fibers

The supplied ports are an initial retained summary and a time shift. The
missing requested port is the later integrated magnetic energy. Set
`u=UB=k²Q²/2`, `v=UE=P²/2`, and `r=(u,v)`.
For any reached `(u,v)`, the complete original-source fiber is
`{(σ sqrt(2u)/k, τ sqrt(2v)): σ,τ in {-1,+1}}`, with duplicate points
removed. It has four members when `u,v>0`, two on a nonzero axis, and one
at the origin. Negative energies or `u+v>Emax` lie outside the reached
summary carrier.

For `k=1` (hence `L=2π` in the chosen length unit), `Emax>=1`, and initial
states `(1,1)` and `(1,-1)`, both summaries are `(1/2,1/2)`. At
`kt=atan2(4,3)`, the evolved amplitudes are `(7/5,-1/5)` and
`(-1/5,-7/5)`, respectively. Their magnetic energies are exactly `49/50`
and `1/50`. Therefore `r` fails the declared dynamical receiver despite
answering the present magnetic-energy question exactly.

The repair `r+=(u,v,C)`, `C=kQP`, retains a real physical relationship:
`C=(1/k)dUB/dt=-(1/k) integral E·curl(B) d³x`. The integration-by-parts
step uses periodic boundaries. Direct substitution gives
`integral E·curl(B)=-k²QP`, verifying the sign. In particular, `C` is not
an assigned energy penalty, and it is not `integral E·B` (which vanishes
for this polarization). Its field expression is gauge invariant.

Introduce the Gram matrix
`G=[[2u,C],[C,2v]]=(kQ,P)(kQ,P)^T` and rotation
`R=[[c,s],[-s,c]]`. Then `G'=R G R^T`, which independently yields

```text
u' = u c² + v s² + C s c
v' = v c² + u s² - C s c
C' = C(c²-s²) + 2(v-u)s c.
```

The complete reached image is `u,v>=0`, `u+v<=Emax`, `C²=4uv`.
Every nonzero rank-one positive semidefinite `G` has precisely the two
source factors `(kQ,P)` and `(-kQ,-P)`. Thus repaired fibers are exactly
the antipodal pairs, with the origin a singleton. The formulas preserve
the reached image and compose according to time addition, so they satisfy
both observation and successor congruence for every admitted time shift.

The repair determines every homogeneous quadratic form in `(Q,P)` and
its later values within this fixed mode; constants can also be added.
It does not determine arbitrary polynomials of degree at most two when
they include sign-sensitive linear terms. Antipodes reverse the physical
field strengths and are not U(1) gauge equivalent except at the origin.
They are also related by a half-wavelength spatial translation, which is
a physical global symmetry in the fixed coordinate contract. Linear
smeared E or B readouts distinguish them. No global minimality across
other receiver families or enlarged physical carriers is required here.

## Finite-box negative control and remaining physical boundary

For the separate standard quantum Fock factor of nonzero free transverse
radiation modes, periodic momenta are `2π n/L`, `n in Z³\{0}`. The
normal-ordered energies above its vacuum are sums of
`ℏ c (2π/L)|n|` times nonnegative integer occupations. Hence the least
positive excitation energy is `ΔE(L)=2πℏc/L`. Normal ordering sets the
vacuum reference; it does not create this spacing. This is a gap above
that vacuum, not a lower bound on every pairwise difference between
excited energies. For any proposed common `δ>0`, choosing
`L>2πℏc/δ` gives `ΔE(L)<δ`.

This quantum radiation factor excludes zero modes as a separate modeling
restriction. One must not reinterpret the classical fixing of both flat
coordinates and their momenta as a simultaneously sharp quantum state.
No non-Abelian interaction, continuum construction of quantum Yang–Mills,
or uniform positive infinite-volume gap has been derived. The fixed
classical mode already admits arbitrarily small positive energies by
amplitude scaling. Its nonzero oscillation frequency is not a classical
lower bound on excitation energy.

The review supports the physical relevance of the bounded receiver test:
phase retention can control a real gauge-invariant energy readout under
an actual supplied evolution. Extending that statement to interacting
non-Abelian dynamics requires a new physical carrier and a derivation
of its observable/update closure; the Maxwell invariant-mode argument
does not provide that closure.
