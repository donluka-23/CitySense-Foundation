"""Rebuild explicitly synthetic fixtures without live providers or random values."""

import json
from datetime import UTC, datetime, timedelta
from pathlib import Path
from uuid import NAMESPACE_URL, uuid5

from citysense.evaluation import content_hash
from citysense.models import EvaluateRequest

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures"


def request(day: int, group: str) -> dict[str, object]:
    decision = datetime(2026, 10, day, 10, tzinfo=UTC)
    places = []
    for side, shade, greenery, walk in (("a", 0.8, 0.6, 8), ("b", 0.2, 0.3, 5)):
        place_id = f"synthetic-{group}-{side}"
        place: dict[str, object] = {
            "place_id": place_id,
            "name": f"Synthetic {group} {side}",
            "walk_minutes": walk,
        }
        for key, value in (
            ("feature_shade", shade),
            ("feature_greenery", greenery),
            ("feature_traffic_proximity", 0.9 if side == "a" else 0.1),
        ):
            place[key] = {
                "value": value,
                "quality": "derived_spatial",
                "data_kind": "estimated_proxy",
                "source_id": "synthetic-fixture",
                "source_version": "fixture-1",
                "license_id": "CC0-synthetic",
                "method_version": "synthetic-identity-1",
                "unit": "fraction",
                "observed_or_valid_at": (decision - timedelta(hours=1)).isoformat(),
                "retrieved_at": (decision - timedelta(minutes=10)).isoformat(),
                "issued_at": None,
                "valid_until": None,
                "spatial_resolution_m": 10,
                "quality_metadata": {"synthetic": "true"},
                "observation_id": str(uuid5(NAMESPACE_URL, place_id + key)),
            }
        places.append(place)
    return {
        "need": "cool_walk",
        "decision_at": decision.isoformat(),
        "target_time": decision.isoformat(),
        "max_walk_minutes": 30,
        "places": places,
    }


def write(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> None:
    records, predictions = [], []
    for split, day in (("train", 1), ("validation", 4), ("test", 7)):
        for i in range(4):
            group = f"{split}-{i}"
            req = EvaluateRequest.model_validate(request(day, group)).model_dump(mode="json")
            records.append(
                {
                    "record_id": group,
                    "participant_id": f"participant-{group}",
                    "place_time_group": f"pair-{group}",
                    "spatial_block": f"block-{group}",
                    "time_block": f"day-{day}",
                    "collected_at": f"2026-10-{day:02}T11:00:00Z",
                    "consent": False,
                    "split": split,
                    "request": req,
                    "preferred_place_id": f"synthetic-{group}-a",
                }
            )
            predictions.append(
                {
                    "record_id": group,
                    "request_hash": content_hash(req),
                    "choice": f"synthetic-{group}-{'a' if i % 2 == 0 else 'b'}",
                    "available_at": req["decision_at"],
                }
            )
    write(
        FIXTURES / "evaluation-manifest.json",
        {
            "dataset_id": "synthetic-paired-choices",
            "dataset_version": "1",
            "synthetic": True,
            "provenance": "Generated software test data; no people or sensors",
            "license_id": "CC0-synthetic",
            "protocol_version": "draft-0.1",
            "information_budget_id": "matched-fixture-v1",
            "latency_budget_seconds": 30,
            "frozen_at": "2026-10-09T12:00:00Z",
            "embargo_hours": 24,
            "records": records,
        },
    )
    write(
        FIXTURES / "baseline-artifact.json",
        {
            "name": "A1-tool-equipped",
            "synthetic": True,
            "model_id": "synthetic-no-model-executed",
            "prompt_hash": content_hash("synthetic-prompt"),
            "tool_configuration_hash": content_hash("synthetic-tools"),
            "information_budget_id": "matched-fixture-v1",
            "latency_budget_seconds": 30,
            "predictions": predictions,
        },
    )
    example = EvaluateRequest.model_validate(request(9, "example"))
    write(
        ROOT.parents[1] / "schemas" / "evaluation-request.example.json",
        example.model_dump(mode="json"),
    )
    write(FIXTURES / "request.json", example.model_dump(mode="json"))
    observations = []
    for place in example.places:
        for key in ("feature_shade", "feature_greenery", "feature_traffic_proximity"):
            feature = getattr(place, key)
            observations.append(
                {**feature.model_dump(mode="json"), "place_id": place.place_id, "feature_key": key}
            )
    write(FIXTURES / "observations.json", observations)
    write(
        FIXTURES / "source-metadata.json",
        {
            "source_id": "synthetic-fixture",
            "source_version": "fixture-1",
            "license_id": "CC0-synthetic",
            "synthetic": True,
            "research_allowed": True,
            "commercial_allowed": False,
            "cache_allowed": True,
            "redistribution_allowed": True,
            "attribution_required": False,
            "terms_url": None,
            "reviewed_at": None,
        },
    )
    write(
        ROOT.parents[1] / "schemas" / "evaluation-request.schema.json",
        EvaluateRequest.model_json_schema(),
    )


if __name__ == "__main__":
    main()
