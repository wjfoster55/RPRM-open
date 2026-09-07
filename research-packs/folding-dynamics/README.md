# Folding dynamics: preserving specified transition questions

**EXPERIMENTAL RESEARCH PROPOSAL — UNEXECUTED.** This pack specifies a finite stochastic reduction and a possible molecular-simulation evaluation. No trajectory bundle has been acquired, no folding model has been fitted, and no biological or speed improvement is reported. The complete four-state example below is synthetic.

The proposed contribution is an explicit account of which microscopic distinctions a chosen future question requires. The algorithm is conventional partition refinement under the standard strong-lumpability condition. RPRM supplies the question/representation/update contract and the requirement to retain counterexamples and reopening information. Any claim of a better molecular method must survive comparison with ordinary Markov-state coarse graining given the same inputs and budget.

## 1. The question and its source model

Choose one published molecular simulation setting, one state assignment and one lag. Ask whether a reduced state preserves specified next-state distributions and finite-horizon observables. Keep the force field, solvent, temperature, sampling scheme and trajectory ancestry with that question. A static conformation minimum does not specify these objects.

The NTL9(1–39) folding study by Voelz and colleagues is a concrete source lead because it combines molecular simulation with a statistical state model. This pack does not claim that its complete input trajectories are presently available in a validated reusable bundle. Recovering the actual inputs and reproducing the relevant source analysis precede a new comparison. [Primary study, 2010](https://pmc.ncbi.nlm.nih.gov/articles/PMC2835335/).

The immediate mathematical carrier can also be a supplied finite transition matrix. That permits exact algorithm checks without implying any molecular interpretation. A result on such a matrix establishes a property of that matrix. A fitted matrix adds estimation error; a physical interpretation adds model and measurement error.

## 2. Proposed inputs and retained information

The following is a proposed normalized schema, not a claim about column names in an existing data release.

| Object | Required fields and meaning |
|---|---|
| Source manifest | Source DOI/version, exact file hashes, reuse terms, source processing version and model settings |
| Trajectory manifest | Neutral trajectory key, run/seed group, model context, time unit, saved-frame spacing, provenance linking restart segments |
| Frame assignment | Trajectory key, frame order, original time, admitted finite microscopic state ID, state-assignment version |
| State manifest | Ordered finite state IDs and the definition of each state; coverage and excluded states |
| Observable contract | Named readouts, their units, target-state membership and any finite horizon; observed and unobserved values remain distinct |
| Transition model | Ordered matrix, lag, estimator, count policy, zero-row disposition, and whether entries are exact supplied probabilities or estimates |
| Evaluation freeze | Group split, baselines, metrics, tolerances, fit settings, cost budget and decision rules |

Never create a transition across the end of one trajectory and start of another. Restarted pieces sharing a parent run stay in the same split. A lag of $\ell$ saved-frame steps uses within-trajectory pairs $(x_t,x_{t+\ell})$, with actual physical lag verified against saved times. Irregular frame timing requires an explicitly different pairing rule.

For a simple empirical estimator, define transition counts $N_{ij}$ from the admitted training pairs, and set
$$
\widehat P_{ij}=N_{ij}/\sum_kN_{ik}
$$
only when the row denominator is positive. A state with no observed outgoing pairs has an unknown row. It is not silently assigned a self-loop. Smoothing, reversibility constraints or another estimator must be declared as additional modeling choices. Exact arithmetic can preserve count fractions, but does not turn estimated probabilities into exact physical probabilities.

Retain the base assignments, count matrix and source manifest while exploring reductions. The reduced matrix alone cannot reconstruct individual trajectories, hidden-state identities or a state assignment that was discarded. Store derived partitions as separate versioned outputs with a route back to the admitted source.

## 3. Exact reduction and a constructive repair

For a finite nonempty state set $S$, supply a complete stochastic matrix $P$, meaning nonnegative entries and row sums one. An initial partition $\mathcal P_0$ specifies the distinctions that must survive: states can be grouped only when every requested current readout agrees. For a target-hitting question, target membership is one such readout. Continuous readouts may force singleton blocks unless an explicit approximation convention changes the request.

For a current partition $\mathcal P$, define the signature of state $x$ as
$$
\operatorname{sig}_{\mathcal P}(x)=
\left([x]_{\mathcal P},\
\left(\sum_{y\in B}P_{xy}\right)_{B\in\mathcal P}\right).
$$
The first component retains the old block; the remaining components give the complete next-block distribution in a fixed block order. Split states into equal-signature classes and repeat until the partition stops changing. For an executable protocol, admit exact rational entries as integer numerators with positive integer denominators and use exact equality. The written finite argument also applies when exact comparisons of a more general supplied number field are available; it supplies no algorithm for deciding equality of arbitrarily described real numbers. Canonicalize the initial partition by input-state order, with blocks ordered by their first state, so a mere reordering is not counted as a refinement.

```text
admit a finite nonempty ordered state list and a complete stochastic P
admit an initial partition that covers each state exactly once
canonicalize its members and blocks by the input-state order
partition = canonical_initial_partition
repeat:
    for each state x:
        signature[x] = (old block of x,
                        exact sum of P[x,y] into each old block)
    refined = classes of identical signatures
              (ordered by their first state in the input order)
    if refined == partition:
        stop
    retain this split and its distinguishing rows
    partition = refined
for each final block A and target block B:
    Q[A,B] = sum(P[x,y] for y in B), using any x in A
return partition, Q, all source bindings, and retained split witnesses
```

**Finite repair theorem.** This procedure terminates and returns the coarsest refinement of $\mathcal P_0$ whose states have equal next-block distributions within each block. Its output defines an exact reduced Markov chain for every initial distribution. If there are initially $k$ blocks and $n=|S|$, at most $n-k$ strict refinements occur.

**Proof.** Every step retains old block identity, so it only splits. A strict change increases the number of nonempty blocks, bounded above by $n$, proving termination and the stated bound. At a fixed point, equal-block states have identical aggregate rows by the signature definition. Thus the quotient row is independent of its chosen representative, is nonnegative and sums to one.

To prove coarseness, let $\mathcal R$ be any stable refinement of $\mathcal P_0$. Inductively suppose each current block is a union of $\mathcal R$-blocks. Two states in one $\mathcal R$-block have equal transition sums into every $\mathcal R$-block. Summing these equalities over each current block shows that they have identical current signatures and are never separated by the next refinement. Thus $\mathcal R$ refines every iterate and the final partition. The final stable refinement is therefore the coarsest one.

Finally, given any reduced history of positive probability, the conditional microscopic state is a mixture within its current block. Every state in that block has the same next-block row. Their mixture gives that row, independently of the earlier reduced history. This proves the reduced Markov property for every initial distribution. $\square$

This is an exact finite-matrix result. Comparing floating-point signatures with an unspecified tolerance changes the algorithm. Rounding first defines a different supplied matrix, which must itself be stochastic and whose relation to the original must be quantified. The number of refinement steps is not a wall-time bound: charge for building and comparing signatures and retaining the original model.

## 4. A complete positive and hostile example

Use state order $a,b,c,d$, initial blocks $A=\{a,b\}$, $B=\{c,d\}$, and
$$
P=\begin{pmatrix}
1/2&1/4&1/4&0\\
1/4&1/2&0&1/4\\
1/4&0&1/2&1/4\\
0&1/4&1/4&1/2
\end{pmatrix}.
$$
The complete signatures after the old-block component are $(3/4,1/4)$ for both $a,b$ and $(1/4,3/4)$ for both $c,d$. No split occurs, and
$$
Q=\begin{pmatrix}3/4&1/4\\1/4&3/4\end{pmatrix}.
$$
Every block path probability is preserved. Starting at $a$, the probability of $B$ after two steps is $3/8$, whether computed microscopically or with $Q$.

Now replace rows $b,d$ by $(1/4,3/4,0,0)$ and $(0,0,1/4,3/4)$, leaving the other rows unchanged. The four complete block-distribution signatures are now
$$
a:(3/4,1/4),\quad b:(1,0),\quad
c:(1/4,3/4),\quad d:(0,1).
$$
Both initial blocks split; the final partition has four singletons. Exact preservation of those original block observations and their futures admits no coarser stable refinement in this example. The algorithm has correctly declined to compress.

Both matrices are symmetric and stochastic, so both admit the uniform stationary microscopic distribution and the same block occupancies $(1/2,1/2)$. Equilibrium agreement therefore fails to certify dynamical preservation. These matrices are unitless mathematical controls, not sampled molecular trajectories.

## 5. Approximate reductions and testable tolerances

Exact refinement of a noisy fitted matrix may return nearly all singletons. That outcome does not refute the possibility of a useful approximate reduction; it refutes the advertised exact reduction for that matrix and initial partition.

An approximate candidate supplies its own stochastic $Q$. For every microscopic row define
$$
\varepsilon_x=\frac12\sum_B\left|
\sum_{y\in B}P_{xy}-Q_{[x],B}\right|,
\qquad\varepsilon=\max_x\varepsilon_x.
$$
For a completely supplied finite $P$, this is a complete row audit. After $t$ steps, the difference in block marginals is at most $\min(1,t\varepsilon)$: mix the one-step row bounds, use contraction of total variation under stochastic multiplication, and induct from zero initial error. This bound is derived in the manuscript's molecular research chapter. It does not automatically bound every path statistic or infinite mean passage time.

For empirical $\widehat P$, report this fitted-matrix residual separately from held-out evidence about transition behavior. A row with few or no sampled transitions must not receive an unwarranted confidence claim. A tolerance and useful physical time horizon are selected using development information, simulation uncertainty and the requested observable before final evaluation.

## 6. Evaluation designed to distinguish useful outcomes

Freeze the state assignment using training data or a separately supplied published assignment. Keep entire trajectory groups out of fitting and hyperparameter selection. The baseline receives the same trajectories, lag and source features as the proposed method. At least three comparisons are needed:

1. The unreduced finite model for exact preservation and full information cost.
2. Ordinary coarse graining using the same initial observable partition and conventional clustering or Markov-state method.
3. The proposed retained-state repair, with its actual changes and construction cost identified.

Before comparing distribution scores, freeze one common next-outcome carrier and the same held-out transition pairs. Every model must report probabilities for those same events. In this protocol, use the initial observable partition: every candidate refinement can sum its predicted probabilities back to those fixed blocks. For a microscopic current state x and observed target block B, the unreduced prediction is the sum of P[x,y] over y in B; a refined model sums its quotient row into all refined blocks contained in B. Do not compare negative log likelihoods computed on model-specific partitions. If microscopic next-state scoring is chosen instead, every reduced model needs an explicit development-frozen decoder to that microscopic carrier, with its fit, uncertainty and cost counted.

The primary model-fidelity endpoint is then a declared held-out score on that common outcome carrier, such as average negative log likelihood over the same admitted transition pairs, supplemented by calibration for those same events. A model that collapses two outcomes into a single event would otherwise obtain log loss zero for that easier question; this is not an improvement on the original two-outcome task. The target partition and its scientific meaning remain fixed across candidates. Zero predicted probability for an observed transition incurs infinite log loss unless a development-frozen smoothing rule applies equally to the compared models. Do not add smoothing only after seeing the failure.

For kinetic claims, separately specify the target, lag and finite horizon, then evaluate the stated population or passage observable with uncertainty accounting for trajectory dependence. A sampled passage average from censored or incomplete trajectories is not automatically the population mean first-passage time. Require enough independent transitions for the requested precision; otherwise the outcome is insufficient evidence.

Report state count, matrix storage, base-state retention, preprocessing, refinement, estimation, query work and any added simulation. A smaller quotient with greater total cost is not a measured efficiency gain. A quotient matching a fitted model but failing held-out transitions is not a predictive success. A physical folding claim requires comparison with a matching independently measured physical observable; simulation agreement alone does not supply it.

## 7. Completion and failure records

An executable study remains pending until the source files and reuse terms, exact state assignment, lag, estimator, zero-row policy, split, baselines, horizon, tolerances and uncertainty procedure are fixed. The portable protocol and finite theorem can be reviewed before those empirical inputs exist.

Reject exact preservation on the first unequal aggregate-row pair within an advertised block. Preserve that pair and target block as a concrete counterexample. Reject an approximation claim when its declared residual or held-out error exceeds the frozen bound. Reject added-value claims that vanish under equal inputs, dependence controls or complete cost accounting. Keep all failed strata and null results in the report.

The reproducible output is a source-bound partition, quotient or explicit failure, complete residual rows, split witnesses, evaluation results and scope statement. Any released examples use synthetic states or appropriately reusable scientific data; no personal records are required. Original pack prose and new code may use the repository's broad reuse terms, while linked studies, datasets and implementations retain their own rights.
