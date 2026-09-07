# Immune mechanisms: preserving alternatives and selecting informative assays

**Status: experimental evidence pack; quantitative evaluation unexecuted and currently unavailable.** This pack contains a source-to-assay evidence matrix, a finite inference specification and a complete synthetic example. It contains no person-level records, recovered historical biological theory, fitted classifier or diagnostic result. The proposed operation is to expose which observations distinguish specified mechanistic hypotheses and which uncertainties remain.

## A concrete question beyond the antibody label

Different molecular routes can be associated with an overlapping antibody-deficiency phenotype. The research question is therefore conditional: given a declared cellular context and a partial assay record, which source-supported mechanism hypotheses remain compatible, and which additional observation would separate them?

The selected NFKB1 study links altered transcripts and protein processing with insufficient NF-κB1 p50 in its investigated setting. NFKB1 encodes the p105 precursor from which p50 is processed. This supplies a transcript/protein-processing route with defined experimental observations. [Fliegauf et al., American Journal of Human Genetics (2015)](https://pubmed.ncbi.nlm.nih.gov/26279205/).

The selected CTLA4 study concerns a distinct inhibitory-regulatory pathway. It connects CTLA4 insufficiency with regulatory T-cell dysfunction and altered effector T-cell and B-cell behavior. Neither result identifies a universal mechanism for the entire CVID label. [Kuehn et al., Science (2014)](https://pubmed.ncbi.nlm.nih.gov/25213377/).

The proposal is useful only if it preserves these distinctions while admitting missing, mixed and unresolved evidence. A mechanism name is not a numerical target until its experimental definition and independent evidence are fixed.

## Source-to-assay-to-target evidence matrix

Each row below is a literature-level evidence unit. It is not a synthetic individual or a reusable quantitative observation. “Not supplied” describes this matrix's evidence coverage, not normal biology.

| Mechanism or evidence level | Source-supported assay path | Target this path can support | Missing information and claim boundary |
|---|---|---|---|
| NFKB1 transcript/protein route | Transcript analysis by RT-PCR and sequencing; p105/p50 immunoblotting; stimulus-related p50 localization observations | Reconstruction of the reported transcript, protein-supply and processing evidence leading to p50 insufficiency in the studied context | No CTLA4 functional measurement is supplied by this row. Do not assign all NFKB1 variants the same effect or turn this into a universal deterministic assay signature. [2015 primary study](https://pubmed.ncbi.nlm.nih.gov/26279205/) |
| CTLA4 regulatory route | CTLA4 RNA/protein measurements; regulatory T-cell phenotype and suppressive-function assays; effector T-cell proliferation observations | Reconstruction of the reported inhibitory-regulatory defect and its cellular consequences | No NFKB1 processing measurement is supplied by this row. Expression, suppression and proliferation are distinct endpoints; one cannot replace another without a tested map. [2014 primary study](https://pubmed.ncbi.nlm.nih.gov/25213377/) |
| B-cell phenotype classification | Flow-cytometric B-cell subsets, including switched-memory, transitional and CD21-low populations, with appropriate gates and denominators | Published subgroup assignment and its reported associations | EUROclass is a phenotype classification, not a unique molecular mechanism. Its exact methods and thresholds must be pinned before implementation. [Wehr et al., Blood (2008)](https://ashpublications.org/blood/article/111/1/77/107980/The-EUROclass-trial-defining-subgroups-in-common) |
| Association or modifier evidence | A later CVID cohort distinguishes causative assignments from associated variants, including TNFRSF13B/TACI associations | An explicitly graded association claim or hypothesis for functional investigation | An associated variant alone does not supply a sufficient causal mechanism or a measured pathway target. No matching functional assay table is acquired here. [Cunningham-Rundles, Casanova and Boisson (2024)](https://www.frontiersin.org/journals/genetics/articles/10.3389/fgene.2023.1272912/full) |
| Unresolved, other or mixed mechanism | The same cohort describes heterogeneous genetic/phenotypic findings, including incomplete causal resolution | Preservation of unresolved evidence and competing explanations | This is an explicit open category, not a negative control proving normal function. Absence of an identified cause does not identify one common unknown cause. [2024 primary study](https://www.frontiersin.org/journals/genetics/articles/10.3389/fgene.2023.1272912/full) |

These paths nominate assays for further research; they do not establish that those assays perfectly separate the rows. In particular, cross-pathway normal values must not be invented to complete a rectangular table.

## Two tasks and their admitted inputs

**Task E: evidence completion.** Starting with source assertions and a declared context, return the complete set of compatible named hypotheses, their supporting and conflicting evidence, and the measurements still missing. The current deliverable supports this task at literature level.

**Task A: prediction of a withheld assay block.** If appropriate reusable quantitative inputs become available, predict an independently measured cellular endpoint or its calibrated outcome set. Examples are a supplied protein-processing measurement or an independently measured regulatory-function readout. This task remains unavailable; a paper's aggregate counts are not individual observations.

For Task A, the target block and every derived copy are excluded from inputs. A class defined by p50 measurements cannot be predicted from those same p50 measurements and called independent validation. A suppression target cannot use the suppression assay or a mechanism label constructed from it as a feature. Gene identity may be an explicitly admitted baseline input in a future genotype-to-assay task, but identifying the gene from its name is not a mechanistic discovery. Source title, study identifier and publication fingerprint remain provenance, not predictors.

The present input schema has no person, family or sample identifier fields:

| Field block | Proposed content |
|---|---|
| Evidence locator | DOI/URL, version, figure or methods section, assertion locator, extraction date and source hash when local reuse is authorized |
| Assertion grade | Direct assay observation, experimental perturbation, association, proposed explanation, contradiction or unresolved |
| Context | Species, cellular system, stimulation and culture condition, measurement time, comparator and experimental scope |
| Assay definition | Molecule/cell population, operation measured, instrument/readout type, units, denominator or normalization, gating convention |
| Value availability | Reported value or qualitative direction; uncertainty when supplied; observed, not reported, failed assay, not applicable or unresolved interpretation |
| Dependencies | Upstream measurements and transformations; whether the field is eligible as input, target or neither for the chosen task |
| Hypothesis binding | Exact claim being supported or challenged; allowable context; explicit alternatives and cross-assays still missing |

A quantitative extension would need a separate validated experimental-record table with real independence groups and input/target lineage. Construct-based or other suitably public cellular experiments could qualify. No patient data are acquired or represented by this pack.

## What RPRM would add, and what ordinary methods already do

The proposed RPRM contribution is a receiver-specific contract combining three operations: keep the full compatible joint fiber, expose an explicit witness when a proposed grouping loses the requested assay answer, and choose a bounded next observation using its actual separating power. It would retain source routes and distinguish unobserved values from contradictions.

None of these elementary operations is claimed as new decision theory. Conventional missing-data models, constraint solvers and active feature acquisition are necessary comparators. The testable application claim is that enforcing this joint evidence contract prevents unsupported unique answers while achieving a useful ambiguity/cost tradeoff. Simply adding protein and cell features to an ordinary classifier is not a distinct RPRM result.

An antibody-only grouping is the coarsest literature-level baseline. EUROclass is a richer phenotype baseline when its required B-cell measurements actually exist. Neither should be numerically evaluated on inputs it does not admit. A conventional regularized model using exactly the available features, and a conventional cost-aware assay-selection rule using the same candidate constraints, provide matched comparisons when quantitative data become available.

## Complete finite inference rule

Let $H$ be a finite catalogue of context-specific hypotheses and let $J$ be a finite set of admitted assay coordinates. Each coordinate $j$ has a declared finite nonempty outcome alphabet $V_j$. An admitted hypothesis supplies a finite nonempty joint allowed relation
$$
R_h\subseteq\prod_{j\in J}V_j.
$$
A tuple $t\in R_h$ assigns one result to every declared coordinate. Correlations between coordinates belong to this relation. Per-assay allowed sets $S_{hj}$ are the special product model $R_h=\prod_j S_{hj}$; their separate marginals do not determine a general joint relation. A completely unconstrained hypothesis uses the full product. An empty proposed relation is an inconsistent model hypothesis and fails admission, rather than contributing a possible state.

These are supplied model constraints, not laws inferred from a disease name. Hard elimination is appropriate only when the hypothesis actually makes a hard prediction at that context and resolution. An experimental mean or noisy estimate does not automatically define such a constraint. Real assay bins, uncertainties and admissibility require separate validation; the literature matrix above does not yet supply them. Unreported joint constraints must not be invented.

Retain an ordered evidence record, including repeated source occurrences and missingness reasons. Let $O$ be its observed-value records $(j,v)$, with $v\in V_j$. Each coordinate denotes one fixed result at its declared context and measurement occurrence. Repeating the same value at that coordinate is idempotent for filtering, while the extra evidence occurrence is retained. Different exact values at that same fixed coordinate have no common completion; preserve both records and report the contradiction. A genuine new replicate, time or stimulus needs its own declared coordinate or validated observation model. A variable repeated measurement is not silently treated as the same fixed result.

The full joint completion object and its hypothesis projection are
$$
W(O)=\{(h,t):h\in H,\ t\in R_h,\ t_j=v
       \text{ for every observed record }(j,v)\in O\},
\qquad
F(O)=\pi_H W(O).
$$
A missing value adds no constraint. With no observations the hypothesis fiber is all of $H$, since every admitted $R_h$ is nonempty. The output records NONE, ONE or MANY **within this catalogue**, together with an open-world flag stating that unlisted or mixed mechanisms remain unresolved. A singleton catalogue fiber is not a unique biological diagnosis. An empty catalogue fiber requests review or a new carrier; it does not establish absence of a biological explanation.

Retain $W(O)$, or equivalently the original joint relations and the entire observation record. The hypothesis names $F(O)$ alone do not retain the conditional assay alternatives. A next observation filters $W(O)$; requested joint assay answers are projections of that same object, not Cartesian products of separate marginal answers.

Let $A(O)\subseteq J$ contain exactly the available, budget-admitted coordinates whose fixed result is not already observed. If $F(O)$ is empty, return contradiction/model review. If $A(O)$ is empty, return NO_AVAILABLE_ACTION. Otherwise an outcome $v$ at a candidate coordinate $j$ would leave
$$
F_{j,v}(O)=\{h:\exists t,\ (h,t)\in W(O),\ t_j=v\},
\qquad
w_j(O)=\max_{v\in V_j}|F_{j,v}(O)|.
$$
The finite nonempty alphabets make these maxima defined. Select the smallest score; among equal scores prefer lower declared assay cost. Preserve all ties after these comparisons and use a fixed order only for presentation. Outcome buckets can overlap when hypotheses allow several values. No probability is inferred from the number of compatible hypotheses.

Only a best score strictly below $|F(O)|$ gives a guaranteed one-step reduction of hypothesis count. Otherwise return NO_GUARANTEED_REDUCTION for this objective, retaining the scored alternatives for inspection. This does not establish that no multi-assay plan or other objective could be useful. In particular, a singleton hypothesis can still allow several assay outcomes.

**Elementary guarantee.** For every outcome admitted by the current joint model, the updated hypothesis fiber has size at most the selected assay's worst bucket size, by its definition. Complete enumeration over a nonempty finite candidate-assay set attains the smallest such one-step worst-case size among those assays. An observed alphabet value with no joint completion instead gives NONE and model review. The guarantee proves a finite supplied-model property, not assay efficacy in biological material.

## Complete synthetic demonstration

The following closed model has three abstract states and two deterministic binary assays. These symbols are not assigned to NFKB1, CTLA4 or any measured immune record.

| State | Broad label | Assay $u$ | Assay $v$     |
|---|---|---:|---:|
| $\alpha$ | L | 0 | 1   |
| $\beta$ | L | 1 | 0   |
| $\gamma$ | L | 0 | 0   |

With label L alone the fiber is $\{\alpha,\beta,\gamma\}$. All first-assay outcomes are explicit: $u=0$ leaves $\{\alpha,\gamma\}$, $u=1$ leaves $\{\beta\}$; $v=0$ leaves $\{\beta,\gamma\}$, and $v=1$ leaves $\{\alpha\}$. At equal assay costs both first choices tie with worst remaining size two.

After $u=0$, observing $v=1$ yields $\{\alpha\}$, whereas $v=0$ yields $\{\gamma\}$. An unavailable $v$ leaves both alternatives. Repeating deterministic $u$ supplies no further distinction; observing $v$ has worst remaining size one. The complete joint outcome table is $00\mapsto\{\gamma\}$, $01\mapsto\{\alpha\}$, $10\mapsto\{\beta\}$, $11\mapsto\varnothing$.

Both marginal outcome sets are $\{0,1\}$. Their Cartesian product contains the impossible pair 11. Thus retaining marginal possibilities alone loses a joint constraint. In this synthetic carrier that is a fully demonstrated failure; it is not evidence that these binary signatures occur in immune biology.

A second abstract model exposes correlations within a set-valued hypothesis and the limit of a one-step selection rule:

| Hypothesis | Complete allowed $(u,v)$ tuples   |
|---|---|
| $a$ | $\{00,11\}$     |
| $b$ | $\{01,10\}$     |

Each hypothesis separately has marginal allowed sets $\{0,1\}$ for both assays. A product of those marginals would falsely allow 01 for $a$ and 00 for $b$. Joint filtering instead gives $00,11\mapsto\{a\}$ and $01,10\mapsto\{b\}$, with the displayed tuples retained as the complete joint states.

Initially either single assay has worst remaining hypothesis count two, so this one-step rule reports NO_GUARANTEED_REDUCTION. After $u=0$, however, the retained joint states are exactly $(a,00)$ and $(b,01)$: observing $v=0$ selects $a$, and $v=1$ selects $b$. After $u=1$, the states are $(a,11)$ and $(b,10)$, so $v=1$ selects $a$ and $v=0$ selects $b$. A two-assay plan therefore identifies the hypothesis even though neither first assay guarantees immediate shrinkage. Such a plan is outside the stated one-step selector's guarantee.

## Algorithm, endpoints and rejection criteria

~~~text
validate every source assertion, context, missingness state, and dependency
select the question; exclude its target block and all derived target copies
admit finite nonempty outcome alphabets and joint hypothesis relations
W := every admitted (hypothesis, joint outcome tuple)
retain the entire ordered evidence record
for each supplied observation:
    if missing: retain W unchanged and record the missing reason
    otherwise: validate its fixed coordinate and outcome alphabet
        filter W to tuples matching that coordinate value
F := the hypothesis projection of W
report W, F, catalogue disposition, and unresolved/open-world status
if F is empty:
    preserve all conflicting records; return contradiction/model review
A := available, budget-admitted coordinates not already observed
if A is empty: return NO_AVAILABLE_ACTION with the evidence result
for each coordinate in A:
    enumerate each outcome's hypothesis projection from the current W
    record worst remaining size and declared assay cost
if the best worst-case size is not smaller than |F|:
    return NO_GUARANTEED_REDUCTION with all scored alternatives
otherwise:
    retain minimum-score choices, then minimum-cost ties
    return the complete evidence result and those separating assays
~~~

The immediate structural endpoints are exact agreement with independent exhaustive enumeration on supplied finite carriers, correct handling of the empty-observation block, preservation of joint constraints, and zero instances of converting missing evidence into normal results. Such implementation checks have not been executed here; the displayed toy is an analytic specification.

Quantitative evaluation requires a new frozen data manifest. Entire studies, experimental batches and related constructs must be kept in declared groups. With one paper per named mechanism, study identity and mechanism are confounded: a random split of extracted statements cannot establish transfer. Leave-one-study-out evaluation becomes meaningful only when independent studies supply adequate overlapping assays and targets. Any later authorized human-derived benchmark would additionally need its actual relatedness and site structure respected; aggregate papers cannot supply that information.

For a continuous withheld assay, use held-out MAE with source units and uncertainty. For validated discrete assay outcomes, evaluate prediction-set coverage and size, abstention rate, and calibration only if probabilities are actually fitted. Compare assay-acquisition cost at matched coverage, counting representation construction and reopening. Mechanism names are not automatically ground-truth class labels. All margins, units, exclusion rules and uncertainty procedures must be frozen before evaluation.

Ablations remove joint constraints, stimulus/context, assay denominators or explicit missingness one at a time. Compare random, greedy and exact finite assay selection with equal candidate assays and costs. Include antibody-only and EUROclass baselines only on their admitted inputs. Source-label prediction and target-derived annotations are deliberate leakage controls, never scientific competitors.

Reject the added-value claim if an ordinary matched method produces the same coverage/cost result, if supposed unique answers rely on missing-as-normal filling, or if benefit disappears under study separation. A contradiction of a hard model constraint reopens that hypothesis and context; it does not refute an entire disease category. Unresolved alternatives must remain visible rather than being scored as confident errors against invented mechanism labels.

## Separate availability and execution gates

**Input-availability gate:** the primary studies support the literature matrix. They do not currently provide this pack with a validated, appropriately reusable joint quantitative benchmark. The 2024 cohort states that datasets are available upon request; that statement is not public numerical access or permission to redistribute records. [Primary data-availability statement](https://www.frontiersin.org/journals/genetics/articles/10.3389/fgene.2023.1272912/full). Cross-study assay alignment, actual independence groups, licensed input bytes and independent target measurements remain missing.

**Execution gate:** no quantitative importer, fitted model, benchmark split, calibrated threshold, measured cost or executable replay receipt exists. Numeric assay outcome constraints have not been inferred from the literature summaries. A future quantitative stage needs all of these and a frozen comparator protocol; until then its performance is unavailable.

The pack can be reviewed and shared as an unexecuted research proposal now. Its completed contribution is a specific evidence matrix and refutable inference design, with a demonstrated finite joint-information problem. Improved immune-mechanism prediction remains an open experimental question.
