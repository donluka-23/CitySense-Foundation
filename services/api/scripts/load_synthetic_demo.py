"""Explicit additive fixture setup on a disposable loopback development/test database."""

import json
import os
from datetime import timedelta
from pathlib import Path
from urllib.parse import urlsplit

import psycopg

from citysense.db import Repository
from citysense.ingestion import SourceMetadata
from citysense.models import EvaluateRequest, Observation, SpatialPlace


def main() -> None:
    url = os.environ["CITYSENSE_DATABASE_URL"]
    target = urlsplit(url)
    if target.hostname not in {"127.0.0.1", "localhost", "::1"} or not target.path.endswith(
        ("_dev", "_test")
    ):
        raise SystemExit(
            "Fixture setup requires a disposable loopback database ending _dev or _test"
        )
    fixtures = Path(__file__).resolve().parents[1] / "tests/fixtures"
    request = EvaluateRequest.model_validate_json(
        (fixtures / "request.json").read_text(encoding="utf-8")
    )
    source = SourceMetadata.model_validate_json(
        (fixtures / "source-metadata.json").read_text(encoding="utf-8")
    )
    observations = [
        Observation.model_validate(o)
        for o in json.loads((fixtures / "observations.json").read_text(encoding="utf-8"))
    ]
    if not source.synthetic or any(
        o.quality_metadata.get("synthetic") != "true" for o in observations
    ):
        raise ValueError("Only explicitly fictional observations may be loaded")
    with psycopg.connect(url) as connection:
        connection.execute("SET LOCAL statement_timeout=5000")
        repository = Repository(connection)
        old = connection.execute(
            "SELECT metadata FROM sources WHERE id=%s", (source.source_id,)
        ).fetchone()
        if old is None:
            repository.add_source(source.source_id, source.model_dump(mode="json"))
        elif SourceMetadata.model_validate(old[0]) != source:
            raise ValueError("Immutable source differs")
        for i, p in enumerate(request.places):
            place = SpatialPlace(
                place_id=p.place_id,
                city_id="batumi",
                name=p.name,
                longitude=41.63 + i * 0.01,
                latitude=41.65,
                source_id=source.source_id,
                license_id=source.license_id,
                retrieved_at=request.decision_at - timedelta(days=1),
            )
            row = connection.execute(
                "SELECT city_id,label,longitude,latitude,source_id,source_license,retrieved_at FROM places WHERE id=%s",
                (p.place_id,),
            ).fetchone()
            if row is None:
                repository.add_place(place)
            elif row != (
                place.city_id,
                place.name,
                place.longitude,
                place.latitude,
                place.source_id,
                place.license_id,
                place.retrieved_at,
            ):
                raise ValueError("Immutable place differs")
        for o in observations:
            old = connection.execute(
                "SELECT payload FROM observations WHERE id=%s", (o.observation_id,)
            ).fetchone()
            if old is None:
                repository.add_observation(o)
            elif Observation.model_validate(old[0]) != o:
                raise ValueError("Immutable observation differs")
    print("SYNTHETIC DEMO fixtures present; no real Batumi measurements loaded")


if __name__ == "__main__":
    main()
