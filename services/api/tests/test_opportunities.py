import json
from datetime import UTC, datetime

import pytest
from conftest import FIXTURES

from citysense.opportunities import Offer, ProviderEntity


def provider():
    return dict(
        provider_id="local-provider",
        place_id="local-place",
        city_id="batumi",
        display_name="Synthetic offer",
        geometry=dict(
            coordinates=[41.63, 41.65],
            revision_id=None,
            valid_at="2026-10-09T00:00:00Z",
            retrieved_at="2026-10-09T00:00:00Z",
            source_id="synthetic-fixture",
            source_version="fixture-1",
            license_id="CC0-synthetic",
        ),
        source=json.loads((FIXTURES / "source-metadata.json").read_text()),
    )


def test_discovery_does_not_require_google_or_other_external_map_id():
    entity = ProviderEntity.model_validate(provider())
    assert entity.lifecycle == "discovered" and entity.external_ids == {}
    assert not entity.publication_permission


@pytest.mark.parametrize("change", ["coordinates", "license", "future_geometry"])
def test_opportunity_geometry_cannot_exceed_bounds_rights_or_time(change):
    data = provider()
    if change == "coordinates":
        data["geometry"]["coordinates"] = [200, 41.65]
    elif change == "license":
        data["geometry"]["license_id"] = "undeclared-license"
    else:
        data["geometry"]["valid_at"] = "2026-10-10T00:00:00Z"
    with pytest.raises(ValueError):
        ProviderEntity.model_validate(data)


@pytest.mark.parametrize(
    "fields",
    [
        dict(lifecycle="verified"),
        dict(
            lifecycle="bookable",
            verification_method="document_review",
            last_verified_at=datetime.now(UTC),
        ),
        dict(
            publication_permission=True,
            source={
                **json.loads((FIXTURES / "source-metadata.json").read_text()),
                "redistribution_allowed": False,
            },
        ),
    ],
)
def test_unverified_unconfirmable_and_unlicensed_states_rejected(fields):
    with pytest.raises(ValueError):
        ProviderEntity.model_validate({**provider(), **fields})


@pytest.mark.parametrize(
    "fields",
    [
        dict(price=10),
        dict(availability="confirmed_available"),
        dict(checked_at="2026-10-09T00:00:00Z", valid_until="2026-10-08T00:00:00Z"),
    ],
)
def test_price_and_availability_cannot_be_invented(fields):
    with pytest.raises(ValueError):
        Offer(offer_id="offer", category="guided_walk", title="Synthetic", **fields)
