"""Synthetic transcripts, complete fibers, and explicit model-failure controls."""
import argparse
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("communication_model", HERE / "model.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.output and not args.output.is_absolute():
        parser.error("--output must be absolute")
    history = []
    steps = [m.analyze(history)]
    supplied_rule = "01"
    while steps[-1]["selection"]["chosen_context"] is not None:
        question = steps[-1]["selection"]["chosen_context"]
        history = m.append_answer(history, question, m.answer(supplied_rule, question))
        steps.append(m.analyze(history))
    changed = [{"context": 0, "answer": 0}, {"context": 0, "answer": 1}]
    count_left = [{"context": 0, "answer": 0}]
    count_right = [{"context": 1, "answer": 0}]
    omitted_context_left = [{"context": 0, "answer": 0}, {"context": 1, "answer": 1}]
    result = {"status": "EXPERIMENTAL_NEWLY_PROPOSED", "schema": "context-communication-example/v1",
              "assumptions": ["one fixed member of the four-rule family", "binary truthful answers",
                              "stable meaning of each context", "both questions available at equal unit cost"],
              "worked_example": {"supplied_synthetic_rule": supplied_rule, "steps": steps},
              "changed_response_control": m.analyze(changed),
              "count_fold_control": {"left": m.analyze(count_left), "right": m.analyze(count_right),
                                     "same_survivor_count": 2,
                                     "conclusion": "A count loses which context remains informative."},
              "omit_context_control": {"history": omitted_context_left,
                                       "lawful_fiber": m.fiber(omitted_context_left),
                                       "conclusion": "Different contexts can lawfully return different answers; deleting context labels creates a false conflict."},
              "binary_port_boundary": {"excluded_answer": "undecided",
                                       "action": "Admission error; declare a richer response carrier before continuing."},
              "hidden_change_control": {"observations": [{"context": 0, "answer": 0}, {"context": 1, "answer": 0}],
                                        "fixed_model_fiber": m.fiber([{"context": 0, "answer": 0}, {"context": 1, "answer": 0}]),
                                        "alternative_process": "First response from rule01, second response from rule10.",
                                        "conclusion": "A unique fixed-rule fit does not prove the process stayed fixed."}}
    payload = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    print(payload)


if __name__ == "__main__":
    main()
