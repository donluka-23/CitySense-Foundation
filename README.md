# CitySense — evidence-first urban suitability foundation

CitySense evaluates urban places against explicit human needs using geospatial and
time-stamped evidence. Batumi is the initial setting; city identity is data, not engine code.
Provider offers and booking remain separate future capabilities.

**Status: Sprint 3 PARTIAL acceptance.** Local engineering checks and real PostGIS tests
pass; hosted GitHub Actions and the Docker setup remain unexecuted in this environment.
Checked-in test datasets are synthetic; five real OSM geometries remain in private ignored archives.
Scores, proxies and freshness limits are unvalidated
hypotheses. There are no empirical research results or production safety claims.
Read [current Sprint report](docs/SPRINT_3_REPORT.md), [architecture review](docs/ARCHITECTURE_REVIEW.md),
[scorecard](docs/QUALITY_SCORECARD.md) and [risks](docs/KNOWN_RISKS.md).

## Clean local setup

Requires Python **3.12.13** and network access for the first install. Windows and Linux
use the same package lock. The bootstrap installer and development tools are pinned.

```sh
python -m pip install uv==0.12.24
cd services/api
uv sync --locked
uv run --locked pytest -q -m "not integration"
uv run --locked uvicorn citysense.app:app --host 127.0.0.1 --port 8000 --no-access-log --no-proxy-headers
```

`GET /health` is liveness only. `POST /v1/evaluate` accepts the complete synthetic example
in [schemas/evaluation-request.example.json](schemas/evaluation-request.example.json).
No provider keys, LLM, account, real person or database are needed for this path.
The strict v0.2 contract requires decision/target timestamps and full feature provenance.

## Local PostGIS and persisted replay

Use Docker Compose or an explicitly selected PostgreSQL 16+ database with PostGIS 3.5+.
The Compose image is digest-pinned and exposed on loopback port 55432. On an existing
local service, choose another unused port and update URLs; never replace its data.
From the repository root:

```sh
python services/api/scripts/init_local_env.py
docker compose up -d --wait
docker compose exec db createdb -U citysense citysense_test
cd services/api
uv run --locked --env-file ../../.env alembic upgrade head
uv run --locked --env-file ../../.env python scripts/seed_synthetic.py
uv run --locked --env-file ../../.env pytest -q
uv run --locked --env-file ../../.env uvicorn citysense.app:app --host 127.0.0.1 --port 8000 --no-access-log --no-proxy-headers
```

The environment initializer generates local credentials, never prints them and refuses
to overwrite an existing `.env`. For an existing database, use `.env.example` as the
field guide and set URLs explicitly. `.env` and local tools/data are excluded from Git.
The seed command is an explicit, one-time synthetic insert; repeat insertion fails rather
than changing evidence. It prints the stable `/v1/replay/{snapshot_id}` URL.
Database migrations never run at API startup. Downgrades destroy evidence and belong only
on disposable databases. Do not apply `infra/sql/001_foundation.sql`, the legacy proposal.

Integration tests require `CITYSENSE_TEST_DATABASE_URL` naming a database ending `_test`.
They create and remove their own random schemas; they do not truncate unrelated tables.
CI sets `CITYSENSE_REQUIRE_DB=1` so missing database configuration fails, rather than skips.

## Quality and fixture reproduction

```sh
uv run --locked ruff format --check src tests migrations scripts
uv run --locked ruff check src tests migrations scripts
uv run --locked mypy
uv run --locked bandit -r src -q
uv run --locked python scripts/check.py --require-db
uv run --locked python scripts/run_synthetic_experiment.py --output ../../artifacts/new-experiment.json
```

For `.env` values add `--env-file ../../.env` before the tool name. `check.py` retains
redacted logs, JUnit results, full dependency audit and gate outcomes in `artifacts/checks/`.
Its workflow syntax gate requires actionlint **1.7.7** on PATH (or in `.local/actionlint/`);
the CI workflow shows the official download and checksum. Without it the gate reports
unavailable. Windows test temporaries are scoped under `.local/tmp` by the runner.
Experiment files use exclusive creation and cannot silently overwrite prior results.
`scripts/build_synthetic_fixtures.py` rebuilds fixed test fixtures and the request schema.
No live network provider is called by unit tests. The normalized HTTP gateway adapter is
a provider boundary, not a completed mapping to a licensed environmental source.

## Repository and guardrails

`models.py` defines evidence; `ingestion.py` normalizes provider boundaries; `db.py` stores
append-only PostGIS state; `engine.py` applies walking-time eligibility and deterministic
scoring; `evaluation.py` enforces grouped independent comparison; `security.py` bounds and
redacts requests. Alembic owns schema history. ADRs document choices and alternatives.

Preserve valid, issued and retrieved times, source/version/license, resolution and method.
Missing data stays missing. Traffic proximity is a structural proxy, not measured noise.
Scores have no psychological units and are not probabilities. Genuine strong baseline runs,
field collection, source rights and calibrated models require independent review.
Private research controls do not satisfy public deployment requirements; consult the risk register.

## Sprint 2 agent and empirical readiness

See [Sprint 2 report](docs/SPRINT_2_REPORT.md), [API contract](docs/OPENAPI_CONTRACT.md),
[platform architecture](docs/AGENT_PLATFORM_ARCHITECTURE.md) and [data governance](docs/DATA_GOVERNANCE_AND_LICENSING.md).
Five `/v1/cities/{city_id}` read operations query authorized stored evidence through one service.
A configured `X-API-Key` is mandatory; `CITYSENSE_READ_CITIES` restricts operator city access.
Keep the process on loopback. MCP is an in-process adapter prototype, not a server.
Opportunity discovery, availability and booking have no operational endpoints.

```sh
uv run --locked python scripts/export_contracts.py --check
uv run --locked python scripts/check.py --require-db --output ../../artifacts/sprint2/checks
```

Migration 0002 adds point revisions; migrate forward explicitly, never at startup.
`demonstrate_osm.py --output PATH` invokes one bounded aggregate retrieval; normal tests/startup
do not call live providers. `persist_osm_archive.py PATH` appends its nonpersonal archived evidence
once to an explicitly configured database. Rights/retention are reviewed per use. No efficacy claim
follows from a capture. The next engineering task and field review gates are in the report.

## Sprint 3 prospective baseline and private Telegram demo

The [A1 runner](docs/A1_BASELINE_RUNNER.md) executes a bounded frozen-context model loop with
typed label-free manifests and retained receipts. Fixture mode is offline and explicitly invented;
live model calls require independent rights review and explicit authorization. No genuine model
call or empirical comparison has occurred. [Real coverage](docs/REAL_WORLD_DATA_COVERAGE.md)
records five source-reported OSM park boundary points, four abstentions and one estimated-walk
exclusion, with exact replay. Required environmental features, routes and availability are missing.

[Telegram setup](docs/TELEGRAM_SETUP.md) provides local offline transcripts and optional authorized
private polling. The adapter uses the authenticated REST application boundary, two explicit modes,
allowlists and no persistent chat/location history. Real OSM publication remains blocked. No
Telegram token, webhook, booking or participant workflow was enabled. See
[acceptance](docs/END_TO_END_ACCEPTANCE.md) and [ADR-0010](docs/adr/0010-prospective-capture-and-private-adapters.md).

```sh
uv run --locked python scripts/run_a1.py --manifest tests/fixtures/prospective-manifest.json --config tests/fixtures/a1-fixture-config.json --output ../../artifacts/new-offline-a1
uv run --locked python scripts/check.py --require-db --output ../../artifacts/sprint3/checks
```
