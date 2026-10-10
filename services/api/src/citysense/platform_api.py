"""Versioned transport only; no scoring, rights or geometry selection logic."""

import secrets
from collections.abc import Iterator
from typing import Annotated

import psycopg
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.security import APIKeyHeader
from pydantic import AwareDatetime

from .models import Identifier
from .platform import (
    AccessContext,
    ComparisonQuery,
    IntelligenceService,
    PlaceResult,
    SearchQuery,
    SearchResult,
    StateQuery,
    StateResult,
    SuitabilityQuery,
    SuitabilityResult,
)
from .security import Settings


def platform_router(settings: Settings) -> APIRouter:
    router = APIRouter(prefix="/v1/cities", tags=["private-agent-read"])
    key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

    def service(key: Annotated[str | None, Depends(key_header)]) -> Iterator[IntelligenceService]:
        if not settings.api_key or not key or not secrets.compare_digest(key, settings.api_key):
            raise HTTPException(401, "Configured operator authentication required")
        if not settings.database_url:
            raise HTTPException(503, "Intelligence database is not configured")
        try:
            with psycopg.connect(settings.database_url, connect_timeout=5) as connection:
                connection.execute("SET TRANSACTION ISOLATION LEVEL REPEATABLE READ, READ ONLY")
                connection.execute("SET LOCAL statement_timeout=5000")
                # A single operator service identity, not a multi-tenant identity service.
                access = AccessContext(
                    "local-operator",
                    frozenset(settings.read_cities),
                    frozenset({"city.read", "suitability.read"}),
                )
                yield IntelligenceService(connection, access)
        except PermissionError as error:
            raise HTTPException(403, "City, scope or publication rights denied") from error
        except KeyError as error:
            raise HTTPException(404, "Requested city or place unavailable") from error
        except psycopg.Error as error:
            raise HTTPException(503, "Intelligence database unavailable") from error
        except ValueError as error:
            raise HTTPException(409, "Stored intelligence integrity check failed") from error

    Service = Annotated[IntelligenceService, Depends(service)]

    @router.get("/{city_id}/places", response_model=SearchResult, operation_id="search_places")
    def search(
        city_id: Identifier,
        service: Service,
        longitude: Annotated[float, Query(ge=-180, le=180)],
        latitude: Annotated[float, Query(ge=-90, le=90)],
        radius_m: Annotated[float, Query(gt=0, le=10000)],
        decision_at: AwareDatetime,
        limit: Annotated[int, Query(ge=1, le=30)] = 20,
    ) -> SearchResult:
        return service.search_places(
            city_id,
            SearchQuery(
                longitude=longitude,
                latitude=latitude,
                radius_m=radius_m,
                decision_at=decision_at,
                limit=limit,
            ),
        )

    @router.get(
        "/{city_id}/places/{place_id}", response_model=PlaceResult, operation_id="get_place_details"
    )
    def details(
        city_id: Identifier, place_id: Identifier, decision_at: AwareDatetime, service: Service
    ) -> PlaceResult:
        return service.get_place_details(city_id, place_id, decision_at)

    @router.post("/{city_id}/state", response_model=StateResult, operation_id="get_city_state")
    def state(city_id: Identifier, query: StateQuery, service: Service) -> StateResult:
        return service.get_city_state(city_id, query)

    @router.post(
        "/{city_id}/suitability",
        response_model=SuitabilityResult,
        operation_id="evaluate_suitability",
    )
    def suitability(
        city_id: Identifier, query: SuitabilityQuery, service: Service
    ) -> SuitabilityResult:
        return service.evaluate_suitability(city_id, query)

    @router.post(
        "/{city_id}/comparison", response_model=SuitabilityResult, operation_id="compare_places"
    )
    def comparison(
        city_id: Identifier, query: ComparisonQuery, service: Service
    ) -> SuitabilityResult:
        return service.compare_places(city_id, query)

    return router
