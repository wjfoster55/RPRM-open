# Mathematical context and references

RPRM builds with established mathematics. The names used for a question,
receiver or workflow do not establish priority over related constructions.
The references below identify relevant antecedents and background; they are
not endorsements of RPRM or proofs of every claim made here.

The full book's [bibliography](../MANIFESTO.md#bibliography) supplies the
broader reading list for the expanded argument. It separates
[standard mathematics](../MANIFESTO.md#mathematical-definitions-and-standard-theory),
[established Fermat attribution](../MANIFESTO.md#established-fermat-attribution),
[supplied models and computational constructions](../MANIFESTO.md#standard-models-and-computational-constructions),
[empirical starting points](../MANIFESTO.md#empirical-context-and-experimental-starting-points),
and [historical antecedents](../MANIFESTO.md#historical-antecedents-and-further-reading).
The entries below retain the more specific context for the core, operator
and implementation references. A citation to empirical literature does not
report execution of this repository's research proposals.

- **E. F. Codd, “A Relational Model of Data for Large Shared Data Banks” (1970).**
  The original relational-model paper develops n-ary relations and operations
  while separating data from a chosen representation. This is relevant to the
  finite relation and projection language used here. RPRM's specific typed
  translation and fiber claims are proved in the adjacent documents.
  [Publisher's research record](https://research.ibm.com/publications/a-relational-model-of-data-for-large-shared-data-banks).
- **Gordon D. Plotkin, “A Structural Approach to Operational Semantics.”**
  Transition systems and their rule-based interpretation are established
  foundations for talking about operations and executions. The deterministic
  quotient conditions in this repository specify an additional preservation
  question about such a system.
  [Author's paper](https://homepages.inf.ed.ac.uk/gdp/publications/sos_jlap.pdf).
- **Julien David, “The Average Complexity of Moore's State Minimization
  Algorithm is O(n log log n)” (2010), sections 2.1–2.2.**
  The discussion of finite-word indistinguishability and Moore refinement is
  relevant to the finite-future algorithms. This repository supplies its own
  proof for tagged failure and arbitrary admitted observations; it does not
  claim the paper's average-case complexity for the reference implementation.
  [Author's paper](https://lipn.fr/~david/articles/mfcs10.pdf).
- **Tobias Fritz, “A synthetic approach to Markov kernels, conditional
  independence and theorems on sufficient statistics” (2020).**
  This develops a categorical account of probability and sufficiency.
  RPRM's implemented stochastic quotient is much narrower: finite rational
  kernels and exact mass on retained classes. No equivalence with the whole
  Markov-category framework is asserted without a specified bridge.
  [Author's paper](https://arxiv.org/abs/1908.07021).
- **The Lean community, “Theorem Proving in Lean 4,” Axioms and Computation.**
  This explains the foundational role of propositional extensionality,
  quotients and choice. Those are the allowed dependency names in this
  repository's formal replay; actual use is reported declaration by declaration.
  [Official documentation](https://lean-lang.org/theorem_proving_in_lean4/Axioms-and-Computation/).

Links cite external works without redistributing their text or licensing
their contents. The repository's reuse licenses apply to the original
material described in [LICENSING.md](../LICENSING.md).
