"""Certified finite square-frontier expansion using ordinary trial division.

Code: 0BSD. A complete prime list through B >= 2 decides every integer in
[2, B**2]. Construction checks the complete-list premise with a sieve; no
caller-supplied certification flag is trusted. This is not a speedup claim.
"""

from dataclasses import dataclass
from math import isqrt


def _integer(value, minimum, name):
    if type(value) is not int or value < minimum:
        raise ValueError(name + " must be an exact integer >= " + str(minimum))


def _complete_primes(bound):
    """Admission check, separately implemented from the classification scan."""
    marked = bytearray(bound + 1)
    for p in range(2, isqrt(bound) + 1):
        if not marked[p]:
            for multiple in range(p * p, bound + 1, p):
                marked[multiple] = 1
    return tuple(n for n in range(2, bound + 1) if not marked[n])


@dataclass(frozen=True)
class Frontier:
    """Immutable bound and complete increasing prime list, copied on admission.

    Creating a large frontier incurs finite computation and storage. The
    state retains the list needed for continuation; a Boolean success label
    alone is not its certificate.
    """

    bound: int
    primes: tuple

    def __post_init__(self):
        _integer(self.bound, 2, "bound")
        if type(self.primes) not in (tuple, list):
            raise ValueError("primes must be a complete materialized tuple or list")
        values = tuple(self.primes)
        for p in values:
            _integer(p, 2, "prime")
        if values != _complete_primes(self.bound):
            raise ValueError("primes must be exactly the increasing primes through bound")
        object.__setattr__(self, "primes", values)

    @property
    def state(self):
        """Complete exact state admitted by the finite proof-donut checker."""
        return self.bound, self.primes

    def classify(self, candidate):
        """Return (is_prime, smallest_factor); prime answers carry factor zero."""
        _integer(candidate, 2, "candidate")
        if candidate > self.bound * self.bound:
            raise ValueError("candidate lies outside the certified square frontier")
        for p in self.primes:
            if p * p > candidate:
                return True, 0
            if candidate % p == 0:
                return False, p
        # Completeness and the admitted bound justify this exhaustion branch.
        return True, 0

    def expand(self):
        """Return the certified successor and every answer in candidate order.

        The answer tuple covers exactly 2..B**2. The successor's constructor
        checks that its retained list satisfies the next input contract.
        """
        next_bound = self.bound * self.bound
        answers = tuple(self.classify(n) for n in range(2, next_bound + 1))
        primes = tuple(n for n, answer in enumerate(answers, 2) if answer[0])
        return Frontier(next_bound, primes), answers
