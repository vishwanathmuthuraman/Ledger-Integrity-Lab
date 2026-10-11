# Original development scenarios

These 16 hand-authored synthetic bundles describe intended behavior. They are small examples, not real company data, a trained model, or measured benchmark outcomes. Expected files are kept separate so a future runtime cannot access labels.

Use [index.json](index.json) to find paired inputs and expected specifications. `scenario_id`, filename, IDs and prose are excluded from model features. Expected admission failures are intentionally schema-valid where possible: semantic accounting and authorization checks must catch them.

The reversal-before/after-known pair tests information availability. Related-counterpart complete/incomplete scope tests abstention. Authorized late posting and documented accrual reversal are deliberate hard negatives. Duplicate, currency, balance and organization cases test integrity rather than fraud. Future document content cannot affect an earlier report or issue commands.

The documentation validator checks shapes, exact fixture totals and expected input validity conditions. It does not execute the future ranking engine or prove that it meets these expected outcomes. No ranking scores or model results are provided.
