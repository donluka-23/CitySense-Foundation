"""Explicit fixture insertion for local replay. Never runs on API startup."""

import json
import os
from datetime import timedelta
from pathlib import Path
from uuid import NAMESPACE_URL, uuid5

import psycopg

from citysense.db import Repository
from citysense.models import EvaluateRequest, FeatureSnapshot, Observation, SpatialPlace
from citysense.parameters import load_parameters


def main() -> None:
    fixtures = Path(__file__).resolve().parents[1] / "tests" / "fixtures"
    request = EvaluateRequest.model_validate_json((fixtures / "request.json").read_text())
    parameters = load_parameters()
    snapshot_id = uuid5(NAMESPACE_URL, "citysense-synthetic-snapshot-v1")
    with psycopg.connect(os.environ["CITYSENSE_DATABASE_URL"]) as connection:
        repository = Repository(connection)
        # Conflict means evidence already exists; never overwrite it silently.
        repository.add_source(
            "synthetic-fixture", json.loads((fixtures / "source-metadata.json").read_text())
        )
        for i, place in enumerate(request.places):
            repository.add_place(
                SpatialPlace(
                    place_id=place.place_id,
                    city_id="batumi",
                    name=place.name,
                    longitude=41.63 + 0.01 * i,
                    latitude=41.65,
                    source_id="synthetic-fixture",
                    license_id="CC0-synthetic",
                    retrieved_at=request.decision_at - timedelta(days=1),
                )
            )
        for observation in json.loads((fixtures / "observations.json").read_text()):
            repository.add_observation(Observation.model_validate(observation))
        repository.add_model(parameters)
        repository.add_snapshot(
            FeatureSnapshot(
                snapshot_id=snapshot_id,
                build_version="identity-normalized-v1",
                created_at=request.decision_at + timedelta(minutes=1),
                request=request,
                model_version=parameters.version,
                parameter_hash=parameters.digest,
            )
        )
    print(f"Synthetic fixture persisted. Replay: /v1/replay/{snapshot_id}")


if __name__ == "__main__":
    main()
