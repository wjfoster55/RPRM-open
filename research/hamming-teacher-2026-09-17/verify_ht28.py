"""Independent census of the 35 three-check panels on F_2^3.

Does not import the 12 September panel verifier or the SAT pilot.
Null names are those frozen in NULL.md. This script computes the fibers;
it does not choose a predicted count after seeing them.
"""
from itertools import combinations, product
import json
from pathlib import Path

CHECKS = tuple(range(1, 8))
SOURCES = tuple(range(8))
BASIS = (1, 2, 4)
SWAP_XOR = (1, 2, 5)
SWAP_SUM = (1, 2, 3)
HOSTILE_LINE = (1, 2, 3)

HERE = Path(__file__).resolve().parent


def bit_dot(functional, source):
    return (functional & source).bit_count() % 2


def fibers(panel):
    buckets = {}
    for source in SOURCES:
        key = tuple(bit_dot(u, source) for u in panel)
        buckets.setdefault(key, []).append(source)
    return buckets


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


def error_syndrome(word):
    result = 0
    for position in range(7):
        if word & (1 << position):
            result ^= position + 1
    return result


def require(condition, name):
    if not condition:
        raise AssertionError(name)


def frozen_dependent_family():
    lines = set()
    for a, b in combinations(CHECKS, 2):
        third = a ^ b
        if third and third not in (a, b):
            lines.add(frozenset((a, b, third)))
    return lines


def hamming_weight_three_supports():
    supports = set()
    for word in range(128):
        if error_syndrome(word) != 0 or word.bit_count() != 3:
            continue
        support = frozenset(i + 1 for i in range(7) if word & (1 << i))
        supports.add(support)
    return supports


def panel_record(panel):
    family = fibers(panel)
    rank = linear_rank(panel)
    sizes = sorted(len(members) for members in family.values())
    covered = sorted(source for members in family.values() for source in members)
    answers = list(product((0, 1), repeat=3))
    empty_answers = [list(answer) for answer in answers if answer not in family]
    require(covered == list(SOURCES), 'each_panel_covers_all_sources')
    require(len(family) == 1 << rank, 'rank_matches_occupied_answers')
    require(set(sizes) == {1 << (3 - rank)}, 'rank_matches_fiber_size')
    return {
        'panel': list(panel),
        'rank': rank,
        'injective': rank == 3,
        'occupied_answers': len(family),
        'fiber_sizes': sizes,
        'empty_answers': empty_answers,
        'fibers': {''.join(str(bit) for bit in key): members for key, members in family.items()},
    }


def classify_count(count):
    names = {35: 'N_any', 7: 'N_lines', 21: 'N_pairs', 28: 'N_p5'}
    return names.get(count, 'UNNAMED_COUNT')


def main():
    require('verify_panels' not in globals(), 'no_old_verifier_name')
    triples = list(combinations(CHECKS, 3))
    require(len(triples) == 35, 'complete_triple_carrier')

    records = [panel_record(panel) for panel in triples]
    injective = [tuple(record['panel']) for record in records if record['injective']]
    failing = [tuple(record['panel']) for record in records if not record['injective']]
    fail_sets = {frozenset(panel) for panel in failing}

    q1_count = len(injective)
    q1_null = classify_count(q1_count)
    q2_yes = fail_sets == frozen_dependent_family()
    q4_yes = fail_sets == hamming_weight_three_supports()

    swap_xor = panel_record(SWAP_XOR)
    swap_sum = panel_record(SWAP_SUM)
    hostile = panel_record(HOSTILE_LINE)
    require(tuple(swap_sum['panel']) == tuple(hostile['panel']), 'hostile_is_named_sum_swap')

    if swap_xor['injective'] and not swap_sum['injective']:
        q3_null = 'N_p6'
    elif swap_xor['injective'] and swap_sum['injective']:
        q3_null = 'N_both'
    elif (not swap_xor['injective']) and (not swap_sum['injective']):
        q3_null = 'N_neither'
    else:
        q3_null = 'UNNAMED_SWAP'

    shared_zero = hostile['fibers'].get('000', [])
    require(len(records) == 35, 'census_length')

    receipt = {
        'status': 'PASS',
        'evidence_grade': 'FINITE_EXHAUSTIVE_CENSUS',
        'claim': 'HT-28',
        'Q1': {
            'question': 'how many of 35 triples are injective',
            'count': q1_count,
            'failing': len(failing),
            'surviving_null': q1_null,
            'rejected_nulls': [name for name in ('N_any', 'N_lines', 'N_pairs', 'N_p5') if name != q1_null],
            'disposition': f'ONE({q1_count})',
        },
        'Q2': {
            'question': 'Fail equals {{a,b,a XOR b} : distinct nonzero a,b}',
            'surviving_null': 'N_q2_yes' if q2_yes else 'N_q2_no',
            'disposition': 'ONE(yes)' if q2_yes else 'NONE',
            'failing_triples': [list(panel) for panel in failing],
        },
        'Q3': {
            'SWAP_XOR': {k: swap_xor[k] for k in ('panel', 'injective', 'rank', 'fiber_sizes', 'fibers')},
            'SWAP_SUM': {k: swap_sum[k] for k in ('panel', 'injective', 'rank', 'fiber_sizes', 'fibers')},
            'HOSTILE_LINE': {k: hostile[k] for k in ('panel', 'injective', 'rank', 'fiber_sizes', 'fibers')},
            'hostile_shared_000': shared_zero,
            'surviving_null': q3_null,
            'disposition': 'ONE(N_p6)' if q3_null == 'N_p6' else f'ONE({q3_null})',
        },
        'Q4': {
            'question': 'Fail equals Hamming-7 weight-three supports',
            'surviving_null': 'N_q4_yes' if q4_yes else 'N_q4_no',
            'disposition': 'ONE(yes)' if q4_yes else 'NONE',
            'hamming_codewords': sum(1 for word in range(128) if error_syndrome(word) == 0),
        },
        'limits': (
            'Complete census of linear checks on F_2^3 only. Not SAT, not Hamming-8, '
            'not a free source toggle, not a general soundness proof of this script.'
        ),
    }
    (HERE / 'CENSUS.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
    return receipt


if __name__ == '__main__':
    print(json.dumps(main(), indent=2))
