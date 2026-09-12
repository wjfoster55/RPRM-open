# Written proofs for advertised envelope identities

**RCF01-envelope-1 · evidence grade: written proof, separate from finite tests.**

These proofs apply to the declared carriers. Finite tests do not enlarge them.
No novelty is claimed for Möbius inversion or ordinary factorization.

## Carrier

Sites `X = {0,1}^3` addressed by masks `s in {0,...,7}` with bit0=`h`, bit1=`x`,
bit2=`y`. Functions `f: X -> Q`. Coefficients

```text
r_S = sum_{T subseteq S} (-1)^(|S|-|T|) f(T),
f(S) = sum_{T subseteq S} r_T.
```

`C2` retains `(r_S : |S| <= 2)` and omits `r_{hxy}`. Equivalently, retain `f` on
`B2 = {s : |s| <= 2}` (masks `0..6`). Grade is relative to this origin/basis.

## Identity 1 — `C2` is closed under pointwise `+` and `*`

**Hypotheses.** Arbitrary `f,g: X -> Q`. Operators never read `r_{hxy}` or `f(111)`.

Addition is linear, so retained coefficients add.

For multiplication: after Boolean reduction `u^2 = u`, the product of monomials
indexed by subsets `A,B` with `|A|<=2` and `|B|<=2` has support `A union B`.
If `|A union B| <= 2`, the output coefficient of degree `<=2` is determined by
retained inputs. A factor already containing all three coordinates cannot appear
among those inputs, and cannot contribute a lower-degree term through union.
Hence every degree-`<=2` output coefficient is a function of the seven retained
coefficients of each factor.

Equivalently, `f|B2 * g|B2 = (f*g)|B2`, so the B2 restriction is a product
subalgebra of `Q^X`.

**Not claimed.** Division, symbolic algebra off the cube, or admission predicates.
**Finite-test bound.** All 256 Boolean-valued tables and all 65,536 ordered pairs;
32 structured rational tables for round-trip. Not a theorem for `n>3` from these
counts. The written argument is for this `n=3` Boolean cube (the union support
claim is the same for general `n` with omitted grade `n`, but that is a separate
contract).

## Identity 2 — pullback acts on `C_S` iff `H(S) subseteq S`

**Hypotheses.** `X` finite, `Y` has at least two values, every `f: X -> Y`
admitted. `C_S(f) = f|S`. `U_H(f) = f compose H`.

If `H(S) subseteq S`, every needed value `f(H(s))` is retained, so `U_H` descends.

Conversely, if some `s in S` has `H(s) = u notin S`, choose `f,g` agreeing off
`u` and disagreeing at `u`. Then `C_S(f)=C_S(g)` but `U_H(f)(s) != U_H(g)(s)`,
so no well-defined output from `C_S` alone.

**Least repair in the retained-site family.** For a finite set of maps, close `S`
forward. Because `X` is finite this stops; the result `S*` is the least
forward-closed superset. Any smaller retained-site superset fails for some
arbitrary law.

**Hostile constrained class.** If laws are restricted to degree `<=1`, the two
functions differing only at `u=111` are not both in the class, so the converse
need not apply. Affine laws remain exact on `C2` under `flip_h` (PE20). This is
a successful simplification, not a refutation of Identity 2 on its stated domain.

**For this cube.** `B2` plus `h`-flip reaches mask `7`, so `S*` is all eight
sites. `clamp_*_0` and identity leave `B2` closed. `flip_*` and `clamp_*_1` do
not.

## Identity 3 — finite fiving adapter

On `C10`, `d = 5h + r` with `h in {0,1}`, `r in {0,...,4}`. `F(d) = d+5 mod 10`
preserves `r` and toggles `h`. For each `r`,

```text
A_r(h,x,y) = (5h+r, x, y)
(F x id x id) A_r = A_r compose (h |-> 1-h).
```

Checked on all 40 triples `(r,h,x,y)`. This is an authored adapter, not evidence
that every historical fiving is a cube bit-flip. It is not F5 arithmetic.

## Identity 4 — strong winding

`n = 10w + 5h + r`. One fiving: `(w,h,r) -> (w+h, 1-h, r)`. Two fivings:
`(w,h,r) -> (w+1, h, r)`. Finite display return is not strong return.

Algebra holds for all integers `w` and the stated `h,r`. Finite samples
`w in {-3,...,3}` are tests, not the identity.

## Identity 5 — Double-Stamp enabledness

Using donor labels `{c,a0,a1,b0,b1,c0,c1,z}` and the stamp-swap involution,
quotient counts are `A5=(3,2,0)`, `B6=(3,3,1)`, `C7=(4,3,0)`. Dwell is an
authored process permission: admitted at `A5` and `C7`, forbidden at `B6`.
Vertex-orbit count `3` does not decide dwell. Raw vertex count `5` does not
identify fiving display `5`.

Split `A5 -> B6` and midpoint `B6 -> C7` are the source-declared transitions.
No physical-safety theorem.

## What is not proved

- Prestige One's full 1-to-9 acquisition lifecycle
- A commuting bridge from fiving splice `{0,5}` to Double-Stamp restart
- Runtime advantage of `C2` (instrumented, not benchmarked)
- Universal compression failure for every law class
- LawCube F2 ANF equivalence (different field and address order)
