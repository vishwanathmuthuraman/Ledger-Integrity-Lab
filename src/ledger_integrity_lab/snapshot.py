"""Content-addressed input snapshot identity and reimport reconciliation.

Offline and in-memory only: nothing is persisted and no source system is contacted.
"""

from .common import ContractError, digest, timestamp, unique, validate_shape

_KEYS = {
    "accounts": lambda r: (r["account_id"], r["mapping_version"]),
    "periods": lambda r: (r["entity_id"], r["period_id"], r["calendar_version"]),
    "evidence": lambda r: (r["evidence_id"],),
    "entries": lambda r: (r["entity_id"], r["entry_id"], r["source_event_id"], r["recorded_at"]),
}
_VERSIONED = ("accounts", "periods")


def _index(records, key):
    result = {}
    for record in records:
        identity = (tuple(key(record)), digest(record))
        result[identity] = {
            "key": list(identity[0]),
            "digest": identity[1],
            "available_at": record["available_at"],
        }
    return [result[k] for k in sorted(result)]


def snapshot_manifest(scenario):
    """Return a deterministic identity for one validated input; the input is not modified."""
    validate_shape(scenario, "scenario")
    unique(scenario["accounts"], _KEYS["accounts"])
    unique(scenario["periods"], _KEYS["periods"])
    unique(scenario["evidence"], _KEYS["evidence"])
    timestamp(scenario["observed_as_of"])
    components = {kind: _index(scenario[kind], key) for kind, key in _KEYS.items()}
    body = {
        "organization_id": scenario["organization_id"],
        "engagement_id": scenario["engagement_id"],
        "observed_as_of": scenario["observed_as_of"],
        "scope_digest": digest(scenario["scope"]),
        "policy_digest": digest(scenario["policy"]),
        "components": components,
    }
    return {"kind": "input_snapshot_manifest", "snapshot_id": digest(body), **body}


def reconcile_reimport(prior, scenario):
    """Classify a reimport against a prior manifest; refuse silent rewrites of known inputs.

    Returns ``identical_replay`` for the same content or ``new_snapshot`` for a compatible
    later import. Raises ContractError when identity, scope, cutoff or history conflicts.
    """
    if prior.get("kind") != "input_snapshot_manifest":
        raise ContractError("prior value is not a snapshot manifest")
    current = snapshot_manifest(scenario)
    if (current["organization_id"], current["engagement_id"]) != (
        prior["organization_id"],
        prior["engagement_id"],
    ):
        raise ContractError("reimport organization or engagement mismatch")
    if current["snapshot_id"] == prior["snapshot_id"]:
        return {"status": "identical_replay", "snapshot_id": current["snapshot_id"]}
    if current["scope_digest"] != prior["scope_digest"]:
        raise ContractError("reimport changes authorized scope")
    prior_cutoff = timestamp(prior["observed_as_of"])
    if timestamp(current["observed_as_of"]) < prior_cutoff:
        raise ContractError("reimport moves knowledge cutoff backwards")
    for kind in _KEYS:
        now = {(tuple(r["key"]), r["digest"]) for r in current["components"][kind]}
        now_keys = {tuple(r["key"]) for r in current["components"][kind]}
        for row in prior["components"][kind]:
            identity = (tuple(row["key"]), row["digest"])
            if identity in now:
                continue
            if kind in _VERSIONED and tuple(row["key"]) in now_keys:
                raise ContractError("versioned " + kind + " content changed under the same version")
            if timestamp(row["available_at"]) <= prior_cutoff:
                raise ContractError("previously visible " + kind + " record changed or removed")
    return {
        "status": "new_snapshot",
        "snapshot_id": current["snapshot_id"],
        "supersedes_snapshot_id": prior["snapshot_id"],
    }
