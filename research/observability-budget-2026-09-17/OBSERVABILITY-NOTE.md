# Finite-budget observability, in one sitting

17 September 2026. Standalone note for tomorrow. Not BSD. Not AD-R3. Not
a new control-theoretic principle.

Branch `research/observability-budget-2026-09-17` in worktree
`C:\github\RPRM-open-observability-budget`. Replay:

```powershell
python -I -B research/observability-budget-2026-09-17/verify_ob.py
```

Nulls were frozen before each enumerator. Evidence grade is written
kernel arguments plus a complete finite check on three named machines.
Lean was not run. The independent-math Rank 2 prompt was: given a finite
machine, a budget `k`, and a question `Q`, which `k` observation ports
make `Q` constant on the representation fiber.

---

## 1. What is being asked

A **port** is a function `p:X→O`, not a string. A **panel** `S` is a
finite family of ports. The representation is the joint readout
`C_S(x)=(p(x))_{p∈S}`. Its **joint kernel** is
`ker C_S={(x,y):C_S(x)=C_S(y)}`. A question `Q:X→D` is constant on the
`C_S` fibers if and only if `ker C_S ⊆ ker Q`. That is Manifesto II.2 /
factorization. `NONE`, `ONE`, and `MANY` classify a complete fiber of
panels or a complete yes/no, never an unfinished search.

Two other budgets sit next to `k = |S|`. **Time** records `C_S` after
words of an admitted action alphabet. An **intervention** changes that
alphabet (on the four-state layer, `reveal` is not `tick`). These are
different repairs. A new occurrence of an already-read function is not a
repair at all.

This note does not place sensors on a plant, estimate noise, or replay
the linear continuation subspace AD-R3. It records what the finite
ports already force.

---

## 2. Three machines

**L — four-state layer** (`docs/relational-layer.md`). States
`(r,h)∈{0,1}²`, `Q=h`. Ports: `H=h`, `R=r`, `R2=r` (distinct
occurrence, equal function), `X=r XOR h`, `Z=0`. Total `tick` flips
both bits. Optional total `reveal(r,h)=(h,h)` is a different alphabet.

**M — lookalike.** States `{0,1,2}`, `Q=[s=1]`. Ports `A=A2=(0,0,1)` as
functions; `B=(0,1,1)`. Identity is the only action used for time.

**N — hostile shift `{Y}`.** States `(a,b,c)∈{0,1}³`, `Q=c`, port
`Y=a`, `shift(a,b,c)=(b,c,0)`.

---

## 3. Sensor budget on L

| Cut | Result |
|---|---|
| Budget 1 | **ONE(`{H}`)** |
| `{R,R2,Z}` (more sensors) | **NONE** — both `r`-fibers still split `h` |
| Extra `tick`-time of `{R}` | **NONE** — traces `0,1,0,1` and `1,0,1,0` |
| Budget 2 | **MANY(6)**: every pair with `H`, plus `{R,X}` and `{R2,X}` |
| `{R}` plus `reveal` | **ONE(yes)** — same port, new alphabet |

The historical guess “more sensors help” dies on copies of `R` plus a
constant. `{R,X}` works because `h = r XOR (r XOR h)` on every source,
not because a second occurrence of `R` was added. `reveal` is not extra
time of `tick`.

---

## 4. Duplicates are equal functions

Let `p'` be a port. If `p'=p` as functions for some `p` already in `S`,
then `C_{S∪{p'}}(x)=(C_S(x),p(x))`, so `ker C_{S∪{p'}}=ker C_S`.
Therefore `Q` is constant on the new fibers if and only if it was
constant on the old. Names are not functions.

Eighty nonempty-L trials that adjoin a fresh value-copy: repairs
**NONE**. Machine M: `{A}` and `{A,A2}` keep ghost `{0,1}`; `{A,B}`
kills it because `B≠A`. A second function printed with the same
**codename** is the hostile, not a duplicate.

This is factorization again. It is not a new observability law.

---

## 5. Extra time versus an independent port

`S` **descends** under a total action `T` when `C_S ∘ T` is a function
of `C_S`. Then `C_S(T_w x)` is a function of `C_S(x)` for every finite
word, so `ker C_S = ker(trace_b)` at every horizon. Extra time cannot
refine the panel and cannot make a previously non-constant `Q` constant.

A port `q` is **independent** of `S` when `q` is not a function of
`C_S`. Then `ker C_{S∪{q}}` may strictly refine `ker C_S`.

On L every one of the 31 nonempty panels descends under `tick`. Horizon
3 never refines. `{R,X}` is the independent-port repair. On N, `Y∘shift`
reads `b`, which is not a function of `a`, so `{Y}` does not descend,
and horizon 2 of `Y` makes `Q=c` constant.

`reveal` on L is a second letter that does **not** descend for `{R}`:
`R∘reveal=h` is independent of `r`. Changing the alphabet is not extra
time of the old one.

---

## 6. When extra time refines Q

That last paragraph already says when time *cannot* help. When it *can*:

Extra time **weakly refines Q** at horizon `b` iff some word of length
at most `b` splits a present Q-ghost: same `C_S`, different `Q`, later
different `C_S`. It **repairs Q** when the static kernel misses `ker Q`
and the trace kernel sits inside `ker Q`.

If `C_S` is a dynamical homomorphism, both are forbidden. Homomorphism
failure is **not** a Q-statement. It may split only Q-constant pairs.

On L, refine-Q under `tick` is **NONE** (31 panels). On M with identity,
**NONE**. Hostile `{Y}`: frozen `N_y_delay` said horizon 1 misses every
Q-ghost. The census is **ONE(`N_y_immediate`)**. Pair `(000),(001)`
still reads `Y=0,0` after one shift and `0,1` after two. Pair
`(000),(011)` is another Q-ghost and already splits at horizon 1. Repair
of all of `Q=c` still needs horizon 2.

So the dynamical observation kernel of `{Y}` is not a congruence of the
shift, and it is not enough to say that. The Q-relevant fact is which
ghost a later reading hits, and at which length. That is the last typed
claim of this branch. Stop padding.

---

## 7. What this is not

It is not Kalman rank, Petreczky switched-system observability, or
AD-R3 row-space closure `W_{b+1}=W_b+Σ A_a^*W_b`. Those remain the
linear ancestry named in the Rank 2 reading. It is not a sensor-placement
algorithm for an unstated plant. It is not a proof that the hidden bit
`h` exists because `R` was seen — the two-state `r`-only control in the
relational-layer note still matches every `tick` trace of `R`. It is not
BSD, fluid, Hamming, or n=4 obstruction padding.

Equal values are not equal occurrences: `R` and `R2` stay distinct names
with one function. A hash of this note binds bytes; it does not prove
the kernels.

---

## 8. Tomorrow

Reuse the three theorems at their stated carriers. Do not open another
five-port subset census. If the next cut is linear, start from AD-R3
with an already-retained row space, a finite budget, and one hostile
nonlinear or partial-enabledness case. If the next cut stays discrete,
the live seam is **enabledness**: a port that is not total, or an action
that is not, can split states that every value-copy and every descending
trace leaves joined. That is a new contract, not a longer word on `{Y}`.

Frozen-null commits: OB-k `e758dd3`, duplication `f535cd0`, time
`784f27a`, iff `4aa1c13`. Desktop one-liner:
`C:\Users\bkbee\Desktop\OB-k-2026-09-17.txt`.
