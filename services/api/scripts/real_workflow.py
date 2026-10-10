"""Explicit bounded research acquisition and stored abstention/replay on a local DB."""

import argparse
import json
import os
from datetime import UTC, datetime, timedelta
from pathlib import Path
from uuid import uuid4

import httpx
import psycopg

from citysense.db import Repository
from citysense.engine import evaluate
from citysense.ingestion import SourceMetadata
from citysense.models import FeatureSnapshot, Need
from citysense.native_sources import Bounds, NativeRetriever
from citysense.parameters import load_parameters
from citysense.platform import AccessContext, IntelligenceService, SuitabilityQuery
from citysense.real_context import RealInventory, park_geometry_query, parse_park_geometry


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--acquire", action="store_true")
    parser.add_argument("--inventory", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    if args.acquire:
        source = SourceMetadata(
            source_id="osm-overpass",
            source_version="batumi-geometries-v1",
            license_id="ODbL-1.0",
            synthetic=False,
            research_allowed=True,
            commercial_allowed=False,
            cache_allowed=True,
            redistribution_allowed=False,
            attribution_required=True,
            terms_url="https://www.openstreetmap.org/copyright",
            reviewed_at=datetime.now(UTC),
        )
        bounds = Bounds(west=41.615, south=41.638, east=41.635, north=41.658)
        with httpx.Client(
            trust_env=False,
            headers={
                "User-Agent": "CitySense-local-research/0.4 (bounded skeleton geometry query)"
            },
        ) as http:
            payload = NativeRetriever(source, http).fetch(
                "overpass", {"data": park_geometry_query(bounds)}
            )
        inventory = parse_park_geometry(payload, bounds, source)
        # Validate the nonpersonal skeleton envelope before persisting any upstream bytes.
        payload.archive(args.output, source)
        with args.inventory.open("x", encoding="utf-8") as handle:
            handle.write(inventory.model_dump_json(indent=2) + "\n")
    else:
        inventory = RealInventory.model_validate_json(args.inventory.read_text(encoding="utf-8"))
    access = AccessContext(
        "local-research-operator",
        frozenset({"batumi"}),
        frozenset({"city.read", "suitability.read"}),
        audience="local_research",
    )
    # This script never serves HTTP/Telegram or transfers source records to external models.
    with psycopg.connect(os.environ["CITYSENSE_DATABASE_URL"]) as connection:
        connection.execute("SET LOCAL statement_timeout='5s'")
        repo = Repository(connection)
        # Existing Sprint 2 source has different immutable version; use a distinct ingestion ID.
        source = inventory.source.model_copy(update={"source_id": "osm-batumi-geometries"})
        stored = connection.execute(
            "SELECT metadata FROM sources WHERE id=%s", (source.source_id,)
        ).fetchone()
        if stored is None:
            repo.add_source(source.source_id, source.model_dump(mode="json"))
        elif SourceMetadata.model_validate(stored[0]) != source:
            raise ValueError(
                "Stored inventory source differs; append a separately reviewed source version"
            )
        for place in inventory.places:
            normalized = place.model_copy(update={"source_id": source.source_id})
            row = connection.execute(
                "SELECT source_id,longitude,latitude,retrieved_at FROM places WHERE id=%s",
                (place.place_id,),
            ).fetchone()
            if row is None:
                repo.add_place(normalized)
            elif row != (source.source_id, place.longitude, place.latitude, place.retrieved_at):
                raise ValueError("Existing geometry differs; use append-only revision ingestion")
        decision = datetime.now(UTC)
        # Calendar evening is explicit; if already past, tomorrow at 20:00 Tbilisi.
        target = decision.replace(hour=16, minute=0, second=0, microsecond=0)
        if target < decision:
            target += timedelta(days=1)
        query = SuitabilityQuery(
            need=Need.QUIET_REST,
            decision_at=decision,
            target_time=target,
            max_walk_minutes=30,
            candidates=[
                {"place_id": p.place_id, "walk_minutes": 20 if i < 4 else 45}
                for i, p in enumerate(inventory.places)
            ],
        )
        result = IntelligenceService(connection, access).evaluate_suitability("batumi", query)
        params = load_parameters()
        repo.add_model(params)
        snapshot = FeatureSnapshot(
            snapshot_id=uuid4(),
            build_version="sprint3-real-workflow-v1",
            created_at=datetime.now(UTC),
            request=result.inputs,
            model_version=params.version,
            parameter_hash=params.digest,
        )
        repo.add_snapshot(snapshot)
        frozen, replay_params = repo.replay(snapshot.snapshot_id)
        replayed = evaluate(frozen.request, replay_params)
        # JSON canonicalization removes tuple/list representation differences from database JSONB.
        if replayed.model_dump(mode="json", exclude={"warning"}) != result.assessment.model_dump(
            mode="json", exclude={"warning"}
        ):
            keys = [
                k
                for k, v in replayed.model_dump(mode="json", exclude={"warning"}).items()
                if v != result.assessment.model_dump(mode="json", exclude={"warning"})[k]
            ]
            raise AssertionError("Replay differs in fields: " + ",".join(keys))
        receipt = {
            "synthetic": False,
            "snapshot_id": str(snapshot.snapshot_id),
            "inventory_hash": inventory.raw_sha256,
            "result": result.model_dump(mode="json"),
            "replay_equal": True,
            "routing": "unverified caller estimates; no routing provider enabled",
            "weather": "missing; live Open-Meteo disabled",
            "availability": "unknown",
            "sport": {
                "status": "insufficient_data",
                "courts": 0,
                "missing": [
                    "court inventory",
                    "weather exposure",
                    "verified availability",
                    "walking routes",
                ],
            },
            "empirical_status": "NOT EVALUATED",
        }
        with (args.output / (str(snapshot.snapshot_id) + ".decision.json")).open(
            "x", encoding="utf-8"
        ) as handle:
            json.dump(receipt, handle, indent=2, ensure_ascii=False)
        publication = IntelligenceService(
            connection, AccessContext("publication-check", access.cities, access.scopes)
        )
        try:
            publication.get_place_details("batumi", inventory.places[0].place_id, decision)
        except PermissionError:
            publication_blocked = True
        else:
            raise AssertionError("Private-source publication must remain blocked")
    print(
        json.dumps(
            {
                "synthetic": False,
                "places": len(inventory.places),
                "snapshot_id": str(snapshot.snapshot_id),
                "replay_equal": True,
                "non_null_scores": sum(p.score is not None for p in result.assessment.ranked),
                "abstentions": sum(p.score is None for p in result.assessment.ranked),
                "hard_exclusions": len(result.assessment.excluded),
                "publication_blocked": publication_blocked,
                "raw_sha256": inventory.raw_sha256,
                "retrieved_at": inventory.retrieved_at.isoformat(),
                "provider_database_at": inventory.provider_database_at.isoformat(),
                "empirical_status": "NOT EVALUATED",
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
