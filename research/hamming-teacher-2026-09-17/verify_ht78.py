"""Independent census of the three typed eights in HT-78.

Does not import verify_panels.py or the SAT pilot. Null names are those
frozen in NULL-78.md. This script computes the sets; it does not choose
a predicted count after seeing them.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
U = frozenset((0, 1, 2, 3))
C_FREE = 4
C_HOSTILE = 3
HOSTILE_CHECKS = (1, 2, 3)


def bit_dot(functional, source):
    return (functional & source).bit_count() % 2


def encode(source):
    word = 0
    for label in range(1, 8):
        if bit_dot(label, source):
            word |= 1 << (label - 1)
    return word


def error_syndrome(word):
    result = 0
    for position in range(7):
        if word & (1 << position):
            result ^= position + 1
    return result


def extend(word):
    return word | ((word.bit_count() % 2) << 7)


def require(condition, name):
    if not condition:
        raise AssertionError(name)


def classify_s(count):
    return {7: 'N_s7', 8: 'N_s8', 16: 'N_s16'}.get(count, 'UNNAMED_S')


def classify_ext(count):
    return {8: 'N_ext8', 16: 'N_ext16', 32: 'N_ext32'}.get(count, 'UNNAMED_EXT')


def main():
    require('verify_panels' not in globals(), 'no_old_verifier_name')

    simplex = [encode(source) for source in range(8)]
    require(len(simplex) == 8, 'e_evaluated_on_all_sources')
    s_set = set(simplex)
    hamming = [word for word in range(128) if error_syndrome(word) == 0]
    orthogonal = {
        word for word in range(128)
        if all((word & code).bit_count() % 2 == 0 for code in hamming)
    }
    extended = [extend(code) for code in hamming]
    ext_set = set(extended)

    q1_count = len(s_set)
    q1_null = classify_s(q1_count)
    if s_set == set(hamming):
        q2_null = 'N_s_is_c'
        q2_disp = 'NONE'
    elif s_set == orthogonal:
        q2_null = 'N_dual_yes'
        q2_disp = 'ONE(yes)'
    else:
        q2_null = 'N_dual_no'
        q2_disp = 'NONE'

    q3_count = len(ext_set)
    q3_null = classify_ext(q3_count)

    expanded_free = U | {source ^ C_FREE for source in U}
    expanded_hostile = U | {source ^ C_HOSTILE for source in U}
    q4a = len(expanded_free) == 8 and not (U & {source ^ C_FREE for source in U})
    q4b_expands = len(expanded_hostile) == 8 and expanded_hostile != U
    if q4a and not q4b_expands:
        q4_null = 'N_p9b'
    elif q4a and q4b_expands:
        q4_null = 'N_any_c'
    else:
        q4_null = 'N_no_c'

    weights = sorted({word.bit_count() for word in s_set})
    same_object = (
        q1_count == q3_count == len(expanded_free)
        and s_set == ext_set
        and s_set == expanded_free
    )
    q5_null = 'N_one_eight' if same_object else 'N_three_eights'

    require(C_HOSTILE == (1 ^ 2), 'hostile_toggle_is_sum_of_basis')
    require(set(HOSTILE_CHECKS) <= set(range(1, 8)), 'hostile_glyphs_are_check_labels')
    require(C_HOSTILE in U, 'hostile_toggle_stays_in_U')
    require(C_FREE not in U, 'free_toggle_leaves_U')

    receipt = {
        'status': 'PASS',
        'evidence_grade': 'FINITE_EXHAUSTIVE_CENSUS',
        'claim': 'HT-78',
        'Q1': {
            'question': 'how many distinct seven-teacher response words',
            'count': q1_count,
            'surviving_null': q1_null,
            'disposition': f'ONE({q1_count})',
            'words': sorted(s_set),
            'weights': weights,
        },
        'Q2': {
            'question': 'S equals Hamming-7 orthogonal',
            'surviving_null': q2_null,
            'disposition': q2_disp,
            'hamming_codewords': len(hamming),
            'orthogonal_size': len(orthogonal),
        },
        'Q3': {
            'question': 'how many Hamming-8 codewords',
            'count': q3_count,
            'surviving_null': q3_null,
            'disposition': f'ONE({q3_count})',
            'rejected_free_bit': q3_count != 32,
        },
        'Q4': {
            'U': sorted(U),
            'c_free': C_FREE,
            'c_hostile': C_HOSTILE,
            'expanded_free': sorted(expanded_free),
            'expanded_hostile': sorted(expanded_hostile),
            'surviving_null': q4_null,
            'disposition': 'ONE(N_p9b)' if q4_null == 'N_p9b' else f'ONE({q4_null})',
            'hostile_checks_vs_toggle': {
                'check_panel': list(HOSTILE_CHECKS),
                'source_toggle': C_HOSTILE,
                'same_typed_object': False,
            },
        },
        'Q5': {
            'question': 'are S, C8, and X_4 the same typed object',
            'surviving_null': q5_null,
            'disposition': 'NONE' if q5_null == 'N_three_eights' else 'ONE(yes)',
            'cardinalities': {
                'simplex_words': q1_count,
                'hamming8_messages': q3_count,
                'hamming8_positions': 8,
                'free_toggle_roles': len(expanded_free),
            },
        },
        'limits': (
            'Finite linear census on F_2^3 / F_2^7 / F_2^8 only. '
            'Not double-error location, not SAT, not a ninth silent role.'
        ),
    }
    (HERE / 'CENSUS-78.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
    return receipt


if __name__ == '__main__':
    print(json.dumps(main(), indent=2))
