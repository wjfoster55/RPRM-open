# YM lane audit for closure master 07

12 September 2026, America/Denver. Read-only audit of the YM and BSD source
lanes; this is the only file written by this subtask. No task was messaged or
interrupted. No old YM/BSD checker or large campaign was rerun.

## Source selection and current endpoint

The inspected task is **Complete YM2 SU(2) readout test**, task ID
`01a0965b-9165-78d2-81fe-19720be304f6`. Its newest completed turn at inspection
was `01a09827-ebd1-7d63-bef3-0138f83251af`. That turn explicitly read
**Run BSD E5 test 01**, including the completed column-handoff result. The
task was idle. Its latest actual result is
`C:/github/RPRM-open/research/ym2_operational_seam/RESULT.md` and the detailed
proof is `COMBINED_RESULT.md` in that directory. The older overlap-only
bound is not the current endpoint.

The current contract is: finite open subgraphs of the square or cubic
lattice; SU(2) on each positively oriented edge; unit-round link metric;
gauge constraints at every vertex; no boundary charges or periodic
identifications; all spins admitted. Write

```text
T = -Delta/2,
A = T-rS,  S = sum_p a_p,  a_p = Tr(U_p)/2,
m = 2(d-1),  x = mr,  d = 2 or 3,  r >= 0.
```

The physical Hamiltonian is `E_el A` plus a constant, so its gap is
`E_el gap(A)`. Equal link occurrences remain shared variables. Fourier
blocks retain their complete representation labels, coefficient matrices,
and actual supports; equal numerical energies do not identify blocks.

The new source bound, composed with accepted all-spin analytic results,
constructs the actual positive lattice vacuum and certifies, for d=3:

| Coupling interval | Guaranteed physical gap divided by E_el |
|---|---|
| `0 <= r <= 1/12` | `(9/20) exp(-41/90)`, approximately `0.285343` |
| `0 <= r <= 7/80` | `(17/80) exp(-23/45)`, approximately `0.127464` |

These are lower bounds on the same Hamiltonian, not measurements of its
true gap. They are uniform over admitted finite graph sizes and include all
spins. The physical excited complement must be nonempty; on a tree the
corresponding form inequality is vacuous.

The new source coefficient in d=3 is
`125/6+7sqrt(3)/3`, approximately `24.874785`, reduced from `59/2=29.5`.
It comes from retaining output support and the actual orientation class
before taking the norm. One channel has spin zero on the common edge and
must not be charged at that anchor.

Evidence grade: written derivations using explicitly accepted analytic
dependencies, an independent written review, and saved execution evidence
of 633 exact new controls. This audit freshly checked source hashes and
selected scalar arithmetic. It did not independently re-prove all inherited
Banach-space, regularity, vacuum-selection and conditional-cover results.

## Exact solved receiver and its boundary

On two adjacent squares retain trace coordinates `(a,b,c)`, where c is the
merged-loop half-trace. The admitted quotient is

```text
Omega = {(a,b,c) in [-1,1]^3 : 1-a^2-b^2-c^2+2abc >= 0}.
Ta = 6a,  Tb = 6b,  Tc = 9c,  T(ab) = 13ab-c.
h13 = ab-c/4,  T h13 = 13 h13.
Gamma(a,b) = 3c/4-h13.
```

The pair `(c,h13)` is a complete operational quotient for kinetic
continuation of `W=span{ab,c}`. It preserves all kinetic powers, heat
responses and nonnegative resolvent shifts on W. The inverse decoder from
the present/next pair is `c=13ab-T(ab)`, then `h13=ab-c/4`.

This is genuinely closed at that receiver. It is not the full interacting
receiver. The admitted points `(1/2,1/2,1/4)` and `(3/4,1/3,1/4)` have the
same `(c,h13)` but different `a+b`, and their `A(r)c` values differ by
`-r/48`. Retaining full `(a,b,c)` restores the already accepted two-square
gauge quotient and its differential operator. That fixed-graph geometric
closure was established before the BSD donor pass; the new pass must not
be credited with first establishing it.

An especially relevant exact witness is `(a,b,c)=(1/2,1/2,1/4)`:
`Gamma(a,b)=0` but `T^-1 Gamma(a,b)=1/156`. A present pointwise cancellation
does not preserve the response of two different kinetic channels. In the
anchored Fourier norm, opposite signs in distinct blocks do not cancel.

Sources: `SPECTRAL_CHANNEL.md`, SP1-SP17, especially lines 97, 200, 355,
416 and 454; `OPERATIONAL_REVIEW.md`, sections 1 and 5.

## What the remaining uniform estimate actually asks for

The current mean-zero log vacuum is `u=u0+v`, with `u0=rS/6`, and its exact
equation is

```text
B(f,g) = T^-1 Q Gamma(f,g),
v = h+B(u0,v)+(1/2)B(v,v),  h=(1/2)B(u0,u0),
||B(f,g)||_* <= ||f||_* ||g||_*/3,
||u0||_* <= 4x,  ||h||_* <= (25/16)x^2.
```

Here, for full Peter-Weyl coefficients `f_J=Tr(B_J pi_J)`,

```text
lambda_J = sum_e 2j_e(j_e+1),
||f||_* = max_e sum_(J:e in supp J) lambda_J ||B_J||_1.
```

On a ball `||v||_*<=Z`, the accepted scalar certificate is

```text
M_x(Z) = (25/16)x^2+(4/3)xZ+Z^2/6 < Z,
L_x(Z) = (4x+Z)/3 < 1,
q <= x+4Z/3 < 1,
D <= 2(x+Z)/3,
gap_phys(A) >= [3d/(2(d-1))](1-q) exp(-D).
```

These are distinct ports: constructing the actual vacuum does not by itself
make the conditional physical-gap bound positive. This particular scalar
certificate loses simultaneous conditional positivity at
`x=(sqrt(1066)-25)/21`, approximately `0.364269`, although its vacuum
construction root remains available until approximately `0.424817`.
Neither threshold proves that the physical gap closes.

The latest proposed direction is a tail or relative-scale estimate for the
actual nonlinear iterates. It must retain full output blocks and control
their mixed contributions before taking trace norms, uniformly in all
spins and admitted graph sizes. The exact product identity is

```text
P_L Gamma(u_J,v_K)
 = (lambda_J+lambda_K-lambda_L) P_L(u_J v_K).
```

Thus a useful cancellation must occur in the sum of coefficients reaching
the same complete block L. A shared energy value alone is insufficient.
The inverse denominator `lambda_L` already cancels the norm's output-energy
weight once; it cannot be counted a second time as free decay.

A more explicit sufficient recentering target survives from
`research/ym2_overlap_cover/OVERLAP_INVERSE.md`, OI2 and OI11-OI13. At an
actual vacuum center u*, set `K*=I-B(u*,.)` and `a=T^-1 S`. Obtain

```text
||K*^-1 a||_* <= A*,
||K*^-1 B(f,g)||_* <= C* ||f||_* ||g||_*.
```

Then `2 A* C* |delta r|<1` suffices for a local continuation. Alternatively
construct a bounded approximate left inverse N with

```text
||I-N K*|| <= rho < 1,
||N a||_* <= A_pre,
||N B(f,g)||_* <= C_pre ||f||_* ||g||_*,
2 A_pre C_pre |delta r| < (1-rho)^2.
```

The old note's numerical constants are historical; the target operator
identity is the reusable part. A sequence of successful finite steps would
still need coverage sufficient to reach the desired coupling regime; steps
that accumulate at a finite r would not establish unbounded continuation.

## Carry, sawtooth and scale audit

The latest YM donor account agrees with the actual BSD column-handoff
source at the inspected hashes. Its claim is scoped: a scalar fold can
agree while its lawful next display differs. It gives no map from the
elliptic coefficient to a YM coupling or spectral coefficient.

For the master's supplied decimal model,

```text
F(d)=100d1+10d2+10d3+d4,
S(d_i)=d_i+1 mod 10,
F_(k+1)=F_k+121-10 W_(9,k),
C_(k+1)=C_k+W_(9,k),  L_k=F_k+10C_k,
L_(k+1)=L_k+121.
```

Over ten S steps each digit wraps once, so `C_(k+10)=C_k+121` and
`L_(k+10)=L_k+1210`, while F and the weighted occurrence record return.
This establishes an exact lift of the specified finite operational law.
Admitting indefinitely many carry rows is an explicit enlarged carrier.
The lifted drift does not provide a terminal criterion, a YM coercivity
estimate, or a continuum limit.

The useful transfer is the preservation question: retain what the next
operation needs. It has already helped YM through channel/support
retention. The quantitative limit is witnessed without losing any carry:
on one square use `chi_j` and `chi_(1/2)`, for half-integral j>=1. Their
bilinear source has channels

```text
8(j+1) chi_(j-1/2) - 8j chi_(j+1/2),
lambda_- = 8j^2-2,  lambda_+ = 8j^2+16j+6.
```

For fixed z>0, the shifted-to-unshifted anchored-norm ratio is a positive
weighted average of `lambda_-/(lambda_-+z)` and
`lambda_+/(lambda_++z)`, and tends to one. The exact block identities and
all signs/supports are already retained. A missing coordinate is therefore
not the entire obstruction to this proposed bound.

## One concrete candidate test, executed in this audit

**Candidate:** use a proportional spectral shift `z_J=alpha lambda_J`, with
constant alpha>0. This passes the isolated high-mode test: every inverse
channel gains the uniform factor `1/(1+alpha)`. Test the full equation
transport before claiming that this gain improves vacuum construction.

Write its original fixed-point map as `v=Fmap(v)`. Replacing T by
`T+alpha T` while retaining the original equation requires

```text
v = G_alpha(v) = [Fmap(v)+alpha v]/(1+alpha).
```

Dropping `alpha v` would change the equation. With the existing positive
majorants, the exact transported majorants obey

```text
M_alpha(Z) = [M_x(Z)+alpha Z]/(1+alpha),
L_alpha(Z) = [L_x(Z)+alpha]/(1+alpha),
Z-M_alpha(Z) = [Z-M_x(Z)]/(1+alpha),
1-L_alpha(Z) = [1-L_x(Z)]/(1+alpha).
```

Thus this proportional shift alone supplies no new self-map ball or
contraction threshold from the existing majorant. It preserves each sign
of the required margin. For alpha=1 the exact checked cases were:

| `(x,Z)` | Old ball margin | Transported ball margin |
|---|---|---|
| `(1/3,7/20)` | `1/2400` | `1/4800` |
| `(7/20,5/12)` | `13/6912` | `13/13824` |
| `(2/5,3/5)` | `-3/100` | `-3/200` |

The last is a hostile failed ball whose failure survives the shift.
For a positive scalar linear map with multiplier `3/2`, the transported
multiplier at alpha=1 is `5/4>1`; no generic contraction follows from
the isolated inverse factor one half.

Fresh in-memory Python `fractions.Fraction` checks passed for those three
balls and alpha in `{1/2,1,3}`. They also checked exact inverse transport
at the actual local energies 9 and 13, and the isolated proportional
factor for j in `{1,3/2,10,100}`. Command used a PowerShell here-string
piped to `python -I -B -`; no test file or saved source was changed.
The algebra above proves the displayed scalar-majorant identities beyond
those finite samples.

**Disposition:** reject the claim that this proportional shift, by itself,
improves the existing positive-majorant certificate. This does not reject
all relative scales. A nonuniform scale, structured operator preconditioner,
same-block cancellation, or proved tail distribution has additional
mathematical content and requires its own full transport and uniform bound.
This small gate is useful before undertaking a new large calculation.

## Later continuum condition

The inherited convention is `r=8/g_b^4` and `E_el=g_b^2/(4a)`. The retained
small-bare-coupling continuum route sends r to infinity. The present
bounded intervals therefore do not cover it. One still needs construction
of a nontrivial limiting quantum theory and a positive excitation scale in
fixed physical units after the relevant limits. A positive lattice gap at
one fixed r, or an exact cyclic/lifted representation, supplies neither
condition. Status of those obligations: **OPEN**.

## Inspected byte versions

All paths below are relative to `C:/github/RPRM-open/`. SHA-256 values were
freshly computed in this audit and agree with the cited packet/review.

| Path | SHA-256 |
|---|---|
| `research/ym2_operational_seam/COMBINED_RESULT.md` | `db8c340ae3f8955ee439249e56a5752a6edb6d3ef7af9cfa862aa0bc293cefe3` |
| `research/ym2_operational_seam/SPECTRAL_CHANNEL.md` | `d69f9413b85dfe6bb3ae64fb32fef32d731951eb8674765d95c709d2f2a19c01` |
| `research/ym2_operational_seam/CHANNEL_SOURCE.md` | `ff817b7cb2700636e4ad1497120c6f67765d51d75ef5148fa237abc1c2361d38` |
| `research/ym2_operational_seam/BSD_DONOR.md` | `54d161387b6172e7ba98109c3cae4fd3d28a1ff2ba1b2b897c934de3f9ef609c` |
| `research/ym2_operational_seam/OPERATIONAL_REVIEW.md` | `a000905c65d9e446a0263bf415396a433d06e47b38fc78439fc40d745bf88cbc` |
| `research/ym2_operational_seam/RESULTS.json` | `ccb5cc2d023f068f32493093c84f621df841267aad18947fc383634cd2d8b3dc` |
| `research/ym2-operational-20260912-delivery/YM2-operational-seam-2026-09-12.zip` | `19c6b86a31ebdea7d4c6f83a332a472cc3fabdcc3a908512b7f1616c65bc7d05` |
| `research/bsd-carry-key-06/COLUMN_HANDOFF.md` | `7c75f84dae917d718e18e07d3aedf433d2e16ebaf7f61df857a5e81044fd77bf` |
| `research/bsd-carry-key-06/work/column_handoff.py` | `d1c999598b40f1056073927ea839f2752aa14af854e88db957525f4614b659ce` |
| `research/bsd-carry-key-06/evidence/column_handoff_extended.json` | `5df84c3ba6eca77c41f851ec4152a1b9ddd445fce9fb37b129cabee263a469c1` |

The prior portable run reports 633 exact checks, fresh extraction and
unchanged source hashes in
`research/ym2-operational-20260912-delivery/FINAL_EXPORT_EVIDENCE.md`.
Those are attributed execution claims, not freshly replayed by this audit.
Hashes bind the inspected bytes and do not prove mathematical truth.
