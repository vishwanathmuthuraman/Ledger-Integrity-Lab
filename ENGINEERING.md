# Standing engineering policy

These instructions remain in force for future work on this project. They govern implementation quality and publication; they do not authorize remote publication or live financial actions.

## Language choices

Use **Python and SQL** for the initial accounting, data and algorithm work. Require exact integer/decimal money semantics, tested time/identity contracts and reproducible experiments. A high-quality implementation is demonstrated by correctness, maintainability and evidence, not a prestigious language name.

Use **Go** for a bounded ingestion or connector service only if measured throughput, memory, concurrency or deployment needs justify it. Consider **Rust** for a demonstrated low-level bottleneck where ownership, safety and maintenance costs are understood. Record the profile, alternatives, decision and contract-parity tests before introducing another runtime. The local core remains simple until evidence requires more components.

## Ownership and contribution records

Use the owner's configured personal Git identity: username `vishwanathmuthuraman`, email `vishwanathmuthuraman19@gmail.com`. Verify local repository configuration before future commits; do not change global identity or use an unrelated account.

Do not add automated-tool promotional messages, generated-by signatures or invented co-author trailers to code, documentation or commits. Keep real contributor attribution accurate, preserve honest history, and follow disclosure rules explicitly required by a research venue or assessment. Do not fabricate evidence of authorship, awards, certification or completed work.

## Public/private boundary

This is the curated public research specification. Keep the full internal delivery handoff separate. A later implemented release needs an explicit file allowlist, original synthetic or properly licensed data, enough implementation to assess the claims, and real reproducible results. Keep customer data, private identities, commercial strategy, credentials, live control settings and held-out labels private.

Anything published can be inspected and copied. Language choice, renamed files and omitted attribution do not prevent copying. Choose a license deliberately; do not confuse a software license with institutional certification.

## Quality gates

- Read requirements, architecture and evaluation before coding. Preserve task/requirement/test traceability.
- Keep money, balance, period logic, organization access and information availability deterministic.
- Separate anomalies, missing context, input faults and established human findings.
- Fit or select using only data and labels known at the declared cutoff. Freeze before held-out scoring.
- Run meaningful acceptance tests; record real evidence and failures. Documentation checks never count as detector tests.
- Use qualified accounting review for domain judgments and an independent held-out custodian for evaluation.
- Keep all actions read-only until separately authorized and concretely scoped. No automatic accusations, ledger changes or personnel decisions.
