# RPRM pi three-level 3-4-5 matrix 01

Status: **BOUNDED FINITE RECEIPT PASS**

This packet seals the smallest useful version of the current pi experiment.
It does not attempt to prove or compute all one million digits.  It keeps five
claims separate:

1. an exact rational Machin interval certifies `3.141592653589`;
2. three literal occurrence fibers are measured on one hash-pinned ingress;
3. every certified finite decimal cell has a forward and upper-anchor reading;
4. the addressed window `3|141|592|653|5` supports one explicitly declared
   3-by-3 arithmetic receiver and contextual zipper; and
5. `0|1` and `1|0` are the two orientations of one finite binary seam, with a
   reset tagged separately in `Option(Bit)`.

The result is a proof about these typed finite carriers.  It is not a pi digit
generator or a claim that the same reading is intrinsic to every occurrence of
the digits.

## 1. Three levels and their inverse

On the normalized one-million source carrier, with the leading `3` at position
zero:

```text
141        -> 1006 occurrences -> MANY(1006)
141592     ->    2 occurrences -> MANY(2)
141592653  ->    1 occurrence  -> ONE
```

The two six-digit contexts are

```text
3|141592|6       at position 1
7|141592|2       at position 821582
```

and the unique nine-digit context is

```text
3|141592653|5    at position 1.
```

Forward appending of the frozen groups `592` and `653` narrows the fiber.  The
inverse removes a group: forgetting `653` reopens the label-only address to two
candidates; forgetting `592` reopens it to 1,006.  If the absolute address is
retained, this reopening does not occur.  Label-only and addressed inverse are
therefore different typed operations.

The ingress is the file published at
[angio.net](https://www.angio.net/pi/digits/pi1000000.txt).  Its raw and
normalized hashes are frozen in the verifier.  The packet independently proves
only the short prefix; later substring results are exact membership claims on
the pinned ingress, not an independent proof that every ingress digit is pi.

## 2. Bottom-down is the other side of one finite cell

There is no final digit of pi.  The lawful opposite endpoint exists at each
finite decimal resolution.  Let

```text
p_n = floor(10^n (pi-3))
q_n = 10^n-1-p_n.
```

Then the same half-open cell is

```text
[3+p_n/10^n, 3+(p_n+1)/10^n)
  = [4-(q_n+1)/10^n, 4-q_n/10^n).
```

The reflection `J_n(k)=10^n-1-k` exchanges the two rails and squares to the
identity.  At layer two this is

```text
[3.14,3.15) = [4-.86,4-.85),   p=14, q=85.
```

At a finite cyclic layer, `99...9` precedes `00...0`; the number of nines grows
with the resolution.  A literal `90|314...` is therefore at most a declared
protocol word, not hidden terminal digits of pi.

The verifier proves these cells at layers `0..12` from exact rational Machin
bounds.  It first checks the exact Gaussian-integer certificate
`(5+i)^4(239-i)=114244(1+i)` and its positive principal branch.  Refinement
appends the certified digit to `p` and its decimal shadow to `q`.  Without a
certified next digit, ten refinements are possible: `MANY`.

## 3. The final 3-by-3 window

Arrange the three groups row-major between the addressed flanks:

```text
        [ 1 4 1 ]
3   |  [ 5 9 2 ]  |   5
        [ 6 5 3 ]
```

The interior contains `{1,2,3,4,5,6,9}`.  It omits `{0,7,8}`.  Under the
declared receiver that reserves `0` for the external finite-wrap boundary, the
payload complement is `{7,8}`.

The endpoints have

```text
delta    = 5-3 = 2
midpoint = (3+5)/2 = 4
sum      = 3+5 = 8.
```

The derived sum `8` is not stored in the interior.  This is a frozen hard rule
of this receiver: a literal payload `8` is not allowed to masquerade as the
endpoint-derived check value.

The contextual abduction receiver returns the decimal digits strictly between
the endpoints.  Thus `between(3,5)={4}` is `ONE`; `between(3,4)` is `NONE`;
and `between(3,6)={4,5}` is `MANY`.  The statement

```text
3|141592653|5 -> 4
```

is about that receiver.  The integer `141592653` is not numerically equal to
four.

## 4. Contextual zipper

The right column supplies the three-digit code

```text
c=(1,2,3).
```

For ordered decimal endpoints `A<B`, define

```text
D_(A,B)(c1,c2,c3) =
  [ c1    (A+B)/2    c1 ]
  [ B     A+B+c1     c2 ]
  [ B+c1  B           c3 ].
```

The map is partial: the midpoint must be integral and every output must remain
a decimal digit.  In the baseline context,

```text
D_(3,5)(1,2,3) = [141;592;653].
```

The encoder extracts the right column only after checking that all six derived
cells match this decoder.  On its admitted image, encode and decode are exact
inverses.  The verifier exhausts 4,000 admitted images over every endpoint pair
and every three-digit code.

Receiver context is load-bearing:

```text
(3,5,123)                  -> ONE matrix
123 with endpoints erased  -> MANY(10) matrices
```

For code `123`, the derived-sum-absent rule leaves three endpoint contexts:
`(2,4)`, `(2,6)`, and `(3,5)`.  Crossing with the complete decimal-closure
grammar leaves only `(3,5)`.

The zipper reduces a nine-digit matrix payload to a three-digit code only when
the endpoints and decoder are retained.  A storage claim must charge that
context and decoder; one hand-built instance does not receive free compression.

## 5. The 3-4-5 decimal closure matrix

For unordered pairs with repetition from `{3,4,5}`, retain absolute difference
and sum:

| pair | difference | sum |
|---|---:|---:|
| `3,3` | 0 | 6 |
| `3,4` | 1 | 7 |
| `3,5` | 2 | 8 |
| `4,4` | 0 | 8 |
| `4,5` | 1 | 9 |
| `5,5` | 0 | 10 |

Therefore

```text
difference rail = 0,1,2
seed rail       = 3,4,5
in-digit sums   = 6,7,8,9
full sum rail   = 6,7,8,9,10
decimal carry   = 10 (outside the one-digit carrier).
```

### The binary seam reduction

Read `0|1` and `1|0` as symbol words, not as the decimal numbers one and ten.
They are the two orientations of the same unordered seam `{0,1}`.  Reflection
and coordinatewise bit complement both exchange them, and reflection twice is
the identity:

```text
forward convention   0|1
reflect/complement   1|0
reflect again        0|1.
```

With orientation retained, each word is `ONE`.  Erasing orientation produces
one coarse seam, also `ONE`; inverse refinement of that coarse seam reopens a
fiber of `MANY(2)` oriented presentations.  A reset/no-active state is not a
third bit: the typed carrier is
`Option(Bit)={Reset,Active(0),Active(1)}`.  Collapsing `Reset` with `Active(0)`
is explicitly tested as information loss.  Raw `None`, including a contextual
decoder's no-image result, is rejected rather than coerced to reset.  The decimal carry value
`10` and the bit word `1|0` are different typed objects; no adapter between
them is asserted.  The words “forward” and “reverse” are conventions of this
packet; the bare binary seam has no intrinsic direction, and this finite
result is not a hidden endpoint of pi.

The endpoint circuit gives the decimal digits in order:

```text
0 = 3-3              5 = 5
1 = 3-(5-3)          6 = 3+3
2 = 5-3              7 = 5+(5-3)
3 = 3                8 = 3+5
4 = (3+5)/2          9 = 4+5.
```

All 45 endpoint pairs `A<B` are exhausted; 20 have an integer midpoint.  Only
`(3,5)` closes exactly to the set of decimal digits under this frozen grammar.
This is a bounded uniqueness result for the grammar, not a universal meaning
of the numbers three and five.

## 6. Receiver refinement inside the matrix

The addressed center cell `9` has four frozen witnesses:

```text
(3+5)+M11 = 9
(3+5)+M13 = 9
M12+5     = 9
3+M31     = 9.
```

The two addressed `1` cells merge at the expression receiver.  All expressions
merge at the value receiver:

```text
addressed witnesses -> MANY(4)
expression forms    -> MANY(3)
value               -> ONE(9).
```

Both interior `5` cells also equal the addressed right endpoint.  These are
redundant equality checks, not independent evidence that the digit five has a
universal role.

The compensation operators are partial decimal translations:

```text
C_-(x)=x-1
C_+(x)=x+1.
```

They are mutual inverses whenever the intermediate value stays inside
`0..9`.  “Present-to-past” and “future” are retained only as user-proposed
directional labels; the sealed theorem is the partial inverse arithmetic.

## 7. Two-sided contextual addressing

The source contains 96 occurrences of `3141`.  One digit on each side gives
64 combined flank classes, 41 singleton occurrences, and a maximum fiber of
four.  Two digits on each side uniquely distinguish all 96 within this
carrier.  The start boundary is `BOS|3141|59`; replacing `BOS` with an ordinary
digit loses that special address.

The literal `90|3141` occurs twice, in `90|3141|65` and `90|3141|94`.  It is a
useful hostile: the smaller seam is real but remains `MANY` until the right
context is retained.

## 8. Interpretation and ceiling

The musical “remix” analogy is useful but not an additional theorem.  The
literal digit carrier is one source structure; the 3-4-5 arithmetic grammar is
a second renderer.  A lawful remix preserves both projections.  Matching an
evocative result under only one untyped receiver is not enough.

This packet does **not** establish:

- a full proof, generator, random-access oracle, or predictor for pi;
- a terminal digit of pi;
- normality, randomness, statistical significance, or universality;
- intrinsic semantics for a digit word outside the declared receiver;
- `dimension=3`, `cap=5`, physical time, or a biomechanical law; or
- authentication.  Hashes provide integrity only.

## 9. Cold replay

From this directory:

```powershell
python -I -B .\verify_pi_three_level_345_matrix.py --require-sources
python -I -B .\verify_pi_three_level_345_matrix.py --require-sources --verify-stored --verify-manifest
```

The full acceptance command verifies both immutable parent packets, the pinned
ingress, live results, stored output, and the flat manifest.
