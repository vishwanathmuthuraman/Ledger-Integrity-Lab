# 06 — Sources and design rationale

Research checked **11 October 2026**. The sources below are primary standards, first-party documentation, original research or an institutional publication record. They motivate the problem and establish related work. They do not endorse this project. Standards applicability depends on engagement, jurisdiction and reporting period.

## The evidence chain

The source base supports studying accounting review and the difficulty of evaluating anomaly detection. The engineering design is our proposed response: deterministic accounting checks, evidence-linked review, explicit information cutoffs and independent evaluation. It is not a claim that a source recommends this exact implementation.

### S01 — AS 2401: Consideration of Fraud in a Financial Statement Audit

[PCAOB](https://pcaobus.org/oversight/standards/auditing-standards/details/AS2401) · Current standard page checked 2026-10-11

Paragraphs .05, .11, .57-.62 distinguish potential concerns from legal findings and address journal entries, adjustments and management override.

**Scope:** Supports journal-review scope and cautious language; does not certify this software or establish universal rules.

### S02 — ISA 240 (Revised)

[IAASB](https://www.iaasb.org/publications/isa-240-revised-auditor-s-responsibilities-relating-fraud-audit-financial-statements) · 2025-07-08

The revised standard strengthens fraud-related auditor responsibilities and applies to financial statement periods beginning on or after 2026-12-15.

**Scope:** Verify local adoption and applicable period with a qualified reviewer; the blueprint is not a compliance opinion.

### S03 — AS 2410: Related Parties

[PCAOB](https://pcaobus.org/oversight/standards/auditing-standards/details/AS2410) · Current standard page checked 2026-10-11

The standard addresses identifying and assessing related-party relationships and transactions and responding to related risks.

**Scope:** Motivates explicit entity relationships and evidence gaps; shared identifiers alone do not prove a related party.

### S04 — Key Findings from Occupational Fraud 2026: A Report to the Nations

[ACFE](https://cms.acfe.com/acfe-insights-blog/blog-detail?s=key-findings-report-to-the-nations-2026) · 2026-05

The study covers 2,402 investigated occupational-fraud cases across 143 countries/territories. Financial statement fraud appears in 6% of cases and has a $1 million median loss within that category.

**Scope:** Selected investigated cases are not a representative prevalence estimate, product TAM, or projected savings.

### S05 — Generating synthetic journal entries for audit analytics: Method and dataset

[Gronewald et al. / Data in Brief](https://pmc.ncbi.nlm.nih.gov/articles/PMC13599566/) · 2026

The paper describes a labeled synthetic general ledger covering two fiscal years of a fictional business, using double-entry postings and injected problematic entries; it links a Zenodo dataset.

**Scope:** An external benchmark candidate only; no dataset was downloaded or redistributed. Original record and license must be verified before use.

### S06 — Publication record: Generating Synthetic Journal Entries for Audit Analytics

[DFKI](https://www.dfki.de/web/forschung/projekte-publikationen/publikation/17692) · 2026

The authors institutional record identifies the work as Data in Brief volume 69 (2026) and describes synthetic patterns and probabilistic generation.

**Scope:** Corroborates provenance; not independent validation of real-world generalization.

### S07 — Anomaly Detection in General Ledger Data: Results from a Hybrid Approach

[Gronewald et al.](https://arxiv.org/abs/2609.18228) · 2026-09-16 arXiv submission; page says presented at a 2024 conference

The research-in-progress paper studies combining journal entry tests with machine learning on synthetic normal and anomalous entries.

**Scope:** Direct related work; hybrid rules plus models is not a novelty claim for this project.

### S08 — Detection of Anomalies in Large Scale Accounting Data using Deep Autoencoder Networks

[Schreyer et al.](https://arxiv.org/abs/1709.05254) · 2017; revised 2018

The paper proposes an autoencoder-based anomaly assessment for journal entries and reports experiments on two real accounting datasets.

**Scope:** Alternative method for literature comparison; this handoff does not claim access to those datasets or reuse their performance.

### S09 — Leakage and the Reproducibility Crisis in ML-based Science

[Kapoor and Narayanan](https://arxiv.org/abs/2207.07048) · 2022; version history on source

The paper documents data leakage as a source of unreproducible machine-learning scientific findings.

**Scope:** Motivates auditable split and feature-availability tests; the specific split protocol here is a project design.

### S10 — Common pitfalls and recommended practices

[scikit-learn](https://scikit-learn.org/stable/common_pitfalls.html) · Current documentation checked 2026-10-11

The documentation describes data leakage and recommends fitting preprocessing only on training subsets, with pipelines helping enforce boundaries.

**Scope:** Pin application library versions when implementing; current documentation is not a tested dependency lockfile.

### S11 — IsolationForest

[scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html) · Current documentation checked 2026-10-11

The estimator offers unsupervised anomaly scoring; its score direction and offset need to be interpreted consistently.

**Scope:** Candidate algorithm, not a calibrated fraud probability. Freeze score orientation and preprocessing in tests.

### S12 — Metrics and scoring

[scikit-learn](https://scikit-learn.org/stable/modules/model_evaluation.html) · Current documentation checked 2026-10-11

The documentation defines ranking/classification measures including precision-recall and average precision.

**Scope:** Use exact named metric definitions; review-budget recall, coverage and case deduplication require project-specific definitions.

## Originality and research position

Journal-entry anomaly detection, rules, autoencoders and hybrid systems already have substantial prior work. A credible contribution would be an independently reproducible study of **time-correct linked evidence and constrained review budgets**, including difficult legitimate cases, missing context, alert grouping and source-faithful explanations. Whether that contribution is new enough for a research venue remains a literature-review question. Do not label it novel before the study and full comparison exist.

The original fixtures in this folder are deliberately small, hand-authored specifications. They are not copied from a real company, the papers, or their linked datasets. Their numerical amounts and identifiers carry no observed business meaning.

## External dataset intake contract

One promising optional benchmark is the synthetic GL dataset linked by S05 at [Zenodo DOI](https://doi.org/10.5281/zenodo.22014653). Direct record access failed during this research pass. Therefore its exact file hashes, current version, reuse permissions and label definitions remain **unverified**, and no external dataset files are included.

Before enabling that benchmark, record the resolved immutable version URL, creators, license text/reference, checksum of each file, target definitions, posting-group key, dates covered, any labeling limitations and whether generator metadata leaks labels. Keep raw downloads local. Treat it as a separate benchmark domain with its own results; do not mix it into the original corpus and claim independent generalization.

A synthetic dataset may reproduce the author's generation rules more than real accounting behavior. A high score cannot establish real fraud detection, prevalence, savings or audit assurance. Third-party paper results never become our results through citation.

The structured [source register](../research/source-register.json) records exact claim boundaries and the unverified dataset candidate.
