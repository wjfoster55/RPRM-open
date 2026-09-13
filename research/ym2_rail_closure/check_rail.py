"""New bounded exact controls; never imports or runs an earlier packet checker."""
from fractions import Fraction as F
from itertools import product, permutations
from pathlib import Path
import json
import sys

HERE = Path(__file__).resolve().parent
count = 0

def need(condition, label):
    global count
    count += 1
    if not condition:
        raise AssertionError(label)

def replace(x, i, a):
    return x[:i] + (a,) + x[i+1:]

def kernels(weights):
    def k(i, a, x):
        return F(weights[replace(x, i, a)],
                 sum(weights[replace(x, i, b)] for b in (0, 1)))
    return k

def ratio(k, i, x, y):
    return k(i, y[i], x) / k(i, x[i], x)

def walk(k, start, updates):
    x, value = start, F(1)
    for i, a in updates:
        y = replace(x, i, a)
        value *= ratio(k, i, x, y)
        x = y
    return x, value

def check_law(weights):
    states = tuple(weights)
    n = len(states[0])
    k = kernels(weights)
    total = sum(weights.values())
    reference = states[0]
    reconstructed = {}
    for x in states:
        for order in permutations(range(n)):
            end, value = walk(k, reference, [(i, x[i]) for i in order])
            need(end == x, "ordered path endpoint")
            need(value == F(weights[x], weights[reference]), "ordered ratio reconstruction")
            reconstructed[x] = value
        for i in range(n):
            need(sum(k(i, a, x) for a in (0, 1)) == 1, "conditional normalization")
            for j in range(i+1, n):
                xi, xj = replace(x, i, 1-x[i]), replace(x, j, 1-x[j])
                xij = replace(xi, j, 1-x[j])
                first = ratio(k, i, x, xi)*ratio(k, j, xi, xij)
                second = ratio(k, j, x, xj)*ratio(k, i, xj, xij)
                need(first == second, "rectangle closure")
        updates = [(i, 1-x[i]) for i in range(n)]
        updates += [(i, x[i]) for i in reversed(range(n))]
        end, loop = walk(k, x, updates)
        need(end == x and loop == 1, "reverse loop closure")
    normalizer = sum(reconstructed.values())
    for x in states:
        need(reconstructed[x]/normalizer == F(weights[x], total), "normalized joint reconstruction")

def compute():
    global count
    count = 0
    two = tuple(product((0, 1), repeat=2))
    families = 0
    for values in product(range(1, 5), repeat=4):
        check_law(dict(zip(two, values)))
        families += 1
    three = tuple(product((0, 1), repeat=3))
    for seed in range(16):
        values = [1+((seed+1)*(i+1)+i*i) % 13 for i in range(8)]
        check_law(dict(zip(three, values)))
        families += 1

    def incompatible(i, a, x):
        p = F(2, 3) if i == 0 and x[1] == 1 else F(1, 2)
        return p if a == 1 else 1-p
    for x in two:
        for i in range(2):
            need(sum(incompatible(i, a, x) for a in (0, 1)) == 1,
                 "hostile kernels remain normalized")
    _, forward = walk(incompatible, (0, 0), [(0, 1), (1, 1)])
    _, reverse = walk(incompatible, (0, 0), [(1, 1), (0, 1)])
    need((forward, reverse) == (1, 2), "exact incompatible path ratios")

    spin_states = tuple(product((-1, 1), repeat=2))
    gaps = []
    laws = []
    for base in (1, 2, 4, 2, 1):
        raw = {x: F(base) ** (x[0]*x[1]) for x in spin_states}
        z = sum(raw.values())
        p = {x: w/z for x, w in raw.items()}
        laws.append(p)
        t = F(base*base-1, base*base+1)
        def generator(f, x):
            result = F(0)
            for i in range(2):
                candidates = [replace(x, i, a) for a in (-1, 1)]
                z_cond = sum(p[y] for y in candidates)
                result += sum(p[y]*f(y) for y in candidates)/z_cond-f(x)
            return result
        basis = [lambda x: F(1), lambda x: F(x[0]+x[1]),
                 lambda x: F(x[0]-x[1]), lambda x: x[0]*x[1]-t]
        eigenvalues = [F(0), 1-t, 1+t, F(2)]
        for f, e in zip(basis, eigenvalues):
            for x in spin_states:
                need(generator(f, x) == -e*f(x), "heat-bath exact eigenfunction")
        gaps.append(str(1-t))
    need(gaps == ['1', '2/5', '2/17', '2/5', '1'], "closed-loop gap values")
    for x in spin_states:
        accumulated_square = F(1)
        for before, after in zip(laws, laws[1:]):
            multiplier_square = before[x]/after[x]
            need(after[x]*multiplier_square == before[x], "weighted chart isometry")
            accumulated_square *= multiplier_square
        need(accumulated_square == 1, "closed normalized chart loop")

    matrix = [[F(0), F(3,5), F(3,5)], [F(3,5), F(0), F(0)],
              [F(3,5), F(0), F(0)]]
    s, q = [F(3,2), F(1), F(1)], F(9,10)
    action = [sum(a*b for a, b in zip(row, s)) for row in matrix]
    need(max(map(sum, matrix)) == F(6,5), "ordinary row bound fails")
    for a, b in zip(action, s):
        need(a <= q*b, "weighted influence certificate")

    exact_v0, approximate_v0 = F(3, 7), F(2, 9)
    exact_v, approximate_v, total_h, total_e = exact_v0, approximate_v0, F(0), F(0)
    max_signed, norm_sum = F(0), F(0)
    for k in range(100):
        h = F((k % 5)-2, 13)
        e = F((-1)**k, 10)
        exact_v -= h
        approximate_v += -h+e
        total_h += h
        total_e += e
        need(exact_v-approximate_v == exact_v0-approximate_v0-total_e,
             "signed calibration defect identity")
        need(approximate_v == approximate_v0-total_h+total_e, "approximate chart telescope")
        max_signed = max(max_signed, abs(total_e))
        norm_sum += abs(e)
    need(max_signed == F(1,10) and norm_sum == 10 and total_e == 0,
         "signed cancellation differs from absolute accumulation")
    need(sum(F(1,10) for _ in range(100)) == 10, "equal-sign accumulation")

    # New minimal occurrence control illustrating, not replaying, the accepted FLICK contract.
    current = (0, 'A')
    def commit(expected_revision, payload):
        nonlocal current
        if expected_revision != current[0]:
            return False
        current = (current[0]+1, payload)
        return True
    need(commit(0, 'B'), "first accepted installation")
    need(not commit(0, 'C') and current == (1, 'B'), "same-parent competitor rejected")
    need(commit(1, 'A') and current == (2, 'A'), "equal payload new occurrence")
    need(not commit(0, 'stale') and current == (2, 'A'), "ABA stale revision rejected")
    need(current[1] == 'A' and current[0] != 0, "payload equality is not revision equality")

    return {
        'schema': 'ym2-rail-exact-controls-v1', 'status': 'PASS', 'assertions': count,
        'positive_joint_families': families, 'two_bit_weight_range': [1, 4],
        'three_bit_families': 16, 'incompatible_order_ratios': [str(forward), str(reverse)],
        'exact_auxiliary_loop_gaps': gaps,
        'weighted_matrix_max_row': '6/5', 'weighted_certificate_q': '9/10',
        'signed_prefix_bound': str(max_signed), 'sum_absolute_defects': str(norm_sum),
        'aba_final_state': list(current), 'old_checkers_run': False,
        'evidence_ceiling': 'Exact finite controls, not a formal proof of smooth SU(2), an actual vacuum construction, cryptographic security, or a uniform continuum gap.'
    }

def main():
    result = compute()
    output = HERE/'RESULTS.json'
    if sys.argv[1:] == ['--record']:
        if output.exists():
            raise RuntimeError('Receipt already exists; refuse accidental overwrite')
        output.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    elif sys.argv[1:]:
        raise SystemExit('usage: check_rail.py [--record]')
    else:
        expected = json.loads(output.read_text(encoding='utf-8'))
        if expected != result:
            raise AssertionError('Saved complete receipt differs from new computation')
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
