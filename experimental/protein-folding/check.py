"""Cold finite check with an independent brute-direction oracle.

Run with Python 3.10+: python -I -B check.py [--output ABSOLUTE_JSON].
The checker reconstructs its oracle from local bytes and uses no network/data.
"""
import argparse
import hashlib
import importlib.util
import itertools
import json
import os
from uuid import uuid4
from pathlib import Path

HERE = Path(__file__).resolve().parent
PUBLIC_PREFIX = "experimental/protein-folding/"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def oracle_paths(length):
    # Deliberately enumerate all 4**(length-1) words, including collision words.
    # Complex coordinates and an all-pairs check differ from model's path growth.
    result = set()
    for word in itertools.product((1, 1j, -1, -1j), repeat=length - 1):
        vertices = [0j]
        for step in word:
            vertices.append(vertices[-1] + step)
        if len(set(vertices)) == length:
            result.add(tuple((int(z.real), int(z.imag)) for z in vertices))
    return result


def oracle_contacts(path):
    # Enumerate occupied undirected grid edges; remove backbone edges.
    occupancy = {complex(x, y): index for index, (x, y) in enumerate(path)}
    edges = set()
    for vertex, index in occupancy.items():
        for delta in (1, 1j):
            neighbor = occupancy.get(vertex + delta)
            if neighbor is not None and abs(index - neighbor) > 1:
                edges.add(tuple(sorted((index, neighbor))))
    return tuple(sorted(edges))


def oracle_energy(sequence, contacts):
    score = 0
    for i, j in contacts:
        if sequence[i] == "H" and sequence[j] == "H":
            score -= 1
    return score


def _run_checks(args):
    source_files = tuple(HERE / name for name in ("README.md", "model.py", "example.py", "check.py"))
    spec = importlib.util.spec_from_file_location("checked_hp_model", HERE / "model.py")
    model = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(model)
    counts = {"sequences": 0, "sequence_path_energies": 0, "minimizer_fibers": 0,
              "path_contact_maps": 0, "reflection_checks": 0, "extension_actions": 0,
              "completion_queries": 0, "prefix_minimizer_fibers": 0,
              "admission_rejections": 0}
    walk_counts = []
    expected_walk_counts = (1, 4, 12, 36, 100, 284, 780, 2172)
    for length in range(1, 9):
        expected = oracle_paths(length)
        actual = model.enumerate_paths(length)
        require(len(actual) == len(set(actual)), "duplicate enumerated path")
        require(set(actual) == expected, "path enumeration differs from brute-direction oracle")
        require(len(actual) == expected_walk_counts[length - 1], "walk count control")
        walk_counts.append({"residues": length, "oriented_paths": len(actual),
                            "oracle_direction_words": 4 ** (length - 1)})
        contacts = {path: oracle_contacts(path) for path in expected}
        for path in actual:
            require(model.contact_map(path) == contacts[path], "contact-map oracle mismatch")
            counts["path_contact_maps"] += 1
            reflected = tuple((x, -y) for x, y in path)
            require(model.mirror(path) == reflected and reflected in expected,
                    "mirror missing or wrong")
            require(model.mirror(reflected) == path and contacts[reflected] == contacts[path],
                    "reflection involution or contact preservation failed")
            counts["reflection_checks"] += 1
            for action, step in (("E", 1), ("N", 1j), ("W", -1), ("S", -1j)):
                endpoint = complex(*path[-1]) + step
                point = (int(endpoint.real), int(endpoint.imag))
                successor = None if length == 8 or point in path else path + (point,)
                require(model.extend(path, action) == successor, "extension action mismatch")
                counts["extension_actions"] += 1
        for letters in itertools.product("HP", repeat=length):
            sequence = "".join(letters)
            scores = {path: oracle_energy(sequence, cm) for path, cm in contacts.items()}
            for path, score in scores.items():
                require(model.energy(sequence, path) == score, "energy oracle mismatch")
                counts["sequence_path_energies"] += 1
            minimum = min(scores.values())
            winners = {path for path, value in scores.items() if value == minimum}
            result = model.minimizers(sequence)
            require(result["minimum_energy"] == minimum and set(result["paths"]) == winners,
                    "incomplete or incorrect minimizer fiber")
            require(result["count"] == len(winners)
                    and result["disposition"] == ("ONE" if len(winners) == 1 else "MANY"),
                    "minimizer fiber disposition mismatch")
            counts["sequences"] += 1
            counts["minimizer_fibers"] += 1

    # Check every prefix occurring in the <=5-residue carrier, every possible
    # toy energy and impossible integer controls, against explicit filtering.
    for length in range(1, 6):
        paths = oracle_paths(length)
        sequence = "H" * length
        prefixes = {path[:size] for path in paths for size in range(1, length + 1)}
        for prefix in prefixes:
            eligible = {path: oracle_energy(sequence, oracle_contacts(path))
                        for path in paths if path[:len(prefix)] == prefix}
            lowest = min(eligible.values())
            winners = {path for path, score in eligible.items() if score == lowest}
            result = model.minimizers(sequence, prefix)
            require(result["minimum_energy"] == lowest and set(result["paths"]) == winners
                    and result["count"] == len(winners)
                    and result["disposition"] == ("ONE" if len(winners) == 1 else "MANY"),
                    "prefix-constrained minimizer fiber mismatch")
            counts["prefix_minimizer_fibers"] += 1
            for target in (None, *range(-length, 2)):
                expected = {path for path in paths if path[:len(prefix)] == prefix
                            and (target is None or oracle_energy(sequence, oracle_contacts(path)) == target)}
                result = model.completions(sequence, prefix, target)
                tag = "NONE" if not expected else "ONE" if len(expected) == 1 else "MANY"
                require(set(result["paths"]) == expected and result["count"] == len(expected)
                        and result["disposition"] == tag, "completion fiber mismatch")
                counts["completion_queries"] += 1

    straight = ((0, 0), (1, 0), (2, 0))
    bent = ((0, 0), (1, 0), (1, 1))
    require(model.contact_map(straight) == model.contact_map(bent) == (), "loss witness projection")
    require(model.energy("PPP", straight) == model.energy("PPP", bent) == 0, "loss witness energy")
    require(model.extend(straight, "W") is None and model.extend(bent, "W") is not None,
            "contact-map enabledness hostile case must distinguish")
    require(model.mirror(bent) != bent, "reflections must remain distinct")
    require(model.minimizers("HPPH")["minimum_energy"] == -1
            and model.minimizers("HPPH")["count"] == 8, "worked example control")
    require(model.completions("HPPH", target_energy=1)["disposition"] == "NONE", "NONE control")
    require(model.completions("H", target_energy=0)["disposition"] == "ONE", "ONE control")

    invalid_calls = [
        lambda: model.admit_sequence(""), lambda: model.admit_sequence("HPX"),
        lambda: model.admit_sequence("hp"), lambda: model.admit_sequence("H" * 9),
        lambda: model.admit_sequence(None), lambda: model.enumerate_paths(True),
        lambda: model.enumerate_paths([]), lambda: model.enumerate_paths(1.0),
        lambda: model.enumerate_paths(0), lambda: model.enumerate_paths(9),
        lambda: model.admit_path(((0, 0), (1, 0), (0, 0))),
        lambda: model.admit_path(((0, 0), (2, 0))),
        lambda: model.admit_path(((1, 0),)), lambda: model.admit_path(((False, 0),)),
        lambda: model.admit_path(((0.0, 0),)), lambda: model.admit_path(()),
        lambda: model.energy("HP", ((0, 0),)),
        lambda: model.completions("H", prefix=((0, 0), (1, 0))),
        lambda: model.completions("H", target_energy=True),
        lambda: model.completions("H", target_energy=0.0),
        lambda: model.extend(((0, 0),), "NE")]
    for call in invalid_calls:
        try:
            call()
        except ValueError:
            counts["admission_rejections"] += 1
        else:
            raise RuntimeError("malformed or out-of-carrier input admitted")

    result = {"status": "PASS", "evidence_grade": "EXHAUSTIVE_FINITE_TEST",
              "context": "hp-square-oriented-v1; NEWLY_PROPOSED; 1..8 residues",
              "scope": "all 510 H/P sequences and every oriented path through 8 residues; complete minimizer fibers",
              "limitations": "no biological inference, physical folding dynamics, speedup, or coverage beyond 8 residues",
              "checks": counts, "walk_counts": walk_counts,
              "hostile_controls": ["same contact map and energy, different W enabledness",
                                   "distinct mirror retained", "self-collision rejected",
                                   "impossible energy gives NONE", "single H gives ONE"],
              "source_hashes": {PUBLIC_PREFIX + path.name: hashlib.sha256(path.read_bytes()).hexdigest()
                                for path in source_files}}
    payload = json.dumps(result, indent=2) + "\n"
    _publish(args.output, result)
    print(payload, end="")


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


if __name__ == "__main__":
    main()
