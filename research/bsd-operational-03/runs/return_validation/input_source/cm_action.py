"""Fresh finite CM-action certificate for E34 at conductor 68.

cm_group() returns sorted pairs (a,b), representing a+b*i modulo 68.
The proof identifying this finite subgroup with the arithmetic Galois image
is in TRACE_FORMULA_AUDIT.md. This program alone proves finite identities.
Standard library only; it computes no Sha value or critical-value trace.
"""
from collections import deque
from hashlib import sha256
from math import gcd, isqrt
from pathlib import Path
import argparse
import json

MODULUS = 68
MODEL = (0, 0, 0, -1156, 0)
SPLIT_PRIMES = (5, 13)


def multiply(z, w):
    """Gaussian multiplication modulo the fixed conductor."""
    a, b = z
    c, d = w
    return ((a*c-b*d) % MODULUS, (a*d+b*c) % MODULUS)


def generated_subgroup(generators):
    seen = {(1, 0)}
    queue = deque(seen)
    while queue:
        value = queue.popleft()
        for generator in generators:
            product = multiply(value, generator)
            if product not in seen:
                seen.add(product)
                queue.append(product)
    return seen


def point_count(prime):
    """Count the same fixed E34, independently of CM predictions."""
    square_counts = [0]*prime
    for y in range(prime):
        square_counts[y*y % prime] += 1
    return 1 + sum(square_counts[(x*x*x-1156*x) % prime]
                   for x in range(prime))


def build_certificate():
    generators = []
    prime_rows = []
    discriminant = -64*(-1156)**3
    for prime in SPLIT_PRIMES:
        assert prime % 4 == 1 and discriminant % prime != 0
        count = point_count(prime)
        trace = prime+1-count
        assert trace % 2 == 0
        real = trace//2
        imaginary = isqrt(prime-real*real)
        assert imaginary > 0 and real*real+imaginary*imaginary == prime
        additions = [(real % MODULUS, imaginary % MODULUS),
                     (real % MODULUS, (-imaginary) % MODULUS)]
        generators.extend(additions)
        prime_rows.append({
            'prime': prime, 'point_count': count, 'a_prime': trace,
            'CM_Frobenius_real_part': real,
            'CM_Frobenius_imaginary_absolute_value': imaginary,
            'generators_mod_68': additions,
            'generated_order_so_far': len(generated_subgroup(generators)),
        })
    subgroup = generated_subgroup(generators)
    gaussian_units = {(1, 0), (67, 0), (0, 1), (0, 67)}
    all_units = {(a, b) for a in range(MODULUS) for b in range(MODULUS)
                 if gcd(a*a+b*b, MODULUS) == 1}
    covered = {multiply(u, g) for u in gaussian_units for g in subgroup}
    assert len(subgroup) == 512
    assert subgroup <= all_units
    assert len(all_units) == 2048 and covered == all_units
    assert subgroup & gaussian_units == {(1, 0)}
    # Membership, inverse and closure are checked as finite sets, not merely
    # inferred from the traversal's name or its expected cardinality.
    for g in subgroup:
        norm_inverse = pow((g[0]*g[0]+g[1]*g[1]) % MODULUS, -1, MODULUS)
        inverse = (g[0]*norm_inverse % MODULUS,
                   -g[1]*norm_inverse % MODULUS)
        assert inverse in subgroup and multiply(g, inverse) == (1, 0)
        assert all(multiply(g, h) in subgroup for h in subgroup)
    frobenius_five = (67, 2)
    value = (1, 0)
    order = 0
    while True:
        value = multiply(value, frobenius_five)
        order += 1
        if value == (1, 0):
            break
        assert order <= len(subgroup)
    assert order == 16
    # The involution fixing Y/(2X): a=f/(1+i)-1=33-34i mod68.
    involution = (33, 34)
    assert involution in subgroup and involution != (1, 0)
    assert multiply(involution, involution) == (1, 0)
    assert all(multiply(u, g) != g for u in gaussian_units-{(1, 0)}
               for g in subgroup)
    return {
        'status': 'EXACT_FINITE_CM_ACTION_CERTIFICATE_COMPLETED',
        'model': MODEL, 'modulus': MODULUS,
        'source_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
        'prime_rows': prime_rows, 'generators': generators,
        'group': sorted(subgroup), 'group_order': len(subgroup),
        'full_unit_group_order': len(all_units),
        'mu4_intersection': sorted(subgroup & gaussian_units),
        'mu4_times_G_equals_full_unit_group': covered == all_units,
        'frobenius_5_order': order,
        'involution_fixing_r': involution,
        'arithmetic_identification': 'WRITTEN_CM_AND_CLASS_FIELD_PROOF_REQUIRED',
        'critical_trace_computed': False,
        'evidence_grade': 'EXACT_FINITE_ARITHMETIC_WITH_CITED_THEOREM_DEPENDENCIES',
    }


def cm_group():
    """Return the freshly certified CM image as 512 pairs modulo 68."""
    return tuple(tuple(z) for z in build_certificate()['group'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = build_certificate()
    if args.output is not None:
        if args.output.exists():
            raise FileExistsError('Use a fresh certificate path')
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k: result[k] for k in
                     ('status', 'prime_rows', 'group_order', 'full_unit_group_order',
                      'mu4_intersection', 'mu4_times_G_equals_full_unit_group',
                      'frobenius_5_order', 'involution_fixing_r')}, indent=2))


if __name__ == '__main__':
    main()
