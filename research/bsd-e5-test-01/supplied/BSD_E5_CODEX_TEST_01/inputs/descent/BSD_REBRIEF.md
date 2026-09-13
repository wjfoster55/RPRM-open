# BSD rebrief — 12 September 2026 — E5 descent and lifting

## Active question
Resume the original Selmer-level map question: distinguish genuine rational
classes from local-compatible obstruction classes, retaining enough information
to answer a stronger quotient question. Paper/other lanes offscope; review005 and
the AD 14/16 tie remain closed. Supplied BSD_CHAT_UPDATE and CURRENT_STATE were read.
Accepted C1/AD1 provide explicit scope/reuse discipline, not a new arithmetic theorem
or measured general advantage.

## New worked outcome in this chat
For E/Q: y^2=x^3-25x, with P=(-4,6) and K=E(Q)[2]={O,(0,0),(5,0),(-5,0)}:

1. The full Kummer signature ([x],[x-5],[x+5]), with standard exceptional-point
   conventions, has kernel 2E(Q). Local conditions restrict Sel_2 to 32 supported
   real-admissible triples. Eight signatures are realized by T and P+T, T in K.
2. Those eight form H. The other three cosets have representatives (2,2,1),
   (1,2,2), (2,1,2), excluded by primitive congruences modulo 4/8. Hence
   Sel_2=E(Q)/2E(Q), order 8; rank E(Q)=1; Sha(E/Q)[2]=0.
3. No 2-torsion in Sha implies Sha[2^n]=0 for every n. The three nonzero points
   in K are not doubles, so there is no rational 4-torsion. For every n>=1,
   (m mod 2^n,T) -> [mP+T] gives Sel_{2^n} ~= Z/2^n x (Z/2)^2. The transition
   reduces m and retains T. Each class has exactly two refinements one level up.
4. A finite algorithm extracts these coordinates from any supplied rational R
   by its signature and exact rational halving. It also retains Rn with
   R=mP+T+2^n Rn, permitting exact reconstruction rather than mistaking a quotient
   representative for the original point.
5. Q=2P=(1681/144,-62279/1728) has delta(Q)=delta(O)=(1,1,1), yet Q is not in 4G.
   At level 4 its coordinate is (2,O), while O is (0,O). A coarse class cannot
   determine the original source's finer class.

## Evidence and limits
Classical arithmetic derived here, no priority claim. Standard inputs: Milne's
Kummer map; Mordell–Weil; Stoll's Selmer exact sequence; Bekker–Zarhin halving.
Exact code enumerated the complete mod-2/4/8 filters by two routes, checked the
rational witnesses/cosets, and verified 256 decoder/readback cases. Code and
receipt are supplied. General conclusions use the written proof, not extrapolation.

No L-series, analytic rank, odd-primary Sha, total Sha, odd-index saturation,
proof of P as an integral generator, general Selmer solver, or new BSD theorem.
The all-level quotient descriptions are proved, not covering equations enumerated
at infinitely many levels. No old audit or agent dispatch occurred.

## Remaining arithmetic frontier
For a curve with extra Sel_2 classes, the disappearance of 2-primary obstruction
must not be assumed. Resume the original image Sel_4 -> Sel_2 problem there;
Cassels' pairing supplies a standard image test. This example completely handles
the favorable zero-2-primary-obstruction case but does not solve that next case.
The global BSD target still needs the arithmetic rank connected to the order of
vanishing of L at 1 (and, for full BSD, the leading coefficient).

Details: E5_DESCENT_NOTE.md. Run: python -B e5_descent.py --output fresh_receipt.json.
