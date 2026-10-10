from datetime import timedelta

import pytest
from fastapi.testclient import TestClient

from citysense.app import create_app
from citysense.engine import evaluate
from citysense.models import DataKind, EvaluateRequest, Feature, FeatureQuality
from citysense.parameters import load_parameters
from citysense.security import Settings


def test_tiny_missing_weight_still_abstains(request_fixture):
    parameters = load_parameters()
    parameters.weights[request_fixture.need] = {"feature_shade": 1e-8, "feature_greenery": 1 - 1e-8}
    request_fixture.places[0].feature_shade = None
    result = evaluate(request_fixture, parameters)
    assert next(r for r in result.ranked if r.place_id.endswith("a")).score is None


def test_forecast_horizon_and_freshness_are_separate(request_fixture):
    request_fixture.target_time += timedelta(hours=12)
    feature = request_fixture.places[0].feature_shade.model_dump()
    feature.update(
        data_kind=DataKind.FORECAST,
        quality=FeatureQuality.REGIONAL_FORECAST,
        issued_at=request_fixture.decision_at - timedelta(hours=1),
        observed_or_valid_at=request_fixture.target_time,
    )
    request_fixture.places[0].feature_shade = Feature.model_validate(feature)
    assert evaluate(request_fixture).ranked[0].score == 0.73


def test_deterministic_order_and_components(request_fixture):
    one = evaluate(request_fixture)
    assert one == evaluate(request_fixture)
    request_fixture.places.reverse()
    assert one == evaluate(request_fixture)
    assert one.ranked[0].score == 0.73
    assert sum(c.contribution for c in one.ranked[0].components) == pytest.approx(0.73)
    assert one.ranked[0].confidence == "unvalidated"


def test_missing_data_abstains_not_zero(request_fixture):
    request_fixture.places[0].feature_shade = None
    ranked = next(r for r in evaluate(request_fixture).ranked if r.place_id.endswith("a"))
    assert ranked.score is None and ranked.status == "insufficient_data"
    assert ranked.coverage == 0.35


def test_explicit_unavailable_value_is_preserved(request_fixture):
    payload = request_fixture.places[0].feature_shade.model_dump()
    payload.update(value=None, data_kind=DataKind.UNAVAILABLE, quality=FeatureQuality.UNKNOWN)
    request_fixture.places[0].feature_shade = Feature.model_validate(payload)
    result = evaluate(request_fixture)
    assert next(r for r in result.ranked if r.place_id.endswith("a")).score is None
    assert request_fixture.places[0].feature_shade.value is None


def test_hard_constraint_excludes(request_fixture):
    request_fixture.max_walk_minutes = 6
    result = evaluate(request_fixture)
    assert result.excluded == [request_fixture.places[0].place_id]
    assert result.exclusions[0].reason == "walk_time_exceeded"


@pytest.mark.parametrize("value", [1.2, -0.1, float("nan"), float("inf")])
def test_invalid_scale_fails_closed(request_fixture, value):
    request_fixture.places[0].feature_shade.value = value
    with pytest.raises(ValueError):
        evaluate(request_fixture)


def test_duplicate_ids_rejected(request_fixture):
    request_fixture.places[1].place_id = request_fixture.places[0].place_id
    with pytest.raises(ValueError, match="Duplicate"):
        evaluate(request_fixture)


def test_stale_data_abstains(request_fixture):
    request_fixture.places[0].feature_shade.observed_or_valid_at -= timedelta(days=31)
    assert evaluate(request_fixture).ranked[-1].score is None


def test_forecast_future_retrieval_fails_closed(request_fixture):
    feature = request_fixture.places[0].feature_shade.model_dump()
    feature.update(
        data_kind=DataKind.FORECAST,
        quality=FeatureQuality.REGIONAL_FORECAST,
        issued_at=request_fixture.decision_at - timedelta(hours=1),
        observed_or_valid_at=request_fixture.target_time,
        retrieved_at=request_fixture.decision_at + timedelta(minutes=1),
    )
    request_fixture.places[0].feature_shade = Feature.model_validate(feature)
    with pytest.raises(ValueError, match="retrieved after"):
        evaluate(request_fixture)


def test_forecast_requires_issuance(request_fixture):
    feature = request_fixture.places[0].feature_shade.model_dump()
    feature.update(data_kind="forecast", quality="regional_forecast")
    with pytest.raises(ValueError, match="requires issued_at"):
        Feature.model_validate(feature)


def test_timestamps_are_aware_and_extra_fields_rejected(request_fixture):
    payload = request_fixture.model_dump(mode="json")
    for invalid in ("not-a-time", "2026-10-09T10:00:00"):
        payload["decision_at"] = invalid
        with pytest.raises(ValueError):
            EvaluateRequest.model_validate(payload)
    payload = request_fixture.model_dump(mode="json")
    payload["commission"] = 0.5
    with pytest.raises(ValueError):
        EvaluateRequest.model_validate(payload)


def test_api_validation(request_fixture):
    client = TestClient(create_app(Settings()))
    assert client.get("/health").status_code == 200
    response = client.post("/v1/evaluate", json=request_fixture.model_dump(mode="json"))
    assert response.status_code == 200
    assert response.json() == evaluate(request_fixture).model_dump(mode="json")
