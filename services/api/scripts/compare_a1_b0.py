"""Join independent labels only after capture. No labels are sent to a model."""

import argparse
from pathlib import Path

from citysense.baseline_runner import ProspectiveManifest, RunnerConfig
from citysense.evaluation import DatasetManifest, FrozenToolBaseline, run_experiment
from citysense.prospective_audit import join_reviewed_receipts


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--receipts", type=Path, nargs="+", required=True)
    parser.add_argument("--dataset", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--review-approved-data", action="store_true")
    args = parser.parse_args()
    if not args.review_approved_data:
        raise SystemExit(
            "Independent consent, protocol, source and receipt review must precede this join"
        )
    manifest = ProspectiveManifest.model_validate_json(args.manifest.read_text(encoding="utf-8"))
    config = RunnerConfig.model_validate_json(args.config.read_text(encoding="utf-8"))
    dataset = DatasetManifest.model_validate_json(args.dataset.read_text(encoding="utf-8"))
    artifact = join_reviewed_receipts(manifest, config, args.receipts, dataset)
    result = run_experiment(dataset, FrozenToolBaseline(artifact, dataset), args.output)
    print(
        "Synthetic software check"
        if result["synthetic"]
        else "Exploratory comparison; independent review required"
    )


if __name__ == "__main__":
    main()
