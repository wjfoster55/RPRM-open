# Exact equality, remainders, and levels of readout

This note answers the user's new suggestion that a decimal can be real
while reading as zero at a coarser number level. The useful interpretation
is an observation at a chosen resolution. We retain exact equality as a
separate question. No claim about physical existence is inferred.

## The latest input and the admitted construction

William explicitly offered tentative intuition:

> when we're measuring under one ... 0. something is the same as 0 ...
> it's a different level of number hierarchy ... the decimals 0.1 to 0.9
> represent the space in between 0 and 1 ... it's real, but it's still 0.

The full message is conversational evidence, not a theorem premise.
The following is an analyst-defined precise version, restricted initially
to nonnegative rational numbers. It is consistent with reading a fraction
as zero **whole units**, and does not assign exact numerical equality
between that fraction and zero.

At level k≥0, set D=10^k and retain

    n = floor(Dx),       r = Dx−n,       0≤r<1.

The pair (n,r) recovers x exactly through x=(n+r)/D. The integer n
counts completed units at that scale; r is the remainder measured in
those units. The whole-unit observation alone has the complete fiber

    {x≥0 rational : floor(Dx)=n}
      = [n/D,(n+1)/D) intersect Q,      n≥0.

Thus x=0.6 has state (0,0.6) at k=0 and (6,0) at k=1. Its whole-unit
readout is zero at the first level, and its exact value is retained.
The fiber is MANY; it is not ONE(0). If the receiver only asks for
whole-unit count, its readout is settled. If the receiver asks whether
x=0, that question is not constant on the fiber.

This is ordinary positional arithmetic and a specified observation map.
The existing local [zero/rail account](../../recovered-concepts/ZERO-AND-RAILS.md)
also distinguishes source value, chart coordinate and retained winding;
that historical account does not supply this new readout contract or a
BSD identity automatically.

## Addition needs the retained carry

For two states (n,r), (m,s) at the same scale, let c=floor(r+s). Since
0≤r,s<1, c is 0 or 1. Exact addition transports to

    (n,r) + (m,s) = (n+m+c, r+s−c).

The new remainder lies in [0,1), and decoding gives the sum of the
decoded inputs. This proves closure and the transport identity for all
admitted states. Both terms are used; the coarse count alone cannot
support this update. For example,

    0.6 + 0.6 = 1.2  → one whole unit, remainder 0.2,
    0.2 + 0.2 = 0.4  → zero whole units, remainder 0.4.

Both pairs supply coarse inputs (0,0), but their coarse sums differ.
This is a complete distinguishing case against treating floor as an
additive map. Replacing each input by its coarse zero erases information
that determines the next carry.

Negative values need a stated convention. For −0.6, ordinary floor
returns −1, whereas truncation toward zero returns 0. The user's new
message does not choose between those extensions. We therefore keep
the proved construction nonnegative and retain that signed extension
as OPEN_SPECIFICATION. For a signed discrepancy we may observe its
nonnegative magnitude without silently choosing either convention.

## When finer levels really would prove zero

**Fixed-value lemma.** If one fixed nonnegative real x satisfies
floor(10^k x)=0 for every integer k≥0, then x=0.

**Proof.** Each such observation gives 0≤x<10^(−k). If x>0, the
Archimedean property gives an integer k with 10^k x≥1, a contradiction.
The converse is immediate. Applied to |x|, the statement also detects
zero of a signed real value.

The quantifiers matter. For any fixed finite depth K, the nonzero value
x=10^(−K−1) has zero whole-unit observations at all levels 0 through K.
It first reads as one unit at level K+1. The finite checks cannot be
promoted to the all-level premise. Changing the underlying x while
refining also does not establish an assertion about one fixed source.

For our actual normalized discrepancy d=Q_E−1, the certified interval
gives |d|<10^(−4). Thus the whole-unit observation of |d| is zero
through level 4. It does not establish the all-level premise. The bound
is about the exact same curve and normalization throughout.

The sufficient telescoping certificate in `EXPLICIT_IDENTITY_TARGET.md`
provides another way to supply an all-stage argument: prove the exact
matching rule and a boundary estimate tending to zero. A constant
boundary remainder 1/2 has coarse readout zero but does not tend to zero.
Discarding it would invalidate the proposed equality.

## A finite equality certificate if arithmetic supplies discreteness

Define the actual real quotient

    Q_E = [L''(E,1)/2] / [Ω_E Reg_E].

The fresh replay again proves it lies in

    [0.999920542, 1.000092816].

This interval has width. Its endpoints are rational; that does not
prove its unknown member Q_E is rational.

**Conditional denominator lemma.** Suppose, independently, Q_E=a/b
in lowest terms with 1≤b≤10000. Then Q_E=1.

**Proof.** If a≠b, the nonzero integer a−b has absolute value at
least 1, so |Q_E−1|≥1/b≥1/10000. The displayed interval is strictly
within distance 1/10000 of 1, a contradiction.

This is an elementary rational-separation argument. It requires a bound
on the actual quotient's denominator, not a chosen number of display
digits. The numbers with denominator at most 10000 do not form an
evenly spaced decimal grid; only their minimum possible distance from
the integer 1 is used here.

Using the exact raw intervals, the largest denominator bound for which
this particular interval isolates 1 is **10774**. The next denominator
already admits the different rational **10776/10775** inside the
interval. The simpler bound 10000 is therefore sufficient and has a
margin. The source checks every denominator through 10000 and proves
the sharper endpoint cutoff using exact integer ceilings.

Rationality alone does not suffice: 1+10^(−12) is a noninteger rational
inside the interval. These are controls on a proposed inference about
real numbers, not claims that these alternatives are realized by E34
or counterexamples to BSD.

The actual bounded-rationality premise remains NOT_ESTABLISHED. The
theorem review in `EXACT_IDENTITY_THEOREMS.md` identifies no applicable
proved theorem supplying it here. Even if this gate established Q_E=1,
the arithmetic group Sha would still need its own proof of order 1 to
conclude the full formula. Conversely, a direct proof of Sha=0 would
leave this real equality to establish.

## A direct use of finer readout in the odd-prime attempt

The trace T in `ODD_PRIME_ATTEMPT.md` uses a different, precisely
specified hierarchy: residues modulo 25 and modulo 125. The admitted
theorem supplies divisibility by 25, so the complete fiber of its
modulo-125 residue over coarse residue zero is

    {0,25,50,75,100}.

The four nonzero residues certify that T has exactly two factors of 5.
Through the proved theorem reduction, any of those outcomes would
establish Sha[5^∞]=0. Residue zero would leave this sufficient criterion
inconclusive; it would not prove Sha has a nonzero element.

Here 25 and 125 both read as zero modulo 25, while their residues modulo
125 differ. Unlike floor, reduction modulo 25 is compatible with
addition. The exact valuation question still distinguishes members of
its fiber. The actual T has not been computed; we do not select a
favorable fine residue from the five available candidates. This gives
the hierarchy idea a concrete question to answer without assigning a
new meaning to the ordinary decimal examples.

## Evidence and next mathematical obligation

`work/identity_gate.py` reconstructs the quotient from freshly executed
analytic, full-basis height and period evidence. It binds source and
receipt bytes and retains the written theorem dependencies. It then
checks 10000 denominator cases, the first rational counterexample
beyond the admissible bound, 1764 exact addition cases over four
levels, hidden remainders through ten finite depths, and all five lifts
of coarse trace residue zero modulo 125. These finite
controls accompany the general written proofs above; they do not
prove their own unbounded hypotheses or the BSD identity.

The next mathematical contribution could be an exact law showing that
the actual quotient belongs to the required discrete set, or a correct
all-stage identity forcing the retained discrepancy to zero. A change
of readout by itself supplies neither premise. We have kept the user's
level distinction useful by making the remainder recoverable and by
showing exactly which future carry depends on it.
