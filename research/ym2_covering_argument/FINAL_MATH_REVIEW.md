# Final mathematical review of the covering result and next obligation

12 September 2026. This review reads the final synthesis and next-obligation
documents without changing them. The reviewer derived the direct Fourier
proof and therefore does not claim independence from that proof's authorship.
This is a separate audit of the root-written synthesis and limit contract.
The direct proof itself has the two other reviews linked in its opening.

**Disposition: PASS, after the root incorporated the two normalization and
domain clarifications described below. No remaining mathematical blocker
was found in the reviewed documents.** This is written review, not external
peer review or formal verification.

## Exact reviewed bytes

| File | SHA-256 |
|---|---|
| [COVERING_RESULT.md](COVERING_RESULT.md) | `b65cf3fbbf8bea4f4173d9263750814fdb2878b158e1d5ec6f60854424b65002` |
| [NEXT_OBLIGATION.md](NEXT_OBLIGATION.md) | `f428f56bde1a85544efc7f4ccf313a3cb6f26f93598b57f57fdf7c76da105e42` |

These hashes bind the inspected bytes; they do not prove their contents.
The portability edits to two links in `CONDITIONAL_REFINEMENT.md` do not
change the conditional mathematics reviewed here.

## Construction endpoint and geometric margin

Let `b=4/3`. The sufficient fixed-point radius obeys
`t=Y-bY^2`, with `t=8mr`. Completing the square gives

```text
Y-(4/3)Y^2 = 3/16-(4/3)(Y-3/8)^2.
```

Thus the maximum source majorant is `3/16`, attained at `Y=3/8`.
Its coupling value is `r=3/(128m)`. The Lipschitz bound of the map on
that radius is `(8/3)Y=1`, which does not establish a strict contraction.
The document correctly states the proved stronger interval with a strict
inequality at this endpoint.

If the endpoint radius were available by an additional argument, its
geometric estimate would still be `1-2Y=1/4`. The wording "would still
be" correctly treats this as the value of the geometric formula at the
uncertified construction endpoint, not as a theorem obtained by applying
Banach contraction there. The safe closed interval `r<=1/(48m)` instead
has `Y<=1/4`, map contraction at most `2/3`, and gap at least `1/2`.

The scalar inequality `y<=t+by^2` also allows sufficiently large `y`.
The documents explicitly retain the small invariant ball and contraction
as the construction. They do not infer a small solution from that scalar
inequality alone, nonexistence of a vacuum from a negative discriminant,
or a physical transition from failure of the sufficient estimate.

## Quantum scale conversion

The primary source was independently reopened:
[D'Andrea et al., *New basis for Hamiltonian SU(2) simulations*, equations
(56)-(57), printed page 8](https://scoap3-prod-backend.s3.cern.ch/media/files/84451/10.1103/PhysRevD.109.074501.pdf).
It has electric coefficient `g_b^2/(2a)` multiplying the ordinary
`j(j+1)` Casimir and magnetic coefficient `1/(2g_b^2 a)` multiplying
`Tr[2I-P-P^dagger]`. For SU(2), that trace is `4(1-a_p)`.

In the supplied metric, `T=2 sum J_e^2`. Matching coefficients therefore
gives exactly `E_el=g_b^2/(4a)` and `r=8/g_b^4`, as in (C8).
This calculation states one source convention; it does not identify all
published generator normalizations. A common energy-unit rescaling leaves
the ratio unchanged. The usual direction `g_b->0` sends this ratio to
infinity, outside the certified small-r interval. None of these algebraic
observations constructs a continuum limit.

## Actual-vacuum measure and the next comparison form

Two clarifications were requested and are present in the reviewed bytes:

1. The synthesis now defines `psi_hat=exp(u)/||exp(u)||_2` and
   `dnu=psi_hat^2 dmu`. The Haar-mean-zero log-vacuum convention by itself
   does not normalize `exp(u)` in `L^2`. The Hessian and weighted Ricci
   tensors are unchanged by a scalar normalization, but the probability
   measure and variance need the explicit normalization now supplied.
2. The next obligation defines `D_s` as the dimensionless actual form
   `q_(H_s-E_0,s)/E_el,s` after its ground-state transform. It requires
   positive `a_s,kappa_s`, and both comparisons on every function in the
   transformed actual physical form domain, included in the reference
   domain. Thus multiplying by `E_el,s` in (N1) does not count the energy
   scale twice or omit actual trial states through a smaller test domain.

The common actual-vacuum measure, or a separately proved measure transport,
is explicitly required. The fixed physical reference energy cannot be
defined as the gap being proved. Consequently (N1) is a valid sufficient
target: when its stated ports are supplied, chaining its inequalities
gives a positive lower bound relative to the fixed physical reference.
It is properly presented as an open comparison obligation, not as a
comparison already constructed at large r.

## Conditional refinement and claim ceiling

The new (C9) agrees with (CR1)-(CR6):

```text
W(t)=Y(t)-t-(4/3)t^2 <= 10t^3,
sum_j epsilon_ej <= (16/3)W(8mr) <= (160/3)(8mr)^3.
```

At the safe endpoint, `W=5/108`. The head and remainder yield
`1/48+(m-1)/(16848m)+5/81<1/12`, for both `m=2` and `m=4`.
The synthesis preserves the distinction between this actual conditional
bound and the separate all-state spectral transfer through Bochner.

The main result covers every vector in the actual form domain, all spins,
and all admitted finite graphs, and contains the gauge-invariant ground
state. It does not require a physical tensor-product decomposition.
Graphs without a physical excited complement receive a vacuous complement
form inequality, not a fabricated first excited eigenvalue.

The claimed closure is uniform finite-volume exclusion at fixed admitted
local ratio and energy scale. The notes keep infinite-volume states and
representations, limiting dynamics, continuum existence, increasing-r
continuation, and physical mass-gap survival as further obligations.
No complete eigenfunction fiber, novel physical law, formal certificate,
or literature-priority conclusion is claimed.

## New finite exact controls

The standalone [check_conditional_cover.py](check_conditional_cover.py)
uses only the Python standard library and `Fraction` arithmetic. It
imports or runs no previous checker. Its receipt is
[RESULTS_CONDITIONAL_COVER.json](RESULTS_CONDITIONAL_COVER.json).

The checker corroborates:

- Two polynomial identities for (CR5), five rational majorant controls,
  the exact cubic constant, and the strict-contraction endpoint values.
- The centered two-square coefficient match in (CR7)-(CR9), including
  the kinetic residual using explicitly supplied degree-two identities,
  edge-disjoint cancellation, and a nonzero residual when an adjacent
  pair is incorrectly treated as disconnected.
- The exact endpoint conditional bounds and strict margins below `1/12`
  in dimensions two and three.
- Seven specified multiaffine polynomials on four SU(2) rotors, with
  `x_i=Tr(U_i)/2`. Enumerating their trace-coordinate corners exhausts
  their mixed extrema. These finite examples check cancellation when a
  link is absent, the attained factor `8`, complete outside-link counting,
  and the energy-weighted support bound. They reject replacing `8` by
  `4`, dropping an outside occurrence of a triple, or omitting the
  support-energy weight on a four-link term.

These controls do not verify the unrestricted Fourier product theorem,
the Banach theorem, regularity, the all-spin Hessian estimate, arbitrary
conditional supremum theorem, Bochner identity, or any limiting theory.
The receipt explicitly retains these limits. Its embedded checker hash
binds the checker bytes; no proof text is claimed proved by a hash.

Executed successfully:

```powershell
python -I -B research/ym2_covering_argument/check_conditional_cover.py --write-receipt
python -I -B research/ym2_covering_argument/check_conditional_cover.py
python -I -O -B research/ym2_covering_argument/check_conditional_cover.py
```

The first command intentionally wrote the new receipt. The latter two
recomputed it and compared the full parsed receipt without writing.
The conditions remain active under optimized Python; they do not rely
on removable `assert` statements.

| New artifact | SHA-256 |
|---|---|
| `check_conditional_cover.py` | `82454cbd3c5374253222d04b230ba09390cc80c2c035f51a6e525f391c971bbb` |
| `RESULTS_CONDITIONAL_COVER.json` | `3bad81c602b9f8b2104786b1c45eec419909117b8971a9b6868d1351aa41a311` |
