# Exact two-path lab

An exact rational implementation of supplied conventional two-path quantum models. The suite contains 31 tests covering finite fixtures, independent matrix calculations, hostile controls and input admission. It reports no physical experiment, new physical law, arbitrary slit geometry or continuous-time dynamics.

The [main manuscript](../../MANIFESTO.md) gives the written two-path derivations. This directory's [test contract](TEST_CONTRACT.md) states the admitted subset and expected controls; the model and tests run without that manuscript or any private file.

## Run

Python 3.10 or newer; standard library only. From this directory:

```sh
python -I -B test_model.py
python -I -B test_model.py --output .artifacts/two-path.json
```

The default receipt is `.artifacts/two-path.json` beside the test runner. An explicit relative output is resolved against the working directory. The output must be a `.json` file under a directory named `.artifacts`; missing parent directories are created. `--receipt` is an alias for `--output`.

From the release repository root, the aggregate-compatible direct command is:

```sh
python -I -B experimental/two-path-lab/test_model.py --output .artifacts/two-path.json
```

The tests load the adjacent model by its explicit local path, so isolated Python needs no installation or `PYTHONPATH`. The model performs no I/O. The test runner reads the four declared source inputs and writes its selected receipt; it makes no network request or subprocess call and uses no random sampling.

## Exact types and bounds

`Q(real, imag)` represents a complex number with `Fraction` components. Constructors accept only exact `int` or `Fraction` components; `bool`, binary `float`, strings and Python `complex` are rejected. Probabilities are `Fraction` values. No tolerance is used for any claimed equality.

`matrix(rows)` returns immutable tuples of `Q` entries. Every axis has length at most six. Path and marker dimensions are two, with joint basis `(00,01,10,11)`. Path measurements have two or three outputs; marker POVMs have one to four outcomes. The maximum six-dimensional matrix arises after a three-output path isometry on a joint state. The underlying quantum state space is continuous. This exact API admits a countably infinite rational-component subset; the test fixtures are finite.

`ScaledOperator(A,d)` represents `A/sqrt(d)` for positive rational `d`. Conjugation is computed as `A rho A* / d`, with no root evaluation. A Hadamard or balanced recombiner uses `d=2`. The API does not coherently add arbitrary differently scaled operators; such a sum can leave this rational representation.

For Hermitian matrices of dimension at most six, `validate_positive` checks all principal minors by exact Gaussian-rational elimination. Their nonnegativity is necessary and sufficient for positive semidefiniteness. `validate_density` additionally requires exact trace one. It does not merely check the diagonal. There are at most 63 nonempty principal minors.

`pure_density(vector)` intentionally normalizes a nonzero rational vector at the density level. Other state APIs reject invalid densities rather than silently renormalize them. Marker vectors supplied to `marked_joint` must already be normalized.

## Admitted API

| API | Contract |
|---|---|
| `Q`, `matrix`, `identity`, `dagger`, `multiply`, `scale`, `add`, `tensor`, `trace`, `determinant` | Bounded exact arithmetic; dimensions and numeric types are checked. |
| `validate_positive`, `validate_density` | Exact Hermitian/PSD check; a density also has trace one. |
| `pure_density(vector)` | Normalize a nonzero exact vector, dimension at most six. |
| `marked_joint(path_state, marker_zero, marker_one)` | Apply the isometry mapping path basis state i to i tensor d_i, for any rational path density and pure normalized qubit markers. |
| `partial_trace_marker(joint)` | Trace the full marker out of a valid four-dimensional density. Arbitrary rational mixed joint states may be supplied directly. |
| `ScaledOperator`, `validate_isometry`, `apply_isometry` | Complete scaled isometry evolution within dimension six; column orthonormality is checked. |
| `phase_gate(index)`, `phase_recombiner(index)` | Indices 0,1,2,3 mean phases 0,pi/2,pi,3pi/2. Recombiner rows are `[1,z]`, `[1,-z]`, divided by sqrt(2). |
| `full_output_probabilities(joint, path_operator)` | Evolve the full joint matrix, then sum output marker diagonals. Does not call partial trace or the coherence formula. |
| `reduced_output_probabilities(path_state, path_operator)` | Reduced-matrix measurement using the supplied path density. |
| `marker_channel(joint, kraus)` | One to four scaled qubit Kraus matrices satisfying exact completeness; marker-only action. `RESET_MARKER` and `DEPHASE_MARKER` are supplied. |
| `coherent_cnot_inverse(joint)` | Apply self-inverse CNOT; it undoes the fixture prepared by that interaction, not every possible marker. |
| `joint_output_probabilities(joint, path_operator, marker_effects)` | Complete positive marker POVM; result indexed `[path output][marker outcome]`. |
| `marginal_output(table)`, `conditional_output(table, marker_index)` | Validate a normalized nonnegative exact joint table. Conditional returns `(weight, distribution)` and rejects weight zero. |
| `CoherenceReceiver.from_density(state)` | Retain `chi=rho[1,0]`; `probabilities(index)` gives the balanced output distribution. |
| `CoherenceReceiver.advance("phase", index)` | Only supported continuation. Other operations, including `"hadamard"`, raise `UnsupportedOperation`. |

The full-matrix scaled-isometry primitive supports more operations than the compressed receiver. That does not enlarge the receiver contract.

For `gamma=<d0|d1>` and input amplitudes a,b, `chi=conjugate(a)*b*gamma`. The output convention is `P_plus=1/2+Re(z*chi)`. Detector overlap i gives plus probability zero at phase index 1. All amplitudes and basis labels use that fixed convention.

Retaining chi compresses a supplied mathematical state description; it does not extract exact amplitudes from one unknown particle. It preserves the admitted phase scans and loses population and joint-marker detail. Path states zero and one form the hostile collision when a Hadamard is added.

## Verification scope

The frozen tests include all 48 entries of six markers by four phases by two outputs, nine entries of the rational three-output controls, independent test-side contractions, eraser joint and weighted conditional patterns, mixed states, phase continuation, the unbalanced population collision, local channels versus controlled inversion, and invalid inputs.

Negative controls reject dropped coherence, magnitude-only coherence, conjugation, coherent addition of distinct marker outcomes, and presenting a selected fringe as the marginal. Full-matrix evolution and the hand-frozen expected probabilities do not depend on the receiver formula.

The runner writes a fresh PENDING receipt before checking, then requires exactly 31 tests, successful assertions, no skipped or expected-failure tests, and equal source hashes before and after execution. The final JSON contains PASS or FAIL, exact fixture coverage, interpreter identity, failures and the four source hashes. A changed suite size requires an explicit update to this contract and the expected-count gate.

The snapshots are taken after model import and after the tests. Equal endpoint hashes do not establish the absence of a transient modification or independently attest committed-byte origin. A successful run establishes its finite implementation checks, not experimental agreement or a continuum geometry theorem.

Additional exact regression controls cover a non-leading negative principal minor, noncanonical complex preparation, a nonprojective Kraus channel with different scale weights, and a complete three-by-four joint POVM table. They are implementation regression coverage, not held-out experimental predictions.

`SOURCE_MANIFEST.json` inventories the four distributable source files by SHA-256. It is a byte binding, not an execution receipt or proof of correctness.
