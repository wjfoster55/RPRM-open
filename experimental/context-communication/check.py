"""Independent finite truth-table oracle; checks remain active under python -O."""
import argparse
from copy import deepcopy
import hashlib
import importlib.util
from itertools import combinations, product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def run_checks():
    # Import only after the CLI has replaced any old receipt with PENDING.
    spec = importlib.util.spec_from_file_location("communication_model", HERE / "model.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    functions = {"00": lambda c: 0, "01": lambda c: c,
                 "10": lambda c: 1-c, "11": lambda c: 1}
    ids = tuple(functions)
    records = tuple({"context": c, "answer": a} for c in (0, 1) for a in (0, 1))
    counts = {"assertions": 0, "histories": 0, "hypothesis_subsets": 0,
              "prediction_queries": 0, "append_transitions": 0,
              "truthful_policy_runs": 0, "rejections": 0}

    def require(ok, reason):
        counts["assertions"] += 1
        if not ok:
            raise RuntimeError(reason)

    def rejects(fn):
        try:
            fn()
        except ValueError:
            counts["rejections"] += 1
        else:
            raise RuntimeError("An out-of-carrier input was admitted")

    def tag(values):
        return ("NONE", "ONE", "MANY")[min(len(values), 2)]

    def oracle(history):
        # Independently accumulate per-context allowed bits, then evaluate four
        # handwritten functions, instead of parsing hypothesis ID characters.
        allowed = [{0, 1}, {0, 1}]
        for record in history:
            allowed[record["context"]].intersection_update({record["answer"]})
        return [key for key, fn in functions.items()
                if fn(0) in allowed[0] and fn(1) in allowed[1]]

    for key, fn in functions.items():
        for c in (0, 1):
            require(m.answer(key, c) == fn(c), "Response law differs from handwritten function")
    require(tuple(m.HYPOTHESES) == ids, "Declared hypothesis carrier changed")
    for length in range(7):
        for word in product(range(4), repeat=length):
            history = [dict(records[i]) for i in word]
            before = deepcopy(history)
            want = oracle(history)
            expected_fiber = {"disposition": tag(want), "hypotheses": want}
            require(m.fiber(history) == expected_fiber, "Complete hypothesis fiber disagreement")
            result = m.analyze(history)
            require(result["schema"] == "context-communication/v1", "Context schema")
            require(result["history"] == history and result["fiber"] == expected_fiber,
                    "Analysis discarded or changed an occurrence")
            pairs = []
            for context in (0, 1):
                zeros = [i for i, r in enumerate(history) if r == {"context": context, "answer": 0}]
                ones = [i for i, r in enumerate(history) if r == {"context": context, "answer": 1}]
                pairs.extend({"context": context, "occurrences": sorted((i, j))}
                             for i in zeros for j in ones)
            pairs.sort(key=lambda p: p["occurrences"])
            require(result["conflicts"] == pairs, "Complete conflict occurrence-pair disagreement")
            require(bool(pairs) == (not want), "Empty fiber must match a same-context contradiction")
            for context in (0, 1):
                values = sorted({functions[key](context) for key in want})
                predicted = {"disposition": tag(values), "values": values}
                require(m.predictions(history, context) == predicted, "Prediction readout disagreement")
                require(result["predictions"][context] == {"context": context, **predicted},
                        "Analysis predictions disagree")
                counts["prediction_queries"] += 1
            require(result["selection"] == m.minimax(want), "Analysis uses wrong candidate set")
            for record in records:
                after = m.append_answer(history, record["context"], record["answer"])
                require(after == history+[record], "Append lost or rewrote an answer")
                require(m.fiber(after)["hypotheses"] == oracle(history+[record]),
                        "Append successor fiber disagreement")
                require(set(m.fiber(after)["hypotheses"]).issubset(want), "Filtering added a hypothesis")
                counts["append_transitions"] += 1
            require(history == before, "Query or append mutated its source history")
            counts["histories"] += 1

    # All 16 candidate subsets, including those not reached from this full prior.
    for length in range(5):
        for chosen in combinations(ids, length):
            result = m.minimax(list(reversed(chosen)))
            require(result["hypotheses"] == list(chosen), "Candidate canonical order")
            if not chosen:
                require(result["status"] == "INCONSISTENT" and result["questions"] == []
                        and result["chosen_context"] is None and result["worst_case_size"] is None,
                        "Empty model invented a minimax guarantee")
                best = []
            else:
                partitions = []
                scores = []
                for context in (0, 1):
                    zero = [key for key in chosen if functions[key](context) == 0]
                    one = [key for key in chosen if functions[key](context) == 1]
                    score = max(len(zero), len(one))
                    partitions.append({"context": context, "branches": [
                        {"answer": 0, "hypotheses": zero}, {"answer": 1, "hypotheses": one}],
                        "worst_case_size": score})
                    scores.append(score)
                require(result["questions"] == partitions, "Exact minimax branches")
                best = [c for c in (0, 1) if scores[c] == min(scores) and scores[c] < len(chosen)]
                require(result["worst_case_size"] == min(scores), "Wrong minimax cardinality")
                require(result["status"] == ("ASK" if best else "IDENTIFIED"), "Selection status")
            require(result["choice_fiber"] == {"disposition": tag(best), "contexts": best},
                    "Optimal question ties were not preserved")
            require(result["chosen_context"] == (min(best) if best else None), "Declared tie break")
            counts["hypothesis_subsets"] += 1

    for truth, fn in functions.items():
        history = []
        contexts = []
        for _ in range(2):
            context = m.minimax(m.fiber(history)["hypotheses"])["chosen_context"]
            require(context in (0, 1), "Policy stopped before identifying source")
            contexts.append(context)
            history = m.append_answer(history, context, fn(context))
        require(contexts == [0, 1], "Two-query policy did not query both contexts")
        require(m.fiber(history) == {"disposition": "ONE", "hypotheses": [truth]}, "Truthful source lost")
        require(m.minimax([truth])["chosen_context"] is None, "Policy did not stop on identification")
        counts["truthful_policy_runs"] += 1

    # Equal summary sizes lose different next questions; duplicate occurrences
    # remain distinct even though redundant answers do not shrink the fiber.
    left = [{"context": 0, "answer": 0}]
    right = [{"context": 1, "answer": 0}]
    require(len(m.fiber(left)["hypotheses"]) == len(m.fiber(right)["hypotheses"]) == 2,
            "Count-fold fixture")
    require(m.analyze(left)["selection"]["chosen_context"] == 1
            and m.analyze(right)["selection"]["chosen_context"] == 0, "Count summary wrongly preserved policy")
    repeated = m.append_answer(left, 0, 0)
    require(len(repeated) == 2 and m.fiber(repeated) == m.fiber(left), "Redundant occurrence was collapsed")
    contradiction = m.append_answer(left, 0, 1)
    require(m.analyze(contradiction)["selection"]["status"] == "INCONSISTENT", "Contradiction treated as unknown source")
    require(m.predictions(contradiction, 1) == {"disposition": "NONE", "values": []}, "Vacuous prediction")
    context_sensitive = [{"context": 0, "answer": 0}, {"context": 1, "answer": 1}]
    require(m.fiber(context_sensitive)["hypotheses"] == ["01"], "Context distinction lost")
    hidden_change = [{"context": 0, "answer": functions["01"](0)},
                     {"context": 1, "answer": functions["10"](1)}]
    require(m.fiber(hidden_change)["hypotheses"] == ["00"], "Hidden-change false-fit control")
    require(functions["01"](1) != functions["00"](1), "Unique fit was confused with changing process")
    capacity = [{"context": 0, "answer": 0} for _ in range(32)]
    require(m.fiber(capacity)["hypotheses"] == ["00", "01"], "History boundary")
    require(m.analyze(capacity)["history"] == capacity, "Boundary occurrences lost")
    rejects(lambda: m.append_answer(capacity, 1, 1))
    rejects(lambda: m.fiber(capacity+[capacity[0]]))
    mutable = m.append_answer(left, 1, 1)
    mutable[0]["answer"] = 1
    require(left == [{"context": 0, "answer": 0}], "Append aliases caller records")
    for bad in (True, False, 1.0, -1, 2, "0", None):
        rejects(lambda value=bad: m.answer("00", value))
        rejects(lambda value=bad: m.append_answer([], 0, value))
    for bad in (True, 0, "0", "02", "000", None):
        rejects(lambda value=bad: m.answer(value, 0))
    for bad in (None, {}, "00", [{"context": 0}], [{"context": 0, "answer": 0, "note": "extra"}]):
        rejects(lambda value=bad: m.fiber(value))
    for bad in (("00", "00"), ("02",), "00", None):
        rejects(lambda value=bad: m.minimax(value))
    rejects(lambda: m.append_answer([], 0, "undecided"))

    return {"status": "PASS", "evidence_grade": "EXHAUSTIVE_FINITE_TEST_AT_REPORTED_BOUNDS",
            "schema": "context-communication-check/v1", "python_optimized": not __debug__, "counts": counts,
            "bounds": {"hypotheses": 4, "contexts": 2, "answers": 2, "all_history_lengths": "0..6",
                       "append_successor_lengths": "1..7", "all_candidate_subsets": 16,
                       "api_history_capacity": 32, "capacity_cases": "selected 32/33-record controls, not all histories"},
            "limits": ["fixed deterministic truthful source assumption", "no empirical response model",
                       "no diagnosis, therapy or communication-efficacy claim", "no speedup claim"],
            "source_hashes": {f"experimental/context-communication/{name}": hashlib.sha256((HERE/name).read_bytes()).hexdigest()
                              for name in ("README.md", "model.py", "example.py", "check.py")}}


def _write(output, value):
    payload = json.dumps(value, indent=2, allow_nan=False) + "\n"
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(payload, encoding="utf-8")
    return payload


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.output and not args.output.is_absolute():
        parser.error("--output must be absolute")
    _write(args.output, {"status": "PENDING", "schema": "context-communication-check/v1"})
    try:
        result = run_checks()
        if type(result) is not dict or result.get("status") != "PASS":
            raise RuntimeError("Checker did not produce PASS")
    except BaseException as exc:
        result = {"status": "FAIL", "schema": "context-communication-check/v1", "error_type": type(exc).__name__}
        print(_write(args.output, result))
        return 1
    print(_write(args.output, result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
