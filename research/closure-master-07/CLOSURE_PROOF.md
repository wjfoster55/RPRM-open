# Carry, return, and a justified endpoint

Evidence grade: elementary written proofs, accompanied by fresh finite checks. These are not machine-checked formal proofs or a new proof of a Millennium conjecture. The selected carry operation below is a precise model for William's sawtooth proposal; it is not asserted to exhaust his proposed RPRM operations.

## 1. Contract and the exact diagonal

Supply a base `b >= 2`, a nonempty finite digit tuple `d=(d_1,...,d_n)` in `{0,...,b-1}^n`, and fixed positive integer weights `w_i`. Equality of tuples is coordinatewise; equal values at different positions remain different occurrences. Put `A=sum_i w_i`. One forward step adds one to **each** digit modulo `b`. The digit map is a bijection, with inverse subtract-one modulo `b`. It has period exactly `b` on every admitted tuple.

The wrapped receiver observes

\[
d_{i,k}=(d_i+k)\bmod b,\qquad F_k=\sum_i w_i d_{i,k}.
\]

The retained receiver also observes weighted accumulated wraps

\[
C_k=\sum_i w_i\left\lfloor\frac{d_i+k}{b}\right\rfloor,
\qquad C_0=0.
\]

Time `k` and the accumulated wraps are extra data: the finite tuple does not determine how many times its orbit was traversed. Euclidean division gives, for every admitted digit and every integer `k >= 0`,

\[
d_i+k=d_{i,k}+b\left\lfloor\frac{d_i+k}{b}\right\rfloor.
\]

Multiplying by weights and summing proves the exact lift

\[
\boxed{L_k:=F_k+bC_k=F_0+Ak.}\tag{1}
\]

If `W_k=sum_{i:d_{i,k}=b-1} w_i` is the weighted set of digits about to wrap, the exact successor rules are

\[
F_{k+1}-F_k=A-bW_k,\qquad C_{k+1}-C_k=W_k.\tag{2}
\]

After a full turn,

\[
F_{k+b}=F_k,\quad C_{k+b}=C_k+A,\quad L_{k+b}-L_k=bA.\tag{3}
\]

Thus a repeating, possibly jagged sawtooth and a straight line are compatible observations of the same declared process. A line's numerical slope depends on the chosen weights and time units; it is not an assertion about physical dimensions or a universal 45-degree angle.

### The supplied decimal example

For the word `5426`, choose weights `(100,10,10,1)`. This deliberately merges the middle two digits into the same tens contribution: `100*5+10*4+10*2+6=566`. It is **not** the ordinary place-value interpretation `5426`.

Here `A=121`, so

\[
L_k=566+121k.
\]

At `k=10`, the digit tuple and wrapped value return to `5426` and `566`; `C_10=121` and `L_10=1776`. The full-turn drift is **1210**. The plot is generated from exact integer values, not fitted decimals.

![Wrapped and retained trajectories](figures/sawtooth_and_lift.png)

### Fibers and the missing inverse

For a fixed initial tuple, observing that tuple again admits times `k=jb`, `j>=0`. Observing only `F` can merge still more states: `5426` and `5246` have equal weighted readout and equal future weighted readouts under this uniform increment, but they are different source tuples. A receiver that later addresses either middle occurrence separately can distinguish them. A weighted sum has no unconditional inverse to the original ordered tuple.

For a known initial tuple and known weights, the lifted readout determines `k=(L-F_0)/A` when this is an admitted nonnegative integer. It does not recover an unknown initial tuple without additional data. The projected digit map is reversible; the legal forward history with `C_0=0` has an initial boundary and is not a two-sided unbounded history by default.

No terminal predicate or upper budget follows from (1). An arbitrary restriction `k<=K` imposes a boundary; it does not prove that a separate analytic or arithmetic question is resolved there.

## 2. When a cycle's accumulated cost can be a state difference

**Finite potential theorem.** Let `X` be a supplied finite set, `T:X -> X` a deterministic total map, and `h:X -> R` a real edge cost. There is a function `g:X -> R` satisfying

\[
h(x)=g(x)-g(Tx)\tag{4}
\]

if and only if the sum of `h` on every directed cycle is zero.

**Necessity.** Summing (4) around a cycle cancels every potential value, leaving zero.

**Sufficiency.** Each weak component of a finite functional graph has one directed cycle. Choose one cycle vertex and set its potential to zero. Use (4) to propagate around the cycle; the zero cycle sum is precisely the consistency condition on return. Then set `g(x)=h(x)+g(Tx)` successively along each finite tree entering that cycle. This assigns every vertex and satisfies every edge. All solutions differ by one arbitrary additive constant on each weak component. The empty graph has the unique empty assignment. This gives the complete solution family, not merely an unfinished search.

An additive accumulator `z_{k+1}=z_k+h(x_k)` may therefore drift even when `x_k` returns. Changing the state coordinate by `z'_k=z_k+g(x_k)` changes its edge cost to `h(x)+g(Tx)-g(x)`. The sum on a cycle is unchanged.

For the carry model take `h(x)=bW(x)`. Equation (2) implies

\[
h(x)-A=F(x)-F(Tx).
\]

The fluctuating part is a state difference, but the full cycle has sum `bA>0`. No potential on the finite digit states can eliminate that mean drift. Retaining the lift accounts for it exactly. This elementary obstruction makes precise why a closed display alone cannot certify that the underlying accumulated quantity vanished.

Scope: this theorem concerns additive scalar costs on a finite deterministic graph. It does not automatically cover nondeterministic transitions, noncommuting operator products, analytic boundary limits, or a continuum of states. Each extension requires its own contract.

## 3. Three different ways an endpoint can actually be forced

### A. A well-founded discrete rank

Suppose a process has a rank `r(x)` in the nonnegative integers. Every admitted nonterminal state has a next step; rank zero is terminal; and every nonterminal step reduces the rank by at least one. It follows inductively that at most `r(x_0)` steps occur before a terminal state is reached.

The terminal state must also certify the requested result. For a polynomial-time algorithm, the initial rank, state representation, and **all work between decreases**, including finding a valid step, must have suitable polynomial bounds in input bit length. A rank that decreases only on occasional successful updates does not bound unsuccessful searches or a scheduler that repeats a redundant operation forever.

### B. An error bound and an independently known separation

If a residual `D` is independently known to belong to `delta*Z`, with `delta>0`, then `|D|<delta` forces `D=0`.

A p-adic version makes the missing data explicit. If `D=a/b` is reduced, `5` does not divide `b`, `|a|<=H` is known, and `v_5(D)>=N` for an integer `N>=0` with `5^N>H`, then `5^N` divides `a`, so `a=0`. Use `v_5(0)=+infinity`. Without the height bound, `a=5^N` is a nonzero counterexample at every finite precision. Without a theorem placing the actual target in this rational class, the criterion does not apply at all.

Alternatively, a single fixed real `D` satisfying a proved bound `|D|<=epsilon_k` for **every** `k`, where `epsilon_k -> 0`, is exactly zero. What matters is the proved universal continuation and that the same residual is bounded. Computing finitely many increasingly accurate approximations does not establish that quantifier.

### C. Sufficient accumulated decrease through every transition

Here is a simple continuous version. Suppose a process surviving until time `T` supplies a nonnegative quantity `B` on that interval. On every finite interval it is piecewise absolutely continuous, has only finitely many jumps, all jumps are nonpositive, and satisfies `B'(t)<=-q(t)` almost everywhere between jumps. Assume `q>=0` is locally integrable and `integral_0^T q` is unbounded as `T -> infinity`. Integrating on the pieces and summing the jumps gives

\[
B(T)\le B(0)-\int_0^Tq(t)\,dt.
\]

The right side eventually becomes negative, so survival forever is impossible. An analogous version uses continuous functions and a justified upper Dini derivative comparison. A geometric application must establish its actual comparison regularity, persistence of the witness, and behavior through surgery or other singular transitions.

`B(t)=exp(-t)` is strictly decreasing and positive forever; its accumulated decrease is finite. The discrete sequence `2^-k` likewise never reaches zero. Separately, finite systems with positive gaps `Delta_n=2^-n` have no positive uniform gap. These distinguish monotonicity, finite termination, and a positive bound surviving a limit.

## 4. Poincare supplies a real reference, with additional mathematics

Perelman's finite-extinction theorem assumes a closed oriented three-manifold whose prime decomposition has no aspherical factors, with any initial metric. On a surviving component carrying the nontrivial class tracked by the proof, the least-disk-area minmax quantity satisfies a comparison

\[
D^+A\le-2\pi-\tfrac12 R_{\min}A,
\qquad R_{\min}\ge-\frac{3}{2(t+C)}.
\]

Here `C>0` is chosen from the initial scalar-curvature bound. For `B=A/(t+C)`, this gives

\[
D^+B\le-\frac{2\pi}{t+C}-\frac{A}{4(t+C)^2}
\le-\frac{2\pi}{t+C}.
\]

The accumulated term `2*pi*log((T+C)/C)` is unbounded. The general case also uses the prime-decomposition and surgery reduction in §1.5; one does not assume a single fixed witness automatically persists on every component. Topological witnesses, comparison through controlled surgeries, and the topology of discarded pieces are essential to the argument. Simply connectedness then selects `S^3` from the resulting classification. A flat three-torus is an excluded, aspherical stationary-flow control. [Perelman, finite extinction, §§1 and 3](https://arxiv.org/pdf/math/0307245)

The [reference audit](agents/POINCARE_REFERENCE.md) separates this original proof from the Colding–Minicozzi sphere-width argument, records the needed surgery and noncollapsing conditions, and preserves the Morgan–Tian correction. The lesson is a conditional method for searching for estimates, not a transport of Ricci-flow theorems to a different carrier.

## 5. Verification and remaining obligation

The source [check_closure.py](work/check_closure.py) uses exact integers and fractions. Fresh evidence covers 10,477 source states and 216,583 successor checks in four admitted radix/weight families; all 729 three-state functional-graph/cost models; every parity cube at boundary sizes 3 through 8; and explicit stopping counterexamples. Its bounded potential search is complete for the tested three-state costs in `{-1,0,1}`: anchoring a zero-sum cycle and its trees needs potentials of magnitude at most two. The written proofs above cover their stated arbitrary parameters independently of those tests.

**OPEN bridge:** construct an operation from the actual domain data that preserves the requested readout, then derive a bound satisfying that domain's quantifiers without assuming the desired conclusion. For BSD this includes the exact boundary identity and actual Sha identification; for YM it includes uniform continuation and the continuum theory; for P versus NP it includes the cost of constructing and composing exact retained relations. Neither the existence of the diagonal nor a repeated occurrence of a familiar digit supplies these missing ports.
