# MC-k: toy measurement-contract audit of Count2 / Mean2 / FourState

17 September 2026. Smallest Rank-8 cut from the independent mathematical
reading. Nulls are frozen in [NULL.md](NULL.md) and were written before
this packet's enumerator ran.

## Task record

1. **Carrier, types, equality, admitted context.** Bits2 is the four
   ordered pairs on `{0,1}` with tuple equality. Count2 is integer
   bit-count `a+b`. Mean2 is exact `Fraction` density `(a+b)/2`.
   FourState is Manifesto III.7.2 `a+2b`. No floats, no
   booleans-as-ints, no imported `rprm` measurement helper.
2. **Supplied ports, missing ports, requested readout.** Supplied: both
   bits when the instrument is enabled; Q11 supplies only `a=1`.
   Requested: whether named `Q` is constant on representation fibers;
   the complete pair-fiber at named displays; joint versus product of
   marginals; units/receiver of Mean2; enabledness with a missing port.
3. **Operation kind, direction, enabledness.** Kind is a total function
   on `X` when both ports are present. Direction is measurement:
   source pair to display. Count2/Mean2 is enabled iff both ports are
   supplied. FourState uses the same enabledness.
4. **Receiver.** Each question names its `Q` (`XOR`, `FST`, `PAIR`) or
   a typed units/enabledness obligation. A representation preserves `Q`
   exactly when `Q` is constant on each fiber. The display numeral
   equalling `Q` is a different receiver (estimator equivalence).
   Occupancy of `[0,1]` is not a probability-of-XOR receiver.
5. **Inverse / complete fiber.** Pair-fibers are listed
   lexicographically. `NONE`/`ONE`/`MANY` only after a complete census
   of `X`. A missing port is not a fiber of the pair; it is disabled.
6. **Coverage, hostile case, evidence grade.** Coverage: all 4 points,
   every named display, exact integer/`Fraction` arithmetic. Hostile:
   Q3/Q12 a Count2 display that looks like an identified pair (`ONE`
   representative or CAR) while count `1` is `MANY`; Q4 independent
   missing ports; Q2/Q10 estimator-as-display and `[0,1]` occupancy as
   a probability law; Q5 first-bit from the mean; Q11 one-sample mean
   of a missing-port instrument. Grade: **finite exhaustive test** of
   these named instruments. Not Lean. Not a laboratory audit. Not a
   physics law.

## Claim

On Bits2, Count2/Mean2 identifies `XOR` (parity is a function of
count) and does not identify `FST` or `PAIR`. The Mean2 numeral is not
`XOR`. Count `1` is `MANY((0,1),(1,0))`, not a representative and not
the product of bit-marginals. Mean2 and Count2 share a kernel and not
a unit. A missing port disables Mean2. FourState identifies the pair
at codes `1` and `2`.

## What this is not

Not Rank-8's machine-readable workflow standard. Not Process Mechanics'
BRCA1 or figure-reconstruction calibration. Not an edit of the
published Manifesto. Not a physical measurement law.
