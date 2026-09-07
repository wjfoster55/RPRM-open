# Formal proof scope

The repository contains two Lean source files, pinned by `lean-toolchain` to
Lean 4.22.0. Both import only `Init`. The replay compiles fresh copies of the
source, makes warnings errors, checks the complete expected axiom-report
inventory, and rejects dependencies outside `propext`, `Quot.sound` and
`Classical.choice`. Independently generated probes query the freshly compiled
modules; arbitrary messages printed by a proof source are not accepted as
declaration evidence. No prebuilt project module is supplied to the build.

## Relational laws

[Relations.lean](../lean/Relations.lean) contains 11 declarations in
`RPRM.Relations`:

| Declaration | Meaning |
|---|---|
| `identity_left`, `identity_right` | Relational identities on each side |
| `compose_assoc` | Associativity with existential intermediate witnesses |
| `converse_involutive` | Reversing twice recovers the relation |
| `converse_compose` | Converse reverses composition order |
| `graph_identity`, `graph_compose` | Function graphs preserve identity and composition |
| `graph_converse_inverse` | A two-sided inverse gives the converse graph |
| `retraction_section_injective` | A left inverse makes the encoding injective |
| `aperture_backward_forward` | Decoding an encoded fiber member restores it under the stated left inverses |
| `aperture_forward_backward` | Encoding a decoded target fiber member restores it under the additional right inverse |

## Observations and all finite continuations

[Carrier.lean](../lean/Carrier.lean) contains nine declarations in `RPRM`:

| Declaration | Meaning |
|---|---|
| `factorization_iff` | An observation descends exactly when it is constant on encoding fibers, with the stated surjectivity |
| `decoder_unique` | The descended observation is unique on an onto target |
| `toReachable_onto` | Restricting an encoding to its reached image gives an onto map |
| `option_map_eq_iff` | Tagged partial-result equality separates failure from success |
| `operational_fold_iff` | Fiberwise observation, enabledness and successor congruence characterize exact operational descent |
| `run_commutes` | The encoding commutes with every finite action word |
| `run_defined_iff` | Source and quotient agree on execution definedness |
| `future_preserved` | Every finite-word observation is preserved |
| `fiber_conditions_preserve_all_futures` | The fiber conditions supply quotient maps with all three execution guarantees |

These statements quantify over the types and maps in the Lean declarations,
not merely the finite examples. Partial execution uses `Option`; a missing
transition is distinct from an ordinary returned value. The all-futures
theorems concern deterministic partial operations under their hypotheses.

## Reproduce and interpret

```sh
python -I -B checks/formal.py --lean /path/to/lean --output /absolute/path/formal.json
```

Alternatively add `--lean /path/to/lean` to the root `verify.py` command.
The JSON records each declaration's actual axiom dependencies, source hashes,
compiler version/hash and compilation transcript. The temporary compiled
modules are discarded after checking.

The selected compiler and its standard library are trusted dependencies.
The portable wrapper records their compiler identity; it does not authenticate
an entire installed toolchain against an official distribution. A compiler
hash alone is not such authentication.

The full first-order unification translation, the shortest-witness bound,
minimal refinement/repair claims, geometry and all implementation correctness
are **not** thereby formalized. Their written proofs and finite checks have
their own stated scopes. No custom axiom asserting “RPRM is correct” or the
proof donut's correctness is admitted by this formal replay.
