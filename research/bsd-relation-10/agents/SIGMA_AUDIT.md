# E34: CM sigma truncation and formal-log precision audit

Prepared 2026-09-12. **The proposed CM uniqueness argument is valid.** For
the specified model at 5 it proves

\[
c=0,\qquad \sigma(it)=i\sigma(t),\qquad
\sigma(t)/t\in 1+t^4\mathbf Z_5[[t^4]].
\]

For every nonzero `t` with `r=v_5(t)>=1`, it follows that

\[
v_5\left(\frac{\log_5(\sigma(t)/t)}5\right)\ge 4r-1\ge3.
\]

Independently, the formal elliptic logarithm `lambda=log_omega` satisfies

\[
v_5\left(\frac{\lambda(t)-t}{5}\right)=5r-2\ge3.
\]

Thus both omitted contributions vanish modulo `125 Z_5`, and therefore
modulo `25 Z_5`. The notation `lambda(t)=t+O(t^5/5)` is acceptable only
with this **evaluated valuation meaning**. The coefficientwise claim
`lambda(t)-t in (t^5/5) Z_5[[t]]` is false.

## Contract and source admission

The carrier is `E/Q_5: y^2=x^3+A x` with `A=-1156`, its displayed integral
model, `omega=dx/(2y)`, and `t=-x/y`. Formal series equality is
coefficientwise equality over `Q_5`, with integral subrings stated
explicitly. Evaluation uses the formal neighbourhood `t in 5 Z_5`.
The two logarithms are distinct: `log_5` is the scalar Iwasawa logarithm,
while `lambda=log_omega` is the elliptic formal logarithm normalized by
`lambda(0)=0` and `d lambda=omega`.

The supplied ports are the model, differential, parameter and prime. The
missing ports are the normalized MST pair `(sigma,c)` and the precision
of the two discarded tails. The receiver retains the residues modulo 25
or 125 after division by 5, and after division by any additional 5-adic
unit such as 8 or 64. It does not retain exact heights or exact elliptic
logarithms. A retained residue has its entire congruence class as scalar
preimage.

The discriminant is `-64 A^3=2^12*17^6`, a 5-adic unit. Reduction gives
`#E(F_5)=8`, so `a_5=-2` and 5 is ordinary. These are the local hypotheses
needed below. Global height admission, the rational point arithmetic,
and modular-symbol calculations remain owned by their separate reports.

MST Theorem 1.3, printed p. 588, asserts uniqueness of the pair consisting
of an integral normalized odd sigma series and an integral constant
satisfying

\[
x+c=-D\left(\frac{D\sigma}{\sigma}\right),\qquad D=\frac d\omega.
\tag{1}
\]

Remark 1.4 emphasizes the oddness and leading-coefficient conditions.
This is uniqueness of the pair, not merely uniqueness after fixing an
externally supplied value of `c`. [MST, Theorem 1.3 and Remark 1.4](https://wstein.org/papers/pheight/pheight.pdf#page=4).

Harvey clarifies that oddness means compatibility with formal-group
inversion, and explains the possible `a_1/2` coefficient of `t^2` in a
general Weierstrass parameter. Here `a_1=a_3=0`, so inversion is exactly
`t -> -t`. [Harvey, Section 4, printed p. 7](https://arxiv.org/pdf/0708.3404#page=7).

No additional sigma normalization is being omitted. In particular,
integrality, oddness and leading coefficient 1 are all preserved in the
construction below. The prior
[PADIC_HEIGHT_AUDIT.md](../../bsd-coefficient-05/dependencies/PADIC_HEIGHT_AUDIT.md)
used only the weaker consequence `sigma(t)/t in 1+t^2 Z_5[[t]]`; that
earlier modulo-5 argument is not contradicted or edited here.

## Exact CM transport of the differential equation

Hensel lifting either simple root 2 or 3 of `X^2+1` modulo 5 gives a unit
`i in Z_5` with `i^2=-1`, of exact order 4. Define the automorphism

\[
\phi(x,y)=(-x,iy).
\]

It preserves the displayed curve and the origin. Direct calculation gives

\[
\phi^*x=-x,\qquad \phi^*t=it,\qquad
\phi^*\omega=\frac{-dx}{2iy}=i\omega.
\tag{2}
\]

Write `U=phi^*`, so `Uf(t)=f(it)`. For any formal function or Laurent
series `f`, differentiation of its pullback yields the chain rule

\[
D(Uf)=i\,U(Df).
\tag{3}
\]

This step accounts for the differential's scaling; applying two
ordinary `t` derivatives without that scaling would not justify (1).

Let `(sigma,c)` be the pair supplied by the theorem and put
`tau=i^{-1}U sigma`. Then

\[
\tau\in t\mathbf Z_5[[t]],\quad
\tau=t+\cdots,\quad \tau(-t)=-\tau(t).
\]

In detail, the leading coefficient is `i^{-1}i=1`; substitution by the
integral unit `i` preserves integrality; and the last identity follows
from the oddness of `sigma` under the actual inversion `t -> -t`.
Furthermore `-c` belongs to the same constant ring `Z_5`. Using (3),

\[
\frac{D\tau}{\tau}=i\,U\left(\frac{D\sigma}{\sigma}\right),
\qquad
D\left(\frac{D\tau}{\tau}\right)
=-U\left(D\left(\frac{D\sigma}{\sigma}\right)\right).
\]

Equation (1) and `Ux=-x` now give

\[
-D\left(\frac{D\tau}{\tau}\right)
=U(-x-c)=x-c.
\]

Therefore `(tau,-c)` is another pair satisfying every hypothesis of the
same uniqueness theorem on the same model, parameter and differential.
Uniqueness forces `tau=sigma` and `-c=c`; since 2 is a unit, `c=0`.
Consequently `sigma(it)=i sigma(t)`.

If `sigma(t)=sum s_n t^n`, coefficient comparison gives
`(i^{n-1}-1)s_n=0`. For `n` not congruent to 1 modulo 4 the factor is a
unit, already nonzero modulo 5. Hence

\[
\sigma(t)=t+\sum_{k\ge1}s_{4k+1}t^{4k+1},\quad
s_{4k+1}\in\mathbf Z_5.
\tag{4}
\]

This proves the proposed truncation for the entire series, without
inferring the infinite tail from finitely many computed coefficients.

## Sigma tail after evaluation

For `r=v_5(t)>=1`, equation (4) gives
`delta=sigma(t)/t-1 in 5^{4r} Z_5`. In

\[
\log_5(1+\delta)=\sum_{n\ge1}\frac{(-1)^{n+1}\delta^n}{n},
\]

the `n`th term has valuation at least `4rn-v_5(n)>=4r`.
The valuations tend to infinity, so the full logarithm belongs to
`5^{4r} Z_5`. Division by 5 proves the bound in the opening statement.
Division by the unit `m^2=64` preserves it. Thus, whenever the separate
MST height admission holds for `8R`, replacing `sigma(t)` by `t` changes
`h_5(R)` by an element of `125 Z_5` or a smaller ideal.

A direct first-coefficient check gives a stronger optional bound here.
From `x=t^{-2}-A t^2+O(t^6)`,
`omega=(1+2A t^4+O(t^8))dt`, and equation (1) with `c=0`,

\[
\sigma(t)=t+\frac{5A}{12}t^5+O(t^9)
=t-\frac{1445}{3}t^5+O(t^9).
\]

The `t^5` coefficient has valuation 1, while all remaining allowed
coefficients are integral. Hence for nonzero `t in 5 Z_5`,

\[
v_5(\sigma(t)/t-1)=4r+1,\qquad
v_5\left(\log_5(\sigma(t)/t)/5\right)=4r.
\]

The weaker bound suffices for the requested modulo-125 receiver; no
reliance on this refinement is necessary.

## Formal elliptic logarithm and its exact valuation

Substituting `y=-x/t` into the curve equation gives
`x^2-t^{-2}x+A=0`. The Laurent branch at the origin is therefore

\[
x(t)=\frac{1+\sqrt{1-4At^4}}{2t^2}.
\]

Since `omega=-t x'(t)/(2x(t)) dt`, differentiation and simplification give

\[
\omega=\frac{dt}{\sqrt{1-4At^4}}
=\sum_{k\ge0}\binom{2k}{k}A^k t^{4k}\,dt.
\]

All displayed differential coefficients are integral. Integrating with
zero constant term gives the exact formal identity over `Q_5`

\[
\lambda(t)=\sum_{k\ge0}
\frac{\binom{2k}{k}A^k}{4k+1}t^{4k+1}
=t-\frac{2312}{5}t^5+\frac{2672672}{3}t^9+\cdots.
\tag{5}
\]

For `n=4k+1>=5`, the corresponding evaluated term has valuation at least
`nr-v_5(n)`. For any positive integer `n`, writing `a=v_5(n)` gives
`n>=5^a>=1+4a`, hence `v_5(n)<=(n-1)/4`. It follows that

\[
nr-v_5(n)\ \ge\ 5r-1+(n-5)(r-1/4)\ \ge\ 5r-1.
\]

These bounds tend to infinity, justify convergence, and are strict for
`n>5`. The coefficient `-2312/5` has valuation exactly `-1`, so its term
has valuation exactly `5r-1`, and no later term can cancel its leading
digit. Thus

\[
v_5(\lambda(t)-t)=5r-1,\qquad
v_5((\lambda(t)-t)/5)=5r-2.
\tag{6}
\]

For `t=t(8R)`, the elliptic logarithm is
`log_omega(R)=lambda(t)/8`; consequently

\[
\frac{\log_\omega(R)}5\equiv\frac{t(8R)}{40}
\pmod{125\mathbf Z_5}.
\]

Computing `t(8R) mod 625` suffices for this quotient modulo 125;
computing it modulo 125 suffices for the quotient modulo 25. An arbitrary
lift of a residue known only modulo 125 cannot determine the quotient
modulo 125, because division by 5 loses one digit.

## Hostile cases and evidence ceiling

* **Coefficientwise overclaim:** In (5), the coefficient of `t^25` is
  `924 A^6/25`, of valuation `-2`. Therefore multiplying the whole tail
  by 5 does not make all coefficients integral. Equation (6), not a
  global denominator-5 series bound, is the valid assertion.
* **One further digit:** If `v_5(t)=1`, the omitted contribution to
  `lambda(t)/5` has valuation exactly 3. It is zero modulo 125 but is
  nonzero modulo 625. Precision modulo 625 therefore requires the
  `-2312 t^5/25` correction. This distinguishes a correct truncation
  rule from indefinite reuse at higher precision.
* **Changed curve or parameter:** For a general short Weierstrass model
  with a nonzero constant coefficient, `(-x,iy)` need not preserve the
  curve. For a general Weierstrass equation, inversion need not be
  `t -> -t`. Neither CM coefficient sparsity nor literal odd powers may
  then be imported without a new argument.
* **Changed prime or scalar:** Existence of `i in Z_5`, good ordinary
  reduction, integral sigma coefficients and `t in 5 Z_5` are used.
  Dividing additionally by a scalar of positive 5-adic valuation loses
  further precision; the unit-8 and unit-64 conclusions do not cover it.

The normalized pair fiber is **ONE**, by the imported MST theorem and
the written transport proof. Both requested truncation obligations are
proved on the entire declared formal neighbourhood. Evidence consists
of primary-source theorem inspection and explicit written algebra and
valuation arguments. This is not a formal proof-assistant certificate,
a general sigma implementation, a modular-symbol replay, or an exact
BSD coefficient comparison. No older lane files were modified.

Verification: an inline Python `Fraction`/`math.comb` check passed for
the two displayed nonleading logarithm coefficients, the sigma `t^5`
coefficient, and `binom(12,6)=924` with its 5-adic unit numerator. This
finite transcription check supplements, and does not replace, the
all-orders arguments above.
