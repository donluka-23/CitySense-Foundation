"""Local adapter/REST/DB transcript. No Telegram connection, users or model API."""

import argparse
import asyncio
import json
import os
import secrets
from datetime import UTC, datetime, timedelta
from pathlib import Path

import httpx

from citysense.app import create_app
from citysense.models import EvaluateRequest
from citysense.real_context import RealInventory
from citysense.security import Settings
from citysense.telegram_demo import DemoSettings, OperatorHTTPBackend, TelegramDemo


async def demonstrate(mode: str, inventory_path: Path | None) -> dict:
    fixture = Path(__file__).resolve().parents[1] / "tests/fixtures/request.json"
    if mode == "synthetic":
        request = EvaluateRequest.model_validate_json(fixture.read_text(encoding="utf-8"))
        at, target = request.decision_at, request.target_time
        ids = [p.place_id for p in request.places]
        need = request.need.value
    else:
        if inventory_path is None:
            raise ValueError("Real mode requires the private acquired inventory")
        inventory = RealInventory.model_validate_json(inventory_path.read_text(encoding="utf-8"))
        ids = [p.place_id for p in inventory.places[:3]]
        at, target, need = datetime.now(UTC), datetime.now(UTC) + timedelta(hours=1), "quiet_rest"
    operator_key = secrets.token_urlsafe(32)  # Ephemeral local authentication, never output.
    app = create_app(
        Settings(database_url=os.environ["CITYSENSE_DATABASE_URL"], api_key=operator_key)
    )
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), trust_env=False) as client:
        settings = DemoSettings.model_validate(
            {"mode": mode, "allowed_users": [111], "place_ids": ids}
        )
        adapter = TelegramDemo(
            settings,
            OperatorHTTPBackend("http://127.0.0.1:8000", operator_key, client),
            now=lambda: at,
        )
        commands = [
            "/start",
            "/needs",
            "/places",
            f"/evaluate {need} {target.isoformat()} 30 " + " ".join(p + ":20" for p in ids),
            "/sports",
        ]
        transcript = [
            {"request": command, "response": await adapter.handle(111, command)}
            for command in commands
        ]
        # No current dataset rights are inferred from success in synthetic mode.
        denied = await client.get(
            "http://127.0.0.1:8000/v1/cities/batumi/places",
            params={
                "longitude": 41.625,
                "latitude": 41.65,
                "radius_m": 1000,
                "decision_at": at.isoformat(),
            },
        )
    return {
        "mode": mode,
        "telegram_connected": False,
        "real_user_ids_used": False,
        "operator_auth_denial": denied.status_code,
        "decision_at": at.isoformat(),
        "transcript": transcript,
        "empirical_status": "NOT EVALUATED",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["synthetic", "real"], required=True)
    parser.add_argument("--inventory", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = asyncio.run(demonstrate(args.mode, args.inventory))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2, ensure_ascii=False)
    print("Offline " + args.mode + " adapter transcript retained; Telegram was not connected")


if __name__ == "__main__":
    main()
