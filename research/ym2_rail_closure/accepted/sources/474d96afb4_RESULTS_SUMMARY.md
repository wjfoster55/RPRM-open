# RPRM Full-Zip Hypercube Ladder 01 — result

## Outcome

**PASS on the frozen finite ladder `Q_0` through `Q_4`.** The recursive runner
and the non-importing direct-word checker produced byte-identical result JSON.
Each rejected all 55 registered mutations.

The primary path emitted compact sorted-key ASCII artifact bytes at every
stage, then reparsed those literal bytes before constructing the next stage.
The checker independently enumerated `{0,1,*}^n`, inferred incidence by
pairwise face comparison, reproduced every canonical byte hash and
domain-separated root, and audited the full input/output receipt chain.

## Exact ladder

| n | f-vector | Total faces | Incidences | Artifact root |
|---:|---|---:|---:|---|
| 0 | `1` | 1 | 0 | `0D5A04EE141659681DFAD7B8A2DDEB3116E3251A01FDA8A54EAC7EADD3BD942F` |
| 1 | `2,1` | 3 | 2 | `B6799C3950EC942502C4B13D4981102345336F74E52A1EBC8FCA551AA0940859` |
| 2 | `4,4,1` | 9 | 12 | `31A13DEF8CFA4EA94C92967736056CE8C33DEF51CE8AA72B9B70A3E0474CE811` |
| 3 | `8,12,6,1` | 27 | 54 | `0C8B826684743D070521D5A87AB9A32B9D8161A50A6B35FF11D20AFCFD1E3E60` |
| 4 | `16,32,24,8,1` | 81 | 216 | `22A079AB2C93CE243CFA1E69A6F81A02917CFFA893C50263144E96DFEA54F43A` |

The vertex counts are `1,2,4,8,16`; non-anchor vertices are `0,1,3,7,15`.
Every face count satisfies `f_k=C(n,k)2^(n-k)`, and every mod-two boundary
squares to zero.

At each nonzero stage the faces split exactly into two inherited copies,
proper swept cells, and one unique new top cell. Both inherited layers
decompile—including their incidence and boundary—to the exact artifact
reparsed from the directly prior bytes.

The requested dimensional facts are explicit:

- `Q_2`: one new square swept from the old edge;
- `Q_3`: four new side squares swept from old edges and six square facets
  total; and
- `Q_4`: six new connecting cubes swept from old squares and eight cubic
  facets total—two inherited plus six swept.

All `n!` coordinate permutations for each `n<=4` preserve faces, incidence,
and the `GF(2)` boundary. Positional alpha-renaming normalizes exactly.

## Receiver reopening

Dropping the final vertex bit creates `1,2,4,8` weak fibers at stages one
through four. Every fiber contains the two new-layer vertices. Restoring the
bit reopens and separates all pairs.

## Separate global parity swatch

The supplied law `XOR(all vertex values)=0` is attached to the unique top cell,
not to cubical incidence or any vertex. One known erasure is recovered from
`1,3,7,15` other values.

Without the law, the result is `UNRESOLVED_NO_RELATION`. Two erased corners
leave the exact two-candidate fiber `[(0,0),(1,1)]`. One unknown-location bit
flip is detected by odd parity but leaves all `2^n` vertices as candidate
locations. No general error-correction claim is made.

## Deferred vacancy scout

`F3_SHEAR_SCOUT`, with `S_t(x,y,z)=(x+t*z,y,z) mod 3`, is only a typed future
interface on a carrier separate from `Q_n`. It was not executed, scored, or
counted as evidence. Static parity erasure and a moving vacancy schedule remain
different operations.

## Claim boundary

This establishes only the registered finite cubical recursion, direct
handoffs, incidence, `GF(2)` boundary, decompilation, symmetry, receiver, and
supplied parity facts. It does not establish a universal Full-Zip compiler,
privileged physical dimensions, a Boolean-scar identity, a general coding
result, a moving-gap law, or progress on an open problem.
