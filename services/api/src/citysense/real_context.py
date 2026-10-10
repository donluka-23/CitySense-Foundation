"""Small OSM geometry inventory; no park-count-to-greenery or synthetic features."""

import json
from datetime import datetime
from typing import Self

from pydantic import AwareDatetime, Field, model_validator

from .ingestion import SourceMetadata
from .models import Contract, SpatialPlace
from .native_sources import Bounds, RetrievedPayload


def park_geometry_query(bounds: Bounds) -> str:
    bounds = Bounds.model_validate(bounds.model_dump())
    # Skeleton geometry excludes contributor identities, contacts and free-form tags upstream.
    return (
        f'[out:json][timeout:15][maxsize:1048576];way["leisure"="park"]'
        f"({bounds.south},{bounds.west},{bounds.north},{bounds.east});out skel geom 5;"
    )


class RealInventory(Contract):
    source: SourceMetadata
    bounds: Bounds
    query: str
    raw_sha256: str = Field(pattern="^[a-f0-9]{64}$")
    retrieved_at: AwareDatetime
    provider_database_at: AwareDatetime
    places: list[SpatialPlace] = Field(min_length=1, max_length=5)
    geometry_method: str = "first_returned_vertex_in_query_window_v1"
    geometry_warning: str = "OSM boundary vertex; not a verified entrance or interior activity site"
    attribution: str = "© OpenStreetMap contributors; ODbL 1.0"

    @model_validator(mode="after")
    def coherent(self) -> Self:
        if self.source.synthetic or self.provider_database_at > self.retrieved_at:
            raise ValueError("Invalid real source chronology")
        if (
            not self.source.research_allowed
            or not self.source.cache_allowed
            or len({p.place_id for p in self.places}) != len(self.places)
            or self.query != park_geometry_query(self.bounds)
        ):
            raise ValueError("Inventory outside research envelope")
        for p in self.places:
            if (p.city_id, p.source_id, p.license_id, p.retrieved_at) != (
                "batumi",
                self.source.source_id,
                self.source.license_id,
                self.retrieved_at,
            ):
                raise ValueError("Inventory lineage mismatch")
            if not (
                self.bounds.west <= p.longitude <= self.bounds.east
                and self.bounds.south <= p.latitude <= self.bounds.north
            ):
                raise ValueError("Inventory point outside window")
        return self


def parse_park_geometry(
    payload: RetrievedPayload, bounds: Bounds, source: SourceMetadata
) -> RealInventory:
    if source.source_id != "osm-overpass":
        raise ValueError("Wrong geometry provider")
    data = json.loads(payload.raw)
    if set(data) - {"version", "generator", "osm3s", "elements"}:
        raise ValueError("Unexpected or partial geometry response")
    if set(data["osm3s"]) - {"timestamp_osm_base", "timestamp_areas_base", "copyright"}:
        raise ValueError("Unexpected geometry metadata")
    elements = data["elements"]
    if not 1 <= len(elements) <= 5:
        raise ValueError("Geometry inventory must contain one to five ways")
    places = []
    for item in elements:
        if set(item) - {"type", "id", "nodes", "bounds", "geometry"} or item["type"] != "way":
            raise ValueError("Only tag-free skeleton way geometries are accepted")
        if type(item["id"]) is not int or item["id"] <= 0:
            raise ValueError("Invalid OSM identity")
        points = item["geometry"]
        if not 2 <= len(points) <= 10000:
            raise ValueError("Invalid bounded geometry")
        normalized = []
        for p in points:
            if set(p) != {"lat", "lon"}:
                raise ValueError("Unexpected point properties")
            # Validate all vertices, including ones outside the small selection window.
            point = SpatialPlace(
                place_id="check",
                city_id="batumi",
                name="check",
                longitude=p["lon"],
                latitude=p["lat"],
                source_id=source.source_id,
                license_id=source.license_id,
                retrieved_at=payload.retrieved_at,
            )
            if (
                bounds.west <= point.longitude <= bounds.east
                and bounds.south <= point.latitude <= bounds.north
            ):
                normalized.append(point)
        if not normalized:
            raise ValueError("No actual vertex in bounded window")
        point = normalized[0]
        places.append(
            point.model_copy(
                update={
                    "place_id": f"batumi:osm:way:{item['id']}",
                    "name": f"OSM mapped park way {item['id']} (boundary point)",
                }
            )
        )
    return RealInventory(
        source=source,
        bounds=bounds,
        query=park_geometry_query(bounds),
        raw_sha256=payload.sha256,
        retrieved_at=payload.retrieved_at,
        provider_database_at=datetime.fromisoformat(
            data["osm3s"]["timestamp_osm_base"].replace("Z", "+00:00")
        ),
        places=places,
    )
