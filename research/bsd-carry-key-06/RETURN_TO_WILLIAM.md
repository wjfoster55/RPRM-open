# What your operational reading found

Your follow-up now has an executable compression-and-handoff version:
2301+3125=5426 folds to 566 by merging its middle columns. With the
source's carry information retained, the candidate shadow map sending
each digit through N after M gives the path 566 -> 687 -> 808 -> ... .
566 remains an intermediate state, as you specified. The next stage
depends on the chosen operation and retained source ports; it is not
ordinary counting. [COLUMN_HANDOFF.md](COLUMN_HANDOFF.md) gives the
complete proof, inverse repair and ten-step continuation.

The model passes an exhaustive audit on 10,000 four-digit source words.
It retains 5,500 distinct operational states, preserving every later
folded readout under the admitted shadow and mirror operations. This
is a verified finite mechanism. Its identification with a BSD bridge
and its final readiness condition remain open.

The ordered digits do support exact constructions. We found

    426 -> reverse -> 624 -> add 1 -> 625.

The carry is especially clear in base five: 624 is 4444, and adding
one makes 10000. The initial reversal is decimal, so the change of
number representation has to stay in the rule.

Your midpoint/gap reading also has a complete finite version:

| View 426 | View 625 |
|---|---|
| center 4 | computed outer value 6 |
| gap 2 | the same gap 2 |
| computed outer value 4+2=6 | upper endpoint 4+2/2=5 |

The record has endpoints 3 and 5, center 4 and gap 2. This relates to
the recovered pi key. Both views recover the same record. The rule works
across seven admitted records, and only this row meets a power-of-five
modulus. This is a proposed assignment of roles to the BSD digits;
we have not proved that the curve forces membership in that family.

The precision test preserves a useful boundary. A fresh analytic
calculation gives the next digit:

    b2 = 2301 modulo 3125.

Reversing 2301 and adding one gives 1033, not 3125. More strongly,
none of the five possible next lifts can satisfy that same reversal
rule. The old finite key is exact; its unchanged extension fails.

There is a stronger retained-carry connection. Treat the coefficient
as an operation that multiplies a state. It preserves the state's
lower two base-five digits while moving a higher digit block. Five
repetitions give:

    b2^5 = 1   modulo 125
    b2^5 = 251 modulo 625.

The coarse display has returned, while the finer display still records
a remainder of 250. Every further five-fold iteration moves this
nonzero carry up one precision level. This is an exact version of
retaining what happened when a lower layer appears to close.

The 4/6 cue also yields a valid coordinate conversion: 6=1+5 and
-4=1-5 define opposite nearby logarithmic coordinates. The quadratic
analytic coefficient and the matching arithmetic determinant transform
by the same factor. Their ratio is preserved.

The remaining question is now concrete: can an operation derived
independently from the arithmetic data select the analytic scalar,
including its successive carries? The operations tested here do not
yet do that. General BSD, full E34 BSD and total Sha remain open.

Full contracts, proofs and counterexamples are in OPERATIONAL_PROOF.md;
the runnable source and fresh evidence are in work/ and runs/fresh_validation/.
