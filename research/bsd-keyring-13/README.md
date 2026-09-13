# Three component loops and a shared connector

The user clarified a **three-plus-one keyring**: one loop for `2.`, one
for `0340`, one for the paired numerical tails, and a fourth loop threading
all three. This changes the candidate geometry from the previous two-arc
model. The paired tails remain one joint record on the third loop.

We constructed that arrangement, proved its linking properties, and
tested an exact positional readback and carry operation for the labels.
The geometry is a precise candidate representation. No rule deriving it
from the BSD constants, or using it to prove their comparison, is asserted.

## The geometric model

The connector is a horizontal radius-3 circle. Three radius-3/4 circles
stand in vertical radial planes, centered at three equally spaced points
on the connector. These are convenient construction parameters, not
values inferred from the user's digits or the elliptic curve.

Each small circle links the connector once. The small circles have
pairwise disjoint containing balls, so they form an unlink when the
connector is removed. The four wires never intersect: every point of a
small circle is exactly distance 3/4 from the connector. Their linking
graph is a star with three leaves, while the wires themselves remain
four separate components. This distinction is what a physical keyring
illustrates.

The [independent geometric proof](agents/KEYRING_AUDIT.md) gives exact
formulas, separation bounds, signs and hostile controls. Its linking
calculation uses the signed spanning-surface intersection theorem in
[Licata's lecture notes, Theorem 3](https://www.math.ias.edu/files/wam/LicataLecture3.pdf).
The interactive drawing is illustrative; the proof does not depend on
pixels or sampled intersections.

The visible line is treated as part of the proposed closed connector.
Closing that line outside the displayed window is a modeling choice.
A linearly ordered number carrier does not become cyclic without an
explicit cut and wrap convention.

## An exact operation for the connector

A concrete candidate is that the fourth loop retains the shared decimal
frame, block roles and transfer rule. Let I be the integer block, P the
integer represented by the w-digit middle word, and T a tail of m digits.
The readback is

\[
\boxed{V(I,P,T;w,m)=I+\frac{P}{10^w}+\frac{T}{10^{w+m}}.}
\]

For canonical blocks, admit I in {0,...,9}, 0<=P<10^w and 0<=T<10^m,
with positive fixed widths. Equality of values differs from equality of
the retained words. Multiplying V by 10^(w+m) and applying Euclidean
division recovers I, P and T uniquely, with zero padding to the supplied
widths. This proves the inverse on that finite grid. Forgetting the
widths would lose leading-zero occurrences and the requested grouping.

For the requested interval, retain a **joint** tail pair Tlo<=Thi with
shared I,P,w,m. Apply V to each endpoint. The existing twelve-place
distance enclosures read back as follows:

| Existing input stage | Integer | Middle | Joint tails, each width 8 |
|---|---|---|---|
| Depth 9 | 2. | 0340 | (01230068, 10481998) |
| Depth 10 | 2. | 0340 | (04870820, 07183803) |

For example, the depth-10 record reconstructs exactly

\[
[2.034004870820,\;2.034007183803].
\]

These are attributed inputs from experiment 12, whose source and height
tail proof remain there. This experiment freshly evaluates and inverts
the block records; it does not claim another fresh height refinement.

## Carry is a real transfer between these blocks

For an explicitly extended tail with one possible overflow, write

\[
T=q10^m+T',\quad P+q=k10^w+P'.
\]

Then the exact invariant is

\[
V(I,P,T;w,m)=V(I+k,P',T';w,m).
\]

Retaining q and k also recovers the original block state. Without those
tags, canonical normalization can merge different original records. We
tested all 200 source inputs I=2, P in {0,...,9}, T in {0,...,19}, w=m=1;
every value and tagged inverse was preserved. These inputs normalize to
110 distinct values; their carry tags retain the original occurrences.
This is a complete finite
one-carry carrier, with normalized I in {2,3}.

At the actual widths, tail 100000000 promotes middle 0340 to 0341 and
leaves tail 00000000. If middle 9999 also overflows, I=2 becomes 3.
These are synthetic boundary controls, not observed carries in the
current height interval.

There is a significant **joint boundary case**. An interval can straddle
a carry boundary:

```text
2.0340 | 99999999
2.0341 | 00000000
```

The two endpoints then require different normalized middle words. A
single shared canonical `0340` block is insufficient. Retain separate
endpoint prefixes or a wider signed/extended offset relative to a common
frame; declare the changed carrier before continuing. Of the complete
2,100 source interval records with I=2, P=0..9, 0<=a<=b<20, exactly
1,000 straddle that boundary and 1,100 retain a shared prefix. Those
records represent 1,605 distinct normalized numerical intervals; a
different initial frame can encode the same interval. The
[joint-seam evidence](evidence/joint-seam.json) preserves this case.

Thus there is an actual value-preserving operation available for the
connector. Assigning that operation to the fourth hoop is the proposed
interpretation; the geometry alone does not force it.

## What the keyring shape leaves open

With I=2, P=0340 and two-digit tails 0<=a<=b<100, there are exactly 5,050
distinct interval records. Every one can decorate this same four-hoop
construction. We enumerated them all and verified each positional inverse.
The bare shape has MANY(5,050) preimages on this declared carrier. The
fully labelled and framed record has an exact readback. No complete
classification of all possible RPRM loop interpretations is claimed.

These tails enclose one arithmetic height distance. They are not already
the analytic and arithmetic sides of BSD. For the previously fixed curve,
the outstanding real comparison still concerns L''(E,1)/2, the real
period, the full-height regulator, and the separately justified order of
Sha. The new keyring model changes none of those earlier proof statuses.

The next substantive obligation is to specify how a change in one loop
acts on the others, with a readout equation connecting the actual BSD
quantities. Internal agreement of positional representations is exact;
the analytic-to-arithmetic comparison remains OPEN. A circular drawing
does not supply that equation, nor does its presence alone single out pi
as the numerical reference required by the BSD problem.

## Replay and evidence

From this directory, Python 3.10+ and the standard library suffice:

```powershell
python -I -B work/check_keyring.py --output evidence/my-keyring.json
python -I -B work/check_joint_seam.py --output evidence/my-joint-seam.json
```

Use new output paths. The [fresh block evidence](evidence/keyring.json)
binds the source and attributed input bytes. The [visual check](evidence/visual-check.json)
records desktop/mobile rendering and an actual rotation change; it is
visual verification, not a topology proof. The browser check uses Node
and Playwright, with CODEX_NODE_MODULES optionally pointing to the module
directory. The [independent block review](agents/BLOCK_REVIEW.md) separates
source-record counts from distinct normalized values.
[BSD_REBRIEF.md](BSD_REBRIEF.md) gives the concise status.

Only this new experiment and its task-owned visualization were written.
Older BSD packets and other active research lanes were left untouched.
