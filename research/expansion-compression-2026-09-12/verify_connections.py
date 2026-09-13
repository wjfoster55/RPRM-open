"""Exact finite checks; TEST-SPEC.md was written before this implementation."""
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import product
from math import comb, gcd
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parent


def moore_classes(size, actions, observation):
    """Partition from observation and full successor signatures, no gcd used."""
    labels = [observation(h) for h in range(size)]
    rounds = 0
    while True:
        signatures = [(labels[h], tuple(labels[(h+k) % size] for k in actions))
                      for h in range(size)]
        codes = {signature: i for i, signature in enumerate(dict.fromkeys(signatures))}
        updated = [codes[s] for s in signatures]
        rounds += 1
        if updated == labels:
            break
        labels = updated
    classes = defaultdict(set)
    for h, label in enumerate(labels):
        classes[label].add(h)
    return {frozenset(cell) for cell in classes.values()}, rounds


def main():
    checks = Counter()

    def require(condition, family):
        if not condition:
            raise AssertionError(family)
        checks[family] += 1

    histograms = []
    for n in range(13):
        fibers = defaultdict(list)
        phases = set()
        for word in product((0, 1), repeat=n):
            literal = sum((Fraction(b) - Fraction(3, 5) for b in word), Fraction(0))
            k = sum(word)
            require(literal == Fraction(5*k-3*n, 5), 'rational_stack')
            winding, fifth = 0, 0
            for b in word:
                carry, fifth = divmod(fifth + 5*b - 3, 5)
                winding += carry
            require(literal == winding + Fraction(fifth, 5), 'incremental_winding_phase')
            require((winding, fifth) == divmod(5*k-3*n, 5), 'canonical_winding_phase')
            phases.add(fifth)
            fibers[k].append(word)
            if n < 12:
                for b in (0, 1):
                    direct_next = literal + Fraction(b) - Fraction(3, 5)
                    require(direct_next == Fraction(5*(k+b)-3*(n+1), 5), 'compressed_next_bit')
        require(set(fibers) == set(range(n+1)), 'all_sum_values')
        for k, cell in fibers.items():
            require(len(cell) == comb(n, k), 'complete_binomial_fiber')
        require(phases == {(-3*n) % 5}, 'phase_forgets_count')
        histograms.append({'n': n, 'histories': 1 << n, 'sum_classes': n+1,
                           'fixed_n_minimum_bits': n.bit_length(),
                           'phase_classes': len(phases),
                           'max_history_fiber': max(map(len, fibers.values()))})

    require(Fraction(-3, 5) % 1 == Fraction(2, 5) % 1 and
            Fraction(-3, 5) != Fraction(2, 5), 'phase_total_hostile')
    require(Fraction(5*0-3*1, 5) == Fraction(5*3-3*6, 5) and
            Fraction(-3, 5) / 1 != Fraction(-3, 5) / 6, 'sum_without_n_mean_hostile')
    require(sum((0, 1)) == sum((1, 0)) and (0, 1)[0] != (1, 0)[0], 'order_receiver_hostile')

    size, initial_g = 60, 12
    action_stages = [(12,), (12, 18), (12, 18, 20),
                     (12, 18, 20, 25), (12, 18, 20), (12,)]
    stages = []
    for actions in action_stages:
        g = gcd(size, *actions)
        actual, rounds = moore_classes(size, actions, lambda h: h // initial_g)
        expected = {frozenset(range(start, start+g)) for start in range(0, size, g)}
        require(actual == expected, 'independent_moore_vs_gcd_partition')
        for h in range(size):
            q = h // g
            require(h == g*q + h % g, 'full_reopen')
            require(h // initial_g == q // (initial_g // g), 'original_peek_decodes')
            for step in actions:
                require(((h+step) % size) // g == (q + step//g) % (size//g), 'quotient_update')
        stages.append({'actions': actions, 'g': g, 'classes': len(actual),
                       'minimum_fixed_bits': (len(actual)-1).bit_length(),
                       'source_fiber': g, 'moore_iterations': rounds})
    require([row['classes'] for row in stages] == [5, 10, 30, 60, 30, 5], 'grow_then_coarsen')
    for before, after in zip(stages, stages[1:]):
        old_g, new_g = before['g'], after['g']
        for h in range(size):
            old_q, new_q = h // old_g, h // new_g
            if old_g >= new_g:
                factor = old_g // new_g
                tag = (h % old_g) // new_g
                require(new_q == factor*old_q + tag, 'mixed_radix_refinement')
                require(old_q == new_q//factor and tag == new_q % factor, 'migration_inverse')
            else:
                require(new_q == old_q // (new_g // old_g), 'retired_future_coarsening')
    # h=0 and h=6 had the same old Peek; adding +18 separates them.
    require(0//12 == 6//12 and 18//12 != 24//12, 'stale_operator_quotient_hostile')

    valid_boolean_tables = []
    for table in product((0, 1), repeat=4):
        works = all(table[2*int(a == 0)+int(b == 0)] == int((a ^ b) == 0)
                    for a, b in product(range(4), repeat=2))
        if works:
            valid_boolean_tables.append(table)
    require(not valid_boolean_tables, 'terminal_identity_fold_noncompositional')
    require((1 ^ 1) == 0 and (1 ^ 2) != 0, 'identity_fold_explicit_hostile')

    equal = {(0, 0), (1, 1)}
    opposite = {(0, 1), (1, 0)}
    marginals = lambda relation: tuple({row[i] for row in relation} for i in range(2))
    require(marginals(equal) == marginals(opposite), 'same_coordinate_supports')
    require({sum(row) for row in equal} == {0, 2} and
            {sum(row) for row in opposite} == {1}, 'joint_sum_hostile')

    def variance(rows):
        values = [sum(row) for row in rows]
        mean = Fraction(sum(values), len(values))
        return sum(((v-mean)**2 for v in values), Fraction(0)) / len(values)
    independent = list(product((0, 1), repeat=2))
    require(variance(independent) == Fraction(1, 2) and
            variance(sorted(equal)) == 1, 'independence_vs_shared_source')

    return {'status': 'PASS', 'evidence_grade': 'FINITE_EXACT_CONNECTION_CHECKS',
            'assertions': sum(checks.values()), 'checks': dict(checks),
            'stack_histograms': histograms, 'operator_stages': stages,
            'boolean_identity_update_tables_tested': 16,
            'valid_boolean_identity_update_tables': len(valid_boolean_tables),
            'limits': 'Declared finite scopes only; source histories remain distinct; no general complexity theorem.'}


if __name__ == '__main__':
    receipt = {'implementation_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
               'specification_sha256': hashlib.sha256((ROOT/'TEST-SPEC.md').read_bytes()).hexdigest()}
    try:
        receipt.update(main())
    except Exception as exc:
        receipt.update(status='FAIL', error={'type': type(exc).__name__, 'message': str(exc)})
        raise
    finally:
        (ROOT/'RESULTS.json').write_text(json.dumps(receipt, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({'status': receipt['status'], 'assertions': receipt['assertions'],
                      'operator_class_counts': [row['classes'] for row in receipt['operator_stages']]}, indent=2))
