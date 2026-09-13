# E34: the CM theorem route and its exact remaining port

Date: 2026-09-12. Status: **OPEN for the real leading coefficient**.

**The 5-primary result is already complete:**
`Sha(E/Q)[5^infinity]=0` was proved in
[bsd-trace-02](../../bsd-trace-02/TRACE_CALCULATION.md). This note's initial
version mistakenly presented that completed CLS trace route as a next
unknown. The history-aware correction below retains its existing proof;
the new contribution here is the literature applicability audit and the
explicit theta specialization. Neither supplies the real leading-coefficient
comparison `L''(E,1)/(2 Omega Reg)`.

## Contract and normalization

The input is `E/Q: y^2=x^3-1156x`, with `n=34`, CM by `Z[i]`,
conductor `18496=136^2`, rank two, and supplied integral basis
`P=(-2,48), Q=(-16,120)`. The initial delegation's number `36992`
was explicitly corrected by the parent; it is not a competing computed
conductor. The inherited target uses `alpha=pi/68`, the full logarithmic
x-height regulator, and `Omega` over both real components. These remain
the conventions of [the target](../../bsd-identity-01/EXPLICIT_IDENTITY_TARGET.md).

Carriers retained separately are the real central derivative, the real
Mordell-Weil Gram determinant, algebraic higher Hecke values, p-adic
valuations, and the actual cohomological Sha. A theorem may transport only
the observations it states. Exact valuation conditions enable the Sha
readout below; they do not enable a real central-value comparison. No
inverse from a valuation to its rational input is asserted. The unresolved
central-comparison fiber is OPEN, not NONE.

## A rank-unrestricted CM theorem that does apply

Let `K=Q(i)`, let `psi` be E's CM Hecke character, and let `omega_r`
be the least positive real period, so `omega_r=Omega/2` for our model.
For a good split prime `p`, put

\[
C_p=\omega_r^{-p}L(\overline\psi^{\,p},p).
\]

Coates--Liang--Sujatha I, Theorems 2.1--2.2, give rationality and
valuation bounds. The hypotheses are good reduction, splitting in the
CM field, primality to the roots-of-unity order and the period multiplier,
and equal analytic/algebraic rank parity. With `g=rank E(Q)`, a valuation
below `g+2` implies p-primary finiteness. Valuation `g`, together with
`p` prime to 6 and to `#E(F_p)`, implies p-primary triviality over K,
and hence over Q. These statements concern the displayed higher Hecke
value, not a central derivative.
[CLS I, Theorems 2.1--2.2, pp. 4--5](https://arxiv.org/pdf/0901.3832#page=4).

For E34, every prime `p=1 mod 4`, `p!=17`, meets the field, reduction,
roots-of-unity, and period conditions: `w_K=4`; the square lattice has
period multiplier 1 in the displayed positive-D model. A change to a
minimal model over K can affect the differential only at the bad primes,
which are units at these p. The supplied ranks give even parity. Thus
the exact specialized consequences are

\[
C_p\in\mathbb Q_{>0},\qquad v_p(C_p)\ge2,
\]
\[
v_p(C_p)\le3\Longrightarrow\#\Sha(E/\mathbb Q)[p^\infty]<\infty,
\qquad
v_p(C_p)=2\Longrightarrow\Sha(E/\mathbb Q)[p^\infty]=0.
\tag{CM34}
\]

The remaining nonanomalous condition holds here. Full rational 2-torsion
injects at every odd good prime, so `4` divides `#E(F_p)`. Hasse's bound
gives `#E(F_p)<2p` for `p>=7`, excluding a positive multiple of p since
`#E(F_p)=p` would be odd. At `p=5`, direct enumeration gives 8.
Restriction followed by corestriction is multiplication by 2, so the
restriction on odd-primary Sha from Q to K is injective.

The distinction between rank over Q and rank over K is exact:
the (-1)-twist is the same equation; therefore
`L(E/K,s)=L(E/Q,s)^2`, `rank_Z E(K)=4`, and
`rank_Z[i] E(K)=2`. This is why the CM inequality has lower bound two,
whereas a simple-Hecke-zero theorem remains unavailable.

## The completed trace result and the equivalent coordinates

The existing
[trace calculation](../../bsd-trace-02/TRACE_CALCULATION.md),
[CM orbit proof](../../bsd-trace-02/TRACE_FORMULA_AUDIT.md), and
[claim ledger](../../bsd-trace-02/CLAIM_LEDGER.json) establish
`v_5(C_5)=2` and therefore `Sha(E/Q)[5^infinity]=0`. They supersede the
earlier OPEN status of the admission-only
[odd-prime attempt](../../bsd-identity-01/ODD_PRIME_ATTEMPT.md).

Their auxiliary model is `E': y^2=x^3+289x`, with `f=68`,
`f1=34(1-i)`, and a degree-256 ray field `H_f1/K`. For the specified
period-defined root `rho'`, they use

\[
T=\operatorname{Tr}_{H_{f1}/K}(2\rho'^5+289\rho'),\qquad
C_5(E)=\pm16T/68^5.
\]

The completed orbit calculation obtains a Gaussian-unit multiple
`S=100 mod125`. Its nonzero quotient `S/25=4 mod5` proves valuation
two. The written orbit argument covers all 512 CM point occurrences,
the twofold fibers of `r(P)=Y/(2X)`, both split primes above five, and
the primitive CM annihilator. The separate reassembly records the same
residue and valuation; the character-weighted construction gives 25
modulo 125 up to sign. These are attributed existing proofs and
computations, not fresh trace runs in this audit.
[Stored trace evidence](../../bsd-trace-02/evidence/trace125.json),
[independent reassembly](../../bsd-trace-02/evidence/trace_formula_reassembly.json).

This audit independently repeated only these small point counts:

| p | #E(F_p) | a_p | Reduction |
|---|---:|---:|---|
| 5 | 8 | -2 | good ordinary |
| 13 | 20 | -6 | good ordinary |
| 29 | 40 | -10 | good ordinary |
| 37 | 40 | -2 | good ordinary |

The replay used only `1+sum(1 for x in range(p) for y in range(p)
if (y*y-x*x*x+1156*x)%p==0)`; it used no curve database.

CLS II gives the corrected full division-field trace formula before
equation (77). Let `f` generate the Hecke conductor, `F=K(E[f])`,
`Lambda` be the period lattice, and `V=Phi(omega_r/f,Lambda)`. Then

\[
C_p=-\frac{f^{-p}}{(p-1)!}
\operatorname{Tr}_{F/K}\!\left(\wp^{(p-2)}(\omega_r/f,\Lambda)\right).
\tag{T}
\]

The paper explicitly corrects a spurious roots-of-unity factor in I's
equations (24) and (53). Its smaller-field Lemmas 4.1 and 4.4 require an
odd prime divisor of D, which `D=1156` has. The stronger odd-exponent
condition in I's Lemma 3.3 is a different lemma and must not be imported
into this route. Its example `D=-34` means `x^3+34x`, not our curve.
No reported example value was used.
[CLS II, corrected trace formula and correction notice, p. 19](https://arxiv.org/pdf/1005.4206#page=19),
[smaller-field lemma, II p. 15](https://arxiv.org/pdf/1005.4206#page=15).

For this even congruent-number input the CM character is defined modulo
`2n Z[i]=68 Z[i]`; this agrees with the conductor norm
`18496/|disc Q(i)|=4624`. In particular, using `136 Z[i]` would
conflict with the retained conductor. The simplified `4 rad(D)` formula
printed in CLS I Lemma 3.2 cannot be substituted blindly at `D=1156`.
The congruent-number character construction provides that same modulus.
[Guo--Ye--Yin, section 2](https://arxiv.org/pdf/2505.13133#page=3).
The existing trace proof had already resolved this discrepancy using the
K-isomorphic odd auxiliary model `D'=-289`; no conductor issue in its
proof was found here.

At `p=5`, the Weierstrass equations give `wp=x`, `wp'=2y`,
and `wp'''=12 wp wp'=24xy`. Thus the general corrected trace formula
also admits the direct-model expression

\[
\boxed{C_5=-68^{-5}\operatorname{Tr}_{K(E[68])/K}(x(V)y(V)).}
\tag{T5}
\]

This is an alternative expression, not a missing p=5 computation or an
improvement to the old orbit proof. In the direct model put
`rho^2=wp(omega_r/f1)`, with the square-root branch of CLS II Lemma 4.4.
The field degree is the same as in the completed calculation:

\[
[K(\rho):K]=\varphi((68))/8=(8\cdot16\cdot16)/8=256.
\]

In the paper's differential recurrence, `W'=V`, `V'=2W^3`, and
`V^2=W^4-D`. Therefore `A_1(X)=24X^5-12DX`, and equation (77)
becomes

\[
C_5=\pm\left(\frac{68}{1+i}\right)^{-5}
\left[\operatorname{Tr}_{K(\rho)/K}(\rho^5)
-578\operatorname{Tr}_{K(\rho)/K}(\rho)\right].
\tag{T5-small}
\]

Here is the exact coordinate comparison with that completed trace.
Set `v=1-i`. The prior period proof gives
`Lambda_E'=v Lambda_E` and `Omega_infinity(E')=v omega_r(E)`.
The scaling law for the Weierstrass function yields
`rho=+/-v rho'`. Since `v^4=-4`, the bracket in (T5-small) is

\[
\operatorname{Tr}(\rho^5)-578\operatorname{Tr}(\rho)
=\mp2v\operatorname{Tr}(2\rho'^5+289\rho')=\mp2vT.
\]

Multiplication by `(68/(1+i))^-5` therefore recovers
`C_5(E)=+/-16T/68^5`, exactly the existing normalization. The same
field, conductor, trace degree, and valuation receiver are retained.
The direct expression supplies neither a smaller field nor a new orbit
certificate. The existing proof already constructs the relevant orbit
without needing a characteristic-zero defining polynomial, and already
checks the first five polynomial coefficients modulo 125 through Newton
identities. The earlier suggestion to construct such a polynomial was
unnecessary for its completed readout.

What remains uncomputed in that lane is the **distinguished signed
rational value** of T or C5, not its valuation or the 5-primary result.
No such signed value is needed for the theorem already applied.

## Recent central and full-BSD results checked

**A concrete additional exact relation.** Guo--Ye--Yin (2025),
Theorem 1.1, applies because `34=2*17` and `17=1 mod 4`. Taking
`b=38` gives `b^2+1=5*17^2` and hence

\[
L(E,1)=0\quad\Longleftrightarrow\quad
\theta_{(\cdot/17)}\!\left(\frac{327+i}{578}\right)=0.
\]

The supplied analytic rank therefore proves this explicit theta zero.
The theorem specializes at `s=1`; differentiating its theta variable
does not supply an identity for differentiation in the L-function's
s-variable.
[Theorem 1.1](https://arxiv.org/pdf/2505.13133#page=2).

| Primary result | Actual scope and E34 consequence |
|---|---|
| Burungale--Flach, Theorem 1.1 and Corollaries 1--2 | Full CM BSD, including previously troublesome primes, assumes nonzero central Hecke value. E34's value is zero. Neither Q nor CM base change meets this hypothesis. [Full text](https://arxiv.org/pdf/2206.09874#page=2) |
| Castella, published 2025, Theorem A | Assumes a **simple Hecke zero**, `p` prime to `6h_K` and split in K, conductor prime to p, and the stated exact different-divisibility condition. E34 has Hecke order two. Over K the Hasse--Weil order is four. No choice of p fixes this failed rank hypothesis. [Theorem A and Remark 1.1.1](https://web.math.ucsb.edu/~castella/Katz.pdf#page=2) |
| Tian--Yuan--Zhang, Theorem 1.1 and Corollary 1.3 | In the even-sign residue classes, the integral invariant is built from `L(E_n,1)`; their invariant is zero for higher analytic rank. The full-BSD criterion requires rank zero and trivial 2-primary Sha. E34 has rank two. An integral zero here gives no denominator bound for the second derivative quotient. [Definitions and results](https://web.math.princeton.edu/~shouwu/publications/cn.pdf#page=2) |
| Xu, September 2026 preprint, Theorems 1.1 and 2.6 | Relates central representation defects to the Pfaffian/radical of the pure 2-Selmer Cassels pairing. At nonzero defect the conclusions identify rank-zero Sha; its proof treats zero central value by zero defect and zero Pfaffian. Its `E_{34q}` family has another prime q and is not E34. No rank-two leading coefficient appears. [Statements](https://arxiv.org/pdf/2609.03238#page=3), [zero-value proof branch](https://arxiv.org/pdf/2609.03238#page=9) |
| Stein--Wuthrich, Algorithms 11.1 and Theorem 1.1 | The published article explicitly imposes non-CM from section 3 onward; its large computation also requires surjective mod-p image. Those outputs cannot be transferred to E34. The CM route above uses elliptic units and the CM main conjecture instead. [Scope statement](https://wstein.org/papers/mcom2649-iwasawa-alg.pdf#page=5) |

The recent results were inspected at their displayed hypotheses, not
inferred from titles containing “CM”, “full BSD”, or a rank-two number
over a different field. The search also covered CM p-parts, higher-rank
congruent-number results, and explicit Hecke-value formulas. This is a
bounded literature audit, not proof that no stronger theorem exists.

## The exact unresolved port

The available CM comparison gives algebraicity for `C_p`, whose Hecke
character and evaluation point both depend on p. It does not give
algebraicity for

\[
Q_E=\frac{L''(E,1)/2}{\Omega\operatorname{Reg}}.
\]

Even exact evaluation of every checked `C_p` would leave the archimedean
comparison missing. The existing
[generalized Perrin--Riou bridge audit](../../bsd-identity-01/EXACT_IDENTITY_THEOREMS.md)
states that missing comparison explicitly. One needs a proved central
derived-class/height identity, or a theorem putting this particular real
quotient in an effective discrete set. The CM weight-p trace does not
become such a theorem by analytic continuation or by sending p toward 1.

Evidence grades: cited published theorems and identified preprint
statements; written E34 specialization and coordinate comparison; four
finite point-count checks. **Established prior arithmetic:** the
2-primary and 5-primary Sha groups vanish, with the latter proved by the
completed trace lane. The CLS criterion is a repeated theorem route,
not a new arithmetic result of this audit. **New here:** the checked
literature boundaries and explicit theta-zero specialization.
**Still OPEN:** the real leading-coefficient comparison, the other
primary groups, total-Sha finiteness/order, and the distinguished signed
rational fifth-power Hecke value. The p=5 valuation and its theorem
application are complete. No old file was edited and no trace experiment
was rerun.
