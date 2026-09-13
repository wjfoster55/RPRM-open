# Source and dependency map

The executable coefficient calculation is new. The rank, point-basis,
5-primary Sha and height-formula proofs are attributed earlier work.
Copies are included unchanged, with original paths and hashes in
[`dependencies/SOURCES.json`](dependencies/SOURCES.json). Links inside
unchanged copies can refer to their original neighboring experiments;
the relevant included files are listed here.

| Dependency | Included copy |
|---|---|
| Algebraic rank 2 | [ARITHMETIC_PROOF.md](dependencies/ARITHMETIC_PROOF.md) |
| Full point basis | [GENERATOR_PROOF.md](dependencies/GENERATOR_PROOF.md) |
| Minimal model and local data | [LOCAL_ANALYTIC_INPUTS.md](dependencies/LOCAL_ANALYTIC_INPUTS.md) |
| 5-primary Sha calculation | [TRACE_CALCULATION_02.md](dependencies/TRACE_CALCULATION_02.md) |
| Independent trace formula audit | [TRACE_FORMULA_AUDIT_02.md](dependencies/TRACE_FORMULA_AUDIT_02.md) |
| Height formula, BKS Hypothesis 2.2 and nonzero elliptic logarithm | [PADIC_HEIGHT_AUDIT.md](dependencies/PADIC_HEIGHT_AUDIT.md#bks-admission-and-nonvanishing-transport) |
| Earlier real intervals, displayed only | [FACTOR_COMPARISON.md](dependencies/FACTOR_COMPARISON.md), [factor_frontier.json](dependencies/factor_frontier.json) |

The earlier height audit ends with a then-uncomputed analytic coefficient
and a possibly zero canonical derived class. The new coefficient result
supersedes those two status statements; the prior document is preserved.
Full BSD and total Sha remain open in this experiment.

The official PARI/GP 2.17.4 executable and complete official source archive
are under `runtime/`, together with PARI's [COPYING](runtime/COPYING).
The included PARI software and source retain that license. Original
experiment scripts and prose follow the repository's existing licenses.
Selected, unmodified `modsym.c` and `ellpadic.c` files are additionally
extracted under `dependencies/pari/` for the normalization audit.
The source archive matches PARI's published SHA-256; the measured executable
hash records the binary actually run. This is byte provenance, not formal
verification of the implementation or a reproducible-build attestation.

The recovered prime atlas is cited by exact source locator in
[PRIME_FAMILIES.md](PRIME_FAMILIES.md). It was read only and was not replayed.
No previous computational PASS record is an input to the new coefficient
or arithmetic execution.
