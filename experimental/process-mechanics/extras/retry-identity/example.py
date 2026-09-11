"""Retry identity toy: payload equality vs occurrence/request identity."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

# Resolve only the core shipped alongside this example.
REPO_CANDIDATES = [
    Path(__file__).resolve().parents[4],
]


def load_core():
    for root in REPO_CANDIDATES:
        core = root / "rprm" / "core.py"
        if core.is_file():
            sys.path.insert(0, str(root))
            from rprm.core import Occurrence, attach_occurrences  # noqa: WPS433
            return Occurrence, attach_occurrences
    raise RuntimeError("rprm.core not found")


def run() -> dict:
    Occurrence, attach_occurrences = load_core()
    payload = ("POST", "/charge", "sku=1")
    first = Occurrence("checkout", "req-001", "http", payload)
    retry = Occurrence("checkout", "req-002", "http", payload)  # intentional second op
    duplicate_delivery = Occurrence("checkout", "req-001", "http", payload)

    # Payload-only bag loses distinct request identities.
    payload_bag = {first.payload, retry.payload}
    identity_bag = {(first.identifier, first.payload), (retry.identifier, retry.payload)}
    payload_only = {
        "unique_payloads": len(payload_bag),
        "unique_identity_payload_pairs": len(identity_bag),
        "would_collapse_intentional_retry": len(payload_bag) < len(identity_bag),
        "note": "Payload-only dedup treats intentional second operation as one item",
    }
    # attach_occurrences retains ordered seam pairs by equal payload; objects stay distinct.
    seams = attach_occurrences((first,), (retry, duplicate_delivery))
    occurrence_aware = {
        "distinct_objects": first != retry,
        "seam_count_first_to_right": len(seams),
        "note": "Equal payloads can seam; occurrence identifiers remain distinct values",
    }
    try:
        conflict = Occurrence("checkout", "req-001", "http", ("POST", "/charge", "sku=2"))
        attach_occurrences((first,), (conflict,))
        conflict_status = "UNEXPECTED_ACCEPT"
    except Exception as exc:  # noqa: BLE001
        conflict_status = type(exc).__name__ + ": " + str(exc)

    return {
        "kit_id": "process-mechanics/extras/retry-identity",
        "evidence_grade": "NEW_ILLUSTRATIVE_DEMO",
        "claim_ids": ["UNMAPPED"],
        "payload_only": payload_only,
        "occurrence_aware": occurrence_aware,
        "conflict_rejection": conflict_status,
        "positive": payload_only["would_collapse_intentional_retry"] and occurrence_aware["distinct_objects"],
        "null": first.identifier != retry.identifier,
    }


def main() -> None:
    result = run()
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    out = Path(__file__).resolve().parent / "expected" / "demo_receipt.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(text, encoding="utf-8")
    print(text, end="")
    print("sha256", hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()
