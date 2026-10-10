# Sprint 3 retained evidence

These files record actual local implementation verification, not independent scientific/security
certification. Acceptance PARTIAL; empirical performance NOT EVALUATED.

`quality-gates.json` and `pytest.txt`: final 179 passing cases, 31 real PostGIS integration cases,
format/lint/strict types/contract drift/Bandit/lock/audit/workflow success. `test-counts.json` separates
modules, existing 115 cases and 64 additions. `dependency-audit.json` contains all 64 locked packages
and zero reported advisories; hash-required Python scope only, no OS/image assurance.

`clean-install.json`, `clean-quality-gates.json`, `clean-pytest.txt`, `clean-source-parity.json`: fresh
no-cache locked install into a separate checkout/venv, final source synchronization and successful
full gates. Generated editable-package metadata/caches are excluded from executable hash parity.
`setup-smoke.json` records isolated, additive, idempotent synthetic fixture loading and offline demo.

`preserved-foundation.json` compares protected/core/parameter/migration/original fixture/ADR hashes
to the final Sprint 2 executable copy; this is filesystem evidence, not Git history. `changed-files.json`
lists actual added/modified delivered files and their SHA256, excluding its own index and private/
ignored generated files. There is no Git metadata/upstream in this workspace.

`real-source-summary.json` and `retained-db-smoke.json` record actual five-way private OSM inventory,
source times/raw hash, four real-data abstentions, one estimate-based exclusion, exact snapshot replay,
preserved Sprint 1 replay and publication denial. Restricted raw source geometries/records and full
decision receipts remain in ignored `artifacts/sprint3/real-data/`, not this public evidence directory.

`offline-a1-summary.json` and `synthetic-*.jsonl` are actual local CLI executions with entirely
invented model responses/usage. Their fixture timing is retrospective, not eligible empirical
capture. No actual model/account evidence exists. `demo-summary.json` records local adapter/ASGI/
PostGIS transcripts; Telegram was not connected and no real account/location was used.
`unavailable-checks.json` names external/hosted/deployment/research checks that did not occur.

Full redacted logs, JUnit and requirements are retained privately under `artifacts/sprint3/`; no
credentials are delivered. See [report](../../SPRINT_3_REPORT.md) for scope, source rights and next work.
