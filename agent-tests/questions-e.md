# Targeted handbook follow-up E

Use only the supplied revised handbook and the data below. This assessment
targets three clarity edits following a prior review; do not inspect any
prior assessment, answer, rubric or other source. Show the reasoning rather
than citing a bound without deriving it. No solver, external reference or
scientific execution is needed.

1. A complete supplied partial machine has eight source states, three
   distinct present observation values, and finitely many actions. Disabled
   actions become transitions to one absorbing failure state whose tagged
   observation differs from every success. Starting from present
   observations, what bounds follow for strict refinement rounds and the
   length of a necessary distinguishing word? Derive them from the state
   and initial-block counts. How many total refinement comparisons might
   an implementation need, including the final no-split comparison? Does
   the bound assert that a word of that maximum length actually exists?
2. A single-action machine has states x0,...,x6 and constant observation 9.
   Action a sends xi to x(i+1) for i<6 and is disabled at x6. Find the
   shortest word distinguishing x1 and x3, give both tagged outputs, and
   prove that no shorter word works. Relate the answer to the general
   distinguishing bound without confusing a bound with an attained length.
3. A candidate update was validated against payload A at integer version 8.
   Before installation, two accepted updates changed A to B and then B to A.
   Versions strictly increase by one per accepted update. May the original
   candidate install merely because the payload is A again? What is the
   current version? Would an arbitrary nondecreasing version sequence alone
   guarantee rejection? Give a counterexample to that weaker assumption.
4. In a supplied central-force model, radius is 5, tangential speed is 2,
   and the acceleration vector's component along the outward radial unit
   vector is -4/5. The coordinate identity is
   d²r/dt² = acceleration_vector_dot_radial_unit + tangential_speed²/r.
   Find d²r/dt². Explain why an inward acceleration vector does not itself
   say that the object is moving inward, and why calling that vector's
   radial component the same thing as d²r/dt² loses a distinction.
