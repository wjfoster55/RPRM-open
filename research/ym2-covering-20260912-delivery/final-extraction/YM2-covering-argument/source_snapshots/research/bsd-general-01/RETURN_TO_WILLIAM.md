# Starting the general BSD argument

We have started the general argument in a separate research directory. This
first pass produces general proof components and exact tests, and identifies
where they stop. It does not prove general BSD. The underlying ingredients
are established mathematics; no claim of a new theorem in the literature is
made.

## What we can now say beyond E5

**A compatible sequence of finite answers needs a source-height bound.**
We proved that compatible rational-point residue classes come from a single
rational point exactly when their representatives can be chosen within one
fixed height bound. Here height measures numerator and denominator size,
not merely the apparent size of a displayed coordinate. Using moduli n!
recovers a unique point. Using only powers of one prime can leave some
torsion ambiguity.

This gives a precise place where a carry/readback construction could help:
prove the source-height bound and its compatibility, and the reconstruction
step follows. The complete operation is not yet specified, so this is a
testable requirement for it, not an assumption about what it does.

We also proved a counterexample to omitting the bound. For every n, solve
3m=1 modulo 2^n. Each finite problem has an integer answer, and those answers
are compatible. Yet there is no single integer with 3m=1. Using the primitive
E5 generator turns this into an actual elliptic-curve example, even though
E5's Sha is trivial. This prevents us from confusing infinitely compatible
labels with a rational source point. [Proof and full fibers](RECONSTRUCTION.md)

**Selmer information splits into rational-point information and Sha.**
For every elliptic curve over Q, prime p and positive n, the exact formula is

    |Sel_(p^n)| = p^(n r) * |T/p^n T| * |Sha[p^n]|.

Here r counts independent infinite directions, and T is the finite torsion
group. Thus the total number of finite classes alone does not determine r:
Sha can contribute extra classes. We proved a finite certificate that closes
rank and one primary part of Sha when independent points meet a sound Selmer
upper bound. This generalizes the logical form of the E5 descent without
assuming every curve behaves like E5.

There is also a useful exact stopping criterion: once the actual rank and
torsion are known, if the normalized Sha contribution has equal size at two
adjacent p-power levels, the whole p-primary part has been reached. Equality
of approximate bounds does not suffice. Settling each prime separately still
requires a proof that only finitely many primes contribute to settle total
Sha. [Written proofs and counterexamples](SELMER_TOWER.md)

**The analytic calculation now has an arbitrary-order formula and a proved
tail bound.** We derived it for the completed L-function of any E/Q, with
the conductor, sign and local factors explicitly supplied. The tiny tail can
be bounded using rational arithmetic. The included utility calculates this
bound; it does not yet evaluate the new finite integral heads for another
curve. [Formula and proof](ANALYTIC_BRIDGE.md)

## The next obstacle is now more precise

There is a useful refinement to my earlier explanation. Existing theorems
say that analytic rank zero or one forces the matching arithmetic rank.
Consequently an independently proved arithmetic rank at least two rules out
analytic ranks zero and one. Combined with the functional-equation sign:

- For a rank-two curve with positive sign, a rigorous nonzero second
  completed coefficient finishes the rank comparison.
- For a rank-three curve with negative sign, a rigorous nonzero third
  coefficient does the same.
- For rank four with positive sign, these ingredients still leave an exact
  second-coefficient zero to prove before a nonzero fourth coefficient
  establishes rank four.

These are applications of known results, not a claim that all cases of
ranks two or three are settled. They identify which certificate remains
necessary for an individual input. [Wiles, the low-analytic-rank theorem](https://www.claymath.org/wp-content/uploads/2022/05/birchswin.pdf#page=4)

This exact-zero issue matters. The function t^4 + epsilon*t^2 has even
symmetry and a nonzero fourth coefficient, but has order two for every
epsilon>0, however tiny. So “the lower coefficient looks like zero” cannot
complete the argument. This is a test of the proposed inference, not a
counterexample to BSD or an asserted elliptic L-function.

Our concrete next numerical target is a certified second-coefficient
interval for one independently established rank-two input. It would test
the generalized kernel beyond E5's one-direction case. The harder general
research target is a proved mechanism for the remaining exact zeros,
together with the separate finiteness and leading-value arguments. A
successful rank-two calculation would not itself supply those arguments.

## What was executed and what remains open

Seven groups of fresh, exact checks passed: finite quotient sizes, bounded
reconstruction, compatible towers without a rational source, generator
saturation, Selmer-growth ambiguity/stabilization models, analytic false
inference controls, and the rational Mellin tail utility. The evidence keeps
actual E5 rational-point checks distinct from abstract group and polynomial
controls. The proofs cover the stated general domains; finite tests do not
stand in for those proofs. No formal proof assistant was run.

General rank equality, general Sha finiteness, and the full general BSD
formula remain OPEN. The carry/swap law and its arithmetic/analytic adapter
remain OPEN too. The prior E5 results are reused at their stated scope;
no further curve computation, paper, publication or other research lane was
started. The new work is fully contained in this directory.

Start with [README.md](README.md) for reproduction and
[CLAIM_LEDGER.json](CLAIM_LEDGER.json) for the proof obligations.
