# RPRM pi three-level 3-4-5 matrix 01 evidence

Status: **SUPPORTED BOUNDED RECEIPT**  
Date: 2026-08-21

## Release identity

- packet: `C:\github\RPRMResearch\RPRM_PI_THREE_LEVEL_345_MATRIX_01`
- archive: `C:\github\RPRMResearch\RPRM_PI_THREE_LEVEL_345_MATRIX_01.zip`
- archive SHA-256: `5C4BB0BDF8F1B155A3F20EBED3453B1B29A5ACC6788376819AD2C4597D6321FA`
- verifier SHA-256: `E248BAC39014EFBDAD9047E15B010FEA65DBC619531FFA57F671880DB16CC8C7`
- `RESULTS.json` SHA-256: `61934E0BDE360651D80F78335FAB84BA1C9EBB195C24028681ECD092A0608AFC`
- `MANIFEST.sha256` SHA-256: `52DD8E029CBD782C3BDB074B6B5134E40DB884537B13224F3E093F9EA0E92CB6`
- result root: `A5E00A1C5E2B7B21EE070C23FE355E9D6147EEA5A7A25BF823FA20502445BC36`
- checks: `4,193`
- flat ZIP members: `10`

## Pins and acceptance

The release pins the final receiver-saturation seal 03, the final
minimum-completion algebra 01, and one raw million-digit ingress. The raw
ingress has SHA-256
`B50EA720602439DCB8A56265B75FADFA4D0A0FBD46D9705693DDE14B8A053FB0`;
ASCII-digit normalization has length `1,000,001` and SHA-256
`130203EB055A962B8441AF76C22B75627EC18C672A485904E567F59251E8EE18`.

The live stored/manifest command exited zero:

```powershell
python -I -B .\verify_pi_three_level_345_matrix.py --require-sources --verify-stored --verify-manifest
```

The archive was expanded into a fresh temporary root beside fresh copies of
both pinned parent directories and archives. The same command exited zero.
The extracted release contained exactly ten files and no subdirectories.

## Supported result

An exact Gaussian-integer Machin certificate and rational alternating-series
bounds certify only the prefix `3.141592653589`. Literal overlapping scans on
the hash-pinned ingress give the nested fibers
`MANY(1006) -> MANY(2) -> ONE` for `141`, `141592`, and `141592653`.
Two-sided radius-two flanks distinguish all 96 occurrences of `3141` within
that carrier.

At decimal layers `0..12`, the receipt proves the two descriptions of one
finite half-open cell with `p+q+1=10^n` and involutive reflection. It does not
construct a terminal digit of pi.

For the frozen addressed window `3|141|592|653|5`, the declared endpoint
grammar uniquely closes the decimal alphabet at endpoint pair `(3,5)` among
all 45 pairs `A<B`. The contextual zipper exhausts 45,000 endpoint/code
candidates, admits 4,000 exact encode/decode images, and classifies code `123`
as `MANY(10)` without endpoints but `ONE` at context `(3,5)`. The single
frozen center has the computed refinement `MANY(4) -> MANY(3) -> ONE(9)`.

The binary seam is separately typed. `0|1` and `1|0` are the two oriented
presentations; orientation erasure produces one coarse output, while inverse
refinement reopens two oriented preimages. Reset is a tagged constructor in
`Option(Bit)={Reset,Active(0),Active(1)}`. Raw decoder `None` is rejected as
reset, and decimal carry value `10` is not identified with the bit word `1|0`.

## Claim ceiling

This evidence does not establish correctness of all ingress digits, a pi
generator/predictor/random-access oracle, a terminal digit, normality,
randomness, statistical significance, universal number semantics, intrinsic
binary direction, free compression, physical dimension/time, a musical or
biomechanical theorem, authentication, or novelty. Literal occurrence results
belong only to the pinned ingress; arithmetic interpretations belong only to
their declared receivers.

Source ingress: https://www.angio.net/pi/digits/pi1000000.txt
