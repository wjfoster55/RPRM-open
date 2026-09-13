# Independent analytic calculation and certified first central coefficient

For the fixed curve `E: y^2=x^3-25x` over Q, the new exact computation gives

\[
\boxed{\quad \frac{556371}{250000}<L'(E,1)<\frac{1114529}{500000}\quad}.
\]

These endpoints are exactly `2.225484` and `2.229058`; their exact difference
is `1787/500000 = 0.003574 < 1/100`. The value bounded is the number multiplying
`t` in `L(E,1+t)`, not an Euler coefficient `a_n`. Combining this positive
interval with the separately checked exact central zero proves that the zero
has order one. It does not compute the other quantities in the full BSD formula.

## Contract, evidence, and inputs

The mathematical carrier is this elliptic curve's Euler coefficients over the
integers and its analytically continued L-function; numerical enclosures have
rational endpoints and ordinary equality. The supplied ports are the fixed
model, the Euler-factor theorem, the Hasse bound, and the independently checked
sign-minus central-derivative identity. The requested readout is a positive
rational enclosure of width at most `1/100` for `c1=L'(E,1)`.

Evaluation is enabled once these analytic premises are supplied with their
checked hypotheses. The representation is a finite coefficient head together
with a bound on every omitted term. It preserves the requested interval and
nonvanishing question. It does not reconstruct all Euler coefficients, all
digits of the derivative, or the original L-function from this interval. No
complete preimage fiber of that lossy representation is asserted, and there is
no inverse or singleton-source claim.

The evidence is an independently written exact rational computation plus the
written inequalities below, using standard cited elliptic-curve theorems. It
is not a formal proof, a rigorous-ball backend comparison, or a reuse of an
archived receipt. The local source checker was not imported or run by this
implementation. Source mathematics was read openly. The original programs'
fresh replay is separately reported by the parent task. No arithmetic rank,
BSD prediction, or exposed decimal target enters this calculation.

The analytic identity and hypotheses are checked separately in task B01,
in [ANALYTIC_THEOREMS.md](ANALYTIC_THEOREMS.md):

\[
c_1=2\sum_{n\ge1}\frac{a_n}{n}E_1(\alpha n),\qquad
\alpha=\frac{\pi}{10\sqrt2},\qquad
E_1(x)=\int_x^\infty\frac{e^{-t}}t\,dt.
\]

That dependency includes conductor 800, root sign -1, additive factors 1 at
2 and 5, modularity, Mellin normalization, and the justification for the
convergent representation at the center. A finite arithmetic check does not
establish those theorems. The Hasse source is [MIT 18.783 Fall 2023, Lecture 7,
§7.2 Theorem 7.3](https://math.mit.edu/classes/18.783/2023/LectureNotes7.pdf);
the separate source worker checked this actual theorem and its specialization.
The identity's documented convention is [Sage `Lseries_ell.deriv_at1`](https://doc.sagemath.org/html/en/reference/arithmetic_curves/sage/schemes/elliptic_curves/lseries_ell.html),
with the Mellin derivation included in B01. This script does not call Sage.

## Independent finite Euler coefficients

For every odd prime through the current cutoff, the checker computes

\[
\chi_p(x^3-25x)\quad\text{using Euler's criterion},\qquad
\#E(\mathbf F_p)=p+1+\sum_{x=0}^{p-1}\chi_p(x^3-25x).
\]

Here a zero right-hand side contributes 0 to the character sum and has one
square root; a nonzero square contributes 1 and has two roots; a nonsquare
contributes -1 and has none. This is independently structured from the supplied
pair-enumeration/root-multiplicity routes. At p=2 the two affine solutions are
explicitly enumerated, giving three projective model points. At the bad primes
these are singular model counts; no nonsingular elliptic reduction is presumed.

| p | Projective model count | a_p | Local status |
|---:|---:|---:|---|
| 2 | 3 | 0 | additive |
| 3 | 4 | 0 | good |
| 5 | 6 | 0 | additive |
| 7 | 8 | 0 | good |
| 11 | 12 | 0 | good |
| 13 | 20 | -6 | good |
| 17 | 20 | -2 | good |
| 19 | 20 | 0 | good |
| 23 | 24 | 0 | good |
| 29 | 40 | -10 | good |
| 31 | 32 | 0 | good |
| 37 | 36 | 2 | good |

The code assigns zero to every coefficient divisible by 2 or 5 from their
additive local factors. It never applies the good-prime recurrence there.
For each other prime factor it generates

\[
a_{p^0}=1,\quad a_{p^1}=a_p,\quad
a_{p^k}=a_pa_{p^{k-1}}-p a_{p^{k-2}},
\]

and multiplies the coprime prime-power coefficients. The only nonzero values
through 20 are `(1,1),(9,-3),(13,-6),(17,-2)`. Through 40 the additional
nonzero values are `(29,-10),(37,2)`. In particular `a9=a3^2-3=-3`.
The complete coefficient table, rather than just its nonzero entries, is saved.
The finite Hasse inequalities also checked by the code are consistency tests;
the all-prime theorem is the independently cited mathematical input.

## All-term coverage

At a good prime, Hasse gives `|a_p|<=2 sqrt(p)`. The two roots r,s of
`X^2-a_p X+p` therefore have absolute value `sqrt(p)`. Expanding the Euler
factor as `1/((1-rT)(1-sT))` gives

\[
a_{p^k}=\sum_{j=0}^k r^j s^{k-j},\qquad
|a_{p^k}|\le(k+1)p^{k/2}.
\]

Multiplicativity implies `|a_n|<=d(n) sqrt(n)` for n prime to 10; an integer
divisible by 2 or 5 has coefficient zero and obeys the same inequality.
Pair every divisor d with n/d. There are at most `floor(sqrt(n))` divisors on
the lower side and at most that many partners, so `d(n)<=2 sqrt(n)`.
Consequently `|a_n|<=2n` for **every integer n>=1**, not just the finite table.

For x>0, positivity and `1/t<=1/x` on `[x,infinity)` give

\[
0<E_1(x)\le e^{-x}/x.
\]

The exact constant construction below proves `1/5<alpha<1/4`.
Since `exp(alpha)>1+alpha>6/5`, `exp(-alpha)<q=5/6`. Thus for every M>=1,

\[
\begin{aligned}
|R_M|
&=\left|2\sum_{n\ge M+1}(a_n/n)E_1(\alpha n)\right|\\
&\le4\sum_{n\ge M+1}E_1(\alpha n)\\
&<20\sum_{n\ge M+1}q^n/n\\
&\le\frac{20}{M+1}\sum_{n\ge M+1}q^n
=\frac{120}{M+1}q^{M+1}.
\end{aligned}
\]

The geometric series is over the entire infinite suffix, independent of its
unknown signs or possible additional zeros. The bound is strict because the
coarse alpha and exponential inequalities are strict.

## Every algebraic step in the baseline positivity certificate

The factorial expansion gives `e<3`: for k>=2, `k!>=2^(k-1)`, with strict
inequality for k>=3, so `sum_(k>=2) 1/k! < sum_(k>=2) 2^(-(k-1)) = 1`.
The positive integrated geometric series gives
`log(2)=2(1/3+(1/3)^3/3+(1/3)^5/5+...)>2/3`.
Using `alpha<1/4` and `exp(-t)>1/3` for `1/4<=t<=1` therefore yields

\[
2E_1(\alpha)>2\int_{1/4}^{1}e^{-t}\,dt/t
>\frac23\log4>\frac89.
\]

Each retained negative term has magnitude less than
`10 |a_n| q^n/n^2`. The separate rational contributions are

| n | a_n | Upper bound on magnitude of `2 a_n E1(alpha n)/n` |
|---:|---:|---:|
| 9 | -3 | `9765625/136048896` |
| 13 | -6 | `6103515625/183938107392` |
| 17 | -2 | `3814697265625/1222951144882176` |

Their sum is exactly
`Bneg = 22338243056640625/206678743485087744`.
The entire n>=21 tail is bounded in absolute value by

\[
T_{20}=\frac{120}{21}(5/6)^{21}
=\frac{2384185791015625}{19194831810330624}.
\]

All other terms through 20 vanish. Subtracting these three quantities using
exact fractions reconstructs

\[
c_1>\frac89-B_{\rm neg}-T_{20}
=\frac{615556405007957768183}{937494780448358006784}
>\frac{13}{20}.
\]

The exact final margin above `13/20` is
`30923988582625318867/4687473902241790033920`. The advertised rational is
only compared after all operands are independently computed. This agreement
alone would not establish the analytic premises recorded above.

## Declared finite budget and actual stopping point

The file `work/INTERVAL_BUDGET.json` was written before the first interval run.
Its SHA-256 recorded at execution is
`26731f4d32e764490da30358b36e9acf02d65a1dcac8159c98fd9df561ac1895`.
The digest identifies those bytes; the observable execution order is the
predeclaration evidence, and neither establishes mathematics by hashing.

The fixed order is M=40,80,160; for each M, try K=32,64,128 panels per doubling
band, and stop the whole calculation at the first positive enclosure of width
at most `1/100`. The integration endpoint is B=32; the dyadic grid has 80 bits;
there are at most eight doubling bands and 1024 panels per retained term.
The arctangent and exponential truncation degrees were also fixed beforehand.

The first attempt M=40,K=32 passed. It used six nonzero coefficients and
respectively 256,160,128,128,96,64 panels, totaling 832. The later K and M
values were **not run**. A portable reproduction of that same completed run
is a replay of the fixed computation, not further search or refinement.

## Rational alpha enclosure

For `0<z<1`, the alternating arctangent series gives adjacent rigorous bounds
by its S_m partial sum and S_(m+1). The code uses m=64 for z=1/5 and m=20 for
z=1/239, then forms `pi=16 atan(1/5)-4 atan(1/239)` with signs respected.

For completeness, this Machin identity has no unspecified tangent branch.
Put theta=atan(1/5), phi=atan(1/239). The tangent-doubling formula gives
`tan(2 theta)=5/12`, `tan(4 theta)=120/119`, and hence
`tan(4 theta-phi)=1`. Also `theta>phi>0`, and
`0<4 theta-phi<4/5<pi/2` (the elementary geometric inequality pi>2 suffices).
On this first-quadrant branch the angle is pi/4, proving the identity.

With D=2^80, the square-root calculation uses `r=isqrt(2 D^2)` and verifies
`r^2<2D^2<(r+1)^2`. Thus `r/D<sqrt2<(r+1)/D`. The exact rational integer
witnesses and outward-rounded pi and sqrt2 bounds are in the JSON.
Positive division with the denominator endpoints reversed, followed by
outward dyadic rounding, gives

\[
\frac{134277897436623868511801}{604462909807314587353088}
\le\alpha\le
\frac{268555794873247737023603}{1208925819614629174706176}.
\]

These bounds themselves imply `1/5<alpha<1/4`; the computation is not relying
on decimal pi or a floating square root.

## Certified exp and E1 evaluations

For a nonnegative rational r, divide by `2^k` until `z=r/2^k<=1`.
The alternating exponential series has decreasing nonnegative term magnitudes,
so its degree-31 partial sum is below `exp(-z)` and its degree-30 partial sum
is above it. Round the lower bound down and the upper bound up to multiples
of `2^-80`. Both are nonnegative; squaring preserves their order. Square k
times with outward dyadic rounding at every step. This constructs an enclosure
of `exp(-r)` without treating observed convergence as a proof.

For retained term n, let `[x_lo,x_hi]=n[alpha_lo,alpha_hi]`. Evaluate at x_lo.
The alpha uncertainty is separately covered by

\[
0\le E_1(x_{\rm lo})-E_1(x)\le
\int_{x_{\rm lo}}^{x_{\rm hi}}dt/x_{\rm lo}
= (x_{\rm hi}-x_{\rm lo})/x_{\rm lo}.
\]

Round this loss upward and subtract it only from the final E1 lower bound.

Partition `[x_lo,32]` into bands `[x_lo,2x_lo]`, `[2x_lo,4x_lo]`, etc.,
shortening the last band at 32; divide each into K equal rational panels.
On one panel `[u,u+h]` use midpoint m. For `f(t)=exp(-t)/t`,

\[
f''(t)=e^{-t}(1/t+2/t^2+2/t^3)>0,
\qquad
f'''(t)=-e^{-t}(1/t+3/t^2+6/t^3+6/t^4)<0.
\]

Convexity gives `h f(m)<=integral f`. Taylor's theorem or the integrated
second-derivative remainder gives

\[
0\le\int_u^{u+h}f(t)\,dt-hf(m)
\le \frac{h^3}{24}\sup_{[u,u+h]}f''
=\frac{h^3}{24}f''(u).
\]

The factor 1/24 comes from integrating `(t-m)^2/2` over the centered panel;
the linear Taylor term integrates to zero. The displayed negative third
derivative justifies choosing the **left endpoint** for the supremum.
The certified upper exponential at u supplies an upper bound for f''(u).

Each `h exp(-m)/m` lower and upper contribution is rounded outward to the
80-bit grid. All upper curvature-error contributions are rounded upward.
Finally `0<E1(32)<=exp(-32)/32` supplies an upper bound on the integration
tail. The E1 lower endpoint is the summed lower midpoint contribution minus
alpha loss; its upper endpoint is the summed upper midpoint contribution plus
the curvature bound plus this integral tail.

Each retained E1 record saves x endpoints, midpoint endpoints, alpha loss,
curvature bound, exponential/rounding gap, integral tail, full E1 endpoints,
panel counts, and its signed contribution. The code verifies the exact identity

`E1 width = alpha loss + midpoint enclosure gap + curvature bound + integral tail`.

It additionally bounds the midpoint gap by the sum of the propagated
exponential interval widths plus `2 * panel_count * 2^-80` for outward
rounding. The curvature bound includes its own exponential upper enclosure
and upward rounding (the latter at most `panel_count * 2^-80`); these are
already included, not silently discarded. If a permitted later-cutoff term
had `x_lo>=32`, the budgeted direct branch would use
`0<=E1(x)<=exp(-x_lo)/x_lo`; that branch was not needed in the successful run.

## Signed combination and the complete error ledger

For each n multiply its E1 interval by `2a_n/n`. A negative multiplier swaps
the lower and upper endpoints. These multiplications and all additions use
exact `Fraction` arithmetic, so their rounding contribution is exactly zero.
The summed finite head is enclosed by

\[
\left[
\frac{957703659238384762517985725821}{430014309574013790128399450112},
\frac{957813149603364226864572400643}{430014309574013790128399450112}
\right].
\]

For M=40 the **entire infinite coefficient tail radius** is

\[
T_{40}=\frac{120}{41}(5/6)^{41}
=\frac{227373675443232059478759765625}
{137016819023148274195348171259904}.
\]

Subtract T40 from the head's lower endpoint and add it to the upper endpoint.
Those raw rational endpoints are saved. Then round outward to denominator
1,000,000 solely for a readable delivered interval, including this enlargement
in the width and success test. Strict `|R40|<T40` proves the strict final
inequalities even though some intermediate endpoint bounds are non-strict.

The machine ledger contains exact rational contributions summing identically
to `1787/500000`. The following simpler rational upper bounds help show scale;
they are rounded bounds, not the ledger operands.

| Contribution to final interval width | Simple rational upper bound |
|---|---:|
| Alpha enclosure, propagated through every retained term | `< 2/10^23` |
| Retained quadrature curvature bounds | `< 255/10^6` |
| Retained midpoint exponential enclosures and outward rounding | `< 8/10^22` |
| Retained tails of the defining E1 integrals after 32 | `< 2/10^15` |
| Entire coefficient tail after n=40, two-sided width 2T40 | `< 3319/10^6` |
| Signed multiplication and summation rounding | `0` |
| Final outward endpoint export enlargement | `< 1/2000000` |

The coefficient tail dominates this deliberately conservative enclosure. No
unopened coefficient is assumed to vanish. Decimal stable digits play no part
in the proof or stopping rule.

## Two executed analytic controls

**K03.** The checker wrote an actual complete coefficient record through 20,
copied it, and changed its `a9` field to zero. It read that mutated JSON through
the recurrence check and obtained `a3^2-3=-3`, whereas the supplied field was
0: a mismatch of 3. The false record was rejected and the program succeeded.
Both actual records are retained under `evidence/controls/`.

**K04.** The interval code promotes an actual finite-head claim by consuming
its accompanying all-term tail premise and reconstructing the rational tail
radius. The control copied that same claim representation and deleted the
`all_term_coefficient_bound` premise. The same promotion path returned
`OPEN`, refused the infinite-sum promotion, and returned no infinite interval.
Its finite-head interval remains available. This demonstrates exactly the
missing coverage obligation; it neither refutes nonvanishing nor credits some
other proof that was not supplied on that path. The check requires presence
and correct scope of the cited theorem but does not pretend that a string
field proves Hasse; the written/source evidence supplies that theorem.

## Reproduction and limits

From the experiment directory, run:

```text
python -B work/analytic_check.py --output-dir runs/fresh_analytic
```

The default output directory is the experiment root. The program reads the
pre-existing budget file before computing the first interval, and writes
`DERIVATIVE_INTERVAL.json`, `evidence/analytic.json`, and the four actual
control-input JSON files. The original first-execution command output is
`evidence/analytic-command.log`. It uses the Python standard library only.
Hashes record byte identities, and the run's elapsed-time field is only a
display measurement; neither is used as mathematical evidence.

All B02 arithmetic and both analytic controls passed; D01 met the requested
width on the first allowed attempt. The source baseline needed no repair in
this independently checked analytic portion. Optional external ball backends
and formal proof assistants were not run. The interval does not settle full
BSD, generator saturation, or any odd-primary Sha question.
