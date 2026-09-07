# Supplementary Fermat research: bounded proof and runnable reference

Documentation: CC0-1.0.

The supplementary [independent study](fermat-study.md#iii2-a-bounded-side-fermat-theorem)
contains the complete former chapter and its
[certificate appendix](fermat-study.md#certificate-appendix-iii2-the-auxiliary-prime-premises),
including all 302 auxiliary-prime premises. The book retains a short scope
and proof summary. This runnable reference preserves the bounded argument,
the fixed-gap interface and the direct replay route below.

The general relations below use a variable range H. The value 4000 belongs
to the completed bounded certificate, rather than to the definition of the
Fermat relation. A new range or representation must state which proof
obligations it inherits and which remain to be established.

**Theorem proved below.** If `a,b,c` are positive integers and `n>2` is an
integer, then

$$\min(a,b)\le4000\quad\Longrightarrow\quad a^n+b^n\ne c^n.$$

In words: the smaller of the two input bases a and b is at most four thousand.
The number 4000 bounds that smaller base, not its nth power. For example,
bases 17 and 1,000,000 fall within this statement for every integer exponent
above two. This bounded statement alone does not cover pairs where both
bases exceed 4000; the additional all-height results below cover some of them.

There is no separate assumed upper bound on `b`, `c`, or `n`. Those bounds
are derived from the smaller root. The argument also proves all-height
exclusions for exponents divisible by three or four, a first-case exclusion
for every odd prime through 1999, and a necessary root bound for every
exponent at least 100.

The independent unrestricted RPRM derivation remains **OPEN**. Its missing
step is an arithmetic exclusion or a descent for the remaining primitive prime cases
beyond the bounded theorem. Fermat's Last Theorem itself is established
mathematics; see [Wiles's paper](https://annals.math.princeton.edu/1995/141-3/p01).
That theorem is not used as a premise here. Importing its conclusion would
not complete this independent research goal. No novelty claim is made for
the classical ingredients.

The proof uses integer and rational arithmetic, prime factorization,
well-ordering, a justified Eisenstein-integer factorization, and a finite
table of auxiliary primes. [The checker](../checks/fermat.py) reconstructs
every residue in that table and verifies the stated finite arithmetic
premises. It is not a formal verification of the prose. The repository's
separate Lean proofs do not formalize this Fermat argument.

The supplementary study also proves [Theorem III.2.3, the fixed-gap decision](fermat-study.md#an-exact-decision-for-every-fixed-gap-aperture).
For supplied integer `n≥2` and positive integer gaps `s,d`, it decides the
complete positive-integer fiber of
`D(a)=a^n+(a+s)^n-(a+s+d)^n=0` inside the derived bracket
`0≤a≤2n(s+d)`. Strict increase of `D(a)/a^n` on positive real `a`, together
with the proved endpoint signs, excludes both integer tails after the final
adjacent bracket. The answer is NONE or ONE; `(n,s,d)=(2,1,1)` returns `a=3`.
The [fixed-gap tool](../rprm/fixed_gap.py) implements this per-aperture
decision, with a [registered independent check](../checks/fixed_gap.py)
and a [command-line example](../examples/fixed_gap.py). It does not assert
that every gap pair is empty or establish unrestricted FLT.

### Use the fixed-gap decision

From the repository root:

```sh
python -I -B examples/fixed_gap.py --n 2 --s 1 --d 1
python -I -B examples/fixed_gap.py --n 5 --s 2 --d 1
python -I -B checks/fixed_gap.py --output /absolute/path/to/checkout/.artifacts/fixed-gap-check.json
```

The checker requires an absolute `.json` destination. Within the repository
it writes only under `.artifacts`, accepts only a fresh path or the aggregate
runner's exact PENDING placeholder, and rejects every preexisting external
output before writing.

The example writes a new receipt under `.artifacts/fixed-gap/` by default;
`--output /path/to/new.json` selects a fresh path and rejects an existing
file. Its execution status is COMPLETE with a nested NONE or ONE fiber,
ERROR for a failed execution, or PENDING if interrupted before publication.
An incomplete run never reports an empty fiber. Each completed receipt binds
the executed module, admission helpers and example by SHA-256; those hashes
identify source bytes and do not prove their correctness.

For library use, `from rprm.fixed_gap import decide_fixed_gap` supplies
`decide_fixed_gap(n, s, d)`. Inputs must be exact Python integers with
`n>=2,s>0,d>0`; bool, floats, integer subclasses and coercions are rejected
with `AdmissionError`. The returned `fiber` is a tuple of all admitted `a`
values. For ONE, `source` reconstructs `(a,a+s,a+s+d,n)`. The receipt also
retains the derived bound, initial and final signed brackets, and every
midpoint evaluation. Zero is only a sentinel, not a positive source.
The square example returns `(3,)`; the fifth-power example returns `()`
with `D(11)=-5480` and `D(12)=27281`.

The bisection keeps `D(L)<0<=D(U)` and finishes at `U=L+1`, even if an
earlier midpoint is an exact root. It requires at most
`ceil(log2(2*n*(s+d)))` midpoint evaluations, plus two initial endpoint
evaluations. This counts exact power evaluations, not their bit complexity
or wall time. Python integers avoid rounding and fixed-width overflow,
but very large inputs can exhaust time, memory or integer-to-text limits.
The library propagates such failures; it has no mathematical height cutoff
or timeout that could be mistaken for a completed decision.

The focused check compares every integer in the derived brackets for
`n=2..8,s=1..6,d=1..6` using independent repeated multiplication, replays
all recorded bisection invariants, checks exact quadratic fibers with
large integers, and rejects malformed/domain inputs. It retains a case
where raw `D` decreases: only the normalized residual is asserted to be
strictly increasing. These are finite implementation checks of the written
general decision argument, not a formal proof of that argument or a test
of every gap pair. The fixed-gap suite is also requested by `verify.py`.

## The relation and the retained carrier

Keep the source tuple and its exact residual:

$$\mathcal R(a,b,c,n,r)\iff r=a^n+b^n-c^n.$$

The roots are positive integers; the exponent is an integer above two.
The question is whether the fiber `r=0` has a source. An invertible change of
coordinates must transport the operations, target predicate, and integer
image together. A lossy observation needs a proved condition sufficient to
decide that fiber. These requirements organize the proof; they do not imply
that a fiber is empty.

Divide a hypothetical solution by its common gcd. Primitivity implies
pairwise coprimality: a prime dividing two roots divides the third. The
smaller-root cap survives division. Equal roots would make `c/a` a rational
nth root of two. A reduced rational number with integral nth power has
denominator one, and no integer nth power is two for `n>=2`. Thus relabel
so that `a<b<c`, and put `d=c-b>=1`.

If `e` divides `n`, the powered roots `a^(n/e), b^(n/e), c^(n/e)` would give
a solution at exponent `e`. Every `n>2` has an odd prime divisor or is
divisible by four. This reduction changes the roots. In the bounded proof
we retain the original root cap and apply valuations to those original
roots, including when the intermediate carrier consists of their squares.

## Shell bounds, with coverage

The difference-of-powers identity gives

$$a^n=d\sum_{j=0}^{n-1}c^j b^{n-1-j}>nd\,b^{n-1}.$$

Since `b>a` and `n>=3`, it follows that

$$nd<a,\qquad 3db^2<a^3.$$

We also need the stronger uniform statement `a>=2n`. For fixed `a,n`, the
smallest shell occurs at `b=a+1,d=1`. Set `m=2n-1`. Expanding around the
midpoint `2n+1/2`, the linear term and the positive cubic term give

$$(2n+1)^n-(2n)^n>n(2n+\tfrac12)^{n-1}.$$

The first three binomial terms have the exact excess

$$1+\frac{3(n-1)}{2m}+\frac{9(n-1)(n-2)}{8m^2}-\frac mn
=\frac{(n-1)(n+4)(n-2)}{8nm^2}>0.$$

Consequently the minimal shell at `a=m` exceeds `m^n`. Moreover

$$\frac{(a+2)^n-(a+1)^n}{a^n}
=\sum_{k=1}^{n}\binom nk\frac{2^k-1}{a^k}$$

strictly decreases with positive `a`. The contradiction therefore holds
for every `a<=2n-1`. This proves `a>=2n`. The strict excess vanishes at the
excluded boundary `n=2`; the square equality `(3,4,5)` is retained.

For any positive integer cap `H`, these inequalities give complete finite
coverage:

$$3\le n\le\lfloor a/2\rfloor,\quad
1\le d\le\lfloor(a-1)/n\rfloor,\quad
a<b\le\left\lfloor\sqrt{\left\lfloor\frac{a^3-1}{3d}\right\rfloor}\right\rfloor,
\quad c=b+d,\quad a\le H.$$

This justifies bounded exhaustive verification. The proof for `H=4000`
will instead eliminate most of that carrier symbolically.

### Variable ranges and representation changes

Let C_H contain the primitive ordered integer candidates satisfying the
displayed necessary bounds, with c=b+d and a<=H. Each C_H is finite and
C_H is contained in C_(H+1). Every hypothetical positive integer solution
reduces to a candidate in some C_H. The general construction uses H as an
input; no special change in the equation occurs at 4000 or 4001.

The zero-exclusion certificate below is established at H=4000. Its auxiliary
prime coverage, seam ceilings and surviving fifth/tenth-power branch lists
depend on that range. Substituting a larger H into the general bounds does
not establish those certificate premises for the larger range. A uniform
proof must exclude the zero fiber for every H, or supply another argument
covering every remaining candidate, such as a proved descent.

A change of representation can remove large displayed coordinates while
preserving the precise problem. On jointly primitive triples a<b<c, retain
the exponent n and set x=a/c, y=b/c as exact rational numbers. The image is
the rational triangle 0<x<y<1. Let L be the least common multiple of the
reduced denominators of x and y. The inverse is

$$a=Lx,\qquad b=Ly,\qquad c=L.$$

For a source triple, this least common denominator is
c/gcd(a,b,c)=c. Conversely, minimality of L makes the reconstructed triple
jointly primitive. Thus the chart is bijective on the stated carrier.
Requiring pairwise coprimality adds that condition to its rational image;
general nonprimitive triples additionally need their common scale retained.

The equation becomes x^n+y^n=1, and the source range becomes Lx<=H.
The normalized residual is (a^n+b^n-c^n)/L^n, so zero is preserved exactly.
Across the unrestricted chart, the coordinates stay below one while their
denominators remain unbounded.
For example, primitive triples (a,a+1,a+2) map to denominators L=a+2.
A rounded picture or a fixed denominator grid therefore cannot replace this
exact rational carrier. This chart supplies a lawful change of representation;
a contradiction valid for its entire admitted image is a further obligation.

## A separate bound for every exponent at least 100

Every hypothetical solution with `n>=100` satisfies `a>81n/40`.
Let `kappa=81/40`, assume `a<=kappa*n`, and put `r=(a+1)/(a+2)`. Then

$$r^{-n}\ge 1+\frac n{\kappa n+1}
+\frac{n(n-1)}{2(\kappa n+1)^2}
+\frac{n(n-1)(n-2)}{6(\kappa n+1)^3}.$$

Each factor `(n-j)/(kappa*n+1)`, `j=0,1,2`, increases with `n`: its forward
difference has positive numerator `1+kappa*j`. Thus the lower bound is
at least its exact value at 100,

$$\frac{9991013}{6129013}>\frac{13}{8}.$$

Therefore `r^n<8/13`. Since `a/(a+2)<r^2`,

$$\frac{a^n+(a+1)^n-(a+2)^n}{(a+2)^n}
<r^{2n}+r^n-1<-\frac1{169}.$$

All larger shells also exclude equality. One rational certificate and the
proved monotonicity cover the unbounded exponent range; sampling later
exponents is unnecessary.

## Quartic descent

We prove the stronger statement that no positive integers satisfy
`x^4+y^4=z^2`. Choose a solution with least `z`. Dividing by a common gcd
of `x,y` would decrease `z`, so they are coprime. They cannot both be odd
modulo four. Relabel `x` odd and `y` even.

For a primitive triangle `A^2+B^2=C^2` with `A` odd and `B` even, the
positive integers `(C+A)/2` and `(C-A)/2` are coprime and their product is
`(B/2)^2`. Unique factorization makes them individually squares. Hence

$$A=m^2-n^2,\quad B=2mn,\quad C=m^2+n^2,$$

where `m>n>0` are coprime and of opposite parity. Apply this to
`(x^2,y^2,z)`. If `m` were even, `x^2=m^2-n^2` would be three modulo four.
Thus `m` is odd and `n` even. From `(y/2)^2=m(n/2)` and coprimality,
write `m=u^2,n=2v^2`. This yields

$$x^2+(2v^2)^2=(u^2)^2.$$

This triangle is primitive: a prime dividing `x` and `n` would divide
`m`. Parametrize it again to obtain
`x=r^2-s^2, v^2=rs, u^2=r^2+s^2`, with coprime positive `r>s`.
Thus `r=R^2,s=S^2`, and

$$R^4+S^4=u^2,\qquad 0<u\le u^2=m<m^2+n^2=z.$$

This contradicts the minimal choice of `z`. Substituting `z=c^2` excludes
fourth powers, and exponent inheritance excludes every multiple of four.

## Cubic descent and its lifted carrier

Assume a primitive nonzero signed solution `x^3+y^3+z^3=0`, chosen with
least height `max(|x|,|y|,|z|)`. A prime dividing two coordinates divides
the third, so they are pairwise coprime. Cubes modulo nine are `0,1,-1`;
exactly one coordinate is divisible by three. Name it `z`. Then `3` does
not divide `xy`, and `3` divides `x+y`.

Use the ring `Z[omega]`, where `omega^2+omega+1=0`, and the norm

$$N(m+n\omega)=m^2-mn+n^2.$$

It is multiplicative, is a nonnegative integer, and vanishes only at zero.
Its norm-one elements are precisely the six units `±1, ±omega, ±omega^2`.
For a quotient in `Q(omega)`, round its two rational coordinates. The
errors `e,f` are in `[-1/2,1/2]`, so `e^2-ef+f^2<=3/4<1`. Multiplication
back gives a remainder of smaller norm. Thus Euclidean division gives
gcds and Bezout identities; irreducibles are prime, and induction on the
norm gives unique factorization up to order and units.

Put `lambda=1-omega`. Then `N(lambda)=3` and `lambda^2=-3*omega`.
Reduction of `m+n*omega` to `m+n` modulo three has kernel `(lambda)`.
Consequently `lambda` is prime,

$$\lambda\mid(m+n\omega)\iff3\mid(m+n),\qquad
v_\lambda(t)=2v_3(t)\quad(t\in\mathbb Z\setminus\{0\}).$$

The integer `x^2-xy+y^2=(x+y)^2-3xy` has three-adic valuation one.
Factoring `x^3+y^3=-z^3` gives
`v_3(x+y)+1=3v_3(z)`, hence `9` divides `x+y`.

In the factorization

$$(x+y)(x+y\omega)(x+y\omega^2)=-z^3,$$

two factors share no prime except `lambda`. Their differences are unit
multiples of `y*lambda`, so a different common prime would divide `x,y`,
contrary to their integer Bezout identity. Also
`x+y*omega=(x+y)-y*lambda` has lambda-valuation exactly one. All other
prime exponents in this factor are multiples of three. Thus

$$x+y\omega=\varepsilon\lambda\gamma^3,\qquad
\gamma=m+n\omega,\quad\lambda\nmid\gamma.$$

Write

$$\gamma^3=A+B\omega,\quad
A=m^3-3mn^2+n^3,\quad B=3mn(m-n).$$

Then `lambda*gamma^3=(A+B)+(2B-A)*omega`. Multiplication by the units
`±1, ±omega, ±omega^2` gives coefficient sums respectively
`±3B, ±3(A-B), ∓3A`. Since `A` is nonzero modulo three and `B` is zero
modulo three, `9|(x+y)` forces `epsilon=±1`. Therefore
`x+y=±9mn(m-n)`. Taking norms and using the original equation gives

$$mn(m-n)=\pm\left(\frac z{3N(\gamma)}\right)^3.$$

The rational cube is an integer, so its root is an integer. A common
rational prime dividing `m,n` would divide both coefficients `x,y`
through `gamma^3`. Hence `m,n,m-n` are pairwise coprime and nonzero.
Prime valuations make each a signed cube: `m=r^3,n=s^3,m-n=t^3`.
The new primitive nonzero signed triple satisfies `r^3-s^3-t^3=0`, and

$$\max(|r|,|s|,|t|)\le|rst|=\frac{|z|}{3N(\gamma)}
<|z|\le\max(|x|,|y|,|z|).$$

Here `N(gamma)` is a positive integer. The strict decrease contradicts
minimality. This excludes cubes and every multiple of three. This ring's
factorization property has been proved only for the ring used here; it is
not assumed for rings associated with higher prime exponents.

## Auxiliary primes: the precise first-case theorem

Let `p` be an odd prime, `q` a different prime, and `R` the full group of
nonzero pth powers modulo `q`. Suppose

$$R\cap(1-R)=\varnothing,\qquad p\bmod q\notin R.$$

Then there is no primitive nonzero integer solution `x^p+y^p=z^p` with
`p` not dividing `xyz`. This is the **first case**, with no root bound.

For coprime integers `X,Y`, the sum quotient is congruent to
`p*Y^(p-1)` modulo `X+Y`. No prime other than `p` can divide both factors;
the same holds for a difference factorization. In the first case,
`t^p=t (mod p)` makes each of `x+y,z-x,z-y` nonzero modulo `p`.
The factorizations are therefore into coprime integers, and prime
valuations give signed pth powers

$$x+y=A^p,\quad z-x=B^p,\quad z-y=C^p,\quad
\frac{x^p+y^p}{x+y}=D^p.$$

The denominators are nonzero on a nonzero solution. If `q` divided no
coordinate, dividing the equation by `z^p` would give two members of `R`
summing to one. Hence it divides a coordinate, uniquely by pairwise
coprimality. Permute the signed equation `x^p+y^p+(-z)^p=0` so that
`q|z`. Since `p` is odd, `-1=(-1)^p` belongs to `R`; signed renaming is
valid. The identities `z-x=B^p,z-y=C^p` now imply `x,y` belong to `R`
modulo `q`, including their minus signs.

If `x+y` were nonzero modulo `q`, it too would belong to `R`, and division
by it would again violate the first condition. Thus `x+y=0 (mod q)`.
The quotient identity becomes `D^p=p*x^(p-1) (mod q)`. The right side is
nonzero because `q!=p` and `q` does not divide `x`. Dividing by the member
`x^(p-1)` of `R` forces `p` into `R`, a contradiction.

The checker contains **302 explicit `(p,q)` pairs**, one for every odd
prime `3<=p<=1999`. It verifies primality, `q=2kp+1`, and both conditions
by constructing `{a^p mod q: 1<=a<q}` from all `q-1` nonzero residues.
This is 4,052,680 source powers and 3,936 distinct residues summed over
the moduli; the largest `q` is 185849. Missing or duplicate exponents
fail the complete census. The data establish the lemma's premises for
this finite prime range. They do not supply auxiliary primes for every
odd prime, and do not by themselves exclude the second case `p|xyz`.

The [square-frontier prime mechanism](../experimental/primes/square-frontier.md)
shows how a complete certified prime list can support successive larger
regions by a uniform factor theorem. It can supply the primality premises
for p and q. The two full residue-image conditions above, their coverage
over the required exponents, and the second-case exclusion remain separate
obligations. Extending a prime-classification region establishes that
classification property; its use here must retain the Fermat target.

## Valuations and the original root cap

For odd prime `p`, distinct integers `X,Y` with `p` not dividing `XY` and
`p|(X-Y)`, and positive integer `m`,

$$v_p(X^m-Y^m)=v_p(X-Y)+v_p(m).$$

For an exponent `k` coprime to `p`, the quotient modulo `p` is
`k*Y^(k-1)`, so its valuation is zero. For exponent `p`, expand
`(Y+h)^p-Y^p` with `p|h`. The first term has valuation `v_p(h)+1` and
every later term has greater valuation, including `h^p` since `p>=3`.
Write `m=p^e*k` and iterate. For odd `m`, replacing `Y` with `-Y` gives
the sum version.

Let `m` be odd and let `p` be its least prime divisor. Then
`gcd(m,p-1)=1`, since every prime factor of `p-1` is smaller than `p`.
Thus mth powering is injective on the nonzero residues modulo `p`:
choose an inverse of `m` modulo `p-1`, and use `t^(p-1)=1`.
The latter congruence follows by multiplying the nonzero residues after
their permutation by `t`.

If `X^m+Y^m=Z^m` is primitive and `p` divides one coordinate,
injectivity forces the matching seam `Z-Y`, `Z-X`, or `X+Y` to be
divisible by `p`. Its exact valuation is

$$v_p(\text{seam})=m\,v_p(\text{divisible coordinate})-v_p(m).$$

For odd original exponent `n`, use `m=n` and roots `(a,b,c)`. For
`n=2m` with odd `m`, use `(a^2,b^2,c^2)`. The latter seams are quadratic,
and their valuation is `n` times the valuation of the original divisible
root, minus `v_p(m)`. The original bound `a<=4000` remains attached to
`a`, not to the powered root used in exponent reduction.

Discard multiples of three or four. Every remaining `n>=5` satisfies

$$5db^4<a^5,\qquad n\le2000,\quad b<22000,\quad d<800,
\quad c<22800.$$

For example `4000^5<5*22000^4` proves the bound on `b`. Linear seams
are below 26000 and quadratic seams below
`22800^2+22000^2<1100000000`. Put `m=n` if `n` is odd and `m=n/2`
otherwise. Its least prime divisor `p>=5` is at most 1999. Reduction to
exponent `p` and the auxiliary lemma force `p` to divide an original
root, because taking positive powers does not change divisibility.

The valuation floors now exceed the relevant ceilings:

| Exponent branch | Seam floor | Seam ceiling |
|---|---:|---:|
| Odd prime `n=p>=7` | `p^(p-1)>=7^6=117649` | 26000 |
| Odd composite `n>=25` | `5^20` | 26000 |
| `n=2p`, prime `p>=7` | `p^(2p-1)>=7^13` | 1100000000 |
| `n=2m`, odd composite `m>=25` | `5^45` | 1100000000 |

For the composite rows, if `e=v_p(m)`, then
`e<=p^(e-1)<=m/p<=m/5`. This gives the displayed exponents. Therefore
only `n=5` and `n=10` remain. The checker also classifies every integer
`n=3..2000` individually and verifies its exact valuation comparison.

## Fifth powers: every branch at the cap 4000

For a primitive difference or odd-power sum, the seam and its companion
quotient share no prime other than `p`. If `p` divides the seam, the
valuation rule makes the companion's p-valuation exactly one. Every
other prime in the seam must then have valuation a multiple of `p`.

At `n=5`, first suppose `5|a`. The gap has the form `d=625*t^5`.
Since `d<800`, it must be 625. But at the upper cap the minimal shell
already has positive excess

$$4626^5-4001^5-4000^5=69217768803909375>0.$$

The ratio `[(a+626)^5-(a+1)^5]/a^5` decreases with `a`: expand it as a
sum of positive coefficients times negative powers of `a`. Thus this
excludes every smaller `a` as well.

Now `5` does not divide `a`, so the gap and companion are coprime and
`d=t^5<800`. Hence `d` is exactly one of `1,32,243`. The auxiliary lemma
forces `5|b` or `5|c`. The corresponding seam `c-a` or `a+b` is
`625*u^5<26000`, hence is exactly one of `625,20000`.

For `5|b`, write `c-a=L` and define

$$E_{d,L}(a)=a^5+(a+L-d)^5-(a+L)^5.$$

The shell ratio `[(a+L)^5-(a+L-d)^5]/a^5` strictly decreases, because
`L>d` and its inverse-power coefficients are positive. It can equal one
at most once. For `L=20000`, its value already exceeds one at `a=4000`
and the smallest gap `d=1`:

$$24000^5-23999^5-4000^5=634741765759880001>0.$$

Increasing `d` only increases that shell. This removes every difference
branch with `L=20000`.

For `5|c`, write `a+b=L` and define

$$F_{d,L}(a)=a^5+(L-a)^5-(L-a+d)^5.$$

This is strictly increasing on `0<a<L`: `a^5` increases while the
subtracted shell decreases. When `L=625`, order gives `a<=312` and
`5d<a` excludes `d=243`. The remaining exact checks are:

| Branch | Consecutive integer inputs | Residuals |
|---|---|---|
| `E(1,625)` | 335, 336 | -18753691826; 26900909375 |
| `E(32,625)` | 1028, 1029 | -1142821221024; 1641632904757 |
| `E(243,625)` | 2523, 2524 | -35451102937500; 32297263771651 |
| `F(1,625)` | 181, 182 | -926025000; 6250588651 |
| `F(32,625)` | 296, 297 | -4201942176; 60664215625 |
| `F(1,20000)` | 3296, 3297 | -329671369090625; 353993777122976 |

The unique crossings lie strictly between integers. The other two
increasing branches are still negative at the cap:

$$F_{32,20000}(4000)=-9503787009999634432,$$
$$F_{243,20000}(4000)=-81057900031960689443.$$

Thus no branch has an integer zero. Independently of these monotonicity
arguments, the checker directly evaluates every admitted integer input
in all derived branches: 32,319 inputs across 11 branches, including the
three large difference branches already excluded by the shell bound.

## Tenth powers: complete factor fibers

At `n=10`, the shell gives `d<400,b<8000`, using
`4000^10<10*8000^9`. Thus `c+b<16400` and

$$c^2-b^2=d(c+b)<6560000.$$

Factor `c^10-b^10` as a difference of fifth powers of the coprime squares
`c^2,b^2`. If `5|a`, the seam and companion share only five, with
companion valuation one. Therefore `c^2-b^2=5^9*u^10`. The upper bound
forces `u=1`. The gap is odd, so `b,c` have opposite parity, and
`c-b,c+b` are coprime. Their product is the prime power `5^9`. Therefore
`c-b=1,c+b=5^9=1953125`, violating `c+b<16400`.

If `5` does not divide `a`, the factors are coprime, so

$$(c-b)(c+b)=t^{10}.$$

If `b,c` have opposite parity, the factors are odd, coprime tenth
powers. The larger is greater than one, hence at least
`3^10=59049>16400`. If both roots are odd, put
`u=(c-b)/2<200,v=(c+b)/2<8200`. They are coprime and of opposite
parity, with `4uv=t^10`. The odd factor is a tenth power. The even
factor is `256` times a tenth power, since its two-adic valuation is
eight modulo ten.

The bound on `u` prevents it from being even; as an odd tenth power
below 200 it is one. Thus `v=256*w^10`; `v<8200` forces `w=1`.
The only factor candidate is `(b,c)=(255,257)`. Here `5|b`, so the
other quadratic seam must satisfy `c^2-a^2>=5^9`. But
`c^2=257^2=66049<5^9`, a contradiction. The checker independently
enumerates all positive divisor pairs for every allowed tenth-power
gap, yielding exactly this one ordinary candidate and no candidate in
the branch `5|a`.

Primitive normalization, every exponent, and both parity branches have
now been covered. This completes the theorem for `min(a,b)<=4000`.

## What transport earns, and what remains open

For fixed roots, retain `s=a+b` and `q=a^2+b^2`. Then `t=(s^2-q)/2=ab`
and the power sums satisfy

$$S_0=2,\quad S_1=s,\quad S_{j+2}=sS_{j+1}-tS_j.$$

Each root satisfies `X^2-sX+t=0`, which proves the recurrence at every
depth. The source image is explicit: `2q-s^2=h^2` must be a
nonnegative square, `s,h` must have the same parity, and both
`(s-h)/2,(s+h)/2` must be positive. The sorted pair is then unique;
the ordered fiber has two elements if the roots differ. One depth
alone is insufficient: `(1,7)` and `(5,5)` have square sum 50 and
different cube sums 344 and 250.

Determination of `S_n` does not exclude `S_n-c^n=0`. Likewise, if a
complete state changes by an invertible linear map `J`, its target
covector changes by the inverse: `ell'=ell*J^-1`. Then
`ell'(Jv)=ell(v)` for every admitted source. Testing one component
while leaving the target or other components behind is a different
question. A negative isolated component is not a contradiction to
the retained whole relation.

Several failed implications have exact controls. The shell residual
at `(5,6,7;3)` is -2 and at `(6,7,8;3)` is 47, so its sign does not
propagate upward in root size. Three summands already give
`3^3+4^3+5^3=6^3`; changing summand count changes the target. The
near equality `6^3+8^3-9^3=-1` retains its nonzero residual under a
faithful transport. These controls refute those particular shortcuts.

After exponent reduction, the remaining hypothetical counterexample
can be primitive with odd prime exponent `p>=5`, ordered positive
roots, and smaller root above 4000. For `p<=1999`, a root must be
divisible by `p`; larger prime exponents require additional premises
for either case. One sufficient completion lemma would construct,
from every such solution, another primitive positive solution of
the same exponent with strictly smaller smaller root. It must prove
integer landing, preservation of the equation, and strict decrease.
Well-ordering would then finish the argument. Such a construction
has not been supplied here.

Homogeneity `D_n(ka,kb,kc)=k^n*D_n(a,b,c)` does not supply that descent:
division by two lands in integers only when all roots are even.
New primitive triples in the next band remain an obligation.
Similarly, a sum of squares of residual and transport errors is
nonnegative, but on a consistent source it reduces to
`(a^n+b^n-c^n)^2`. Proving it strictly positive is the outstanding
zero-exclusion problem. A [proof-donut audit](proof-donut.md) can
check supplied finite carriers and preservation rules; it cannot
certify this missing universal statement by referring to its own
success label.

## Replay and evidence scope

From the repository, run the following with an absolute output path
appropriate to the checkout:

```text
python -I -B checks/fermat.py --output /absolute/path/to/checkout/.artifacts/fermat.json
```

See [verification](verification.md) for the repository replay boundary.
The command uses only bundled integer pairs and the Python standard
library. It writes PENDING before checking and PASS or FAIL at completion.
The receipt separates finite certificate checks from the written
mathematical proof. The contracts remain active under Python `-O`.

| Evidence | Scope |
|---|---|
| Written shell, descent, valuation and monotonicity proofs | Their explicitly quantified carriers and premises |
| 302 full residue-image certificates | Auxiliary-prime lemma for odd primes through 1999 |
| 1,998 exponent classifications | Complete finite exponent range derived from `a<=4000` |
| Fifth-branch and tenth-factor enumeration | Complete finite carriers derived in the written proof |
| Hostile controls | Rejection of specified malformed certificates and failed implications |
| Unrestricted same-target RPRM descent | OPEN |

For primary comparison formalizations of the classical ingredients,
see Mathlib's [exponent three](https://leanprover-community.github.io/mathlib4_docs/Mathlib/NumberTheory/FLT/Three.html),
[exponent four](https://leanprover-community.github.io/mathlib4_docs/Mathlib/NumberTheory/FLT/Four.html),
and [basic exponent reductions](https://leanprover-community.github.io/mathlib4_docs/Mathlib/NumberTheory/FLT/Basic.html).
Those external proofs are comparison references, not a formal check of
the text or finite checker in this repository.
