"""Provider-native parsing and bounded, explicitly invoked retrieval; no startup feeds."""

import hashlib
import json
import random
import time
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, Literal, Self
from uuid import NAMESPACE_URL, uuid5

import httpx
from pydantic import AwareDatetime, Field, model_validator

from .ingestion import SourceMetadata
from .models import Contract, DataKind, FeatureQuality, Identifier, Observation

ENDPOINTS = {
    "overpass": "https://overpass-api.de/api/interpreter",
    "open_meteo": "https://api.open-meteo.com/v1/forecast",
}


class Bounds(Contract):
    west: float = Field(ge=-180, le=180)
    south: float = Field(ge=-90, le=90)
    east: float = Field(ge=-180, le=180)
    north: float = Field(ge=-90, le=90)

    @model_validator(mode="after")
    def small_area(self) -> Self:
        if not 0 < self.east - self.west <= 0.05 or not 0 < self.north - self.south <= 0.05:
            raise ValueError("Native count demonstration requires a small bounding box")
        return self

    @property
    def query(self) -> str:
        # Only numeric bounds; no arbitrary user-supplied Overpass expressions or tags.
        return (
            f'[out:json][timeout:15][maxsize:1048576];way["leisure"="park"]'
            f"({self.south},{self.west},{self.north},{self.east});out count;"
        )


@dataclass(frozen=True)
class RetrievedPayload:
    raw: bytes
    retrieved_at: datetime
    endpoint: str

    @property
    def sha256(self) -> str:
        return hashlib.sha256(self.raw).hexdigest()

    def archive(self, directory: Path, source: SourceMetadata) -> Path:
        source = SourceMetadata.model_validate(source.model_dump())
        if not source.cache_allowed:
            raise PermissionError("Raw response storage is not permitted")
        directory.mkdir(parents=True, exist_ok=True)
        path = directory / (self.sha256 + ".raw.json")
        with path.open("xb") as output:
            output.write(self.raw)
        return path


class NativeRetriever:
    def __init__(
        self,
        source: SourceMetadata,
        client: httpx.Client,
        *,
        sleep: Callable[[float], None] = time.sleep,
        clock: Callable[[], datetime] = lambda: datetime.now(UTC),
    ) -> None:
        self.source = SourceMetadata.model_validate(source.model_dump())
        self.client, self.sleep, self.clock = client, sleep, clock

    def fetch(
        self, provider: Literal["overpass", "open_meteo"], parameters: dict[str, str]
    ) -> RetrievedPayload:
        if self.source.synthetic or not self.source.research_allowed:
            raise PermissionError("Live retrieval requires explicitly reviewed research access")
        expected_source = "osm-overpass" if provider == "overpass" else "open-meteo"
        if self.source.source_id != expected_source:
            raise ValueError("Source metadata does not match provider")
        endpoint = ENDPOINTS[provider]
        for attempt in range(2):
            try:
                with self.client.stream(
                    "GET", endpoint, params=parameters, timeout=20, follow_redirects=False
                ) as response:
                    if response.status_code == 429 or response.status_code >= 500:
                        if attempt == 1:
                            raise RuntimeError(
                                "Provider temporarily unavailable; no cached substitution"
                            )
                        delay = response.headers.get("Retry-After")
                        if delay is not None and (not delay.isdigit() or int(delay) > 10):
                            raise RuntimeError("Provider requested deferred retrieval")
                        self.sleep(float(delay) if delay else 1 + random.SystemRandom().random())
                        continue
                    response.raise_for_status()
                    raw = bytearray()
                    for chunk in response.iter_bytes():
                        raw.extend(chunk)
                        if len(raw) > 262144:
                            raise ValueError("Native response exceeds archive bound")
                    received_at = self.clock()
                    if received_at.tzinfo is None:
                        raise ValueError("Retrieval clock must have timezone")
                    return RetrievedPayload(bytes(raw), received_at.astimezone(UTC), endpoint)
            except (httpx.TimeoutException, httpx.NetworkError):
                if attempt == 1:
                    raise RuntimeError("Provider transport unavailable") from None
                self.sleep(1 + random.SystemRandom().random())
        raise RuntimeError("Provider retrieval exhausted")


def parse_overpass_count(
    payload: RetrievedPayload, bounds: Bounds, source: SourceMetadata, place_id: str
) -> Observation:
    bounds = Bounds.model_validate(bounds.model_dump())
    source = SourceMetadata.model_validate(source.model_dump())
    if source.source_id != "osm-overpass":
        raise ValueError("Wrong source for Overpass payload")
    data = json.loads(payload.raw)
    if set(data) - {"version", "generator", "osm3s", "elements", "remark"}:
        raise ValueError("Unexpected nonaggregate payload metadata")
    if "remark" in data:
        raise ValueError("Overpass returned partial/error data")
    elements = data["elements"]
    if len(elements) != 1 or elements[0]["type"] != "count":
        raise ValueError("Only aggregate-only Overpass payloads are accepted")
    if set(elements[0]) - {"type", "id", "tags"} or set(data["osm3s"]) - {
        "timestamp_osm_base",
        "timestamp_areas_base",
        "copyright",
    }:
        raise ValueError("Unexpected individual metadata in aggregate response")
    tags = elements[0]["tags"]
    if set(tags) != {"nodes", "ways", "relations", "total"}:
        raise ValueError("Unexpected count fields")
    if any(
        not isinstance(value, str) or not value.isascii() or not value.isdigit()
        for value in tags.values()
    ):
        raise ValueError("Counts must be nonnegative integers")
    if int(tags["nodes"]) or int(tags["relations"]) or int(tags["ways"]) != int(tags["total"]):
        raise ValueError("Count differs from bounded park-way query")
    snapshot_time = datetime.fromisoformat(
        data["osm3s"]["timestamp_osm_base"].replace("Z", "+00:00")
    )
    if snapshot_time.tzinfo is None or snapshot_time > payload.retrieved_at:
        raise ValueError("Invalid provider database snapshot time")
    return Observation(
        observation_id=uuid5(
            NAMESPACE_URL, place_id + payload.sha256 + payload.retrieved_at.isoformat()
        ),
        place_id=place_id,
        feature_key="park_way_count",
        value=int(tags["ways"]),
        unit="count",
        quality=FeatureQuality.DERIVED_SPATIAL,
        data_kind=DataKind.DERIVED,
        source_id=source.source_id,
        source_version=source.source_version,
        license_id=source.license_id,
        observed_or_valid_at=payload.retrieved_at,
        retrieved_at=payload.retrieved_at,
        method_version="bounded-osm-park-way-count-v1",
        spatial_resolution_m=None,
        quality_metadata={
            "raw_sha256": payload.sha256,
            "provider_database_at": snapshot_time.astimezone(UTC).isoformat(),
            "query_sha256": hashlib.sha256(bounds.query.encode()).hexdigest(),
            "bounds_wgs84": json.dumps(bounds.model_dump(), sort_keys=True),
            "interpretation": "Mapped way count; not park area, greenery fraction or microclimate",
        },
    )


class WeatherSample(Contract):
    city_id: Identifier
    longitude: float = Field(ge=-180, le=180)
    latitude: float = Field(ge=-90, le=90)
    valid_at: AwareDatetime
    valid_until: AwareDatetime
    retrieved_at: AwareDatetime
    issued_at: None = None
    temperature_c: float | None
    wind_m_s: float | None = Field(ge=0)
    source: SourceMetadata
    raw_sha256: str = Field(pattern="^[a-f0-9]{64}$")
    data_kind: Literal["forecast_candidate"] = "forecast_candidate"
    quality: Literal["regional_forecast"] = "regional_forecast"
    historical_replay_eligible: Literal[False] = False
    spatial_resolution_m: None = None
    uncertainty: str = "Ordinary forecast API lacks authenticated issuance/run metadata; grid resolution unconfirmed"


def parse_open_meteo(
    payload: RetrievedPayload, source: SourceMetadata, city_id: str
) -> list[WeatherSample]:
    source = SourceMetadata.model_validate(source.model_dump())
    if source.source_id != "open-meteo":
        raise ValueError("Wrong source for weather payload")
    data: dict[str, Any] = json.loads(payload.raw)
    if data.get("error") or data.get("utc_offset_seconds") != 0:
        raise ValueError("Weather parser requires a successful UTC response")
    hourly, units = data["hourly"], data["hourly_units"]
    times = hourly["time"]
    if not 1 <= len(times) <= 384 or len(set(times)) != len(times):
        raise ValueError("Invalid hourly forecast horizon")
    if (
        units["time"] != "iso8601"
        or units["temperature_2m"] not in ("°C", "°F")
        or units["wind_speed_10m"] not in ("m/s", "km/h")
    ):
        raise ValueError("Unknown provider units")
    temperatures, winds = hourly["temperature_2m"], hourly["wind_speed_10m"]
    if len(temperatures) != len(times) or len(winds) != len(times):
        raise ValueError("Mismatched hourly arrays")
    result: list[WeatherSample] = []
    previous: datetime | None = None
    for timestamp, temperature, wind in zip(times, temperatures, winds, strict=True):
        valid = datetime.fromisoformat(timestamp)
        valid = valid.replace(tzinfo=UTC) if valid.tzinfo is None else valid.astimezone(UTC)
        if previous is not None and valid - previous != timedelta(hours=1):
            raise ValueError("Forecast hours are not contiguous")
        previous = valid
        if any(
            v is not None and (isinstance(v, bool) or not isinstance(v, (int, float)))
            for v in (temperature, wind)
        ):
            raise ValueError("Invalid weather value")
        celsius = (
            temperature
            if temperature is None or units["temperature_2m"] == "°C"
            else (temperature - 32) * 5 / 9
        )
        meters = wind if wind is None or units["wind_speed_10m"] == "m/s" else wind / 3.6
        result.append(
            WeatherSample(
                city_id=city_id,
                longitude=data["longitude"],
                latitude=data["latitude"],
                valid_at=valid,
                valid_until=valid + timedelta(hours=1),
                retrieved_at=payload.retrieved_at,
                temperature_c=celsius,
                wind_m_s=meters,
                source=source,
                raw_sha256=payload.sha256,
            )
        )
    return result
