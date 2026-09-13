"""Independent aggregation of supplied E34 CM orbit rows modulo 125.

Reads raw rho and term rows only; no PASS field is a mathematical premise.
Uses integer Kronecker packing, independently of trace125.py's convolution.
Orbit identification remains a dependency of the construction and its audit.
"""

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

MODULUS = 125
DEGREE = 16
PACK_BITS = 18
PACK_MASK = (1 << PACK_BITS)-1
ZERO = (0,)*DEGREE
ONE = (1,)+(0,)*(DEGREE-1)


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def admit_vector(value):
    require(isinstance(value, list) and len(value) == DEGREE,
            "Expected exactly sixteen stored coefficients")
    require(all(type(c) is int and 0 <= c < MODULUS for c in value),
            "Stored coefficients must be canonical integers modulo 125")
    return tuple(value)


def add(a, b):
    return tuple((x+y) % MODULUS for x, y in zip(a, b))


def scale(a, n):
    return tuple(n*x % MODULUS for x in a)


def sub(a, b):
    return add(a, scale(b, -1))


def packed_multiply(a, b):
    """Each convolution coefficient is <=16*124^2<2^18, so no packed carry.

    Multiplying the packed integers computes every raw coefficient exactly.
    Reduction by z^16=2 then folds coefficient j+16 into coefficient j.
    """
    packed_a = sum(c << (PACK_BITS*j) for j, c in enumerate(a))
    packed_b = sum(c << (PACK_BITS*j) for j, c in enumerate(b))
    product = packed_a*packed_b
    result = []
    for j in range(DEGREE):
        lower = (product >> (PACK_BITS*j)) & PACK_MASK
        upper = (product >> (PACK_BITS*(j+DEGREE))) & PACK_MASK
        result.append((lower+2*upper) % MODULUS)
    return tuple(result)


def power(a, exponent):
    require(type(exponent) is int and exponent >= 0, "Nonnegative exponent required")
    result = ONE
    while exponent:
        if exponent & 1:
            result = packed_multiply(result, a)
        exponent //= 2
        if exponent:
            a = packed_multiply(a, a)
    return result


def h(rho):
    return add(scale(power(rho, 5), 2), scale(rho, 289))


def total(values):
    result = ZERO
    for item in values:
        result = add(result, item)
    return result


def first_five_coefficients(roots):
    # Product of (X-rho), retaining the five terms below the leading monomial.
    coefficients = [ONE]+[ZERO]*5
    for count, rho in enumerate(roots, 1):
        for k in range(min(count, 5), 0, -1):
            coefficients[k] = sub(coefficients[k], packed_multiply(rho, coefficients[k-1]))
    return coefficients[1:]


def newton_sums(coefficients):
    sums = [ZERO]
    for k in range(1, 6):
        mixed = scale(coefficients[k-1], k)
        for j in range(1, k):
            mixed = add(mixed, packed_multiply(coefficients[j-1], sums[k-j]))
        sums.append(scale(mixed, -1))
    return sums[1:]


def expanded_trace(coefficients):
    a, b, c, d, e = coefficients
    terms = (
        scale(power(a, 5), -2),
        scale(packed_multiply(power(a, 3), b), 10),
        scale(packed_multiply(power(a, 2), c), -10),
        scale(packed_multiply(a, power(b, 2)), -10),
        scale(packed_multiply(a, d), 10),
        scale(packed_multiply(b, c), 10),
        scale(e, -10),
        scale(a, -289),
    )
    return total(terms)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path,
                        default=Path(__file__).resolve().parents[1]/"evidence"/"trace125.json")
    parser.add_argument("--output", type=Path,
                        default=Path(__file__).resolve().parents[1]/"evidence"/"trace_readback.json")
    args = parser.parse_args()
    source_bytes = args.input.read_bytes()
    data = json.loads(source_bytes)
    require(data.get("modulus") == MODULUS, "Input modulus is not 125")
    require(data.get("curve") == "Y^2=X^3-1156X", "Input names a different curve")
    rows = data.get("orbit_terms")
    require(isinstance(rows, list) and len(rows) == 512, "Expected all 512 supplied rows")
    require(DEGREE*(MODULUS-1)**2 < (1 << PACK_BITS), "Packing radix is too small")
    z = (0, 1)+(0,)*(DEGREE-2)
    require(power(z, 16) == scale(ONE, 2), "Ring relation failed")
    require(power(z, 17) == scale(z, 2), "Folded ring relation failed")
    require(packed_multiply(ONE, (124,)*16) == (124,)*16, "Multiplicative identity failed")

    roots, terms, labels = [], [], []
    for index, row in enumerate(rows):
        require(isinstance(row, dict), "Malformed orbit row")
        rho, term = admit_vector(row.get("rho")), admit_vector(row.get("term"))
        require(h(rho) == term, f"Stored term disagrees with independent h(rho), row {index}")
        roots.append(rho)
        terms.append(term)
        action = row.get("gaussian_action")
        require(isinstance(action, list) and len(action) == 2 and
                all(type(c) is int for c in action), "Malformed action label")
        labels.append(tuple(action))
    require(len(set(labels)) == 512, "An action label is repeated")
    multiplicities = Counter(roots)
    require(len(multiplicities) == 256 and set(multiplicities.values()) == {2},
            "The supplied rho fibers are not exactly 256 pairs")
    distinct = sorted(multiplicities)
    full_sum = total(terms)
    halved = scale(full_sum, 63)  # 2^-1 modulo 125, not integer division of residues.
    distinct_sum = total(h(rho) for rho in distinct)
    require(halved == distinct_sum, "Multiplicity correction disagrees with distinct sum")

    coefficients = first_five_coefficients(distinct)
    sums = newton_sums(coefficients)
    direct_powers = [total(power(rho, k) for rho in distinct) for k in range(1, 6)]
    require(sums == direct_powers, "Newton sums disagree with direct power sums")
    newton_trace = add(scale(sums[4], 2), scale(sums[0], 289))
    expanded = expanded_trace(coefficients)
    require(newton_trace == expanded == distinct_sum, "Independent trace routes disagree")
    for k in range(1, 5):
        changed = list(coefficients)
        changed[k] = add(changed[k], scale(z, 25))
        require(expanded_trace(changed) == expanded, "Mixed precision modulo 25 failed")

    wrong_cover = distinct + [scale(rho, -1) for rho in distinct]
    wrong_sum = total(h(rho) for rho in wrong_cover)
    require(wrong_sum == ZERO, "Enlarged signed cover did not cancel")
    require(distinct_sum != wrong_sum, "Wrong-cover control failed to distinguish this trace")
    require(not any(distinct_sum[1:]), "Trace has nonconstant extension-ring coefficients")
    residue = distinct_sum[0]
    valuation_two = residue % 25 == 0 and residue % 125 != 0
    require(valuation_two, "Computed trace does not have the requested residue valuation")
    claimed = admit_vector(data.get("trace_unit_multiple"))
    require(distinct_sum == claimed, "Recomputed trace disagrees with saved trace field")

    result = {
        "status": "PASS_INDEPENDENT_AGGREGATION",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "input_path": str(args.input.resolve()),
        "input_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "ring": {"modulus": MODULUS, "degree": DEGREE, "relation": "z^16=2",
                 "multiplication": "integer Kronecker packing with 18-bit digits",
                 "no_carry_maximum": DEGREE*(MODULUS-1)**2},
        "rows_recomputed": len(rows), "distinct_action_labels": len(set(labels)),
        "distinct_rho_values": len(distinct), "rho_occurrence_multiplicity": 2,
        "full_512_term_sum": full_sum, "full_sum_times_inverse_2": halved,
        "distinct_256_term_sum": distinct_sum,
        "polynomial_degree": len(distinct),
        "first_five_monic_polynomial_coefficients": coefficients,
        "coefficients_are_base_ring": all(not any(c[1:]) for c in coefficients),
        "first_five_newton_sums": sums,
        "direct_power_sums": direct_powers,
        "newton_trace": newton_trace, "expanded_newton_trace": expanded,
        "trace_residue_unit_multiple": residue,
        "residue_implies_v5_exactly_2_given_integral_orbit": valuation_two,
        "saved_trace_field_agrees": True,
        "wrong_enlarged_signed_cover": {"occurrences": len(wrong_cover),
                                       "distinct_values": len(set(wrong_cover)),
                                       "trace": wrong_sum,
                                       "disposition": "REJECTED: enlarging by opposite rho changes the trace"},
        "independence": "No imports from trace125.py or cm_action.py; no status or PASS field used as an arithmetic premise",
        "evidence_ceiling": "Independent aggregation of supplied rho rows; primitive orbit identity, field admission, unit comparison and Sha theorem hypotheses remain dependencies of the construction and mathematical audit",
        "actual_distinguished_real_period_trace_fixed": False,
        "full_complex_BSD_identity": "NOT_PROVED_BY_THIS_READBACK",
    }
    args.output.write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "rows": len(rows),
                      "distinct_roots": len(distinct), "trace_unit_multiple_mod125": residue,
                      "first_five_coefficients_if_scalar": [c[0] if not any(c[1:]) else list(c) for c in coefficients],
                      "output": str(args.output)}, indent=2))


if __name__ == "__main__":
    main()
