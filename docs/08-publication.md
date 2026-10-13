# 08 — Public research and private material

**Current state: curated public research blueprint. The proposed detector and experiments are not implemented.** The complete internal implementation handoff is maintained separately. Review the exact file manifest before each publication.

## Two editions with different purposes

| Public research edition | Private development / pilot material |
|---|---|
| Accurate README, runnable reference implementation, architecture sufficient to understand it | Full roadmap, commercial assumptions, customer discovery and proposed deals |
| Original synthetic examples and permitted dataset instructions | Customer GL exports, mappings, identities and correspondence |
| Baselines, frozen evaluation recipe, actual aggregate results, error analysis | Private held-out labels before evaluation, customer-specific thresholds and operations |
| Reproducible model configuration when claiming reproducible results | Proprietary trained artifacts or licensed data whose rights restrict publication |
| Honest authorship/contribution history and cited related work | Credentials, private affiliations, restricted security configuration and personal records |

Public code and designs can be read and copied. A license defines permitted reuse; it does not make publication confidential. Choosing Go, Rust or any other language does not prevent copying. Original code, documentation and synthetic fixtures are licensed under Apache-2.0; see LICENSE and NOTICE. Third-party material retains its own terms.

Public credibility needs enough evidence for someone to inspect and reproduce the claimed work. Protect genuine secrets by keeping them out of the public edition, not by hiding the methods needed to assess a performance claim. If a private model cannot be distributed, label the public artifact a limited demonstration and state exactly what cannot be reproduced.

## Before a public release

1. Build the research edition in a fresh staging directory from an explicit allowlist. Do not copy the whole local folder and hope ignore rules remove private files.
2. Check every staged file, generated report, archive and Git history for personal/customer identifiers, credentials, private affiliations and raw operational records.
3. Confirm all data and assets have a recorded origin and redistribution permission. Link to restricted external data rather than bundling it.
4. Preserve sources and actual contributor attribution. Use the owner's configured Git identity; do not add promotional tool signatures or invented co-authors. Follow any disclosure requirements of a research venue or assessment.
5. Publish results only after the exact experiment exists. Remove empty score badges and “production-ready” claims from unfinished work.
6. Mark diagrams and screenshots as proposed or synthetic when appropriate. Never use an institutional logo or certificate-style badge to imply an award or endorsement.
7. Run release integrity checks and retain the manifest linking public claims to evidence.

## Research submission path

First reproduce baselines, then state a narrow question about linked evidence, observation time and review budget. Freeze the experiment, inspect failures, compare directly with related work, and have independent readers challenge the conclusions. A preprint is not peer review; a paper submission is not acceptance; a software license is not institutional certification.

No future paper should claim real fraud detection from synthetic anomalies alone. No publication requirement can be satisfied by invented results, hidden test tuning or false authorship. If the negative result is informative, report it.

## Restricted material

Keep raw company records, implementation schedules, customer-specific controls and commercial material outside this public repository. Do not place secrets in sample environment files. Publishing a research specification does not authorize financial actions, real-data access or outbound integrations.
