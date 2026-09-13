# An exact separating witness for the actual two-cell vacuum

12 September 2026. New written derivation, with exact rational checks.
This note uses the analytic vacuum expansion proved in
[CONNECTED_VACUUM.md](CONNECTED_VACUUM.md) and the previously accepted
[finite-graph vacuum comparison](accepted_sources/ym2_signed_differences/VACUUM_COMPARISON.md).
It does not rerun that source or identify the vacuum with a classical Gibbs law.

## Result and contract

Use the full, interacting two-square SU(2) link Hamiltonian and its physical
gauge-invariant space. In the accepted convention,

```text
H/(alpha hbar^2) = T + r(2-a-b),    T=-L/2,
r=beta/(alpha hbar^2),   alpha>0, hbar>0, beta>=0.
```

The two rooted plaquette holonomies are U,V. Define their half traces and
the outer-loop half trace by a=Sc(U), b=Sc(V), w=Sc(UV). Their complete
configuration quotient is

```text
K = { (a,b,w) in [-1,1]^3 :
      1-a^2-b^2-w^2+2abw >= 0 }.
```

The Haar probability mu is the pushforward of independent Haar U,V.
Let phi_r be the positive ground-state eigenfunction with Haar mean one,
and let rho_r=phi_r^2 / integral phi_r^2 dmu be the probability density of
the actual vacuum. Equality of readouts here is equality mu-almost everywhere.
All functions used below have continuous representatives on the compact
source. The operator and form domains are inherited from that source.

**Theorem.** For every real 0<r<=1/3000,

```text
D(a,b,w) = w-ab,
J(r) = integral D log(rho_r) dmu,
J(r) > (4/58500) r^2 > 0.                              (W1)
```

In particular, rho_r is not a measurable function of (a,b) alone, and
cannot be a product of two separate single-plaquette densities. The readout
(a,b) loses a distinction required by the actual vacuum. This is stronger
than a formal second-order obstruction: an explicit bound on the whole
remainder prevents its cancellation. The small interval is a sufficient,
conservative certificate, not an optimal threshold.

The supplied port is the Hamiltonian, Haar law and full gauge constraint.
The requested readout is whether the actual vacuum retains a joint
orientation invisible to the individual traces. The operation is the
forward ground-state construction; no new dynamics or boundary condition is
chosen. This is a separating witness, not an explicit full eigenfunction,
complete spectrum, or complete inverse fiber.

## 1. The missing joint and its complete fiber

Write U=(a,u), V=(b,v) as unit quaternions. Then

```text
|u|^2=1-a^2,    |v|^2=1-b^2,
w=ab-u.v,      D=-u.v.
```

Conditionally on a,b under Haar, the two directions are independent and
uniform on S^2. Their relative cosine is uniform on [-1,1]. Thus

```text
w | (a,b) is uniform on [ab-R, ab+R],
R = sqrt((1-a^2)(1-b^2)),
E_mu[D | a,b]=0,
E_mu[D^2 | a,b]=(1-a^2)(1-b^2)/3.                        (W2)
```

At R=0 the conditional is a point mass. For every admitted (a,b), this is
also the complete configuration-quotient completion fiber: ONE(ab) if R=0,
MANY([ab-R,ab+R]) if R>0. Values outside [-1,1]^2 are admission errors.
There are no additional hidden configuration invariants for this pair of
SU(2) holonomies modulo simultaneous conjugation. This does not describe
the larger classical phase-space joint containing electric momenta.

Since E[a^2]=E[b^2]=1/4 and a,b are independent,

```text
E[D]=0,       ||D||_2^2=3/16,
<D,g(a,b)>_mu=0 for every square-integrable g,
<D,w>_mu=3/16.                                         (W3)
```

This conditional residual is useful precisely because every explanation
using only a,b integrates to zero against it. A nonzero J certifies the
missing joint without reconstructing the whole eigenfunction.

## 2. The exact second-order coefficient

The companion derivation supplies

```text
phi_r = 1+r u1+r^2 u2+R_phi,
u1 = (a+b)/6,
u2 = (a^2+b^2-1/2)/96 + ab/39 + w/351,
||R_phi||_2 <= r^3/[2 sqrt(2)(1-r)]  for 0<=r<1.         (W4)
```

The nonconstant terms in the order-two expansion of log(rho_r) are

```text
r(a+b)/3 + r^2[-(a^2+b^2)/144 - ab/234 + 2w/351].       (W5)
```

Constants depend on normalization, but cancel against D. By (W3), the
linear coefficient and every a,b-only term vanish in J. Its first
nonzero coefficient is therefore

```text
(2/351)<D,w> = (2/351)(3/16) = 1/936.                   (W6)
```

For a concrete hostile pair, a=b=0 and w=+3/5 or -3/5 are both admitted
interior points of K. They have identical single-loop traces but different
relative orientations. Their second-order log-density coefficients differ
by 4/585. This pair illustrates the exact jet obstruction. The global L2
bound below does not supply a pointwise remainder at those two chosen
points; the actual-vacuum theorem uses the integral witness J instead.

## 3. Convert the vacuum remainder to a logarithmic remainder

L2 control alone does not justify taking logarithms near zero. The accepted
positive-vacuum comparison supplies the missing lower bound:

```text
max(phi_r)/min(phi_r) <= K0 exp(16r/3),
K0=104207/52043 < 7/3.
```

For 0<=r<=1/10, exp(16r/3)<=exp(8/15)<e<3. Consequently the ratio is
strictly less than 7. Haar mean phi_r=1 implies min(phi_r)>1/7.
The elementary e<3 follows, for example, from n!>=2^(n-1) for n>=2,
with strict inequality for n>=3, in its complete exponential series.
This is a uniform pointwise lower bound on this fixed compact source.

Put p2=1+r u1+r^2 u2. The exact coefficients give

```text
||u1||_infinity <= 1/3,
||u2||_infinity <= 1/64+1/39+1/351 < 1/20,
p2 >= 1-r/3-r^2/20 > 9/10        for r<=1/10.
```

The logarithm has Lipschitz constant at most 7 between phi_r and p2.
Moreover 1/[2 sqrt(2)(1-r)]<=5/(9 sqrt(2))<2/5, since 625<648.
It follows from (W4) that

```text
||log(phi_r)-log(p2)||_2 < (14/5) r^3,  0<r<=1/10.       (W7)
```

To control the remaining elementary logarithm, set z=r u1+r^2 u2.
For r<=1/10, |z|<=7r/20<1/10, and the complete scalar Taylor suffix obeys

```text
|log(1+z)-z+z^2/2| <= |z|^3/[3(1-|z|)]
                    <= (343/21600) r^3.
```

The cross terms in z-z^2/2 contribute at most
`r^3/60+r^4/800 <= (1/60+1/3200)r^3`; the last bound deliberately uses
the weaker r<=1/4. Hence

```text
||log(p2)-r u1-r^2(u2-u1^2/2)||_infinity
 <= (343/21600+1/60+1/3200)r^3 < (1/25)r^3.
```

Combining with (W7), and using that mu is a probability,

```text
||log(phi_r)-r u1-r^2(u2-u1^2/2)||_2 < 3r^3,
                                                   0<r<=1/10.  (W8)
```

No L2-to-L-infinity inference was used. The pointwise lower bound came
from a separate accepted semigroup proof; the logarithmic approximation
error remains an L2 bound.

## 4. Certify the actual signed readout

Since log(rho_r)=2log(phi_r)-log integral phi_r^2 dmu, its normalizing
constant integrates to zero against D. Cauchy--Schwarz and
2||D||_2=sqrt(3)/2<1 turn (W8) into

```text
|J(r)-r^2/936| < 3r^3,                  0<r<=1/10.      (W9)
```

For r<=1/3000, 3r<=1/1000, so

```text
J(r) > r^2(1/936-1/1000) = (4/58500)r^2 > 0.
```

If rho_r were a function of (a,b), its bounded logarithm would be one as
well and (W3) would force J(r)=0. This contradiction proves (W1).
At r=0, rho_0=1 and J(0)=0: the strict conclusion correctly excludes
the uncoupled control.

## 5. What has been closed and what has not

The concrete obstruction is now closed on an explicit interval: the actual
vacuum distinguishes joint orientations discarded by (a,b). The generator
already exposes the same missing port through T(ab)=13ab-w. A rechart of
the same two retained numbers cannot recover w. Retaining w is sufficient
for the full configuration quotient, though computing arbitrary nonlinear
vacuum functions on that quotient is still an infinite-dimensional problem.

This is a narrow realization of the RPRM question-preservation principle,
not a replacement definition of RPRM, joint, distinction, or scaling.
The readout J is one declared receiver; other questions may need other ports.

The theorem does not show that this dependence persists for every coupling,
that it is a monotone correlation, that an all-order connected expansion is
uniform in graph size, or that a quantum continuum field has been constructed.
It also does not by itself improve the previously established finite-graph
gap bound. Its L2 remainder can certify this integral readout; it cannot
bound worst-case changes of conditional densities. The next obligation is
an actual connected log-density remainder controlled under local exterior
changes, with constants summable uniformly over a graph family. That
stronger norm and its graph quantifiers remain OPEN.

The equation uses the dimensionless relation r=beta/(alpha hbar^2).
Changing units consistently preserves r and the witness. Changing graph
resolution, couplings or boundary contracts is a new family problem; it
does not inherit the fixed-graph radius automatically. The constants here
come from the declared source spectrum and bounds, rather than a rule
that scaling must be fixed at every level.

## Evidence

The theorem is a written analytic proof using the companion perturbation
proof and the accepted heat comparison. It is not a proof-assistant proof.
[check_witness.py](check_witness.py) independently recomputes the exact Haar
moments, coefficient contraction, admissible hostile pair, and rational
inequalities. Its [receipt](RESULTS_WITNESS.json) binds the checker bytes.
Those finite checks support the derivation; they do not establish analytic
perturbation theory, the accepted operator domain, or all of mathematics by
testing finitely many inputs. The real interval in (W1) is covered by the
written uniform inequalities, not by sampling couplings.

```powershell
python -I -B -X utf8 check_witness.py
```

Default execution is read-only and compares the saved receipt. Use
`--write-results` only when intentionally generating that adjacent receipt.
