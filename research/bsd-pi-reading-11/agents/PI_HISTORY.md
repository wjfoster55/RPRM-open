# PI11 — historical pi closure and the `3|4` adapter

Date: 2026-09-12. This is a bounded recovery and a newly derived coordinate chart, not a registry promotion. Original repositories and prior lanes were read only. The parent task owns interval refinement, the endpoint-word experiments, and memory-fabric retrieval.

Later depth-9 evidence and the adopted actual-value digit extractor are reviewed in
`C:/github/RPRM-open/research/bsd-pi-reading-11/agents/READING_REVIEW.md`. That
review certifies the explicit composition from d to the finite pi word and
retains its complete real fiber; it refines the preliminary interval-adapter
status below without changing the recovered historical contracts.

The strongest recovered bridge is concrete: **read `3|4` as endpoint and midpoint `(A,m)=(3,4)`, recover `B=2m-A=5`, and the earlier finite codebook reconstructs `31415926535`.** The direct endpoint reading `(A,B)=(3,4)` is a different contract and fails the older integer-half-gap admission rule. That failure does not refute the endpoint–midpoint reading. Selection of the latter grammar from the E34 interval is still an open inference obligation.

## Source identities and evidence

Read current files:

- `C:/Users/bkbee/.codex/skills/rprm-math-lenses/SKILL.md`.
- `C:/github/RPRMLexicon/operational_numbers/README.md`.
- `C:/github/RPRMLexicon/operational_numbers/PI_CLOSURE_LEGEND_AUDIT.md`.
- `C:/github/RPRMLexicon/operational_numbers/translate_number.py`, especially lines 26–36, 137–233 and 267–286.
- `C:/github/RPRMLexicon/operational_numbers/SOURCE_MANIFEST.json`.
- `C:/github/RPRMLexicon/lexicon/RPRM_PI_CLOSURE_LEGEND.md`.
- `C:/github/PiDigitSymmetry/README.md`, `RESULTS.md`, and `FRONTIER.md`.

The primary finite decoder specification was read directly from
`C:/github/RPRMFoundry/evidence/sealed/RPRMPiViewfinder_SEALED_96f920a.zip`, entry
`experiments/PI_VIEWFINDER_TEACHER_ZIP_01/TEST_SPEC.md`, especially sections
“Direct decoder carrier”, “Endpoint teacher adapter”, “Reduction views and
conditional abduction”, and “Inverse, mirror, and circle”. The adjacent archived
README and `docs/PI_INVERSE_MIRROR_CIRCLE.md` were also read.

Fresh SHA-256 check: the ZIP is
`01109ae7e8e89fe2010e7c737085272a74ca0204d0ab28de276c8f396497c6c2`, matching
`SOURCE_MANIFEST.json`. The current legend is
`9ebdf2d739994e5d0e6679b62c6100d80e14e983103c8faf449ffadf182b07dc`, which differs
from the audit's pinned input `5b5fe3e1c8e577aac3d054aef0d31f106c82af8535b223b4442799664dc6f085`.
The current legend includes scope repairs; it cannot be described as identical
to that earlier audited input. A hash check establishes this byte relationship,
not the truth of either text.

Historical proof/check claims below are recovered from these sources. The old
full verifiers were not rerun in this subtask. The seven-row coordinate table
and D0 serialization below were freshly recomputed with Python using the exact
displayed formulas. No historical evidence grade was increased.

## Exact source window and digit maps

The source is the eleven-digit **word**

```text
W = 31415926535 = 3 | 141 | 592 | 653 | 5.
```

Its outer endpoints are `A=3, B=5`, gap `g=B-A=2`, half-gap `delta=1`, and
midpoint `m=4`. The row-major array is `141/592/653`. The viewfinder grouping
and decoder family are declared choices; a new word of length eleven is not
automatically another member of that finite source family.

On the decimal digit carrier `D={0,...,9}`:

| digit | P | N | T=P after N | M |
|---:|---:|---:|---:|---:|
| 0 | 5 | 0 | 5 | 9 |
| 1 | 9 | 9 | 1 | 8 |
| 2 | 8 | 8 | 2 | 7 |
| 3 | 3 | 7 | 7 | 6 |
| 4 | 6 | 6 | 4 | 5 |
| 5 | 0 | 5 | 0 | 4 |
| 6 | 4 | 4 | 6 | 3 |
| 7 | 7 | 3 | 3 | 2 |
| 8 | 2 | 2 | 8 | 1 |
| 9 | 1 | 1 | 9 | 0 |

Thus `P=(0 5)(1 9)(2 8)(4 6)`, `N(d)=-d mod 10`,
`T=(0 5)(3 7)`, and `M(d)=9-d`. Each map is its own inverse. `P,N,T` form
the three nonidentity members of a Klein four group. Their fixed sets are
`{3,7}`, `{0,5}`, and `{1,2,4,6,8,9}`, respectively, partitioning the ten
digits. `M` is the separate decimal nines-flip; it is not `P` or `N`.

Applied coordinatewise to W, the pinned shadows are:

```text
P(W) = 39690184030
N(W) = 79695184575
T(W) = 71410926070
M(W) = 68584073464.
```

Every displayed transform has a known inverse and is a dependent rendering
of W. The source legend's `4-pi=0.8584073464...` is a further, distinct
arithmetic-complement object. In particular, applying M to the whole word
does not produce `08584073464`: its first digit is 6. Nor may the real
complement's prefix be confused with subtracting the exact finite decimal
`3.1415926535` from 4, whose result ends in `...3465`. Truncation, a retained
infinite source, and positional subtraction require separate contracts.

## A fully specified `34 -> 35 -> W` zip

The older endpoint teacher family is exactly

```text
S = {(0,2),(0,4),(0,6),(1,3),(1,5),(2,4),(3,5)}.
```

Equivalently take integers `A>=0`, `delta>=1` with `2A+3delta<=9`, and put
`B=A+2delta`. Its shell sizes for `delta=1,2,3` are `4,2,1`.

Define the new chart `C(A,B)=(A,m)` where `m=(A+B)/2`. Its exact inverse on
the image is `C_inverse(A,m)=(A,2m-A)`. The image is exactly the seven pairs
shown below; there is no need to restrict the chart to `m-A=1`.

| `(A,m)` word | `(A,B)` word | delta | direct code | D0 word |
|---|---|---:|---|---|
| 01 | 02 | 1 | 120 | 01112323202 |
| 02 | 04 | 2 | 240 | 02224646404 |
| 03 | 06 | 3 | 360 | 03336969606 |
| 12 | 13 | 1 | 121 | 11213524313 |
| 13 | 15 | 2 | 241 | 12325847515 |
| 23 | 24 | 1 | 122 | 21314725424 |
| **34** | **35** | **1** | **123** | **31415926535** |

The restriction `delta=1` gives chart words `01,12,23,34`, corresponding to
endpoint words `02,13,24,35`. This is the ascending version of the earlier
`35 -> 24 -> 13 -> 02` subtract-11 shell. Width is retained, so `01` remains
a two-port word rather than being silently reduced to scalar 1.

The target chain and its inverse checks are:

1. `(A,m)=(3,4) <-> (A,B)=(3,5)` by `B=2m-A`, `m=(A+B)/2`.
2. `(A,B) <-> (A,g,B)=(3,2,5)` by `g=B-A`; inverse drops the gap only after
   checking `A+g=B` and membership in S.
3. `(A,B) <-> (A,B,delta)=(3,5,1)` by `delta=(B-A)/2`; inverse drops the
   checked derived coordinate.
4. `(A,B,delta) <-> c=(delta,2delta,A)=(1,2,3)`. Inverse reads
   `delta=c1`, `A=c3`, requires `c2=2c1`, then recovers `B=A+2delta` and checks
   the finite carrier.
5. D0 builds the matrix

   ```text
   [ delta,   A+delta,  delta ]
   [ A+2delta,2A+3delta,2delta]
   [ A+3delta,A+2delta,A     ].
   ```

   At the target this is `141/592/653`. Inverse reads the direct code from
   the right column and requires full matrix equality. Reading a convenient
   column alone without this equality check is not the historical decoder.
6. Serialize the external A, nine row-major matrix digits, and external B:
   `3|141592653|5`. The inverse parses those exact positions and checks the
   decoder. This is the fixed-width word W.

Every arrow above is reversible on its declared reached carrier. Therefore
`(A,m)=(3,4)` has **ONE(W)** as its complete D0-word output on this chart.
The chart is a newly derived synthesis of existing finite formulas, not a
claim that the old source already named bare `34` as pi.

The archived packet also keeps decoder tag D1. Under the endpoint generator,
D1 changes D0's bottom-left entry from `A+3delta` to `2A`; all other displayed
entries agree. Equality of the two whole matrices requires `A=3delta`, whose
only solution in S is `(A,delta)=(3,1)`. Consequently the target word is shared
by both tags. The target has two tagged decoder explanations `{D0,D1}`;
recovering its unique word does not choose one universal decoder law.

This zip reconstructs a configured, independently certified finite pi prefix.
It does not generate the rest of pi, predict an unseen digit, recover pi as
an analytic real from a context-free `34`, or make every D0 codeword a prefix
of a named constant. Its evidence is finite coding and a reversible chart.

## Direct `3|4` receipts, distinct from the midpoint chart

For a decimal ordered pair `A|B`, use `signed_gap=B-A` and
`centered_sum=A+B-9`:

| operation | word | signed gap | centered sum |
|---|---|---:|---:|
| I | 34 | +1 | -2 |
| pair reversal O | 43 | -1 | -2 |
| coordinatewise M | 65 | -1 | +2 |
| O after M | 56 | +1 | +2 |

The formulas are `M(g,s)=(-g,-s)`, `O(g,s)=(-g,s)`,
`(O after M)(g,s)=(g,-s)`. The pair `(g,s)` recovers the digits by
`A=(s+9-g)/2`, `B=(s+9+g)/2` when these are admitted decimal integers.
The gap `+1` alone has the complete nine-word fiber
`{01,12,23,34,45,56,67,78,89}`. Adding centered sum `-2` recovers ONE(34).

The older endpoint pair 35 instead has `(g,s)=(2,-1)` and midpoint 4. Direct
endpoints 34 have midpoint 3.5 and half-gap 0.5, so they are not in S. The
same visible word 34 can lawfully denote the chart `(A,m)` above, but that
requires the role assignment to be retained. Bare glyphs do not select it.

Coordinatewise `P(34)=36`, `N(34)=76`, `T(34)=74`, `M(34)=65` are exact
word maps. They do not establish that these outputs are all admitted
endpoint–midpoint chart states. In the old packet, P images of all 13,570
decoder words fail to land back in that same decoder union. A digit
involution on `D^11` is not thereby an automorphism of the decoder family.

## Interval and carry adapters worth testing

Only the displayed bounds `2.0339867006` and `2.0340237084` were supplied to
this subtask. Treat their provenance and numeric enclosure guarantees as
parent-task obligations. At the displayed precision they straddle `2.034`;
their common textual prefix is `2.03`, followed by lower digit 3 and upper
digit 4. A candidate extraction rule can produce the ordered pair `3|4`
from that **specific aligned position**, retaining lower/upper occurrence,
decimal scale, suffixes, and the original bounds. A bare extraction that
forgets those data has a large fiber and cannot recover the interval.

One testable two-stage hypothesis is:

```text
aligned boundary digits (lower 3, upper 4)
  -> interpret as (endpoint A, midpoint m)
  -> 35 -> the old finite W.
```

The first stage is a lexical/interval operation. The second stage is a role
adapter. Its latter algebra is exact; why this interval should select those
roles, this decimal width, and this scale remains OPEN. Shifting decimal
scale with the shift index retained is reversible. Removing the point,
dropping zeros, sorting, or selecting a substring each needs its own
retained-position contract. An eleven-digit bound word and W share a width;
that alone does not make their source constructions interchangeable.

Keep the carry candidates separate:

- Linear digit successor stops at 9. At 3 it sends 3 to 4 without carry.
- Cyclic successor on `Z/10Z` permits `9 -> 0`; exactly
  `N after M(d)=d+1 mod 10`, while `M after N(d)=d-1 mod 10`.
- Positional increment takes a digit plus carry-in, emits the remainder mod
  10 and a carry-out. It increments a word by propagation from the right.
  Applying cyclic successor to **every** digit is not positional word
  increment.
- A retained `(carry-row,digit)` lift distinguishes turns of a helix which
  the digit-only projection merges.
- A displayed seam such as `...2033999... -> ...2034000...` can reflect
  positional carry, but its scale and changed column must be named. Decimal
  refinements decide whether this is the actual selected seam.
- Real-limit equality `0.999...=1` uses a real evaluation map and nonunique
  expansion, distinct from finite modular wrap or discarded carry output.

These are live, specifiable candidates. Failure of a particular fixed digit
map should be recorded as REJECT for that explicit map. It cannot settle the
still underspecified family “pi zipped up by shifts/carry/swap”. Conversely,
an underspecified family does not yet supply a completed inverse fiber.

## What the old closure established and retained corrections

The earlier seven-record packet supplied an exact finite zip, two-way chart
checks, decoder fibers, finite source certification, shell/address relations,
and a declared mirror construction. The distinct word-action levels must be
kept in order: `P,R,O` give eight target words; adding N gives sixteen; the
later `FRONTIER.md` section 3 expands to five independent digit-pair swaps
and five mirror-position swaps, giving 1024 distinct target words. The last
bound is maximal only within its stated uniform digit-permutation and
position-permutation scope. These are transformations of one source.

For a word `w=d u`, the historical mirror ring is
`reverse(P(u)) · d · u`, of length `2|w|-1`. Its reflected P equality holds
away from the center by construction. At the center it is exactly `P(d)=d`.
Hence it closes if and only if the leading digit is 3 or 7. For W, the ring
is `030481096931415926535`, with a fixed central 3 and paired far seam 0/5.
This proves the named finite construction. It does not constrain the order
of the remaining source digits. A control word beginning in 3 with an
arbitrary tail also closes; changing the leading digit to a nonfixed digit
breaks closure. The exact theorem, rather than a provenance label, sets
this receiver boundary.

Corrections that must travel with reuse:

- The target's role-value 6 is the computed corner `2+4`; a literal 6 also
  occurs in the source window. “6 never occurs in the source” is false.
- The no-fourth-rung result is confined to the declared shell-ladder family
  with bound `alpha*A+beta*delta<=c`. It does not prohibit every possible
  carrier of 8. The paired-four/negative-half interpretation remains a
  reading awaiting its own operation and receiver.
- `P(W)`, `N(W)`, and `4-pi` are exact dependent shadows. Independent
  anti-pi remains OPEN, not refuted.
- `1234679` and the displayed arithmetic-complement support admit the audited
  T-fixed opposite-half relation; that is a finite support property and a
  candidate for held-out testing, not an independently observed anti-pi
  stream.
- The decoder's failure to propagate through later tested pi windows is
  bounded stream evidence. It rejects that fixed propagation claim; it
  does not establish that every possible digit grammar has failed.
- No finite periodic or mirror-ring closure here supplies a universal
  analytic identity for pi or a new digit-generating law.

The immediate usable conclusion is the complete finite chart
`34_(A,m) <-> 35_(A,B) <-> 31415926535_(D0 word)`. The outstanding seam is
an independently justified role-and-scale adapter from the E34 enclosure to
that chart. That seam is a bounded experimental target, not grounds for
discarding the candidate through an origin explanation.
