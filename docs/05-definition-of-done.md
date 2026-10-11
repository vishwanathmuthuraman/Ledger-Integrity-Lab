# 05 — Definition of done

## R0: handoff completeness

R0 is complete when the documentation validator succeeds on the authored schemas, source register, original fixture pairs and requirement-to-acceptance-test coverage. The public reading guide must link to its source documents. A successful R0 check is **not** an algorithm run or application test.

## R1: reproducible research application

All required R1 tasks have reviewed evidence. The optional external dataset task may remain blocked if rights or provenance cannot be established. The following are mandatory:

1. A clean environment installs the locked application; import, replay, ranking and report commands execute as specified.
2. Exact money, balancing, supported currency, coverage reconciliation and semantic validation are tested with meaningful failure cases.
3. Observation time, organization scope and versioned mappings/periods apply to every source, feature, explanation and export.
4. Rules, amount/random baselines and at least one candidate run on the same case population and fixed budgets.
5. Source-linked packets show neutral questions, evidence gaps and precise calculations; no unsupported intent or probability claim appears.
6. Reviewer corrections and findings preserve history. Earlier reports reproduce from their original hashes and versions.
7. The independent evaluation protocol is frozen before test outcomes are inspected. Labels and synthetic generator hints remain outside runtime features.
8. The report includes every planned baseline, hard negatives, failures, coverage, denominators, uncertainty and limitations. A losing candidate is reported honestly.
9. Resource use is actually measured on named hardware and dataset sizes; synthetic targets are not pasted in as measured performance.
10. A second person can reproduce the report from the release manifest without access to undisclosed private data.

A candidate that fails the promotion threshold may still produce a complete research release. Record which method would be used and why. A dataset that is not sufficiently realistic or independently reviewed restricts the claims; it is not fixed by a polished README.

## R2: supervised real-data pilot

Require a written authorized source scope, qualified accounting reviewer, approved security/data handling and retention, limited access, a review process for disagreements and an operational owner. Run in shadow mode against an existing human process. No autonomous ledger changes, sanctions, personnel outcomes or audit opinions.

Measure new evidence: accepted review cases, reviewer workload, blind spots, false alarms and operational failures. Define in advance which findings can be reported externally and who authorizes release. A pilot without sufficient resolved outcomes cannot establish detection accuracy.

## Release evidence packet

Use [release-evidence.md](../templates/release-evidence.md). Include source/config/code hashes, actual commands, real results, role of each contributor, limitations and private/public packaging decision. Public claims must be supported by these artifacts. Omit claims of awards, certification, professional assurance, customers or originality unless those have actually been earned and verified.

The current repository is a public research blueprint. All application tests in [acceptance-tests.csv](../planning/acceptance-tests.csv) remain `not_started`.
