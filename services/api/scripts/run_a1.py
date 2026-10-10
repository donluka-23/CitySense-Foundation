"""Offline capture by default. Live invocation requires explicit operator authorization."""

import argparse
import json
import os
from pathlib import Path

import httpx

from citysense.baseline_runner import (
    FixtureClient,
    OpenAIResponsesClient,
    ProspectiveManifest,
    RunnerConfig,
    run_scenario,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--authorize-live", action="store_true")
    args = parser.parse_args()
    manifest = ProspectiveManifest.model_validate_json(args.manifest.read_text(encoding="utf-8"))
    config = RunnerConfig.model_validate_json(args.config.read_text(encoding="utf-8"))
    if config.provider != "fixture" and not args.authorize_live:
        raise SystemExit("Live model execution requires explicit authorization and reviewed rights")
    with httpx.Client(trust_env=False) as http:
        client = (
            FixtureClient()
            if config.provider == "fixture"
            else OpenAIResponsesClient(os.environ.get("OPENAI_API_KEY", ""), http)
        )
        results = [
            run_scenario(
                s, manifest.digest, manifest.information_budget_id, config, client, args.output
            )
            for s in manifest.scenarios
        ]
    print(json.dumps({"dataset_hash": manifest.digest, "runs": results}, indent=2))
    if any(r["status"] not in {"completed", "abstained"} for r in results):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
