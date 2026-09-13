# BSD trace 02 return

We closed one previously open arithmetic obligation for
**E34: y²=x³−1156x**: its **5-primary Sha subgroup is zero**.
That means there is no nonzero Sha element whose order is a power of5.
This is additional progress beyond the earlier two-primary result.

The calculation was exact. One construction gives a unit multiple of the
required trace equal to100 modulo125. A second construction gives25
modulo125, with a coherent sign ambiguity. Both prove precisely two
factors of5 divide the trace. The checked published theorem then turns
that valuation into the stated Sha conclusion; this is not a decimal
estimate or an assumption of BSD.

The completed Yang–Mills work supplied a useful methodological comparison:
retain the complete relevant family and preserve the operation being
measured. Here we proved which512 division points form the arithmetic
orbit and why each of the256 trace values occurs twice. Including the
opposite orbit would instead produce a false zero. Its own lower-bound
argument and physical assumptions were not imported as a BSD theorem.
The active YM task was inspected read-only and was not altered or interrupted.

Your idea of a zero at one level hiding a remainder has a precise instance
here. The calculation is zero modulo25, yet100 modulo125. Keeping that
next level is exactly what distinguishes the required valuation2 from a
larger valuation. It does not make the actual number zero.

The remaining proof gap is still substantial. Other prime-primary parts
of Sha are unexamined, its total order is not established here, and the
full complex BSD leading-coefficient identity remains open. The useful
next question for a general argument is: **what exact relation forces the
analytic quantity and the arithmetic quantity to agree?** In the YM
argument, uniqueness comes from an actual contraction equation. We have
not constructed a shared equation or a uniform arithmetic spacing theorem
that supplies that comparison for BSD. Matching approximations does not
fill that missing premise.

The [mathematical explanation](TRACE_CALCULATION.md) and
[CM orbit audit](TRACE_FORMULA_AUDIT.md) give the proof and theorem conditions.
The [alternative proof](DIVISION_ORBIT.md) and
[YM comparison](YM_TO_BSD.md) preserve their respective scope limits.
The [rebrief](BSD_REBRIEF.md) records the current boundary.

All six fresh execution stages passed in the isolated return run, including
the two moduli, separate chord orbit, independent ring aggregation and
independent torsion reassembly. Runtime was about9 seconds using only
Python's standard library. See `runs/return_validation/RUN.json` for source
hashes, logs and cross-precision checks. Earlier rank proofs are separately
attributed in `dependencies/`; their old PASS records were not calculation
inputs. This remains a written computational proof using named published
theorems, rather than a proof-assistant formalization.

This bounded p=5 experiment is complete. No paper, publication, automation,
other-prime campaign or modification of another research lane was started.
