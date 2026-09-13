# Atom imagery and a bounded circle-phase example

Date: 2026-09-12. Scope: a source-grounded physical distinction followed by an exact mathematical analogy. This note introduces no atomic model, BSD theorem, or physical identification of positional carry.

The useful question suggested by a ring picture is: **what has a display forgotten about how a state fits around the ring?** Modern atomic orbitals are wavefunctions, not prescribed planetary trajectories. IUPAC defines an atomic orbital as a one-electron wavefunction solving the atom's Schrödinger equation; DOE illustrates electron positions through probability distributions. A nucleus-and-rings icon therefore supplies a prompt for investigation, not a mathematical identification. [IUPAC atomic orbital definition](https://old.goldbook.iupac.org/html/A/A00500.html); [DOE, Quantum Mechanics](https://www.energy.gov/science/doe-explainsquantum-mechanics).

## Exact five-state contract

Take the circle coordinate `theta in R/(2*pi*Z)` with normalized measure `dmu = dtheta/(2*pi)`. The admitted source carrier is exactly

```text
N = {-2,-1,0,1,2}
X = {psi_n : n in N},       psi_n(theta) = exp(i*n*theta).
```

Equality is equality of complex functions; `psi_n(0)=1` fixes their constant-phase representative. Define total readout maps on this carrier:

```text
density:    C(psi) = |psi|^2
winding:    W(psi) = (1/(2*pi*i)) * integral_0^(2*pi) psi'(theta)/psi(theta) dtheta
energy:     E(psi) = integral |psi'(theta)|^2 dmu.
```

The winding formula is enabled here because every admitted wave is smooth and nowhere zero. Energy is a dimensionless derivative quadratic form. It is not an atomic binding energy. The receiver may request density, signed winding, or this energy; those are different questions.

Since `psi_n' = i*n*psi_n`, `|psi_n|=1`, and the normalized circle has measure one, direct substitution proves:

| n | Density C | Winding W | Derivative energy E |
|---:|---:|---:|---:|
| -2 | 1 everywhere | -2 | 4 |
| -1 | 1 everywhere | -1 | 1 |
| 0 | 1 everywhere | 0 | 0 |
| 1 | 1 everywhere | 1 | 1 |
| 2 | 1 everywhere | 2 | 4 |

With density `1` supplied and `n` missing, the complete source fiber is `MANY({-2,-1,0,1,2})`. Coverage is complete because these are all admitted states. Density alone preserves neither winding nor energy. Energy `1` has complete fiber `MANY({-1,1})`, so adding energy still loses orientation. Adding winding recovers `ONE(psi_n)` for each admitted `n`. A constant global phase does not change these readouts; the relevant distinction is phase variation along the circle.

## Where the integer comes from

For this paragraph explicitly enlarge the candidate family to `psi_lambda(theta)=exp(i*lambda*theta)`, with real `lambda`. To descend from the real coordinate to a single-valued function on this circle, impose the **ordinary periodic boundary condition**:

```text
psi_lambda(theta+2*pi) = psi_lambda(theta)
iff exp(2*pi*i*lambda) = 1
iff lambda is an integer.
```

This proves the complete allowed parameter family is `Z` for that enlarged question; the five-state experiment then restricts it to `N`. The hostile candidate `lambda=1/2` fails because its values at `0` and `2*pi` are `1` and `-1`. A twisted boundary condition would be a changed contract and can admit shifted integers.

The lifted phase `phi_n(theta)=n*theta` on `[0,2*pi]` accumulates `2*pi*n`, although the complex endpoint values agree. Thus an endpoint display can forget accumulated turns. This is a precise candidate analogy to retaining a carry/lift coordinate. No map from this winding integer to the BSD/keyring or positional-carry state has been supplied here.

These periodic modes are standard in the separate ideal particle-on-a-ring problem, where the physical free-ring energies have factor `hbar^2/(2*m*a^2)` multiplying `n^2`, with opposite signs of `n` degenerate. [MIT 8.06, Spring 2018, Assignment 2, problem 2, page 2](https://ocw.mit.edu/courses/8-06-quantum-physics-iii-spring-2018/aa2e4ad093b2758251bd05dbb1e96d25_MIT8_06S18ps2.pdf).

## The constant-mode obstruction

For the five individual waves, excluding `n=0` gives `E>=1`. To discuss mixtures, explicitly change the carrier to the finite-dimensional space `V=span_C{psi_n : n in N}` with the same measure and pointwise equality. Orthogonality follows by integrating `exp(i*(n-m)*theta)`. Hence for `f=sum c_n*psi_n`,

```text
||f||^2 = sum |c_n|^2,
E(f)    = sum n^2*|c_n|^2.
```

The constant wave `f=1` has norm one and energy zero, refuting any uniform bound `E(f)>=c*||f||^2` with `c>0` on all of `V`. On the mean-zero subspace `c_0=0`, the exact bound is `E(f)>=||f||^2`, attained by `psi_1`. On all of `V`, the corresponding bound is `E(f)>=||f-c_0||^2`.

Merely requiring a wave to be nonconstant is insufficient: for nonzero real `epsilon`, `f=1+epsilon*psi_1` is nonconstant yet `E(f)/||f||^2=epsilon^2/(1+epsilon^2)` approaches zero. The constant component must be removed, or the norm must measure deviation from it.

Evidence grade: exact definitions and written proofs above; published-source support for the orbital distinction and free-ring precedent. No formal proof or numerical experiment is claimed. Atomic interpretation and a BSD adapter remain unsupplied; the established result is the explicit loss of phase/winding under density observation and the stated finite-dimensional gap calculation.
