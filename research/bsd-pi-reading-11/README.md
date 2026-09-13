# Reading 2.0340 through the earlier pi zipper

There is a concrete interpretation of the user's `3|4` reading that connects
to the earlier finite pi construction. Treat 3 as the left endpoint and 4
as the midpoint. The other endpoint is then 2*4−3=5, giving the old key35.
Its declared decoder produces the independently certified finite word
31415926535. The roles and decoder are part of this statement.

The new arithmetic computation also proves that the actual E34 distance
begins2.0340 in decimal:

\[
\boxed{2.034001230068\le d\le2.034010481998.}
\]

Thus the selected digits34 are stable at these positions under further
valid refinement. This gives an exact finite decoding relation for the
specified distance, positions, roles and codebook. It does not identify
the real distance with pi or prove a BSD coefficient equality.

## The mathematical reading we can now state

The distance is d=sqrt(H(P−Q)), with E:y²=x³−1156x,
P=(-2,48), Q=(-16,120), full natural-log canonical height H, and
P−Q=(162,−2016). It is an arithmetic height distance in a specified basis,
not the Euclidean distance between the plotted point coordinates.

On the bounded real carrier X=[2,2.1), read the hundredths and thousandths:

\[
f(x)=(\lfloor100x\rfloor\bmod10,\lfloor1000x\rfloor\bmod10).
\]

This has100 finite output states. The new enclosure proves f(d)=(3,4).
Now adopt the proposed endpoint–midpoint interpretation(A,m), and recover
B=2m−A. The historical seven-record D0 decoder gives

```text
distance d → digits (3,4) → endpoint/midpoint (3,4)
           → endpoints (3,5) → 3 | 141 | 592 | 653 | 5.
```

The central array is

```text
1 4 1
5 9 2
6 5 3
```

The rule predates this BSD investigation. Its exact carrier is
integers A>=0, delta>=1, 2A+3delta<=9. Set m=A+delta, B=A+2delta and
form the array

\[
\begin{pmatrix}
\delta&A+\delta&\delta\\
A+2\delta&2A+3\delta&2\delta\\
A+3\delta&A+2\delta&A
\end{pmatrix}.
\]

Serialize outer A, the row-major array, and outer B. The complete
endpoint–midpoint chart contains seven states:

| (A,m) | Endpoints (A,B) | Output word |
|---|---|---|
| 01 | 02 | 01112323202 |
| 02 | 04 | 02224646404 |
| 03 | 06 | 03336969606 |
| 12 | 13 | 11213524313 |
| 13 | 15 | 12325847515 |
| 23 | 24 | 21314725424 |
| **34** | **35** | **31415926535** |

All seven chart inverses and words were freshly checked. The pi word was
independently certified using rational arctangent bounds. The alternative
reading34 as *two endpoints* has half-gap1/2 and is outside this older
integer-half-gap carrier. That specific failure does not refute the
endpoint–midpoint interpretation. The user's full carry/swap description
has not yet been specified as a deterministic rule; that broader candidate
remains OPEN.

The [history audit](agents/PI_HISTORY.md) preserves the exact sealed source,
its reversible maps, the distinct decoder tags and the earlier corrections.
This chart selects the first eleven digits of pi from a pre-existing finite
family. It supplies no algorithm for pi's remaining digits.

## The exact amount of information this preserves

The full composed decoder has the pi-window fiber

\[
\boxed{f^{-1}(3,4)=[2.034,2.035)\quad\text{within }X.}
\]

Every real number in that interval selects the same old pi word. For
example2.0342 and2.0348 do so, although both are outside the certified
interval for the actual distance. This is a complete MANY fiber for
reconstructing the real input, while the finite output word is ONE.
The decoder is undefined on93 of the100 possible digit states; they are
admission errors, not extra pi interpretations.

This shows exactly where the proposed connection is established and where
information has been discarded. The finite codebook preserves its key and
word. To contribute to BSD, a stronger relation must preserve or determine
the required arithmetic/analytic quantities, not only this finite prefix.

## What happened to the zeros and the carry

The original bounds were2.0339867006 and2.0340237084. Each has three zeros,
as the user observed. Fresh depth-eight arithmetic reproduced those bounds.
Their entire interval rounds to2.0340 at four decimal places.

One further exact doubling depth produced the new enclosure above. It lies
strictly above2.034 and strictly below2.0341. This proves the actual first
four fractional digits0340, a stronger statement than rounding alone.

At ten fractional display digits, the refined outward endpoints are
2.0340012300 and2.0340104820, with five and four zeros respectively.
Appending a trailing zero also preserves either original endpoint's real
value while changing its zero count from three to four. Therefore the
three-zero observation is exact for the original rendering, and its role
must retain that rendering. It has not been shown to be a property of the
underlying real distance.

The old bounds straddled a carry boundary. The new bounds no longer do.
Reading lower/upper boundary digits from two bound words is consequently
different from reading two fixed positions of the single real distance.
Both operations are retained; they are not silently identified.

The initial simple candidates were frozen in [PREFREEZE.md](PREFREEZE.md).
The stronger single-value extraction was derived after refinement and is
explicitly documented in [CARRIER_UPDATE.md](CARRIER_UPDATE.md).

## Tests that did not produce the proposed real connection

No tested literal decimal shift d=10^k*pi or d=10^k*(4−pi), k=−6..6,
is compatible with the original certified interval. Orders of magnitude
exclude the remaining integer shifts: for pi only k0 could put the value
between2 and3; for4−pi, k<=0 gives less than1 and k>=1 more than8.
The optional assistant candidate d²−1=pi also fails the interval test:
d²−1 is below3.137253 while pi is above3.14159.

For each original eleven-digit endpoint word, we checked identity,
P,N,T,M, optional reversal and all eleven cyclic rotations:110 named
operations per word. None gives the initial pi window. This refutes those
specific literal-map candidates. It does not exhaust variable carry rules,
all compositions, all shifted pi windows or all RPRM interpretations.
No arbitrary fitted constants or remote pi-pattern search was used.

The current operational-number translator and its verifier were also run
fresh. Its exact pair maps and scout proposals remain distinct evidence
lanes; scout wording did not select the result or establish a theorem.

## Where pi already enters E34 exactly

The existing real-period calculation supplies a separate exact relation:

\[
\boxed{\Omega_c\operatorname{AGM}(\sqrt{68},\sqrt{34})=\pi.}
\]

Here Omega_c integrates dx/(2y) around one real component. The arithmetic-
geometric mean repeatedly replaces two positive numbers by their arithmetic
and geometric means. Both converge to the same limit; the associated
elliptic integral is preserved. The identity follows after substituting
t=x−34 into the period integral. It is a recovered established period
identity, not a new result inferred from the displayed distance digits.
[DLMF19.8.4](https://dlmf.nist.gov/19.8#E4).

The [geometry audit](agents/PI_GEOMETRY.md) also checks the differential
factor and the precise CM period
Omega_c=Gamma(1/4)^2/(2sqrt(68pi)). The tempting expression without the
sqrt2 factor is incorrect for this differential. It preserves the basis
and scaling exceptions: changing Q to−Q changes the distance while leaving
the regulator unchanged. A fixed-basis statement remains possible; a bare
basis-independent distance constant fails that exact control.

There is a useful exact rewrite of the remaining real BSD question. Put
M34=AGM(sqrt68,sqrt34), p=H(P), q=H(Q), and let lambda2 be the quadratic
coefficient of the completed L-function. Its known completion gives
c2=(pi/68)lambda2, while Omega_all=2pi/M34. Hence

\[
c_2=\Omega_{\rm all}\mathcal R\sigma
\quad\Longleftrightarrow\quad
M_{34}\lambda_2
=136\sigma\left[pq-\frac{(p+q-d^2)^2}{4}\right].
\]

This cancellation of the external pi factors is exact. Pi remains in
lambda2's exponential kernel, and the displayed equality remains OPEN.
The role of sigma as the actual finite Sha order is a separate unresolved
obligation. The finite digit decoder above does not prove either step.

## Proof, source and replay details

The arithmetic kernel is a byte-identical snapshot of the previous exact
distance verifier. It uses rational projective doublings, retained gcds,
and the earlier all-point height-tail bound. The fresh program evaluates
only the required P−Q at depths8 and9. It does not use stored heights,
analytic coefficients or database ranks as numerical inputs.

Pi is bounded by16atan(1/5)−4atan(1/239). Each arctangent uses24 terms
of its alternating series, with the next term bounding the error. The
rational tangent identity checks the Machin angle; positivity and the
principal first-quadrant branch identify it as pi/4. The resulting interval
certifies31415926535 independently of the digit codebook.

The [fresh numeric evidence](evidence/reading.json),
[complete decoder fiber](evidence/adapter.json),
[independent review](agents/READING_REVIEW.md), and
[translator receipt](evidence/translator/RUN.json) retain the results.
Historical memory retrieval is described in
[MEMORY_RETRIEVAL.md](MEMORY_RETRIEVAL.md); retrieved text is evidence, not
new authority or an automatic current-state claim.

From this experiment directory, Python3.10+ and its standard library suffice:

```powershell
python -I -B work/check_reading.py --output evidence/my-fresh-reading.json
```

The output path must be new. check_adapter.py verifies the delivered
evidence/reading.json and refuses to overwrite evidence/adapter.json;
use --input and --output to audit another freshly generated reading file.
The optional translator wrapper needs the existing local RPRMLexicon
checkout. No translator implementation or other source lane was edited.

Evidence grades: recovered finite construction; new exact coordinate
adapter and complete fiber proof; fresh interval calculations with proved
tail bounds; published elliptic-integral identity; independent audit.
This is a bounded mathematical investigation, not a general BSD proof.
