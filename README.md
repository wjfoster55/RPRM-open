# The RPRM Manifesto

**A relational framework for mathematical unification.**

**RPRM stands for Relational Pressure Retention Model.** The name comes from
the motivating physics proposal about underlying relations, pressure and
retention. It remains the name of the whole framework. The
[relational-layer account](docs/relational-layer.md) explains that motivation
and distinguishes it from the mathematical results proved here.

**Current reading edition:** [MANIFESTO.md](MANIFESTO.md) and the
[155-page PDF](RPRM-Manifesto.pdf) contain the revised text and the author's
afterword. The PDF has completed its layout review; exact source and build
inputs are recorded in [DOCUMENT_BUILD.json](DOCUMENT_BUILD.json).

RPRM describes mathematical problems through their carriers, relations,
operations, observations, and missing information. Its purpose is to connect
existing mathematics while preserving what each source system means. An
explicit change of representation can expose a different question, explain
why information was lost, or show exactly what must be retained to continue.

Its [relational-layer proposal](docs/relational-layer.md) asks whether
observable physical behavior arises from underlying relations and lawful
continuations. The core makes observational sufficiency and incomplete
source recovery precise. Identifying a physical source remains a further
modeling and experimental task.

This release candidate contains the full mathematical book, seven executable
experimental packs, formal proofs of selected laws, and an interactive 2D
Mechanical Motion Atlas. Three separate research specifications propose
unexecuted scientific comparisons. Each result states its scope. The broad
unifying aim is supported by specific preservation theorems; it is not a claim that every mathematical
problem has been solved or that a physical theory of everything follows.

## One law, several questions

For the law `a + b = c`, ordinary evaluation supplies `a,b` and asks for `c`.
Another **aperture** supplies `a,c` and asks for `b`. A third supplies only `c`
and asks for the *joint* pair `(a,b)`. The carrier and law stay explicit.

On the bounded integers `{0,1,2,3,4}`, with ordinary addition and no wrap:

| Supplied ports | Missing ports | Complete answer |
|---|---|---|
| `a=1,b=2` | `c` | ONE: `3` |
| `a=1,c=3` | `b` | ONE: `2` |
| `c=3` | `(a,b)` | MANY: `(0,3),(1,2),(2,1),(3,0)` |
| `a=4,c=0` | `b` | NONE in this carrier |

The last answer changes if negative integers are admitted. The third answer
is a correlated set of pairs, not two independent lists. These distinctions
are part of the mathematical contract, not annotations added after solving.

## Read and use

| Start here | Contents |
|---|---|
| [Main book](MANIFESTO.md) · [Reading PDF](RPRM-Manifesto.pdf) | Four connected parts, appendices and the author's afterword; 155 PDF pages including the cover |
| [Core definitions](docs/core.md) | Carriers, ports, apertures, receivers, fibers, representations and affine coordinates |
| [Reader's guide](LAYPERSON_GUIDE.md) | A self-contained introduction using ordinary examples |
| [Agent handbook](AGENT_HANDBOOK.md) | Version 6: core reasoning, relational-layer scope, worked applications and a reusable procedure |
| [Relational layer](docs/relational-layer.md) | The physical proposal, what closed observations can reveal, complete examples and distinguishing controls |
| [Conceptual bridge](docs/concepts.md) | Multiple number descriptions, three plus one, errors, teachers and paired strands |
| [Operations](docs/operations.md) | Typed operations, exact quotients, shortest distinctions, stable repair and compilation |
| [Unification](docs/unification.md) | Faithful relational presentation of supplied many-sorted structures; explicit preservation proofs and scope |
| [Glossary](docs/glossary.md) | Definitions and links for the working vocabulary, including named constructions |
| [Proof donut](docs/proof-donut.md) | Coverage, compatible constraints and finite proof certificates; executable mutual checks |
| [Bounded Fermat proof](docs/fermat.md) | The min(a,b)≤4000 theorem, full argument and finite certificate replay; the independent unrestricted RPRM derivation remains open |
| [Seven executable packs](experimental/README.md) | Primes, rays, music, lattice conformations, synthetic question selection, two-path calculations and Rule Lab |
| [Three research proposals](research-packs/README.md) | Folding dynamics, BRCA1 cellular function and immune mechanisms; data-driven and scientific comparisons remain unexecuted |
| [Handbook assessments](agent-tests/README.md) | Versioned questions, answer keys, grading and bounded comprehension evidence |
| [Initial states and origins](docs/origins.md) | Generative models, zero/balance distinctions, and the premises needed for a physical interpretation |
| [Verification](docs/verification.md) | Reproduction commands, coverage, hostile controls and trust boundaries |
| [Formal proofs](docs/formal-proofs.md) | The exact 20 Lean declarations and their relation to the written mathematics |
| [References](docs/references.md) | Established mathematical context and scholarly credit |
| [Included tools](CONTENTS.md) | API inventory and development status |
| [Agent instructions](AGENTS.md) | A small starting contract for agents using or extending RPRM |

The book contains 87 written theorem, proposition, lemma and corollary
statements, including four opening statements restated in the chapters.
The [formal scope](docs/formal-proofs.md) is exactly 20 selected Lean
declarations. These counts describe different evidence.

Handbook version 6's [assessment F](agent-tests/results.md) scored 24/24 on
six targeted transfer questions, with a disclosed correction to its frozen
answer key. Version 5's assessment E scored 16/16
on four targeted follow-up questions. Assessment D scored 79/80 on twenty
broader questions using version 4; assessment C belongs to historical version 3.
The scores do not establish a controlled improvement or universal comprehension.

Run the finite examples from this directory with Python 3.10 or newer:

```sh
python -I -B examples/quickstart.py
python -I -B examples/proof_donut.py
python -I -B examples/fixed_gap.py
```

Open [atlas/index.html](atlas/index.html) in a modern browser for the local
Mechanical Motion Atlas. Its JavaScript modules are included locally; the
mathematical tools do not require an account or network service.

Run all executable Python and Node checks (Node.js 18 or newer):

```sh
python -I -B verify.py
```

Add `--lean /path/to/lean` with Lean 4.22.0 to re-elaborate the formal proofs.
Without that argument, the aggregate receipt explicitly records the formal
suite as `NOT_RUN`. Fresh receipts go into `.artifacts/`; they are not source
files and are not accepted as substitutes for executing the checks.

## Freedom to reuse

Original software is under [0BSD](LICENSE); original prose, diagrams and data
are under [CC0](LICENSES/CC0-1.0.txt). Neither asks for attribution to this
release, a contribution back, or continued contact. See [licensing](LICENSING.md)
for the boundary with external work and [third-party notices](THIRD_PARTY_NOTICES.md).

This is intended as a self-contained contribution that others can fork,
adapt and maintain independently. There is no promise of continuing support,
issue triage or review. The source, contracts and checks are supplied so that
future work can proceed without the original contributors.
