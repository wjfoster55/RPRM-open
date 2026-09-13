# Stacked centered differences: complexity, variance and gap separate

12 September 2026. This note tests the user's `-0.6,+0.4` example on a
fully specified probability carrier. It is a control for the inference
from offsets and stacking to a gap obstruction, not a proposed SU(2)
vacuum or a replacement definition of RPRM signs.

## 1. A family that keeps the offset exactly

For each supplied finite integer `n>=1`, let `B_1,...,B_n` be independent
Bernoulli variables with `p=3/5`, and put `Z_i=B_i-p`. Every coordinate
therefore takes the two values

```text
Z_i=-3/5 with probability 2/5,
Z_i=+2/5 with probability 3/5.
```

These unequal-looking offsets are centered under the supplied measure:
`E Z_i=0`, `E Z_i²=6/25`. Equal weighting of the two displayed values would
be a different measure and would give mean `-1/10`. The probabilities are
a required port, not information supplied by the two numerals alone.

Point equality means equality of every ordered coordinate occurrence.
The centered encoding is a bijection with inverse `B_i=Z_i+3/5`.
Different occurrences with equal negative values are not automatically
identified or added. Below, summation is a separately declared readout.

Let `S_n=sum_i Z_i` and `M_n=S_n/n`. Independence gives

```text
Var(S_n)=6n/25,
Var(M_n)=6/(25n).                                        (S1)
```

Without independence, the exact identity would instead be
`Var(sum_i Z_i)=sum_i Var(Z_i)+2 sum_(i<j) Cov(Z_i,Z_j)`.
Thus correlations can matter decisively. The signs of the coordinate
labels alone do not supply those covariances.

## 2. The whole conditional-difference spectrum, for every finite n

Let `P_i f=E[f | all B_j with j!=i]` under this product law, and define

```text
R_i=I-P_i,
A_n=sum_i R_i.
```

This `A_n` is an auxiliary conditional-resampling operator on functions.
It is not the SU(2) quantum Hamiltonian or an assertion about actual
classical time. The requested receiver is its spectrum and the optimal
constant in

```text
Var(f) <= C_mix sum_i ||R_i f||².                         (S2)
```

For each subset `J` of `{1,...,n}`, define
`chi_J=product_(j in J)(B_j-p)`, with `chi_empty=1`.
Independence and centering make the `2^n` functions mutually orthogonal.
Every one has nonzero norm because `0<p<1`. Since functions on the carrier
have dimension `2^n`, this is a complete basis, not selected eigenmodes.

Conditional averaging gives `P_i chi_J=0` when `i in J`, and
`P_i chi_J=chi_J` otherwise. Hence

```text
A_n chi_J = |J| chi_J,
spectrum(A_n) = {0,1,...,n}, with multiplicity binomial(n,k),
delta(A_n)=1 and C_mix=1 for every n>=1.                  (S3)
```

The equality between the quadratic form of `A_n` and the sum in (S2)
uses the orthogonal-projection identity `R_i²=R_i`. Expanding in the
complete basis proves the inequality and choosing any singleton `J`
proves sharpness. The written proof covers every finite `n` and every
`0<p<1`, not just the value `p=3/5` or the checker's small dimensions.

Update normalization is part of this contract. If instead an algorithm
chooses only one of `n` coordinates per discrete step, its kernel is
`K_n=(1/n)sum_i P_i=I-A_n/n`, whose gap is `1/n`. That factor records the
chosen update clock. It is not produced by the minus signs. The continuous
resampling generator `-A_n` updates each coordinate at rate one.

## 3. An exact hostile case for our new vacuum-comparison method

Compare this law `nu_n` with uniform probability `mu_n` on the same cube.
For `p=3/5`, the density is

```text
dnu_n/dmu_n = product_i [(6/5) if B_i=1, (4/5) if B_i=0].
```

Its ratio of maximum to minimum is

```text
R_n=(3/2)^n.                                             (S4)
```

Yet the actual constant in (S2) is exactly one. A generic comparison bound
`C_mix<=R_n` therefore loses exponentially with dimension while the
actual resampling gap stays fixed. This is an exact family counterexample
to the inference “a worsening global density-ratio bound proves worsening
mixing.” It also shows why a successful fixed-graph density comparison
in [VACUUM_COMPARISON.md](VACUUM_COMPARISON.md) is not, by itself, an
adequate route to a uniform Yang–Mills limit.

The quantum model needs its own true joint vacuum measure. We cannot
replace it with independent signs. The control identifies what a better
estimate should avoid: paying for every local density bias as though all
of those biases were one collective obstruction.

## 4. More configurations do not determine the spectral conclusion

The carrier has `2^n` points. That combinatorial count increases
exponentially even while (S3) stays fixed. Both statements are true and
concern different receivers. Here the sum has only `n+1` possible values.
For a supplied sum `s`, put `k=s+np`. Its complete source fiber is

```text
all binary words with exactly k ones,
```

if `k` is an integer in `[0,n]`; otherwise it is empty. Its size is
`binomial(n,k)` when admitted. At `k=0` or `n` the fiber is ONE; at interior
`k` it is MANY. An invalid `n` is an admission error. This is a complete
fiber proof: every such word gives the sum and every source word has that
number of ones.

This gives a precise version of the backward-trace issue. The final sum
usually does not retain which coordinate occurrences contributed. Keeping
the whole ordered joint makes the encoding reversible. Keeping only its
sum loses those distinctions, regardless of how many minuses are used to
write it. These are static source words, not claimed dynamical histories.

## 5. Evidence and RPRM connection

The local RPRM core's residual and centered-coordinate contracts distinguish
a negative value, a negation operation, an occurrence and a zero readout.
The historical Prestige discussion also asks where added relational
complexity must be retained. This control honors that question by exposing
four separate measurements: configuration count, sum variance, lost fiber,
and residual-operator gap. It does not assign these measurements universal
RPRM stage numbers.

Variance tensorization and conditional resampling are established methods;
for the general dependence question see
[Caputo, Menz and Tetali, introductory setup and Proposition 1.1](https://arxiv.org/pdf/1405.0608).
The complete elementary product-basis proof above is given here rather
than inferring a theorem from the checks. No novelty is asserted.

[check_stacking.py](check_stacking.py) independently implements conditional
averaging maps on small cubes and checks their complete product bases
with exact rational arithmetic. It also retains the density-ratio and
variance controls. Its finite execution corroborates this derivation;
the all-finite-n statement rests on the displayed proof. No simulation
or claim about actual SU(2) chaos is involved.
