# Model comparison metrics

Grid 100x64. Steps: basin 2000, utube 6000, dam 2000.
Driven headlessly through node against the same `js/` physics the demo uses.

| scenario | model | mass err (max/final %) | settle step | residual moved/step | surface std (cells) | U-tube Δh | avg active % | label cells/step | label passes/step |
|---|---|---|---|---|---|---|---|---|---|
| basin | A binary | 0.000 / 0.000 | jitter (never) | 62.0 | 1.32 | - | 22.2 | - | - |
| basin | B momentum | 0.000 / 0.000 | jitter (never) | 47.0 | 0.96 | - | 25.1 | - | - |
| basin | C mass-level | 0.000 / 0.000 | jitter (never) | 79.4 | 0.97 | - | 25.4 | - | - |
| basin | D level-aware | 0.000 / 0.000 | 39 | 0.0 | 0.00 | - | 0.8 | 64 | 0.08 |
| basin | E D_fast (=D, exact) | 0.000 / 0.000 | 39 | 0.0 | 0.00 | - | 0.8 | 64 | 0.07 |
| utube | A binary | 0.000 / 0.000 | jitter (never) | 44.0 | - | 26.58 | 29.1 | - | - |
| utube | B momentum | 0.000 / 0.000 | jitter (never) | 22.0 | - | 26.75 | 28.1 | - | - |
| utube | C mass-level | 0.000 / 0.000 | jitter (never) | 62.6 | - | 17.94 | 23.4 | - | - |
| utube | D level-aware | 0.000 / 0.000 | 17 | 0.0 | - | 0.07 | 0.1 | 7 | 0.01 |
| utube | E D_fast (=D, exact) | 0.000 / 0.000 | 17 | 0.0 | - | 0.07 | 0.1 | 7 | 0.01 |
| dam | A binary | 0.000 / 0.000 | jitter (never) | 90.0 | 2.36 | - | 39.0 | - | - |
| dam | B momentum | 0.000 / 0.000 | jitter (never) | 43.0 | 0.84 | - | 41.6 | - | - |
| dam | C mass-level | 0.000 / 0.000 | jitter (never) | 369.7 | 6.55 | - | 43.3 | - | - |
| dam | D level-aware | 0.000 / 0.000 | 54 | 0.0 | 0.00 | - | 1.4 | 177 | 0.09 |
| dam | E D_fast (=D, exact) | 0.000 / 0.000 | 54 | 0.0 | 0.00 | - | 1.4 | 176 | 0.06 |
| stress | A binary | 0.000 / 0.000 | jitter (never) | 162.0 | 1.02 | - | 100.0 | - | - |
| stress | B momentum | 0.000 / 0.000 | jitter (never) | 102.8 | 1.02 | - | 99.8 | - | - |
| stress | C mass-level | 0.000 / 0.000 | 1045 | 0.0 | 0.76 | - | 22.5 | - | - |
| stress | D level-aware | 0.000 / 0.000 | 59 | 0.0 | 0.74 | - | 2.9 | 110 | 0.56 |
| stress | E D_fast (=D, exact) | 0.000 / 0.000 | 59 | 0.0 | 0.74 | - | 2.9 | 110 | 0.55 |

## Compressibility sweep (model C, U-tube)

| MaxCompress | final Δh (cells) | residual moved/step |
|---|---|---|
| 0.02 | 26.8 | 95.4 |
| 0.05 | 24.2 | 83.6 |
| 0.1 | 21.9 | 73.2 |
| 0.2 | 17.9 | 62.6 |
| 0.4 | 13.9 | 54.7 |

## Model D relabel-amortization sweep (U-tube)

| RelabelEvery k | final Δh (cells) | avg label cells/step | mass err final % |
|---|---|---|---|
| 1 | 0.07 | 7 | 0.000 |
| 2 | 0.06 | 5 | 0.000 |
| 4 | 0.07 | 4 | 0.000 |
| 8 | 0.05 | 3 | 0.000 |
| 16 | 0.07 | 3 | 0.000 |
