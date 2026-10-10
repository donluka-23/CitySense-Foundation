import json
from datetime import timedelta

import pytest
from conftest import FIXTURES

from citysense.evaluation import (
    BaselineArtifact,
    DatasetManifest,
    FrozenToolBaseline,
    PairedOutcome,
    RuleComparator,
    brier_score,
    clustered_difference,
    grouped_split,
    run_experiment,
)


def dataset():
    return DatasetManifest.model_validate_json((FIXTURES / "evaluation-manifest.json").read_text())


def baseline(data):
    return FrozenToolBaseline(
        BaselineArtifact.model_validate_json((FIXTURES / "baseline-artifact.json").read_text()),
        data,
    )


def test_frozen_synthetic_experiment_is_reproducible(tmp_path):
    data = dataset()
    first = run_experiment(data, baseline(data), tmp_path / "first.json")
    second = run_experiment(data, baseline(data), tmp_path / "second.json")
    assert first == second
    assert first["synthetic"] is True
    assert first["B1_status"] == "not_implemented"
    assert "no empirical validation" in first["interpretation"]
    assert first["metrics"]["B0-citysense"]["denominator"] == 4
    with pytest.raises(FileExistsError):
        run_experiment(data, baseline(data), tmp_path / "first.json")


@pytest.mark.parametrize(
    "field", ["participant_id", "place_time_group", "spatial_block", "time_block"]
)
def test_group_leakage_fails_closed(field):
    data = dataset().model_dump()
    data["records"][4][field] = data["records"][0][field]
    with pytest.raises(ValueError, match="Leakage"):
        DatasetManifest.model_validate(data)


def test_place_leakage_fails_closed():
    data = dataset().model_dump()
    record = data["records"][4]
    record["request"]["places"][0]["place_id"] = data["records"][0]["request"]["places"][0][
        "place_id"
    ]
    record["preferred_place_id"] = record["request"]["places"][0]["place_id"]
    with pytest.raises(ValueError, match="Leakage"):
        DatasetManifest.model_validate(data)


def test_temporal_embargo_and_real_consent_fail_closed():
    data = dataset().model_dump()
    data["embargo_hours"] = 168
    with pytest.raises(ValueError, match="embargo"):
        DatasetManifest.model_validate(data)
    data["embargo_hours"] = 24
    data["synthetic"] = False
    with pytest.raises(ValueError, match="consent"):
        DatasetManifest.model_validate(data)


def test_baseline_candidate_hash_and_future_knowledge_fail_closed():
    data = dataset()
    artifact = baseline(data).artifact.model_dump()
    artifact["predictions"][0]["request_hash"] = "0" * 64
    with pytest.raises(ValueError, match="different candidates"):
        FrozenToolBaseline(BaselineArtifact.model_validate(artifact), data)
    artifact = baseline(data).artifact.model_dump()
    artifact["predictions"][0]["available_at"] += timedelta(seconds=1)
    with pytest.raises(ValueError, match="future"):
        FrozenToolBaseline(BaselineArtifact.model_validate(artifact), data)


def test_connected_components_and_insufficient_groups():
    data = dataset()
    proposal = grouped_split(data.records)
    assert len(proposal) == len(data.records)
    assert set(proposal.values()) == {"train", "validation", "test"}
    for split in ("train", "validation", "test"):
        assert len({proposal[r.record_id] for r in data.records if r.split == split}) == 1
    for record in data.records:
        record.participant_id = "same-person"
    with pytest.raises(ValueError, match="independent components"):
        grouped_split(data.records)


def test_small_cluster_ci_is_unavailable():
    outcome = PairedOutcome(
        record_id="one", participant_id="p", place_time_group="g", need="cool_walk", correct=True
    )
    assert clustered_difference([outcome], [outcome])["interval"] is None


def test_abstention_and_probability_metric():
    record = dataset().records[0]
    record.request.places[0].feature_shade = None
    assert RuleComparator().predict(record) is None
    assert brier_score([0.8, 0.2], [True, False]) == pytest.approx(0.04)
    with pytest.raises(ValueError):
        brier_score([float("nan")], [True])


def test_fixture_files_have_explicit_provenance():
    data = json.loads((FIXTURES / "evaluation-manifest.json").read_text())
    assert data["synthetic"] and data["license_id"] == "CC0-synthetic"


def test_baseline_budget_mismatch_rejected():
    data = dataset()
    artifact = baseline(data).artifact.model_dump()
    artifact["information_budget_id"] = "unmatched"
    with pytest.raises(ValueError, match="budgets"):
        FrozenToolBaseline(BaselineArtifact.model_validate(artifact), data)


def test_calibration_cannot_fit_holdout(tmp_path):
    data = dataset()

    class LeakyComparator:
        name = "B1-calibrated"

        def predict(self, record):
            return record.preferred_place_id

        def configuration(self):
            return {
                "dataset_hash": data.digest,
                "fit_record_ids": ["test-0"],
                "tuning_record_ids": [],
            }

    with pytest.raises(ValueError, match="train-only"):
        run_experiment(data, baseline(data), tmp_path / "leaky.json", LeakyComparator())
