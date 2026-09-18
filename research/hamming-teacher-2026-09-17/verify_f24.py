"""Identity check: on F_2^4, a 4-check panel injects iff rank 4.

Nulls frozen in NULL-F24.md. This is not a new campaign. A matching
N_rank result means stop padding.
"""
from itertools import combinations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHECKS = tuple(range(1, 16))
SOURCES = tuple(range(16))
HOSTILE = (1, 2, 3, 4)
GL24 = 15 * 14 * 12 * 8
UNORDERED_BASES = GL24 // 24


def bit_dot(functional, source):
    return (functional & source).bit_count() % 2


def linear_rank(vectors):
    pivots = {}
    for vector in vectors:
        current = vector
        while current:
            pivot = current.bit_length() - 1
            if pivot not in pivots:
                pivots[pivot] = current
                break
            current ^= pivots[pivot]
    return len(pivots)


def injective(panel):
    seen = {}
    for source in SOURCES:
        key = tuple(bit_dot(u, source) for u in panel)
        if key in seen:
            return False
        seen[key] = source
    return len(seen) == 16


def require(condition, name):
    if not condition:
        raise AssertionError(name)


def main():
    triples = list(combinations(CHECKS, 4))
    require(len(triples) == 1365, 'complete_four_set_carrier')
    injective_count = 0
    rank_match = True
    for panel in triples:
        inj = injective(panel)
        full = linear_rank(panel) == 4
        if inj != full:
            rank_match = False
            break
        if inj:
            injective_count += 1
    require(rank_match, 'injective_iff_rank_4')
    require(injective_count == UNORDERED_BASES, 'count_is_gl_over_factorial')
    require(not injective(HOSTILE), 'hostile_1234_fails')
    require(linear_rank(HOSTILE) == 3, 'hostile_1234_rank_3')
    shared = [
        source for source in SOURCES
        if all(bit_dot(u, source) == 0 for u in HOSTILE)
    ]
    require(shared == [0, 8], 'hostile_kernel_0_and_8')

    if not rank_match:
        surviving = 'UNNAMED'
    elif injective_count == 1365:
        surviving = 'N_any'
    elif 1365 - injective_count == 7:
        surviving = 'N_fano_only'
    else:
        surviving = 'N_rank'

    receipt = {
        'status': 'PASS',
        'claim': 'F24-LIFT',
        'surviving_null': surviving,
        'injective_four_sets': injective_count,
        'total_four_sets': 1365,
        'unordered_bases_formula': UNORDERED_BASES,
        'hostile': {
            'panel': list(HOSTILE),
            'injective': False,
            'rank': 3,
            'zero_fiber': shared,
        },
        'padding': surviving == 'N_rank',
        'stop': surviving == 'N_rank',
        'limits': 'Same rank identity as HT-28. Not a new theorem.',
    }
    (HERE / 'CENSUS-F24.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
    return receipt


if __name__ == '__main__':
    print(json.dumps(main(), indent=2))
