"""A law with several apertures, and a shortest future distinction."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from rprm.core import Sort, Port, Value, Relation, solve
from rprm.futures import Machine, shortest_witness, future_quotient

# This is addition restricted to the explicitly finite carrier, with no wrap.
number = Sort("bounded_integer", tuple(range(5)))
addition = Relation(tuple(Port(p, number) for p in ("left", "right", "sum")),
                    frozenset((a, b, a+b) for a in number.values for b in number.values if a+b in number.values))
for supplied in ({"left": 1, "right": 2}, {"left": 1, "sum": 3}, {"sum": 3}, {"left": 4, "sum": 0}):
    answer = solve(addition, {p: Value(number, v) for p, v in supplied.items()})
    print(supplied, "=>", answer.disposition, answer.ports, sorted(answer.members))

# Present observations agree at p and q; a later observation distinguishes them.
machine = Machine(("p", "q", "u", "v", "r"), ("step",),
                  {"p": 0, "q": 0, "u": 0, "v": 0, "r": 1},
                  {"step": {"p": "u", "q": "v", "u": "r", "v": "v", "r": "r"}})
print("shortest distinguishing word:", shortest_witness(machine, "p", "q"))
print("future-equivalence classes:", future_quotient(machine)["classes"])
