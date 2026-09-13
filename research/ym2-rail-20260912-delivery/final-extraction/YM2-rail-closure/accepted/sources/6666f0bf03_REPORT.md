# Audit84 report: the middle is the aligned intersection of three lossies

## Result

Audit84 passes its frozen candidate.

For

```text
Q_L = floor(10 * 10^L / 1001),
1001 = 7 * 11 * 13,
O = 10^(10^100),
L = 10^O,
D11 = 10^(10^50)+1,
D13 = 10^(10^40)+3,
```

the twenty-four-digit block beginning `O` places from the left is

```text
900099900099900099900099.
```

The computation does not materialize `O`, either delta, `L`, the quotient
integer, or the skipped prefix.  It retains three modular observations and two
finite action receipts, aligns the observations, reconstructs live remainder
`901 mod 1001`, and emits the requested block.

## What “the two lossies make the middle” means exactly

The ordinary arithmetic phrase “the lossies add up” is not the operation in
this carrier.  Each lossy view selects a fiber—a set of still-possible live
states.  Combining views intersects those fibers.

Here the component and pair fibers are:

| Retained view | Maximum candidates | Unresolved pairs |
|---|---:|---:|
| mod 7 | 143 | 71,071 |
| shifted mod 11 | 91 | 45,045 |
| shifted mod 13 | 77 | 38,038 |
| mod 7 + shifted mod 11 | 13 | 6,006 |
| mod 7 + shifted mod 13 | 11 | 5,005 |
| shifted mod 11 + shifted mod 13 | 7 | 3,003 |
| all three, correctly aligned | 1 | 0 |

So none of the views contains the center, and no pair contains enough to
identify it.  The center appears only as the unique member of the aligned
three-way intersection.  Keeping the views separate also makes the
retraction explicit: re-encode `901` into each factor port and reapply each
frame action.

This realizes the proposed abductive zipper without guessing an unfinished
middle.  In each possible viewing order the candidate set shrinks until the
last independent view makes it `ONE`:

```text
1001 -> 143 -> 13 -> 1
1001 -> 143 -> 11 -> 1
1001 -> 91  -> 13 -> 1
1001 -> 91  -> 7  -> 1
1001 -> 77  -> 11 -> 1
1001 -> 77  -> 7  -> 1
```

The partial fibers are the useful “negative space.”  They say exactly how far
the current aperture is from identifying the requested center.

## Operator match: carrier, action, and inverse

The two future observations are both `1`, and both relative shift actions are
written `10`.  A numeral-only comparison would say that the operators match.
They do not match as typed operations:

```text
10 mod 11 has inverse 10,
10 mod 13 has inverse 4.
```

The port modulus is therefore part of the operator receipt.  Aligning the
future observations gives

```text
1 * 10 mod 11 = 10,
1 * 4  mod 13 = 4.
```

Together with `5 mod 7`, CRT lands at `901 mod 1001`.

The raw address deltas are deliberately forgotten.  For these receivers only
their finite actions matter.  The mod-eleven action group has two states; the
mod-thirteen action group has six.  Forgetting their actions produces this
aperture lattice for the fixed observation `(5,1,1)`:

| Known shifted actions | Possible past remainders |
|---|---:|
| both | 1 |
| mod 11 only | 6 |
| mod 13 only | 2 |
| neither | 12 |

The `12` is the product aperture `2*6`, not an additive action period.  Even
with both actions known, their raw deltas remain `MANY` outside the action
receiver.

## Big-number significance

This is an actual non-bottom-up interior Peek for a structured huge-number
family.  The requested position is not traversed digit by digit.  The address
is compiled through modular action classes, the live state stays inside
`0..1000`, and only the requested twenty-four digits are emitted.

That does not make every big number equally accessible.  The shortcut exists
because the quotient word has a finite long-division state law and `10` is a
unit modulo `1001`.  An arbitrary explicit integer, an arbitrary irrational,
or an untyped “Prestige” label supplies no such transition law by itself.

The length boundary is also proved rather than inferred from the spelling.
Both deltas are below `O`, so the latest requested frame is below `2O`; the
declared length `10^O` contains that frame and its width.  A small or
incomparable compact expression is rejected.

## Controls and boundaries

The package and independent cold verifier agree on:

- four package tests;
- all 1,001 live remainders;
- every one-, two-, and three-probe bundle in the frozen library;
- all six factor-view orders;
- all four known/unknown action apertures;
- 192,192 bounded modular joins;
- 32,032 literal quotient-window comparisons;
- rejection of nonunit and undersized carriers;
- direct exact next-digit and previous-digit descent on the admitted probes.

The inherited full Moore-closure helper deliberately stops at 256 states, so
Audit84 does not raise that global cap.  It exhausts static fibers over all
1,001 states and checks the two declared transitions directly.  This boundary
is a tooling scope, not missing evidence for the static result.

The operational-number translator independently reports the exact
factorization `7*11*13`, digit sum `2`, and no scout proposal for decimal word
`1001`.  Only the factorization is load-bearing.  The spelling and digit sum
select no carrier and assign no intrinsic meaning.

The fixed witness has source support one.  Its repeating block is
deterministic.  The result establishes no entropy, randomness, secrecy,
one-wayness, compression ratio, measured speedup, hardness result, P=NP
result, or physical dimensional interpretation.

## Next seam

This carrier reconstructs the full live remainder because the requested
twenty-four-digit block is injective on all 1,001 states.  The next useful
experiment is a coarser target receiver whose minimum sufficient bundle
identifies exactly the requested output but deliberately does not recover the
full live state.  That will test “the most informative lossy information” as a
target-relative aperture rather than another full-state CRT reconstruction.
