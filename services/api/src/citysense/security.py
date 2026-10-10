"""Single-process research controls; no request bodies, IPs or identifiers in logs."""

import logging
import os
import secrets
import threading
import time
from collections import OrderedDict
from dataclasses import dataclass, field
from typing import Literal

from opentelemetry import trace
from starlette.responses import JSONResponse
from starlette.types import ASGIApp, Message, Receive, Scope, Send

LOGGER = logging.getLogger("citysense.request")
TRACER = trace.get_tracer("citysense")


@dataclass(frozen=True)
class Settings:
    mode: Literal["development", "production"] = "development"
    database_url: str | None = field(default=None, repr=False)
    api_key: str | None = field(default=None, repr=False)
    rate_limit: int = 60
    body_limit: int = 262144
    read_cities: tuple[str, ...] = ("batumi", "tbilisi-fixture")

    def __post_init__(self) -> None:
        if self.mode not in ("development", "production"):
            raise ValueError("Unknown runtime mode")
        if not 1 <= self.rate_limit <= 10000 or not 1024 <= self.body_limit <= 1048576:
            raise ValueError("Invalid resource limits")
        if self.mode == "production" and (not self.api_key or len(self.api_key) < 32):
            raise ValueError(
                "Production mode requires a generated API key of at least 32 characters"
            )

    @classmethod
    def from_env(cls) -> "Settings":
        mode = os.environ.get("CITYSENSE_MODE", "development")
        if mode not in ("development", "production"):
            raise ValueError("Unknown runtime mode")
        return cls(
            mode="production" if mode == "production" else "development",
            database_url=os.environ.get("CITYSENSE_DATABASE_URL") or None,
            api_key=os.environ.get("CITYSENSE_API_KEY") or None,
            rate_limit=int(os.environ.get("CITYSENSE_RATE_LIMIT", "60")),
            body_limit=int(os.environ.get("CITYSENSE_BODY_LIMIT", "262144")),
            read_cities=tuple(
                os.environ.get("CITYSENSE_READ_CITIES", "batumi,tbilisi-fixture").split(",")
            ),
        )


class Telemetry:
    def __init__(self) -> None:
        self.lock = threading.Lock()
        self.counts: dict[tuple[str, int], int] = {}
        self.latency_seconds: dict[str, float] = {}
        self.latency_buckets: dict[tuple[str, float], int] = {}

    def record(self, route: str, status: int, latency: float) -> None:
        with self.lock:
            self.counts[route, status] = self.counts.get((route, status), 0) + 1
            self.latency_seconds[route] = self.latency_seconds.get(route, 0) + latency
            for boundary in (0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 5.0, float("inf")):
                if latency <= boundary:
                    self.latency_buckets[route, boundary] = (
                        self.latency_buckets.get((route, boundary), 0) + 1
                    )


class GuardMiddleware:
    def __init__(self, app: ASGIApp, settings: Settings, telemetry: Telemetry) -> None:
        self.app, self.settings, self.telemetry = app, settings, telemetry
        self.windows: OrderedDict[str, tuple[float, int]] = OrderedDict()
        self.max_clients = 10000

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        started = time.monotonic()
        headers = dict(scope["headers"])
        status = 500

        async def safe_send(message: Message) -> None:
            nonlocal status
            if message["type"] == "http.response.start":
                status = message["status"]
                message["headers"] += [
                    (b"x-content-type-options", b"nosniff"),
                    (b"cache-control", b"no-store"),
                ]
            await send(message)

        async def reject(code: int, detail: str) -> None:
            await JSONResponse({"detail": detail}, status_code=code)(scope, receive, safe_send)

        try:
            if scope["path"] != "/health" and self.settings.api_key:
                provided = headers.get(b"x-api-key", b"")
                if not secrets.compare_digest(provided, self.settings.api_key.encode()):
                    await reject(401, "Authentication required")
                    return
            # Use only the direct peer. Untrusted forwarded headers cannot bypass limits.
            client = str(scope.get("client", ("unknown",))[0])
            window, count = self.windows.get(client, (started, 0))
            if started - window >= 60:
                window, count = started, 0
            if client not in self.windows and len(self.windows) >= self.max_clients:
                # Fail closed under client churn; remove only expired windows.
                for key, (begin, _) in list(self.windows.items()):
                    if started - begin >= 60:
                        del self.windows[key]
                if len(self.windows) >= self.max_clients:
                    await reject(429, "Request capacity exceeded")
                    return
            self.windows[client] = window, count + 1
            if count >= self.settings.rate_limit:
                await reject(429, "Rate limit exceeded")
                return
            try:
                declared = int(headers.get(b"content-length", b"0"))
            except ValueError:
                await reject(400, "Invalid content length")
                return
            if declared < 0 or declared > self.settings.body_limit:
                await reject(413, "Request body too large")
                return
            # Buffer within a fixed bound so chunked bodies are checked before parsing.
            body = bytearray()
            while True:
                message = await receive()
                if message["type"] == "http.disconnect":
                    return
                body.extend(message.get("body", b""))
                if len(body) > self.settings.body_limit:
                    await reject(413, "Request body too large")
                    return
                if not message.get("more_body", False):
                    break
            delivered = False

            async def bounded_receive() -> Message:
                nonlocal delivered
                if delivered:
                    return await receive()
                delivered = True
                return {"type": "http.request", "body": bytes(body), "more_body": False}

            with TRACER.start_as_current_span("citysense.request") as span:
                await self.app(scope, bounded_receive, safe_send)
                span.set_attribute("http.response.status_code", status)
        finally:
            route = getattr(scope.get("route"), "path", "unmatched")
            elapsed = time.monotonic() - started
            self.telemetry.record(route, status, elapsed)
            LOGGER.info(
                "request route=%s status=%d duration_ms=%.2f", route, status, elapsed * 1000
            )
