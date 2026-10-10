import json
from datetime import timedelta
from pathlib import Path

import pytest
from test_baseline_runner import config, scenario

from citysense.baseline_runner import (
    FixtureClient,
    FrozenScenario,
    ModelReply,
    run_scenario,
    verify_receipt,
)


def test_annotations_cannot_carry_hidden_labels(request_fixture):
    value = scenario(request_fixture).model_dump(mode="json")
    value["request"]["places"][0]["feature_greenery"]["quality_metadata"]["human_label"] = (
        "invented"
    )
    with pytest.raises(ValueError, match="annotations"):
        FrozenScenario.model_validate(value)


def test_geographic_universe_cannot_be_changed(request_fixture):
    value = scenario(request_fixture).model_dump(mode="json")
    value["places"][0]["place_id"] = "invented-new-place"
    with pytest.raises(ValueError, match="universes"):
        FrozenScenario.model_validate(value)


def test_late_response_has_no_eligible_prediction(tmp_path, request_fixture):
    clock = [0.0]

    class DelayedClient(FixtureClient):
        def complete(self, payload, timeout):
            reply = super().complete(payload, timeout)
            clock[0] += 31
            return reply

    result = run_scenario(
        scenario(request_fixture),
        "a" * 64,
        "fixture-budget",
        config(request_fixture.decision_at),
        DelayedClient(),
        tmp_path,
        now=lambda: request_fixture.decision_at - timedelta(seconds=1),
        monotonic=lambda: clock[0],
    )
    assert result["status"] == "latency_exhausted" and result["prediction"] is None
    assert verify_receipt(Path(result["receipt_path"]))[-1]["kind"] == "finish"


def test_provider_usage_above_reserved_output_is_invalid(tmp_path, request_fixture):
    class Overbudget(FixtureClient):
        def complete(self, payload, timeout):
            body = json.loads(super().complete(payload, timeout).raw)
            body["usage"] = {"input_tokens": 100, "output_tokens": 1000, "total_tokens": 1100}
            return ModelReply(raw=json.dumps(body))

    result = run_scenario(
        scenario(request_fixture),
        "a" * 64,
        "fixture-budget",
        config(request_fixture.decision_at),
        Overbudget(),
        tmp_path,
        now=lambda: request_fixture.decision_at - timedelta(seconds=1),
    )
    assert (
        result["status"] == "provider_usage_exceeded_reservation" and result["prediction"] is None
    )


def test_no_tool_or_request_budget_never_yields_genuine_choice(tmp_path, request_fixture):
    class NoTool(FixtureClient):
        def complete(self, payload, timeout):
            output = {"type": "function_call_output"}
            return super().complete({**payload, "input": [output]}, timeout)

    result = run_scenario(
        scenario(request_fixture),
        "a" * 64,
        "fixture-budget",
        config(request_fixture.decision_at),
        NoTool(),
        tmp_path,
        now=lambda: request_fixture.decision_at - timedelta(seconds=1),
    )
    assert result["status"] == "not_tool_equipped" and result["prediction"] is None


def test_real_prospective_chronology_with_invented_mock_only(tmp_path, request_fixture):
    # Every value and response here is invented; never evidence of an external run.
    item = scenario(request_fixture)
    item.synthetic, item.external_model_permitted = False, True
    for source in item.sources:
        source.synthetic = False
        source.terms_url = "https://example.invalid/invented-test-review"
        source.reviewed_at = item.frozen_at - timedelta(hours=1)

    class InventedLiveMock(FixtureClient):
        provider, synthetic = "openai", False

    settings = config(
        request_fixture.decision_at,
        provider="openai",
        input_usd_per_million=1,
        output_usd_per_million=1,
    )
    result = run_scenario(
        item,
        "a" * 64,
        "test-only",
        settings,
        InventedLiveMock(),
        tmp_path,
        now=lambda: request_fixture.decision_at - timedelta(seconds=1),
    )
    assert result["status"] == "abstained"
    with pytest.raises(ValueError, match="prospective"):
        run_scenario(
            item,
            "a" * 64,
            "test-only",
            settings,
            InventedLiveMock(),
            tmp_path,
            now=lambda: request_fixture.decision_at + timedelta(seconds=1),
        )
