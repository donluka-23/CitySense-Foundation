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
from psycopg.types.json import Jsonb

from citysense.app import create_app
from citysense.db import Repository
from citysense.engine import evaluate
from citysense.models import DataKind, Feature, FeatureQuality, FeatureSnapshot, SpatialPlace
from citysense.parameters import load_parameters
from citysense.security import Settings

pytestmark = pytest.mark.integration


def seed(connection, request, observations):
    repository = Repository(connection)
    repository.add_source(
        "synthetic-fixture", json.loads((FIXTURES / "source-metadata.json").read_text())
    )
    for i, place in enumerate(request.places):
        repository.add_place(
            SpatialPlace(
                place_id=place.place_id,
                city_id="batumi",
                name=place.name,
                longitude=41.63 + i * 0.01,
                latitude=41.65,
                source_id="synthetic-fixture",
                license_id="CC0-synthetic",
                retrieved_at=request.decision_at - timedelta(days=1),
            )
        )
    for observation in observations:
        repository.add_observation(observation)
    repository.add_model(load_parameters())
    return repository


def snapshot(request):
    parameters = load_parameters()
    return FeatureSnapshot(
        snapshot_id=uuid4(),
        build_version="identity-normalized-v1",
        created_at=request.decision_at + timedelta(minutes=1),
        request=request,
        model_version=parameters.version,
        parameter_hash=parameters.digest,
    )


def test_real_spatial_storage_units_and_index(
    db_connection, request_fixture, observations_fixture, spatial_database
):
    repository = seed(db_connection, request_fixture, observations_fixture)
    assert repository.nearby(41.63, 41.65, 100, "batumi") == [request_fixture.places[0].place_id]
    assert len(repository.nearby(41.63, 41.65, 1000, "batumi")) == 2
    assert repository.nearby(41.63, 41.65, 1000, "other-city") == []
    row = db_connection.execute(
        "SELECT ST_Distance(a.location,b.location) FROM places a, places b "
        "WHERE a.id=%s AND b.id=%s",
        (request_fixture.places[0].place_id, request_fixture.places[1].place_id),
    ).fetchone()
    assert 800 < row[0] < 900  # geodesic meters at Batumi latitude; not angular degrees
    db_connection.execute("SET LOCAL enable_seqscan=off")
    plan = db_connection.execute(
        "EXPLAIN SELECT id FROM places WHERE ST_DWithin(location,"
        "ST_SetSRID(ST_MakePoint(41.63,41.65),4326)::geography,100)"
    ).fetchall()
    assert "places_location_gist" in " ".join(row[0] for row in plan)
    row = db_connection.execute(
        "SELECT ST_SRID(location::geometry),ST_IsValid(location::geometry) FROM places LIMIT 1"
    ).fetchone()
    assert row == (4326, True)
    assert (
        repository.get_observation(observations_fixture[0].observation_id)
        == observations_fixture[0]
    )


def test_snapshot_replay_uses_historical_parameters(
    db_connection, request_fixture, observations_fixture
):
    repository = seed(db_connection, request_fixture, observations_fixture)
    saved = snapshot(request_fixture)
    repository.add_snapshot(saved)
    replayed, parameters = repository.replay(saved.snapshot_id)
    assert replayed == saved
    assert evaluate(replayed.request, parameters) == evaluate(request_fixture)
    assert db_connection.execute("SELECT count(*) FROM feature_snapshot_inputs").fetchone()[0] == 6


def test_forecast_history_and_future_knowledge_rejected(
    db_connection, request_fixture, observations_fixture
):
    repository = seed(db_connection, request_fixture, observations_fixture)
    observation = observations_fixture[0].model_copy(deep=True)
    observation.observation_id = uuid4()
    observation.data_kind = DataKind.FORECAST
    observation.quality = FeatureQuality.REGIONAL_FORECAST
    observation.observed_or_valid_at = request_fixture.target_time
    observation.issued_at = request_fixture.decision_at - timedelta(minutes=20)
    observation.retrieved_at = request_fixture.decision_at - timedelta(minutes=10)
    repository.add_observation(observation)
    request_fixture.places[0].feature_shade = Feature.model_validate(
        repository.get_observation(observation.observation_id).model_dump(
            exclude={"place_id", "feature_key"}
        )
    )
    saved = snapshot(request_fixture)
    repository.add_snapshot(saved)
    assert evaluate(repository.replay(saved.snapshot_id)[0].request).ranked[0].score == 0.73
    # Direct SQL must also reject caller payloads altered after their original validation.
    future = observation.model_copy(deep=True)
    future.observation_id = uuid4()
    future.issued_at = request_fixture.decision_at + timedelta(minutes=1)
    future.retrieved_at = request_fixture.decision_at + timedelta(minutes=2)
    repository.add_observation(future)
    malicious = saved.model_dump(mode="json")
    malicious["snapshot_id"] = str(uuid4())
    malicious["request"]["places"][0]["feature_shade"] = future.model_dump(
        mode="json", exclude={"place_id", "feature_key"}
    )
    with pytest.raises(psycopg.errors.RaiseException, match="future knowledge"):
        with db_connection.transaction():
            db_connection.execute(
                "INSERT INTO feature_snapshots(id,build_version,decision_at,target_time,"
                "created_at,model_version,parameter_hash,payload) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                (
                    malicious["snapshot_id"],
                    saved.build_version,
                    saved.request.decision_at,
                    saved.request.target_time,
                    saved.created_at,
                    saved.model_version,
                    saved.parameter_hash,
                    Jsonb(malicious),
                ),
            )


def test_snapshot_forged_values_and_unlinked_features_rejected(
    db_connection, request_fixture, observations_fixture
):
    repository = seed(db_connection, request_fixture, observations_fixture)
    request_fixture.places[0].feature_shade.value = 0.1
    with pytest.raises(psycopg.errors.RaiseException, match="evidence mismatch"):
        repository.add_snapshot(snapshot(request_fixture))
    request_fixture.places[0].feature_shade.value = 0.8
    request_fixture.places[0].feature_shade.observation_id = None
    with pytest.raises(psycopg.errors.RaiseException, match="stored observation"):
        repository.add_snapshot(snapshot(request_fixture))


@pytest.mark.parametrize(
    "statement",
    [
        "UPDATE observations SET feature_value=.1",
        "DELETE FROM observations",
        "UPDATE places SET latitude=0",
        "UPDATE model_versions SET parameter_hash=repeat('0',64)",
    ],
)
def test_append_only_guards(db_connection, request_fixture, observations_fixture, statement):
    seed(db_connection, request_fixture, observations_fixture)
    with pytest.raises(psycopg.errors.RaiseException, match="append-only"):
        with db_connection.transaction():
            db_connection.execute(statement)


def test_database_coordinate_and_forecast_constraints(
    db_connection, request_fixture, observations_fixture
):
    seed(db_connection, request_fixture, observations_fixture)
    with pytest.raises(psycopg.errors.CheckViolation):
        with db_connection.transaction():
            db_connection.execute(
                "INSERT INTO places(id,city_id,label,longitude,latitude,source_id,"
                "source_license,retrieved_at) VALUES ('invalid','batumi','bad',200,41.65,"
                "'synthetic-fixture','CC0-synthetic',now())"
            )
    with pytest.raises(ValueError):
        Repository(db_connection).nearby(float("nan"), 41.65, 10, "batumi")


def test_database_rejects_payload_column_disagreement(
    db_connection, request_fixture, observations_fixture
):
    seed(db_connection, request_fixture, observations_fixture)
    with pytest.raises(psycopg.errors.RaiseException, match="disagree"):
        with db_connection.transaction():
            db_connection.execute(
                "INSERT INTO observations SELECT %s,place_id,feature_key,feature_value,"
                "unit,data_kind,quality_class,source_id,source_version,source_license,valid_at,valid_until,"
                "issued_at,retrieved_at,method_version,spatial_resolution_m,payload FROM observations LIMIT 1",
                (uuid4(),),
            )


def test_real_replay_endpoint(spatial_database, request_fixture, observations_fixture):
    url, schema, config = spatial_database
    isolated_schema = schema + "_endpoint"
    with psycopg.connect(url, autocommit=True) as connection:
        connection.execute(sql.SQL("CREATE SCHEMA {}").format(sql.Identifier(isolated_schema)))
    original = os.environ["CITYSENSE_DATABASE_URL"]
    endpoint_url = url.replace(schema, isolated_schema)
    os.environ["CITYSENSE_DATABASE_URL"] = endpoint_url
    try:
        command.upgrade(config, "head")
        saved = snapshot(request_fixture)
        with psycopg.connect(endpoint_url) as connection:
            seed(connection, request_fixture, observations_fixture).add_snapshot(saved)
        client = TestClient(create_app(Settings(database_url=endpoint_url)))
        response = client.get(f"/v1/replay/{saved.snapshot_id}")
        assert response.status_code == 200
        assert response.json() == evaluate(request_fixture).model_dump(mode="json")
        assert client.get(f"/v1/replay/{uuid4()}").status_code == 404
    finally:
        os.environ["CITYSENSE_DATABASE_URL"] = original
        with psycopg.connect(url, autocommit=True) as connection:
            connection.execute(
                sql.SQL("DROP SCHEMA {} CASCADE").format(sql.Identifier(isolated_schema))
            )


def test_migration_head_and_roundtrip(spatial_database):
    url, schema, config = spatial_database
    with psycopg.connect(url) as connection:
        assert connection.execute("SELECT version_num FROM alembic_version").fetchone() == ("0002",)
    # Independent schema prevents this destructive round-trip touching other test evidence.
    isolated_schema = schema + "_migration"
    with psycopg.connect(url, autocommit=True) as connection:
        connection.execute(sql.SQL("CREATE SCHEMA {}").format(sql.Identifier(isolated_schema)))
    original = os.environ["CITYSENSE_DATABASE_URL"]
    os.environ["CITYSENSE_DATABASE_URL"] = url.replace(schema, isolated_schema)
    try:
        command.upgrade(config, "head")
        command.upgrade(config, "head")
        command.downgrade(config, "base")
        command.upgrade(config, "head")
    finally:
        os.environ["CITYSENSE_DATABASE_URL"] = original
        with psycopg.connect(url, autocommit=True) as connection:
            connection.execute(
                sql.SQL("DROP SCHEMA {} CASCADE").format(sql.Identifier(isolated_schema))
            )
