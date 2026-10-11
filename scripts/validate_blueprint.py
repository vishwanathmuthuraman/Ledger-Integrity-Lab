#!/usr/bin/env python3
"""Validate blueprint integrity; this does not execute the proposed detector."""
from __future__ import annotations
import csv
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote, urlsplit
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]

def read_json(path):
    return json.loads(path.read_text())

def csv_rows(name):
    with (ROOT / 'planning' / name).open(newline='') as stream:
        return list(csv.DictReader(stream))

def require(condition, message):
    if not condition:
        raise AssertionError(message)

def main():
    schemas = {}
    for path in sorted((ROOT / 'schemas').glob('*.json')):
        value = read_json(path)
        Draft202012Validator.check_schema(value)
        schemas[path.name] = Draft202012Validator(value, format_checker=FormatChecker())
    requirements = csv_rows('requirements.csv')
    tests = csv_rows('acceptance-tests.csv')
    req_ids = {r['requirement_id'] for r in requirements}
    require(len(req_ids) == len(requirements), 'Duplicate requirement ID')
    require(len({r['test_id'] for r in tests}) == len(tests), 'Duplicate test ID')
    for rows in (tests,):
        coverage = set()
        for row in rows:
            linked = set(row['requirement_ids'].split(';'))
            require(linked <= req_ids, 'Unknown linked requirement')
            coverage |= linked
            require(row['status'] in {'not_started', 'in_progress', 'blocked', 'complete'}, 'Unknown task/test status')
        require(coverage == req_ids, 'A requirement lacks task/test coverage')
    require(not (ROOT / 'planning/tasks.csv').exists(), 'Internal task schedule must remain outside public edition')
    require(not (ROOT / 'planning/estimate-summary.json').exists(), 'Internal effort estimates must remain outside public edition')
    index = read_json(ROOT / 'examples/index.json')['scenarios']
    require(len({r['id'] for r in index}) == len(index), 'Duplicate scenario ID')
    admissions = {'accepted': 0, 'quarantined': 0, 'rejected': 0}
    for row in index:
        scenario = read_json(ROOT / 'examples' / row['scenario'])
        expected = read_json(ROOT / 'examples' / row['expected'])
        schemas['scenario.schema.json'].validate(scenario)
        schemas['expected-result.schema.json'].validate(expected)
        require(scenario['scenario_id'] == expected['scenario_id'] == row['id'], 'Fixture identity mismatch')
        require(not (set(expected['required_reason_codes']) & set(expected['forbidden_reason_codes'])), 'Conflicting reason expectations')
        admission = expected['expected_admission']
        require(admission == row['expected_admission'], 'Admission manifest drift')
        admissions[admission] += 1
        # Only integrity checks of authored fixtures; no rule ranking or model execution.
        integrity = set()
        unique = {}
        for entry in scenario['entries']:
            require(entry['recorded_at'] <= entry['available_at'], 'Impossible fixture availability')
            previous = unique.get(entry['entry_id'])
            if previous is not None and previous != entry:
                integrity.add('duplicate_conflict')
            unique.setdefault(entry['entry_id'], entry)
            if entry['organization_id'] != scenario['organization_id']:
                integrity.add('cross_organization_reference')
            require(entry['entity_id'] in scenario['scope']['authorized_entities'], 'Fixture entity scope invalid')
            if any(line['currency'] != entry['currency'] for line in entry['lines']):
                integrity.add('currency_mismatch')
            if sum(line['debit_minor'] for line in entry['lines']) != sum(line['credit_minor'] for line in entry['lines']):
                integrity.add('unbalanced_entry')
            for line in entry['lines']:
                require((line['debit_minor'] > 0) != (line['credit_minor'] > 0), 'Fixture line must have one positive side')
        for evidence in scenario['evidence']:
            require(evidence['recorded_at'] <= evidence['available_at'], 'Impossible evidence availability')
            if evidence['organization_id'] != scenario['organization_id']:
                integrity.add('cross_organization_reference')
            require(set(evidence['entry_ids']) <= set(unique), 'Fixture evidence has missing entry')
        for record in [*scenario['accounts'], *scenario['periods'], *scenario['scope']['expected_counterparts'], scenario['policy']]:
            require(record['recorded_at'] <= record['available_at'], 'Metadata availability conflict')
        if admission == 'accepted':
            require(not integrity, f'Accepted fixture has integrity fault: {row["name"]}')
            visible = [e for e in unique.values() if e['available_at'] <= scenario['observed_as_of']]
            withheld = [e['entry_id'] for e in unique.values() if e['available_at'] > scenario['observed_as_of']]
            totals = {}
            for entry in visible:
                totals[entry['currency']] = totals.get(entry['currency'], 0) + sum(line['debit_minor'] for line in entry['lines'])
            require([e['entry_id'] for e in visible] == expected['visible_entry_ids_after_dedup'], 'Visible IDs drift')
            require(withheld == expected['withheld_entry_ids'], 'Withheld IDs drift')
            require(totals == expected['expected_gross_debits_minor_by_currency'], 'Exact fixture amount drift')
        else:
            require(bool(integrity), 'Rejected fixture lacks its specified integrity fault')
            require(integrity <= set(expected['required_reason_codes']), 'Integrity fixture expectation mismatch')
    source_register = read_json(ROOT / 'research/source-register.json')
    sources = source_register['sources']
    require(len({r['id'] for r in sources}) == len(sources), 'Duplicate source IDs')
    for row in sources:
        require(urlsplit(row['url']).scheme == 'https', 'Source must have HTTPS URL')
        require(bool(row['checked_on'] and row['supported_claim'] and row['limitations']), 'Source provenance incomplete')
    links = 0
    for path in ROOT.rglob('*.md'):
        if any(part in {'.venv', 'private', '.git'} for part in path.relative_to(ROOT).parts):
            continue
        for target in re.findall(r'\]\(([^)]+)\)', path.read_text()):
            target = target.strip('<>')
            if urlsplit(target).scheme or target.startswith('#'):
                continue
            relative = unquote(target.split('#', 1)[0])
            if not relative:
                continue
            resolved = (path.parent / relative).resolve()
            if resolved == ROOT / 'docs/blueprint-validation.json':
                continue
            require(resolved.exists(), f'Broken local link in {path.name}: {relative}')
            links += 1
    result = {
        'check_type': 'documentation_contract_and_fixture_integrity_only',
        'checked_at': datetime.now(timezone.utc).isoformat(),
        'passed': True,
        'edition': 'curated_public_specification', 'internal_delivery_plan_included': False,
        'requirements': len(requirements), 'planned_application_tests': len(tests),
        'schema_count': len(schemas), 'fixture_pairs': len(index), 'fixture_admissions': admissions,
        'primary_sources': len(sources), 'local_markdown_links_checked': links,
        'requirement_acceptance_test_coverage': 'complete',
        'full_application_implemented': False, 'implementation_evidence': 'reports/initial-implementation/verification.json', 'application_tests_run': False, 'benchmark_run': False,
        'fixture_manifest_sha256': hashlib.sha256((ROOT / 'examples/index.json').read_bytes()).hexdigest()
    }
    (ROOT / 'docs/blueprint-validation.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
