# Tri-temporal hidden-coordinate calibration

This package tests the independent ChatGPT proposal that a candidate hidden coordinate can affect a closure's past-facing receipt, present operational identity, and future continuation map.

## Definitions

For a held-fixed pair of finite-machine states `(s,t)`:

```text
P = past_readout(s) differs from past_readout(t)
C = observation(s) differs from observation(t)
F = some positive-length continuation makes the same observation differ
```

The same operational observation is used for `C` and `F`; the future channel is not an unrelated programmed label. The three-bit code is `(P,C,F)`.

For retention, the package distinguishes:

- `never`: no finite word distinguishes the pair;
- `finite`: distinguishing words have a finite maximum length;
- `unbounded`: distinguishing words occur at arbitrarily large finite lengths; and
- `persistent_path`: one infinite action sequence has distinguishing prefixes infinitely often.

`persistent_path` implies `unbounded`, but the converse fails.

## Exact results

The unary deterministic census uses a fixed ordered pair `(0,1)`, binary past/operational readouts, and every labeled transition table.

| Signature | Meaning | Minimum states | Labeled count at minimum search level |
|---|---|---:|---:|
| `000` | inert for all three interfaces | 2 | 16 at 2 states |
| `001` | future-predictive only | 3 | 96 at 3 states |
| `010` | present-only, then merges | 2 | 8 at 2 states |
| `011` | present and future | 2 | 8 at 2 states |
| `100` | provenance-only | 2 | 16 at 2 states |
| `101` | provenance and future, presently hidden | 3 | 96 at 3 states |
| `110` | past and present, then extinct | 2 | 8 at 2 states |
| `111` | tri-temporal under the declared interfaces | 2 | 8 at 2 states |

Thus future relevance does not imply tri-temporal relevance, and tri-temporal relevance is not forced by the transition semantics. Each interface must be measured.

The binary-action search found the first unbounded-without-persistence machines at three states:

```text
1 state: impossible because the intervention pair must be distinct
2 states: 0 labeled machines
3 states: 64 labeled machines with fixed pair (0,1)
```

The frozen minimum witness has distinguishing language

```text
0*1 = {1, 01, 001, 0001, ...}
```

so distinguishing words occur at arbitrarily large lengths. After the first `1`, however, the state pair merges on the next move. No single infinite input has distinguishing prefixes infinitely often.

## Interpretation

The tests support ChatGPT's taxonomy as a useful measurement system. They reject two stronger readings:

1. predictive relevance alone does not make a coordinate tri-temporally constitutive; and
2. arbitrarily long finite retention does not imply one infinitely persistent lineage.

The result is finite and signature-relative. It does not establish a universal hidden `+1`, a general definition of infinity, a physical ontology, or a Millennium bridge.

## Verify

From `C:\github\NariZoo`:

```powershell
& 'C:\Users\bkbee\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' `
  -B -m unittest millennium_rprm.tri_temporal.test_tri_temporal -v

& 'C:\Users\bkbee\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' `
  -B -m millennium_rprm.tri_temporal.experiment
```

The first command reruns the exhaustive searches, differential word-oracle checks, controls, and exact frozen-result replay. The second prints the deterministic JSON result stored at [`runs/tri_temporal_01.json`](runs/tri_temporal_01.json).
