# RCF01-R1 review package

Start with `REVIEW.md`. `CURSOR_RCF01_R2.md` is the one proposed active handoff for a bounded repair of the reviewed implementation. The original uploaded package was not modified.

## Contents

- Review, repair assignment, and pinned submitted source snapshots.
- Actual full unmodified portable replay, including the 26-case envelope and 12-case starter.
- Independent direct-table arithmetic/map checks and reproducible interface counterexamples.
- Real export-deletion/ID-only controls.
- Runner-only fault-injection controls, explicitly separate from mathematical execution.
- Preservation and source-identity records.

## Reproduce

Extract the user's outer `core-recovery-r1.zip`. Select the corrected inner `core-recovery-r1/dist_02/RCF01-portable-r1.zip` and extract it into a fresh directory. Its entries are at the root, without an extra wrapper folder. Then use new output directories:

```text
python -B <extract>/run_portable.py --output-dir <fresh-full-replay>
python -B independent_review.py --package <extract> --output-dir <fresh-independent-review>
python -B review_runner_controls.py --package <extract> --output-dir <fresh-runner-controls>
```

The independent reviewer script is a diagnostic tied to the reviewed R1 API. It exits successfully when it records its checks, including reproduced defects; that exit does not certify the candidate implementation. A subsequent explicit API restriction may require an honestly versioned adaptation of the generic-map diagnostic.

The runner harness replaces expensive child computations in disposable copies with clearly marked fixtures. Its output tests aggregate logic only, never the mathematical cases. Use the separate unmodified full replay for mathematical execution evidence.

All tables are exact Fraction arithmetic. Do not run these scripts with Python optimization that disables assertions. No installation, network access, or remote actions are required.

`MANIFEST.json` pins the review package's delivered files, excluding itself. The submitted package's own manifest is a separate source artifact, not this review's result.
