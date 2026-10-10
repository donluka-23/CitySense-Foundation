"""Strict normalized features. Quality labels describe evidence, not accuracy."""

from datetime import UTC, datetime
from enum import Enum
from typing import Annotated, Literal, Self
from uuid import UUID

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, field_validator, model_validator

Identifier = Annotated[str, Field(min_length=1, max_length=128, pattern=r"^[a-zA-Z0-9_.:-]+$")]


class Contract(BaseModel):
    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)


class Need(str, Enum):
    COOL_WALK = "cool_walk"
    QUIET_REST = "quiet_rest"
    FAMILY_WALK = "family_walk"


class FeatureQuality(str, Enum):
    REGIONAL_FORECAST = "regional_forecast"
    DERIVED_SPATIAL = "derived_spatial"
    OBSERVED_MANUAL = "observed_manual"
    MEASURED_LOCAL = "measured_local"
    REPORTED_PROVIDER = "reported_provider"
    UNKNOWN = "unknown"


class DataKind(str, Enum):
    OBSERVED = "observed"
    FORECAST = "forecast"
    DERIVED = "derived"
    PROXY = "estimated_proxy"
    UNAVAILABLE = "unavailable"


class Evidence(Contract):
    value: float | None
    quality: FeatureQuality
    data_kind: DataKind
    source_id: Identifier
    source_version: Identifier
    license_id: Identifier
    method_version: Identifier
    unit: str = Field(min_length=1, max_length=32)
    observed_or_valid_at: AwareDatetime
    issued_at: AwareDatetime | None = None
    retrieved_at: AwareDatetime
    valid_until: AwareDatetime | None = None
    spatial_resolution_m: float | None = Field(default=None, gt=0)
    quality_metadata: dict[str, str] = Field(default_factory=dict, max_length=20)

    @field_validator("observed_or_valid_at", "issued_at", "retrieved_at", "valid_until")
    @classmethod
    def utc_times(cls, value: datetime | None) -> datetime | None:
        return value.astimezone(UTC) if value is not None else None

    @model_validator(mode="after")
    def evidence_semantics(self) -> Self:
        if self.data_kind == DataKind.FORECAST:
            if self.issued_at is None or self.quality != FeatureQuality.REGIONAL_FORECAST:
                raise ValueError("Forecast requires issued_at and regional_forecast quality")
        elif self.issued_at is not None or self.quality == FeatureQuality.REGIONAL_FORECAST:
            raise ValueError("Forecast issuance/quality requires forecast data_kind")
        if self.issued_at is not None and self.issued_at > self.retrieved_at:
            raise ValueError("Forecast issuance exceeds retrieval")
        if self.data_kind != DataKind.FORECAST and self.observed_or_valid_at > self.retrieved_at:
            raise ValueError("Observation/derivation exceeds retrieval")
        if self.valid_until is not None and self.valid_until < self.observed_or_valid_at:
            raise ValueError("Invalid validity interval")
        if (self.data_kind == DataKind.UNAVAILABLE) != (self.value is None):
            raise ValueError("Unavailable must have null value; numeric evidence requires a value")
        if self.data_kind == DataKind.UNAVAILABLE and self.quality != FeatureQuality.UNKNOWN:
            raise ValueError("Unavailable evidence must have unknown quality")
        if self.data_kind in (DataKind.DERIVED, DataKind.PROXY):
            if self.quality != FeatureQuality.DERIVED_SPATIAL:
                raise ValueError("Spatial derivations/proxies require derived_spatial quality")
        if self.data_kind == DataKind.OBSERVED and self.quality not in (
            FeatureQuality.MEASURED_LOCAL,
            FeatureQuality.OBSERVED_MANUAL,
            FeatureQuality.REPORTED_PROVIDER,
        ):
            raise ValueError("Observed values require observed evidence quality")
        return self


class Feature(Evidence):
    value: float | None = Field(ge=0, le=1)
    unit: Literal["fraction"]
    observation_id: UUID | None = None


FEATURE_KEYS = ("feature_shade", "feature_greenery", "feature_traffic_proximity")


class Place(Contract):
    place_id: Identifier
    name: str = Field(min_length=1, max_length=200)
    walk_minutes: float = Field(ge=0, le=10000)
    feature_greenery: Feature | None = None
    feature_shade: Feature | None = None
    feature_traffic_proximity: Feature | None = None


class EvaluateRequest(Contract):
    need: Need
    decision_at: AwareDatetime
    target_time: AwareDatetime
    max_walk_minutes: float = Field(default=45, ge=0, le=180)
    places: list[Place] = Field(min_length=1, max_length=100)

    @model_validator(mode="after")
    def request_semantics(self) -> Self:
        self.decision_at = self.decision_at.astimezone(UTC)
        self.target_time = self.target_time.astimezone(UTC)
        if self.target_time < self.decision_at:
            raise ValueError("Target time precedes decision")
        ids = [p.place_id for p in self.places]
        if len(ids) != len(set(ids)):
            raise ValueError("Duplicate place_id")
        for place in self.places:
            for key in FEATURE_KEYS:
                feature = getattr(place, key)
                if feature is None:
                    continue
                if feature.retrieved_at > self.decision_at:
                    raise ValueError("Evidence retrieved after decision")
                if feature.issued_at is not None and feature.issued_at > self.decision_at:
                    raise ValueError("Forecast issued after decision")
        return self


class ScoreComponent(Contract):
    feature_key: str
    value: float
    weight: float
    contribution: float
    data_kind: DataKind
    quality: FeatureQuality
    source_id: str


class RankedPlace(Contract):
    place_id: str
    score: float | None
    coverage: float
    status: Literal["insufficient_data", "scored_unvalidated"]
    reasons: list[str]
    components: list[ScoreComponent]
    confidence: Literal["unvalidated", "insufficient_evidence"]


class Exclusion(Contract):
    place_id: str
    reason: str


class EvaluateResponse(Contract):
    model_version: str
    parameter_hash: str
    candidate_ids: list[str]
    ranked: list[RankedPlace]
    excluded: list[str]
    exclusions: list[Exclusion]
    warning: str


class SpatialPlace(Contract):
    place_id: Identifier
    city_id: Identifier
    name: str = Field(min_length=1, max_length=200)
    longitude: float = Field(ge=-180, le=180)
    latitude: float = Field(ge=-90, le=90)
    source_id: Identifier
    license_id: Identifier
    retrieved_at: AwareDatetime


class Observation(Evidence):
    observation_id: UUID
    place_id: Identifier
    feature_key: Identifier


class FeatureSnapshot(Contract):
    snapshot_id: UUID
    build_version: Identifier
    created_at: AwareDatetime
    request: EvaluateRequest
    model_version: Identifier
    parameter_hash: str = Field(pattern=r"^[0-9a-f]{64}$")

    @model_validator(mode="after")
    def snapshot_chronology(self) -> Self:
        self.created_at = self.created_at.astimezone(UTC)
        if self.created_at < self.request.decision_at:
            raise ValueError("Snapshot construction precedes decision")
        return self
