# Contract implementation guide

Canonical input: [scenario schema](../schemas/scenario.schema.json). Intended future output: [review report schema](../schemas/review-report.schema.json). Test-only oracle: [expected result schema](../schemas/expected-result.schema.json).

These are strict JSON Schema 2020-12 contracts. Runtime implementation must additionally validate: unique source keys and conflicting duplicates; referenced entries/accounts/entities/periods; positive one-sided line amounts; per-entry currency consistency and exact balance; authorized organization/entity boundaries; recorded-before-available ordering; date membership in fiscal period; source/evidence visibility; reversal acyclicity; actual completeness assertions; period permission scope; and report population reconciliation.

The bundle is a replay container and may include future records. A valid future record stays hidden from as-of-time views. Test-only expected outcomes must never be loaded by importer, feature or ranking functions. A source scenario file being schema-valid does not mean its financial or authorization semantics are valid.

Fixture permissions and policies are synthetic harness facts, not production authentication. Before a pilot, replace them with trusted imports, permission evidence and approved mapping contracts. Extend the schema under a versioned migration before adding structured role intervals, multiple source systems or multicurrency accounting.

Report ranks and scores are provisional relative priority. `score_meaning` is explicitly `relative_priority_not_probability` or `not_scored`. Reason operands must resolve to available authorized source records; the output schema alone cannot establish faithfulness.


## Metadata versions and availability

Account mappings are scoped by `entity_ids` and have `mapping_version`, `recorded_at` and `available_at`. Fiscal records carry `calendar_version` and record availability in addition to independently observed close events. Expected counterpart declarations carry relationship ID/version and availability. Policy snapshots carry policy version and availability. These fields are mandatory even in synthetic cases; a future-known declaration or mapping cannot affect an earlier view.

The small replay bundle contains a bounded snapshot collection, not a complete production policy-history export. **Version selection and history storage must be implemented before R1 is complete.** Multiple mapping/calendar versions require as-of selection with deterministic latest-observed precedence; future versions stay hidden. A selected policy snapshot unavailable at cutoff is invalid for that run and produces an explicit missing-configuration result. Before accepting multiple policy snapshots in one runtime file, extend the input schema under a versioned migration rather than silently ignoring history. Related-party links follow the declaration version available at cutoff.

Private labels follow [label-record.schema.json](../schemas/label-record.schema.json). `available_at` is the first knowable adjudicated outcome time, not the entry date. For resolved expert/confirmed labels, `adjudicated_at` must be non-null and no later than `available_at`. Unknown labels have `undetermined` value and cannot be treated as routine. Validate creation/adjudication/availability order semantically. Any model fitting, selection, calibration or threshold stage rejects labels unavailable at its declared cutoff.
