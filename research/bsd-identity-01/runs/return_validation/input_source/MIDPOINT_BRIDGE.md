# The common midpoint and the analytic reflection

Date: 2026-09-12. This note develops William's clarified observation that
0.5 is the common middle of 0.6 and 0.4, and that the two sides can be
recovered through that middle. The useful mathematical content is an exact
change from two endpoints to a center and a signed displacement. The
analytic continuation of that idea is a reflection around the completed
L-function's center.

The earlier 0.6, -0.6, 0.4 and tentative “inverse” -0.4, 0.6 are retained
as exploratory examples. They do not specify a complete transformation,
domain, or iteration rule. The clarified common-middle construction is
the operation used below; no recurrence is inferred from the tentative
sign sequence. The latest correction is specifically about directed
movement: **0.6 to 0.4 has step -0.2, while its half-step is -0.1 and
ends at 0.5 without reaching the other endpoint.** That correction does
not assert cancellation of squares or Taylor coefficients. The phrase
“Summary Size” is retained without assigning it a formal mathematical
meaning here.

## 1. What can be recovered through the middle

**Contract.** Endpoint pairs are ordered elements of \(\mathbb Q^2\),
with ordinary rational equality. Decimal examples denote exact rationals.
The output is \((m,d)\in\mathbb Q^2\), where \(m\) is the midpoint
and \(d\) the first endpoint's signed displacement. The receiver retains
both endpoints and their ordering. The operation is the bijection

\[
(a,b)\longmapsto(m,d)=\left(\frac{a+b}{2},\frac{a-b}{2}\right),
\qquad (m,d)\longmapsto(a,b)=(m+d,m-d).
\tag{1}
\]

Adding and subtracting the two equations proves both inverse identities.
For the clarified pair,

\[
a=\frac35=0.6,\quad b=\frac25=0.4,
\qquad m=\frac12=0.5,\quad d=\frac1{10}=0.1.
\]

Thus the common middle and the learned displacement do derive both sides:
\(0.5+0.1=0.6\) and \(0.5-0.1=0.4\). If the middle and either one
endpoint are retained instead, the other is recovered by \(b=2m-a\).
These are two complete recovery contracts.

If only \(m=1/2\) is retained, the complete ordered-pair fiber over
\(\mathbb Q^2\) is

\[
\operatorname{MANY}\left\{\left(\frac12+d,\frac12-d\right):
d\in\mathbb Q\right\}.
\tag{2}
\]

The pairs \((0.6,0.4)\) and \((0.7,0.3)\) are distinct members of that
fiber. If endpoints are additionally restricted to \([0,1]\), the exact
fiber has \(-1/2\le d\le1/2\). If their order is prescribed by
\(a\ge b\), it has \(0\le d\le1/2\). These bounds are changes of
admitted context, not properties supplied by the midpoint alone.

Three specified operations show why the signs must keep their roles:

| Operation on endpoints | Operation on \((m,d)\) | Example from \((0.6,0.4)\) |
|---|---|---|
| Exchange \((a,b)\mapsto(b,a)\) | \((m,d)\mapsto(m,-d)\) | \((0.4,0.6)\) |
| Negate both \((a,b)\mapsto(-a,-b)\) | \((m,d)\mapsto(-m,-d)\) | \((-0.6,-0.4)\) |
| Reflect an endpoint about fixed \(m\): \(x\mapsto2m-x\) | Signed displacement \(x-m\mapsto-(x-m)\) | \(0.6\mapsto0.4\) for \(m=0.5\) |

The pair \((0.6,-0.6)\) has midpoint 0 and displacement 0.6. Its center
is different from the clarified pair's center. Ordinary negation is the
special case of reflection whose fixed midpoint is 0.

### Directed full step and half-step

To record the latest correction directly, use the oriented gap
\(\delta=b-a=-2d\). Then

\[
\delta=0.4-0.6=-0.2,\qquad
a+\delta=0.4,\qquad
a+\delta/2=0.6-0.1=0.5=m.
\tag{2a}
\]

The full first-slot movement reaches the second endpoint. Its half-step
reaches the middle and does not cross it. If the midpoint and original
directed gap are retained, recovery is exact:

\[
a=m-\delta/2,\qquad b=m+\delta/2.
\tag{2b}
\]

Exchanging endpoint slots reverses \(\delta\). Merely stopping the first
slot at the midpoint does not itself exchange the slots. If the second
endpoint is retained, the update \((a,b)\mapsto(m,b)\) is invertible,
with inverse \((m,b)\mapsto(2m-b,b)\). Thus halfway movement need not
discard the information needed for recovery.

For a separate, explicitly **analyst-defined comparison**, one can move
both endpoints simultaneously by

\[
P_\tau(a,b)=((1-\tau)a+\tau b,\;\tau a+(1-\tau)b),
\qquad0\le\tau\le1.
\tag{2c}
\]

This is a supplied interpolation family, not an inferred user recurrence.
In centered coordinates it is \((m,d)\mapsto(m,(1-2\tau)d)\):
\(\tau=0\) preserves the pair, \(\tau=1\) exchanges it, and
\(\tau=1/2\) gives \((m,m)\). The half-step in this whole-pair
model has zero separation, so it has not exchanged the endpoints.
For known \(\tau\ne1/2\), the original displacement is recovered
by dividing the output displacement by \(1-2\tau\). At
\(\tau=1/2\), retaining only the two new positions loses the original
gap. A retained original gap (or equivalent information sufficient to
recover it) restores the inverse; the phase value \(\tau=1/2\) alone
does not.

## 2. The exact half-center in the completed L-function

The existing [general analytic bridge](../bsd-general-01/ANALYTIC_BRIDGE.md),
§2, uses the standard elliptic-curve normalization

\[
\alpha=\frac{2\pi}{\sqrt N},\qquad
\Lambda(s)=\alpha^{-s}\Gamma(s)L(E,s),\qquad
\Lambda(2-s)=w\Lambda(s),\quad w\in\{+1,-1\}.
\tag{3}
\]

This completion and functional equation are given in Cremona's
*Algorithms for Modular Elliptic Curves*, equations (2.8.5)–(2.8.6),
printed page 29. His Fricke eigenvalue is \(\varepsilon_N=-w\);
the sign change is essential.
[Cremona, chapter 2, page 29](https://johncremona.github.io/book/fulltext/chapter2.pdf#page=23)

The analytic carrier here is the entire completed function of a modular
elliptic curve over \(\mathbb Q\), with its actual conductor, Euler
factors and root number. This uses modularity and its functional equation
as established theorems, with the hypotheses and Mellin justification in
the linked general bridge. Its equality is equality of analytic functions,
and its requested readout is the central Taylor coefficients and zero order.

To place its center at a half, define

\[
z=s/2,\qquad F(z)=\Lambda(2z).
\]

This substitution is invertible, and equation (3) becomes

\[
F(1-z)=wF(z).
\tag{4}
\]

The fixed midpoint is now \(z=1/2\). Writing \(z=1/2+d\) gives

\[
F(1/2+d)=\Lambda(1+2d),\qquad
F(1/2-d)=wF(1/2+d).
\tag{5}
\]

For example, \(z=0.6\) and \(z=0.4\) correspond to \(s=1.2\) and
\(s=0.8\). The midpoint construction identifies the reflection's paired
**arguments**. The root number then determines whether the function's
**values** at those arguments agree or have opposite signs. The endpoint
decimals are not asserted to be values of \(F\).

The corrected directed half-step therefore has a valid argument-level
bridge: from \(z=0.6\) toward \(z=0.4\), it reaches \(z=0.5\),
and in the original variable it moves from \(s=1.2\) to \(s=1\).
Equation (4) compares values at reflected endpoint arguments. It does
not identify the midpoint value with the average of the endpoint values.
For instance \(F(1/2+d)=d^2\) has equal positive values at the two
nonzero reflected displacements and zero at the midpoint. An additional
relation is needed to pass from directed argument movement to a conclusion
about an analytic coefficient.

Thus the half is a natural fixed point in this normalized coordinate.
In the original elliptic-curve coordinate, the same fixed point is 1.
The substitution preserves the zero order; it does not add an analytic
constraint.

## 3. Exactly which coefficients the reflection determines

Let

\[
\Lambda(1+t)=\sum_{k\ge0}\lambda_k t^k,
\qquad F(1/2+d)=\sum_{k\ge0}\beta_k d^k.
\]

Substituting \(t=2d\) gives the exact scale conversion

\[
\boxed{\beta_k=2^k\lambda_k},\qquad
F^{(k)}(1/2)=2^k\Lambda^{(k)}(1).
\tag{6}
\]

In particular the quadratic coefficient becomes \(4\lambda_2\),
and the quartic coefficient becomes \(16\lambda_4\). Since these
scale factors are nonzero, vanishing and the first nonzero index are
unchanged.

By (5) and uniqueness of Taylor coefficients,

\[
\sum_k(-1)^k\beta_k d^k=w\sum_k\beta_k d^k,
\qquad ((-1)^k-w)\beta_k=0\quad\text{for every }k.
\tag{7}
\]

This is a written proof of the parity consequence:

| Reflection sign | Coefficients forced to zero | Coefficients still permitted |
|---|---|---|
| \(w=-1\) | All even indices, including the constant | Odd indices |
| \(w=+1\) | All odd indices | Even indices, including the constant |

The reflection therefore supplies exact cancellations in the forbidden
parity. For \(w=+1\), a claim of order four still requires
\(\beta_0=\beta_2=0\) and \(\beta_4\ne0\). The parent bridge's
independent arithmetic-rank and low-analytic-rank theorem can supply
\(\beta_0=0\) when the proved arithmetic rank is at least two.
The first further same-parity obligation at rank four remains
\(\beta_2=0\), equivalently \(\lambda_2=0\). Neither the half-center
nor a positive quartic coefficient supplies that equality.

These parity equations concern \(\Lambda\) and \(F\). The raw
\(L(E,1+t)\) also has its gamma and conductor factors; it need not be
even or odd. The general bridge, equation (4), retains the required
triangular coefficient conversion. Cremona's Proposition 2.13.1 likewise
states the lower-vanishing premise for its derivative formula.
[Cremona, Proposition 2.13.1](https://johncremona.github.io/book/fulltext/chapter2.pdf#page=37)

An exact distinguishing pair makes the remaining freedom visible. For
any rational \(\epsilon>0\), define analytic germs by

\[
F_0(1/2+d)=d^4,\qquad
F_\epsilon(1/2+d)=d^4+\epsilon d^2.
\tag{8}
\]

Both have \(+1\) reflection symmetry, value zero at the midpoint,
quartic coefficient 1, and strictly positive values at every nonzero real
displacement. Their zero orders are respectively 4 and 2. On
\(|d|\le D\), their value difference is at most \(\epsilon D^2\),
which can be made arbitrarily small by choosing \(\epsilon\).
These are polynomial controls on the proposed inference from analytic
symmetry and small coefficients. They are not asserted to be elliptic-curve
L-functions or counterexamples to BSD.

## 4. What an additional equal-and-opposite pairing could prove

The user's correction supplies a directed-step rule. Separately, if a
later proposed bridge requires a coefficient to vanish, the following
is one sufficient mechanism to test; it is not attributed to that
correction. Let \((X,\mu)\) be a space with a finite
signed measure, and let \(T:X\to X\) be a measurable involution. Assume
that \(T_*\mu=\mu\), and that \(h\) is integrable with respect to
the total variation of \(\mu\), with \(h\circ T=-h\) almost
everywhere. Then

\[
\int_Xh\,d\mu=\int_Xh\circ T\,d\mu
=-\int_Xh\,d\mu,
\qquad\boxed{\int_Xh\,d\mu=0}.
\tag{9}
\]

This proof uses both preservation of the measure and the opposite-value
condition. For a finite or absolutely convergent sum, the analogous
certificate is an involution on all contributing indices that pairs
equal-and-opposite **weighted terms**; its fixed terms must be zero.
Absolute convergence licenses rearrangement. Paired names or equal
distances alone do not imply equal weighted contributions.

For example, the actual permitted-parity coefficient for \(w=+1\) is

\[
\lambda_2=\sum_{n\ge1}a_nJ_2(\alpha n),\qquad
J_2(b)=\int_1^\infty e^{-bu}(\log u)^2\,du>0.
\tag{10}
\]

An involution \(T\) on these indices satisfying
\(a_{T(n)}J_2(\alpha T(n))=-a_nJ_2(\alpha n)\), with complete
coverage, would prove the desired cancellation. It would be additional
structure to establish for the actual coefficient sum. The functional
equation already supplies reflection in the analytic argument; for
\(w=+1\) that reflection preserves the quadratic term, as (7) shows.
No such further coefficient-pairing involution is constructed in this
note. Its existence for a proposed rank-four target remains an explicit
open port.

## 5. Replay and evidence ceiling

```powershell
python -I -B research/bsd-rank-two-01/work/midpoint.py --output research/bsd-rank-two-01/evidence/midpoint.json
```

The replay uses exact `Fraction` arithmetic. It checks (1) and the two
sign operations on all 441 ordered pairs from the declared grid
\(\{j/10:-10\le j\le10\}\), coefficient factors \(2^k\), both
parities, the distinct orders in (8) using \(\epsilon=10^{-12}\),
and a finite signed-measure example of (9). Two controls break measure
preservation or opposite-value pairing and give nonzero sums.
It also checks the corrected directed gap -0.2 and half-gap -0.1,
recovery from midpoint plus original gap, and the analyst's whole-pair
interpolation at five exact phases for each grid pair.

The algebraic inverse identities, parity implication, coefficient scaling,
polynomial zero orders and cancellation lemma are written proofs above;
the executable evidence is their bounded rational replay. The analytic
functional equation is a cited theorem. No new historical RPRM mathematics,
novelty claim, physical interpretation, or new L-value/rank calculation
is inferred from this construction. The common middle has a precise role:
it gives the reflection's fixed point and an exact recovery coordinate
when the displacement is retained. A higher central zero requires the
additional same-parity cancellation just identified.
