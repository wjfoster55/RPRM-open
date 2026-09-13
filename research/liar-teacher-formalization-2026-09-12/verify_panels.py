"""Finite, independently enumerated fixtures for the written panel claims.

No historical verifier is imported. Run with -I -B; output is JSON on stdout.
Source vectors, dual functionals and error positions use separate functions.
"""
from collections import Counter, defaultdict
from itertools import combinations, permutations, product
import json


def linear_readout(functional, source):
    return (functional & source).bit_count() % 2


def fibers(dimension, functionals):
    out = defaultdict(list)
    for source in range(1 << dimension):
        out[tuple(linear_readout(u, source) for u in functionals)].append(source)
    return dict(out)


def linear_rank(vectors):
    pivots = {}
    for v in vectors:
        while v:
            p = v.bit_length() - 1
            if p not in pivots:
                pivots[p] = v
                break
            v ^= pivots[p]
    return len(pivots)


def error_syndrome(word):
    result = 0
    for position in range(7):
        if word & (1 << position):
            result ^= position + 1
    return result


def extension(word):
    return word | ((word.bit_count() % 2) << 7)


def code_distance(words):
    return min((a ^ b).bit_count() for a, b in combinations(words, 2))


def main():
    checks = Counter()

    def require(condition, family):
        if not condition:
            raise AssertionError(f'Failed fixture: {family}')
        checks[family] += 1

    panel_spectra = Counter()
    dependent = []
    for count in range(8):
        for panel in combinations(range(1, 8), count):
            family = fibers(3, panel)
            r = linear_rank(panel)
            require(len(family) == 1 << r, 'rank_vs_enumerated_fibers')
            require({len(f) for f in family.values()} == {1 << (3-r)}, 'rank_vs_enumerated_fibers')
            # All admitted answer words, including empty preimages.
            for reply in product((0, 1), repeat=count):
                direct = [x for x in range(8) if all(linear_readout(u, x) == y for u, y in zip(panel, reply))]
                require(family.get(reply, []) == direct, 'complete_reply_fibers')
            if count == 3:
                panel_spectra[r] += 1
                if r == 2:
                    dependent.append(panel)
            if count >= 4:
                require(len(family) == 8, 'all_four_or_more_separate')
    require(panel_spectra == {2: 7, 3: 28}, 'triple_census')
    bases = [p for p in permutations(range(1, 8), 3) if len(fibers(3, p)) == 8]
    require(len(bases) == 168, 'ordered_basis_census')

    for a, b in permutations(range(1, 8), 2):
        valid = [c for c in range(1, 8) if len(fibers(3, (a, b, c))) == 8]
        require(len(valid) == 4, 'anchored_replacement')
        require(a ^ b not in valid, 'anchored_replacement')
        for c in valid:
            require(set(valid) == {c, c ^ a, c ^ b, c ^ a ^ b}, 'anchored_replacement')
            for x in range(8):
                require(linear_readout(c ^ a, x) == (linear_readout(c, x) ^ linear_readout(a, x)), 'calibrated_composition')
            old = {0, a, b, a ^ b}
            new = {0, a, c, a ^ c}
            coset = {x ^ c for x in old}
            require(old & new == {0, a}, 'primal_quartet_exchange')
            require(not (old & coset) and old | coset == set(range(8)), 'primal_expansion')
    for pair in combinations(range(1, 4), 2):
        require(len(fibers(2, pair)) == 4, 'two_of_three_on_four_states')

    # Include newcomers inside the old span and the degenerate two-role cases.
    for a, b in permutations(range(1, 8), 2):
        old = {0, a, b, a ^ b}
        for c in range(8):
            coset = {x ^ c for x in old}
            new = {0, a, c, a ^ c}
            require((not (old & coset)) == (c not in old), 'primal_coset_iff')
            if c in {0, a}:
                require(new == {0, a}, 'primal_degenerate_hostile')
            elif c in old:
                require(new == old, 'primal_inside_span_hostile')

    for old, new, x in product(range(8), repeat=3):
        old_relative = x ^ old
        new_relative = old_relative ^ old ^ new
        require(new_relative == x ^ new, 'anchor_transport')
        for u in range(1, 8):
            require(linear_readout(u, new_relative) == (linear_readout(u, old_relative) ^ linear_readout(u, old ^ new)), 'character_transport')
    for relative in range(8):
        require({relative ^ anchor for anchor in range(8)} == set(range(8)), 'forgotten_anchor_hostile')

    hamming = [w for w in range(128) if error_syndrome(w) == 0]
    simplex = [sum(linear_readout(u, x) << (u-1) for u in range(1, 8)) for x in range(8)]
    require(len(hamming) == 16 and code_distance(hamming) == 3, 'hamming_code')
    require(len(set(simplex)) == 8 and code_distance(simplex) == 4, 'simplex_code')
    require({w.bit_count() for w in simplex if w} == {4}, 'simplex_code')
    orthogonal = [v for v in range(128) if all((v & c).bit_count() % 2 == 0 for c in hamming)]
    require(set(orthogonal) == set(simplex), 'simplex_hamming_duality')
    weight_three = {tuple(i+1 for i in range(7) if w & (1 << i)) for w in hamming if w.bit_count() == 3}
    require(weight_three == set(dependent), 'dependent_triples_are_hamming_words')
    for c in hamming:
        require(error_syndrome(c) == 0, 'single_error_decode')
        for i in range(7):
            damaged = c ^ (1 << i)
            require(error_syndrome(damaged) == i+1, 'single_error_decode')
            require(damaged ^ (1 << (error_syndrome(damaged)-1)) == c, 'single_error_decode')
        for i, j in combinations(range(7), 2):
            damaged = c ^ (1 << i) ^ (1 << j)
            alias = error_syndrome(damaged)
            corrected = damaged ^ (1 << (alias-1))
            require(corrected != c and corrected in hamming, 'double_error_alias_hostile')
    extended = [extension(c) for c in hamming]
    require(len(set(extended)) == 16 and code_distance(extended) == 4, 'extended_code')
    for c in extended:
        signatures = {(error_syndrome(c), c.bit_count() % 2)}
        for i in range(8):
            damaged = c ^ (1 << i)
            signature = (error_syndrome(damaged), damaged.bit_count() % 2)
            require(signature == ((i+1) if i < 7 else 0, 1), 'extended_single_error_location')
            signatures.add(signature)
        require(len(signatures) == 9, 'extended_single_and_none_distinct')
    pair_classes = defaultdict(list)
    for i, j in combinations(range(8), 2):
        error = (1 << i) ^ (1 << j)
        syn = error_syndrome(error)
        pair_classes[syn].append((i, j))
        for c in extended:
            damaged = c ^ error
            require(damaged.bit_count() % 2 == 0 and error_syndrome(damaged) != 0, 'extended_double_detection')
    require(set(pair_classes) == set(range(1, 8)), 'double_error_fibers')
    require({len(v) for v in pair_classes.values()} == {4}, 'double_error_fibers')

    # A present-sufficient summary can fail a future or its enabledness.
    summary = lambda x: x & 1
    swap = lambda x: ((x & 1) << 1) | (x >> 1)
    require(summary(0) == summary(2) and summary(swap(0)) != summary(swap(2)), 'future_handoff_hostile')
    enabled = lambda x: (x >> 1) == 0
    require(summary(0) == summary(2) and enabled(0) != enabled(2), 'enabledness_handoff_hostile')
    nonlinear = lambda x: (x & 1) & ((x >> 1) & 1)
    require(all(nonlinear(x) == 0 for x in (1, 2, 4)) and nonlinear(3) == 1, 'unproved_newcomer_grammar_hostile')

    # Evaluate every Boolean function on three bits: translation invariances
    # form a subgroup. All affine relations, including empty, are included.
    stabilizer_sizes = Counter()
    for truth_mask in range(256):
        f = lambda x: (truth_mask >> x) & 1
        stabilizer = {t for t in range(8) if all(f(x) == f(x ^ t) for x in range(8))}
        require(0 in stabilizer and all(a ^ b in stabilizer for a in stabilizer for b in stabilizer), 'translation_stabilizer')
        stabilizer_sizes[len(stabilizer)] += 1
    require(all((x != 0) != ((x ^ 1) != 0) for x in (0, 1)), 'nonaffine_symmetry_hostile')
    matrix_fixtures = list(combinations(range(1, 8), 3))
    matrix_fixtures += [(), (0,)] + [(u,) for u in range(1, 8)]
    matrix_fixtures += [(0, u) for u in range(1, 8)] + [(u, u) for u in range(1, 8)]
    for masks in matrix_fixtures:
        for rhs in product((0, 1), repeat=len(masks)):
            allowed = {x for x in range(8) if tuple(linear_readout(u, x) for u in masks) == rhs}
            kernel = {x for x in range(8) if all(linear_readout(u, x) == 0 for u in masks)}
            actual = {t for t in range(8) if {x ^ t for x in allowed} == allowed}
            require(actual == (kernel if allowed else set(range(8))), 'affine_stabilizer_with_empty_control')
            for shift in range(8):
                shifted_rhs = tuple(r ^ linear_readout(u, shift) for r, u in zip(rhs, masks))
                transformed = {y for y in range(8) if tuple(linear_readout(u, y) for u in masks) == shifted_rhs}
                require(transformed == {x ^ shift for x in allowed}, 'affine_rechart')

    return {'status': 'PASS', 'evidence_grade': 'FINITE_EXHAUSTIVE_FIXTURES', 'assertions': sum(checks.values()),
            'checks_by_family': dict(checks), 'triple_census': {'separating': 28, 'dependent': 7, 'ordered_bases': 168},
            'dependent_triples': dependent, 'hamming_codewords': len(hamming), 'simplex_codewords': len(simplex),
            'extended_double_error_classes': {str(k): v for k, v in pair_classes.items()},
            'boolean_function_stabilizer_sizes': dict(stabilizer_sizes),
            'limits': 'Finite checks of the written contracts; no general soundness, SAT performance, or P-versus-NP claim.'}


if __name__ == '__main__':
    print(json.dumps(main(), indent=2))
