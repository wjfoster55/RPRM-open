# Protein-folding direction: a finite HP lattice toy

**EXPERIMENTAL — NEWLY PROPOSED.** This is a new executable teaching and
research proposal, not an extraction of a historical protein-folding result.
It solves a small, explicitly defined mathematical model. It makes no claim
to predict a real protein's structure, folding time, function, or energy.

The established hydrophobic/polar (HP) lattice-model tradition is described
by K. F. Lau and K. A. Dill, [“A lattice statistical mechanics model of the
conformational and sequence spaces of proteins,” *Macromolecules* 22,
3986–3997 (1989)](https://doi.org/10.1021/ma00200a030). The present pack chooses
its own finite bound and symmetry convention below. The RPRM contribution
here is the explicit question, complete fiber, and receiver-loss comparison;
the HP idea and exhaustive enumeration are established methods.

## Contract

Context `hp-square-oriented-v1` admits a string `s` of 1 through 8 uppercase
`H` or `P` symbols. Symbols designate toy hydrophobic/polar types. Occurrence
indices `0,...,n-1` remain distinct even when their symbols agree.

The conformation carrier is every ordered path `p=(p_0,...,p_(n-1))` in
`Z^2` with `p_0=(0,0)`, distinct vertices, and Manhattan distance 1 between
successive vertices. Equality is exact coordinate-tuple equality. Anchoring
removes translations. **Rotations, mirror images, and chain order are
retained; the first bond is not fixed to a direction.** There are 2,172
such paths at 8 residues (7 bonds). No bounding box, periodic boundary,
obstacle, probabilistic law, or time evolution is supplied.

The full contact map is the tuple of all zero-based pairs `(i,j)` with
`i+1<j` and Manhattan distance 1 between `p_i,p_j`. Its dimensionless toy
energy is

```text
E(s,p) = - sum(1 for (i,j) in contact_map(p) if s_i = s_j = H).
```

Backbone neighbors never count, and P contacts contribute zero. This is an
integer optimization score, not a measured physical energy.

| Interface | Supplied ports | Missing/readout ports | Exact direction and answer |
|---|---|---|---|
| `energy` | sequence, full path | integer score | Deterministic evaluation |
| `completions` | sequence, optional anchored prefix, optional integer energy | complete full paths | Solve the constrained relation; `NONE`, `ONE`, or `MANY` |
| `minimizers` | sequence, optional anchored prefix | minimum score and all minimizing paths | Exhaust every compatible full path; retain all ties |
| `extend` | anchored path, E/N/W/S | next full path | Partial geometric action; collision or 8-residue cap disables it |
| `mirror` | full path | reflected full path | Reflect in the x axis; applying twice is the identity |

Malformed paths (including a self-collision), invalid types, length mismatch,
and out-of-bound sequences raise `ValueError`: they are admission errors.
An admitted integer energy with no compatible path returns `NONE`. A query
does not treat an unfinished search as `NONE`; this implementation has no
sampling or early search cutoff. All paths returned by a fiber are full
coordinate witnesses, not independent per-position possibilities.

Completeness has a finite construction argument: the initial path is the
unique origin vertex; at each stage try all four unit directions and reject
exactly occupied vertices. Every admitted longer path has an admitted
prefix and one of these four final bonds. Induction therefore enumerates
all and only the admitted paths. Filtering retains precisely the requested
constraints, and comparing all retained integer scores retains every tie.
This argument specifies why the algorithm is appropriate; the independent
checker below tests its implementation on the declared finite carrier.

For `extend`, the direction is relative to the fixed ambient axes. To extend
an HP state, the caller must additionally supply the new occurrence's H/P
symbol. The sequence-extended state then uses the same score law. At the
length cap all four geometric actions are disabled by this finite contract;
a longer-chain experiment requires a new declared boundary.

## What survives a representation

The score receiver asks only for `E(s,p)`. The retained representation
`C(s,p)=(s,contact_map(p))` suffices: the displayed sum decodes the score.
This is a question fold by the defining equation. It is lossy because
different coordinate paths can have identical maps. The entire source
fiber can be recovered by enumerating this finite carrier and filtering
by `C`; neither the contact map nor an energy supplies a unique inverse.
`completions` implements the prefix/energy fiber, not a contact-map inverse
API. The example retains its source coordinates as a cold reopen witness.

The extension receiver additionally asks whether each named direction can
be appended and what contact representation the successor has. The same
`C` fails even its enabledness requirement. With sequence `PPP`, consider

```text
straight = ((0,0),(1,0),(2,0))
bent     = ((0,0),(1,0),(1,1))
```

Both contact maps are empty and both scores are zero. Appending `W` to the
straight path collides with occurrence 1. Appending `W` to the bent path
lands at `(0,1)` and is legal. Thus energy sufficiency does not establish
operational sufficiency. Retaining the full path repairs this receiver in
the present carrier. No smallest geometric repair is claimed.

Reflection preserves the score and contact map because it preserves lattice
adjacency and occurrence indices. It is an invertible map on this carrier,
with itself as inverse; it is not an identification of mirror paths.
Directional actions must be transported too: reflection swaps N and S,
and leaves E and W fixed. Equal scores do not choose one historical path.

## Worked example and reproduction

From the repository root, with Python 3.10 or newer and no dependencies:

```sh
python -I -B experimental/protein-folding/example.py
python -I -B experimental/protein-folding/check.py
```

For `HPPH`, enumeration visits all 36 oriented four-residue paths. The
minimum score is `-1`: the first and last H form a nonconsecutive contact
around three sides of a unit square. There are **8** minimizing paths,
including their orientations and reflections. The example prints every
coordinate witness. Requesting energy `+1` gives `NONE`; the one-residue
query `H` at energy 0 gives `ONE(((0,0),))`.

To also write a receipt, supply an absolute file path, for example:

```sh
python -I -B experimental/protein-folding/check.py --output /absolute/output/hp-check.json
```

On Windows use an absolute path such as `C:/output/hp-check.json`. The same
JSON is printed to stdout. Failed checks exit nonzero. The receipt hashes
all four source files using public repository-relative names; hashes bind
bytes and do not prove the underlying mathematics.

`example.py` accepts the same optional absolute `--output` argument and
exports schema `hp-square-oriented-example/v1` with only synthetic model data.

The checker independently constructs every direction word (including
collisions) with complex coordinates, filters self-intersections, and
builds contacts from occupied grid edges. The model instead grows valid
coordinate paths and compares occurrence pairs. Their path sets, contacts,
energies, and **complete minimizer fibers** must agree for all **510 H/P
strings** of lengths 1–8. It also checks every path's mirror and four
extension actions; all occurring prefixes through length 5 under the
all-H sequence, including constrained minima and all possible energies plus
impossible controls; and
admission errors, `NONE`/`ONE`/`MANY`, and the loss witness above.

## Evidence boundary and next experiment

The score decoder and reflection statements have direct arguments above;
the executable agreement is **exhaustive finite testing**. The checker is
a separately implemented oracle, not a formally verified proof of itself.
It runs from the delivered local source bytes without private data,
historical archives, network access, or a stored receipt as evidence.

The baseline is exhaustive enumeration. No faster optimizer is supplied,
and enumeration's growth is not resolved by calling its answer a fiber.
The next useful experiment is a proposed pruning or representation method
that reproduces **every** minimizing path on this frozen carrier, compared
with this baseline. Charge construction, admission, search, verification,
and output costs. A single missing tie, false collision decision, incorrect
score, or retained-map update disagreement refutes exactness. Benchmarking
and a claim of reduced total cost remain **OPEN**.

Larger chains, three dimensions, amino-acid-specific interactions, solvent,
temperature, kinetics, and comparison with experimental structures are
outside this contract. Each requires its own inputs, receiver, validation,
and admitted carrier. This pack provides no biological transfer result.
