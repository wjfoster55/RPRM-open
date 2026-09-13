"""Exact, bounded calibration of homogeneous SU(2) joint Gram dynamics.

Python 3.10+, standard library only. A and v have color rows and spatial
columns. Coefficient n means the ordinary coefficient of t**n (derivative/n!).
The source solver uses nested color cross products. The independent joint
solver advances only S,T,U using polynomial matrix convolution; it never
reconstructs A or v and never calls the source solver.

Run: python -I -B research/ym2_joint_scaling/check_joint.py
Regenerate this directory's receipt explicitly with --write-results.
Nothing in the frozen YM2 packet is imported, executed, or modified.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations
from math import factorial
from pathlib import Path
import argparse
import json


DEGREE = 4
LABELS = ("S", "T", "U")


def matrix(rows):
    return tuple(tuple(F(x) for x in row) for row in rows)


def zero(rows=3, columns=3):
    return tuple(tuple(F(0) for _ in range(columns)) for _ in range(rows))


def identity(n=3):
    return matrix([[int(i == j) for j in range(n)] for i in range(n)])


def diagonal(values):
    return matrix([[values[i] if i == j else 0 for j in range(3)] for i in range(3)])


def transpose(a):
    return tuple(zip(*a))


def add(a, b):
    return tuple(tuple(x + y for x, y in zip(ar, br)) for ar, br in zip(a, b))


def scale(c, a):
    return tuple(tuple(c * x for x in row) for row in a)


def sub(a, b):
    return add(a, scale(-1, b))


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), F(0))


def multiply(a, b):
    return tuple(tuple(dot(ar, bc) for bc in transpose(b)) for ar in a)


def trace(a):
    return sum((a[i][i] for i in range(len(a))), F(0))


def cross(a, b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2],
            a[0]*b[1]-a[1]*b[0])


def vector_add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def vector_scale(c, a):
    return tuple(c * x for x in a)


def rank(a):
    work = [list(row) for row in a]
    pivot_row = 0
    for col in range(len(work[0])):
        pivot = next((r for r in range(pivot_row, len(work)) if work[r][col]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        divisor = work[pivot_row][col]
        work[pivot_row] = [x/divisor for x in work[pivot_row]]
        for r in range(len(work)):
            if r != pivot_row:
                factor = work[r][col]
                work[r] = [x-factor*y for x, y in zip(work[r], work[pivot_row])]
        pivot_row += 1
        if pivot_row == len(work):
            break
    return pivot_row


def determinant(a):
    if len(a) == 1:
        return a[0][0]
    return sum(((-1)**j * a[0][j] * determinant(tuple(
        tuple(row[k] for k in range(len(a)) if k != j) for row in a[1:]))
        for j in range(len(a))), F(0))


def inverse(a):
    n = len(a)
    work = [list(a[i])+list(identity(n)[i]) for i in range(n)]
    for col in range(n):
        pivot = next((r for r in range(col, n) if work[r][col]), None)
        if pivot is None:
            raise ValueError("singular matrix: inverse chart unavailable")
        work[col], work[pivot] = work[pivot], work[col]
        divisor = work[col][col]
        work[col] = [x/divisor for x in work[col]]
        for r in range(n):
            if r != col:
                factor = work[r][col]
                work[r] = [x-factor*y for x, y in zip(work[r], work[col])]
    return tuple(tuple(row[n:]) for row in work)


def series_product(a, b, n):
    out = zero(len(a[0]), len(b[0][0]))
    for k in range(n+1):
        if k < len(a) and n-k < len(b):
            out = add(out, multiply(a[k], b[n-k]))
    return out


def series_cross(a, b, n):
    out = (F(0), F(0), F(0))
    for k in range(n+1):
        if k < len(a) and n-k < len(b):
            out = vector_add(out, cross(a[k], b[n-k]))
    return out


def source_acceleration_coefficient(a, n, g):
    """Independent force: g^2 sum_j A_j cross (A_j cross A_i)."""
    columns = [[transpose(coefficient)[i] for coefficient in a] for i in range(3)]
    result = []
    for i in range(3):
        value = (F(0), F(0), F(0))
        for j in range(3):
            inner = [series_cross(columns[j], columns[i], k) for k in range(n+1)]
            value = vector_add(value, series_cross(columns[j], inner, n))
        result.append(vector_scale(g*g, value))
    return transpose(result)


def source_series(a0, v0, g=F(1), degree=DEGREE):
    a, v = [a0], [v0]
    for n in range(degree):
        acceleration = source_acceleration_coefficient(a, n, g)
        next_a = scale(F(1, n+1), v[n])
        next_v = scale(F(1, n+1), acceleration)
        a.append(next_a)
        v.append(next_v)
    return {"A": a, "v": v}


def gram(a, v):
    return {"S": multiply(transpose(a), a), "T": multiply(transpose(a), v),
            "U": multiply(transpose(v), v)}


def c_from_s(s, g):
    return scale(g*g, sub(scale(trace(s), identity()), s))


def joint_rhs(joint, g):
    s, t, u = (joint[label] for label in LABELS)
    c = c_from_s(s, g)
    return {"S": add(t, transpose(t)), "T": sub(u, multiply(s, c)),
            "U": scale(-1, add(multiply(c, t), multiply(transpose(t), c)))}


def joint_series(initial, g=F(1), degree=DEGREE):
    """Closed polynomial recurrence on S,T,U, with no source reconstruction."""
    s, t, u = ([initial[label]] for label in LABELS)
    for n in range(degree):
        c = [c_from_s(coefficient, g) for coefficient in s]
        tt = [transpose(coefficient) for coefficient in t]
        next_s = scale(F(1, n+1), add(t[n], tt[n]))
        next_t = scale(F(1, n+1), sub(u[n], series_product(s, c, n)))
        next_u = scale(F(-1, n+1), add(series_product(c, t, n),
                                                series_product(tt, c, n)))
        s.append(next_s)
        t.append(next_t)
        u.append(next_u)
    return dict(zip(LABELS, (s, t, u)))


def gram_series(source):
    a, v = source["A"], source["v"]
    at, vt = [transpose(x) for x in a], [transpose(x) for x in v]
    return {"S": [series_product(at, a, n) for n in range(len(a))],
            "T": [series_product(at, v, n) for n in range(len(a))],
            "U": [series_product(vt, v, n) for n in range(len(a))]}


def source_energy_series(source, g, volume):
    a, v = source["A"], source["v"]
    columns = [[transpose(coefficient)[i] for coefficient in a] for i in range(3)]
    magnetic = [[series_cross(columns[i], columns[j], n) for n in range(len(a))]
                for i, j in combinations(range(3), 2)]
    electric, potential = [], []
    for n in range(len(a)):
        electric.append(volume/2 * sum((dot(v[k][r], v[n-k][r])
                        for k in range(n+1) for r in range(3)), F(0)))
        potential.append(volume*g*g/2 * sum((dot(b[k], b[n-k])
                         for b in magnetic for k in range(n+1)), F(0)))
    return {"electric": electric, "magnetic": potential,
            "total": [e+b for e, b in zip(electric, potential)]}


def joint_energy_series(joint, g, volume):
    s, u = joint["S"], joint["U"]
    electric = [volume*trace(coefficient)/2 for coefficient in u]
    magnetic = [volume*g*g/4 * (sum((trace(s[k])*trace(s[n-k])
                 for k in range(n+1)), F(0))-trace(series_product(s, s, n)))
                for n in range(len(s))]
    return {"electric": electric, "magnetic": magnetic,
            "total": [e+b for e, b in zip(electric, magnetic)]}


def source_gauss_series(source):
    a, v = source["A"], source["v"]
    at, vt = [transpose(x) for x in a], [transpose(x) for x in v]
    return [sub(series_product(a, vt, n), series_product(v, at, n))
            for n in range(len(a))]


def block_gram(joint):
    s, t, u = (joint[label] for label in LABELS)
    tt = transpose(t)
    return tuple(s[i]+t[i] for i in range(3))+tuple(tt[i]+u[i] for i in range(3))


OMEGA = tuple(zero()[i]+identity()[i] for i in range(3)) + tuple(
    scale(-1, identity())[i]+zero()[i] for i in range(3))


def block_gauss_series(joint):
    blocks = [block_gram({label: joint[label][n] for label in LABELS})
              for n in range(len(joint["S"]))]
    left = [multiply(block, OMEGA) for block in blocks]
    return [series_product(left, blocks, n) for n in range(len(blocks))]


class Checks:
    def __init__(self):
        self.counts = Counter()

    def require(self, condition, category, label):
        if not condition:
            raise AssertionError(f"{category}: {label}")
        self.counts[category] += 1


def inspect_state(checks, name, a, v, g=F(1), volume=F(1), admitted=True):
    require = checks.require
    initial = gram(a, v)
    source = source_series(a, v, g)
    lifted = gram_series(source)
    joint = joint_series(initial, g)
    force = source_acceleration_coefficient([a], 0, g)
    c = c_from_s(initial["S"], g)
    require(force == scale(-1, multiply(a, c)), "source_force", name)
    source_rhs = {"S": add(multiply(transpose(v), a), multiply(transpose(a), v)),
                  "T": add(multiply(transpose(v), v), multiply(transpose(a), force)),
                  "U": add(multiply(transpose(force), v), multiply(transpose(v), force))}
    rhs = joint_rhs(initial, g)
    for label in LABELS:
        require(source_rhs[label] == rhs[label], "closure_derivative", name+" "+label)
        for n in range(DEGREE+1):
            require(lifted[label][n] == joint[label][n], "closure_taylor", f"{name} {label} {n}")
    energies = source_energy_series(source, g, volume)
    joint_energies = joint_energy_series(joint, g, volume)
    for label in energies:
        for n in range(DEGREE+1):
            require(energies[label][n] == joint_energies[label][n], "energy_readout", f"{name} {label} {n}")
    require(all(x == 0 for x in energies["total"][1:]), "energy_conservation", name)
    gauss = source_gauss_series(source)
    block_gauss = block_gauss_series(joint)
    require((gauss[0] == zero()) == admitted, "gauss_admission", name)
    require((block_gauss[0] == zero(6, 6)) == admitted, "block_gauss_admission", name)
    require(all(x == zero() for x in gauss[1:]), "gauss_conservation", name)
    if admitted:
        require(all(x == zero(6, 6) for x in block_gauss), "block_gauss_continuation", name)
    else:
        require(gauss[0] != zero() and block_gauss[0] != zero(6, 6), "negative_gauss_control", name)
    block = block_gram(initial)
    x = tuple(a[i]+v[i] for i in range(3))
    require(block == multiply(transpose(x), x), "realizable_gram", name)
    require(rank(block) == rank(x) <= 3, "gram_rank", name)
    minors = [determinant(tuple(tuple(block[i][j] for j in indices) for i in indices))
              for size in range(1, 7) for indices in combinations(range(6), size)]
    require(all(minor >= 0 for minor in minors), "gram_psd_principal_minors", name)
    chart = {"status": "UNAVAILABLE", "reason": "S is singular; joint polynomial evolution remains enabled"}
    if determinant(initial["S"]) > 0 and admitted:
        s, t, u = (initial[label] for label in LABELS)
        sinv = inverse(s)
        b = multiply(sinv, t)
        bprime = sub(multiply(sinv, rhs["T"]), multiply(multiply(sinv, rhs["S"]), b))
        expected_bprime = scale(-1, add(multiply(b, b), c))
        require(b == transpose(b), "spd_chart", name+" B symmetric")
        require(u == multiply(multiply(transpose(b), s), b), "spd_chart", name+" U")
        require(rhs["S"] == add(multiply(s, b), multiply(b, s)), "spd_chart", name+" S prime")
        require(bprime == expected_bprime, "spd_chart", name+" B prime")
        chart = {"status": "PASS", "B": b, "B_prime": bprime,
                 "expected_B_prime": expected_bprime}
    elif not admitted:
        chart = {"status": "NOT_ADMITTED", "reason": "Off-Gauss diagnostic only"}
    return {"name": name, "admitted_physical_initial_state": admitted,
            "parameters": {"g": g, "V": volume}, "A": a, "v": v,
            "initial_joint": initial, "C": c, "rank_A": rank(a), "rank_joint": rank(x),
            "T_symmetric": initial["T"] == transpose(initial["T"]),
            "source_acceleration": force, "source_gram_derivative": source_rhs,
            "closed_joint_derivative": rhs, "source_taylor": source,
            "source_gram_taylor": lifted, "independent_joint_taylor": joint,
            "source_energy_taylor": energies, "joint_energy_taylor": joint_energies,
            "source_gauss_taylor": gauss, "block_gram": block,
            "gram_principal_minors": minors, "block_gauss_taylor": block_gauss,
            "spd_chart": chart, "status": "PASS"}


WITNESSES = (
    ("R3_A", (1, 1, 0), (0, 0, 1), (F(1, 2), F(1, 2), 0, 0, 0)),
    ("R3_B", (1, 1, 0), (F(2, 3), F(-2, 3), F(1, 3)), (F(1, 2), F(1, 2), 0, F(-8, 3), 0)),
    ("R4_plus", (1, 1, 1), (1, 1, -2), (3, F(3, 2), 0, -12, 36)),
    ("R4_minus", (1, 1, 1), (-1, -1, 2), (3, F(3, 2), 0, -12, -36)),
)


def run_checks():
    checks = Checks()
    require = checks.require
    states = []
    for name, q, p, expected in WITNESSES:
        row = inspect_state(checks, name, diagonal(q), diagonal(p))
        energy = row["source_energy_taylor"]
        observed = (energy["electric"][0], energy["magnetic"][0],
                    *(factorial(n)*energy["magnetic"][n] for n in (1, 2, 3)))
        require(observed == expected, "frozen_witness_readout", name)
        row["R4_and_L"] = dict(zip(("U_E", "U_B", "J", "K", "L"), observed))
        states.append(row)
    a = diagonal((1, 2, 3))
    b = matrix(((0, 1, 0), (1, 0, 0), (0, 0, 0)))
    non_diagonal = inspect_state(checks, "non_diagonal_admissible", a, multiply(a, b))
    require(not non_diagonal["T_symmetric"], "nonsymmetric_T_admissible", "Gauss does not require T symmetric")
    states.append(non_diagonal)
    boundary = inspect_state(checks, "rank_boundary_A_zero_v_identity", zero(), identity())
    require(boundary["rank_A"] == 0 and boundary["rank_joint"] == 3,
            "rank_boundary", "S singular, joint rank three")
    require(boundary["independent_joint_taylor"]["S"][2] == identity(),
            "rank_boundary", "S(t)=t^2 I+O(t^5)")
    states.append(boundary)

    reflection = diagonal((-1, 1, 1))
    require(multiply(transpose(reflection), reflection) == identity() and determinant(reflection) == -1,
            "reflection_setup", "common color reflection")
    mirrors = []
    for base in states:
        reflected = inspect_state(checks, base["name"]+"_improper_reflection",
                                  multiply(reflection, base["A"]), multiply(reflection, base["v"]))
        require(reflected["initial_joint"] == base["initial_joint"], "reflection_gram", base["name"])
        for label in ("A", "v"):
            for n in range(DEGREE+1):
                require(reflected["source_taylor"][label][n] == multiply(reflection, base["source_taylor"][label][n]),
                        "reflection_source_taylor", f"{base['name']} {label} {n}")
        require(reflected["independent_joint_taylor"] == base["independent_joint_taylor"],
                "reflection_joint_taylor", base["name"])
        require(reflected["source_energy_taylor"] == base["source_energy_taylor"],
                "reflection_energy", base["name"])
        reflected["base_state"] = base["name"]
        mirrors.append(reflected)

    scaled_rows = []
    for base in states:
        for lam in (F(1, 2), F(2), F(3)):
            row = inspect_state(checks, base["name"]+"_scale_"+str(lam),
                                scale(lam, base["A"]), scale(lam*lam, base["v"]))
            for label, weight in (("A", 1), ("v", 2)):
                for n in range(DEGREE+1):
                    require(row["source_taylor"][label][n] == scale(lam**(n+weight), base["source_taylor"][label][n]),
                            "scaling_source_taylor", f"{base['name']} lambda={lam} {label} {n}")
            for label, weight in (("S", 2), ("T", 3), ("U", 4)):
                for n in range(DEGREE+1):
                    require(row["independent_joint_taylor"][label][n] == scale(lam**(n+weight), base["independent_joint_taylor"][label][n]),
                            "scaling_joint_taylor", f"{base['name']} lambda={lam} {label} {n}")
            for label in ("electric", "magnetic", "total"):
                for n in range(DEGREE+1):
                    require(row["source_energy_taylor"][label][n] == lam**(n+4)*base["source_energy_taylor"][label][n],
                            "scaling_energy_taylor", f"{base['name']} lambda={lam} {label} {n}")
            row.update({"base_state": base["name"], "lambda": lam,
                        "comparison_time": "scaled t corresponds to original lambda*t",
                        "fixed_parameters": True})
            scaled_rows.append(row)

    # A symmetric T can still violate Gauss when S is not scalar.
    desired_t = b
    off_v = multiply(inverse(transpose(a)), desired_t)
    off_gauss = inspect_state(checks, "T_symmetric_but_off_Gauss", a, off_v, admitted=False)
    require(off_gauss["T_symmetric"], "symmetric_T_insufficient", "negative admission control")

    controls = []
    base = states[1]
    for g, volume in ((F(2), F(1)), (F(1), F(3)), (F(2), F(3))):
        row = inspect_state(checks, f"g_{g}_V_{volume}", base["A"], base["v"], g, volume)
        require(row["source_acceleration"] == scale(g*g, base["source_acceleration"]),
                "coupling_control", row["name"]+" acceleration")
        require(row["source_energy_taylor"]["electric"][0] == volume*base["source_energy_taylor"]["electric"][0],
                "normalization_control", row["name"]+" electric")
        require(row["source_energy_taylor"]["magnetic"][0] == volume*g*g*base["source_energy_taylor"]["magnetic"][0],
                "normalization_control", row["name"]+" magnetic")
        if g == 1:
            require(row["source_taylor"] == base["source_taylor"], "volume_flow_control", row["name"])
            require(row["independent_joint_taylor"] == base["independent_joint_taylor"], "volume_flow_control", row["name"]+" joint")
            require(all(row["source_energy_taylor"][label][n] == volume*base["source_energy_taylor"][label][n]
                        for label in ("electric", "magnetic", "total") for n in range(DEGREE+1)),
                    "volume_energy_control", row["name"])
        controls.append(row)

    # The two tangent vectors have equal speed and force-normal component,
    # but different Hessian quadratic contractions. No trigonometric floats.
    geometry = []
    hessian = matrix(((1, 2, 0), (2, 1, 0), (0, 0, 2)))
    f = (F(1), F(1), F(0))
    for p, expected_k in (((F(0), F(0), F(1)), F(0)),
                          ((F(2, 3), F(-2, 3), F(1, 3)), F(-8, 3))):
        hp = tuple(dot(row, p) for row in hessian)
        contraction = dot(p, hp)
        k = contraction-dot(f, f)
        require(dot(p, p) == 1 and dot(f, p) == 0, "geometry_tangent", str(p))
        require(k == expected_k == -6*p[0]*p[0], "geometry_curvature", str(p))
        geometry.append({"q": (1, 1, 0), "p": p, "speed_squared": dot(p, p),
                         "force_dot_velocity": dot(f, p), "hessian": hessian,
                         "velocity_hessian_velocity": contraction, "force_norm_squared": dot(f, f),
                         "K": k, "formula_on_unit_tangent_circle": "K=-6 a^2 for p=(a,-a,b), 2a^2+b^2=1"})

    axis_factors = (F(2), F(1), F(1))
    original_acc = source_acceleration_coefficient([identity()], 0, F(1))
    changed_acc = source_acceleration_coefficient([diagonal(axis_factors)], 0, F(1))
    time_squared_ratios = tuple(changed_acc[i][i]/(axis_factors[i]*original_acc[i][i]) for i in range(3))
    require(time_squared_ratios == (F(1), F(5, 2), F(5, 2)) and len(set(time_squared_ratios)) > 1,
            "anisotropic_countercheck", "no common time dilation can intertwine this axis scaling")
    anisotropic = {"A": identity(), "scaled_A": diagonal(axis_factors),
                   "axis_factors": axis_factors, "g": F(1), "V": F(1),
                   "source_acceleration": original_acc, "changed_acceleration": changed_acc,
                   "required_common_time_dilation_squared_per_axis": time_squared_ratios,
                   "result": "FAILS_UNIVERSAL_SCALING", "status": "PASS_EXPECTED_COUNTEREXAMPLE"}

    return {"status": "PASS", "schema_version": 1,
            "method": "fractions.Fraction exact arithmetic; independently implemented source and joint Taylor recurrences",
            "coefficient_convention": "coefficient[n] = derivative at zero / n!",
            "taylor_degree": DEGREE, "matrix_convention": "color rows; spatial columns; A=[A1 A2 A3]",
            "contract": {"model": "classical homogeneous SU(2), temporal gauge; fixed positive g,V",
                         "primary_source_carrier": "real 3x3 A,v with A v^T-v A^T=0; these tests use only listed rational states",
                         "joint_carrier": "G=[[S,T],[T^T,U]] PSD of rank <=3 with G Omega G=0",
                         "receiver": "joint polynomial continuation and electric/magnetic energy readouts",
                         "equality": "joint matrix equality; common O(3) color changes are merged, not asserted to be SU(2) gauge",
                         "scaling": "A_lambda(t)=lambda A(lambda t), v_lambda(t)=lambda^2 v(lambda t); positive listed rational lambda",
                         "boundary": "rank(A)=0 is admitted; no inverse of S is used by joint evolution",
                         "fiber_status": "No finite point sampling is presented as a complete source reconstruction fiber"},
            "counts": {"assertions": sum(checks.counts.values()),
                       "assertions_by_category": dict(sorted(checks.counts.items())),
                       "base_states": len(states), "main_YM2_witnesses": len(WITNESSES),
                       "reflection_rows": len(mirrors), "scaling_rows": len(scaled_rows),
                       "normalization_rows": len(controls), "off_Gauss_rows": 1,
                       "full_state_rows": len(states)+len(mirrors)+len(scaled_rows)+len(controls)+1,
                       "geometry_rows": len(geometry), "anisotropic_counterchecks": 1},
            "base_states": states, "improper_reflection": {"O": reflection, "determinant": determinant(reflection), "rows": mirrors},
            "scaling_rows": scaled_rows, "normalization_controls": controls,
            "off_Gauss_control": off_gauss, "geometry_validation": geometry,
            "anisotropic_countercheck": anisotropic,
            "limitations": ["Finite rational checks through Taylor degree four are calibration, not a universal proof or numerical trajectory.",
                            "Source and joint solvers share exact matrix utilities but use different polynomial right-hand sides.",
                            "All tested joint states are lifted from explicit source states; no arbitrary joint-state realization algorithm is certified.",
                            "Common improper reflections preserve this Gram receiver but are not declared SU(2) gauge transformations.",
                            "Scaling tests keep g,V and units fixed; scaled states need not remain in the old YM2 initial energy/coordinate caps.",
                            "The off-Gauss row is a deliberate admission countercontrol, not an admitted physical state.",
                            "No formal proof, quantum theory, mass gap, spectral calculation, universal anisotropic scaling, or literature novelty is claimed."]}


def strings(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {key: strings(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [strings(item) for item in value]
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-results", action="store_true", help="write this directory's RESULTS.json after all checks pass")
    args = parser.parse_args()
    result = strings(run_checks())
    result_path = Path(__file__).resolve().with_name("RESULTS.json")
    if args.write_results:
        result_path.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n", encoding="utf-8")
        mode = "written"
    else:
        if not result_path.is_file():
            raise SystemExit("RESULTS.json absent; use --write-results to create the bounded receipt")
        if json.loads(result_path.read_text(encoding="utf-8")) != result:
            raise SystemExit("RESULTS.json differs from freshly computed results")
        mode = "matched"
    print(json.dumps({"status": result["status"], "results": mode, "counts": result["counts"]}, sort_keys=True))


if __name__ == "__main__":
    main()
