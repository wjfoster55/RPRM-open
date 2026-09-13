# What is needed for the exact BSD identity

We have made the missing identity explicit and tested several ways of
closing it. The exact complex BSD identity for this curve is still
unproved in this investigation. The established results remain substantial:
arithmetic and analytic rank two, a complete integral basis, rigorous
height and leading-coefficient intervals, and a trivial 2-primary part
of Sha. The new work identifies exactly what those results do not yet
connect.

For this curve, the local factors and torsion factors cancel. With the
period and height conventions fixed, the remaining equation is

\[
\frac{L''(E,1)}2=\Omega\operatorname{Reg}\,\#\Sha(E/\mathbb Q).
\]

The proved interval for the quotient of the first two real quantities is

\[
0.999920542\le
Q_E:=\frac{L''(E,1)/2}{\Omega\operatorname{Reg}}
\le1.000092816.
\]

That establishes close agreement. Exact agreement needs an additional
reason why the actual quotient cannot be a nearby noninteger. One
precise sufficient result would be: **\(Q_E\) is rational with reduced
denominator at most 10,000.** Any such rational different from 1 is at
least \(1/10000\) away from 1, while the entire certified interval is
closer. That would force \(Q_E=1\). The denominator premise remains
unproved; choosing four decimal places does not supply it. Even exact
real equality would still need a proof identifying the actual Sha group
and establishing its finiteness. [Theorem review](EXACT_IDENTITY_THEOREMS.md).

Your distinction between number levels has a precise use here. At the
whole-unit level, 0.6 reads as zero completed units while retaining a
remainder of 0.6. That remainder matters: two such inputs add to one
whole unit and remainder 0.2. Discarding both remainders would lose the
carry. Likewise, a small discrepancy can read as zero at the current
level and remain nonzero. A proof that the **same fixed discrepancy's magnitude**
reads as zero at every successively finer level would establish exact
zero; finitely many levels cannot. The signed movement remains as you
corrected it: the full step is −0.2, and the half-step is −0.1, ending
at the midpoint. [Exactness and levels](EXACTNESS_AND_LEVELS.md).

We also developed a direct identity route. The analytic side is an
explicit convergent weighted integral sum. The arithmetic side is now
an explicit convergent logarithmic doubling series, retaining every gcd
removed from the coordinates. Their finite sums and determinant changes
have exact formulas and complete tail bounds. To turn this into equality,
we need an exact matching rule valid at every stage, plus a proof that
its retained boundary remainder tends to zero. Setting that remainder
to zero because it has a coarse-zero readout would break the argument.
The new exact replay verifies the finite height telescoping and its
exceptional points; it does not supply the missing matching rule.
[Explicit identity target](EXPLICIT_IDENTITY_TARGET.md).

For an additional arithmetic component, we admitted an applicable
theorem at the odd prime 5 and reduced its missing calculation to a
specific algebraic trace \(T\) modulo 125. The current information
leaves all five possibilities
\(0,25,50,75,100\). Any of the four nonzero residues would prove
the 5-primary part of Sha trivial. Zero would leave this criterion
inconclusive. **The actual trace has not been computed.**

The next concrete computation is to construct and certify the correct
primitive CM division-point orbit, then calculate the first five
coefficients of its degree-256 minimal polynomial modulo 125. Newton
sums then give \(T\); an arbitrary polynomial factor cannot substitute
for that orbit. This would address the 5-primary component. The exact
real identity and the remaining Sha components still require their own
proofs. [Odd-prime attempt and exact next calculation](ODD_PRIME_ATTEMPT.md).
