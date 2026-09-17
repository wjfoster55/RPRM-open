# Extremal partition shapes for the order of $T(X,\mathcal{P})$

**A note on which partition shape admits the most partition-preserving transformations**

*17 September 2026. Self-contained. No prior context assumed.*

---

## Abstract

Let $X$ be a finite set with $|X| = n$ and let $\mathcal{P}$ be a partition of
$X$ into $m$ blocks. Sarkar and Singh (2021) computed the order of the monoid
$T(X,\mathcal{P})$ of partition-preserving full transformations for an arbitrary
finite partition. That order depends only on the multiset of block sizes, so it
is a function of the *shape* of $\mathcal{P}$ — a partition of $n$ into $m$
parts. We ask which shape maximises and which minimises it.

We prove that for fixed $n$ and fixed $m \ge 2$, the order is **strictly
increasing along the dominance order** on shapes. Consequently it is uniquely
maximised at the most unequal shape $(n-m+1, 1, \dots, 1)$ and uniquely minimised
at the balanced shape. The same statement and the same proof hold for the natural
$r$-ary generalisation at every arity $r \ge 1$, and for the submonoid of partial
maps whose domain is a union of blocks.

The proof is short. The order is a product of factors $\sum_j n_j^{\,k}$, and the
shape enters twice: once as the **bases** $n_j$, and once as the **exponents**
$k = n_i$ at which those factors are evaluated. Separating the two roles, the
base dependence is handled by Karamata's inequality and the exponent dependence
by log-convexity of sums of exponentials. Both steps move the same way under a
dominance-increasing exchange.

We also record a **negative result that delimits the phenomenon**. The analogous
count for partial transformations *without* a condition on the domain — the
object of Cicalò, Fernandes and Schneider (2012) — has factor function
$\sum_j (n_j+1)^k - (m-1)$, a sum of exponentials *minus* a positive constant.
Subtracting a constant does not preserve log-convexity, the proof fails, and the
extremal law is **false**: at $n = 11$, $m = 9$ the maximiser and minimiser
exchange places.

We claim no priority. Section 7 records what was and was not found in the
literature, and which unobtained papers could overturn that.

---

## 1. The object

Let $X$ be a finite set, $|X| = n$, and let $\mathcal{P} = \{X_1, \dots, X_m\}$
be a partition of $X$ into nonempty blocks, $|X_i| = n_i$. Write
$p = (n_1, \dots, n_m)$, a partition of $n$ into exactly $m$ positive parts; we
call $p$ the **shape** of $\mathcal{P}$ and always list it in weakly decreasing
order.

Following Pei, a map $f \in \mathcal{T}_X$ **preserves** $\mathcal{P}$ if for
every block $X_i$ there is a block $X_j$ with $X_i f \subseteq X_j$; equivalently
$x \sim_{\mathcal{P}} y \implies xf \sim_{\mathcal{P}} yf$. The two formulations
coincide for total maps, a point stated explicitly by Araújo and Schneider. Write

$$
T(X,\mathcal{P}) = \{\, f \in \mathcal{T}_X : (\forall X_i)(\exists X_j)\ X_i f \subseteq X_j \,\},
$$

a submonoid of $\mathcal{T}_X$.

**Proposition 1.1 (Sarkar–Singh, 2021, Thm. 6.1).**
$$
|T(X,\mathcal{P})| \;=\; \prod_{i=1}^{m} \; \sum_{j=1}^{m} n_j^{\,n_i}.
$$

*Remark.* Sarkar and Singh state this grouped by size classes, as
$\prod_{i} \big( \sum_j m_j n_j^{n_i} \big)^{m_i}$ where there are $m_i$ blocks of
size $n_i$. The two forms are equal; regrouping over individual blocks is more
convenient here. The formula is immediate: each block $X_i$ independently chooses
a target block $X_j$ and then an arbitrary map $X_i \to X_j$, of which there are
$n_j^{\,n_i}$.

Since the right-hand side depends only on $p$, we write $\tau(p)$ for it.

### The $r$-ary version

For $r \ge 1$ call an operation $f : X^r \to X$ **partition-preserving** if for
every ordered $r$-tuple of blocks $T = (X_{i_1}, \dots, X_{i_r})$ there is a block
$X_j$ with $f(X_{i_1} \times \cdots \times X_{i_r}) \subseteq X_j$. The same
count applies with the product block $\prod_{i \in T} n_i$ in place of $n_i$:

$$
\tau_r(p) \;=\; \prod_{T} \; \sum_{j=1}^{m} n_j^{\,e_T},
\qquad e_T = \prod_{i \in T} n_i ,
$$

the product running over all $m^r$ ordered $r$-tuples. At $r = 1$ this is
Proposition 1.1. At $r = 0$ there is a single input tuple and
$\tau_0(p) = n$ independent of the shape, so $r \ge 1$ is required throughout.

---

## 2. The question, and an example

$\tau_r$ is a function on the set of partitions of $n$ into exactly $m$ parts.
That set carries the **dominance** (majorisation) order: $q \succeq p$ when
$\sum_{i \le t} q_i \ge \sum_{i \le t} p_i$ for every $t$, with equal totals. Its
unique maximum is $(n-m+1, 1, \dots, 1)$ and its unique minimum is the balanced
shape, with parts differing by at most one.

**Question.** How does $\tau_r$ behave along this order?

All five shapes of $n = 8$ into $m = 3$ blocks, listed in decreasing dominance
order:

| shape | $\tau(p) = \lvert T(X,\mathcal{P})\rvert$ |
|---|---:|
| $(6,1,1)$ | 2,986,112 |
| $(5,2,1)$ | 757,920 |
| $(4,3,1)$ | 248,768 |
| $(4,2,2)$ | 165,888 |
| $(3,3,2)$ | 84,568 |

Monotone, and the spread is not marginal. The ratio between extremes grows
quickly:

| $n$ | $m$ | argmax | argmin | ratio |
|---:|---:|---|---|---:|
| 8 | 3 | $(6,1,1)$ | $(3,3,2)$ | $35.3$ |
| 10 | 4 | $(7,1,1,1)$ | $(3,3,2,2)$ | $249$ |
| 12 | 4 | $(9,1,1,1)$ | $(3,3,3,3)$ | $4.92 \times 10^{3}$ |
| 16 | 8 | $(9,1^7)$ | $(2^8)$ | $9.46 \times 10^{4}$ |
| 20 | 10 | $(11,1^9)$ | $(2^{10})$ | $1.39 \times 10^{7}$ |

---

## 3. The exchange lemma

Everything follows from a single local move.

**Definition.** Let $p$ be a shape containing parts $a$ and $b$ with
$a \ge b \ge 2$. The **exchange** at $(a,b)$ replaces them by $a+1$ and $b-1$,
producing a shape $q$ of the same $n$ with the same number of parts. Requiring
$b \ge 2$ keeps the part from vanishing.

These moves generate the dominance order: $q \succ p$ if and only if $q$ is
reachable from $p$ by a sequence of such exchanges, and every covering relation is
of this form.

**Theorem 3.1 (Exchange lemma).** *For every $r \ge 1$ and every exchange with
$a \ge b \ge 2$,*
$$
\tau_r(q) \;>\; \tau_r(p).
$$

**Corollary 3.2 (Extremal shapes).** *For fixed $n$ and $m \ge 2$, $\tau_r$ is
strictly increasing along the dominance order. It attains a unique maximum at
$(n-m+1,1,\dots,1)$ and a unique minimum at the balanced shape.*

*Proof of the corollary from the theorem.* A shape that is not balanced has two
parts differing by at least $2$, so it admits a reverse exchange strictly
decreasing $\tau_r$; iterating terminates at the balanced shape. A shape other
than $(n-m+1,1,\dots,1)$ has a non-largest part of size at least $2$, so it admits
a forward exchange strictly increasing $\tau_r$; iterating terminates there.
Uniqueness is uniqueness of the extremes of the dominance order. $\square$

Note that "unique" means a unique **shape**, not a unique labelled partition of
$X$.

---

## 4. Proof of the exchange lemma

### 4.1 The two roles of the shape

Write $S_k(p) = \sum_{j} n_j^{\,k}$ and

$$
\tau_r(p) = \prod_{T} S_{e_T}(p) .
$$

The shape appears twice, and this is the whole difficulty: it supplies the
**bases** $n_j$ inside $S_k$, and it supplies the **exponents** $e_T$ at which
$S_k$ is evaluated. An exchange changes both simultaneously. Attempts to compare
$\tau_r(q)$ with $\tau_r(p)$ term by term fail because the two effects are
entangled. The proof is to separate them and show that they move the same way.

### 4.2 Step 1: the bases

**Lemma 4.1.** *If $q \succ p$ then $S_k(q) \ge S_k(p)$ for every $k \ge 1$, with
equality iff $k = 1$.*

*Proof.* $x \mapsto x^k$ is convex on $[0,\infty)$ and strictly convex for
$k \ge 2$. Karamata's inequality applied to $q \succ p$ gives
$\sum_j q_j^k \ge \sum_j p_j^k$, strictly for strictly convex $x^k$ when the two
multisets differ. At $k=1$ both sides equal $n$. $\square$

Hence $S_k(q) \ge S_k(p)$ **pointwise in $k$**, which is what lets the spectator
factors be handled with no estimate at all.

### 4.3 Step 2: the exponents

**Lemma 4.2.** *For any fixed shape $q$, the function $k \mapsto S_k(q)$ is
log-convex on $\mathbb{R}$.*

*Proof.* $S_k(q) = \sum_j e^{k \ln q_j}$ is a sum of exponentials with positive
coefficients. For such a function, $(\ln S)''(k)$ is the variance of the values
$\ln q_j$ under the probability weights $q_j^k / S_k$, hence nonnegative.
$\square$

This is the only analytic input in the argument, and it is worth being precise
about what it does and does not require. A constant term is harmless: a constant
$c$ equals $c \cdot 1^k$, another exponential with positive coefficient and base
$1$. So $1 + S_k$ is log-convex exactly as $S_k$ is, and neither the presence nor
the absence of a constant term matters. What matters is that **every** term is a
positive multiple of an exponential. Section 6 shows what goes wrong when one is
not.

**Lemma 4.3.** *Let $f$ be log-convex and positive, and let $a \ge b$. Then
$f(a+1) f(b-1) \ge f(a) f(b)$.*

*Proof.* $h = \ln f$ is convex, so $h'$ is nondecreasing in the sense that
increments over intervals further right are larger. Since $a \ge b$, the interval
$[a, a+1]$ lies weakly to the right of $[b-1, b]$, whence
$h(a+1) - h(a) \ge h(b) - h(b-1)$. Rearranging and exponentiating gives the
claim. $\square$

### 4.4 Step 3: arity one

Let $q$ be obtained from $p$ by the exchange at $(a,b)$. Then

$$
\tau(q) = \Big( \prod_{c} S_c(q) \Big) \cdot S_{a+1}(q) \, S_{b-1}(q),
$$

where $c$ runs over the parts of $p$ other than the chosen occurrences of $a$ and
$b$ — the **spectators**, which are the same for $p$ and $q$. Now

$$
\tau(q)
\;\ge\; \Big( \prod_{c} S_c(q) \Big) S_a(q)\, S_b(q)
\;>\; \Big( \prod_{c} S_c(p) \Big) S_a(p)\, S_b(p)
\;=\; \tau(p),
$$

the first inequality by Lemmas 4.2 and 4.3 applied to $f = S_\bullet(q)$, the
second by Lemma 4.1 applied factor by factor. The second inequality is
**strict**: the factor at exponent $a$ satisfies $a \ge 2$, where Lemma 4.1 is
strict. So no equality case can arise even if Step 2 is an equality. $\blacksquare$

### 4.5 Step 4: every arity, by tensoring

At arity $r$ the exponents are the products $e_T$, and Step 2 must be replaced by

$$
\sum_T \varphi(e_T(q)) \;\ge\; \sum_T \varphi(e_T(p)) \qquad \text{for all convex } \varphi. \tag{$*$}
$$

By Karamata, $(*)$ holds as soon as the exponent multiset $\{e_T(q)\}$ majorises
$\{e_T(p)\}$. It does, and the reason is clean.

**Lemma 4.4.** *If $q \succ p$ then $\{e_T(q)\}_T \succeq \{e_T(p)\}_T$ for every
$r \ge 1$.*

*Proof.* By Birkhoff–von Neumann, $q \succ p$ gives a doubly stochastic matrix $D$
with $p = Dq$. Then $p^{\otimes r} = D^{\otimes r} q^{\otimes r}$, and a Kronecker
product of doubly stochastic matrices is doubly stochastic. The coordinates of
$p^{\otimes r}$, indexed by ordered $r$-tuples, are exactly the products $e_T$.
A vector obtained from another by a doubly stochastic matrix is majorised by it.
$\square$

Applying $(*)$ with $\varphi = \ln S_\bullet(q)$, convex by Lemma 4.2, gives
$\prod_T S_{e_T(q)}(q) \ge \prod_T S_{e_T(p)}(q)$, and Lemma 4.1 finishes as
before. Strictness again comes from the all-$a$ tuple, whose exponent $a^r \ge 2$.
$\blacksquare$

*Remark.* A cellwise argument in the convex order also works — condition on which
coordinates of the tuple land in the changed blocks, use closure of the convex
order under multiplication by independent nonnegative factors, and sum over cells.
It is longer. It is worth mentioning only because majorisation is **not** additive
across such a decomposition while the inequality $(*)$ is, so the cellwise route
must be phrased in the convex order; the tensor route above avoids the issue by
never decomposing.

---

## 5. The partial-map submonoid with block-saturated domain

Let $PT_{\mathcal{P}}^{\,\mathrm{sat}}(X)$ denote the partial maps $t$ that
preserve $\mathcal{P}$ in the sense of Section 1 wherever defined **and** whose
domain is a union of blocks. This is a submonoid: if $s$ sends block $B$ into
block $B'$, then $B'$ is wholly inside or wholly outside $\operatorname{dom} t$,
so $B$ survives or dies as a unit. Its idempotent partial identities are the
$\operatorname{id}_D$ for $D$ a union of blocks, forming a semilattice isomorphic
to the Boolean lattice $2^m$; it is a left restriction submonoid of $PT_X$.

**Proposition 5.1.**
$\displaystyle \big|PT_{\mathcal{P}}^{\,\mathrm{sat}}(X)\big| = \prod_{i=1}^{m} \Big( 1 + \sum_{j=1}^{m} n_j^{\,n_i} \Big).$

*Proof.* Each block independently is either wholly undefined, one way, or picks a
target block and an arbitrary map into it. $\square$

**Proposition 5.2 (reduction to Proposition 1.1).** *Adjoin a point $*$ and set
$\mathcal{P}' = \mathcal{P} \cup \{\{*\}\}$ on $X \cup \{*\}$. The bijection
"undefined $\mapsto *$" identifies $PT_{\mathcal{P}}^{\,\mathrm{sat}}(X)$ with the
stabiliser of $*$ in $T(X \cup \{*\}, \mathcal{P}')$. Hence*
$$
\big|PT_{\mathcal{P}}^{\,\mathrm{sat}}(X)\big| \;=\; \frac{\big|T(X \cup \{*\},\, \mathcal{P}')\big|}{\,n+1\,}.
$$

*Proof.* Under the bijection a block either maps into a block of $\mathcal{P}$ or
is sent wholesale to $*$, and $\{*\}$ is itself a block of $\mathcal{P}'$ — so
block-saturation of the domain is exactly what makes the extended map
partition-preserving. The block $\{*\}$ has $n+1$ possible images, of which one
fixes $*$. $\square$

So Proposition 5.1 is a corollary of Proposition 1.1, not an independent count.
Its factor function $1 + S_k$ is a sum of exponentials, so Theorem 3.1 and
Corollary 3.2 apply verbatim, at every arity.

*Terminology.* The domain condition — if a point lies in the domain, so does its
whole block — is not new. It appears in the literature on inverse semigroups as
**$\mathcal{P}$-stability**, for *injective, order-preserving* partial maps; see
Section 7 for the attribution and its evidential status.

---

## 6. A negative result: what happens without the domain condition

Drop the condition on the domain and keep only agreement on successors where
defined. This is the monoid $PT_E$ of Cicalò, Fernandes and Schneider, whose
order for a **uniform** partition into $m$ blocks of size $n$ they give as
$\big(m(n+1)^n - m + 1\big)^m$. For an arbitrary shape the same reasoning gives

$$
\beta(p) \;=\; \prod_{i=1}^{m} \Big( 1 + \sum_{j=1}^{m} \big[ (n_j+1)^{n_i} - 1 \big] \Big)
\;=\; \prod_{i=1}^{m} \Big( \sum_{j=1}^{m} (n_j+1)^{n_i} - (m-1) \Big).
$$

The factor function is now a sum of exponentials **minus a positive constant**.
That is precisely the hypothesis of Lemma 4.2 failing: adding a positive constant
is harmless because a constant is an exponential with base $1$, but subtracting
one is not, because $-c$ is not a positive multiple of an exponential.

**Example 6.1.** At $p = (1,1)$ the factor function is $2^{k+1} - 1$, so
$f(1), f(2), f(3) = 3, 7, 15$ and
$$
f(1) f(3) = 45 \;<\; 49 = f(2)^2 ,
$$
so $f$ is not log-convex.

And the conclusion fails with it.

**Example 6.2 (the extremal law is false for $\beta$).** At $n = 11$, $m = 9$,
$$
\beta(3,1^8) = 120 \cdot 12^8 = 51{,}597{,}803{,}520,
\qquad
\beta(2,2,1^7) = 38^2 \cdot 12^7 = 51{,}741{,}130{,}752 .
$$
The two shapes are comparable in dominance with $(3,1^8) \succ (2,2,1^7)$, yet
$\beta$ is larger at the *less* unequal one. Since $\tau$ and $\big|PT^{\mathrm{sat}}\big|$
are both maximised at $(3,1^8)$ and minimised at $(2,2,1^7)$ in this cell, the
maximiser and minimiser **exchange places** when the domain condition is dropped.

**Controlled comparison.** Holding the bases fixed at $n_j + 1$ and deleting only
the subtracted constant isolates the cause. Over all shapes with $n \le 26$
(42,903 distinct exchanges) and log-convexity probes over all shapes with
$n \le 12$ (1,482 instances):

| factor function | log-convexity failures | exchange-lemma failures |
|---|---:|---:|
| $\sum_j (n_j+1)^k$ — no subtraction | 0 / 1,482 | 0 / 42,903 |
| $\sum_j (n_j+1)^k - (m-1)$ — the monoid $PT_E$ | 292 / 1,482 | 66 / 42,903 |
| $\sum_j n_j^k$ — Proposition 1.1 | 0 / 1,482 | 0 / 42,903 |
| $1 + \sum_j n_j^k$ — Proposition 5.1 | 0 / 1,482 | 0 / 42,903 |

Rows 1 and 2 differ only by the subtraction and differ in outcome; rows 3 and 4
differ only by an added constant and do not.

**The implication runs one way only.** Failure of log-convexity at the exchanged
exponents is *necessary* for an exchange to fail — across all 42,903 exchanges,
every one of the 66 losses lies among the 3,871 log-convexity failures, and none
outside. It is far from sufficient: only $66/3871 \approx 1.7\%$ of log-convexity
failures produce an actual loss, since the spectator factors can absorb the
deficit. A characterisation of the failing cells is **open**.

---

## 7. Position in the literature

### 7.1 What is known

| Source | Object | Total/partial | Domain condition | Result |
|---|---|---|---|---|
| Pei, *Semigroup Forum* **49** (1994), 49–58 | introduces $T_E(X)$ | total | — | lattices of $T$-equivalences, $\alpha$-congruences; **no cardinality** |
| Araújo–Schneider, arXiv:0807.1214 | $T(X,\mathcal{P})$, uniform | total | — | rank |
| Araújo–Bentz–Mitchell–Schneider, arXiv:1404.1598 | $T(X,\mathcal{P})$, arbitrary | total | — | rank, as a function of shape |
| Dolinka–East, *Comm. Algebra* **44** (2016) | $T(X,\mathcal{P})$, **uniform** | total | — | **enumerates the idempotents**; also idempotent-generated submonoid, rank |
| Dolinka–East–Mitchell, *Bull. Aust. Math. Soc.* **93** (2016) | $T(X,\mathcal{P})$, **non-uniform** | total | — | rank and idempotent rank of $\langle E \rangle$ — **not** an idempotent count |
| Cicalò–Fernandes–Schneider, arXiv:1210.4775 | $PT_E$, **uniform** | partial | none | order $\big(m(n+1)^n-m+1\big)^m$ |
| **Sarkar–Singh**, *Comm. Algebra* **49** (2021), 331–342 | $T(X,\mathcal{P})$, **arbitrary** | total | — | **order**; our Proposition 1.1 |
| Pei–Zhou, *Adv. Math. (China)* (2009) | $P_E(X)$, arbitrary $E$ | partial | none | Green's relations, regularity; **no cardinality** |
| Fernandes, *Semigroup Forum* **56** (1998), 418–433 | normally ordered inverse semigroups | partial, injective | union of blocks | origin of $\mathcal{P}$-stability |
| Caneco–Fernandes–Quinteiro, arXiv:1905.11489 | $POI_{k\times m}$ | partial, injective | union of blocks | order, rank, presentation |
| Sun, *Bull. Malays. Math. Sci. Soc.* **36** (2013), 179–192 | $OP_E(X)$, **uniform** | total | — | order and idempotent count |

### 7.2 What was not found

**No extremal or majorisation result for the order of any of these monoids as a
function of partition shape.** The literature studies **rank** as a function of
shape — Araújo–Bentz–Mitchell–Schneider give the exact rank of $T(X,\mathcal{P})$
for arbitrary $\mathcal{P}$ — and computes **order** only for a partition that is
fixed in advance.

There is a structural reason, and it is worth stating because it explains the
absence without appealing to novelty. **Almost the entire literature on these
monoids assumes a uniform partition.** Cicalò–Fernandes–Schneider,
Araújo–Schneider, Caneco–Fernandes–Quinteiro, Fernandes–Quinteiro and Sun all fix
$m$ blocks of size $n$ by hypothesis; under that hypothesis the shape is
determined by $(m,n)$ and the extremal question cannot be posed. The order for an
arbitrary shape appears to have become available only with Sarkar–Singh in 2021.
The question asked here is a natural one to ask of that formula, and we do not
claim to be the first to ask it — only to record that a search did not find it
asked.

Searches returning nothing relevant: "saturated domain", "block-saturated",
"$\mathcal{P}$-saturated" partial transformations; partition-preserving combined
with non-uniform; extremal or Schur-convexity results for transformation-monoid
orders. The extremal literature that surfaces on these terms — Hwang–Rothblum and
related work on Schur-convex bounded-shape partition problems — concerns
partitioning *numbers*, not counting partition-preserving maps. **OEIS**: no
hits for the value sequences of $\tau$ or of Proposition 5.1, nor for
Cicalò–Fernandes–Schneider's own published table; the only match is A014566
($n^n+1$), the degenerate one-block case.

### 7.3 Papers not obtained, and what would overturn the above

Honesty about sources is part of the claim. Three papers were sought and the
outcomes differ:

| Paper | Outcome | Bearing |
|---|---|---|
| **Sun 2013**, BMMS 36(1), 179–192 | **Obtained in full** (open access, EMIS). Counts $OP_E(X)$, $O_E(X)$ and their idempotents for a **uniform** partition, with Fibonacci numbers $F_{2n}$ in the idempotent formulas. No shape dependence, no extremal statement | Does not overturn |
| **Pei 1994**, *Semigroup Forum* 49, 49–58, DOI 10.1007/BF02573470 | **Not obtained** — Springer paywalled, EuDML copy unreachable. **zbMATH review obtained in full** (Zbl 0804.20046), which quotes the definition $T_E(X) = \{f \in \mathcal{T}_X : (f(a),f(b)) \in E \ \forall (a,b) \in E\}$ and summarises the contents as lattices of $T$-equivalences and $\alpha$-congruences | Low risk. The reviewed content contains no cardinality of any kind |
| **Fernandes 1998**, *Semigroup Forum* **56**, 418–433, DOI 10.1007/PL00005955 | **Not obtained.** No preprint; the author's own publication page lists the citation without a file | **The attribution of $\mathcal{P}$-stability to this paper is not verified from the primary source.** It rests on the restatement in Caneco–Fernandes–Quinteiro, arXiv:1905.11489 |

An earlier draft of this note cited Fernandes 1998 as volume 58; the author's
publication page and the DOI record both give **volume 56**, and that is used
above.

**What would overturn "no published extremal result".** A counting result in the
Chinese-language literature on these semigroups — *Advances in Mathematics
(China)*, *J. Guizhou Normal Univ.*, *Xinyang Normal Univ. J.* — which is poorly
indexed and was largely inaccessible; the Pei–Zhou 2009 full text, of which only
a database abstract was read; or any treatment of $T(X,\mathcal{P})$ for
non-uniform $\mathcal{P}$ predating Sarkar–Singh.

---

## 8. Coverage boundary

The theorem is a statement about a specific counting measure, and it is false for
several natural neighbours. These are recorded because they delimit it.

| Class of operations counted | Extremal law |
|---|---|
| All maps $X^r \to X$, $r \ge 1$ (Prop. 1.1 and its $r$-ary form) | **Theorem 3.1** |
| Partial maps with block-saturated domain (Prop. 5.1) | **Theorem 3.1** |
| Nullary, $r = 0$ | Vacuous: $\tau_0 = n$, shape-independent |
| Partial maps, no domain condition ($PT_E$) | **False.** Example 6.2 |
| Bijections only | **False** for the minimum. At $n=4$, $m=2$, the shape $(2,2)$ admits 8 partition-preserving permutations against 6 for $(3,1)$ |
| Maps of a prescribed domain size | **False.** At $n=6$, $m=3$, domain size 4, the shape $(2,2,2)$ admits 432 against 258 for $(4,1,1)$ |
| Idempotents only | **Open** — see below |

### The idempotent case

For idempotent partial maps with block-saturated domain, write
$S_i = \operatorname{Fix}(t) \cap X_i$. A block carrying fixed points must target
*itself*, since its fixed points map to themselves; a fixed-point-free block in
the domain may target any block that carries some. Hence

$$
\sigma^{\mathrm{idem}}(p) = \sum_{D,\,(s_i)_{i \in D}} \ \prod_{i \in D} \binom{n_i}{s_i}
\cdot \!\!\prod_{\substack{i \in D \\ s_i \ge 1}}\!\! s_i^{\,n_i - s_i}
\cdot \!\!\prod_{\substack{i \in D \\ s_i = 0}}\!\! \Big( \sum_{\substack{j \in D \\ s_j \ge 1}} s_j^{\,n_i} \Big),
$$

validated against exhaustive enumeration for all 29 shapes with $n \le 6$.

**Priority.** For the *total* maps and a **uniform** partition this count is
published: Dolinka and East (2016) enumerate the idempotents of $T(X,\mathcal{P})$
and tabulate $|E(T(X,\mathcal{P}))|$. Specialising the formula above to a full
domain reproduces **all ten** of their tabulated values exactly, from
$|E| = 41$ at $(m,n) = (4,1)$ to $977{,}698{,}734{,}939{,}376$ at $(5,5)$. We
claim nothing new for the uniform case.

For a **non-uniform** partition the sequel — Dolinka, East and Mitchell (2016) —
computes the rank and idempotent rank of the subsemigroup *generated by* the
idempotents, which is a different invariant from how many idempotents there are.
So the pattern of §7.2 recurs exactly here: where this literature goes
non-uniform it computes rank, and where it computes a count it fixes the
partition uniform.

The last bracket is the obstruction to extending Section 4: a fixed-point-free
block's factor depends on which *other* blocks carry fixed points. The count is a
sum over configurations, not a product of per-block factors, so there is no
factor function for log-convexity to be a property of, and the method has nothing
to act on. The extremal law nevertheless holds in every case computed (719
exchanges, $n \le 14$). We state it as a conjecture and note that a proof would
need a different mechanism.

---

## 9. Evidence grades

Stated separately, because the statements here are not all of the same kind.

| Statement | Grade |
|---|---|
| Proposition 1.1 | Published (Sarkar–Singh 2021). Independently checked here against exhaustive enumeration for all shapes with $n \le 6$ |
| Propositions 5.1, 5.2 | Written proof; the identity of 5.2 verified exactly for all 507 shapes with $n \le 14$ |
| Theorem 3.1, Corollary 3.2 | **Written proof**, not formalised. Every step machine-checked in exact integer arithmetic: arity 1 over 128,121 exchanges on 28,622 shapes; arities 2–5 for the majorisation step; direct verification of the conclusion at arities 1–4 |
| Independent audit | An independent reviewer confirmed the proof on the stated domain and rejected three surrounding explanatory claims, since corrected; in particular an earlier draft wrongly asserted that the constant term is essential to Lemma 4.2 |
| Examples 6.1, 6.2 and the table in §6 | Exact finite computation, complete enumeration in the stated ranges |
| Coverage boundary rows | Exact counterexamples, retained |
| Idempotent formula | Written derivation; exhaustive validation $n \le 6$; and the full-domain uniform case reproduces all ten published values of Dolinka–East |
| Idempotent extremal law | **Conjecture**, finite test only |
| §7.2, "not found in the literature" | **A recorded search outcome, not a novelty claim.** §7.3 lists what was not read and what would overturn it |

All computations are in exact integer or rational arithmetic; no floating point
is used in any verification. Reproduction scripts accompany this note.

---

## References

1. J. Araújo, W. Bentz, J. D. Mitchell, C. Schneider, *The rank of the semigroup of transformations stabilising a partition of a finite set*, Math. Proc. Cambridge Philos. Soc. **159** (2015). arXiv:1404.1598.
2. J. Araújo, C. Schneider, *The rank of the endomorphism monoid of a uniform partition*, Semigroup Forum **78** (2009). arXiv:0807.1214.
3. I. Dolinka, J. East, *Idempotent generation in the endomorphism monoid of a uniform partition*, Comm. Algebra **44** (2016), 5179–5198. arXiv:1407.3312.
4. I. Dolinka, J. East, J. D. Mitchell, *Idempotent rank in the endomorphism monoid of a non-uniform partition*, Bull. Aust. Math. Soc. **93** (2016), 73–91. arXiv:1504.02520.
5. A. Caneco, V. H. Fernandes, T. M. Quinteiro, *On the monoid of partial isometries / $\mathcal{P}$-stable $\mathcal{P}$-order-preserving partial permutations*. arXiv:1905.11489.
6. S. Cicalò, V. H. Fernandes, C. Schneider, *Partial transformation monoids preserving a uniform partition*. arXiv:1210.4775.
7. V. H. Fernandes, *Normally ordered inverse semigroups*, Semigroup Forum **56** (1998), 418–433. DOI 10.1007/PL00005955. **Not obtained.**
8. H. Pei, *Equivalences, $\alpha$-semigroups and $\alpha$-congruences*, Semigroup Forum **49** (1994), 49–58. DOI 10.1007/BF02573470. Zbl 0804.20046. **Not obtained; review read.**
9. H. Pei, H. Zhou, *Semigroups of partial transformations preserving an equivalence relation*, Adv. Math. (China) (2009). **Abstract only.**
10. M. Sarkar, S. N. Singh, *On certain semigroups of transformations that preserve a partition*, Comm. Algebra **49** (2021), 331–342. arXiv:2006.04242.
11. L. Sun, *Combinatorial results for certain semigroups of transformations preserving orientation and a uniform partition*, Bull. Malays. Math. Sci. Soc. **36** (2013), 179–192.
