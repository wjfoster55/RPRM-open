# General BSD starting investigation 01

The current user explicitly authorized working toward a general argument.
This expands the earlier one-curve experiment's scope without changing its
results. Historical instructions to stop that experiment are preserved in
its files; they do not cancel the newer request. This is a research note
and executable set of controls, not a paper or a general BSD solution.

- [Readable return](RETURN_TO_WILLIAM.md)
- [General reconstruction theorem and fibers](RECONSTRUCTION.md)
- [Independent reconstruction audit](TOWER_AUDIT.md)
- [Selmer certificates and primary stabilization](SELMER_TOWER.md)
- [General analytic formula, tail and remaining exact zeros](ANALYTIC_BRIDGE.md)
- [Requirements for the carry/swap bridge](CARRY_BRIDGE.md)
- [Claim ledger](CLAIM_LEDGER.json)

## Reproduce

Use Python 3.10 or newer; no additional libraries or network are needed for
the executable checks. The sources do not read prior PASS records.

From this directory on Windows:

```powershell
py -3 -I -B work/check_general.py --output evidence/my_fresh_checks.json
py -3 -I -B work/mellin_tail.py --alpha-lower 1/5 --coefficient 2 --cutoff 40
```

On another system use `python3` in place of `py -3`. Choose a new output path
for each check run: an existing receipt is not overwritten. The current
final-source receipt is `evidence/general_checks_release.json`, with its
execution log alongside. The earlier six-group receipt is preserved as an
intermediate run from before the tail utility was added; its source hash
differs by design. The intermediate seven-group `general_checks_final.json`
predates added audit controls and exact-input guards. The release receipt
contains seven groups and hashes both executed source files.

The tail command is an example of a conditional analytic bound, with no
curve assigned. It requires a separately proved lower bound on
alpha=2*pi/sqrt(N), correct Euler data and the stated all-coefficient theorem.
It does not compute a finite integral head or infer an analytic rank.

## Verification scope

The first executable checks abstract groups Z^r plus finite cyclic torsion,
with r=0..3 and moduli 1..12; a rank-two bounded reconstruction example;
12 levels of the inverse-of-three tower; actual E5 point witnesses for five
levels; rank-two sublattice controls; 1,875 finite plateau cases; and exact
polynomial controls. It also checks 84 rational tail cases plus five invalid
inputs, the independent audit's 40 levels and 101 fixed bounds, and Gram
normalization/threshold controls. Each finite range is an operational bound, separate from the written
universally quantified statements.

E5's primitive generator is an explicit prior theorem dependency for the
actual-curve nonrealizability argument. This package does not re-prove it.
The source and earlier proof are at
`../bsd-e5-completion/GENERATOR_PROOF.md`. That path and the analytic E5
derivation links refer to the unchanged sibling experiments in this workspace.
The generic group controls and tail utility run without those directories.

Assertions cover substantive distinguishing cases; a PASS is finite evidence,
not a proof of the standard cohomology, height, modularity or low-rank theorems
cited in the notes. Original general BSD and the unspecified carry law remain
OPEN. No performance or literature-novelty claim is made.
