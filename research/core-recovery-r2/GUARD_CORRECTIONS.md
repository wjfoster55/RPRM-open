# Guard corrections (RCF01-R2)

These are corrections to the reviewed R1 portable implementation. They
are not backdated source or protocol changes. Frozen RCF01-envelope-1 and
RCF01-envelope-1-r1 bytes are unchanged.

## Output family

Addition is over Q. The retained seven values of a sum do not certify a
global Boolean output class. `hxy+hxy` has C2 zero and omitted value 2; the
output family is `rational_cube`. Multiplication of Boolean-valued laws
remains Boolean. Mixed Boolean/rational cube operands are explicitly coerced
to `rational_cube`. A `boolean_cube` promotion whose table leaves `{0,1}` is
rejected. Unique C2 output remains `ONE`; candidate-family propagation for
Q-sums stays outside this API.

## Map interface

`apply_fixed_receiver_map` is the certified generic entry for named
coordinate maps and uses the same contract gate as `apply_input_map`.
Arbitrary eight-site maps are not certified there. `apply_raw_site_map` is
an unchecked/reference helper: it validates the site carrier, unsets
`degree_bound`, and reduces the contract so the result is not a certified
public continuation.

## Aggregate runner

`run_portable.py` computes one verdict from every required job, including
starter unless `--skip-starter` reports that narrower scope. JSON status,
printed status, and process exit use that verdict. Expected omit/duplicate/
unexpected coverage rejection requires a FAIL receipt containing
`Coverage mismatch`. An unrelated crash, missing output, or malformed
output is not that rejection.
