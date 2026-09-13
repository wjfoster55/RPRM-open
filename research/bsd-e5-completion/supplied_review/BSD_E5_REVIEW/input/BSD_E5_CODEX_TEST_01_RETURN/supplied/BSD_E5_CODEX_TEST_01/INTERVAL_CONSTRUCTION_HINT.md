# Optional constructive route to a rigorous derivative interval

**This is a proposed route for Codex to derive and execute, not an interval
already calculated in this package.** A rigorous installed ball backend may be
simpler. Preserve every approximation's error and the sign of its coefficient.

For alpha>0 and M>=1,

    L'(E,1) = 2 sum_{n=1}^M (a_n/n) E1(alpha*n) + R_M,
    |R_M| <= 4 exp(-alpha*(M+1)) /
                 (alpha*(M+1)*(1-exp(-alpha))).

The tail follows from |a_n|<=2n and E1(x)<=exp(-x)/x. If alpha>=a>0 and
exp(-alpha)<=q<1 are proved, the entirely rational substitute

    |R_M| <= 4*q^(M+1)/(a*(M+1)*(1-q))

is available. The source uses a=1/5, q=5/6. For accurate retained terms alpha
needs a MUCH tighter enclosure than (1/5,1/4); improve pi/sqrt2 with certified
bounds. Monotonicity gives, when alpha in [a,b],

    E1(b*n) <= E1(alpha*n) <= E1(a*n).

Signed multiplication reverses endpoints when a_n is negative. Do not bound
all terms as if their coefficients were positive.

One standard-library route for positive rational x is to pick B>x and write

    E1(x) = integral_x^B f(t)dt + E1(B), f(t)=exp(-t)/t.

Here f is positive and convex, since

    f''(t)=exp(-t)*(1/t + 2/t^2 + 2/t^3) > 0.

For each subinterval [u,v], convexity gives

    (v-u)*f((u+v)/2) <= integral_u^v f(t)dt
                       <= (v-u)*(f(u)+f(v))/2.

Use lower bounds for function values on the left and upper bounds on the right.
The tail satisfies 0<E1(B)<=exp(-B)/B. This makes the gap between midpoint and
trapezoid sums an explicit, inspectable enclosure, not a heuristic estimate.

For exp(-r), r>=0 rational, choose k so 0<=z=r/2^k<=1. The even and odd partial
sums of exp(-z)'s alternating factorial series bound exp(-z). Their nonnegative
endpoints can be squared k times, with exact arithmetic or outward rounding.
If rational denominators grow too much, round OUTWARD to a declared dyadic grid
at each step; retain the accumulated enclosure rather than assuming cancellation.

A geometric/adaptive quadrature mesh can reduce work near the small lower endpoint.
Choose a finite subinterval/refinement cap before execution and report it. A
positive interval wider than 1/100 is still valid evidence, but does not meet the
stronger target width. A pair of close unproved approximations is not an enclosure.

For two independently certified intervals of the same quantity, their nonempty
intersection is certified. Do not assume intervals produced at larger M must
be nested; different truncation and rounding errors can shift both endpoints.
An empty intersection is a discrepancy to investigate, not permission to choose
the preferred interval.

This machinery only refines c1 for the fixed curve. It does not determine a
regulator, certify an integral Mordell–Weil generator, or verify full BSD.
