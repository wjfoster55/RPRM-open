# Independent review of the vacuum separating witness

12 September 2026, 18:40 UTC snapshot. Bounded review of
`VACUUM_SEPARATING_WITNESS.md`, its companion perturbation proof, and the
accepted positive-vacuum comparison. No old checker was rerun. Only this
review file was added by the reviewer; the exact rational calculations below
used an independent, ephemeral Python `Fraction` calculation.

**Verdict:** the displayed theorem for every real `0<r<=1/3000` follows
from the stated fixed-graph premises. I found no substantive mathematical
error in its remainder conversion, coefficient contraction, or interval
isolation. One local strictness statement needs its positive-r domain made
explicit; one source link awaited export staging at this snapshot.

## Corrections identified

1. Equation W7 has a strict `<` while its immediately preceding discussion
   admits `r=0`. At zero both sides are zero. State `0<r<=1/10` at W7, or
   use `<=` there. The claimed theorem W1 already excludes zero, so its
   conclusion and strict endpoint margin are unaffected.
2. The relative link to
   `accepted_sources/ym2_signed_differences/VACUUM_COMPARISON.md` did not
   yet exist when inspected. The actual accepted source was read at
   `C:/github/RPRM-open/research/ym2_signed_differences/VACUUM_COMPARISON.md`.
   Complete the planned copy or adjust the link before delivery. This is an
   artifact dependency issue, not a gap in the displayed mathematical chain.

## Quantifiers and norm conversion

The companion's real positive mean-one eigenvector agrees with the unique
physical ground state. Its Neumann-resolvent argument gives an analytic
eigenline on `|r|<3/2`, and the reduced inverse prevents its Haar mean from
vanishing. The Cauchy estimate on the circle `|r|=1` therefore bounds every
omitted coefficient jointly by the displayed L2 geometric suffix for
`|r|<1`. This covers the requested real interval without sampling couplings.

For `0<=r<=1/10`, the accepted ratio bound implies `M/m<7` for the actual
positive eigenfunction. Mean one implies `1<=M<7m`, hence `m>1/7`.
The independently bounded polynomial approximation satisfies `p2>9/10`.
Thus every real interval between their pointwise values stays above `1/7`,
and the ordinary mean-value theorem gives
`|log(phi)-log(p2)|<=7|phi-p2|` pointwise. Integrating this inequality is
legitimate. There is no hidden inference of a supremum bound from the L2
remainder, and no pointwise Taylor error is inferred at the hostile pair.

This argument uses continuous positive representatives on the original
compact source. Passing to the complete gauge quotient preserves the Haar
integrals of invariant functions. It introduces no regular-coordinate
assumption at the singular boundary. The separate regularity discussion in
the companion is not needed to upgrade this explicit L2 log bound.

The scalar logarithm estimate is uniform over the admitted configurations
and `0<r<=1/10`. Squaring the eigenfunction doubles its logarithm;
probability normalization adds a scalar annihilated by `E[D]=0`.
Consequently the factor `2||D||2=sqrt(3)/2<1` in the witness contraction
is correct. All constants in this review are for this fixed graph.

## Independent exact constants

The inequalities were reconstructed directly from the displayed formulas,
without importing either checker or reading its result fields.

| Quantity | Exact value or comparison |
|---|---|
| Vacuum ratio prefactor | `104207/52043 < 7/3` |
| Supremum majorant for `u2` | `1/64+1/39+1/351 = 991/22464 < 1/20` |
| Polynomial lower bound at `r=1/10` | `1-1/30-1/2000 = 5797/6000 > 9/10` |
| Coefficient in `|z|<=r(1/3+r/20)` | `1/3+1/200 = 203/600 < 7/20` |
| Comparison `5/(9 sqrt(2)) < 2/5` | equivalent to `625<648` |
| Elementary logarithm error constant | `343/21600+1/60+1/3200 = 2839/86400 < 1/25` |
| Combined logarithm error majorant | `14/5+2839/86400 = 244759/86400 < 3` |
| Conditional variance contraction | `(3/4)^2/3 = 3/16 = ||D||2^2` |
| Quadratic coefficient of the witness | `(2/351)(3/16) = 1/936` |
| Endpoint lower margin | `1/936-1/1000 = 1/14625 = 4/58500 > 0` |
| Hostile pair quotient slack | `1-(3/5)^2 = 16/25 > 0` |
| Hostile pair log-jet difference | `(2/351)(6/5) = 4/585` |

Under the conditional Haar law, `D` has zero mean at each `(a,b)`, and
`w=ab+D`. Therefore `<D,w>=E[D^2]=3/16`; every other displayed first-
or second-order nonconstant term is orthogonal to D. For positive r the
strict log bound yields `|J-r^2/936|<3r^3`. Since `3r<=1/1000` throughout
the claimed interval, the final strict margin remains valid at
`r=1/3000`. At zero the witness vanishes, as separately stated.

If the density were measurable in `(a,b)` alone, its bounded logarithm
would be as well, forcing this same Haar contraction to vanish. Thus W1
certifies actual measurable joint dependence, not merely a formal jet.
The complete conditional configuration fiber follows from the relative
cosine of two independent Haar quaternion directions; it is not a claim
about electric momenta or a complete vacuum/spectral fiber.

## Claim ceiling and source identity

The text correctly leaves the graph-uniform conditional-response norm,
summability over exterior changes, stronger coupling range, physical
continuum construction, and any improvement to the gap estimate OPEN.
An integral L2 witness cannot supply the missing worst-case conditional
estimate. No inappropriate gap or scaling conclusion was found.

This is a written mathematical review plus exact finite arithmetic, not a
proof-assistant proof or a new verification of the accepted spectral and
semigroup theorems. The following SHA-256 values identify the inspected
bytes at 18:40:07 UTC; subsequent author corrections may change them.
Paths are relative to `C:/github/RPRM-open/`.

| Source | SHA-256 |
|---|---|
| `research/ym2_connected_vacuum/VACUUM_SEPARATING_WITNESS.md` | `45CC0D4F1E1EE0A25F8CF6C455893985E8C49FC5AF5A85C9D65309BE474D12B7` |
| `research/ym2_connected_vacuum/CONNECTED_VACUUM.md` | `4ECD426F8D25C942D73B310D90BD5DF469B931636D26AE8CF19AE4B738BAF652` |
| `research/ym2_signed_differences/VACUUM_COMPARISON.md` | `164871AE2E06EEFBC5B47304CBDDAAEA4DF0E72DB262E276ABE67A61726E6D01` |
