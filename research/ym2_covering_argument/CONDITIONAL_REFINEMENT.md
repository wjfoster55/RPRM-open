# Actual-vacuum conditional remainder from the Fourier contraction

12 September 2026. This is a written refinement of the reviewed proof in
[DIRECT_COVER_ATTEMPT.md](DIRECT_COVER_ATTEMPT.md). It reuses the exact head factors and conditional
definitions in
[NEXT_CONDITIONAL_PORTS.md](accepted_sources/ym2_connected_vacuum/NEXT_CONDITIONAL_PORTS.md).
No existing packet or receipt is changed.

**Result.** Under the same finite open square/cubic graph,
metric, operator, all-spin and coupling contract as the direct proof,
the previously missing actual-vacuum remainder sum has the explicit bound

```text
t=8mr,                       m=2(d-1),
Y(t)=(3/8)[1-sqrt(1-16t/3)],
W(t)=Y(t)-t-(4/3)t^2,
eta(r)=(16/3)W(8mr),

sup_(G,e) sum_(j!=e) epsilon_ej(G,r) <= eta(r),
0<=r<=1/(48m).                                           (CR1)
```

Every square root in this interval is real. A simpler, weaker bound is

```text
eta(r) <= (160/3)(8mr)^3.                                (CR2)
```

Together with the accepted head count (CP1), this gives an actual
conditional row bound strictly below `1/12` throughout that interval.
The spectral gap in the companion proof is obtained separately from the
weighted Bochner identity; this note does not use a conditional row bound
as an unstated spectral-gap theorem.

## 1. Contract, representation and requested remainder

The carrier is the full product configuration space
`Q_G=SU(2)^(E_G)` with ordinary link occurrences and product Haar measure.
The true positive normalized ground-state density is `rho_G`. Conditional
laws fix the actual outside links, including exteriors of Haar measure
zero; smooth positivity supplies a unique continuous version everywhere.

Retain the source functions from (CP2):

```text
F_head=(r/3)sum_p a_p
       +r^2[-sum_p a_p^2/144+sum_(p<q,p~q) C_pair(p,q)],
C_pair(p,q)=(4w_pq-3a_p a_q)/702,
R_G=log rho_G-F_head,

epsilon_ej(G,r)=sup_(omega,omega' differing only at j)
  osc_(U_e)[R_G(U_e,omega')-R_G(U_e,omega)].              (CR3)
```

The requested receiver is the complete supremum over outside
configurations and sum over outside-link occurrences in (CR3). It is
stronger than an `L^2` remainder. The input supplied by the companion
construction is an actual log vacuum `u` with Haar mean zero, satisfying

```text
rho_G=e^(2u)/integral e^(2u) dmu,
u=s+(1/2)B(u,u),
s=rT^-1 S,
B(v,w)=T^-1 Q sum_(i,k)(D_(i,k)v)(D_(i,k)w),
||B(v,w)||_* <= (8/3)||v||_*||w||_*,
||s||_*<=t=8mr,           ||u||_*<=Y(t).                 (CR4)
```

Here `Q` subtracts the Haar mean, and the norm, Fourier coefficients,
kinetic weights and support sets are exactly (DC2). This norm is a new
explicit stronger contract, not a consequence inferred from the earlier
fixed-graph `L^2` bounds.

## 2. An actual norm bound after subtracting two orders

Put `b=4/3` and define

```text
q=(1/2)B(s,s),             w=u-s-q.
```

The number `Y` is the smaller nonnegative solution of `Y=t+bY^2`.
For `0<=t<=1/6`, it satisfies `0<=Y<=1/4`. Equation (CR4) gives

```text
||u-s||_* <= bY^2=Y-t.
```

Using bilinearity, without discarding any terms of the actual solution,

```text
w=(1/2)[B(u-s,u)+B(s,u-s)],
||w||_* <= b(Y+t)(Y-t)
          =b(Y^2-t^2)=Y-t-bt^2=W(t).                    (CR5)
```

This proves (CR5) directly for the converged fixed point. It does not
assume that a formal Taylor series converges or that higher connected
coefficients vanish.

For the explicit cubic form, `t=Y(1-bY)` and `Y<=1/4` imply
`Y<=3t/2`. Therefore

```text
W=b^2(Y+t)Y^2 <= b^2(5t/2)(9t^2/4)=10t^3.              (CR6)
```

At the endpoint `t=1/6`, the values are `Y=1/4` and
`W=5/108`. Both the exact expression and the cubic bound agree there.

## 3. The subtracted polynomial is exactly the accepted head

Write `u1=T^-1 S=S/6` and `q=r^2 v2`. The exact kinetic product rule is

```text
T(f^2)=2fTf-|grad f|^2.
```

Consequently

```text
v2=T^-1 Q(S u1)-(1/2)Q(u1^2).                           (CR7)
```

The first term is precisely the second wavefunction coefficient in
[CONNECTED_VACUUM.md, (CV13)](accepted_sources/ym2_connected_vacuum/CONNECTED_VACUUM.md),
whose local coefficient identities apply to the declared graph family.
Substituting those coefficients into (CR7) gives

```text
v2=-sum_p(a_p^2-1/4)/288
    +(1/2)sum_(p<q,p~q) C_pair(p,q).                     (CR8)
```

In detail, each edge-disjoint pair cancels because its wavefunction
coefficient `a_p a_q/36` equals its contribution to `u1^2/2`. For an
adjacent pair,

```text
a_p a_q/39+w_pq/351-a_p a_q/36
  =-a_p a_q/468+w_pq/351=(1/2)C_pair(p,q).
```

The one-plaquette coefficient is
`(1/96-1/72)(a_p^2-1/4)=-(a_p^2-1/4)/288` after Haar centering.
Thus the identity of functions is

```text
2(s+q)=QF_head,
R_G=2w+(a configuration-independent scalar).             (CR9)
```

The scalar includes both density normalization and the Haar mean of
`F_head`. It disappears from every conditional oscillation in (CR3).
There is no replacement of the actual vacuum by the exponential of its
polynomial head.

## 4. Fourier supports control all exterior replacements

For any real function `h` with an absolutely convergent Fourier expansion
`h=sum_J h_J`, put `a_J=||h_J||_A`. A component with `e` absent from its
support is independent of the inside link `e`, so its contribution to
an inside oscillation is zero. A component with `j` absent is unchanged
under the outside replacement at `j`.

For a component containing both links, the alternating difference in the
two inside and two outside choices is a sum of four function values.
Each has absolute value at most `a_J`. Although individual Fourier
components may be complex, this absolute-value bound applies before
summing, while the full alternating difference is real. Therefore

```text
sup_(omega,omega' differing only at j)
  osc_(U_e)[2h(U_e,omega')-2h(U_e,omega)]
 <=8 sum_(J:e,j in supp J) a_J.                          (CR10)
```

Uniform absolute convergence justifies taking these suprema and
termwise bounds. Summing over outside-link occurrences gives

```text
sum_(j!=e) [right side of (CR10)]
 =8 sum_(J:e in supp J)(|supp J|-1)a_J
 <=(16/3)sum_(J:e in supp J)lambda_J a_J
 <=(16/3)||h||_*.                                       (CR11)
```

The middle inequality uses the complete all-spin lower bound
`lambda_J>= (3/2)|supp J|`, so that
`|supp J|-1 <= (2/3)lambda_J`. The proof includes every Fourier support,
including supports generated at arbitrarily high perturbative order;
there is no assumption of a finite interaction range for the true log
vacuum.

Apply (CR10)-(CR11) to `h=w` and use (CR5), (CR9). This proves (CR1).
Applying (CR6) then proves (CR2).

## 5. The conditional readout for the actual density

For comparison, applying (CR10) to `h=u` bounds the full conditional
log-density tilt. The bounded-tilt lemma retained in the accepted packet
gives `TV<=tanh(osc/4)<=osc/4`. Hence directly

```text
c_ej(G,r)<=2 sum_(J:e,j in supp J)||u_J||_A,
sum_(j!=e)c_ej(G,r)<=(4/3)||u||_*<=(4/3)Y<=1/3.          (CR12)
```

Keeping the much sharper known head separately gives the stronger bound
from (CP1):

```text
sum_(j!=e)c_ej(G,r)
 <= mr+[16m(m-1)/117]r^2+(4/3)W(8mr).                    (CR13)
```

For every `0<=r<=1/(48m)`, (CR6) yields

```text
mr<=1/48,
[16m(m-1)/117]r^2 <= (m-1)/(16848m),
(4/3)W <= (4/3)(5/108)=5/81.
```

Their sum is strictly below `1/12`. One direct comparison is

```text
1/12-1/48-5/81=1/1296,
(m-1)/(16848m)<1/16848=1/(13*1296).
```

Thus the exact requested (CP8) ports can be filled with the function
`eta` in (CR1) and `theta=1/12`, uniformly for dimensions two and three
over the stated interval, using the companion Fourier fixed-point proof.
The earlier restriction `r<=1` in the head
estimate is satisfied by this smaller interval.

## 6. Hostile control and evidence boundary

The argument would fail if support were inferred from a diagram or a
truncated connected polynomial. What is used instead is independence
of a link variable for every Peter--Weyl component trivial on that link,
and an absolutely summable bound on all reached components. Even a
component with support across the entire finite graph is counted with
all of its outside links in (CR11).

A small `L^2` remainder still cannot replace (CR5): arbitrarily narrow
smooth spikes can have small `L^2` norm and large exterior oscillations.
The local energy-weighted Fourier norm supplies the uniform absolute
convergence and support-size weight that that hostile case lacks.

The fixed-point norm construction is the only new analytic dependency.
The remainder estimate, the head matching, and the all-exterior counting
are written derivations here, with their separate
[review](CONDITIONAL_REVIEW.md). This refinement inherits any later
correction to its analytic dependencies. It provides an explicit
graph-uniform cubic remainder in the exact norm previously missing from
(CP8), without rerunning or changing old finite receipts. The evidence
grade is written mathematics, not formal proof or a claim of novelty.
There is no continuum or thermodynamic-limit promotion.
