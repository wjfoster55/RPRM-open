# E34 precision-source audit

Date: 2026-09-12. Scope: the real intervals A and B1 quoted in
[TWO_SCALES.md](C:/github/RPRM-open/research/bsd-coefficient-05/TWO_SCALES.md:11).
This is source inspection and exact arithmetic on saved width data, not a
fresh evaluation of either BSD side or a reproof of its mathematical premises.

**Finding:** the inspected numerical path uses exact Python integers and
`fractions.Fraction`, with explicit outward rounding. The reported width is
principally truncation uncertainty: the uncomputed Euler-series suffix for A
and the finite-depth canonical-height tail for B1. Ordinary floating-point
noise is not a supported explanation for these widths. Nor do the enclosures
establish a nonzero discrepancy: A is contained in B1. Their endpoint decimal
digits specify bounds, not that many known digits of the underlying values.

## Original source and arithmetic safeguards

The original construction is in `research/bsd-rank-two-01`, rather than the
later coefficient/display experiments.

| Object | Generating source and safeguards |
|---|---|
| A = L''(E,1)/2 | [interval.py](C:/github/RPRM-open/research/bsd-rank-two-01/work/interval.py:9) imports `Fraction`; lines 24–40 implement exact floor/ceiling to a dyadic grid and signed interval multiplication. [BUDGET.json](C:/github/RPRM-open/research/bsd-rank-two-01/work/BUDGET.json:9) sets 80 bits. Lines 44–111 enclose exp by alternating degree-31/30 sums and repeated outward squaring, log by a 32-term atanh series plus remainder, and pi by rational alternating Machin sums. |
| Canonical heights and regulator | [generator.py](C:/github/RPRM-open/research/bsd-rank-two-01/work/generator.py:14) uses exact Fractions/integers, a 100-bit grid, and eight doublings. Lines 59–84 implement 96-term logarithm bounds, enclosing large integer mantissas between adjacent 100-bit dyadics. Lines 123–157 perform exact projective duplication, actual gcd cancellation, and add a proved finite-depth height tail. Lines 215–218 enclose the mixed pairing and determinant. |
| B1 = Omega_all Reg_full | [factor_frontier.py](C:/github/RPRM-open/research/bsd-rank-two-01/work/factor_frontier.py:9) uses Fractions and a 100-bit grid. Lines 32–68 bound square roots by integer squares, pi by Machin sums, and the period by seven AGM updates. Lines 86–98 reconstruct the regulator from the unrounded Gram intervals and multiply by the unrounded period. Lines 28–29 and 112–114 produce the nine-place outward B1 display. |

The analytic producer first exports the completed coefficient outward at
eight decimal places, then multiplies its interval by `alpha=pi/68` at
[interval.py:312](C:/github/RPRM-open/research/bsd-rank-two-01/work/interval.py:312)
and [interval.py:342](C:/github/RPRM-open/research/bsd-rank-two-01/work/interval.py:342).
The saved raw `alpha_times_lambda2_interval`, rounded outward at eight places,
gives exactly A = [6.38511803, 6.38518585]. The simpler A display is documented
in [ANALYTIC_PROOF.md](C:/github/RPRM-open/research/bsd-rank-two-01/ANALYTIC_PROOF.md:148).
The saved `rhs_without_sha_outward` gives exactly
B1 = [6.384593255, 6.385625424]. Decimal exports use rational floor/ceiling;
they are not binary-float-to-string approximations.

## What determines the widths

The following numbers are diagnostic decimal renderings of exact Fraction
algebra on saved ledger fields. They do not claim a new execution receipt.

**Analytic side.** At M=160 the saved ledger has 27 nonzero Euler terms and
7,360 Simpson panels. The complete omitted-coefficient bound is implemented
at [interval.py:168](C:/github/RPRM-open/research/bsd-rank-two-01/work/interval.py:168):
the finite majorant covers 160 < n <= 4096 using divisor counts, ceiling square
roots, proved support restrictions, and upward-rounded exponential powers;
the geometric remainder covers every n > 4096. The head/suffix assembly is at
[interval.py:281](C:/github/RPRM-open/research/bsd-rank-two-01/work/interval.py:281).

| Width contribution | Saved-ledger size |
|---|---:|
| Completed finite head | 1.41523003169322e-8 |
| Complete symmetric Euler suffix, twice its radius | 0.00146768088607552 |
| Euler suffix share of raw completed width | 99.9990357465% |
| A, displayed width | 0.00006782 |

The suffix width is about 103,706 times the finite-head width. In the scaled
finite head `S=alpha*lambda2`, summing `abs(weight)*width_components[name]`
over the 27 saved terms gives quadrature width 6.53174792072e-10, improper
integral-tail width 6.59953615513e-13, elementary-enclosure/rounding width
3.59173472019e-21, and parameter width 8.33958685809e-22. These are S units,
not completed-coefficient units. The ledger fields and their construction
are at [interval.py:215](C:/github/RPRM-open/research/bsd-rank-two-01/work/interval.py:215)
and [interval.json](C:/github/RPRM-open/research/bsd-rank-two-01/evidence/interval.json:59).

The integral has distinct signed Simpson-error bounds, the alpha-parameter
correction, and a positive tail beyond transformed endpoint 32. Thus even
the finite-head uncertainty is predominantly a quadrature bound, not a
rounding artifact. The complete series suffix dominates all these terms.

**Arithmetic side.** The retained finite-depth bound is

`q(R) in 4^-k log H_x(2^k R) + [-log C0, log C1]/(3*4^k)`,

where k=8, C0=5,345,344 and C1=1,338,649. Its derivation is explicitly retained
in [GENERATOR_PROOF.md](C:/github/RPRM-open/research/bsd-rank-two-01/GENERATOR_PROOF.md:111).
The width from this tail alone is about 0.000150547830779886 for each of
P, Q and P+Q. The saved logarithm-enclosure contribution after division by
4^8 is only 2.86e-30 to 7.88e-30; final dyadic padding is around 1e-30.
The mixed-pairing interval and determinant propagate those height tails.
They also forget dependence when taking endpoint products, conservatively
enlarging the output; this is enclosure overestimation rather than float noise.

| Object | Saved raw width |
|---|---:|
| Period Omega_all | 4.73316543133e-30 |
| Regulator | 0.00114767142913550 |
| B1 | 0.00103216785007958 |
| B1, displayed width | 0.001032169 |

For the product-width identity
`width(Omega*Reg) = Omega_lo*width(Reg) + Reg_hi*width(Omega)`,
the period contribution is only about 3.36e-29. The regulator term accounts
for the shown B1 width to the displayed precision. Raw values are retained in
[factor_frontier.json](C:/github/RPRM-open/research/bsd-rank-two-01/evidence/factor_frontier.json:124).
The displayed B1 width is about 15.22 times the displayed A width. The
canonical-height tail is therefore the principal source of uncertainty in
this comparison. More arithmetic bits alone would barely change it.

## Evidence boundary and remaining seam

This audit read the three producers and the relevant written error bounds.
A read-only Python snippet parsed their saved JSON using `Fraction`, summed
the width fields, decomposed the product width, and checked the outward A/B1
exports. It also checked that each producer's current SHA-256 matches its
saved receipt's `source_sha256`; all three matched. Hash matching binds the
inspected bytes to the stored claim, not to mathematical validity. No saved
`PASS` was accepted as fresh verification, no producer was rerun, and no
new central interval was evaluated.

The code's exact arithmetic does not by itself prove the bound derivations,
curve inputs, analytic lower-zero premise, or full-basis theorem. Those are
separate written dependencies, not re-established here. The comparison's
exact identity/integrality seam also remains: overlapping intervals and a
quotient interval containing 1 do not prove equality or identify it with
#Sha. That restriction is explicit in
[FACTOR_COMPARISON.md](C:/github/RPRM-open/research/bsd-rank-two-01/FACTOR_COMPARISON.md:76).

Strongest supported conclusion: the source gives a finite-precision
enclosure budget dominated by omitted tails, and the decimal endpoints
cannot be read as measured nonzero disagreement. Tightening those tails
would improve numerical resolution; it would not on its own supply the
missing exact BSD comparison theorem.
