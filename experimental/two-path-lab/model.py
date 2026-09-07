"""Bounded exact two-path algebra. No floating point, simulation, or I/O."""

from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations

MAX_DIM = 6
MAX_MARKER_OUTCOMES = 4


class InvalidState(ValueError):
    pass


class UnsupportedOperation(ValueError):
    pass


class ZeroProbabilityEvent(ValueError):
    pass


def rational(value):
    if type(value) not in (int, Fraction):
        raise TypeError("Exact integers or fractions required; no bool/float/complex.")
    return Fraction(value)


@dataclass(frozen=True)
class Q:
    """A Gaussian rational, conjugate-linear in the bra convention."""

    real: Fraction = Fraction(0)
    imag: Fraction = Fraction(0)

    def __post_init__(self):
        object.__setattr__(self, "real", rational(self.real))
        object.__setattr__(self, "imag", rational(self.imag))

    def __add__(self, other):
        other = q(other)
        return Q(self.real + other.real, self.imag + other.imag)

    __radd__ = __add__

    def __neg__(self):
        return Q(-self.real, -self.imag)

    def __sub__(self, other):
        return self + (-q(other))

    def __rsub__(self, other):
        return q(other) - self

    def __mul__(self, other):
        other = q(other)
        return Q(self.real * other.real - self.imag * other.imag,
                 self.real * other.imag + self.imag * other.real)

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = q(other)
        norm = other.norm_squared()
        if not norm:
            raise ZeroDivisionError("Zero Gaussian rational.")
        numerator = self * other.conjugate()
        return Q(numerator.real / norm, numerator.imag / norm)

    def conjugate(self):
        return Q(self.real, -self.imag)

    def norm_squared(self):
        return self.real * self.real + self.imag * self.imag


def q(value):
    return value if isinstance(value, Q) else Q(rational(value))


ZERO, ONE, I = Q(), Q(1), Q(0, 1)
PHASES = (ONE, I, -ONE, -I)


def matrix(rows):
    result = tuple(tuple(q(x) for x in row) for row in rows)
    if not result or not result[0]:
        raise ValueError("A matrix must be nonempty.")
    width = len(result[0])
    if len(result) > MAX_DIM or width > MAX_DIM:
        raise ValueError("Matrix axis exceeds the documented bound of six.")
    if any(len(row) != width for row in result):
        raise ValueError("Ragged matrix.")
    return result


def identity(n):
    if type(n) is not int or not 1 <= n <= MAX_DIM:
        raise ValueError("Invalid identity dimension.")
    return matrix([[int(i == j) for j in range(n)] for i in range(n)])


def dagger(a):
    a = matrix(a)
    return matrix([[a[j][i].conjugate() for j in range(len(a))]
                   for i in range(len(a[0]))])


def multiply(a, b):
    a, b = matrix(a), matrix(b)
    if len(a[0]) != len(b):
        raise ValueError("Matrix dimensions do not compose.")
    return matrix([[sum((a[i][k] * b[k][j] for k in range(len(b))), ZERO)
                    for j in range(len(b[0]))] for i in range(len(a))])


def scale(a, scalar):
    a, scalar = matrix(a), q(scalar)
    return matrix([[x * scalar for x in row] for row in a])


def add(a, b):
    a, b = matrix(a), matrix(b)
    if (len(a), len(a[0])) != (len(b), len(b[0])):
        raise ValueError("Matrix shapes differ.")
    return matrix([[x + y for x, y in zip(ar, br)] for ar, br in zip(a, b)])


def tensor(a, b):
    a, b = matrix(a), matrix(b)
    return matrix([[x * y for x in ar for y in br] for ar in a for br in b])


def trace(a):
    a = matrix(a)
    if len(a) != len(a[0]):
        raise ValueError("Trace requires a square matrix.")
    return sum((a[i][i] for i in range(len(a))), ZERO)


def determinant(a):
    a = matrix(a)
    if len(a) != len(a[0]):
        raise ValueError("Determinant requires a square matrix.")
    work, result = [list(row) for row in a], ONE
    for k in range(len(a)):
        pivot = next((i for i in range(k, len(a)) if work[i][k] != ZERO), None)
        if pivot is None:
            return ZERO
        if pivot != k:
            work[k], work[pivot] = work[pivot], work[k]
            result = -result
        lead = work[k][k]
        result *= lead
        for i in range(k + 1, len(a)):
            factor = work[i][k] / lead
            for j in range(k + 1, len(a)):
                work[i][j] -= factor * work[k][j]
            work[i][k] = ZERO
    return result


def validate_positive(a):
    """For Hermitian matrices, all principal minors >= 0 iff PSD."""
    a = matrix(a)
    if len(a) != len(a[0]) or a != dagger(a):
        raise InvalidState("A positive operator must be square and Hermitian.")
    for size in range(1, len(a) + 1):
        for indices in combinations(range(len(a)), size):
            minor = matrix([[a[i][j] for j in indices] for i in indices])
            value = determinant(minor)
            if value.imag or value.real < 0:
                raise InvalidState("Negative principal minor: operator is not PSD.")
    return a


def validate_density(state, dimension=None):
    state = validate_positive(state)
    if dimension is not None and len(state) != dimension:
        raise InvalidState("Wrong state dimension for this operation.")
    if trace(state) != ONE:
        raise InvalidState("Density operator must have exact trace one.")
    return state


def pure_density(vector):
    """Normalize a nonzero rational vector exactly at the density level."""
    vector = tuple(q(x) for x in vector)
    if not 1 <= len(vector) <= MAX_DIM:
        raise ValueError("Vector length outside bound.")
    norm = sum((x.norm_squared() for x in vector), Fraction(0))
    if not norm:
        raise InvalidState("Cannot normalize a zero vector.")
    return matrix([[x * y.conjugate() / norm for y in vector] for x in vector])


def marked_joint(path_state, marker_zero, marker_one):
    """Apply the isometry |i> -> |i>|d_i> to a supplied path density."""
    path_state = validate_density(path_state, 2)
    markers = tuple(tuple(q(x) for x in vector)
                    for vector in (marker_zero, marker_one))
    if any(len(v) != 2 or sum((x.norm_squared() for x in v), Fraction(0)) != 1
           for v in markers):
        raise InvalidState("Marker vectors must be normalized qubit vectors.")
    result = matrix([[path_state[i][j] * markers[i][mu] *
                      markers[j][nu].conjugate()
                      for j in range(2) for nu in range(2)]
                     for i in range(2) for mu in range(2)])
    return validate_density(result, 4)


def partial_trace_marker(joint):
    joint = validate_density(joint, 4)
    return matrix([[sum((joint[2*i+mu][2*j+mu] for mu in range(2)), ZERO)
                    for j in range(2)] for i in range(2)])


@dataclass(frozen=True)
class ScaledOperator:
    """Physical matrix raw/sqrt(denominator_squared); no root is evaluated."""

    raw: tuple
    denominator_squared: Fraction = Fraction(1)

    def __post_init__(self):
        object.__setattr__(self, "raw", matrix(self.raw))
        denominator = rational(self.denominator_squared)
        if denominator <= 0:
            raise ValueError("Squared denominator must be positive.")
        object.__setattr__(self, "denominator_squared", denominator)


def validate_isometry(operator, input_dimension=None):
    if not isinstance(operator, ScaledOperator):
        raise TypeError("A ScaledOperator is required.")
    a, d = operator.raw, operator.denominator_squared
    if input_dimension is not None and len(a[0]) != input_dimension:
        raise ValueError("Wrong isometry input dimension.")
    if multiply(dagger(a), a) != scale(identity(len(a[0])), d):
        raise ValueError("Operator is not a complete isometry.")
    return operator


def apply_isometry(state, operator):
    state = validate_density(state)
    validate_isometry(operator, len(state))
    return scale(multiply(multiply(operator.raw, state), dagger(operator.raw)),
                 Fraction(1, 1) / operator.denominator_squared)


def quarter_phase(index):
    if type(index) is not int or not 0 <= index < 4:
        raise ValueError("Phase index must be an integer in 0..3.")
    return PHASES[index]


def phase_gate(index):
    return ScaledOperator(((1, 0), (0, quarter_phase(index))))


def phase_recombiner(index):
    z = quarter_phase(index)
    return ScaledOperator(((1, z), (1, -z)), 2)


HADAMARD = ScaledOperator(((1, 1), (1, -1)), 2)
CNOT = ScaledOperator(((1, 0, 0, 0), (0, 1, 0, 0),
                       (0, 0, 0, 1), (0, 0, 1, 0)))
THREE_OUTPUT = ScaledOperator(((Fraction(3, 5), Fraction(-12, 25)),
                               (Fraction(4, 5), Fraction(9, 25)),
                               (0, Fraction(4, 5))))
RESET_MARKER = (ScaledOperator(((1, 0), (0, 0))),
                ScaledOperator(((0, 1), (0, 0))))
DEPHASE_MARKER = (ScaledOperator(((1, 0), (0, 0))),
                  ScaledOperator(((0, 0), (0, 1))))
ERASER_EFFECTS = (matrix(((Fraction(1, 2), Fraction(1, 2)),
                          (Fraction(1, 2), Fraction(1, 2)))),
                  matrix(((Fraction(1, 2), Fraction(-1, 2)),
                          (Fraction(-1, 2), Fraction(1, 2)))))


def _output_joint(joint, path_operator):
    joint = validate_density(joint, 4)
    validate_isometry(path_operator, 2)
    if len(path_operator.raw) not in (2, 3):
        raise ValueError("Only two or three path outputs are admitted.")
    lifted = ScaledOperator(tensor(path_operator.raw, identity(2)),
                            path_operator.denominator_squared)
    return apply_isometry(joint, lifted)


def _probability(value):
    value = q(value)
    if value.imag or not 0 <= value.real <= 1:
        raise InvalidState("Not an exact probability.")
    return value.real


def full_output_probabilities(joint, path_operator):
    """Reference route: evolve the full joint matrix, then sum its diagonal."""
    output = _output_joint(joint, path_operator)
    return tuple(_probability(output[2*j][2*j] + output[2*j+1][2*j+1])
                 for j in range(len(path_operator.raw)))


def reduced_output_probabilities(path_state, path_operator):
    path_state = validate_density(path_state, 2)
    if len(path_operator.raw) not in (2, 3):
        raise ValueError("Only two or three path outputs are admitted.")
    output = apply_isometry(path_state, path_operator)
    return tuple(_probability(output[j][j]) for j in range(len(output)))


def marker_channel(joint, kraus):
    joint = validate_density(joint, 4)
    kraus = tuple(kraus)
    if not 1 <= len(kraus) <= 4:
        raise ValueError("A qubit channel needs one to four supplied Kraus terms.")
    completeness = matrix(((0, 0), (0, 0)))
    result = matrix([[0]*4 for _ in range(4)])
    for operator in kraus:
        if not isinstance(operator, ScaledOperator) or (
                len(operator.raw), len(operator.raw[0])) != (2, 2):
            raise ValueError("Marker Kraus terms must be qubit operators.")
        weight = Fraction(1, 1) / operator.denominator_squared
        completeness = add(completeness,
                           scale(multiply(dagger(operator.raw), operator.raw), weight))
        lifted = tensor(identity(2), operator.raw)
        result = add(result, scale(multiply(multiply(lifted, joint), dagger(lifted)),
                                   weight))
    if completeness != identity(2):
        raise ValueError("Marker channel is not trace preserving.")
    return validate_density(result, 4)


def coherent_cnot_inverse(joint):
    """CNOT is its own inverse; restoration assumes CNOT produced the marking."""
    return apply_isometry(validate_density(joint, 4), CNOT)


def joint_output_probabilities(joint, path_operator, marker_effects):
    effects = tuple(validate_positive(effect) for effect in marker_effects)
    if not 1 <= len(effects) <= MAX_MARKER_OUTCOMES:
        raise ValueError("One to four complete marker effects are required.")
    complete = matrix(((0, 0), (0, 0)))
    for effect in effects:
        if len(effect) != 2:
            raise ValueError("Marker effects must be two-dimensional.")
        complete = add(complete, effect)
    if complete != identity(2):
        raise ValueError("Marker effects are not complete.")
    output = _output_joint(joint, path_operator)
    result = []
    for j in range(len(path_operator.raw)):
        block = matrix([[output[2*j+mu][2*j+nu] for nu in range(2)]
                        for mu in range(2)])
        result.append(tuple(_probability(trace(multiply(effect, block)))
                            for effect in effects))
    return tuple(result)


def _probability_table(table):
    table = tuple(tuple(rational(x) for x in row) for row in table)
    if not 2 <= len(table) <= 3 or not table[0] or len(table[0]) > 4:
        raise ValueError("Invalid output/marker probability table shape.")
    if any(len(row) != len(table[0]) for row in table):
        raise ValueError("Ragged probability table.")
    if any(x < 0 for row in table for x in row):
        raise ValueError("Negative probability.")
    if sum((sum(row) for row in table), Fraction(0)) != 1:
        raise ValueError("Joint probabilities must sum to one.")
    return table


def marginal_output(table):
    return tuple(sum(row) for row in _probability_table(table))


def conditional_output(table, marker_index):
    table = _probability_table(table)
    if type(marker_index) is not int or not 0 <= marker_index < len(table[0]):
        raise ValueError("Invalid marker outcome index.")
    weight = sum(row[marker_index] for row in table)
    if not weight:
        raise ZeroProbabilityEvent("Cannot condition on probability zero.")
    return weight, tuple(row[marker_index] / weight for row in table)


@dataclass(frozen=True)
class CoherenceReceiver:
    chi: Q

    def __post_init__(self):
        value = q(self.chi)
        if value.norm_squared() > Fraction(1, 4):
            raise InvalidState("Coherence lies outside the admitted disk.")
        object.__setattr__(self, "chi", value)

    @classmethod
    def from_density(cls, state):
        state = validate_density(state, 2)
        return cls(state[1][0])

    def probabilities(self, phase_index):
        plus = Fraction(1, 2) + (quarter_phase(phase_index) * self.chi).real
        return plus, 1 - plus

    def advance(self, operation, phase_index=None):
        if operation != "phase":
            raise UnsupportedOperation("chi-only receiver supports phase gates only.")
        return CoherenceReceiver(quarter_phase(phase_index) * self.chi)
