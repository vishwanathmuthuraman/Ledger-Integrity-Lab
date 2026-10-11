# Initial implementation — 0.1.0

This is the first implemented offline slice. “Complete” below means the bounded component passed the recorded checks; it does not mean the proposed product or evaluation is complete.

## Completed component tasks

| Task | Work | Status | Delivered behavior |
|---|---|---|---|
| C01 | Implement scoped as-of journal admission | Complete for this slice | Validate organization/engagement scope, deduplicate records, withhold unavailable evidence and quarantine conflicting or malformed accounting entries. |
| C02 | Produce exact accounting controls | Complete for this slice | Check debit/credit sides, fiscal dates, visible account mappings, balanced entries and currency units; conserve row populations and compute scoped gross-debit totals. |
| C03 | Package, test and document the slice | Complete for this slice | Independent Python package, packaged existing schema resources, locked dependencies, CLI error behavior, behavioral tests, CI and captured demo evidence. |

Source: [core](../src/ledger_integrity_lab/core.py), [contracts/utilities](../src/ledger_integrity_lab/common.py), [CLI](../src/ledger_integrity_lab/cli.py), [behavioral tests](../tests/test_core.py), [CLI tests](../tests/test_cli.py). Runtime selection is recorded in [ADR 0001](decisions/0001-offline-core.md).

## What actually ran

Verified on Python **3.12.13**, Darwin: **31 tests passed, zero failed**, Ruff lint/format checks passed. A wheel was built, installed with locked dependency hashes into a fresh environment and exercised from outside the checkout; its schema files loaded from the installed package. The CLI input/output hashes and implementation-file hashes are in the [verification record](../reports/initial-implementation/verification.json). That file identifies exact tested inputs; expected specifications were not copied into an execution report.

```sh
uv sync --locked
uv run --locked ledger-lab inspect examples/normal-recurring.scenario.json
uv run --locked ruff check src tests
uv run --locked ruff format --check src tests
uv run --locked pytest
```

Observed demo: The normal recurring case admits one balanced entry with 250,000 USD minor units of gross debits. That total is an accounting control, not suspected loss. Missing source control totals remain an explicit completeness limitation.

[Captured output](../reports/initial-implementation/demo-1.json). Test use of authored expected files is restricted to development assertions; application code does not open them. These are component regressions, not independent held-out evaluation or performance measurements.

## Relationship to the full plan

Contracts, data quality and as-of evidence have partial implementation evidence. Contextual reason packets, review ranking, labeled experiments and a full research release remain pending.

The [build plan](03-build-plan.md), [requirements](01-product-requirements.md), [evaluation](04-evaluation.md) and [definition of done](05-definition-of-done.md) remain the release criteria. Planned acceptance registers describe the wider system; partial progress does not replace their full conditions. Documentation checks validate authored artifacts separately from application CI.

## Explicit limits

There is no behavioral anomaly ranker, fraud finding, audit opinion, review UI, persisted source snapshot or verified population-completeness claim. Original development fixtures are used for admission checks only; their proposed review-priority reasons are not implemented. A visible mapping must be unique; a complete mapping-version resolution policy is future work.

All example records and observations are synthetic. No network integration or external business action exists in this slice. Financial and property results support human review. No customer impact, trained-model quality, production readiness or independent endorsement is established.

## Next implementation steps

1. Persist immutable input snapshots and versioned chart/calendar mappings; retain scope and as-of boundaries across reimports.
2. Build supported accounting-context reason packets for reversals, closing adjustments and related-entity evidence with explicit incomplete coverage.
3. Add legitimate controls and review-budget baselines, then freeze the temporal/entity evaluation before measuring detection quality.

For each step, add meaningful failure-case tests, capture actual output, preserve evidence/time/money boundaries, and update this record with the revision and unresolved limitations. Do not mark the full release complete from component test counts.
