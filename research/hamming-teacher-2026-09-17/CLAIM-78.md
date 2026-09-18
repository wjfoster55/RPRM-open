# HT-78: seven answers, eight words, two other eights

17 September 2026. Next cut after HT-28, because the injectivity-vs-line
lemma is immediate ([LEMMA.md](LEMMA.md)). Nulls are frozen in
[NULL-78.md](NULL-78.md) and were written before this packet's
enumerator ran.

## Task record

1. **Carrier, types, equality, admitted context.** Three carriers with
   a shared numeral 8:
   - source `V = F₂³` and response words `E(x) ∈ F₂⁷`;
   - Hamming-7 `C = ker H ⊂ F₂⁷` and its even-parity extension `C8 ⊂ F₂⁸`;
   - source subgroup `U = span{1,2} = {0,1,2,3}` and a candidate toggle
     `c`.
   Equality is integer equality of the chosen bit-words. Checks, source
   roles, and error positions remain different types even when the
   bitmask is the same. Admitted context: exact linear algebra on these
   finite spaces. Nonlinear teachers and unfinished search are out of
   carrier.
2. **Supplied ports, missing ports, requested readout.** Supplied: column
   order `1..7` for `H` and `E`, named `U`, named `c = 4` and hostile
   `c = 3`. Missing: the image `S = E(V)`, whether `S = C⊥`, the
   cardinality of `C8`, and whether `U ∪ (c+U)` is eight source roles.
   Readouts are those complete sets and the yes/no equalities.
3. **Operation kind, direction, enabledness.** `E` is a total linear map.
   Parity extension is the determined bit `p = wt(z) mod 2`. Source
   expansion is XOR translation by `c`. No enabledness vacancy on these
   maps. Replacing a check panel is not this operation.
4. **Receiver.** Distinguish the three eights. `E` is asked to preserve
   source identity (`Q = id_V`), which is injectivity of `E`. Hamming-8
   is asked only for its message set, not for unique double-error
   location. Free toggle is asked for source-role cardinality, not for
   a dual-check panel.
5. **Inverse / complete fiber.** List all 8 values of `E`; all 16 words
   of `C`; all extensions in `C8`; the two sets `U ∪ (4+U)` and
   `U ∪ (3+U)`. Report ONE only after those lists are complete. Q5 is
   NONE if the three objects are not interchangeable, even if two of
   them have cardinality 8.
6. **Coverage, hostile case, evidence grade.** Coverage: every source
   `0..7`, every 7-bit word for `ker H` and for `C⊥`, both named
   toggles. Hostile: check panel `{1,2,3}` and source toggle `c = 3`
   share glyphs and must not be merged. Distinguishing control: `c = 4`
   really is outside `U`. Grade: **written** for P9–P9b as already in
   THEORY.md; **finite exhaustive test** for this replay. Not Lean.
   Not a claim that Hamming-8 double errors locate uniquely (they do
   not; that fiber is MANY, out of scope here).

## Claim under test

The seven-teacher map produces eight simplex words dual to Hamming-7.
Hamming-8 keeps sixteen messages. An independent source toggle doubles
four roles to eight. These are not one object.

## What this is not

Not a new coding theorem. Not a proof that every historical “seven plus
one” sentence is the simplex encoding. Not SAT. Not the silent ninth
position.
