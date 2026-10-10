import logging
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from citysense.app import create_app
from citysense.security import Settings


def test_production_requires_authentication():
    with pytest.raises(ValueError, match="API key"):
        Settings(mode="production")
    with pytest.raises(ValueError):
        Settings(mode="production", api_key="short")


def test_key_auth_and_missing_db(request_fixture):
    app = create_app(Settings(mode="production", api_key="fixture-key-only-" * 3))
    client = TestClient(app)
    assert client.get("/health").status_code == 200
    assert (
        client.post("/v1/evaluate", json=request_fixture.model_dump(mode="json")).status_code == 401
    )
    response = client.post(
        "/v1/evaluate",
        json=request_fixture.model_dump(mode="json"),
        headers={"x-api-key": "fixture-key-only-" * 3},
    )
    assert response.status_code == 200
    assert response.headers["cache-control"] == "no-store"
    assert (
        client.get(
            f"/v1/replay/{uuid4()}", headers={"x-api-key": "fixture-key-only-" * 3}
        ).status_code
        == 503
    )


def test_body_size_checks_declared_and_chunked():
    client = TestClient(create_app(Settings(body_limit=1024)))
    assert client.post("/v1/evaluate", content="x" * 1025).status_code == 413
    response = client.post("/v1/evaluate", content=iter([b"x" * 512, b"y" * 513]))
    assert response.status_code == 413


def test_forwarded_addresses_do_not_bypass_rate_limit():
    client = TestClient(create_app(Settings(rate_limit=2)))
    assert client.get("/health").status_code == 200
    assert client.get("/health", headers={"x-forwarded-for": "1.2.3.4"}).status_code == 200
    assert client.get("/health", headers={"x-forwarded-for": "5.6.7.8"}).status_code == 429


def test_logs_and_validation_do_not_echo_sensitive_input(request_fixture, caplog):
    caplog.set_level(logging.INFO, logger="citysense.request")
    app = create_app(Settings())
    client = TestClient(app)
    payload = request_fixture.model_dump(mode="json")
    payload["need"] = "private-person-location-41.65"
    response = client.post("/v1/evaluate", json=payload)
    assert response.status_code == 422
    assert "private-person" not in response.text
    assert "private-person" not in caplog.text
    snapshot_id = str(uuid4())
    client.get(f"/v1/replay/{snapshot_id}")
    assert snapshot_id not in caplog.text
    assert app.state.telemetry.counts[("/v1/evaluate", 422)] == 1
    assert app.state.telemetry.counts[("/v1/replay/{snapshot_id}", 503)] == 1


def test_database_outage_is_sanitized():
    client = TestClient(create_app(Settings(database_url="postgresql://unused@127.0.0.1:1/absent")))
    response = client.get(f"/v1/replay/{uuid4()}")
    assert response.status_code == 503
    assert "unused" not in response.text and "127.0.0.1" not in response.text
