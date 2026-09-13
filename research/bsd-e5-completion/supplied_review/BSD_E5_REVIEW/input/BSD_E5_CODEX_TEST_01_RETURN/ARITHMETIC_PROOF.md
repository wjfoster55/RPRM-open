# Independent arithmetic proof for BSD-E5-CODEX-TEST-01

This check confirms A01, A02 and C01, with the cited standard theorem dependencies below. It also executes K01_OFF_CURVE, K05_LOST_REMAINDER and K06_FRAME_TRANSPORT. No mathematical correction to the supplied descent was needed. The independent implementation, exact data and fresh logs are `work/arithmetic_check.py`, `evidence/arithmetic.json`, and `evidence/arithmetic_execution_final.log`.

## Contract and evidence boundary

The mathematical carrier is the abelian group G=E(Q) of rational points on the nonsingular projective curve E: y²=x(x−5)(x+5), with O its identity. The displayed model has a-invariants (0,0,0,−25,0) and discriminant −16(4(−25)³)=1,000,000. Equality of points is exact rational/projective equality. A quotient label means equality modulo the specified subgroup; it does not identify a point occurrence. Multiplication by 2 is a group operation, halving is its preimage problem, −P is group inversion, and O is a group identity.

For descent the supplied ports are the curve and a squareclass triple; the requested readout is whether that triple is globally realized. For readback the supplied ports are an admitted rational point R and positive integer n; the returned data are its quotient coordinates and a rational reconstruction remainder. The complete rational halving fiber has four members when enabled, and is empty otherwise. The decoder selects one of those four by a declared deterministic policy. A missing remainder does not make the quotient fiber empty.

Universal conclusions use written arguments and explicitly cited theorems. The executable checks a bounded collection of rational points at n=1,2,3,4, plus complete finite residue and cube carriers. It admits at most 4096 bits in each point-coordinate numerator/denominator; the measured maximum is 1053. That is a point-storage guard for this implementation, not a universal height theorem or a cap on intermediate integer arithmetic. The universal all-n group description does not depend on this guard, and the finite tests are not presented as its proof.

## Standard dependencies and checked hypotheses

* **S_KUMMER, THEOREM_CITED:** the split rational two-torsion Kummer map is a homomorphism with kernel 2G, including its exceptional values. Its cohomology carrier can be written as triples in (Q*/Q*²)³ whose product is trivial. The two-coordinate identification and exceptional convention are in [Milne, *Elliptic Curves*, IV §3, Remark 3.7, printed p.113, PDF page 121](https://www.jmilne.org/math/Books/ectext6.pdf#page=121). Here the roots 0,5,−5 are distinct rational integers and the discriminant is nonzero, so the split hypothesis holds.
* **S_SELMER, THEOREM_CITED:** Sel_N is the subgroup whose restriction at every place lies in the local Kummer image, and 0→G/NG→Sel_N→Sha[N]→0 is exact. See [Stoll, *Descent on Elliptic Curves*, §1.1, printed/PDF pp.2–3](https://arxiv.org/pdf/math/0611694#page=2). Q is a number field, E is elliptic, and each N=2^n is an integer greater than one. The local conditions below give necessary exclusions; the rational witnesses establish every remaining all-place condition. No assumption of finiteness of the whole Sha is used.
* **S_MW, THEOREM_CITED:** G is finitely generated. See [Milne, Chapter IV opening, finite-basis theorem, printed p.101, PDF page 109](https://www.jmilne.org/math/Books/ectext6.pdf#page=109). Its elliptic-curve/number-field hypotheses were checked above.
* **S_HALF, THEOREM_CITED:** over characteristic different from two with all three roots in the field, an affine point is a double precisely when all three root differences are squares. The half formulas are [Bekker–Zarhin, §2, Theorem 2.1 and equations (3)–(6)](https://arxiv.org/html/1702.02255v2#S2). These hypotheses hold over Q; enabled calls check the differences exactly. O is treated separately. Their Example 2.2 treats a torsion target; here no nonzero rational two-torsion point is a double.

These primary sources were opened and the named passages checked during this run. The source records in `evidence/arithmetic.json` distinguish citations from the exact specialization. Neither a program PASS nor a hash proves these theorems.

## A01: complete doubling-class calculation

Write [a] for the class of nonzero a in Q*/Q*², represented by a signed squarefree integer. For x not among 0,5,−5,

    delta((x,y))=([x],[x−5],[x+5]).

Set delta(O)=(1,1,1). At a root e_i, replace the zero factor by (e_i−e_j)(e_i−e_k), retaining the two nonzero factors. Thus

    delta(T0)=(-1,-5,5),
    delta(Tplus)=(5,2,10),
    delta(Tminus)=(-5,-10,2).

Zero is never processed as a multiplicative squareclass. These conventions and the ordinary product being y² give a trivial product in every case.

Consider any Selmer class and a prime q other than 2 or 5. Its q-local image comes from an E(Q_q) point. If v_q(x)<0, all three factors have that valuation m; since 3m is even, m is even. If v_q(x)≥0, the factors are integral and their differences 5 or 10 are q-units. At most one factor can have positive valuation; the square product makes that valuation even. O and the exceptional signatures satisfy the same restriction directly. Therefore the rational squareclasses have no odd valuation outside {2,5}.

Let D={−10,−5,−2,−1,1,2,5,10}. Choosing d1,d2 in D determines d3=[d1d2], giving exactly 64 supported triples. The real curve has x in [−5,0] or [5,infinity), apart from O. Its nonexceptional sign triples are (--+) or (+++); the exceptional conventions give the same alternatives. Hence d1,d2 have the same sign and d3>0. The resulting 32-element subgroup is V. These facts establish Sel_2⊆V before any finite test.

For d in V consider the homogeneous covering equations

    d1 u1² − d2 u2² = 5t²,
    d3 u3² − d1 u1² = 5t².                 (1)

A local realization supplies a nonzero projective solution: for a usual point set x−e_i=d_i(u_i/t)² and clear denominators. For a root point set the corresponding u_i=0; the other two differences and the product-square condition recover exactly the exceptional signature. Conversely, if t≠0, set x=d1(u1/t)²; (1) gives the other two factors and their product gives y², because d1d2d3 is a rational square. A zero factor gives the just-described torsion case. If t=0, all three d_i u_i² are the same nonzero value. Thus their squareclasses over the field of the solution coincide; their product being a square forces that common class to be trivial in that field. This is the restriction of the O signature. Over Q the rational triple is therefore (1,1,1), with witness (1,1,1,0). Over a completion this is a statement about the local classes, not a general inference from local squareness to rational squareness. There is no additional infinity case in the covering/Kummer interpretation.

Any nonzero Q_2 projective solution can be multiplied by a power of two so the minimum of the four coordinate valuations is zero. This gives a vector in Z_2^4 with an odd coordinate. Its reduction modulo 4 and 8 is primitive and satisfies (1). The absence of such a residue vector is therefore a valid Q_2 obstruction. Existence of a residue vector is only a necessary test.

The checker exhausts the primitive solutions modulo 2, then lifts each surviving vector by all 16 choices of its four next binary digits to modulus 4 and again to modulus 8. Every primitive solution at the next level has one unique parent, so induction proves this enumerates the full finite solution set without omission or duplication. It independently obtains 32,16,8 surviving signatures at moduli 2,4,8. The complete counts and first witnesses for all 32 triples are retained in the receipt. This route differs from both the supplied flat quadruple enumeration and its weighted-square compression.

Eight exact rational witnesses saturate the upper bound. With P=(−4,6) and K=G[2]={O,T0,Tplus,Tminus}, the chord law gives:

| Representative | Point | Signature |
|---|---|---|
| O | O | (1,1,1) |
| T0 | (0,0) | (−1,−5,5) |
| Tplus | (5,0) | (5,2,10) |
| Tminus | (−5,0) | (−5,−10,2) |
| P | (−4,6) | (−1,−1,1) |
| P+T0 | (25/4,75/8) | (1,5,5) |
| P+Tplus | (−5/9,−100/27) | (−5,−2,10) |
| P+Tminus | (45,−300) | (5,10,2) |

The code recomputes these points, identifies each squareclass by eight exact rational-square membership tests, and constructs its homogeneous witness by clearing denominators. No archived answer is consulted. The eight signatures are distinct; call their subgroup H. As rational points they supply all-local witnesses, so H⊆delta(G)⊆Sel_2. Matching the eight independent mod-8 survivors proves equality throughout.

There is also a short written exclusion proof, giving an independent way to see completeness. The four disjoint cosets in V/H have representatives 1, A=(2,2,1), B=(1,2,2), AB=(2,1,2). Their multiplication and partition are exhaustively checked from the exact squareclasses.

* **A, modulo 4:** its first equation makes t even. Its second says u3²=2u1² modulo 4, forcing u1 and u3 even. The first then forces u2 even. This contradicts primitivity.
* **AB, modulo 4:** the second equation makes t even. The first gives 2u1²=u2² modulo 4, forcing u1,u2 even. The second then forces u3 even.
* **B, modulo 8:** if t is even, the first equation modulo 2 makes u1 even; the first and second modulo 4 then make u2,u3 even. If t is odd, u1 is odd, and the first equation modulo 8 says 1−2u2²=5, or u2²=2 modulo 4, impossible.

The inverse image of the Q_2 local Kummer image in V is a subgroup containing H. If a member c h of a rejected coset were locally admissible, multiplying by the locally admissible h would make c admissible. This contradicts its exclusion. Thus excluding the representatives really excludes the entire cosets; it is not an inference from cube appearance. Either the exhaustive filter plus rational witnesses or this coset proof gives

    Sel_2 = delta(G) = H,   |G/2G|=8,   Sha[2]=0.

By finite generation G≅Z^r⊕T with T finite. The finite-group kernel/image count gives |T/2T|=|T[2]|=4, since the displayed roots exhaust E[2]. Thus 8=2^r·4 and **rank E(Q)=1**. If a nonzero Sha element were killed by 2^n, its exact order would be 2^j for some j≥1, and multiplication by 2^(j−1) would produce nonzero Sha[2]. Consequently **Sha[2^n]=0 for every n≥1**. This elementary implication does not require total Sha finiteness and says nothing about odd-primary Sha.

## A02: tower coordinates and retained readback

Every nonzero member of K has nontrivial delta. Hence none is a rational double, so there is no rational point of order 4 or higher 2-power order. The 2-primary torsion subgroup is exactly K. Any odd-order torsion disappears in every G/2^nG, since multiplication by 2^n is an automorphism on it.

The class of P is outside the four classes contributed by K. In a decomposition G≅Z⊕T its free coefficient k must therefore be odd: if k were even, its mod-2 class would come from torsion, whose image is precisely K. For every n the map

    Psi_n: (Z/2^n) × K → G/2^nG,
    (m,T) ↦ [mP+T]

is an isomorphism. Multiplication by odd k is invertible modulo 2^n, and K injects because there is no higher 2-primary torsion. These give both surjectivity and injectivity, even if P has a torsion component. Together with Sha[2^n]=0 and S_SELMER,

    Sel_(2^n) ≅ G/2^nG ≅ Z/2^n × (Z/2)^2,
    |Sel_(2^n)|=2^(n+2).

The transition induced by [2]:E[2^(n+1)]→E[2^n] sends the class of the same rational point to its class modulo 2^nG. Indeed, if 2^(n+1)S=R over an algebraic closure, applying [2] to its Kummer cocycle gives the cocycle constructed from 2S, for which 2^n(2S)=R. Thus coordinates reduce as (m,T)↦(m mod 2^n,T). Every level-n class has exactly two level-(n+1) lifts. This transition is not the operation of finding a rational half of R.

For an actual point R, its signature picks the unique (epsilon,T) in {0,1}×K with the same signature. The difference R−epsilon P−T lies in 2G. Choose a rational half R1 and repeat. At step j,

    R_j = epsilon_j P + T_j + 2 R_(j+1).

Substitution gives m=sum(2^j epsilon_j), 0≤m<2^n, and

    R = mP + T_0 + 2^n R_n,

because 2^j T_j=O for j≥1. This proves the readback identity at every finite n. Half choices can change the remainder but not the unique quotient coordinate.

For an affine enabled target S=(x,y), rational roots r_i²=x−e_i yield half abscissas X=x+r1r2+r1r3+r2r3. Choosing r1r2r3=−y gives Y=−y−(r1+r2+r3)(X−x). The four valid sign choices describe all halves (S_HALF). The independent checker instead uses all eight signs to collect abscissas, obtains both candidate ordinates by exact square roots of X³−25X, and keeps those whose chord-law double is S. O has the complete half fiber K. The finite deterministic branch chooses minimum coordinate height; the source program sorts by coordinates.

Fresh evidence contains 112 cases R=mP+T with m in {−3,−1,0,1,2,3,5}, T in K, and n=1,2,3,4. It checks each step, full exact reconstruction, and transition compatibility. A separate search over x=a/b², −80≤a≤200 and 1≤b≤4 tests 951 distinct abscissas and finds 11 affine points; their signatures are in H, with six additional level-4 readbacks. This search is a spot check on the same curve and is not a point-completeness argument.

The oddness of k is sufficient for every binary quotient, but does not prove |k|=1. For example, 3Z maps onto Z/2^n for every n yet is a proper subgroup of Z. Integral generator saturation at odd primes remains unperformed; no such conclusion is smuggled in through the tower.

## C01 and controls: exact representation and lost information

Define a map from F_2^5 to V in bit order (p,t0,tplus,u,v), using generators delta(P), delta(T0), delta(Tplus), A and B. It multiplies the selected signatures componentwise. The map is bijective on all 32 vertices and sends XOR to squareclass multiplication on all 32²=1024 pairs. The independently established admissible subset is H. Pulling that subset back gives u=v=0, whose integer-valued indicator on bit vertices is (1−u)(1−v). The XOR group operation is over F_2; the displayed indicator uses ordinary integer multiplication. They are explicitly different operations.

For K06 use the involutive linear map b3'=b3 XOR b0 and b2'=b2 XOR b4, fixing the other bits. The new encoding is old_encoding composed with its inverse, and the new readout is old_indicator composed with its inverse. All 32 transported readouts and all pair operations agree. Keeping the old readout has eight real mismatches. A concrete witness is old bits (1,0,0,0,0), new bits (1,0,0,1,0): both represent delta(P)=(−1,−1,1), whose correct admissibility is 1; the stale indicator says 0. Thus correct relabeling passes, while failing to transport the receiver produces a false answer.

K01 supplies (0,1); its curve-equation residual is 1. Both the actual addition and signature paths raise an admission error before processing it. This is rejection of a malformed curve point, not failure of an elliptic-curve identity.

For K05 exact doubling gives Q=2P=(1681/144,−62279/1728), with the three square roots 41/12,31/12,49/12. Therefore Q and O share the full level-one coordinate (0,O). Their complete four-point half fibers are respectively P+K and K. Every member of P+K has nontrivial delta, proving Q∉4G. Their full level-two coordinates are respectively (2,O) and (0,O). Retaining R or the level-one remainder recovers the correct answer by the decoder; deleting that backing leaves two possible finer quotient lifts. The finer source-specific choice is OPEN from the coarse label alone, while the complete finer-class fiber is MANY(two), not NONE. Group operations supported by the coarse quotient remain valid.

Likewise delta(P)=delta(−P), with full coordinate (1,O) modulo 2G, but coordinates (1,O) and (3,O) modulo 4G. This is independently checked with exact points and reconstruction.

The eight classes include the identity. A wrapper creates no ninth class. Five coordinate bits, arithmetic rank one, the indicator's displayed degree two, and an analytic Taylor-zero order have separate types and meanings. This construction is a scoped operational quotient and retained reconstruction route; it preserves the supplied C1 correction and does not identify this carrier with the original seven-site C1 quotient or claim to define all of Prestige One. No new shadow or alternation law is inferred.

## Reproduction and correction record

From the experiment directory run:

    python -I -B work/arithmetic_check.py --output evidence/arithmetic.json

The checker uses only Python's standard library and fixed E5 inputs. It does not import the supplied source, read historical result fields, or use arithmetic-rank/backend labels. Reading the supplied proof and source informed the mathematical task; the independently written implementation intentionally uses different residue, squareclass, multiplication and half-point paths.

`evidence/arithmetic_fresh.log` preserves an initial Python syntax error in a control-loop tuple. It occurred before any mathematical execution. That implementation typo was repaired, the successful intermediate run is `evidence/arithmetic_execution.log`, and the final run after strengthening full-coordinate collision assertions is `evidence/arithmetic_execution_final.log`. No failed mathematical claim is being hidden by that distinction. Source hashes identify the executed checker bytes only.

No analytic rank, derivative value, odd-primary Sha result, total Sha order, general BSD theorem or performance advantage is established by this arithmetic file.
