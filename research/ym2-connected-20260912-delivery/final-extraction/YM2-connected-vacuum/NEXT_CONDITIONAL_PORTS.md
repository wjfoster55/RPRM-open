# The next conditional port: a local remainder oscillation

12 September 2026. This note derives a bound independent of graph volume
for the order-two log-density head in
[CONNECTED_VACUUM.md, (CV14)](CONNECTED_VACUUM.md). It then retains the
exact missing remainder term needed to apply the same bound to the actual
vacuum. It does not infer a spectral gap from a conditional row sum.

**Result.** On the declared finite open square or cubic lattice graphs,
put `m=2(d-1)` for dimension `d in {2,3}`. For `0<=r<=1`, the actual
single-edge conditional influence coefficients obey

```text
sum_(j != e) c_ej(G,r)
 <= m r + [16m(m-1)/117] r^2
          + (1/4) sum_(j != e) epsilon_ej(G,r).           (CP1)
```

Here `epsilon_ej` is the full exterior-change oscillation of the actual
log-density remainder, defined below. The first two terms are proved and
independent of the number of plaquettes. A useful uniform bound on the
last term is the next missing port.

## 1. Carrier and exact decomposition

Use the finite graph class in (CV12)-(CV15): distinct elementary square
plaquettes on an open subgraph of the ordinary square or cubic lattice,
full link kinetic operator, gauge invariance at every vertex, and no
periodic identifications or duplicated plaquette occurrences. The
configuration carrier here is the full product `Q_G=SU(2)^(E_G)` with
product normalized Haar measure. The actual positive vacuum density is
gauge invariant on this carrier. Conditional distributions are taken by
fixing the actual outside link occurrences; they are not conditionals of
an assumed product of trace coordinates.

For each plaquette and unordered shared-edge pair, define real functions

```text
f_p(U_p) = (r/3)a_p - (r^2/144)a_p^2,
g_pq(U_(p union q)) = r^2 C_pair(a_p,a_q,w_pq),
C_pair(a,b,w) = (4w-3ab)/702,
F_head = sum_p f_p + sum_(p<q, p~q) g_pq,
F_G = log rho_G = F_head + R_G.                           (CP2)
```

An additive normalization scalar may be assigned to either summand; it
does not affect any oscillation below. Definition (CP2) is exact for the
actual density. Near zero, `R_G` is the Taylor remainder plus a scalar.
No claim that it is small at every `0<=r<=1` is made. The polynomial
head and all conditional inequalities below are well-defined throughout
that interval, while the size of `R_G` remains a separate question.

The supplied ports are the graph, the true density, and the proved head.
The requested readout is a uniform bound on conditional changes under
one outside-link replacement. The missing port is a graph-uniform bound
on the joint remainder response. No inverse fiber or complete ground
state is inferred from this inequality.

## 2. Each head factor has a fixed oscillation bound

For a real function, `osc h=sup h-inf h` on its declared carrier.
The function `f(a)=ra/3-r^2a^2/144` is nondecreasing on `[-1,1]`
for `0<=r<=1`: its derivative is at least `r/3-r^2/72>=0`.
Its endpoint difference is `2r/3`. The adjacent coefficient bound from
(CV2) gives

```text
osc f_p = 2r/3,
osc g_pq <= 4r^2/351.                                   (CP3)
```

The latter is the exact full two-square oscillation; an embedding or
fixed exterior can only reduce the admitted range. The factor support
is the seven-edge union of the two plaquettes. In particular, the
outer-loop term alone is not used as the support of the whole pair
factor: `a_p a_q` can depend on the shared edge too.

Let `A` range over these explicit factor occurrences, with function
`F_A` and edge support `supp A`. For distinct edges `e,j`, set

```text
b_ej(r) = 2 sum_(A: e,j in supp A) osc F_A.               (CP4)
```

If two outside configurations differ only at edge `j`, every factor
that does not contain `e` contributes only an inside-independent scalar
to their conditional log-density ratio. Every factor containing `e`
but not `j` has identical values in the two exteriors. For a remaining
factor, the inside oscillation of its difference is at most twice its
full oscillation. Thus `b_ej` bounds exactly the required head response,
including its shared occurrences.

## 3. Count only factors incident to the updated edge

Every edge belongs to at most `m=2(d-1)` elementary plaquettes. Each
plaquette has four edges, and on each edge there are at most `m-1`
other plaquettes. Hence it has at most `4(m-1)` adjacent plaquettes.

An adjacent pair whose union contains `e` has at least one plaquette
containing `e`. Choosing that plaquette first gives at most
`4m(m-1)` unordered pairs. This is a safe overcount: a pair in which
both plaquettes contain `e` is counted twice. A single plaquette has
three edges other than `e`; a pair union has six. Therefore

```text
sum_(j != e) b_ej
 = 2 sum_(A: e in supp A) (|supp A|-1) osc F_A
 <= 2m * 3 * (2r/3)
    + 2[4m(m-1)] * 6 * (4r^2/351)
 = 4m r + [64m(m-1)/117] r^2.                           (CP5)
```

The finite local incidence checker confirms the complete interior stars:
there are `7` such unordered adjacent pairs in two dimensions and `42`
in three, below the safe bounds `8` and `48`. The exact interior count
is `4m(m-1)-binomial(m,2)` because the pairs sharing `e` are exactly
the double counts. Boundary removal or selecting fewer plaquettes cannot
increase the number. The proof of (CP5) uses only the safe bound.

Keeping only pairs whose *both* plaquettes contain `e` would miss valid
factors: that count is just `1` in two dimensions and `6` in three,
omitting `6` and `36` incident pair factors respectively. This is a
distinguishing hostile count retained in the checker.

## 4. The actual remainder port and conditional comparison

Let `pi_e^G(.|omega)` be the normalized single-link conditional law of
the actual vacuum, where `omega` fixes all links other than `e`.
For two exteriors `omega,omega'` that agree away from `j`, define

```text
epsilon_ej(G,r) = sup_(omega,omega' differing only at j)
  osc_(U_e) [R_G(U_e,omega')-R_G(U_e,omega)],

c_ej(G,r) = sup_(same omega,omega')
  TV(pi_e^G(.|omega'), pi_e^G(.|omega)).                   (CP6)
```

Total variation is `sup_A |mu(A)-nu(A)|`. Smooth positivity on each
fixed compact source makes these versions of the conditional laws and
their log ratios well-defined for every exterior. The remainder
oscillations are finite on each fixed graph, but no graph-uniform
summability follows from that fact.

The complete conditional log tilt has inside oscillation at most
`b_ej+epsilon_ej`. Apply the accepted
[bounded-tilt lemma, (C4)](accepted_sources/ym2_signed_differences/NEXT_CONNECTED_OBLIGATION.md):

```text
c_ej(G,r) <= tanh((b_ej+epsilon_ej)/4)
           <= (b_ej+epsilon_ej)/4.                       (CP7)
```

Summing and using (CP5) proves (CP1). In particular, for the explicit
head density `rho_head=exp(F_head)/integral exp(F_head)`, the remainder
is only a scalar and every `epsilon_ej` is zero. Its proved row bounds
are `2r+(32/117)r^2` in two dimensions and
`4r+(64/39)r^2` in three dimensions. These are statements about that
specified head density. Equation (CP1), with its remainder term, is
the statement about the actual vacuum.

To obtain a strict actual conditional row bound `theta<1` uniformly,
one sufficient missing estimate would be a number `eta(r)` satisfying

```text
sup_(admitted G,e) sum_(j != e) epsilon_ej(G,r) <= eta(r),
m r+[16m(m-1)/117]r^2+eta(r)/4 <= theta < 1.              (CP8)
```

This exposes an explicit next theorem to prove. No spectral-gap theorem
is invoked here. A further transfer would have to supply its precise
conditional criterion, function space, measure, update rates, relation
to the electric Dirichlet form, and any volume or physical-scale limits.

## 5. Why the current remainder does not fill this port

The proved two-square `L^2` wavefunction remainder, and the subsequent
`L^2` log remainder used for the integral witness, do not control a
supremum over outside configurations and an inside oscillation. A
function may have small `L^2` norm while being large on a narrow set of
positive measure. Nor does the fixed-graph `C^k` existence argument
supply a constant summable over all outside edges and all graph sizes.
The elementary global analytic radius `3/N` also shrinks with volume.

Thus (CP5) closes the volume-independent *head* count. The actual
remainder estimate (CP8) remains OPEN. The positive actual-vacuum
witness supplies a real missing-joint distinction, but not the stronger
conditional norm needed here.

## Verification

Run from this packet directory:

```powershell
python -I -B check_conditional_head.py
```

The default is read-only and compares the full deterministic receipt
[RESULTS_CONDITIONAL_HEAD.json](RESULTS_CONDITIONAL_HEAD.json).
`--write-results` intentionally regenerates it. The checker generates
only the finite elementary plaquette incidence stars around one edge in
dimensions two and three and checks the rational coefficients. It does
not build a large graph, simulate a density, run old suites, or verify
the written all-graph or all-exterior quantifiers by sampling.
