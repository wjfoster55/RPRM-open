# Circular reference and offset-hook experiment12

The latest clarification makes the “69” resemblance a shape: two partial
closures with complementary openings, rather than literal digits 6 and 9.
Two complementary simple arcs on an oriented circle force exactly one
complete turn, provided they share the two marked seams and have no
extra turns or overlapping interiors. We also tested two operational
realizations. A complementary-gap relation survives
the new distance bounds and their rescaling. A two-leg operational loop can
have no closing state, one closing state, or many, depending on its maps.
The [shape explanation](TWO_HALVES.md) gives the formulas, examples and
the remaining connection to BSD. This interpretation remains a candidate.

Two parts of the proposal have precise finite realizations. The old
three-port code123 does give midpoint4. The framed words0012300 and01230
can also be represented by the short hook010, with an explicit decoder,
reference and frame metadata. More than one rule gives that target, so
the intended operation is not yet uniquely selected.

The new distance calculation supplies a limiting case: its bounds are now

\[
\boxed{2.034004870820\le d\le2.034007183803.}
\]

The former lower-tail123 does not persist in these new endpoint words.
It was a feature of one certified enclosure stage. A rule for changing
offset hooks remains possible, but has to specify that change. This
literal-word failure does not refute the user's clarified shape proposal.

## The exact123-to4 relation

Reuse the seven-state carrier
S={(A,delta): A>=0, delta>=1, 2A+3delta<=9}, with integer coordinates.
The direct code is c=(delta,2delta,A), the endpoints are(A,A+2delta),
and their midpoint is m=A+delta. Thus

```text
123 = (half-gap 1, full gap 2, left endpoint 3)
midpoint = 3+1 = 4.
```

This is the old coordinate rule. Ordinary digit addition123 gives6 and is
a different operation. Midpoint4 has just one code preimage in S, namely123.
Other midpoints have larger fibers:2 comes from121 or240;3 comes from122,
241 or360. The [decoder audit](agents/HOOK_DECODER.md) gives the full table.

## Two different exact ways to obtain010

First, retain only the half-gap and normalize each external zero frame to
one displayed zero:

```text
00 | 123 | 00 → 0 | 1 | 0 = 010,
 0 | 123 |  0 → 0 | 1 | 0 = 010.
```

The original frame counts remain in the packet. Without a reference,
the half-gap1 permits four codes:120,121,122,123. Given the separately
supplied endpoint A=3, reconstruction is c=(1,2,3). The selected pi-window
record can supply that reference. A different source supplying the same
typed A would work too; circularity or the constant pi is not required
by this finite reconstruction theorem.

There is a further limitation at this exact target: A=3 alone already
forces delta1 in S. The hook010 then checks consistency with a state
already fixed by the reference. It contributes no further distinction.
Across the whole carrier, reference plus half-gap determines every code.
We tested63 framed states, with each frame count from1 through3, and
recovered every original word exactly.

Second, use the old residual view(0,A−2delta). At123 this gives01.
Define a new overlap operation u⊙v by merging the longest equal suffix
of u and prefix of v. Then

\[
0\mathbin{\odot}01\mathbin{\odot}0=010.
\]

This is a different proposed composition, selected after the target was
given. On the complete seven-state carrier its signed outputs are all
distinct. Negative residuals retain their signs; they are structured
tokens such as0-20, not unsigned decimal numbers. Restricting to digit-only
outputs leaves the two codes122 and123, giving00 and010.

The two candidates agree at the user's example and separate at01220:

| Framed code | Keep half-gap | Residual plus overlap |
|---|---|---|
| 01230 | 010 | 010 |
| 01220 | 010 | 00 |

Both are now executable, and neither is selected as the user's uniquely
intended grammar. Their inverse requirements differ. Literal digit
permutations and reversal preserve length and therefore cannot by
themselves shrink a five- or seven-character word to010.

Greedy zero deletion is not used:01200 contains code120, whose final zero
is a code port. Fixed core width and external frame counts preserve it.

## The overlap at2.0340 is real, at a specified decimal frame

The previous ten-place lower bound was2.0340012300. Split it in either way:

```text
2.034  | 0012300
2.0340 |  012300
```

The anchor values are equal, but the widths differ. The first suffix
includes the zero already used by the second anchor. Likewise the old
upper bound splits as2.034|0104820 or2.0340|104820.

For a=2.034=2.0340, define r3=10³(d−a) and r4=10⁴(d−a). Exactly,

\[
\boxed{r_4=10r_3,\qquad d=a+10^{-3}r_3=a+10^{-4}r_4.}
\]

At the previous enclosure these normalized offsets were
r3 in[0.001230068,0.010481998] and
r4 in[0.01230068,0.10481998]. Moving the boundary changes the offset scale;
the original real quantity is retained by changing the scale with it.

We verified two complete compressed packets for the same old lower bound:

| Prefix | Visible hook | Endpoint reference | External zero counts |
|---|---|---|---|
| 2.034, width3 | 010 | A=3 | (2,2) |
| 2.0340, width4 | 010 | A=3 | (1,2) |

Each reconstructs2.0340012300 exactly with the declared decoder. This is
a concrete reference-and-offset interpretation of the proposed hook.
The short display010 alone does not reconstruct the bound, its scale,
or its enclosing interval.

“Prestige Pi” can provisionally name a reference record that retains the
pi source, decoder, scale and reopen route. This resembles the recovered
prestige description of keeping a relationship and a route into it.
It is a proposed use of that vocabulary, not a claim that2.0340 has
become equal to pi or that a new constant has been defined uniquely.

## The refinement test and its failed persistence candidate

Fresh rational point arithmetic recomputed depths9 and10. At twelve
decimal places, the intervals are

| Depth | Lower bound | Upper bound |
|---|---|---|
| 9 | 2.034001230068 | 2.034010481998 |
| 10 | 2.034004870820 | 2.034007183803 |

At ten places, the suffixes after2.034 changed from0012300/0104820 to
0048708/0071839. Neither new suffix contains123. The old initial010 upper
hook is also absent. The literal fixed-hook persistence candidate fails.
The new enclosure still certifies the original0340 prefix and now fixes
one additional fractional zero, giving03400.

These suffixes are values of the bound calculation, not two independent
tails of the unknown distance. A changing-hook theory could describe
enclosure refinement, but needs a transition rule that determines the
next state or retains the quantity relevant to BSD. Reinterpreting each
new bound after seeing it does not supply that rule.

## What a circular reference can lock

A circle with compatible relative offsets determines all positions up
to a common rotation. A marked reference can fix that remaining phase.
For arbitrary finite graphs of phase constraints, the
[circular-lock report](agents/CIRCULAR_LOCK.md) proves the complete
solution family: closed-walk offset sums must vanish modulo the circle
length, and the permitted root phases must intersect. ONE requires that
intersection to be a singleton in every connected component.

The report also proves a word-gluing law: compatible patches determine
the covered positions; every uncovered position remains free. This is
actual constraint solving around a loop. A loop may close modulo its
length while retaining a nonzero whole-turn count. Phase, traveled
distance and scale must be retained separately when they matter.

On the artificially wrapped finite pi word31415926535, forward35 occurs
at one position, but that3 is the inner occurrence at index9. The old
semantic endpoint A=3 is at index0. Reversing orientation and crossing
the seam gives the endpoint reading. Equal digits do not identify those
occurrences. No wrap of this finite window is asserted to describe the
continuation of pi's infinite expansion.

## The remaining BSD obligation

A reference-assisted decoder can expose and check a relationship. If the
reference itself is computed solely from a lossy digit key, attaching it
does not distinguish values already sharing that key. In the previous
experiment the pi-key fiber was[2.034,2.035), even after its word decoder
was uniquely selected.

To force the BSD multiplier, a proved relation must connect the circular
or offset state to the actual analytic coefficient and arithmetic height
regulator. A unique phase alone does not supply that equation. The
independent period identity Omega_c*AGM(sqrt68,sqrt34)=pi remains an
established example of such a correctly normalized geometric relation.
The central analytic-to-arithmetic coefficient comparison remains OPEN.

The results here are the exact finite hook models, their complete fibers,
reference/frame readback, a general finite phase/overlap theorem, and a
fresh arithmetic refinement that rejects fixed suffix persistence.
They do not establish a full pi digit law, total Sha or full BSD.

## Source, verification and replay

The [fresh evidence](evidence/hooks.json) contains the seven-state tables,
63 framed round-trips, exact offset coordinates, point-doubling ledgers,
and complete finite phase tables. The
[anchor readback](evidence/anchor-readback.json) retains the two complete
packets and exact rational reconstruction. An
[independent numeric review](agents/NUMERIC_REVIEW.md) checks the readouts.

The height kernel is an unchanged local snapshot of the previous proof-backed
rational interval implementation. Its universal tail theorem is attributed
earlier mathematics, not inferred from agreement between computed depths.
The old decoder source is also retained in dependencies. No saved PASS or
database rank was used to generate the new numerical bounds.

From this directory, Python3.10+ and the standard library suffice:

```powershell
python -I -B work/check_hooks.py --output evidence/my-hooks.json
python -I -B work/check_anchor_readback.py --input evidence/my-hooks.json --output evidence/my-readback.json
python -I -B work/check_two_halves.py --input evidence/my-hooks.json --output evidence/my-two-halves.json
```

Use new output paths. The depth-ten exact integer computation takes longer
than the finite decoder checks. The agent reports also contain short
standalone replays for their independent finite proofs. No other lane,
task, registry, source archive or paper was changed.

The [concise BSD rebrief](BSD_REBRIEF.md) separates the new results from
earlier proof dependencies. The packet includes source snapshots and their
original locators in [SOURCE_CAPTURE.json](SOURCE_CAPTURE.json).
