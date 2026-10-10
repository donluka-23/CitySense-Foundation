"""One explicit aggregate-only OSM request; no personal tags, polling or deployment."""

import argparse
import json
import os
from datetime import UTC, datetime
from pathlib import Path

import httpx
import psycopg

from citysense.db import Repository
from citysense.ingestion import SourceMetadata
from citysense.models import SpatialPlace
from citysense.native_sources import Bounds, NativeRetriever, parse_overpass_count


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--persist", action="store_true")
    args = parser.parse_args()
    source = SourceMetadata(
        source_id="osm-overpass",
        source_version="park-way-count-v1",
        license_id="ODbL-1.0",
        synthetic=False,
        research_allowed=True,
        commercial_allowed=True,
        cache_allowed=True,
        redistribution_allowed=False,
        attribution_required=True,
        terms_url="https://www.openstreetmap.org/copyright",
        reviewed_at=datetime.now(UTC),
    )
    bounds = Bounds(west=41.615, south=41.638, east=41.635, north=41.658)
    place_id = "batumi:research-unit:osm-count-demo"
    with httpx.Client(
        trust_env=False,
        headers={"User-Agent": "CitySense-local-research/0.3 (single aggregate query)"},
    ) as client:
        payload = NativeRetriever(source, client).fetch("overpass", {"data": bounds.query})
    observation = parse_overpass_count(payload, bounds, source, place_id)
    args.output.mkdir(parents=True, exist_ok=True)
    raw_path = payload.archive(args.output, source)
    manifest = {
        "synthetic": False,
        "endpoint": payload.endpoint,
        "query": bounds.query,
        "bounds": bounds.model_dump(),
        "raw_file": raw_path.name,
        "source": source.model_dump(mode="json"),
        "observation": observation.model_dump(mode="json"),
        "attribution": "© OpenStreetMap contributors, ODbL 1.0",
        "publication": "Private engineering demonstration; derivative database publication requires ODbL review",
        "persisted": args.persist,
    }
    if args.persist:
        with psycopg.connect(os.environ["CITYSENSE_DATABASE_URL"]) as connection:
            repository = Repository(connection)
            repository.add_source(source.source_id, source.model_dump(mode="json"))
            repository.add_place(
                SpatialPlace(
                    place_id=place_id,
                    city_id="batumi",
                    name="Research sampling window (not a park entity)",
                    longitude=41.625,
                    latitude=41.648,
                    source_id=source.source_id,
                    license_id=source.license_id,
                    retrieved_at=payload.retrieved_at,
                )
            )
            repository.add_observation(observation)
    with (args.output / "manifest.json").open("x", encoding="utf-8") as output:
        json.dump(manifest, output, indent=2, ensure_ascii=False)
        output.write("\n")
    print(
        f"Real mapped park-way count: {observation.value}; raw hash: {payload.sha256}; persisted: {args.persist}"
    )
    print("This count does not estimate greenery, shade, park area or suitability.")


if __name__ == "__main__":
    main()
