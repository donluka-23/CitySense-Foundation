"""Provider-independent normalized boundary. No live provider rights are assumed."""

import random
import time
from collections import OrderedDict
from collections.abc import Callable
from datetime import UTC, datetime
from typing import Protocol, Self
from urllib.parse import urlparse

import httpx
from pydantic import AwareDatetime, Field, TypeAdapter, model_validator

from .models import Contract, Identifier, Observation


class SourceMetadata(Contract):
    source_id: Identifier
    source_version: Identifier
    license_id: Identifier
    synthetic: bool
    research_allowed: bool
    commercial_allowed: bool
    cache_allowed: bool
    redistribution_allowed: bool
    attribution_required: bool
    terms_url: str | None = None
    reviewed_at: AwareDatetime | None = None

    @model_validator(mode="after")
    def live_rights_require_review(self) -> Self:
        if not self.synthetic and any(
            (
                self.research_allowed,
                self.commercial_allowed,
                self.cache_allowed,
                self.redistribution_allowed,
            )
        ):
            if self.reviewed_at is None or not self.terms_url:
                raise ValueError("Live source permissions require dated terms review")
        return self


class SnapshotQuery(Contract):
    place_ids: list[Identifier] = Field(min_length=1, max_length=100)
    target_time: AwareDatetime


class SourceAdapter(Protocol):
    def source_metadata(self) -> SourceMetadata: ...
    def get_snapshots(self, query: SnapshotQuery) -> list[Observation]: ...


class ProviderUnavailable(RuntimeError):
    """Safe public failure; upstream body/credentials are never included."""


class FakeProvider:
    def __init__(self, observations: list[Observation], metadata: SourceMetadata) -> None:
        if not metadata.synthetic:
            raise ValueError("Fake provider requires synthetic metadata")
        self.observations = [o.model_copy(deep=True) for o in observations]
        self.metadata = metadata.model_copy(deep=True)

    def source_metadata(self) -> SourceMetadata:
        return self.metadata.model_copy(deep=True)

    def get_snapshots(self, query: SnapshotQuery) -> list[Observation]:
        return [
            o.model_copy(deep=True)
            for o in self.observations
            if o.place_id in query.place_ids and o.observed_or_valid_at == query.target_time
        ]


class NormalizedHTTPProvider:
    """A normalized gateway adapter, not an implementation of a named weather API.

    Hosts/URL are operator configuration. Redirects are disabled. No user-supplied URLs.
    A licensed provider-specific mapping must be added before live data use.
    """

    def __init__(
        self,
        url: str,
        allowed_hosts: frozenset[str],
        metadata: SourceMetadata,
        client: httpx.Client,
        *,
        timeout_seconds: float = 5,
        max_attempts: int = 3,
        ttl_seconds: float = 60,
        max_cache_entries: int = 128,
        monotonic: Callable[[], float] = time.monotonic,
        sleep: Callable[[float], None] = time.sleep,
        jitter: Callable[[], float] | None = None,
        received_at: Callable[[], datetime] | None = None,
    ) -> None:
        parsed = urlparse(url)
        if (
            parsed.scheme != "https"
            or parsed.hostname not in allowed_hosts
            or parsed.username
            or parsed.password
            or parsed.query
            or parsed.fragment
        ):
            raise ValueError("Provider must use an allowlisted HTTPS URL without credentials/query")
        if (
            not 0 < timeout_seconds <= 30
            or not 1 <= max_attempts <= 5
            or not 0 <= ttl_seconds <= 3600
            or not 1 <= max_cache_entries <= 1000
        ):
            raise ValueError("Invalid provider budgets")
        self.url, self.metadata, self.client = url, metadata.model_copy(deep=True), client
        self.timeout_seconds, self.max_attempts = timeout_seconds, max_attempts
        self.ttl_seconds, self.max_cache_entries = ttl_seconds, max_cache_entries
        self.monotonic, self.sleep = monotonic, sleep
        self.jitter = jitter or random.SystemRandom().random
        self.received_at = received_at or (lambda: datetime.now(UTC))
        self.cache: OrderedDict[str, tuple[float, list[Observation]]] = OrderedDict()
        self.failures = 0
        self.open_until = 0.0

    def source_metadata(self) -> SourceMetadata:
        return self.metadata.model_copy(deep=True)

    def get_snapshots(self, query: SnapshotQuery) -> list[Observation]:
        key = query.model_dump_json()
        if not self.metadata.research_allowed:
            raise ProviderUnavailable("Source is not cleared for research ingestion")
        cached = self.cache.get(key)
        now = self.monotonic()
        if cached and cached[0] > now:
            return [o.model_copy(deep=True) for o in cached[1]]
        if self.open_until > now:
            raise ProviderUnavailable("Provider circuit is open")
        for attempt in range(self.max_attempts):
            retry_after: float | None = None
            try:
                with self.client.stream(
                    "GET",
                    self.url,
                    params={
                        "places": ",".join(query.place_ids),
                        "target_time": query.target_time.isoformat(),
                    },
                    timeout=self.timeout_seconds,
                    follow_redirects=False,
                ) as stream:
                    payload = bytearray()
                    for chunk in stream.iter_bytes():
                        payload.extend(chunk)
                        if len(payload) > 1048576:
                            raise ProviderUnavailable("Provider payload exceeded limit")
                    response = httpx.Response(
                        stream.status_code, headers=stream.headers, content=bytes(payload)
                    )
                if response.status_code == 429:
                    try:
                        retry_after = float(response.headers.get("Retry-After", "1"))
                    except ValueError:
                        # HTTP-date is conservatively treated as unavailable, never retried early.
                        raise ProviderUnavailable("Unusable provider retry budget") from None
                    if not 0 <= retry_after <= 10:
                        raise ProviderUnavailable("Provider retry budget exceeded")
                elif response.status_code < 500:
                    if response.status_code != 200:
                        raise ProviderUnavailable("Provider rejected normalized request")
                    if len(response.content) > 1048576:
                        raise ProviderUnavailable("Provider payload exceeded limit")
                    observations: list[Observation] = TypeAdapter(list[Observation]).validate_json(
                        response.content
                    )
                    received = self.received_at()
                    if received.tzinfo is None or received.utcoffset() is None:
                        raise ValueError("Local retrieval clock must be timezone-aware")
                    for observation in observations:
                        if (
                            observation.source_id != self.metadata.source_id
                            or observation.source_version != self.metadata.source_version
                            or observation.license_id != self.metadata.license_id
                            or observation.place_id not in query.place_ids
                        ):
                            raise ValueError("Provider lineage/candidate mismatch")
                        if observation.retrieved_at > received:
                            raise ValueError("Provider retrieval timestamp exceeds local receipt")
                        # A remote archive's earlier retrieval does not establish local availability.
                        original = observation.retrieved_at.isoformat()
                        observation.retrieved_at = received
                        observation.quality_metadata["upstream_retrieved_at"] = original
                    observations = [
                        Observation.model_validate(o.model_dump()) for o in observations
                    ]
                    ids = [o.observation_id for o in observations]
                    if len(ids) != len(set(ids)) or len(ids) > 1000:
                        raise ValueError("Duplicate/excessive observations")
                    self.failures = 0
                    if self.metadata.cache_allowed and self.ttl_seconds > 0:
                        self.cache[key] = (self.monotonic() + self.ttl_seconds, observations)
                        self.cache.move_to_end(key)
                        while len(self.cache) > self.max_cache_entries:
                            self.cache.popitem(last=False)
                    return [o.model_copy(deep=True) for o in observations]
            except (httpx.TimeoutException, httpx.TransportError):
                pass
            if attempt + 1 < self.max_attempts:
                self.sleep(
                    retry_after if retry_after is not None else min(2**attempt + self.jitter(), 10)
                )
        self.failures += 1
        if self.failures >= 3:
            self.open_until = self.monotonic() + 30
        raise ProviderUnavailable("Provider retry attempts exhausted")


def observation_to_feature(observation: Observation) -> dict[str, object]:
    """Explicit identity transformation only; raw units never silently become fractions."""
    if observation.unit != "fraction":
        raise ValueError("A versioned transformation is required for this raw unit")
    return observation.model_dump(exclude={"place_id", "feature_key"})
