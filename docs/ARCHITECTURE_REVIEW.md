# CitySense architecture review — 2026-10-09

This file preserves the Sprint 1 audit. Current Sprint 3 evidence appears in
[ADR-0010](adr/0010-prospective-capture-and-private-adapters.md) and
[Sprint 3 report](SPRINT_3_REPORT.md). Historical Sprint 2 evidence appears in
[ADR-0009](adr/0009-agent-first-platform.md), [impact review](ARCHITECTURE_CHANGE_IMPACT.md),
[research readiness](RESEARCH_VALIDATION_READINESS.md) and [Sprint 2 report](SPRINT_2_REPORT.md).

Reviewer: Codex, implementation self-audit. Review responsibilities span architecture,
backend, geospatial, data, research, security and QA/SRE. No independent human approval,
production certification or scientific validation is implied.

## Scope and starting evidence

Read the full supplied repository: README, handoff, all four original ADRs, architecture,
data contracts, protected evaluation protocol, source/privacy/provider specifications,
delivery plan, quality artifacts, request example, SQL proposal, API code and six tests.
No AGENTS.md was found. The supplied directory has no Git metadata or upstream; therefore
no branch, commit, PR or hosted CI run can be attributed to this work.

The product boundary is sound: an urban state and human-suitability engine, with offers
kept outside environmental validity. A small typed modular monolith fits the current team
and evidence constraints. Microservices, a neural model and LLM ranking remain unjustified.

## Findings and disposition

| Perspective | Starting problem | Sprint 1 disposition | Remaining requirement |
|---|---|---|---|
| Architecture | Logical modules mostly documentation; SQL not connected to service | Explicit contract, ingestion, repository, scoring, evaluation and runtime modules | Monitor coupling and measured workload |
| Backend | Open dependency ranges; untyped validator; arbitrary timestamp strings; sparse API tests | Exact pins/lock, strict mypy, aware times, typed errors and negative tests | Pooling, production identity and version policy |
| Geospatial | Correct geography choice, but no actual database/index proof | Alembic schema, generated WGS84 points, bounds, GiST, meter-distance and plan tests | Geometry revisions, polygons, routes, transfer study |
| Data | Provenance/forecast rules existed only in docs; no immutable snapshots | Canonical evidence, observation/source/model/snapshot tables, matching/temporal triggers | Licensed provider mappings and provider-native archives |
| Research | Arbitrary weights and proxy constructs; no actual independent comparator | Explicit unvalidated JSON parameters, exact abstention and frozen comparator interface | Field labels, construct review, train-only calibration |
| Evaluation | No executable split, manifest, metrics or experiment tracking | Group and temporal gates, synthetic paired fixtures, exploratory crossed bootstrap and hashes | Review blocks/estimator and execute genuine strong baseline |
| Security | No auth, request budget, rate limits or diagnostic redaction | Private runtime key mode, body limits, direct-peer quotas, sanitized errors/logs and scans | TLS/gateway, roles, privacy review and load/egress tests |
| QA/SRE | Only six tests; unlocked CI; no PostGIS job | Local gates, real DB tests, pinned CI and retained evidence | Execute hosted Linux/Docker CI and operational recovery drills |

## Contradictions resolved

1. Python support differed between architecture (3.12+) and packaging (3.11+).
   The verified foundation targets Python 3.12.13 and one minor until its matrix is expanded.
2. ADR-0002 promised immutable historical evidence while code used caller features and
   string timestamps. Persistence/replay now enforce availability and lineage.
3. Coverage used a floating threshold to mean all required features. Exact presence now
   controls abstention, including a regression for a tiny required weight.
4. Forecast issuance alone was insufficient against future knowledge. Retrieval time also
   must precede the decision; freshness and forecast horizon are evaluated separately.
   HTTP receipt is stamped locally so remote archive retrieval cannot backdate availability.
5. The old SQL could be mistaken for an applied migration. It is marked legacy; Alembic
   owns schema history. The snapshot envelope extends the original per-place sketch to
   preserve the complete candidate set atomically.
6. A1 was a methodological requirement, not an implemented strong system. Its adapter is
   now executable, while synthetic comparator outputs remain clearly labeled.
7. Old quality notes reported unavailable package downloads/Ruff/PostGIS. Those are
   historical; this session obtained dependencies and exercised a real isolated cluster.

## Unjustified assumptions retained only as hypotheses

Weights, normalized shade/greenery/traffic proxies and freshness intervals have no local
validation. Evidence quality classes are not probability estimates. Walking-time inputs
are caller estimates, without route accessibility or safety validation. Regional forecasts
cannot imply street microclimate. No empirical user ratings, superiority, measured noise,
crowding, psychology or cross-city performance was fabricated.

The crossed bootstrap is exploratory infrastructure, not an approved statistical analysis.
Strict participant/place/time grouping can make the pilot unsplittable. The correct response
is more independent data or a reviewed protocol change, never silently weakening the gate.
External training declarations cannot be proven truthful by an interface alone.

## Decisions and dependencies

ADRs 0005-0008 compare realistic alternatives and record the selected build, persistence,
evaluation and private-runtime designs. Existing ADRs 0001-0004 remain the architectural
starting decisions. All new implementation ADRs await human release/research review.
Concrete quality evidence is in [SPRINT_1_REPORT.md](SPRINT_1_REPORT.md); remaining
security, scientific and operational dependencies are in [KNOWN_RISKS.md](KNOWN_RISKS.md).
