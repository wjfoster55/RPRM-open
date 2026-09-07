# Included tools and status

This inventory distinguishes implemented tools from definitions and future
work. A named concept in the glossary is not automatically an implemented
solver. The standalone repository contains mathematical exposition and code;
external scholarly work is cited where used.

## Executable finite mathematics

| Module | Tools | Boundary |
|---|---|---|
| [Core](rprm/core.py) | Nominal sorts, typed ports/values, finite relations, complete aperture fibers, converse, composition and retained middle witnesses | Exact enumerated tables; no arbitrary symbolic solver |
| [Core](rprm/core.py) | Occurrence attachment with context and identity | Equal payloads do not merge distinct occurrences |
| [Core](rprm/core.py) | Deterministic, nondeterministic and rational stochastic quotient checks | Complete declared source tables; rejects inconsistent retained behavior |
| [Core](rprm/core.py) | Question refinement, lift–motion–landing, vacancy swaps | Declared maps and finite state carriers |
| [Core](rprm/core.py) | Atomic state successor with validation and stale-parent rejection | In-process reference behavior; no distributed service or persistence promise |
| [Futures](rprm/futures.py) | Shortlex-least separating word, canonical finite future quotient, least stable refinement retaining an old summary | Finite deterministic partial machines; failure is an explicit observation tag |
| [Proof donut](rprm/proof_donut.py) | Fiber/readout disposition, aperture transport, invariant induction, descent, paths/cycles and quotient certificates | Complete finite built-in carriers and tables; no circular soundness certificate |
| [Unification checker](checks/unification.py) | Small first-order syntax translation and independent semantic evaluation | A bounded executable example of the written general translation theorem |

The scripts in [examples](examples/quickstart.py) demonstrate several
apertures of one law, a distinction that appears only after continuation,
and agreement between independently implemented quotient checkers.

## Mechanical Motion Atlas

The [2D atlas](atlas/index.html) provides ideal mechanism laws, a typed
component builder, equations and export. Its own [README](atlas/README.md)
documents exactly which outputs, projections and numerical approximations
are implemented. A sampled picture is a receiver of the law's output; it is
not interchangeable with the full state or an exact inverse.

The earlier spatial-display prototype is not included in this candidate.
Its scalar/vector output and discontinuity propagation need a consistent
contract before a useful standalone successor can be offered. No general
3D solid mechanics, collision solver or arbitrary shape-morphing tool is
claimed by the 2D application.

## Proof and concept coverage

- [Core](docs/core.md), [operations](docs/operations.md) and
  [unification](docs/unification.md) give definitions, written proofs and
  counterexamples. The glossary is a navigation layer over these and other
  explicitly scoped constructions.
- [Two Lean sources](docs/formal-proofs.md) formalize 20 selected relational
  and deterministic operational-fold declarations.
- [Independent finite checks](docs/verification.md) test the implementations
  and expose hostile cases. Their passing counts are finite evidence.
- [Origins](docs/origins.md) offers mathematical initial-state and generative
  models. The physical interpretation remains an open modeling question.
- [Revised Fermat proof](docs/fermat.md) establishes the stated bounded-side
  result for min(a,b)<=4000 and every n>2. Its [checker](checks/fermat.py)
  replays finite certificates used by the written reduction. The unrestricted
  RPRM proof remains open.
- The [main paper](MANIFESTO.md), [PDF](RPRM-Manifesto.pdf),
  [reader's guide](LAYPERSON_GUIDE.md) and [agent handbook](AGENT_HANDBOOK.md)
  offer connected entry points. [Four figures](figures/README.md) show complete
  small examples and failure cases. [Handbook assessments](agent-tests/README.md)
  retain the tested versions and bounded comprehension evidence.

## Experimental starter packs

All five [packs](experimental/README.md) are explicitly experimental. Each
contains a README, executable model and independent finite checker. Ray
tracing, music, protein and question selection also include worked examples.

| Pack | Delivered tool | Open application boundary |
|---|---|---|
| [Primes](experimental/primes/README.md) | Compact numeral queries, scale coordinates, small conventional Lucas–Lehmer reference, certified square-frontier expansion with an independent proof-donut audit | No record-prime certificate or established algorithmic advantage; finite expansion does not close the unrestricted Fermat derivation |
| [Ray tracing](experimental/ray-tracing/README.md) | Exact rational toy geometry and retained relation updates | Bounded 2D scenes; no production renderer speedup |
| [Music](experimental/music/README.md) | Exact symbolic pitch, assignment and cyclic event relations | No perceptual or acoustic validation |
| [Protein folding](experimental/protein-folding/README.md) | Newly proposed exhaustive H/P lattice toy through eight residues | No molecular conformation prediction |
| [Context and communication](experimental/context-communication/README.md) | Newly proposed synthetic hypothesis fibers and question selection | No psychological or therapeutic efficacy claim |

Further geometry, infinite-state algorithms, automatic certificate discovery,
and physical modeling can be added by supplying their own carriers, proofs,
admission checks and counterexamples. They are not silently covered by the
existing executable or formal receipts.
