"""E34, p=5: exact admission and trace-target certificate, NOT a Sha computation.

The CM critical-value trace is deliberately absent. This script must return
OPEN, even when all finite admission checks succeed. See ODD_PRIME_ATTEMPT.md.
No saved Sha value, curve database, rank backend, or old receipt is read.
"""
from datetime import datetime, timezone
from fractions import Fraction
from hashlib import sha256
import argparse
import json
from math import gcd
from pathlib import Path


def poly_add(a, b):
    c = dict(a)
    for k, v in b.items():
        c[k] = c.get(k, 0)+v
    return {k: v for k, v in c.items() if v}


def poly_mul(a, b):
    c = {}
    for k, v in a.items():
        for j, w in b.items():
            c[k+j] = c.get(k+j, 0)+v*w
    return {k: v for k, v in c.items() if v}


def poly_derivative(a):
    return {k-1: k*v for k, v in a.items() if k*v}


def neg(a):
    return {k: -v for k, v in a.items()}


def finite_points(a4, prime):
    return [(x, y) for x in range(prime) for y in range(prime)
            if (y*y-x*x*x-a4*x) % prime == 0]


def run():
    prime, a4, a4_isogenous = 5, -1156, 289
    points, isogenous_points = finite_points(a4, prime), finite_points(a4_isogenous, prime)
    assert len(points)+1 == len(isogenous_points)+1 == 8
    discriminant = -64*a4**3
    assert discriminant % prime != 0
    assert (prime+1-(len(points)+1)) % prime != 0
    assert gcd(prime, 6*4) == 1 and prime % 4 == 1
    assert 2*2+1 == prime and 2*2 % prime == prime-1

    # Degree-two isogeny E': y^2=x^3+289x -> E34. Laurent-polynomial
    # substitution proves the target equation away from x=0; O,(0,0)
    # are the usual two-point kernel and projective extensions.
    b = a4_isogenous
    source_rhs = {3: 1, 1: b}
    x_image = {1: 1, -1: b}
    y_multiplier = {0: 1, -2: -b}
    y_image_square = poly_mul(source_rhs, poly_mul(y_multiplier, y_multiplier))
    target_rhs = poly_add(poly_mul(poly_mul(x_image, x_image), x_image),
                          {k: -4*b*v for k, v in x_image.items()})
    assert poly_add(y_image_square, neg(target_rhs)) == {}
    assert poly_derivative(x_image) == y_multiplier
    assert -4*b == a4

    # E' has D'=-289, so the odd-D conductor formula in CLS I gives
    # f=4*17=68. The theorem use is a cited input, not inferred from this count.
    conductor_generator = 68
    unit_count = sum(gcd(a*a+b*b, conductor_generator) == 1
                     for a in range(conductor_generator)
                     for b in range(conductor_generator))
    assert unit_count == 2048 and unit_count//8 == 256
    assert 4*conductor_generator**2 == 18496
    alpha_norm = 2  # alpha(E')=1+i in the stated period convention.
    assert gcd(prime, alpha_norm*conductor_generator) == 1

    # CLS II V'=2W^3, W'=V, V^2=W^4-D': take two more derivatives.
    d_prime = -289
    a0 = {3: 2}
    a1 = poly_add(poly_mul(poly_derivative(poly_derivative(a0)), {4: 1, 0: -d_prime}),
                  poly_mul(poly_derivative(a0), {3: 2}))
    assert a1 == {5: 24, 1: 3468}
    target_scale = Fraction(16, conductor_generator**5)
    assert gcd(target_scale.numerator*target_scale.denominator, prime) == 1

    return {
        'status': 'OPEN',
        'finite_admission_checks': 'COMPLETED',
        'sha_5_primary_conclusion': 'NOT_ESTABLISHED',
        'critical_value_valuation': None,
        'utc': datetime.now(timezone.utc).isoformat(),
        'source_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
        'curve': {'a_invariants': [0,0,0,a4,0], 'D_in_CLS_notation': 1156,
                  'CM_field': 'Q(i)', 'CM_order': 'Z[i]', 'discriminant': discriminant},
        'prime_admission': {'p': prime, 'good_reduction_discriminant_residue': discriminant % prime,
            'affine_points_mod_p': points, 'projective_point_count': len(points)+1,
            'a_p': prime+1-(len(points)+1), 'ordinary': True, 'non_anomalous': True,
            'split_factorization': '5=(2+i)(2-i)', 'roots_of_unity_count': 4,
            'prime_to_6w': True,
            'residual_surjectivity': 'NOT_A_HYPOTHESIS_OF_CLS_I_THEOREM_2_2'},
        'accepted_inputs': {'algebraic_rank': 2, 'analytic_rank': 2,
            'source': '../../bsd-rank-two-01/ARITHMETIC_PROOF.md and its analytic certificates',
            'rank_parity_agrees': True, 'no_saved_receipt_read': True},
        'isogenous_model': {'a_invariants': [0,0,0,289,0], 'D_in_CLS_notation': -289,
            'degree': 2, 'x_map': 'x+289/x', 'y_map': 'y*(1-289/x^2)',
            'curve_identity_laurent_residual': {}, 'differential_pullback_factor': 1,
            'K_isomorphism_scale_fourth_power': -4,
            'projective_point_count_mod_5': len(isogenous_points)+1},
        'CM_conductor': {'model_used_for_CLS_I_Lemma_3_2': 'D=-289',
            'f_generator': 68, 'f_norm': 4624, 'f1_generator': '34*(1-i)',
            'phi_f_exact_unit_count': unit_count, 'rho_minimal_polynomial_degree': 256,
            'norm_conductor_consistency': '4*N(f)=18496'},
        'period_normalization': {'differential': 'dx/(2y)',
            'Omega_plus': 'least positive real period, not total real integral',
            'Omega_plus_isogenous_over_original': 2,
            'alpha_isogenous': '1+i', 'beta_isogenous': 68,
            'c5_original_over_isogenous': 32},
        'trace_target': {'rho': 'positive sqrt(wp(Omega_plus(Eprime)/68,L_Eprime))',
            'field': 'ray class field of Q(i) modulo 34*(1-i)',
            'A1_polynomial': {'5': 24, '1': 3468},
            'T': 'Trace(2*rho^5+289*rho)',
            'critical_value_original': '+/-16*T/68^5',
            'v5_equivalence': 'v5(c5_plus(E34))=v5(T)',
            'sufficient_exact_residues_mod_125': [25,50,75,100],
            'rho_polynomial': None, 'trace_T_mod_125': None,
            'Newton_sum_target': 'T=2*s5+289*s1, using the first five monic polynomial coefficients'},
        'missing_calculation': 'Construct and certify the correct degree-256 rho polynomial or equivalent trace algebra, then compute T modulo125',
        'literature_limit': {'targeted_search_queries_used': 4, 'maximum': 4,
            'provided_papers_read': ['https://arxiv.org/pdf/1005.4206','https://arxiv.org/pdf/0901.3832']},
        'not_established': ['v5(c5_plus)=2', 'Sha[5^infinity]=0', 'full Sha finiteness', 'full BSD identity'],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    data = run()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(data, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({'status': data['status'], 'finite_admission_checks': data['finite_admission_checks'],
        'p': 5, 'rho_degree': 256, 'trace_modulus': 125,
        'trace_T_mod_125': None, 'sha_5_primary_conclusion': 'NOT_ESTABLISHED',
        'output': str(args.output)}, indent=2))


if __name__ == '__main__':
    main()
