# Sprint 2 execution report — 2026-10-09

**Acceptance: PARTIAL.** Local implementation and executable verification are complete. Hosted
CI/Docker, independent scientific/security/privacy review, full source-specific commercial
clearance, genuine strong A1, B1 calibration and field/cross-city validation remain open.
This is an implementation self-audit by Codex, not an independent certification.

## Outcome and scope

CitySense now exposes five bounded private read operations over stored urban evidence through a
shared application service. Stable place IDs survive append-only point corrections. Native OSM
aggregate/weather parsing and a future genuine-baseline capture audit are implemented. Opportunity
Registry is contracts only. The platform remains human need × place × time × urban state →
unvalidated suitability, explanation and uncertainty; no concierge/marketplace/booking expansion.

The initial audit read the actual foundation, ADRs 0001–0008, reports, protected protocol,
contracts, migrations and tests. It found calculator-only API access, immutable initial geometry,
normalized-gateway-only ingestion and no genuine model-run receipts. These were addressed additively.
The concise implementation plan was followed: city/revision boundary → stored read APIs and rights
→ native mapping and bounded capture → baseline/registry contracts → reviewed documentation/gates.

## Actual files changed

| Area | Added / modified files |
|---|---|
| Application / agent boundary | Added `services/api/src/citysense/platform.py`, `platform_api.py`, `agent_tools.py`; modified `app.py`, `db.py`, `security.py` |
| Data / research / registry | Added `native_sources.py`, `baseline_capture.py`, `opportunities.py`, `parameters/cities.json` |
| Persistence | Added `services/api/migrations/versions/0002_geometry_revisions.py`; migration 0001 unchanged |
| Scripts / CI | Added `scripts/demonstrate_osm.py`, `persist_osm_archive.py`, `export_contracts.py`; modified `scripts/check.py`, `.github/workflows/ci.yml`, `.env.example` |
| Tests | Added `test_platform.py`, `test_native_sources.py`, `test_baseline_capture.py`, `test_opportunities.py`; updated migration-head assertion in `test_postgis.py` |
| Architecture documentation | Added ADR [0009](adr/0009-agent-first-platform.md), [platform](AGENT_PLATFORM_ARCHITECTURE.md), [OpenAPI](OPENAPI_CONTRACT.md), [MCP](MCP_INTERFACE_DESIGN.md), [multi-city](MULTI_CITY_ARCHITECTURE.md), [registry](OPPORTUNITY_REGISTRY_DESIGN.md), [impact](ARCHITECTURE_CHANGE_IMPACT.md) |
| Evidence / strategy documentation | Added [data governance](DATA_GOVERNANCE_AND_LICENSING.md), [competitive analysis](COMPETITIVE_TECHNICAL_ANALYSIS.md), [research readiness](RESEARCH_VALIDATION_READINESS.md), this report and `docs/evidence/sprint-2/` |
| Generated specifications | Added `docs/contracts/openapi.json`, `mcp-tools-design.json`, `provider-entity.schema.json`, `baseline-capture.schema.json`, `weather-candidate.schema.json`, `city-config.schema.json`, `geometry-revision.schema.json` |
| Updated navigation / readiness | `README.md`, `CODEX_HANDOFF.md`, `docs/QUALITY_SCORECARD.md`, `KNOWN_RISKS.md`, `delivery-plan.md`, `ARCHITECTURE_REVIEW.md`, `architecture.md`, `data-contracts.md`, `security-privacy.md`, `provider-onboarding.md`, `source-register.md`, `quality/review-report.md`, `quality/scorecard.md` |

Exact retained file hashes appear in [changed-files.json](evidence/sprint-2/changed-files.json).
This directory has no Git metadata, so no commit/PR/upstream execution is claimed. Ignored `.local/`
holds test tools, clean checkout, isolated PostgreSQL and orchestration helpers; `artifacts/sprint2/`
holds full logs, raw private source capture and persistence receipt. No secrets are in the delivered
schemas/evidence. Synthetic test payloads/receipts remain clearly identified as invented test data.

## Decisions, functionality and tradeoffs

ADR-0009 follows the existing lowercase-number filename convention. Modular monolith and
REST/OpenAPI were chosen over distributed services and MCP-first production deployment. Domain,
application and transport responsibilities are separated; no scoring/network logic is duplicated
in the adapter. Existing calculator, replay, engine, models, parameters and evaluation are preserved.
Stored assessments correct the legacy calculator's caller-input warning to state their stored origin;
all scores/components/exclusions/model fields remain identical for equivalent inputs.

Operational locally: `search_places`, `get_place_details`, `get_city_state`,
`evaluate_suitability`, `compare_places`. New routes require configured operator authentication,
authorized city/scopes and source purpose/redistribution permissions, with read-only repeatable-read
transactions and sanitized errors. State/suitability cap candidates at 30; comparison requires two;
search radius caps at 10 km and results at 30. Missing/stale/uncertain data remain explicit. Walking
times are unverified caller estimates. Dynamic reads do not insert frozen snapshots.

Geometry revision 0002 preserves original place identity/evidence, records both times and lineage,
and prevents ordinary update/delete. Historical searches ignore late-retrieved corrections. Current
revisions are points; polygon/route/conflation and scalable composed query plans remain future work.
Batumi and a synthetic Tbilisi configuration demonstrate boundaries, not cross-city field transfer.

MCP has a typed catalog and in-process delegation prototype only. Registry schemas support internal
IDs, offers, unknown availability, dated verification/confirmation/expiry and rights; no external
map ID is required. A named confirmation adapter does not prove operational bookability. Discovery,
availability and booking tools are not registered or served. Commissions cannot enter organic scoring.

## Actual verification

| Gate / experiment | Actual result | Retained evidence |
|---|---|---|
| Full test suite | **115 passed**, zero skips/failures; **16 real PostGIS integration cases** | `pytest.txt`, `test-counts.json`, full JUnit in ignored artifacts |
| Sprint 1 regression | All original 66 tests pass; 49 new cases added | Test module totals and existing replay/engine assertions |
| Format/lint | Ruff pass | `quality-gates.json`, full logs |
| Types | Strict mypy pass, 18 source/migration files | Same |
| Contract drift | Checked-in OpenAPI/tool/JSON schemas match generated exports | Same; new local and hosted-workflow gate |
| Security | Bandit pass | Same |
| Dependencies | **63 locked packages**, **zero reported vulnerabilities**, hashes required | `dependency-audit.json` |
| Workflow | Structural validator and actionlint 1.7.7 pass | Same; hosted execution not claimed |
| Fresh installation | Separate checkout/venv, `uv sync --locked --no-cache` exit 0; final suite/gates pass there | `clean-install.json`, `clean-quality-gates.json`, `clean-pytest.txt` |
| Migrations | Head 0002, idempotent upgrade and round-trip on disposable test schemas pass | Integration suite |
| Retained local database | Forward migration only; existing snapshot replay unchanged; stored API parity and restricted real-source denial verified | `retained-db-smoke.json` |
| Preserved foundation | Protected protocol, engine, models, evaluation, parameter artifact, first migration, project config/lock match historical Sprint 1 executable copy | `preserved-foundation.json` |
| Live source | One bounded aggregate OSM request, archived and appended/read back identically | `live-source-summary.json`; private raw/persistence files in artifacts |

Tests use PostgreSQL **16.14** / PostGIS **3.6.2** on loopback port 55432. This is not the pinned
Linux image (PG16/PostGIS3.5); Docker executable is absent. There is no upstream to run hosted CI.
The existing host PostgreSQL service was untouched. The isolated sprint cluster was stopped after
verification. No API was publicly exposed and no paid or participant workflow ran.

The initial direct test invocation hit the known Windows temp ACL issue; the project runner's
workspace temp directory resolved it. One new negative test initially reached the consent guard
before its intended tool-receipt guard; the invented fixture was corrected. Final runs above pass.
The existing Starlette HTTPX compatibility warning remains recorded, not suppressed. All package
pins/lock remain unchanged; API interface metadata is 0.3.0, frozen heuristic version is 0.2.0.

## Data sources and licensing status

Real integration: aggregate-only OSM/Overpass count of **10 mapped park ways** in the bounded Batumi
research window, retrieved **2026-10-09T13:37:41.385476Z**; provider database timestamp is separately
**13:36:35Z**. Raw SHA256 `057c1cfa6e6f0587e27ef79f4aeb26bb500fea2effe45dd1b03f02667e39712f`.
It is a mapped-way count in count units, not park area, greenery fraction, local weather or a
suitability feature. Public source results are blocked until the derivative publication plan is
reviewed. [OSM licensing](https://www.openstreetmap.org/copyright) and the
[Overpass service policy](https://dev.overpass-api.de/overpass-doc/en/preface/commons.html)
support this narrow private demonstration, not a production feed or blanket rights clearance.

Open-Meteo native hourly fixture parser is tested for units, timestamps, coordinates, nulls and
unknown issuance. Live remains disabled: [access terms](https://open-meteo.com/en/terms) restrict free
noncommercial access, and ordinary payloads do not provide authenticated issuance/run identity for
historical replay. Overture, Mapbox and Georgian NSDI resources were assessed from official docs;
none was purchased/enabled. Specific storage, redistribution, attribution, quotas, grids/time and
coverage limits are recorded in the governance ledger. No contributor identities or participant
information were collected.

## Competitive findings and differentiation

Public-source review separates facts, vendor claims, inference and unknowns. [Placewave](https://placewave.pro/business)
describes venue assistants/Telegram distribution and affiliate/priority offerings.
[Synta](https://synta.global/) has the strongest infrastructure overlap: public API/MCP/GIS and
geospatial workflow claims. [GOAGENTIC](https://www.goagentic.dev/) emphasizes supplier digitization,
provenance and AI discoverability; its demonstration metrics are explicitly fictional.
Biliki's published history shows self-guided tours evolving toward AI sustainable travel; current
transactional operation remains unconfirmed after failed site/store access, not declared closed.
Full dated sources and caveats are in the competitive report. Some Synta descriptions were available
via indexed official pages when direct subpage retrieval failed; no endpoint access was tested.

These findings do not establish novelty or efficacy. Candidate differentiation is independent
human-need/place/time outcome evidence with lawful lineage, matched strong baselines and honest
abstention/coverage. CitySense currently has no proven advantage or defensible empirical corpus.

## Research review, remaining risks and milestones

The protected protocol is unchanged. Companion proposals mark constructs, split graph, crossed
bootstrap/common-score estimand and cluster sufficiency **REVIEW REQUIRED**. Current shade/green
proxies cannot fully operationalize thermal or family safety/access suitability. A narrow quiet-rest
or thermal target must be independently selected for feasibility; no weights were changed. The
proposed 24 locations are selection criteria, not fabricated surveyed sites or representative coverage.

Capture audit now checks dataset/request hashes, candidate universe, tool/response envelopes, receipt
chronology and token/tool/latency budgets. No genuine A1 was executed. A future runner must receive
label-free inputs; receipts/declarations require independent review. B1 remains train-only future work.
No consented data collection, validated effect size or psychological measurement is claimed.

Highest remaining risks: source-specific commercial/publication and revocation; independent protocol/
privacy approval; genuine A1/held-out labels; operator-only identity/quotas; privileged DB writers and
backdating; geometry/identity/query capacity; hosted Linux/Docker; release recovery and OS/image audit.
See [risk register](KNOWN_RISKS.md), [scorecard](QUALITY_SCORECARD.md) and [eight-week roadmap](delivery-plan.md).

Remaining stages: W3 verified lawful micro-place/context inventory; W4 genuine label-free A1 and
approved design/splits; W5 consent/withdrawal/blinded pilot; W6 frozen holdout readout; W7 train-only
B1 and real second-city evidence if sufficient; W8 economics, operational/release review and honest
report. Human approvals/collection seasons constrain these stages; no automatic release follows.

**Next engineering task:** build the label-free prospective strong A1 runner over frozen lawful tool
responses, with actual provider/model receipts, explicit abstention/timeouts and audited budgets.
Human research/data/privacy review proceeds alongside it. Do not divert this work into supplier or
booking commercialization. The final separate self-review checked scope, no invented measurements,
rights/temporal/auth boundaries, preserved core and distinction between implementation and research;
it does not replace an independent human review.
