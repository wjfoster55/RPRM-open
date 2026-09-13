# Independent review: signed stacking and the vacuum comparison

Date: 2026-09-12. Review disposition: no blocking mathematical or
implementation issue found at the stated fixed-source and finite-family
scopes. One optional implementation-description correction is recorded below.
This is a written review with bounded exact checker replay, not a formal
proof certificate or an independent construction of the continuum theory.

## Reviewed artifacts and retained source

- [VACUUM_COMPARISON.md](VACUUM_COMPARISON.md)
- [check_vacuum_comparison.py](check_vacuum_comparison.py)
- [STACKING_AND_SCALING.md](STACKING_AND_SCALING.md)
- [check_stacking.py](check_stacking.py)

The model and source analytic floor were read from
[GAP_BRIDGE.md](accepted_sources/ym2_global_phase_joint/GAP_BRIDGE.md) and
[NEXT_GLUE_LEMMA.md](accepted_sources/ym2_global_phase_joint/NEXT_GLUE_LEMMA.md).
Their accepted test suites were not rerun. The old source remains the
authority for the seven-link graph, full gauge invariance at all six
vertices, generator metric, inherited self-adjoint/form domains, and
ground-state transform. The present review checks the new deductions under
that contract rather than silently enlarging it.

## 1. Two different auxiliary spectra are kept distinct

For product Haar, edge integration `P_e` is an orthogonal projection onto
functions independent of that edge. Different edge projections commute.
They commute with the full gauge action because Haar integration is both
left- and right-invariant, so they preserve physical functions.

On a product Peter–Weyl component, `I-P_e` has eigenvalue zero for the
trivial edge representation and one for a nontrivial edge representation.
Thus `A_mu=sum_e(I-P_e)` counts nontrivial edge occurrences. A nonconstant
physical component cannot have a support vertex of degree one; its support
contains a cycle and therefore has at least four edges on this graph.
The plaquette fundamental trace attains this value. The physical auxiliary
gap is 4 and its sharp Haar variance constant is `1/4`.

By contrast, `-sum_e Delta_e` charges each nontrivial edge at least the
fundamental Casimir 3 in the retained `i sigma_k` convention. Its physical
gap is 12, attained by the same four-edge trace. Multiplying by
`kappa=alpha hbar^2/2` gives the free quantum gap `6 alpha hbar^2`.
The reviewed note does not interchange the count gap 4 and Casimir gap 12.

## 2. The global conditional-variance comparison needs one density ratio

Write `m<=rho<=M` and `R=M/m`. For a fixed subspace of candidate predictors,
the identity

```text
inf_g integral |f-g|^2 dnu
```

allows comparison before choosing either law's optimal predictor. In
particular,

```text
Var_nu(f) <= M Var_mu(f),
v_e^mu(f) <= (1/m) v_e^nu(f).
```

Equivalent bounded densities ensure that the admissible predictor spaces
coincide as sets of square-integrable functions. Combining the two
inequalities with the physical Haar constant `1/4` gives

```text
Var_nu(f) <= (R/4) sum_e v_e^nu(f).
```

The conditional expectations under the two laws need not agree. The
variational argument avoids that false assumption and pays for `M/m`
exactly once. Without the physical restriction, Haar tensorization supplies
the corresponding sufficient constant `R`.

## 3. Conditional local transfer gives R/3

After the outside links are fixed, dividing `rho` by its one-edge integral
normalizes the conditional density. That denominator cancels from the
conditional maximum-to-minimum ratio, leaving a ratio at most `R`.
The one-edge Haar Poincare constant is `1/3` under the same metric.
Variational comparison of the conditional variance, followed by reverse
density comparison of the derivative energy, therefore gives `R/3`.
Integration uses the actual vacuum exterior marginal. No exterior
independence or autonomous patch-vacuum assumption is introduced.

The seven singleton patches have overlap multiplicity one. Consequently
the sufficient glue inequality gives
`gamma>=alpha hbar^2/[2(R/4)(R/3)]=6 alpha hbar^2/R^2`.
The second factor of `R` here comes from composing two different
inequalities. It was not spuriously inserted into the conditional-variance
transfer alone.

## 4. The heat bound covers the entire series at the chosen time

The retained generator convention gives Casimir `n^2-1` for dimension
`n=2j+1`, so the character expansion and character modulus bound lead to
`sum_(n>=2) n^2 exp[-(n^2-1)]`. The expansion agrees with the Riemannian
kernel in [Baudoin and Bonnefont, section 3.2, equation (3.2)](https://arxiv.org/pdf/0802.3320):
their index `m=n-1` has `m(m+2)=n^2-1`. Their subelliptic kernel is a
separate object; the reviewed note explicitly retains this distinction.

For every integer `n>=2`,
`n^2-1-3(n-1)=(n-1)(n-2)>=0`. The finite positive Taylor partial sum
through degree eight is already greater than 20, so `exp(3)>20`.
The resulting geometric majorant is the complete convergent series

```text
sum_(n>=2) n^2 (1/20)^(n-1)
  = (1+1/20)/(1-1/20)^3 - 1
  = 1541/6859 < 1/4.
```

This proves `3/4<=q_1<=5/4` with analytic coverage of every spin. The
checker confirms the rational arithmetic and polynomial factorization;
it does not turn a finite spin enumeration into this universal argument.
The seven-factor heat-kernel ratio is consequently at most `(5/3)^7`.

## 5. The ground energy cancels, and squaring doubles the exponent

For bounded real potential the positive semigroup comparison is

```text
exp(-t max V) P_t u <= exp(-tH)u <= exp(-t min V) P_t u.
```

The scalar bounded-potential specialization is compatible with the
Feynman–Kac framework in [Boldt and Güneysu, Theorem 2.2](https://arxiv.org/pdf/2012.15551).
It also follows directly from positive Trotter factors as stated in the
note. The semigroup uses inverse-energy time and `P_t=exp(t kappa sum Delta)`.

Applying this to the positive eigenfunction produces a common factor
`exp(t E_0)` in the upper and lower pointwise estimates. It cancels when
taking their ratio. At `t=1/kappa`, the potential-oscillation exponent is

```text
t osc(V) <= 4 beta/kappa = 8r.
```

Thus the wavefunction oscillation is at most `exp(8r)(5/3)^7`, and its
squared density has ratio
`R_actual<=exp(16r)(5/3)^14=R_bar`. The positive integral of `psi_0`
also cancels. No replacement of the quantum vacuum by `exp(-V)` occurs.

For `N_p` plaquettes and `N_e` links, this same deliberately crude
construction has `osc(V)<=2 beta N_p` and therefore gives
`exp(8r N_p)(5/3)^(2N_e)`. The family scaling in the note is consistent.

## 6. Direct physical transfer improves R squared to R

Applying the physical Haar Poincare inequality directly gives

```text
Var_nu(f) <= M Var_mu(f)
          <= (M/12) integral |Df|^2 dmu
          <= (R/12) integral |Df|^2 dnu.
```

The ground-state transform then yields
`gamma>=12kappa/R=6 alpha hbar^2/R`, and replacing `R` by `R_bar`
preserves this lower bound. Smooth strict positivity on the compact source
makes multiplication and division by `psi_0` bounded invertible maps of
the inherited `H^1` form domain. Gauge invariance is retained. Closing the
smooth physical core therefore relates the inequality to the specified
physical Hamiltonian and does not select a new boundary extension of its
singular quotient.

The combined lower bound with the accepted variational estimate is valid.
The new positive term covers every finite `r` on the fixed graph, while
its deterioration with graph size or large `r` proves only deterioration
of this estimate. The exact free-vacuum control `R_actual=1` is correctly
preserved instead of being replaced by the loose heat upper bound.

## 7. The Bernoulli control has a uniform actual constant

For each finite `n>=1` and `0<p<1`, the `2^n` product functions
`chi_J=product_(j in J)(B_j-p)` form a complete orthogonal nonzero basis.
Conditional averaging annihilates a factor exactly when its coordinate
belongs to `J`. Therefore `A_n chi_J=|J| chi_J`, and the full spectrum,
multiplicities, sharp gap 1 and sharp constant `C_mix=1` follow.
Changing to one uniformly selected coordinate per discrete step gives
`I-A_n/n` and gap `1/n`; its clock is explicitly different.

For `p=3/5`, the centered outcomes, mean, variance, density ratio and sum
fibers in the note are correct. In particular `R_n=(3/2)^n`, while the
actual conditional-resampling constant remains one. This is a valid exact
family counterexample to interpreting an exponentially bad global
density comparison as evidence of an exponentially bad actual gap.
It supplies no statement about the actual Yang–Mills vacuum's correlations.

The general conditional-variance setup is consistent with the introductory
Poincare/heat-bath formulation in
[Caputo, Menz and Tetali](https://arxiv.org/pdf/1405.0608).
The stronger all-finite-`n` product conclusion is justified by the complete
basis proof in the reviewed note itself.

## 8. Execution and implementation scope

The following new default checker commands were run successfully:

```powershell
python -I -B research/ym2_signed_differences/check_vacuum_comparison.py
python -I -B research/ym2_signed_differences/check_stacking.py
```

Both recomputed their results and compared saved adjacent receipts without
writing. The stacking run covered 12 cubes (`n=1,...,4` for three admitted
probabilities), 90 complete-basis eigenvectors, 465 off-diagonal
orthogonality controls, and 42 complete sum fibers. The vacuum checker
replayed the exact rational constants, Taylor bound, factorization, and
gap-coefficient arithmetic.

Both implementations use explicit `require` checks rather than removable
Python `assert` statements. No old-source suite, `--write-results` mode,
eigensolver, simulation, or package installation was used for this review.
The checks do not establish general analytic soundness, operator-domain
facts, Peter–Weyl completeness, or uniform continuum limits; the review and
the notes retain those proof dependencies explicitly.

Optional wording issue: the final paragraph of `STACKING_AND_SCALING.md`
says the checker constructs conditional averaging matrices. The program
implements conditional averaging maps on a complete product basis without
materializing matrices. Replacing that phrase with “implements conditional
averaging maps” would describe the implementation more literally. This
does not change the result or its verification scope. No other author's
file was changed during this review.
