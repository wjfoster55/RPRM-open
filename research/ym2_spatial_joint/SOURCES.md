# Sources and evidence grades

Accessed 2026-09-12. Established literature supplies the gauge theory and
invariant-theory setting. Exact witnesses, the chosen graph normalization,
the explicit calculations and their explanatory connection to the retrieved
chats are derived in this task. No priority claim is made.

- John Kogut and Leonard Susskind, *Hamiltonian formulation of Wilson's
  lattice gauge theories*, Physical Review D 11 (1975), 395–408.
  [Publisher record](https://journals.aps.org/prd/abstract/10.1103/PhysRevD.11.395).
  The abstract was inspected for the established Hamiltonian lattice/rotator
  construction. We do not attribute our coefficient choices or graph-specific
  formulas to an unread part of this paper.
- Andreas Ipp and David Müller, *Implicit schemes for real-time lattice gauge
  theory*, [arXiv:1804.01995](https://arxiv.org/html/1804.01995), introduction
  and §4, equations (95)–(110), especially (100)–(108). These were inspected
  for link transformation, reversed links, plaquette transport, gauge-invariant
  traces and small-spacing correspondence. Their numerical schemes are not
  used or rerun. Their continuum commutator convention differs from the first
  YM2 note; this task explicitly defines its group and generator convention.
- Giovanni Forni, William Goldman, Sean Lawton and Carlos Matheus,
  *Non-ergodicity on SU(2) and SU(3) character varieties of the once-punctured
  torus*, Annales Henri Lebesgue 7 (2024), 1099–1130,
  [author-hosted PDF](https://math.umd.edu/~wmg/AHL_2024__7__1099_0.pdf),
  §2.1–2.2, pp.1101–1102. The compact-group quotient and classical
  Fricke–Vogt three-trace result provide established context for our direct
  two-quaternion proof. No ergodicity result is imported.

The source and Gauss constraints in DYNAMICS.md are defined and derived
explicitly. STATIC_JOIN.md proves its image, fibers and update laws directly
from Pauli multiplication and Euclidean inner products. The exact checkers
test explicit rows, including gauge transformations, against independent
matrix calculations. Finite tests support these formulas; they are not formal
proofs or proof of the checkers' universal soundness.

CHAT_BRIDGE.md gives exact chat titles, IDs and relevant message IDs. Those
are attributed conceptual leads, not independently accepted new arithmetic
or complexity theorems. Earlier YM1 and YM2 evidence is reused within its
previously recorded scope. This finite classical spatial test does not
construct a continuum quantum theory or establish a spectral bound; it
identifies and repairs particular information losses relevant to building
larger interacting descriptions.
