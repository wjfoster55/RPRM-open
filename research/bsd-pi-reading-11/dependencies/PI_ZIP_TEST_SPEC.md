# Test specification

## Source

Recompute rational alternating-series bounds for
`pi = 16 atan(1/5) - 4 atan(1/239)`, verify the Gaussian-integer branch
identity, and require `floor(pi*10^12)=3141592653589`.

## Direct decoder carrier

Enumerate all decimal `A<B` and all three-digit codes.

```text
D0(A,B,c) =
  [c1, (A+B)/2, c1]
  [B,  A+B+c1, c2]
  [B+c1, B,     c3]

D1(A,B,c) =
  [c1, B-c1,    c1]
  [B,  2B-c1,   c2]
  [A+B-c2, B,   c3]
```

Admit only integer decimal outputs; `D0` additionally requires an integer
midpoint. Require record counts `4000` and `9600`. Extract code from the right
column `(M13,M23,M33)` only after full oracle equality. Exhaust both inverse
directions. Parse all three length-11 windows of the certified prefix and
require only window zero to close under either decoder. Require the target
fiber inside the frozen tag set `{D0,D1}` to have size two; leave unrestricted
decoder identity open.

Hash-verify the sealed parent archive and every member in its inner manifest,
then extract and normalize the pinned million-digit ingress in memory. Freeze
the complete `D0` and `D1` word sets before scanning all 999,991 overlapping
length-11 windows. Require sole hits at derivation position zero for `D0`,
`D1`, their intersection, and each seven-word endpoint-generated set; require
zero hits at held-out positions `1..999990`.

Independently count the progressive visual filters `M11=M13`, then
`M21=M32`, then the typed endpoint receipts, then the shared cross. Require
counts `99,946 -> 9,883 -> 1 -> 1`. Record uniform-IID expected counts only as
descriptive arithmetic; do not assign a discovery p-value to a post-target
rule.

## Hamming carrier

For `m=3,4`, use parity positions `1,2,4,...`, systematic data in the remaining
positions, and least-significant syndrome coordinate first. Exhaust all
`2^(2^m-1-m)` payloads.

Require:

- encode/extract round trip for every payload;
- minimum distances 3 and 4 before/after overall parity;
- every single-bit error located and corrected;
- every ordinary double error miscorrected by the one-error decoder;
- every extended double error detected but not claimed located;
- complete individual and joint syndrome fibers;
- complete LSB-first error-to-syndrome tables with unit-vector anchors;
- a dependent-row mutation loses position separation;
- triple errors expose single-error-promise failure;
- the exact weight-four undetected hostile count for extended Hamming-16.

## Pi lift

BCD-encode all eleven digits of `31415926535`, split the 44 bits into four
11-bit blocks, and extended-Hamming encode each to 16 bits. Require exact
forward/backward equality. Exhaust all 64 single flips and all 2,016 double
flips: same-block pairs must be detected; cross-block pairs must correct under
the per-block promise. Require named three- and four-error silent-wrong-output
hostiles. Reject invalid BCD and type aliases.

## Endpoint teacher adapter

Freeze the post-target endpoint generator

```text
delta=(B-A)/2
code=(delta,2*delta,A).
```

Enumerate the full decimal endpoint carrier under both decoder tags. Require
exactly seven admitted endpoint skeletons with delta fibers `4,2,1`. Verify
that `position=2^(3-delta)+A` is a two-way bijection to nonzero Hamming-7
syndromes, and that target `(3,5)` maps to position `7`. Keep decoder identity:
the tags agree on exactly one of the seven generated matrices.

Require the adapter-selection fibers `7!=5040`, shell-preserving `4!*2!=48`,
the full `GL(3,2)` gauge orbit of target syndrome `111`, decimal-base
specificity, zero-excluded count, and a target-fitting rival endpoint
generator with the same seven skeletons.

Require the shared residual
`T_(A,delta)(midpoint)-D0.M22 = D1.M31-D0.M31 = A-3*delta`, its singleton
zero fiber, and its dependency label.

Require exact row-intersection and oriented-zero receipts for the doubled
`1` ports and the two internal `B=5` ports.

## Reduction views and conditional abduction

On the seven endpoint-generated records, enumerate and invert all named views:

```text
direct code       (delta,2*delta,A)                    target 123
hybrid            (delta,A,A+3*delta)                  target 136
central column    (midpoint,midpoint+B,B)              target 495
middle row        (B,midpoint+B,2*delta)               target 592
D0 corner fold    (2*delta,A+3*delta,A)                target 263
D1 corner fold    (2*delta,2*A,A)                      target 263
endpoint core     (A,B)                                target 35
explicit gap      (A,2*delta,B)                        target 325
gap-anchor view   (2*delta,A)                          target 23
residual view     (0,A-2*delta)                        target 01
shell address     2^(3-delta)+A                        target 7.
```

Require each tagged chart to identify all seven records. Require `136`, `236`,
and `263` not to masquerade as straight matrix lines or direct code. Deleting
row `592` and column `495` must leave corners `1163`; summing the equal top
corners and retaining the lower edge left-to-right must give `263`. Require
`263` to reconstruct omitted ports `(M21,M12,M22,M32,M23)=5,4,9,5,2`.

The `D0/D1` tag-erased corner-fold union must have 13 values across 14 tagged
records, with the sole collision at target `263`. Require the seven endpoint
pairs to be exactly `02,04,06,13,15,24,35`. Prove that `35 -> 325` by
`gap=B-A` and `325 -> 35` by dropping the checked derived gap are exact inverse
renderings with the same seven semantic states. The longer glyph may expose
the relation `A+gap=B`, but it must be labeled as adding no semantic
information.

Require all scalar endpoint projections to be lossy. In particular, gap-only
`2` has target fiber `MANY(4)`, with complete gap fibers `4,2,1`. Record
`23`, normalized `01`, and ordered address `7` as other typed views, not
successive untyped identities. Address `7` requires a stipulated one-of-5,040
ordering; one binary bit cannot encode the seven-state carrier.

Attack the visible `325` relation. It admits 55 decimal triples when zero gap
is allowed, of which 48 lie outside the named seven; transposition `235`
passes the relation but exits the carrier. As a literal serialization, lawful
`325` detects every single-symbol substitution but cannot uniquely correct
one, and `224` is a valid two-symbol neighboring state. These coding facts do
not add mathematical content beyond `35`.

Require the exact common-mode endpoint ladder
`35 -> 24 -> 13 -> 02 -> (-1,1)`. Its first four words must be exactly the
decimal `delta=1` shell; the centered final word lies outside the decimal
carrier. Keep the separate bare-pair normalization `23 -> 12 -> 01` typed.

Finally require one explicit two-way finite zip:

```text
35 <-> 325 <-> (A,B,delta)=(3,5,1) <-> 123
   <-> 141/592/653 <-> 3|141592653|5
   <-> certified finite prefix 31415926535 <-> 35.
```

Test `53` as the port-reversal involution with signed gap `-2` and reverse
magnitude rendering `5-2=3`. Require full-word reversal
`31415926535 -> 53562951413`, matrix rotation
`141/592/653 -> 356/295/141`, and shadow code `123` from the left column read
bottom-to-top. Require the naive ordinary right-column code `651` to fail.
Exhaust all forward decoder records and require exact involutive reversal of
4,000 `D0` plus 9,600 `D1` tagged records and equal 13,570-word unions. Mark
the result derived, not independent. The current `A<B` decoder rejects untyped
`53`. Generate the `35/24/13/02` shell under
both tags and require only `35` to be both a tag crossing and a certified
source hit. Infinite pi generation, an independent `53` source/decoder, and
lower-shell "pi-equivalent" names remain `OPEN_NEW_CARRIER`.

Treat endpoint-only swap `O` and full reversal `R` as distinct lifts of `53`.
Require their target words `51415926533` and `53562951413`, operation fiber
`MANY(2)`, and the free eight-word `C2^3` orbit under `P,R,O`. Require 24
directed / 12 undirected generator edges and preserve the two-to-one
endpoint-forgetting projection to four inner matrices. Do not identify that
word cube with the separate 16-member `D4 x P` matrix orbit.

Build the seven-record receipt codebooks for `3553=ABBA`, `325523=AgBBgA`,
`345=AmB`, `375=ApB`, and the stacked `(A,g,m,p,B)` target `32475`. Exhaust
their distance and hostile fibers. Require distance four and exhaustive
one-to-three-symbol detection plus one-symbol correction for `32475`, while
retaining the selected-order cost of address `p` and leaving dimensional
interpretation open.

Invert the selected binary-shell address directly. Require the exact table
`1..7 -> 333/222/232/111/121/131/141`, binary form leading `1` plus
fixed-width `A`, power-of-two roots `1/2/4`, and target reconstruction
`7=111 -> delta=1,A=3,midpoint=4,row141,endpoint35`. Enumerate both
`p=gap+midpoint+1` and `p=gap+midpoint+delta`; each must agree exactly on
`02/13/24/35` and fail `04/06/15`. Require midpoint `4` to select `35` inside
that shell. Also require `midpoint+gap=D0.M31` on every record,
`D0.M31=D1.M31` only at `35`, and the target path
`4+2=6; 6+delta(1)=7`. Retain the selected-tree rule cost throughout.

Require tagged equalities `M11=M13=delta` and `M21=M32=B` on all seven records.
Attack the untyped shortcut: numeral `B` varies, some records have additional
palindromic lines, and some lower-row value intersections contain more than
the tagged `B` occurrence.

## Inverse, mirror, and circle

Complete the user-stated inverse examples to a decimal permutation only under
the explicit bijection-and-involution promise. Require the unique cycle form

```text
P=(0 5)(1 9)(2 8)(4 6), with fixed digits 3 and 7.
```

Require `141 -> 969`, `5 -> 0`, `9 -> 1`, `2 -> 8`, and `3 -> 3`, then
exhaust `P(P(d))=d` on all digits. Let `R` reverse word positions. Verify
`PR=RP`, all three nonidentity operations square to identity, and the exact
target orbit:

```text
I   31415926535
P   39690184030
R   53562951413
RP  03048109693.
```

Encode the word one-hot as a position-by-digit matrix. Require `P` to be a
digit-axis permutation matrix, `R` a position-axis permutation matrix, and
their two multiplication orders to agree literally. Record the Klein-four
carrier as one source plus three derived renderings, never four independent
observations. Require four view states, eight directed generator moves, four
undirected generator edges, and six total undirected pair relations.

Apply the same audit to the target `3x3` matrix. Require the four
`I/P/R180/R180P` words `141592653/969018403/356295141/304810969`; require the
eight D4 spatial presentations and their eight disjoint `P` images to make a
16-presentation orbit. Exhaust all 13,570 current decoder words and all 13
endpoint-generated words; require zero `P` images to land back in the same
respective carrier.

For a chosen source prefix `w` beginning at fixed entrance `3`, define its
left display as `R(P(w))` and join the two far labels. Require a labeled cycle
of `2|w|-1` vertices with `P`-reflection at every position. At the target,
require the 21-digit cycle word `030481096931415926535`, entrance `3`, and far
seam `0<->5`. Also require the first fixed-anchor lens
`3141592653 / 3969018403`, whose two endpoints are both `3`.

Apply the same construction to the pinned 1,000,001-digit ingress. Hash the
inverse, mirror-inverse, and 2,000,001-digit circle; apply both involutions back;
and check all 2,000,001 positions, distinguishing 1,000,000 nontrivial
reflection pairs from the one fixed center. Mark the transformed side `DEPENDENT`: it is
computed from the source and is not an independent pi witness.

Classify bounded-to-unbounded continuations separately. The integer endpoint
generator must remain an affine line in `Z^9`; the next `A=4` row exits the
decimal matrix at center `11`. Modulo 10 creates a ten-cycle only after adding
that quotient. The dyadic index rule `theta_n/pi=1-2^-n` uses zero-based
indices with the entrance at `n=0`; therefore the eleventh digit has `n=10`
and remaining half-arc `1/1024`. It compactifies two mirrored rays to a circle
only after adding the geometric schedule. None is
analytic continuation. Möbius topology requires a band plus twisted glue;
an infinity crossing requires a decision whether the crossing is identified;
a Lie/root-system adapter requires adjacency preservation.

Use this as the bounded/unbounded relation gate: name the bounded carrier,
name the continuation or compactification, prove their relation and return,
and retain rival continuations. This is a methodological description, not a
prescription or ontological claim.

## Boundary and uncube carrier

For `1/3/7 | {141}{592}{653} | ?/5/?`, solve the first-order integer affine
recurrence and require the conditional completion `2/5/11`, gaps `1/2/4`, and
the closed forms through level eight. Also retain at least two simple rival
families; without the rule tag the completion must remain `MANY`.

Bind the uncubed ports as `(c1,c2)->(A,B)`, retain `c3=A` as a distinct-port
equality check, and require the graph `(1,2,4)->(3,5,9)`. Enumerate the frozen
four-port `(c1,c2,A,B)` assignment permutations and modular-affine rivals.
Require the numerical `[7,4]` and staggered `(L_4,R_3)=[15,11]` parameter
alignments, and prove that the cross-level dimension identity has only the
`m=4` solution for integer `m>=2` using the explicit base and monotonic
increment receipt.

Exhaust the eight D4 matrix orientations. For each, extract the right-column
code and enumerate both decoders and every decimal endpoint pair. Require that
only the original orientation closes. Verify transpose words
`156/495/123`, row/column margins, total conservation, and one separately
named equal-row-sum hostile.

Hash-pin the user workbook and verify its extracted `Sheet1!A3:H5` geometry:
vertical boundary `1/3/7`, top-down columns `141/592/653`, transposed rows
`156/495/123`, and bottom close `1,2,3,4,5`. Treat its three open cells as
`MANY(1000)`. Under a constant vector step from `653`, require five decimal
completions; under the separately named local tail arithmetic continuation,
require the candidate columns `754,855` but do not call them forced.

## Claim ceiling

Finite properties only. `35` is minimum only among direct lossless endpoint
projections on the named carrier; no context-free compression theorem follows.
No decoder discovery, untagged boundary law, forced workbook tail, horizontal
uncube adapter, new pi digit, infinite-pi generator, intrinsic fourth
dimension, zeta-zero statement, or RH proof is tested.
