"""Bounded research API. Replay requires an explicitly configured spatial database."""

from uuid import UUID

import psycopg
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse

from .db import Repository
from .engine import evaluate
from .models import EvaluateRequest, EvaluateResponse
from .platform_api import platform_router
from .security import GuardMiddleware, Settings, Telemetry


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or Settings.from_env()
    app = FastAPI(title="CitySense Urban Intelligence", version="0.3.0")
    telemetry = Telemetry()
    app.state.telemetry = telemetry
    app.add_middleware(GuardMiddleware, settings=settings, telemetry=telemetry)
    app.include_router(platform_router(settings))

    @app.exception_handler(RequestValidationError)
    async def validation_error(request: Request, error: RequestValidationError) -> JSONResponse:
        # Pydantic's default response echoes invalid input; omit values and error contexts.
        return JSONResponse(
            status_code=422,
            content={"detail": [{"loc": e["loc"], "type": e["type"]} for e in error.errors()]},
        )

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "stage": "unvalidated_research_foundation"}

    @app.post("/v1/evaluate", response_model=EvaluateResponse)
    def evaluate_places(request: EvaluateRequest) -> EvaluateResponse:
        return evaluate(request)

    @app.get("/v1/replay/{snapshot_id}", response_model=EvaluateResponse)
    def replay(snapshot_id: UUID) -> EvaluateResponse:
        if not settings.database_url:
            raise HTTPException(status_code=503, detail="Replay database is not configured")
        try:
            with psycopg.connect(settings.database_url, connect_timeout=5) as connection:
                connection.execute("SET LOCAL statement_timeout=5000")
                snapshot, parameters = Repository(connection).replay(snapshot_id)
                return evaluate(snapshot.request, parameters)
        except KeyError as error:
            raise HTTPException(status_code=404, detail="Snapshot not found") from error
        except psycopg.Error as error:
            raise HTTPException(status_code=503, detail="Replay database unavailable") from error
        except ValueError as error:
            raise HTTPException(status_code=409, detail="Replay integrity check failed") from error

    return app


app = create_app()
