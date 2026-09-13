# BSD rank-two rebrief — 12 September 2026

**Curve:** E34/Q, y²=x³−1156x. **Status:** rank equality proved for
this case; full BSD and general BSD remain OPEN in this investigation.

| Readout | Established result | Evidence |
|---|---|---|
| Rational group | Z·(−2,48) ⊕ Z·(−16,120) ⊕ (Z/2)² | Complete descent and integral-basis proof |
| Basis index | 1; every possible finite index covered | Height cutoff 987; 38,205 reduced abscissas; all 25 affine points accounted for |
| Two-primary Sha | Sha[2^∞]=0 | Complete 16-class 2-Selmer group, equal to the Kummer image |
| Minimal local data | N=18496; c_2=c_17=4; root number +1 | Minimality, exceptional 2-adic Tate steps and family sign checked |
| Analytic rank | Exactly 2 | Exact lower zeros via cited low-rank theorem; positive second coefficient |
| Original coefficient | 6.38511803 ≤ L''(1)/2 ≤ 6.38518585 | Exact interval head plus all-term tail |
| Completed coefficient | 138.20634136 ≤ Λ''(1)/2 ≤ 138.20780907 | Λ(s)=(68/π)^s Γ(s)L(s) |
| Real period | [0.899358321446, 0.899358321447] | Minimal dx/(2y), both real components, rational AGM enclosure |
| Full-basis regulator | [7.099053962, 7.100201634] | Certified full x-height Gram determinant |
| BSD quotient | [0.999920542, 1.000092816] | Rigorous comparison only; not identified with #Sha |
| Odd-primary / total Sha | NOT_ESTABLISHED | Missing applicable primewise/global argument |
| Full leading-coefficient identity | NOT_ESTABLISHED | Numerical enclosure does not provide the connecting theorem |

**User correction retained:** 0.6→0.4 has signed step −0.2;
0.6→0.5 has half-step −0.1. Midpoint plus directed gap recovers
both endpoints. No assertion that their squares cancel was attributed
to this correction. The complete carry recurrence and its relation to
the L-function coefficients remain OPEN.

**Failed obligations retained:** cutoffs 40 and 80 did not attain the
declared width with their tail bounds; cutoff 160 succeeded using 7,360
panels. Shallow mod-4 solubility failed to imply 2-adic solubility;
mod-8 obstruction was required. A blanket kernel-convexity assumption
was refuted; signed derivative bounds were used. The old E5 full-BSD
theorem fails both its conductor and analytic-rank conditions here.

**Freshness:** the seven-stage final replay copied source only and
recomputed its evidence. Standard library Python; no curve database
rank or expected L-value. `RUN.json` records source/receipt hashes and
execution logs. Written theorem arguments remain necessary dependencies;
no formal proof assistant was run. This is an independently checked
standard-method case study, not a new proof of general BSD.

**Next precise gap:** derive a rule connecting the retained directed
operation with the actual arithmetic and analytic data, strong enough
to force exact lower zeros and the full arithmetic leading coefficient.
Reflection supplies parity; it does not supply all these identities.

**Exact Sha completion criterion:** with the group structure and p=2
result already proved, #Sha=1 is equivalent to |Sel_p(E/Q)|=p² for
every odd prime p. `SHA_ORDER_CRITERION.md` proves the reduction; the
all-odd-prime premise is OPEN. Proving Sha=0 by this route would still
leave the exact analytic leading-coefficient identity to establish.
