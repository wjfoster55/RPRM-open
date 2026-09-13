# Operational value and the next BSD relation

The operational-value material helped. We recovered the definition you
meant, implemented a concrete relation on the curve, and proved another
previously open arithmetic ingredient. We have not proved full BSD.

Your earlier correction is preserved: a number's lawful relations belong
to the admitted mathematical structure before we discover them. RPRM's
operational state selects what must remain available for a particular
question and its next operations. It does not create those relations.
The original user passages and corrected definition are in
[OPERATIONAL_VALUE_RECOVERY.md](OPERATIONAL_VALUE_RECOVERY.md).

## The implemented shadow relation

Two different points on E34 have the same scalar shadow:

    P=(−2,48),       twin=(578,−13872),
    shadow(P)=shadow(twin)=−12.

A mirror of that same value also agrees, so it adds no distinguishing
information. But the shadow after doubling is positive for one point
and negative for the other. Retaining the present and next shadows gives
an explicit inverse recovering the original point.

The complete finite test covered4096 curve points. One shadow grouped
them into2048 pairs; the present-and-next pair distinguished all4096.
This is an actual implementation of the operational-state idea, with
its inverse, allowed operations and exceptional cases checked.

There is a more relevant pairing test too. P and its twin have the same
individual canonical height. After adding the same Q, their 5-adic
quadratic heights give different residues:4 and3 modulo5. Thus the
arithmetic receiver needs the relationship between points when they
combine. Separate scalar values alone lose that information. The
[operational explanation](OPERATIONAL_BRIDGE.md) gives the formulas.

## The new arithmetic result

We calculated the ordinary cyclotomic5-adic height pairing on the actual
free basis. In the explicitly named MST convention its matrix is

    [1 2]
    [2 2]   modulo5,

whose determinant is3 modulo5. It is therefore nondegenerate. This was
derived from exact rational eightfold points and a bound covering the
entire uncomputed sigma-function tail; no matching decimal was used.
An independent implementation using different duplication formulas agreed.

Together with the earlier rank and Sha5 results, this closes the
Bockstein-regulator nonvanishing condition in the published BKS route.
The [independent audit](PADIC_HEIGHT_AUDIT.md) checks the theorem
hypotheses and normalization conversions.

We also made an arithmetic third object concrete: a vector W constructed
from that pairing and elliptic logarithms. It is the unique solution of
a specified linear pairing equation and is invariant under a change of
integral basis. Its first normalized5-adic digit is W/5=3Q modulo5.
That is a congruence, not an exact identity W=15Q.

## The precise issue still stopping the proof

A published theorem places the canonical derived5-adic class in the line
spanned by this regulator. The exact multiplier connecting that relation
to the **real** analytic BSD leading coefficient remains unproved.
The derived class may still be zero; its nonzero scale was not inferred
merely from collinearity.

This sharpens the third-relation question: we now have a concrete
arithmetic relation, its nonzero vector and a proved5-adic comparison.
The next missing law is the exact scalar comparison in BKS Corollary6.7,
equivalently its rank-two Generalized Perrin–Riou comparison. Describing
that multiplier as a shadow, or approximating it at finitely many
precisions, does not by itself fix its exact value.

Total Sha and the full complex BSD identity also remain open. No claim
that general BSD follows from operational reconstruction is made.

The return includes runnable source, fresh witness files, independent
readbacks, the theorem audits, original-source recovery and
[BSD_REBRIEF.md](BSD_REBRIEF.md). Run the four new calculation stages with
`python -I -B work/run_operational.py --output runs/my_fresh_run`.
The included isolated final replay is `runs/return_validation/RUN.json`.
