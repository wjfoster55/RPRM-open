# A forward/backward RPRM bridge

Evidence: elementary written proofs plus bounded exact execution. This is an RPRM-first construction: start with occurrences, operations, receiver requirements and a missing handoff; then translate the proposed relations into explicit mathematics. It does not replace the source laws or infer how close any open conjecture is to resolution.

## 1. What we recovered before constructing the bridge

William's earlier correction calls seven the **most complete state pre-carry**. The recovered record explicitly distinguishes finishing a local object from transferring and accepting that object in its receiving context. It also records that the individual eight/nine operations were not observed in that experiment. The corpus contains other seven/eight counts with different mathematical carriers; they do not define this process. [Exact recovery and corrections](agents/CORPUS_MAP.md)

The proof-donut donor requires a common completion fiber, compatible constraints, coverage and a landing back at the original question. Backward arrows may ask for a preimage; they are not automatically inverse functions. We therefore propose three separate operations:

1. derive what the supplied source can actually produce;
2. propagate a specified receiving condition backward through the same laws;
3. test whether they meet at the **same full intermediate state**, with a receiver that distinguishes existence from a forced conclusion.

These are candidate process roles. We do not assign canonical eight/nine labels or count the surrounding evidence to force a missing center.

## 2. Rise and fall are exact inverse motions on a retained carry state

Fix integers `b>=2`, `Q>=0`. The finite carrier is

\[
X_{b,Q}=\{(q,d):-Q\le q\le Q,\ 0\le d<b\},
\qquad z=bq+d.
\]

Here `q` is a signed carry row, `d` is a digit, and equality retains both coordinates. Increment `U` acts where `z` is below the upper boundary; decrement `D` acts where `z` is above the lower boundary. They change `z` by `+1` and `-1`. At a wrap,

\[
U(q,b-1)=(q+1,0),\qquad D(q,0)=(q-1,b-1),
\]

when the new row remains admitted. Each map is the partial inverse of the other on its actual image.

Define the reflection

\[
R(q,d)=(-q,b-1-d),\qquad R(z)=b-1-z.
\]

This is a total involution on this symmetric carrier. Direct substitution proves

\[
R\,U=D\,R,\qquad R\,U\,R=D,\tag{1}
\]

including enabledness: `U` is enabled at `z` exactly when `D` is enabled at `R(z)`. Thus the partner falls precisely when the first side rises. Their conserved total is

\[
z+R(z)=b-1.\tag{2}
\]

For base ten with `Q>=1`, starting at 7, the paired path is

| Step | Rising lift | Falling lift | Rising `(row,digit)` | Falling `(row,digit)` |
|---:|---:|---:|---|---|
| 0 | 7 | 2 | `(0,7)` | `(0,2)` |
| 1 | 8 | 1 | `(0,8)` | `(0,1)` |
| 2 | 9 | 0 | `(0,9)` | `(0,0)` |
| 3 | 10 | -1 | `(1,0)` | `(-1,9)` |
| 4 | 11 | -2 | `(1,1)` | `(-1,8)` |
| 5 | 12 | -3 | `(1,2)` | `(-1,7)` |

The partner of 10 is -1 in this retained chart. Printing its last digit 9 alone would forget the row -1. The cyclic digit mirror is also an exact operation, but it answers a different receiver.

This generalizes to the previous weighted tuple lift: reflecting each lifted digit gives total `(b-1)*sum(weights)`. That is why the folded four-digit model has mirror center `1089/2`, not the center of an ordinary three-digit display.

The paired conservation does not itself force completion. On the separately declared integer carrier, `z_k=7+k` and its partner `2-k` continue for every `k>=0`. The finite carrier stops at its imposed boundary; that boundary must have a problem-derived meaning to certify a problem-derived endpoint.

## 3. What it means for the two directions to meet

Supply a finite state set `X`, a transition relation `T` on `X`, source subset `I`, receiving subset `G`, horizon `N>=0`, and split `0<=k<=N`. Nondeterminism is allowed. The state must retain every coordinate affecting future enabledness and observations; a time-dependent law can instead use time-tagged states.

Let `F_k` be the states reachable from `I` in exactly `k` steps. Let `B_(N-k)` be the states from which a member of `G` can be reached in exactly `N-k` steps, found by relational preimages. Define

\[
S_k=F_k\cap B_{N-k}.\tag{3}
\]

**Seam theorem.** There is a lawful length-N path from `I` to `G` if and only if `S_k` is nonempty. More precisely, `S_k` is exactly the set of kth states of all such paths.

**Proof.** Every full path provides a prefix ending at its kth state and a suffix beginning at that same state, proving one inclusion. Conversely, a member of `S_k` has a witnessed prefix and a witnessed suffix with the same meeting state. Concatenating them constructs a lawful full path. Retaining every compatible prefix/suffix pair gives the complete path family, including multiple paths sharing a meeting state. Empty input sets and zero-length paths are covered by `F_0=I`, `B_0=G`.

In relational language, if the prefix is `P subset I x X` and suffix is `Q subset X x G`, retain triples `(i,x,g)` with `(i,x) in P` and `(x,g) in Q`. These triples preserve the endpoints and meeting state, not every internal path history; the full histories need their own retained witnesses. Independent coordinate lists can invent joins using two different middle occurrences.

### The separating carry example

Use base ten and the finite carrier with `Q=2`, increment only, source 7, horizon five and split two.

| Receiving target | Forward seam value | Backward seam value | Same last digit? | Lawful full path? |
|---:|---:|---:|---|---|
| 2 | `9=(0,9)` | `-1=(-1,9)` | Yes | No |
| 12 | `9=(0,9)` | `9=(0,9)` | Yes | Yes: `7,8,9,10,11,12` |

Thus **compare before discarding the carry**, or retain a summary already proved sufficient for this target and its continuations. The wrong target 2 was a supplied hostile input, not a result deduced from a desired answer.

### Existence is different from proving the actual source has the target property

If an unknown actual source lies in `H={0,1}`, intersecting H with the desired condition `x=0` leaves a singleton, but does not prove the actual source equals zero. It only finds a source that would satisfy the condition. Likewise, a nonempty bidirectional seam proves a compatible path exists; it does not say every possible path has the requested readout.

To force a readout of an unknown actual source, its membership in the retained completion family must be proved independently, and the readout must be constant on that entire nonempty family. For a universal theorem, all intended sources must be covered. A backwards target is a legitimate source of necessary constraints, not evidence that the original system satisfies them.

## 4. A paired budget can force stopping, under explicit conditions

The paired picture suggests an additional candidate: one side records completed work `a`, the other records the remaining budget `r`, with `a+r=E` and `r>=0`. Suppose every nonterminal step transfers at least a fixed `epsilon>0` from r to a, with no external replenishment. After n such steps,

\[
0\le r_n\le r_0-n\epsilon,
\quad n\le\lfloor r_0/\epsilon\rfloor.\tag{4}
\]

This bounds the steps. To infer a valid terminal result, a nonterminal state must always admit a next step satisfying these laws, and terminal status must imply the requested result. Otherwise exhausting the budget may only leave the method stuck.

Two hostile cases show the load-bearing assumptions:

- **Shrinking step cost:** `a_k=1-2^-k`, `r_k=2^-k` conserve total one and keep `r_k>0` forever. Each step consumes a positive amount, but there is no fixed positive minimum consumption.
- **Hidden replenishment:** a displayed budget repeatedly reset from zero to two allows unlimited steps. The correct law is `a+r=E+incoming`, retaining the accumulated incoming resource. Erasing that boundary term creates a false closure proof.

These are concrete candidates for the user's falling/rising relation. No such nonreplenished budget or minimum cost has been established for the BSD defect, the YM continuum construction, or general SAT. The budget has to be derived from their data; naming the desired result “zero remaining” would be circular.

## 5. Backward constraints sharpen the actual BSD search

The BSD subtask applies the same method to the actual rank-two determinant, rather than choosing digit patterns. Let

\[
\mathcal R(p,q,s)=pq-\frac{(s-p-q)^2}{4}.
\]

Refining p by u and q by v while holding s fixed gives the exact mixed finite difference

\[
\Delta_p\Delta_q\mathcal R=uv/2.\tag{5}
\]

A potential built as a sum of independent single-height terms has mixed difference zero. It therefore cannot match the required BSD defect on an admitted two-direction refinement grid when `u,v,Omega,sigma` are nonzero. The [BSD seam proof](agents/BSD_SEAM.md) derives the exact source increments, normalizations, exceptional cases and the limited scope of this obstruction.

This is a useful backwards discovery: the receiving formula forces **joint interaction terms** before we attempt to construct the bridge. Retaining those terms repairs this particular candidate grammar. It does not prove that the resulting expression equals the independent analytic side, or identify Sha.

## 6. Result of this pass

The exact mirrored rise/fall model survives its wrap and boundary checks. Meeting by last digit fails. Joining on the retained state succeeds for the declared path question. A paired conserved total needs a quantitative budget law to force termination. The backward BSD test narrows a candidate class by a source-generated obstruction.

Fresh [bridge evidence](evidence/bridge.json) checks 270 carry states, 261 enabled forward edges, and 69,120 seam equalities across all 512 relations on three states. [Budget evidence](evidence/budget.json) checks 44 finite constant-cost cases and retains the nontermination and replenishment controls. These are bounded executions; the written proofs establish their separately stated parameterized laws. A more compact or efficient representation is a further claim, not a consequence of bidirectionality.

The RPRM jump here is to make the **receiving handoff** the object of investigation: what extra joint structure must a locally complete result retain so that the next context can accept it? The equations define and test part of that idea. The full domain bridge remains OPEN.
