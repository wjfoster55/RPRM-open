# Exact Fourier norm of the oriented elementary plaquette

Date: 2026-09-12. Independent written proof and exact finite-matrix arithmetic audit.

**Result: PASS.** In the coefficient convention of `accepted/DIRECT_COVER_ATTEMPT.md`, DC2, the actual positive-coordinate elementary SU(2) plaquette satisfies

```text
a(U1,U2,U3,U4) = (1/2)Tr(U1 U2 U3^(-1) U4^(-1)),
||a||_A = 4.                                             (SN1)
```

The earlier DC6 bound ||a||_A<=8 is valid but not sharp. It arose from summing the absolute norms of sixteen monomials without retaining their coefficient-matrix structure. This note changes no accepted proof file and makes no literature-priority claim.

## Carrier and coefficient convention

The four link occurrences are distinct, each ranges independently over SU(2), and the displayed word is the elementary plaquette word when links are stored in positive coordinate orientation. The full Fourier carrier remains all Peter-Weyl representations of the complete link product. The source function itself lies exactly in one multi-spin block, with spin 1/2 on these four links and zero on all other links. Working with its exact 16-dimensional coefficient matrix is therefore not a truncation of the full Hamiltonian or an assumption excluding high-spin states.

Use the equivalent irreducible product representation

```text
pi(U) = U1 tensor U2 tensor conjugate(U3) tensor conjugate(U4)
```

on C2 tensor C2 tensor C2 tensor C2, with basis vectors |i1,i2,i3,i4>. The accepted convention is a(U)=Tr(B pi(U)), with no further dimension factor outside B. Let every matrix index below run over {0,1}.

The inverse entries obey

```text
(U3^(-1))_(c,d) = conjugate(U3)_(d,c),
(U4^(-1))_(d,a) = conjugate(U4)_(a,d).
```

Thus the trace expands as

```text
a(U) = (1/2) sum_(a,b,c,d)
  (U1)_(a,b) (U2)_(b,c) conjugate(U3)_(d,c) conjugate(U4)_(a,d).
```

The product-representation row is (a,b,d,a) and its column is (b,c,c,d). Since Tr(B pi)=sum_(x,y) B_(x,y) pi_(y,x), the coefficient matrix is exactly

```text
B = (1/2) sum_(a,b,c,d) |b,c,c,d><a,b,d,a|.               (SN2)
```

This verifies the row-column reversal in the trace convention. In particular, neither inverse link may be treated as an untransposed conjugate entry.

## Exact singular values

For each pair (b,d), define

```text
v_(b,d) = sum_c |b,c,c,d>,
w_(b,d) = sum_a |a,b,d,a>.
```

The two families separately satisfy

```text
<v_(b,d),v_(b',d')> = 2 delta_(b,b') delta_(d,d'),
<w_(b,d),w_(b',d')> = 2 delta_(b,b') delta_(d,d').
```

The first identity follows by the first and fourth basis entries; the second follows by the second and third entries. Each sum has two orthogonal unit summands. No orthogonality between the v-family and the w-family is required.

Set vhat=v/sqrt(2) and what=w/sqrt(2). Equation SN2 becomes

```text
B = (1/2)sum_(b,d)|v_(b,d)><w_(b,d)|
  = sum_(b,d)|vhat_(b,d)><what_(b,d)|.
```

Hence B is an isometry from the four-dimensional span of the what vectors onto the four-dimensional span of the vhat vectors and is zero on the orthogonal complement of its initial space. Therefore

```text
B*B = sum_(b,d)|what_(b,d)><what_(b,d)|,
BB* = sum_(b,d)|vhat_(b,d)><vhat_(b,d)|,
singular values of B = 1,1,1,1,0,...,0,
||B||_1 = 4.                                            (SN3)
```

Because pi is one irreducible representation of the four-factor product group, its coefficient matrix is unique and SN3 is the exact Fourier-algebra norm, not merely the norm of a nonminimal decomposition.

## Returning to the declared fundamental representation

Let

```text
epsilon = [[0,1],[-1,0]].
```

This matrix is unitary and every U in SU(2) satisfies conjugate(U)=epsilon U epsilon^(-1). With C=I tensor I tensor epsilon tensor epsilon,

```text
pi(U) = C [U1 tensor U2 tensor U3 tensor U4] C^(-1),
Tr(B pi(U)) = Tr([C^(-1)BC] [U1 tensor U2 tensor U3 tensor U4]).
```

Unitary conjugation preserves singular values and trace norm. The coefficient in the DC2 choice of fundamental representatives therefore also has norm 4. There is no extra factor 16: the dimension factor from the usual normalized Fourier transform is already absorbed in the coefficient B of the displayed trace convention.

As a consistency check, ||B||_HS^2=4 and the product irreducible dimension is 16, so Peter-Weyl orthogonality gives integral |a|^2 dmu=4/16=1/4, agreeing with the normalized Haar plaquette moment.

## The orientation distinction is material

For the different function

```text
a_plus(U) = (1/2)Tr(U1 U2 U3 U4),
```

the analogous coefficient matrix is

```text
B_plus = (1/2)sum_(a,b,c,d)|b,c,d,a><a,b,c,d|.
```

Twice this matrix is a cyclic permutation of all sixteen basis vectors. Its sixteen singular values are 1/2, so ||a_plus||_A=8. Inverting only selected coordinates of a nonabelian product group need not preserve the Fourier-algebra norm; it is not in general a group automorphism or the global inversion map. In coefficient form, such changes can involve partial transpose. Consequently the all-positive norm cannot be substituted for the actual oriented norm by invoking orientation invariance.

This does not change the positive-coordinate graph contract. Its elementary loop has precisely two forward and two reverse links in the displayed order, up to cyclic relabeling and reversal of the traced word, and SN1 applies to that actual source.

## Consequence for the anchored source estimate

Every elementary plaquette has kinetic eigenvalue 6. The inverse eigenvalue cancels the energy weight in the anchored norm, exactly as in DC7. Therefore

```text
||T^(-1)sum_p a_p||_* <= 4 max_e #{p:e in p} <= 4m,
m=2(d-1).                                               (SN4)
```

For the stated distinct elementary plaquettes, their four-link supports are distinct. They consequently occupy different multi-spin blocks, making the first inequality an equality when there is at least one plaquette. The upper bound SN4 is all that subsequent estimates need.

Using SN4 with the unchanged DC5 bilinear constant 8/3 would already double the old sufficient interval to r<=1/(24m) at radius R=1/4. Any further improvement of the bilinear constant is a separate proof dependency. This source audit does not assume that improvement.

## Exact small-matrix audit

The following standard-library calculation was executed with integer matrix products and rational monomial coefficients. It enumerates the complete fixed 16-dimensional source block. It does not sample configurations, simulate a vacuum, or run an old checker. M=2B has integer entries; N=M^T M obeys N^2=4N and Tr N=16. Therefore B*B=N/4 is an orthogonal projection of rank 4, giving SN3 without floating-point singular-value calculations.

```python
from itertools import product
from fractions import Fraction

basis = list(product(range(2), repeat=4))
idx = {v: i for i, v in enumerate(basis)}
n = len(basis)
M = [[0] * n for _ in range(n)]
direct = {}
for a, b, c, d in product(range(2), repeat=4):
    M[idx[b, c, c, d]][idx[a, b, d, a]] += 1
    key = ((a, b), (b, c), (d, c), (a, d))
    direct[key] = direct.get(key, Fraction(0)) + Fraction(1, 2)

encoded = {}
for row in range(n):
    for col in range(n):
        if M[row][col]:
            key = tuple((basis[col][k], basis[row][k]) for k in range(4))
            encoded[key] = encoded.get(key, Fraction(0)) + Fraction(M[row][col], 2)

def transpose(A):
    return list(map(list, zip(*A)))

def mul(A, B):
    return [[sum(a * b for a, b in zip(row, col))
             for col in zip(*B)] for row in A]

def scale(k, A):
    return [[k * v for v in row] for row in A]

N = mul(transpose(M), M)
assert encoded == direct
assert mul(N, N) == scale(4, N)
assert sum(N[i][i] for i in range(n)) == 16
assert mul(M, N) == scale(4, M)

P = [[0] * n for _ in range(n)]
for a, b, c, d in product(range(2), repeat=4):
    P[idx[b, c, d, a]][idx[a, b, c, d]] = 1
identity = [[int(i == j) for j in range(n)] for i in range(n)]
assert mul(transpose(P), P) == identity
```

Observed result: all assertions passed. The exact monomial dictionaries agree; the actual coefficient has trace norm 4; the all-positive comparison has trace norm 8; the Haar second-moment check is 1/4. The written representation argument supplies the general SU(2) identity; the finite audit verifies its explicit coefficient matrix and rational arithmetic.

Only this new note was written for the source-norm audit. No accepted old file, old test, simulation, package installation, git state, or other research lane was changed.

## Requested follow-up: independent contracted-estimate compatibility audit

After completing the source calculation, the independent note `SIGNED_AND_CONTRACTED_AUDIT.md` was read in full. Its replacement bilinear estimate

```text
||B(u,v)||_* <= (16/9)||u||_*||v||_*
```

passes independent written review. The following are the load-bearing checks.

1. For a pair of spins j,l, the contracted anti-Hermitian generators have channel eigenvalues 2[j(j+1)+l(l+1)-s(s+1)]. With a=min(j,l), b=max(j,l), their operator norm is 4a(b+1). Dividing by lambda_j lambda_l gives 1/[b(a+1)]. Except for j=l=1/2, this is at most 2/3 over every positive half-integral pair. Zero input spin gives zero derivative.
2. The tensor product of two SU(2) irreducibles is multiplicity free, and this remains true for irreducibles of the product of the link groups. Thus the contracted generator is scalar on every reached product-group output block. Moving it from the left to the right of the input coefficient, as derivative conventions may require, does not change the projected scalar block.
3. For rank-one inputs, the two coefficient vectors are x tensor z and y tensor w. Weighted Cauchy-Schwarz over the output projections bounds the sum of projected trace norms by the geometric mean of their expectations of |Omega_i|. In the fundamental pair, Omega_i=I-2F and |Omega_i|=2I-F, where F swaps the two link factors.
4. Entanglement among links within x or z is allowed. Because x tensor z is a product between the two input sides, its reduction at the differentiated link is rho tensor sigma. Consequently its expectation of |Omega_i| is 2-Tr(rho sigma)<=2. The same is true on the second coefficient vector. Separate singular-value expansions of arbitrary complex B_J and C_K then prove the local constant 2 without imposing positivity or separability on those coefficient matrices themselves.
5. This constant equals (8/9)lambda_(1/2)^2. The nonfundamental bound 2/3 is smaller than 8/9. The two safe input-anchor contributions therefore sum to 16/9 by the original anchored counting, with no graph-size factor. Support loss and removal of the scalar block only remove terms from the positive norm bound.

The all-spin channel formula is consistent with the total-Casimir identity and spin range in the cited [angular-momentum notes, section 15.2](https://etneil.github.io/grad_qm_lec_notes/addition_J.html#addition-of-angular-momentum); its generator factors were independently checked above. The local hostile example u(U)=U_11, v(U)=U_22 has contracted function 2-uv, Fourier norm 2, and loses its scalar coefficient 3/2 under Q, as that note states. It is not an optimality witness for the complete anchored inverse operator.

This refinement and SN4 use exactly the same DC2 norm. The unitary changes relating dual fundamental representatives to the declared representatives preserve trace norms and conjugate the generator matrices consistently. Arbitrary source coefficient matrices are admitted by the contracted proof. The two improvements are therefore compatible.

Writing t=|r|, their combined scalar self-map and Lipschitz bounds are

```text
||F_r(u)||_* <= 4mt+(8/9)R^2,
Lip(F_r on radius R) <= (16/9)R.
```

At R=1/4, the nonlinear contribution is 1/18 and the Lipschitz constant is 4/9. The closed ball is invariant whenever 4mt<=7/36, that is t<=7/(144m). The inherited Hessian and Bochner argument then gives gap>=1/2, with the same physical-subspace qualification as the accepted proof.

More generally the smaller scalar root is

```text
R(t)=(9/16)[1-sqrt(1-128mt/9)],
0<=t<9/(128m).
```

The inherited curvature lower bound yields gap>=1-2R(t)>0 precisely on t<5/(72m). At t=5/(72m), R=1/2 while the contraction factor is still 8/9<1. The fixed point is therefore constructed there, but this particular norm-based curvature lower bound is zero. The positive-curvature certificate ends before the contraction interval does. Neither the actual curvature nor the actual spectral gap is proved to vanish. These are sufficient estimates with no optimality or novelty claim.

No file belonging to the contracted-estimate author was edited in this follow-up audit.
