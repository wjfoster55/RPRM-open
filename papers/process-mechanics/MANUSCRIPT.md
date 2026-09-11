---
title: The Right Answer Is Not Enough
subtitle: 'RPRM Process Mechanics: What Scientific Descriptions Must Preserve'
author: William J Foster
date: 11 September 2026
version: 0.3
status: Working paper
author-given-names: William J
author-family-names: Foster
doi: 10.5281/zenodo.22709682
url: https://zenodo.org/records/22709682
license: CC0-1.0
pdf-filename: The-Right-Answer-Is-Not-Enough.pdf
lang: en-US
---

## Abstract {.unnumbered}

Scientific descriptions become useful through the work they let us do next: predict a response, combine observations, or reuse a result. A correct answer to one question can nevertheless discard a distinction that the next question requires. This paper develops RPRM Process Mechanics as a human-guided method for finding and testing those distinctions. It connects the choice of a representation to three obligations: preserving continuation, composing evidence about compatible sources, and reusing conclusions under the conditions that support them. Measurement interpretation connects the calculation back to the scientific quantity being requested.

The mathematical core specializes established factorization results, gives conditions for resolving a question from joint records, and distinguishes logical resolution from probabilistic improvement. Development cases show how these distinctions change the appropriate next step. In known-equation circuits, present state can suffice, timed observations can improve estimation or recover hidden current, and an unprovided future input can remain unresolved. Exact interval summaries compose across 76 law-partition comparisons, while a structurally accepted false summary exposes the limits of a correct Boolean answer. A biological-figure reconstruction retains useful partial results while identifying missing calibration and sampling relations. These are worked diagnoses, not a demonstrated comparative advantage. Existing proposals for protein-folding dynamics and BRCA1 cellular function show how the same reasoning could guide harder applications: test which distinctions a reduced description must retain for the desired behavior or measurement. Those molecular comparisons remain unexecuted. The aim is a usable connection between mathematical sufficiency and the scientific choice of what to retain, what to measure, and what to do next.

# 1. A correct answer can hide a broken description

Imagine leaving home, going to a shop, and returning home. A record containing only the starting and ending locations correctly says **home to home**. It tells us where you finished. It cannot tell us whether you went out: staying home would produce the same record. Nothing is wrong with that summary when only the destination matters. The problem begins when we ask it to answer a question about the journey.

Scientific descriptions face the same choice, with more consequential questions. A description adequate for a protein's present shape may be inadequate for predicting a later transition. A voltage reading may omit a current that helps determine how a circuit evolves. A fitted curve may preserve its appearance while losing the units or observation times needed to interpret it. The missing information differs in each case. So does the way to recover it, if recovery is possible.

This paper asks: **what must a description retain for the next scientific question?** The question has a constructive purpose. Changing a representation can make a hidden relation available for calculation. It can also show that a smaller description already contains everything the task needs. The aim is to distinguish those opportunities from cases where an answer depends on information that has not been supplied.

Protein folding makes the motivation concrete. Knowing a structural feature, finding a low-energy conformation, and predicting when a chain reaches a chosen state are different accomplishments. A representation useful for one need not be useful for all three. RPRM's existing folding-dynamics proposal asks how to test a smaller state description against a specified future probability [[1]](#bib-rprm). This paper develops the reasoning behind that question through simpler cases whose laws and evidence can be inspected, then returns to the molecular prospect in Section 8.1.

RPRM, the Relational Pressure Retention Model, approaches these problems through explicit relations, representations, and receiving tasks. Its name comes from the framework's motivating proposal; the present paper develops a mathematical and methodological use of it. A **receiver** is the question or behavior a description is meant to preserve. It may ask for a present value, an event during a time window, a probability under a stated model, or the result of a later action. Naming that use turns a general concern about information loss into something we can test.

The contribution of Process Mechanics is to connect that test to a human-guided scientific workflow. A person or assistant proposes a correspondence, a missing variable, a useful observation, or a cheaper representation. The proposal is expressed as a claim about what a specified operation must preserve. A proof, a separating example, a scoped computation, or an admitted measurement determines how far the claim survives. The result can justify a recovered state, a useful simplification, a better-directed observation, continued ambiguity, or a completed partial result.

The development cases give this workflow distinct jobs. The circuits distinguish an adequate state, a noisy estimate, a recoverable hidden current, and an unknown future input. The interval study shows both how correct pieces can preserve a whole-window question and why an accepted join is not a truth test. The cancer-oriented measurement attempt identifies what a numerical fit still needs before it represents the requested biological quantity. Their different outcomes are the point: they call for different scientific actions, even when each begins with an apparently successful calculation.

This is a companion to *The RPRM Manifesto* [[1]](#bib-rprm). Its elementary preservation laws have established mathematical ancestry and are proved here so the argument can be read independently. The cases informed the method during development; they are not independent prospective confirmations of a new theory. The argument follows a result into its next use: Section 3 asks when a description can answer and continue, Section 4 asks how observations resolve a question, and Section 5 asks what can be composed and reused. Section 6 gives the case results, Section 7 connects them to established practice and a historical discovery, and Section 8 develops their prospective scientific use. The equations provide the conditions; the surrounding argument explains the choices those conditions enable.

# 2. From a promising analogy to a testable obligation

## 2.1 Begin with the task, then choose the description

Begin with four ordinary questions: which situations are allowed, what information is supplied, what is being requested, and which complete possibilities still fit? The vocabulary names these choices as they arise. A **carrier** specifies the allowed objects and their equality. A **port** names a typed role, such as a voltage, a time, an input, or a requested output.

On the integer carrier $D=\{0,1,2,3,4\}$, consider ordinary addition $a+b=c$, without wraparound. Supplying $a=1,b=2$ determines $c=3$. Supplying only $c=3$ leaves the four pairs

$$
(a,b)\in\{(0,3),(1,2),(2,1),(3,0)\}.
$$

Choosing which roles are supplied and which are missing is an **aperture**. The four compatible pairs form the **fiber** for this choice. The sum is determined while the pair is not. Moreover, those pairs must stay joint: replacing them by independent lists of possible $a$ and $b$ would introduce sums other than three. The same issue arises when scientific observations share a source, a control, or a nuisance parameter. Equal displayed numbers do not make two measurements the same occurrence, and separately plausible values need not form a plausible joint state.

For a scientific task, collect the relevant choices in a contract $K$. A contract is not a claim that the model is true. It states what must be true for the calculation to answer the intended question. The most useful components are shown in Table 1.

| Component | What must be made explicit |
|:--|:--|
| Question and source | The typed answer; admitted states, parameters, and models; the source population the result is meant to cover. |
| Time and input | Origin, horizon, sampled or continuous event, endpoint rules, past drives, active controls, and which future inputs are supplied. |
| Observation | Channel, units, acquisition time, event side, calibration, preprocessing, noise or hard error bounds, dependence, and missingness. |
| Identity and operations | Which records belong together; allowed updates, their direction and enabled domains; dependencies required for reuse. |
| Evaluation | Costs of acquiring and using information; comparator inputs; prior exposure to cases; the evidence needed to close the claim. |

: The task contract. Different applications need different fields; the obligation is semantic completeness for the promised use, not a universal form to fill out. {#tbl-contract}

A future input announced before prediction is legitimate available information. An input not supplied remains an alternative unless a specified statistical model assigns it a distribution. These are different prediction tasks even when their observations of the past are identical. Likewise, a threshold on the next hundred sampled voltages differs from a threshold anywhere in the intervening continuous trajectory. The observation and time contract decides which statement a successful calculation supports.

## 2.2 Let the proposal be broad and the test be precise

The human-guided stage has a positive role. It is where someone notices that a familiar description may be hiding the wrong distinction: a voltage without its dynamical partner, a curve without its units, a summary without its interval, or two readings without the relation that joins them. Cross-domain reasoning is useful here when it maps roles and dependencies. Similar mathematical roles can suggest a test without making the physical mechanisms identical.

The resulting proposal should state an alternative and a consequence. For example: if two timed voltages encode a missing current under a known circuit law, then the stated observation map should have a valid inverse at the chosen lag. If endpoints preserve a whole-window range, then a curve with interior extrema should not defeat them. If a recorded past determines a future event, two admissible future inputs with the same past should not yield opposite answers. Each consequence can fail in an informative way.

The workflow is therefore a sequence of scientific choices with explicit outputs:

1. **Frame.** State the receiver, admitted source family, observation process, and relevant continuation.
2. **Propose.** Name the reduction or correspondence, its alternatives, and a result that would distinguish them.
3. **Challenge.** Seek a proof at the claimed domain, a separating witness, or an appropriately scoped empirical comparison.
4. **Refine or retain.** Add a justified distinction, keep an adequate simple description, acquire a permitted observation, or preserve the unresolved alternatives.
5. **Carry or stop.** Return the answer with its support and binding; specify what would invalidate reuse. A partial result can finish the current task.

This procedure does not require history to help, or require every question to be answered. A noiseless state can already be sufficient. An unknown future action can remain unknowable from the past. A missing measurement calibration can prevent a computable slope from becoming the requested scientific quantity. The method is useful only if it allows those outcomes as readily as a successful refinement.

The checks below make parts of this procedure executable. The choice of roles, cases, and representations remains human-guided. The supplied evidence does not show a general algorithm autonomously diagnosing an unfamiliar scientific system.

The first payoff is justified simplification. We need not recover every detail of a source if the distinctions we discard cannot change the answer. The next section makes that test precise, then asks what changes when the description must stand in for the system through further operations.

# 3. Preserve the answer, or preserve the ability to continue

## 3.1 What one answer requires

Can we discard detail and still answer the promised question? Imagine sorting all allowed states by the summary they produce. Inside any one group, the summary cannot tell the states apart. If their answers differ, no decoder using that summary alone can choose correctly for all of them. If their answers agree in every group, that common answer gives a decoder. Proposition 1 makes this test precise.

Fix a contract $K$, an admitted state carrier $X$, and a supplied future plan $\pi$. Let $q_K(x,\pi)\in B$ be the requested answer and let $r:X\to Z$ be a proposed retained description. Here the answer is a total function on the admitted domain; if a task can fail, that failure must have its own explicit tag or the domain must be restricted accordingly. A plan is fixed context in this subsection, not a single update operation.

**Proposition 1. Question factorization.** A decoder $h_\pi:r(X)\to B$ exists with

$$
q_K(x,\pi)=h_\pi(r(x)) \quad (x\in X)
\tag{1}
$$

if and only if

$$
r(x)=r(y)\ \Longrightarrow\ q_K(x,\pi)=q_K(y,\pi)
\quad (x,y\in X).
\tag{2}
$$

The decoder is unique on the reached image $r(X)$.

*Proof.* If the decoder exists, equal descriptions give equal decoded answers. Conversely, for a reached value $z$, define $h_\pi(z)$ to be the answer of any state with $r(x)=z$. Equation (2) makes the answer independent of that choice. Every decoder satisfying (1) must take this value at $z$, which proves uniqueness. The construction also covers an empty $X$, where the reached-image decoder is the unique empty function. $\square$

This is the established quotient-factorization argument, specialized from Manifesto Theorem 1 [[1]](#bib-rprm). No decoder is promised on unreached values of $Z$. Such values have no source meaning under the current representation. If several plans are allowed, the condition must hold for each one; passing for a single plan says nothing by itself about another.

The proposition provides a direct test of a proposed description. Two states with equal descriptions and different answers refute its sufficiency on a domain containing them. Failing to find a counterexample in sampled states does not prove the condition on a larger carrier. Conversely, a many-member source fiber can have one answer. Recovering that answer need not identify the source.

One exact repair is $r'(x)=(r(x),q_K(x,\pi))$. It retains the old description and the missing answer. Any other description that decodes both also decodes their pair, so this is the least informative refinement retaining those two readouts, up to mutual decoding on reached images. It need not be a cheap repair: computing the new coordinate may cost as much as the original problem. Information sufficiency and computational efficiency are separate promises.

In the opening example, one extra distinction—whether the person left home—would repair the journey question without recording every stop. In a scientific model, the useful repair is likewise tied to a question. The circuit case will show a more informative possibility: under a known law, timed observations can supply a missing state coordinate rather than requiring a direct measurement of it.

## 3.2 What later actions require

A description intended to stand in for a system has a harder job than a one-use answer. Suppose we want to keep working from a compact summary without consulting the discarded detail. Two detailed states with the same summary must agree on what we can observe now, which actions are possible, and what summary each action produces. Otherwise, the compact description hides a choice it must make. Agreement on the current answer checks only the first obligation. Agreement on all three lets the compact system continue step by step. These are the three conditions in Proposition 2.

A representation may preserve today's answer and still be unusable after an update. For that stronger task, let $O:X\to B$ be a current observation and let $T_a:X\rightharpoonup X$ be a deterministic partial operation for each action label $a$ in an alphabet $\mathcal A$. The operation is **enabled** exactly on its domain. Inputs, parameters, and clocks that affect the update must either be retained in the state or bound by the fixed contract. We now use $a$ for one action and $w=a_1\cdots a_n$ for a finite action word; $\pi$ remains a supplied plan.

**Proposition 2. Operational factorization.** Exact observations and partial updates descend through $r$ to its reached image if and only if each pair $x,y$ with $r(x)=r(y)$ satisfies all three conditions:

1. $O(x)=O(y)$;
2. for every $a$, $T_a$ is enabled at $x$ exactly when it is enabled at $y$;
3. whenever enabled, $r(T_a(x))=r(T_a(y))$.

In that case there are well-defined maps $\bar O:r(X)\to B$ and $\bar T_a:r(X)\rightharpoonup r(X)$ such that

$$
O=\bar O\circ r,\qquad
r(T_a(x))=\bar T_a(r(x))
\tag{3}
$$

on the enabled domain, with matching definedness. Every finite action word has matching execution success or failure, and successful runs have equal final observations.

*Proof.* Descended observations, domains, and updates cannot depend on which source state represents a summary, giving necessity. For sufficiency, choose any representative of a reached summary and use it to define the observation, enabled actions, and successor summaries. Conditions 1–3 make all these choices independent of the representative.

For continuation, the empty word preserves the encoded state and its observation. Suppose the result holds after a prefix. If the next action is disabled, matching enabledness makes both executions fail. If it is enabled, (3) preserves the encoded successor. Induction proves the statement for every finite word. A failure tag is distinct from every successful observation value. $\square$

This is Manifesto Theorem 2's partial-operation specialization of established congruence and state-refinement reasoning [[1]](#bib-rprm). A simple hostile case shows why enabledness matters: merge two states with the same present observation, but enable an action at only one. The merged description cannot predict even whether the action will run. Matching current answers is insufficient.

For a scientific reduction, these conditions ask whether the smaller state can actually be used as a state: can we tell which next actions are possible, and can we calculate their retained consequences? Section 8.1 illustrates this with two small chain shapes that share a score but allow different geometric extensions. A score can be completely correct while failing that next-use test.

The theorem concerns the declared deterministic operations. Nondeterministic successors and stochastic kernels require their own set or distribution preservation conditions. Approximate agreement also needs a separate error contract: tolerance-based closeness is generally not transitive and cannot simply replace equality in an exact quotient. When the receiver asks for costs, intermediate outputs, or additional path properties, those observations must be included in the promise.

## 3.3 Inference itself has a state

The same problem occurs in a research notebook: knowing that two explanations remain is not always enough to interpret the next reading. We may need to retain which explanations remain. The following small example isolates that difference.

Continuation is not limited to moving physical systems. Updating a set of possible explanations is also an operation. Consider three complete candidates $a,b,c$ with target values $q(a)=q(b)=0$ and $q(c)=1$. Earlier records can leave either

$$
C_1=\{a,c\},\qquad C_2=\{b,c\}.
\tag{4}
$$

Both descriptions have two candidates and the same answer set $\{0,1\}$. Now a sensor reports 0, where its deterministic readings are 0 for $a$, 1 for $b$, and 0 for $c$. The same observation leaves $C_1$ ambiguous but reduces $C_2$ to $\{c\}$, resolving the target to 1.

Thus the present answer set, even together with its size, is not a sufficient state for this evidence update. The complete identities matter, or some smaller description that provably preserves their future observation behavior. This is a constructed finite example from the supplied mathematical note. It adds no experimental evidence. Its role is to connect the operational theorem to the everyday act of carrying an inference forward.

We can now ask which differences between surviving explanations new evidence must settle, and which can remain unresolved without changing the answer.

# 4. Evidence must meet in the same possible source

## 4.1 Resolve the question without pretending to recover everything

What must new evidence settle? Often we need agreement on one answer, rather than a unique account of everything that happened. Several circuit states, for example, could all predict the same threshold event. We can keep the states distinct while reporting that shared answer. The task is to track the explanations compatible with the observations, then ask whether any of them disagree about the question.

Fix a nonempty finite family $\mathcal H_K$ of complete admitted candidates. A candidate $h$ binds the state, parameters, and any unresolved future input or nuisance variables that the model requires. Let $q_K(h)$ be its target answer. Let $U_K(h)$ be the nonempty set of joint records admitted for that candidate under the observation contract. These are sets of possible records; probabilities have not yet been introduced.

For a realized record $e$, define

$$
C_K(e)=\{h\in\mathcal H_K:e\in U_K(h)\},\qquad
A_K(e)=\{q_K(h):h\in C_K(e)\}.
\tag{5}
$$

If $C_K(e)$ is nonempty and $A_K(e)$ is a singleton, the question is resolved within the model. All surviving explanations agree on the requested answer. The conclusion applies to the actual source only if that source is covered by the admitted family and its record obeys the observation contract. Enumeration can establish completeness within a finite catalogue; it cannot establish that the catalogue contains nature's mechanism.

If several answers survive, the receiver remains ambiguous. If no candidate survives, the record is unsupported under this family. That last result is not affirmative evidence that a physical event did not occur. An incomplete search remains open, while malformed input is an admission error. The RPRM labels NONE, ONE, and MANY describe the cardinality of a *complete solved fiber*. They should not be substituted for a partial enumeration or confused with the separate question of how many target answers its members share.

One opposing surviving pair, with different $q_K$ values, is enough to certify ambiguity. Resolving the target requires excluding every such pair while retaining at least one candidate. Appendix A gives the equivalent condition for a fixed observation bundle to resolve every admissible record. This is elementary set reasoning, closely related to established equivalence-class determination [[5]](#bib-golovin); it is not an observation-selection algorithm or a cost guarantee.

## 4.2 Why joint records cannot be replaced by independent lists

Two readings can each fit an explanation while failing to fit it together. The practical question is whether one allowed source can produce the complete observed record. Imagine an underlying binary condition reported through two indicator lights. Under a proposed observation rule, the lights agree for one condition and differ for the other, while an unknown shared setting can switch both readings. Either light alone can be on or off under either condition. Their pair identifies the condition if that observation rule holds.

Write 0 for off and 1 for on. Let the target $q\in\{0,1\}$ name the underlying condition, and let $b\in\{0,1\}$ be the shared nuisance that determines the first light's state. Admit all four complete states $(q,b)$ and specify the observation rule

$$
A=b,\qquad B=q\mathbin{\mathrm{XOR}}b.
\tag{6}
$$

| Target $q$ | Shared bit $b$ | Reading $A$ | Reading $B$ |
|:--:|:--:|:--:|:--:|
| 0 | 0 | 0 | 0 |
| 0 | 1 | 1 | 1 |
| 1 | 0 | 0 | 1 |
| 1 | 1 | 1 | 0 |

: The complete shared-bit carrier. Either channel alone leaves both target values possible; the pair determines their XOR. {#tbl-xor}

For a fixed target, the two joint record sets are

$$
U(q=0)=\{(0,0),(1,1)\},\qquad
U(q=1)=\{(0,1),(1,0)\}.
\tag{7}
$$

They are disjoint. Both targets nevertheless have the same support $\{0,1\}$ on either individual channel. Multiplying those target-level marginals invents all four pairs for both targets and destroys the available distinction. Under the additional uniform probability law on the four states, each reading alone also leaves the target probabilities at one half. The pair determines $q=A\mathbin{\mathrm{XOR}}B$ exactly.

Combining evidence requires a source that can account for the complete record. When admissibility factors over observations *at the complete-candidate level*, filtering by each reading and intersecting survivors is exact. If a nuisance remains outside the candidate, or errors satisfy a joint restriction, independently compatible marginal readings may not be jointly compatible. The general test is membership in $U_K(h)$, not an automatic product of marginal supports.

Three qualifications keep the example precise.

First, at the complete-state level $(q,b)$ the readings are deterministic singleton supports. The non-product relation in (7) appears after the nuisance has been marginalized out.

Second, under the uniform law, $A$ and $B$ are actually independent *without conditioning on the target*. The useful relation is in their target-conditional joint records; an informal assertion that “the readings are correlated” would obscure it.

Third, individual insufficiency does not in general require such a shared nuisance to become joint sufficiency. Different readings can eliminate different opposing pairs. If a target is an ordered pair of bits, reading each coordinate separately leaves the full pair unresolved, while reading both resolves it. Each separate reading then supplies partial information rather than none.

The opposite modeling error is equally revealing. If the actual readings use separate unrestricted bits, $A=b_1$ and $B=q\mathbin{\mathrm{XOR}}b_2$, the shared-bit decoder is wrong on four of the eight complete states. For every observed pair, both target values remain possible. A useful joint model must be justified by the source and observation process; its ability to produce a desired answer does not justify inventing it.

The shared-bit construction is mathematical exposition, not a new scientific experiment. Its scientific lesson is about the observation model: whether the two readings share the same nuisance changes what their pair can establish. In a biological application, pairing records therefore requires justified source identity and timing. A computational join alone cannot establish that two measured quantities describe the same cell or event.

## 4.3 A high probability is a different kind of answer

A probability of 0.6 and a probability of 0.9 both yield “yes” at a decision threshold of one half. They express different forecasts. This is why an unchanged decision need not mean that an observation added nothing: evidence can become more useful without ruling out every opposing explanation. A probability may support a better forecast or a decision under an accepted risk while leaving logical alternatives open. We therefore need to distinguish eliminating an answer from assigning it less weight.

Equation (5) assigns no probability to its candidates. Catalogue size is not a prior. Probability statements require a specified joint law, likelihood and prior, or another statistical construction with an explicit interpretation.

In a finite Bayesian model, positive prior and positive likelihood give positive posterior mass. If an observed finite transcript has positive likelihood under two opposing targets, neither is eliminated by posterior support alone. For example, give targets 0 and 1 equal priors and let a binary reading have probabilities $1/4$ and $3/4$ of returning 1, respectively. With conditionally independent repetitions, four readings of 1 give posterior $81/82$ for target 1; eight give $6561/6562$. These can support a decision with an admitted error risk, but they are not exact source identification.

A hard error bound and a probabilistic noise model therefore make different promises. A confidence or credible interval cannot silently turn a full-support noise distribution into a hard admissibility bound. Conversely, a model-conditional exact answer is not automatically a calibrated probability about the physical world.

There is also a positive reason to keep probability quality separate from hard decisions. For nested information $\mathcal F\subseteq\mathcal G$ and a square-integrable target $Y$, put $m=\mathbb E[Y\mid\mathcal F]$ and $n=\mathbb E[Y\mid\mathcal G]$. Then

$$
\mathbb E[(Y-m)^2]-\mathbb E[(Y-n)^2]
=\mathbb E[(n-m)^2]\geq0.
\tag{8}
$$

The improvement is strict exactly when the conditional expectations differ on a set of positive probability. Appendix A proves the identity and works through an example in which the probability forecasts improve although the decision at threshold one half never changes. For binary $Y$, this is a statement about Bayes-optimal Brier loss under the stipulated law. It gives no promise that arbitrary fitted learners improve when features are added. That distinction will matter when interpreting the circuit nulls.

We now have two ways an observation can help: it can remove incompatible answers, or improve an appropriately evaluated probability. Either result may become an input to a larger calculation. The next obligation is to preserve its meaning when several such inputs are combined.

# 5. Compose correct parts, then decide what can be reused

## 5.1 Time composition keeps the candidate fixed

To summarize a long interval from shorter ones, we first need each piece to describe the same possible trajectory correctly. We can then combine those pieces. Only afterward do we compare alternative trajectories. This order matters when different candidates reach a threshold at different times.

Suppose one complete candidate defines a bounded real-valued signal $s_h(t)$ on a nonempty window $I=(t_0,t_m]$. Partition it into finitely many nonempty children $I_j=(t_{j-1},t_j]$. A range summary stores the infimum, supremum, and whether each is attained. It need not describe every attained value between the bounds: a step signal can take only 10 and 12 while its range bounds are $[10,12]$.

For correct child summaries, the parent lower bound is the minimum of the child infima and the parent upper bound is the maximum of the child suprema. A parent bound is attained exactly when a child attaining that same extreme value says it is attained. The event “reaches at least $\theta$ somewhere” is the OR of the child events for this same candidate. Appendix A gives the complete finite-union argument.

Boundary information can change the answer even when numerical bounds agree. The ranges $[10,11)$ and $(10,11]$ have the same infimum and supremum. Only the second reaches 11. A summary that promises to answer a threshold at its upper bound must retain attainment, or something that determines it.

Candidate alternatives must then be combined in the order required by the question. For guaranteed reach somewhere in the full window, the claim is

$$
\forall h\in C_K(e),\ \exists j:\ s_h\text{ reaches the threshold in }I_j.
\tag{9}
$$

It is generally stronger to require one child interval that works for every candidate:

$$
\exists j,\ \forall h\in C_K(e):\ s_h\text{ reaches the threshold in }I_j.
\tag{10}
$$

In plain language, every possible trajectory may cross the threshold somewhere, even though there is no single time window in which they all cross. Two candidates that reach in different children satisfy (9) but not (10). First compose time within each candidate; then evaluate the receiver across alternatives. Otherwise, a calculation can erase a guaranteed whole-window event or assemble a path from incompatible histories.

## 5.2 Structural compatibility is a premise check

An interval join can check coverage, boundaries, source identity, and matching contracts. Such checks are valuable: they prevent a missing interval, an incompatible catalogue, or a different candidate from silently entering the composition. But they cannot establish that the child values are true merely because those values arrived in a valid format.

The triangle counterexample in Section 6.2 exposes a different failure from an ordinary malformed-input example. The endpoint-only children satisfy the structural join contract and the composer returns `JOIN_OK`. Their contents are false for the promised range receiver. The composition theorem remains valid because it explicitly assumes correct children; the counterexample refutes the stronger inference from accepted structure to semantic truth.

Correctness can be supported by a trusted derivation, an independently checked certificate, or a suitable reference calculation. Which support is needed depends on the task. A hash identifies bytes; it does not prove their assertions, supply missing source data, or establish that the identified program was executed as intended.

## 5.3 Reuse carries a statement and its conditions

After a calculation succeeds, what must accompany it so that someone can use it again? The answer alone may omit the very condition that made it valid. A result about one input plan, for example, does not automatically answer the same question under another plan.

A cached result is a conclusion under a binding. Reuse is justified when the dependencies needed for that conclusion still hold: the question, model, parameters, input plan, source version, interval, units, and any other material assumptions. A certificate should identify the statement it supports and the conditions whose change requires reopening it.

Invalidation is not logical negation. A range certificate computed for yesterday's input may cease to justify today's range without proving that the old range statement was false. Similarly, an opposing pair certifies ambiguity while both members survive. If one member is eliminated, that witness expires; another opposing pair may remain. A replacement search or a complete answer-class check is required before declaring resolution.

Dependency-aware reuse has substantial prior work in self-adjusting computation [[4]](#bib-acar). Process Mechanics uses the same basic obligation in a broader scientific setting, where dependencies can include measurement interpretation and candidate identity. The supplied interval repair has a producer-reported 24/24 audit. That historical receipt is preserved at its reported grade; the current companion checks do not constitute an independent replay of that repaired historical implementation.

# 6. Three cases, different useful outcomes

The cases put the same scientific question through three different demands: a forecast that must continue, a summary that must compose, and a number that must retain its measurement meaning. We want to know what changes in the next calculation or observation when the missing distinction is made explicit.

The development evidence asks whether these obligations distinguish situations that would otherwise be described too loosely as “more information helps.” It consists of known-equation circuit simulations, exact interval fixtures, and a synthetic calibration followed by a partial biological-figure reconstruction. The cases have already informed the method. They are not untouched prospective tests.

## 6.1 Circuits: four reasons a history may or may not help

A voltage reading describes one aspect of a circuit's present condition. The prediction asks what happens later. In the RLC model, current is another state coordinate needed to continue the evolution; under the known dynamics, its effect can be recovered from appropriately timed voltage readings. This gives the missing-information question a physical meaning before the numerical comparisons begin.

A record of past voltages can serve several different purposes. It might help estimate a noisy present value, reveal a hidden current through known dynamics, or add nothing because the state is already sufficient. It cannot choose a future input that the task leaves unspecified. The four cases below distinguish those possibilities before asking whether the resulting event predictions improve.

The circuit receiver is specific: at an eligible origin, does any of the next $H$ sampled **true capacitor voltages** fall to or below $0.5\,\mathrm V$? Eligibility requires the current measured voltage to exceed that threshold and the declared past and future windows to be available. Labels refer to the native simulation grid, rather than a continuous-time crossing between samples. The complete domain return [[9]](#bib-pc1) supplies the model and information contract; saved rows support the arithmetic summarized here.

The RC case uses $R=1{,}000\,\Omega$, $C=1\,\mu\mathrm F$, and time constant $RC=1\,\mathrm{ms}$. Samples are spaced by $20\,\mu\mathrm s$ and the horizon is 100 samples, or $2\,\mathrm{ms}$. The input is held at 1 V through 4 ms and then either remains at 1 V or switches to 0 V. Known-plan predictors receive the announced future choice. In the noisy case, Gaussian voltage measurement noise has standard deviation $0.05\,\mathrm V$; the model adds no process noise.

**Already sufficient state.** In the noiseless known-plan RC panel, the equation-based state prediction agrees with every one of the 220 sampled event labels. All four learned representations also tie in their Brier score. In this deterministic model, present state and the supplied input plan already support continuation. Extra history is not required for the declared event. This is a substantive sufficient-state null, not a failure of the framework to find a benefit.

**Noisy observation.** Several recent readings need not describe the same state. If voltage is changing, averaging them can blur that change while reducing noise. A model-aware estimate accounts for the evolution before using the readings to estimate the present. In the noisy RC panel, this correction improves present-voltage estimation. Table 3 reports the mean squared errors reaggregated from 660 saved observer rows.

| Present-voltage estimate | Mean squared error $(\mathrm V^2)$ |
|:--|--:|
| Current noisy reading | $2.85715\times10^{-3}$ |
| Mean of 49 past readings | $3.77142\times10^{-3}$ |
| Model-aware least squares, 50 readings | $1.35335\times10^{-5}$ |

: Noisy-RC state estimation. The least-squares calculation uses 49 past readings plus the current reading and detailed past-drive timing. The plain past mean averages a changing state without that correction. These are development errors from saved rows, not a confidence interval or an identical-input ranking against the learned feature methods. {#tbl-mse}

The plain mean is worse than the current reading here because averaging a changing quantity can mix different states. Least squares accounts for the supplied dynamics. Yet the learned methods already make every evaluated binary event decision correctly, and their RC event probability scores tie. Better voltage estimation and additional correct event decisions are distinct results. The least-squares event output is itself a hard mean-state plug-in decision; no event-probability calibration follows merely from its improved state MSE.

The information comparison also has a material boundary. The learned window uses 51 readings and a compressed input representation, whereas least squares uses 50 readings, absolute window times, and detailed past-drive timing. After a switch, the learned plan fields lose elapsed-since-switch information that the equation-aware estimator receives. The result supports the value of modeling the known evolution for this estimation task. It does not isolate an algorithm advantage under exactly matched inputs.

**Recoverable hidden state.** The RLC case uses $R=200\,\Omega$, $L=1\,\mathrm{mH}$, and $C=1\,\mu\mathrm F$. It is overdamped. Samples are spaced by $0.5\,\mu\mathrm s$, with a 199-sample horizon of $99.5\,\mu\mathrm s$. Current is hidden from voltage-only predictors; the drive is known and constant within an episode. Two voltage readings separated by the tested $2.5\,\mu\mathrm s$ lag permit an ordinary affine reconstruction of the current. Across 2,391 saved origins, the maximum absolute current error is $1.3173\times10^{-16}\,\mathrm A$, and the observer has zero event disagreements.

Appendix B shows what the inverse requires: the coefficient linking earlier current to later voltage must be nonzero. At zero lag it vanishes, and near singularity the inverse can amplify noise. The recorded numerical accuracy concerns noiseless readings, known parameters, constant drive, and the tested lag. It is a scoped reconstruction result, not a claim of sensor-noise robustness or an RPRM-exclusive estimator.

**An input the past cannot supply.** The withheld-plan control keeps the past fixed and admits two future actions. Sixty paired origins yield 24 pairs with opposite event outcomes. For those pairs, no function of the identical past can know which unprovided branch is taken. Under the control's explicit equal prior, the best event probability is one half and its squared loss is one quarter on either realized branch.

There are 48 ambiguous branch rows among 120, so the unclipped aggregate Brier loss is

$$
\frac{48(1/4)+72(0)}{120}=0.10.
\tag{11}
$$

On the ambiguous subset alone it is 0.25. Clipping predictions to $[10^{-6},1-10^{-6}]$ changes the aggregate to approximately $0.1000000000006$, because the 72 agreeing rows acquire a negligible squared loss. This is uncertainty over an unprovided input in a stipulated model, not evidence that the state estimator failed.

**The hard-decision null.** The saved learner export contains 15,475 prediction rows across 13 panel/view combinations. Recomputing decisions at probability threshold 0.5 gives zero errors in every combination. The RLC learned Brier scores vary slightly across views; the RC scores tie within each panel. Neither fact should be rewritten as extra correct classifications. Appendix B reports the separate probability scores so the null does not erase what was actually measured.

These rows are not independent experiments. The development panel contains eight RC configurations, 24 noisy records based on those same configurations, and 32 RLC configurations. Origins overlap in time and the views reuse sources. Some noisy records reuse random vectors across release-plan sources: the 24 development records use 16 distinct seeds. The source return reports disjoint training and development initial-state lists and no train/development seed overlap, but the present editorial reaggregation does not regenerate or reauthenticate those trajectories.

The four outcomes identify different tasks: retain an already sufficient state; estimate a noisy state using known dynamics; recover a missing state coordinate under an invertible observation map; or retain an unresolved input branch. The diagnosis changes the next action. Keep the sufficient state; improve the estimate when the observation is noisy; recover the hidden coordinate when the observation map permits it; or supply a future-input assumption and retain the alternatives it leaves. Treating all four as a generic demand for more history would miss these different remedies. The useful result is knowing which kind of missing information we face.

## 6.2 Intervals: the positive theorem and its trust boundary

A scientific calculation often needs a whole time window while its records or computations arrive in pieces. The opportunity is to retain a compact summary of each piece and combine them without losing the requested range or event. This case asks two separate questions: do correct local summaries compose correctly, and does accepting a join establish that its inputs were correct? The first has a positive answer under the stated contract. The triangle below supplies the boundary to the second.

The interval study uses 19 precisely defined signal patterns: a constant, a ramp, nine triangle phases, and eight step times. Each law is known in full. The primary receiver asks for whole-window range bounds, attainment, and reach at least $11.5$ on $(4,8]$. Four partition arrangements use two, four, or eight equal children, or the mixed children $(4,5]$, $(5,6]$, and $(6,8]$.

For all 19 laws and all four arrangements, correct child summaries agree with direct exact evaluation. This gives $19\times4=76$ deterministic comparisons [[10]](#bib-water). The current supplied companion replay also reproduces these 76 comparisons. Nested compositions reuse the same laws; they do not create additional physical systems or independent confirmations. The reference is ordinary direct interval evaluation with the same law information, so agreement establishes preservation rather than superiority over that reference.

The accompanying triangle counterexample makes the distinction exact. The signal takes the values 10, 11, 10, 9, and 10 at successive times 4, 5, 6, 7, and 8, with straight segments between them. Looking only at the ends of each child window loses the rise and fall inside it. Endpoint-only children on $(4,6]$ and $(6,8]$ both claim $[10,10]$; the actual range is $[9,11]$. Their metadata match, so the structural join accepts those false contents.

The primary question asks whether the signal ever reaches 11.5. Because 11.5 is above the actual peak, the exact law answers no. The false constant-at-10 description also answers no. That agreement does not expose the range error. Ask the auxiliary question “Does it reach 11?” and the answers separate: the exact signal reaches 11, while the false summary says it does not. Figure 1 shows both the hidden variation and the two thresholds.

![An existing exact triangle fixture on $(4,8]$. The solid trace has values 10, 11, 10, 9, 10 at times 4, 5, 6, 7, 8 and is linear between them. Endpoint-only summaries of $(4,6]$ and $(6,8]$ report $[10,10]$; their structural join accepts those contents. The exact range is $[9,11]$. Both descriptions answer no at the primary threshold 11.5; only the exact one answers yes at the auxiliary threshold 11. This redraws a supplied mathematical fixture, not measured data.](figures/triangle.pdf){#fig-triangle width=100%}

If the only promised task is the frozen 11.5 test on this fixture, both descriptions give its correct Boolean value. That success does not validate the range, another threshold, or a later use of the summary. The example contains no measurement noise or difficult numerical approximation: the error is the loss of interior extrema. The reach-11 question is explicitly auxiliary. It would be incorrect to report a primary-threshold error, or to say that the joiner detected the false child contents.

The two results work together. The positive theorem says what a compact description must retain to make exact composition possible. The counterexample shows why checking the composition's structure cannot replace checking that retained content. This is a useful distinction for any later calculation that consumes a summary: an accepted interface and one correct answer are not a certificate for every question about the underlying signal. The recorded result concerns exact stipulated signals.

The historical cache-context repair has a producer audit reporting 24/24. Its preserved source identity and reported status remain part of the evidence. The supplied public adapter implements selected context and invalidation checks, but executing that adapter is not an independent behavioral replay of the original repaired cache. No cache speedup or lifecycle performance advantage is claimed here.

The interval case could compare its summaries with a law supplied in full. A measurement-derived number introduces a further question: what relation connects that number to the physical quantity we mean to study?

## 6.3 Measurement: a number can be computable before its meaning is established

The motivating biological question concerns how cells differ in their response and timing after DNA damage. The source study follows polo-like kinase-1 activity and G2 checkpoint behavior [[8]](#bib-liang). To use a reconstructed curve in that setting, we need more than its shape: a slope must refer to the intended activity scale and time interval, and a claim about a cell's changing behavior must preserve which observations belong to that cell.

Here the difficult step is establishing what a number measures. A curve can yield a finite slope even when the conversion from pixels to scientific units is missing. The case distinguishes success at the numerical calculation from success at recovering the requested measurement.

The cancer-oriented case begins with an easy synthetic calibration. Six admitted candidates are distinguished by a measurement named $D$. All 18 nominal source/policy cases choose that same measurement and resolve after one read; the historical calibration replay reports 60 passing tests [[11]](#bib-cancer). Here $D$ is a field in the synthetic fixture, not a newly validated clinical test. The null is useful: the task does not require an elaborate observation policy, and it demonstrates no RPRM-specific policy advantage.

A separate, nonblind reconstruction attempted to recover four group-mean curves from the published figure context in Liang et al. [[8]](#bib-liang). Their study concerns polo-like kinase-1 activity and G2 checkpoint timing. Its Figure 3d and methods supply a specific quantitative context; matching the appearance of a curve is not sufficient to reproduce the publication's estimator.

The reconstruction produced finite pixel-space fits, but the main plot's vertical conversion into publication units was not established. A scale shown elsewhere in a figure cannot be transferred without a justified calibration. Nor was excluding the last raster sample shown equivalent to excluding the study's last original observation. Two requested terminal windows also remained incomplete. Table 4 records the resulting distinctions.

| Published group | Retained measurement status |
|:--|:--|
| Damaged + caffeine | The terminal tip was not recovered. An earlier continuous proxy window can support a pixel-space fit, but not the requested terminal estimator. |
| Asynchronous | Terminal coverage remained incomplete. The available fitted window did not establish the requested three-hour coverage. |
| Synchronized | Coverage met the reconstruction's raster rules; vertical calibration and original-sample equivalence remained unresolved. |
| Damaged | Coverage met the same raster rules, with the same calibration and sample-equivalence limits. |

: Four distinct curve outcomes within one partial reconstruction. The status is relative to the published measurement target. Neither a valid numerical fit nor adequate raster coverage supplies the missing unit conversion or source-sample identity. {#tbl-measurement}

This result is **partial reconstruction**. It preserves what the attempt obtained without promoting its slopes into the publication's units or treating the curves as linked individual-cell measurements. No linked acquisition-clock single-cell analysis was performed. Publisher images are not reproduced here, and the current review does not independently redigitize them.

The case exposes a failure that a pure numerical check may never detect. Least squares can correctly fit extracted pixels while the fit still fails to represent the requested biological quantity. More interpolation or another successful numerical run cannot by itself restore a missing calibration, a terminal observation, or an identity linking measurements to the same cell. The unfinished measurement bridge limits a biological inference; it does not refute that inference or establish a negative result about malignancy.

The constructive outcome is a more exact account of the next evidence needed. Original numerical observations or a justified calibration could support a quantity in the publication's units; adequate terminal samples could support the requested window. The four retained outcomes distinguish the reconstruction obligations still open; an individual-cell analysis would require the additional linkage between observations. They keep the completed fitting work usable while preventing it from silently becoming a different biological claim.

## 6.4 What changes in the next scientific step

The cases return us to one question: what must this description retain for its next scientific use? They provide more than a warning about information loss. They distinguish choices that would otherwise be easy to confuse.

**Use known relations to recover or estimate state.** In the RLC model, current is absent from the voltage channel but recoverable through the relation between timed readings. In the noisy RC model, accounting for that time evolution improves an estimate of an existing coordinate. These are different uses of history. The useful connection is that a representation can expose information already implicit in supplied observations and laws.

**Make simplification earn its next use.** The noiseless RC state and known input are already sufficient. The interval theorem likewise identifies content that can be combined exactly without retaining the full signal as the working summary. The triangle shows where that permission ends: the coarse endpoint description happens to answer the frozen Boolean correctly while losing the range. The response is to retain the distinction needed by the intended use, not to abandon all simplification.

**Turn unresolved inference into a specific scientific question.** The withheld-input control identifies a future choice that the past cannot supply. The biological reconstruction identifies calibration, sampling, and source-linkage obligations that another fit cannot fill. These outcomes tell us what kind of additional evidence would matter, or which alternatives must remain in the answer. They do not make the unresolved part disappear.

This is the proposed connection between the paper's mathematics and scientific practice. A failed forecast, an inadequate summary, and an uninterpretable measurement need different repairs. Expressing their relations explicitly can make that difference visible before we choose a larger model, a longer record, or another calculation. The supplied cases establish these worked diagnoses at their stated scopes. Whether the integrated workflow improves discovery, prediction, or cost over competent existing practice remains to be tested.

The prospective molecular questions now have a specific form. Which distinctions between represented states change a chosen future probability? Which molecular and measurement context is needed for a cellular assay score? These questions connect the worked cases to established scientific practice and to the molecular applications developed in Section 8.

# 7. The method's place among established approaches

Process Mechanics sits at an intersection of established mathematical and scientific practices. The proposed contribution is to connect these established conditions across the successive uses of a scientific result. Its value should be evaluated against the practices that already address those problems.

**Abstraction and refinement.** Abstract interpretation gives a framework for relating concrete computations to abstract descriptions, including sound approximations that need not decide every property [[2]](#bib-cousot). Counterexample-guided abstraction refinement uses spurious abstract behaviors to drive refinement [[3]](#bib-clarke). The distinction from the exact factorization in Section 3 matters: a sound overapproximation can be useful without giving an exact decoder for every requested output. The present human-guided proposal stage does not replace automated refinement. It extends the surrounding task specification to observations, physical inputs, measurement interpretation, and the evidence supporting those choices.

**State estimation.** Kalman's state-transition formulation of filtering and prediction relates noisy observations to a dynamical state and its estimation error [[6]](#bib-kalman). The present RC least-squares calculation and RLC affine reconstruction are ordinary equation-aware methods; they are not claimed as Kalman filters or new optimal estimators. Their methodological role is to distinguish an uncertain reading, an omitted but recoverable coordinate, and an unprovided future input. Those conditions require different responses even when all appear as uncertainty in a forecast.

**Determining an answer class.** Equivalence-class determination is particularly close prior work [[5]](#bib-golovin). It partitions hypotheses by the answer class that must be identified, allowing irrelevant latent detail to remain unresolved. The EC$^2$ criterion cuts prior-weighted edges between opposing classes and supports expected-cost guarantees under the authors' specified assumptions. Their noisy-test construction includes latent noise and correlated test outcomes; it does not require conditional independence as a universal premise. When hypotheses cannot be fully identified, they also formulate classes by the decisions that complete observations would support. Process Mechanics does not implement EC$^2$ or inherit its approximation guarantees. The overlap directly limits any priority claim for target-relative resolution or opposing-pair reasoning.

**Dependency-aware reuse.** Self-adjusting computation combines memoization with change propagation and proves consistency and correctness for a specified programming-language semantics [[4]](#bib-acar). Its theorems illustrate the rigor a reuse guarantee requires. A scientific cache must separately establish its own bindings and validity conditions; a paper citation cannot make those premises true for it.

**Discriminating measurement.** Meselson and Stahl's DNA-replication experiment makes the relation between a question and an observation particularly clear [[7]](#bib-meselson). The issue was how parental material was distributed among daughter molecules. Labeling that material with heavy nitrogen, then allowing replication in a light-nitrogen medium, turned competing accounts into different predictions about DNA density. After one generation the DNA occupied an intermediate band; after two, intermediate and light bands were observed. Following the distribution across generations supplied a distinction that a single overall amount of DNA would not retain.

The methodological lesson is a change in what is observed: preserve the parental-material relation and the generational sequence that make the alternatives distinguishable. The experiment earned conclusions from those observations. It does not show that RPRM would have produced the discovery earlier, nor does it provide new evidence for the present biological reconstruction. It gives an established example of the scientific act that the framework seeks to make explicit: choose a representation and observation whose outcomes can separate the explanations that matter.

Taken together, these predecessors show that the underlying problems are real and well studied. The proposed integration is a common working language for moving from a suggested relation to a preservation obligation, then carrying the result into a further scientific use. It makes state, input, observation, joint-source, and reuse conditions visible in one argument. Its usefulness as a method still needs comparison against ordinary practice; that open question should be tested at the level of the workflow rather than answered by the familiarity of its components.

# 8. From worked diagnoses to harder scientific questions

The value sought in a difficult application is a change in what can be asked, inferred, or computed with justified meaning. A new coordinate can expose a distinction that an old description merged; a proved reduction can show that the distinction is unnecessary for the chosen task. The following applications already appear in the Manifesto and its public research specifications [[1]](#bib-rprm). They are prospective uses of the method, not additional completed case studies.

## 8.1 Protein folding: a correct score is not yet a continuing model

Protein modeling asks several questions that a single answer can obscure. Which conformations fit the constraints? Which minimize a supplied energy? What transitions are possible, with what probabilities and on what time scale? The last questions require a law of motion or transition in addition to a set of shapes and scores. A useful abstraction must be chosen for the particular behavior we intend to predict.

An existing finite example makes this distinction visible before introducing molecular dynamics. The Manifesto's companion uses an explicitly bounded hydrophobic/polar lattice model in the established HP tradition [[1]](#bib-rprm), [[15]](#bib-lau-dill). A chain is an ordered path on a square grid; its score is minus the number of non-backbone H–H contacts. Consider two three-bead chains whose beads are all P. Both have score zero; the two geometries below also have empty non-backbone contact maps. One chain is straight and one bends upward. Append a bead one step west from the end: the straight chain would collide with its middle bead, while the bent chain has a free site. Figure 2 shows the supplied witness.

![The same score can hide a different available next action. Both supplied three-P chains have an empty non-backbone contact map and score zero. A westward extension from the straight chain's endpoint collides with an occupied site; the same named extension from the bent chain reaches an empty site. Coordinates, chain order, and ambient directions are retained by this toy's contract. This redraws an existing finite geometric witness; appending a bead is not a simulation of molecular folding kinetics.](figures/chain-continuation.pdf){#fig-chain width=100%}

The contact description has done its scoring job correctly. It has nevertheless discarded geometry that the extension question needs. Retaining the full path repairs this particular receiver in the toy; a smaller adequate repair would require its own argument. This is Proposition 2's enabledness condition made concrete. It explains why a correct optimization score is not, by itself, a description that can be continued through every operation we care about.

The proposed folding-dynamics application asks the corresponding question for probabilities. Supply a finite Markov model of molecular states, its transition probabilities at a stated time lag, and a grouping of states into retained descriptions. The grouping must retain the observable being predicted; for a target-reaching question, no group may mix target and non-target states. For an exact reduced Markov model valid for every starting distribution, states placed in one group must give the same total probability of entering every retained group at the next step. This is the conventional strong-lumpability condition, treated in the Manifesto's stochastic argument and in established work [[1]](#bib-rprm), [[16]](#bib-geiger-temmel). A common present label then carries one well-defined next distribution. If the probabilities disagree, the label hides a distinction relevant to continuation.

This turns the search for a useful molecular representation into an inspectable question. A structural grouping may need to split states that take different future routes, retain a justified history variable, or accept an explicitly bounded approximation. In the Manifesto's supplied four-state control, two models have the same equilibrium group occupancies but different transition behavior. Matching how often a group is occupied can therefore miss how it is entered and left. Those states are synthetic; their role is to identify a test a molecular model would have to pass.

Voelz and colleagues' NTL9 study provides the existing proposal's scientific source lead: it combines folding trajectories with Markov-state analysis [[13]](#bib-voelz). The RPRM proposal would evaluate candidate reductions on a fixed future event and common time scale, preserving trajectory ancestry and comparing with ordinary coarse-graining methods given the same inputs. Exact preservation of a supplied matrix, agreement on held-out simulated transitions, and agreement with a physical kinetic measurement would answer three different questions. No trajectory acquisition or molecular comparison has been performed for this proposal.

The possible payoff is a smaller description that remains useful for the behavior we ask of it, or a concrete reason why that reduction fails. A separating pair can identify what the description must distinguish instead of treating every mismatch as a generic demand for greater model complexity. That is a research opportunity supported by an explicit mathematical test; a useful molecular reduction and any performance advantage remain to be earned.

## 8.2 Biological function: retain the context that makes the question answerable

The measurement case points toward another existing proposal: a representation adequate for a protein-level description may merge nucleotide changes that matter to a cellular assay. The BRCA1 specification asks which supplied sequence and context features are needed for a declared cellular-function score [[1]](#bib-rprm). It is distinct from the PLK1 reconstruction in Section 6.3; the connection is an inference obligation, not a shared established mechanism.

Findlay and colleagues' saturation-genome-editing study supplies the proposal's source lead, with separate cellular-function and RNA-abundance readouts [[14]](#bib-findlay). The prospective question is whether a coarser representation merges records with different task-relevant effects, and whether adding justified context produces useful prediction on unseen records. The source measurement and its construction must stay explicit: a cellular-function score, an RNA measurement, and a thermodynamic stability estimate are different quantities. Additional measured RNA would define a different input task from predicting function from sequence alone.

In this application, a richer description might retain nucleotide identity or splice context that a coarser protein-level grouping omits. A new coordinate matters when it distinguishes scientifically different possibilities that the old description treated as identical. The useful question is whether that distinction supports prediction on new records under the same input and measurement contract. More coordinates can also identify training records without helping a new case, so the added context must be judged against the requested score, uncertainty, and a fair conventional comparison. The BRCA1 comparison remains unexecuted and makes no treatment or individual-risk claim.

Taken together, the folding and assay directions explain why the present diagnoses matter beyond their small fixtures. They offer a way to formulate an otherwise vague suspicion—something important has disappeared from the description—as a candidate distinction, a predicted consequence, and an observation or calculation that could test it.

## 8.3 Separate information, algorithms, and implementation

Three different improvements can be confused. An **information improvement** supplies a new channel, a timed relation, or an input that was previously unavailable. An **algorithm improvement** uses the same available information more effectively. An **implementation improvement** preserves the same output semantics while reducing computational work. They require different comparisons.

The circuit least-squares contrast illustrates why the distinction is practical. Known future plans are aligned, but the past-drive and observation packages differ. The interval comparisons establish exact preservation, but the law is supplied and no sensing cost is measured. A compact output may require expensive setup, retrieval, or verification. Storage size, acquisition cost, feature-computation time, and total lifecycle cost should therefore be measured separately rather than compressed into one efficiency claim.

A prospective comparison would need the procedure, permitted adapter changes, source population, independent unit, comparator information, outcomes, exclusions, costs, and stopping rule fixed before new outcomes are inspected. The cases in this paper do not provide that comparison. An informative endpoint could be agreement with a competent baseline, correct retention of ambiguity, or a completed partial measurement. Unlimited post-result refinement would make those outcomes disappear and undermine the proposed evaluation.

## 8.4 Match the evidence to the statement

The mathematical propositions are written arguments under stated assumptions. The supplied finite suites check implementations and examples. Circuit saved-row reaggregation recomputes reported arithmetic; it does not regenerate trajectories or refit learners. Historical source reports support narrower statements where the complete implementation or measurement inputs are absent. Appendix C maps the ten retained claim labels to those evidence grades.

The original editorial review reaggregated the 15,475 learner rows, 3,271 observer rows, and 60 withheld-plan pairs with a separately written arithmetic checker, and replayed the supplied mathematical example suite. For this working-paper candidate, the existing public companion checks and public saved-row arithmetic were run from the assembled public files, including the optional NumPy/SciPy circuit path. Appendix C distinguishes the public reproduction route from those earlier reviewer-local checks. These executions verify supplied records and finite examples; they add no experiments or independent scientific units. No formal proof assistant was run for either pass.

The strongest boundaries are concrete. The circuit evidence concerns synthetic known models and an easy sampled event; it is not hardware or noisy-RLC validation. The interval evidence assumes supplied laws and correct children. The measurement reconstruction does not establish publication-unit slopes or linked single-cell dynamics. No result here establishes a cancer mechanism or treatment, molecular folding kinetics, a new physical law, autonomous discovery, or universal computational advantage.

## 8.5 Conclusion: a description should leave us able to continue

The opening record, “home to home,” was useful for a destination question and inadequate for a journey question. The scientific cases give that simple distinction different consequences. A known circuit law can make a hidden current recoverable from timed voltage readings. A sufficient state can make additional history unnecessary. A correct range summary can carry a whole-window question through composition. A numerically successful curve fit can still leave a specific measurement relation to be established.

The common result is a way to decide what kind of work comes next. Recover a missing coordinate when the observations and law permit it. Keep a smaller state when it preserves the promised behavior. Preserve an unresolved input when the past does not determine it. Seek calibration or source linkage when the quantity being inferred requires it. The mathematical obligations matter because these are different scientific decisions, not interchangeable requests for more data or a more elaborate model.

Protein folding gives the forward question a clear form: can a reduced description retain the future behavior we want to predict while leaving irrelevant microscopic distinctions behind? The cellular-function proposal asks the analogous question about molecular and measurement context. The present paper does not settle those applications, but it makes their central test concrete. If a description merges states or records that require different answers, the failure points to a distinction to investigate. If the required answers and continuations survive, simplification has a reason to be trusted.

RPRM Process Mechanics proposes to connect scientific imagination to that discipline. A suggested relation becomes a stated preservation claim; a proof, observation, or counterexample determines what can be carried forward. The ambition is to make difficult problems more tractable by discovering which distinctions actually matter. Its practical purpose is an inference we can now make, an observation with a clear reason to make it, or a simpler model we have reason to use. A useful scientific description preserves what that next step requires.
