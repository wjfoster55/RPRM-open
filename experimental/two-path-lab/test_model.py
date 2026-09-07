"""Frozen exact fixtures plus independent contractions; local-run receipt."""

import argparse
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import sys
import unittest

LAB = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("two_path_exact_model", LAB / "model.py")
m = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = m
SPEC.loader.exec_module(m)

HALF = F(1, 2)
PLUS = m.matrix(((HALF, HALF), (HALF, HALF)))
MARKER_ZERO = (1, 0)
MARKERS = (
    (1, 0), (0, 1), (-1, 0), (m.I, 0),
    (F(3, 5), F(4, 5)), (m.Q(F(3, 5), F(4, 5)), 0),
)
# Every output entry is literal, rather than computed from the other output.
EXPECTED = (
    ((F(1), F(0)), (HALF, HALF), (F(0), F(1)), (HALF, HALF)),
    ((HALF, HALF), (HALF, HALF), (HALF, HALF), (HALF, HALF)),
    ((F(0), F(1)), (HALF, HALF), (F(1), F(0)), (HALF, HALF)),
    ((HALF, HALF), (F(0), F(1)), (HALF, HALF), (F(1), F(0))),
    ((F(4, 5), F(1, 5)), (HALF, HALF),
     (F(1, 5), F(4, 5)), (HALF, HALF)),
    ((F(4, 5), F(1, 5)), (F(1, 10), F(9, 10)),
     (F(1, 5), F(4, 5)), (F(9, 10), F(1, 10))),
)
THREE_EXPECTED = (
    (F(9, 1250), F(841, 1250), F(400, 1250)),
    (F(369, 1250), F(481, 1250), F(400, 1250)),
    (F(729, 1250), F(121, 1250), F(400, 1250)),
)


def fixture(row):
    return m.marked_joint(PLUS, MARKER_ZERO, MARKERS[row])


def independent_full_contraction(joint, operator):
    """Test-side index contraction: no model multiplication/trace/receiver."""
    answer = []
    for output_row in operator.raw:
        value = m.ZERO
        for marker in range(2):
            for source in range(2):
                for other in range(2):
                    value += (output_row[source] *
                              joint[2*source+marker][2*other+marker] *
                              output_row[other].conjugate())
        value /= operator.denominator_squared
        if value.imag:
            raise AssertionError("Non-real contracted probability.")
        answer.append(value.real)
    return tuple(answer)


class ExactModelTests(unittest.TestCase):
    def test_all_48_frozen_phase_output_entries(self):
        for row in range(6):
            joint = fixture(row)
            reduced = m.partial_trace_marker(joint)
            receiver = m.CoherenceReceiver.from_density(reduced)
            for phase in range(4):
                with self.subTest(row=row, phase=phase):
                    operator = m.phase_recombiner(phase)
                    expected = EXPECTED[row][phase]
                    actual = m.full_output_probabilities(joint, operator)
                    self.assertEqual(actual, expected)
                    self.assertEqual(independent_full_contraction(joint, operator), expected)
                    self.assertEqual(m.reduced_output_probabilities(reduced, operator), expected)
                    self.assertEqual(receiver.probabilities(phase), expected)
                    self.assertEqual(sum(expected), 1)
                    self.assertTrue(all(type(p) is F for p in actual))

    def test_three_complete_output_distributions(self):
        for row, expected in enumerate(THREE_EXPECTED):
            joint = fixture(row)
            self.assertEqual(m.full_output_probabilities(joint, m.THREE_OUTPUT), expected)
            self.assertEqual(independent_full_contraction(joint, m.THREE_OUTPUT), expected)
            self.assertEqual(m.reduced_output_probabilities(
                m.partial_trace_marker(joint), m.THREE_OUTPUT), expected)
            self.assertEqual(sum(expected), 1)

    def test_partial_trace_complex_orientation(self):
        rho = m.partial_trace_marker(fixture(5))
        self.assertEqual(rho, m.matrix(((HALF, m.Q(F(3, 10), F(-2, 5))),
                                       (m.Q(F(3, 10), F(2, 5)), HALF))))
        self.assertEqual(m.trace(rho), m.ONE)
        joint = fixture(5)
        direct = m.matrix(((joint[0][0] + joint[1][1],
                            joint[0][2] + joint[1][3]),
                           (joint[2][0] + joint[3][1],
                            joint[2][2] + joint[3][3])))
        self.assertEqual(rho, direct)

    def test_joint_constructor_and_cnot_preparation_agree(self):
        product = m.tensor(PLUS, m.pure_density((1, 0)))
        self.assertEqual(m.apply_isometry(product, m.CNOT), fixture(1))
        self.assertEqual(m.trace(fixture(1)), m.ONE)

    def test_mixed_joint_state_and_phase_averaging(self):
        mixed_path = m.scale(m.identity(2), HALF)
        mixed = m.marked_joint(mixed_path, (1, 0), (1, 0))
        self.assertEqual(m.partial_trace_marker(mixed), mixed_path)
        averaged = m.scale(m.add(fixture(0), fixture(2)), HALF)
        self.assertEqual(averaged, mixed)
        for phase in range(4):
            self.assertEqual(m.full_output_probabilities(
                mixed, m.phase_recombiner(phase)), (HALF, HALF))

    def test_eraser_joint_conditional_and_weighted_marginal(self):
        expected_tables = (
            ((HALF, F(0)), (F(0), HALF)),
            ((F(1, 4), F(1, 4)), (F(1, 4), F(1, 4))),
            ((F(0), HALF), (HALF, F(0))),
            ((F(1, 4), F(1, 4)), (F(1, 4), F(1, 4))),
        )
        for phase, expected in enumerate(expected_tables):
            table = m.joint_output_probabilities(
                fixture(1), m.phase_recombiner(phase), m.ERASER_EFFECTS)
            self.assertEqual(table, expected)
            self.assertEqual(m.marginal_output(table), (HALF, HALF))
            terms = [m.conditional_output(table, outcome) for outcome in range(2)]
            self.assertEqual(tuple(weight for weight, _ in terms), (HALF, HALF))
            recovered = tuple(sum(weight * conditional[out]
                                  for weight, conditional in terms) for out in range(2))
            self.assertEqual(recovered, (HALF, HALF))
            self.assertEqual(terms[0][1], EXPECTED[0][phase])
            self.assertEqual(terms[1][1], EXPECTED[2][phase])

    def test_marker_joint_povm_complex_effect_orientation(self):
        marker = m.pure_density((1, m.I))
        joint = m.tensor(PLUS, marker)
        effects = (marker, m.add(m.identity(2), m.scale(marker, -1)))
        table = m.joint_output_probabilities(joint, m.phase_recombiner(0), effects)
        self.assertEqual(table, ((F(1), F(0)), (F(0), F(0))))

    def test_marker_channels_preserve_full_path_marginal(self):
        channels = ((m.HADAMARD,),
                    (m.ScaledOperator(((0, 1), (1, 0))),),
                    m.DEPHASE_MARKER, m.RESET_MARKER)
        for row in range(6):
            before = fixture(row)
            for channel in channels:
                after = m.marker_channel(before, channel)
                with self.subTest(row=row, channel=channel):
                    self.assertEqual(m.partial_trace_marker(after),
                                     m.partial_trace_marker(before))
                    for phase in range(4):
                        self.assertEqual(m.full_output_probabilities(
                            after, m.phase_recombiner(phase)), EXPECTED[row][phase])

    def test_controlled_inverse_is_not_local_reset(self):
        joint = fixture(1)
        inverted = m.coherent_cnot_inverse(joint)
        reset = m.marker_channel(joint, m.RESET_MARKER)
        self.assertEqual(inverted, m.tensor(PLUS, m.pure_density((1, 0))))
        self.assertEqual(reset, m.tensor(m.scale(m.identity(2), HALF),
                                        m.pure_density((1, 0))))
        self.assertEqual(m.full_output_probabilities(inverted, m.phase_recombiner(0)),
                         (F(1), F(0)))
        self.assertEqual(m.full_output_probabilities(reset, m.phase_recombiner(0)),
                         (HALF, HALF))
        self.assertNotEqual(inverted, reset)

    def test_unbalanced_population_collision(self):
        path = m.matrix(((F(9, 10), F(3, 10)), (F(3, 10), F(1, 10))))
        joint = m.marked_joint(path, (1, 0), (1, 0))
        other = m.partial_trace_marker(fixture(4))
        self.assertNotEqual(path, other)
        self.assertEqual(m.CoherenceReceiver.from_density(path),
                         m.CoherenceReceiver.from_density(other))
        for phase in range(4):
            self.assertEqual(m.full_output_probabilities(
                joint, m.phase_recombiner(phase)), EXPECTED[4][phase])

    def test_all_admitted_phase_continuations_commute(self):
        for row in range(6):
            rho = m.partial_trace_marker(fixture(row))
            receiver = m.CoherenceReceiver.from_density(rho)
            for gate in range(4):
                evolved = m.apply_isometry(rho, m.phase_gate(gate))
                advanced = receiver.advance("phase", gate)
                self.assertEqual(m.CoherenceReceiver.from_density(evolved), advanced)
                for phase in range(4):
                    self.assertEqual(advanced.probabilities(phase),
                                     EXPECTED[row][(gate + phase) % 4])

    def test_hadamard_hostile_continuation_and_explicit_rejection(self):
        left, right = m.pure_density((1, 0)), m.pure_density((0, 1))
        receiver = m.CoherenceReceiver.from_density(left)
        self.assertEqual(receiver, m.CoherenceReceiver.from_density(right))
        with self.assertRaises(m.UnsupportedOperation):
            receiver.advance("hadamard")
        with self.assertRaises(m.UnsupportedOperation):
            receiver.advance("arbitrary_dynamics", 0)
        left_h = m.apply_isometry(left, m.HADAMARD)
        right_h = m.apply_isometry(right, m.HADAMARD)
        self.assertEqual(m.reduced_output_probabilities(left_h, m.phase_recombiner(0)),
                         (F(1), F(0)))
        self.assertEqual(m.reduced_output_probabilities(right_h, m.phase_recombiner(0)),
                         (F(0), F(1)))

    def test_dropped_coherence_mutant_is_rejected(self):
        wrong = tuple((HALF, HALF) for _ in range(4))
        self.assertNotEqual(wrong, EXPECTED[0])
        self.assertNotEqual(wrong, EXPECTED[4])

    def test_magnitude_only_mutant_is_rejected(self):
        wrong = m.CoherenceReceiver(m.Q(HALF))
        self.assertNotEqual(wrong.probabilities(0), EXPECTED[3][0])
        self.assertNotEqual(wrong.probabilities(1), EXPECTED[3][1])

    def test_conjugated_coherence_mutant_is_rejected(self):
        correct = m.CoherenceReceiver.from_density(m.partial_trace_marker(fixture(3)))
        wrong = m.CoherenceReceiver(correct.chi.conjugate())
        self.assertEqual(wrong.probabilities(1), (F(1), F(0)))
        self.assertNotEqual(wrong.probabilities(1), EXPECTED[3][1])

    def test_coherent_marker_sum_mutant_is_rejected(self):
        distinct = (m.Q(HALF), m.Q(HALF))
        correct = sum(amplitude.norm_squared() for amplitude in distinct)
        wrong = sum(distinct, m.ZERO).norm_squared()
        self.assertEqual(correct, HALF)
        self.assertEqual(wrong, 1)
        self.assertNotEqual(wrong, EXPECTED[1][0][0])

    def test_selected_as_marginal_mutant_is_rejected(self):
        table = m.joint_output_probabilities(
            fixture(1), m.phase_recombiner(0), m.ERASER_EFFECTS)
        weight, selected = m.conditional_output(table, 0)
        self.assertEqual(weight, HALF)
        self.assertEqual(selected, (F(1), F(0)))
        self.assertNotEqual(selected, m.marginal_output(table))

    def test_positive_states_include_singular_and_maximum_bound(self):
        for n in range(1, 7):
            state = m.scale(m.identity(n), F(1, n))
            self.assertEqual(m.validate_density(state), state)
        self.assertEqual(m.validate_density(PLUS), PLUS)
        self.assertEqual(m.pure_density((2, 2)), PLUS)
        self.assertEqual(m.CoherenceReceiver(m.Q(HALF)).chi, m.Q(HALF))

    def test_nonpositive_states_rejected_beyond_diagonal_checks(self):
        bad = (
            ((F(3, 2), 0), (0, F(-1, 2))),
            ((HALF, F(3, 5)), (F(3, 5), HALF)),
            ((F(1, 3), F(-1, 5), F(-1, 5)),
             (F(-1, 5), F(1, 3), F(-1, 5)),
             (F(-1, 5), F(-1, 5), F(1, 3))),
        )
        for state in bad:
            with self.assertRaises(m.InvalidState):
                m.validate_density(state)
        with self.assertRaises(m.InvalidState):
            m.CoherenceReceiver(m.Q(F(3, 5)))

    def test_nonhermitian_and_wrong_trace_rejected(self):
        for state in (((HALF, m.I), (m.I, HALF)), ((1, 0), (0, 1))):
            with self.assertRaises(m.InvalidState):
                m.validate_density(state)
        with self.assertRaises(m.InvalidState):
            m.pure_density((0, 0))

    def test_exact_numeric_and_phase_domains(self):
        for bad in (0.5, complex(1, 0), True, "1/2"):
            with self.assertRaises(TypeError):
                m.Q(bad)
            with self.assertRaises(TypeError):
                m.matrix(((bad,),))
        for phase in (-1, 4, HALF, True, None, "0"):
            with self.assertRaises(ValueError):
                m.phase_recombiner(phase)
            with self.assertRaises(ValueError):
                m.CoherenceReceiver(m.ZERO).advance("phase", phase)
        with self.assertRaises(ValueError):
            m.ScaledOperator(((1,),), 0)
        with self.assertRaises(TypeError):
            m.ScaledOperator(((1,),), 2.0)

    def test_empty_oversized_ragged_and_wrong_dimensions(self):
        for rows in ((), ((),), ((1,), (1, 2)), [[0]*7 for _ in range(7)]):
            with self.assertRaises(ValueError):
                m.matrix(rows)
        with self.assertRaises(ValueError):
            m.tensor(m.identity(4), m.identity(2))
        with self.assertRaises(m.InvalidState):
            m.partial_trace_marker(PLUS)
        with self.assertRaises(m.InvalidState):
            m.marked_joint(m.identity(1), (1, 0), (1, 0))
        with self.assertRaises(ValueError):
            m.apply_isometry(PLUS, m.CNOT)
        with self.assertRaises(ValueError):
            m.multiply(m.identity(2), m.identity(3))

    def test_marker_vectors_and_incomplete_isometries_rejected(self):
        for vector in ((1, 1), (1,), (0, 0), (1, 0, 0)):
            with self.assertRaises(m.InvalidState):
                m.marked_joint(PLUS, (1, 0), vector)
        for operator in (m.ScaledOperator(((1, 1), (1, 1))),
                         m.ScaledOperator(m.THREE_OUTPUT.raw[:2])):
            with self.assertRaises(ValueError):
                m.full_output_probabilities(fixture(0), operator)
        with self.assertRaises(ValueError):
            m.apply_isometry(PLUS, m.ScaledOperator(((1, 0), (0, 1)), 2))

    def test_invalid_channels_rejected(self):
        for channel in ((), m.RESET_MARKER[:1],
                        (m.ScaledOperator(((2, 0), (0, 2))),),
                        (m.CNOT,), (m.HADAMARD,)*5):
            with self.assertRaises(ValueError):
                m.marker_channel(fixture(1), channel)

    def test_invalid_and_zero_marker_effects(self):
        for effects in ((), m.ERASER_EFFECTS[:1],
                        (m.matrix(((2, 0), (0, -1))),),
                        (m.identity(1),), (m.identity(2),)*5):
            with self.assertRaises(ValueError):
                m.joint_output_probabilities(fixture(1), m.phase_recombiner(0), effects)
        effects = (m.identity(2), m.matrix(((0, 0), (0, 0))))
        table = m.joint_output_probabilities(fixture(1), m.phase_recombiner(0), effects)
        self.assertEqual(table, ((HALF, F(0)), (HALF, F(0))))
        with self.assertRaises(m.ZeroProbabilityEvent):
            m.conditional_output(table, 1)
        self.assertEqual(m.conditional_output(table, 0), (F(1), (HALF, HALF)))

    def test_malformed_probability_tables_rejected(self):
        for table in ((), ((1,),), ((HALF,), (HALF, 0)),
                      ((F(-1), F(1)), (F(1), F(0))),
                      ((0, 0), (0, 0)), ((0.5,), (0.5,))):
            with self.assertRaises((ValueError, TypeError)):
                m.marginal_output(table)
        for index in (-1, 2, True, HALF):
            with self.assertRaises(ValueError):
                m.conditional_output(((HALF, 0), (HALF, 0)), index)

    def test_gaussian_rational_arithmetic(self):
        z = m.Q(F(3, 5), F(4, 5))
        self.assertEqual(z * z.conjugate(), m.ONE)
        self.assertEqual(z / z, m.ONE)
        self.assertEqual(m.determinant(((0, m.I), (m.I, 0))), m.ONE)
        with self.assertRaises(ZeroDivisionError):
            z / m.ZERO

    def test_reviewer_nonleading_negative_principal_minor(self):
        bad = ((0, 0, 0), (0, HALF, F(3, 5)), (0, F(3, 5), HALF))
        # All leading determinants vanish; the lower-right minor is negative.
        for size in (1, 2, 3):
            self.assertEqual(m.determinant(tuple(row[:size] for row in bad[:size])), m.ZERO)
        self.assertEqual(m.determinant(((HALF, F(3, 5)), (F(3, 5), HALF))), m.Q(F(-11, 100)))
        with self.assertRaises(m.InvalidState):
            m.validate_density(bad)

    def test_reviewer_noncanonical_complex_preparation(self):
        path = m.matrix(((HALF, m.Q(0, -HALF)), (m.Q(0, HALF), HALF)))
        joint = m.marked_joint(path, (F(3, 5), m.Q(0, F(4, 5))), (F(3, 5), F(4, 5)))
        expected_joint = m.scale(m.matrix(((9, -12*m.I, -9*m.I, -12*m.I),
                                           (12*m.I, 16, 12, 16),
                                           (9*m.I, 12, 9, 12),
                                           (12*m.I, 16, 12, 16))), F(1, 50))
        self.assertEqual(joint, expected_joint)
        expected = ((F(41, 50), F(9, 50)), (F(8, 25), F(17, 25)),
                    (F(9, 50), F(41, 50)), (F(17, 25), F(8, 25)))
        for phase, distribution in enumerate(expected):
            operator = m.phase_recombiner(phase)
            self.assertEqual(m.full_output_probabilities(joint, operator), distribution)
            self.assertEqual(independent_full_contraction(joint, operator), distribution)

    def test_reviewer_nonprojective_channel_with_distinct_scales(self):
        channel = (m.ScaledOperator(((1, 0), (0, F(3, 5)))),
                   m.ScaledOperator(((0, 1), (0, 0)), F(25, 16)))
        after = m.marker_channel(fixture(1), channel)
        expected = m.matrix(((HALF, 0, 0, F(3, 10)), (0, 0, 0, 0),
                             (0, 0, F(8, 25), 0), (F(3, 10), 0, 0, F(9, 50))))
        self.assertEqual(after, expected)
        self.assertEqual(m.partial_trace_marker(after), m.scale(m.identity(2), HALF))

    def test_reviewer_complete_three_by_four_povm_table(self):
        joint = m.tensor(m.pure_density((1, 0)), m.scale(m.identity(2), HALF))
        effects = (m.scale(m.identity(2), F(1, 4)),) * 4
        table = m.joint_output_probabilities(joint, m.THREE_OUTPUT, effects)
        expected = ((F(9, 100),) * 4, (F(4, 25),) * 4, (F(0),) * 4)
        self.assertEqual(table, expected)
        marginal = (F(9, 25), F(16, 25), F(0))
        self.assertEqual(m.marginal_output(table), marginal)
        for outcome in range(4):
            self.assertEqual(m.conditional_output(table, outcome), (F(1, 4), marginal))


def run():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", "--receipt", dest="output", type=Path,
                        default=LAB / ".artifacts" / "two-path.json",
                        help="JSON receipt under .artifacts; relative paths use the working directory.")
    args = parser.parse_args()
    receipt_path = args.output.resolve()
    if (receipt_path.suffix.lower() != ".json"
            or not any(parent.name == ".artifacts" for parent in receipt_path.parents)):
        parser.error("Output must be a JSON file under a .artifacts directory.")
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    receipt_path.write_text('{"schema": "two-path-exact-lab-v2", "status": "PENDING"}\n',
                            encoding="utf-8")
    inputs = ("model.py", "test_model.py", "README.md", "TEST_CONTRACT.md")
    before = {name: hashlib.sha256((LAB / name).read_bytes()).hexdigest()
              for name in inputs}
    suite = unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    after = {name: hashlib.sha256((LAB / name).read_bytes()).hexdigest()
             for name in inputs}
    expected_tests = 31
    passed = (result.testsRun == expected_tests and result.wasSuccessful() and not result.skipped
              and not result.expectedFailures and before == after)
    receipt = {
        "schema": "two-path-exact-lab-v2",
        "status": "PASS" if passed else "FAIL",
        "evidence_grade": "fresh_finite_implementation_check",
        "scientific_experiment": False,
        "utc": datetime.now(timezone.utc).isoformat(),
        "python": platform.python_version(),
        "implementation": platform.python_implementation(),
        "tests_run": result.testsRun,
        "expected_tests": expected_tests,
        "failures": [{"test": str(test), "detail": detail} for test, detail in result.failures],
        "errors": [{"test": str(test), "detail": detail} for test, detail in result.errors],
        "skipped": [{"test": str(test), "reason": reason} for test, reason in result.skipped],
        "unexpected_successes": [str(test) for test in result.unexpectedSuccesses],
        "expected_failures": [{"test": str(test), "detail": detail}
                              for test, detail in result.expectedFailures],
        "frozen_phase_output_entries": 48,
        "three_output_probability_entries": 9,
        "input_sha256_before": before,
        "input_sha256_after": after,
        "input_hashes_match_before_after": before == after,
        "contract": "TEST_CONTRACT.md",
    }
    receipt_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print("Receipt:", receipt_path.name)
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(run())
