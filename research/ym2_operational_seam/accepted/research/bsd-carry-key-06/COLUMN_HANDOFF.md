# The zero-column compression and pending shadow handoff

William's next two corrections supply these task constraints:

- Add the refined coefficient representative and precision modulus:
  2301+3125=5426; a zero may allow a column to be removed or merged,
  producing a display such as 566.
- Treat 566 as an intermediate process state. A carry or shadow handoff
  follows; it is not yet the terminal value to use. The cue is that five
  can become six in a shadow chart.

The following is one explicit mathematical implementation. Its maps and
finite fibers are proved; choosing this as the intended BSD handoff
remains a candidate. No terminal readiness criterion has been supplied.

## 1. The compression is exact with its column rule

For a four-digit source n=1000a+100b+10c+d, leading zeros retained,
define

\[
F(n)=100a+10(b+c)+d=10\lfloor n/100\rfloor+(n\bmod100).
\]

It merges the two middle columns by adding them. Ordinary output
carrying is allowed: F(9999)=1089, so the actual output carrier is
0,...,1089, not an assumed three-digit interval.

In the current case,

\[
F(2301)=231,\quad F(3125)=335,\quad
F(5426)=566=231+335.
\]

The zero in the first operand enables literal deletion of that column
there. The matching operation on the second operand combines 1 and 2.
It is not permission to delete an unrelated nonzero contribution.

For n+m<10000, the exact general addition law is

\[
F(n+m)=F(n)+F(m)-90\kappa,
\quad\kappa=\left\lfloor\frac{(n\bmod100)+(m\bmod100)}{100}\right\rfloor.
\]

Write n=100q+r and m=100s+t to prove it directly: replacing r+t by
r+t-100k and q+s by q+s+k changes the folded total by -90k.
This is precisely the carry from the tens to the hundreds column.
For the current operands k=0. The hostile case 99+1 has
F(99)+F(1)=100 but F(100)=10, exhibiting the missing carry correction.
All 10,000 local remainder pairs were checked.

## 2. Retaining context restores this coefficient

The complete width-four fiber F^-1(566) has ten totals:

    4796 4886 4976 5066 5156 5246 5336 5426 5516 5606

Subtracting the known modulus 3125 gives ten candidate coefficients,
all in its canonical residue range:

    1671 1761 1851 1941 2031 2121 2211 2301 2391 2481

Retaining either the known zero in the coefficient's tens column or
its earlier residue 426 modulo 625 selects exactly ONE(2301).
The program enumerates all 3,125 canonical coefficient candidates;
this is a complete fiber, not a search stopped at the desired answer.

Thus this compression can be reversible with the retained context.
Knowing the output 566 or zero mask after computing the coefficient
does not independently predict it. An arithmetic argument forcing
that mask beforehand would select this lift; that argument is missing.

## 3. A precise five-to-six shadow map

Use the recovered digit maps M(d)=9-d and N(d)=(-d) modulo 10.
Their directed composition S=N after M satisfies

\[
5\xrightarrow M4\xrightarrow N6,
\qquad S(d)=d+1\pmod{10}.
\]

Order matters: M after N gives cyclic subtraction by one. These are
uniform digit operations at a fixed width, not positional increment
of the integer. An old checkpoint guard {0,5} transports under S to
{1,6}. That explains how six can occupy the corresponding checkpoint
role in a shifted chart. It does not assign universal safety to a
digit or override the user's current intermediate-stage label.

For width four, M4(n)=9999-n. The exact operation on the compressed
carrier is

\[
F(M_4n)=1089-F(n).
\]

So its transported mirror sends 566 to 523. Applying a three-digit
mirror directly gives 433, differing by90. Compression changed the
column weights and hence the mirror's center. This is a concrete
normalization correction at the handoff.

## 4. Why the next shadow needs a carry record

Apply S independently to each of the four original source digits:

| Original source | Compressed | Source after S | Compressed after S |
|---:|---:|---:|---:|
| 5426 | 566 | 6537 | 687 |
| 4796 | 566 | 5807 | 587 |

Therefore S does not have a single induced next value on the bare
compressed observation 566. Its complete next-output fiber there is
{587,687}. Of all 1,090 reached folded outputs, 980 have this kind
of ambiguity for S. Applying S directly to the three digits 566
instead gives 677; this is a different declared operation.

The missing information has an exact, small form. For each digit j,
retain a weighted occurrence count

\[
W_j=100[a=j]+10[b=j]+10[c=j]+[d=j].
\]

Then sum(W_j)=121, F(n)=sum(j W_j), and

\[
F(S_4n)=F(n)+121-10W_9.
\]

Each source digit rises by one, except a9 which wraps and contributes
an extra subtraction of ten times its retained column weight. Thus
W9 is precisely the immediate wrap information needed here.
For repeated operations retain the entire W record, which updates as

\[
W'_j=W_{j-1\bmod10}\quad(S),\qquad
W'_j=W_{9-j}\quad(M).
\]

Both operations are total and invertible on their reached W carrier;
their updates and every future folded readout are exact. W forgets
only the order of the two middle source digits. It preserves their
multiplicity. Operations treating those two positions differently
require another audit or an additional retained port.

There are exactly 10*10*55=5,500 such operational classes: the outer
two digits remain individually identified, and the middle two form an
unordered pair with repetition. The executable checks all 10,000
source words and all ten cyclic continuations, including leading zeros.
It finds exactly 5,500 distinct W states and future signatures.

There is a proof of minimality for this receiver. The ten future values
y_k=F(S^k n), with y10=y0, give
W_(9-k)=(121-y_(k+1)+y_k)/10. Hence their values recover every W_j.
Conversely W generates all these observations and all S/M continuations.
So two sources are indistinguishable under this operation family
exactly when their W records agree. This is a complete operational
quotient for the stated finite system, not a quotient for arbitrary
arithmetic operations on the coefficient.

## 5. A bounded repeated handoff

The retained prior residue and modulus recover the current source 5426,
whose W record has no9 initially. The chosen S continuation therefore
has the exact compressed path

    566 -> 687 -> 808 -> 929 -> 1040 -> 161
        -> 182 -> 303 -> 324 -> 445 -> 566.

The source width remains four throughout; step 5's source is 0971.
The path is not ordinary counting. The carry rule and retained column
weights produce its jumps. The ten-step return is the closure of the
declared cyclic digit operation. No theorem turns that finite closure
into the BSD leading-coefficient identity.

This implements a meaningful compression -> retained carry -> handoff
loop. The unresolved BSD adapter is to derive which such operation,
if any, is forced by the elliptic curve's analytic and arithmetic
objects, and which observation marks successful completion. The user
has not selected S as the unique intended operation, so 687 is the
next value under this candidate, not an unqualified answer to the next
number question.

Replay the extension independently:

```powershell
python -I -B work/column_handoff.py --output evidence/my_new_handoff.json
```

Use a new output path. `evidence/column_handoff_extended.json` records
the executed census, carry controls, inverse fibers and full source
path. The earlier smaller audit and its hash-matching source snapshot
are preserved separately.
