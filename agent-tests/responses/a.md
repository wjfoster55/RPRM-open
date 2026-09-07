# Assessment A: scored mathematical response

1. With both missing ports jointly typed in `{0,1,2,3,4}`, the complete fiber is
   `{(0,0),(0,1),(0,2),(0,3),(0,4),(1,0),(2,0),(3,0),(4,0)}`.
   The disposition is **MANY** with these nine members. Completeness follows because ordinary multiplication of nonnegative integers is zero exactly when at least one factor is zero. The readout `a*b` is nevertheless determined as **0**: every member gives the same readout. Determining that readout does not uniquely determine the missing joint tuple. This is an exact finite result for the stated carrier and law.

2. When no ports are missing, there is exactly one possible assignment to the empty set of ports: the empty tuple `()`. For a lawful supplied row that assignment succeeds, so the completion fiber is `{()}`, with disposition **ONE(())**. For an unlawful supplied row it fails, so the fiber is `∅`, with disposition **NONE**. These are distinct fibers, of cardinalities one and zero; this conclusion follows from the completion definition.

3. Assuming the two witnesses are distinct and have been checked against the law, the search may report **at least two compatible witnesses**, identify them, and mark the unresolved complete fiber **OPEN**. A time limit supplies no completeness argument on the infinite carrier. It may not present those witnesses as a complete **MANY** family. A separate proof giving an exhaustive parameterization could establish MANY, but no such proof is supplied here.

4. Using the same middle witness in both relations, the endpoint composition is
   `S∘R = {(u,v)}`.
   The retained-witness relation is
   `{(u,m0,v),(u,m1,v)}`.
   Assuming `m0≠m1`, projection `(x,y,z)↦(x,z)` merges two different triples and is therefore not a CAR between these carriers. It is an acceptable lossy projection for a receiver asking only which endpoint pairs are reachable, or whether an endpoint pair has some middle witness. It is insufficient for a receiver retaining middle-witness identity or multiplicity. These conclusions are exhaustive for the supplied finite relations.

5. The marginal product is
   `{(red,small),(red,large),(blue,small),(blue,large)}`.
   Its spurious answers are `(red,large)` and `(blue,small)`. Retain the original joint set, or carry an equivalent constraint permitting exactly its two correlated rows. Independent marginal membership cannot replace joint membership. This is an exact comparison of the supplied finite sets.

6. No. An exact operational quotient for this partial action requires enabledness to be constant within each C-fiber: `T_a` must be enabled at both p and q or at neither. That condition fails even though their present observations agree. Consequently a single quotient state cannot determine whether action a is permitted. This is a direct counterexample to the claimed quotient, so the proposed quotient certificate is **REJECT**.

7. The shortest separating word is `a`, of length one. The empty word gives observation 0 for both states; after a, p reaches r with observation 1 and q remains q with observation 0. Enabledness agrees because the action is total, but successor summaries do not: `C(T_a(p))=B≠A=C(T_a(q))`. Thus update compatibility fails in the merged A-fiber, and the proposed operational quotient is **REJECT**. The empty-word and one-step checks prove shortestness in this supplied machine.

8. Two future classes are required, one for each distinct present observation. The separating word is the empty word `ε`. With no actions it is the only finite word, and observations 3 and 4 already distinguish the two states. This is the complete future comparison for the stated machine.

9. Assuming all three states have the same enabled action alphabet and every action is the stated self-loop, every finite word leaves each state's observation unchanged and equal to the others'. The canonical future quotient therefore has **one class**. The least stable refinement retaining the old summary has **three classes**, since retaining that summary forbids any of the old distinctions from being merged. Its initial three singleton classes are already stable under the self-loops. These conclusions follow for all finite words by induction; no sampling is needed.

10. If these are the complete old fibers under consideration, the smallest additional reusable tag alphabet has **three symbols**. The fiber with three distinct Q-values requires three tags, because C is constant there and the decoder must distinguish those values. Three tags also suffice: assign distinct tags to the Q-values within each old fiber, using only two of the symbols in the first fiber. Tags may be reused across different old fibers because C identifies which fiber's decoding rule applies. This proves both the lower bound and its attainability for the stated finite value counts. Unspecified additional fibers could raise the bound.

11. Assuming A and B are different successor summary classes, the states cannot merge under a receiver retaining the next-summary probability law. Their probabilities of landing in A are respectively `1/4` and `3/4`, so that receiver distinguishes them. Equal support reports only which classes have positive probability and does not settle equality of laws. The conclusion uses the supplied exact probability masses; it does not require any inference about longer path distributions.

12. The landed operation is `L=D∘P∘E:X→X`. The equation `D∘E=id_X` proves recovery when no intervening motion changes the encoding, but it does not determine what arbitrary P will do. To implement a desired operation F, prove `D∘P∘E=F`, with any relevant domains and enabledness if the desired operation is partial. Any claimed receiver-preservation equation must also be proved. Reversibility requires an actual inverse on the declared carriers and verification of the inverse equations; it does not follow from the retraction. For example, on a two-element X with E and D both identity, constant P makes L constant and noninvertible. This is an ordinary mathematical counterexample to any unconditional invertibility claim.

13. In the source singleton carrier, `∀x P(x)` is true because P holds at s. In the full target carrier `{s,extra}`, the unrestricted statement `∀y P_target(y)` is false because P does not hold at extra. For the encoding with image `{s}`, the correct translation is
    `∀y (y∈E(X) ⇒ P_target(y))`,
    equivalently quantification restricted to the encoded image. It is true and agrees with the source. This example shows exactly why injective encoding alone does not justify unrestricted target quantification.

14. Assume N is a nonnegative integer and positions are indexed from the left starting at zero. The constructor gives a word of width `N+1`: digit 0 is `1`, and each digit at a valid position `1≤i≤N` is `0`. A local query can compare its index with these bounds and answer without expanding the entire word. This exploits the particular constructor's rule. It does not supply a compact rule for every arbitrary word of the same length, nor make arbitrary global predicates on such words cheap; access to or computation over their actual content remains necessary. "Cheap" here means avoiding full expansion, not a proved constant bit-operation bound.

    Forgetting width by converting a numeral to an integer can merge representations such as `0010` and `10`, losing leading-zero and position data. For this particular canonical word, the value is `10^N` and has N+1 canonical decimal digits, so there is no leading zero to lose. Nevertheless, retaining only an integer does not by itself retain the original constructor or guarantee its cheap query procedure. These are statements about representation information and available access, not a benchmark result.

15. Four readings must be typed separately:

    - **Integer value:** 1000 is an element of the integers, equal to `10^3`.
    - **Decimal word:** `"1000"` is a four-position base-ten string consisting of one leading 1 and three zeros. Decimal evaluation maps it to the integer.
    - **Multiplication path:** starting at 1 and applying multiplication by ten three times gives `1→10→100→1000`. The path carries three transitions and intermediate states; its endpoint is the integer 1000.
    - **Proposed geometric dimension:** describing 1000 as a three-dimensional object needs a defined geometric carrier, a specified notion of dimension, and an explicit construction/map with the claimed preservation property.

    Neither the exponent 3, the three zero symbols, nor the path's three steps alone supplies that geometric connection. One may construct a particular geometric model, but its dimensional property comes from that model and its proof. The first three views above are exact elementary descriptions; the unspecified fourth connection remains **OPEN**, and introducing its geometric carrier requires an explicit new-carrier declaration.

16. Rearranging the XOR equation gives
    `b4=b1 XOR b2 XOR b3=1 XOR 0 XOR 1=0`.
    This uniquely recovers the erased bit under the supplied parity law and trusted three given values: **ONE(0)**.

    If instead exactly one bit of an originally valid four-bit word is flipped at an unknown position, a nonzero parity check detects the error, but it does not locate which of the four bits flipped or determine the unique corrected word. Flipping any one of the four received positions restores parity, leaving four candidate originals if there are no further constraints. Without an error-count promise, a nonzero check indicates a parity violation, consistent with an odd number of bit flips; even numbers of flips may escape detection. These are exact consequences of this parity code, not a claim about the truth of external data.

17. With a guarantee of at most one wrong report about the same binary proposition, the proposition is **1**: if its value were 0, the three reports of 1 would all be wrong, contradicting the guarantee. With no error guarantee, the reports establish agreement among three channels and disagreement with the fourth, but they do not determine the proposition's truth. In particular, a common wrong source could produce all three 1s while the 0 is correct. The first conclusion is deductive conditional on the guarantee; the second identifies an unresolved source-truth question.

18. Passing every row can support a finite-model invariant only after establishing that every admitted seed enters the safe set, the checked rows cover all required transitions, those transitions preserve the safe set, and the safe set excludes bad states. For a claim about a real-world system, one additionally needs a justified bridge showing that its admitted initial states and all relevant possible transitions are covered by this model, and that the model's safety/bad-state interpretation matches the external claim. Induction then supports every finite run within those established assumptions.

    A donut check that passes itself cannot supply that external coverage and transition bridge merely by checking itself. Nor does assuming its own soundness prove its soundness. Independent implementation agreement is useful checking evidence, but neither that agreement nor the finite table pass alone proves the unrestricted real-world claim. The external claim remains **OPEN** until the missing bridge is established.

19. No. An exact construction certifies the specified integer, not its primality. The prime exponent `p=11` gives
    `2^11−1=2047=23·89`,
    a concrete hostile case. The factorization is an exact disproof of the implication "prime exponent implies Mersenne prime."

    The expression is a compact description relative to the expanded number. Its compactness does not establish low cost for every requested computation, including primality certification or factorization. For example, the binary output has p one-bits, so materializing that full output already requires work proportional to its output length in a usual explicit-output model, even if p was supplied compactly. Label length, representation access, expanded-output cost, and decision/proof cost are separate quantities.

20. Assuming the manuscript actually proves the stated obligations, its strongest conclusion is semantic preservation for its supplied class of many-sorted structures with finite finitary signatures: injective sort encodings, graph/relation translations, atomic preservation and reflection, and image-guarded quantifiers yield truth-preserving first-order translations by structural induction. This is a theorem about faithful representation at that scope. It supplies neither a universal decision procedure nor an automatic speedup.

    A toy protein contact table, by itself, supplies a finite proposed model or example. Any exhaustively verified answers or experimentally observed results would support only their explicitly admitted table, receiver, conditions, and evidence grade; the question supplies no such successful result to presume. A real protein-folding conclusion requires its own justified link to physical states, relevant laws/energetics and conditions, target notion of a correct answer, coverage, and actual solving or validation evidence. The representation theorem can preserve the statements of a supplied model without making that model an adequate account of proteins or solving its instances. The protein pack therefore does not inherit a solved protein-folding result. Such an application remains an experimental proposal until its own evidence establishes more.

## Concrete handbook omissions or ambiguities encountered

No missing core concept prevented an answer to these 20 questions. The following clarifications would make the self-contained contract more precise:

1. **Digit-query cost model (question 14):** "cheap local digit queries" does not specify how N and the query index are represented, an indexing convention, or the cost model. The constructor justifies avoiding expansion; it does not by itself justify constant-time bit complexity.
2. **Complete MANY representations (questions 1 and 3):** the requirement is clear, but the handbook gives no worked infinite-fiber example with a parameterization and a surjectivity/coverage proof. Such an example would help a reader implement its completeness obligation beyond the finite examples.
3. **Repair-tag upper bound (question 10):** the handbook explicitly gives the necessary maximum-fiber lower bound, but does not explicitly state the finite construction proving that this number of reusable symbols also suffices. The ordinary within-fiber assignment argument fills that small gap.
4. **Reopen-route content (question 4):** the handbook requires an explicit preimage family or reopen route after loss, but does not specify a minimal record by which a later receiver can actually recover forgotten witnesses. The concrete retained triples suffice in this question; a general implementation would need to define that record.

