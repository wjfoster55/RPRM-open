# Independent analytic theorem audit: E5

This audit confirms B01 for the supplied curve over Q with ordered Weierstrass
coefficients `[0,0,0,-25,0]`. It supplies the analytic premises for B02 and D01.
The analytic branch uses no arithmetic-rank result, database rank, BSD formula,
archived PASS, or backend zero forced from a rank. The cited theorems remain
`THEOREM_CITED`; their applications and the estimates below are written proofs,
not formal proofs. Source pages and formulas were opened on 12 September 2026.

The carrier is this fixed nonsingular rational elliptic curve, its correctly
normalized entire L-function, and real positive E1 arguments. The supplied ports
are the equation and established elliptic-curve theorems. The requested readouts
are the exact central zero and a certified bound on its derivative. The operation
is forward specialization, Mellin continuation, and enclosure. It does not invert
the L-function to recover a curve or enumerate a completion fiber. The receiver
retains curve identity, normalization, signed coefficients, and the entire omitted
tail. A changed equation or a missing tail proof disables the affected conclusion.

## 1. Exact model, conductor, sign and bad Euler factors

Write the supplied coordinates as `(x,y)=(5u,25v)`. Direct substitution gives

    625v^2 = 125u^3 - 125u, hence 5v^2 = u^3-u.

The inverse is `(u,v)=(x/5,y/25)` and the map fixes the point at infinity. Thus
this is a rational isomorphism to Elkies's E_D with D=5. The integer 5 is nonzero,
positive, squarefree, odd and congruent to 5 modulo 8. Elkies §1.1, printed pp.1–2,
defines this family and gives sign −1 for squarefree |D| congruent to 5,6,7 mod8;
§2, printed p.4, gives conductor 32D² for odd D under its squarefree hypothesis.
The specialization is therefore N=32·25=800 and epsilon=−1. These are theorem
inputs with checked hypotheses, not conclusions of finite point counting. The
paper's point-construction/rank theorem is not needed. [Elkies](https://arxiv.org/pdf/math/0208056)

Independently, the integral model has c4=1200, c6=0 and
Delta=−16(4(−25)^3)=1,000,000=2^6·5^6. A rational Weierstrass change multiplies
Delta by a twelfth power. In any Q_p-isomorphic integral equation the discriminant
valuation therefore differs by an integer multiple of 12 and remains nonnegative.
The valuations 6,6, and 0 cannot decrease. This proves minimality at every prime,
including 2; it does not presume that being written in short form proves
minimality. The transformation/discriminant formulas used here are in Cremona
§3.1, printed pp.62–63, equations (3.1.2)–(3.1.3).
[Cremona, chapter 3](https://johncremona.github.io/book/fulltext/chapter3.pdf)

All p other than 2,5 have nonsingular reduction because Delta is a p-adic unit.
At p=5 the reduction is y²=x³, a cusp. At p=2 the equation is y²=x³+x.
Set X=x+1; then y²=X³+X². Set Z=y+X; then Z²=X³. These invertible changes over
F2 exhibit its cusp. The point at infinity remains nonsingular. A cuspidal
reduction of a minimal model is additive (Milne II §3, printed p.59). For additive
reduction the local polynomial is P_p(T)=1, while at a good prime it is
P_p(T)=1−a_pT+pT², with a_p=p+1−#E(F_p); L is the product of P_p(p^(−s))^(−1)
(Milne IV §10, printed p.163). [Milne](https://www.jmilne.org/math/Books/ectext6.pdf)

Consequently the factors at 2 and 5 are exactly 1, a_(2^k)=a_(5^k)=0 for k≥1,
and a_n=0 when 2 or 5 divides n. A count on a singular cubic alone would not
justify the good-prime quadratic factor. No conductor exponent is inferred from
the simple cusp count: the conductor comes from the applicable Elkies formula.

## 2. Cited modularity and normalization; independent Mellin derivation

The projective cubic has a rational point at infinity and nonzero discriminant,
so it is an elliptic curve over Q. Breuil–Conrad–Diamond–Taylor, Theorem A,
Introduction p.1, applies without a semistability restriction. The equivalence
of modularity with L(E,s)=L(f,s) for a weight-two form at level N(E) is stated in
the same Introduction, pp.2–3. We use the associated normalized rational newform
f(z)=sum_(n≥1) a_n exp(2*pi*i*n*z), with a_1=1.
[BCDT](https://www.math.u-psud.fr/~breuil/PUBLICATIONS/STW.pdf)

Cremona §2.8, printed p.29, equations (2.8.5)–(2.8.6), states the normalization
and Fricke transformation. His Fricke eigenvalue, call it eta, is the NEGATIVE
of this audit's functional-equation sign epsilon: eta=−epsilon=+1. Hence
f(−1/(Nz))=eta*N*z²*f(z). With g(u)=f(iu/sqrt(N)), this is
g(1/u)=−eta*u²*g(u)=epsilon*u²*g(u). This explicit minus sign prevents confusing
the Fricke eigenvalue with the root number.
[Cremona, chapter 2](https://johncremona.github.io/book/fulltext/chapter2.pdf)

Put alpha=2*pi/sqrt(800)=pi/(10*sqrt(2))>0. In a right half-plane, integrating
each exponential after the substitution t=alpha*n*u gives

    Lambda(s) := alpha^(−s)*Gamma(s)*L(E,s)
              = integral_0^infinity g(u)*u^(s−1) du.

Section 3 below gives an all-n coefficient bound. In particular, on u≥1,

    |g(u)| <= sum 2n*exp(−alpha*n*u)
            = 2exp(−alpha*u)/(1−exp(−alpha*u))².

This decays exponentially. The Fricke transformation supplies decay at zero
as well. For the elementary initial interchange it suffices to take Re(s)>2;
the sharper divisor bound gives the usual Re(s)>3/2 convergence half-plane.
Substitute u=1/v in the integral over (0,1), retaining du=−v^(−2)dv:

    Lambda(s) = integral_1^infinity
                  g(u)*(u^(s−1)+epsilon*u^(1−s)) du.                 (1)

On any compact set of s, the integrand and every s derivative are dominated by
an exponential times a fixed power of u and log(u). Thus (1) is entire, allows
differentiation under the integral, and agrees with the initial Mellin function.
It supplies analytic continuation; no center substitution into a divergent
Euler product occurs. Replacing s by 2−s proves the functional equation.

For epsilon=−1, (1) vanishes exactly at s=1. Since alpha^(−1)*Gamma(1)=1/alpha
is finite and nonzero, L(E,1)=0. It is Lambda(1+t) that is odd in t; raw L need
not be odd. Differentiating (1) at 1 gives

    Lambda'(1) = 2 integral_1^infinity g(u)*log(u) du.

Absolute exponential domination justifies the coefficient interchange. For
b=alpha*n>0, integration by parts has zero boundary terms and gives

    integral_1^infinity exp(−bu)*log(u) du
      = (1/b)*integral_1^infinity exp(−bu)/u du = E1(b)/b.

Here E1(x)=integral_x^infinity exp(−t)/t dt, for real x>0, matching DLMF
6.2.1 on the positive real branch. [NIST DLMF](https://dlmf.nist.gov/6.2#E1)
In differentiating Lambda=alpha^(−s)Gamma(s)L, the term proportional to L(1)
vanishes. Thus Lambda'(1)=L'(E,1)/alpha and

    L'(E,1) = 2 sum_(n≥1) (a_n/n) E1(alpha*n).                     (2)

As a direct primary-source cross-check, Cremona Proposition 2.13.1, printed
p.43 (derivation p.42), has hypotheses newform, order at least r, and Fricke
eigenvalue eta=(−1)^(r−1). Set r=1: exact vanishing was proved above and eta=+1;
his G_1(x)=integral_1^infinity exp(−xy)dy/y equals E1(x). No premise that the
zero is already simple is needed. Sage's official `deriv_at1` documentation
also gives (2) and explicitly requires L(E,1)=0. We checked that warning and
formula, but did not run Sage or borrow its numerical error estimate. Cohen
§7.5.3 is credited there; Cohen's book was not independently opened here.
[Sage reference](https://doc.sagemath.org/html/en/reference/arithmetic_curves/sage/schemes/elliptic_curves/lseries_ell.html#sage.schemes.elliptic_curves.lseries_ell.Lseries_ell.deriv_at1)

## 3. Every premise of the rational nonvanishing bound

The independent B02 computation in `work/analytic_check.py`, freshly recorded
in `evidence/analytic.json`, confirms that the nonzero coefficients through 20
are a_1=1, a_9=−3, a_13=−6, a_17=−2. This audit read both that implementation
and its fresh coefficient/prime-count record. Odd-prime counts use Euler's
criterion, then good-prime power recurrences and coprime multiplicativity;
the bad factors at 2,5 are correctly separated. The following written estimates
account for every infinite-sum premise attached to that independently checked head.

1. **All good primes.** Hasse's theorem for elliptic E/F_q gives
   |q+1−#E(F_q)|≤2sqrt(q). The source is Sutherland, MIT 18.783 Fall 2023,
   Lecture 7, §7.2, Theorem 7.3, printed pp.1–2 (statement p.1 and proof continuing
   p.2). It applies for each p other than 2,5, whose reductions were proved
   nonsingular above. [Hasse theorem source](https://math.mit.edu/classes/18.783/2023/LectureNotes7.pdf)

2. **All powers, then all n.** If beta_p,gamma_p are the roots of
   X²−a_pX+p, Hasse implies they are conjugate roots of modulus sqrt(p),
   including the repeated-root endpoint. Expanding
   1/[(1−beta_pT)(1−gamma_pT)] gives
   a_(p^k)=sum_(j=0)^k beta_p^j*gamma_p^(k−j), so
   |a_(p^k)|≤(k+1)p^(k/2). The Euler product makes coefficients multiplicative
   for coprime indices. If n is prime to 10 this yields |a_n|≤d(n)sqrt(n);
   otherwise a_n=0 and the same inequality holds. Pair each divisor below
   sqrt(n) with its complementary divisor above it, counting the central one
   only once. This proves d(n)≤2sqrt(n), hence |a_n|≤2n for EVERY n≥1.
   This is a written all-n derivation from Hasse and the local factors, not
   a finite test of the first several coefficients.

3. **Rational bounds on alpha.** The task's Machin method is valid, but an
   independent shorter route suffices. The alternating arctan expansion at 1
   gives pi>4 sum_(k=0)^7 (−1)^k/(2k+1)>3 and
   pi<4(1−1/3+1/5)=52/15<7/2. The alternating remainder justifies both strict
   bounds. Squaring gives 7/5<sqrt(2)<3/2. Therefore
   1/5=3/(10·3/2)<alpha<(7/2)/(10·7/5)=1/4.
   All endpoints and comparisons here are rational.

4. **A uniform geometric envelope.** For alpha>0, exp(alpha)>1+alpha>6/5.
   Thus exp(−alpha)<q=5/6, with 0<q<1. For x>0, positivity of the defining
   integral and 1/t≤1/x for t≥x give 0<E1(x)≤exp(−x)/x. Combining these,
   E1(alpha*n)<5q^n/n for every positive integer n.

5. **Positive first term.** The factorial series gives e<3: for k≥2,
   k!≥2^(k−1), with strict inequality for k≥3. Also
   log(2)=2 sum_(j≥0) (1/3)^(2j+1)/(2j+1)>2/3, obtained by integrating the
   geometric series for 1/(1−t²). On [1/4,1], exp(−t)≥exp(−1)>1/3.
   Since alpha<1/4 and all omitted integrals are positive,
   2E1(alpha)>(2/3)log(4)>8/9.

6. **Every retained negative term.** For a_n<0,
   |2(a_n/n)E1(alpha*n)|<10|a_n|q^n/n². The head's three negative terms
   therefore have total magnitude less than

       Bneg = 10(3q^9/9² + 6q^13/13² + 2q^17/17²)
            = 22338243056640625/206678743485087744.

7. **The entire unopened tail.** Formula (2) and the ALL-n bound give

       |2 sum_(n≥21) (a_n/n)E1(alpha*n)|
          <=4 sum_(n≥21) E1(alpha*n)
          <20 sum_(n≥21) q^n/n
          <=(20/21)sum_(n≥21)q^n=(120/21)q^21
          =2384185791015625/19194831810330624.

   This covers every n≥21 regardless of sign or vanishing pattern. For any
   cutoff M≥0 the same proof gives tail <20q^(M+1)/((M+1)(1−q)); sharper
   enclosures of alpha or exp(−alpha) may reduce it with their own proofs.

8. **Exact assembly and zero order.** Subtracting these two negative budgets
   from 8/9 gives

       R = 615556405007957768183/937494780448358006784 > 13/20.

   The finite rational comparisons were independently executed by B02; this
   audit establishes why that computation bounds the analytic function. The
   fresh B02 record reconstructs the stated R and positive margin exactly.
   Thus (2) proves L'(E,1)>R>0. Since L is
   holomorphic and L(1)=0, its first nonzero Taylor term is linear, so its
   vanishing order is exactly one. The Euler coefficient a_1=1 is different
   from the central Taylor coefficient c_1=L'(E,1).

No missing analytic premise was found. Modularity, local-factor conventions,
the conductor/sign rule, Hasse, and the modular-form correspondence are cited
standard mathematics. The specialization, minimality/cusp computations,
normalization, central zero, termwise integral argument, and all-term bound
are explicit written derivations. B02's fresh finite coefficient and
rational-arithmetic evidence has been reconciled here; D01 supplies its own
stronger error ledger in `DERIVATIVE_INTERVAL.json`.

## 4. K02: changed-model certificate rejection

Run from the experiment root:

    python -I -B work/model_binding_check.py --output evidence/model_binding.json

The script reads the actual supplied `TEST_PLAN.json` curve, validates its
integral Weierstrass shape and nonsingularity, and accepts its equality to the
E5 certificate's bound field and ordered coefficients. It then makes a
disposable real mutation a4=−36 and passes that mutated model through the same
identity guard. The guard rejects reuse of E5's conductor/sign certificate.
The receipt retains both models, their recomputed invariants and the changed
polynomial. Under the E5 substitution x=5u,y=25v, the defining polynomial's
u coefficient changes from 125 to 180, a difference 55u. Both j-invariants
are 1728, which illustrates why j alone would be an insufficient identity key.

This checks exact model binding; it is not a general isomorphism classifier.
No changed-curve rank, conductor, sign or analytic value is inferred. The
script's input digest records bytes, while the model tuple and actual
polynomial mismatch supply the semantic rejection. A rejected certificate is
the successful outcome of this control, not a program failure.
