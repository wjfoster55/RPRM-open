# Exact two-path lab: test contract

This contract specifies a bounded exact submodel of conventional quantum mechanics and the finite controls used by its 31-test suite. It is a portable statement of the implemented requirements and expected values, not a claim that these public document bytes preceded the original implementation.

The [README](README.md) gives the API, commands and output contract. The [main manuscript](../../MANIFESTO.md) supplies the mathematical derivations. Neither an external source file nor private provenance material is needed to execute these checks.

## Admitted subset

- Exact rational real and imaginary components only; no binary floats or Python `complex` in claimed exact arithmetic.
- Path and marker each have dimension two, ordered joint basis `(00,01,10,11)`. Path output has two or three outcomes. Matrix axes have a hard maximum of six.
- Rational matrices may represent a common scalar square-root denominator: an operator `(A,d)` means `A/sqrt(d)` with positive rational `d`; density evolution is exactly `A rho A* / d`.
- Four phase settings only: indices `0,1,2,3` mean phases `0, pi/2, pi, 3pi/2`, respectively. State overlaps may be arbitrary admitted rational complex values. No arbitrary-angle numerical approximation is claimed.
- Full joint density construction, marker partial trace, complete isometry output probabilities, marker-only trace-preserving channels, marker POVMs with joint and conditional output probabilities, controlled-NOT and the phase-only coherence receiver are admitted.
- States must be square Hermitian positive semidefinite with exact trace one. Exhaustive state-positivity testing uses all principal minors at the small bound. Input-domain violations must raise an explicit exception.
- Geometry, physical acquisition, arbitrary time evolution and a general quantum SDK are outside the API.

## Frozen positive expected values

Use balanced path input, marker 0 equal to `(1,0)`, and marker 1 equal to `(gamma,sqrt(1-|gamma|^2))`. The listed vectors all have rational complex components. For each row, the four numbers below are the plus-output probabilities at phase indices `0,1,2,3`; minus-output probabilities are their complements and must be checked independently for normalization.

| gamma | Marker 1 | Four plus probabilities |
|---|---|---|
| 1 | `(1,0)` | `1, 1/2, 0, 1/2` |
| 0 | `(0,1)` | `1/2, 1/2, 1/2, 1/2` |
| -1 | `(-1,0)` | `0, 1/2, 1, 1/2` |
| i | `(i,0)` | `1/2, 0, 1/2, 1` |
| 3/5 | `(3/5,4/5)` | `4/5, 1/2, 1/5, 1/2` |
| (3+4i)/5 | `((3+4i)/5,0)` | `4/5, 1/10, 1/5, 9/10` |

The complete rational three-output isometry is `[[3/5,-12/25],[4/5,9/25],[0,4/5]]`. For balanced input with gamma `1,0,-1`, its expected full output distributions are `(9,841,400)/1250`, `(369,481,400)/1250`, and `(729,121,400)/1250` respectively.

For the orthogonally marked balanced state, marker measurement in the plus/minus basis has two equally probable outcomes. Its plus-output joint probabilities at phase `theta` are `(1+cos(theta))/4` and `(1-cos(theta))/4`; the minus-output row reverses them. Conditional patterns have complementary full fringes; the unconditional output remains `(1/2,1/2)`.

The unbalanced pure path density `[[9/10,3/10],[3/10,1/10]]` with identical markers and the balanced partially marked state with gamma `3/5` have the same coherence and phase scan but different populations.

## Independent routes and controls

The principal reference route evolves the full joint matrix with the complete path isometry, then sums the marker diagonal for each output. Its implementation must not use the coherence formula or partial trace internally. A second route takes an explicit partial trace and performs a reduced matrix measurement. The receiver formula is a third route, not the sole oracle. Frozen numbers above and direct test-side contractions provide independent expected results.

Required hostile controls:

1. Dropping coherence, replacing coherence by its magnitude, or conjugating coherence must each disagree with at least one frozen case; the complex phase row must catch conjugation.
2. Coherently summing distinct final marker outcomes must fail a frozen orthogonal-marker case.
3. Treating one selected eraser pattern as the marginal must fail the weighted-marginal check.
4. Common marker unitaries, nonselective measurements and marker reset must preserve the path marginal. Full controlled-NOT reversal on the controlled-NOT-marked fixture must restore the coherent path state. Local reset must not do so.
5. A phase-only receiver must commute with all four admitted phase gates. It must explicitly reject a Hadamard continuation. Full matrix Hadamard evolution must distinguish the `|0>` and `|1>` inputs that previously shared coherence zero.
6. Reject non-Hermitian, nonpositive, wrong-trace, empty, oversized and dimension-mismatched state inputs; reject float/complex arithmetic inputs, unnormalized marker vectors, non-isometries and incomplete channels/POVMs.
7. Reject a zero-probability conditional event rather than return a normalized fiction. Validate probability-table shape, exact nonnegativity and total normalization.

## Acceptance and receipt

Every positive equality and normalization is exact. Every required negative control must expose its incorrect claim, and every domain rejection must be exercised. Acceptance requires exactly 31 tests, all successful, with no skipped or expected-failure tests. The test count is an explicit coverage gate; it does not prove that the tests themselves are sufficient for every possible use.

The runner writes a fresh JSON receipt under `.artifacts`, first with PENDING status and then with the final PASS or FAIL. The final receipt includes test count, expected count, failures/errors/skips, interpreter identity and before/after SHA-256 values for model.py, test_model.py, README.md and this contract. A source-hash mismatch prevents PASS. Independent committed-byte replay is a separate verification step; the runner does not attest its own commit origin.

The original fixture requirements are supplemented by four exact regression controls: a non-leading negative principal minor, noncanonical complex preparation, nonprojective scaled Kraus action, and a three-by-four complete POVM table. These are regression tests, not measured data or held-out scientific predictions. Probability return-type checks apply to the actual computed outputs.

The model's mathematical implementation and the independent test cases are distinct from receipt I/O. Changing output paths does not widen the state carrier, operation family, physical interpretation or evidence grade.
