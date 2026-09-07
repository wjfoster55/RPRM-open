# BRCA1 cellular function: a receiver-specific representation experiment

**Status: experimental proposal, unexecuted.** This pack specifies an experiment and gives a complete synthetic arithmetic example. No assay dataset or model checkpoint has been downloaded, no importer or predictor has been run, and no biomedical improvement is reported. The endpoint is a published cellular assay of BRCA1 variants. Cancer relevance motivates the question; tumor response, treatment choice and individual cancer risk are outside this experiment.

## Question and source-supported starting point

Can a smaller, explicitly audited representation retain useful information about BRCA1 cellular function when a protein-only description merges nucleotide changes with different consequences? There are two separate questions: whether a finite representation merges different supplied assay scores, and whether a model using that representation predicts unseen scores. Success at the first does not imply success at the second.

Findlay and colleagues measured 3,893 single-nucleotide variants across 13 BRCA1 exons encoding the RING and BRCT domains using saturation genome editing in a HAP1 cellular setting. The study includes cellular-function and RNA-abundance measurements. These provide distinct experimental readouts with which to investigate nucleotide effects and protein-level consequences. The measured function score is not a direct measurement of protein thermodynamic stability. [Findlay et al., Nature (2018)](https://www.nature.com/articles/s41586-018-0461-z).

The authors' GEO record lists a processed supplementary spreadsheet and links raw sequencing data. That is an identified acquisition route, not a validated local dataset: the spreadsheet's columns, exclusions, reuse terms and exact bytes have not been checked here. [GEO GSE117159](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE117159).

## Separate the targets before forming features

The primary task, **F-sequence**, predicts the published cellular-function score $Y_F$ from sequence and annotation inputs. A secondary task, **R-sequence**, predicts the published RNA-expression score $Y_R$ from those inputs. Each has its own eligible rows, fitted model and evaluation. Missing RNA scores do not become zeros or inferred normal values.

The source's Figure 4 excludes exon 18 from RNA measurements. The RNA task
therefore cannot inherit the complete function-score population or its
evaluation folds without its own eligibility check. [Findlay et al., primary
study figures](https://pubmed.ncbi.nlm.nih.gov/30209399/)

An optional **F-with-RNA** task would predict $Y_F$ after an RNA measurement is supplied. It is an assay-augmented task with additional experimental input, and must be compared with ordinary models receiving that same measurement. It is unavailable under the current pack. Before opening it, the measurement lineage must establish an independent predictor/target construction: overlapping raw count normalization or shared experimental noise must not create a shortcut. An independently measured RNA assay or adequately justified independent replicate construction would be required. RNA measurements and every feature derived from them are forbidden inputs to R-sequence.

The preprocessing manifest must preserve a dependency graph for each derived column. Target scores, target-derived classes, post-selection annotations and descendants of target measurements are excluded from predictor features. Clinical labels are unnecessary for these tasks and are not imported.

## Proposed input contract

The following is the proposed internal schema, not a claim about the deposited spreadsheet's column names. An eventual importer must publish a checked source-column mapping.

| Record block | Required fields and purpose |
|---|---|
| Variant identity | Genome assembly, chromosome, position, reference and alternate allele; transcript accession and version; validated transcript coordinate. Used for joins and grouping, never as a unique-record predictor. |
| Molecular context | Exon, consequence class, reference/alternate amino acid where applicable, residue coordinate, RING/BRCT context, distance to the relevant splice boundary, and a reference-sequence window. |
| Assay context | Cell system, experimental condition, readout definition, scale and sign, measurement time, replicate grouping, source quality status and the authors' stated exclusions. |
| Target table | Separate $Y_F$ and $Y_R$ values, reported uncertainty or replicate dispersion where available, and upstream measurement dependencies. Missing targets remain absent.     |
| Annotation availability | For every proposed input: observed, not measured, unavailable annotation, failed validation or not applicable. These states remain distinguishable. |
| Source binding | Source URL/version, acquired-file hash, row locator and transformation history. Retained for audit and reopening; excluded from biological predictors. |

Resolve reference-allele and transcript mismatches before admission. Do not silently translate coordinates between transcript versions. Keep all measurements of a variant together. An uncertainty field absent from the source is marked absent, not manufactured from the pooled variant distribution.

The admitted carrier $X$ is the finite, frozen set of imported variant records passing the independently specified source filters for one task. It is neither all BRCA1 sequence space nor all variants encountered in tumors. An empty eligible scored carrier makes that task unavailable; it is not a successful zero-error experiment.

## Feature maps and the proposed RPRM contribution

A fixed coarse base representation $C_0$ records consequence class, reference/alternate amino acid when applicable, domain and a 20-residue position bin. Noncoding changes have a typed not-applicable protein coordinate. A protein-only baseline is compared on its admitted missense subset; performance on splice or noncoding variants is reported separately.

Four additional groups form a finite candidate family:

1. Reference/alternate nucleotide identity.
2. Splice-distance class: boundary positions 1–2, positions 3–8, more distant, or not applicable, with side and annotation-missing states retained.
3. A 21-nucleotide reference window centered on the variant, represented by nucleotide indicators with separate boundary-padding and unknown symbols.
4. Exact residue position, or exact transcript position where no protein coordinate applies.

All annotations require validated reference inputs. Distance conventions, window orientation and bin boundaries are frozen before evaluation. Enumerating subsets gives 16 candidate augmentations of $C_0$. Exact position and long windows can nearly identify records; this is a hostile case to report, not automatic evidence of a useful representation.

The RPRM proposal is a **receiver-conditioned selection and repair rule**, not a new biological feature: retain the least costly candidate whose observed fibers meet a stated answer-loss budget, preserve the source route and separating witnesses, and return OPEN if no candidate earns admission. Compare it with conventional feature subset selection over the same 16 choices, identical inputs, decoder families and search budget. Ordinary feature engineering can use every proposed group.

The substantive hypothesis is that this rule can produce a more useful tradeoff between retained information, predictive performance and auditability. A predictive gain caused solely by adding nucleotide features is evidence for those features, not a distinct RPRM advantage. The finite fiber audit itself uses elementary mathematics; no novel general theorem is claimed.

## Exact finite audit and a complete synthetic example

For a nonempty finite scored carrier $X$, a representation $C:X\to Z$, and supplied scalar scores $Q:X\to\mathbb R$, a fiber contains every admitted record with the same representation. For each attained $z\in C(X)$, define
$$
a_z=\min_{C(x)=z}Q(x),\qquad b_z=\max_{C(x)=z}Q(x).
$$
Every decoder using only $z$ has worst error at least $(b_z-a_z)/2$ on that fiber. Indeed, any common prediction $v$ satisfies
$$
b_z-a_z\le |b_z-v|+|v-a_z|.
$$
The midpoint $(a_z+b_z)/2$ attains this bound. Consequently the minimum worst error over the entire finite carrier is
$$
L^*(C)=\tfrac12\max_{z\in C(X)}(b_z-a_z).
$$
This exact result concerns the supplied scores. It does not remove assay noise or prove generalization.

The following four records and scores are entirely synthetic, with arbitrary units and no assigned BRCA1 variant identity.

| Record | $C_0$ | Additional flag $h$ | Score $Q$       |
|---|---:|---:|---:|
| $\alpha$ | P | 0 | 0   |
| $\beta$ | P | 1 | 2   |
| $\gamma$ | Q | 0 | 5   |
| $\delta$ | Q | 0 | 5   |

The original fibers are $\{\alpha,\beta\}$ and $\{\gamma,\delta\}$. Their score sets are $\{0,2\}$ and $\{5\}$; hence $L^*(C_0)=1$, attained by predictions 1 and 5. Refinement $C_1=(C_0,h)$ gives all three fibers: $\{\alpha\}$, $\{\beta\}$, and $\{\gamma,\delta\}$. Each score is constant, so $L^*(C_1)=0$.

If a query supplies P but the flag is unavailable, its complete compatible-record set remains $\{\alpha,\beta\}$, with answer set $\{0,2\}$. Imputing flag zero and reporting score zero would erase a live alternative. A query supplying Q and flag one has no completion in this four-record carrier. It says nothing about whether such a biological state can exist.

Singleton fibers explain part of the apparent improvement. Record identifiers alone would also yield zero error. Accordingly the proposed audit reports the proportion of records in fibers containing at least two distinct variants, record multiplicities, distinct-variant cardinalities, all singleton counts and the largest collision. Replicate records of one variant do not establish cross-variant sharing. Midpoints calculated from evaluation answers are post hoc audit summaries, never fitted predictions.

## Executable procedure and evaluation design

The initial experiment uses nested leave-one-exon-out evaluation. Every variant and its replicates stay in one outer fold. Inner exon grouping selects features and hyperparameters using only the outer training portion. Report per-exon results and a separate RING/BRCT transfer stress test; neither constitutes coverage of unassayed BRCA1 regions.

A required inner or outer scored fold that is empty makes its planned outer evaluation OPEN before fitting or scoring. Within each nonempty outer training portion let $s$ be its target interquartile range. If $s$ is undefined or $s=0$, mark the normalized analysis OPEN and report the degeneracy. The proposed initial audit budget is $\varepsilon=0.25s$. At least half of eligible inner-development records must lie in fibers containing at least two distinct frozen variant identities; two replicate records of a uniquely represented variant do not qualify. If source measurements are aggregated before this audit, the source-supported aggregation rule must be declared. These are experiment design choices, not biological thresholds. A change requires a new protocol version before outer targets are inspected.

Representational cost is the number of retained categorical coordinates after the fixed encoding, including missingness symbols. Memory and elapsed computation are measured separately; coordinate count alone is not a speed claim.

~~~text
validate source mapping, coordinates, eligibility, and feature/target lineage
if the task's eligible scored carrier is empty: report unavailable and stop
freeze outer exon groups and candidate feature definitions
for each outer held-out exon:
    use remaining exons only for all development and fitting
    if any required inner or outer scored fold is empty:
        record OPEN; continue to the next outer fold
    determine scale s from this training portion
    if s is undefined or zero:
        record OPEN; continue to the next outer fold
    for each of the 16 feature subsets:
        form exact inner-development fibers using the fixed representation
        record half-range, distinct-variant coverage and separating pairs
        fit the same regularized decoder on inner-training data
        score inner-development predictions without refitting on their targets
    retain candidates satisfying the frozen fiber and coverage constraints
    if none qualify:
        record OPEN; continue to the next outer fold without a selection
    otherwise choose minimum coordinate cost, then development MAE,
        then the fixed lexicographic feature-subset order
    refit the selected decoder using outer training data only
    freeze model, selected map, preprocessing, and all comparison models
    predict outer test once; retain every prediction and exclusion
    calculate held-out metrics and a separate retrospective fiber audit
report OPEN folds and coverage before aggregation
calculate paired metrics only on common available folds and populations
any planned OPEN outer fold precludes a full-cohort retention/superiority claim
~~~

Use a training-median predictor, a regularized protein-feature model on its admitted subset, and an ordinary regularized model with all admissible sequence/context groups. Add conventional subset selection minimizing inner-validation MAE over the same candidates. Use the same regularization grid and computational budget for comparable methods. A pretrained predictor is optional only after its training overlap, target compatibility and exact version are established; none is currently selected.

Primary endpoint is held-out MAE, in assay-score units, with equal-exon aggregation alongside pooled MAE. Secondary endpoints are within-exon rank correlation, performance by consequence class, feature cost and total construction/training/query/reopening cost. A correlation undefined because of too few valid points or constant ranks is reported unavailable, not zero. Report uncertainty at the exon level; 13 source exons give limited independent groups. Precision–recall and calibration are permitted only after freezing a source-supported assay-loss threshold and a training-only probability calibration rule.

Every comparison uses paired predictions on the same eligible variants and exons. Protein-only comparisons restrict both methods to their common admitted missense subset; full-task sequence/context comparisons use their common eligible task rows. F-sequence and R-sequence retain separate target populations. Report the planned and evaluated exon/variant coverage, every OPEN fold, and exclusions for each comparison. Any planned OPEN outer fold precludes a full-cohort retention or superiority claim. Metrics on the common available folds and populations are conditional descriptive results, with that restricted coverage stated; an absent selection is never fitted or counted as a prediction.

For a nonempty common evaluated exon set $E$, let $s_e$ be exon $e$'s defined nonzero outer-training target IQR. On the same eligible rows within each exon define
$$
d_e=
\frac{\operatorname{MAE}_{\mathrm{proposal},e}
-\operatorname{MAE}_{\mathrm{baseline},e}}{s_e},
\qquad
\bar d=\frac1{|E|}\sum_{e\in E}d_e.
$$
An empty comparison population has no MAE or uncertainty bound. For a full-cohort retention-at-lower-cost claim, all planned folds must be available; require the one-sided 95% upper uncertainty bound for $\bar d$ to be below the dimensionless noninferiority margin $0.05$, and observed total resource savings to survive construction costs. The corresponding raw-score margin in fold $e$ is $0.05s_e$. For full-cohort predictive superiority, require the upper bound to be below zero. These are separate claims. Record the uncertainty method, inner-fold aggregation, regularization grid and fixed encoding before execution, and avoid treating one small dataset as definitive.

## Ablations, failure criteria and gates

Ablate nucleotide identity, splice context, sequence window and positional detail separately. Compare equal feature subsets under the RPRM and ordinary selection rules. Include a deliberately record-identifying representation as a negative generalization control and target permutation within training groups as a leakage check. Keep source/row identifiers unavailable to every scientific predictor.

The claim fails if apparent benefit vanishes with exon separation, depends on target-derived inputs, merely reproduces the all-feature baseline at higher cost, or cannot meet the fixed collision/coverage constraints. An admitted contradictory score pair refutes exact retention of the supplied scores; a physical distinction additionally requires assay uncertainty and replication. Missing observations and absent folds cannot be counted as successful predictions.

**Input-availability gate:** a public deposit is identified, but file acquisition and hashes, reuse conditions, source-column mapping, source filters, validated reference sequence/transcript mapping and uncertainty fields remain unfilled. F-with-RNA additionally lacks a validated independent input/target measurement construction.

**Execution gate:** no import, frozen split file, fitted decoder, measured timing, prediction table or independent replay receipt exists. Execution requires those artifacts and a pre-evaluation manifest binding endpoints, thresholds, software and exclusions. The protocol and exact synthetic calculation are complete enough to review now. The scientific added-value claim remains untested.
