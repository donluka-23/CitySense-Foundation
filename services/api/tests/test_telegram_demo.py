import asyncio
import importlib.util
from datetime import timedelta
from pathlib import Path

import httpx
import pytest
from test_platform import ACCESS
from test_postgis import seed

from citysense.platform import IntelligenceService
from citysense.telegram_demo import DemoSettings, OperatorHTTPBackend, TelegramDemo


class StoredBackend:
    def __init__(self, service):
        self.service, self.calls = service, 0

    async def details(self, pid, at):
        self.calls += 1
        return self.service.get_place_details("batumi", pid, at)

    async def search(self, query):
        self.calls += 1
        return self.service.search_places("batumi", query)

    async def evaluate(self, query):
        self.calls += 1
        return self.service.evaluate_suitability("batumi", query)


@pytest.fixture
def adapter(db_connection, request_fixture, observations_fixture):
    seed(db_connection, request_fixture, observations_fixture)
    backend = StoredBackend(IntelligenceService(db_connection, ACCESS))
    settings = DemoSettings(
        mode="synthetic",
        allowed_users=[111],
        place_ids=[p.place_id for p in request_fixture.places],
        per_minute=20,
    )
    return TelegramDemo(settings, backend, now=lambda: request_fixture.decision_at)


def command(request):
    return f"/evaluate {request.need.value} {request.target_time.isoformat()} 30 " + " ".join(
        f"{p.place_id}:{p.walk_minutes}" for p in request.places
    )


@pytest.mark.integration
def test_telegram_calls_shared_stored_service_and_labels_fixture(adapter, request_fixture):
    reply = asyncio.run(adapter.handle(111, command(request_fixture)))
    assert "SYNTHETIC DEMO" in reply and "0.730" in reply
    assert "unverified caller estimates" in reply
    assert "unvalidated" in reply and "within_model_limit" in reply
    assert "openstreetmap.org/?mlat=" not in reply
    assert adapter.backend.calls == 1


@pytest.mark.integration
@pytest.mark.parametrize("text", ["/start", "/help", "/needs", "/sports"])
def test_deterministic_commands_need_no_llm(adapter, text):
    reply = asyncio.run(adapter.handle(111, text))
    assert "SYNTHETIC DEMO" in reply and adapter.backend.calls == 0
    if text == "/sports":
        assert "Three courts cannot be returned" in reply


@pytest.mark.integration
def test_authorization_private_chat_and_rate_limits(adapter, request_fixture):
    assert "denied" in asyncio.run(adapter.handle(222, command(request_fixture)))
    assert "denied" in asyncio.run(adapter.handle(111, command(request_fixture), private=False))
    assert not adapter.windows and adapter.backend.calls == 0
    adapter.settings.per_minute = 1
    asyncio.run(adapter.handle(111, "/start"))
    assert "Rate limit" in asyncio.run(adapter.handle(111, "/help"))
    assert adapter.backend.calls == 0


@pytest.mark.integration
def test_coordinate_request_uses_search_and_same_evaluation_service(adapter, request_fixture):
    text = f"/near cool_walk {request_fixture.target_time.isoformat()} 30 41.63 41.65 20"
    reply = asyncio.run(adapter.handle(111, text))
    assert "0.730" in reply and adapter.backend.calls == 2
    assert not hasattr(adapter, "locations")


@pytest.mark.integration
@pytest.mark.parametrize("bad", ["nan", "-1", "181", "1000000"])
def test_invalid_walk_budget_never_reaches_scoring(adapter, request_fixture, bad):
    text = command(request_fixture).replace(" 30 ", f" {bad} ")
    assert "Invalid request" in asyncio.run(adapter.handle(111, text))
    assert adapter.backend.calls == 0


@pytest.mark.integration
def test_future_unknown_place_and_mode_mix_fail_closed(adapter, request_fixture):
    text = command(request_fixture)
    assert "not cleared" in asyncio.run(
        adapter.handle(111, text.replace(request_fixture.places[0].place_id, "invented"))
    )
    later = (request_fixture.decision_at + timedelta(days=8)).isoformat()
    assert "Invalid" in asyncio.run(
        adapter.handle(111, text.replace(request_fixture.target_time.isoformat(), later))
    )
    adapter.settings.mode = "real"
    assert "not cleared" in asyncio.run(adapter.handle(111, text))


@pytest.mark.integration
def test_insufficient_data_exclusion_and_places_are_honest(adapter, request_fixture):
    async def missing(query):
        result = adapter.backend.service.evaluate_suitability("batumi", query)
        # Invented transport fixture of missing evidence, no claimed current data.
        for p in result.assessment.ranked:
            p.score, p.status, p.reasons = None, "insufficient_data", ["feature_shade:unavailable"]
        result.state.features = []
        return result

    adapter.backend.evaluate = missing
    assert "Insufficient data" in asyncio.run(adapter.handle(111, command(request_fixture)))
    assert "fictional evidence" in asyncio.run(adapter.handle(111, "/places"))
    assert not hasattr(adapter, "locations")


@pytest.mark.parametrize(
    "url,key",
    [
        ("https://example.com", "x" * 32),
        ("http://127.0.0.1:8000?redirect=bad", "x" * 32),
        ("http://user@127.0.0.1", "x" * 32),
        ("http://127.0.0.1", "short"),
    ],
)
def test_operator_transport_rejects_egress_and_missing_credentials(url, key):
    with pytest.raises(ValueError):
        OperatorHTTPBackend(url, key, None)


def test_transport_keeps_operator_auth_and_rights_denial():
    async def run():
        def handler(request):
            assert request.headers["X-API-Key"] == "x" * 32
            return httpx.Response(403)

        async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as http:
            backend = OperatorHTTPBackend("http://127.0.0.1:8000", "x" * 32, http)
            with pytest.raises(PermissionError):
                await backend.search(
                    __import__("citysense.platform", fromlist=["SearchQuery"]).SearchQuery(
                        longitude=41.625,
                        latitude=41.65,
                        radius_m=1000,
                        decision_at="2026-10-09T10:00:00Z",
                    )
                )

    asyncio.run(run())


def test_polling_application_can_be_built_without_network_or_persistence():
    spec = importlib.util.spec_from_file_location(
        "run_telegram", Path(__file__).parents[1] / "scripts/run_telegram.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    demo = TelegramDemo(
        DemoSettings(mode="synthetic", allowed_users=[111], place_ids=["invented"]), None
    )
    app = module.build_application("123456:invented-test-token", demo)
    assert app.persistence is None and app.concurrent_updates == 1
    assert len(app.handlers[0]) == 8
