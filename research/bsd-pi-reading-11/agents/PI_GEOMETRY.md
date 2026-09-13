# E34: frozen candidates for the pi and height-geometry audit

Date: 2026-09-12. This bounded agent report concerns E34: y^2=x^3-1156x, the fixed points P=(-2,48), Q=(-16,120), and the full logarithmic canonical height H=lim 4^(-k) log H_x(2^k R). It changes no earlier report. The parent task handles the exact digit-stream and rational-pi interval tests.

## Candidate freeze, before dispositions

These are typed audit candidates, not an attribution of their precise mathematical wording to William. The user's proposed reading of `0340` as “pi zipped up” remains a live motivation for specifying a map.

| ID | Frozen claim or question | Supplied context and missing port | Distinguishing test |
|---|---|---|---|
| PG1 | A stated pi/carry operation explains a feature of d(P,Q)=sqrt(H(P-Q)) for this exact fixed basis and height convention. | E34, P, Q, natural logarithm, full height, and decimal encoding supplied; the exact pi-to-height map and its predictive receiver remain required. | Prove a source-derived relation or test a frozen prediction beyond the digits used to choose it. Basis changes transport this candidate rather than automatically refute it. |
| PG2 | The same bare distance or its decimal carry threshold is an invariant pi-closure readout of the E34 rational-point lattice under every integral basis choice. | Integral basis class, exact height metric, fixed decimal display; no extra basis tag allowed. | Reverse Q or shear Q to Q+nP while retaining the lattice. |
| PG3 | Pi enters the independently defined E34 L-function through its Fourier/Mellin normalization, with alpha=pi/68. | Minimal E34 model, conductor, modular form, full L-function, and specified completion. | Derive alpha from 2pi/sqrt(N), and check the lower-vanishing premise when converting the second coefficient. |
| PG4 | The connected period for dx/(2y) is Gamma(1/4)^2/(2 sqrt(pi) sqrt(34)). | Exact differential and one real component supplied. This formula is a factor-check candidate, not an accepted premise. | Derive the integral with endpoints and compare one-component versus all-component normalization. |
| PG5 | There is an exact, independently defined pi relation for E34's real period and an arithmetic-geometric-mean iteration. | Positive real integrals and the AGM carrier; minimal differential retained. | Derive its scale from the cubic integral and the elliptic-integral AGM identity, keeping it distinct from Mordell-Weil height geometry. |

All candidate dispositions are initially OPEN in this freeze. No exhaustive set of all RPRM interpretations is asserted.

## Contract and retained evidence

The height carrier is E(Q)/torsion with its full canonical quadratic form, and its real vector-space extension when discussing Gram matrices. Equality modulo torsion differs from equality of rational point occurrences. The supplied points, basis, natural logarithm, full-height convention, and decimal radix are retained. The published height theorem and the earlier rational interval proof are dependencies; this audit does not rerun or replace them.

The analytic carriers are the positive real period integral for omega=dx/(2y), the complex modular L-function, and positive ordered real pairs for AGM. These are explicitly separate from the rational-point group. The receiver is a normalization-correct relation that could inform the BSD comparison. No inverse from a height, period, L-value, or decimal word to a rational point is claimed. An unspecified decoder remains OPEN rather than having an empty fiber.

The inherited enclosure is

\[
2.0339867006\le d(P,Q)\le2.0340237084.
\]

Its rigorous derivation and group identity P-Q=(162,-2016) are in [DISTANCE_AND_SEAM.md](../../closure-seam-09/DISTANCE_AND_SEAM.md), sections 4–5. This agent makes no claim that this enclosure by itself certifies a particular unrounded four-digit suffix; the parent task audits the digit receiver.

## PG3: pi in the Mellin normalization — established

The independently proved conductor is N=18496=136^2. Fourier terms exp(2 pi i m z), evaluated at z=iu/sqrt(N), become exp(-2 pi m u/sqrt(N)). Thus the exact decay parameter is

\[
\alpha=\frac{2\pi}{\sqrt N}=\frac{\pi}{68},\qquad
\Lambda(s)=\alpha^{-s}\Gamma(s)L(E,s).
\]

These are Fourier/Mellin normalization identities, not fitted decimal relations. Cremona gives this completion in equation (2.8.5) and the central derivative integral in (2.13.1). [Cremona, chapter 2](https://johncremona.github.io/book/fulltext/chapter2.pdf#page=23)

For the already proved lower vanishing L(E,1)=L'(E,1)=0, writing lambda_2=Lambda''(1)/2 and c_2=L''(1)/2 gives

\[
c_2=\frac{\pi}{68}\lambda_2,
\qquad
\lambda_2=\sum_{m\ge1}a_m\int_1^\infty e^{-(\pi/68)mu}(\log u)^2\,du.
\]

The simple coefficient conversion needs those lower zeros: otherwise derivatives of the completion factor contribute cross terms. The input conductor and lower-zero proofs are retained from [LOCAL_ANALYTIC_INPUTS.md](../../bsd-trace-02/dependencies/LOCAL_ANALYTIC_INPUTS.md) and [ANALYTIC_PROOF.md](../../bsd-trace-02/dependencies/ANALYTIC_PROOF.md). Pi's appearance here is established independently of BSD's leading-coefficient equality.

## PG4: the exact CM period factor — proposed formula corrected

For n>0 on y^2=x^3-n^2x, the unbounded real component has two branches. With omega=dx/(2y), each contributes half of the following positive integral, so the connected period is

\[
\Omega_{n,c}=\int_n^\infty\frac{dx}{\sqrt{x(x^2-n^2)}}.
\]

There are two real components. Translation by a point of the other component preserves the invariant differential, hence their volumes are equal and Omega_(n,all)=2 Omega_(n,c). For E34 this all-component convention is the one already used in the BSD target. [Prior factor comparison](../../bsd-identity-01/input_source/FACTOR_COMPARISON.md)

To evaluate without a guessed factor, set x=n/u^2 and then v=u^4:

\[
\Omega_{n,c}
=\frac{2}{\sqrt n}\int_0^1\frac{du}{\sqrt{1-u^4}}
=\frac{1}{2\sqrt n}B(1/4,1/2)
=\frac{\Gamma(1/4)^2}{2\sqrt{2\pi n}}.
\]

The last equality uses B(a,b)=Gamma(a)Gamma(b)/Gamma(a+b), Gamma(1/2)=sqrt(pi), and Gamma(1/4)Gamma(3/4)=pi sqrt(2). [DLMF beta integral](https://dlmf.nist.gov/5.12#E1), [DLMF reflection formula](https://dlmf.nist.gov/5.5#E3)

Therefore

\[
\boxed{\Omega_{34,c}=\frac{\Gamma(1/4)^2}{2\sqrt{68\pi}},
\qquad
\Omega_{34,\mathrm{all}}=\frac{\Gamma(1/4)^2}{\sqrt{68\pi}}.}
\]

The old rigorous all-component enclosure is [0.899358321446,0.899358321447]; division by two gives the connected enclosure [0.449679160723,0.4496791607235]. The PG4 expression Gamma(1/4)^2/(2 sqrt(pi) sqrt(34)) equals sqrt(2) times the connected period and is not either of these two conventions. This is an exact factor refutation, not a disagreement based on approximate values.

The curve's CM is visible in the algebraic automorphism i:(x,y)↦(-x,iy) over Q(i), whose square is group inversion and whose pullback sends omega to i omega. In particular j=1728, also obtained directly from j=1728·4A^3/(4A^3+27B^2) with A=-1156 and B=0. This is actual quarter-turn structure on the complex elliptic curve. It does not supply a quarter-turn on the rational Mordell-Weil lattice: for instance i(P)=(2,48i) is outside E(Q). Equal ranks of two lattices do not identify their metrics or operations.

## PG5: an exact pi relation with a closing iteration — established and already present

Define M34=AGM(sqrt(68),sqrt(34)). Substitution t=x-34 gives

\[
\Omega_{34,c}=\int_0^\infty\frac{dt}{\sqrt{t(t+34)(t+68)}}.
\]

The AGM integral identity gives this integral as pi/M34. Consequently

\[
\boxed{\Omega_{34,c}M_{34}=\pi,
\qquad\Omega_{34,\mathrm{all}}M_{34}=2\pi.}
\]

The source identity is [DLMF 19.8.4](https://dlmf.nist.gov/19.8#E4). This is a clean re-expression of the AGM formula already derived in the [prior factor comparison](../../bsd-identity-01/input_source/FACTOR_COMPARISON.md); it is not a new discovery or a new proof of BSD.

There is an exact operational structure available here. On the positive ordered carrier a>=b>0, iterate

\[
(a,b)\longmapsto(A,G)=\left(\frac{a+b}{2},\sqrt{ab}\right),
\qquad(a_0,b_0)=(\sqrt{68},\sqrt{34}).
\]

The endpoints converge to the same M34; b_k<=M34<=a_k, so the associated period bounds pi/a_k<=Omega_(34,c)<=pi/b_k close together. The AGM and its corresponding period integral are preserved by every step. The exact update is invertible on this ordered carrier:

\[
(A,G)\longmapsto
\left(A+\sqrt{A^2-G^2},\ A-\sqrt{A^2-G^2}\right).
\]

Both legs follow from a+b=2A and ab=G^2. Without ordering, swapping the two initial occurrences is forgotten. Passing to the common limit forgets initial shape even with ordering: for any m>0 the complete limit fiber is

\[
\left\{\left(\frac{mr}{\operatorname{AGM}(r,1)},
\frac{m}{\operatorname{AGM}(r,1)}\right):r\ge1\right\}.
\]

Indeed homogeneity proves every displayed pair has AGM m; conversely any a>=b>0 with AGM m has r=a/b and m=b AGM(r,1), giving the displayed pair. Thus finite updates can retain recoverability while the limiting scalar retains the period receiver and loses shape. This is a written synthesis from the classical AGM theorem, not a decimal test. Positivity, order, and the selected receiver are essential; zero inputs or arbitrary complex square-root choices require another contract.

The initial E34 pair is a specified member of this positive-real carrier. Neither its AGM update nor its inverse is the rational group doubling used to construct canonical heights. A pi/carry claim concerning the latter still needs a map preserving the requested observation and update behavior.

## PG2: a basis-independent bare-distance claim — exactly refuted

Let p=H(P), q=H(Q), beta=(H(P+Q)-p-q)/2, and R=pq-beta^2. The earlier height proof gives

\[
d(P,Q)^2=p+q-2\beta.
\]

Changing the basis from (P,Q) to (P,-Q) preserves the lattice and regulator but replaces the squared distance by p+q+2 beta=H(P+Q). The previous rational enclosures put the original distance between 2.03 and 2.04 and the reversed distance between 2.6 and 2.7. Thus a fixed bare distance and any assertion requiring that same fixed decimal word for every integral basis already fail on this one curve. [Exact height and reversal audit](../../closure-seam-09/DISTANCE_AND_SEAM.md)

More generally, Q_n=Q+nP is an integral basis shear for every integer n. Its exact squared distance is

\[
d(P,Q_n)^2=q+(n-1)^2p+2(n-1)\beta,
\]

which grows without bound as |n| grows because p>0, while the regulator stays R. This is a complete argument against the frozen invariant-distance version, rather than only a finite sample of bases. It does not refute an operator whose retained state includes the basis and transforms its readout correctly.

A threshold must still be specified individually. For example, the receiver H(P-Q)>5 is false in the original basis and true after reversing Q. This does not prove that every conceivable threshold receiver changes; a constant receiver such as H(P-Q)>0 on independent basis pairs is a different, weaker observation.

Height conventions also matter. H↦lambda H gives d↦sqrt(lambda)d and a rank-two regulator R↦lambda^2 R. Choosing lambda=1/2 changes the distance by 1/sqrt(2). Changing the logarithm base similarly changes the numerical metric. Those are known coordinate/convention changes, not transformations of the underlying rational group. A statement specific to the fixed natural-log full-height convention remains a legitimate local statement; a convention-free decimal claim does not survive these controls.

## A useful exact re-expression of the remaining BSD comparison

The two established pi identities above permit a source-derived rewrite. With c_2=(pi/68)lambda_2 and Omega_all=2pi/M34,

\[
\frac{c_2}{\Omega_{\rm all}R}
=\frac{M_{34}\lambda_2}{136R}.
\]

For a specified candidate positive integer sigma, the real equality c_2=Omega_all R sigma is therefore equivalent to

\[
\boxed{M_{34}\lambda_2
=136\sigma\left[pq-\frac{(p+q-d^2)^2}{4}\right].}
\]

The cancellation of the explicit outer pi factor is exact. Pi still occurs inside lambda_2's exponential kernel; this rewrite does not eliminate the analytic content or establish equality. It displays the actual bridge obligation among the analytic moments, real-period AGM, and joint height geometry. The underlying [identity target](../../bsd-identity-01/EXPLICIT_IDENTITY_TARGET.md) also separately requires identifying finite sigma with the actual Sha order before calling it the full BSD formula.

## Final dispositions and claim ceiling

| Candidate | Disposition | What remains |
|---|---|---|
| PG1, fixed-basis pi/carry reading | OPEN | An explicit source-derived map and a held-out prediction or proof; the parent digit audit can narrow specified versions. |
| PG2, basis-independent bare distance | REJECT, exact hostile basis changes | A covariant formulation retaining its basis is a different admissible contract. |
| PG3, Mellin pi/68 | Established theorem dependency plus exact E34 substitution | No new analytic-to-height identity follows automatically. |
| PG4, proposed connected gamma-period factor | REJECT as written; corrected exact formula proved above | Retain differential and real-component count. |
| PG5, period times AGM equals pi | Established; recovered from existing work, with an explicit operation/inverse/limit-fiber account here | Connecting this operation to rational height doubling or the user's digit operator is OPEN. |

Evidence: elementary written deductions, primary normalization sources inspected on 2026-09-12, and attributed reuse of earlier certified intervals. No new formal proof, arbitrary-precision numerical computation, Sha computation, general transcendence assertion about heights, or classification of all pi/RPRM interpretations is claimed. In particular, this report neither proves nor assumes that canonical heights cannot satisfy a more subtle exact relation involving pi.
