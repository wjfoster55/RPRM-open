"""Finite deterministic future quotients and shortest separating words.

Failure is observed through a distinct tag. All state/operation tables are
complete finite declarations; no black-box callbacks are evaluated here.
"""
from __future__ import annotations
from collections import deque
from dataclasses import dataclass
from types import MappingProxyType
from .core import atom, carrier, require, total_table


@dataclass(frozen=True)
class Machine:
    states: tuple
    actions: tuple
    observation: object
    transitions: object

    def __post_init__(self):
        carrier(self.states)
        require(type(self.actions) is tuple and all(type(a) is str and a for a in self.actions)
                and len(set(self.actions)) == len(self.actions), "Actions need distinct nonempty names")
        total_table(self.states, self.observation, "Observation")
        require(type(self.transitions) is dict
                and all(type(a) is str for a in self.transitions)
                and set(self.transitions) == set(self.actions),
                "Every action needs exactly one transition table")
        tables = {}
        for action, table in self.transitions.items():
            require(type(table) is dict, "Partial transition must be a dictionary")
            for source, target in table.items():
                atom(source)
                atom(target)
                require(source in self.states and target in self.states, "Transition outside carrier")
            tables[action] = MappingProxyType(dict(table))
        object.__setattr__(self, "observation", MappingProxyType(dict(self.observation)))
        object.__setattr__(self, "transitions", MappingProxyType(tables))


def observe_word(machine, state, word):
    require(type(machine) is Machine, "Machine required")
    atom(state)
    require(state in machine.states and type(word) is tuple, "Admitted state and finite tuple word required")
    require(all(type(a) is str and a in machine.actions for a in word), "Unknown action")
    current = state
    for action in word:
        table = machine.transitions[action]
        if current not in table:
            return ("FAIL",)
        current = table[current]
    return ("OK", machine.observation[current])


def shortest_witness(machine, left, right):
    """Return ONE(shortlex-least word) or NONE after complete product exploration."""
    require(type(machine) is Machine, "Machine required")
    atom(left)
    atom(right)
    require(left in machine.states and right in machine.states, "Unadmitted comparison states")
    failure = object()
    def observation(state):
        return ("FAIL",) if state is failure else ("OK", machine.observation[state])
    def step(state, action):
        return failure if state is failure else machine.transitions[action].get(state, failure)
    queue = deque([(left, right, ())])
    seen = {(left, right)}
    while queue:
        a, b, word = queue.popleft()
        if observation(a) != observation(b):
            return {"status": "ONE", "word": word, "visited_pairs": len(seen)}
        for action in machine.actions:
            pair = (step(a, action), step(b, action))
            if pair not in seen:
                seen.add(pair)
                queue.append((*pair, word + (action,)))
    return {"status": "NONE", "word": None, "visited_pairs": len(seen)}


def stable_refinement(machine, retained=None):
    """Coarsest stable refinement of retained information plus present observation."""
    require(type(machine) is Machine, "Machine required")
    if retained is None:
        retained = {state: 0 for state in machine.states}
    total_table(machine.states, retained, "Retained information")
    def labels(signatures):
        identifiers = {}
        return {state: identifiers.setdefault(signatures[state], len(identifiers))
                for state in machine.states}
    blocks = labels({x: (retained[x], machine.observation[x]) for x in machine.states})
    rounds = 0
    while True:
        signature = {}
        for state in machine.states:
            successors = tuple(("OK", blocks[machine.transitions[a][state]])
                               if state in machine.transitions[a] else ("FAIL",)
                               for a in machine.actions)
            signature[state] = (blocks[state], successors)
        refined = labels(signature)
        if refined == blocks:
            break
        blocks = refined
        rounds += 1
    classes = tuple(tuple(x for x in machine.states if blocks[x] == label)
                    for label in range(len(set(blocks.values()))))
    observation = {label: machine.observation[group[0]] for label, group in enumerate(classes)}
    transitions = {action: {label: blocks[machine.transitions[action][group[0]]]
                            for label, group in enumerate(classes)
                            if group[0] in machine.transitions[action]}
                   for action in machine.actions}
    quotient = Machine(tuple(range(len(classes))), machine.actions, observation, transitions)
    return {"classes": classes, "encoding": blocks, "machine": quotient, "strict_rounds": rounds}


def future_quotient(machine):
    """Canonical labels follow source enumeration; the partition is semantic."""
    return stable_refinement(machine)
