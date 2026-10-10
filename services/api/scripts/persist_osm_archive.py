"""Append the already captured aggregate; no second network request or evidence overwrite."""

import argparse
import json
import os
from pathlib import Path

import psycopg

from citysense.db import Repository
from citysense.ingestion import SourceMetadata
from citysense.models import Observation, SpatialPlace
from citysense.native_sources import Bounds, RetrievedPayload, parse_overpass_count


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("capture", type=Path)
    args = parser.parse_args()
    capture = args.capture.resolve()
    manifest = json.loads((capture / "manifest.json").read_text(encoding="utf-8"))
    source = SourceMetadata.model_validate(manifest["source"])
    bounds = Bounds.model_validate(manifest["bounds"])
    archived = Observation.model_validate(manifest["observation"])
    raw_path = (capture / manifest["raw_file"]).resolve()
    if raw_path.parent != capture or raw_path.stat().st_size > 262144:
        raise ValueError("Invalid archive path or size")
    payload = RetrievedPayload(raw_path.read_bytes(), archived.retrieved_at, manifest["endpoint"])
    if (
        payload.sha256 != archived.quality_metadata["raw_sha256"]
        or manifest["query"] != bounds.query
    ):
        raise ValueError("Capture integrity mismatch")
    observation = parse_overpass_count(payload, bounds, source, archived.place_id)
    if observation != archived or source.synthetic or not source.research_allowed:
        raise ValueError("Capture is not permitted real aggregate evidence")
    receipt_path = capture / "persistence.json"
    if receipt_path.exists():
        raise FileExistsError("Persistence receipt already exists")
    with psycopg.connect(os.environ["CITYSENSE_DATABASE_URL"]) as connection:
        repository = Repository(connection)
        repository.add_source(source.source_id, source.model_dump(mode="json"))
        repository.add_place(
            SpatialPlace(
                place_id=observation.place_id,
                city_id="batumi",
                name="Research sampling window (not a park entity)",
                longitude=(bounds.west + bounds.east) / 2,
                latitude=(bounds.south + bounds.north) / 2,
                source_id=source.source_id,
                license_id=source.license_id,
                retrieved_at=payload.retrieved_at,
            )
        )
        repository.add_observation(observation)
        assert repository.get_observation(observation.observation_id) == observation
        version = connection.execute("SELECT version_num FROM alembic_version").fetchone()[0]
        pg_version = connection.execute("SELECT version()").fetchone()[0]
        postgis_version = connection.execute("SELECT PostGIS_Lib_Version()").fetchone()[0]
    receipt = {
        "persisted": True,
        "observation_id": str(observation.observation_id),
        "raw_sha256": payload.sha256,
        "alembic_revision": version,
        "postgres_version": pg_version,
        "postgis_version": postgis_version,
        "readback_equal": True,
        "suitability_feature": False,
        "external_publication_enabled": False,
    }
    with receipt_path.open("x", encoding="utf-8") as output:
        json.dump(receipt, output, indent=2)
        output.write("\n")
    print(
        "Captured real aggregate appended and read back identically; publication remains disabled"
    )


if __name__ == "__main__":
    main()
