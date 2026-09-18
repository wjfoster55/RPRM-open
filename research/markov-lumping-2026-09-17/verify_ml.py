"""Exact tests of receiver-specific Markov lumping on named 2-4 state chains.

Does not import rprm, obstruction, fluid, Hamming, observability, or BSD.
Null names are those frozen in NULL.md at commit f191077. This script
computes block masses and enabledness; it does not choose a predicted
name after seeing them.
"""
from fractions import Fraction
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
NULL_COMMIT = "f191077e1e8032b3ae4c21537157d9547a5abdb1"

H = "H"
T = "T"
L = "L"
D = "D"
A = "a"
B = "b"
C = "c"
E = "d"

F = Fraction


def row(*vals):
    out = tuple(F(v) for v in vals)
    if sum(out, F(0)) != 1:
        raise ValueError("row_not_stochastic")
    if any(v < 0 for v in out):
        raise ValueError("negative_mass")
    return out


FAIR_STATES = (H, T)
FAIR_P = {
    H: row(F(1, 2), F(1, 2)),
    T: row(F(1, 2), F(1, 2)),
}

ABS_STATES = (L, D)
ABS_P = {
    L: row(F(1, 2), F(1, 2)),
    D: row(F(0), F(1)),
}

FOUR_STATES = (A, B, C, E)
FOUR_P = {
    A: row(F(1, 2), F(1, 4), F(1, 4), F(0)),
    B: row(F(1, 4), F(1, 2), F(0), F(1, 4)),
    C: row(F(1, 4), F(0), F(1, 2), F(1, 4)),
    E: row(F(0), F(1, 4), F(1, 4), F(1, 2)),
}
FOUR_PT = {
    A: row(F(1, 2), F(1, 4), F(1, 4), F(0)),
    B: row(F(1, 4), F(3, 4), F(0), F(0)),
    C: row(F(1, 4), F(0), F(1, 2), F(1, 4)),
    E: row(F(0), F(0), F(1, 4), F(3, 4)),
}

SKEW_STATES = (A, B, C)
SKEW_P = {
    A: row(F(1, 2), F(1, 4), F(1, 4)),
    B: row(F(1, 8), F(1, 8), F(3, 4)),
    C: row(F(0), F(0), F(1)),
}


def index_of(states):
    return {name: i for i, name in enumerate(states)}


def mass_to(P, states, src, dests):
    ix = index_of(states)
    return sum((P[src][ix[y]] for y in dests), F(0))


def block_masses(P, states, src, blocks):
    labels = tuple(sorted(blocks))
    return tuple((label, str(mass_to(P, states, src, blocks[label]))) for label in labels)


def q_constant(states, r, question):
    seen = {}
    for x in states:
        value = question[x]
        if r[x] in seen and seen[r[x]] != value:
            return False
        seen[r[x]] = value
    return True


def strongly_lumpable(P, states, r, blocks):
    profiles = {}
    for x in states:
        masses = tuple(mass_to(P, states, x, blocks[label]) for label in sorted(blocks))
        if r[x] in profiles and profiles[r[x]] != masses:
            return False
        profiles[r[x]] = masses
    return True


def enabled_match(states, r, rate):
    seen = {}
    for x in states:
        flag = rate(x) > 0
        if r[x] in seen and seen[r[x]] != flag:
            return False
        seen[r[x]] = flag
    return True


def operational(P, states, r, blocks, question, ports):
    q_ok = q_constant(states, r, question)
    lump_ok = strongly_lumpable(P, states, r, blocks)
    en_ok = all(enabled_match(states, r, rate) for rate in ports)
    if q_ok and lump_ok and en_ok:
        fail = None
    elif not q_ok:
        fail = "q_not_constant"
    elif not lump_ok:
        fail = "not_lumpable"
    else:
        fail = "enabledness"
    return {
        "q_constant": q_ok,
        "lumpable": lump_ok,
        "enabledness": en_ok,
        "operational": q_ok and lump_ok and en_ok,
        "fail": fail,
    }


def enter_ports(P, states, blocks):
    ports = []
    for label in sorted(blocks):
        dests = blocks[label]
        ports.append(lambda x, dests=dests: mass_to(P, states, x, dests))
    return ports


def decide(yes, surviving, rejected):
    return surviving if yes else rejected


FAIR_R = {H: "M", T: "M"}
FAIR_BLOCKS = {"M": (H, T)}
FAIR_Q_CONST = {H: 0, T: 0}
FAIR_Q_ID = {H: H, T: T}

ABS_R = {L: "M", D: "M"}
ABS_BLOCKS = {"M": (L, D)}
ABS_Q_CONST = {L: 0, D: 0}

AB = {A: "A", B: "A", C: "B", E: "B"}
AB_BLOCKS = {"A": (A, B), "B": (C, E)}
FINE = {A: "a", B: "b", C: "B", E: "B"}
FINE_BLOCKS = {"a": (A,), "b": (B,), "B": (C, E)}
DIAG = {A: "G", B: "H", C: "G", E: "H"}
DIAG_BLOCKS = {"G": (A, C), "H": (B, E)}
Q_COLOR = {A: 0, B: 0, C: 1, E: 1}
Q_SPLIT = {A: 0, B: 1, C: 0, E: 1}

SKEW_R = {A: "A", B: "A", C: "B"}
SKEW_BLOCKS = {"A": (A, B), "B": (C,)}
SKEW_Q = {A: 0, B: 0, C: 1}


def main():
    fair_ports = enter_ports(FAIR_P, FAIR_STATES, FAIR_BLOCKS)
    q1 = operational(FAIR_P, FAIR_STATES, FAIR_R, FAIR_BLOCKS, FAIR_Q_CONST, fair_ports)
    q2 = operational(FAIR_P, FAIR_STATES, FAIR_R, FAIR_BLOCKS, FAIR_Q_ID, fair_ports)

    abs_ports = enter_ports(ABS_P, ABS_STATES, ABS_BLOCKS)
    abs_enter_L = [lambda x: mass_to(ABS_P, ABS_STATES, x, (L,))]
    q3 = operational(ABS_P, ABS_STATES, ABS_R, ABS_BLOCKS, ABS_Q_CONST, abs_ports + abs_enter_L)
    q4_match = enabled_match(ABS_STATES, ABS_R, abs_enter_L[0])

    p_ab_ports = enter_ports(FOUR_P, FOUR_STATES, AB_BLOCKS)
    q5 = operational(FOUR_P, FOUR_STATES, AB, AB_BLOCKS, Q_COLOR, p_ab_ports)
    q6 = operational(FOUR_P, FOUR_STATES, AB, AB_BLOCKS, Q_SPLIT, p_ab_ports)
    q7 = operational(
        FOUR_P, FOUR_STATES, FINE, FINE_BLOCKS, Q_COLOR, enter_ports(FOUR_P, FOUR_STATES, FINE_BLOCKS)
    )
    q8 = operational(
        FOUR_P, FOUR_STATES, DIAG, DIAG_BLOCKS, Q_COLOR, enter_ports(FOUR_P, FOUR_STATES, DIAG_BLOCKS)
    )

    pt_ports = enter_ports(FOUR_PT, FOUR_STATES, AB_BLOCKS)
    pt_enter_B = [lambda x: mass_to(FOUR_PT, FOUR_STATES, x, AB_BLOCKS["B"])]
    q9 = operational(FOUR_PT, FOUR_STATES, AB, AB_BLOCKS, Q_COLOR, pt_ports)
    q10_match = enabled_match(FOUR_STATES, AB, pt_enter_B[0])

    sk_ports = enter_ports(SKEW_P, SKEW_STATES, SKEW_BLOCKS)
    sk_enter_B = lambda x: mass_to(SKEW_P, SKEW_STATES, x, SKEW_BLOCKS["B"])
    q11_match = enabled_match(SKEW_STATES, SKEW_R, sk_enter_B)
    q12 = operational(SKEW_P, SKEW_STATES, SKEW_R, SKEW_BLOCKS, SKEW_Q, sk_ports)

    names = {
        "Q1": decide(q1["operational"], "N_fair_yes", "N_fair_no"),
        "Q2": decide(q2["operational"], "N_fair_lump", "N_fair_qfail"),
        "Q3": decide(q3["operational"], "N_abs_qenough", "N_abs_mass"),
        "Q4": decide(q4_match, "N_abs_en_yes", "N_abs_en_no"),
        "Q5": decide(q5["operational"], "N_p_yes", "N_p_no"),
        "Q6": decide(q6["operational"], "N_p_lump", "N_p_qfail"),
        "Q7": decide(q7["operational"], "N_fine_qenough", "N_fine_mass"),
        "Q8": decide(q8["operational"], "N_diag_lump", "N_diag_qfail"),
        "Q9": decide(q9["operational"], "N_pt_same", "N_pt_mass"),
        "Q10": decide(q10_match, "N_pt_en_yes", "N_pt_en_no"),
        "Q11": decide(q11_match, "N_sk_en_yes", "N_sk_en_no"),
        "Q12": decide(q12["operational"], "N_sk_support", "N_sk_mass"),
    }

    frozen = {
        "Q1": "N_fair_yes",
        "Q2": "N_fair_qfail",
        "Q3": "N_abs_mass",
        "Q4": "N_abs_en_no",
        "Q5": "N_p_yes",
        "Q6": "N_p_qfail",
        "Q7": "N_fine_mass",
        "Q8": "N_diag_qfail",
        "Q9": "N_pt_mass",
        "Q10": "N_pt_en_no",
        "Q11": "N_sk_en_yes",
        "Q12": "N_sk_mass",
    }

    census = {
        "null_commit": NULL_COMMIT,
        "names": names,
        "frozen": frozen,
        "match": names == frozen,
        "Q1": q1,
        "Q2": q2,
        "Q3": q3,
        "Q4": {
            "enter_L_match": q4_match,
            "rate_L": str(mass_to(ABS_P, ABS_STATES, L, (L,))),
            "rate_D": str(mass_to(ABS_P, ABS_STATES, D, (L,))),
        },
        "Q5": q5,
        "Q6": q6,
        "Q7": {
            **q7,
            "K_c": block_masses(FOUR_P, FOUR_STATES, C, FINE_BLOCKS),
            "K_d": block_masses(FOUR_P, FOUR_STATES, E, FINE_BLOCKS),
        },
        "Q8": q8,
        "Q9": {
            **q9,
            "K_a_B": str(mass_to(FOUR_PT, FOUR_STATES, A, AB_BLOCKS["B"])),
            "K_b_B": str(mass_to(FOUR_PT, FOUR_STATES, B, AB_BLOCKS["B"])),
        },
        "Q10": {
            "enter_B_match": q10_match,
            "K_a_B": str(mass_to(FOUR_PT, FOUR_STATES, A, AB_BLOCKS["B"])),
            "K_b_B": str(mass_to(FOUR_PT, FOUR_STATES, B, AB_BLOCKS["B"])),
        },
        "Q11": {
            "enter_B_match": q11_match,
            "K_a_B": str(sk_enter_B(A)),
            "K_b_B": str(sk_enter_B(B)),
        },
        "Q12": {
            **q12,
            "K_a_B": str(sk_enter_B(A)),
            "K_b_B": str(sk_enter_B(B)),
        },
        "C_diag_lumpable_on_P": strongly_lumpable(FOUR_P, FOUR_STATES, DIAG, DIAG_BLOCKS),
        "C_AB_lumpable_on_P": strongly_lumpable(FOUR_P, FOUR_STATES, AB, AB_BLOCKS),
    }

    path = HERE / "CENSUS.json"
    path.write_text(json.dumps(census, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    if names != frozen:
        dead = {q: {"got": names[q], "wanted": frozen[q]} for q in frozen if names[q] != frozen[q]}
        raise SystemExit("frozen_null_miss: " + json.dumps(dead, sort_keys=True))

    print("PASS")
    print("null_commit", NULL_COMMIT)
    for q in ("Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "Q8", "Q9", "Q10", "Q11", "Q12"):
        print(q, names[q])


if __name__ == "__main__":
    main()
