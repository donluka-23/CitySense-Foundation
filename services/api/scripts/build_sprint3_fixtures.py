"""Invented, label-free engineering cases; never current Batumi facts."""

import json
from datetime import timedelta
from pathlib import Path

from citysense.baseline_runner import FrozenScenario, ProspectiveManifest, RunnerConfig
from citysense.ingestion import SourceMetadata
from citysense.models import EvaluateRequest, Need, SpatialPlace


def main() -> None:
    directory = Path(__file__).resolve().parents[1] / "tests/fixtures"
    request = EvaluateRequest.model_validate_json(
        (directory / "request.json").read_text(encoding="utf-8")
    )
    source = SourceMetadata.model_validate_json(
        (directory / "source-metadata.json").read_text(encoding="utf-8")
    )
    places = [
        SpatialPlace(
            place_id=p.place_id,
            city_id="batumi",
            name=p.name,
            longitude=41.63 + i * 0.01,
            latitude=41.65,
            source_id=source.source_id,
            license_id=source.license_id,
            retrieved_at=request.decision_at - timedelta(days=1),
        )
        for i, p in enumerate(request.places)
    ]
    cases = []
    for need in Need:
        item = request.model_copy(deep=True)
        item.need = need
        cases.append(
            FrozenScenario(
                scenario_id="synthetic-" + need.value,
                synthetic=True,
                request=item,
                places=places,
                frozen_at=item.decision_at - timedelta(seconds=10),
                sources=[source],
                capture_permitted=True,
                external_model_permitted=False,
                no_personal_data=True,
            )
        )
    manifest = ProspectiveManifest(
        information_budget_id="synthetic-engineering-v1", scenarios=cases
    )
    config = RunnerConfig(
        provider="fixture",
        model_id="invented-offline-model-v1",
        input_usd_per_million=0,
        output_usd_per_million=0,
        pricing_reviewed_at=request.decision_at,
    )
    for name, value in {
        "prospective-manifest.json": manifest.model_dump(mode="json"),
        "a1-fixture-config.json": config.model_dump(mode="json"),
    }.items():
        (directory / name).write_text(
            json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    print("Synthetic, label-free Sprint 3 fixtures generated")


if __name__ == "__main__":
    main()
