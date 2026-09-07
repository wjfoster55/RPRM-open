"""Independent finite conformance and hostile controls for fixed-gap decisions.

--output must be an absolute .json path. Repository outputs must be inside
.artifacts. Outputs must be fresh, except the aggregate runner's exact
PENDING placeholder inside .artifacts; existing external outputs are rejected.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from math import isqrt
import os
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from rprm.core import AdmissionError
from rprm.fixed_gap import decide_fixed_gap


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def direct(a, n, s, d):
    # Independent power construction: no imported residual/author evaluator.
    powers = []
    for base in (a, a + s, a + s + d):
        value = 1
        for _ in range(n):
            value *= base
        powers.append(value)
    return powers[0] + powers[1] - powers[2]


def inspect_receipt(result, n, s, d):
    """Replay every recorded midpoint and bracket against the direct oracle."""
    bound = 2 * n * (s + d)
    require(result["parameters"] == {"n": n, "s": s, "d": d}, "Changed supplied ports")
    require(result["derived_bound"] == bound, "Undeclared height bound")
    lower, upper = 0, bound
    require(result["initial_bracket"] == {
        "lower": lower, "upper": upper, "lower_residual": direct(lower, n, s, d),
        "upper_residual": direct(upper, n, s, d)}, "Initial endpoint receipt")
    require(direct(lower, n, s, d) < 0 < direct(upper, n, s, d), "Derived endpoint signs")
    for step in result["trace"]:
        width = upper - lower
        require(width > 1, "Extra step after adjacency")
        midpoint = (lower + upper) // 2
        value = direct(midpoint, n, s, d)
        require(step == {"lower": lower, "upper": upper,
                         "midpoint": midpoint, "residual": value}, "Midpoint trace differs")
        require(lower < midpoint < upper, "Midpoint outside open bracket")
        if value < 0:
            lower = midpoint
        else:
            upper = midpoint
        require(upper - lower <= (width + 1) // 2 < width, "Bisection did not shrink")
        require(direct(lower, n, s, d) < 0 <= direct(upper, n, s, d), "Lost sign invariant")
    require(upper == lower + 1, "Incomplete terminal bracket")
    require(result["final_bracket"] == {
        "lower": lower, "upper": upper, "lower_residual": direct(lower, n, s, d),
        "upper_residual": direct(upper, n, s, d)}, "Final endpoint receipt")
    require(result["bisection_rounds"] == len(result["trace"]) <= (bound - 1).bit_length(),
            "Wrong bisection count/bound")
    require(result["residual_evaluations"] == len(result["trace"]) + 2, "Wrong evaluation count")
    expected = (upper,) if direct(upper, n, s, d) == 0 else ()
    require(result["fiber"] == expected, "Fiber disagrees with terminal zero")
    require(result["status"] == ("ONE" if expected else "NONE"), "Wrong disposition")
    require(result["source"] == ((upper, upper + s, upper + s + d, n) if expected else None),
            "Wrong reconstructed source")


def run():
    square = decide_fixed_gap(2, 1, 1)
    inspect_receipt(square, 2, 1, 1)
    require(square["fiber"] == (3,) and square["source"] == (3, 4, 5, 2), "Square equality lost")
    require(any(step["residual"] == 0 for step in square["trace"]), "Exact midpoint control missing")
    fifth = decide_fixed_gap(5, 2, 1)
    inspect_receipt(fifth, 5, 2, 1)
    require(fifth["status"] == "NONE" and fifth["final_bracket"] == {
        "lower": 11, "upper": 12, "lower_residual": -5480, "upper_residual": 27281},
        "Fifth-power hostile bracket changed")
    # The raw polynomial decreases here. Assuming its monotonicity is invalid.
    require(direct(1, 5, 2, 1) < direct(0, 5, 2, 1) < 0, "Raw-D hostile control")

    apertures = integer_inputs = normalized_comparisons = 0
    dispositions = {"NONE": 0, "ONE": 0}
    for n in range(2, 9):
        for s in range(1, 7):
            for d in range(1, 7):
                result = decide_fixed_gap(n, s, d)
                inspect_receipt(result, n, s, d)
                bound = 2 * n * (s + d)
                expected = []
                previous = None
                for a in range(1, bound + 1):
                    value = direct(a, n, s, d)
                    if value == 0:
                        expected.append(a)
                    normalized = Fraction(value, a**n)
                    if previous is not None:
                        require(previous < normalized, "Finite normalized monotonicity control")
                        normalized_comparisons += 1
                    previous = normalized
                    integer_inputs += 1
                require(result["fiber"] == tuple(expected), "Full derived finite fiber mismatch")
                require(len(expected) <= 1, "Unexpected multiple integer roots")
                apertures += 1
                dispositions[result["status"]] += 1

    # Quadratic completion independently gives a=d+sqrt(2*d*(s+d)).
    # These values exceed fixed machine integers, without floating point.
    scale = 10**80
    large_cases = ((2, scale, scale), (2, scale + 1, scale),
                   (2, 2**300, 1), (5, 10**60, 1))
    for n, s, d in large_cases:
        result = decide_fixed_gap(n, s, d)
        inspect_receipt(result, n, s, d)
        if n == 2:
            radicand = 2 * d * (s + d)
            root = isqrt(radicand)
            expected = (d + root,) if root * root == radicand else ()
            require(result["fiber"] == expected, "Independent quadratic fiber mismatch")

    class IntSubclass(int):
        pass

    invalid_types = (True, False, 2.0, float("nan"), float("inf"), "2", None,
                     Fraction(2, 1), complex(2, 0), IntSubclass(2), (), [])
    admission_controls = 0
    for position in range(3):
        for value in invalid_types:
            arguments = [2, 1, 1]
            arguments[position] = value
            try:
                decide_fixed_gap(*arguments)
            except AdmissionError:
                admission_controls += 1
            else:
                raise RuntimeError("Non-exact input was coerced or accepted")
    for arguments in ((1, 1, 1), (0, 1, 1), (-2, 1, 1), (2, 0, 1),
                      (2, -1, 1), (2, 1, 0), (2, 1, -1)):
        try:
            decide_fixed_gap(*arguments)
        except AdmissionError:
            admission_controls += 1
        else:
            raise RuntimeError("Out-of-domain input was accepted")

    # Changing a returned record cannot alter a later independent decision.
    square["trace"][0]["residual"] = 999
    require(decide_fixed_gap(2, 1, 1)["trace"][0]["residual"] != 999, "Shared mutable receipt")
    return {"apertures": apertures, "family": "n=2..8, s=1..6, d=1..6",
            "integer_inputs": integer_inputs, "normalized_comparisons": normalized_comparisons,
            "dispositions": dispositions, "large_integer_cases": len(large_cases),
            "admission_controls": admission_controls, "output_guard_controls": check_output_guards(),
            "coverage": "Direct multiplication over every a=1..2*n*(s+d) in the finite family, "
                        "every recorded bisection invariant, named square/fifth controls, "
                        "independent quadratic fibers and malformed inputs. "
                        "The all-input coverage theorem remains a written proof; this is not a Lean proof or universal FLT test."}


def write_result(path, result):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + "." + uuid4().hex + ".tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def initialize_output(path, root=ROOT):
    """Admit the destination before any write, then claim its PENDING receipt."""
    if not path.is_absolute():
        raise ValueError("--output must be an absolute JSON path")
    path = path.resolve()
    root = root.resolve()
    if path.suffix.lower() != ".json":
        raise ValueError("--output must end in .json")
    # Compare resolved destinations to the literal artifact subtree. A link
    # from .artifacts back into source must not grant source-write admission.
    in_artifacts = path.is_relative_to(root / ".artifacts")
    if path.is_relative_to(root) and not in_artifacts:
        raise ValueError("Repository outputs must be inside .artifacts")
    existing = path.exists()
    if existing:
        placeholders = (b'{"status": "PENDING"}\n', b'{"status": "PENDING"}\r\n')
        if not in_artifacts or not path.is_file() or path.read_bytes() not in placeholders:
            raise ValueError("Output exists; use a fresh path or the runner's exact PENDING placeholder")
    pending = {"schema": "rprm-fixed-gap-conformance/v1", "status": "PENDING"}
    path.parent.mkdir(parents=True, exist_ok=True)
    if existing:
        write_result(path, pending)
    else:
        # Exclusive creation also rejects a file that appeared after admission.
        with path.open("x", encoding="utf-8") as stream:
            stream.write(json.dumps(pending) + "\n")
    return path


def check_output_guards():
    """Use only a disposable mock repository; never probe real source writes."""
    with TemporaryDirectory(prefix="rprm-fixed-gap-guards-") as temporary:
        area = Path(temporary).resolve()
        root = area / "mock-repository"
        sources = {root / "checks/fixed_gap.py": b"source must survive\n",
                   root / "DOCUMENT_BUILD.json": b'{"asset": "must survive"}\n',
                   root / ".artifacts/old.json": b'{"status": "PASS"}\n',
                   area / "external.json": b'{"status": "PENDING"}\n'}
        for path, data in sources.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        rejected = (root / "checks/fixed_gap.py", root / "DOCUMENT_BUILD.json",
                    root / ".artifacts/../DOCUMENT_BUILD.json",
                    root / "new/nested/output.json", root / ".artifacts/old.json",
                    area / "external.json", area / "new/output.txt", Path("relative.json"))
        before_files = {p.relative_to(area): p.read_bytes() for p in area.rglob("*") if p.is_file()}
        before_paths = {p.relative_to(area) for p in area.rglob("*")}
        for path in rejected:
            try:
                initialize_output(path, root)
            except ValueError:
                pass
            else:
                raise RuntimeError("Unsafe output destination was admitted")
            require({p.relative_to(area): p.read_bytes() for p in area.rglob("*") if p.is_file()}
                    == before_files, "Rejected output modified source/assets/old content")
            require({p.relative_to(area) for p in area.rglob("*")} == before_paths,
                    "Rejected output created paths")
        accepted = (root / ".artifacts/fresh/nested.json", area / "fresh-external.json",
                    root / ".artifacts/runner-lf.json", root / ".artifacts/runner-crlf.json")
        accepted[2].write_bytes(b'{"status": "PENDING"}\n')
        accepted[3].write_bytes(b'{"status": "PENDING"}\r\n')
        for path in accepted:
            require(initialize_output(path, root) == path.resolve(), "Wrong admitted output path")
            require(json.loads(path.read_text(encoding="utf-8")) == {
                "schema": "rprm-fixed-gap-conformance/v1", "status": "PENDING"}, "Pending claim failed")
        require(all(path.read_bytes() == data for path, data in sources.items()), "Fixture source changed")
    return {"rejected": len(rejected), "accepted": len(accepted),
            "boundary": "Disposable mock repository only; rejected paths created no files/directories "
                        "and left source, JSON assets and existing output bytes unchanged."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        args.output = initialize_output(args.output)
    except (ValueError, OSError) as error:
        parser.error(str(error))
    names = ("rprm/fixed_gap.py", "rprm/core.py", "checks/fixed_gap.py")
    before = {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in names}
    try:
        counts = run()
        after = {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in names}
        require(before == after, "Source changed during checking")
        result = {"schema": "rprm-fixed-gap-conformance/v1", "status": "PASS", "counts": counts,
                  "source_hashes": before, "source_unchanged": True,
                  "python": sys.version, "formal_proof": False, "universal_flt_proof": False}
    except Exception as error:
        write_result(args.output, {"schema": "rprm-fixed-gap-conformance/v1", "status": "FAIL",
                                  "error": f"{type(error).__name__}: {error}", "source_hashes": before})
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    write_result(args.output, result)
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
