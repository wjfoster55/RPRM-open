# review005 — acceptance and closure review

## Decision

Accept the delivered default run and close the Lind–Reichardt worked example.
No blocking mathematical or reproducibility defect was found. One vacuous
assertion should be removed during ordinary maintenance; it does not invalidate
the surrounding checks or require another certificate-development phase.
This review does not authorize a new experiment or reopen earlier obligations.

## Inputs and preservation

Input: `review005.zip`, containing a complete runnable snapshot, the new local
checker, receipts, and the accepted global-obstruction dependency.

Active manifest: `MANIFEST.review005.json`.
SHA-256: `1803aed09eaf2e18a53ad4512503ca7d75e85d26a3dddb0974fd4a65f826a529`.

Rehashed:
- 60 delivery inventory entries, with no missing, mismatched, or unlisted payloads;
- 40 snapshot inventory entries, likewise complete;
- all 28 manifest-bound files, unchanged from the prior review004 source.

These are overlapping inventories, not 128 independent tests.
Delivery inventory SHA-256:
`544d1c728eaff6129d31b160ea300a79e2efd4d1ca1419e87f63d5855be82b26`.

All original input bytes remained unchanged. Execution occurred in a reconstructed
workspace and new output directories, not over the submitted receipts.

## Fresh execution

1. Reconstructed the bound source and supplied manifest, then ran `run_all.py`.
   All five stages, post-run integrity, and protocol coverage returned PASS.
   Question cases 11/11, operation cases 3/3, and controls 21/21 appeared exactly
   once. All five mathematical result objects matched the delivered records and
   the preceding review004 result objects.
2. Ran the supplied reviewer probe to a fresh path.
3. Ran the submitted independent local checker against that fresh receipt.
   Local witness arrays, identities, opposite-branch records, and controls match
   the submitted records. Timestamps, runtime metadata, and paths are not expected
   to be byte-identical.

The local construction covers every prime at most 199: 46 primes and 604 recorded
prefixes, comprising depth 12 at the 45 odd primes and depth 64 for the normalized
2-adic variable. There are 558 adjacent-prefix transitions. Six local negative
controls executed successfully. No new mutation campaign was conducted.

See `evidence/REPLAY_AND_INVENTORY.json` and the fresh execution files.

## Separate reviewer implementation

`independent_math_check.py` imports neither submitted local checker. It uses
SymPy 1.14.0 for exact symbolic identities and independent prime enumeration.
It then reconstructs each root by enumerating the complete next-digit fiber,
not by using the inverse-derivative update in the submitted generators.

Results:
- 604/604 prefixes matched the new construction;
- 558/558 next-digit fibers contained exactly the recorded continuation;
- original homogeneous curve equations and weighted-chart identities checked at
  all prefixes;
- all 604 rational representatives have nonzero exact rational residual: they
  are approximations, not rational solutions;
- direct affine and infinity enumeration agreed at all 45 odd probe primes;
- opposite exceptional branches at 2, 3, 5, and 17 were checked;
- the alternate x-lifting direction was checked at all 30 zero-y seeds across
  13 probe primes, through depth four.

The last item tests an existing branch of the derivation which the first-affine-
seed selection did not happen to exercise. It is not a new arithmetic family.

This is an independently written finite mathematical check, not independent
proof-assistant verification of the universal theorems or a comparison of agent
performance. See `evidence/INDEPENDENT_MATH_CHECK.json`.

## Written proof review

### Scope

The curve is the smooth projective model of `2y^2 = 1 - 17x^4`, with the
weighted equation `2Y^2 = Z^4 - 17X^4`. The affine `Z=1` and infinity `X=1`
charts cover the odd-characteristic curve; the ambient exceptional point with
X=Z=0 does not lie on the curve there.

### Exceptional places

- Real: x=0 and either real root of `2y^2=1` give points. This is an exact
  algebraic witness, not a decimal approximation.
- p=17: `2y^2-1`, residue y=3, has residual 17 and derivative 12. Its affine
  seed is smooth even though the displayed special fiber is singular at infinity.
- p=3: at x=1, `2y^2+16`, residue y=1, has residual 18 and derivative 4.
- p=5: no affine F_5 points; the infinity chart has residues Y=2 and Y=3.
  Fixing Z=5 produces `2Y^2-608`, residue 2, residual -600 and derivative 8.
  Hensel gives beta, and `[1:beta:5]` becomes `(1/5,beta/25)` over Q_5.
- p=2: `17(1+4z)^4+31 = 16g(z)` is an exact integer-polynomial identity,
  where `g=3+17z+102z^2+272z^3+272z^4`. At z=1 the value is 666 and the
  derivative 2125. Dividing exact polynomial coefficients in Z is not modular
  inversion of 16 at 2.

### All remaining primes

For odd p not 17, the partial derivatives exclude a singularity in either
chart. The quartic has four distinct geometric zeros, so the associated
separable double cover is geometrically connected and has genus one by the
stated Riemann–Hurwitz formula. The zero multiplicities also show it remains
nonsquare over the algebraic closure; geometric connectedness is not inferred
from a finite point count.

For p>=7, Hasse–Weil gives more than two projective points because
`(p-1)^2-4p > 0`. There are at most two infinity points, so an affine seed exists.
The required inequality follows uniformly by writing p=7+h with h>=0:
`(p-1)^2-4p = h^2+8h+8 > 0`.

At a seed, either y is nonzero and the y derivative is a unit, or y=0 and the x
derivative is a unit. The simple-root Hensel theorem supplies the exact local
point. This is the all-primes proof; the 46-prime run is not extrapolated into it.

### Precision

The submitted guarantee at p=5 is correct for the equation residual:
`R_affine = R_homogeneous / 5^4`.
Depth n in the homogeneous residual therefore implies valuation at least n-4
in the affine residual. At the delivered depth 12 the bound is at least 8; the
particular final representative happens to have valuation 9. The guaranteed
bound is conservative, not erroneous.

Do not conflate the precision of beta, beta/25, and the equation residual.
For beta known modulo 5^n, the y-coordinate uncertainty scales by 5^-2 while
the displayed equation residual scales by 5^-4. The exact coordinate change
does not make the exact point less valid.

## One nonblocking implementation cleanup

`source_snapshot/extras/review005_local/independent_local_check.py`, line 266:

```python
require(affine_residual.denominator == 1 or True, 'fraction_residual')
```

This predicate is always true. It provides no validation and should be removed,
not advertised as a test. Do not blindly replace it with a blanket integrality
requirement: affine residuals at low p-adic precision can be nonintegral.

It is redundant with respect to this delivered result: the surrounding code
checks the exact chart identity and homogeneous divisibility, and the new reviewer
checker independently evaluates rational p-adic valuations at every prefix.
No corruption was observed, and the delivered default-depth guarantee remains
valid. This review is not a certification of every optional CLI parameter or
an adversarial parser audit.

A wording improvement for the next ordinary edit: 5 is invertible in Q_5 but
not a unit of Z_5. Avoid the phrase 'Q_5 unit-inverse denominator' when the
relevant distinction is membership in these different rings.

## Integrated meaning and claim boundary

Review004 explicitly left the local constructions unexecuted. Review005 closes
that task. Combined with the accepted covering certificate and global reciprocity
proof, this is one inspectable classical example of points everywhere locally
but none over Q. It is not an unresolved numerical experiment.

The covering/Jacobian identification is inherited, not re-proved in this pass.
The resulting nonzero class killed by two in Sha(Q,E), with E: V^2=U^3+17U,
retains its earlier scope. No total Sha order, rank, Selmer enumeration, analytic
L-function, BSD theorem, novel arithmetic theorem, performance benefit, or
proof-assistant certification is established by these checks.

Freeze this as an exposed development/reference case. The separate semantic,
arithmetic-transfer, and SQL sampler remains the next active method test. Do
not count this thoroughly exposed example as an unseen test of the protocol.

## Primary theorem references checked in this review

- Keith Conrad, Hensel's Lemma, Theorem 2.1 and Remark 2.3:
  https://kconrad.math.uconn.edu/blurbs/gradnumthy/hensel.pdf
- Stacks Project, Riemann–Hurwitz:
  https://stacks.math.columbia.edu/tag/0C1B
- Colliot-Thélène and Poonen, Algebraic Families of Nonzero Elements of
  Shafarevich–Tate Groups: introduction for the exact Lind–Reichardt statement;
  local-point discussion for the use of Weil bounds and Hensel lifting:
  https://math.mit.edu/~poonen/papers/shafamily.pdf

These are theorem dependencies, not new results proved by the finite checker.
