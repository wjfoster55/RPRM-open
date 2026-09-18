# IF-j: XOR/C fibers are not products of their marginals

17 September 2026. Rank-7 joint-correlation cut. Nulls are frozen in
[NULL-JOINT.md](NULL-JOINT.md) and were written before this cut's
enumerator ran.

## Task record

1. **Carrier, types, equality, admitted context.** Bits2 and Bits3 as
   in IF-k, tuple equality, exact integer bits. A marginal is a set of
   coordinate values. A product of marginals is a set of tuples. Those
   are different types from a joint fiber.
2. **Supplied ports, missing ports, requested readout.** Supplied: the
   IF-k complete fibers `XOR1`, `XOR0`, `AND1`, `C00`, `C11`. Missing:
   whether each equals the product of its one-port marginals, and the
   exact extra-illegal family. Readout is yes/no of equality plus the
   complete extra list.
3. **Operation kind, direction, enabledness.** Kind is projection to a
   coordinate then Cartesian product. Direction is reconstruction from
   separate missing ports. Enabledness does not split this cut.
4. **Receiver.** The joint fiber, not the independently reconstructed
   product. A later continuation that needed the XOR=1 law would fail
   if given `(1,1)` from the product.
5. **Inverse / complete fiber.** The extras are the complete difference
   `product \ fiber`. `NONE` of equality is issued only after both
   sets are fully listed. An unfinished listing of extras is `OPEN`.
6. **Coverage, hostile case, evidence grade.** Coverage: every member
   of each named fiber, every member of each product. Hostile:
   reconstructing XOR=1 from `{0,1}×{0,1}` admits `(0,0)` and `(1,1)`.
   Distinguishing control: AND=1 **does** equal `{1}×{1}`; QJ8 — XOR=0
   and XOR=1 share one product. Grade: **finite exhaustive test**. Not
   Lean. Not a physics law.

## Claim

On Bits2, the XOR=1 fiber is not the product of its one-bit marginals:
that product is all four pairs and adds the XOR=0 fiber. The C=(0,0)
and C=(1,1) fibers are not the three-way products of their bit
marginals: each product is all eight triples. Reconstructing missing
ports independently yields extra illegal tuples. A singleton AND=1
fiber does equal its product. Complementary XOR fibers share one
product, so the product does not select the law.

## What this is not

Not IF-k's representative-as-ONE hostile. Not discriminating-view
selection. Not a claim that no fiber ever factors. Not a physics law.
