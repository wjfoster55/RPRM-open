# Prestige one, numerical uncertainty, and a justified stopping scale

The user proposes that, at higher prestige levels, further apparent
decimal structure might become floating-point loss or currently unknown
detail. This experiment tests that distinction against the actual BSD
producer code and a recovered prestige-envelope construction.

The main correction to the previous explanation is simple: the small
BSD difference interval does not establish a small nonzero discrepancy.
It contains zero. Its width records uncertainty in the current enclosure.

## What the actual arithmetic does

The original E34 programs use Python integers and `Fraction` for their
coefficient, point and interval calculations. They reduce interval
endpoints to a dyadic grid using outward rounding:

```
down(x) = floor(2^p*x)/2^p
up(x)   = -down(-x)
```

Consequently `down(x) <= x <= up(x)`. This finite precision enlarges an
enclosure rather than silently replacing uncertain lower digits with
asserted digits. The analytic kernel also retains explicit errors from
quadrature and omitted series/integral tails. The canonical-height
kernel retains the remaining height tail after eight point doublings.

The [source audit](agents/PRECISION_AUDIT.md) records the exact producer
locators and error accounting. It identifies the omitted analytic series
tail and, more strongly in the final comparison, the arithmetic height
tail as the dominant retained uncertainties. Its quantitative breakdown
uses saved exact error ledgers as attributed input; it does not rerun the
original producers or certify every theorem behind those ledgers.

Fresh exact subtraction of the previously attributed endpoints gives:

| Enclosure | Width |
|---|---:|
| A, analytic coefficient | 0.000067820 |
| B1, period times full regulator | 0.001032169 |
| D1=A-B1 | 0.001099989 |

The arithmetic-side width contributes `1032169/1099989` of the last
width, about 94%. These are widths of independent interval enclosures,
not measurements of a nonzero BSD discrepancy.

For a specific floating-point control, binary64 cannot distinguish the
integers `2^53` and `2^53+1` after conversion; exact fractions keep their
difference equal to one. That failure mode exists. However, repeating
just the displayed BSD endpoint subtraction in binary64 introduces less
than `10^-15` error per endpoint. The current D1 width is more than a
trillion times larger than those particular conversion/subtraction errors.
This comparison concerns the final subtraction only; the source audit
establishes the earlier producers' different arithmetic mechanism.

## What prestige retains

The [recovered prestige account](../../recovered-concepts/PRESTIGE-AND-NUMBER-OPERATIONS.md)
describes a completed construction that can appear as one while retaining
a relationship or route into its contents. It explicitly preserves the
user's correction that the contents need not all be materialized inside
the visible symbol. That historical account is broader than the particular
finite envelope used below.

The current [envelope proofs](../../experiments/core_recovery_bridge_01_r2/PROOFS.md)
provide a useful exact example. A Boolean-valued function on a three-bit
cube has eight values. Retain seven and keep a route to the omitted one.
The all-zero function and the function whose only one is at the eighth
site have the same seven-value summary:

```
retained summary: 0 0 0 0 0 0 0
possible full state 1: 0 0 0 0 0 0 0 0
possible full state 2: 0 0 0 0 0 0 0 1
```

All 256 Boolean tables were freshly enumerated. There are 128 summaries,
each with exactly two full-state preimages. For questions about the seven
retained sites, the summary is sufficient. For "is the whole function
zero?", it is insufficient. Flipping the first coordinate brings the
hidden site into a retained position and separates the two possibilities.

The omitted bit is exact structured data, not roundoff noise. A prestige
summary can stop reopening details only for observations and operations
proved to be preserved by that summary. This criterion is already part
of the envelope contract; it does not make every lower-level distinction
irrelevant at a higher prestige level.

More generally, a readout descends through a summary exactly when every
two admitted sources with that summary have the same answer. Necessity:
one summary output cannot give two different answers. Sufficiency:
assign the common answer to each attained summary. This proof supplies
a question-specific stopping condition without pretending omitted data
has been recovered.

## A stopping scale the existing BSD bounds actually justify

For E34, take the attributed intervals

```
A  in [6.38511803, 6.38518585]
B1 in [6.384593255, 6.385625424]
Q  = A/B1.
```

B1 uses the candidate Sha-order-one arithmetic factor. This experiment
does not establish the actual finite order of Sha or the exact BSD identity.
Because B1 is positive, interval division gives
`Q in [A_lower/B1_upper, A_upper/B1_lower]` exactly.

Nearest-decimal rounding, with ties upward for these positive inputs,
is monotone. Both endpoints round to 1.000 at three decimal places;
therefore every compatible Q does too. This is a proved rounded readout
conditional on the attributed enclosures.

At four decimal places the lower endpoint rounds to 0.9999 and the upper
to 1.0001. The rounded readout is no longer uniquely determined. The
tests check decimal-place requests zero through six using rational
arithmetic, with no decimal approximations in the decisions.

The old interval premises admit both abstract controls:

| A | B1 | Exact Q | Q rounded to three places |
|---|---|---|---|
| 6.38515 | 6.38515 | 1 | 1.000 |
| 6.38515 | 6.38505 | 127703/127701 | 1.000 |

They show why the rounded answer can be settled while exact equality
remains unsettled. They are not claimed as alternative actual L-values
or counterexamples to BSD.

Changing scale does not remove the distinction if the inverse is retained:
`(A/s-B1/s)=(A-B1)/s`, and multiplying back by s recovers it for s!=0.
The exact nonzero control D1=1/10000 remains nonzero at tested scales
1, 10 and 10000. A unit label by itself does not prove that finer values
are prohibited by the mathematical carrier.

The useful next mathematical obligation is to identify a summary and a
proved law that preserve the exact BSD equality question, or to prove an
independent discreteness restriction on the actual normalized quantity.
The existing prestige construction does not itself provide that BSD law.
More digits alone also do not replace it.

## Replay and evidence boundary

Run the standard-library verifier with a fresh output path:

```powershell
python -I -B .\work\check_precision.py --output .\replay\precision.json
```

The [fresh evidence](evidence/precision.json) records exact fractions,
the binary64 control, complete zero-summary fiber, all tested rounding
requests, interval-compatible controls, and source hash. The script
checks 256 Boolean cube tables, seven big-integer conversion cases,
seven rounding resolutions and three retained changes of scale.

No new L-function or height enclosure was evaluated. Existing source
claims, source inspection, exact manipulations of saved ledgers, written
proofs, finite tests and the open BSD obligation remain distinct. Other
research lanes, prior packets, and prestige implementations were read only.
