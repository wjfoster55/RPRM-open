# What the completed YM cover contributes to the BSD trace

Completion note: this transfer was written before the trace was computed.
The missing orbit and residue described below are now supplied by
[TRACE_CALCULATION.md](TRACE_CALCULATION.md), with the audited 5-primary
conclusion. The full complex identity comparison remains open.

Read-only inspection: 12 September 2026, 20:11:38 UTC. The active YM
continuation was neither messaged nor interrupted. No YM file or earlier
checker was modified or run. The inspected completed source versions are
bound by paths, sizes and SHA-256 digests in
[the snapshot](evidence/ym_snapshot.json); hashes bind bytes, not truth.

Two useful transfers emerge. First, the exact trace needs a complete
CM-orbit cover **with its selected component and multiplicities retained**.
An ambient enlargement alone can produce the wrong answer. Second,
preserving the signed Newton-sum formula reduces the required precision:
the first polynomial coefficient is needed modulo 125, while coefficients
two through five are needed only modulo 25. Neither transfer imports a
Yang–Mills physical theorem into number theory.

## 1. What the completed donor actually proves

The [covering result](../ym2_covering_argument/COVERING_RESULT.md) and
[direct argument](../ym2_covering_argument/DIRECT_COVER_ATTEMPT.md)
work on finite open square/cubic lattices with full SU(2) link rotors,
the declared metric and actual interacting vacuum. Their energy-weighted
Fourier norm counts every support touching a fixed link, including
arbitrarily high spins and collective supports. Differentiation forces
shared support, and the inverse kinetic operator cancels the norm's
output-energy weight. These exact identities give graph-independent
estimates and a small invariant contraction ball. An all-state form bound
on the ambient link Hilbert space then covers the gauge-invariant sector
with the same operator, actual vacuum and energy subtraction.

On \(0\le r\le1/(48m)\), \(m=2(d-1)\), the source proves a
dimensionless gap bound of \(1/2\). Its
[conditional refinement](../ym2_covering_argument/CONDITIONAL_REFINEMENT.md)
constructs the actual remainder after an exactly matched second-order
head. It uses \(\|w\|_*\le Y-t-(4/3)t^2\), then translates that
norm into the complete exterior-oscillation receiver by an all-support
count. A small average \(L^2\) remainder would not suffice: narrow
spikes can have small average norm and large supremum response.
The [conditional review](../ym2_covering_argument/CONDITIONAL_REVIEW.md)
and [direct review](../ym2_covering_argument/DIRECT_COVER_REVIEW.md)
check these specific written arguments.

The completed norm bounds absolute coefficient sizes. Signed correlations
are retained when the known head cancels exactly. A sharper signed/support
norm is proposed in [the next obligation](../ym2_covering_argument/NEXT_OBLIGATION.md);
it is not a further theorem already established there. Likewise, the
completed result is not a continuum mass-gap theorem. The relevant donor
is its method of matching an exact operation and a complete receiver,
not an asserted relation between physical energies and elliptic curves.

## 2. The exact receivers determine what a cover may do

| Setting | Fixed carrier and operation | Requested readout | Required preservation |
|---|---|---|---|
| Completed YM source | Actual finite-lattice form domain, actual vacuum transform | Lower bound for every excited trial vector | Isometric inclusion and the same form, vacuum and energy subtraction |
| BSD real identity | Fixed E34, normalized Mellin coefficient and full-basis height determinant | Equality of two particular real constants | Exact matching law and vanishing boundary, with every analytic and height remainder retained |
| BSD trace | The actual degree-256 primitive CM orbit for the specified \(\rho\) | \(\operatorname{Tr}(2\rho^5+289\rho)\bmod125\) | Correct orbit, all conjugate occurrences, coefficient integrality and multiplicity-preserving aggregation |

The BSD targets are those in the existing
[explicit identity](../bsd-identity-01/EXPLICIT_IDENTITY_TARGET.md) and
[odd-prime attempt](../bsd-identity-01/ODD_PRIME_ATTEMPT.md). In particular,
the trace is for the specified primitive division point on the admitted
CM-isogenous curve. Its conditional 5-primary conclusion does not concern
an arbitrary degree-256 root or the raw complex second derivative.

An ambient lower bound transfers to a subset because every possible
counterexample in the subset is also in the ambient set. Exact summation
has no such automatic monotonicity. To see the danger here, an ambient
root cover containing both \(\rho\) and \(-\rho\) cancels the odd
function \(h(X)=2X^5+289X\) pairwise. That proves the trace over that
enlarged signed cover is zero; it does not identify the trace over the
particular CM orbit. This is an inference counterexample, not a statement
that the actual E34 trace is nonzero.

Here is a correct finite-cover lemma. Suppose \(\pi:C\to O\) is a
certified surjection onto the actual conjugate-occurrence set, every fiber
has known size \(\mu\), and the function on the cover is exactly
\(h\circ\pi\). Then

\[
\sum_{c\in C}h(\pi(c))=\mu\sum_{o\in O}h(o).
\tag{1}
\]

For a residue modulo 125, division by \(\mu\) is enabled if
\(5\nmid\mu\). If \(\mu=5\), the cover sum modulo 125
does not uniquely recover the original residue modulo 125. A cover that
changes the sign of \(h\) on its fibers also violates the function
preservation premise. Equal values and equal conjugate occurrences must
remain distinct when computing the multiplicity.

A concrete orbit-completeness certificate can instead retain the
generators of the admitted ray-class Galois action, a correctly identified
primitive seed, its generated orbit, and closure under every generator
and inverse. Closure from that seed proves coverage of its full orbit;
the supplied degree theorem checks the expected size 256. Size 256 alone
does not identify the orbit: two disjoint orbits can have that same size
and different sums. The seed and action must be the actual CM objects,
not labels chosen to fit the expected trace.

## 3. A component projector gives an exact ambient trace adapter

One sufficient algebraic implementation is as follows. Put
\(A=(\mathbb Z/125\mathbb Z)[i]\). Let \(B\) be a certified
finite free commutative \(A\)-algebra modeling a complete integral
division carrier. Suppose its element \(\rho\) and idempotent
\(e\), \(e^2=e\), select a direct summand \(eB\) identified with
the actual degree-256 trace algebra. Then

\[
T=\operatorname{Tr}_B\bigl(m_{e(2\rho^5+289\rho)}\bigr)
=\operatorname{Tr}_{eB}\bigl(m_{2\rho^5+289\rho}\bigr).
\tag{2}
\]

Proof: \(B=eB\oplus(1-e)B\), and multiplication by \(eh\)
acts as multiplication by \(h\) on the first summand and zero on
the second. Matrix trace adds over that direct sum. This retains a
complete ambient carrier while projecting the **correct** readout.

Because \(i\) has roots 57 and 68 modulo 125, \(A\) is the product
of two copies of \(\mathbb Z/125\mathbb Z\). Rank 256 must hold
in both components, and the two traces must satisfy the descent/rationality
comparison from the admitted theorem. Agreement is a useful check; it
does not prove that a wrongly chosen summand is the right CM orbit.

There is a useful lifting invariant. Suppose the correct component
idempotent \(e_0\) has been identified modulo 5 and its coordinates
lifted into \(B\). Set \(a=e^2-e\), \(v=2e-1\). Since
\(v^2=1+4a\) and \(a\in5B\), \(v\) is invertible. The update

\[
e'=e-(e^2-e)(2e-1)^{-1}
\quad\Longrightarrow\quad
e'^2-e'=(e^2-e)^2(2e-1)^{-2}
\tag{3}
\]

doubles the error's 5-adic divisibility. Two updates take error in
\(5B\) to error in \(5^4B=0\), so they produce an exact idempotent
modulo 125. This finite invariant does not need a real small-error norm.
Idempotents lift uniquely through the nilpotent ideal \(5B\): if two
lifts \(e,f\) agree modulo it, the idempotents \(e(1-f)\) and
\(f(1-e)\) are nilpotent, hence zero, giving \(e=f\).

The indispensable missing premise is identification of the correct
component modulo 5 in a valid carrier. The present note constructs neither
\(B\) nor \(e_0\). An unramified field does not by itself imply
that a chosen primitive element has squarefree minimal polynomial modulo
5: distinct conjugate occurrences can collide in that coordinate. A
component construction must certify its algebra and basis rather than
discard repeated-looking residues. Using a suitable prime-to-5 division
scheme can retain the additional coordinates needed to separate them.

## 4. Signed aggregation lowers the required coefficient precision

Let the correct monic polynomial be
\(X^{256}+a_1X^{255}+\cdots+a_5X^{251}+\cdots\), with coefficients
integral at 5. Newton identities use only integer operations here:

\[
s_1=-a_1,\qquad
s_k=-\left(\sum_{j=1}^{k-1}a_js_{k-j}+ka_k\right),
\qquad T=2s_5+289s_1.
\]

Expanding the signed expression gives

\[
\boxed{T=-2a_1^5+10a_1^3a_2-10a_1^2a_3-10a_1a_2^2
+10a_1a_4+10a_2a_3-10a_5-289a_1.}
\tag{4}
\]

Every occurrence of \(a_2,a_3,a_4,a_5\) has coefficient divisible
by 5. Changing any of those inputs by a multiple of 25 therefore
changes \(T\) by a multiple of 125. Thus the sufficient mixed
precision contract is

\[
a_1\pmod{125},\qquad a_2,a_3,a_4,a_5\pmod{25}.
\tag{5}
\]

There is no division by 5 in Newton's fifth step. This reduction is
specific to the requested combination of traces; applying a common
worst-case precision to each intermediate quantity would miss it.
The first coefficient generally still needs modulus 125: its linear
coefficient \(-289\) is a 5-adic unit, and replacing \(a_1=0\)
by 25 with the other inputs zero changes \(T\) modulo 125.

Equations (4)–(5) hold over the commutative local coefficient algebra,
not only for rational integer inputs. They require the coefficients of
the actual integral trace polynomial. They do not identify that polynomial.
Once supplied, the result can be compared with the complete remaining
fiber \(\{0,25,50,75,100\}\) from the admitted valuation lower
bound. Zero remains an inconclusive outcome of the sufficient Sha test.

## 5. What a stronger real-identity transfer would have to supply

The YM argument gains more than convergence: it constructs the actual
solution inside a complete invariant ball, proves uniqueness there, and
matches its exact head before estimating its remainder. For the fixed
BSD discrepancy \(D=c^{\rm an}_2-\Omega\sigma\mathcal R\),
a corresponding sufficient mechanism would be an independently derived
joint residual \(z\) and bounded linear operator \(L\) satisfying

\[
z=Lz+r_k\quad\text{for every }k,\qquad
\|L\|\le\kappa<1,\qquad\|r_k\|\le\eta_k\to0,
\qquad |D|\le C\|z\|.
\tag{6}
\]

The geometric-series/resolvent estimate gives
\(\|z\|\le\eta_k/(1-\kappa)\) for every \(k\), hence
\(z=0\) and \(D=0\). A shared strict contraction with correctly
identified analytic and arithmetic fixed points is another realization
of the same uniqueness mechanism. These are precise sufficient
conditions, not operators or residual equations supplied by the YM source
for E34. No such \(L,z,r_k\) is constructed here. The existing BSD
telescoping criterion likewise still needs its exact all-stage matching
rule and terminal boundary proof.

The source's own stopping diagnosis reinforces this distinction:
\(y\le t+(4/3)y^2\) alone allows large solutions; the small invariant
ball and strict contraction are essential. Its construction estimate
stops before its geometric lower bound would reach zero. Failure of a
BSD coverage construction or a trace valuation criterion likewise does
not falsify BSD or establish a nontrivial Sha component.

William's retained half-step remains \(-0.2/2=-0.1\), stopping at
the midpoint. Coarse zero retains a remainder at the next readout level.
Neither operation supplies the missing CM orbit selection or equation
(6). The useful advance here is to specify a complete finite receiver
for the trace and a precision invariant that can be used in its actual
construction.

## Evidence and current boundary

The snapshot records the completed sources and selected reviews. New
bounded scalar arithmetic checks verified the expanded Newton identity
on 78,125 inputs, its four mixed-precision invariances in 312,500 checks,
and the two-step idempotent update for all 50 scalar lifts whose residues
are idempotent modulo 5. The exact grids and deterministic procedures
are in the JSON. Their integer intermediates were below \(2^{53}\);
they used exact integer arithmetic. They corroborate the written algebra,
not a constructed CM trace algebra or any unrestricted analytic theorem.

The finite-cover, projector, lifting, and mixed-precision implications
are written derivations at their stated premises. Actual primitive-orbit
coverage, the trace value, and any resulting 5-primary conclusion are
left to the ongoing trace computation. The full complex BSD identity
and total-Sha identification remain outside this transfer result.
