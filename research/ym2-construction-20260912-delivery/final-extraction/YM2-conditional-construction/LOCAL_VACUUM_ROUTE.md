# A local second-order source estimate that improves actual construction

12 September 2026. Bounded written continuation; publication remains on hold.
Only this note is written by this task. No old checker, simulation, spin
cutoff, installation, git mutation, or other-lane edit is used.

**Result.** The second-order connected plaquette log coefficient has a
source-specific anchored norm substantially below the generic quadratic
majorant. With the already accepted bilinear constant `16/9`, this proves
an actual positive vacuum, uniformly over the admitted finite graphs, for

```text
0 <= r <= 1/(12m),        m=2(d-1),        d in {2,3}.       (LV1)
```

This interval exceeds the previous entire sufficient construction interval
`r<9/(128m)`. It is not obtained by merely renaming the old scalar root.
The construction also supplies actual conditional bounds and the physical
gap

```text
gap_phys(A) >= [51d/(40(d-1))] exp(-17/90).                (LV2)
```

The physical excited complement must be nonempty, as in the retained
conditional/forest-cover theorem. A tree-only physical sector instead
inherits its vacuous complement form inequality. Separately, the inherited
full-space Bochner argument gives `gap(A)>=7/30` on the same interval.

The second-order polynomial alone is not the actual vacuum. Its residual
still has oscillation at least `N r^3/288` on a family of `N` disjoint-edge
squares connected by bridges. What closes the actual construction is the
small, locally estimated defect followed by a convergent correction.

**Further compatible gain.** The independently derived gauge coefficient
estimate recorded below reduces the adjacent-pair constant from `32` to
`24` and the complete bilinear constant to `1/3`. The addendum constructs
the actual vacuum and closes its conditional gap certificate through
`mr=1/3`. LV1--LV20 remain the stand-alone result using only earlier
accepted estimates; the stronger result has its additional proof
dependency stated explicitly.

## Contract and dependencies

The carrier is the full `SU(2)^E` configuration space of any finite open
square/cubic lattice subgraph with distinct elementary plaquettes. Link
occurrences are independent coordinates; equality of Fourier functions is
ordinary Haar almost-everywhere equality, with smooth representatives for
the eventual vacuum and every conditional exterior. All spins are admitted.
Keep the unit-round link metric, normalized product Haar measure, full
vertex gauge action, and

```text
T=-Delta/2,       a_p=Tr(U_p)/2,       S=sum_p a_p,
A(r)=T-rS,       Gamma(f,g)=sum_i <grad_i f,grad_i g>.
```

The supplied inverse is `T^-1 Q`, where `Q` removes the Haar mean. The
unknown is the actual real gauge-invariant log vacuum up to an additive
constant. We fix its Haar mean to zero. The receiver retains the complete
actual positive vacuum, all exterior conditional oscillations, and a
volume-uniform excitation bound. We do not enumerate the spectral fiber
or solve the continuum/infinite-volume problem. The inverse on mean-zero
Fourier coefficients is fixed; multiplication and exponentiation are not
treated as lossless inverses after their constants are forgotten.

The retained definitions and all-spin regularity argument are in
[`DIRECT_COVER_ATTEMPT.md`](accepted/research/ym2_overlap_cover/accepted/estimate/accepted/DIRECT_COVER_ATTEMPT.md),
especially DC2 and DC8--DC17. Write its norm as `||.||_*` and its bilinear
map as

```text
B(f,g)=T^-1 Q Gamma(f,g).
```

Use the proved source norm `||T^-1 S||_*<=4m` from
[`SOURCE_NORM_REFINEMENT.md`](accepted/research/ym2_overlap_cover/accepted/estimate/SOURCE_NORM_REFINEMENT.md)
and the accepted all-input estimate

```text
||B(f,g)||_* <= K ||f||_* ||g||_*,        K=16/9,         (LV3)
```

from
[`SIGNED_AND_CONTRACTED_AUDIT.md`](accepted/research/ym2_overlap_cover/accepted/estimate/SIGNED_AND_CONTRACTED_AUDIT.md).
Its SC9 also gives, for two fundamental multi-spin source blocks and a
shared link `i`,

```text
||Gamma_i(a_p,a_q)||_A <= 2 ||a_p||_A ||a_q||_A=32.        (LV4)
```

The exact second-order head below agrees with the previously derived head
in
[`CONDITIONAL_REFINEMENT.md`](accepted/research/ym2_overlap_cover/accepted/estimate/accepted/CONDITIONAL_REFINEMENT.md),
CR7--CR9. The new load-bearing step here is its improved anchored **norm**,
followed by the resulting convergent actual correction. The conditional
gap transfer is the accepted CR5 in
[`CONDITIONAL_RAIL.md`](accepted/research/ym2_rail_closure/CONDITIONAL_RAIL.md),
or TR8 in
[`TRIAL_REFERENCE.md`](accepted/research/ym2_vacuum_handoff/TRIAL_REFERENCE.md).

## Exact local second-order algebra

Put

```text
s=rS/6,
z2=(1/2)B(s,s)=r^2 v2,
v2=(1/72)T^-1 Q Gamma(S,S).                              (LV5)
```

Different elementary plaquettes share at most one link. If they share no
link, their gradient pairing is identically zero, including when their
vertices touch. Thus `v2` consists only of one-plaquette terms and pairs
sharing one link. This is an exact support statement about the source
coefficient, not a finite-range claim for the completed log vacuum.

For one plaquette, let `chi_(1),p=4a_p^2-1` be the spin-one character of its
holonomy. The elementary metric identities give

```text
Gamma(a_p,a_p)=4(1-a_p^2)=3-chi_(1),p,
Q Gamma(a_p,a_p)=-chi_(1),p,
T chi_(1),p=16 chi_(1),p.
```

Its contribution to `v2` is therefore

```text
-chi_(1),p/1152=-(a_p^2-1/4)/288.                        (LV6)
```

For adjacent `p,q` with common link `i`, set

```text
b=a_p a_q,        c=4 integral a_p a_q dmu_i,
```

where the six exterior links are held fixed. This definition fixes the
orientation convention without guessing a merged loop word. To see the
formula directly, write each plaquette trace at that link as the real
linear function `A dot x` or `B dot x` of its unit-quaternion coordinate
`x in S^3`. Both coefficient vectors have Euclidean norm one. Inversion
of the shared link is accommodated by a fixed orthogonal change of these
coefficients. Haar has `integral x_alpha x_beta=delta_alpha,beta/4`, so
`c=A dot B`. Projection onto the tangent space of the sphere gives

```text
Gamma_i(a_p,a_q)=c-b.                                   (LV7)
```

The shared-link singlet part of `b` is `c/4`; its complementary shared-link
part has spin one. Every exterior link remains fundamental. Consequently

```text
T c=9c,             T(b-c/4)=13(b-c/4),
T^-1 Gamma_i(a_p,a_q)
  =(3/4)c/9-(b-c/4)/13=(4c-3b)/39.                      (LV8)
```

Both terms have zero full Haar mean: an exterior link appears once in
each and remains fundamental. A pair occurs twice in `Gamma(S,S)`, giving
the exact formula

```text
v2=-sum_p(a_p^2-1/4)/288
   +sum_(p<q:p~q) [c_pq/351-a_p a_q/468].                (LV9)
```

This shows explicitly the extra local variable needed at a shared link.
The merged observable `c_pq` cannot be removed by treating `a_p,a_q` as
independent replacement coordinates. All six/seven source link
occurrences are retained in (LV7)--(LV9).

## The source-specific anchored norm

First, the exact Fourier norm of the character in (LV6) is

```text
||chi_(1),p||_A=27.                                     (LV10)
```

Here is a direct extension of the source coefficient proof, rather than
an assumption that squaring preserves its original norm. In a unitary
irreducible representation of dimension `n`, the raw character of the
oriented four-link word has coefficient

```text
C=sum_(a,b,c,d=1)^n |b,c,c,d><a,b,d,a|
 =sum_(b,d) |v_(b,d)><w_(b,d)|,
v_(b,d)=sum_c |b,c,c,d>,
w_(b,d)=sum_a |a,b,d,a>.
```

Each family has `n^2` orthogonal vectors of norm `sqrt(n)`. Thus `C` has
`n^2` nonzero singular values, each equal to `n`, and trace norm `n^3`.
The dual representations at inverse links are unitarily equivalent to
the declared SU(2) representatives. Trace norm is preserved by these
unitary changes. Taking `n=3` proves (LV10). Its output energy `16`
cancels the inverse energy in (LV5); the resulting anchored contribution
of one self pair is `27/72=3/8`.

For a distinct adjacent unordered pair, (LV4) bounds its contribution to
the anchored norm by `32/36=8/9` if the output anchor lies in the union
of its supports, and by zero otherwise. Removal of the mean, singlet
support loss, and the possibility of cancellations between coefficients
can only lower this upper bound. No output-support equality is assumed.

For a fixed anchor link `e`, write `k_e` for the number of plaquettes
containing it. Every plaquette has four links and therefore at most
`4(m-1)` adjacent distinct plaquettes. Counting pairs from a plaquette
containing `e` counts each pair whose two plaquettes both contain `e`
twice; there are exactly `choose(k_e,2)` such pairs. Thus the number of
adjacent unordered pairs whose union contains `e` is at most

```text
4k_e(m-1)-k_e(k_e-1)/2 <= (7/2)m(m-1).                   (LV11)
```

The last expression is the value at `k_e=m`; the preceding polynomial
is increasing for integer `0<=k_e<=m` and `m in {2,4}`. This count also
covers boundary links and arbitrary admitted subgraphs. It uses that
distinct elementary squares share at most one link; duplicated source
occurrences would change the incidence contract.

Summing the self and adjacent-pair contributions proves the volume-uniform
bound

```text
||z2||_* <= h= kappa_m r^2,
kappa_m=(3/8)m+(28/9)m(m-1),
kappa_2=251/36,       kappa_4=233/6,
kappa_m/m^2 <= 5/2.                                     (LV12)
```

The old generic majorant assigns the larger value

```text
(K/2)||s||_*^2 <= (128/9)m^2 r^2.
```

The strict improvement in (LV12) comes from the actual local source and
its exact self character. It does not assert an improvement of (LV3) for
arbitrary inputs.

## Convergent correction and an explicit improved interval

Seek the complete log vacuum as `u=s+v`. The exact equation is

```text
v=z2+B(s,v)+(1/2)B(v,v).                                (LV13)
```

For `t=4mr`, a closed radius-`Z` ball for `v` is invariant if

```text
h+KtZ+(K/2)Z^2 <= Z,
```

and its Lipschitz multiplier is at most `K(t+Z)`. This is an estimate
of the full equation, with no perturbative truncation. It has the explicit
smaller-root choice

```text
D=(1-Kt)^2-2Kh,
Z(r)=[1-Kt-sqrt(D)]/K,
K(t+Z)=1-sqrt(D)<1,                                     (LV14)
```

whenever `1-Kt>sqrt(2Kh)`. In particular, with the accepted `K=16/9`,

```text
0 <= r < 1 / [(64/9)m + sqrt((32/9)kappa_m)]             (LV15)
```

is a sufficient construction interval. Since
`kappa_m<(128/9)m^2`, its upper endpoint is strictly larger than
`9/(128m)`. At equality in (LV15) the displayed contraction multiplier
would be one; that endpoint is not claimed by this argument.

For a simple closed interval, take `r<=1/(12m)` and `Z=1/20`. Then
`t<=1/3`, `h<=5/288`, and exactly

```text
h+KtZ+(K/2)Z^2
 <= 5/288+4/135+1/450
 =1063/21600 < 1080/21600=1/20,
K(t+Z) <= 92/135 < 1.                                  (LV16)
```

Banach contraction supplies `v` with `||v||_*<=1/20` and therefore
`||u||_*<=23/60`, uniformly in graph size. Iterating (LV13) from zero
preserves reality and gauge invariance. The complete all-spin norm and
the accepted fixed-finite-graph elliptic regularity argument imply that
`u` is smooth and

```text
(T-rS)e^u=E e^u,
E=-(1/2)integral |grad u|^2 dmu.
```

The positive ground-state form identity makes this the unique normalized
positive vacuum after division by `||e^u||_2`. Hence these are bounds on
the actual correction, not a hypothetical solution port. The inherited
Hessian/Bochner inequality gives

```text
gap(A) >= 1-2||u||_* >= 7/30.                            (LV17)
```

The scalar algebra also makes the noncosmetic gain explicit. With
`Y=t+Z`, the sufficient scalar equality becomes

```text
Y=t+h-(K/2)t^2+(K/2)Y^2.
```

The previous shifted calculation had `h=(K/2)t^2`, giving the old
equation exactly. Equation (LV12) strictly lowers this actual source
defect, so the subtractive term now survives.

## Actual conditional construction and gap readout

Let `p=e^(2u)/integral e^(2u)` and use its normalized one-link
conditionals. Smooth positivity, gauge covariance, and the rectangle
identity are automatic consequences of this constructed joint density.
Its local energy is exactly constant by the completed equation above.

For any anchored Fourier remainder `v`, the absolute four-value
difference and the all-spin energy bound
`lambda_J>=(3/2)|supp J|` give

```text
d_v=max_i osc_i(2v) <= (8/3)||v||_*,
b_v=max_i sum_(j!=i) mixedosc_ij(2v) <= (16/3)||v||_*.
```

Indeed a single-link difference is at most
`4 sum_(J:i in supp J)||v_J||_A`; the mixed difference is at most eight
times the corresponding two-link sum, and summing `j` gives the factor
`|supp J|-1`. Absolute Fourier convergence permits every exterior
replacement, not just almost every exterior.

The explicit reference `s=rS/6` therefore gives exactly the ports used
by TR8:

```text
D_actual <= 2mr/3+(8/3)Z,
q_actual <= mr+(4/3)Z,
gap_phys(A)
 >= [d/(d-1)](3/2)[1-mr-(4/3)Z]
      exp[-2mr/3-(8/3)Z].                              (LV18)
```

At the closed interval (LV1) with `Z=1/20`, these become

```text
D_actual <= 17/90,
q_actual <= 3/20,
gap_phys(A) >= [51d/(40(d-1))] exp(-17/90),
```

which proves (LV2). This uses the accepted conditional Poincare and
forest-complement argument; compatibility by itself is not substituted
for its collective contraction port.

The sharper `Z(r)` in (LV14) may be inserted in (LV18) wherever its
contraction condition holds and its bracket is positive. The displayed
closed-interval result does not require optimizing that endpoint.

## Why stopping at the second-order polynomial still fails

Write `w1=S/6` and let `w2=v2` from (LV9). For the normalized trial
`phi proportional to exp(rw1+r^2w2)`, the exact local-energy residual is

```text
R_phi= -r^2 N_p/24
        -r^3 Gamma(w1,w2)-(r^4/2)Gamma(w2,w2).           (LV19)
```

To check the scalar, `integral Gamma(S,S)=3N_p`: each self pair has
mean three and distinct plaquettes are orthogonal kinetic eigenfunctions.
Thus the order-two nonconstant part cancels while its vacuum energy
remains.

On `N` squares with disjoint edge supports connected by bridges,
`w2=-sum_p(a_p^2-1/4)/288`, so (LV19) is the sum of independent
one-square functions

```text
f_r(a)= -r^2/24
        +(r^3/216)a(1-a^2)
        -(r^4/10368)a^2(1-a^2).
```

Every plaquette holonomy can independently attain `a=1/2` or `a=-1/2`.
The even terms cancel between these choices, and

```text
f_r(1/2)-f_r(-1/2)=r^3/288,
osc R_phi >= N r^3/288                 for r>0.           (LV20)
```

This is an exact SU(2) hostile family. Raising the residual order from
two to three does not make its bulk oscillation uniform in volume. It
does not show that the actual gap vanishes. Equation (LV13), and not
dropping this residual, is the actual closure mechanism of (LV1)--(LV2).

## Compatibility with a separately improved bilinear estimate

Equations (LV5)--(LV12) require only the accepted local source estimate
(LV4). If a separate proof supplies a smaller complete bilinear constant
`K_new` on a closed invariant function space containing `s,z2` and all
iterates, (LV13)--(LV14) apply with that constant unchanged. The resulting
source-refined sufficient interval is

```text
r < 1 / [4K_new m + sqrt(2K_new kappa_m)].                (LV21)
```

This is a conditional adapter, not evidence for any proposed value of
`K_new`. Its proof must cover the actual all-spin iterates and the same
anchored norm; a source-only or finite-order bound cannot fill that port.
It improves that new constant's generic source majorant precisely when
`kappa_m<8K_new m^2`. The strict inequality holds for `K_new=16/9` and
also algebraically for `K_new=4/9`, should the latter be independently
established. No other agent's candidate proof is assumed in LV1--LV20.

## Addendum: gauge coefficients lower the local source bound again

After LV1--LV20 were complete, the written all-spin proof in
[`GAUGE_NORM_GAIN.md`](GAUGE_NORM_GAIN.md), GN14--GN20, was read and
independently audited in full. It proves on the closed invariant subspace

```text
||B(f,g)||_* <= (1/3)||f||_*||g||_*,
||Gamma_i(f_J,g_K)||_A <= (3/2)||f_J||_A||g_K||_A
       when the two differentiated spins are fundamental. (LV22)
```

The gauge intertwiner relation makes the one-link reductions of each
positive coefficient matrix `|B_J|,|B_J^*|` scalar. The separate
singular-value expansions and two Cauchy--Schwarz inequalities then
replace the fundamental bound `2` by the normalized trace
`(3+3)/4=3/2` of the absolute contracted generator. The same note proves
the all-spin extension using the total physical input Casimir. Its
support argument requires the admitted simple triangle-free graph and
the full vertex constraints, including the boundary; both are retained
here. Individual singular vectors are not assumed to be invariant.

Every single source block `a_p` is itself gauge invariant, so LV22 applies
to the pair estimate directly and gives `||Gamma_i(a_p,a_q)||_A<=24`.
The self coefficient and support count LV10--LV11 are unchanged. Thus

```text
||z2||_* <= h_sharp=kappa'_m r^2,
kappa'_m=(3/8)m+(7/3)m(m-1),
kappa'_2=65/12,        kappa'_4=59/2,
kappa'_m/m^2 <= 59/32.                                  (LV23)
```

Use LV13--LV14 on the gauge-invariant subspace with `K=1/3` and
`h=h_sharp`. A uniform construction interval is

```text
r < 12/[m(16+sqrt(177))].                               (LV24)
```

Indeed `4Km+sqrt(2Kkappa'_m)` is at most
`m[4/3+sqrt(59/48)]=m(16+sqrt(177))/12`. This endpoint exceeds the
gauge proof's generic source endpoint `3/(8m)`, since `sqrt(177)<16`.
Equation LV24 is an actual construction statement; a physical-gap
claim still requires a positive bracket in LV18.

For that readout, the same gauge support proof gives `lambda_J>=6` for
every nonzero invariant block, including every block in `v`. The
single-link oscillation bound consequently improves to

```text
d_v<= (2/3)||v||_*,      b_v<=(16/3)||v||_*.
```

The second inequality retains its previous constant because the number
of outside links in a support need not be bounded. The conditional
certificate becomes

```text
q_actual <= mr+(4/3)Z,
D_actual <= (2/3)(mr+Z),
gap_phys(A) >= [d/(d-1)](3/2)[1-mr-(4/3)Z]
                       exp[-(2/3)(mr+Z)].              (LV25)
```

Take `mr<=1/3` and `Z=4/9`. Then `t<=4/3`, `h<=59/288`, and

```text
h+(1/3)tZ+(1/6)Z^2
 <= 59/288+16/81+8/243
 =3385/7776 < 3456/7776=4/9,
(1/3)(t+Z)<=16/27<1.
```

The same invariant contraction and smooth-positive-vacuum argument
therefore completes the actual correction. Substitution in LV25 yields

```text
0<=r<=1/(3m):
q_actual<=25/27,      D_actual<=14/27,
gap_phys(A)>=[d/(9(d-1))]exp(-14/27).                    (LV26)
```

For a larger gap on a smaller interval, take `mr<=1/4`, `Z=3/16`.
Here `h<=59/512`, `t<=1`, and

```text
h+(1/3)tZ+(1/6)Z^2
 <=59/512+1/16+3/512=47/256 < 48/256=3/16,
(1/3)(t+Z)<=19/48<1,
q_actual<=1/2,        D_actual<=7/24,
gap_phys(A)>=[3d/(4(d-1))]exp(-7/24).                    (LV27)
```

Both results concern the actual constructed vacuum and use its exact
constant local energy. They do not replace the operator by its
second-order trial reference, whose obstruction LV20 still applies.

The independent gauge proof is load-bearing for LV22--LV27. Its
fundamental local estimate, invariant closure, total-Casimir argument,
partial-trace argument, and complete all-spin case split passed this
task's written audit. These are mutually compatible improvements to
different steps of the same norm proof, not a multiplication of two
inverse factors already counted once.

## Evidence, verification, and remaining scope

The general statements are written derivations from the accepted
all-spin Fourier/conditional theorems and explicit coefficient algebra.
The finite arithmetic checks in this task verify the values in LV12,
the LV16 radius inequalities, the LV18 endpoint constants, and the
one-square polynomial residual; they do not prove the analytic theorems
by testing. Observed result: **PASS**, using only Python standard-library
`fractions.Fraction` arithmetic. The residual check represented the
complete polynomial by keys `(power_of_a,power_of_r)` and verified
`T w-2(1-a^2)(w')^2-ra` coefficient by coefficient against LV19--LV20,
with `T w=-2[(1-a^2)w''-3aw']`. No old verification suite was rerun.

The exact radius portion can be reproduced directly:

```python
from fractions import Fraction as F
K=F(16,9)
for m, expected in [(2,F(251,36)), (4,F(233,6))]:
    kappa=F(3,8)*m+F(28,9)*m*(m-1)
    assert kappa == expected
    assert kappa/m**2 <= F(5,2)
    t=F(1,3); h=kappa/F(144*m*m); z=F(1,20)
    assert h+K*t*z+K*z*z/2 < z
assert F(5,288)+F(4,135)+F(1,450) == F(1063,21600) < F(1,20)
assert K*(F(1,3)+F(1,20)) == F(92,135) < 1
assert F(2,3)*F(1,12)+F(8,3)*F(1,20) == F(17,90)
assert F(1,12)+F(4,3)*F(1,20) == F(3,20)
```

New exact Fraction checks of LV23, LV26 and LV27 also passed: the two
invariant-ball margins are `71/7776` and `1/256`; their Lipschitz
multipliers, conditional row bounds, and density bounds agree with the
displayed fractions. The all-spin and all-volume conclusions continue
to depend on the written proofs.

An independent written audit by the conditional-obstruction agent found
no defect in LV6--LV20, including the oriented spin-one coefficient norm,
the incident-pair count, the exact local `c_pq` algebra, the actual
fixed-point radius, and its conditional conversions. Its separate report
is `CONSTRUCTION_REVIEW.md` in this directory. This is an independent
written review, not formal verification or an external peer review.

The completed result is an enlarged sufficient interval for actual
finite-graph vacua and a volume-uniform physical gap at the retained
lattice units. No optimality, literature novelty, continuum mass gap,
or infinite-volume representation is claimed. The full strong-coupling
construction and complete spectral/continuum fibers remain OPEN.
