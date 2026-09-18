# Linear triples on $\mathbb{F}_2^3$ and the simplex code

**A short note on which three nonzero linear functionals separate eight vectors, and why the seven-bit evaluation map is the Hamming dual**

*17 September 2026. Self-contained. No prior context assumed.*

---

## Abstract

Let $V = \mathbb{F}_2^3$. There are seven nonzero linear functionals $V \to \mathbb{F}_2$. Of the $\binom{7}{3} = 35$ unordered triples, **exactly 28** give an injective joint map $V \to \mathbb{F}_2^3$. The other seven triples are the sets $\{\,a,\,b,\,a+b\,\}$ — the lines of the Fano plane $\mathrm{PG}(2,2)$.

Evaluating all seven functionals produces an injective map $E \colon V \to \mathbb{F}_2^7$ whose image is the binary simplex code $[7,3,4]$. That image is the orthogonal of the Hamming code $[7,4,3]$. Extending Hamming by one overall-parity bit yields the $[8,4,4]$ code: sixteen words, not thirty-two. The extra coordinate is determined, not free.

None of this is new coding theory. The note records a complete enumeration, a worked failing triple, the orthogonality identity, and the boundary at which the same argument stops being a special count and is only rank. We claim no priority.

---

## 1. The question

Write $V = \mathbb{F}_2^3$ for the eight-element vector space, addition componentwise modulo 2. For each $u \in V$ the map

$$
\ell_u(x) \;=\; u \cdot x \;\in\; \mathbb{F}_2
$$

is linear, and $\ell_u = 0$ if and only if $u = 0$. The seven nonzero functionals are thus labelled by the seven nonzero vectors. A **panel** is an unordered triple of distinct nonzero labels. It determines the joint evaluation

$$
C_{\{u,v,w\}} \colon V \to \mathbb{F}_2^3,\qquad
x \mapsto \bigl(\ell_u(x),\,\ell_v(x),\,\ell_w(x)\bigr).
$$

**Question.** For how many panels is $C$ injective? Equivalently: for how many triples does the $3 \times 3$ matrix with rows $u,v,w$ have full rank?

A natural guess is “all of them”: any three of the seven functionals might seem as good as any other. That guess is false. The rest of the note says exactly how, and how the seven-bit evaluation sits next to the Hamming code.

---

## 2. Rank and fibres

More generally, let $A$ be an $m \times n$ matrix over $\mathbb{F}_2$, viewed as a map $A \colon \mathbb{F}_2^n \to \mathbb{F}_2^m$.

**Proposition 2.1.** For every $y$ in the image of $A$, the fibre $A^{-1}(y)$ is a coset of $\ker A$ and has size $2^{n-\mathrm{rk}\,A}$. In particular $A$ is injective if and only if $\mathrm{rk}\,A = n$.

*Proof.* $Ax = Ax_0$ if and only if $A(x-x_0) = 0$. A basis of the kernel contributes $2^{n-r}$ elements. $\square$

Specialising to $n = 3$ and $m = 3$, a panel separates the eight vectors if and only if its three labels are linearly independent.

---

## 3. Twenty-eight of thirty-five

The group $\mathrm{GL}(3,2)$ has order $(8-1)(8-2)(8-4) = 168$. Each unordered basis is counted $3! = 6$ times among ordered bases, so there are $168/6 = 28$ unordered bases. There are $\binom{7}{3} = 35$ triples of distinct nonzero vectors. Hence **28 panels are injective and 7 are not**.

**Proposition 3.1.** The seven dependent triples are precisely the sets $\{\,a,\,b,\,a+b\,\}$ for distinct nonzero $a,b$.

*Proof.* Three distinct nonzero vectors cannot have rank $0$ or $1$ (a one-dimensional subspace has a single nonzero vector). Dependence therefore means rank $2$. A two-dimensional subspace of $V$ has exactly three nonzero vectors, and for any two of them the third is their sum. The converse is immediate. The number of such lines is $\binom{7}{2}/3 = 7$. $\square$

These seven triples are the lines of the Fano plane $\mathrm{PG}(2,2)$, whose points are the nonzero vectors of $V$.

A complete enumeration of the 35 triples confirms the count and the list. The seven failing triples, writing labels as integers $1,\dots,7$ in the usual bitmask encoding, are

$$
\{1,2,3\},\;
\{1,4,5\},\;
\{1,6,7\},\;
\{2,4,6\},\;
\{2,5,7\},\;
\{3,4,7\},\;
\{3,5,6\}.
$$

---

## 4. A working replacement and a failing one

Fix the standard basis $\{e_1,e_2,e_3\} = \{1,2,4\}$. This panel is injective.

Keep $\{e_1,e_2\}$ and replace $e_3$ by $e_1+e_3 = 5$. The new triple $\{1,2,5\}$ still has rank 3, so it is injective. The third coordinate of the new evaluation is the old third coordinate plus the first; the old third coordinate is recovered by adding the first answer back. This is a change of basis, not a loss of information.

Keep $\{e_1,e_2\}$ and replace $e_3$ by $e_1+e_2 = 3$ instead. The triple $\{1,2,3\}$ is a line. Its joint evaluation has rank 2. The zero fibre is

$$
C^{-1}(0,0,0) \;=\; \{0,\,e_3\} \;=\; \{0,4\}.
$$

The four occupied answer-words each have two preimages; the other four words in $\mathbb{F}_2^3$ do not occur. In particular the third functional is the sum of the first two, so it cannot supply the missing bit.

The same pattern holds with any two independent anchors: exactly four choices of a third label complete a basis (the vectors outside their span), and the newcomer equal to their sum always fails.

---

## 5. Seven evaluations, eight words

Let $H$ be the $3 \times 7$ matrix whose columns are the nonzero vectors of $V$, in the order $1,\dots,7$. Define

$$
E \colon V \to \mathbb{F}_2^7,\qquad
E(x) \;=\; H^{\mathsf T} x \;=\; \bigl(\ell_u(x)\bigr)_{u \ne 0}.
$$

**Proposition 5.1.** $E$ is injective. Its image $S$ is an $[7,3,4]$ linear code: eight words, minimum distance four, every nonzero word of weight four. Moreover $S = C^{\perp}$, where $C = \ker H$ is the Hamming code $[7,4,3]$.

*Proof.* $H$ contains the three standard-basis columns, so $\mathrm{rk}\,H = 3$ and $E$ is injective. Thus $|S| = 8$. For $x \ne 0$ the functional $u \mapsto u\cdot x$ takes the value $1$ on exactly four of the eight vectors of $V$; one of those eight is $u = 0$, which is not a column, so $\mathrm{wt}(E(x)) = 4$. Differences of distinct words of $S$ are nonzero words of $S$, so the minimum distance is 4.

For the duality: $z \in S^{\perp}$ if and only if $(H^{\mathsf T}x)\cdot z = 0$ for every $x \in V$, if and only if $x \cdot (Hz) = 0$ for every $x$, if and only if $Hz = 0$, if and only if $z \in C$. The standard dot product is nondegenerate, so taking orthogonals gives $S = C^{\perp}$. Then $|C| = 2^{7-3} = 16$. $\square$

This is the binary simplex code of length 7, the dual of the Hamming code of length 7. Hamming's original paper constructs $C$ by taking the same seven nonzero columns as parity checks: a single-bit error is the unique column equal to the syndrome $Hy$, and a double error on positions $a,b$ produces the same syndrome as the single error $a+b$. The seven weight-three codewords of $C$ are supported on exactly the seven lines of Proposition 3.1. That is the same Fano geometry, read as error positions rather than as functionals.

Matching the number seven does not by itself prove duality. The displayed identity $S^{\perp} = \ker H$ does.

Under the promise of at most one error, the syndrome $Hy$ locates the error: $Hy = 0$ means no error, and each nonzero column of $H$ occurs once, so it names a unique position. Two errors at distinct positions $a,b$ produce syndrome $a+b$, which is also a single column. A decoder that assumes at most one error will therefore “correct” a third position and land on a different Hamming word. That is the usual double-error alias; it is not a failure of the 28/35 count, which did not promise error correction.

---

## 6. An eighth coordinate that is not a free bit

Append to each $c \in C$ the bit $p = \mathrm{wt}(c) \bmod 2$. The image $C_8 \subset \mathbb{F}_2^8$ is the extended Hamming code $[8,4,4]$. The map $c \mapsto (c,p)$ is bijective onto its image, so $|C_8| = 16$. The extra bit is a function of the first seven.

A different construction *does* double a four-element set to eight: if $U \subset V$ is a two-dimensional subspace and $c \notin U$, then $U \cup (c+U)$ is all of $V$. That is an independent coordinate on the *source*. It is not the parity extension of $C$.

Three objects that share the numeral eight are therefore distinct:

| Object | What is counted | Size |
|---|---|---:|
| Image of $E$ | words of the simplex code | 8 |
| Extended Hamming code $C_8$ | messages | 16 |
| Block length of $C_8$ | coordinates | 8 |
| $U \cup (c+U)$ for $c \notin U$ | source vectors | 8 |

In particular, Hamming-8 does not have 32 words. Treating the parity bit as a free source coordinate would predict 32; that prediction is false.

The same glyphs can also be misread across types. The failing panel $\{1,2,3\}$ is a set of *functionals*. The vector $1+2 = 3$, read as a *source* translation, lies in the plane $U = \mathrm{span}\{1,2\} = \{0,1,2,3\}$ and does not enlarge $U$. Linear dependence of checks and failure of a source translation are different statements that happen to use the same three bits.

---

## 7. What does not lift

Proposition 2.1 did not use $n = 3$. On $V_n = \mathbb{F}_2^n$ a list of linear functionals separates $V_n$ if and only if their labels span $V_n$. For $n = 4$ there are fifteen nonzero labels and $\binom{15}{4} = 1365$ unordered quadruples. The injective ones are the unordered bases, of which there are

$$
\frac{|\mathrm{GL}(4,2)|}{4!} \;=\; \frac{15\cdot 14\cdot 12\cdot 8}{24} \;=\; 840.
$$

A complete check of the 1365 quadruples confirms injectivity if and only if rank equals 4. The quadruple $\{1,2,3,4\}$ — the Fano line $\{1,2,3\}$ plus one new coordinate — has rank 3; its zero fibre is $\{0,8\}$.

That census is a count of bases. It is not a second theorem, and the Fano list of seven lines does not survive unchanged (525 quadruples fail, not 7). The special content at $n = 3$ is that a dependent *triple* of nonzero vectors is forced to be a line, so the failures have a one-line description and coincide with the Hamming weight-three supports. At $n = 4$ a dependent quadruple can have rank 1, 2, or 3, and the geometry is larger.

Panels of size at least four on $V_3$ are automatically spanning, because a proper subspace contains at most three nonzero vectors. That is again rank, plus the same subspace count used in Proposition 3.1.

---

## 8. Evidence grades

The statements are not all of one kind.

| Statement | Grade |
|---|---|
| Proposition 2.1 | Written linear algebra, any $n$ |
| $28$ of $35$; Proposition 3.1 | Written ($|\mathrm{GL}(3,2)|/3!$ and the $2$-flat count); confirmed by complete enumeration of the $35$ triples |
| The seven listed triples | Complete finite list |
| Section 4, fibres of $\{1,2,5\}$ and $\{1,2,3\}$ | Exact evaluation on eight vectors |
| Proposition 5.1 | Written; $|S|$, weights, and $S = C^{\perp}$ confirmed by enumerating the eight values of $E$ and the $128$ words of $\mathbb{F}_2^7$ |
| $|C_8| = 16$ | Written (determined parity); confirmed by enumerating the sixteen Hamming words and their extensions |
| $U \cup (c+U) = V$ iff $c \notin U$ | Written; checked for $U = \{0,1,2,3\}$ with $c = 4$ and $c = 3$ |
| Section 7, $840$ of $1365$ | Derived from $\|\mathrm{GL}(4,2)\|$; confirmed by complete enumeration of the $1365$ quadruples. **Not an independent theorem** |
| “Not found as a new coding theorem” | These objects are in Hamming (1950) and in any standard account of the simplex code. This note claims no priority |

All checks are exact bit operations. A matching count does not prove the written identities; the identities are the proofs, and the enumerations are finite confirmations on the stated carriers.

---

## References

1. R. W. Hamming, *Error detecting and error correcting codes*, Bell System Technical Journal **29** (1950), 147–160.
2. F. J. MacWilliams and N. J. A. Sloane, *The Theory of Error-Correcting Codes*, North-Holland, 1977. The binary simplex and Hamming codes, and the duality $S = C^{\perp}$, are standard; see e.g. Ch. 1 and the tables of best codes.
3. J. H. van Lint, *Introduction to Coding Theory*, 3rd ed., Springer, 1999. Fano geometry of the Hamming code of length 7.

We did not rely on a claim of absence from the coding-theory literature. The constructions above are the usual ones.
