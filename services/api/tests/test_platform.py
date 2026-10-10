import json
import os
from datetime import timedelta
from uuid import uuid4

import psycopg
import pytest
from alembic import command
from conftest import FIXTURES
from fastapi.testclient import TestClient
from psycopg import sql
from test_postgis import seed

from citysense.agent_tools import call_tool, tool_catalog
from citysense.app import create_app
from citysense.engine import evaluate
from citysense.models import SpatialPlace
from citysense.platform import (
    AccessContext,
    ComparisonQuery,
    GeometryRevision,
    IntelligenceService,
    SearchQuery,
    StateQuery,
    SuitabilityQuery,
    load_cities,
)
from citysense.security import Settings

ACCESS = AccessContext(
    "test-tenant", frozenset({"batumi"}), frozenset({"city.read", "suitability.read"})
)


def test_configs_are_separate_from_scoring():
    cities = load_cities()
    assert cities["batumi"].timezone == "Asia/Tbilisi"
    assert cities["tbilisi-fixture"].validation_status == "synthetic_configuration_only"
    assert all(t["annotations"]["readOnlyHint"] for t in tool_catalog())
    with pytest.raises(ValueError, match="future tool"):
        call_tool(None, "request_booking", {})


def test_openapi_and_private_auth_gates():
    client = TestClient(create_app(Settings()))
    assert client.post("/v1/cities/batumi/state", json={}).status_code == 401
    schema = client.app.openapi()
    operations = {
        entry["operationId"]
        for path in schema["paths"].values()
        for entry in path.values()
        if isinstance(entry, dict) and "operationId" in entry
    }
    assert {
        "search_places",
        "get_place_details",
        "get_city_state",
        "evaluate_suitability",
        "compare_places",
    } <= operations
    assert "request_booking" not in operations
    assert schema["paths"]["/v1/cities/{city_id}/places"]["get"]["security"] == [
        {"APIKeyHeader": []}
    ]
    client = TestClient(create_app(Settings(api_key="x" * 32)))
    assert client.get("/v1/cities/batumi/places", headers={"X-API-Key": "bad"}).status_code == 401
    assert (
        client.get("/v1/cities/batumi/places", headers={"X-API-Key": "x" * 32}).status_code == 503
    )


@pytest.mark.integration
def test_geometry_revision_asof_and_stable_identity(
    db_connection, request_fixture, observations_fixture
):
    repository = seed(db_connection, request_fixture, observations_fixture)
    service = IntelligenceService(db_connection, ACCESS)
    at = request_fixture.decision_at
    pid = request_fixture.places[0].place_id
    old = service.get_place_details("batumi", pid, at)
    revision = GeometryRevision(
        revision_id=uuid4(),
        place_id=pid,
        longitude=41.7,
        latitude=41.7,
        valid_at=at - timedelta(hours=1),
        retrieved_at=at + timedelta(minutes=1),
        source_id="synthetic-fixture",
        source_version="fixture-1",
        license_id="CC0-synthetic",
    )
    repository.add_geometry_revision(revision)
    assert service.get_place_details("batumi", pid, at) == old
    changed = service.get_place_details("batumi", pid, at + timedelta(minutes=2))
    assert changed.place_id == old.place_id and changed.geometry.coordinates == (41.7, 41.7)
    assert changed.geometry.revision_id == revision.revision_id
    assert (
        service.search_places(
            "batumi", SearchQuery(longitude=41.63, latitude=41.65, radius_m=100, decision_at=at)
        )
        .places[0]
        .place_id
        == pid
    )
    assert not service.search_places(
        "batumi",
        SearchQuery(
            longitude=41.63, latitude=41.65, radius_m=100, decision_at=at + timedelta(minutes=2)
        ),
    ).places
    with pytest.raises(psycopg.errors.RaiseException, match="append-only"):
        with db_connection.transaction():
            db_connection.execute("UPDATE place_geometry_revisions SET latitude=0")


@pytest.mark.integration
def test_stored_suitability_matches_frozen_engine_and_no_future_evidence(
    db_connection, request_fixture, observations_fixture
):
    repository = seed(db_connection, request_fixture, observations_fixture)
    service = IntelligenceService(db_connection, ACCESS)
    query = SuitabilityQuery(
        decision_at=request_fixture.decision_at,
        target_time=request_fixture.target_time,
        need=request_fixture.need,
        max_walk_minutes=request_fixture.max_walk_minutes,
        candidates=[
            {"place_id": p.place_id, "walk_minutes": p.walk_minutes} for p in request_fixture.places
        ],
    )
    result = service.evaluate_suitability("batumi", query)
    assert call_tool(
        service,
        "evaluate_suitability",
        {"city_id": "batumi", "query": query.model_dump(mode="json")},
    ) == result.model_dump(mode="json")
    assert result.assessment.model_dump(exclude={"warning"}) == evaluate(
        request_fixture
    ).model_dump(exclude={"warning"})
    assert (
        result.evidence_origin == "stored_database"
        and "stored evidence" in result.assessment.warning
    )
    future = observations_fixture[0].model_copy(deep=True)
    future.observation_id = uuid4()
    future.retrieved_at = request_fixture.decision_at + timedelta(hours=1)
    future.observed_or_valid_at = future.retrieved_at
    future.value = 0.01
    repository.add_observation(future)
    assert service.evaluate_suitability("batumi", query) == result
    assert len(result.state.features) == 6 and all(
        f.rights.synthetic for f in result.state.features
    )
    with pytest.raises(PermissionError):
        service.get_place_details(
            "tbilisi-fixture", request_fixture.places[0].place_id, query.decision_at
        )
    with pytest.raises(KeyError):
        service.get_place_details("batumi", "missing", query.decision_at)


@pytest.mark.integration
def test_publication_and_scope_fail_closed(db_connection, request_fixture, observations_fixture):
    repository = seed(db_connection, request_fixture, observations_fixture)
    rights = json.loads((FIXTURES / "source-metadata.json").read_text())
    rights.update(source_id="restricted", redistribution_allowed=False)
    repository.add_source("restricted", rights)
    pid = request_fixture.places[0].place_id
    repository.add_geometry_revision(
        GeometryRevision(
            revision_id=uuid4(),
            place_id=pid,
            longitude=41.63,
            latitude=41.65,
            valid_at=request_fixture.decision_at,
            retrieved_at=request_fixture.decision_at,
            source_id="restricted",
            source_version="fixture-1",
            license_id="CC0-synthetic",
        )
    )
    service = IntelligenceService(db_connection, ACCESS)
    with pytest.raises(PermissionError):
        service.get_place_details("batumi", pid, request_fixture.decision_at)
    found = service.search_places(
        "batumi",
        SearchQuery(
            longitude=41.63, latitude=41.65, radius_m=2000, decision_at=request_fixture.decision_at
        ),
    )
    assert pid not in {p.place_id for p in found.places}
    no_scope = IntelligenceService(
        db_connection, AccessContext("other", frozenset({"batumi"}), frozenset())
    )
    with pytest.raises(PermissionError):
        no_scope.get_city_state(
            "batumi",
            StateQuery(
                decision_at=request_fixture.decision_at,
                target_time=request_fixture.target_time,
                place_ids=[pid],
            ),
        )


@pytest.mark.parametrize(
    "changes",
    [
        dict(place_ids=["a", "a"]),
        dict(place_ids=[]),
        dict(place_ids=[str(i) for i in range(31)]),
        dict(target_time="2026-01-01T00:00:00Z"),
        dict(decision_at="2026-10-09T00:00:00"),
    ],
)
def test_state_negative_contracts(changes):
    data = {
        "place_ids": ["a"],
        "decision_at": "2026-10-09T00:00:00Z",
        "target_time": "2026-10-09T01:00:00Z",
    }
    data.update(changes)
    with pytest.raises(ValueError):
        StateQuery.model_validate(data)


def test_comparison_exactly_two_candidates():
    with pytest.raises(ValueError):
        ComparisonQuery(
            decision_at="2026-10-09T00:00:00Z",
            target_time="2026-10-09T01:00:00Z",
            need="cool_walk",
            candidates=[{"place_id": "a", "walk_minutes": 2}],
        )


@pytest.mark.integration
def test_real_platform_transport_and_city_isolation(
    spatial_database, request_fixture, observations_fixture
):
    url, schema, config = spatial_database
    isolated = schema + "_platform"
    with psycopg.connect(url, autocommit=True) as connection:
        connection.execute(sql.SQL("CREATE SCHEMA {}").format(sql.Identifier(isolated)))
    original = os.environ["CITYSENSE_DATABASE_URL"]
    endpoint_url = url.replace(schema, isolated)
    os.environ["CITYSENSE_DATABASE_URL"] = endpoint_url
    try:
        command.upgrade(config, "head")
        with psycopg.connect(endpoint_url) as connection:
            repo = seed(connection, request_fixture, observations_fixture)
            repo.add_place(
                SpatialPlace(
                    place_id="second-city-synthetic",
                    city_id="tbilisi-fixture",
                    name="No field observations",
                    longitude=44.8,
                    latitude=41.72,
                    source_id="synthetic-fixture",
                    license_id="CC0-synthetic",
                    retrieved_at=request_fixture.decision_at,
                )
            )
        client = TestClient(create_app(Settings(api_key="x" * 32, database_url=endpoint_url)))
        headers = {"X-API-Key": "x" * 32}
        params = dict(
            longitude=41.63,
            latitude=41.65,
            radius_m=2000,
            decision_at=request_fixture.decision_at.isoformat(),
            limit=1,
        )
        response = client.get("/v1/cities/batumi/places", params=params, headers=headers)
        assert response.status_code == 200 and response.json()["truncated"]
        pid = request_fixture.places[0].place_id
        assert (
            client.get(
                f"/v1/cities/batumi/places/{pid}",
                params={"decision_at": params["decision_at"]},
                headers=headers,
            ).status_code
            == 200
        )
        assert (
            client.get(
                f"/v1/cities/tbilisi-fixture/places/{pid}",
                params={"decision_at": params["decision_at"]},
                headers=headers,
            ).status_code
            == 404
        )
        assert (
            client.get("/v1/cities/unauthorized/places", params=params, headers=headers).status_code
            == 403
        )
        assert (
            client.get(
                "/v1/cities/batumi/places", params={**params, "radius_m": 10001}, headers=headers
            ).status_code
            == 422
        )
        assert (
            client.get(
                "/v1/cities/batumi/places", params={**params, "longitude": "NaN"}, headers=headers
            ).status_code
            == 422
        )
        query = {
            "decision_at": params["decision_at"],
            "target_time": request_fixture.target_time.isoformat(),
            "place_ids": [pid],
        }
        assert (
            client.post("/v1/cities/batumi/state", json=query, headers=headers).status_code == 200
        )
        bad = client.post(
            "/v1/cities/batumi/state", json={**query, "place_ids": [pid, pid]}, headers=headers
        )
        assert bad.status_code == 422 and "input" not in str(bad.json())
        comparison = {
            "decision_at": params["decision_at"],
            "target_time": request_fixture.target_time.isoformat(),
            "need": request_fixture.need.value,
            "candidates": [
                {"place_id": p.place_id, "walk_minutes": p.walk_minutes}
                for p in request_fixture.places
            ],
        }
        for path in ("comparison", "suitability"):
            assessed = client.post(f"/v1/cities/batumi/{path}", json=comparison, headers=headers)
            assert assessed.status_code == 200
            assessment = assessed.json()["assessment"]
            assert "stored evidence" in assessment.pop("warning")
            assert assessment == evaluate(request_fixture).model_dump(
                mode="json", exclude={"warning"}
            )
        second = client.post(
            "/v1/cities/tbilisi-fixture/suitability",
            headers=headers,
            json={
                **comparison,
                "candidates": [{"place_id": "second-city-synthetic", "walk_minutes": 5}],
            },
        )
        assert (
            second.status_code == 200 and second.json()["assessment"]["ranked"][0]["score"] is None
        )
        with psycopg.connect(endpoint_url) as connection:
            assert connection.execute("SELECT count(*) FROM feature_snapshots").fetchone()[0] == 0
    finally:
        os.environ["CITYSENSE_DATABASE_URL"] = original
        with psycopg.connect(url, autocommit=True) as connection:
            connection.execute(sql.SQL("DROP SCHEMA {} CASCADE").format(sql.Identifier(isolated)))
