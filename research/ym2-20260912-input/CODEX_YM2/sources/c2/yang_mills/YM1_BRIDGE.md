# YM1: a Maxwell energy-transfer bridge

**Bounded task complete:** a concrete gauge field supplies two physically distinct
states with equal retained electric and magnetic energies but different later
magnetic energy. Retaining their signed energy-transfer relationship repairs this
receiver under the declared dynamics. A separate finite-box control shows why its
positive free-mode quantum spacing does not supply a volume-independent mass gap.
The main target is **preservation of magnetic-energy readout under time evolution**.

## Inherited physical model and selected sector

Use source-free classical **U(1) Maxwell theory in 3+1 dimensions**, with
natural units c=ℏ=1 and field normalization

\[
S=-\frac14\int F_{\mu\nu}F^{\mu\nu}\,dt\,d^3x,
\quad F=dA,\quad E=-\dot{\mathbf A}-\nabla A_0,
\quad B=\nabla\times\mathbf A.
\]

Gauge transformations identify potentials differing by an admitted gauge gradient;
they leave E and B unchanged. Gauss constraints are div E=div B=0. In radiation
gauge, A0=0 and div A=0, the transverse field obeys the wave equation and its
energy is ∫(E²+B²)/2. These are supplied physical laws, not consequences of RPRM.
[Tong, §§6.1–6.2.1, equations 6.493–6.524](https://www.damtp.cam.ac.uk/user/tong/qft/qfthtml/S6.html).

Choose space to be the periodic torus [0,L)³, L>0, volume V=L³. This is a
boundary-condition choice; there are no material conducting walls. Work in the
topologically trivial radiation sector: harmonic electric/magnetic fields and
flat-connection holonomy are fixed to their trivial values. Otherwise local E/B
would not describe all global gauge information on the torus. Fix a spatial
origin, polarization y, and the nonzero fundamental wave number k=2π/L. Spatial
translations and rotations are not being declared gauge redundancies.

The selected real one-mode sector consists of gauge classes with representative

\[
\mathbf A=\alpha Q\cos(kx)\,\hat y,\qquad
\mathbf E=-\alpha P\cos(kx)\,\hat y,\qquad
\mathbf B=-\alpha kQ\sin(kx)\,\hat z,
\quad \alpha=\sqrt{2/V}.
\]

Q and P are real physical Fourier amplitudes in this fixed frame. Q is recovered
from B by Q=−α∫Bz sin(kx)/k; P=−α∫Ey cos(kx). Thus these amplitudes, and their
product below, are gauge invariant in the specified sector. P is the **canonical
mode momentum** Qdot; because E=−Adot, it has the opposite sign from the electric
field's cosine amplitude. It is not an independently invented velocity law.

The constraints hold identically: Ey depends only on x and Bz only on x. Fields
and their derivatives are smooth and periodic. All omitted Fourier amplitudes
remain zero because the source-free Maxwell equation is linear. This invariant
subspace is exact for these initial data, although it covers only a small class
of Maxwell states. It is not a simulation of non-Abelian Yang–Mills interactions.

To bound the operational enclosure, fix a finite Emax>0 and admit
X={gauge classes represented above with (P²+k²Q²)/2≤Emax}. Amplitudes are bounded,
continuous real coordinates; they are not a finite enumerated state set. Equality
in X means equal physical fields in this fixed sector/frame. L, k, Emax, units
and boundary sector belong to the contract, not to a freely changing source port.

## Derive the actual dynamics

Periodic integration gives ∫cos²(kx)=∫sin²(kx)=V/2. Substitution into S gives
the one-mode Lagrangian (Qdot²−k²Q²)/2. The Legendre transform and equation of
motion therefore give

\[
H=\tfrac12(P^2+k^2Q^2),\qquad \dot Q=P,\qquad \dot P=-k^2Q.
\]

For a supplied time t, set c=cos(kt), s=sin(kt). The full-state continuation is

\[
T_t(Q,P)=(Qc+(P/k)s,\;Pc-kQs).
\]

This transformation preserves H and X and is enabled for every real t. Its
inverse is T−t, and Tt∘Tu=T(t+u). No Euler stepping, numerical stability claim,
dissipation, force-fitting parameter or added mass term is involved. In natural
units, [k]=length⁻¹, [Q]=length^(1/2), [P]=length⁻(1/2), [H]=length⁻¹; kt is
dimensionless. Any displayed numeric amplitudes use a fixed reference length ℓ0.

## Retained description and separating continuation

Let b=UB=∫B²/2=k²Q²/2 and e=UE=∫E²/2=P²/2. The proposed hot description
is r(Q,P)=(b,e), with k and the sector contract retained alongside it. It answers
present magnetic energy exactly and also fixes total energy b+e. The requested
readout is UB after the supplied time operation. Missing information is the
relative sign/phase between electric and magnetic mode amplitudes.

Choose L=2πℓ0, k=1/ℓ0, Emax=2/ℓ0. In units based on ℓ0, take
x+=(Q,P)=(1,+1), x−=(1,−1). Both have (b,e)=(1/2,1/2), H=1. They are not
gauge equivalent: their electric fields differ while their magnetic fields agree.
Both are physically admissible initial data of the same constrained Maxwell model.

Use t=atan2(4,3)/k, so (c,s)=(3/5,4/5). Direct evolution yields

| State | Initial retained (b,e) | Evolved Q | Later UB |
|---|---|---|---|
| x+ | (1/2,1/2) | 7/5 | 49/50 |
| x− | (1/2,1/2) | −1/5 | 1/50 |

The energy difference 24/25 is a derived exact value in the selected units. No
function of r alone can return this later UB for both states. This is a falsifier
of **this retained map for this time-evolved receiver**, not of Maxwell dynamics.
It remains a useful negative result even though both energies are gauge invariant.

An especially direct physical form of the lost relationship is the signed energy
transfer. Periodicity gives, using Maxwell's equations and integration by parts,

\[
\dot U_B=-\int B\cdot(\nabla\times E)\,d^3x
        =-\int E\cdot(\nabla\times B)\,d^3x=k^2QP.
\]

The two states initially have opposite magnetic-energy derivatives. Their
distinction is a **seam relative to this observation and continuation**. It is
not a spatial cut, new substance, force or extra energy charge.

## Explicit repair and preservation proof

Retain z=kQP=UBdot/k in addition to (b,e). This is an existing field
relationship, measurable here through the signed transfer integral. It adds no
Hamiltonian term. The image carrier is

\[
Y=\{(b,e,z): b,e\ge0,\ b+e\le E_{max},\ z^2=4be\}.
\]

Expanding the full-state continuation gives the following exact retained update:

\[
\begin{aligned}
b'&=bc^2+es^2+zsc,\\
e'&=ec^2+bs^2-zsc,\\
z'&=z(c^2-s^2)+2(e-b)sc.
\end{aligned}
\]

Each equality is obtained by substituting Q'=Qc+Ps/k and P'=Pc−kQs into
(k²Q'²/2,P'²/2,kQ'P'). Consequently r+∘Tt=Ut∘r+ for every admitted state,
Ut maps Y to itself, and Ut has inverse U−t on Y. Enabledness matches because
all time operations are enabled in both carriers. Initial magnetic-energy
readout is the b projection; repeated time operations stay supported. This
proves preservation for the declared receiver and continuation family. Retaining
only energy and then freezing it would fail: the individual b/e values change.

The complete physical-source fibers in the one-mode sector are explicit. For
b>0 choose Q0=√(2b)/k and P0=z/(kQ0); the fiber is exactly
{(Q0,P0),(−Q0,−P0)}. If b=0 and e>0, it is {(0,√(2e)),(0,−√(2e))}.
At b=e=z=0 it is the singleton (0,0). The displayed conditions defining Y
are necessary and sufficient for such a source; out-of-image triples are
admission errors for the retained-state update. No search is being called closed
without a coverage argument.

Antipodal source states are physical field-sign reversal, **not** U(1) gauge
copies. They are identified only because this receiver and time family cannot
distinguish them. The product's sign resolves the relevant relative phase, but
does not recover all physical source data. A linear Fourier-field query would
distinguish antipodes and require more information. No global minimality over
arbitrary encodings, arbitrary field modes or other receivers is claimed. For
the present energies, r already suffices; the stronger repair is needed only for
the declared later-energy question.

## Separate finite-box negative control

For the quantum comparison use the **standard free transverse-mode quantization**,
not a quantum theory inferred from the classical trajectory. The free photon
Hamiltonian has excitation frequency |k| after vacuum-energy subtraction.
[Tong, §6.2.1, equation6.524](https://www.damtp.cam.ac.uk/user/tong/qft/qfthtml/S6.html).
Periodic fields allow kx=2πn/L, derived directly by requiring exp(ikxL)=1;
finite-box and vacuum-subtraction conventions are discussed in
[Tong, §2.3, equations 2.99–2.104](https://www.damtp.cam.ac.uk/user/tong/qft/qfthtml/S2.html).

For the nonzero radiation-mode sector, the fundamental one-quantum excitation has
energy Δ(L)=2πℏc/L above vacuum. At fixed finite L this is positive. Now take
Lm=2πmℓ0, m any positive integer. Then

\[
\Delta(L_m)/(\hbar c/\ell_0)=1/m\longrightarrow0.
\]

For every proposed ε>0 in those energy units, choosing m>1/ε supplies an
admitted nonzero mode with excitation energy below ε. That is the analytic
failure of a common positive lower bound; the finite table 1,1/2,1/4,1/8 in
the checker is only a calibration of this formula. No volume or cutoff campaign
is run. An upper momentum cutoff retaining the fundamental mode does not remove
this 1/L dependence. A one-mode or occupation truncation also cannot establish
what happens after adding omitted modes/interactions.

The classical H≤Emax cap belongs to the earlier operational example, not to the
quantum Fock-space definition. The quantum comparison uses the nonzero-mode
radiation Fock factor; it does not impose simultaneously sharp quantum values
of conjugate harmonic holonomy and electric zero-mode momentum. Classical amplitudes already allow arbitrarily
small positive H, so no classical energy gap was claimed either. Zero/harmonic
torus sectors were excluded explicitly; Δ(L) is not asserted to describe an
unanalysed full torus Hilbert space including them. Finite volume breaks the
conditions for interpreting a box-mode energy as a Lorentz-invariant rest mass.

The official non-Abelian target instead concerns existence of a quantum theory
on four-dimensional unbounded spacetime and a positive vacuum excitation gap.
That target is distinct from this Abelian classical receiver result and its free
mode control. [Jaffe–Witten, §4; volume limits in §§5–6](https://www.claymath.org/wp-content/uploads/2022/06/yangmills.pdf).

## Evidence, scope and the one next physical obligation

The action, gauge treatment and standard free-mode quantization are inherited
physical definitions/results. The sector normalization, separating pair, exact
retained update, full fiber and 1/L argument are written derivations here.
`check_ym1.py` uses Fraction arithmetic for the fixed rotation/pair and a few
boundary/antipodal controls, then samples the actual field formulas on a 16-point
periodic grid to check integrated energies and signed transfer. The numerical
sampling is a calibration of one analytic mode, not a new field-theory solver or
a numerical spectral theorem. Its exact comparisons and floating tolerances are
recorded with results; final exported replay is recorded externally.

The broader recovered cube/two-photon source and its original meanings stay
preserved under `supplied/sources/yang_mills/`; their old checker was not rerun
and is not being relabeled as this bridge. No approximate prestige, fiving,
Double-Stamp or curve question is closed by YM1.

**One next physical obligation, not launched:** determine whether a gauge-invariant
retained description containing electric energy, magnetic energy and signed
energy transfer closes under a specified interacting SU(2) evolution with Gauss
constraints, or supply a pair with equal retained data and different future
magnetic energy. Nonlinear mode coupling prevents simply assuming the Maxwell
closure above. That would be a separate physical contract; even success would
still leave the quantum continuum mass-gap obligation untouched. No additional
YM1 work is needed to complete this bounded assignment.
