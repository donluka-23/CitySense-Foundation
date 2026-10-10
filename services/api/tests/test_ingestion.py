import json
from datetime import UTC, datetime, timedelta

import httpx
import pytest
from conftest import FIXTURES

from citysense.ingestion import (
    FakeProvider,
    NormalizedHTTPProvider,
    ProviderUnavailable,
    SnapshotQuery,
    SourceMetadata,
    observation_to_feature,
)
from citysense.models import Feature


def metadata():
    return SourceMetadata.model_validate_json((FIXTURES / "source-metadata.json").read_text())


def query(request_fixture):
    return SnapshotQuery(
        place_ids=[p.place_id for p in request_fixture.places],
        target_time=request_fixture.decision_at - timedelta(hours=1),
    )


def provider(handler, **kwargs):
    return NormalizedHTTPProvider(
        "https://fixtures.invalid/snapshots",
        frozenset({"fixtures.invalid"}),
        metadata(),
        httpx.Client(transport=httpx.MockTransport(handler)),
        jitter=lambda: 0,
        received_at=kwargs.pop("received_at", lambda: datetime(2026, 10, 9, 10, tzinfo=UTC)),
        sleep=kwargs.pop("sleep", lambda _: None),
        **kwargs,
    )


def test_fake_provider_is_deterministic_and_returns_copies(request_fixture, observations_fixture):
    fake = FakeProvider(observations_fixture, metadata())
    expected = fake.get_snapshots(query(request_fixture))
    assert expected == observations_fixture
    expected[0].value = 0
    assert fake.get_snapshots(query(request_fixture))[0].value == 0.8
    assert Feature.model_validate(observation_to_feature(observations_fixture[0])).value == 0.8


def test_retry_timeout_then_rate_limit_then_success(request_fixture):
    calls, sleeps = [], []

    def handler(request):
        calls.append(request)
        assert request.extensions["timeout"]["read"] == 5
        if len(calls) == 1:
            raise httpx.ReadTimeout("fixture timeout")
        if len(calls) == 2:
            return httpx.Response(429, headers={"Retry-After": "2"})
        return httpx.Response(200, content=(FIXTURES / "observations.json").read_bytes())

    adapter = provider(handler, sleep=sleeps.append)
    assert len(adapter.get_snapshots(query(request_fixture))) == 6
    assert len(adapter.get_snapshots(query(request_fixture))) == 6
    assert len(calls) == 3 and sleeps == [1, 2]


def test_cache_expiry_and_no_stale_fallback(request_fixture):
    calls = []
    now = [0.0]

    def handler(request):
        calls.append(request)
        if len(calls) == 1:
            return httpx.Response(200, content=(FIXTURES / "observations.json").read_bytes())
        return httpx.Response(503)

    adapter = provider(handler, monotonic=lambda: now[0])
    adapter.get_snapshots(query(request_fixture))
    now[0] = 61
    with pytest.raises(ProviderUnavailable, match="exhausted"):
        adapter.get_snapshots(query(request_fixture))
    assert len(calls) == 4


def test_validation_is_not_retried(request_fixture):
    calls = []

    def handler(request):
        calls.append(request)
        return httpx.Response(200, json=[{"invalid": "payload"}])

    with pytest.raises(ValueError):
        provider(handler).get_snapshots(query(request_fixture))
    assert len(calls) == 1


@pytest.mark.parametrize("status", [301, 400, 401, 403, 404])
def test_permanent_errors_and_redirects_are_not_retried(request_fixture, status):
    calls = []

    def handler(request):
        calls.append(request)
        return httpx.Response(status, headers={"Location": "http://127.0.0.1/secret"})

    with pytest.raises(ProviderUnavailable):
        provider(handler).get_snapshots(query(request_fixture))
    assert len(calls) == 1


def test_retry_after_beyond_budget_fails_without_sleep(request_fixture):
    sleeps = []
    adapter = provider(
        lambda _: httpx.Response(429, headers={"Retry-After": "3600"}), sleep=sleeps.append
    )
    with pytest.raises(ProviderUnavailable, match="budget"):
        adapter.get_snapshots(query(request_fixture))
    assert not sleeps


@pytest.mark.parametrize(
    "url",
    [
        "http://fixtures.invalid/x",
        "https://127.0.0.1/x",
        "https://user:password@fixtures.invalid/x",
    ],
)
def test_ssrf_configuration_rejected(url):
    with pytest.raises(ValueError):
        NormalizedHTTPProvider(url, frozenset({"fixtures.invalid"}), metadata(), httpx.Client())


def test_lineage_mismatch_and_raw_units_rejected(request_fixture, observations_fixture):
    payload = json.loads((FIXTURES / "observations.json").read_text())
    payload[0]["source_id"] = "different-provider"
    with pytest.raises(ValueError, match="lineage"):
        provider(lambda _: httpx.Response(200, json=payload)).get_snapshots(query(request_fixture))
    observations_fixture[0].unit = "degrees_celsius"
    with pytest.raises(ValueError, match="transformation"):
        observation_to_feature(observations_fixture[0])


def test_circuit_opens_after_exhaustion(request_fixture):
    calls = []

    def handler(request):
        calls.append(request)
        return httpx.Response(500)

    adapter = provider(handler)
    for _ in range(3):
        with pytest.raises(ProviderUnavailable, match="exhausted"):
            adapter.get_snapshots(query(request_fixture))
    with pytest.raises(ProviderUnavailable, match="circuit"):
        adapter.get_snapshots(query(request_fixture))
    assert len(calls) == 9


def test_provider_stream_limit(request_fixture):
    adapter = provider(lambda _: httpx.Response(200, content=b"x" * 1048577))
    with pytest.raises(ProviderUnavailable, match="payload exceeded"):
        adapter.get_snapshots(query(request_fixture))


def test_live_rights_cannot_be_assumed():
    data = metadata().model_dump()
    data["synthetic"] = False
    with pytest.raises(ValueError, match="terms review"):
        SourceMetadata.model_validate(data)


def test_gateway_archive_timestamp_cannot_backdate_local_availability(request_fixture):
    received = request_fixture.decision_at + timedelta(hours=1)
    adapter = provider(
        lambda _: httpx.Response(200, content=(FIXTURES / "observations.json").read_bytes()),
        received_at=lambda: received,
    )
    observation = adapter.get_snapshots(query(request_fixture))[0]
    assert observation.retrieved_at == received
    assert "upstream_retrieved_at" in observation.quality_metadata
    request_fixture.places[0].feature_shade = Feature.model_validate(
        observation_to_feature(observation)
    )
    from citysense.engine import evaluate

    with pytest.raises(ValueError, match="retrieved after"):
        evaluate(request_fixture)
