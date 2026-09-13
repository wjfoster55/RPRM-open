"""Bounded decimal-word checks; no BSD or universal digit-meaning claim."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import product
import json
from pathlib import Path

DIGITS = "0123456789"
WORDS = tuple(a + b for a, b in product(DIGITS, repeat=2))


def max_overlap(u: str, v: str) -> tuple[str, int]:
    """Concatenate after the longest suffix(u) = prefix(v), including full overlap."""
    k = max(k for k in range(min(len(u), len(v)) + 1)
            if k == 0 or u[-k:] == v[:k])
    return u + v[k:], k


def overlap_word(w: str) -> str:
    if w not in WORDS:
        raise ValueError("admission error: expected an exact two-digit word")
    return max_overlap(w, w[::-1])[0]


def certificate(w: str) -> str:
    return w + "2" + overlap_word(w)


def fiber(table: dict[str, str], z: str) -> dict:
    # Scans the complete, explicitly finite source carrier.
    values = [w for w in WORDS if table[w] == z]
    return {"disposition": "NONE" if not values else "ONE" if len(values) == 1 else "MANY",
            "values": values}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    rows = []
    table = {w: overlap_word(w) for w in WORDS}
    codes = {w: certificate(w) for w in WORDS}
    max_fixed, grammar_agree, grammar_differ = [], [], []
    for w in WORDS:
        a, b = w
        joined, k = max_overlap(w, w[::-1])
        # Independent case formula derived from the two possible positive overlaps.
        assert joined == (w if a == b else a + b + a)
        assert k == (2 if a == b else 1)
        assert joined[:2] == w and codes[w][:2] == w
        assert fiber(table, joined) == {"disposition": "ONE", "values": [w]}
        assert fiber(codes, codes[w]) == {"disposition": "ONE", "values": [w]}
        one_symbol = w + w[::-1][1:]
        (grammar_agree if joined == one_symbol else grammar_differ).append(w)
        if joined == w:
            max_fixed.append(w)
        rows.append({"source": w, "reverse": w[::-1], "overlap_length": k,
                     "max_overlap": joined, "one_symbol_overlap": one_symbol,
                     "certificate": codes[w]})
    assert len(set(table.values())) == len(set(codes.values())) == 100
    assert max_fixed == [d + d for d in DIGITS]
    assert len(grammar_agree) == 90 and grammar_differ == max_fixed
    assert codes["59"] == "592595"
    assert codes["58"] == "582585"
    assert codes["55"] == "55255"
    assert table["55"] == "55" and "55" + "55"[1:] == "555"
    assert 2 * 59 == 118 and "59" * 2 == "5959"
    output_carrier = tuple("".join(ds) for n in (2, 3) for ds in product(DIGITS, repeat=n))
    dispositions = Counter(fiber(table, z)["disposition"] for z in output_carrier)
    assert dispositions == {"ONE": 100, "NONE": 1000}
    # A separate declared positional grammar: tag | numerator | 9 | denominator.
    lower_rows, rational_fibers = [], defaultdict(list)
    for tag, a, b in product(DIGITS, repeat=3):
        word = tag + a + "9" + b
        assert (word[0], word[1], word[3]) == (tag, a, b) and word[2] == "9"
        lower_rows.append(word)
        if b != "0":
            rational_fibers[Fraction(int(a), int(b))].append(word)
    lower_pair_fiber = [s for s in lower_rows if (s[1], s[3]) == ("3", "4")]
    q_fiber = rational_fibers[Fraction(3, 4)]
    assert len(lower_rows) == 1000 and len(lower_pair_fiber) == 10 and len(q_fiber) == 20
    assert [s for s in q_fiber if s[0] == "7"] == ["7394", "7698"]
    assert Fraction(7394) != Fraction(3, 4)
    lower = Fraction("6.38511803") - Fraction("6.385625424")
    upper = Fraction("6.38518585") - Fraction("6.384593255")
    assert lower == Fraction(-507394, 10**9) and upper == Fraction(592595, 10**9)
    assert "507394"[:2] == "50" and "507394"[2:] == "7394"
    report = {
        "schema": "bsd-sliding-hook-15/digit-scout-checks/v1",
        "status": "PASS", "candidate_status": "POSTTARGET_FITTED",
        "carrier": "all 100 exact width-two base-10 words, including leading zero",
        "max_overlap_image_count": len(set(table.values())),
        "certificate_image_count": len(set(codes.values())),
        "certificate_length_counts": dict(Counter(map(len, codes.values()))),
        "overlap_fibers_on_all_width_two_or_three_words": dict(dispositions),
        "fixed_words": max_fixed,
        "bounded_two_grammar_fiber_after_59": ["max_overlap", "one_symbol_overlap"],
        "grammar_agree_count": len(grammar_agree), "grammar_differ_words": grammar_differ,
        "certificate_fibers": {z: fiber(codes, z) for z in ("592595", "582585", "55255", "552555", "592594", "507394")},
        "lower_parser_count": len(lower_rows),
        "lower_rational_enabled_count": sum(map(len, rational_fibers.values())),
        "lower_pair_3_4_fiber": lower_pair_fiber,
        "lower_rational_3_over_4_fiber": q_fiber,
        "retained_lower_prefix": "50", "selected_lower_suffix": "7394",
        "bound_fractions": {"lower": str(lower), "upper": str(upper)},
        "9_divisibility": {w: int(w) % 9 == 0 for w in ("592595", "507394", "7394", "59", "595", "55")},
        "rows": rows,
        "claim_ceiling": "Definitions, direct finite proofs, and exhaustive tests of declared word maps; no inferred global numeral meanings or BSD equality.",
    }
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k != "rows"}, indent=2))


if __name__ == "__main__":
    main()
