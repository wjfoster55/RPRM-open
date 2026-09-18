# ML-k: receiver-specific Markov lumping on named 2–4 state chains

17 September 2026. Smallest Rank-3 cut from the independent mathematical
reading. Nulls are frozen in [NULL.md](NULL.md) and were written before
this packet's enumerator ran.

## Task record

1. **Carrier, types, equality, admitted context.** Finite named states
   with name equality. Kernels are exact nonnegative `Fraction` tables,
   one normalized row per state. Partitions are surjective block maps.
   Receivers are total maps to a declared answer set. No floats, no
   booleans-as-ints, no imported `rprm` kernel checker.
2. **Supplied ports, missing ports, requested readout.** Supplied: the
   five named chains and the named partitions/receivers/ports in
   [NULL.md](NULL.md). Missing: which of those pairs are operational
   quotients. Readout is `ONE(yes)` or `NONE` per question, plus the
   matching-enabledness yes/no for Q4, Q10, Q11.
3. **Operation kind, direction, enabledness.** Kind is `KERNEL`.
   Direction is coarse-graining (state to block). Enabledness of a named
   zero-rate port is `rate>0`. Default ports are `enter_b`. A zero row
   is not admitted; every displayed row sums to `1`.
4. **Receiver.** Each question names its `Q`. A representation preserves
   `Q` exactly when `Q` is constant on each block (Manifesto II.2 /
   factorization). An operational quotient additionally requires strong
   lumpability (Manifesto IV.1.2 / handbook §11) and matching
   enabledness. Full source identity is not requested. The lumped matrix
   is not a molecular or physical law.
5. **Inverse / complete fiber.** For each named `(chain, C, Q)`, the
   fiber of the operational-quotient predicate is a singleton yes or an
   empty no. When `NONE`, the failing conjunct is named:
   `q_not_constant`, `not_lumpable`, or `enabledness`. Hidden paths
   inside a block remain a MANY fiber of the source chain and are not
   reconstructed.
6. **Coverage, hostile case, evidence grade.** Coverage: every named
   state, every named block-mass, every named port, exact `Fraction`
   arithmetic. Hostile: Q3/Q7/Q9 preserve `Q` and fail lumpability;
   Q2/Q6/Q8 are lumpable (or would be judged so) and fail `Q`-constancy.
   Distinguishing control: Q11/Q12 — equal supports of `enter_B` are
   not equal laws. Grade: **finite exhaustive test** of these named
   chains. Not Lean. Not a new lumpability theorem. Not a physics law.

## Claim

On these carriers, `C` is an operational quotient for `Q` exactly when
`Q` is constant on the blocks **and** the lumped process is strongly
lumpable, with matching enabledness at every named zero-rate port.
Constant `Q` is not enough. Lumpability is not enough. Equal supports
are not equal masses.

## What this is not

Not Rank-3's coarsest hitting/path/intervention construction. Not
Proposition IV.1.3's total-variation bound. Not an edit of the published
Manifesto. Not a claim that a reduced Markov matrix exists in nature.
