# Architecture | v0.2

## Context
Goal: test whether a human-need-specific suitability model yields better *observed place choices* than strong navigation/LLM baselines in Batumi. Product positioning: reusable city context infrastructure, not a travel agency or generic AI chatbot.

## Design tenets
- **Evidence-first**: experiment infrastructure and source-quality metadata ship before an attractive chat UI.
- **Modular monolith**: Python 3.12.13, FastAPI/Pydantic v2, explicit domain boundaries; no microservices until throughput or organizational ownership requires them.
- **Geospatial correctness**: PostgreSQL+PostGIS `geography(Point,4326)` for meter-based filtering, GiST indices; raw vs derived observations distinct.
- **Stable deterministic core**: safety constraints, suitability scoring, uncertainty/coverage, and tie-breaking have no stochastic LLM dependency.
- **Anti-corruption adapters**: weather/OSM/routing feeds normalized before writing snapshots; adapters cannot directly choose recommendations.
- **LLM at the edge**: format explanations from ranked results with structured response contract, no unverified environment assertions.
- **Replayability**: snapshot raw observations plus feature lineage, model/version, full candidate set, consented evaluations.
- **Progressive data fidelity**: forecast/regional, structural spatial proxy, locally audited, instrument observed; do not blend without labels.

## Logical modules
1. `integrations`: per-provider clients, quotas/caching, license ledger, validation, retry/backoff.
2. `city_registry`: versioned spatial place IDs and venue coordinates, source provenance, dedup.
3. `city_state`: spatiotemporal feature snapshots, observation vs forecast semantics.
4. `suitability`: hard feasibility filters, need ontology, explicit scoring, coverage and tie policy.
5. `recommendations`: shortlist and cited user explanations; commercial interests excluded from organic ranking.
6. `opportunity_registry`: separately verified offers, statuses, manual booking requests, hotel attribution.
7. `evaluation`: frozen datasets, place-time-group splits, baseline outputs, experiments, metrics.
8. `platform`: identity/roles, audit, tracing, rate limiting and policy enforcement.

## Lifecycle
```text
Source → adapter/validation → append-only observations → versioned feature build
                                            ↓
User need + candidate universe → hard constraints → scoring + feature availability
                                            ↓
                         ranked options + reasons + confidence/abstention
                                            ↓
                            optional grounded LLM phrasing
                                            ↓
                       audit log + separate opt-in feedback stream
```

## Deploy (after gate)
API container + worker scheduler + managed PostgreSQL/PostGIS, object storage for snapshots, CDN-hosted TS/React web map. Queue only after actual async ingest load. Observability through OpenTelemetry traces/metrics and structured logs; redact personal data.

## Scaling tests
City transfer is not a deployment claim: measure city onboarding steps, dataset mapping, model transfer error, and required manual annotation. API for external agents is a separate product milestone.

## Non-goals for v0.1
Real-time crowd stress, high-resolution street AQI, radar hardware, payments, full inventory marketplace, vector DB, Kubernetes, custom neural models, multi-agent runtime and full 3D digital twin.

## Sprint 1 implementation map

For additive Sprint 2 service boundaries and revisions, see [ADR-0009](adr/0009-agent-first-platform.md)
and [agent platform architecture](AGENT_PLATFORM_ARCHITECTURE.md). The table below is historical.

| Boundary | Code | Limit |
|---|---|---|
| Source contracts | `ingestion.py` | Fake and normalized HTTP gateway; no licensed live provider |
| Spatial registry/state | `models.py`, `db.py`, Alembic 0001 | Point places, append-only observations and candidate snapshots |
| Suitability | `engine.py`, `parameters.py`, packaged JSON | Three unvalidated need hypotheses and named identity transform |
| Replay/API | `app.py` | Caller evidence evaluation and database-backed historical replay |
| Comparison | `evaluation.py` | Synthetic manifests, frozen A1 boundary and leakage gates |
| Runtime | `security.py` | Per-process keys/limits, redacted logs and telemetry stubs |
| Verification | `scripts/check.py`, Actions | Local checks retained; hosted run pending |

ADRs 0005-0008 extend the starter design. Only Alembic revision files are executable
schema history; the original SQL is a marked legacy proposal. API startup performs
neither migrations nor provider ingestion. Operators select database URLs explicitly.
City IDs are data fields; no Batumi-specific branch exists in the engine or repository.
Full route/polygon support, real providers and second-city evidence remain future work.
See [actual outcomes](SPRINT_1_REPORT.md) and [risks](KNOWN_RISKS.md).
