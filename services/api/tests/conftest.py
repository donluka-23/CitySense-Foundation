import json
import os
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit
from uuid import uuid4

import psycopg
import pytest
from alembic import command
from alembic.config import Config
from psycopg import sql

from citysense.models import EvaluateRequest, Observation

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture
def request_fixture():
    return EvaluateRequest.model_validate_json((FIXTURES / "request.json").read_text())


@pytest.fixture
def observations_fixture():
    data = json.loads((FIXTURES / "observations.json").read_text())
    return [Observation.model_validate(o) for o in data]


@pytest.fixture(scope="session")
def spatial_database():
    url = os.environ.get("CITYSENSE_TEST_DATABASE_URL")
    if not url:
        if os.environ.get("CITYSENSE_REQUIRE_DB") == "1":
            pytest.fail("CI requires a real PostGIS test URL")
        pytest.skip("CITYSENSE_TEST_DATABASE_URL is not configured")
    parts = urlsplit(url)
    if not parts.path.endswith("_test"):
        pytest.fail("Integration tests require a dedicated database with name ending _test")
    schema = "citysense_test_" + uuid4().hex
    with psycopg.connect(url, autocommit=True) as connection:
        connection.execute("CREATE EXTENSION IF NOT EXISTS postgis")
        connection.execute(sql.SQL("CREATE SCHEMA {}").format(sql.Identifier(schema)))
    query = dict(parse_qsl(parts.query))
    query["options"] = f"-csearch_path={schema},public"
    schema_url = urlunsplit(parts._replace(query=urlencode(query)))
    old = os.environ.get("CITYSENSE_DATABASE_URL")
    os.environ["CITYSENSE_DATABASE_URL"] = schema_url
    config = Config(str(Path(__file__).parents[1] / "alembic.ini"))
    try:
        command.upgrade(config, "head")
        yield schema_url, schema, config
    finally:
        if old is None:
            os.environ.pop("CITYSENSE_DATABASE_URL", None)
        else:
            os.environ["CITYSENSE_DATABASE_URL"] = old
        with psycopg.connect(url, autocommit=True) as connection:
            connection.execute(sql.SQL("DROP SCHEMA {} CASCADE").format(sql.Identifier(schema)))


@pytest.fixture
def db_connection(spatial_database):
    with psycopg.connect(spatial_database[0]) as connection:
        try:
            yield connection
        finally:
            connection.rollback()
