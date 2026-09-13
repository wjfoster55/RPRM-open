# E34: rigorous analytic rank two and leading Taylor coefficient

For E/Q: y²=x³−1156x, the independent arithmetic proof gives rank E(Q)=2.
The local audit gives conductor 18496, additive Euler factors 1 at 2 and 17,
and root number +1. With these inputs the fresh exact calculation proves

    138.20634136 <= lambda_2 <= 138.20780907,
    6.38511803 <= c_2=L''(E,1)/2 <= 6.38518585.

The decimal endpoints are exact finite decimals (rational numbers).
Here lambda_2=Lambda''(E,1)/2 for
Lambda(s)=(68/pi)^s Gamma(s)L(E,s), whereas c_2 is the coefficient of
t² in the original L(E,1+t). They are different quantities. The certified
width of the completed interval is 0.00146771, below the declared 0.01.

## The exact zero proof precedes the coefficient interpretation

E is nonsingular over Q. By modularity its L-function is entire and has
the indicated completed functional equation. These are established theorems;
the equation, conductor and sign are checked in LOCAL_ANALYTIC_INPUTS.md.

The published low-analytic-rank theorem says that if ord_(s=1)L(E,s) is
zero or one, it equals rank E(Q). Since the arithmetic rank here is two,
those two analytic orders are impossible. Thus the constant and linear
Taylor coefficients vanish exactly. The plus functional-equation sign also
kills all odd completed coefficients. This is a theorem argument, not a
deduction from approximate zeros or an assumption of BSD for E34.
[Wiles, official BSD description, printed p.4](https://www.claymath.org/wp-content/uploads/2022/05/birchswin.pdf#page=4).

The completion factor is analytic and nonzero at 1. Hence lambda_2>0 proves
the exact analytic order is two, matching the independent arithmetic rank.
Because both lower coefficients vanish, c_2=(pi/68)lambda_2. Without that
vanishing premise the scaled completed coefficient would not automatically
be the original L-function coefficient.

## Mellin identity and all omitted coefficients

Set alpha=pi/68 and g(u)=f(iu/136), where f is the normalized weight-two
newform supplied by modularity. The correct Fricke sign gives
g(1/u)=u²g(u). Splitting its Mellin integral at u=1 gives

    Lambda(1+t) = integral_1^infinity g(u)(u^t+u^(-t)) du,
    lambda_2 = sum_(n>=1) a_n J_2(alpha n),
    J_2(b) = integral_1^infinity exp(-bu)(log u)^2 du.

Exponential decay and |a_n|<=2n justify termwise integration and
differentiation uniformly on compact t-sets. Modularity and the Mellin/Fricke
normalization are the standard inputs in
[Cremona, section 2.13, equations (2.8.5), (2.13.1)](https://johncremona.github.io/book/fulltext/chapter2.pdf#page=36).
The general proof was also written in the preceding BSD starting note;
the present computation binds every input to E34.

The finite head computes every prime coefficient through its cutoff by
counting the actual reduced equation, with the bad factors handled separately.
It derives prime powers by their correct Euler recurrences and uses coprime
multiplicativity. A second implementation independently checks these values.
No database rank, conductor, special value or stored expected decimal enters.

The universal bound |a_n|<=d(n)sqrt(n)<=2n follows from Hasse, the Euler
roots and multiplicativity, including all bad-prime powers. A further
support fact is proved here, rather than guessed from the head. For every
good p congruent to 3 modulo 4, the cubic F(x)=x³−1156x is odd and
chi_p(-1)=-1. Pairing x and -x therefore cancels the full character sum;
the fixed point x=0 contributes zero. Hence a_p=0. The recurrence then
makes a_(p^k)=0 for odd k. Together with the additive factors this implies

    a_n != 0  =>  n congruent to 1 modulo 4, and 17 does not divide n.

This necessary condition is used only to drop terms proved zero; it does
not assert nonvanishing for every remaining n.

For b>0, log u<=u−1 gives J_2(b)<=2 exp(-b)/b³. Let A=alpha_lower>0,
and let a certified q<1 bound exp(-A) from above. For each cutoff M, the
radius used for the entire suffix is

    sum_(M<n<=K, n=1 mod4, 17 not dividing n)
        2 d(n) ceil(sqrt(n)) q^n / (A³ n³)
    + 4 q^(K+1) / (A³ (K+1)² (1−q)),       K=4096.

The finite sum computes divisor counts, not additional signed Euler
coefficients. Its final term bounds every n>K with the general |a_n|<=2n
bound; no support assumption is needed there. Upward dyadic rounding of
the iterative q powers preserves upper bounds. The infinite geometric
suffix uses the upward bound for q^(K+1), and the exact rational denominator
1−q. Directed rounding is included in the saved radius.

## Finite integral computation and its errors

Integration by parts and t=bu give

    J_2(b) = (2/b) H(b),
    H(b) = integral_b^infinity exp(-t) log(t/b) / t dt.

Thus S=2 sum_(n<=M) (a_n/n) H(alpha n) is alpha times the truncated
completed coefficient, without assuming any lower zero. The program divides
its signed interval by the positive alpha interval before adjoining the
completed-coefficient tail. It multiplies the final interval by alpha only
when exporting the separately interpreted c_2 enclosure.

The transformed integral is evaluated by Simpson's rule on doubling bands
from b_lower to 32, with 64 panels per band. Write L=log(t/b_lower), and

    f(t)=exp(-t)L/t,
    f''''(t)=exp(-t)[
        L(1/t+4/t²+12/t³+24/t⁴+24/t⁵)
        −(4/t²+18/t³+44/t⁴+50/t⁵)].

On each panel [l,r], the rational positive expressions in t decrease,
while L increases. Endpoint intervals bound the bracket. Multiplication
by [exp(-r)_lower,exp(-l)_upper] uses all four endpoint products, so it
also handles negative or sign-changing curvature. The integral minus
the single-panel Simpson sum lies in

    [−h^5 f4_upper/2880, −h^5 f4_lower/2880].

In particular a signed curvature error is not silently treated as positive.
Parameter uncertainty is bounded by

    H(b_lower)−H(b_actual)
        <= (b_upper−b_lower) exp(-b_lower)/b_lower²,

because H'(b)=−E1(b)/b and E1(b)<=exp(-b)/b. It is subtracted from the
lower endpoint only. The improper tail past U=32 is at most
exp(-32)/b_lower, since log(t/b_lower)/t<=1/b_lower on t>=32>=b_lower.

All elementary enclosures use rational arithmetic on an outward 2^-80
grid: Machin's arctangent identity for pi, alternating degree-31/30 bounds
for exp(-z) on 0<=z<=1 followed by monotone squaring, and a 32-term
atanh series with geometric remainder for logarithms after normalization
to [1,2]. Each panel and each signed assembly retains its error components.
The independent audit derives the calculus and checks those interval rules.

## Preserved attempts and result

The budget was written before execution: head cutoffs 40, 80, 160 in that
order, 64 Simpson panels per doubling band, no panel refinement, and
divisor-majorant cutoff 4096. At M=40 and M=80, twice the proved tail
radius alone already exceeded the width goal, so the corresponding finite
head was not evaluated. Those attempts remain OPEN_WITH_THIS_TAIL_BOUND.
They are not failures of BSD or evidence of a central zero.

At M=160 the calculation evaluated 27 nonzero terms using 7,360 panels.
The completed finite-head width is about 1.41523e-8. The whole infinite
suffix radius is about 0.000733840443. Outward export gives

    lambda_2 in [1727579267/12500000, 13820780907/100000000].

The exact raw product interval for c_2 is retained in evidence/interval.json.
The simpler decimal enclosure quoted at the start rounds that product
outward. The rank comparison follows from the exact nonzero lower bound,
not from agreement with a familiar decimal value.

The changed-model control is rejected because the input theorems are bound
to this equation. Removing the all-term tail prevents promotion of the
finite head to an L-function interval; the finite head is preserved.

## What remains outside this result

The result is rank E(Q)=analytic rank E=2, a certified second coefficient,
and the separate arithmetic 2-primary Sha result. It does not identify
the total order of Sha or prove the full BSD leading coefficient formula.
The E5 full-BSD theorem requiring analytic rank at most one cannot be
reused here. `GENERATOR_PROOF.md` now settles the saturated-basis
question; that result still does not supply the missing Sha/analytic
identity. `FACTOR_COMPARISON.md` records the resulting factor interval.

The independent review is source inspection and exact ledger reconstruction,
including freshly recomputed Euler coefficients and tails. It does not
claim an independent reevaluation of every Simpson panel. No formal proof
assistant was used. The written and computational evidence is explicit;
general BSD remains OPEN.
