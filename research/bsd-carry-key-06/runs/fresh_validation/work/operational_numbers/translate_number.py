#!/usr/bin/env python3
"""Emit concurrent, typed operational readings for a decimal digit string."""

from __future__ import annotations

import argparse
import json
import math
import re
from collections import Counter
from pathlib import Path
from typing import Any

from carrier_lexer import classify


LANES = {
    "EXACT_ARITHMETIC",
    "EXACT_DECLARED_MAP",
    "DERIVED_DEPENDENT",
    "RPRM_READING",
    "OPEN_HYPOTHESIS",
    "SCOUT_PROPOSAL",
}

P = {0: 5, 1: 9, 2: 8, 3: 3, 4: 6, 5: 0, 6: 4, 7: 7, 8: 2, 9: 1}
N = {d: (-d) % 10 for d in range(10)}
T = {d: P[N[d]] for d in range(10)}
M = {d: 9 - d for d in range(10)}
MAPS = {"P": P, "N": N, "T": T, "M": M}
PAIR_ORBITS = [[0, 5], [1, 9], [2, 8], [3, 7], [4, 6]]

PI_WINDOW = "31415926535"
PI_P = "39690184030"
PI_N = "79695184575"
FOUR_MINUS_PI_PREFIX = "08584073464"


def record(lane: str, operation: str, value: Any, **extra: Any) -> dict[str, Any]:
    if lane not in LANES:
        raise ValueError(f"unknown evidence lane: {lane}")
    item = {"lane": lane, "operation": operation, "value": value}
    item.update(extra)
    return item


def apply_map(digits: str, mapping: dict[int, int]) -> str:
    return "".join(str(mapping[int(digit)]) for digit in digits)


def positive_divisors(value: int) -> list[int]:
    if value <= 0:
        return []
    low: list[int] = []
    high: list[int] = []
    for divisor in range(1, math.isqrt(value) + 1):
        if value % divisor == 0:
            low.append(divisor)
            partner = value // divisor
            if partner != divisor:
                high.append(partner)
    return low + list(reversed(high))


def factor_pairs(value: int) -> list[list[int]]:
    if value <= 0:
        return []
    return [[divisor, value // divisor] for divisor in positive_divisors(value)]


def prime_factorization(value: int) -> list[int]:
    if value < 2:
        return []
    factors: list[int] = []
    remaining = value
    divisor = 2
    while divisor * divisor <= remaining:
        while remaining % divisor == 0:
            factors.append(divisor)
            remaining //= divisor
        divisor = 3 if divisor == 2 else divisor + 2
    if remaining > 1:
        factors.append(remaining)
    return factors


def digit_facts(digit: int, readings: dict[str, Any]) -> dict[str, Any]:
    fixed_by = [name for name, mapping in MAPS.items() if mapping[digit] == digit]
    facts = [
        record("EXACT_ARITHMETIC", "parity", "even" if digit % 2 == 0 else "odd"),
        record("EXACT_ARITHMETIC", "binary", format(digit, "b")),
        record("EXACT_ARITHMETIC", "positive_divisors", positive_divisors(digit)),
        record("EXACT_ARITHMETIC", "ordered_factor_pairs", factor_pairs(digit)),
        record("EXACT_ARITHMETIC", "prime_factorization", prime_factorization(digit)),
        record("EXACT_DECLARED_MAP", "P_image", P[digit]),
        record("EXACT_DECLARED_MAP", "N_image", N[digit]),
        record("EXACT_DECLARED_MAP", "T_image", T[digit]),
        record("EXACT_DECLARED_MAP", "M_image", M[digit]),
        record("EXACT_DECLARED_MAP", "fixed_by", fixed_by),
    ]
    if digit == 3:
        facts.append(record("EXACT_ARITHMETIC", "square", 9, expression="3^2"))
    if digit == 6:
        facts.append(record("EXACT_ARITHMETIC", "target_corner_identity", 6, expression="2+4"))
    if digit == 8:
        facts.extend(
            [
                record("EXACT_ARITHMETIC", "power_of_two", True, expression="2^3=8"),
                record("EXACT_ARITHMETIC", "paired_four_sum", 8, expression="4+4"),
            ]
        )
    if digit == 9:
        facts.append(record("EXACT_ARITHMETIC", "decimal_residue", -1, expression="9 == -1 (mod 10)"))
    return {
        "digit": digit,
        "facts": facts,
        "readings": readings["digits"].get(str(digit), []),
    }


def sequence_matches(digits: str, readings: dict[str, Any]) -> list[dict[str, Any]]:
    matches: list[dict[str, Any]] = []
    for entry in readings["sequences"]:
        pattern = entry["pattern"]
        positions = [match.start() for match in re.finditer(f"(?={re.escape(pattern)})", digits)]
        if positions or digits == pattern:
            match = dict(entry)
            match["positions"] = positions or [0]
            matches.append(match)
    return matches


def pair_word(pair: tuple[int, int]) -> str:
    return f"{pair[0]}{pair[1]}"


def signed_pair_receivers(digits: str) -> list[dict[str, Any]]:
    """Type every adjacent decimal pair before applying any gap filter.

    ``signed_gap`` is the ordered difference ``B-A``. It is deliberately not
    named ``g`` because the active number-closure source uses ``g`` for gcd.
    """
    receivers: list[dict[str, Any]] = []
    for index in range(len(digits) - 1):
        left = int(digits[index])
        right = int(digits[index + 1])
        source = (left, right)
        swap = (right, left)
        m_oriented = (M[left], M[right])
        fold = (m_oriented[1], m_oriented[0])
        signed_gap = right - left
        centered_sum = left + right - 9

        states = [
            ("I", source),
            ("O", swap),
            ("M", m_oriented),
            ("F=O_after_M", fold),
        ]
        complete_orbit = [
            {
                "operation": operation,
                "word": pair_word(pair),
                "pair": list(pair),
                "signed_gap": pair[1] - pair[0],
                "centered_sum": pair[0] + pair[1] - 9,
            }
            for operation, pair in states
        ]
        distinct_state_count = len({pair for _, pair in states})

        gap_fiber = [
            (fiber_left, fiber_right)
            for fiber_left in range(10)
            for fiber_right in range(10)
            if fiber_right - fiber_left == signed_gap
        ]
        gap_fiber_count = len(gap_fiber)
        gap_disposition = "ONE" if gap_fiber_count == 1 else "MANY"

        total = centered_sum + 9
        recovered = ((total - signed_gap) // 2, (total + signed_gap) // 2)
        source_word = pair_word(source)
        receivers.append(
            {
                "lane": "EXACT_DECLARED_MAP",
                "coordinate_lane": "EXACT_ARITHMETIC",
                "source_relation": "DERIVED_DEPENDENT",
                "independence": "ONE_DEPENDENT",
                "carrier": "base-10 ordered adjacent digit pair",
                "position": index,
                "source": source_word,
                "pair": list(source),
                "signed_gap_definition": "B-A",
                "signed_gap": signed_gap,
                "centered_sum_definition": "A+B-9",
                "centered_sum": centered_sum,
                "words": {
                    "source_I": source_word,
                    "swap_O": pair_word(swap),
                    "coordinatewise_M": pair_word(m_oriented),
                    "fold_O_after_M": pair_word(fold),
                },
                "complete_orbit": complete_orbit,
                "distinct_state_count": distinct_state_count,
                "signed_gap_fiber": {
                    "lane": "EXACT_ARITHMETIC",
                    "source_relation": "DERIVED_DEPENDENT",
                    "signed_gap": signed_gap,
                    "words": [pair_word(pair) for pair in gap_fiber],
                    "count": gap_fiber_count,
                    "disposition": gap_disposition,
                    "typed_disposition": (
                        f"ONE({pair_word(gap_fiber[0])})"
                        if gap_disposition == "ONE"
                        else f"MANY({gap_fiber_count})"
                    ),
                },
                "combined_coordinate_recovery": {
                    "lane": "EXACT_ARITHMETIC",
                    "source_relation": "DERIVED_DEPENDENT",
                    "coordinates": {
                        "centered_sum": centered_sum,
                        "signed_gap": signed_gap,
                    },
                    "formula": "A=(centered_sum+9-signed_gap)/2; B=(centered_sum+9+signed_gap)/2",
                    "pair": list(recovered),
                    "word": pair_word(recovered),
                    "count": 1,
                    "disposition": "ONE",
                    "typed_disposition": f"ONE({pair_word(recovered)})",
                },
                "terminology_boundary": "signed_gap is B-A; it is not gcd",
            }
        )
    return receivers


def gap_two_receivers(digits: str) -> list[dict[str, Any]]:
    """Type ascending adjacent gap-two pairs into the decimal tower carrier."""
    receivers: list[dict[str, Any]] = []
    for index in range(len(digits) - 1):
        left = int(digits[index])
        right = int(digits[index + 1])
        if right - left != 2:
            continue
        m_oriented = [M[left], M[right]]
        fold = list(reversed(m_oriented))
        receivers.append(
            {
                "lane": "EXACT_DECLARED_MAP",
                "carrier": "decimal ascending gap-two tower",
                "position": index,
                "pair": [left, right],
                "M_oriented": m_oriented,
                "fold_O_after_M": fold,
                "chart_visible": 2 * left + 3 <= 9,
                "digit_sum": left + right,
                "carry": (left + right) // 10,
                "remainder": (left + right) % 10,
                "mirror_swap_equals_numeric_plus_11": fold == [left + 1, right + 1],
            }
        )
    return receivers


def pi_profile(digits: str) -> dict[str, Any]:
    is_window = digits == PI_WINDOW
    profile: dict[str, Any] = {
        "declared_profile": "pi-window",
        "matches_canonical_eleven_digit_window": is_window,
        "claim_ceiling": "All shadows are computed from the supplied window; none is an independent anti-Pi observation.",
    }
    if is_window:
        profile["shadows"] = [
            record("DERIVED_DEPENDENT", "P(pi_window)", apply_map(digits, P), expected=PI_P),
            record("DERIVED_DEPENDENT", "N(pi_window)", apply_map(digits, N), expected=PI_N),
            record(
                "DERIVED_DEPENDENT",
                "4_minus_pi_prefix",
                FOUR_MINUS_PI_PREFIX,
                display="0.8584073464...",
                note="Pinned arithmetic-complement prefix; still computed from pi.",
            ),
        ]
    return profile


def scout_proposals(
    digits: str,
    digit_reports: list[dict[str, Any]],
    matches: list[dict[str, Any]],
    signed_pairs: list[dict[str, Any]],
    gap_two: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Generate a bounded deterministic proposal set from explicit receipts."""
    proposals: list[dict[str, Any]] = []
    unique_digits = sorted({int(digit) for digit in digits})
    if any(item["source"] == "64" for item in signed_pairs):
        proposals.append(
            record(
                "SCOUT_PROPOSAL",
                "signed_64_anti_mirror_probe",
                "This ordered 64 may be the declared M anti-mirror of 35; retain centered_sum +1, signed_gap -2, and M lineage before selecting it from the eight-member negative-gap fiber. It is not an independent anti-Pi source.",
                receipts=["M(64)=35", "signed_gap(64)=-2", "centered_sum(64)=+1", "signed-gap -2 fiber is MANY(8)"],
                authority="NONE",
            )
        )
    if 8 in unique_digits:
        proposals.append(
            record(
                "SCOUT_PROPOSAL",
                "paired_four_probe",
                "This 8 may be acting like two fours with a shadowed half; test a named fold rather than assuming it.",
                receipts=["4+4=8", "2^3=8", "P(2)=8"],
                authority="NONE",
            )
        )
    if 6 in unique_digits:
        proposals.append(
            record(
                "SCOUT_PROPOSAL",
                "computed_six_probe",
                "This 6 may be wearing a computed-corner role; compare literal-source and 2+4 lineages.",
                receipts=["2+4=6", "2*3=6", "P(4)=6"],
                authority="NONE",
            )
        )
    if 3 in unique_digits:
        proposals.append(
            record(
                "SCOUT_PROPOSAL",
                "three_nine_probe",
                "Let the 3 point toward a possible 9-coordinate, then ask which operation carries the arrow.",
                receipts=["3^2=9", "N(3)=7", "P(3)=3"],
                authority="NONE",
            )
        )
    if any(match["id"] == "nine_one_carry_brink" for match in matches):
        proposals.append(
            record(
                "SCOUT_PROPOSAL",
                "carry_brink_probe",
                "Treat 9|1 as a possible seam and compare the sequence before and after a declared +1 carry.",
                receipts=["9+1=10", "adjacent pattern 91 observed"],
                authority="NONE",
            )
        )
    if any(item["pair"] == [3, 5] for item in gap_two):
        proposals.append(
            record(
                "SCOUT_PROPOSAL",
                "m_fold_35_probe",
                "This 35 occupies the last chart-admitted gap-two rung: compare its M-oriented image 64 with its ascending fold 46, keeping the two orientations distinct.",
                receipts=["M(35)=64", "O(M(35))=46", "35 is the unique tower rung where mirror-swap equals numeric +11"],
                authority="NONE",
            )
        )
    if digits == "1234679":
        proposals.append(
            record(
                "SCOUT_PROPOSAL",
                "p_orbit_vacancy_probe",
                "Ask whether the missing 8 is a P-shadow of the present 2, because every other P-orbit keeps its membership.",
                receipts=["P-set symmetric difference is {2,8}"],
                authority="NONE",
            )
        )
    source_set = {int(digit) for digit in digits}
    t_image_set = {T[digit] for digit in source_set}
    p_delta = source_set ^ {P[digit] for digit in source_set}
    if t_image_set == source_set and p_delta == {2, 8}:
        proposals.append(
            record(
                "SCOUT_PROPOSAL",
                "t_fixed_opposite_half_probe",
                "This support is held as a set by T while P and N expose opposite halves of {2,8}; compare it with other T-fixed supports before assigning anti-Pi significance.",
                receipts=["T(source set)=source set", "P(source set)=N(source set)", "P symmetric difference is {2,8}"],
                authority="NONE",
            )
        )
    return proposals[:5]


def translate(raw: str, profile: str | None = None, scout: bool = False) -> dict[str, Any]:
    lexical_carrier = classify(raw)
    digits = lexical_carrier["normalized_digits"]
    if not digits:
        raise ValueError("input must contain at least one ASCII decimal digit")
    readings_path = Path(__file__).with_name("readings.json")
    readings = json.loads(readings_path.read_text(encoding="utf-8"))

    transforms = {
        name: record(
            "DERIVED_DEPENDENT",
            f"{name}(source)",
            apply_map(digits, mapping),
            source=digits,
            independence="ONE_DEPENDENT",
        )
        for name, mapping in MAPS.items()
    }
    counts = Counter(digits)
    unique = sorted({int(digit) for digit in digits})
    image_sets = {
        name: sorted({mapping[digit] for digit in unique})
        for name, mapping in MAPS.items()
    }
    set_deltas = {
        name: sorted(set(unique) ^ set(image_set))
        for name, image_set in image_sets.items()
    }
    set_stabilizer = [name for name, image_set in image_sets.items() if image_set == unique]
    orbit_membership = []
    source_set = set(unique)
    for left, right in PAIR_ORBITS:
        present = [digit for digit in (left, right) if digit in source_set]
        orbit_membership.append(
            {
                "orbit": [left, right],
                "present": present,
                "occupancy": ["none", "half", "full"][len(present)],
            }
        )
    matches = sequence_matches(digits, readings)
    signed_pairs = signed_pair_receivers(digits)
    gap_two = gap_two_receivers(digits)
    integer_facts: list[dict[str, Any]] = []
    if len(digits) <= 200:
        integer_value = int(digits)
        integer_facts = [
            record("EXACT_ARITHMETIC", "integer_value", integer_value),
            record("EXACT_ARITHMETIC", "digit_sum", sum(int(digit) for digit in digits)),
        ]
        if integer_value <= 10_000_000:
            integer_facts.extend(
                [
                    record("EXACT_ARITHMETIC", "integer_positive_divisors", positive_divisors(integer_value)),
                    record("EXACT_ARITHMETIC", "integer_prime_factorization", prime_factorization(integer_value)),
                ]
            )

    report: dict[str, Any] = {
        "schema": "rprm-operational-number-report/v1",
        "input": {"raw": raw, "digits": digits, "base": 10, "lexical_carrier": lexical_carrier},
        "policy": {
            "concurrent_lenses": True,
            "construction_history_preserved": True,
            "scout_has_authority": False,
            "lexical_carrier_precedes_digit_normalization": True,
            "punctuation_erasure_selects_no_semantic_carrier": True,
            "claim_ceiling": "This report enumerates affordances and proposals; it does not prove a unique meaning, independent source, or cross-carrier adapter.",
        },
        "sequence": {
            "length": len(digits),
            "digit_counts": {digit: counts[digit] for digit in sorted(counts)},
            "unique_digits": unique,
            "integer_facts": integer_facts,
            "adjacent_pairs": [digits[index : index + 2] for index in range(len(digits) - 1)],
            "signed_pair_receivers": signed_pairs,
            "gap_two_receivers": gap_two,
            "matched_readings": matches,
        },
        "declared_maps": {
            "definitions": {
                "P": "(0 5)(1 9)(2 8)(4 6), fixes 3 and 7",
                "N": "d -> -d mod 10, fixes 0 and 5",
                "T": "P after N = (0 5)(3 7)",
                "M": "d -> 9-d = (0 9)(1 8)(2 7)(3 6)(4 5)",
            },
            "fixed_sets": {
                name: [digit for digit in range(10) if mapping[digit] == digit]
                for name, mapping in MAPS.items()
            },
            "transforms": transforms,
            "source_set": unique,
            "image_sets": image_sets,
            "set_symmetric_differences": set_deltas,
            "set_stabilizer": set_stabilizer,
            "pair_orbit_membership": orbit_membership,
            "P_and_N_image_sets_equal": image_sets["P"] == image_sets["N"],
        },
        "digits": [digit_facts(digit, readings) for digit in unique],
    }
    if "T" in set_stabilizer and set_deltas["P"] == [2, 8]:
        report["declared_maps"]["finite_support_class"] = {
            "property": "T-fixed decimal digit support with P symmetric difference exactly {2,8}",
            "matching_supports": 32,
            "all_decimal_digit_supports": 1024,
            "derivation": "Choose full/empty membership on four P-orbits and one of two representatives on {2,8}: 2^4*2.",
            "lane": "EXACT_ARITHMETIC",
        }
    if profile == "pi-window":
        report["profile"] = pi_profile(digits)
    if scout:
        report["scout"] = {
            "mode": "BOUNDED_VIBE_SCOUT",
            "status": "PROPOSAL_NOT_AUTHORITY",
            "proposals": scout_proposals(digits, report["digits"], matches, signed_pairs, gap_two),
        }
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("value", help="A decimal numeral or digit string; punctuation is ignored.")
    parser.add_argument("--profile", choices=["pi-window"])
    parser.add_argument("--scout", action="store_true", help="Add bounded colloquial hypothesis prompts.")
    parser.add_argument("--compact", action="store_true", help="Emit compact rather than indented JSON.")
    args = parser.parse_args()
    try:
        report = translate(args.value, profile=args.profile, scout=args.scout)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        parser.error(str(error))
    print(json.dumps(report, indent=None if args.compact else 2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
