#!/usr/bin/env python3
"""Tiny coverage check: RCF01 concept IDs must remain present or have successors."""
from __future__ import annotations
import json
import sys
from pathlib import Path

REQUIRED = [
    "RCF-P1", "RCF-P2", "RCF-P3", "RCF-F1", "RCF-F2", "RCF-F3",
    "RCF-C1", "RCF-C2", "RCF-C3", "RCF-N1", "RCF-R1", "RCF-PI1", "RCF-AD1",
]
REGISTER = Path(__file__).resolve().parent / "CONCEPT_REGISTER.json"


def main() -> int:
    payload = json.loads(REGISTER.read_text(encoding="utf-8"))
    ids = [entry["id"] for entry in payload["entries"]]
    missing = [i for i in REQUIRED if i not in ids]
    extra = [i for i in ids if i not in REQUIRED]
    if missing or extra or len(ids) != len(set(ids)):
        print(json.dumps({"status": "FAIL", "missing": missing, "extra": extra, "duplicate": len(ids) != len(set(ids))}))
        return 2
    print(json.dumps({"status": "PASS", "ids": ids, "count": len(ids)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
