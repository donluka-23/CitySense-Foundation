# Codex implementation handoff | Sprint 3 continuation

## Sprint 3 current state — 2026-10-09

Read `docs/SPRINT_3_REPORT.md`, ADR-0010, A1_BASELINE_RUNNER, REAL_WORLD_DATA_COVERAGE and
TELEGRAM_SETUP first. Label-free prospective capture, optional Responses client, separate later
label join, real geometry parser/workflow and deterministic private Telegram adapter are implemented.
Five real OSM ways remain private in ignored artifacts; four abstentions and one estimate-based
walking exclusion replay exactly. Telegram real mode correctly denies their publication. Synthetic
offline adapter/REST/DB and baseline capture work. No model credential, Telegram connection or human
label was used. Protected engine/models/evaluation/parameters/protocol remain unchanged. Repository
replay restores content-identical packaged parameter order lost by JSONB. Migration head stays 0002;
next ADR is 0011. Acceptance is PARTIAL, and empirical status is NOT EVALUATED.

Do not grant `local_research` audience through HTTP/Telegram. It is for trusted local research/cache
access only; public/private-message redistribution requires its own clearance. No supplied real
entrance, route, forecast issuance, court or operating-availability evidence exists. Next priority:
freeze a publishable verified quiet-rest micro-site/feature envelope and run the actual authorized
strong A1 against it, with independent model/budget/source/privacy review. Do not relax missingness
or divert work into opportunity transactions.

## Historical Sprint 2 state — 2026-10-09

Read `docs/SPRINT_2_REPORT.md`, ADR-0009 and `docs/RESEARCH_VALIDATION_READINESS.md` first.
Sprint 1 is preserved. Private city APIs, shared agent adapter prototype, city configuration,
point revisions, native parsers, opportunity contracts and baseline capture audit are implemented.
Live OSM is a private aggregate demonstration, not suitability validation. Open-Meteo live stays
disabled; ordinary forecast candidates cannot enter historical replay. Next ADR: 0010.
Migration head: 0002; never rewrite migration 0001. No production MCP server, operational registry,
genuine A1/B1 or participant collection exists. The protected protocol is unchanged. Acceptance: PARTIAL.

`scripts/export_contracts.py --check` is a required gate. New city APIs require the configured
operator key even in development; city scope is `CITYSENSE_READ_CITIES`. This is not a tenant platform.
The historical Sprint 1 handoff follows for continuity.

You are implementing the CitySense evidence-first foundation. Do not replace the architecture without a reviewed ADR. Treat `docs/evaluation-protocol.md` as a protected research contract, not an optimizer's target.

## First PRs (independently reviewable)
1. Generate `uv.lock`; pin dependencies; install CI dependency audit; make CI green.
2. Add typed source-adapter interfaces (`get_snapshots`, `source_metadata`), a fake provider and fault tests. Never call external provider in unit tests.
3. Create Alembic migration for PostGIS schema; run PostgreSQL + PostGIS in CI, test spatial/index constraints.
4. Add versioned feature snapshots and replay endpoint; prove historical forecast issuance time never exceeds decision timestamp.
5. Add evaluation dataset manifest, strong baseline adapter boundary, and participant/place-time grouped split fixture; make leakage tests fail closed.
6. Implement automatic security checks, rate limits and metrics/tracing stubs with privacy-redacted logs.

## Role-based review protocol
Tech Lead (human) checks boundaries and ADRs; Research Lead (human) checks construct validity, holdout protocol and leakage; Security/Privacy checklist required for external user collection; Data steward checks legal terms and source lineage; QA validates negative cases. AI agents may act in these roles *as reviewers*, but cannot self-certify production safety or scientific validity.

## Acceptance for sprint 1
CI lint/format/test green on clean machine; SQL spatial tests run; reproducible fixture response; missing data abstains; all delivered datasets provenance-labeled; red-team cases documented. Explicitly record any unfinished item and prohibit marketing claims of validated model.

## Activated handoff — 2026-10-09

Sprint 1 source, migrations, fixtures and local verification are implemented. Read
`docs/SPRINT_1_REPORT.md`, `docs/ARCHITECTURE_REVIEW.md`, `docs/QUALITY_SCORECARD.md` and
`docs/KNOWN_RISKS.md` before continuing. Overall acceptance is PARTIAL because the supplied
directory has no Git metadata/upstream to execute hosted Actions, and Docker is absent.
Real local PostGIS tests and a separate clean locked install have executed; do not replace
that evidence with a claim that the hosted service/image has passed. No model is validated.
Next work must preserve the protected protocol, immutable evidence and synthetic fixture labels.
