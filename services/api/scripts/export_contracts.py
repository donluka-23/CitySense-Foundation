"""Deterministic checked-in contract exports; --check fails on generated-file drift."""

import argparse
import json
from pathlib import Path

from citysense.agent_tools import tool_catalog
from citysense.app import create_app
from citysense.baseline_capture import CaptureManifest
from citysense.baseline_runner import ProspectiveManifest, RunnerConfig
from citysense.native_sources import WeatherSample
from citysense.opportunities import ProviderEntity
from citysense.platform import CityConfig, GeometryRevision
from citysense.real_context import RealInventory
from citysense.security import Settings
from citysense.telegram_demo import DemoSettings


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[3]
    directory = root / "docs" / "contracts"
    contracts = {
        "openapi.json": create_app(Settings()).openapi(),
        "mcp-tools-design.json": {
            "status": "in_process_prototype_no_mcp_server",
            "tools": tool_catalog(),
        },
        "provider-entity.schema.json": ProviderEntity.model_json_schema(),
        "baseline-capture.schema.json": CaptureManifest.model_json_schema(),
        "weather-candidate.schema.json": WeatherSample.model_json_schema(),
        "city-config.schema.json": CityConfig.model_json_schema(),
        "geometry-revision.schema.json": GeometryRevision.model_json_schema(),
        "prospective-a1.schema.json": ProspectiveManifest.model_json_schema(),
        "a1-runner-config.schema.json": RunnerConfig.model_json_schema(),
        "real-inventory.schema.json": RealInventory.model_json_schema(),
        "telegram-demo.schema.json": DemoSettings.model_json_schema(),
    }
    for name, value in contracts.items():
        path = directory / name
        text = json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != text:
                raise SystemExit(f"Contract export drift: {name}")
        else:
            directory.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
    print("Contract exports match" if args.check else "Contract exports written")


if __name__ == "__main__":
    main()
