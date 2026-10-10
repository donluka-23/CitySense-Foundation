"""In-process adapter prototype; no MCP transport, sessions, network or server."""

from typing import Any

from pydantic import AwareDatetime

from .models import Contract, Identifier
from .platform import (
    ComparisonQuery,
    IntelligenceService,
    SearchQuery,
    StateQuery,
    SuitabilityQuery,
)


class SearchToolInput(Contract):
    city_id: Identifier
    query: SearchQuery


class PlaceToolInput(Contract):
    city_id: Identifier
    place_id: Identifier
    decision_at: AwareDatetime


class StateToolInput(Contract):
    city_id: Identifier
    query: StateQuery


class SuitabilityToolInput(Contract):
    city_id: Identifier
    query: SuitabilityQuery


class ComparisonToolInput(Contract):
    city_id: Identifier
    query: ComparisonQuery


INPUT_MODELS: dict[str, type[Contract]] = {
    "search_places": SearchToolInput,
    "get_place_details": PlaceToolInput,
    "get_city_state": StateToolInput,
    "evaluate_suitability": SuitabilityToolInput,
    "compare_places": ComparisonToolInput,
}


def tool_catalog() -> list[dict[str, Any]]:
    return [
        {
            "name": name,
            "inputSchema": model.model_json_schema(),
            "annotations": {
                "readOnlyHint": True,
                "destructiveHint": False,
                "idempotentHint": True,
                "openWorldHint": False,
            },
        }
        for name, model in INPUT_MODELS.items()
    ]


def call_tool(service: IntelligenceService, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    if name == "search_places":
        search = SearchToolInput.model_validate(arguments)
        return service.search_places(search.city_id, search.query).model_dump(mode="json")
    if name == "get_place_details":
        place = PlaceToolInput.model_validate(arguments)
        return service.get_place_details(
            place.city_id, place.place_id, place.decision_at
        ).model_dump(mode="json")
    if name == "get_city_state":
        state = StateToolInput.model_validate(arguments)
        return service.get_city_state(state.city_id, state.query).model_dump(mode="json")
    if name == "evaluate_suitability":
        suitability = SuitabilityToolInput.model_validate(arguments)
        return service.evaluate_suitability(suitability.city_id, suitability.query).model_dump(
            mode="json"
        )
    if name == "compare_places":
        comparison = ComparisonToolInput.model_validate(arguments)
        return service.compare_places(comparison.city_id, comparison.query).model_dump(mode="json")
    raise ValueError("Unknown or future tool")
