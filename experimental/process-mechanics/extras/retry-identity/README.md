# Retry identity

Finite teaching toy: identical payloads may be an intentional second operation
or a retry/duplicate delivery. Compare payload-only collapse with
`rprm.core.Occurrence` identity.

Evidence grade: `NEW_ILLUSTRATIVE_DEMO`. Not a distributed transaction system.

```sh
python -I -B experimental/process-mechanics/extras/retry-identity/example.py
python -I -B experimental/process-mechanics/extras/retry-identity/check.py
```
