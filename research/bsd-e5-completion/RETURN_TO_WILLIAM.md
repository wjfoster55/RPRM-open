# E5 completion — the three arithmetic unknowns are settled

For **E/Q: y²=x³−25x**, the new continuation establishes:

- **P=(-4,6) is a primitive generator of the infinite part.** Every rational
  point is uniquely mP+T, with integer m and T one of O,(0,0),(5,0),(-5,0).
- **Sha is trivial.** Its total order is 1, and every odd-primary part is zero.
- **The full BSD leading-coefficient formula holds for this curve.** In the
  explicitly checked normalization it reduces to

\[
\boxed{L'(E,1)=\frac{\Omega(E)\,\widehat H_x(P)}2.}
\]

The global identity is established by an applicable published theorem. The
primitive-generator proof and certified factor calculations are new work here.
This distinction is explicit throughout the evidence: no database generator,
rank, regulator, analytic Sha entry, or rounded decimal equality is used.

## What “one generating step” means

The infinite part is a copy of the integers. Calling P primitive means that
P represents one step, rather than 3Q, 5Q, or some other multiple of a
smaller rational free step Q, allowing a torsion adjustment. The integer
coordinate m=0 is the zero free step and m=1 is the unit free step.
Those labels do not have to resemble the visible pair (-4,6).

The new proof excludes every possible proper odd index at once. If P had
such an index, a global height inequality would force a primitive generator
Q to have x=a/b in lowest terms with **max(|a|,b)≤20**. The checker exhausts
all **511** possible rational x-values and solves the ordinate question
exactly. The only points are torsion and ±P or ±(P+(5,0)). That contradicts
the proposed proper index. This is a complete bounded search because the
written argument proves the bound; it is not saturation up to a guessed
list of primes. See [GENERATOR_PROOF.md](GENERATOR_PROOF.md).

Your (-1,0) suggestion has a valid coordinate realization. Under
**X=x+3, Y=y−6**, the same generator becomes (-1,0), on

    Y²+12Y=X³−9X²+2X+12.

Under **X=x+4, Y=y−5**, it becomes (0,1), on

    Y²+10Y=X³−12X²+23X+11.

The equations and inverse operations move with the coordinates. Neither map
shrinks the generator to a fractional group step. The maps and their direct
group-law checks are in [COORDINATE_NOTE.md](COORDINATE_NOTE.md). Your stated
carry/swap trace and its exact downward inverse are also preserved there;
its full phase/sign rule and bridge to this curve remain unspecified.

## What Sha means, and what order one says

**Sha**, pronounced “shah” and often written Ш, is the Tate–Shafarevich
group. It records a particular kind of local-to-global obstruction: certain
covering equations attached to E can have solutions over the real numbers
and over every p-adic completion of Q, yet fail to have a rational solution.
Nontrivial Sha classes record those failures.

The “p-primary part” consists of elements killed by some power of the prime
p. “Odd-primary” refers to the primes 3,5,7 and so on. The previous
experiment eliminated the part associated with powers of two. The present
calculation eliminates all the remaining parts.

**Order one means the group contains only its identity: zero nontrivial
obstructions.** A trivial group has one element, not zero elements. This
conclusion concerns Sha attached to this particular E; it is not a universal
local-to-global theorem for every equation.

## Why the full formula is now established

[Creutz–Miller, Theorem 1.1](https://arxiv.org/pdf/1105.4018v2#page=2)
proves full BSD for every elliptic curve over Q with conductor below 5000
and analytic rank at most one. We read the actual theorem and checked its
conditions. E5 has conductor **800**, and the earlier independent analytic
proof establishes a simple central zero. No CM or exceptional-prime
condition removes E5 from this theorem's scope.

For rank one the theorem states

\[
L'(E,1)=\Omega\,\mathrm{Reg}\,\#\Sha\,
\frac{\prod_p c_p}{\#E(\mathbb Q)_{\rm tors}^{,2}}.
\]

The new computations give these factors, with exact rational endpoint
enclosures rather than assumed stable digits:

| Factor | Meaning | Certified value or interval |
|---|---|---|
| Ω | Integral of the absolute minimal differential over both real components | [2.345239572925, 2.345239572926] |
| Reg=Hhat_x(P) | Canonical-height size of the primitive free step, in the BSD convention | [1.899437, 1.899511] |
| c₂,c₅ | Local component indices at the two bad primes | 2, 4 |
| Other c_p | Local index at every good prime | 1 |
| Rational torsion order | The finite part of E(Q) | 4 |

The Tate-algorithm branches at 2 and 5 were checked separately. The period
enclosure bounds the entire arithmetic-geometric-mean limit. The height
enclosure uses eight exact doublings and a proved bound on every omitted
height correction. Its logarithms are enclosed by rational series. The
factor-of-two conventions for the real components and canonical height
were checked against the primary sources. See [BSD_FACTORS.md](BSD_FACTORS.md).

Substituting these certified intervals and the earlier derivative enclosure
shows that the BSD quotient lies between **0.999138 and 1.000782**. The
theorem identifies that quotient with the actual positive integer #Sha.
There is only one integer in that interval, so **#Sha=1 exactly**. This is
integer isolation after a theorem, not rounding a plausible decimal.

An even simpler exact check suffices: Ω>2, Reg>3/2, and the product of the
local indices is 8. Therefore

\[
0<\#\Sha<\frac{1114529}{750000}<2.
\]

With #Sha=1 and torsion order 4, the local/torsion multiplier is 8/16=1/2,
giving the boxed identity. It also yields the tighter, **BSD-derived**
enclosure 2.227317≤L′(E,1)≤2.227404. This last interval is a consequence
of the now-established formula; it is distinct from the independent
Euler-series certificate used to establish analytic rank one.

## What was checked and what remains separate

The supplied review was read and all 153 members were preserved. Its
152-entry inventory and the embedded prior return's inventory match.
The torsion corollary's finite-field counts were freshly recomputed. The
prior unchanged descent and analytic proofs were reused at their exact scope.
The new generator, factor, coordinate and integration checks all ran freshly
under the standard-library runner, with logs in `runs/final_validation/`.

The full-BSD theorem retains the grade **THEOREM_CITED**, including its
published computational proof. We did not replay the authors' whole
finite-conductor campaign or create a new proof of general BSD. The
specialization to E5 and the new finite certificates are supplied here.
[BSD_SHA_THEOREMS.md](BSD_SHA_THEOREMS.md) records the exact source conditions.

No arithmetic frontier named in the earlier E5 rebrief remains open for
this curve. The general carry/swap/phase law is a different, incompletely
specified representation question; its observed edges are retained without
forcing a universal rule. Other research lanes, old pilots, papers, and the
previous E5 delivery were not modified. This continuation stops here.
