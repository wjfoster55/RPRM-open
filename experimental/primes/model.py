"""Exact small reference tools and a non-expanding decimal-word constructor.

EXPERIMENTAL application pack: no record-sized primality run or novel prime
test. The Lucas-Lehmer reference is deliberately capped at exponent 31.
"""


def natural(value, name):
    if type(value) is not int or value < 0:
        raise ValueError(name + " must be an exact nonnegative integer")


def zero_word_digit(zero_count, index):
    """Digit of the exact word '1' followed by zero_count zeros, without expansion."""
    natural(zero_count, "zero_count"); natural(index, "index")
    if index > zero_count:
        raise ValueError("Index outside the word")
    return "1" if index == 0 else "0"


def trial_prime(n):
    """Transparent conventional reference on 0 <= n <= 2^31-1."""
    natural(n, "n")
    if n > (1 << 31)-1:
        raise ValueError("Outside the reference bound")
    if n < 2: return False
    if n % 2 == 0: return n == 2
    d = 3
    while d*d <= n:
        if n % d == 0: return False
        d += 2
    return True


def mersenne_reference(p):
    """Lucas-Lehmer on prime exponents, with the p=2 exception handled explicitly."""
    natural(p, "p")
    if not 2 <= p <= 31:
        raise ValueError("Reference exponent bound is 2 through 31")
    m = (1 << p)-1
    if not trial_prime(p):
        return {"exponent": p, "number": m, "prime": False, "reason": "composite exponent", "residues": ()}
    if p == 2:
        return {"exponent": p, "number": m, "prime": True, "reason": "M2=3", "residues": ()}
    s, residues = 4, []
    for _ in range(p-2):
        s = (s*s-2) % m
        residues.append(s)
    return {"exponent": p, "number": m, "prime": s == 0, "reason": "Lucas-Lehmer", "residues": tuple(residues)}


def exponent_grade(exponent):
    """Invertible three-step scale coordinate, not geometric dimension."""
    natural(exponent, "exponent")
    return divmod(exponent, 3)
