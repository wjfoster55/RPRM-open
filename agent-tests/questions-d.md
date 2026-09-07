# Expanded handbook comprehension assessment D

Use only the supplied handbook and the data in these questions. Do not read
the main manuscript, other tasks, source notes, rubrics, prior answers or
external references. Derive the answers; a keyword alone is insufficient.
If the supplied material cannot support a conclusion, identify the exact
missing condition. Answer all twenty questions in order. Short equations,
tables and concrete counterexamples are welcome. No model execution or
scientific experiment is requested.

1. On the integer carrier {-2,-1,0,1,2}, the relation is x+y=z without wrap.
   Give the complete fiber for z=-1. Then give the fiber when all three
   supplied values are (x,y,z)=(2,-2,0). Explain the difference between an
   empty tuple and an empty fiber.
2. A complete source family has rows (0,0),(1,1). A tool returns independent
   marginal sets {0,1} and {0,1}. Does this preserve the source family? For
   the question x XOR y, what answer does the actual family settle?
3. Let X={u,v,w}, C(u)=C(v)=A, C(w)=B, with Q(u)=Q(v)=7 and Q(w)=9.
   Describe the unique decoder on the reached image. If the target also
   contains an unused symbol Z, is its decoder value forced? Now change
   Q(v) to 8: what minimum repair-tag alphabet suffices, and why?
4. Take one total action p→r, q→s, r→r, s→s. Observations are all zero.
   C(p)=C(q)=A, C(r)=B, C(s)=D, with distinct A,B,D. Does C answer every
   finite future observation? Does it have an exact update? Give a correct
   coarser operational representation.
5. A chain has four states x0→x1→x2→x3 under action a, disabled at x3;
   all observations are zero. What is the shortest word distinguishing
   x0 and x1, and what are the two tagged answers? Does adding a failure
   state force a length-four distinguishing bound for this source machine?
6. A four-bit word must have even parity. Three labeled values are 1,0,1
   and the fourth is erased. Recover it. If instead all four are reported
   and the parity is odd, can you locate a single unknown wrong position?
   State what is known and what remains ambiguous.
7. A source function has the form a+bx+cy+dxy on [-1,1]^2. Its four corner
   values are 2,4,6,8. What is the center value, and are all values on the
   square positive? Would observing these corners justify the same claims
   for arbitrary continuous functions? Supply a concrete counterexample
   or construction demonstrating the obstruction.
8. Four lane maps come from one initial state h. After an update T, a lane
   measures O(T(h)). A procedure retains only the number of surviving
   hypotheses and discards their identity and prior constraints. Is that
   enough to apply all later lanes? Explain what must be retained and why
   four generated views are not automatically four independent measurements.
9. All primes through 7 have been certified. Describe the next square-bound
   sieve stage and explain why it classifies 49 correctly while retaining
   47 as prime. Does a finite stage alone establish every later stage?
10. A reader says, "The bounded Fermat result tests every variable only up
    to 4000, and the fixed-gap solver proves that every gap is impossible."
    Correct both statements with exact domains. Use a concrete square-power
    example to show why a per-tuple decision can return ONE.
11. Suppose a power discrepancy has normalized sign strictly increasing
    for positive a, with negative value at integer 17 and positive value
    at integer 18. Can a positive integer zero exist below 17, above 18,
    or between them? Does this one aperture resolve every other exponent
    and gap choice? Explain the role of coverage.
12. Explain the difference between 0.333...=1/3, an eventually repeating
    machine state, an unbounded sequence of integers, and a coordinate
    singularity. Which, if any, proves a physical object reaches infinity?
13. Let S={a,b,c}, r(a)=r(b)=A and r(c)=B. The rows of P are
    a:(1/3,1/3,1/3), b:(1/6,1/2,1/3), c:(0,0,1).
    Give the reduced transition matrix and the probability of being in B
    after two steps starting at a. Change the b-row to (1/6,5/6,0): does
    the same quotient work for every initial distribution? Justify.
14. A proposed reduced matrix has a proved all-source-state row error at
    most epsilon=1/50 in total variation. With matched initial states,
    what marginal bound follows at t=12, and at t=80? Does this argument
    also bound the error of every infinite-horizon hitting-time statistic?
15. A finite carrier has scores {-3,1} in one representation fiber and
    {4,4} in another. Find the minimum worst absolute reconstruction error
    and an attaining decoder. Does attaining it prove accuracy on new data?
16. In the supplied two-path model chi=i/4. Find the plus probabilities
    at theta=0 and theta=pi/2, and the complete interval of compatible p.
    Is there exactly one reduced state? Would a unique reduced state alone
    identify every possible path-plus-marker preparation?
17. Two path states have chi=0 but p=0 and p=1. Can the phase-only receiver
    distinguish them before an operation? What happens to their coherences
    under H=(1/sqrt(2))*[[1,1],[1,-1]]? What does this show about continuation?
18. Marker selection has two equal-probability outcomes. At one phase,
    their conditional plus probabilities are 0.9 and 0.1. Give each joint
    plus probability and the unconditioned plus probability. Does the
    coherence of the unconditioned path alone determine every selected
    distribution, or does that question require additional state?
19. Hypothesis a allows joint bit rows {00,11}; b allows {01,10}. With no
    observations, what is the worst hypothesis count after asking either
    single bit? After learning first bit=1, which second-bit result selects
    which hypothesis? Does no immediate guaranteed reduction mean no useful
    two-step plan exists?
20. An experiment compares a one-category summary's zero log loss with a
    full model predicting four distinct outcomes. The summary also omits
    the folds where selection failed and reports accuracy on the rest.
    Identify both comparison defects and the information a valid comparison
    must freeze and report. Is either defect repaired by a correct finite
    preservation theorem?
