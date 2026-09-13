# Certified BSD factors for E5

For the fixed minimal model `E: y^2=x^3-25x` and `P=(-4,6)`, the new
standard-library rational computation proves these enclosing intervals. Every
displayed terminating decimal here denotes the exact rational number it writes.

| Quantity | Certified enclosure or exact value |
|---|---:|
| Real period, all real components, `Omega` | `[2.345239572925, 2.345239572926]` |
| BSD canonical height of `P` | `[1.899437, 1.899511]` |
| Tamagawa number `c2` | `2` |
| Tamagawa number `c5` | `4` |
| Other finite Tamagawa numbers | `1` |
| Rational torsion order | `4` |
| `A = Omega * height(P) * 8 / 16` | `[2.227317, 2.227404]` |
| Prior certified `L'(E,1) / A` | `[0.999138, 1.000782]` |

The [primitive-generator proof](GENERATOR_PROOF.md) identifies this height with
the rank-one regulator. The factors and intervals alone do not prove the full BSD
identity: that is the separate theorem input. With those two dependencies, the
last row encloses the positive integer `#Sha(E/Q)` and forces it to be `1`.
The interval is not being rounded to an integer on numerical-agreement grounds.

## Contract and provenance

The carrier is this one elliptic curve over Q, its minimal differential,
rational points, local component indices, and real limits enclosed by rational
endpoints. Ordinary rational and real equality apply. Supplied ports are the
model, `P`, the accepted analytic derivative interval, the torsion proof, and the
cited height, AGM, and Tate-algorithm results. The operation is forward exact
specialization and enclosure; changing the model or the height/period convention
disables reuse. The receiver retains the factor normalization and the complete
infinite tails. There is no inverse reconstruction of the L-function, no
exhaustive source-curve fiber, and no general elliptic-curve algorithm claim.

The implementation is [work/bsd_factors.py](work/bsd_factors.py); its rational
operands, seven AGM iterates, eight exact point doublings, final coordinates in
hexadecimal, logarithm bounds, all-term height tail, and quotient are recorded in
[evidence/bsd_factors.json](evidence/bsd_factors.json). This is a written proof
and exact finite computation using cited mathematics, not a formal proof.
The source hash identifies bytes and is not evidence of their mathematical
correctness. No elliptic-curve database or floating-point backend was called.

The reused derivative is strictly between `556371/250000` and
`1114529/500000`, proved in the prior
[INTERVAL_DERIVATION.md](supplied_review/BSD_E5_REVIEW/input/BSD_E5_CODEX_TEST_01_RETURN/INTERVAL_DERIVATION.md). Its analytic
normalization and minimal-model proof are in
[ANALYTIC_THEOREMS.md](supplied_review/BSD_E5_REVIEW/input/BSD_E5_CODEX_TEST_01_RETURN/ANALYTIC_THEOREMS.md). Those baseline
calculations were not rerun. The accepted
[TORSION_COROLLARY.md](supplied_review/BSD_E5_REVIEW/TORSION_COROLLARY.md)
proves `E(Q)_tors=E(Q)[2]` of order four from good reduction at 3; it does not
prove primitivity. The new script imports no prior implementation.

## Differential and height normalization

The discriminant is `1,000,000=2^6*5^6`. Discriminant valuations of integral
isomorphic models differ by multiples of 12, so this integral model is minimal
at every prime. Its minimal invariant differential is `omega=dx/(2y)`.

For reduced `x(Q)=a/b`, `b>0`, put `H_x(Q)=max(|a|,b)` and

    hhat(Q) = lim_(n->infinity) 4^(-n) log H_x(2^n Q),
    <Q,R> = (hhat(Q+R)-hhat(Q)-hhat(R))/2.

The diagonal of this pairing is `hhat(Q)`, hence the rank-one regulator of a
primitive `P` is `hhat(P)`. Cremona explicitly identifies this full-height
normalization as the BSD convention and distinguishes it from the half-height
convention. [Cremona, §3.4, printed pp.71–72](https://johncremona.github.io/book/fulltext/chapter3.pdf#page=10)

The total period used below agrees with the `Omega` specified in the leading
coefficient formula of Creutz–Miller Theorem 1.1: the integral of the absolute
minimal differential over **all** of `E(R)`.
[Creutz–Miller, printed p.2](https://arxiv.org/pdf/1105.4018#page=2)

## Real period and its entire limit

The three real roots are `-5,0,5`. The real locus has two components: the oval
above `[-5,0]`, and the component above `[5,infinity)` together with infinity.
On each, adding the upper and lower branches cancels the differential's `1/2`.
Thus the two positive component integrals are

    I = integral_5^infinity dx / sqrt(x(x-5)(x+5)),
    J = integral_-5^0 dx / sqrt(x(x-5)(x+5)).

In `I`, substitute `x=10/t^2-5`; in `J`, substitute `x=-5+5t^2`.
Direct differentiation and factoring give, in both cases,

    I = J = (2/sqrt(10)) integral_0^1
             dt / sqrt((1-t^2)(1-t^2/2))
          = (2/sqrt(10)) K(1/sqrt(2)).

Consequently

    Omega = I+J = 4 K(1/sqrt(2))/sqrt(10)
          = 2*pi / (sqrt(10)*AGM(1,1/sqrt(2))).

The last equality is the AGM identity for the complete elliptic integral.
[NIST DLMF 19.8.1 and 19.8.5](https://dlmf.nist.gov/19.8#E5)

For initial positive `a0=1`, `g0=1/sqrt(2)`, define
`a_(j+1)=(a_j+g_j)/2`, `g_(j+1)=sqrt(a_j*g_j)`. Arithmetic-geometric mean
inequality shows `g_j <= AGM <= a_j` at **every** step; their common limit is
the AGM. This bounds all uncomputed iterations, not merely the last observed
change. The code propagates rational lower and upper endpoints through seven
steps and uses `[g7_lower,a7_upper]` for the limit. Every operation is rounded
outward to denominator `2^100`.

Square roots use `r=isqrt(floor(x*2^200))` with the explicitly checked
inequalities `(r/2^100)^2 <= x < ((r+1)/2^100)^2`. The interval for pi comes
from `16 atan(1/5)-4 atan(1/239)` and adjacent alternating partial sums of 64
and 20 terms. The branch proof for this Machin identity is the one documented
in the prior interval derivation. All arithmetic is repeated exactly here;
no decimal value of pi or square root is an input. The raw period enclosure
has width below `10^-25`; its displayed 12-place enlargement is also outward.

## Exact duplication height bound

Write `x=a/b` in lowest terms with `b>0`. For a non-torsion point the usual
duplication formula specializes to

    x(2Q) = F/G,
    F = (a^2+25b^2)^2,
    G = 4ab(a^2-25b^2).

With `H=max(|a|,b)`, direct inequalities give

    H^4 <= max(|F|,|G|) <= 676 H^4.

Indeed `F>=a^4` and `F>=625b^4`, while `F<=(1+25)^2 H^4` and
`|G|<=4(1+25)H^4`. The cancellation factor `d=gcd(F,G)` divides
`2^2*5^4=2500`. Here is the all-input divisibility argument, also used by the
separate generator proof:

* A common prime other than 2 or 5 would force both `a^2+25b^2=0` and
  `a(a^2-25b^2)=0` modulo that prime, contrary to `gcd(a,b)=1`.
* At 2, opposite parities make `F` odd. If both are odd, their squares are
  1 modulo 8, so `a^2+25b^2=2 mod 8` and `v2(F)=2`.
* At 5, `5` not dividing `a` makes `F` a unit. If `v5(a)>=2`, then
  `v5(F)=4`. If `a=5c` with `c,b` both 5-adic units, the two factors
  `c^2+b^2` and `c^2-b^2` cannot both be divisible by 5. When the first is
  a unit, `v5(F)=4`; when it is not, the second is a unit and `v5(G)=3`.

Thus, for every such doubling,

    -log(2500) <= log H_x(2Q)-4 log H_x(Q) <= log(676).

Divide by `4^(j+1)` and sum the complete tail from `j=n` to infinity.
The geometric sum is `1/(3*4^n)`. This proves

    log H_x(2^n P)/4^n - log(2500)/(3*4^n)
        <= hhat(P) <=
    log H_x(2^n P)/4^n + log(676)/(3*4^n).

Eight exact integer doublings suffice. Each numerator and denominator is
reduced by its exact gcd, and the receipt saves that gcd and final exact
coordinates. No later point or local correction is assumed to vanish.

For completeness, the logarithm bounds do not use floating-point `log`.
For a positive integer `N`, set `k=bit_length(N)-1`, so
`log N=k log 2+log(N/2^k)`. The normalized argument is enclosed in `[1,2]`
on the same rational grid. For any `1<=r<=2`, put `z=(r-1)/(r+1)<=1/3`.
The positive expansion and its full tail obey

    log r = 2 sum_(j>=0) z^(2j+1)/(2j+1),
    0 <= remainder_after_m_terms
       <= 2 z^(2m+1) / ((2m+1)(1-z^2)).

The program uses `m=96`, monotonic endpoint evaluation, and outward rounding.
It applies these certified logarithms both to the finite height and the
constants in the tail. The readable height enclosure is widened outward to
six decimal places. The exact height need not be given by a closed elementary
expression for this certification to apply.

## Tamagawa factors from the actual local branches

The local index is `c_p=[E(Q_p):E_0(Q_p)]`. The branches used here are
Cremona's explicit Tate algorithm, §3.2, printed pp.66–67, steps 23–24 and
34–37. The following arithmetic specializes those branches, including the
residue-characteristic-two coordinate change.
[Cremona, Tate's algorithm](https://johncremona.github.io/book/fulltext/chapter3.pdf#page=5)

At 2, perform `T(1,0,0,1)`, meaning `x=X+1,y=Y`. The model becomes
`[0,3,0,-22,-24]`, with `a6=-24` and
`b8=4*3*(-24)-(-22)^2=-772`. Here `2|c4`, `4|a6`, and `8` does not divide
`b8`. This selects type III, giving `c2=2` and conductor exponent `6-1=5`.
In particular, it is not legitimate to apply the odd-prime I0* pattern at 2.

At 5, no translation is needed. The tests for II, III, and IV all fail:
`25|a6=0`, `125|b8=-625`, `125|b6=0`. The auxiliary cubic is
`T^3+(a2/5)T^2+(a4/25)T+a6/125=T^3-T`. Its three roots modulo 5 are
`0,1,4`, and the derivative `3T^2-1` is nonzero at each. This selects I0*,
with `c5=1+3=4` and conductor exponent `6-4=2`. The good primes contribute
`c_p=1`. Thus `product c_p=8`, independently consistent with conductor 800.

## Quotient and integer isolation

Multiply positive endpoints and reverse denominator endpoints on division.
The exact computation uses the raw intervals, then widens its display to six
decimal places. It proves

    0.999138 <= 16 L'(E,1)/(Omega*hhat(P)*8) <= 1.000782.

Every factor in the denominator is positive. Once primitivity and the full
BSD identity are supplied, the quotient is the positive integer `#Sha`, so
`#Sha=1`. An even coarser sufficient bound is independently explicit:
`Omega>2`, `hhat(P)>3/2`, and `product c_p=8`, whence `A>3/2`; therefore
`0<#Sha<1114529/750000<2`. No perfect-square or odd-primary shortcut is needed.

Three executed sensitivity controls retain the incorrect quotient intervals
obtained by using only one real component, using the half-height as regulator,
and treating `2P` as a primitive generator. Each excludes 1. These controls
show why the stated conventions matter; their output does not independently
establish the conventions or BSD.

Reproduce from this directory with:

```text
python -B work/bsd_factors.py
```

The script intentionally records the remaining theorem and primitivity ports
as dependencies of the Sha readout. Their completion is reported by this
continuation's separate generator and full-BSD theorem artifacts.
