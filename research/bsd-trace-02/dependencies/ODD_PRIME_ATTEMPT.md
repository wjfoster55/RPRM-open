# One odd-prime attempt: E34 at p=5

**Result: OPEN.** The Coates–Liang–Sujatha theorem hypotheses at p=5 have
been admitted, and the missing value has been reduced to one specific
degree-256 algebraic trace modulo 125. That trace has **not** been
calculated. No conclusion that Sha(E34/Q)[5^infinity]=0 is established.

The new executable `work/odd_prime.py` checks the finite admission data,
an explicit isogeny identity, the conductor norm count and the trace
polynomial. Its fresh `evidence/odd_prime.json` deliberately reports
`OPEN`, with null trace and valuation fields. A successful admission check
is not a successful critical-value calculation.

## Fixed curve, readout and precise theorem

Our curve is E:y²=x³−1156x, hence **D=1156** in the papers' notation
y²=x³−Dx. It is not their D=−34 curve y²=x³+34x. The requested readout is
the actual 5-primary subgroup of the cohomologically defined Sha, not a
conjectural analytic order or a database prediction. The accepted input
proofs in `input_source/` establish algebraic and analytic ranks two.

The relevant theorem is [CLS I, Theorem 2.2, PDF p.5](https://arxiv.org/pdf/0901.3832#page=5):
at an admitted split good prime, with matching rank parity and the stated
unit conditions, valuation equal to the rank of its critical Hecke value
implies trivial primary Sha when reduction is non-anomalous and p is
prime to six. The theorem does not assume complex BSD. The presentation
in [CLS II, §4, PDF p.19](https://arxiv.org/pdf/1005.4206#page=19) gives the
corresponding rational-field criterion and corrected trace formula.

For a least positive real period Omega_plus of the specified minimal
differential, the required value is

    c5_plus(E)=Omega_plus(E)^(-5) L(bar(psi_E)^5,5).

It is a rational number. It is not L''(E,1)/2. The missing condition is
v5(c5_plus(E))=2, with v5(5)=1. The theorem supplies the lower bound two;
it does not supply the nonzero residue needed to prove equality.

## Local and theorem admissions

The CM field is K=Q(i), with maximal order Z[i] and four roots of unity.
The action i:(x,y)↦(−x,iy) is fixed. The prime five splits as
(2+i)(2−i). Direct enumeration gives #E(F5)=8, so a5=−2, the curve is
ordinary at five, and its reduction has order prime to five. The
discriminant is nonzero modulo five. The factors 6 and 4 are units at
five. Rank parity is 2≡2 modulo two, using the accepted exact rank proofs.

The comparison factor alpha for the period convention used below has
norm two, hence is a five-adic unit. The CM conductor also has norm prime
to five. These discharge the prime/unit restrictions in CLS I, Theorem
2.2. That theorem imposes no residual-surjectivity hypothesis; no
surjectivity assertion from a non-CM theorem is being imported here.

The theorem's conclusion over K implies the rational-field conclusion by
restriction/corestriction: the extension degree two is invertible on a
5-primary group. Its argument treats both primes over five. Equivalently,
the rational-field formulation in CLS II applies after these admissions.

## Conductor discrepancy and the isogenous model

A literal substitution D=1156 into the printed conductor formula of
[CLS I, Lemma 3.2, PDF p.13](https://arxiv.org/pdf/0901.3832#page=13) would
give 136Z[i]. This conflicts with the compatible value below and the
accepted conductor 18496=4·68². This discrepancy is retained openly; the
even-D substitution is not used as an admitted formula in this attempt.
No general correction to that printed lemma is claimed.

Instead use the explicit rational degree-two isogeny

    E': y²=x³+289x  ->  E: y²=x³−1156x,
    (x,y) -> (x+289/x, y(1−289/x²)).                    (1)

The program verifies the target equation as a Laurent-polynomial
identity, and verifies that (1) pulls dx/(2y) on E back to dx/(2y) on E'.
The usual projective extension sends O and (0,0) to O. This is the
standard quotient with the rational two-point kernel; it has degree two.

Over K there is also an isomorphism E'→E given by
(x,y)↦(u²x,u³y), where u=1+i and u⁴=−4. Both maps commute with the
chosen action of Z[i]. Thus their compatible K-adic Tate modules have
the same Hecke character, not an unexplained quadratic or quartic twist.
In particular the primitive Hecke L-functions of the fifth powers agree.

E' has D'=−289, which is odd, fourth-power-free, and 3 modulo four.
Applying the odd-D case of CLS I, Lemma 3.2 gives

    f=68Z[i], f1=f/(1+i)=34(1−i)Z[i].

The generator 68 has norm 4624, consistent with 4N(f)=18496. The finite
Gaussian-unit enumeration gives phi(68Z[i])=2048. E and E' are
K-isomorphic, so this Hecke conductor is common to them. The rational
isogeny also preserves their algebraic/analytic ranks. Its degree is a
five-adic unit, so it induces an isomorphism of their 5-primary Sha
groups; applying the criterion to E' would therefore suffice.

## Period and critical-value scaling

All real periods in this section are the **least positive real period**,
not the integral over all real components. E' is minimal over Q: its
discriminant valuations at 2 and 17 are both six, precluding a decrease
by twelve. E's minimal differential is the one already certified in the
preceding experiment. Changes needed for a model over K are supported at
two, so their differential factors are units at five; they cannot change
the valuation criterion.

The complex isomorphism above gives L_E'=u L_E for these displayed
differentials. Since L_E=Omega_plus(E)Z[i], the least positive real
element of u L_E is 2Omega_plus(E). Hence

    Omega_plus(E')=2Omega_plus(E),
    c5_plus(E)=32 c5_plus(E').                         (2)

For the trace computation choose the lattice generator
Omega_infinity(E')=Omega_plus(E')/(1+i), exactly the negative-D convention
of CLS II. Then alpha(E')=1+i and beta=f alpha/(1+i)=68. This generator
differs by a Gaussian unit from u Omega_plus(E); the lattice is identical.
Equation (2) uses the same Hecke character and explicitly named real
periods. No factor is inferred from numerical proximity of L-values.

## The exact calculation still required

Put

    rho = positive sqrt(wp(Omega_plus(E')/68, L_E')).

The argument equals Omega_infinity/f1. [CLS II, Lemma 4.4 and equations
(74), (77), PDF pp.15,19](https://arxiv.org/pdf/1005.4206#page=15) identify
K(rho) with the ray class field H_f1, of degree phi(f)/8=256 over K.
Only this stated field and primitive division-point choice is admitted;
an arbitrary degree-256 factor would require an identification proof.

For E', W²=wp, V²=W⁴−D', W'=V and V'=2W³. Differentiating twice more
gives, with D'=−289,

    V'''=24W⁵+3468W.

The corrected trace formula therefore specializes to

    T = Trace_(H_f1/K)(2rho⁵+289rho),
    c5_plus(E') = ±T/(2·68⁵),
    c5_plus(E)  = ±16T/68⁵.                           (3)

The sign is immaterial for the five-adic valuation. The multiplying
factor 16/68⁵ is a five-adic unit, so the desired assertion is exactly

    T mod125 is one of 25,50,75,100.                   (4)

The trace is rational by (3). It is integral at five: the division point
has order prime to five on a curve with good reduction, so its affine
coordinates are integral there, as is their square root rho. Thus (4)
is a well-typed residue question. This local integrality does not
determine its residue.

Let a1,...,a5 be the first five coefficients of the correct monic minimal
polynomial X^256+a1 X^255+... of rho. The calculation can be reduced to
Newton sums:

    s1=−a1,
    sm=−(a1 s_(m−1)+...+a_(m−1)s1+m am), 2≤m≤5,
    T=2s5+289s1.

Consequently one does not need a high-power L-series approximation or
all 256 trace powers. One needs a **certified construction of those five
coefficients modulo125**, or an equivalent trace algebra with its
primitive CM division orbit identified. No such polynomial or trace
algebra has been constructed in this attempt. The cited papers' supplied
examples concern other D values; their displayed residues cannot fill
this port.

CLS II explicitly corrects a spurious factor four in the earlier paper's
trace formulas. Formula (3) uses the corrected version. Four is a unit
at five, so that historical normalization error would not change v5,
but it would change a claimed exact critical value and is not ignored.

## Stopping point and reproduction

Four targeted search queries and direct reads of both primary papers
were completed. No correct rho polynomial or ready implementation for
this curve was located in that bounded search. This is a missing exact
field/trace computation, not a failed valuation test, a proof of an
exceptional prime, or a claim that the calculation is impossible.

The next concrete step is to construct the primitive f1-division trace
algebra, certify its CM orbit, and compute the above Newton combination
modulo125. A field definition without that orbit certificate, or a
floating-point rational recognition without a justified denominator
bound, would not close (4). No larger software system was installed and
no unbounded factorization or multi-prime campaign was started.

Run the completed admission certificate from this directory:

    python -I -B work/odd_prime.py --output evidence/odd_prime.json

The executable is standard-library-only. It returns OPEN and leaves the
critical trace and valuation null. Its exact finite checks establish no
new odd-primary Sha result. Even a future successful p=5 calculation
would prove only that primary component vanishes; the remaining primes
and the full complex BSD identity would still require their own proofs.
