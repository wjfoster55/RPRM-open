# Symbolic music experiment

**EXPERIMENTAL — exact symbolic relations, integer sample operations, and a
finite event sequencer.** Current state: executable models with bounded cold
checks. There is no recorded audio, physical frequency model, color renderer,
observer dataset, preference model, or psychological validation.

## Run and inspect

Python 3.10 or newer; standard library only. From the repository root:

```sh
python -I -B experimental/music/example.py
python -I -B experimental/music/check.py
```

Both print JSON and optionally accept `--output ABSOLUTE_JSON_PATH` with an
absolute filename. A failed check exits nonzero. Receipts include executed
bounds and relative source hashes. Example JSON contains only synthetic
integers, labelled ports, formulas, and complete finite example answers.

## Pitch tokens, maps, and receivers

The base carrier is `Z12={0,...,11}` with modular arithmetic. Tokens are
abstract pitch classes; no register or tuning measurement is supplied.

| Carrier/readout | Definition | Count for three tokens |
|---|---|---:|
| Labelled triples | `Z12^3`; voice position observable | 1,728 |
| Multisets | Sorted triples; multiplicity observable | 364 |
| Distinct trichords | Three-element subsets | 220 |

`multiset` forgets order, and `labelled_fiber` returns **all** labelled triple
preimages. For `(0,0,7)` these are `(0,0,7)`, `(0,7,0)`, `(7,0,0)`: `MANY`.
`distinct_set` also forgets multiplicity. These are lossy readouts, not
interchangeable source identities.

There are 24 invertible maps `g_(a,s)(x)=s*x+a mod12`, where `a in Z12` and
`s in {-1,+1}`. Their inverses have parameters `(-s*a mod12,s)`. A reversed
orientation transports a rotation by `k` to a rotation by `-k`. The declared
cycle supplies no preferred origin or orientation and no natural mapping to
another domain such as colors.

The circular distance is `d(x,y)=min(|x-y|,12-|x-y|)`. On triples, the
matching distance is the minimum sum of three such distances over all six
occurrence assignments. `matching(left,right)` returns the distance and
**every** minimizing assignment as indices into the right triple. Repeated
values can give distinct assignments with the same visible values. This
assignment fiber preserves occurrence identity.

Example: `(0,4,7)` to `(2,5,9)` has matching distance `5`, witnessed by the
positionwise assignment. It measures this declared integer cost, not perceived
musical similarity. The cost is a metric on multisets: zero matching cost
means the same multiset, inversion gives symmetry, and composing minimizing
assignments with the scalar triangle inequality gives the triangle inequality.
Applying the same dihedral isometry to both inputs preserves each assignment
cost. These are direct mathematical arguments. The checker exhausts matching
costs and assignment fibers on all 364 sorted multiset representatives;
labelled-fiber and inverse-action checks also use all 1,728 labelled triples.

## Preserved counterexamples

- `(0,4,7)` and `(7,4,0)` have the same multiset and different voice orders.
- `(0,0,7)` and `(0,7,7)` have the same set and matching distance `5`.
- Integer note labels `60` and `72` both reduce to class `0`; their registers
  differ. Modulo reduction does not preserve a register query.
- A permutation such as multiplication by five can destroy chromatic
  adjacency. A fifths-based distance is a different receiver from the
  chromatic cycle distance.
- `{0,1,3,7}` and `{0,1,4,6}` have the same six-bin interval-class histogram
  `(1,1,1,1,1,1)`, but no dihedral map relates them. A histogram forgets
  arrangement. `interval_histogram` rejects repeated values because its
  carrier is a distinct subset.

## Sign, phase and addition on sampled sequences

`wave` admits 1–64 integer samples, each in `[-1,000,000,1,000,000]`.
`shift(w,k)[i]=w[(i+k) mod length]` is an invertible cyclic shift; `negate`
is pointwise additive inverse. Shift arguments are bounded integers with
absolute value at most one million. `sum_waves` requires the same sample
domain and has integer outputs in `[-2,000,000,2,000,000]`; feeding an output
back into the input carrier requires its samples to meet the input bound.

For `(0,1,0,-1)`, a two-sample shift equals negation, and adding the negative
gives four zeros. For `(4,0,-2,0,-2,0)`, **none** of its six cyclic shifts equals
its negative. Thus sign reversal is not universally a phase shift. Cancellation
also forgets the two nonzero contributions. These are integer-sequence laws,
not statements about recorded sound, hearing, or psychoacoustics.

## Finite event sequencer

A context supplies a binary mask `e` of length `P in 1..16` and a state modulus
`q in 1..16`. Its carrier is `Z_P x Z_q`, with transition

`T(f,h)=(f+1 mod P, h+e[f] mod q)`.

The inverse decrements the phase and subtracts that preceding phase's event.
Let `K=sum(e)`, `c_f=sum(e[0:f])`, and `g=gcd(K,q)`. Then `h-c_f mod g` is
invariant. A complete phase lap adds `K` to the second coordinate, so every
orbit has length `P*q/g`, and there are `g` orbits. For `K=0`, `g=q`; this
includes the all-zero mask. `event_cycles` enumerates all cycles, retaining
ordered states. It does not infer an event mask from an unstated law.

Two masks of the same length and total admit the bijective adapter
`(f,h) -> (f,h+c_target[f]-c_source[f] mod q)`. The prefix difference shows
directly that it commutes with the transitions. Equal totals still do not
mean equal temporal readouts: `(1,0)` and `(0,1)` act differently at phase zero.
The example mask `(1,0,1,0)` with `q=6` has two cycles of length 12.

## Tests, costs, and next experiments

The checker constructs scalar distances independently by breadth-first search
on the 12-cycle and compares every one of 132,496 multiset pair costs and its
complete optimal assignment fiber with a subset-assignment dynamic program.
It tests all 48,228,544 triangle inequalities
and 3,179,904 simultaneous dihedral actions, complete labelled fibers, inverse
maps, and the hostile cases above. The six-assignment implementation and
eight-mask dynamic program are transparent baselines, not a speedup claim.

The event census covers all binary masks of lengths 1–6 and moduli 1–6:
756 contexts, complete cycle decompositions, inverses, invariants, and the
adapter to each reversed mask. It does not exhaust the API's larger 1–16 bounds.
Wave checks cover every array over `{-1,0,1}` of lengths 1–5 plus the frozen
six-sample counterexample. Boolean/numeric-type and operation-domain controls
are included. Exact integers avoid rounding but do not establish any empirical
adapter.

A useful next experiment could add an explicitly supplied tuning map, a
synthesizer, or a labelled observation dataset as a **new contract**. A claim
about perception or psychology would additionally require a specified target,
held-out evaluation, leakage controls and shuffled-label baselines. Synthetic
labels and exact symbolic invariances alone do not establish such a claim.
