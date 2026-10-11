"""Exact journal admission and an as-of view; no intent or fraud classifier."""

from datetime import date

from .common import ContractError, exact_integer, timestamp, unique, validate_shape


def inspect(scenario):
    validate_shape(scenario, "scenario")
    organization = scenario["organization_id"]
    cutoff = timestamp(scenario["observed_as_of"])
    scope = set(scenario["scope"]["authorized_entities"])
    if not set(scenario["scope"]["coverage_entities"]) <= scope:
        raise ContractError("coverage outside authorized scope")
    for record in scenario["entries"] + scenario["evidence"]:
        if record["organization_id"] != organization or record["entity_id"] not in scope:
            raise ContractError("organization or engagement scope mismatch")
    for record in (
        scenario["accounts"]
        + scenario["periods"]
        + scenario["entries"]
        + scenario["evidence"]
        + [scenario["policy"]]
    ):
        if timestamp(record["recorded_at"]) > timestamp(record["available_at"]):
            raise ContractError("availability precedes source recording")
    groups = {}
    for entry in scenario["entries"]:
        groups.setdefault((entry["entity_id"], entry["entry_id"]), []).append(entry)
    entries = {}
    deliveries = {}
    conflicts = set()
    duplicates = len(scenario["entries"]) - len(groups)
    for key, group in groups.items():
        known = [row for row in group if timestamp(row["available_at"]) <= cutoff]
        entries[key] = known[0] if known else group[0]
        for entry in known:
            if entry != known[0]:
                conflicts.add(key)
            delivery = entry["entity_id"], entry["source_event_id"]
            if delivery in deliveries and deliveries[delivery] != key:
                conflicts.update({key, deliveries[delivery]})
            deliveries[delivery] = key
    accounts = unique(scenario["accounts"], lambda row: (row["account_id"], row["mapping_version"]))
    periods = unique(
        scenario["periods"],
        lambda row: (row["entity_id"], row["period_id"], row["calendar_version"]),
    )
    unique(scenario["evidence"], lambda row: row["evidence_id"])
    visible = []
    withheld = []
    quarantined = []
    controls = {}
    currency_units = {}
    for key in sorted(entries):
        entry = entries[key]
        if key in conflicts:
            quarantined.append(
                {
                    "entry_id": entry["entry_id"],
                    "entity_id": entry["entity_id"],
                    "reason_codes": ["duplicate_identity_conflict"],
                    "route": "data_quality",
                }
            )
            continue
        if timestamp(entry["available_at"]) > cutoff:
            withheld.append(entry["entry_id"])
            continue
        reasons = []
        line_ids = set()
        debit = credit = 0
        for line in entry["lines"]:
            debit_value = exact_integer(line["debit_minor"], 0, 9_000_000_000_000)
            credit_value = exact_integer(line["credit_minor"], 0, 9_000_000_000_000)
            if (debit_value > 0) == (credit_value > 0):
                reasons.append("invalid_debit_credit_sides")
            if line["line_id"] in line_ids:
                reasons.append("duplicate_line_identity")
            line_ids.add(line["line_id"])
            if line["currency"] != entry["currency"]:
                reasons.append("mixed_currency_entry")
            mapped = [
                a
                for a in accounts.values()
                if a["account_id"] == line["account_id"]
                and entry["entity_id"] in a["entity_ids"]
                and timestamp(a["available_at"]) <= cutoff
            ]
            if len(mapped) != 1:
                reasons.append("account_mapping_missing_or_ambiguous")
            debit = exact_integer(debit + debit_value)
            credit = exact_integer(credit + credit_value)
        if debit != credit:
            reasons.append("unbalanced_entry")
        period = [
            p
            for p in periods.values()
            if p["entity_id"] == entry["entity_id"]
            and p["period_id"] == entry["period_id"]
            and timestamp(p["available_at"]) <= cutoff
        ]
        if len(period) != 1:
            reasons.append("fiscal_period_missing_or_ambiguous")
        elif (
            not date.fromisoformat(period[0]["starts_on"])
            <= date.fromisoformat(entry["effective_date"])
            <= date.fromisoformat(period[0]["ends_on"])
        ):
            reasons.append("effective_date_outside_fiscal_period")
        currency = entry["currency"]
        exponent = entry["currency_exponent"]
        if currency in currency_units and currency_units[currency] != exponent:
            raise ContractError("inconsistent currency exponent")
        currency_units[currency] = exponent
        if reasons:
            quarantined.append(
                {
                    "entry_id": entry["entry_id"],
                    "entity_id": entry["entity_id"],
                    "reason_codes": sorted(set(reasons)),
                    "route": "data_quality",
                }
            )
        else:
            visible.append(entry)
            control_key = entry["entity_id"], entry["period_id"], currency, exponent
            controls[control_key] = exact_integer(controls.get(control_key, 0) + debit)
    evidence = [row for row in scenario["evidence"] if timestamp(row["available_at"]) <= cutoff]
    return {
        "schema_version": "0.1",
        "kind": "journal_admission_report",
        "organization_id": organization,
        "engagement_id": scenario["engagement_id"],
        "observed_as_of": scenario["observed_as_of"],
        "visible_entry_ids": [row["entry_id"] for row in visible],
        "withheld_entry_ids": withheld,
        "visible_evidence_ids": [row["evidence_id"] for row in evidence],
        "quarantined": quarantined,
        "control_totals": [
            {
                "entity_id": key[0],
                "period_id": key[1],
                "currency": key[2],
                "currency_exponent": key[3],
                "gross_debits_minor": value,
            }
            for key, value in sorted(controls.items())
        ],
        "population": {
            "submitted": len(scenario["entries"]),
            "duplicate_deliveries": duplicates,
            "unique": len(entries),
            "admitted": len(visible),
            "withheld": len(withheld),
            "quarantined": len(quarantined),
        },
        "completeness": "source_control_totals_not_supplied",
        "review_ranking_implemented": False,
    }
