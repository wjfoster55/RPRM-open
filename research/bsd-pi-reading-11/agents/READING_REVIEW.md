# PI11 reading review — actual-distance digit extraction and the complete fiber

Date: 2026-09-12. Reviewed `work/check_reading.py`, `work/height_kernel.py`,
and selected structured fields from `evidence/reading.json`. No root code was
edited. Fresh independent checks used exact `fractions.Fraction` arithmetic
on the recorded bounds, enumerated the 100 decimal cells, rebuilt all seven
admitted D0 words, checked boundary controls, and verified both recorded
source hashes. All of those checks passed.

**Disposition: the adopted adapter now has an exact finite-prefix output for
the actual enclosed distance, not merely an open glyph reading.** Its
complete real-input fiber is `[2.034,2.035)`. The role and position choice
is an explicitly proposed adapter; neither a context-free decoding rule nor
a universal pi/BSD relation follows.

## 1. What the refinement certifies

The recorded exact rational distance endpoints give:

| depth | lower bound | upper bound |
|---:|---|---|
| 8 | 2.033986700633 | 2.034023708364 |
| 9 | 2.034001230068 | 2.034010481998 |

The depth-8 interval is inside the earlier printed interval
`[2.0339867006,2.0340237084]`. The two depths use the source kernel's same
curve, input point, height convention, and tail theorem. This review
checked the downstream exact interval arithmetic and source identity; it
did not rerun the large height recurrence or supply a new proof of the
kernel's attributed global height-tail theorem.

At depth 9, exact rational comparison gives

```text
2.0340 < lower <= d <= upper < 2.0341.
```

Therefore `floor(10000*d)=20340`: the first four fractional digits are
literally `0340` under the canonical floor-based digit convention. The
certificate does not fix the fifth fractional digit, because the interval
crosses `2.03401`.

The entire original interval already rounded to `2.0340` at four fractional
places using nearest, with ties upward. It sits strictly within that
rounding cell `[2.03395,2.03405)`, so no tie policy affects this result.
However, the original interval did not certify the literal digit pair of
the actual value: it crossed `2.034`. Depth 9 resolves that distinction.

The `zero_counts` fields count digits in **outward decimal displays of
interval bounds**. They do not count an intrinsic property of d. In
particular, a four-place outward upper display can be `2.0341` while the
strict exact interval still certifies `floor(10000*d)=20340`. The counts of
three zeros in the original ten-place bounds are true at that width;
appending one valid trailing zero preserves both rational values and changes
the counts to four. This is a tested representation dependence.

## 2. Carrier, extraction law, and full inverse fiber

Use the **bounded real carrier** `X=[2,2.1)` with real equality. This is not
a finite carrier. Its digit readout has the finite carrier `D^2` of 100
ordered decimal pairs:

```text
f(x) = (floor(100*x) mod 10, floor(1000*x) mod 10).
```

The two selected ports are the hundredths digit and thousandths digit of
the same real value. They are not the curve parameter 34, an arbitrary
occurrence of the string 34, or a lower-bound digit paired with an
upper-bound digit. This extraction is a new explicitly adopted adapter.

For every pair `(a,m)` in `D^2`, its complete fiber on X is

```text
f^-1(a,m) = [2 + a/100 + m/1000,
             2 + a/100 + (m+1)/1000).
```

Proof: `n=floor(1000*x)` ranges over precisely `2000,...,2099`. Then the
second port is `n mod 10`, and the first is `floor(n/10) mod 10`. Every
pair in `D^2` specifies exactly one n. Its real preimage is exactly
`[n/1000,(n+1)/1000)`. This proves both directions and complete coverage,
including the half-open boundary conventions.

Thus

```text
f^-1(3,4) = [2.034,2.035).
```

The depth-9 interval is contained in this fiber, so `f(d)=ONE((3,4))` as
a readout of the admitted d. Recovering d from that pair instead returns
the complete `MANY([2.034,2.035))` real fiber. No finite enumeration of real
members is claimed or needed.

## 3. Composing the historical finite chart

The endpoint–midpoint chart is defined on exactly

```text
C = {01,02,03,12,13,23,34}.
```

It sends `(A,m)` to endpoints `(A,B)=(A,2m-A)` and half-gap `delta=m-A`.
The old endpoint carrier is exactly the integer family
`A>=0`, `delta>=1`, `2A+3delta<=9`. The root script independently exhausts
that family and agrees with the older seven pairs. D0 then constructs

```text
[delta,    A+delta,   delta ]
[A+2delta, 2A+3delta, 2delta]
[A+3delta, A+2delta,  A     ]
```

and serializes `A | row-major matrix | B`. The complete composed map is
partial on X: it is enabled precisely on the following seven real cells.
An implementation wishing to make it total must add an explicit
out-of-chart result for the other 93 digit states.

| f value | enabled real cell | D0 output word |
|---|---|---|
| 01 | [2.001,2.002) | 01112323202 |
| 02 | [2.002,2.003) | 02224646404 |
| 03 | [2.003,2.004) | 03336969606 |
| 12 | [2.012,2.013) | 11213524313 |
| 13 | [2.013,2.014) | 12325847515 |
| 23 | [2.023,2.024) | 21314725424 |
| 34 | [2.034,2.035) | **31415926535** |

These seven distinct codewords make the composition's target fiber exact:
if `F = D0_serialize after endpoint_midpoint_chart after f`, then

```text
F(d) = 31415926535,
F^-1(31415926535) = [2.034,2.035).
```

This is an exact finite-prefix-decoder relation about the actual d under
the adopted adapter. The word-side chart is reversible on its seven
states. The whole map from real values is lossy at f. The recovered
historical D0/D1 tag ambiguity remains: both historical decoder tags agree
at the target, so a unique word does not determine a unique decoder law.

The root's independent Machin evaluation certifies
`floor(10^10*pi)=31415926535`; therefore the composed output equals the
actual first eleven decimal digits of pi. The exact rational tangent
identity and alternating-series bounds support this calculation. The
principal branch follows from
`0 < 4 atan(1/5)-atan(1/239) < 4/5 < pi/2`, together with tangent equal to
1. This numerical verification is independent of the E34 height
calculation. It does not make the historical codebook's selection or the
new digit-role adapter an independently discovered source law.

## 4. Distinguishing controls and preserved open questions

Fresh exact boundary controls:

| x | f(x) | four-place truncation | nearest four places |
|---|---|---|---|
| 2.033999999 | (3,3) | 2.0339 | 2.0340 |
| 2.034 | (3,4) | 2.0340 | 2.0340 |
| 2.034075 | (3,4) | 2.0340 | 2.0341 |
| 2.0349 | (3,4) | 2.0349 | 2.0349 |
| 2.035 | (3,5) | 2.0350 | 2.0350 |

The first control shows why old rounded `2.0340` did not suffice to prove
`f(d)=34`. The last control proves the target fiber excludes its upper
endpoint. The two internal controls produce the same pi-prefix output
while changing finer digits or rounding. They explicitly witness the
information that F forgets. Neither is asserted to be the actual E34
distance.

The 220 root word tests reject exactly the tested family: on each old
eleven-digit bound word, choose one map from `{I,P,N,T,M}`, optionally
reverse, and choose one of eleven cyclic rotations. Every resulting
literal word differs from the certified pi prefix. This does not test
arbitrary compositions of digit maps, all position permutations, a
positional carry grammar, or the endpoint–midpoint chart now adopted.

The 26 decimal-shift tests reject the explicit equalities
`d=10^k*pi` and `d=10^k*(4-pi)` for integer `k=-6,...,6`. The additional
`d^2-1=pi` equality is also rejected by separated exact intervals. These
outcomes do not refute the broader underspecified carry/swap/zip reading.

The arithmetic result is consequently stronger than “only a glyph
candidate”: with the displayed adapter adopted, the source enclosure
forces the output. What remains proposed is selecting the hundredths and
thousandths positions, interpreting them as endpoint and midpoint, and
using the historical codebook for this question. This report does not
attribute those choices to a user preference that was never specified.

No full-pi generation, recovery of the source real from the output,
analytic identity tying pi to this height, full BSD comparison, or universal
closure theorem is established. Independent anti-pi remains the earlier
open source question. A new claim would need a newly specified receiver,
operation, and distinguishing experiment.

## 5. Relationship to PI_HISTORY.md

`PI_HISTORY.md` was written before the depth-9 evidence. Its initial
interval candidate paired the differing thousandths digits of two bounds.
The f used here instead reads hundredths and thousandths in one actual
value. Both adapters are well defined once named; they have different
input types and must not be silently identified.

The historical report's endpoint–midpoint formulas and codebook remain
unchanged. Its earlier statement that an actual-distance extraction
remained wholly unresolved is refined here: **the explicit extraction
and chart composition are now exactly certified; choosing that grammar
as the intended interpretation remains proposed.**
