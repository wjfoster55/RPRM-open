# The generator, zero/one labels, and the carry/swap trace

The generator question is now solved: every rational point on the original
curve is uniquely **mP+T**, where m is an integer, P=(-4,6), and
T is one of O,(0,0),(5,0),(-5,0). Thus m=0 labels the zero free step and
m=1 labels one generating step. These integer labels are not the affine
coordinates of the point. Coordinate size and divisibility in this group
are different readouts.

There is no preferred numerically smallest pair across all coordinate systems.
Even on the original equation, P+(5,0)=(-5/9,-100/27) is also a primitive
generator modulo torsion and has a smaller absolute x-coordinate than P.
The new proof establishes that P is one full free step, rather than three,
five, or another odd number of smaller free steps. It does not canonize its
visible coordinate numerals as the base of every representation.

## Exact coordinate changes matching two suggested labels

Your proposed (-1,0) can be the coordinates of this same generator. Set

    X=x+3,  Y=y-6;    inverse: x=X-3, y=Y+6.

Substitution transports the whole equation to

    Y²+12Y = X³-9X²+2X+12.

Now P is **(-1,0)**. Its group inverse is **(-1,-12)**, and the identity
is still the projective point at infinity. The zero Y-coordinate therefore
does not make it a two-torsion point: the inversion rule has changed from
(x,y)↦(x,-y) to (X,Y)↦(X,-Y-12).

Likewise, the reversible map

    X=x+4,  Y=y-5;    inverse: x=X-4, y=Y+5

gives

    Y²+10Y = X³-12X²+23X+11,

with **P=(0,1)**. This is an ordered pair. If the slash notation 0/1 means
the arithmetic quotient zero instead, that scalar has a different type.
In these new coordinates (0,1) is the generator, while O is still the group
identity. Both maps are translations of the same elliptic curve's coordinates;
they preserve its rational group, primitivity, differential, and BSD invariants.
They do not realize the proposed carry/swap recurrence merely by matching an
endpoint.

For a general translation (X,Y)=(x+s,y+t), expansion gives the ordered
Weierstrass coefficients

    [a1,a2,a3,a4,a6]=[0,-3s,-2t,3s²-25,-s³+25s-t²].

This identity proves the map on every rational point and its inverse, with O
fixed. The checker also implements the chord/tangent law directly for the
translated equations and verifies commuting addition on 49 pairs for each
map, including O, torsion, P,-P, and 2P. This is more than copying the old
addition output under a new label: the new equation's group formula is tested.

The earlier scaling (u,v)=(x/5,y/25) is another different coordinate system,
with equation **5v²=u³-u**. There P=(-4/5,6/25), and (-1,0) is the image
of (-5,0), a point of order two. The same written pair (-1,0) therefore
has different meanings on the two explicitly different equations. No
coordinate pair supplies its own carrier or group law.

## Preserve the stated carry/swap operation without inventing it

The latest supplied trace is retained as ordered slots:

    (0,1) → (2,1) → (3,4) → (6,4).

Its three observed edges define an injective **partial** map. They have the
exact reverse

    (6,4) → (3,4) → (2,1) → (0,1).

The accompanying base symbol `--0` and the direction-dependent sign language
are retained as supplied context. No arithmetic double negation, signed zero,
orientation state, or identification with O is silently assigned to that symbol.

Two particularly simple fully stated candidate rules were tested:
increment the first slot by one and then swap, giving (a,b)↦(b,a+1);
or swap and then increment the first slot, giving (a,b)↦(b+1,a).
Neither reproduces the observed trace. This rejects those two literal
candidates, not your broader operation with retained carry, phase and sign.
Their mismatches are in the executable receipt.

Reducing slot pairs to scalar fractions would itself be a lossy operation:
(6,4) and (3,2) both have rational value 3/2 but are different ordered states.
If carry, phase or swapping depends on the slots, that quotient alone may
forget needed information. The code retains this concrete collision.

The full carry/phase/sign recurrence remains **OPEN**: the trace does not yet
specify an output for every admitted input, which slot receives a carry,
what the reversal does to the sign state, or how the resulting states map to
E(Q). The three observed inverse edges are exact; an unbounded universal law
does not follow from them. A claimed bridge to elliptic-curve division needs
an explicit map and its transported group operation. A reversible group map
preserves primitive generators and element orders.

Fresh code and evidence: `work/coordinate_check.py` and
`evidence/coordinates.json`. The literal-point and partial-abscissa checks
there concern only their named equations; an off-curve result on the old
equation is not a refutation of a coordinate change to a new equation.
