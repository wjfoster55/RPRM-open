# Assessment B: scored mathematical response

## 1. Degenerate interpolation aperture

The admitted carrier is real-valued ports with the given exact equation; only `R` is missing. At `L=3,u=0`, the equation reduces to `x=3`, independently of `R`.

- With `x=3`, the complete fiber is `MANY({R=t : t in R})`: every real `R` satisfies the equation, and every admitted completion is real.
- With `x=4`, the complete fiber is `NONE`, because the equation would require `4=3`.

Rearranging to `R=(x-(1-u)L)/u` is valid only when `u` is nonzero. Dividing by zero here would discard the exact branch that determines whether there are infinitely many completions or none. No carrier enlargement is needed for either answer.

## 2. Abstract singleton versus two source witnesses

The complete source fiber is `{a,b}` with distinct witnesses; its exact image under `beta` is the complete abstract fiber `{z}`. Existence transfers in both directions: a source witness has an abstract image, and each abstract witness has a source preimage by the stated image equality. The abstract completion is unique, but the source completion is not: its disposition is `MANY({a,b})`.

Source uniqueness would imply abstract uniqueness under this exact-image condition, but the converse fails here. Likewise, `z` alone cannot identify which original witness was used. Returning the complete preimage `{a,b}` preserves the ambiguity; choosing one representative does not reconstruct an arbitrary original source witness.

Injectivity of `beta` on the relevant source fiber, together with the existing image equality, would make the restricted map a bijection and transfer uniqueness and exact reconstruction. That property is incompatible with the supplied collision, so achieving it would require a changed representation, such as an additional witness tag. Global injectivity outside the relevant fiber is unnecessary for this particular aperture.

## 3. Typed equality

The receiver's value carrier and equality must be implemented faithfully. For example, represent these outputs in a tagged union as `Bool(true)` and `Int(1)`; they are distinct even if an implementation's untyped numeric comparison identifies them. A checker that uses that comparison can incorrectly certify preservation.

For a proposed summary `C`, a faithful quotient requires `C(x)=C(y)` to imply `Q(x)=Q(y)` under the receiver's declared typed equality, with an exact decoder `Q=h composed with C` on reached summaries. Therefore a summary merging these two states must be refined, for example to `(C,Q)`. If the summary already separates them, its partition may be adequate, but the comparison and decoder still need to respect the types. The question does not supply an actual summary, so an existing source-state merge cannot itself be inferred.

## 4. Empty surviving hypothesis set

No particular readout about an actual source is established by vacuous agreement. Taking the stated emptiness to be a complete result, the compatible-hypothesis fiber has disposition `NONE`. The actual-source readout remains unsupported, or `OPEN` as an outstanding question; it is not a determined value.

The next obligation is to check the observations and inference and establish a consistent admitted model that covers the actual source. Contradictory observations, an inadequate admitted hypothesis class, or an implementation error are possibilities to investigate, not conclusions already proved. Malformed input would be an admission error if demonstrated. If emptiness were only the result of an unfinished search, even the empty-fiber claim would instead remain `OPEN`.

## 5. Future distinction and stable refinement

Read words left to right as execution order. A shortest distinguishing word is `ab`:

`x --a--> r --b--> t`, with final observation `1`, while
`y --a--> s --b--> s`, with final observation `0`.

The empty word gives observation `0` at both states. A one-letter `a` gives `r,s`, both observed as `0`; a one-letter `b`, or any other action, leaves `x,y` unchanged. Thus no word of length less than two distinguishes their observation behavior. All operations are total here, so failure tags do not affect this witness.

Present-only preservation allows the merge because `O(x)=O(y)`. Repair for the single present question, `(C,O)`, also keeps this pair together. Repair specifically for the question “what is observed after `ab`?” separates this pair, but satisfying one question alone does not prove that the repaired summary supports every operation and future question.

Full stable refinement requires equal enabledness and successor summary classes for every action within every remaining fiber. If the stated initial summary gives `r` and `s` distinct values, the merge of `x,y` already violates this condition on action `a`, despite equal observations after that one action. If `r,s` initially share a value, the refinement first separates them using action `b` and the different observations at `t,s`, and then separates `x,y` using action `a`. The observational distinguishing word remains `ab` in either reading. Retaining a summary that separates each of `r,s,t` from `x,y` prevents the otherwise observationally equivalent states `y,s` from merging.

## 6. Sets, multiplicities, and probabilities

Assuming `A,B` denote the relevant successor classes, both successor sets are `{A,B}`. With equal current observations, they may merge for this particular step under set-valued semantics. A full quotient still has to pass the other declared operations and receiver obligations.

Under multiplicity semantics the multisets differ: the first has two occurrences of `A`, and the second has one. A receiver preserving those counts forbids this merge.

A list alone does not specify probabilities. If each list entry is equally likely, the first transition assigns masses `(2/3,1/3)` to `(A,B)` and the second assigns `(1/2,1/2)`, so they cannot merge under that stochastic receiver. Other explicitly supplied weighting rules could yield equal masses. The required check is equality of total probability into each summary class; absent a weighting rule, the stochastic verdict remains `OPEN`.

## 7. Two versus two under an at-most-one-error guarantee

There is no lawful completion. If the common proposition is `0`, both `1` reports are wrong; if it is `1`, both `0` reports are wrong. Each possible truth value requires two errors, exceeding the guarantee. These two cases exhaust the binary truth carrier, proving `NONE` for the observed row under the stated model.

Neither a truth value nor individual liar identities follow. The observation and the complete set of premises cannot all hold together; the next investigation must locate the failed premise, observation, or model bridge without silently relaxing the error bound. There is no majority to select.

## 8. Endpoint and step-count receivers

An endpoint compiler is correct for a receiver asking only for the final partial function and its failure disposition: both supplied programs implement the same successful identity map. The number of executed steps is outside that receiver.

For a receiver that also asks how many steps occurred, collapsing these programs is incorrect because their answers are `1` and `2`. A compiler faithful to this second receiver must retain enough information to recover the count, for example an endpoint function paired with the step count. If the receiver instead requests the full trace, the compiler must retain the requested ordered intermediate states, actions, or event occurrences; a count alone would then be insufficient. Equal endpoint behavior never supplies those extra observations automatically.

## 9. Information and performance

If parity is exactly decoded from the tag, the information claim is that this representation preserves the parity question: parity is constant on each tag fiber. It does not follow that the tag reconstructs the whole number. Cheap access once the tag exists supplies no end-to-end speedup when producing the tag incurs the original expensive computation; a benefit for repeated access would need a stated workload and an amortized cost result. “Instantly” also needs a cost model if intended literally.

Fair comparison, in two sentences: Compare the tag method with an ordinary parity baseline on the same declared constructor class, input sizes, hardware or abstract cost model, and held-out cases, charging both methods for input access, preprocessing or tag construction, queries, and storage. Report one-query total cost and repeated-query amortized cost for a declared query count, retaining failures and giving neither method free preprocessing.

## 10. Complete integer parameterization

The complete fiber is

`MANY({(t+7,t) : t in Z})`.

Correctness: for every integer `t`, both coordinates are integers and `(t+7)-t=7`. Coverage: for any admitted solution `(x,y)`, choose `t=y`; the equation forces `x=y+7=t+7`, so the pair occurs in the displayed family. The parameter is unique because it is the second coordinate.

This is an exhaustive symbolic parameterization with a written universal correctness-and-coverage proof for this equation. It also induces an enumeration if the integer parameters are listed, for example in the order `0,1,-1,2,-2,...`; no completed finite listing of all solutions is claimed. It can serve as a certificate of this particular answer and gives no proof of an arbitrary integer-equation solving procedure.

## 11. Synthetic psychology table

The supplied result is finite agreement between independent implementations on the supplied synthetic rows. It is useful implementation evidence for that tested scope, but it neither establishes checker soundness nor validates a connection between internal labels and actual human psychology. If those rows were proved to exhaust a declared finite carrier, the agreement would cover that entire finite table; that extra coverage premise is not supplied here.

A proposed external test is to define, before collecting outcomes, a bridge from the model's inputs to a specific observable response in a standardized task, freeze predictions, and evaluate them on consenting held-out participants against a predeclared base-rate or other ordinary baseline. Record the measured prediction accuracy and uncertainty and a failure criterion, such as no held-out advantage over that baseline; a reported answer or observed choice is the measured outcome, not automatically a person's latent belief.

A hostile control is to randomly permute the outcome assignments across held-out participants while retaining the outcome frequencies and rerun the frozen evaluation. Comparable apparent success on that control would undermine the claimed input-to-outcome bridge and motivate checking leakage or an uninformative metric. These are proposed tests, not observed validation results.

The internal table labels do not authorize diagnosing a person's beliefs. Even a successful test of the narrow observable response would establish only the tested bridge and scope, not an unrestricted belief or personality diagnosis.

## 12. Purpose for a skeptical reader — five sentences

RPRM organizes mathematical problems around explicit carriers, relations, operations, and the questions a representation must preserve. Its tools connect to existing mathematics such as relational representations, fibers, quotients, and transition-system refinement, so renamed concepts do not establish novelty. One valid bridge encodes a supplied many-sorted structure with a finite finitary signature using injective sort encodings and relational graphs, preserving and reflecting atomic statements and restricting quantifiers to encoded images; structural induction then preserves the truth of translated first-order statements. A concrete question it exposes is whether retaining integer parity suffices for a later operation enabled only at zero, which fails because the same summary merges `0` and `2` despite their different enabledness. Physical interpretations remain separate hypotheses requiring an explicit model-to-system bridge and evidence, and neither shared terminology nor this semantic encoding establishes physical truth or an all-purpose theorem solver.

## Handbook sufficiency and concrete ambiguities

The handbook alone suffices for the core reasoning required by all twelve questions, with ordinary mathematics supplying the small calculations and coverage arguments. I found no blocking omission requiring a companion RPRM document. The assessment establishes this bounded result, not mastery of every domain or universal theorem-proving ability.

Concrete places where assumptions must remain visible:

1. **Exam 5's initial partition:** “distinguishes r,s,t from x,y” does not explicitly say whether `r,s,t` are pairwise separated. The shortest observation witness is unchanged, but the first refinement step and whether action `a` already violates the initial summary congruence depend on it. Listing the partition blocks would remove this ambiguity.
2. **Exam 6's stochastic extension:** successor lists have no probability rule by themselves. The handbook supplies the correct class-mass criterion, but the actual probabilities require a declared rule; uniformity over entries and uniformity over distinct outcomes are different conventions.
3. **Exam 3's implementation description:** it does not state an actual summary map, so the faulty typed comparison is established while a source-state merge is only conditional. Writing the source, receiver codomain, and proposed summary separately would make the implementation defect fully concrete.
4. **Exam 10's result categories:** a proved symbolic family may also serve as a certificate and induce an enumeration; those labels are not mutually exclusive. The decisive boundary is the scope of the proved coverage, not the label chosen for the answer.
5. **Domain validation in Exam 11:** neither input supplies an operational bridge from synthetic psychological labels to human measurements. The handbook makes clear why such a bridge is required, but cannot supply a domain-specific validation protocol or diagnosis from internal agreement alone. This is an explicitly unresolved application obligation, not a missing core mathematical rule.

