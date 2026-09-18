"""Count2 fiber of 1 is the XOR=1 inverse fiber.

Identification of two already-closed dispositions on Bits2, not a new
census. Does not import rprm or the inverse-fiber tree.

Carrier: Bits2 = {(0,0),(0,1),(1,0),(1,1)}, tuple equality.
Count2(a,b) = a+b. XOR(a,b) = 1 iff a ≠ b.
Claim: {x | Count2(x)=1} = {x | XOR(x)=1} = ((0,1),(1,0)).
Disposition: MANY of that family.
Decoder h(0)=0, h(1)=1, h(2)=0 satisfies XOR = h ∘ Count2.
Mean numeral (a+b)/2 is a different receiver and is not XOR.
Product of bit-marginals is not the fiber.
"""
from fractions import Fraction

X = ((0, 0), (0, 1), (1, 0), (1, 1))
H = {0: 0, 1: 1, 2: 0}


def xor(ab):
    a, b = ab
    return 1 if a != b else 0


def count2(ab):
    a, b = ab
    return a + b


def mean2(ab):
    a, b = ab
    return Fraction(a + b, 2)


def fiber(fn, z):
    return tuple(x for x in X if fn(x) == z)


def product_of_marginals(pairs):
    first = tuple(sorted({a for a, _ in pairs}))
    second = tuple(sorted({b for _, b in pairs}))
    return tuple((a, b) for a in first for b in second)


def main():
    expected = ((0, 1), (1, 0))
    count1 = fiber(count2, 1)
    xor1 = fiber(xor, 1)
    if count1 != expected or xor1 != expected or count1 != xor1:
        raise SystemExit("count1_is_not_xor1")
    if any(H[count2(x)] != xor(x) for x in X):
        raise SystemExit("decoder_fails")
    if mean2((1, 1)) == xor((1, 1)):
        raise SystemExit("mean_numeral_is_xor")
    if count1 == product_of_marginals(count1):
        raise SystemExit("fiber_is_product_of_marginals")
    print("PASS")
    print("MANY", count1)
    print("decoder", H)


if __name__ == "__main__":
    main()
