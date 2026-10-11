# 01 — Product requirements

## Product and user

Ledger Integrity Lab is a proposed read-only accounting analytics system for a controller, internal audit analyst or independent accounting reviewer. Its job is to **prioritize records and evidence for a human to investigate**, including concerns that survive ordinary debit/credit and invoice/payment reconciliation. It does not replace an audit, establish wrongdoing or determine an employee's character.

The initial deliverable is a local reproducible research application. The future customer hypothesis is an internal review team or accounting firm whose existing journal-entry tests produce more items than it can investigate. Access to an authorized ledger export and a qualified reviewer is a prerequisite for a useful pilot; neither is claimed today.

## Release boundaries

| Release | Supported scope | Exit boundary |
|---|---|---|
| R0 — this handoff | Requirements, contracts, original small cases, documentation tooling | No implemented detector or benchmark |
| R1 — research application | Offline structured GL exports, functional-currency entries, synthetic evidence, local review packets, comparable baselines | Reproducible study; no real-money actions |
| R2 — supervised pilot | One authorized organization's selected periods/entities, approved data handling, qualified reviewers | Real evidence of review usefulness; not an audit opinion |
| R3 — later product | Repeated customer value, connectors and operational controls | Separately scoped; no implementation estimate promised here |

R1 accepts ordinary journals and separately tagged consolidation/reporting adjustments. The field `entry_kind` preserves their distinction. Exports may omit off-ledger adjustments or inaccessible subsidiaries; show those blind spots rather than a “complete books checked” badge. The input scope declares which records and entities are present. A complete export is an input assertion to reconcile, not proof that no undisclosed records exist.

## Concrete workflow

1. An analyst selects one organization and authorized engagement and imports a structured export plus an account mapping.
2. The system records provenance and checks file shape, identity, totals, currencies and debit/credit balance. Integrity failures enter a separate quality queue.
3. The analyst selects an observation time. The system exposes only records available by that time, while using entity-specific fiscal dates for accounting-period logic.
4. Deterministic signals produce traceable review cases; the optional model changes their priority only within its documented scope.
5. The reviewer inspects the source entries, associated documents, policy evidence and missing context. A case asks a specific review question rather than accusing a person.
6. The reviewer records an unresolved, explained or follow-up finding. New information creates a version, not a rewritten historical report.
7. The experiment harness computes held-out measures with labels and future evidence unavailable to the ranker.

## Signals and deliberate counterexamples

| Signal family | Reason to review | Essential counterexample |
|---|---|---|
| Period-end revenue adjustment | Manual adjustment near close with required support absent in available records | Documented legitimate recognized revenue |
| Reversal context | A linked reversal changes the understanding of a previously unsupported adjustment | Recurring accrual with approved reversal schedule |
| Close/approval exception | Observed entry after close lacks the permission required by the configured policy | Authorized reopen/late-post process |
| Related-entity gap | Explicit expected counterpart is absent from a complete, comparable scoped feed | Counterpart outside coverage or arriving within a permitted delay |
| Repeated small adjustments | Linked entries collectively merit review against the agreed policy | Legitimate installments or recurring charges |
| Novel account/preparer context | Unusual combination relative to permitted history | New entity, new hire, system migration or seasonal work |

Rules encode a chosen review policy, not a universal legal definition. Thresholds and classifications are versioned engagement configuration. Identity and demographic attributes are not fraud predictors in R1. User IDs can establish authorized role and historical workflow context; output must not turn that into person-level guilt scoring.

## State model and terminology

- **data_quality:** the submitted records fail an integrity condition or cannot support the expected operation. No accounting conclusion follows.
- **context_missing:** the operation is potentially relevant but coverage, time history or source evidence is insufficient to assess it.
- **needs_review:** the recorded evidence matches a documented review criterion.
- **reviewed_explained:** a human recorded an explanation and supporting evidence.
- **reviewed_follow_up:** the reviewer requests further work; the case remains unresolved.
- **superseded:** a newer version exists; the old version is still inspectable.

A classifier label called “fraud” is prohibited for the original fixtures. Their intended labels are `review_relevant`, `routine`, `undetermined` or `input_invalid`. A later authorized real-world study may contain confirmed findings only with recorded provenance and a qualified process. The system still does not issue legal verdicts.

## Invariants

Amounts are integers within a documented currency exponent. A v1 entry has one functional currency and all its lines share that entry currency; transaction-currency translations are unsupported and must be explicitly transformed with an audited mapping first. Never net USD debits against INR credits. An entry is balanced only when its exact debit sum equals its exact credit sum; matching balance does not imply truthful business substance.

An organization is the security boundary; a legal entity is an accounting scope within it. Linking entries across legal entities requires their explicit inclusion in the engagement. The same apparent customer or bank identifier in another organization grants no access.

`effective_date`, `recorded_at` and `available_at` have different meanings. Earlier economic dates do not establish earlier information availability. The latest required availability timestamp controls feature visibility. Related-party declarations, approvals and calendar changes are versioned evidence too.

## Functional contracts

The complete machine-readable list is [requirements.csv](../planning/requirements.csv). Each requirement must map to at least one planned acceptance test. Internal implementation tracking is maintained separately.

### LI-001 — Authorized immutable import

Record organization, engagement, source hash, extract time, mapping version and permitted purpose; keep source bytes unchanged.

### LI-002 — Exact money and currency

Use integer minor units and an explicit currency exponent; prohibit binary floating-point arithmetic for balance and amount comparisons.

### LI-003 — Double-entry and completeness checks

Check each entry balances in its supported functional currency; reconcile available row/entry/control totals and report absent completeness evidence.

### LI-004 — Idempotent ingestion

Same source identity and hash yields no extra records; same identity with changed bytes is an integrity conflict.

### LI-005 — Organization and engagement scope

Reject cross-organization evidence references; authorize each legal entity within the active engagement.

### LI-006 — As-of-time visibility

Use only entries, evidence, approvals and relationships available at the observation cutoff; retain effective date separately.

### LI-007 — Fiscal periods and late posting

Version the entity calendar and close/reopen events; evaluate late posting with permission evidence known at the cutoff.

### LI-008 — Chart mapping and provenance

Version account classification, preserve source account code and quarantine unknown mappings instead of inventing classes.

### LI-009 — Period-end support gaps

Identify configured manual revenue adjustments near period end lacking required available support, with exact evidence gaps.

### LI-010 — Reversal context

Link explicit reversal references and distinguish documented recurring accrual reversal from unexplained change after closing.

### LI-011 — Control exceptions

Compare entry and approval records with a versioned policy; distinguish missing feed, missing approval and observed policy breach.

### LI-012 — Related-entity context

Evaluate expected counterpart entries only when relevant entity, time and currency coverage are explicit; otherwise abstain.

### LI-013 — Aggregated patterns

Group linked repeated/manual adjustments using predeclared windows and keys; do not label legitimate installment patterns as proven evasion.

### LI-014 — Historical feature generation

Compute prior-account frequency, preparer-account novelty and amount context using only permitted past records and training transformations.

### LI-015 — Transparent rule baseline

Produce deterministic versioned rule reasons, grouped candidates and stable review ordering.

### LI-016 — Simple ranking controls

Implement amount-only and seeded random ranking using the same eligible candidate population and review budget.

### LI-017 — Unsupervised candidate

Evaluate a frozen Isolation Forest candidate with documented scoring orientation and missing-value handling; scores are not fraud probabilities.

### LI-018 — Hybrid candidate and ablations

Combine rules/context with a frozen candidate ranker; report rules-only, model-only and context-removed comparisons.

### LI-019 — Grouped review queue

Deduplicate a connected case before budget allocation; preserve entry-level findings without double counting case recall.

### LI-020 — Faithful evidence packets

Show exact rule operands, source IDs, hashes, availability times, missing context and a neutral review question.

### LI-021 — Human adjudication

Store reviewer finding, rationale, evidence and revision separately from input features; unresolved cases stay unresolved.

### LI-022 — Label provenance

Separate synthetic injected issue labels, expert review relevance and confirmed real findings; never conflate them.

### LI-023 — Entity and time holdout

Separate connected group identities and generator seeds; freeze development, validation and forward/unknown-entity test views.

### LI-024 — Review-budget metrics

Measure case recall/precision at fixed K, entry diagnostics, coverage, hard-negative burden and group uncertainty.

### LI-025 — Independent hard negatives

Include legitimate closing/reversal/small-entity workflows and an independent case author; keep outcomes outside runtime inputs.

### LI-026 — Reproducible experiment manifest

Record hashes, code/config/dependency versions, seeds, feature cutoff, split and metric definitions; preserve failed runs.

### LI-027 — Untrusted source text

Treat document text as data; template outputs escape text; embedded instructions cannot alter scores, access or reviewers.

### LI-028 — Private storage and export

Keep raw exports, identity maps, trained artifacts and held-out labels outside a public release; verify logs and exports.

### LI-029 — Resource bounds and determinism

Measure ingestion/scoring memory/time on declared hardware, enforce file/row limits and produce stable repeated outputs.

### LI-030 — Neutral states and no automatic actions

Use needs_review, context_missing or data_quality labels; no fraud verdicts, ledger writes or autonomous enforcement.

### LI-031 — Research evidence release

Publish only observed results with reproducible code and limitations; a blueprint is not a detector or institutional certification.

### LI-032 — Qualified supervised pilot gate

Require authorized data use, accountant review, security review, explicit retention and human-owned outcomes before real use.

### LI-033 — External data provenance

Verify exact dataset version, license, hashes, unit, label provenance and temporal semantics before optional benchmark use.

### LI-034 — Language and component discipline

Use Python and SQL first; introduce Go/Rust only through a measured architecture decision and contract parity checks.

### LI-035 — Abstention and failed runs

Record insufficient history, unverified coverage, unsupported inputs and runtime failures explicitly; do not silently drop cases.

### LI-036 — Correction and challenge trail

Allow reviewed corrections to source mappings/findings; append versions and reproduce the prior report without overwriting evidence.

## Explicit exclusions

R1 does not write journals, update vendors, reverse entries, report allegations externally, restrict a person's access, automatically refuse a transaction, value securities, certify statements or establish statutory materiality. It does not infer hidden related parties from private communications or scrape employee activity. It does not promise to find every fraud or use digit distributions as proof of manipulation.

Large-language-model summaries are optional future presentation experiments, not required for R1 and not part of the ranking or accounting authority. The initial faithful explanation is a deterministic template with explicit source fields.
