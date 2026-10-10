"""Future service registry contracts. No discovery, booking or payment runtime."""

from decimal import Decimal
from typing import Literal, Protocol, Self

from pydantic import AwareDatetime, Field, model_validator

from .ingestion import SourceMetadata
from .models import Contract, Identifier
from .platform import Geometry


class Offer(Contract):
    offer_id: Identifier
    category: Identifier
    title: str = Field(min_length=1, max_length=200)
    price: Decimal | None = Field(default=None, ge=0)
    currency: str | None = Field(default=None, pattern="^[A-Z]{3}$")
    duration_minutes: int | None = Field(default=None, gt=0, le=10080)
    availability: Literal["unknown", "unavailable", "reported_available", "confirmed_available"] = (
        "unknown"
    )
    checked_at: AwareDatetime | None = None
    valid_until: AwareDatetime | None = None
    confirmation_method: Literal["none", "provider_api", "operator_confirmation"] = "none"

    @model_validator(mode="after")
    def confirmed(self) -> Self:
        if (self.price is None) != (self.currency is None):
            raise ValueError("Price and currency must appear together")
        if self.valid_until and (not self.checked_at or self.valid_until <= self.checked_at):
            raise ValueError("Invalid availability window")
        if self.availability == "confirmed_available" and (
            self.confirmation_method == "none"
            or self.checked_at is None
            or self.valid_until is None
        ):
            raise ValueError("Confirmed availability requires an operational check and expiry")
        return self


class ProviderEntity(Contract):
    provider_id: Identifier
    place_id: Identifier
    city_id: Identifier
    display_name: str = Field(min_length=1, max_length=200)
    geometry: Geometry
    external_ids: dict[str, str] = Field(default_factory=dict, max_length=10)
    lifecycle: Literal["discovered", "verified", "bookable"] = "discovered"
    verification_method: Literal["none", "document_review", "operator_site_check"] = "none"
    last_verified_at: AwareDatetime | None = None
    source: SourceMetadata
    publication_permission: bool = False
    offers: list[Offer] = Field(default_factory=list, max_length=50)
    booking_confirmation_adapter: Identifier | None = None

    @model_validator(mode="after")
    def lifecycle_evidence(self) -> Self:
        if (self.geometry.source_id, self.geometry.source_version, self.geometry.license_id) != (
            self.source.source_id,
            self.source.source_version,
            self.source.license_id,
        ):
            raise ValueError("Geometry rights require matching reviewed source metadata")
        if self.publication_permission and not self.source.redistribution_allowed:
            raise ValueError("Publication exceeds source rights")
        if self.lifecycle != "discovered" and (
            self.verification_method == "none" or self.last_verified_at is None
        ):
            raise ValueError("Verified identity requires dated verification")
        if self.lifecycle == "bookable" and (
            not self.booking_confirmation_adapter or not self.offers
        ):
            raise ValueError("Bookable entity requires a confirmation adapter and offers")
        return self


class BookingAttribution(Contract):
    request_id: Identifier
    tenant_id: Identifier
    provider_id: Identifier
    offer_id: Identifier
    agent_application_id: Identifier
    organic_assessment_hash: str = Field(pattern="^[a-f0-9]{64}$")


class OpportunityReader(Protocol):
    def discover_local_services(self, city_id: str, category: str) -> list[ProviderEntity]: ...
    def get_service_availability(self, provider_id: str, offer_id: str) -> Offer: ...
