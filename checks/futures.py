"""Independent bounded word enumeration for the finite future APIs."""
import argparse
import hashlib
import itertools as it
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from rprm.futures import Machine, observe_word, shortest_witness, future_quotient, stable_refinement
from rprm.core import AdmissionError


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def direct(table, observation, state, word):
    for action in word:
        if state not in table[action]:
            return ("FAIL",)
        state = table[action][state]
    return ("OK", observation[state])


def check_family():
    machines = pairs = words_checked = 0
    # All two-action partial machines through two states; three-state one-action machines.
    for n, actions in ((0, ("a",)), (1, ("a", "b")), (2, ("a", "b")), (3, ("a",))):
        states = tuple(range(n))
        words = [w for length in range(n) for w in it.product(actions, repeat=length)]
        for observations in it.product((0, 1), repeat=n):
            observation = dict(zip(states, observations))
            for flat in it.product(tuple(range(-1, n)), repeat=n * len(actions)):
                tables = {a: {x: flat[j*n+x] for x in states if flat[j*n+x] != -1}
                          for j, a in enumerate(actions)}
                machine = Machine(states, actions, observation, tables)
                folded = future_quotient(machine)
                for left in states:
                    for right in states:
                        expected = next((w for w in words if direct(tables, observation, left, w)
                                         != direct(tables, observation, right, w)), None)
                        result = shortest_witness(machine, left, right)
                        require(result["word"] == expected, "Shortest word disagrees with independent enumeration")
                        require((folded["encoding"][left] == folded["encoding"][right]) == (expected is None),
                                "Future classes disagree with all bounded word answers")
                        pairs += 1
                    for word in words:
                        expected = direct(tables, observation, left, word)
                        require(observe_word(machine, left, word) == expected, "Source execution mismatch")
                        require(observe_word(folded["machine"], folded["encoding"][left], word) == expected,
                                "Quotient changes tagged answer")
                        words_checked += 1
                machines += 1
    # Empty alphabet must still preserve current observations.
    empty = Machine((0, 1), (), {0: 0, 1: 1}, {})
    require(len(future_quotient(empty)["classes"]) == 2 and shortest_witness(empty, 0, 1)["word"] == (),
            "Empty alphabet dropped present observation")
    # Stable refinement must retain old distinctions even when all futures agree.
    m = Machine((0, 1, 2), ("a",), {0: 0, 1: 0, 2: 0}, {"a": {0: 0, 1: 2, 2: 2}})
    require(len(future_quotient(m)["classes"]) == 1, "Constant future quotient")
    require(len(stable_refinement(m, {0: 0, 1: 0, 2: 1})["classes"]) == 3,
            "Stable repair omitted retained-successor distinction")
    # Input mutation cannot change a declared machine.
    observation, table = {0: 0}, {"a": {0: 0}}
    m = Machine((0,), ("a",), observation, table)
    observation[0], table["a"][0] = 1, 99
    require(observe_word(m, 0, ("a",)) == ("OK", 0), "Declaration is mutable through caller inputs")
    class MutableAction(str):
        enabled = True
        __hash__ = str.__hash__
        def __eq__(self, other):
            return self.enabled and str.__eq__(self, other)
    for constructor in (
            lambda: Machine((0,), ("a",), {0: 0}, {MutableAction("a"): {0: 0}}),
            lambda: Machine((0,), ("a",), {False: 0}, {"a": {0: 0}}),
            lambda: Machine((0,), ("a",), {0: 0}, {"a": {False: 0}})):
        try:
            constructor()
        except AdmissionError:
            pass
        else:
            raise RuntimeError("Non-exact key alias accepted")
    return {"machines": machines, "state_pairs": pairs, "word_executions": words_checked,
            "boundary": "All binary observations and partial maps in the listed size/alphabet families; "
                        "direct word oracle through length n-1. General bound is a written theorem."}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = {"schema": "rprm-future-conformance/v1", "status": "PASS", "counts": check_family(),
              "source_hashes": {name: hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
                                for name in ("rprm/futures.py", "checks/futures.py", "rprm/core.py")}}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result))


if __name__ == "__main__":
    main()
