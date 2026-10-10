import json
from datetime import timedelta
from pathlib import Path

import pytest
from test_baseline_runner import config, scenario
from test_evaluation import dataset

from citysense.baseline_runner import FixtureClient, ProspectiveManifest, run_scenario
from citysense.evaluation import FrozenToolBaseline, content_hash, run_experiment
from citysense.prospective_audit import join_reviewed_receipts


def captured(tmp_path):
    data = dataset()
    scenarios = []
    for record in data.records:
        item = scenario(record.request)
        item.scenario_id = record.record_id
        scenarios.append(item)
    manifest = ProspectiveManifest(
        information_budget_id=data.information_budget_id, scenarios=scenarios
    )
    settings = config(data.frozen_at, latency_seconds=data.latency_budget_seconds)
    paths = []
    for item in scenarios:
        result = run_scenario(
            item,
            manifest.digest,
            manifest.information_budget_id,
            settings,
            FixtureClient(),
            tmp_path,
            now=lambda item=item: item.request.decision_at - timedelta(seconds=1),
        )
        paths.append(Path(result["receipt_path"]))
    return data, manifest, settings, paths


def test_label_free_receipts_join_only_after_generation(tmp_path):
    data, manifest, settings, paths = captured(tmp_path)
    artifact = join_reviewed_receipts(manifest, settings, paths, data)
    result = run_experiment(
        data, FrozenToolBaseline(artifact, data), tmp_path / "software-only.json"
    )
    assert result["synthetic"] and result["metrics"]["A1-tool-equipped"]["coverage"] == 0
    assert "preferred_place_id" not in manifest.model_dump_json()


@pytest.mark.parametrize("mutation", ["missing", "duplicate", "budget", "candidate"])
def test_join_rejects_selection_or_budget_contamination(tmp_path, mutation):
    data, manifest, settings, paths = captured(tmp_path)
    if mutation == "missing":
        paths = paths[:-1]
    elif mutation == "duplicate":
        paths.append(paths[0])
    elif mutation == "budget":
        settings.latency_seconds += 1
    else:
        data.records[0].request.max_walk_minutes = 10
    with pytest.raises(ValueError):
        join_reviewed_receipts(manifest, settings, paths, data)


def test_semantic_accounting_rejects_rehashed_false_total(tmp_path):
    data, manifest, settings, paths = captured(tmp_path)
    events = [json.loads(line) for line in paths[0].read_text().splitlines()]
    events[-1]["value"]["total_tokens"] = 0
    previous = "0" * 64
    for event in events:
        event.pop("hash")
        event["previous_hash"] = previous
        previous = content_hash(event)
        event["hash"] = previous
    paths[0].write_text("\n".join(json.dumps(e) for e in events) + "\n")
    with pytest.raises(ValueError, match="accounting"):
        join_reviewed_receipts(manifest, settings, paths, data)
