import copy
import json
from pathlib import Path

import pytest

from ledger_integrity_lab.common import ContractError
from ledger_integrity_lab.core import inspect

ROOT = Path(__file__).resolve().parents[1]
SCENARIOS = sorted((ROOT / "examples").glob("*.scenario.json"))


@pytest.fixture
def scenario():
    return json.loads((ROOT / "examples/normal-recurring.scenario.json").read_text())


@pytest.mark.parametrize("path", SCENARIOS, ids=lambda path: path.stem)
def test_accounting_admission_only_against_development_spec(path):
    scenario = json.loads(path.read_text())
    expected = json.loads(path.with_name(path.name.replace(".scenario.", ".expected.")).read_text())
    if expected["expected_admission"] == "rejected":
        with pytest.raises(ContractError):
            inspect(scenario)
        return
    result = inspect(scenario)
    assert result["visible_entry_ids"] == expected["visible_entry_ids_after_dedup"]
    assert result["withheld_entry_ids"] == expected["withheld_entry_ids"]
    assert bool(result["quarantined"]) == (expected["expected_admission"] == "quarantined")
    population = result["population"]
    assert (
        population["unique"]
        == population["admitted"] + population["withheld"] + population["quarantined"]
    )
    assert population["submitted"] == population["unique"] + population["duplicate_deliveries"]
    assert result["review_ranking_implemented"] is False


def test_exact_control_totals_are_not_loss_estimates(scenario):
    report = inspect(scenario)
    assert report["control_totals"] == [
        {
            "entity_id": "ENTITY-A",
            "period_id": "PERIOD-03",
            "currency": "USD",
            "currency_exponent": 2,
            "gross_debits_minor": 250000,
        }
    ]
    assert report["completeness"] == "source_control_totals_not_supplied"


def test_unbalanced_entry_is_quality_not_risk(scenario):
    scenario["entries"][0]["lines"][0]["debit_minor"] += 1
    report = inspect(scenario)
    assert report["visible_entry_ids"] == []
    assert report["quarantined"][0]["route"] == "data_quality"
    assert "unbalanced_entry" in report["quarantined"][0]["reason_codes"]


def test_future_mapping_cannot_validate_past_entry(scenario):
    for account in scenario["accounts"]:
        account["available_at"] = "2026-05-01T00:00:00Z"
    assert inspect(scenario)["population"]["admitted"] == 0


@pytest.mark.parametrize("mutation", ["scope", "time", "float", "unknown_field"])
def test_contract_failure_does_not_claim_routine(scenario, mutation):
    if mutation == "scope":
        scenario["entries"][0]["organization_id"] = "FOREIGN"
    elif mutation == "time":
        scenario["entries"][0]["available_at"] = "2026-03-01T00:00:00Z"
    elif mutation == "float":
        scenario["entries"][0]["lines"][0]["debit_minor"] = 250000.0
    else:
        scenario["entries"][0]["label"] = "routine"
    with pytest.raises(ContractError):
        inspect(scenario)


def test_same_entry_id_in_two_authorized_entities_remains_distinct(scenario):
    other = copy.deepcopy(scenario["entries"][0])
    other["entity_id"] = "ENTITY-B"
    scenario["entries"].append(other)
    result = inspect(scenario)
    assert result["population"]["admitted"] == 2
    assert len(result["control_totals"]) == 2


def test_read_only_input_and_repeatable_report(scenario):
    original = copy.deepcopy(scenario)
    assert inspect(scenario) == inspect(scenario)
    assert scenario == original


def test_source_event_collision_quarantines_both_and_conserves_population(scenario):
    another = copy.deepcopy(scenario["entries"][0])
    another["entry_id"] = "SECOND"
    scenario["entries"].append(another)
    report = inspect(scenario)
    assert report["population"] == {
        "submitted": 2,
        "duplicate_deliveries": 0,
        "unique": 2,
        "admitted": 0,
        "withheld": 0,
        "quarantined": 2,
    }


def test_future_conflict_cannot_change_past_admission(scenario):
    future = copy.deepcopy(scenario["entries"][0])
    future["available_at"] = "2026-05-01T00:00:00Z"
    future["lines"][0]["debit_minor"] += 1
    scenario["entries"].append(future)
    report = inspect(scenario)
    assert report["population"]["admitted"] == 1
    assert report["quarantined"] == []
    scenario["observed_as_of"] = "2026-05-02T00:00:00Z"
    assert inspect(scenario)["population"]["quarantined"] == 1
