# A joint field law from compatible conditional steps

12 September 2026. A bounded continuation of the accepted YM2 work. The
positive-conditional reconstruction ingredient is established probability
theory; the explicit smooth SU(2) statement and its vacuum/gap certificate
are derived here at the stated scope. This is not a cryptographic security
theorem or a claim that computational commit order is physical time.

## 1. Supplied carrier, neighboring rules and readout

Fix a finite admitted open lattice graph with N links and configuration
space M=SU(2)^N, product normalized Haar measure mu, and the usual vertex
gauge action. Supply, for each link i, a strictly positive smooth function

```text
k_i(a | x_-i),       integral k_i(a | x_-i) dmu_i(a)=1.
```

It is a proposed full conditional density for link i given every other
link. The carrier is finite-dimensional but includes every group value;
there is no spin cutoff. The theorem does not assume that only geometric
nearest neighbors enter k_i. Finite interaction range would be an
additional property to establish for a proposed family.

The requested readout is the entire joint probability law, not one
particular field configuration and not the chronological update history.
Because all k_i are positive, many configurations are admitted even when
the joint law is uniquely determined. Equal laws and equal sample states
must remain distinct.

For x,y differing only at i, define the positive transition ratio

```text
r_i(x,y)=k_i(y_i | x_-i)/k_i(x_i | x_-i).                (CR1)
```

These ratios automatically telescope along repeated updates of the same
coordinate: r_i(x,y)r_i(y,z)=r_i(x,z), and reversing an update inverts
its ratio. This is a ratio of densities, not a stochastic transition
probability or a quantum time-evolution amplitude.

## 2. The exact compatibility condition

Let x^i replace coordinate i, x^j replace j, and x^ij replace both,
with i different from j. Require the rectangle identity at every such
configuration and every pair of replacement values:

```text
r_i(x,x^i) r_j(x^i,x^ij)
 = r_j(x,x^j) r_i(x^j,x^ij).                            (CR2)
```

**Theorem.** These smooth strictly positive full conditional densities
come from one normalized strictly positive smooth joint density if and
only if CR2 holds. When it exists, that joint density is unique.

**Necessity.** If p is a joint density with these conditionals, then
r_i(x,y)=p(y)/p(x). Both sides of CR2 equal p(x^ij)/p(x).

**Sufficiency.** Choose any reference configuration a. For each x, move
from a to x by replacing each coordinate once in a chosen order. Let F(x)
be the product of the ratios CR1 along that path. Swapping two adjacent
updates leaves this product unchanged by CR2. Every permutation of the
updates therefore gives the same F(x).

More generally, any finite coordinate-update path can be reordered by
these adjacent swaps so that updates to each coordinate are grouped.
Updates in the same coordinate telescope by CR1. The resulting product
depends only on the endpoints. Thus every closed path has product one,
and F(y)/F(x)=r_i(x,y) for every single-coordinate replacement.

F is smooth and positive: its chosen N-step formula is a finite product
of smooth positive functions with nonzero denominators. Compactness
implies 0<Z=integral F dmu<infinity. Define p=F/Z. For a fixed exterior,
p has the same ratios as k_i along coordinate i; their normalizations
then identify its conditional density with k_i.

**Uniqueness.** The ratio of any two such joint densities is unchanged
under every coordinate replacement. Any two configurations are joined
by finitely many replacements, so that ratio is constant. Unit integral
fixes it to one. The reference a changes only the unnormalized scale of
F, which disappears upon normalization.

This gives the complete joint-law fiber: ONE(p) when CR2 holds, and NONE
when a violated rectangle supplies a contradiction. An incomplete check
of infinitely many replacement values is OPEN, not a certificate that
all rectangles close. Malformed or unnormalized supplied kernels are
admission errors.

## 3. What can be forgotten after closure

Once the kernels and their compatibility theorem are retained, the
chronological path used to compute a density ratio is unnecessary for
this readout. Any admitted path gives the same answer. Its endpoint
reference can be changed using the exact ratio; no distinguished
physical starting configuration is required.

This is a precise sense in which current-state reconstruction does not
need a chronological ledger. It still needs the conditional laws, their
scope, and the justification of CR2. Retaining only a hash of unknown
laws does not provide those laws or their soundness. Retaining the
kernels need not be compact or inexpensive: the theorem proves neither
a short encoding nor cheap normalization, acquisition, or compatibility
checking on arbitrary input families.

The use of the word “conditional” also matters. The law for one site
comes from its relations with the rest, but it does not eliminate that
site's possible values. A surrounding context can support several
possible values with specified probabilities. This theorem reconstructs
the distribution of the whole field, not a uniquely forced microstate.

## 4. Gauge covariance is preserved

Assume the supplied kernels transform covariantly under every fixed
vertex gauge transformation: transforming all link arguments leaves
their corresponding conditional density values unchanged. Haar
measure is preserved by the endpoint left/right multiplications.
The gauge-transformed joint p then has the same normalized conditional
kernels as p. Uniqueness proves that p is gauge invariant.

This argument uses covariance while the exterior is transformed. It
does not assume that a conditional law at one frozen exterior is
independently invariant under the whole vertex gauge group.

## 5. A second closure condition selects the actual YM vacuum

Compatibility reconstructs a candidate p. Set phi=sqrt(p), so
||phi||_(L2(mu))=1. Keep the accepted Hamiltonian

```text
A(r)=T-rS,       T=-Delta/2,       S=sum_p a_p.
```

The physical Hamiltonian differs by the scalar r times the plaquette
count and by its stated positive energy unit. Define from the supplied
conditional densities alone

```text
b_i=(1/2) grad_i log k_i.
```

The conditional normalizer is constant in coordinate i, so
b_i=grad_i log phi. Therefore the candidate's local-energy residual is

```text
E_candidate(x)
 = -(1/2) sum_i [div_i b_i + |b_i|^2] - rS(x)
 = (A phi)(x)/phi(x).                                  (CR3)
```

The divergence and gradient use the accepted unit-round SU(2) metric.
Equation CR3 is an identity of smooth functions, not a numerical sample.

**Vacuum certificate.** If the reconstructed gauge-invariant kernels
satisfy the additional condition that CR3 is one constant E on the
entire configuration space, then A phi=E phi. The exact form identity

```text
q_(A-E)[phi f]=(1/2) integral |grad f|^2 p dmu           (CR4)
```

shows E is the lowest energy. Equality forces f constant on the
connected product manifold, so the positive vacuum is unique. Thus
compatible conditional data plus constant local energy can certify the
actual finite-graph vacuum without starting from a global Fourier
construction of log phi.

For a physical gap, supply a third, quantitative port: every k_i has a
conditional gradient Poincare constant at most c_*<infinity, uniformly
over graphs, links and every exterior, and the influence matrix C has a
proved graph-uniform contraction rate q<1. The accepted
conditional-update argument and forest-complement cover then yield

```text
gap_phys(A) >= [d/(d-1)] (1-q)/(2 c_*).                 (CR5)
```

The full physical form domain is covered by the same smooth
approximation and gauge averaging used in the accepted overlap proof.
The independent [chain estimate](CHAIN_ESTIMATES.md) also allows a
positive weighted influence certificate C s<=q s, with its exact
finite-graph and uniformity conditions.

These are three different closure tests:

```text
path consistency  -> one joint law;
constant CR3      -> actual vacuum of this Hamiltonian;
uniform response  -> a positive uniform physical gap.
```

The first does not imply the second, and the second without quantitative
uniformity does not supply the third over increasing graph families.

## 6. Exact separating cases

**Normalized local rules can contradict each other.** On the separately
declared two-bit control carrier, let k_1(1|x_2=0)=1/2 and
k_1(1|x_2=1)=2/3. Let k_2(1|x_1)=1/2 for both x_1 values. All kernels
are positive and normalized. Going from 00 to 11 by changing coordinate
1 then 2 gives ratio one; reversing the order gives ratio two. Hence
CR2 fails and there is no joint positive law with these conditionals.
No assertion by one local rule can repair that contradiction.

**A genuine joint law need not be the YM vacuum.** The explicit
reference from the preceding turn,

```text
phi_r=exp(rS/6)/||exp(rS/6)||_2,
```

gives compatible, positive, smooth, gauge-covariant conditionals and
therefore passes CR2 exactly. The accepted calculation gives

```text
E_candidate(x)=-(r^2/72)|grad S|^2.
```

On a single elementary square this is
-(r^2/18)(1-a^2). For r>0, a=1 gives zero while a=0 gives -r^2/18.
Both are actual SU(2) configurations. Thus this perfectly consistent
conditional network fails the actual-vacuum test CR3. This reuses the
accepted exact trial-reference witness; its old verifier is not rerun.

**Consistent laws with tame local ratios can still have a slow
collective mode.** The preceding vacuum-atlas note constructed
p_N proportional to cosh(t sum a_p) on disjoint squares connected by
tree paths. It is smooth and gauge invariant, all its conditional
ratios are compatible, and its one-link density ranges are uniformly
bounded. Yet its reference diffusion physical gap is at most
2/[N m(t)^2]. That auxiliary family is not asserted to be the actual
vacuum of the retained plaquette Hamiltonian. It shows why consistency
and single-link control cannot replace CR5's collective estimate.

## 7. Past, proposed future, and the instant of acceptance

The official FLICK contract has an exact computational reading here:
retain a valid parent certificate; prepare a proposed successor against
that parent and the next receiver; verify the complete new conditional
and physical obligations; install only if the expected parent revision
is still current. A failed or stale attempt leaves the current committed
state unchanged. It does not restore an old state over an intervening
valid successor.

The causal order of these checks avoids a circular justification in
which a candidate's own acceptance output proves its premises. It does
not prove a physical ontology of past, present and future. Nor does it
require recreating the whole prior chronological log whenever a
receiver-sufficient certificate and its retained source remain available.

For YM, CR2–CR5 give substantive contents for that proposed certificate.
A source-bound record with “PASS” written on it is insufficient unless
the mathematical implications and all admitted cases are justified.

## 8. Established ingredient and open work

Conditional specifications, their restrictions and reconstruction of
joint laws are established literature. Brook (1964) is the historical
source; its publisher metadata were checked, but the original article
was not accessible in this browsing session. A directly inspected
primary treatment is Besag (1972), section 2, equations 4–10, which
derives an ordered density-ratio reconstruction, compares opposite
orders, and discusses extension to continuous densities:

- [Brook, original publication metadata](https://academic.oup.com/biomet/article-abstract/51/3-4/481/291953).
- [Besag, Nearest-Neighbour Systems and the Auto-Logistic Model for Binary Data](https://www2.stat.duke.edu/~scs/Courses/Stat376/Papers/GibbsFieldEst/Besag1972.pdf).

The complete proof above states the particular compact-product version
being used and its SU(2) gauge/vacuum/gap adapter. No novelty claim is
made for conditional reconstruction or path consistency. The new
research contribution is the explicit alternative certificate and the
separation of its still-missing YM obligations.

What remains OPEN is to construct a conditionally compatible family
meeting CR3 for the actual Hamiltonian and CR5 uniformly on a larger
coupling domain, or prove a controlled residual substitute. This note
supplies neither that family nor a continuum limit. The finite checks
test exact illustrative kernels, order changes, violations and source
accounting. The smooth, all-spin and all-volume implications depend on
the written proofs and stated premises, not finite sampling.
