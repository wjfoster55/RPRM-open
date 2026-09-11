"""Eight public-interface regression witnesses for the process-mechanics work tree.

Encodes the hub diagnostics from the I1 integration review. These are software
boundary checks, not new empirical outcomes. Keep the original seven kit example
checks separately passing.
"""

from __future__ import annotations

import argparse
import importlib.util
import itertools
import json
import math
import subprocess
import sys
from pathlib import Path


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def run(root: Path) -> dict:
    root = root.resolve()
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))

    from rprm.process_mechanics.candidates import filter_candidates
    from rprm.process_mechanics.measurement import admit_measurement

    circuit = load_module(
        "contract_regression_circuit_model",
        root / "experimental/process-mechanics/circuits/circuit_model.py",
    )
    rows = [{"candidate_id": "c", "outcome": "NO", "D": 0.0, "S": 0.0}]
    obs = [{"D": 2.0}, {"S": float("nan")}]
    order = [filter_candidates(rows, list(o)).status for o in itertools.permutations(obs)]
    dup = filter_candidates(
        [
            {"candidate_id": "same", "outcome": "YES", "D": 0.0},
            {"candidate_id": "same", "outcome": "NO", "D": 0.0},
        ],
        [],
    )
    typed = filter_candidates(
        [
            {"candidate_id": "a", "outcome": 1, "D": 0.0},
            {"candidate_id": "b", "outcome": "1", "D": 0.0},
        ],
        [],
    )
    adm = admit_measurement(
        arithmetic_ok="false",
        calibration_ok="false",
        coverage_ok="false",
        estimator_equivalence_ok="false",
    )
    exact_end = math.exp(-0.1)
    rejected = False
    try:
        event = circuit.rc_exact_event(
            1.0, 0.0, 1, 1.0, 0.9, 1.0, 0.0, 0.5, circuit.RCParams(1.0, 1.0)
        )
    except ValueError as exc:
        event = "ADMISSION_ERROR: " + str(exc)
        rejected = any(
            term in str(exc).lower() for term in ("grid", "switch", "unsupported")
        )

    cases = [
        {
            "id": "CANDIDATE_INPUT_ORDER",
            "expected": "ADMISSION_ERROR for both observation orders",
            "actual": order,
            "requirement_pass": order == ["ADMISSION_ERROR"] * 2,
        },
        {
            "id": "DUPLICATE_IDS",
            "expected": "ADMISSION_ERROR",
            "actual": dup.__dict__,
            "requirement_pass": dup.status == "ADMISSION_ERROR",
        },
        {
            "id": "OUTCOME_TYPES",
            "expected": "reject unsupported non-string labels or preserve type distinction",
            "actual": typed.__dict__,
            "requirement_pass": typed.status in ("ADMISSION_ERROR", "AMBIGUOUS"),
        },
        {
            "id": "STRICT_ADMISSION_FLAGS",
            "expected": "ADMISSION_ERROR for string truth flags",
            "actual": adm.__dict__,
            "requirement_pass": adm.status == "ADMISSION_ERROR",
        },
        {
            "id": "MIDSTEP_DRIVE",
            "expected_event": 0,
            "expected_final_voltage": exact_end,
            "actual_event": event,
            "algorithm_final_voltage": math.exp(-1),
            "requirement_pass": event == 0 or rejected,
        },
    ]

    script = """const M=require(process.argv[1]);
function attempt(f){try{return f()}catch(e){return {status:'ADMISSION_ERROR',error:String(e)}}}
const rs=attempt(()=>M.reuseCheck({},{}));
const ns=attempt(()=>M.joinCandidates([{id:'a',outcome:'NO',D:0}],[{D:NaN}]));
const unknown=attempt(()=>M.joinCandidates([{id:'a',outcome:'NO',D:0}],[{missing:0}]));
console.log(JSON.stringify({empty_context:rs,nan:ns,unknown_field:unknown}));"""
    model_js = root / "experimental/process-mechanics/playground/model.js"
    proc = subprocess.run(
        ["node", "-e", script, str(model_js)],
        text=True,
        capture_output=True,
        check=True,
    )
    js = json.loads(proc.stdout)
    cases += [
        {
            "id": "JS_EMPTY_CONTEXT",
            "expected": "reject missing required bindings",
            "actual": js["empty_context"],
            "requirement_pass": js["empty_context"]["status"] != "REUSE_OK",
        },
        {
            "id": "JS_NAN",
            "expected": "admission error, not empty family",
            "actual": js["nan"],
            "requirement_pass": js["nan"]["status"] == "ADMISSION_ERROR",
        },
        {
            "id": "JS_UNKNOWN_FIELD",
            "expected": "admission error, not empty family",
            "actual": js["unknown_field"],
            "requirement_pass": js["unknown_field"]["status"] == "ADMISSION_ERROR",
        },
    ]
    return {
        "scope": "eight focused public-interface diagnostics; not new empirical outcomes",
        "checks": cases,
        "passed": sum(1 for c in cases if c["requirement_pass"]),
        "failed": sum(1 for c in cases if not c["requirement_pass"]),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "root",
        type=Path,
        nargs="?",
        default=Path(__file__).resolve().parents[3],
        help="Work-tree root containing rprm/ and experimental/",
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run(args.root)
    text = json.dumps(result, indent=2) + "\n"
    print(text, end="")
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    return 0 if result["failed"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
