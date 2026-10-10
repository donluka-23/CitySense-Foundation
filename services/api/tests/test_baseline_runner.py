import json
from datetime import timedelta
from pathlib import Path

import httpx
import pytest

from citysense.baseline_runner import (
    ClientFailure,
    FixtureClient,
    FrozenScenario,
    ModelReply,
    OpenAIResponsesClient,
    ProspectiveManifest,
    RunnerConfig,
    run_scenario,
    verify_receipt,
)
from citysense.ingestion import SourceMetadata
from citysense.models import SpatialPlace


def scenario(request):
    return FrozenScenario(
        scenario_id="offline-case",
        synthetic=True,
        request=request,
        places=[
            SpatialPlace(
                place_id=p.place_id,
                city_id="batumi",
                name=p.name,
                longitude=41.63 + i * 0.01,
                latitude=41.65,
                source_id="synthetic-fixture",
                license_id="CC0-synthetic",
                retrieved_at=request.decision_at - timedelta(days=1),
            )
            for i, p in enumerate(request.places)
        ],
        frozen_at=request.decision_at - timedelta(seconds=10),
        sources=[
            SourceMetadata(
                source_id="synthetic-fixture",
                source_version="fixture-1",
                license_id="CC0-synthetic",
                synthetic=True,
                research_allowed=True,
                commercial_allowed=False,
                cache_allowed=True,
                redistribution_allowed=True,
                attribution_required=False,
            )
        ],
        capture_permitted=True,
        external_model_permitted=False,
        no_personal_data=True,
    )


def config(at, **changes):
    values = dict(
        provider="fixture",
        model_id="invented-offline-model",
        input_usd_per_million=0,
        output_usd_per_million=0,
        pricing_reviewed_at=at,
    )
    return RunnerConfig(**(values | changes))


def execute(tmp_path, request, client=None, **changes):
    item = scenario(request)
    return run_scenario(
        item,
        "a" * 64,
        "fixture-budget",
        config(request.decision_at, **changes),
        client or FixtureClient(),
        tmp_path,
        now=lambda: request.decision_at - timedelta(seconds=1),
    )


def test_offline_exact_capture_and_exclusive_receipts(tmp_path, request_fixture):
    result = execute(tmp_path, request_fixture)
    assert result["synthetic"] and result["status"] == "abstained"
    assert result["tool_calls"] == 1 and result["total_tokens"] == 280
    events = verify_receipt(Path(result["receipt_path"]))
    request = next(e["value"]["payload"] for e in events if e["kind"] == "request")
    assert request["store"] is False and request["tool_choice"] == "required"
    assert "preferred_place_id" not in json.dumps(events)
    assert "score" not in json.dumps(scenario(request_fixture).model_dump(mode="json"))
    assert execute(tmp_path, request_fixture)["receipt_path"] != result["receipt_path"]
    assert result["empirical_status"] == "NOT EVALUATED"


@pytest.mark.parametrize(
    "changes,status",
    [
        ({"max_total_tokens": 32}, "token_budget_exhausted"),
        ({"input_usd_per_million": 100, "max_cost_usd": 0.001}, "cost_budget_exhausted"),
    ],
)
def test_preflight_budget_never_calls_client(tmp_path, request_fixture, changes, status):
    result = execute(tmp_path, request_fixture, **changes)
    assert result["status"] == status
    assert not any(e["kind"] == "request" for e in verify_receipt(Path(result["receipt_path"])))


class FailureClient(FixtureClient):
    def __init__(self, code, retryable=False):
        self.code, self.retryable, self.calls = code, retryable, 0

    def complete(self, payload, timeout):
        self.calls += 1
        raise ClientFailure(self.code, self.retryable)


@pytest.mark.parametrize("code,retryable,calls", [("timeout", False, 1), ("http_429", True, 4)])
def test_failures_and_bounded_retry_are_retained(tmp_path, request_fixture, code, retryable, calls):
    client = FailureClient(code, retryable)
    item = scenario(request_fixture)
    result = run_scenario(
        item,
        "a" * 64,
        "test-budget",
        config(request_fixture.decision_at),
        client,
        tmp_path,
        now=lambda: request_fixture.decision_at - timedelta(seconds=1),
        sleep=lambda _: None,
    )
    assert result["status"] == code and client.calls == calls
    assert result["prediction"] is None and result["reserved_tokens"] > 0
    assert (
        len([e for e in verify_receipt(Path(result["receipt_path"])) if e["kind"] == "failure"])
        == calls
    )


class MutatedClient(FixtureClient):
    def __init__(self, mutation):
        self.mutation = mutation

    def complete(self, payload, timeout):
        body = json.loads(super().complete(payload, timeout).raw)
        if self.mutation == "unknown_tool":
            body["output"] = [
                {
                    "type": "function_call",
                    "name": "fetch_live_web",
                    "call_id": "bad",
                    "arguments": "{}",
                }
            ]
        elif self.mutation == "usage":
            body["usage"]["total_tokens"] = 1
        elif self.mutation == "model":
            body["model"] = "different-model"
        elif self.mutation == "tools":
            body["output"] *= 3
        elif self.mutation == "invented" and body["output"][0]["type"] == "message":
            body["output"][0]["content"][0]["text"] = json.dumps(
                {"choice": "invented-court", "reason": "fake"}
            )
        return ModelReply(raw=json.dumps(body))


@pytest.mark.parametrize(
    "mutation,status",
    [
        ("unknown_tool", "invalid_response"),
        ("usage", "invalid_response"),
        ("model", "model_or_completion_mismatch"),
        ("tools", "tool_budget_exhausted"),
        ("invented", "invalid_response"),
    ],
)
def test_adversarial_provider_output_fails_closed(tmp_path, request_fixture, mutation, status):
    assert execute(tmp_path, request_fixture, MutatedClient(mutation))["status"] == status


@pytest.mark.parametrize(
    "mutation", ["label", "score", "future", "source", "permission", "duplicate"]
)
def test_manifest_leakage_time_lineage_and_permissions(request_fixture, mutation):
    value = scenario(request_fixture).model_dump(mode="json")
    if mutation in {"label", "score"}:
        value["request"]["places"][0][mutation] = 0.8
    elif mutation == "future":
        value["request"]["places"][0]["feature_shade"]["retrieved_at"] = (
            request_fixture.decision_at.isoformat()
        )
    elif mutation == "source":
        value["sources"][0]["source_version"] = "wrong"
    elif mutation == "permission":
        value["capture_permitted"] = False
    else:
        value["sources"].append(value["sources"][0])
    with pytest.raises(ValueError):
        FrozenScenario.model_validate(value)


def test_live_client_transfer_guard_and_prospectivity(tmp_path, request_fixture):
    class MockLive(FixtureClient):
        provider, synthetic = "openai", False

    with pytest.raises(PermissionError):
        run_scenario(
            scenario(request_fixture),
            "a" * 64,
            "test",
            config(
                request_fixture.decision_at,
                provider="openai",
                input_usd_per_million=1,
                output_usd_per_million=1,
            ),
            MockLive(),
            tmp_path,
        )
    assert not list(tmp_path.glob("*"))


def test_hash_chain_detects_mutation_and_truncation(tmp_path, request_fixture):
    result = execute(tmp_path, request_fixture)
    path = Path(result["receipt_path"])
    lines = path.read_text().splitlines()
    path.write_text("\n".join(lines[:-1]))
    with pytest.raises(ValueError, match="Incomplete"):
        verify_receipt(path)
    lines[0] = lines[0].replace("fixture-budget", "mutated-budget")
    path.write_text("\n".join(lines))
    with pytest.raises(ValueError, match="hash chain"):
        verify_receipt(path)


def test_openai_http_contract_without_any_real_credential():
    def handler(request):
        assert request.url == "https://api.openai.com/v1/responses"
        assert request.headers["Authorization"] == "Bearer invented-test-secret"
        return httpx.Response(200, json={"test": True})

    with httpx.Client(transport=httpx.MockTransport(handler)) as http:
        reply = OpenAIResponsesClient("invented-test-secret", http).complete({"store": False}, 1)
        assert json.loads(reply.raw) == {"test": True}
    with httpx.Client(transport=httpx.MockTransport(lambda _: httpx.Response(302))) as http:
        with pytest.raises(ClientFailure, match="http_302"):
            OpenAIResponsesClient("invented", http).complete({}, 1)


def test_manifest_hash_includes_candidate_universe(request_fixture):
    manifest = ProspectiveManifest(
        information_budget_id="test", scenarios=[scenario(request_fixture)]
    )
    old = manifest.digest
    manifest.scenarios[0].request.max_walk_minutes = 10
    assert manifest.digest != old
