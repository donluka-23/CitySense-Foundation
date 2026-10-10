# ADR-0008: Bounded ingestion and private-by-default research API

Date: 2026-10-09. Status: implemented local controls; public deployment review pending.

## Problem and constraints

Provider faults, oversized input, unbounded requests and diagnostic logs can turn a small
research service into an unreliable or privacy-invasive system. There are no accounts,
commercial provider rights, real participants or production identity provider in Sprint 1.

## Decision

Expose provider-independent `source_metadata` and `get_snapshots` interfaces, a synthetic
fake and an HTTP adapter for normalized gateways. Preserve every canonical evidence field.
HTTPS operator host allowlists and disabled redirects reduce SSRF exposure. Bound retries,
HTTP timeouts, decompressed payload size, TTL cache entries and circuit recovery. Do not
retry schema/lineage validation failures or permanent HTTP errors. Respect bounded numeric
Retry-After; fail closed for excessive delays or HTTP-date values. Never substitute a stale
cache entry. Caching requires explicit permission; live permission claims require a dated
terms review. No provider is enabled on API startup and no live unit-test requests occur.

The API limits candidates, field lengths, finite values and streamed request bytes. A
per-process direct-peer limiter ignores forwarded addresses. Optional development keys
become mandatory in production mode; compare keys in constant time and never log them.
Runtime settings hide secrets in their object representation. Logs contain static route
templates, status and duration only. Validation errors omit submitted values. OpenTelemetry
API spans, counters and fixed latency buckets are stubs for a future exporter. The default
development command disables Uvicorn access logs and forwarded-header trust.

## Tradeoffs and remaining requirements

An API key is adequate for a private single-team prototype, but provides no user roles,
per-user access checks or rotation workflow. In-memory limits/caches do not coordinate
multiple workers; production needs a trusted gateway and shared quota control. TLS,
ingress connection/read deadlines, database runtime roles, egress DNS/IP controls,
tracing exporters, consent deletion workflows and load tests remain release gates.
Default development mode must bind loopback; no public deployment is performed here.

Redis, a full identity platform and distributed workers were deferred because they add
operations without current load evidence. HTTP-date retry handling is intentionally
conservative. Provider-native normalization, licensing decisions and retrieval-time stamping
must be implemented for each actual provider; the gateway boundary does not certify a source.

The normalized gateway stamps local receipt as `retrieved_at`, retaining the upstream
timestamp in quality metadata. An archive fetched later cannot backdate local availability
to its original remote retrieval. The receipt clock is injectable for deterministic tests.

## Evidence

Mock transport tests cover timeout, 429, retry exhaustion, cache expiration, circuit opening,
oversized responses, invalid contracts, redirects and source mismatch. API tests cover keys,
chunked oversized bodies, forwarded-header abuse, failure responses and log redaction.
Bandit and all-dependency audit outcomes are recorded in [report](../SPRINT_1_REPORT.md).
