#!/usr/bin/env python3
"""Classify a raw numeral token before any punctuation-erasing digit view."""

from __future__ import annotations

import re
from typing import Any


UUID = re.compile(r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}")
ISO_DATE = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}")
TIME = re.compile(r"[0-9]{1,2}:[0-9]{2}:[0-9]{2}")
DATETIME = re.compile(r"[0-9]{1,4}(?:[/.-][0-9]{1,2}){2}[ T][0-9]{1,2}:[0-9]{2}(?::[0-9]{2})?")
SCIENTIFIC = re.compile(r"[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)[eE][+-]?[0-9]+")
PLAIN_DIGITS = re.compile(r"[0-9]+")
SIGNED_INTEGER = re.compile(r"[+-][0-9]+")
DECIMAL = re.compile(r"[+-]?[0-9]+\.[0-9]+")
DOTTED = re.compile(r"[0-9]+(?:\.[0-9]+){2,}")
FRACTION = re.compile(r"[+-]?[0-9]+/[0-9]+")
SUM = re.compile(r"[+-]?[0-9]+\+[0-9]+")
COMMA_SEQUENCE = re.compile(r"[0-9]+(?:,[0-9]+)+")
THOUSANDS = re.compile(r"[0-9]{1,3}(?:,[0-9]{3})+")
HYPHEN_SEQUENCE = re.compile(r"[0-9]+(?:-[0-9]+)+")
COLON_SEQUENCE = re.compile(r"[0-9]+(?::[0-9]+)+")


def unwrap(raw: str) -> tuple[str, list[str]]:
    core = raw.strip()
    wrappers: list[str] = []
    pairs = {"(": ")", "[": "]", "{": "}", "`": "`"}
    changed = True
    while changed and len(core) >= 2:
        changed = False
        closing = pairs.get(core[0])
        if closing is not None and core[-1] == closing:
            wrappers.append(core[0] + closing)
            core = core[1:-1].strip()
            changed = True
    return core, wrappers


def classify(raw: str) -> dict[str, Any]:
    core, wrappers = unwrap(raw)
    digits = "".join(character for character in core if character.isascii() and character.isdigit())
    candidates: list[str] = []
    syntax = "TEXT_WITH_EMBEDDED_DIGITS"

    def add(name: str) -> None:
        if name not in candidates:
            candidates.append(name)

    if UUID.fullmatch(core):
        syntax = "UUID_SYNTAX"
        add("UUID_IDENTIFIER")
        add("HYPHENATED_IDENTIFIER")
    elif DATETIME.fullmatch(core):
        syntax = "DATETIME_SYNTAX"
        add("DATE_TIME")
        add("IDENTIFIER_OR_LOG_LABEL")
    elif ISO_DATE.fullmatch(core):
        syntax = "ISO_DATE_SYNTAX"
        add("CALENDAR_DATE")
        add("HYPHENATED_IDENTIFIER")
    elif TIME.fullmatch(core):
        syntax = "TIME_SYNTAX"
        add("CLOCK_TIME")
        add("COLON_SEPARATED_SEQUENCE")
    elif SCIENTIFIC.fullmatch(core):
        syntax = "SCIENTIFIC_NOTATION_SYNTAX"
        add("SCIENTIFIC_NUMBER_LITERAL")
    elif "..." in core or "…" in core:
        syntax = "ELLIPSIS_NUMERAL_SYNTAX"
        add("TRUNCATED_OR_REPEATING_DECIMAL")
        add("PREFIX_WITH_UNSPECIFIED_CONTINUATION")
    elif DOTTED.fullmatch(core):
        syntax = "MULTI_DOTTED_SYNTAX"
        add("SOFTWARE_VERSION")
        add("DOTTED_COORDINATE_OR_SECTION")
    elif DECIMAL.fullmatch(core):
        syntax = "SINGLE_DOT_SYNTAX"
        add("DECIMAL_NUMBER_LITERAL")
        add("VERSION_OR_COORDINATE")
    elif FRACTION.fullmatch(core):
        syntax = "SLASH_SYNTAX"
        add("RATIONAL_FRACTION")
        add("PATH_OR_RATIO_TOKEN")
    elif SUM.fullmatch(core):
        syntax = "PLUS_SYNTAX"
        add("ARITHMETIC_SUM_EXPRESSION")
        add("PLUS_SEPARATED_SEQUENCE")
    elif COMMA_SEQUENCE.fullmatch(core):
        syntax = "COMMA_SYNTAX"
        if THOUSANDS.fullmatch(core):
            add("THOUSANDS_GROUPED_INTEGER")
        add("COMMA_SEPARATED_SEQUENCE")
        add("TUPLE_OR_DIGIT_LIST")
    elif HYPHEN_SEQUENCE.fullmatch(core):
        syntax = "HYPHEN_SYNTAX"
        add("HYPHENATED_SEQUENCE")
        add("IDENTIFIER_FRAGMENT")
    elif COLON_SEQUENCE.fullmatch(core):
        syntax = "COLON_SYNTAX"
        add("COLON_SEPARATED_SEQUENCE")
        add("TIME_OR_RATIO_TOKEN")
    elif SIGNED_INTEGER.fullmatch(core):
        syntax = "SIGNED_INTEGER_SYNTAX"
        add("SIGNED_INTEGER_LITERAL")
        add("SIGNED_DIGIT_WORD")
    elif PLAIN_DIGITS.fullmatch(core):
        syntax = "PLAIN_DIGIT_SYNTAX"
        add("EXACT_DIGIT_WORD")
        add("NONNEGATIVE_INTEGER_LITERAL")
    else:
        add("TEXT_WITH_EMBEDDED_DIGITS")
        add("UNRESOLVED_IDENTIFIER_OR_EXPRESSION")

    return {
        "raw": raw,
        "core": core,
        "wrappers": wrappers,
        "syntax_class": syntax,
        "semantic_fiber": candidates,
        "resolution": "ONE" if len(candidates) == 1 else "MANY",
        "normalized_digits": digits,
        "normalization_changed": core != digits,
        "dispatch_mode": "EXACT_DIGIT_STRING" if syntax == "PLAIN_DIGIT_SYNTAX" else "NORMALIZED_DIGIT_VIEW",
        "requires_explicit_adapter_for_semantic_claim": syntax != "PLAIN_DIGIT_SYNTAX" or len(candidates) != 1,
        "claim_ceiling": "Classification preserves possible lexical carriers; it does not choose the token's mathematical meaning from syntax alone.",
    }


if __name__ == "__main__":
    import argparse
    import json

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("token")
    args = parser.parse_args()
    print(json.dumps(classify(args.token), indent=2, sort_keys=True))
