# E5: full BSD theorem and exact Sha specialization

This continuation concerns only the elliptic curve over Q with ordered
Weierstrass coefficients `[0,0,0,-25,0]`. The supplied review establishes
algebraic rank one, analytic rank one, `Sha(E/Q)[2^infinity]=0`, and
`E(Q)_tors=(Z/2)^2`. Combining an applicable published full BSD theorem with
the new independently justified generator and factor bounds proves
`#Sha(E/Q)=1`. Consequently Sha is trivial at every prime, including all odd
primes, and `L'(E,1)=Omega(E)*Hhat_x((-4,6))/2` exactly.

## Contract and evidence grades

The carrier is this fixed E/Q, its rational Mordell–Weil group, its
Tate–Shafarevich group and its normalized Hasse–Weil L-function. Equality of
curves in this record means the exact supplied Q-model; a common j-invariant
alone is insufficient. The supplied ports are the accepted analytic/descent
results and the explicitly cited theorem. The requested readouts are the full
BSD identity and the order of Sha. The operation is forward theorem
specialization followed by interval isolation of a positive integer. It is
enabled only with all theorem hypotheses and normalization checks below.
The receiver retains model, base field, analytic rank, minimal differential,
height convention and the distinction between a subgroup regulator and the
regulator of the full free group. No inverse curve-identification or search
completion fiber is claimed.

The global theorem is `THEOREM_CITED`, including its published computer-assisted
proof. Applying it to the supplied curve is a `WRITTEN_PROOF`. The new
arithmetic and analytic enclosures retain their own grades; neither a software
self-test nor the publication citation is described as a formal proof or a
fresh replay of the authors' entire computation.

## Published theorem actually inspected

Creutz and Robert L. Miller, *Second Isogeny Descents and the Birch and
Swinnerton-Dyer Conjectural Formula*, Theorem 1.1, states full BSD for E/Q with
conductor below 5000 and analytic rank at most one. The conclusion includes
finite Sha and

    L^(r)(E,1)/r! = Omega(E) Reg(E(Q)) #Sha(E/Q) prod_p c_p / #E(Q)_tors^2.

Here Omega integrates the absolute minimal invariant differential over all
E(R). There is no CM, residual-irreducibility, prime-exclusion, or optimal-curve
hypothesis. The theorem was read in arXiv v2, printed page 2; the proof is in
section 7.1. The arXiv record identifies publication in *Journal of Algebra*
372 (2012), 673–701 and DOI 10.1016/j.jalgebra.2012.09.029.
[Theorem text](https://arxiv.org/pdf/1105.4018v2#page=2),
[publication/version record](https://arxiv.org/abs/1105.4018v2).

As a dependency check, Miller's earlier Theorem 1.2 establishes the primewise
BSD assertion in the same conductor/rank range except eleven reducible pairs.
Table 9, printed page 23, has conductors
546, 570, 858, 870, 1050, 1230, 1938, 1950, 2370, 2550, 3270.
None is 800. Its definition of primewise BSD includes rationality of the
analytic order and equality with the actual primary order; it is stronger than
rank equality. This also supplies a route for E5, but is not an independent
proof of Creutz–Miller's result.
[Miller, Theorem 1.2 and Definition 1.1](https://arxiv.org/pdf/1010.2431v3#page=2),
[Miller, Table 9](https://arxiv.org/pdf/1010.2431v3#page=23).

Both sources were inspected on 12 September 2026. The publisher endpoint for
the Creutz–Miller article returned HTTP 403 to the reading tool; the authors'
arXiv v2 full text and its publication metadata were available and inspected.

## Hypotheses specialized to the supplied equation

1. **An elliptic curve over Q.** The projective completion of
   `y^2=x^3-25x` has its rational identity at infinity and discriminant
   `1,000,000`, which is nonzero. The base field is Q.
2. **Correct conductor.** The accepted `ANALYTIC_THEOREMS.md`, section 1,
   proves the exact rational isomorphism `(x,y)=(5u,25v)` to Elkies's
   `5v^2=u^3-u`, then checks the family theorem's hypotheses to obtain
   `N=32*5^2=800`. In particular `800<5000`.
3. **Analytic rank hypothesis, independently supplied.** The accepted
   analytic argument proves `L(E,1)=0` and
   `556371/250000 < L'(E,1) < 1114529/500000`. Positivity of the lower
   endpoint gives analytic rank exactly one. No algebraic-rank database entry
   is substituted for this premise.
4. **Normalization of the leading coefficient.** At rank one `r!=1` and
   the Taylor coefficient is `L'(E,1)`. The prior analytic argument uses the
   Hasse–Weil L-function with central point 1. The full-period convention in
   the theorem must be used, including both real components.
5. **Minimal differential.** The supplied model is globally minimal: its
   discriminant valuations are 6 at 2 and 5 and zero elsewhere; valuations
   of integral Q-isomorphic equations differ by multiples of 12 and cannot
   become negative. Thus the differential to retain is `omega=dx/(2y)`.
6. **Torsion factor.** The accepted review's `TORSION_COROLLARY.md` proves
   the exact four rational torsion points using good reduction at 3. Hence
   the denominator is `4^2=16`.
7. **Height convention.** Write `Hhat(Q)=lim_n 4^(-n) h_x(2^n Q)`, with
   `h_x(Q)=log max(|a|,c^2)` for reduced `x(Q)=a/c^2`. The BSD pairing is
   `(Hhat(U+V)-Hhat(U)-Hhat(V))/2`; hence its diagonal at Q is `Hhat(Q)`.
   At rank one a primitive P therefore gives `Reg(E(Q))=Hhat(P)`, not
   `Hhat(P)/2`. Cremona, section 3.4, printed pages 71–72 (PDF pages 10–11),
   defines this limit, pairing and determinant and explicitly identifies
   the larger of the two height normalizations as the one for BSD.
   [Cremona, height/regulator normalization](https://johncremona.github.io/book/fulltext/chapter3.pdf#page=10).

The theorem ranges over every rational elliptic curve satisfying these
conditions, so an LMFDB/Cremona label or a choice of optimal representative is
not an additional admission requirement. No database rank, regulator or
analytic Sha value is used here.

These checks prove, without assuming BSD for E5,

    Sha(E/Q) is finite,
    L'(E,1) = Omega(E) Reg(E(Q)) #Sha(E/Q) (prod_p c_p)/16.       (1)

## Exact Sha order: completed specialization

Let `A=Omega(E) Reg(E(Q)) prod_p c_p`. Every factor is positive. Once certified
independent bounds show

    0 < 16 L'(E,1) / A < 2,

equation (1) identifies that real number with the positive integer
`#Sha(E/Q)`, so its unique possible value is 1. This is integer isolation
after an applicable theorem, not numerical rounding used as a proof of BSD.
A tighter enclosure around 1 is optional; no presumed square-order property
or numerical agreement is needed. Order one then makes every primary
subgroup, including every odd-primary subgroup, trivial.

The independent `GENERATOR_PROOF.md` proves that `P=(-4,6)` is primitive, and
`evidence/generator.json` records free index 1. This proof uses descent, the
height theorem, a global height comparison and complete finite enumeration;
it does not use BSD or a presumed Sha order. Thus the height in the factor
receipt is the regulator of the full free group.

`BSD_FACTORS.md` and `evidence/bsd_factors.json` establish

    93809582917/40000000000 <= Omega <= 1172619786463/500000000000,
    1899437/1000000 <= Reg <= 1899511/1000000,
    c_2=2, c_5=4, and c_p=1 for every other prime.

In particular `Omega>2`, `Reg>3/2`, and `prod_p c_p=8`, so `A>24`. The
accepted derivative enclosure and equation (1) now give the exact chain

    0 < #Sha(E/Q) = 16 L'(E,1)/A
                  < 16*(1114529/500000)/24
                  = 1114529/750000 < 2.

Since the group is finite, its order is a positive integer. Therefore the
complete order fiber is **ONE(1)**, and the group fiber is **ONE(trivial)**.
This proves `Sha(E/Q)[p^infinity]=0` for every prime p, including every odd
prime. Together with the established factors, equation (1) becomes

    L'(E,1) = Omega(E) Reg(E(Q))/2
            = Omega(E) Hhat_x((-4,6))/2.                        (2)

An independent Fraction-only reassembly of the readable factor endpoints
also encloses the quotient between `0.999136` and `1.000782`. The factor
receipt obtains its slightly tighter lower endpoint `0.999138` from its raw
intervals. Readable outward rounding widens the recomputed interval, so those
two lower bounds are deliberately distinguished. Either enclosure isolates
the same unique integer. The simpler chain above needs no decimal arithmetic.

No unsolved odd-primary or coefficient-formula seam remains for this E5
specialization. The imported full BSD theorem remains an explicit dependency;
this continuation does not claim a new proof of that general finite-conductor
theorem, its published computational verification, or general BSD.

## Coverage boundary and hostile cases

The universal theorem's range is essential: conductor at least 5000 or
analytic rank above one would disable this application. This record makes no
claim about such a curve. Replacing E5 by a different j=1728 equation would
invalidate the supplied conductor, derivative and arithmetic certificates.
Using only one real component changes Omega by a factor of two. Using a
nontorsion point whose index is m instead of a primitive generator changes
the rank-one regulator by m^2. These normalization failures would invalidate
the Sha-isolation step even though equation (1) remains true with the correct
invariants. Trivial two-primary Sha alone does not rule out odd-primary Sha.

## Local evidence anchors

- `supplied_review/BSD_E5_REVIEW/input/BSD_E5_CODEX_TEST_01_RETURN/ANALYTIC_THEOREMS.md`: exact model, conductor,
  minimality and independent analytic order argument.
- `supplied_review/BSD_E5_REVIEW/REVIEW.md`: accepted independent derivative
  enclosure, arithmetic rank, and two-primary Sha conclusion.
- `supplied_review/BSD_E5_REVIEW/TORSION_COROLLARY.md`: exact torsion group.
- `GENERATOR_PROOF.md` and `evidence/generator.json`: primitive generator,
  independent of the BSD formula.
- `BSD_FACTORS.md` and `evidence/bsd_factors.json`: real period, normalized
  height, Tamagawa factors and exact interval arithmetic.
- `evidence/bsd_sha_theorems.json`: machine-readable hypothesis and source
  audit for this continuation.
