# What the prime seam fixes, and what remains open

The exact identities in `PRIME_SEAM_PROOF.md` fix local conversion factors.
The requested global scalar lies in a different comparison. In the
previously admitted rank-two p=5 setting, put A=mathcal L^(2)_(S,5),
S={infinity,2,5,17}. The coefficient is an augmentation coefficient;
an unconverted ordinary second derivative is a different normalization.
The established nonzero regulator makes C5·A/R5 a well-defined scalar.
The target is

\[
\boxed{C_5 A=\frac{L_S^*(E,1)}{\Omega_\xi R_\infty}R_5.}
\tag{6}
\]

The precise published comparison, including its converse when R5 is
nonzero, is [BKS, Corollary 6.7](https://kurihara.math.keio.ac.jp/bks4.pdf#page=43).
The prior hypothesis and normalization audit is copied into dependencies.
This experiment has not computed A or established (6).

## A same-carrier bridge that does close

Using13 as an auxiliary prime in the p=5 construction differs from using
13 as the p-adic base prime. Write sigma13 for its cyclotomic action in
Gamma5. Its removed Euler factor is

\[
e_{13}=1+\frac6{13}\sigma_{13}^{-1}
          +\frac1{13}\sigma_{13}^{-2},\qquad
e_{13}(1)=\frac{20}{13}.
\tag{7}
\]

The interpolation definition in BKS §6.1 and its uniqueness identify
L_(S+13,5)=e13 L_(S,5). Proposition 6.1 supplies order at least2 here.
[BKS, §6.1 and Proposition 6.1](https://kurihara.math.keio.ac.jp/bks4.pdf#page=41).

Our leading-term argument is elementary. In any power-series ring, if
F(T)=a2 T²+O(T³) and e(T)=e0+O(T), then
e(T)F(T)=e0 a2 T²+O(T³). Hence

\[
\mathcal L^{(2)}_{S+13,5}=\frac{20}{13}\mathcal L^{(2)}_{S,5}.
\tag{8}
\]

On the complex side the ordinary good-prime Euler polynomial is
1−a13·13^(−s)+13^(1−2s), whose value at 1 is20/13. Since the order
of vanishing is2, the same elementary leading-term argument gives
L*_(S+13)=(20/13)L*_S. Thus both sides of (6) transform by the same
known nonzero factor. This is an exact compatibility relation, but an
incorrect equality would remain incorrect after this common multiplication.
Because v5(20/13)=1, dividing a finite-precision result by it costs one
absolute5-adic digit. Lower-order terms would invalidate the simple
leading-term rule; the executable preserves such a hostile example.

## Why relative prime-path agreement leaves an absolute scale

Suppose supplied classes satisfy linear norm relations
Cor(z_(m ell))=P_ell(sigma_ell^−1)z_m. For any common scalar u,
linearity gives the same equations for u z_m. If u is a local unit,
the generated local lattices are also unchanged. If u=1 mod5^N,
the classes agree to that precision in an admitted integral lattice.
Thus homogeneous norm relations and these finite observations do not
determine the scale. Fixed, independently normalized interpolation values
can distinguish the actual system from its rescaling; they are precisely
the extra input missing from this argument.

Even combining several primes with a short real interval needs a
reconstruction premise. Here is an exact countermodel to those proposed
constraints, not a candidate value of the actual BSD quotient. Put

\[
M=2^8 5^8 13^8,\quad B=10^8M+1,\quad
u=\frac{B+M}{B},\quad q=u^2.
\]

Then q>1, q is a positive rational square, its valuations at 2,5,13 are
zero, and q≡1 mod p^8 for all three primes. Yet it lies strictly inside
the previously proved real quotient interval
[0.999920542,1.000092816]. Indeed u−1=M/B<10^−8, so
q−1<2·10^−8+10^−16, with all inequalities checked by exact fractions.
These congruences have not been computed for the actual BSD quotient;
the countermodel shows that even granting them would leave ambiguity
without an additional denominator/height bound or a stronger identity.

A useful sufficient criterion is: if q=A/B is rational, 0<B≤D,
gcd(B,M)=1, q≡1 modM and |q−1|<M/D, then q=1. The congruence says
M divides A−B, while |A−B|=B|q−1|<M. This proves exact equality.
Rationality, the denominator bound and the actual congruence must be
proved; none follows from a shared numeral, norm or lucky membership.

## The next discriminator

An independently normalized value of the augmentation coefficient A
would turn the established R5≠0 into an explicit arithmetic-side
multiplier C5 A/R5. A certified nonzero digit would also rule out a zero
derived class. Matching its normalization to the real side of (6) remains
an additional proof obligation. Local shared-factor cancellation supplies
calibration checks for that work; it has not yet supplied that value.

The prior results rank 2, full Mordell–Weil basis, Sha[2-infinity]=0,
Sha[5-infinity]=0 and nonzero cyclotomic5-adic regulator are retained as
dependencies. This turn establishes no additional primary part of Sha.
Total Sha, the exact real leading-coefficient identity and general BSD
remain OPEN.
