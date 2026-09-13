# Independent reviewer method — E5 interval

Date: 12 September 2026. This is new review work, not a claim about what Codex ran.
The reviewed return is `BSD_E5_CODEX_TEST_01_RETURN.zip`.

## Scope

The reviewer independently reimplements the *finite numerical enclosure* for
E: y^2=x^3-25x. The implementation does not import any submitted checker.
It shares the mathematically justified derivative identity and Hasse-derived
coefficient-tail theorem. It is not an independent proof of modularity, a
formal proof-assistant run, or a different global L-function backend.

The fixed-curve identity is

    L'(E,1) = 2 sum_(n>=1) (a_n/n) E1(alpha*n),
    alpha = pi/(10 sqrt(2)),
    E1(x) = integral_x^infinity exp(-t)/t dt.

The return's `ANALYTIC_THEOREMS.md` verifies conductor 800, sign -1, additive
Euler factors at 2 and 5, and Mellin normalization. The official Sage reference
explicitly states that the derivative formula assumes L(E,1)=0:
https://doc.sagemath.org/html/en/reference/arithmetic_curves/sage/schemes/elliptic_curves/lseries_ell.html
The positive-real definition of E1 is DLMF 6.2.1:
https://dlmf.nist.gov/6.2#E1

## Independent constants

Use pi=4(atan(1/2)+atan(1/3)), not the submitted Machin formula. The tangent
addition formula gives tangent 1, and the positive angle sum is less than
1/2+1/3<1<pi/2, fixing the branch. Eighty alternating terms per arctangent
and the next term enclose the two angles. The integer square root of
2*10^72 supplies rigorous bounds on sqrt(2). All arithmetic is rational,
with outward rounding to the grid 10^-36. This gives an interval for alpha;
in particular 1/5<alpha<1/4.

## Independent exponentials

For x>=0, reduce to z=x/2^k<=1. Sum the *positive* exponential series

    S_N = sum_(j=0)^N z^j/j!, N=40.

The next term is t_(N+1). Subsequent term ratios are at most z/(N+2), hence

    S_N <= exp(z) <= S_N + t_(N+1)/(1-z/(N+2)).

Invert these positive endpoints to enclose exp(-z), then square k times.
Every reciprocal and squaring uses directed rational rounding. This differs
from the submitted alternating negative-exponential series.

## Independent integral quadrature and its conservative bound

Write f(t)=exp(-t)/t. On a panel [a,b] of width L, midpoint m, use

    S = L/6 * (f(a)+4f(m)+f(b)).

Instead of importing a sharp Simpson-error theorem, a direct Taylor argument
supplies a deliberately conservative bound. Let h=L/2 and M bound |f''''|
on the panel. Taylor expansion to degree three around m has remainder at
most M|t-m|^4/24. Its integral is bounded by M h^5/60. The quadrature of
its remainder is bounded by M h^5/36. Simpson integrates the cubic exactly,
so

    |integral_a^b f(t)dt - S| <= (1/60+1/36) M h^5
                              = M L^5/720.

For our positive t,

    f''''(t)=exp(-t)*(1/t+4/t^2+12/t^3+24/t^4+24/t^5).

Each summand is positive and decreasing. Thus the independently enclosed
upper exponential at a gives an upper bound on M. Enclose S using the
three independent exponential intervals, then subtract/add the upward-rounded
error bound. No one-sided Simpson error sign is assumed.

Integrate from x_lo to 32 using doubling bands with 16 panels per band.
The argument error is at most (x_hi-x_lo)/x_lo and is subtracted from the
lower endpoint only. The positive tail after 32 is at most exp(-32)/32
and is added to the upper endpoint. Every endpoint and error operation
uses exact fractions and outward rounding.

## Signed series and the unopened coefficient tail

Prime counts through 40 are freshly enumerated as all coordinate pairs plus
O. Good-prime Euler recurrences and multiplicativity produce the same six
nonzero coefficients, at n=1,9,13,17,29,37. Bad-prime coefficients are zero.

Multiply each independently enclosed E1 term by 2a_n/n, reversing endpoints
for a negative weight. The same all-n coefficient theorem |a_n|<=2n gives

    |tail after 40| < (120/41)*(5/6)^41.

Add this symmetric error bound, then round outwards to denominator 10^9.
The independently obtained final interval is

    2.225705022 < L'(E,1) < 2.229026982.

It is entirely contained in Codex's interval

    2.225484 < L'(E,1) < 2.229058.

Every independently computed E1 enclosure is also contained in the
corresponding submitted enclosure. These comparisons are exact rational
comparisons. The main accepted delivered result remains the Codex interval;
the reviewer interval is independent cross-check evidence, not a performance
comparison or a new curve result.

## Other independent finite checks

The reviewer directly enumerates primitive covering solutions modulo 2,4,8,
checks all eight rational representatives and their squareclasses, and verifies
the 32-vertex cube map and all 1024 group-law pairs. A separate script checks
118 recorded reconstruction identities and all 304 displayed halving trace
steps with its own rational group arithmetic.

These finite checks do not replace Kummer theory, Mordell-Weil, or the written
all-place/denominator argument. Their respective scopes are preserved.
