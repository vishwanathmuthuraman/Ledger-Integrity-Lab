# Project working instructions

Read README.md, START-HERE.md and docs/01-product-requirements.md through docs/05-definition-of-done.md before implementing. Initial admission/control behavior exists; read docs/IMPLEMENTATION.md. Review ranking and benchmark results remain pending.

The persistent cross-session policy is [ENGINEERING.md](ENGINEERING.md). Read it before changing implementation languages, identity configuration or publication boundaries.

## Standing engineering rules

1. Use Python for data validation, feature engineering, model experiments and evaluation; use SQL for transparent transformations and reconciliation. Prefer the simplest maintained tools that meet measured requirements.
2. Add Go only if a measured ingestion/connector bottleneck or deployment constraint justifies a separate service. Consider Rust only for an isolated demonstrated systems bottleneck. A language is not a confidentiality control or a quality credential. Do not rewrite working components for prestige.
3. Money, debit/credit balance, currency units, fiscal periods, organization scope, visibility cutoffs and idempotency must be deterministic. Models may rank review candidates; they cannot authorize accounting changes.
4. Follow the public milestones in docs/03-build-plan.md; preserve requirement and test IDs. Detailed internal delivery schedules stay outside this public repository. Record actual evidence and do not count documentation checks as application validation.
5. Keep labels, future records, adjudication outcomes and held-out generators outside runtime features. Fit transformations on training data only.
6. Every alert explains the exact reason using source references and as-of-time evidence. Avoid claims about intent or character. Distinguish data quality, review priority, inconclusive evidence and verified human findings.
7. Keep customer exports, secrets, private identifiers, commercial plans and private affiliations outside any public edition. Use original synthetic records in demonstrations.
8. Author commits with the owner's configured Git identity. Do not add automated-tool promotional text or fabricated co-authors. Preserve truthful contribution records and any disclosure specifically required by a publication, employer or evaluation venue.
9. Do not claim awards, institutional endorsement, certification, customer savings, detection performance or production readiness without supporting evidence.
10. Do not initialize/push a repository, contact customers, connect accounts or modify financial systems merely because the blueprint describes a future step. Stay within the currently authorized task.

## Documentation

Maintain local relative links. Planned modules use code formatting until they exist. Run scripts/check_public_docs.py and scripts/validate_blueprint.py after document changes. Keep sources paraphrased, linked and accurately scoped. Existing publications are related work, not endorsements. Full-source licenses are not inherited through a citation.
