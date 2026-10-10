# CitySense Sprint 1 report — 2026-10-09

## Outcome and acceptance

**Sprint 1: PARTIAL.** The engineering implementation is delivered and all available local
quality gates pass. A separate clean copy installs from the lock without the package cache;
real PostgreSQL/PostGIS stores, retrieves and replays timestamped city-state evidence.
Overall handoff acceptance remains open because this supplied directory has no Git
metadata/upstream for a hosted Actions run, and Docker is unavailable for executing the
pinned Compose/CI image. A configured workflow is not evidence of a green hosted run.

All datasets and comparator outputs supplied here are synthetic. No study, calibrated
model, improved accuracy, psychological measurement, signed data rights, external approval
or production certification is claimed. Review was performed by Codex as an implementation
self-audit across the requested engineering responsibilities.

## Repository audit

Read the entire starter: README/handoff, all four ADRs, architecture, contracts, protected
evaluation draft, security/privacy, source register, supplier specification, delivery plan,
quality documents, API implementation, SQL proposal, request fixture, workflow and tests.
No AGENTS.md was found. The initial modular monolith and separation of offers were retained.

The main weaknesses were unlocked dependencies, inconsistent Python requirements, string
timestamps, absent executable provenance/forecast history, untested SQL, no persistent
feature/model versions, no baseline/evaluation implementation and no API abuse controls.
The documented scientific safeguards were stronger than the code. The existing weights and
proxy constructs were unsupported hypotheses, not errors to conceal with a more complex model.
[ARCHITECTURE_REVIEW.md](ARCHITECTURE_REVIEW.md) contains the multidisciplinary findings.

## Implementation and decisions

| Workstream | Delivered behavior | Decision / tradeoff |
|---|---|---|
| A: environment | Python 3.12.13, uv 0.12.24, exact pins, hashed lock, Ruff/mypy/pytest/Bandit/pip-audit, pinned CI, environment example and local credential initializer | ADR-0005: one verified Python minor and explicit updates; no open transitive drift |
| B: spatial state | Alembic 0001; source/place/observation/model/snapshot/input tables; WGS84 geography, bounds, GiST, immutable evidence and replay | ADR-0006: direct psycopg SQL; SQLAlchemy only supports migration connections; explicit migrations |
| C: ingestion | Typed `get_snapshots`/`source_metadata`, fake and normalized gateway, evidence kinds, units/quality/rights, timeout/retry/429/cache/circuit/size controls | ADR-0008: operator HTTPS allowlist; no licensed provider-native mapper or live unit-test feed |
| D: suitability | Existing need weights in versioned JSON, named fraction transform, walking-time eligibility, exact missingness/staleness abstention, components and parameter hash | ADR-0007: deterministic hypotheses retained; no invented calibrated confidence or probabilities |
| E: evaluation | Synthetic paired manifests; participant/place/place-time/spatial/time grouping and embargo; A0, frozen A1 boundary, B0 and future B1 interface; metrics, exploratory crossed bootstrap, exclusive hashed artifacts | ADR-0007: fail closed on leakage; genuine tool-equipped baseline and calibration need independent evidence |
| F: documentation | Updated specs, handoff, review, risks, scorecard, ADRs and checked evidence | Human review and field/privacy approvals remain distinct from software tests |

Both issued and retrieved timestamps must precede historical decisions. The HTTP gateway
stamps local receipt, retaining upstream retrieval in metadata; fetching an old archive cannot
backdate local knowledge. Stored feature payloads must match their referenced observation.
Model parameters use sorted canonical JSON so database JSON object order cannot alter replay.
Every scoring feature must be usable even if its weight is tiny; missing values are never
silently zeroed or reweighted. Forecast freshness and target validity are separate checks.

## Files created or changed

- Build/runtime: `services/api/pyproject.toml`, `uv.lock`, `.python-version`, root `.env.example`,
  `.gitignore`, `compose.yml`, `.github/workflows/ci.yml` and `.github/dependabot.yml`.
- Domain/API: updated `models.py`, `engine.py`, `app.py`; added `parameters.py`, model JSON,
  `db.py`, `ingestion.py`, `evaluation.py` and `security.py` under `services/api/src/citysense/`.
- Database: `alembic.ini`, migration environment/template and revision 0001 Python/SQL files.
  Original `infra/sql/001_foundation.sql` is explicitly marked legacy and must not be applied.
- Verification: expanded engine tests; added `conftest.py`, ingestion, security, evaluation and
  PostGIS tests; committed synthetic request, observations, source metadata, manifest and A1 fixtures.
- Scripts: quality runner, CI structure validator, fixture builder, synthetic experiment runner,
  explicit database seed and local `.env` initializer.
- Contracts: refreshed `schemas/evaluation-request.example.json`; generated request JSON Schema.
- Documentation: README, CODEX_HANDOFF, architecture, data contracts, evaluation technical
  appendix, security/privacy, delivery plan, source register, original ADR implementation notes,
  new ADRs 0005-0008, four Sprint deliverables and current pointers in `docs/quality/`.
- Evidence: `docs/evidence/quality-gates.json`, `pytest.txt`, dependency audit summary,
  clean-install summary and real HTTP smoke result. Full raw gate logs/JUnit remain in ignored
  `artifacts/checks/`; local binaries, test data and generated credentials stay under ignored `.local/`.

Because no Git metadata was supplied, this is a file inventory rather than a claimed commit diff.

## Actual verification

Environment: Windows, Python 3.12.13, PostgreSQL **16.14**, PostGIS **3.6.2**.
An isolated password-authenticated, loopback-only cluster was created under `.local/` using
copied PostgreSQL tools and the official PostGIS bundle. The existing PostgreSQL service and
its data were not modified. Temporary API/database processes are stopped after verification.

Final main-workspace gates were run by `python scripts/check.py --require-db` in the locked
environment. [Exact gate exits](evidence/quality-gates.json) and [pytest output](evidence/pytest.txt)
are retained. No skipped tests appear in the final run.

| Gate | Actual command / scope | Outcome |
|---|---|---|
| Lock consistency | `uv lock --check` | PASS, exit 0 |
| Formatting | `ruff format --check src tests migrations scripts` | PASS, 23 Python files |
| Linting | `ruff check src tests migrations scripts` | PASS, exit 0 |
| Static types | strict `mypy` | PASS, 11 source/migration files |
| Unit/API/integration | `pytest -q` with required real database | **66 passed**, 1 compatibility warning, 0 skipped |
| PostGIS integration | 12 integration cases within the full suite | PASS; spatial/index, evidence/replay and migration checks |
| Migration lifecycle | upgrade, repeat upgrade, downgrade, re-upgrade in disposable schemas; revision check | PASS, head `0001` |
| Static security | `bandit -r src -q` | PASS, no findings; one narrow statistical-PRNG exception explained in code |
| Dependency security | export all locked groups, `pip-audit --disable-pip --require-hashes` | PASS, **63 packages**, no known vulnerabilities in scanned set |
| CI structure | `python scripts/validate_ci.py` | PASS; YAML triggers/permissions/pins/mandatory database gate and Compose structure |
| Workflow syntax | checksum-verified actionlint 1.7.7, `-shellcheck=` | PASS, exit 0; ShellCheck is explicitly outside this check |
| Clean installation | fresh separate copy, `uv sync --locked --no-cache` | PASS, 64 installed packages including project |
| Clean-copy checks | format, lint, types, full required-DB tests and Bandit | PASS; final code also checked after retrieval guard update |
| HTTP/persistence smoke | real loopback health, evaluate and persisted replay | All HTTP 200; evaluation/replay equal deterministic engine |
| Synthetic experiment | explicit fixture runner plus two-output reproducibility test | PASS; no empirical interpretation permitted |
| Local credential helper | generate in clean copy; repeat refuses overwrite | PASS; generated secret values were not printed |
| Docker Compose execution | `docker compose config --quiet` / daemon | UNAVAILABLE: Docker executable absent; parser structure checked only |
| Hosted Actions run | supplied directory/upstream inspection | UNAVAILABLE: no Git repository/upstream; hosted service/image not exercised |

The clean copy initially passed 65 tests; the final local-receipt regression adds the 66th.
The only final pytest warning is Starlette's deprecated HTTPX TestClient compatibility path;
it is retained, not represented as a test failure. The pinned Docker image uses
PG16/PostGIS3.5; local PostGIS3.6.2 success does not establish that image's compatibility.

## Failures encountered and resolved

| Failure | Classification | Exact disposition |
|---|---|---|
| First expanded full suite: 55 passed, 1 failed, 1 setup error | Mixed implementation and environment | Replay returned 503 because connection options replaced schema search_path; moved statement timeout to `SET LOCAL`. Pytest Temp ACL denied access on Windows; scoped temporaries inside workspace. Subsequent full runs passed. |
| Initial strict typing | Implementation | Two errors: runtime-mode literal narrowing and provider result annotation. Fixed; final strict mypy passes. |
| Initial Ruff checks | Implementation formatting/lint | Import ordering/unused imports and formatting corrected; final lint/format pass. |
| Bandit B311 | Reviewed scanner finding | Seeded bootstrap PRNG is required for statistical reproducibility, not secrets. Narrow `nosec B311`, with explanation; security randomness uses `secrets`/SystemRandom. |
| Pytest 8.4.2 audit | Dependency risk | PYSEC-2026-1845; changed to 9.0.3 and rescanned. |
| uv 0.8.22 audit | Dependency risk | Four archive/path/entry-point advisories; replaced by 0.12.24, regenerated lock and reinstalled/rescanned. No advisory was globally ignored. |
| uv index diagnostic | Tool-version limitation | `uv pip index` was unsupported by the initial bootstrap; used the package index CLI to inspect availability. |
| Requested image tag `16-3.6` missing | External artifact unavailable | Registry returned MANIFEST_UNKNOWN; selected the supported `16-3.5` tag and verified its immutable digest. |
| First manual helper preservation probe | Verification-harness path error | Windows subprocess could not resolve a relative executable; rerun with absolute paths confirmed no overwrite. |
| Docker / hosted CI | Missing dependency / unavailable external execution | Remain open acceptance blockers; no passing result is claimed. |

## Security and research-validity limits

The final package scan is time-specific, covers the selected Python environment and does
not assess host/container operating systems or undisclosed issues. Production still needs
TLS/gateway deadlines, shared quotas, identity/roles, least-privilege database users,
egress controls, image scanning, backups and independent review. No public deployment
or real personal-data collection occurred. The documented launch binds loopback.

No real source rights were cleared, A1 executed, B1 fitted or participant study conducted.
Weights, proxy meaning, freshness, spatial/time blocks and bootstrap assumptions require
independent research review. Frozen baseline hashes and training declarations establish
software contracts, not truthfulness of externally supplied training or tool records.
The protected protocol remains a draft; only an implementation appendix was added.
See the full [risk register](KNOWN_RISKS.md) and [scorecard](QUALITY_SCORECARD.md).

## Prioritized Sprint 2 backlog

1. **Close Sprint 1 acceptance:** connect a reviewed upstream, execute hosted Linux/PostGIS
   CI, run the pinned Compose image and confirm dependency-updater compatibility.
2. **Protect external use:** independent architecture/security/privacy review; TLS/gateway
   quotas and deadlines, runtime database roles, restore drill and deployment/image supply chain.
3. **Acquire lawful evidence:** source-specific rights ledger, provider-native adapters,
   raw archives, lineage/freshness monitoring and reviewed geometry revisions.
4. **Freeze the field design:** independent construct/statistical/ethics review, real consent
   and withdrawal workflows, data dictionary and sufficient independent place/time/person groups.
5. **Execute fair comparison:** freeze genuine A1 prompts/tools/budgets and source availability,
   gather blinded paired labels, then fit B1 on train only and report holdout uncertainty.
6. **Measure operations and transfer:** exporters, p95/retry/error/cost/load observations,
   second-city onboarding, route accessibility and regression fixtures. Defer marketplace work
   until the core context/evidence program has independent support.
