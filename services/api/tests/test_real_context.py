import importlib.util
import json
import sys
from datetime import timedelta
from pathlib import Path
from uuid import uuid4

import pytest
from test_postgis import seed, snapshot

from citysense.db import Repository
from citysense.engine import evaluate
from citysense.ingestion import SourceMetadata
from citysense.models import Need
from citysense.native_sources import Bounds, RetrievedPayload
from citysense.platform import AccessContext, IntelligenceService, SearchQuery, SuitabilityQuery
from citysense.real_context import park_geometry_query, parse_park_geometry


def invented_geometry(at):
    # Invented provider payload for parser tests, not a real-world acquisition.
    return {
        "version": 0.6,
        "generator": "invented-test-provider",
        "osm3s": {
            "timestamp_osm_base": (at - timedelta(minutes=1)).isoformat(),
            "copyright": "test only",
        },
        "elements": [
            {
                "type": "way",
                "id": 123,
                "nodes": [1, 2],
                "geometry": [{"lat": 41.65, "lon": 41.625}, {"lat": 41.649, "lon": 41.626}],
            }
        ],
    }


def metadata(at):
    return SourceMetadata(
        source_id="osm-overpass",
        source_version="test-geometry-v1",
        license_id="ODbL-1.0",
        synthetic=False,
        research_allowed=True,
        commercial_allowed=False,
        cache_allowed=True,
        redistribution_allowed=False,
        attribution_required=True,
        terms_url="https://www.openstreetmap.org/copyright",
        reviewed_at=at,
    )


def test_geometry_is_a_real_vertex_never_greenery(request_fixture):
    at = request_fixture.decision_at
    bounds = Bounds(west=41.615, south=41.638, east=41.635, north=41.658)
    payload = RetrievedPayload(json.dumps(invented_geometry(at)).encode(), at, "test://invented")
    inventory = parse_park_geometry(payload, bounds, metadata(at))
    assert inventory.places[0].longitude == 41.625
    assert inventory.places[0].place_id == "batumi:osm:way:123"
    assert "boundary" in inventory.geometry_warning.lower()
    assert "skel geom 5" in park_geometry_query(bounds)
    assert "feature_greenery" not in inventory.model_dump_json()


@pytest.mark.parametrize(
    "mutation",
    ["contacts", "author", "partial", "future", "nan", "duplicate", "outside", "count", "empty"],
)
def test_geometry_rejects_unbounded_personal_invalid_or_future_payload(request_fixture, mutation):
    at = request_fixture.decision_at
    body = invented_geometry(at)
    if mutation == "contacts":
        body["elements"][0]["tags"] = {"contact:phone": "invented"}
    elif mutation == "author":
        body["elements"][0]["user"] = "invented-contributor"
    elif mutation == "partial":
        body["remark"] = "timeout"
    elif mutation == "future":
        body["osm3s"]["timestamp_osm_base"] = (at + timedelta(seconds=1)).isoformat()
    elif mutation == "nan":
        body["elements"][0]["geometry"][0]["lon"] = float("nan")
    elif mutation == "duplicate":
        body["elements"].append(body["elements"][0])
    elif mutation == "outside":
        body["elements"][0]["geometry"] = [{"lon": 0, "lat": 0}] * 2
    elif mutation == "count":
        body["elements"][0]["type"] = "count"
    else:
        body["elements"] = []
    with pytest.raises(ValueError):
        parse_park_geometry(
            RetrievedPayload(json.dumps(body).encode(), at, "test://invented"),
            Bounds(west=41.615, south=41.638, east=41.635, north=41.658),
            metadata(at),
        )


@pytest.mark.integration
def test_local_research_access_never_becomes_transport_permission(db_connection, request_fixture):
    repo = Repository(db_connection)
    at = request_fixture.decision_at
    data = parse_park_geometry(
        RetrievedPayload(json.dumps(invented_geometry(at)).encode(), at, "test://invented"),
        Bounds(west=41.615, south=41.638, east=41.635, north=41.658),
        metadata(at),
    )
    repo.add_source(data.source.source_id, data.source.model_dump(mode="json"))
    for place in data.places:
        repo.add_place(place)
    cities, scopes = frozenset({"batumi"}), frozenset({"city.read", "suitability.read"})
    public = IntelligenceService(db_connection, AccessContext("operator", cities, scopes))
    local = IntelligenceService(
        db_connection, AccessContext("operator", cities, scopes, audience="local_research")
    )
    query = SearchQuery(longitude=41.625, latitude=41.65, radius_m=100, decision_at=at)
    assert not public.search_places("batumi", query).places
    assert len(local.search_places("batumi", query).places) == 1
    with pytest.raises(PermissionError):
        public.get_place_details("batumi", data.places[0].place_id, at)
    result = local.evaluate_suitability(
        "batumi",
        SuitabilityQuery(
            need=Need.QUIET_REST,
            decision_at=at,
            target_time=at,
            candidates=[{"place_id": data.places[0].place_id, "walk_minutes": 20}],
        ),
    )
    assert result.assessment.ranked[0].score is None
    assert set(result.assessment.ranked[0].reasons) == {
        "feature_greenery:unavailable",
        "feature_traffic_proximity:unavailable",
    }
    with pytest.raises(ValueError):
        AccessContext("operator", cities, scopes, purpose="commercial", audience="local_research")


@pytest.mark.integration
def test_quiet_rest_jsonb_replay_preserves_exact_reason_order(
    db_connection, request_fixture, observations_fixture
):
    repo = seed(db_connection, request_fixture, observations_fixture)
    request = request_fixture.model_copy(deep=True)
    request.need = Need.QUIET_REST
    for p in request.places:
        p.feature_greenery = None
        p.feature_traffic_proximity = None
    frozen = snapshot(request)
    frozen.snapshot_id = uuid4()
    repo.add_snapshot(frozen)
    saved, parameters = repo.replay(frozen.snapshot_id)
    assert evaluate(saved.request, parameters) == evaluate(request)


def test_acquisition_validates_privacy_before_raw_archive(tmp_path, monkeypatch, request_fixture):
    spec = importlib.util.spec_from_file_location(
        "real_workflow", Path(__file__).parents[1] / "scripts/real_workflow.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    at = request_fixture.decision_at
    body = invented_geometry(at)
    body["elements"][0]["user"] = "invented-contributor-must-not-be-stored"
    payload = RetrievedPayload(json.dumps(body).encode(), at, "test://invented")
    monkeypatch.setattr(module.NativeRetriever, "fetch", lambda *args: payload)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "real_workflow",
            "--acquire",
            "--inventory",
            str(tmp_path / "inventory.json"),
            "--output",
            str(tmp_path / "raw"),
        ],
    )
    with pytest.raises(ValueError, match="skeleton"):
        module.main()
    assert not list(tmp_path.rglob("*.json"))
