# A proved E34 reciprocity relation, with a fresh arithmetic readout

For E34, we have a concrete exact relation between its 5-adic analytic
coefficient and a canonical arithmetic class. Applying the published
Burns–Kurihara–Sano (BKS) reciprocity theorem, with the period, height and
tensor conventions matched, gives

\[
\boxed{K=C_5 b_2 d^2\,G^{-1}\ell.}
\tag{R}
\]

This is a theorem-backed specialization, not a proposed general BSD proof.
The new rational-point and modular-symbol calculations give

\[
\boxed{K\equiv50P+58Q\pmod{125M}.}
\]

Here E is y²=x³−1156x, P=(-2,48), Q=(-16,120), and
M=Z5 tensor E(Q)/torsion. K is the period-normalized canonical derived
Kato class, transported to the Mazur–Stein–Tate (MST) height convention.
It is a 5-adic vector, not the claim that a rational point equals 50P+58Q.
The entire preimage of the displayed residue is 50P+58Q+125M.

## What the relation does

The arithmetic height pairing measures how an unknown vector pairs with
each of P and Q. The reciprocity theorem supplies both answers from the
analytic coefficient. These two independent equations determine one
vector. Their matrix has determinant a 5-adic unit, so there is no hidden
free direction left in this reconstruction.

This makes a precise version of a relation holding two sides together:
the pairing supplies the joint information and a uniqueness theorem
supplies the closure. A distance threshold does not enter this proof.
The RPRM contribution here is the question about retained joint information
and reconstruction; the mathematical bridge is the cited reciprocity
theorem. This experiment establishes no universal RPRM closure principle.

The exact theorem (R) is stronger than any finite digit calculation.
The digits make its consequence explicit and test its normalization.
They do not certify equality by approaching a real number more closely.

## Definitions and the exact proof

Fix omega=dx/(2y), the connected real period Omega_c, and
T=gamma−1 with chi_cyc(gamma)=6. Put

\[
\begin{aligned}
G_{ij}&=B_{\rm MST}(P_i,P_j), & \ell_i&=\log_\omega(P_i),\\
d&=\log_5(6)/5, & C_5&=(1-\alpha^{-1})^{-1}(1-\alpha/5),\\
\alpha^2+2\alpha+5&=0, & \alpha&\equiv3\pmod5.
\end{aligned}
\]

b2 is the coefficient of T² in the connected-period 5-adic L-function,
in the trivial Teichmüller branch. The MST bilinear height is
B(X,Y)=h5(X)+h5(Y)−h5(X+Y), with cyclotomic functional log5/5.

The class K is defined independently of (R): take the canonical BKS
Iwasawa–Darmon derivative kappa, divide out c_xi=Omega_c/Omega_xi, and
transport its degree-one tensor line by rho_MST. The map rho sends T to d;
rho_MST=epsilon rho is oriented so that the transported BKS height equals
the named MST pairing. The height comparison supplies epsilon in {+1,−1};
it is not selected from the output digits. Explicitly,

\[
K=c_\xi^{-1}(\mathrm{id}\otimes\rho_{\rm MST})\kappa.
\]

The degree-two transport has sign epsilon²=1. The reciprocity theorem
then gives B(X,K)=C5 b2 d² log_omega(X). Taking X=P and X=Q proves
G K=C5 b2 d² ell. Since det G is nonzero, inversion gives (R).
The raw, unoriented BKS scalarization is epsilon c_xi K, with those factors
retained. [BKS, Theorem 6.2 and the height comparison in §5](https://kurihara.math.keio.ac.jp/bks4.pdf#page=41).

The detailed [class transport audit](agents/DERIVED_CLASS_ROUTE.md)
records the hypotheses, the previous proof dependencies, and this
normalization. In particular, the theorem does not require assuming
the real BSD coefficient identity. Previously proved rank two,
5-primary Sha finiteness and basis saturation are attributed inputs;
this run does not replay their entire earlier proofs.

## New exact symmetry and precision proof

For i²=−1 in Z5, the automorphism (x,y)↦(−x,iy) takes t=−x/y to it
and omega to i omega. Transforming the unique normalized integral
sigma solution produces another such solution with its constant negated.
Uniqueness forces c=0 and sigma(it)=i sigma(t). Consequently

\[
\sigma(t)/t\in1+t^4\mathbf Z_5[[t^4]].
\]

This is an all-orders written argument. It justifies dropping the sigma
correction modulo 125 after the division by 5 in the height formula.
The separate evaluated formal-log estimate is
v5((log_omega(t)−t)/5)=5v5(t)−2 for nonzero t in 5Z5.
[MST, Theorem 1.3](https://wstein.org/papers/pheight/pheight.pdf#page=4)
and the independent [sigma and tail audit](agents/SIGMA_AUDIT.md) give
the proof and exceptional cases. A coefficientwise denominator-5 bound
for the whole formal logarithm is false; that failed stronger assertion
is retained in the audit.

## Fresh computation

All table entries are residues modulo 125, computed in
[fresh-01](runs/fresh-01/RUN.json).

| Object | Fresh result |
|---|---|
| Analytic coefficient b2 | 51 |
| Arithmetic Gram matrix G | [[66,32],[32,117]] |
| det G | 73 |
| ell/5 | (117,102) |
| W/5, where W=adj(G)ell | (50,113) |
| 5 Lambda, where Lambda=C5 b2 d²/det G | 16 |
| K=(5 Lambda)(W/5) | (50,58) |

For a direct check, (5C5)b2 d²=43 modulo 125, so the two equations are

\[
\begin{pmatrix}66&32\\32&117\end{pmatrix}
\binom{50}{58}
\equiv43\binom{117}{102}
\equiv\binom{31}{11}\pmod{125}.
\]

The analytic program starts with the exact level-32 modular-symbol line
and the proved period anchor 1/4. It constructs the discriminant-136
twist, with its explicit factor 2. Its classical level-four measure sum
has raw logarithmic-moment error in 5^5 Z5. Conversion to b2 divides by
4 log5(6)² and loses exactly two precision digits. A separate
overconvergent integration agrees at the certified precision; that
agreement is not the error proof. The shared symbol and normalization
are disclosed. The [analytic normalization proof](dependencies/COEFFICIENT_PROOF.md)
supplies the exact anchor and measure bound; its historical outputs are
not read by the new program.

The arithmetic program starts from the displayed rational points,
computes 8R exactly, checks the required local components, and evaluates
log5(t(8R)/d(8R)) with a proved truncation. Every prime factor of the
denominator is retained. It checks addition, quadratic height identities,
all rational 2-torsion translations, good ordinarity, and residual
irreducibility. No database rank or saved PASS is an input.

A useful invariance is now explicit. Under any invertible rational
change of basis U,

\[
G'=U^tGU,\quad\ell'=U^t\ell,\qquad
U(G')^{-1}\ell'=G^{-1}\ell.
\]

Thus K is unchanged even when the separate determinant and W change.
The integral tests include a subgroup of index 2. Index divisible by 5
requires extra precision and cannot use the current unit-determinant
modular inversion. A singular pairing does not determine a unique K.

## What is still unproved

The real comparison still needed, in the BKS tensor convention, is

\[
C_5\mathcal L^{(2)}_{S,5}
\stackrel{?}{=}
\frac{L_S^*(E,1)}{\Omega_\xi R_\infty}R_5.
\tag{OPEN}
\]

The real and 5-adic quantities are compared through the period-regulator
construction and the comparison embedding specified in BKS. One cannot
substitute a real decimal interval directly into a 5-adic equation.
With nonzero R5, BKS Corollary 6.7 identifies this as the additional
generalized Perrin–Riou comparison. It is not supplied by Theorem 6.2.
[BKS, Corollary 6.7](https://kurihara.math.keio.ac.jp/bks4.pdf#page=43).

Computing K from b2 and then recovering b2 from the same equation gives
an inverse calculation, not an independent proof of (OPEN). The next
required advance is an independently proved central-value comparison,
or an effective discreteness theorem for the real normalized quotient.
The [CM literature audit](agents/CM_THEOREM_ROUTE.md) checks why the
reviewed rank-zero and simple-zero results do not supply that step for
this rank-two curve. The earlier 5-primary Sha result remains established;
total Sha and the full real BSD identity remain OPEN.

## Run and inspect

Use Python 3.10+ and PARI/GP 2.17.4. The tested official GP executable is
in the earlier coefficient experiment; this smaller packet does not
duplicate that runtime. Supply its path explicitly, or a compatible
installation elsewhere. In PowerShell from C:/github/RPRM-open:

```powershell
python -I -B research/bsd-relation-10/work/run.py --gp C:/github/RPRM-open/research/bsd-coefficient-05/runtime/gp64-2-17-4.exe --output C:/github/RPRM-open/research/bsd-relation-10/runs/my-replay
```

The output directory must be new. The runner snapshots source, records
logs and hashes, and rejects GP error text even if the process exits zero.
Read [fresh evidence](runs/fresh-01/evidence/reciprocity.json),
[the concise BSD rebrief](BSD_REBRIEF.md), and
[the independent finite readback review](agents/FINITE_READBACK_REVIEW.md).
Dependency snapshots are historical proof documents, with source paths
and hashes; their presence does not make their claims fresh computations.

Evidence grades: published theorems, written specialization and new CM
symmetry proof, exact finite calculations with proved error bounds, and
independent review. No formal proof-assistant certificate is claimed.
