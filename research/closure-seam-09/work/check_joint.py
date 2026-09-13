"""Exhaust the 32 binary-coordinate matching sources documented in JOINT_RELATION.md.

Run with --output /absolute/new/receipt.json to save an immutable receipt.
Existing receipt paths are refused. All mathematical checks remain active with -O.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
from itertools import permutations, product
import json
from pathlib import Path
import platform


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def check() -> dict:
    lanes = tuple(product((0, 1), repeat=2))
    matchings = tuple(permutations(range(2)))
    rows = []
    fibers = {}
    ledger = []
    for x, y, pi in product(lanes, lanes, matchings):
        direct = sum((x[i] - y[pi[i]]) ** 2 for i in range(2))
        cross = sum(x[i] * y[pi[i]] for i in range(2))
        expanded = sum(v * v for v in x + y) - 2 * cross
        require(direct == expanded, "cross-term identity failed")
        rows.append((x, y, pi, direct))
        fibers.setdefault((x, y), []).append((pi, direct))
        ledger.append({
            "left_values": x,
            "right_values": y,
            "matching": pi,
            "sum_squared_differences": direct,
            "cross_term": cross,
            "expanded_value": expanded,
        })

    fixed = fibers[((0, 1), (0, 1))]
    require(fixed == [((0, 1), 0), ((1, 0), 2)], "pairing collision changed")
    require(
        all(d == 2 * int(pi == (1, 0)) for pi, d in fixed),
        "repair decoder failed",
    )
    classes = [len({d for _, d in members}) for members in fibers.values()]
    require(len(rows) == 32 and len(fibers) == 16, "finite coverage changed")
    require(max(classes) == 2 and classes.count(2) == 4, "repair classes changed")
    hostile = fibers[((0, 0), (0, 1))]
    require({d for _, d in hostile} == {1}, "distance should be constant")
    require({pi[0] for pi, _ in hostile} == {0, 1}, "occurrence distinction lost")
    return {
        "status": "PASS",
        "sources": len(rows),
        "side_record_fibers": len(fibers),
        "distance_ambiguous_fibers": classes.count(2),
        "maximum_repair_alphabet": max(classes),
        "fixed_records_distances": [d for _, d in fixed],
        "equal_distance_distinct_matchings": len(hostile),
        "parameters": {
            "coordinate_values": [0, 1],
            "occurrences_per_side": 2,
            "matching_carrier": matchings,
            "receiver": "sum_i (x_i - y_pi(i))^2",
            "source_equality": "ordered occurrence values and matching agree",
            "context": "fixed common frame and unit; no assignment optimization",
        },
        "source_ledger": ledger,
        "claim_scope": "exact finite enumeration; written general laws are separate",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="New JSON path; overwrite is refused")
    args = parser.parse_args()
    if args.output is not None and args.output.exists():
        parser.error(f"refusing to overwrite existing receipt: {args.output}")
    receipt = check()
    receipt.update({
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "source_file": "research/closure-seam-09/work/check_joint.py",
        "python_version": platform.python_version(),
    })
    serialized = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    if args.output is None:
        print(serialized, end="")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("x", encoding="utf-8", newline="\n") as handle:
            handle.write(serialized)
        print(f"PASS: {receipt['sources']} sources; receipt: {args.output.resolve()}")


if __name__ == "__main__":
    main()
