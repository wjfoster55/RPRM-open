# Cancer-models kit

**Question:** When do finite candidate joins resolve, stay ambiguous, go empty,
or remain incomplete — and when does a numeric fit fail measurement admission?

**Carrier / model:** Six synthetic candidates with declared observable fields
and active-control / plan tags. Independent absolute tolerance 0.01.

**Examples:**
1. One-reading null: a single `D` reading resolves the easy catalogue.
2. Empty joint family: individually compatible readings from different
   candidates yield `EMPTY_FAMILY` together (not a fabricated shared identity,
   and not a NO_EVENT claim).
3. Measurement admission: pixel-space arithmetic without calibration, coverage
   and estimator equivalence stays `PARTIAL`.

**C1 figure lane:** closed as accepted partial measurement. This kit does not
redigitize figures or reopen landmark analysis.

**Run:**

```sh
python -I -B experimental/process-mechanics/cancer-models/example.py
python -I -B experimental/process-mechanics/cancer-models/check.py
```

**Non-claims:** no clinical risk tool, treatment advice, patient-data entry, or
malignant-transformation evidence.
