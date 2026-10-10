"""Deterministic private Telegram adapter; all evidence decisions use shared REST services."""

import time
from collections.abc import Callable
from datetime import UTC, datetime, timedelta
from typing import Any, Literal, Protocol
from urllib.parse import urlsplit

import httpx
from pydantic import AwareDatetime, Field, TypeAdapter

from .models import Contract, Identifier, Need
from .platform import (
    PlaceResult,
    SearchQuery,
    SearchResult,
    SuitabilityQuery,
    SuitabilityResult,
    WalkingCandidate,
)

Mode = Literal["real", "synthetic"]
HELP = (
    "/needs lists supported needs. /places lists operator-selected research records.\n"
    "/evaluate NEED TIME MAX_WALK ID:ESTIMATED_MINUTES [ID:MINUTES ...]\n"
    "/near NEED TIME MAX_WALK LON LAT ESTIMATED_MINUTES\n"
    "TIME is ISO 8601 with timezone, e.g. 2026-10-10T19:00:00+04:00.\n"
    "Need: quiet_rest, cool_walk or family_walk. Up to three candidates.\n"
    "Walking times are caller estimates. No verified availability, booking or psychological benefit.\n"
    "Sharing a Telegram location gives command guidance; it is not retained."
)


class DemoSettings(Contract):
    mode: Mode
    allowed_users: list[int] = Field(min_length=1, max_length=50)
    place_ids: list[Identifier] = Field(min_length=1, max_length=5)
    per_minute: int = Field(default=6, ge=1, le=30)


class ReadBackend(Protocol):
    async def details(self, place_id: str, at: datetime) -> PlaceResult: ...
    async def search(self, query: SearchQuery) -> SearchResult: ...
    async def evaluate(self, query: SuitabilityQuery) -> SuitabilityResult: ...


class OperatorHTTPBackend:
    def __init__(self, base_url: str, api_key: str, client: httpx.AsyncClient) -> None:
        url = urlsplit(base_url)
        if (
            url.scheme != "http"
            or url.hostname not in {"127.0.0.1", "localhost", "::1"}
            or url.username
            or url.password
            or url.query
            or url.fragment
            or url.path not in {"", "/"}
            or len(api_key) < 32
        ):
            raise ValueError("Private demo requires a loopback operator API and configured key")
        self.url, self._key, self.client = base_url.rstrip("/"), api_key, client

    async def _read(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
    ) -> bytes:
        # Fixed paths and validated identifiers; no arbitrary external destination or API bypass.
        async with self.client.stream(
            method,
            self.url + path,
            headers={"X-API-Key": self._key},
            timeout=5,
            follow_redirects=False,
            params=params,
            json=json,
        ) as response:
            if response.status_code == 403:
                raise PermissionError("Publication rights denied")
            if response.status_code != 200:
                raise RuntimeError("Operator service unavailable")
            body = bytearray()
            async for chunk in response.aiter_bytes():
                body.extend(chunk)
                if len(body) > 262144:
                    raise RuntimeError("Operator response exceeded bound")
            return bytes(body)

    async def details(self, place_id: str, at: datetime) -> PlaceResult:
        TypeAdapter(Identifier).validate_python(place_id)
        return PlaceResult.model_validate_json(
            await self._read(
                "GET",
                f"/v1/cities/batumi/places/{place_id}",
                params={"decision_at": at.isoformat()},
            )
        )

    async def search(self, query: SearchQuery) -> SearchResult:
        return SearchResult.model_validate_json(
            await self._read(
                "GET", "/v1/cities/batumi/places", params=query.model_dump(mode="json")
            )
        )

    async def evaluate(self, query: SuitabilityQuery) -> SuitabilityResult:
        return SuitabilityResult.model_validate_json(
            await self._read(
                "POST", "/v1/cities/batumi/suitability", json=query.model_dump(mode="json")
            )
        )


class TelegramDemo:
    def __init__(
        self,
        settings: DemoSettings,
        backend: ReadBackend,
        *,
        now: Callable[[], datetime] = lambda: datetime.now(UTC),
        monotonic: Callable[[], float] = time.monotonic,
    ) -> None:
        self.settings = DemoSettings.model_validate(settings.model_dump())
        self.backend, self.now, self.monotonic = backend, now, monotonic
        # Bounded by static authorized-user set; counts only, no locations/content.
        self.windows: dict[int, tuple[float, int]] = {}

    @property
    def banner(self) -> str:
        return (
            "SYNTHETIC DEMO — fictional evidence; no current Batumi facts."
            if self.settings.mode == "synthetic"
            else "REAL EVIDENCE — source-reported, unvalidated; availability unknown."
        )

    def _mode(self, places: list[PlaceResult]) -> None:
        if any(
            p.rights.synthetic != (self.settings.mode == "synthetic")
            or not p.rights.research_allowed
            or not p.rights.redistribution_allowed
            for p in places
        ):
            raise PermissionError("Mode or publication rights denied")

    def _format(self, result: SuitabilityResult) -> str:
        self._mode(result.state.places)
        if any(
            f.rights.synthetic != (self.settings.mode == "synthetic")
            or not f.rights.redistribution_allowed
            for f in result.state.features
        ):
            raise PermissionError("Feature mode or rights denied")
        lines = [
            self.banner,
            f"Target: {result.inputs.target_time.isoformat()}",
            f"Model {result.assessment.model_version}; unvalidated suitability.",
        ]
        places = {p.place_id: p for p in result.state.places}
        ranked = [p for p in result.assessment.ranked if p.score is not None][:3]
        if not ranked:
            lines.append(
                "Insufficient data: no place can be recommended from the permitted evidence."
            )
        for item in ranked:
            p = places[item.place_id]
            lines.append(f"{p.name[:120]}: {item.score:.3f} (unvalidated index)")
            lines.extend(item.reasons[:3])
            # Synthetic coordinates never become apparent verified map facts.
            if self.settings.mode == "real":
                lon, lat = p.geometry.coordinates
                lines.append(
                    f"Source-reported point (not field verified): https://www.openstreetmap.org/?mlat={lat}&mlon={lon}#map=17/{lat}/{lon}"
                )
        for item in result.assessment.ranked[:3]:
            if item.score is None:
                lines.append(f"{item.place_id}: " + ", ".join(item.reasons[:3]))
        lines.extend(f"Excluded {e.place_id}: {e.reason}" for e in result.assessment.exclusions[:3])
        lines.append(result.walking_time_warning)
        if result.state.features:
            lines.append(
                "Freshness: " + "; ".join(sorted({f.freshness for f in result.state.features}))
            )
        else:
            lines.append(
                "Environmental evidence: missing. Forecast and operating availability: unknown."
            )
        lines.append("Place existence does not verify access, opening, safety or bookability.")
        if self.settings.mode == "real":
            lines.append(
                "© OpenStreetMap contributors; https://www.openstreetmap.org/copyright (where OSM evidence is used)"
            )
        return "\n".join(lines)[:3900]

    async def handle(self, user_id: int, text: str, *, private: bool = True) -> str:
        if not private or user_id not in self.settings.allowed_users:
            return "Private operator demonstration: access denied."
        started = self.monotonic()
        begin, count = self.windows.get(user_id, (started, 0))
        if started - begin >= 60:
            begin, count = started, 0
        self.windows[user_id] = begin, count + 1
        if count >= self.settings.per_minute:
            return self.banner + "\nRate limit reached; retry in one minute."
        if len(text.encode("utf-8")) > 1024:
            return self.banner + "\nInput exceeds the demonstration limit."
        parts = text.split()
        if not parts:
            return self.banner + "\n" + HELP
        command = parts[0].split("@", 1)[0].lower()
        if command in {"/start", "/help"}:
            return self.banner + "\nCitySense compares place evidence for human needs.\n" + HELP
        if command == "/needs":
            return (
                self.banner
                + "\nquiet_rest (experimental), cool_walk, family_walk.\nChoose a need in /evaluate or /near."
            )
        if command == "/sports":
            return (
                self.banner
                + "\nInsufficient data: no verified court inventory, weather exposure, walking routes or availability. Three courts cannot be returned."
            )
        try:
            now = self.now()
            if command == "/places":
                places = [await self.backend.details(pid, now) for pid in self.settings.place_ids]
                self._mode(places)
                lines = [
                    self.banner,
                    "Operator-selected records; source coordinates are not field verified.",
                ]
                for p in places:
                    lines.append(p.place_id + " — " + p.name[:120])
                    if self.settings.mode == "real":
                        lon, lat = p.geometry.coordinates
                        lines.append(
                            f"https://www.openstreetmap.org/?mlat={lat}&mlon={lon}#map=17/{lat}/{lon}"
                        )
                    lines.append("Geometry retrieved: " + p.geometry.retrieved_at.isoformat())
                if self.settings.mode == "real":
                    lines.append(
                        "© OpenStreetMap contributors; ODbL 1.0: https://www.openstreetmap.org/copyright"
                    )
                return "\n".join(lines)[:3900]
            if command not in {"/evaluate", "/near"} or len(parts) < 5:
                return self.banner + "\n" + HELP
            need = Need(parts[1])
            target: datetime = TypeAdapter(AwareDatetime).validate_python(parts[2])
            if not now <= target <= now + timedelta(days=7):
                raise ValueError("Target must be within the next seven days")
            budget = float(parts[3])
            if command == "/evaluate":
                if not 1 <= len(parts[4:]) <= 3:
                    raise ValueError("One to three places required")
                candidates = [
                    WalkingCandidate(
                        place_id=p.rsplit(":", 1)[0], walk_minutes=float(p.rsplit(":", 1)[1])
                    )
                    for p in parts[4:]
                ]
            else:
                if len(parts) != 7:
                    raise ValueError("Invalid coordinate request")
                search = SearchQuery(
                    longitude=float(parts[4]),
                    latitude=float(parts[5]),
                    radius_m=2000,
                    decision_at=now,
                    limit=30,
                )
                found = await self.backend.search(search)
                allowed = [p for p in found.places if p.place_id in self.settings.place_ids][:3]
                self._mode(allowed)
                if not allowed:
                    return (
                        self.banner
                        + "\nNo permitted research place in this radius; coverage is sparse."
                    )
                candidates = [
                    WalkingCandidate(place_id=p.place_id, walk_minutes=float(parts[6]))
                    for p in allowed
                ]
            if any(p.place_id not in self.settings.place_ids for p in candidates):
                raise PermissionError("Outside operator-selected universe")
            query = SuitabilityQuery(
                need=need,
                target_time=target,
                decision_at=now,
                max_walk_minutes=budget,
                candidates=candidates,
            )
            result = await self.backend.evaluate(query)
            return self._format(result)
        except PermissionError:
            return (
                self.banner + "\nNo result: source publication or operator access is not cleared."
            )
        except (ValueError, IndexError):
            return (
                self.banner
                + "\nInvalid request. Use /help; times need a timezone and walking estimates must be finite."
            )
        except (RuntimeError, httpx.HTTPError):
            return (
                self.banner + "\nEvidence service unavailable. No cached or invented replacement."
            )
