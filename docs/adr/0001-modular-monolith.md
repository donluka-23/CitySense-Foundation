# ADR-0001: Modular monolith with deterministic suitability domain
Status: **Accepted for research starter** | Date: 2026-10-09

## Context
Two-person team, eight-week validation deadline, high data uncertainty, need repeatability.
## Decision
Python/FastAPI/Pydantic boundaries, deterministic scoring in dependency-free module, LLM outside ranking. PostgreSQL/PostGIS when persistent storage is needed.
## Alternatives
Microservices: distributed failure/ops cost now unjustified. LLM-as-ranker: brittle and difficult to explain/replay. Large ML model: labeled ground truth insufficient.
## Consequences
Fast iterations and clear interfaces; later extraction requires monitoring module coupling and versioned API contracts.
## Revisit when
Independent service teams or measured scaling/concurrency bottlenecks justify decomposition.

## Sprint 1 implementation clarification

The deterministic domain consumes Pydantic contracts and versioned JSON parameters; it has
no database/network/LLM dependency in its execution path. The original "dependency-free"
wording describes those infrastructure boundaries, not an absence of contract libraries.
ADRs 0005-0008 extend this architecture. Implementation and human release review are
distinct; see the actual self-audit and quality outcomes in the Sprint 1 report.
