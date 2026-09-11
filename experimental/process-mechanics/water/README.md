# Water composition kit

**Question:** Do exact whole-window range and reach answers for one declared
latent law agree between direct evaluation and child-summary composition on
`(4,8]`?

**Carrier / model:** Nineteen synthetic exact laws (`const10`, `ramp`, eight
triangles, seven steps, plus two named extras). Half-open `(t0,t1]`. Primary
predicate: exists value ≥ 11.5. Auxiliary control: reach ≥ 11.

**Known inputs:** Candidate law id, full phase/event schedule, requested
interval, contract and catalogue ids, boundary convention.

**Hidden / excluded:** Unknown physical hydraulics; independently varying
control schedules; field-water safety claims.

**Readout:** Parent interval summary with attainment flags and reach flags;
structural join status; honest bounds-eval / join counters.

**Ordinary comparator:** Direct `interval_bounds` on the parent window.

**Null / hostile cases:**
- Endpoint-only spoof for `triangle_p4_phi0` returns `JOIN_OK` with wrong
  contents `[10,10]` while exact is `[9,11]`; primary 11.5 stays false;
  auxiliary reach-11 differs.
- Missing child → `OPEN_MISSING_CHILD` (not NONE).
- Changed contract → `REJECT_CONTRACT_MISMATCH`.

**Evidence grades:**
- `W-COMP-01`: `REPRODUCED_PUBLIC_PORT` (19×4 local replay).
- `W-TRUST-01`: `REPRODUCED_PUBLIC_PORT` (frozen spoof numbers).
- `W-REUSE-01`: `NEW_ILLUSTRATIVE_DEMO` (local context keying; not PR14 audit).

**Run:**

```sh
python -I -B experimental/process-mechanics/water/example.py
python -I -B experimental/process-mechanics/water/check.py
```

Requires the additive `rprm.process_mechanics` package on `PYTHONPATH`
(repository root after integration, or `public_payload` during staging).

**Limitations:** Composition preservation under correct children is not a
Navier–Stokes solution, hydraulic speed claim, or child-truth certificate.

**Rights:** Original kit software under 0BSD; prose/example data under CC0.
