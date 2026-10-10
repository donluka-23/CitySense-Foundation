# Quality scorecard — Sprint 3, 2026-10-09

Rubric: 0 absent, 1 outline, 2 specified/partial, 3 implemented and tested,
4 operationally demonstrated in the stated scope. Reviewer: **Codex self-audit**.
No independent certification, human sign-off, production readiness or scientific validation.

| Area | Score | Evidence and limit |
|---|---:|---|
| Product/scope clarity | 3 | ADR-0009 and intelligence/registry/distribution boundaries; demand unvalidated |
| Decision auditability | 3 | ADRs 0001–0010, retained capture/decision receipts; independent review pending |
| Data governance | 2 | Primary-source ledger, rights gates, bounded OSM evidence; no blanket commercial clearance |
| Interfaces/contracts | 3 | Five private APIs, negative/auth tests, generated schema drift gate, agent delegation parity |
| Spatial/time correctness | 3 | Real PostGIS revisions/as-of/stored evidence/replay; polygons/conflation deferred |
| Deterministic suitability | 3 | Frozen engine, hard constraints, components and abstention; unvalidated |
| Native ingestion | 3 | Five real OSM geometries archived/stored; no scoring fractions or live weather |
| Empirical outcome evidence | 0 | No independent human labels or genuine A1/B1 execution |
| Research infrastructure | 3 | Prospective typed runner, optional model client, budgets/receipts/later join; no genuine run |
| Telegram interface | 3 | Deterministic adapter over authenticated REST; offline transcripts and negative tests; polling off |
| Private runtime security | 3 | Key/city/scope/rights bounds, read-only transactions, redacted telemetry and scanned packages |
| External identity / quotas | 2 | Requirements specified; one operator and per-process quotas only |
| Operational reliability | 2 | Bounded queries/retries/archives; no SLO/load/recovery or cost observations |
| CI/test automation | 2 | Local gates/workflow syntax pass; hosted Linux/Docker unverified |
| Reproducibility | 3 | Locked pins, deterministic exports and fresh no-cache install; see Sprint 3 evidence |
| Production release chain | 1 | Pinned image; image/OS scan, SBOM/provenance and restore drill absent |
| City extensibility | 3 | Config/revisions/isolation and synthetic second city abstention; no field transfer evidence |

No row earns 4: manual acquisitions and offline mocks are narrower than operational integration.
Scores are not an averaged readiness number. [Sprint 3 report](SPRINT_3_REPORT.md) and
`docs/evidence/sprint-3/` identify current verification. Earlier reports remain historical evidence.
Overall Sprint 3 acceptance is **PARTIAL**; empirical performance is **NOT EVALUATED**.
