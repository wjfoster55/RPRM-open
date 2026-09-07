"""Independent small-number comparisons; no claim of a new prime or shortcut."""
import argparse
import hashlib
import importlib.util
import json
from math import isqrt
import os
from uuid import uuid4
from pathlib import Path

HERE = Path(__file__).resolve().parent


def oracle_trial_prime(n):
    """Independent complete divisor census; does not call the model."""
    if type(n) is not int or not 0 <= n <= (1 << 31) - 1:
        raise ValueError("oracle input must be an integer in 0..2^31-1")
    return n >= 2 and all(n % divisor for divisor in range(2, isqrt(n) + 1))


def validate_answer(p, answer):
    """Bind every returned field to the requested Mersenne integer."""
    if type(p) is not int or not 2 <= p <= 31:
        raise ValueError("checked exponent must be an integer in 2..31")
    expected_number = (1 << p) - 1
    if type(answer) is not dict or set(answer) != {"exponent", "number", "prime", "reason", "residues"}:
        raise ValueError("wrong Mersenne answer schema")
    if type(answer["exponent"]) is not int or answer["exponent"] != p:
        raise ValueError("answer exponent differs from the requested exponent")
    if type(answer["number"]) is not int or answer["number"] != expected_number:
        raise ValueError("answer number is not the requested 2^p-1")
    if type(answer["prime"]) is not bool or answer["prime"] != oracle_trial_prime(expected_number):
        raise ValueError("prime verdict differs from independent trial division")
    prime_exponent = oracle_trial_prime(p)
    reason = "composite exponent" if not prime_exponent else "M2=3" if p == 2 else "Lucas-Lehmer"
    if type(answer["reason"]) is not str or answer["reason"] != reason:
        raise ValueError("answer reason does not match its exponent branch")
    trace = []
    if prime_exponent and p != 2:
        state = 4
        for _ in range(p - 2):
            state = (state * state - 2) % expected_number
            trace.append(state)
    if (type(answer["residues"]) is not tuple
            or any(type(value) is not int for value in answer["residues"])
            or answer["residues"] != tuple(trace)):
        raise ValueError("residue trace differs from the stated recurrence")


def _run_checks(args):
    spec = importlib.util.spec_from_file_location("prime_example", HERE / "model.py")
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    def require(test, message):
        if not test: raise RuntimeError(message)
    cases = []
    for p in range(2, 32):
        answer = m.mersenne_reference(p)
        validate_answer(p, answer)
        require(m.trial_prime((1 << p) - 1) == oracle_trial_prime((1 << p) - 1),
                "Model trial division differs from the independent divisor census")
        cases.append({"p": p, "prime": answer["prime"]})
    require(not m.mersenne_reference(11)["prime"] and 23*89 == 2047, "Prime-exponent hostile case")
    digit_queries = 0
    for zeros in range(101):
        literal = "1" + "0"*zeros
        for i in range(len(literal)):
            require(m.zero_word_digit(zeros, i) == literal[i], "Constructor query mismatch")
            digit_queries += 1
    enormous = 10**100
    require(m.zero_word_digit(enormous, enormous//2) == "0", "Symbolic middle query")
    for exponent in range(1001):
        grade, remainder = m.exponent_grade(exponent)
        require(3*grade+remainder == exponent and 0 <= remainder < 3, "Scale coordinate inverse")
    for bad in (True, -1, 1.5, "31", None):
        try: m.mersenne_reference(bad)
        except ValueError: pass
        else: raise RuntimeError("Invalid exponent admitted")
    for outside in (0, 1, 32, 150003647):
        try: m.mersenne_reference(outside)
        except ValueError: pass
        else: raise RuntimeError("Unbounded primality work admitted")
    # Keep the demonstrated target substitution and individually malformed
    # fields as rejection controls, separate from the model implementation.
    clean = m.mersenne_reference(5)
    mutations = ({"number": 7, "exponent": 999}, {"number": 7}, {"exponent": 999},
                 {"prime": 1}, {"residues": ()}, {"reason": "composite exponent"})
    for changes in mutations:
        try: validate_answer(5, {**clean, **changes})
        except ValueError: pass
        else: raise RuntimeError("Corrupt Mersenne result admitted")
    result = {"status": "PASS", "scope": "30 requested Mersenne integers through exponent31, independent divisor census and recurrence traces; 5151 literal digit queries; 1001 scale inverses and declared controls. No frontier test or speedup claim.",
              "exponents": cases, "digit_queries": digit_queries,
              "corrupt_answer_rejections": len(mutations),
              "source_hashes": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in (HERE/"model.py", Path(__file__))}}
    payload = json.dumps(result, indent=2) + "\n"
    _publish(args.output, result)
    print(payload)


def _publish(path, result):
    if path is None:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + "." + uuid4().hex + ".tmp")
    temporary.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="optional absolute JSON receipt path")
    args = parser.parse_args()
    if args.output is not None:
        if not args.output.is_absolute():
            parser.error("--output requires an absolute path")
        args.output = args.output.resolve()
        source_files = {(HERE / name).resolve() for name in ("README.md", "model.py", "example.py", "check.py")}
        if args.output in source_files:
            parser.error("--output cannot overwrite this pack's source files")
    _publish(args.output, {"status": "PENDING"})
    try:
        return _run_checks(args)
    except Exception as exc:
        _publish(args.output, {"status": "FAIL", "error": f"{type(exc).__name__}: {exc}"})
        raise


if __name__ == "__main__": main()
