# IF-k: complete preimage fibers of named finite forward maps

17 September 2026. Smallest Rank-7 cut from the independent mathematical
reading. Nulls are frozen in [NULL.md](NULL.md) and were written before
this packet's enumerator ran.

## Task record

1. **Carrier, types, equality, admitted context.** Bits2 is the four
   ordered pairs on `{0,1}` with tuple equality. Bits3 is the eight
   ordered triples. Add3 is `{0,1,2}` with ordinary addition and no
   wrap. Equality of bits is integer equality. Unordered supports are a
   different type from ordered pairs. No floats, no booleans-as-ints, no
   imported `rprm` solver.
2. **Supplied ports, missing ports, requested readout.** Supplied: the
   named total maps `AND`, `XOR`, `NAND`, `CONST0`, the 3-to-2 readout
   `C(x,y,z)=(x XOR y, x XOR z)`, and Add3 with a named sum `c`. Missing:
   the joint input tuple. Readout is the complete preimage fiber,
   classified `NONE` / `ONE` / `MANY` only after a complete census, else
   `OPEN`.
3. **Operation kind, direction, enabledness.** Kind is a total function
   (or the addition relation on Add3). Direction is inverse: output
   supplied, inputs requested. Every named map is total on its domain, so
   enabledness does not split this cut.
4. **Receiver.** The requested observation is the complete joint fiber,
   not a representative, not a class label, and not the product of
   one-port marginals. A later continuation that needed a forgotten
   preimage member would fail if only a representative had been kept.
5. **Inverse / complete fiber.** For `f:X→Z` and specified `z`, the fiber
   is `{x in X: f(x)=z}` listed lexicographically. For Add3 the fiber is
   the joint `(a,b)` completions of `a+b=c`. `NONE`/`ONE`/`MANY` are
   issued only for a complete fiber. An unfinished search is `OPEN`.
6. **Coverage, hostile case, evidence grade.** Coverage: all 4 Bits2
   points, all 8 Bits3 points, all 9 Add3 pairs, exact integer
   arithmetic. Hostile: treating two solutions as one by picking a
   representative (Q2 `N_and0_rep`, Q3 `N_xor1_rep`, Q7 `N_c00_rep`,
   Q8 `N_c11_rep`, Q10 `N_add2_rep`, Q12 `N_xor0_class`). Distinguishing
   controls: Q6 joint versus product of marginals; Q9 stopped search
   must stay `OPEN`. Grade: **finite exhaustive test** of these named
   maps. Not Lean. Not inverse graphics. Not a physics law.

## Claim

On these carriers, the inverse of a specified output is the complete
preimage fiber: `ONE((1,1))` for `AND=1` and `NAND=0`, `NONE` for
`CONST0=1` and Add3 `c=4`, and `MANY` of every remaining listed tuple
for `AND=0`, both XOR outputs, both named `C` outputs, and Add3 `c=2`.
A representative is not a fiber. A product of marginals is not a fiber.
A stopped search is `OPEN`.

## What this is not

Not Rank-7's certified approximate families or discriminating-view
selection. Not a claim that Boolean preimages are new mathematics. Not
an edit of the published Manifesto. Not a physical inverse-design law.
