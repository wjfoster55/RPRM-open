# Supplementary study: independent bounded Fermat arithmetic

Documentation: CC0-1.0.

This study preserves the full bounded argument and auxiliary-prime certificate
formerly printed in the main manuscript. Its theorem numbers are retained for
stable references. The current paper gives only a short scope summary.

The independent unrestricted proof has not been obtained. Version 1.0.1's
theorem-inheritance closure did not answer that research question and has been
withdrawn from the current presentation. The arguments below do not take
unrestricted Fermat's Last Theorem as a premise. Their classical ingredients
and bounded synthesis make no historical priority claim.

- [Complete bounded argument](#iii2-a-bounded-side-fermat-theorem)
- [Exact fixed-gap decision](#an-exact-decision-for-every-fixed-gap-aperture)
- [All 302 auxiliary-prime premises](#certificate-appendix-iii2-the-auxiliary-prime-premises)
- [Executable reference and replay](fermat.md)

### III.2. A bounded-side Fermat theorem

The arithmetic frontier of the preceding chapter can supply primes for a second problem. Here the retained question is whether two positive integer powers can sum to a third power at the same exponent. We will prove a complete theorem in which only the smaller input base is initially bounded.

**Theorem III.2.1 (bounded smaller base).** For positive integers $a,b,c$ and every integer $n>2$,
$$
\min(a,b)\leq4000\quad\Longrightarrow\quad a^n+b^n\ne c^n.
$$
There is no independently assumed bound on $b$, $c$, or $n$.

The proof combines elementary shell inequalities, classical descents for exponents three and four, prime valuations, and a complete finite table of auxiliary primes. The table and its verification procedure appear in Certificate Appendix III.2. These established ingredients and their bounded synthesis make no historical priority claim. Fermat's Last Theorem is already established mathematics; it is not a premise of this argument. The unrestricted independent RPRM route remains an open research question.

We first prove a different result that clarifies how a finite boundary can decide an unbounded aperture: with exponent and both gaps supplied, an exact bracket decides every positive integer smaller base. This does not assume that its answer must be empty.

#### The source relation and normalization

Retain the full source and discrepancy
$$
R(a,b,c,n,D)\iff D=a^n+b^n-c^n.
$$
The question $Q$ asks whether the aperture $D=0$ has a source. Source roots are positive integers, and their common exponent travels with every change of representation.

**Lemma III.2.2 (primitive ordered reduction).** A hypothetical solution at $n>2$ gives one with
$$
a<b<c,\qquad \gcd(a,b)=\gcd(a,c)=\gcd(b,c)=1.
$$
Its smaller root is no larger than the original smaller root. If $e\mid n$, raising each root to $n/e$ gives a solution at exponent $e$.

**Proof.** Divide all three roots by their common gcd. A prime dividing two roots divides the third by the equation; hence a jointly primitive solution is pairwise coprime. Equality $a=b$ would give $(c/a)^n=2$. If a reduced rational $u/v$ has integral $n$th power, then $v^n\mid u^n$, so $v=1$. No integer $n$th power equals two for $n\geq2$. Relabel the two unequal inputs; positivity then gives $c>b>a$. The exponent reduction follows by substitution. $\square$

Every $n>2$ either has an odd prime divisor or is divisible by four. Exponent reduction changes the roots, however. When using the cap 4000 we must retain it on the original $a$; we cannot transfer it unchanged to $a^{n/e}$.

#### An exact decision for every fixed-gap aperture

**Theorem III.2.3 (derived bracket for supplied gaps).** Supply integers $n\geq2$, $s>0$, and $d>0$. The positive integer solutions in $a$ of
$$
D(a)=a^n+(a+s)^n-(a+s+d)^n=0
$$
form either an empty fiber or a singleton. The entire fiber can be decided by exact integer arithmetic inside the derived bracket
$$
0\leq a\leq M,\qquad M=2n(s+d).
$$

**Proof.** On positive real $a$, positive normalization gives
$$
F(a)=\frac{D(a)}{a^n}
=1-\sum_{k=1}^{n}\binom nk\frac{(s+d)^k-s^k}{a^k}.
$$
Every coefficient subtracted is strictly positive. Thus $F$ is continuous and strictly increasing, with limits $-\infty$ at zero and 1 at infinity. It has exactly one positive real zero, so at most one positive integer zero. This asserts monotonicity of $F$, not of the unnormalized polynomial $D$.

At the integer $M$,
$$
\left(1+\frac{s+d}{M}\right)^n
=\left(1+\frac1{2n}\right)^n
\leq\sum_{k=0}^{n}2^{-k}<2,
$$
using $\binom nk\leq n^k$. In contrast, $1+(1+s/M)^n>2$, so $D(M)>0$. The polynomial is defined at the sentinel zero and has $D(0)=s^n-(s+d)^n<0$; we never evaluate $F(0)$.

Begin with $L=0,U=M$. While $U-L>1$, evaluate $D$ at the integer midpoint. Replace $L$ by that midpoint if the value is negative; otherwise replace $U$. The interval strictly shrinks and preserves
$$
D(L)<0,\qquad D(U)\geq0.
$$
At termination $U=L+1$. If $D(U)=0$, return the unique source $(U,U+s,U+s+d,n)$. Otherwise both signs are strict. Every positive integer is at most $L$ or at least $U$; strict increase of $F$ excludes both tails. If $L=0$, the lower positive-integer tail is simply empty. $\square$

The bound is derived afresh from the supplied parameters. The theorem proves complete integer existence and reconstruction for each aperture, without a universal root cap. The positive-real and positive-integer fibers are different: the former is always ONE, while integer landing can be NONE. For $n=2,s=d=1$, the actual square equality $(3,4,5)$ returns ONE.

The companion repository implements this decision in [the fixed-gap tool](../rprm/fixed_gap.py), with a [runnable example](../examples/fixed_gap.py) and [independent finite checks](../checks/fixed_gap.py). It returns the complete fiber and its signed bracket for supplied parameters. Its implementation evidence supports this algorithm at the tested cases; the written proof above supplies the all-height coverage. Resource exhaustion or interruption remains unfinished computation.

**Corollary III.2.4 (one unbounded fifth-power family).** For every integer $w\geq0$,
$$
(w+1)^5+(w+3)^5\ne(w+4)^5.
$$

**Proof.** Set $n=5,s=2,d=1,a=w+1$. Exact evaluation gives
$$
D(11)=-5480,\qquad D(12)=27281.
$$
The normalized monotonicity in Theorem III.2.3 excludes every positive integer $a$. Equivalently, direct expansion yields
$$
P(w)=w^5-60w^3-360w^2-870w-780.
$$
For $w>0$, $P(w)/w^5$ strictly increases and changes sign between 10 and 11. The remaining endpoint is separately $P(0)=-780$. $\square$

This is a complete outside-continuation argument for one gap family. It does not establish that the integer answer is NONE for every choice of exponent and gaps. The bounded-side theorem requires additional arithmetic to close its whole parameter range.

#### Shell inequalities and complete finite coverage

Put $d=c-b\geq1$ on a hypothetical primitive ordered solution.

**Lemma III.2.5 (shell bounds).** Every such solution at $n\geq3$ satisfies
$$
a^n>ndb^{n-1},\qquad nd<a,\qquad 3db^2<a^3,\qquad a\geq2n.
$$

**Proof.** The exact difference-of-powers identity is
$$
a^n=c^n-b^n
=d\sum_{j=0}^{n-1}c^jb^{n-1-j}>ndb^{n-1}.
$$
Since $b>a$, division by $a^{n-1}$ gives $nd<a$. Division by $a^{n-3}$ gives
$$
a^3>ndb^2(b/a)^{n-3}\geq3db^2.
$$

For the last bound, the smallest shell at a fixed $a$ occurs at $b=a+1,d=1$. Write $m=2n-1$. Expanding the shell at $a=m$ around its midpoint $2n+\tfrac12$, the linear term and the positive cubic term imply
$$
(2n+1)^n-(2n)^n>n(2n+\tfrac12)^{n-1}.
$$
The first three terms in the binomial expansion of $(1+3/(2m))^{n-1}$ exceed $m/n$, because
$$
1+\frac{3(n-1)}{2m}
+\frac{9(n-1)(n-2)}{8m^2}-\frac mn
=\frac{(n-1)(n+4)(n-2)}{8nm^2}>0.
$$
Multiplying by $nm^{n-1}$ proves that the smallest shell at $a=m$ already exceeds $m^n$. Finally,
$$
\frac{(a+2)^n-(a+1)^n}{a^n}
=\sum_{k=1}^{n}\binom nk\frac{2^k-1}{a^k}
$$
strictly decreases with positive $a$. Thus every $a\leq m$ is excluded as well, giving $a\geq2n$. $\square$

Consequently any positive integer cap $H$ gives a complete finite enclosure:
$$
\begin{gathered}
2n\leq a\leq H,\qquad 3\leq n\leq\lfloor a/2\rfloor,\\
1\leq d\leq\lfloor(a-1)/n\rfloor,\\
a<b\leq\left\lfloor\sqrt{\left\lfloor\frac{a^3-1}{3d}\right\rfloor}\right\rfloor,\qquad c=b+d.
\end{gathered}
$$
Every hypothetical positive integer solution enters one such enclosure after normalization. The enclosures increase with $H$. The proof below closes $H=4000$; changing $H$ preserves the shell theorem but does not automatically preserve the finite certificate's remaining premises.

**Proposition III.2.6 (exact bounded-coordinate chart).** On jointly primitive positive triples $a<b<c$, the map
$$
(a,b,c)\longmapsto(x,y)=(a/c,b/c)
$$
is a bijection onto the rational triangle $0<x<y<1$. If $L$ is the least common multiple of the reduced denominators of $x,y$, its inverse is $(Lx,Ly,L)$.

**Proof.** For a source triple, the least common denominator is
$c/\gcd(a,b,c)=c$. Conversely, $Lx,Ly,L$ are positive integers; a common divisor greater than one would supply a smaller common denominator, contradicting minimality of $L$. The inequalities and inverse follow directly. $\square$

Retain $n$ as well. The target becomes $x^n+y^n=1$, its residual is $D/L^n$, and the cap is $Lx\leq H$. Pairwise coprimality is an additional image condition when required. Although the displayed coordinates stay below one, their denominators retain arbitrarily large source roots. A fixed rounded grid is a different carrier.

**Proposition III.2.7 (a uniform stronger slope bound).** Every hypothetical solution with $n\geq100$ satisfies $a>81n/40$.

**Proof.** Let $\kappa=81/40$ and suppose $a\leq\kappa n$. For $r=(a+1)/(a+2)$, binomial expansion gives
$$
r^{-n}\geq1+\frac n{\kappa n+1}
+\frac{n(n-1)}{2(\kappa n+1)^2}
+\frac{n(n-1)(n-2)}{6(\kappa n+1)^3}.
$$
Each factor $(n-j)/(\kappa n+1)$, $j=0,1,2$, increases with $n$: its forward difference has positive numerator $1+\kappa j$. Thus the right side is at least its value at 100,
$$
\frac{9991013}{6129013}>\frac{13}{8}.
$$
Hence $r^n<8/13$. Since $a/(a+2)<r^2$,
$$
\frac{a^n+(a+1)^n-(a+2)^n}{(a+2)^n}
<r^{2n}+r^n-1
<\left(\frac8{13}\right)^2+\frac8{13}-1
=-\frac1{169}.
$$
The smallest shell already exceeds $a^n$; every larger shell does too. $\square$

This proposition is independent of a fixed cap. The single rational evaluation supports an argument quantified over every $n\geq100$, rather than a sample of large exponents.

#### The quartic descent

**Lemma III.2.8.** There are no positive integer solutions of $x^4+y^4=z^2$. In particular, the Fermat equation has no positive solution whenever its exponent is divisible by four.

**Proof.** Choose a solution with least positive $z$. If $g=\gcd(x,y)>1$, then $g^4\mid z^2$, so integer prime valuations give $g^2\mid z$; dividing would produce a smaller solution. Thus $x,y$ are coprime. They cannot both be odd, since a square cannot be two modulo four. Relabel $x$ odd and $y$ even.

We will use the primitive Pythagorean parametrization, including its reason. If $A^2+B^2=C^2$ is primitive with $A$ odd and $B$ even, then $C$ is odd and the positive integers $(C+A)/2,(C-A)/2$ are coprime: any common divisor divides $C,A$. Their product is $(B/2)^2$, so unique factorization makes each a square. Therefore
$$
A=m^2-n^2,\quad B=2mn,\quad C=m^2+n^2,
$$
where $m>n>0$ are coprime and have opposite parity.

Apply this to $(x^2,y^2,z)$. If $m$ were even, $x^2=m^2-n^2$ would be three modulo four. Hence $m$ is odd and $n$ even. Now
$$
(y/2)^2=m(n/2)
$$
has coprime positive factors; write $m=u^2,n=2v^2$. We obtain the new primitive triangle
$$
x^2+(2v^2)^2=(u^2)^2.
$$
Primitivity follows because a prime dividing $x,n$ would divide $m$. Parametrize again:
$$
x=r^2-s^2,\qquad v^2=rs,\qquad u^2=r^2+s^2,
$$
with coprime positive $r>s$. Thus $r=R^2,s=S^2$, giving
$$
R^4+S^4=u^2,\qquad 0<u\leq u^2=m<m^2+n^2=z.
$$
This is the same equation with a strictly smaller positive right-hand root, contradicting minimality. Setting $z=c^2$ excludes exponent four; exponent inheritance excludes its multiples. $\square$

#### Cubic descent through an explicitly justified ring

**Lemma III.2.9.** There are no nonzero signed integers $x,y,z$ satisfying $x^3+y^3+z^3=0$. Therefore every exponent divisible by three is excluded.

**Proof.** Normalize and choose a primitive counterexample of least height $\max(|x|,|y|,|z|)$. The roots are pairwise coprime. Cubes modulo nine are $0,1,-1$; a sum of three nonzero residues cannot be zero. Primitivity and the equation exclude two or three coordinates divisible by three. Name the unique divisible coordinate $z$. Thus $3\nmid xy$ and $3\mid x+y$.

Use $\mathbb Z[\omega]$, where $\omega^2+\omega+1=0$, with conjugation $\omega\mapsto\omega^2$. Its norm is
$$
N(m+n\omega)=(m+n\omega)(m+n\omega^2)=m^2-mn+n^2.
$$
It is multiplicative and a positive integer on nonzero elements. Solving $N=1$, or using $(m-n/2)^2+3n^2/4=1$, gives precisely the units $\pm1,\pm\omega,\pm\omega^2$.

For a quotient of two ring elements, round its two rational coordinates to integers. The errors $e,f\in[-1/2,1/2]$ have $e^2-ef+f^2\leq3/4<1$. Multiplication by the denominator therefore gives a remainder of smaller norm. This proves Euclidean division. The Euclidean algorithm supplies gcds and Bezout identities; an irreducible is prime because Bezout shows that an irreducible dividing a product must divide one factor. Induction on the positive norm gives factorization into irreducibles, and their prime property gives uniqueness up to units and order. The needed factorization law has thus been justified for this ring.

Set $\lambda=1-\omega$. Then $N(\lambda)=3$, $\lambda^2=-3\omega$, and imposing $\lambda=0$ gives $\omega=1$ and $3=0$. Hence the quotient by $(\lambda)$ is $\mathbb F_3$, and
$$
\lambda\mid(m+n\omega)\iff3\mid m+n,\qquad
v_\lambda(t)=2v_3(t)\quad(t\in\mathbb Z\setminus\{0\}).
$$
Here $v_\pi$ denotes the multiplicity of a prime factor $\pi$.

The integer
$$
x^2-xy+y^2=(x+y)^2-3xy
$$
has three-adic valuation exactly one. From $(x+y)(x^2-xy+y^2)=-z^3$ we get
$$
v_3(x+y)+1=3v_3(z),
$$
so $9\mid x+y$.

Factor in the ring:
$$
(x+y)(x+y\omega)(x+y\omega^2)=-z^3.
$$
Differences between the factors are unit multiples of $y\lambda$. A common prime other than $\lambda$ would divide both $x,y$, contradicting their integer Bezout identity. Also
$x+y\omega=(x+y)-y\lambda$ has $\lambda$-valuation exactly one: the first term has valuation at least four and the second exactly one. Every other prime exponent in that factor is therefore a multiple of three. Unique factorization gives
$$
x+y\omega=\varepsilon\lambda\gamma^3,\qquad
\gamma=m+n\omega,\qquad \lambda\nmid\gamma.
$$

Write
$$
\gamma^3=A+B\omega,\quad
A=m^3-3mn^2+n^3,\quad B=3mn(m-n).
$$
Then $\lambda\gamma^3=(A+B)+(2B-A)\omega$. Multiplication by the unit families $\pm1,\pm\omega,\pm\omega^2$ gives coefficient sums respectively
$$
\pm3B,\qquad \pm3(A-B),\qquad \mp3A.
$$
Since $A\equiv m+n\ne0\pmod3$ and $B\equiv0\pmod3$, the condition $9\mid x+y$ forces $\varepsilon=\pm1$. Therefore
$$
x+y=\pm9mn(m-n).
$$
Taking norms yields $x^2-xy+y^2=3N(\gamma)^3$. Combining this with the original cubic equation gives
$$
mn(m-n)=\pm\left(\frac{z}{3N(\gamma)}\right)^3.
$$
The rational cube on the right is an integer, so the reduced-denominator argument makes its root an integer. A rational prime dividing both $m,n$ would divide both coefficients of $\varepsilon\lambda\gamma^3=x+y\omega$, contradicting coprimality of $x,y$. Thus $m,n,m-n$ are pairwise coprime; their product is nonzero. Integer prime valuations now make each a signed cube:
$$
m=r^3,\qquad n=s^3,\qquad m-n=t^3.
$$
The primitive nonzero signed triple $(r,-s,-t)$ satisfies the same cubic equation, while
$$
\max(|r|,|s|,|t|)\leq|rst|
=\frac{|z|}{3N(\gamma)}<|z|
\leq\max(|x|,|y|,|z|).
$$
This contradicts the least height. Exponent inheritance finishes the claim. $\square$

The ring lift retains the units, ramified prime, integer return, and decreasing rank. Its factorization law has not been asserted for rings belonging to arbitrary higher exponents.

#### Prime valuations and coprime seam factors

For a nonzero integer $t$, let $v_p(t)$ be the exponent of $p$ in $|t|$.

**Lemma III.2.10 (valuation and seam laws).** Let $p$ be an odd prime, let $X,Y$ be distinct integers with $p\nmid XY$ and $p\mid X-Y$, and let $m$ be a positive integer. Then
$$
v_p(X^m-Y^m)=v_p(X-Y)+v_p(m).
$$
For odd $m$, replacing $Y$ by $-Y$ gives the sum version whenever $X+Y\ne0$. For coprime $X,Y$, a seam $X-Y$ and its $p$th-power companion quotient share no prime except $p$; the corresponding $p$th-power sum has the same property.

**Proof.** For an exponent $k$ coprime to $p$, the difference quotient modulo $p$ equals $kY^{k-1}$, a nonzero residue. For exponent $p$, put $h=X-Y$ and expand $(Y+h)^p-Y^p$. The first term has valuation $v_p(h)+1$. Each later term has larger valuation: the intermediate binomial coefficients are divisible by $p$, and the final term $h^p$ also has larger valuation because $p\geq3$. Writing $m=p^e k$ and iterating proves the formula.

For the final claim, reduce the companion quotient modulo the seam. At $X=Y$ it becomes $pY^{p-1}$. A prime dividing the seam cannot divide $Y$ by coprimality, so only $p$ can divide both factors. Replacing $Y$ with $-Y$ gives the sum claim. If $p$ divides the seam, the valuation formula at exponent $p$ makes the companion's $p$-valuation exactly one. $\square$

We will also use $t^{p-1}=1\pmod p$ for nonzero residues: multiplication by $t$ permutes the nonzero residues, and canceling their product proves the identity. Thus $t^p=t\pmod p$ for every residue.

#### Auxiliary primes exclude the first case

**Lemma III.2.11 (auxiliary-prime implication).** Let $p$ be an odd prime and $q\ne p$ a prime. Form the entire nonzero power image
$$
\mathcal P_{p,q}=\{a^p\bmod q:1\leq a<q\}.
$$
Suppose
$$
\mathcal P_{p,q}\cap(1-\mathcal P_{p,q})=\varnothing,\qquad
p\bmod q\notin\mathcal P_{p,q}.
$$
Then there is no primitive nonzero integer solution of $x^p+y^p=z^p$ with $p\nmid xyz$.

**Proof.** The image is a multiplicative subgroup of $\mathbb F_q^\times$: products and inverses of $p$th powers remain $p$th powers. Since $p$ is odd, it also contains $-1$.

Suppose a first-case solution exists. The congruence $t^p=t\pmod p$ gives
$x+y\equiv z$, $z-x\equiv y$, and $z-y\equiv x\pmod p$; hence none of these seams is divisible by $p$. Lemma III.2.10 makes each seam coprime to its companion quotient. Their products are signed $p$th powers. Integer prime valuations, with signs absorbed because $p$ is odd, yield
$$
x+y=A^p,\qquad z-x=B^p,\qquad z-y=C^p,\qquad
\frac{x^p+y^p}{x+y}=E^p.
$$
The seams are nonzero because the original coordinates are nonzero.

If $q$ divided no coordinate, divide the equation modulo $q$ by $z^p$. Two elements of $\mathcal P_{p,q}$ would sum to one, contradicting its first condition. Thus $q$ divides one coordinate, uniquely by pairwise coprimality. Permuting the signed equation $x^p+y^p+(-z)^p=0$, and changing the sign assigned to the right-hand coordinate, permits us to call it $z$.

Now $-x=B^p$ and $-y=C^p\pmod q$. Because $-1$ belongs to the subgroup, $x,y$ belong to it too. If $x+y\ne0\pmod q$, the identity $x+y=A^p$ would let us divide by that subgroup element and again obtain two members summing to one. Hence $x+y=0\pmod q$.

The quotient polynomial evaluated at $y=-x$ becomes
$$
E^p=p x^{p-1}\pmod q.
$$
It is nonzero since $q\ne p$ and $q\nmid x$. Both $E^p$ and $x^{p-1}$ belong to the subgroup, so division forces $p$ into it, contradicting the second condition. $\square$

Certificate Appendix III.2 supplies one such pair for every odd prime $3\leq p\leq1999$. It records the complete 302 pairs and a finite procedure reconstructing all nonzero power residues. The already retained passing computation checks both conditions and full exponent coverage. The conclusion is an all-height first-case exclusion for each of these exponents. Primality alone supplies neither residue condition; the preceding chapter gives explicit failures of each.

#### All bounded exponent branches except five and ten

**Proposition III.2.12.** Under $a\leq4000$, the preceding results reduce a hypothetical solution to $n=5$ or $n=10$.

**Proof.** Lemma III.2.5 gives $n\leq2000$. Discard all multiples of three and four by the descents. Every remaining exponent is at least five, so the shell inequality also gives
$$
a^5>ndb^4(b/a)^{n-5}\geq5db^4.
$$
Since $4000^5<5\cdot22000^4$, the retained original roots obey
$$
b<22000,\qquad d<a/n\leq800,\qquad c<22800.
$$
Every positive linear seam $c-b,c-a,a+b$ is therefore below 26000. Every corresponding quadratic seam is below
$$
22800^2+22000^2<1100000000.
$$

Put $m=n$ if $n$ is odd, and $m=n/2$ otherwise. Then $m$ is odd; let $p\geq5$ be its least prime divisor. Every prime divisor of $p-1$ is smaller than $p$, so $\gcd(m,p-1)=1$. Raising to $m$ is consequently injective on nonzero residues modulo $p$: raise an equality to an inverse of $m$ modulo $p-1$.

The prime $p$ lies in the appendix's range. Reducing the original equation to exponent $p$, Lemma III.2.11 forces $p$ to divide one of the original roots. If $n$ is odd, use $(X,Y,Z)=(a,b,c)$; otherwise use $(a^2,b^2,c^2)$. Injectivity of $m$th powering modulo $p$ forces the appropriate seam $Z-Y,Z-X$, or $X+Y$ to be divisible by $p$. Lemma III.2.10 then gives its exact valuation
$$
v_p(\text{seam})=n\,v_p(\text{original divisible root})-v_p(m)
\geq n-v_p(m).
$$
The original cap stays attached to $a$, including in the squared-root carrier.

The resulting lower bounds exceed the relevant ceilings:

| Remaining exponent form | Lower bound for its seam | Upper bound |
|---|---:|---:|
| $n=p\geq7$, prime | $p^{p-1}\geq7^6=117649$ | $26000$       |
| $n$ odd composite | $5^{20}$ | $26000$       |
| $n=2p$, prime $p\geq7$ | $p^{2p-1}\geq7^{13}$ | $1100000000$         |
| $n=2m$, odd composite $m$ | $5^{45}$ | $1100000000$         |

For completeness, an odd composite $m$ with least prime factor at least five has $m\geq25$. If $e=v_p(m)\geq1$, then
$$
e\leq p^{e-1}\leq m/p\leq m/5.
$$
The first inequality follows by induction on $e$. Thus $m-e\geq4m/5\geq20$, or $2m-e\geq9m/5\geq45$, proving the composite rows. The listed integer comparisons are strict. Only $n=5,10$ escape them. $\square$

#### Fifth powers: complete seam shapes and strict crossings

**Lemma III.2.13.** A primitive ordered fifth-power solution cannot have $a\leq4000$.

**Proof.** Write $d=c-b<800$. By Lemma III.2.10, a seam and its fifth-power companion share only five. If the associated root is divisible by five, the modulo-five seam argument in Proposition III.2.12 makes the seam divisible by five. Lemma III.2.10 then gives the companion five-adic valuation one. Since their product is a fifth power, the seam has form $5^4t^5=625t^5$. If the associated root is not divisible by five, neither factor contains five; they are coprime, so the seam is an ordinary fifth power.

First suppose $5\mid a$. Then $d=625t^5<800$ forces $d=625$. At $a=4000$, the smallest shell with this gap exceeds $a^5$:
$$
4626^5-4001^5-4000^5=69217768803909375>0.
$$
The ratio $[(a+626)^5-(a+1)^5]/a^5$ is a sum of positive coefficients times inverse powers of $a$, hence decreases with $a$. Its value exceeds one at 4000, so it exceeds one at every smaller positive $a$. This excludes the case.

Now $5\nmid a$. The ordinary gap has exactly the possibilities
$$
d=t^5\in\{1,32,243\},
$$
since $4^5>800$. The auxiliary-prime lemma at $p=5$ forces $5\mid b$ or $5\mid c$. The matching seam $L=c-a$ or $L=a+b$ has form $625u^5<26000$, giving exactly
$$
L\in\{625,20000\}.
$$

If $5\mid b$, then $b=a+L-d,c=a+L$, and define
$$
E_{d,L}(a)=a^5+(a+L-d)^5-(a+L)^5.
$$
Here $L>d$. Its normalized value strictly increases, since the shell ratio
$$
\frac{(a+L)^5-(a+L-d)^5}{a^5}
$$
has positive inverse-power coefficients. Thus its sign crosses zero at most once. When $L=20000$, even the smallest gap has, at the cap,
$$
24000^5-23999^5-4000^5=634741765759880001>0.
$$
The shell ratio increases as $a$ decreases, and the shell increases as $d$ increases. All three large difference-seam branches are excluded.

If $5\mid c$, write $b=L-a,c=L-a+d$, and define
$$
F_{d,L}(a)=a^5+(L-a)^5-(L-a+d)^5.
$$
On $0<a<L$, this function strictly increases: its first term increases and the subtracted shell decreases. For $L=625$, order requires $a\leq312$; then $5d<a$ rules out $d=243$.

The six remaining crossings have the following exact adjacent integer certificates:

| Function | Lower integer | Value there | Value at the next integer |
|---|---:|---:|---:|
| $E_{1,625}$ | 335 | $-18753691826$ | $26900909375$       |
| $E_{32,625}$ | 1028 | $-1142821221024$ | $1641632904757$       |
| $E_{243,625}$ | 2523 | $-35451102937500$ | $32297263771651$       |
| $F_{1,625}$ | 181 | $-926025000$ | $6250588651$       |
| $F_{32,625}$ | 296 | $-4201942176$ | $60664215625$       |
| $F_{1,20000}$ | 3296 | $-329671369090625$ | $353993777122976$       |

For each row, the proved normalized or raw monotonicity excludes all integers on both sides. The two remaining increasing sum branches are still negative at the cap:
$$
F_{32,20000}(4000)=-9503787009999634432,
$$
$$
F_{243,20000}(4000)=-81057900031960689443.
$$
They are negative at every smaller admitted $a$. All possibilities for the divisible root, gap, and exceptional seam have been covered. $\square$

The table is finite exact arithmetic inside a written coverage proof. It can be checked by substituting into the displayed polynomials; an independent retained computation also evaluated every admitted integer in the derived branches. Neither argument assumes the answer from Fermat's Last Theorem.

#### Tenth powers: a complete factor classification

**Lemma III.2.14.** A primitive ordered tenth-power solution cannot have $a\leq4000$.

**Proof.** The tenth-power shell gives $d<400$. Since
$4000^{10}<10\cdot8000^9$, it also gives $b<8000$. Consequently
$$
c+b<16400,\qquad J=c^2-b^2=d(c+b)<6560000.
$$
Factor $c^{10}-b^{10}$ as a difference of fifth powers of the coprime squares $c^2,b^2$.

If $5\mid a$, the companion has five-adic valuation one. All other prime exponents in the seam are multiples of ten, and
$$
J=5^9u^{10}.
$$
The inequality $5^9<6560000<5^9\cdot2^{10}$ forces $u=1$. Thus $J$ is odd, $b,c$ have opposite parity, and $c-b,c+b$ are odd and coprime: any common divisor divides $2b,2c$. Their product is the prime power $5^9$, so the smaller factor is one and
$$
c-b=1,\qquad c+b=5^9=1953125,
$$
contradicting $c+b<16400$.

If $5\nmid a$, seam and companion are coprime, so
$$
(c-b)(c+b)=t^{10}.
$$
When $b,c$ have opposite parity, the two factors are odd and coprime tenth powers. The larger exceeds one, hence is at least $3^{10}=59049>16400$.

The remaining case has $b,c$ both odd. Set
$$
u=(c-b)/2<200,\qquad v=(c+b)/2<8200.
$$
They are coprime, have opposite parity, and satisfy $4uv=t^{10}$. Every odd-prime valuation in each factor is a multiple of ten. The odd factor is therefore a tenth power; the even factor is $2^8$ times a tenth power, because its two-adic valuation is eight modulo ten. The bound $u<200<256$ prevents $u$ from being even. As an odd tenth power below 200, it is one. Thus $v=256w^{10}$, and $v<8200$ forces $w=1$.

The only candidate is $(b,c)=(255,257)$. Here $5\mid b$. The hypothetical equation modulo five gives $c^2\equiv a^2\pmod5$. Apply Lemma III.2.10 to $X=c^2,Y=a^2$ at exponent five: $v_5(c^2-a^2)=10v_5(b)-1\geq9$. This forces
$$
c^2-a^2\geq5^9.
$$
But $c^2=257^2=66049<5^9$, a contradiction. These cases exhaust the possible parities and five-divisibility branches. $\square$

**Completion of Theorem III.2.1.** Normalize by Lemma III.2.2, retaining $a\leq4000$. Lemmas III.2.8–III.2.9 exclude exponents divisible by four or three. Proposition III.2.12 reduces every remaining exponent to five or ten, and Lemmas III.2.13–III.2.14 exclude both. Therefore no source in the stated smaller-base carrier has zero discrepancy. $\square$

#### What the certificates establish and what remains open

The retained finite computation checks the 302 complete auxiliary images, totaling 4,052,680 source powers and 3,936 distinct image elements summed over their moduli. It separately classifies all 1,998 integers $n=3,\ldots,2000$, evaluates 32,319 admitted fifth-branch inputs across 11 nonempty branches, and enumerates 25 positive divisor pairs across the derived tenth-power seam cases. Its passing receipt is evidence for those finite premises and implementation checks. It is not a proof-assistant formalization of this prose. The preceding proofs explain why the finite premises cover the initially unbounded $b,c,n$ ports.

The fixed-gap theorem has its own written universal proof and separate finite implementation evidence. Its corrected reparameterization includes $w=0$. Neither its finite checks nor the bounded-side certificate proves a uniform empty answer for all larger root and prime/gap parameters.

Coordinate preservation likewise does not imply exclusion. For two retained roots, let $s=a+b$, $q=a^2+b^2$, and $t=(s^2-q)/2=ab$. Their power sums obey
$$
S_0=2,\quad S_1=s,\quad S_{j+2}=sS_{j+1}-tS_j,
$$
because each root satisfies $X^2-sX+t=0$. The source image requires $2q-s^2=h^2$ for a nonnegative integer $h$, matching parity of $s,h$, and positive $(s-h)/2,(s+h)/2$. These conditions reconstruct the sorted roots. A single power sum cannot do so: $(1,7)$ and $(5,5)$ both have square sum 50, but cube sums 344 and 250.

Even complete determination of $S_n$ leaves the target $S_n-c^n=0$ to decide. Under an invertible linear change $v\mapsto Jv$, a target row must move as $\ell\mapsto\ell J^{-1}$; then $(\ell J^{-1})(Jv)=\ell v$. Reading an isolated component after discarding the target or its complementary terms changes the question. Similarly, the shell discrepancies at $(5,6,7;3)$ and $(6,7,8;3)$ are $-2$ and 47, so a sign at one root height does not propagate upward without a proved law. The near equality $6^3+8^3-9^3=-1$ remains nonzero under faithful transport.

For the independent unrestricted route, it remains to exclude every hypothetical primitive positive solution at odd prime exponent $p\geq5$ beyond this bounded theorem. For $p\leq1999$, the existing auxiliary table already forces the second case, in which one root is divisible by $p$. Larger primes require additional first-case premises as well. One sufficient completion would map every remaining hypothetical zero to another positive integer zero at the same exponent and strictly smaller integer height, with primitivity restored lawfully. Well-ordering would then contradict a least counterexample. Scaling or dividing displayed coordinates does not supply such an integer return, and the cubic ring's factorization law cannot be inherited by a new ring without proof.

The fixed-gap bracket offers another precise target: prove that its nonnegative endpoint is strictly positive for every surviving prime/gap tuple, using independent arithmetic restrictions. The bracket already decides each supplied aperture; a uniform proof that every such answer is NONE is the remaining quantifier. The established full Fermat theorem and this open obligation in an independent derivation are different statements.

## Certificate Appendix III.2. The auxiliary-prime premises

### The exact finite claim

For each odd prime $p\leq1999$, the table below supplies a prime $q\ne p$. Its required receiver is the **complete** nonzero power image
$$
\mathcal P_{p,q}=\{a^p\bmod q:1\leq a<q\}.
$$
Every pair satisfies
$$
\mathcal P_{p,q}\cap(1-\mathcal P_{p,q})=\varnothing,
\qquad p\bmod q\notin\mathcal P_{p,q}.
$$
These are the finite premises of Lemma III.2.11. The lemma supplies the all-height conclusion for each listed exponent. The table alone makes no assertion about larger primes or second-case solutions.

There are 302 pairs, listed in increasing order of $p$. Each displayed ordered pair has the form $(p,q)$. The largest second coordinate is 185849. The table is explicit numerical certificate data, followed by a bounded procedure sufficient to check every required premise without consulting an external program.

### One complete row

For $(p,q)=(5,11)$, the nonzero residues $a=1,\ldots,10$ have fifth powers modulo 11, in order,
$$
1,10,1,1,1,10,10,10,1,10.
$$
Hence $\mathcal P_{5,11}=\{1,10\}$. Subtracting these residues from one gives $1-\mathcal P_{5,11}=\{0,2\}$ modulo 11, disjoint from the power image. The residue $5$ is also absent from $\{1,10\}$. Both 5 and 11 are prime: neither has a divisor among the primes up to its square root. This checks every premise for this row. The remaining rows require their own complete images and checks under the procedure below.

### All 302 pairs

```text
(3, 7)  (5, 11)  (7, 29)  (11, 23)  (13, 53)
(17, 137)  (19, 191)  (23, 47)  (29, 59)  (31, 311)
(37, 149)  (41, 83)  (43, 173)  (47, 659)  (53, 107)
(59, 827)  (61, 977)  (67, 269)  (71, 569)  (73, 293)
(79, 317)  (83, 167)  (89, 179)  (97, 389)  (101, 809)
(103, 1031)  (107, 857)  (109, 1091)  (113, 227)  (127, 509)
(131, 263)  (137, 1097)  (139, 557)  (149, 1193)  (151, 1511)
(157, 1571)  (163, 653)  (167, 2339)  (173, 347)  (179, 359)
(181, 1811)  (191, 383)  (193, 773)  (197, 7487)  (199, 797)
(211, 2111)  (223, 7583)  (227, 5903)  (229, 5039)  (233, 467)
(239, 479)  (241, 2411)  (251, 503)  (257, 9767)  (263, 5261)
(269, 2153)  (271, 2711)  (277, 1109)  (281, 563)  (283, 9623)
(293, 587)  (307, 1229)  (311, 6221)  (313, 5009)  (317, 8243)
(331, 5297)  (337, 3371)  (347, 2777)  (349, 3491)  (353, 4943)
(359, 719)  (367, 3671)  (373, 1493)  (379, 10613)  (383, 23747)
(389, 14783)  (397, 6353)  (401, 3209)  (409, 1637)  (419, 839)
(421, 4211)  (431, 863)  (433, 1733)  (439, 4391)  (443, 887)
(449, 3593)  (457, 21023)  (461, 9221)  (463, 18521)  (467, 9341)
(479, 3833)  (487, 1949)  (491, 983)  (499, 1997)  (503, 7043)
(509, 1019)  (521, 16673)  (523, 5231)  (541, 11903)  (547, 5471)
(557, 4457)  (563, 7883)  (569, 25037)  (571, 5711)  (577, 2309)
(587, 8219)  (593, 1187)  (599, 4793)  (601, 6011)  (607, 20639)
(613, 6131)  (617, 4937)  (619, 2477)  (631, 6311)  (641, 1283)
(643, 10289)  (647, 9059)  (653, 1307)  (659, 1319)  (661, 14543)
(673, 2693)  (677, 5417)  (683, 1367)  (691, 6911)  (701, 22433)
(709, 2837)  (719, 1439)  (727, 2909)  (733, 7331)  (739, 2957)
(743, 1487)  (751, 52571)  (757, 12113)  (761, 1523)  (769, 7691)
(773, 15461)  (787, 22037)  (797, 11159)  (809, 1619)  (811, 8111)
(821, 6569)  (823, 8231)  (827, 11579)  (829, 8291)  (839, 26849)
(853, 3413)  (857, 6857)  (859, 18899)  (863, 27617)  (877, 14033)
(881, 22907)  (883, 3533)  (887, 23063)  (907, 30839)  (911, 1823)
(919, 3677)  (929, 7433)  (937, 9371)  (941, 7529)  (947, 7577)
(953, 1907)  (967, 15473)  (971, 19421)  (977, 7817)  (983, 13763)
(991, 21803)  (997, 3989)  (1009, 10091)  (1013, 2027)  (1019, 2039)
(1021, 10211)  (1031, 2063)  (1033, 4133)  (1039, 4157)  (1049, 2099)
(1051, 29429)  (1061, 21221)  (1063, 4253)  (1069, 10691)  (1087, 4349)
(1091, 21821)  (1093, 4373)  (1097, 15359)  (1103, 2207)  (1109, 15527)
(1117, 11171)  (1123, 4493)  (1129, 4517)  (1151, 9209)  (1153, 25367)
(1163, 37217)  (1171, 25763)  (1181, 30707)  (1187, 9497)  (1193, 16703)
(1201, 12011)  (1213, 26687)  (1217, 31643)  (1223, 2447)  (1229, 2459)
(1231, 19697)  (1237, 19793)  (1249, 12491)  (1259, 17627)  (1277, 25541)
(1279, 12791)  (1283, 33359)  (1289, 2579)  (1291, 12911)  (1297, 5189)
(1301, 26021)  (1303, 20849)  (1307, 10457)  (1319, 42209)  (1321, 29063)
(1327, 5309)  (1361, 10889)  (1367, 10937)  (1373, 60413)  (1381, 38669)
(1399, 97931)  (1409, 2819)  (1423, 5693)  (1427, 19979)  (1429, 5717)
(1433, 20063)  (1439, 2879)  (1447, 49199)  (1451, 2903)  (1453, 5813)
(1459, 14591)  (1471, 23537)  (1481, 2963)  (1483, 14831)  (1487, 11897)
(1489, 14891)  (1493, 20903)  (1499, 2999)  (1511, 3023)  (1523, 21323)
(1531, 79613)  (1543, 6173)  (1549, 6197)  (1553, 49697)  (1559, 3119)
(1567, 6269)  (1571, 12569)  (1579, 6317)  (1583, 3167)  (1597, 6389)
(1601, 3203)  (1607, 32141)  (1609, 16091)  (1613, 32261)  (1619, 12953)
(1621, 45389)  (1627, 45557)  (1637, 62207)  (1657, 26513)  (1663, 6653)
(1667, 13337)  (1669, 16691)  (1693, 16931)  (1697, 13577)  (1699, 37379)
(1709, 85451)  (1721, 34421)  (1723, 17231)  (1733, 3467)  (1741, 38303)
(1747, 17471)  (1753, 7013)  (1759, 38699)  (1777, 7109)  (1783, 39227)
(1787, 185849)  (1789, 17891)  (1801, 28817)  (1811, 3623)  (1823, 25523)
(1831, 18311)  (1847, 48023)  (1861, 74441)  (1867, 18671)  (1871, 14969)
(1873, 18731)  (1877, 15017)  (1879, 7517)  (1889, 3779)  (1901, 3803)
(1907, 26699)  (1913, 26783)  (1931, 3863)  (1933, 88919)  (1949, 132533)
(1951, 42923)  (1973, 3947)  (1979, 39581)  (1987, 7949)  (1993, 67763)
(1997, 87869)  (1999, 19991)
```

### Complete bounded verification

All divisions and remainders in this procedure are integer operations. A failure in any step rejects the certificate.

1. For each odd integer $h=3,5,\ldots,1999$, test divisibility by every integer $d$ with $2\leq d$ and $d^2\leq h$. Keep exactly the integers with no divisor. Compare this ordered list with the table's entire first-coordinate list, requiring equality entry by entry and no extra rows. The least-divisor lemma from Chapter III.1 proves that this classifies every prime in the interval; it does not rely on a preexisting prime list.
2. For each pair, check that both coordinates are integers, $p$ is an odd prime, $q>p$ is prime by the same divisor procedure, and $q=2kp+1$ for a positive integer $k$. The last condition describes this certificate's construction; primality and the two image conditions remain separate obligations.
3. For **every** integer $a=1,\ldots,q-1$, calculate its residue $a^p\bmod q$. An elementary bounded rule is $r_0=1$, $r_{j+1}=a r_j\bmod q$ for $j=0,\ldots,p-1$; retain $r_p$. Collect the set of all results. Duplicate images are removed only after all source inputs have been represented. This constructs the full $\mathcal P_{p,q}$, rather than a sampled subset or an unproved generator orbit.
4. Require that zero is absent and that the set contains exactly $(q-1)/p$ elements. The cardinality check is an additional consistency test of these rows; the auxiliary-prime proof uses the explicitly constructed full image, not an assumption that any proposed subset has this size.
5. For each retained image element $r$, calculate $(1-r)\bmod q$ and require it to be absent from the set. Then separately require $p\bmod q$ to be absent. The two checks establish the two hypotheses of Lemma III.2.11 without conflating them.

The loops have explicit finite bounds: 999 odd candidate integers in the exponent classification; 302 table rows; $q\leq185849$; at most $q-1$ source inputs per image; and at most $p\leq1999$ modular multiplications per source under the elementary rule. Primality divisions need no candidate divisor above 431 because $432^2>185849$. Modular repeated squaring can shorten step 3, provided it returns the same exact power residue; no such optimization is needed to define the procedure.

The retained passing computation for this exact table used all 4,052,680 nonzero source inputs and obtained 3,936 image elements when image sizes are summed across the 302 moduli. It checked both residue exclusions and complete prime-exponent coverage. These counts are reported from the existing verified receipt; this appendix does not claim a new execution. They summarize the finite computation and do not replace the explicit data and checking rule above.

### How the finite data closes the bounded-side theorem

The shell proof derives $n\leq2000$ from the sole initial smaller-base cap 4000. Cubic and quartic descent remove their respective exponent classes. For each remaining exponent, its least odd prime divisor is among the table's first coordinates. Lemma III.2.11 therefore forces that prime to divide one original root. The seam-valuation bounds in Proposition III.2.12 exclude every remaining exponent except five and ten. Their branches are then closed in Lemmas III.2.13 and III.2.14.

The fifth-power certificates are the six adjacent sign brackets, the two endpoint values, and the two shell comparisons written in the chapter; direct substitution evaluates each exactly. The tenth-power proof gives the whole factor classification and excludes its last candidate. Thus no unexplained box bound on the larger roots or an independently assumed exponent cutoff enters the argument.

### Established Fermat attribution

**Wiles, Andrew (1995).** [“Modular elliptic curves and Fermat's Last Theorem”](https://annals.math.princeton.edu/1995/141-3/p01). *Annals of Mathematics*, second series, 141(3), pp. 443–551. DOI: [10.2307/2118559](https://doi.org/10.2307/2118559). This is the principal publication for the established modularity route to Fermat's Last Theorem, credited in connection with Chapter III.2.

**Taylor, Richard, and Andrew Wiles (1995).** [“Ring-theoretic properties of certain Hecke algebras”](https://annals.math.princeton.edu/1995/141-3/p02). *Annals of Mathematics*, second series, 141(3), pp. 553–572. DOI: [10.2307/2118560](https://doi.org/10.2307/2118560). This companion contribution belongs with the Wiles attribution. The two publications identify the established proof tradition; Chapter III.2 separately states the scope and dependencies of its bounded-side derivation. Neither citation closes the manuscript's open independent unrestricted route.
