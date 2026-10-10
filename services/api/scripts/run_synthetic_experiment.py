"""Exercise the harness; results are software checks, never empirical evidence."""

import argparse
from pathlib import Path

from citysense.evaluation import (
    BaselineArtifact,
    DatasetManifest,
    FrozenToolBaseline,
    run_experiment,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    fixtures = Path(__file__).resolve().parents[1] / "tests" / "fixtures"
    dataset = DatasetManifest.model_validate_json(
        (fixtures / "evaluation-manifest.json").read_text()
    )
    artifact = BaselineArtifact.model_validate_json(
        (fixtures / "baseline-artifact.json").read_text()
    )
    result = run_experiment(dataset, FrozenToolBaseline(artifact, dataset), args.output)
    print(result["interpretation"])
    print(f"Reproducible experiment hash: {result['experiment_hash']}")


if __name__ == "__main__":
    main()
