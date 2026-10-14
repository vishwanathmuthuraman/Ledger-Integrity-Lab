import copy
import json
from pathlib import Path

import pytest

from ledger_integrity_lab.common import ContractError
from ledger_integrity_lab.snapshot import reconcile_reimport, snapshot_manifest

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def scenario():
    return json.loads((ROOT / "examples/normal-recurring.scenario.json").read_text())


def test_manifest_is_deterministic_and_order_independent(scenario):
    shuffled = copy.deepcopy(scenario)
    shuffled["accounts"].reverse()
    shuffled["periods"].reverse()
    assert snapshot_manifest(scenario) == snapshot_manifest(shuffled)
    assert len(snapshot_manifest(scenario)["snapshot_id"]) == 64


def test_manifest_does_not_mutate_input(scenario):
    before = copy.deepcopy(scenario)
    snapshot_manifest(scenario)
    assert scenario == before


def test_any_content_change_changes_identity(scenario):
    changed = copy.deepcopy(scenario)
    changed["entries"][0]["lines"][0]["debit_minor"] = 250001
    assert snapshot_manifest(changed)["snapshot_id"] != snapshot_manifest(scenario)["snapshot_id"]


def test_invalid_input_has_no_manifest(scenario):
    scenario["accounts"].append(dict(scenario["accounts"][0]))
    with pytest.raises(ContractError):
        snapshot_manifest(scenario)


def test_identical_replay(scenario):
    prior = snapshot_manifest(scenario)
    result = reconcile_reimport(prior, copy.deepcopy(scenario))
    assert result == {"status": "identical_replay", "snapshot_id": prior["snapshot_id"]}


def test_later_cutoff_with_new_entry_is_new_snapshot(scenario):
    prior = snapshot_manifest(scenario)
    later = copy.deepcopy(scenario)
    later["observed_as_of"] = "2026-04-11T12:00:00Z"
    entry = copy.deepcopy(later["entries"][0])
    entry["entry_id"] = entry["source_event_id"] = "JE-002"
    for i, line in enumerate(entry["lines"], 1):
        line["line_id"] = f"JE-002-{i}"
    later["entries"].append(entry)
    result = reconcile_reimport(prior, later)
    assert result["status"] == "new_snapshot"
    assert result["supersedes_snapshot_id"] == prior["snapshot_id"]


def test_cutoff_moving_backwards_is_rejected(scenario):
    prior = snapshot_manifest(scenario)
    earlier = copy.deepcopy(scenario)
    earlier["observed_as_of"] = "2026-04-09T12:00:00Z"
    with pytest.raises(ContractError, match="backwards"):
        reconcile_reimport(prior, earlier)


def test_scope_change_is_rejected(scenario):
    prior = snapshot_manifest(scenario)
    narrowed = copy.deepcopy(scenario)
    narrowed["scope"]["authorized_entities"] = ["ENTITY-A"]
    narrowed["scope"]["coverage_entities"] = ["ENTITY-A"]
    narrowed["observed_as_of"] = "2026-04-11T12:00:00Z"
    with pytest.raises(ContractError, match="scope"):
        reconcile_reimport(prior, narrowed)


def test_organization_mismatch_is_rejected(scenario):
    prior = snapshot_manifest(scenario)
    other = copy.deepcopy(scenario)
    other["engagement_id"] = "ENG-002"
    with pytest.raises(ContractError, match="mismatch"):
        reconcile_reimport(prior, other)


def test_rewritten_known_entry_is_rejected(scenario):
    prior = snapshot_manifest(scenario)
    rewritten = copy.deepcopy(scenario)
    rewritten["observed_as_of"] = "2026-04-11T12:00:00Z"
    rewritten["entries"][0]["lines"][0]["debit_minor"] = 1
    rewritten["entries"][0]["lines"][1]["credit_minor"] = 1
    with pytest.raises(ContractError, match="entries"):
        reconcile_reimport(prior, rewritten)


def test_same_mapping_version_with_new_content_is_rejected(scenario):
    prior = snapshot_manifest(scenario)
    remapped = copy.deepcopy(scenario)
    remapped["observed_as_of"] = "2026-04-11T12:00:00Z"
    remapped["accounts"][0]["classification"] = "expense"
    with pytest.raises(ContractError, match="versioned accounts"):
        reconcile_reimport(prior, remapped)


def test_new_mapping_version_is_accepted(scenario):
    prior = snapshot_manifest(scenario)
    later = copy.deepcopy(scenario)
    later["observed_as_of"] = "2026-04-11T12:00:00Z"
    new = copy.deepcopy(later["accounts"][0])
    new["mapping_version"] = "COA-2"
    new["recorded_at"] = new["available_at"] = "2026-04-11T00:00:00Z"
    later["accounts"].append(new)
    assert reconcile_reimport(prior, later)["status"] == "new_snapshot"


def test_removed_visible_record_is_rejected(scenario):
    prior = snapshot_manifest(scenario)
    later = copy.deepcopy(scenario)
    later["observed_as_of"] = "2026-04-11T12:00:00Z"
    later["entries"] = []
    with pytest.raises(ContractError, match="removed"):
        reconcile_reimport(prior, later)


def test_non_manifest_prior_is_rejected(scenario):
    with pytest.raises(ContractError):
        reconcile_reimport({"kind": "other"}, scenario)
