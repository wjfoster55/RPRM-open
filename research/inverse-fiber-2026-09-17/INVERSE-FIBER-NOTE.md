# Inverse fibers, in one sitting

17 September 2026. Standalone note for tomorrow. Not BSD. Not inverse
graphics. Not a physical law.

Branch `research/inverse-fiber-2026-09-17` in worktree
`C:\github\RPRM-open-inverse-fiber`. Replay:

```powershell
python -I -B research/inverse-fiber-2026-09-17/verify_if.py
python -I -B research/inverse-fiber-2026-09-17/verify_joint.py
python -I -B research/inverse-fiber-2026-09-17/verify_view.py
```

IF-k nulls frozen at `3127680`. IF-j at `bd28533`. IF-v at `14c5b8a`.
Evidence grade is exact enumeration of named finite maps, their
marginal products, and two named view menus. Lean was not run.

---

## 1. Complete preimage (IF-k)

The inverse of a specified output is the complete joint fiber.
Representative ≠ fiber. Product of marginals ≠ fiber. Stopped search
is OPEN. Frozen NONE for integer sum 4 died: **ONE((2,2))**.

---

## 2. Joint vs product (IF-j)

XOR=1 is **MANY((0,1),(1,0))**. Its one-bit marginals are both
`{0,1}`. Their product is all four pairs and adds the XOR=0 fiber
`((0,0),(1,1))`. Reconstructing bits independently admits `(1,1)`,
which XOR maps to 0.

C=(0,0) and C=(1,1) each have three `{0,1}` bit-marginals. Each
product is all eight triples and adds six illegal words.

AND=1 **does** equal `{1}×{1}`. Complementary XOR fibers share one
product, so the product does not select the law.

---

## 3. Discriminating view (IF-v)

On XOR=1, exactly `FST` and `SND` from `{FST,SND,AND,OR,EQ,CONST0}`
split the fiber to ONE. AND, OR, EQ, CONST0 are constant. Supplying
`FST=0` leaves **ONE((0,1))**.

On C=(0,0), exactly `X,Y,Z,PARITY,AND3` from
`{X,Y,Z,PARITY,AND3,C0}` split to ONE. Already-supplied `C0` is
constant on both members. Supplying `X=0` leaves **ONE((0,0,0))**.

An extra readout that is constant on the fiber is not a discriminating
view.

---

## 4. Stop

No inverse-graphics grid. No SAT. No min-view search over all Boolean
functions. Rank-7 certified approximate families remain OPEN and are
not this cut.
