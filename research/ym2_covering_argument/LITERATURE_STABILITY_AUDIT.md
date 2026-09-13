# Product-state stability audit for full SU(2) link rotors

Date: 2026-09-12. Evidence: checked primary author text plus a written application proof. No spin truncation, numerical experiment, or formal proof is used.

## Result and source boundary

There is an established product-state stability route to a positive spectral gap, uniform over finite open square or cubic lattice graphs, for sufficiently small plaquette coupling relative to the full-link electric gap. The argument below applies a literature theorem; it is not a new stability theorem or a continuum Yang-Mills result. It subtracts the exact perturbed ground energy and therefore does not require an estimate for a separately computed vacuum-energy remainder.

The best matching primary statement is D. A. Yarotsky, [*Quasi-particles in weak perturbations of non-interacting quantum lattice systems*, arXiv:math-ph/0411042v1](https://arxiv.org/pdf/math-ph/0411042), printed pp. 2-4, Theorem 1 and equations (1)-(5). It admits infinite-dimensional site spaces, unbounded nonnegative on-site Hamiltonians with a unique ground state and gap at least one, and bounded self-adjoint interactions on translates of a fixed finite set S. Equation (3) retains every on-site term and only interactions whose declared support lies in the finite volume. For s = sup_x ||phi_x|| < c1(S), the ground state is unique and equation (5) gives gap >= 1 - c2(S)s, uniformly for every finite volume. Translation invariance is imposed only after Theorem 3, for the subsequent quasiparticle results. Pages 6-9 review the proof; no numerical c1 or c2 is given. The author attributes Theorems 1-3 to earlier work, including his [*Perturbations of ground states in weakly interacting quantum spin systems*, J. Math. Phys. 45, 2134-2152 (2004)](https://doi.org/10.1063/1.1705718), reference [23] on p. 17.

Access qualification: the full original JMP publisher text was not accessible in this audit. Exact theorem numbering and equations above refer to the author's 2004 arXiv restatement, whose complete relevant pages were inspected, including rendered formulas. The published result is thus checked through its author's explicit primary restatement, not through a claim to have inspected the original journal version.

The initially suggested [*Ground states in relatively bounded quantum perturbations of classical lattice systems*, arXiv:math-ph/0412040v1](https://arxiv.org/pdf/math-ph/0412040), is a different paper. Its pp. 2-3 admit infinite-dimensional spaces but explicitly restrict interactions to translation invariance and then use cubic periodic volumes before Theorem 1. A literal citation of that theorem alone does not supply the open-boundary statement. Its [journal record](https://arxiv.org/abs/math-ph/0412040) is Commun. Math. Phys. 261, 799-819 (2006), DOI 10.1007/s00220-005-1456-9. The product theorem above avoids the boundary mismatch.

## Contract

- Carrier: any finite open graph G=(V,E) formed from nearest-neighbor edges of Z^d, d=2 or 3, with each geometric edge stored once in its positive-coordinate orientation. P is any subset of elementary coordinate plaquettes whose four edges are in E. Usual finite open boxes are included.
- Hilbert space: Hspace_G = L2(SU(2)^E, product normalized Haar measure), with all Peter-Weyl representations present. Equal link values do not identify distinct links.
- Operator: K_G(r) = H_G(r)/(alpha hbar^2) = T_G + r sum_{p in P}(1-a_p), where alpha hbar^2>0, T_G = -(1/2) sum_e Delta_e, and a_p=(1/2)Tr(U_p).
- Normalization: the left generators are i sigma_a, so -Delta has eigenvalues 4j(j+1), j=0,1/2,1,...; the single-link operator -(1/2)Delta has unique normalized constant vacuum and gap g=3/2.
- Receiver: uniqueness of the exact finite-volume ground state and a lower bound for energy above that exact ground state, uniform in G, on the full Hilbert space and its all-vertex gauge-invariant subspace.
- Operation: bounded perturbation of the electric operator for each finite G, followed by restriction to a reducing gauge-invariant subspace. The tensor padding below has a vacuum embedding and a retraction; no recovery of a discarded spin sector is needed.
- Missing data: numerical values of the literature constants c1(S), c2(S). Existence and the resulting symbolic threshold are supplied; numerical optimization remains OPEN.

## Exact adapter for open boundaries

Let S={0,e_1,...,e_d}, m=binomial(d,2), and Lambda=V+S. At every site x in Lambda introduce exactly d rotor factors, one for each positive coordinate direction:

    K_x = tensor_{i=1}^d L2(SU(2)),
    h_x = -(1/3) sum_{i=1}^d Delta_(x,i).

The coefficient 1/3 is (1/2)/g. Hence h_x is nonnegative, self-adjoint, has the unique product constant ground vector Omega_x, and satisfies h_x >= 1 on Omega_x perpendicular. Its unbounded spectrum and infinite-dimensional carrier meet the theorem's stated assumptions directly.

Identify every actual link (x,x+e_i) in E with factor (x,i). Let D=(Lambda x {1,...,d}) minus these actual links be the extra factors. They are auxiliary rotors with their own free electric operators, not altered physical boundary links. Reordering the finite tensor product gives the exact unitary identification

    tensor_{x in Lambda} K_x = Hspace_G tensor Hspace_D.

The plaquette based at x in directions i<j has holonomy

    U_(x,i) U_(x+e_i,j) U_(x+e_j,i)^(-1) U_(x,j)^(-1).

After grouping outgoing links by site, its multiplication operator acts only at sites {x,x+e_i,x+e_j}, a subset of x+S. Its normalized SU(2) trace is real and lies in [-1,1], so ||a_p||<=1. In fact equality holds for an elementary plaquette because continuous link configurations can approach holonomy I or -I on sets of positive Haar measure. The norm bound, rather than equality, is all the proof needs.

For each x in Z^d define a graph-dependent interaction on x+S by

    phi_x^G = -(r/g) sum_{p in P with base x} a_p,

and set it to zero when there is no such plaquette. Identity factors extend the operator to the rest of x+S. There are at most m plaquettes based at x, so

    sup_x ||phi_x^G|| <= m |r|/g.

Every actual plaquette has base x in V and x+S is contained in Lambda=V+S. Thus all desired terms survive the theorem's support-containment rule. The extra interaction terms are zero, and no interaction uses an auxiliary rotor. Extend the same on-site factors over Z^d if a complete infinite-lattice input is desired; the interaction field may depend on G because the finite-volume theorem requires no translation invariance and its constants depend only on S.

This padding is material in d=3. Without it, choosing Lambda=V and using the union support S can discard an existing xy-face plaquette at the upper z-boundary merely because x+e_z is absent. The padded construction retains that plaquette exactly.

Write K'_G = K_G(r) - r|P|I. The padded theorem Hamiltonian is exactly

    A_Lambda = (1/g) K'_G tensor I_D + I_G tensor (1/g) T_D,

where T_D=-(1/2)sum_{e in D}Delta_e has unique vacuum Omega_D, energy zero, and gap g when D is nonempty. No estimate replaces this identity.

The embedding J:psi -> psi tensor Omega_D is isometric, J*J=I, and intertwines A_Lambda J = J K'_G/g. The orthogonal auxiliary sectors remain present and decoupled; J* is the retraction used to read the physical-link operator.

## Uniform bound after subtracting the actual ground energy

Let c1=c1(S)>0 and c2=c2(S)>0 be constants from the primary theorem. If

    s = m|r|/g < c1,

it gives a unique padded ground state and, provided 1-c2s>0, a spectral gap at least 1-c2s above its exact energy.

Each finite K'_G is a bounded perturbation of a compact-manifold Laplacian. It is self-adjoint on the electric operator domain, bounded below, and has compact resolvent; hence it has a ground eigenvector. The tensor identity shows that the ground energy of A_Lambda is inf spec(K'_G)/g and its ground eigenspace is the ground eigenspace of K'_G tensored with Omega_D. Padded uniqueness therefore implies uniqueness for K_G. Applying the padded quadratic-form gap bound to psi tensor Omega_D, with psi perpendicular to that ground state, gives

    gap(K_G(r)) >= g(1-c2s)
                   = 3/2 - c2 m |r|.

Here gap means inf(spec(K_G) minus its unique ground energy), excluding that ground eigenvalue. Adding back the scalar r|P| changes neither the eigenspaces nor this gap. It follows that

    r0(d) = (g/m) min{c1(S), 1/(2c2(S))} > 0

is a valid existential threshold: for every |r|<r0(d),

    gap(K_G(r)) >= g/2 = 3/4,
    gap(H_G(r)) >= (3/4) alpha hbar^2.

For d=2, m=1 and r0=(3/2)min{c1,1/(2c2)}. For d=3, m=3 and r0=(1/2)min{c1,1/(2c2)}, with S and therefore the constants specific to that dimension. The physical coupling case r>=0 is included. No decimal lower bound on r0 has been established.

The result is independent of |V|, |E|, |P|, and of the largest admitted spin, because there is no largest admitted spin. It bounds the energy above the exact perturbed ground state without calculating that state's energy. It neither assumes nor produces a uniform perturbative overlap with the product Haar vacuum.

## All-vertex gauge restriction

Let Q=SU(2)^V act by the usual independent vertex transformations U_(x,y) -> q_x U_(x,y) q_y^(-1). Bi-invariance of the link Laplacian and conjugation invariance of every plaquette trace imply that K_G commutes with this strongly continuous unitary action. Its fixed subspace is the physical all-vertex gauge-invariant Hilbert space and is reducing.

By uniqueness, the full ground line transforms by a continuous one-dimensional unitary representation chi of Q. Every continuous character of SU(2)^V is trivial: its Lie algebra is a direct sum of copies of su(2), equal to its commutator algebra, so the derivative of a character vanishes, and connectedness makes the character constant. Therefore the full ground vector lies in the physical subspace.

For any physical vector orthogonal to the ground vector, the full-space gap quadratic-form inequality applies unchanged. The physical ground is consequently unique and

    gap(K_G restricted to H_phys) >= gap lower bound above.

Equivalently, positivity of the Schrödinger ground state gives another route to its gauge invariance, but it is not needed for this group-theoretic argument. For a graph whose physical Hilbert space is one-dimensional, the inequality remains valid; there are no excited physical vectors.

## Distinguishing controls and limits

1. Boundary grouping must retain the electric term on every physical and auxiliary rotor. An unconstrained auxiliary zero-energy factor would make the padded ground degenerate and violate the theorem's hypothesis.
2. The d=3 top-face example above refutes the naive unpadded use of the common support S. It does not refute the padded argument.
3. Unique symmetry-invariant ground *line* is not sufficient for ground-vector invariance for arbitrary groups. For example, on L2(U(1)), the rotation-invariant operator (-i d/dtheta - 1)^2 has a unique ground e^(i theta), which is charged under U(1). The SU(2)^V character argument is required here.
4. A total perturbation norm bound would grow like |P||r|. The literature theorem uses the uniform local norm m|r|/g instead; replacing it with the total norm loses volume uniformity.
5. A nonzero bulk gap under periodic boundaries alone need not control a separately changed boundary model. The proof uses the theorem's literal empty-boundary construction after exact padding.
6. The conclusion concerns fixed lattice spacing, fixed dimension, this electric normalization, and sufficiently small |r|. It does not establish a continuum limit, a continuum mass gap, any numerical weak-coupling threshold in continuum conventions, or an unbounded range of r.
7. No thermodynamic GNS conclusion is claimed for the graph-dependent padded family. Establishing an infinite-volume physical theory with the desired local algebra and limit family is a further task.

## What was checked

Read the author's complete local definitions, finite-volume Theorem 1, equations (1)-(5), and the placement of the later translation-invariance assumption. Rendered and visually inspected preprint pages 2, 3, and 4 to verify the formulas. Read the supporting proof review on pp. 6-9 and publication attribution on pp. 4 and 17. Checked the other candidate's periodic-volume assumption and journal metadata. Independently derived the open-boundary padding, tensor retraction, norm factors, energy scaling, and physical restriction above. No simulations, package installations, existing test suites, or repository files outside this audit were changed.
