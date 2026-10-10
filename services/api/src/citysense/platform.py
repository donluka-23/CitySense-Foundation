"""Read-only application boundary shared by REST and future agent transports."""

from dataclasses import dataclass
from datetime import UTC, datetime
from importlib.resources import files
from typing import Annotated, Any, Literal, Self
from uuid import UUID
from zoneinfo import ZoneInfo

from psycopg import Connection
from psycopg.rows import dict_row
from pydantic import AwareDatetime, Field, model_validator

from .engine import evaluate
from .ingestion import SourceMetadata
from .models import (
    FEATURE_KEYS,
    Contract,
    EvaluateRequest,
    EvaluateResponse,
    Feature,
    Identifier,
    Need,
    Observation,
    Place,
)
from .parameters import load_parameters


class CityConfig(Contract):
    city_id: Identifier
    timezone: str
    bounds: tuple[float, float, float, float]
    validation_status: Literal["initial_research", "synthetic_configuration_only"]

    @model_validator(mode="after")
    def valid_config(self) -> Self:
        ZoneInfo(self.timezone)
        west, south, east, north = self.bounds
        if not -180 <= west < east <= 180 or not -90 <= south < north <= 90:
            raise ValueError("Invalid WGS84 bounds")
        return self


def load_cities() -> dict[str, CityConfig]:
    from pydantic import TypeAdapter

    configs: list[CityConfig] = TypeAdapter(list[CityConfig]).validate_json(
        files("citysense").joinpath("parameters/cities.json").read_text(encoding="utf-8")
    )
    if len({c.city_id for c in configs}) != len(configs):
        raise ValueError("Duplicate city configuration")
    return {c.city_id: c for c in configs}


@dataclass(frozen=True)
class AccessContext:
    tenant_id: str
    cities: frozenset[str]
    scopes: frozenset[str]
    purpose: Literal["research", "commercial"] = "research"
    audience: Literal["publication", "local_research"] = "publication"

    def __post_init__(self) -> None:
        if self.audience == "local_research" and self.purpose != "research":
            raise ValueError("Local research access cannot authorize commercial use")

    def authorize(self, city_id: str, scope: str) -> None:
        if city_id not in self.cities or scope not in self.scopes:
            raise PermissionError("City or scope is not authorized")


class GeometryRevision(Contract):
    revision_id: UUID
    place_id: Identifier
    longitude: float = Field(ge=-180, le=180)
    latitude: float = Field(ge=-90, le=90)
    valid_at: AwareDatetime
    retrieved_at: AwareDatetime
    source_id: Identifier
    source_version: Identifier
    license_id: Identifier

    @model_validator(mode="after")
    def available(self) -> Self:
        if self.valid_at > self.retrieved_at:
            raise ValueError("Geometry cannot be observed in the future")
        return self


class Geometry(Contract):
    type: Literal["Point"] = "Point"
    coordinates: tuple[
        Annotated[float, Field(ge=-180, le=180)], Annotated[float, Field(ge=-90, le=90)]
    ]
    srid: Literal[4326] = 4326
    revision_id: UUID | None
    valid_at: AwareDatetime
    retrieved_at: AwareDatetime
    source_id: Identifier
    source_version: Identifier
    license_id: Identifier
    spatial_accuracy_m: float | None = Field(default=None, ge=0)
    verification_status: Literal["source_reported_unverified"] = "source_reported_unverified"

    @model_validator(mode="after")
    def observed_geometry(self) -> Self:
        if self.valid_at > self.retrieved_at:
            raise ValueError("Geometry validity exceeds retrieval")
        return self


class PlaceResult(Contract):
    place_id: Identifier
    city_id: Identifier
    name: str
    geometry: Geometry
    rights: SourceMetadata
    model_version: Literal["not_applicable"] = "not_applicable"
    uncertainty: list[str] = Field(
        default_factory=lambda: ["Geometry accuracy not independently verified"]
    )


class EvidenceResult(Contract):
    evidence: Observation
    age_seconds: float = Field(ge=0)
    freshness: Literal["within_model_limit", "stale", "unavailable"]
    verification_status: Literal["source_reported_unverified"] = "source_reported_unverified"
    rights: SourceMetadata
    uncertainty: list[str]


class StateResult(Contract):
    city_id: Identifier
    decision_at: AwareDatetime
    target_time: AwareDatetime
    places: list[PlaceResult]
    features: list[EvidenceResult]
    missing_features: dict[str, list[str]]
    model_version: str
    parameter_hash: str
    warning: str = "Sparse place evidence; not a measured psychological or citywide state"


class StateQuery(Contract):
    decision_at: AwareDatetime
    target_time: AwareDatetime
    place_ids: list[Identifier] = Field(min_length=1, max_length=30)

    @model_validator(mode="after")
    def valid_times(self) -> Self:
        self.decision_at = self.decision_at.astimezone(UTC)
        self.target_time = self.target_time.astimezone(UTC)
        if self.target_time < self.decision_at or len(set(self.place_ids)) != len(self.place_ids):
            raise ValueError("Invalid target time or duplicate place IDs")
        return self


class WalkingCandidate(Contract):
    place_id: Identifier
    walk_minutes: float = Field(ge=0, le=10000)
    walking_time_source: Literal["caller_estimate"] = "caller_estimate"


class SuitabilityQuery(Contract):
    decision_at: AwareDatetime
    target_time: AwareDatetime
    need: Need
    candidates: list[WalkingCandidate] = Field(min_length=1, max_length=30)
    max_walk_minutes: float = Field(default=45, ge=0, le=180)

    @model_validator(mode="after")
    def valid_query(self) -> Self:
        StateQuery(
            decision_at=self.decision_at,
            target_time=self.target_time,
            place_ids=[p.place_id for p in self.candidates],
        )
        return self


class ComparisonQuery(SuitabilityQuery):
    candidates: list[WalkingCandidate] = Field(min_length=2, max_length=2)


class SuitabilityResult(Contract):
    city_id: Identifier
    state: StateResult
    assessment: EvaluateResponse
    inputs: EvaluateRequest
    evidence_origin: Literal["stored_database"] = "stored_database"
    walking_time_warning: str = (
        "Walking times are unverified caller estimates; no routing/accessibility guarantee"
    )


class SearchQuery(Contract):
    longitude: float = Field(ge=-180, le=180)
    latitude: float = Field(ge=-90, le=90)
    radius_m: float = Field(gt=0, le=10000)
    decision_at: AwareDatetime
    limit: int = Field(default=20, ge=1, le=30)


class SearchResult(Contract):
    city_id: Identifier
    decision_at: AwareDatetime
    places: list[PlaceResult]
    limit: int
    truncated: bool


PLACE_SQL = """
 SELECT p.id AS place_id,p.city_id,p.label AS name,
 COALESCE(r.longitude,p.longitude) AS longitude,
 COALESCE(r.latitude,p.latitude) AS latitude,r.id AS revision_id,
 COALESCE(r.valid_at,p.retrieved_at) AS valid_at,
 COALESCE(r.retrieved_at,p.retrieved_at) AS retrieved_at,
 COALESCE(r.source_id,p.source_id) AS source_id,
 COALESCE(r.source_license,p.source_license) AS license_id,
 COALESCE(r.source_version,s.metadata->>'source_version') AS source_version,
 s.metadata AS rights
 FROM places p LEFT JOIN LATERAL (
 SELECT * FROM place_geometry_revisions r WHERE r.place_id=p.id
 AND r.retrieved_at<=%(at)s AND r.valid_at<=%(at)s
 ORDER BY r.valid_at DESC,r.retrieved_at DESC,r.id DESC LIMIT 1
 ) r ON true JOIN sources s ON s.id=COALESCE(r.source_id,p.source_id)
 WHERE p.city_id=%(city)s AND p.retrieved_at<=%(at)s
"""


class IntelligenceService:
    def __init__(self, connection: Connection[Any], access: AccessContext) -> None:
        self.connection, self.access = connection, access

    def _authorize(self, city_id: str, scope: str = "city.read") -> None:
        self.access.authorize(city_id, scope)
        if city_id not in load_cities():
            raise KeyError("Unknown city")

    def _rights(self, metadata: dict[str, Any]) -> SourceMetadata:
        rights = SourceMetadata.model_validate(metadata)
        allowed = (
            rights.research_allowed
            if self.access.purpose == "research"
            else rights.commercial_allowed
        )
        permitted_output = (
            rights.redistribution_allowed
            if self.access.audience == "publication"
            else rights.cache_allowed
        )
        if not allowed or not permitted_output:
            raise PermissionError("Source does not permit this data publication")
        return rights

    def _place(self, row: dict[str, Any]) -> PlaceResult:
        rights = self._rights(row.pop("rights"))
        if (row["source_id"], row["source_version"], row["license_id"]) != (
            rights.source_id,
            rights.source_version,
            rights.license_id,
        ):
            raise ValueError("Geometry source metadata mismatch")
        geometry = Geometry(
            coordinates=(row.pop("longitude"), row.pop("latitude")),
            revision_id=row.pop("revision_id"),
            valid_at=row.pop("valid_at"),
            retrieved_at=row.pop("retrieved_at"),
            source_id=row.pop("source_id"),
            source_version=row.pop("source_version"),
            license_id=row.pop("license_id"),
        )
        return PlaceResult(**row, geometry=geometry, rights=rights)

    def search_places(self, city_id: str, query: SearchQuery) -> SearchResult:
        self._authorize(city_id)
        query = SearchQuery.model_validate(query.model_dump())
        permission = (
            "research_allowed" if self.access.purpose == "research" else "commercial_allowed"
        )
        # Policy predicates precede LIMIT. Fixed internal predicate, never user SQL.
        statement = (
            PLACE_SQL
            + " AND s.metadata->>%(permission)s='true' AND s.metadata->>%(output_permission)s='true'"
        )
        statement += " AND ST_DWithin(ST_SetSRID(ST_MakePoint(COALESCE(r.longitude,p.longitude),COALESCE(r.latitude,p.latitude)),4326)::geography,ST_SetSRID(ST_MakePoint(%(lon)s,%(lat)s),4326)::geography,%(radius)s) ORDER BY p.id LIMIT %(limit)s"
        with self.connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute(
                statement,
                {
                    "city": city_id,
                    "at": query.decision_at,
                    "permission": permission,
                    "output_permission": (
                        "redistribution_allowed"
                        if self.access.audience == "publication"
                        else "cache_allowed"
                    ),
                    "lon": query.longitude,
                    "lat": query.latitude,
                    "radius": query.radius_m,
                    "limit": query.limit + 1,
                },
            )
            rows = cursor.fetchall()
        return SearchResult(
            city_id=city_id,
            decision_at=query.decision_at,
            places=[self._place(r) for r in rows[: query.limit]],
            limit=query.limit,
            truncated=len(rows) > query.limit,
        )

    def get_place_details(self, city_id: str, place_id: str, at: datetime) -> PlaceResult:
        self._authorize(city_id)
        with self.connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute(
                PLACE_SQL + " AND p.id=%(id)s", {"city": city_id, "at": at, "id": place_id}
            )
            row = cursor.fetchone()
        if row is None:
            raise KeyError("Place unavailable at decision time")
        return self._place(row)

    def get_city_state(self, city_id: str, query: StateQuery) -> StateResult:
        self._authorize(city_id)
        query = StateQuery.model_validate(query.model_dump())
        places = [
            self.get_place_details(city_id, pid, query.decision_at) for pid in query.place_ids
        ]
        with self.connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute(
                """SELECT DISTINCT ON (o.place_id,o.feature_key) o.payload,s.metadata
                FROM observations o JOIN places p ON p.id=o.place_id JOIN sources s ON s.id=o.source_id
                WHERE p.city_id=%s AND o.place_id=ANY(%s) AND o.feature_key=ANY(%s) AND o.retrieved_at<=%s
                AND (o.issued_at IS NULL OR o.issued_at<=%s)
                AND o.valid_at<=%s AND (o.data_kind!='forecast' OR
                    (o.valid_until IS NOT NULL AND o.valid_until>=%s) OR o.valid_at=%s)
                ORDER BY o.place_id,o.feature_key,o.valid_at DESC,o.retrieved_at DESC,o.id DESC""",
                (
                    city_id,
                    query.place_ids,
                    list(FEATURE_KEYS) + ["park_way_count"],
                    query.decision_at,
                    query.decision_at,
                    query.target_time,
                    query.target_time,
                    query.target_time,
                ),
            )
            rows = cursor.fetchall()
        parameters = load_parameters()
        features: list[EvidenceResult] = []
        present: dict[str, set[str]] = {p: set() for p in query.place_ids}
        for row in rows:
            o = Observation.model_validate(row["payload"])
            rights = self._rights(row["metadata"])
            if (o.source_id, o.source_version, o.license_id) != (
                rights.source_id,
                rights.source_version,
                rights.license_id,
            ):
                raise ValueError("Observation source metadata mismatch")
            reference = o.issued_at if o.data_kind.value == "forecast" else o.observed_or_valid_at
            clock = query.decision_at if o.data_kind.value == "forecast" else query.target_time
            age = max(0.0, (clock - reference).total_seconds()) if reference else 0.0
            freshness: Literal["within_model_limit", "stale", "unavailable"] = (
                "unavailable"
                if o.value is None
                else "stale"
                if age > parameters.max_age_seconds[o.quality]
                or (o.valid_until is not None and query.target_time > o.valid_until)
                else "within_model_limit"
            )
            features.append(
                EvidenceResult(
                    evidence=o,
                    age_seconds=age,
                    freshness=freshness,
                    rights=rights,
                    uncertainty=["Unvalidated feature construct and spatial representativeness"],
                )
            )
            if o.feature_key in FEATURE_KEYS and o.value is not None and o.unit == "fraction":
                present[o.place_id].add(o.feature_key)
        return StateResult(
            city_id=city_id,
            decision_at=query.decision_at,
            target_time=query.target_time,
            places=places,
            features=features,
            missing_features={p: sorted(set(FEATURE_KEYS) - present[p]) for p in sorted(present)},
            model_version=parameters.version,
            parameter_hash=parameters.digest,
        )

    def evaluate_suitability(self, city_id: str, query: SuitabilityQuery) -> SuitabilityResult:
        self._authorize(city_id, "suitability.read")
        query = SuitabilityQuery.model_validate(query.model_dump())
        state = self.get_city_state(
            city_id,
            StateQuery(
                decision_at=query.decision_at,
                target_time=query.target_time,
                place_ids=[p.place_id for p in query.candidates],
            ),
        )
        candidates: list[Place] = []
        names = {p.place_id: p.name for p in state.places}
        for candidate in query.candidates:
            data: dict[str, Any] = {
                "place_id": candidate.place_id,
                "name": names[candidate.place_id],
                "walk_minutes": candidate.walk_minutes,
            }
            for item in state.features:
                o = item.evidence
                if (
                    o.place_id == candidate.place_id
                    and o.feature_key in FEATURE_KEYS
                    and o.unit == "fraction"
                ):
                    data[o.feature_key] = Feature.model_validate(
                        o.model_dump(exclude={"place_id", "feature_key"})
                    )
            candidates.append(Place.model_validate(data))
        request = EvaluateRequest(
            need=query.need,
            decision_at=query.decision_at,
            target_time=query.target_time,
            max_walk_minutes=query.max_walk_minutes,
            places=candidates,
        )
        assessment = evaluate(request)
        assessment.warning = (
            "Unvalidated hypothesis using stored evidence; proxies are not measurements."
        )
        return SuitabilityResult(
            city_id=city_id, state=state, inputs=request, assessment=assessment
        )

    def compare_places(self, city_id: str, query: ComparisonQuery) -> SuitabilityResult:
        query = ComparisonQuery.model_validate(query.model_dump())
        return self.evaluate_suitability(city_id, query)
