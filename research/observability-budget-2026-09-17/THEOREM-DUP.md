# Duplicate ports: equal functions, not equal names

Let `X` be finite and `Q:X→D`. A port is a function `p:X→O`, not a
string. A panel `S` is a finite family of such functions. Set
`C_S(x)=(p(x))_{p∈S}`. The joint kernel is
`ker C_S={(x,y):C_S(x)=C_S(y)}`. Then `Q` is constant on the `C_S`
fibers if and only if `ker C_S ⊆ ker Q`.

Let `p':X→O`. If `p'=p` as functions for some `p` already in `S`, then
`C_{S∪{p'}}(x)=(C_S(x),p(x))`, so `ker C_{S∪{p'}}=ker C_S`. Hence `Q`
is constant on the new fibers if and only if it was constant on the old.

Names are not functions. The hostile case is a second function `g≠p`
printed with the same **codename**. Then `ker C_{S∪{g}}` may strictly
refine `ker C_S`. On machine M, `A=A2` as functions, so `{A,A2}` keeps
ghost `{0,1}`; `B≠A` and `{A,B}` kills that ghost.

This is factorization (Manifesto II.2). Not Lean. Not AD-R3.
Eighty L-trials: repairs **NONE**. Same-codename ≠ same function.
