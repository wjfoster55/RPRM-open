# Hostile audit: the exchange lemma for `sigma_E`

**Date:** 17 September 2026  
**Verdict:** **THEOREM**, on the stated domain: positive arity `r >= 1`,
positive block sizes, fixed finite `n` and `m`, and the uniform prior over all
partial maps `S^r -> S`.

**Evidence grade:** independently checked written proof plus exact finite
recomputation. This is not a formal proof.

The exchange lemma and its extremal-profile corollary are correct. Two parts of
the surrounding explanation are not:

1. the constant `+1` is **not** essential to log-convexity; deleting it leaves
   another sum of exponentials, so the same proof also proves the total-map
   extremal law;
2. the claim that the product-multiset majorisation route “fails” is too strong.
   The route works directly by tensoring a doubly stochastic map.

Those errors do not invalidate the theorem for `sigma_E`, but they should be
corrected before publication.

## 1. Typed scope audited

- Carrier: a finite set `S`, `|S|=n`, partitioned into `m` nonempty blocks with
  profile `p=(n_1,...,n_m)`.
- Equality: equality of integer block sizes; profiles are multisets. “Unique”
  below means a unique **profile**, not a unique labelled set partition.
- Operation: a deterministic partial map `S^r -> S`, with `r >= 1`.
- Survival receiver: enabledness is constant on each product block and all
  defined outputs from a product block land in one partition block.
- Readout:

  `sigma_r(p) = product_T f_p(e_T)`,

  where `T` ranges over ordered `r`-tuples of blocks,
  `e_T=product_{i in T} n_i`, and
  `f_p(k)=1+sum_j n_j^k`.
- Exchange: choose occurrences of blocks `a >= b >= 2` and replace them by
  `a+1,b-1`, obtaining `q`.

The closed form follows because each product block is independently either
wholly undefined (one choice) or maps arbitrarily into one selected target
block (`n_j^k` choices). I found no issue in that counting argument.

## 2. Log-convexity

For every profile `q`,

`f_q(k)=exp(0*k)+sum_j exp(log(q_j)*k)`.

Thus `h(k)=log f_q(k)` is a log-sum-exp function and is convex for every real
`k`, not merely for integer block sizes. Equivalently, `h''(k)` is the weighted
variance of the numbers `0,log(q_1),...,log(q_m)`, hence is nonnegative.
Therefore the property holds at every positive integer and at every product of
positive block sizes used at higher arity.

The text's statement that the constant `1` “is what makes this work” or that
the result is “false without it” is false. Without it,

`g_q(k)=sum_j q_j^k`

is still a sum of exponentials and is still log-convex. The `+1` is essential
to the **partial-map count** because it represents the wholly undefined choice,
but it is not essential to the analytic inequality.

The successor-only factor is different:

`f_blind,p(k)=sum_j (n_j+1)^k-(m-1)`.

This minus-constant function can fail log-convexity. An exact counterexample is
`p=(1,1)`, for which `f_blind(k)=2^(k+1)-1`:

`f_blind(2)^2 = 7^2 = 49 > 3*15 = f_blind(1)f_blind(3)`.

By contrast, the plus-one `sigma_E` factor passes the corresponding inequality.

## 3. Unary exchange proof

The unary proof is valid.

1. The exchanged pair `(a+1,b-1)` strictly majorises `(a,b)`. Hence, for every
   `k>=1`, `sum q_j^k >= sum p_j^k`; equality holds at `k=1`, and the inequality
   is strict at every `k>=2`.
2. Convexity of `h=log f_q` and `a>=b` give
   `h(a+1)-h(a) >= h(b)-h(b-1)`, hence
   `f_q(a+1)f_q(b-1) >= f_q(a)f_q(b)`.
3. Replacing every remaining `f_q(k)` by `f_p(k)` can only decrease the product.
   It decreases it strictly at the old all-`a` factor because `a>=2`.

There is no hidden equality case: even if the exponent/log-convexity step is an
equality, the base step is strict at exponent `a>=2`.

## 4. Higher arity

The convex-order reduction in the written proof is valid. In each cell:

- the before draw is uniform on `{a,b}` and the after draw on
  `{a+1,b-1}`, so the latter dominates in convex order at equal mean;
- multiplying by an independent nonnegative factor preserves convex order,
  because `x -> phi(xy)` is convex for every fixed `y>=0`;
- induction handles the product of the changed coordinates;
- scaling by the fixed positive spectator product preserves the order;
- each before/after cell has the same cardinality, so its average inequality
  converts to a sum inequality, and sums over the disjoint cells add.

I found no gap in the independence or disjoint-union step.

However, the product-multiset majorisation route does not actually fail. Since
`q` majorises `p`, there is a doubly stochastic matrix `D` with `p=Dq`.
Tensoring gives

`p^(tensor r) = D^(tensor r) q^(tensor r)`.

`D^(tensor r)` is doubly stochastic, and the coordinates of these tensor powers
are exactly the ordered-tuple products `e_T`. Therefore the new exponent vector
majorises the old exponent vector directly. This gives a shorter alternative
to the cellwise convex-order proof.

Strictness at all positive arities again comes from the old all-`a` tuple:
its exponent is `a^r>=2`, so at least one base-comparison factor is strict.

## 5. Extremal law and coverage boundary

The exchange lemma implies the claimed extrema over profiles of fixed `n,m`.

- If a profile is not balanced, it has `a>=b+2`; applying the lemma in reverse
  strictly lowers `sigma_r` and iteration ends at the balanced profile.
- If a profile is not `(n-m+1,1,...,1)`, a non-largest block has size at least
  two; a forward exchange strictly raises `sigma_r` and iteration ends at that
  maximally unequal profile.

Thus `sigma_r` has a unique maximum profile at the blob-plus-singletons shape
and a unique minimum profile at the balanced shape. Since the ambient count
`(n+1)^(n^r)` is fixed, fragility has the reverse extrema.

The stated prior boundary is partly right:

- **Bijective prior:** still false. At `n=4,m=2`, `(2,2)` admits 8 surviving
  permutations while `(3,1)` admits 6.
- **Fixed domain size:** still false. At `n=6,m=3,d=4`, `(2,2,2)` has 432
  survivors while `(4,1,1)` has 258.
- **Idempotent prior:** not covered; idempotence couples choices across product
  blocks and destroys the independent factorisation used here.
- **Total-map prior:** contrary to the document, it **is covered by the same
  proof**. Its factor is `g_p(k)=sum_j n_j^k`, also a log-convex sum of
  exponentials. The base and exponent arguments, including higher arity and
  strictness, transfer unchanged.

The explicit theorem says `r>=1`. That qualifier is necessary. At nullary
arity `r=0`, there is one input tuple and `sigma_0(p)=n+1`, independent of the
profile, so a strict exchange lemma would be false.

## 6. Classical successor-only claim

Failure of log-convexity shows that this proof route is unavailable for
`sigma_blind`; by itself it does not imply an extremal-law failure. The finite
enumeration supplies the latter evidence.

I independently reproduced the reported unary census through `n=26`:

- 42,903 distinct exchanges;
- 3,871 failures of the exchanged-exponent log-convexity inequality;
- 66 strict decreases of `sigma_blind`;
- 0 of those 66 outside the 3,871 failures;
- no equality cases among the 66 losses.

Therefore “all 66 losses sit inside the log-convexity failures” is correct as a
finite containment statement. It is not an equivalence or a characterisation:
only 66/3,871, about 1.7%, produce an actual exchange loss. Spectator gains
overcome the other failures. Phrases such as “precisely what destroys ... the
extremal law” or “exactly where” should retain this qualifier.

## 7. Tests rerun

Fresh runs from the research worktree:

- `fragility_proof.py 30`: 128,121 exchanges over 28,622 profiles; every unary
  proof step and direct `sigma_E` comparison passed.
- `fragility_arity.py`: 963 exchanges at arities 2, 3 and 4; cell decomposition,
  six convex probes, two concave controls, and direct `sigma_r` checks passed.
- `fragility_mechanism.py`: 25,702 probes per factor function; 0 `sigma_E`
  log-convexity failures and 7,488 successor-only failures.
- `fragility_predict.py`: reproduced 42,903 / 3,871 / 66 / 0 exactly.

I did not rerun the older 5,686,463-exchange search to `n=40`; the smaller
proof-step census and the independent hostile checks were sufficient because
the warrant is the written proof, not that larger search.

Independent code, not importing the supplied scripts, also checked:

- exponent-product majorisation at previously untested arities 5, 6 and 7 on
  30 profile exchanges at each arity: 0 failures;
- exact strict `sigma_E` increases on selected arity-5, 6 and 7 boundary cases:
  all passed;
- the same selected cases for total maps: all passed;
- the 42,903 classical exchanges and the 66-in-3,871 containment: reproduced.

## Final disposition

**ONE(THEOREM)** for the exchange lemma and unique extremal **profiles** at every
positive arity under the uniform prior over all partial maps.

The proof survives hostile audit. The explanatory claims about the necessity of
the constant `+1`, failure of product-multiset majorisation, and exclusion of
total maps do not.
