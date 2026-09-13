# Independent review of the actual-vacuum separating witness

12 September 2026. Review by the agent responsible for the independent
wavefunction derivation, after reading the root agent's complete
[VACUUM_SEPARATING_WITNESS.md](VACUUM_SEPARATING_WITNESS.md).

**Disposition: the written proof of (W1) passes this mathematical review.**
No correction to its inequality chain was required. This is a human-style
independent derivation review, not a proof-assistant certificate.

The reviewed witness bytes have SHA-256
`b9137decf54e233136c868f601af7d986eadc5dbe3907b74d4dca9dafcc66884`.
The perturbation dependency reviewed at this point has SHA-256
`9923cf495cb7b90d041569afd28805f7f9ac3b9c14100d0e6ff2173c4333c7ab`.
These hashes identify reviewed bytes; they do not establish truth.
The displayed strict bound (W7) was subsequently clarified to include its
explicit `0<r<=1/10` scope; that line was reread before recording the final
witness hash above. No other witness mathematics changed.

## What was independently checked

1. The Haar conditional law gives `E[D|a,b]=0` and
   `E[D^2]=(3/4)^2/3=3/16`, with `D=w-ab`. Thus every square-integrable
   function of `(a,b)` is orthogonal to `D`, and `<D,w>=3/16`.

2. The derived wavefunction coefficients give a `2w/351` term in the
   second-order coefficient of `log rho`. All other terms disappear on
   pairing with `D`. The remaining coefficient is exactly
   `(2/351)(3/16)=1/936`. The point pair `(0,0,+-3/5)` lies in the
   regular interior and has second-order coefficient difference `4/585`.
   The proof correctly treats that pair as a Taylor-jet illustration,
   not as a pointwise consequence of an `L^2` remainder.

3. The accepted [vacuum comparison](accepted_sources/ym2_signed_differences/VACUUM_COMPARISON.md),
   equation (V1a), bounds the ratio of the maximum to minimum of `rho`
   by `exp(32r/3)(104207/52043)^2`. Taking its positive square root
   gives exactly the wavefunction ratio used in (W7). Normalizing the
   Haar mean to one does not change the ratio. At `0<=r<=1/10`, the
   bound is strictly less than `7`, hence `min phi_r>1/7`.

4. The Cauchy remainder coefficient at `r<=1/10` satisfies
   `5/(9 sqrt(2))<2/5`; squaring reduces this to `625<648`.
   The polynomial bound `||u2||_infinity<=1/64+1/39+1/351<1/20`
   is valid on the entire admitted trace body. Therefore `p2>9/10`.
   The real logarithm is Lipschitz with constant at most `7` on each
   interval between `phi_r(x)` and `p2(x)`. This yields a legitimate
   `L^2` logarithm comparison, without taking a logarithm of an
   unbounded `L^2` error.

5. For `z=r u1+r^2 u2`, the bound `|z|<=7r/20<1/10` is conservative.
   The complete scalar logarithm suffix has bound
   `343 r^3/21600`. The omitted quadratic cross terms cost at most
   `r^3/60+r^4/800`. Replacing the final term by `r^3/3200` uses the
   weaker but valid `r<=1/4`. The exact sum
   `343/21600+1/60+1/3200` is less than `1/25`.

6. Adding the two errors gives less than `3r^3` for `log phi_r`.
   The density normalization scalar cancels against `D`, and
   `2||D||_2=sqrt(3)/2<1`. Consequently
   `|J(r)-r^2/936|<3r^3` on `0<r<=1/10`.

7. At `0<r<=1/3000`, the exact lower coefficient is
   `1/936-1/1000=4/58500>0`. Strictness survives at the endpoint.
   If `rho_r` depended only on `(a,b)`, its bounded logarithm would
   be orthogonal to `D`, contradicting this lower bound. The proof
   correctly excludes `r=0` from its strict conclusion.

## Scope of this review

The witness is a statement about an actual ground-state density on the
fixed compact graph and an explicit continuum interval of couplings.
Its interval coverage comes from uniform inequalities, not sampled
couplings. It establishes failure of the two-trace-only representation
for this density receiver, including failure of a product of separate
single-plaquette densities. It does not determine the full ground state,
the sign at larger coupling, graph-uniform conditional influence, or a
continuum Yang-Mills mass gap.

The earlier vacuum comparison and source operator domain are accepted
dependencies; this review checked their cited statement and the
normalization transfer, without rerunning their old verification suites.
The analytic perturbation proof is separately reviewed in
[REVIEW_PERTURBATION.md](REVIEW_PERTURBATION.md). This review does not claim
independence for that dependency from its own author. After the witness
checker was written, this reviewer ran `python -I -B check_witness.py`
from the packet directory. Its read-only receipt comparison passed,
reporting 45 orthogonality and 13 Haar controls. That execution checks
the new finite controls; it does not rerun the accepted old suites.
