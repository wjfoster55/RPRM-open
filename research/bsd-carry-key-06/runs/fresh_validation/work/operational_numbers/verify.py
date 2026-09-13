#!/usr/bin/env python3
"""Black-box verifier for the operational number translator."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
TRANSLATOR = ROOT / "translate_number.py"
P_LITERAL = {0: 5, 1: 9, 2: 8, 3: 3, 4: 6, 5: 0, 6: 4, 7: 7, 8: 2, 9: 1}
N_LITERAL = {digit: (-digit) % 10 for digit in range(10)}
T_LITERAL = {digit: P_LITERAL[N_LITERAL[digit]] for digit in range(10)}
M_LITERAL = {digit: 9 - digit for digit in range(10)}


def run(value: str, *options: str) -> dict:
    completed = subprocess.run(
        [sys.executable, "-B", str(TRANSLATOR), value, *options, "--compact"],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return json.loads(completed.stdout)


def require(condition: bool, name: str) -> None:
    if not condition:
        raise AssertionError(name)


def fact(report: dict, digit: int, operation: str) -> dict:
    digit_report = next(item for item in report["digits"] if item["digit"] == digit)
    return next(item for item in digit_report["facts"] if item["operation"] == operation)


def signed_pair(report: dict, source: str, position: int | None = None) -> dict:
    return next(
        item
        for item in report["sequence"]["signed_pair_receivers"]
        if item["source"] == source and (position is None or item["position"] == position)
    )


def main() -> int:
    checks = 0

    pi = run("3.1415926535", "--profile", "pi-window", "--scout")
    require(pi["input"]["digits"] == "31415926535", "pi punctuation normalization")
    checks += 1
    require(pi["input"]["lexical_carrier"]["syntax_class"] == "SINGLE_DOT_SYNTAX", "pi lexical carrier")
    checks += 1
    require(pi["policy"]["lexical_carrier_precedes_digit_normalization"] is True, "lexing precedes normalization")
    checks += 1
    require(pi["declared_maps"]["transforms"]["P"]["value"] == "39690184030", "P-pi fixture")
    checks += 1
    require(pi["declared_maps"]["transforms"]["N"]["value"] == "79695184575", "N-pi fixture")
    checks += 1
    require(pi["declared_maps"]["transforms"]["M"]["value"] == "68584073464", "M-pi fixture")
    checks += 1
    require(pi["declared_maps"]["fixed_sets"]["M"] == [], "M fixed-point free")
    checks += 1
    final_35 = next(item for item in pi["sequence"]["gap_two_receivers"] if item["pair"] == [3, 5])
    require(final_35["position"] == 9 and final_35["M_oriented"] == [6, 4], "Pi terminal 35 M orientation")
    checks += 1
    require(final_35["fold_O_after_M"] == [4, 6] and final_35["mirror_swap_equals_numeric_plus_11"] is True, "Pi terminal 35 fold")
    checks += 1
    require(any(item["operation"] == "m_fold_35_probe" for item in pi["scout"]["proposals"]), "35 scout proposal")
    checks += 1
    require(pi["profile"]["shadows"][2]["value"] == "08584073464", "4-pi prefix fixture")
    checks += 1
    require(all(item["lane"] == "DERIVED_DEPENDENT" for item in pi["profile"]["shadows"]), "anti-pi dependency labels")
    checks += 1

    four_state_fixtures = {
        "35": {"signed_gap": 2, "centered_sum": -1, "O": "53", "M": "64", "F": "46"},
        "53": {"signed_gap": -2, "centered_sum": -1, "O": "35", "M": "46", "F": "64"},
        "64": {"signed_gap": -2, "centered_sum": 1, "O": "46", "M": "35", "F": "53"},
        "46": {"signed_gap": 2, "centered_sum": 1, "O": "64", "M": "53", "F": "35"},
    }
    four_state_reports = {word: run(word, "--scout") for word in four_state_fixtures}
    for word, expected in four_state_fixtures.items():
        report = four_state_reports[word]
        require(len(report["sequence"]["signed_pair_receivers"]) == 1, f"{word} all-pair receipt count")
        checks += 1
        receipt = signed_pair(report, word, 0)
        require(receipt["pair"] == [int(word[0]), int(word[1])] and receipt["source"] == word, f"{word} source receipt")
        checks += 1
        require(
            receipt["signed_gap"] == expected["signed_gap"]
            and receipt["centered_sum"] == expected["centered_sum"],
            f"{word} signed coordinates",
        )
        checks += 1
        require(
            receipt["words"]
            == {
                "source_I": word,
                "swap_O": expected["O"],
                "coordinatewise_M": expected["M"],
                "fold_O_after_M": expected["F"],
            },
            f"{word} I/O/M/F words",
        )
        checks += 1
        require(
            {item["word"] for item in receipt["complete_orbit"]} == set(four_state_fixtures)
            and receipt["distinct_state_count"] == 4,
            f"{word} complete four-state orbit",
        )
        checks += 1
        require(
            receipt["signed_gap_fiber"]["count"] == 8
            and receipt["signed_gap_fiber"]["disposition"] == "MANY"
            and receipt["signed_gap_fiber"]["typed_disposition"] == "MANY(8)",
            f"{word} signed-gap fiber disposition",
        )
        checks += 1
        recovery = receipt["combined_coordinate_recovery"]
        require(
            recovery["word"] == word
            and recovery["pair"] == receipt["pair"]
            and recovery["count"] == 1
            and recovery["disposition"] == "ONE",
            f"{word} combined-coordinate ONE recovery",
        )
        checks += 1
        require(
            receipt["lane"] == "EXACT_DECLARED_MAP"
            and receipt["coordinate_lane"] == "EXACT_ARITHMETIC"
            and receipt["source_relation"] == "DERIVED_DEPENDENT"
            and receipt["independence"] == "ONE_DEPENDENT",
            f"{word} exact dependent labels",
        )
        checks += 1
        require(
            receipt["signed_gap_definition"] == "B-A"
            and receipt["terminology_boundary"] == "signed_gap is B-A; it is not gcd"
            and "g" not in receipt,
            f"{word} signed-gap versus gcd boundary",
        )
        checks += 1

    plus_two_fiber = ["02", "13", "24", "35", "46", "57", "68", "79"]
    minus_two_fiber = ["20", "31", "42", "53", "64", "75", "86", "97"]
    require(signed_pair(four_state_reports["35"], "35")["signed_gap_fiber"]["words"] == plus_two_fiber, "+2 complete fiber")
    checks += 1
    require(signed_pair(four_state_reports["64"], "64")["signed_gap_fiber"]["words"] == minus_two_fiber, "-2 complete fiber")
    checks += 1
    require(four_state_reports["64"]["sequence"]["gap_two_receivers"] == [], "64 precedes and survives old gap-two filter")
    checks += 1
    require(len(four_state_reports["46"]["sequence"]["gap_two_receivers"]) == 1, "46 remains in old ascending gap-two receiver")
    checks += 1
    expected_legacy_35 = {
        "lane": "EXACT_DECLARED_MAP",
        "carrier": "decimal ascending gap-two tower",
        "position": 0,
        "pair": [3, 5],
        "M_oriented": [6, 4],
        "fold_O_after_M": [4, 6],
        "chart_visible": True,
        "digit_sum": 8,
        "carry": 0,
        "remainder": 8,
        "mirror_swap_equals_numeric_plus_11": True,
    }
    require(four_state_reports["35"]["sequence"]["gap_two_receivers"] == [expected_legacy_35], "35 legacy gap-two receipt unchanged")
    checks += 1
    scout_64 = next(
        item
        for item in four_state_reports["64"]["scout"]["proposals"]
        if item["operation"] == "signed_64_anti_mirror_probe"
    )
    require(scout_64["lane"] == "SCOUT_PROPOSAL" and scout_64["authority"] == "NONE", "64 scout has no authority")
    checks += 1
    require("not an independent anti-Pi source" in scout_64["value"], "64 scout dependency ceiling")
    checks += 1

    endpoint_09 = signed_pair(run("09"), "09", 0)
    require(
        endpoint_09["signed_gap_fiber"]["words"] == ["09"]
        and endpoint_09["signed_gap_fiber"]["count"] == 1
        and endpoint_09["signed_gap_fiber"]["disposition"] == "ONE"
        and endpoint_09["signed_gap_fiber"]["typed_disposition"] == "ONE(09)",
        "endpoint +9 signed-gap ONE fiber",
    )
    checks += 1
    require(endpoint_09["distinct_state_count"] == 2, "endpoint orbit duplicate count")
    checks += 1

    pi_signed_pairs = pi["sequence"]["signed_pair_receivers"]
    expected_pi_gaps = [-2, 3, -3, 4, 4, -7, 4, -1, -2, 2]
    require(len(pi_signed_pairs) == len(pi["input"]["digits"]) - 1 == 10, "Pi all-adjacent signed-pair coverage")
    checks += 1
    require([item["position"] for item in pi_signed_pairs] == list(range(10)), "Pi signed-pair positions")
    checks += 1
    require([item["source"] for item in pi_signed_pairs] == pi["sequence"]["adjacent_pairs"], "Pi signed-pair words")
    checks += 1
    require([item["signed_gap"] for item in pi_signed_pairs] == expected_pi_gaps, "Pi signed-gap vector")
    checks += 1
    require(
        all(
            next(state for state in item["complete_orbit"] if state["operation"] == "M")["signed_gap"]
            == -item["signed_gap"]
            for item in pi_signed_pairs
        ),
        "Pi M negates every adjacent signed gap",
    )
    checks += 1
    require(
        all(
            item["source_relation"] == "DERIVED_DEPENDENT"
            and item["combined_coordinate_recovery"]["disposition"] == "ONE"
            for item in pi_signed_pairs
        ),
        "Pi pair mirrors stay source-dependent with ONE coordinate recovery",
    )
    checks += 1

    vacancy = run("1234679", "--scout")
    require(vacancy["declared_maps"]["image_sets"]["P"] == [1, 3, 4, 6, 7, 8, 9], "P image of candidate set")
    checks += 1
    require(vacancy["declared_maps"]["set_symmetric_differences"]["P"] == [2, 8], "single P-orbit vacancy")
    checks += 1
    require(vacancy["declared_maps"]["set_stabilizer"] == ["T"], "candidate set T stabilizer")
    checks += 1
    require(vacancy["declared_maps"]["P_and_N_image_sets_equal"] is True, "candidate P/N coimage")
    checks += 1
    require(vacancy["declared_maps"]["finite_support_class"]["matching_supports"] == 32, "finite support class count")
    checks += 1
    require(any(item["id"] == "p_orbit_vacancy_toggle" for item in vacancy["sequence"]["matched_readings"]), "vacancy reading emitted")
    checks += 1
    complement = run("08584073464", "--scout")
    require(complement["declared_maps"]["set_stabilizer"] == ["T"], "4-pi prefix support T stabilizer")
    checks += 1
    require(complement["declared_maps"]["set_symmetric_differences"]["P"] == [2, 8], "4-pi prefix opposite half orbit")
    checks += 1
    complement_28 = next(item for item in complement["declared_maps"]["pair_orbit_membership"] if item["orbit"] == [2, 8])
    vacancy_28 = next(item for item in vacancy["declared_maps"]["pair_orbit_membership"] if item["orbit"] == [2, 8])
    require(complement_28["present"] == [8] and vacancy_28["present"] == [2], "opposite {2,8} representatives")
    checks += 1
    all_supports = []
    for mask in range(1 << 10):
        support = {digit for digit in range(10) if mask & (1 << digit)}
        p_image = {P_LITERAL[digit] for digit in support}
        t_image = {T_LITERAL[digit] for digit in support}
        if t_image == support and support ^ p_image == {2, 8}:
            all_supports.append(support)
    require(len(all_supports) == 32, "independent exhaustive support class count")
    checks += 1

    eight = run("8", "--scout")
    require(fact(eight, 8, "power_of_two")["expression"] == "2^3=8", "eight power receipt")
    checks += 1
    require(fact(eight, 8, "paired_four_sum")["lane"] == "EXACT_ARITHMETIC", "eight paired-four arithmetic")
    checks += 1
    eight_reading = next(item for item in eight["digits"][0]["readings"] if item["id"] == "paired_four_negative_half")
    require(eight_reading["lane"] == "RPRM_READING" and "receiver" in eight_reading["missing"], "eight reading stays typed")
    checks += 1

    six = run("6", "--scout")
    require([2, 3] in fact(six, 6, "ordered_factor_pairs")["value"], "six 2x3 capability")
    checks += 1
    require(fact(six, 6, "target_corner_identity")["expression"] == "2+4", "six computed-corner receipt")
    checks += 1
    require(fact(six, 6, "M_image")["value"] == M_LITERAL[6] == 3, "six M image")
    checks += 1

    carrier_fixtures = [
        ("35", "PLAIN_DIGIT_SYNTAX", "35"),
        ("3.5", "SINGLE_DOT_SYNTAX", "35"),
        ("3/5", "SLASH_SYNTAX", "35"),
        ("3+5", "PLUS_SYNTAX", "35"),
        ("3,5", "COMMA_SYNTAX", "35"),
        ("13:53:23", "TIME_SYNTAX", "135323"),
        ("2.4.6", "MULTI_DOTTED_SYNTAX", "246"),
        ("2026-08-21", "ISO_DATE_SYNTAX", "20260821"),
        ("17ac1fc3-c9fc-4600-8050-7bebfdf9a657", "UUID_SYNTAX", "171394600805079657"),
        ("1e-3", "SCIENTIFIC_NOTATION_SYNTAX", "13"),
    ]
    for raw, syntax, normalized in carrier_fixtures:
        carrier = run(raw)["input"]["lexical_carrier"]
        require(carrier["syntax_class"] == syntax and carrier["normalized_digits"] == normalized, f"carrier fixture {raw}")
        checks += 1
    plain_carrier = run("35")["input"]["lexical_carrier"]
    require(plain_carrier["dispatch_mode"] == "EXACT_DIGIT_STRING" and "EXACT_DIGIT_WORD" in plain_carrier["semantic_fiber"], "plain digit backward compatibility")
    checks += 1
    wrapped_carrier = run("(3,5)")["input"]["lexical_carrier"]
    require(wrapped_carrier["wrappers"] == ["()"] and wrapped_carrier["syntax_class"] == "COMMA_SYNTAX", "wrapped tuple carrier")
    checks += 1
    fraction_carrier = run("3/5")["input"]["lexical_carrier"]
    require(fraction_carrier["resolution"] == "MANY" and fraction_carrier["requires_explicit_adapter_for_semantic_claim"] is True, "ambiguous carrier fiber")
    checks += 1

    brink = run("91", "--scout")
    require(any(item["id"] == "nine_one_carry_brink" for item in brink["sequence"]["matched_readings"]), "91 carry-brink prompt")
    checks += 1
    require(any(item["operation"] == "carry_brink_probe" for item in brink["scout"]["proposals"]), "91 scout proposal")
    checks += 1

    for report in (pi, vacancy, complement, eight, six, brink):
        require(report["policy"]["concurrent_lenses"] is True, "concurrent lens policy")
        checks += 1
        if "scout" in report:
            require(report["scout"]["status"] == "PROPOSAL_NOT_AUTHORITY", "scout authority ceiling")
            checks += 1
            require(all(item["lane"] == "SCOUT_PROPOSAL" for item in report["scout"]["proposals"]), "scout lane isolation")
            checks += 1

    invalid = subprocess.run(
        [sys.executable, "-B", str(TRANSLATOR), "no-digits-here"],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    require(invalid.returncode != 0, "reject digitless input")
    checks += 1

    readings = json.loads((ROOT / "readings.json").read_text(encoding="utf-8"))
    require(set(readings["digits"]) == set("0123456789"), "all ten digits have a reading page")
    checks += 1

    print(f"PASS: {checks}/{checks} operational-number checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
