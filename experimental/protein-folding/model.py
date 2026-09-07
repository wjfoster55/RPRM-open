"""NEWLY PROPOSED finite HP lattice toy; no biological prediction claim.

The complete carrier consists of origin-anchored, oriented, self-avoiding
square-lattice paths with 1..8 vertices. Rotations and mirrors are retained.
Only the Python standard library is required.
"""
from functools import lru_cache

MAX_LENGTH = 8
DIRECTIONS = {"E": (1, 0), "N": (0, 1), "W": (-1, 0), "S": (0, -1)}


def admit_sequence(sequence):
    if (not isinstance(sequence, str) or not 1 <= len(sequence) <= MAX_LENGTH
            or any(letter not in "HP" for letter in sequence)):
        raise ValueError("sequence must contain 1..8 uppercase H/P letters")
    return sequence


def admit_path(path):
    if not isinstance(path, (tuple, list)) or not 1 <= len(path) <= MAX_LENGTH:
        raise ValueError("path must contain 1..8 vertices")
    points = []
    for point in path:
        if (not isinstance(point, (tuple, list)) or len(point) != 2
                or any(type(coordinate) is not int for coordinate in point)):
            raise ValueError("vertices must be pairs of integers, excluding booleans")
        points.append(tuple(point))
    points = tuple(points)
    if points[0] != (0, 0):
        raise ValueError("first vertex must be the origin")
    if len(set(points)) != len(points):
        raise ValueError("path must be self-avoiding")
    if any(abs(a[0] - b[0]) + abs(a[1] - b[1]) != 1
           for a, b in zip(points, points[1:])):
        raise ValueError("consecutive vertices must have unit lattice bonds")
    return points


def enumerate_paths(length):
    """Return every admitted oriented path of this length, without symmetry reduction."""
    if type(length) is not int or not 1 <= length <= MAX_LENGTH:
        raise ValueError("length must be an integer in 1..8")
    return _enumerate_paths(length)


@lru_cache(maxsize=8)
def _enumerate_paths(length):
    level = [((0, 0),)]
    for _ in range(length - 1):
        next_level = []
        for path in level:
            x, y = path[-1]
            for dx, dy in DIRECTIONS.values():
                point = (x + dx, y + dy)
                if point not in path:
                    next_level.append(path + (point,))
        level = next_level
    return tuple(sorted(level))


def contact_map(path):
    """All nonconsecutive adjacent occurrence-index pairs, using zero-based indices."""
    path = admit_path(path)
    return tuple((i, j) for i in range(len(path)) for j in range(i + 2, len(path))
                 if abs(path[i][0] - path[j][0]) + abs(path[i][1] - path[j][1]) == 1)


def energy(sequence, path):
    """Dimensionless toy energy: minus the number of nonconsecutive H-H contacts."""
    sequence = admit_sequence(sequence)
    path = admit_path(path)
    if len(sequence) != len(path):
        raise ValueError("sequence and path lengths must agree")
    return -sum(sequence[i] == sequence[j] == "H" for i, j in contact_map(path))


def fiber(paths):
    """Tag a completed finite path family; caller is responsible for completeness."""
    members = tuple(sorted(set(paths)))
    return {"disposition": "NONE" if not members else "ONE" if len(members) == 1 else "MANY",
            "count": len(members), "paths": members}


def _admit_query(sequence, prefix, target_energy):
    sequence = admit_sequence(sequence)
    prefix = admit_path(((0, 0),) if prefix is None else prefix)
    if len(prefix) > len(sequence):
        raise ValueError("prefix cannot be longer than the sequence")
    if target_energy is not None and type(target_energy) is not int:
        raise ValueError("target energy must be an integer, excluding booleans")
    return sequence, prefix


def completions(sequence, prefix=None, target_energy=None):
    """Solve the complete path fiber at a fixed sequence, prefix, and optional energy.

    An integer energy with no solution returns NONE. Invalid input raises
    ValueError. No cutoff, timeout, sampling, or inferred unique selection occurs.
    """
    sequence, prefix = _admit_query(sequence, prefix, target_energy)
    return fiber(path for path in enumerate_paths(len(sequence))
                 if path[:len(prefix)] == prefix
                 and (target_energy is None or energy(sequence, path) == target_energy))


def minimizers(sequence, prefix=None):
    """Return the minimum over all compatible paths and the entire minimizer fiber."""
    sequence, prefix = _admit_query(sequence, prefix, None)
    candidates = completions(sequence, prefix)["paths"]
    if not candidates:
        return {"minimum_energy": None, **fiber(())}
    scores = {path: energy(sequence, path) for path in candidates}
    minimum = min(scores.values())
    return {"minimum_energy": minimum,
            **fiber(path for path, score in scores.items() if score == minimum)}


def extend(path, direction):
    """Partial action: append one vertex; return None for collision or length cap.

    An unknown action or malformed source is an admission error. The action
    changes only a geometric path; extending an HP state also needs a supplied
    new H/P occurrence, which is deliberately a separate port.
    """
    path = admit_path(path)
    if not isinstance(direction, str) or direction not in DIRECTIONS:
        raise ValueError("direction must be E, N, W, or S")
    if len(path) == MAX_LENGTH:
        return None
    dx, dy = DIRECTIONS[direction]
    point = (path[-1][0] + dx, path[-1][1] + dy)
    return None if point in path else path + (point,)


def mirror(path):
    """Reflection across the x axis; an involution on the admitted carrier."""
    return tuple((x, -y) for x, y in admit_path(path))
