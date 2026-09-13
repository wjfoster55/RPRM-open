# Independent review of the connected-response obligation

12 September 2026. Bounded audit of
[NEXT_CONNECTED_OBLIGATION.md](NEXT_CONNECTED_OBLIGATION.md) and the newly
added controls in [check_stacking.py](check_stacking.py). No blocking
mathematical issue was found. This review does not prove that the actual
SU(2) vacuum admits the factorization or uniform response bound proposed
as its next obligation.

## Absolute-support envelope

Equation (C1) is correct for a finite graph containing `N` edge-disjoint
simple square cycles and `d>=0`. Any chosen `k` cycles contribute `4k`
different edge occurrences. Their union has no degree-one vertex:
at a vertex on the union, each incident selected cycle contributes two
distinct incident edges. Sharing vertices does not invalidate this fact.
Edge-disjointness also makes distinct cycle selections give distinct
supports. The `binomial(N,k)` selections therefore supply the stated
subfamily of terms in the full support polynomial.

The direction of the inequality and its use are properly distinguished.
It is a lower bound on `eta_G(d)`, which is itself only an upper-bound
envelope for the kernel deviation. At the certified choice `d=3/5`, six
such cycles give

```text
(1+(3/5)^4)^6-1
 = 64226020542915231/59604644775390625 > 1.
```

Hence `1-eta_G(3/5)` fails as a positive lower bound. This does not bound
the actual kernel deviation below, does not forbid a better one-link
constant or use of cancellations, and does not imply a vanishing gap.
The note preserves these distinctions explicitly.

## Conditional cancellation and bounded tilt

Under the stated finite-factor product-reference contract with positive
factors and bounded logarithms, all conditional normalizers are finite
and nonzero. Factors supported entirely outside `B` cancel in the
normalized conditional law. On changing only exterior coordinate `j`,
the remaining factors that do not contain `j` cancel from the ratio of
unnormalized inside densities. Thus (C3) retains exactly the factors
meeting both `B` and `j`. The ratio of the normalized conditional laws
is the exponential tilt by `h_B,j`, divided by its expectation in the
first conditional law. No normalizing constant was omitted from the
probability comparison.

For the bounded-tilt lemma, finite essential oscillation of the real
function `h` gives `0<a<=c<=b<infinity` in the notation of the note.
When `a<b`, the chord majorization of `|z-c|` has expectation
`2(b-c)(c-a)/(b-a)`. Dividing by `2c` gives the first displayed bound
on total variation. Maximizing over `c` is equivalent to minimizing
`c+ab/c`, whose minimum `2sqrt(ab)` occurs at `c=sqrt(ab)`.
The resulting ratio equals `tanh(log(b/a)/4)`. The two-point law with
that mean is admissible and attains the bound. The separate `a=b`
case is handled correctly. This proves sharpness over the stated
bounded-tilt class, not attainment for every supplied probability.

For a single connecting factor, put `F=log w_C`. The oscillation in
`U_B` of `F(U_B,omega')-F(U_B,omega)` is at most the sum of the two
slice oscillations, hence at most `2 osc(F)` over the full factor
carrier. Oscillation is subadditive under the finite sum, proving the
last inequality of Section 3. Constants independent of inside variables
have zero oscillation, consistent with conditional normalization.

## Exact controls and coverage boundary

Executed without writing:

```powershell
python -I -B research/ym2_signed_differences/check_stacking.py
```

It returned PASS and matched [RESULTS_STACKING.json](RESULTS_STACKING.json).
The three new sharp-tilt rows have raw endpoint pairs
`(1,9/4)`, `(1,4)`, `(1,25)`; normalizers `3/2`, `2`, `5`; and exact
total variations `1/5`, `1/3`, `2/3`, respectively. Their base
probabilities are positive, sum to one, and give the required endpoint
means. The same replay also recomputed the adjacent finite product
controls: 12 cubes, 90 complete basis eigenvectors, 465 orthogonality
controls, and 42 complete sum fibers. These are separate finite checks;
the general support-counting, conditional cancellation, and sharp-tilt
claims have the written proofs audited above.

The note correctly leaves the actual quantum-vacuum factorization,
remainder control, uniform influences, a justified influence-to-variance
criterion with its update rates, physical scaling, and continuum
construction unresolved. No other file was changed by this audit.
