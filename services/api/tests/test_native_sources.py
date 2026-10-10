import json
from datetime import UTC, datetime

import httpx
import pytest

from citysense.ingestion import SourceMetadata
from citysense.native_sources import (
    Bounds,
    NativeRetriever,
    RetrievedPayload,
    parse_open_meteo,
    parse_overpass_count,
)

AT = datetime(2026, 10, 9, 10, tzinfo=UTC)


def source(provider="osm-overpass", live=False):
    return SourceMetadata(
        source_id=provider,
        source_version="test-v1",
        license_id="fixture-only",
        synthetic=not live,
        research_allowed=live,
        commercial_allowed=False,
        cache_allowed=live,
        redistribution_allowed=False,
        attribution_required=True,
        terms_url="https://www.openstreetmap.org/copyright" if live else None,
        reviewed_at=AT if live else None,
    )


def count_payload(**changes):
    data = {
        "osm3s": {"timestamp_osm_base": "2026-10-09T09:59:00Z"},
        "elements": [
            {"type": "count", "tags": {"nodes": "0", "ways": "3", "relations": "0", "total": "3"}}
        ],
    }
    data.update(changes)
    return RetrievedPayload(json.dumps(data).encode(), AT, "fixture")


def test_count_mapping_is_a_spatial_aggregate_not_a_scoring_fraction():
    bounds = Bounds(west=41.62, south=41.64, east=41.63, north=41.65)
    result = parse_overpass_count(count_payload(), bounds, source(), "sample")
    assert result.value == 3 and result.unit == "count"
    assert result.feature_key == "park_way_count" and result.spatial_resolution_m is None
    assert result.observed_or_valid_at == AT and result.retrieved_at == AT
    assert result.data_kind.value == "derived" and result.quality.value == "derived_spatial"
    assert "out count" in bounds.query


@pytest.mark.parametrize(
    "data",
    [
        {"remark": "runtime error"},
        {"elements": [{"type": "node", "id": 1}]},
        {
            "elements": [
                {
                    "type": "count",
                    "tags": {"nodes": "0", "ways": "-1", "relations": "0", "total": "-1"},
                }
            ]
        },
        {"osm3s": {"timestamp_osm_base": "2026-10-10T09:00:00Z"}},
    ],
)
def test_count_rejects_partial_nonaggregate_or_future_data(data):
    with pytest.raises(ValueError):
        parse_overpass_count(
            count_payload(**data),
            Bounds(west=1, south=1, east=1.01, north=1.01),
            source(),
            "sample",
        )


@pytest.mark.parametrize(
    "bounds",
    [
        dict(west=1, south=1, east=2, north=2),
        dict(west=float("nan"), south=1, east=1.01, north=1.01),
        dict(west=2, south=1, east=1, north=1.01),
    ],
)
def test_query_bounds_reject_invalid_or_large_areas(bounds):
    with pytest.raises(ValueError):
        Bounds(**bounds)


def weather_payload(**changes):
    data = {
        "latitude": 41.65,
        "longitude": 41.63,
        "utc_offset_seconds": 0,
        "hourly_units": {"time": "iso8601", "temperature_2m": "°F", "wind_speed_10m": "km/h"},
        "hourly": {
            "time": ["2026-10-09T12:00", "2026-10-09T13:00"],
            "temperature_2m": [68, None],
            "wind_speed_10m": [36, None],
        },
    }
    data.update(changes)
    return RetrievedPayload(json.dumps(data).encode(), AT, "fixture")


def test_forecast_units_nulls_and_unknown_issuance_are_preserved():
    result = parse_open_meteo(weather_payload(), source("open-meteo"), "batumi")
    assert result[0].temperature_c == 20 and result[0].wind_m_s == 10
    assert result[1].temperature_c is None and result[1].wind_m_s is None
    assert result[0].issued_at is None and not result[0].historical_replay_eligible
    assert result[0].valid_at.tzinfo == UTC


@pytest.mark.parametrize(
    "data",
    [
        dict(latitude=100),
        dict(utc_offset_seconds=14400),
        dict(
            hourly_units={"time": "iso8601", "temperature_2m": "Kelvin", "wind_speed_10m": "km/h"}
        ),
        dict(
            hourly={
                "time": ["2026-10-09T12:00"],
                "temperature_2m": [float("nan")],
                "wind_speed_10m": [2],
            }
        ),
    ],
)
def test_forecast_rejects_unknown_units_coordinates_offsets_and_nan(data):
    with pytest.raises(ValueError):
        parse_open_meteo(weather_payload(**data), source("open-meteo"), "batumi")


def test_live_gate_prevents_unreviewed_network_calls():
    with httpx.Client(
        transport=httpx.MockTransport(lambda request: pytest.fail("Network was called"))
    ) as client:
        with pytest.raises(PermissionError):
            NativeRetriever(source(), client).fetch("overpass", {"data": "fixture"})


def test_bounded_retry_local_receipt_and_archive(tmp_path):
    calls = []

    def handler(request):
        calls.append(request)
        return (
            httpx.Response(429, headers={"Retry-After": "0"})
            if len(calls) == 1
            else httpx.Response(200, content=count_payload().raw)
        )

    with httpx.Client(transport=httpx.MockTransport(handler)) as client:
        result = NativeRetriever(
            source(live=True), client, sleep=lambda _: None, clock=lambda: AT
        ).fetch("overpass", {"data": "fixture"})
    assert len(calls) == 2 and result.retrieved_at == AT
    archive = result.archive(tmp_path, source(live=True))
    assert archive.read_bytes() == result.raw
    with pytest.raises(FileExistsError):
        result.archive(tmp_path, source(live=True))
    with pytest.raises(PermissionError):
        result.archive(tmp_path, source())


@pytest.mark.parametrize(
    "response",
    [
        httpx.Response(302, headers={"Location": "https://example.com"}),
        httpx.Response(429, headers={"Retry-After": "1000"}),
        httpx.Response(200, content=b"x" * 262145),
    ],
)
def test_native_retrieval_rejects_redirect_deferred_retry_and_oversize(response):
    with httpx.Client(transport=httpx.MockTransport(lambda request: response)) as client:
        with pytest.raises((httpx.HTTPStatusError, RuntimeError, ValueError)):
            NativeRetriever(source(live=True), client, sleep=lambda _: None).fetch("overpass", {})
