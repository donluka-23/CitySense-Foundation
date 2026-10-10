# ADR-0009 — Agent-first urban intelligence platform

Date: 2026-10-09. Status: accepted for local implementation; external release and scientific approvals pending.
Naming follows existing `0001-*.md` through `0008-*.md`; identifiers are not renumbered.

## Problem and decision

Sprint 1 has a pure deterministic engine, immutable evidence and paired evaluation, but its
calculator accepts caller features and its spatial repository lacks revisionable geometry.
External agents need bounded queries over stored, authorized evidence. CitySense's product
remains human need × place × time × urban state → suitability, explanations and uncertainty.
No psychological measurement, concierge, marketplace or booking runtime is introduced.

Keep the modular monolith. Add `IntelligenceService` for five read capabilities, a REST router,
and an in-process agent adapter prototype over that same service. Existing `/v1/evaluate`,
`/v1/replay`, engine parameters and evaluation protocol retain their semantics. New city APIs
require a configured operator key even in development. City configuration lives in packaged
JSON, outside scoring. Migration 0002 adds point revisions without changing migration 0001.

## Alternatives

| Option | Benefits | Costs / reason |
|---|---|---|
| Extend calculator-only REST | Small change | Cannot independently select stored evidence, enforce publication rights or resolve geometry history |
| Modular monolith + application service + REST | Shared invariants, simple transactions, generated OpenAPI, low operating cost | Application authorization must remain mandatory when adding transports; chosen |
| MCP-first production server | Agent discovery and direct integration | Adds transport authentication, lifecycle and attack surface before empirical value; deferred |
| Separate ingestion, scoring, registry and billing services | Independent scaling | Distributed consistency, queues and operations unsupported by measured demand; deferred |

## Boundaries and compatibility

`models.py`, `parameters.py` and `engine.py` remain the research core. `platform.py` composes
stored evidence, rights, city scope and historical geometry. `platform_api.py` authenticates,
opens a repeatable-read, read-only transaction and maps errors. `agent_tools.py` only validates
arguments and delegates. Native ingestion is explicitly invoked, never on API startup.
Opportunity schemas have no imports into scoring. A commission cannot enter organic ranking.

REST `/v1` is the executable interface. Five stable operation IDs map to five service methods.
Breaking field/semantic changes require `/v2`; schema exports are checked for drift locally
and in the workflow. MCP annotations describe behavior; they confer no permissions.
Transport implementation must preserve the same trusted AccessContext and source policy.

## Identity, publication and costs

Current identity is one local operator, authorized city list and research purpose; application
scopes are `city.read` and `suitability.read`. This is not a tenant account service. Before
external use, add hashed/key-rotatable credentials, tenant and dataset policy, shared quotas,
TLS gateway, trusted proxy rules and independent security review. A commercial principal
must require commercial source permission as well as redistribution permission.

Every new read result carries source rights, geometry provenance, timing and uncertainty.
Research permission alone does not authorize redistribution. Restricted search candidates
are omitted; direct restricted reads return 403. No billing, supplier commissions or paid
provider calls run. Existing telemetry remains bounded route/status latency counters, not
auditable billing. Future usage ledger needs tenant/key/operation, units, provider cost,
response size, timestamp and idempotent request identity, without precise locations in logs.

## Consequences and evidence

Stable place IDs survive corrected point geometry; historical selection uses valid and
retrieved times. Polygon/route revisions and identity conflation remain future work. Spatial
search over resolved revisions is bounded by radius/results and a five-second DB timeout;
its composed expression needs load/index review before scaling. No second-city field transfer
claim follows from the synthetic configuration test. Frozen requests reproduce engine results;
dynamic queries are not permanent snapshots. Independent scientific review remains required.

See [platform architecture](../AGENT_PLATFORM_ARCHITECTURE.md), [API contract](../OPENAPI_CONTRACT.md),
[research readiness](../RESEARCH_VALIDATION_READINESS.md) and the Sprint 2 test evidence.
