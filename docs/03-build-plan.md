# 03 — Research milestones

Initial offline components are implemented and verified. See [component progress and actual evidence](IMPLEMENTATION.md). Contracts, data quality and as-of evidence have partial implementation evidence. Contextual reason packets, review ranking, labeled experiments and a full research release remain pending. The milestones below retain their complete acceptance boundaries.

The public milestones describe observable outcomes. Detailed delivery schedules, implementation assignments and effort estimates are maintained separately.

| Milestone | Observable evidence required | Current status |
|---|---|---|
| Accounting foundation | Immutable import; exact per-entry balance and control totals; explicit organization, currency and time boundaries | Planned |
| Linked review | Deterministic review cases with available source references; legitimate reversals and incomplete coverage handled explicitly | Planned |
| Fair comparison | Rules, amount-only and seeded random controls evaluated against a frozen candidate on the same population and review budget | Planned |
| Independent research release | Held-out results, uncertainty, hard-negative burden, explanation checks and a reproducible experiment manifest | Planned |
| Supervised external validation | Separately authorized data, qualified accounting review and recorded limits on generalization | Future gate |

## What to inspect now

1. Read the [requirements](01-product-requirements.md) and [architecture](02-architecture.md).
2. Compare the original [development scenarios](../examples/README.md), particularly the paired information-availability and coverage examples.
3. Inspect [contracts](../contracts/README.md) and the [planned acceptance tests](../planning/acceptance-tests.csv). Expected specifications do not represent executed outcomes.
4. Review the [evaluation protocol](04-evaluation.md) and [definition of done](05-definition-of-done.md) before interpreting any future performance claim.

## Run the documentation checks

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-blueprint.txt
.venv/bin/python scripts/validate_blueprint.py
```

This validates the authored research specification. It does not ingest company books, rank journal entries or execute a detection algorithm.

## Evidence policy

Requirements retain stable IDs in [requirements.csv](../planning/requirements.csv), with planned application checks in [acceptance-tests.csv](../planning/acceptance-tests.csv). Publish actual implementation and evidence alongside any future completed milestone. A candidate losing to transparent rules remains a valid research finding; preserve that result and its limitations.
