"""Structural checks supplement actionlint; no claim that hosted CI has executed."""

import re
from pathlib import Path

import yaml


def main() -> None:
    root = Path(__file__).resolve().parents[3]
    # BaseLoader preserves YAML's 'on' key and scalar values without YAML 1.1 coercion.
    workflow = yaml.load((root / ".github/workflows/ci.yml").read_text(), Loader=yaml.BaseLoader)
    if not {"push", "pull_request"} <= set(workflow["on"]):
        raise ValueError("Missing CI triggers")
    if workflow["permissions"] != {"contents": "read"}:
        raise ValueError("CI permissions must be read-only")
    for job in workflow["jobs"].values():
        for step in job["steps"]:
            if "uses" in step and not re.fullmatch(r"[\w/-]+@[0-9a-f]{40}", step["uses"]):
                raise ValueError("Actions must use immutable commits")
    job = workflow["jobs"]["python"]
    if "@sha256:" not in job["services"]["postgis"]["image"]:
        raise ValueError("PostGIS image must use a digest")
    if job["env"].get("CITYSENSE_REQUIRE_DB") != "1":
        raise ValueError("CI must require real spatial integration tests")
    compose = yaml.safe_load((root / "compose.yml").read_text())
    if "@sha256:" not in compose["services"]["db"]["image"]:
        raise ValueError("Local database image is not pinned")
    print("CI/Compose structure, triggers, action/image pins and mandatory DB gate: passed")


if __name__ == "__main__":
    main()
