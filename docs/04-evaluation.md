# 04 — Evaluation before promotion

**No application experiment has run.** Small example files are specification fixtures, not a benchmark. The corpus sizes, budgets and promotion criteria here are proposed protocol values to freeze during implementation; none are measured results.

## Research question and unit

Test whether visible linked journal context improves **case recall at a fixed human review budget** compared with transparent rules, amount ranking and a seeded random baseline. The target is review relevance under documented accounting assumptions. It is not the probability that a person committed fraud.

A journal entry consists of its posting lines. Related entries can form one case only through the architecture's permitted grouping rules. Split whole entries, reversals, connected entity groups and shared source transactions together where necessary. Never randomly split lines from the same journal between training and testing.

The evaluation unit is a case at an observation cutoff. For incident recall, count a review-relevant synthetic issue once when any correctly linked member is selected. Also report entry recall and number of entries inside reviewed cases. Group-size distribution is mandatory: merging every entry into one “case” cannot masquerade as efficient review.

## Dataset plan

Build an original synthetic corpus with a target of 30 distinct organization families, 24 fiscal months per family and approximately 120,000 entries total. These are generation targets, not contents already present. Vary charts, entity counts, periodicity, source clocks, fiscal calendars, document availability, preparer roles and legitimate close patterns. Use the same nuisance-generation distributions for relevant and routine cases wherever possible.

Create routine economic processes first: sales, purchases, payroll, accruals, reversals, corrections and intercompany examples. Then create review-relevant variations independently from data-quality faults. A balanced adjustment can be review-relevant; an unbalanced file can simply be broken data. Keep these targets separate.

The 16 supplied development cases are illustrative contracts. They are visible and must never be counted as held-out evidence. The larger corpus, independent challenge set and any accounting review do not exist yet. The plan is at least 120 independently authored or independently reviewed held-out case scenarios across all required families, in addition to the generated scale corpus.

Synthetic issue prevalence is controlled by the generator. Evaluate several declared prevalences, for example 0.1%, 0.5% and 2% of cases, while preserving realistic hard negatives. These values are stress-test assumptions, not estimates of real-world fraud frequency. Report prevalence beside every precision figure.

## Labels and provenance

Use separate fields and files for:

| Label type | Meaning | Permitted claim |
|---|---|---|
| `injected_review_issue` | Generator inserted a documented pattern | Detection of that synthetic pattern |
| `expert_review_relevance` | Qualified independent reviewer judged follow-up appropriate | Agreement with that review judgment |
| `confirmed_finding` | Authorized real-world finding with documented adjudication | Performance on that limited real dataset |
| `unresolved` | Evidence or reviewers do not establish a stable target | Coverage limitation; not a negative label |

Every label includes case/entity scope, author or role pseudonym, creation time, evidence references, confidence rationale, adjudication status and version. The source records alone never contain those label fields. An alert clicked by a reviewer is not a confirmed finding. A reviewer deciding “no further work” may reflect limited scope, not an established clean bill of health.

Each label also has `available_at`: the first time the training/evaluation owner could know its adjudicated outcome. Any supervised fitting, calibration, threshold selection, hybrid-weight choice or future policy optimization may consume only labels available by that stage's declared fit/selection cutoff. Event time is not label-availability time. Labels resolved afterward stay unknown for that historical fit. Preserve the label version used. Freeze all selected choices before scoring the held-out set. An unsupervised detector does not avoid leakage if its configuration is selected using future labeled outcomes.

An independent custodian owns held-out labels. For the review-relevance challenge set, two qualified reviewers should assess cases without seeing algorithm ranking. Resolve disagreements explicitly, report agreement and retain unresolved cases. If this professional review is not available, label the release synthetic-only and do not claim expert validation.

## Splits and observation times

1. Group related legal entities, shared source documents, reversal chains and near-duplicate generator lineages before splitting.
2. Allocate 18 organization families to development, 6 to validation and 6 to completely unseen-organization testing. Freeze the membership and seed in a manifest; any materially connected family stays together.
3. Within the 18 development families, use months 1–12 for fitting, months 13–16 for validation of temporal behavior, and months 17–24 for a **separate forward-time test**. Do not combine this with unseen-organization results in one score.
4. Use only observations through the common end-of-study-month-16 cutoff from the 6 validation families to select algorithm configuration and thresholds. Include only outcome labels adjudicated and available by that cutoff. Do not use their later months to tune a model evaluated on development-family months 17–24. Freeze configuration before study month 17; any refit must consume only data/labels allowed by its declared earlier cutoff.
5. Run months 17–24 of the 6 unseen-organization test families with the same frozen population model. Their earlier visible records may support causal features under a documented warm-up rule, but must not fit the already frozen model. Also report a cold-start track that abstains when history is insufficient.
6. Reserve whole pattern variants and generator templates for independent challenge scenarios; a new random seed on the same template is not sufficient evidence of novel-pattern generalization.
7. At each scoring cutoff, mask future reversals, later documents, revised relationships and reviewer outcomes. Evidence availability—not backdated economic date—controls visibility.

Study months use one declared shared UTC observation calendar; entity fiscal calendars remain separate accounting context. The fitting cutoff is the end of study month 12, and model/configuration selection closes at the end of study month 16. Later adjudications remain unknown for those historical operations. The exact family allocation may change only before the protocol is frozen. If a test bug requires reopening the evaluation, record the correction and call the original set consumed. A new confirmatory claim needs new unseen data or a clearly labeled non-confirmatory rerun.

## Comparable systems

All methods receive the same canonical records, as-of cutoff, case universe, grouping policy and quality/context routing. Compare:

- **B0:** seeded random ordering, repeated with declared seeds;
- **B1:** documented gross-debit magnitude ordering;
- **B2:** transparent rule-family ordering;
- **C1:** simple anomaly model with frozen features;
- **C2:** hybrid rule/model ranking;
- **Ablation:** C2 without linked reversal/counterpart context;
- **Ablation:** C2 without time-availability safeguards, only as a clearly labeled diagnostic demonstrating why an invalid design is misleading, never as a competitive result.

The last diagnostic cannot use real private data to circumvent access boundaries and cannot be advertised as a valid model. Prefer a synthetic leakage canary with an intentionally forbidden future field. It should make the evaluation fail, not become a deployable option.

Train once per frozen split/seed and preserve artifacts. Use three declared training seeds for stochastic candidate stability; compare case-matched outputs. Do not search for the best test seed. Version all preprocessing and choose hybrid weights on validation only. The external dataset branch is optional and reported separately after license/provenance verification.

## Metrics and denominators

Let N be every prediction-eligible case in an organization-period cohort, including cases whose outcome labels are unresolved or absent. Form and rank this population before joining labels. Let P be the number with resolved adjudicated review-relevant labels. Set K = floor(budget_fraction × N), allowing K = 0. Report budgets of 1%, 5% and 10%, absolute K, effective K/N and the number of underlying entries. An unknown-label case still consumes a selected review slot. Never filter unknowns out of the ranking population. A separately named minimum-one-review exploratory policy may be shown with its actual effective budget, but cannot satisfy the primary 5% promotion gate. Exact ties use the frozen deterministic case-ID tie break; disclose the tie frequency.

- **Recall@K:** labeled relevant cases selected in the top K / P. If P = 0, report not applicable, not 100%. If K = 0 and P > 0, recall is zero; precision is not applicable because nothing was reviewed. Recall concerns resolved labeled positives; report label coverage because unseen positive outcomes remain unknown.
- **Precision@K:** labeled relevant selected cases / number of selected cases with resolved labels. If no selected case has a resolved label, resolved precision is not applicable. Also report the resolved-label coverage of the selected K and a conservative lower bound treating unresolved selected cases as non-positive. Do not hide unresolved reviews by shrinking the denominator silently.
- **Average precision:** compute on the fully resolved eligible subset only and report the subset's size and prevalence. Do not rename average precision as an arbitrary trapezoidal PR-AUC.
- **End-to-end recall:** relevant issues reached for review / all labeled relevant issues in the admitted population, including issues lost to supported processing failure or abstention. Report exclusions explicitly. Unsupported source classes outside declared scope have a separate count, not an invisible deletion.
- **Hard-negative burden:** legitimate cases selected / legitimate cases available, separately for recurring reversals, approved late postings, migrations, installments and new entities.
- **Coverage:** scored, context-missing, quarantined, unsupported and failed counts over all submitted cases, with a reconciliation table.
- **Explanation validity:** fraction of asserted source references/operands that resolve, are authorized, were available and match the actual calculation. Report incorrect assertions separately; fluency is not a metric.
- **Workload:** case count, underlying entry count and, if actually measured by blinded reviewers, minutes per case and actionable follow-ups per hour.

Amount-weighted recall may be included as a secondary descriptive measure with an explicitly defined journal magnitude and deduplicated issue amount. It is not loss prevented, cash saved or audit materiality. Reversals and opposite entries are not counted as separate losses. Report macro-averages per organization and micro-averages separately so one large organization cannot hide failure elsewhere.

For uncertainty, cluster-bootstrap organization families with a declared seed and 2,000 resamples. Preserve linked incidents within clusters. With only six unseen families, intervals will be unstable; report this limitation and the per-family results. Do not interpret a narrow synthetic interval as real-market reliability. For analyst timing, account for reviewer and case pairing; do not claim speedup from unpaired anecdotes.

## Hard tests before opening held-out results

- Replaying an earlier cutoff after adding a future reversal leaves the earlier features and output unchanged.
- Duplicating lines or replacing IDs with label-like strings cannot improve the candidate; invalid copies are blocked.
- Scaling the amounts of all positive examples is not the only signal in the data; matched routine large entries remain.
- Approved closing entries, recurring documented reversals, new entities and incomplete subsidiary coverage do not become forced fraud labels.
- A forged source text instruction cannot change authority, classification policy or report scope.
- Adding an unauthorized organization's canary cannot affect output or leak into evidence.
- Removing a cited document changes the explanation and any support-dependent rule state.
- All rows, cases and failure paths reconcile with the evaluation population.

## Promotion and honest failure

A correct **research release** requires reproducibility, required tests, transparent coverage and complete reporting. It does not require the candidate to beat the baseline. A negative result can be useful if the experiment is sound.

A provisional candidate-promotion target is at least **5 percentage points absolute improvement in Recall@5% over B2**, with a positive lower bound of the paired cluster-bootstrap difference, no more than 2 percentage points deterioration in the predeclared hard-negative selection rate, and zero known scope/availability violations. Freeze or revise this target with the domain reviewer before testing. It is a product decision threshold, not a fact inferred from a report or a guarantee of commercial value.

A real-data pilot requires independently recorded utility and acceptable workload in the intended organization. No synthetic benchmark permits a claim that the product catches fraud in real companies, meets a legal standard, replaces auditors or deserves an institutional award.
