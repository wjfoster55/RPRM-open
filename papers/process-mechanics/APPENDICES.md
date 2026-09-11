# Appendix A. Resolution, composition, and probability

These arguments supply the assumptions behind Sections 4 and 5. They are elementary written proofs and specializations, including material in the supplied mathematical note. They are not claims of new mathematical priority. The finite checks described in Appendix C exercise examples of these results; they do not replace the proofs or establish a physical observation model.

## A.1 When a bundle of observations resolves a question

Can a chosen bundle guarantee an answer before we see its outcome? Every pair of explanations giving different target answers must permit disjoint joint records. Otherwise, a shared record would leave that pair unresolved. Proposition 3 states this guarantee for all admissible records, rather than just a favorable observed one.

Fix a contract, a nonempty finite candidate family $\mathcal H$, a target map $q:\mathcal H\to B$, and a nonempty admissible joint-record set $U(h)\subseteq\mathcal Y$ for each $h$. For $e\in\mathcal Y$, put $C(e)=\{h:e\in U(h)\}$.

**Proposition 3. Opposing-support separation.** Every admissible record $e\in\bigcup_h U(h)$ has exactly one target answer if and only if

$$
q(h)\ne q(g)\ \Longrightarrow\ U(h)\cap U(g)=\varnothing.
\tag{A1}
$$

*Proof.* If opposing candidates admit a common record $e$, both survive it and its answer set has at least two elements. Therefore guaranteed resolution implies (A1). Conversely, take any admissible $e$. It has a survivor. Under (A1), no two survivors can have different targets, so all survivors give the same target value. Their nonempty answer set is a singleton. $\square$

For one realized nonempty $C(e)$, the same proof says that resolution is equivalent to absence of an opposing surviving pair. The universal statement in Proposition 3 is stronger: it concerns every admissible record. One favorable reading does not establish it. Nor does it certify coverage of an actual source outside $\mathcal H$.

For a finite observation bundle $S$, suppose admissibility factors **exactly** at the candidate level:

$$
U_S(h)=\prod_{j\in S}U_j(h).
\tag{A2}
$$

Then

$$
U_S(h)\cap U_S(g)
=\prod_{j\in S}\bigl(U_j(h)\cap U_j(g)\bigr).
\tag{A3}
$$

The finite product is empty exactly when one factor is empty. Thus guaranteed resolution is equivalent to every opposing pair being separated by at least one selected observation. Different observations may separate different pairs. For $S=\varnothing$, the record product contains the single empty record, so resolution requires the target already to be constant. This is a covering condition, not a guarantee for a particular greedy selection rule.

The shared-bit example satisfies (A2) for complete states $(q,b)$, whose readings are deterministic. Its target-level supports in (7) do not factor after $b$ is omitted. These two statements are compatible because they refer to different candidate representations. Probabilistic independence, equality of supports, and exact Cartesian factorization are separate properties.

As a concrete boundary case, consider a scalar measurement with a hard bound $\varepsilon\geq0$ and $U(h)=[m_h-\varepsilon,m_h+\varepsilon]$. Two opposing candidates have disjoint record sets exactly when $|m_h-m_g|>2\varepsilon$. Equality is insufficient: the closed intervals touch at a reading both permit. With centers 0 and $3/2$ and radius 1, either center alone eliminates the other candidate, yet the reading $3/4$ leaves both. This illustrates the gap between a nominal separating observation and a guarantee for all admissible observations.

## A.2 Why correct interval summaries compose

The parent interval contains exactly the values found in its children. Its extreme bounds therefore come from the most extreme child bounds. To decide whether a bound is reached, we must also know whether a child actually takes that value. The proposition records both parts of this argument.

Let $m\ge1$, let $I=\bigsqcup_{j=1}^m I_j$ be a finite partition into nonempty sets, and let $s:I\to\mathbb R$ be bounded. The half-open temporal partition in Section 5 is a special case. For each child, define

$$
\ell_j=\inf_{t\in I_j}s(t),\qquad u_j=\sup_{t\in I_j}s(t),
\tag{A4}
$$

with Boolean flags $\alpha_j,\beta_j$ recording whether those two values are attained in $I_j$.

**Proposition 4. Finite range-summary composition.** The exact parent summary is

$$
\ell=\min_j\ell_j,\qquad u=\max_j u_j,
\tag{A5}
$$

$$
\alpha=\bigvee_{j:\ell_j=\ell}\alpha_j,\qquad
\beta=\bigvee_{j:u_j=u}\beta_j.
\tag{A6}
$$

For $R_\theta(J)=[\exists t\in J:s(t)\geq\theta]$, the parent event is

$$
R_\theta(I)=\bigvee_j R_\theta(I_j)
=[u>\theta]\ \lor\ [u=\theta\text{ and }\beta].
\tag{A7}
$$

*Proof.* Every value in the union is at least $\min_j\ell_j$. Choose a child whose infimum is that minimum. Its values approach its infimum arbitrarily closely, so no larger lower bound works for the union. The supremum argument is dual. A value equal to the global infimum is attained somewhere exactly when it is attained in one of the children having that infimum; this gives $\alpha$. The argument for $\beta$ is the same.

Every point of $I$ is in a child, so existence of a threshold-reaching point in $I$ is equivalent to existence in at least one child. If $u>\theta$, the defining property of the supremum supplies a value above $\theta$. If $u=\theta$, reach requires attainment; if $u<\theta$, reach is impossible. This proves (A7). $\square$

All summaries here concern the same signal and contract, and their contents are assumed correct. The algebra also applies to a finite overlapping cover, but the supplied temporal adapter intentionally requires a partition to preserve its interval contract. No claim that all overlapping evidence is inadmissible follows. Neither (A5) nor (A6) says the entire interval between the bounds is attained. The step-law case is an explicit boundary to that stronger claim.

## A.3 The squared-loss identity

Why can better probabilities matter when every hard decision stays the same? A decision threshold groups many forecasts into one action, while squared loss still distinguishes their probability values. The identity below states what additional information does for true conditional expectations under a fixed probability law.

Work on a probability space with $Y\in L^2$ and sigma-algebras $\mathcal F\subseteq\mathcal G$. Define $m=\mathbb E[Y\mid\mathcal F]$ and $n=\mathbb E[Y\mid\mathcal G]$. Conditional expectations are defined up to almost-sure equality and are also in $L^2$.

**Proposition 5. Nested-information squared loss.**

$$
\mathbb E[(Y-m)^2]-\mathbb E[(Y-n)^2]
=\mathbb E[(n-m)^2].
\tag{A8}
$$

*Proof.* Expand $Y-m=(Y-n)+(n-m)$. Subtracting $(Y-n)^2$ gives $(n-m)^2+2(Y-n)(n-m)$. The product is integrable by Cauchy–Schwarz. Because $n-m$ is $\mathcal G$-measurable and $\mathbb E[Y-n\mid\mathcal G]=0$, the cross term has expectation zero. Taking expectations proves (A8). The right-hand side is nonnegative, and equals zero exactly when $n=m$ almost surely. $\square$

For binary $Y$, $m$ and $n$ are conditional event probabilities. This is the standard conditional-expectation projection identity specialized to Brier loss. It concerns the true stipulated distribution. Fitted predictions, finite-sample scores, and calibration claims have additional statistical requirements.

The following supplied example shows why unchanged decisions need not make probability improvement meaningless. Let $W=0$ and $W=1$ each have probability one half, with

$$
P(Y=1\mid W=0)=\frac35,\qquad
P(Y=1\mid W=1)=\frac9{10}.
\tag{A9}
$$

Without $W$, the event probability is $3/4$. A classifier at threshold one half always predicts 1, with or without $W$, and has expected accuracy $3/4$. The expected Brier losses are nevertheless

$$
\frac34\left(1-\frac34\right)=\frac3{16},\qquad
\frac12\left[\frac35\frac25+\frac9{10}\frac1{10}\right]=\frac{33}{200}.
\tag{A10}
$$

Their difference is $9/400$. This is a constructed probability example, not a reinterpretation of the circuit results. The circuit's observed hard-decision null and its separate probability scores remain as recorded.

# Appendix B. Circuit derivations and saved scores

## B.1 Known input makes the RC state sufficient

For positive $R,C$, an ideal RC circuit under input voltage $u(t)$ obeys

$$
\dot v(t)=\frac{u(t)-v(t)}{RC}.
\tag{B1}
$$

On a segment with constant input $u$ and duration $\Delta>0$, solving the scalar linear equation gives

$$
v(t+\Delta)=u+(v(t)-u)e^{-\Delta/(RC)}.
\tag{B2}
$$

Thus a present voltage and a complete piecewise-constant drive schedule determine subsequent voltages by repeated propagation. A sampled event can be computed from those sampled values; no additional past state is needed under this deterministic model. The historical panel's labels use its own native grid and drive convention. Its saved-row replay verifies those labels and predictions as recorded. The continuous segment identity alone should not be used to assert equivalence of different mid-step switch conventions. The companion kit explicitly distinguishes its historical grid port from propagation split at a switch.

For noisy observations $y_j$ at known past times, a known linear evolution permits a representation $y_j=a_j v_*+b_j+\epsilon_j$ in terms of a chosen reference voltage $v_*$. The coefficients encode the known timing and forced response. Ordinary unweighted least squares gives

$$
\widehat v_*=\frac{\sum_j a_j(y_j-b_j)}{\sum_j a_j^2},
\qquad \sum_j a_j^2>0.
\tag{B3}
$$

This follows by differentiating the quadratic residual sum and setting its derivative to zero. It explains why accounting for evolution differs from averaging voltages at different times. Whether it is an appropriate statistical estimator depends on the error model; its empirical errors in Table 3 do not prove superiority under arbitrary noise or information packages.

## B.2 Two timed voltages and one current

For the ideal series RLC model, use the state $x=(v,i)^{\mathsf T}$, with $v$ in volts, $i$ in amperes, and positive $R,L,C$. Under constant input $u$,

$$
\dot x=Mx+bu,\qquad
M=\begin{pmatrix}0&1/C\\-1/L&-R/L\end{pmatrix},\qquad
b=\begin{pmatrix}0\\1/L\end{pmatrix}.
\tag{B4}
$$

Over lag $\Delta$, let $F=e^{M\Delta}$ and $g=\int_0^\Delta e^{M\tau}b\,d\tau$. Then

$$
x_+=Fx_-+gu,\qquad
v_+=F_{11}v_-+F_{12}i_-+g_1u.
\tag{B5}
$$

Here the subscripts on $F$ are one-based matrix indices. If $F_{12}\ne0$,

$$
i_-=\frac{v_+-F_{11}v_- -g_1u}{F_{12}},\qquad
i_+=F_{21}v_-+F_{22}i_-+g_2u.
\tag{B6}
$$

These equations uniquely recover the current for the admitted model and supplied readings. If $F_{12}=0$, the first equation does not constrain $i_-$: it is either inconsistent with the readings or leaves that coordinate unresolved in the unrestricted state model. At zero lag, $F$ is the identity and this coefficient is zero.

With fixed exact coefficients, reading errors $\delta v_-,\delta v_+$ induce

$$
\delta i_-=\frac{\delta v_+-F_{11}\delta v_-}{F_{12}}.
\tag{B7}
$$

The denominator makes the noise-sensitivity issue explicit. Nonzero is an algebraic inversion condition, not a general guarantee of reliable measurement recovery. The supplied implementation also applies a numerical singularity cutoff; that cutoff is not a calibrated uncertainty policy. The historical recorded maximum error of $1.3173\times10^{-16}\,\mathrm A$ is a noiseless finite-panel observation.

## B.3 Probability scores and hard decisions

Table 5 retains the saved learned probability scores separately from hard-decision correctness. Every entry has zero hard errors at threshold 0.5. The eight RC panel/view combinations share two within-panel Brier values; the five RLC views have different scores.

| Saved panel or view | Rows per view | Mean Brier loss |
|:--|--:|--:|
| RC noiseless: each of four views | 220 | $4.28514624\times10^{-5}$ |
| RC noisy: each of four views | 660 | $4.28883748\times10^{-5}$ |
| RLC: present voltage + plan | 2,391 | $6.57501030\times10^{-5}$ |
| RLC: window mean/spread + plan | 2,391 | $6.56176970\times10^{-5}$ |
| RLC: two-voltage lag + plan | 2,391 | $6.43739567\times10^{-5}$ |
| RLC: raw union + plan | 2,391 | $6.42205088\times10^{-5}$ |
| RLC: ideal current readout + plan | 2,391 | $6.56243121\times10^{-5}$ |

: Learned probabilities from the supplied saved rows, rounded for display. The four RC views are present, window mean/spread, two-voltage lag, and raw union, each with the supplied plan. The ideal-current RLC view has an additional state channel. These rows reuse sources and do not constitute independent trials or establish population-level differences between methods. {#tbl-brier}

The total is $4(220)+4(660)+5(2{,}391)=15{,}475$ learner rows. The separate observer export contains $220+660+2{,}391=3{,}271$ rows. Raw squared losses recomputed from each learner's saved probability and label agree with the stored row loss. State-error and observer summaries are reaggregated from the exported error values, rather than independently reconstructed from source trajectories.

The equation-observer scores near $10^{-12}$ arise when a correct hard prediction, 0 or 1, is clipped by $10^{-6}$ before squared loss. They are different from the learned probabilities in Table 5 and do not measure a trillion-to-one physical failure rate.

For the withheld-plan control, the equal prior is local to the 60 supplied pairs. Of these, 36 pairs agree and 24 conflict. With two realized branch rows per pair, the overall unclipped loss is $1/10$ and the ambiguous-subset loss is $1/4$. The exact decimal implied by the stated clipping rule is $0.1000000000006$; the original floating-point summary reports $0.10000000000060001$. This is a last-bit representation difference, not a changed result.

# Appendix C. Claim traceability and reproduction

## C.1 Ten retained claims, with their evidence grades

The short labels below preserve the candidate manuscript's claim mapping. The public `CLAIM_ID_MANIFEST.json` provides the distributed claim record [[12]](#bib-ledger). Full identifiers are formed by appending `-01` to each short label. The evidence grade is part of the claim.

| Label | Claim and scope | Evidence used in this revision |
|:--|:--|:--|
| PC-CONT | Sufficient-state RC null; 220 origins. | Saved observer decisions reaggregated; known-model argument; source-return protocol. |
| PC-EST | Noisy-RC voltage MSE contrast; 660 origins. | Saved error values reaggregated; observation/input mismatch retained. |
| PC-STATE | Noiseless two-voltage reconstruction; 2,391 origins. | Saved current errors reaggregated; affine inverse checked algebraically; companion replay. |
| PC-INPUT | 60 withheld-plan pairs; 24 conflicts. | Saved pair labels and equal-prior arithmetic; 0.10 full loss, 0.25 ambiguous loss. |
| PC-NULL | Zero hard errors in 15,475 learner rows. | Probabilities and labels reaggregated at threshold 0.5; dependent rows retained as such. |
| W-COMP | 19 stipulated laws across four partitions. | Exact companion replay of 76 comparisons; conditional proof in Appendix A. |
| W-TRUST | Structurally accepted wrong triangle range. | Companion hostile-control replay; primary and auxiliary thresholds distinguished. |
| W-REUSE | Historical cache-context repair. | Producer-reported 24/24 receipt identity in supplied return; no independent historical replay. |
| C-CAL | Easy synthetic $D$-first policy null. | Source return reports 60 tests and 18 cases; smaller companion checks separately replayed. |
| C-MEAS | Four-curve partial reconstruction. | Supplied status and domain return; primary figure caption checked; no redigitization. |

: Claim identities and actual review scope. A teaching-kit replay is not a substitute for the historical study named in a claim. {#tbl-claims}

The method, transfer, algorithm, and biological proposals remain, respectively, proposed, untested, not established, and not executed in the supplied ledger. Their original machine labels are `PROPOSED_R2_DRAFT`, `NOT_TESTED`, `NOT_ESTABLISHED`, and `NOT_EXECUTED`. They are not additional accepted empirical results.

## C.2 Source anchors and available artifacts

The interval study in Section 6.2 is archived as the *Water evidence packet* [[10]](#bib-water). Water is the project label for these exact signal and summary fixtures.

The circuit content anchor is `d2e63b56d79d`; the interval-composition anchor is `90bf41040076`; the historical reuse-repair anchor is `40ed3e5a584a`; the measurement tip and content anchors are `a0538e8b50bd` and `2fbc5984a86f`. These are shortened source identifiers, not proof of correctness. The complete supplied identities remain in the companion claim manifest and in this revision's review record.

The candidate's `experimental/process-mechanics/public_evidence/` directory contains the saved circuit rows and pairs, their source summaries, the interval trust extract, the measurement-status card, and the claim-support map. The `rprm/process_mechanics/` modules and the adjacent example kits implement selected finite contracts. Some historical generator, cache, and measurement-reconstruction files are referenced by the domain returns but are not included as runnable source in this public payload.

Section 8 revisits material already included with the first paper. The finite chain witness is specified in `experimental/protein-folding/README.md` and Manifesto Section III.6. The unexecuted molecular comparisons are developed in `research-packs/folding-dynamics/README.md`, `research-packs/brca1-function/README.md`, and Manifesto Section IV.1. Figure 2 redraws that existing geometric witness; it adds no molecular experiment. These application discussions do not change the ten retained claim grades in Table 6. The root lattice pack is separate from the small protein teaching example run by the process-mechanics aggregate below.

The first-paper reference is *The RPRM Manifesto*, version 1.0.3, DOI [10.5281/zenodo.22650748](https://doi.org/10.5281/zenodo.22650748). That DOI identifies the first paper, not this manuscript. The DOI for this working paper is 10.5281/zenodo.22709682.

## C.3 Reproduction and the limits of replay

The public payload contains both the paper and the companion code it uses. Run the following commands from the payload root, which contains `experimental/` and `rprm/`. No private editorial archive, repository, or credential is required. Python 3.10 or newer is required; Node.js 18 or newer runs the JavaScript checks, and NumPy/SciPy enable the optional RLC path.

Create a directory for the new verification receipts. In the command below, replace `<absolute-receipt-directory>` with its actual absolute path. Enter each command as one shell command; visual wrapping in the PDF does not add a newline to its path.

```text
python -I -B experimental/process-mechanics/verify_all.py --output <absolute-receipt-directory>/VERIFY_ALL.json
```

The runner writes the consolidated JSON at that location and individual receipts and logs in its sibling `verify_parts/` directory. Without `--output`, it prints the consolidated receipt and writes the parts under the companion's `expected/` directory. The aggregate comprises seven kit checks, adapter regressions, and public saved-row reaggregation. A successful run returns exit code zero; a failed job returns a nonzero code. Optional dependency skips are reported separately and must remain visible. These are nine software and example jobs, not nine scientific experiments. The protein, retry, and units examples add no scientific claim to this paper.

To repeat only the public saved-row arithmetic, run:

```text
python -I -B experimental/process-mechanics/public_evidence/pc1/reaggregate_tables.py
```

This standard-library script recomputes hard decisions from saved probabilities and labels, aggregates the exported observer-error columns, and recomputes the withheld-plan conflicts and mixture loss. It compares the derived figures with the preserved producer extracts. It does not regenerate trajectories, refit learners, or independently establish how the original source error columns were produced.

The arithmetic command also rewrites three derived summaries in the companion’s `public_evidence/pc1/` directory. The claim table is `CLAIM_TABLE.json`; the other outputs are `hard_decision_counts.json` and `HARD_DECISION_SUMMARY.json`. An optional `--output` redirects only the claim table. The two other summaries still go to the evidence directory. Use a writable local copy. The aggregate runner invokes this same arithmetic command. Both routes were executed for this candidate; the nine aggregate jobs passed with no observed optional skip. The source rows, pair records, and producer extracts retained their original bytes.

The earlier editorial review also replayed 16,875 support-separation cases, 14,580 factorized-support cases, 243 rational squared-loss identities, 510 finite positive-likelihood transcripts, and 14 focused tests. These counts are historical reviewer-local checks of supplied mathematical examples. They were not rerun in this integration and are not promised by either public command above. The private commands and their execution records remain in private review provenance. None of these finite counts enlarges the theorem domains or establishes general tool soundness.

The paper's `BUILD_README.md` gives the separate PDF build route. `DOCUMENT_BUILD.json` binds all three canonical text sources, the template, builder, figures, and PDF. The layout receipt identifies the PDF actually rendered and inspected. A matching hash establishes byte identity; it does not establish mathematical truth, scientific coverage, or publication approval.

## Assistance disclosure {.unnumbered}

Automated assistants and software supported drafting, mathematical and source review, saved-result reaggregation, and typesetting. William J Foster is the named author. Assistance does not establish independent scientific replication or transfer authorship to a tool. The claim-specific evidence grades and limits are stated in the text and Appendix C.
