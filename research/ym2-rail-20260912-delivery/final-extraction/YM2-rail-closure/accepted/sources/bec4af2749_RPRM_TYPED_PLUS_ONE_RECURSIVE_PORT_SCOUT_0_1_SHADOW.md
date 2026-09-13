# RPRM typed plus-one recursive-port Scout 0.1

Status: `FULL_NUMEROLOGY_DRUID_LANE__EXACT_HITS_TYPED__NO_UNIVERSAL_CLAIM`

## Human question

Can the recurring `one -> two -> four -> eight`, “plus one,” center/apex,
rolling-window, and “same outlet feeds the next inlet” intuitions be placed in
one room without pretending they are one operation?

Yes, if the room is a typed recursive port and each constructor keeps its own
law.  The common shape is:

```text
A_n --EXTEND[adapter receipt]--> A_(n+1)

output schema(A_n) = input schema expected by EXTEND
prior emitted root = successor's recorded input root
```

The same outlet is the envelope, not the payload operation.  Product with an
interval, coning with one apex, suspension by two poles, adjoining a vector
generator, and appending a homogeneous coordinate are different adapters.

## Three exact face-polynomial ladders

Let the coefficient meaning travel with the polynomial.

### Simplex: cone / join one apex

For the full `n`-simplex complex, including the empty face, use

```text
S_n(t) = (1+t)^(n+1).
```

The coefficient of `t^k` counts faces with exactly `k` vertices, hence
geometric dimension `k-1`; the empty face is `k=0`.  Coning with a supplied
new apex partitions faces into those that omit it and those that contain it:

```text
S_n = (1+t) S_(n-1).
```

| simplex dimension n | typed coefficients by vertex-cardinality k |
|---:|---|
| 0 | `1, 1` |
| 1 | `1, 2, 1` |
| 2 | `1, 3, 3, 1` |
| 3 | `1, 4, 6, 4, 1` |
| 4 | `1, 5, 10, 10, 5, 1` |

### Cube: product with an interval

For the full face set of the `n`-cube use

```text
C_n(t) = (2+t)^n.
```

Here the coefficient of `t^k` counts geometric `k`-faces.  Product with a
supplied interval makes two endpoint copies of every old face and one swept
face of dimension one higher:

```text
C_n = (2+t) C_(n-1).
```

| cube dimension n | typed coefficients by geometric dimension k |
|---:|---|
| 0 | `1` |
| 1 | `2, 1` |
| 2 | `4, 4, 1` |
| 3 | `8, 12, 6, 1` |
| 4 | `16, 32, 24, 8, 1` |

### Cross-polytope boundary: suspension / join two poles

For the boundary face complex of the `n`-cross-polytope, including the empty
face but excluding the polytope interior, use

```text
X_n(t) = (1+2t)^n.
```

The coefficient of `t^k` counts boundary faces with `k` vertices, geometric
dimension `k-1`.  Suspension joins the old complex with a supplied `S0` of two
antipodal poles; a face may use neither pole or exactly one of the two:

```text
X_n = (1+2t) X_(n-1).
```

| ambient cross-polytope dimension n | typed boundary coefficients by vertex-cardinality k |
|---:|---|
| 0 | `1` |
| 1 | `1, 2` |
| 2 | `1, 4, 4` |
| 3 | `1, 6, 12, 8` |
| 4 | `1, 8, 24, 32, 16` |

The displayed polynomials look like siblings because each recurrence is
multiplication by a degree-one factor.  They are not interchangeable: their
coefficient indices and adapters have different types.

## Structural depth versus state count

Appending one coordinate raises structural depth by exactly one.  For words
over a supplied alphabet of size `b`, it simultaneously multiplies state
count:

```text
depth:       n -> n+1
state count: b^n -> b^(n+1) = b * b^n
```

For `b=2`, the vertex counts are `1,2,4,8,16`.  This is the exact cube-vertex
and binary-word pattern.  It is not a proof that dimension “is” exponential;
dimension increased additively while the number of coordinate assignments
increased multiplicatively.

Nearby exact sequences remain differently typed:

| sequence | exact owner |
|---|---|
| `1,2,4,8,16` | binary words / cube vertices `2^n` |
| `0,1,3,7,15` | non-anchor cube vertices or support excluding one known corner `2^n-1` |
| `1,2,3,4,5` | affine-basis or homogeneous-coordinate count `n+1` |
| `0,2,4,6,8` | cross-polytope vertex count `2n` for `n>=1` |
| `1,2,4,8,16` in the cross family | facet count `2^n`, not vertex count |

## The strongest exact plus-one translator: homogeneous coordinates

Homogeneous coordinates turn an affine operation into a linear one while
preserving a point/vector type bit:

```text
point p  -> (p,1)
vector v -> (v,0)

affine p -> A p + b

               [ A  b ]
homogeneous M =[      ]
               [ 0  1 ]
```

Then exactly

```text
M (p,1) = (A p+b, 1)
M (v,0) = (A v,   0).
```

Rational swatch in dimension two:

```text
A = [[ 2, 1],       b = [ 5,-2]
     [-1, 3]]

p=(1,4)  -> (p,1)=(1,4,1)  -> M(p,1)=(11, 9,1)
v=(2,-1) -> (v,0)=(2,-1,0) -> M(v,0)=( 3,-5,0)
```

This is related to—but is not the same thing as—either:

- an `n`-simplex having `n+1` vertices; or
- affine scalar functions having basis `{1,x1,...,xn}` and dimension `n+1`.

All three are honest plus-one appearances.  Their operations and carriers are
different, so only the typed port envelope is shared.

## Affine `n+1` baseline

On an `n`-dimensional affine coordinate carrier, scalar affine functions have
the supplied basis

```text
{1, x1, ..., xn}.
```

Evaluation at the `n+1` points `{0,e1,...,en}` produces a full-rank square
matrix, proving this registered basis has size `n+1`.  This is a vector-space
dimension statement, not a face count and not a state count.

## Rolling triple and boundary debt

A rolling triple has a literal handoff law:

```text
ROLL((past,present,future), next) = (present,future,next).
```

The old `future` becomes the new `present`, so two slots hand off directly.
But the shift also creates a successor obligation.  If `next` has not been
supplied, the correct output is `(present,future,MISSING)`, not an invented
number.  The lawful dispositions are:

| disposition | exact requirement | example |
|---|---|---|
| `WRAP_PERIODIC` | a period receipt identifies `next` with the wrapped value | `(a,b,c)->(b,c,a)` only under declared period 3 |
| `GENERATE_OR_MEASURE_SUCCESSOR` | a typed generator or measurement action supplies `next` | Fibonacci law `(1,2,3)->(2,3,5)`; a measurement may instead supply an observed value |
| `PROMOTE_CARRY` | a base/value law returns a low-rung digit plus a nonzero carry residual for the next rung | in base 10, supplied raw successor `10` emits digit `0` and carry `1` |
| `MISSING_FUTURE` | no wrap, generator, measurement, or carry law is present | `(p,q,r)->(q,r,MISSING)` |

This is the temporal form of the same zero rule: an absent future is not the
numeric future `0`.  `PROMOTE_CARRY` does not erase debt; it moves a typed part
of the result to the higher-rung receiver.

## Shared-port contract candidate

Every recursive artifact may use one outer envelope:

```text
recursive_port.v1 = {
  family_type,
  depth,
  carrier_type,
  coefficient_semantics,
  emitted_root,
  prior_input_root,
  constructor_receipt,
  verifier_receipt,
  unresolved_residuals
}
```

The successor must consume `emitted_root` directly.  The adapter then proves
its own law:

| adapter | supplied operation law |
|---|---|
| cube | `X -> X x I` |
| simplex | `K -> K * {apex}` |
| cross boundary | `K -> K * S0` |
| vector space | `V -> V direct-sum span{e_new}` |
| homogeneous affine | append point/vector type coordinate and lift `Ap+b` to `M` |
| base-b words | append one alphabet symbol |
| rolling time | shift two slots and discharge successor debt by one declared disposition |

Passing the same JSON shape is not enough.  A manual adapter that rebuilds an
equivalent object, changes coefficient meaning, hides a carry, or treats
`MISSING` as zero fails the port contract.

## What is pattern and what is decoration

The live mechanism is **typed recursive extension with direct handoff**.  The
degree-one polynomial factors are receipts for three real but distinct
extension functors.  Homogeneous coordinates are a real plus-one translation
machine.  Binary powers are real state counts.  Rolling time really does reuse
two slots and owe one successor.

The decorative move would be to erase the types and announce that every
appearance of 1, 2, 4, 8, `n+1`, apex, center, or carry is the same law.  The
Scout keeps the coincidences visible, then asks each one to carry an operation,
a unit/base case, and a receiver.  Pattern matches without those receipts stay
numerology, not evidence.

## Smallest executable next step

Freeze one port fixture through depths 0..4 for the three face-polynomial
families plus binary words.  Require direct prior-root handoff, exact recurrence
coefficients, typed coefficient semantics, decompilation of the inherited
part, and rejection of cross-family adapter swaps.  Add the 2D homogeneous
swatch and the four rolling-window dispositions as separate blocks.  Score
only these finite identities; make no universal generator, physics, quantum,
or open-problem claim.
