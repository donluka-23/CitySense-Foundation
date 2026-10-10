# Sprint 3 execution report — 2026-10-09

**Acceptance: PARTIAL. Empirical performance: NOT EVALUATED.** Local engineering implementation,
real geometry acquisition, stored abstention/replay and offline baseline/Telegram verification are
complete. No external model credential, genuine A1 call, Telegram token/polling, participant data,
public deployment or paid service was used. Independent source/publication, protocol/privacy/security
reviews, usable real environmental features, routes/availability, hosted CI and Docker remain open.
This is a Codex implementation self-audit, not independent certification.

## Architecture decisions and preserved foundation

The repository audit inspected Sprint 2 code, ADRs 0001–0009, protected protocol, source ledger,
contracts, migrations, tests and retained evidence. The actual gaps were an audit-only baseline
boundary, count-only real OSM evidence and no Telegram adapter. Work followed the requested order:
prospective runner → real geometry/stored workflow → deterministic transport → gates/documentation.

[ADR-0010](adr/0010-prospective-capture-and-private-adapters.md) keeps the modular monolith and
existing service/REST boundary. Typed label-free scenarios are separate from later human-label
datasets; a provider-neutral model client supplies optional Responses I/O. A trusted local research
audience requires research/cache permission; publication remains the default for HTTP/Telegram,
requiring redistribution. Telegram calls the authenticated operator API, not a separate engine.
No MCP server, marketplace, itinerary, booking, payment or supplier integration was added.

Protected protocol, engine, models, evaluation, parameters, original fixtures and both migrations
match the final Sprint 2 executable checkout; hashes appear in preserved-foundation.json. Migration
head remains 0002; no migration/startup ingestion changed. Existing tests remain intact. The project
version is still 0.2.0, API metadata 0.3.0 and heuristic `0.2.0-unvalidated`. The next ADR is 0011.

A real quiet-rest replay exposed JSONB object-key reordering: scores were unaffected, but ordered
reason arrays differed. Repository.replay now restores the content-identical packaged parameter
artifact when its digest matches. This preserves the frozen engine and fixes exact reason/component
ordering for its packaged version; unknown future parameter versions still need an explicit ordering
contract. A real PostGIS regression covers this case.

## Actual implementation and files

| Area | Added / changed |
|---|---|
| A1 generation | Added `baseline_runner.py`: typed frozen geometry/request/source envelopes, provider-neutral client, optional OpenAIResponsesClient, deterministic FixtureClient, budgets/tool loop and hash-chained receipts |
| Later comparison | Added `prospective_audit.py`, `scripts/run_a1.py`, `compare_a1_b0.py`, `build_sprint3_fixtures.py`; the existing capture/evaluation contracts remain unchanged |
| Real context | Added `real_context.py`, `scripts/real_workflow.py`; modified `platform.py` for explicit local research audience and `db.py` for matching packaged-order replay |
| Telegram | Added `telegram_demo.py`, `scripts/run_telegram.py`, `demo_offline.py`, `load_synthetic_demo.py`; modified `.env.example`, exact PTB dependency in pyproject/uv.lock |
| Tests/fixtures | Added `test_baseline_runner.py`, `test_baseline_limits.py`, `test_prospective_audit.py`, `test_real_context.py`, `test_telegram_demo.py`, two clearly synthetic label-free JSON fixtures |
| Contracts | Extended exporter; four new JSON schemas for prospective manifest, runner config, inventory and Telegram settings; existing REST/tool/other schemas unchanged |
| Documentation | Added six required Sprint 3 documents plus ADR-0010; updated README, handoff, scorecard, risks, research readiness, roadmap, architecture navigation and future registry boundary |

Exact added/modified file hashes relative to the preserved final Sprint 2 copy appear in
[changed-files.json](evidence/sprint-3/changed-files.json). No Git metadata/upstream exists, so no
commit, PR or hosted execution is claimed. `.local/` contains ignored test tools/isolated clusters/
fresh checkout and execution helpers; `artifacts/sprint3/` contains full private captures/logs.
Delivered evidence contains no credentials, participant identities or raw restricted source records.

## A1 runner status and empirical integrity

Three actual offline CLI runs completed, each with an explicitly invented provider/model response,
one frozen-context tool read, null choice and invented 280-token usage. They are synthetic engineering
checks, not genuine A1. Exact payloads/tool outputs/raw replies, model/config hashes, timestamps,
reported usage and reserved costs are retained in exclusive hash-chained receipts. Provider/account
authenticity is not proven by a hash chain. Source permissions and no-personal-data declarations
require independent review. A live run rejects synthetic data, missing transfer/redistribution
permission and an already-reached decision. The CLI is executable with a later explicitly authorized
key/config/manifest; no live credential was inspected or used.

Generation never accepts labelled DatasetManifest or B0 results. Geometry and request candidate
universes match; freeze/source/retrieval/issuance times, annotations, tool arguments, candidate
eligibility and token/tool/request/time/cost limits are checked. Unknown/invented candidates and late
replies invalidate predictions. 429 retry is bounded; ambiguous billed timeouts are not retried.
Exact model-ID matching requires an independently reviewed supported snapshot. Byte/framing token
reservations and operator tariffs remain engineering assumptions; invoices/cancellation need live
review. Later audit checks hashes, configuration, request reservations, raw provider usage, terminal
choice and complete candidate universe against the separately approved labelled dataset. Failed
runs block joining until a missingness policy is reviewed. No denominator-selection shortcut exists.

The synthetic later-join tests execute the unchanged A0/A1/B0 harness. No real accuracy, effect size,
calibration, superiority or cross-city transfer was estimated. Protected grouping/holdout/embargo
rules and exploratory crossed estimator are unchanged. See [runner](A1_BASELINE_RUNNER.md) and
[research readiness](RESEARCH_VALIDATION_READINESS.md).

## Real versus synthetic data and end-to-end outcome

Real data: one successful bounded skeleton-geometry OSM retrieval returned **five park ways** with
stable IDs, actual vertices and separate database/retrieval timestamps. Retrieved
**2026-10-09T15:15:11.042337Z**, provider database **15:13:08Z**; raw SHA256
`9c54e6cde7ebbd2b1dfdd8b6d138c3bf86a8692c43ca517209ce219e93db11b8`.
Raw polygons and the normalized inventory remain in ignored private artifacts. Skeleton output
contains no author/contact/free-form tags. A point is a selected actual boundary vertex, not a
verified entrance, independent entity survey or suitable interior. No field or participant data exists.

At explicit **20:00 Tbilisi on 2026-10-09**, the actual stored `quiet_rest` evaluation produced
**four abstentions, one hard walking exclusion, zero non-null scores**, model/parameter lineage and
missing feature reasons. Walking estimates of 20/45 minutes were deliberately supplied, not measured
routes. No weather, shade, noise, greenery fraction, traffic fraction, crowding, accessibility or
operating availability was invented. The earlier next-day 19:00 request is also retained. The final
evening snapshot is `69d05735-0024-4375-84dc-04ca7a5a8b46`; exact replay succeeded. A private decision
file preserves full geometry/state/rights/explanation in addition to the scoring snapshot.

Publication checks still deny this inventory. [OSM licensing](https://www.openstreetmap.org/copyright)
and the [Overpass policy](https://dev.overpass-api.de/overpass-doc/en/preface/commons.html) support
this narrow private demonstration; attribution/derivative/share-alike/revocation review precedes
external use. The old park-way count is unchanged and never becomes a scoring fraction.
[Open-Meteo eligibility/terms](https://open-meteo.com/en/terms) and historical issuance remain
uncleared, so live weather is off. No route provider or unsanctioned scraping was substituted.

Selected narrow feasibility proposal: fixed-window quiet-rest comparison with independent acoustic
exposure checks. This is not an approved scientific construct. The smallest technical gap for the
current quiet-rest engine is fresh lawful normalized greenery and traffic features with reviewed
footprint/orientation/method. Full outdoor acceptance additionally needs verified sites/entrances,
run-aware weather, routes and operating access. See [coverage](REAL_WORLD_DATA_COVERAGE.md).

Synthetic data: original clearly fictional feature/place fixtures, new label-free baseline cases,
invented provider replies/adversarial receipts and offline Telegram transcripts. No synthetic
recommendation is presented as a current Batumi fact. Sports /sports returns zero courts and explicit
missing court/weather/routes/availability. No three courts or bookings were invented. Acceptance
dimensions and limitations are separated in [END_TO_END_ACCEPTANCE.md](END_TO_END_ACCEPTANCE.md).

## Telegram readiness and security

The application builds locally without network or persistence. /start, /help, /needs, /places,
/evaluate and coordinate /near use bounded deterministic interactions. Responses display up to three
scored unvalidated indices, components/reasons, exclusions, target/model, freshness/missingness and
uncertainty. Source-reported real map points are labelled unverified; fictional mode has no purported
verified map links. Current real data cannot be published and correctly produces rights denial.

Actual offline runs exercised Telegram adapter → key-protected ASGI REST → stored PostGIS services.
Synthetic mode displayed fictional scores; real mode denied publication. Anonymous operator calls
returned 401. Disposable fresh-database setup and repeated fixture loading succeeded idempotently
(one source, two fictional places, six observations), followed by the same offline transport path.

No real Telegram token, account ID, polling/webhook or public port was enabled. Token lives only in
the process environment; static private-user/place allowlists, per-user quotas, bounded input/body/
reply/queue, sequential handlers, dispatch/HTTP timeouts and sanitized errors apply. No raw chat,
location or user history is stored. Child library logs have a null sink to prevent token-bearing URLs
from fallback logging. Loopback operator auth and source policy are retained; no local-research
capability is exposed through the adapter. This remains an operator demo, not tenant production auth.

The one new locked dependency is [python-telegram-bot 22.8](https://docs.python-telegram-bot.org/en/stable/),
compatible with existing HTTPX 0.28.1 and upstream LGPL-3. No optional framework/webhook packages
were enabled. All former dependency pins remain unchanged. Advisory scope is the locked Python set,
not host/container OS or undisclosed defects. Operational model/hosting/transport costs were not
measured. See [specification](TELEGRAM_DEMO_SPEC.md) and [setup](TELEGRAM_SETUP.md).

## Actual quality gates and retained evidence

| Gate | Actual final result | Evidence under docs/evidence/sprint-3 |
|---|---|---|
| Full suite | **179 passed**, zero failures/skips; **31 real PostGIS integration cases** | pytest.txt, test-counts.json; full JUnit in private artifacts |
| Regression | All original 115 cases pass; 64 new cases | Module counts and protected-file parity |
| Lock/format/lint | uv lock --check, Ruff format/check pass | quality-gates.json; full logs in artifacts |
| Types | Strict mypy passes, 22 source/migration files | quality-gates.json |
| Contracts | Existing exports plus four new schemas match generator | quality-gates.json |
| Security | Bandit passes | quality-gates.json |
| Dependency audit | **64 locked packages**, **zero reported vulnerabilities**, required hashes | dependency-audit.json |
| CI definitions | Structural check and actionlint 1.7.7 pass | quality-gates.json; hosted execution not claimed |
| Fresh installation | Separate checkout/venv, uv sync --locked --no-cache and identical full gates pass | clean-install.json, clean-quality-gates.json, clean-pytest.txt |
| DB/migrations/replay | Existing migration round-trip/as-of/auth suite, new private research and exact quiet-rest replay pass | Full suite plus retained-db-smoke.json |
| CLI/setup | Three offline captures, two mode transcripts, isolated idempotent fixture setup pass | offline-a1-summary.json, demo-summary.json, setup-smoke.json |
| Preserved foundation | Protocol/core/parameters/migrations/original fixtures byte-identical to Sprint 2 | preserved-foundation.json |

The isolated database is PostgreSQL **16.14** / PostGIS **3.6.2**, loopback 55432; the existing host
PostgreSQL service was untouched. It is not the pinned Linux PG16/PostGIS3.5 image. Docker is absent;
Compose/image execution was unavailable. No upstream/Git metadata means hosted CI unavailable.
The isolated sprint cluster was stopped after verification. No code was publicly deployed.

During development: one initial Overpass request without the specific research User-Agent returned
406; the corrected bounded request succeeded. A test initially used the wrong feature-key name and
the PTB concurrency assertion initially assumed 0 instead of its serialized value 1; these fixtures
were corrected. Quiet-rest replay exposed the JSONB-order defect described above and was fixed.
Final runs pass; the existing Starlette HTTPX compatibility warning remains recorded, not suppressed.

The final privacy review also moved skeleton-envelope validation before raw archive writes; an
adversarial CLI test proves an unexpected contributor field is rejected without saving raw bytes.
Final executable source was synchronized into the fresh installed checkout and all gates repeated
there after this change; dependency pins did not change.

## Remaining gates, roadmap and next task

Highest risks: real source publication/revocation and verified activity geometry; feature construct/
direction and missing environment; independent consent/privacy/holdout review; genuine strong A1 and
provider/archive/billing authenticity; reviewed failed-run missingness; single operator identity/
per-process quotas; privileged DB backdating/immutability bypass; route/query capacity; hosted Linux,
release recovery/OS scanning and second-city evidence. [Risk register](KNOWN_RISKS.md) and
[scorecard](QUALITY_SCORECARD.md) do not declare scientific or production readiness.

W3: verify a small lawful rest-site/feature inventory and publication plan. W4: reviewed genuine A1,
budget/source equivalence, split/estimand/missingness simulation. W5: consent/withdrawal/blinded
pilot only after approval. W6: frozen independent holdout with coverage/uncertainty/cost readout.
W7: train-only B1 and second-city evidence if sufficient. W8: honest evidence/economics/release review.
Weather season and human approvals constrain these evidence stages; no automatic launch follows.

Meni.ge is only a potential future restaurant-systems integration. Its [public descriptions](https://meni.ge/)
mention restaurant/POS, reservations/waitlist and agent interfaces; no partner relationship, credential,
verified endpoint or transaction exists. Registry contracts remain extensible and commission-neutral.

**Next highest-value engineering task:** freeze the smallest independently verified, publishable
quiet-rest micro-site/feature envelope and exercise the implemented runner with an actually authorized
strong model, retaining real account/tool receipts. Data/research/privacy reviewers must resolve
construct, forecast/history, matching and consent gates alongside it. Additional Telegram polish or
supplier transactions do not resolve these evidence gaps. Final separate self-review checked scope,
protected-core parity, privacy/auth/rights/time boundaries, raw-versus-synthetic claims, replay and
budget/failure receipts; it does not replace independent review.
