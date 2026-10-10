# Local Telegram setup and offline reproduction

Acceptance is PARTIAL: the adapter is implemented/tested, but no real token or polling is authorized
in this sprint. Default commands do not contact Telegram. Use Python 3.12 and the locked environment:

```powershell
cd services/api
uv sync --locked
uv run --locked python scripts/check.py --require-db
```

Configure CITYSENSE_TEST_DATABASE_URL only for a dedicated `_test` database. The tests create/drop
their own random schemas. Local API/DB instructions remain in the root README. Never share .env.

This Windows workspace also retains the isolated sprint cluster, stopped after verification, at
loopback port 55432. Its tools/credentials live under ignored `.local/` and are not portable release
dependencies. From the project root, restart that existing cluster and set the local DB URL without
printing the generated password:

```powershell
& .\.local\postgres\bin\pg_ctl.exe start -D .local/pgdata -l .local/postgres.log -o '-p 55432 -h 127.0.0.1' -w
$taskDatabaseSecret = (Get-Content -Raw .local/pg-password).Trim()
$env:CITYSENSE_DATABASE_URL = 'postgresql://citysense:' + [Uri]::EscapeDataString($taskDatabaseSecret) + '@127.0.0.1:55432/citysense'
cd services/api
```

The retained citysense database already contains the permitted sprint fixtures and private OSM
inventory. Other machines use their own development PostgreSQL/PostGIS instance and local secret
configuration; do not apply migrations or fixtures to an unrelated host database.

Offline transcript through the actual ASGI API and PostGIS service, without opening a network port:

```powershell
uv run --locked --env-file ../../.env python scripts/demo_offline.py --mode synthetic --output ../../artifacts/new-synthetic-transcript.json
uv run --locked --env-file ../../.env python scripts/demo_offline.py --mode real --inventory ../../artifacts/sprint3/real-inventory.json --output ../../artifacts/new-real-transcript.json
```

The database must contain the existing synthetic-example-a/b fixtures for the first command; the
retained sprint database does. These are fixed historical fixtures, labelled fictional throughout.
For a fresh disposable database, use `scripts/load_synthetic_demo.py` as described below. The real
command reads the separately acquired inventory and currently demonstrates publication denial.
Both transcript files use exclusive creation; choose new paths to preserve previous evidence.

The checked-in integration tests load fixtures only in isolated `_test` schemas. For a new local
development database ending `_dev`, set CITYSENSE_DATABASE_URL to its loopback URL, migrate forward
explicitly with `uv run --locked alembic upgrade head`, then run
`uv run --locked python scripts/load_synthetic_demo.py`. The loader rejects non-loopback and other
database names, checks existing immutable records and inserts only missing fictional source/places/
observations. No evidence is overwritten. Do not pass fixtures off as current Batumi measurements.
The demonstration does not start feeds or automatically mutate the database at API startup.

Only after a separate authorized private transport trial, configure these environment variables:

```text
CITYSENSE_TELEGRAM_TOKEN=<authorized token, never committed>
CITYSENSE_TELEGRAM_MODE=synthetic
CITYSENSE_TELEGRAM_ALLOWED_USERS=[<authorized numeric ID>]
CITYSENSE_TELEGRAM_PLACE_IDS=["synthetic-example-a","synthetic-example-b"]
CITYSENSE_OPERATOR_URL=http://127.0.0.1:8000
CITYSENSE_API_KEY=<same local operator key, at least 32 characters>
CITYSENSE_DATABASE_URL=<local development DB secret URL>
```

Start the existing API on loopback in one terminal and private polling in another:

```powershell
uv run --locked --env-file ../../.env uvicorn citysense.app:app --host 127.0.0.1 --port 8000
uv run --locked --env-file ../../.env python scripts/run_telegram.py --authorize-telegram
```

The explicit flag records operator intent to connect; it is not legal/research approval. Do not run
these network commands as part of an offline demonstration. No webhook deployment path is supplied.
Pending updates are dropped on start; transport timeouts and a bounded queue apply. Stop with Ctrl+C;
polling and the operator HTTP client close. No state must be exported or backed up for chat history.

In private chat: /start, /needs, /places, then /evaluate or /near with an explicit supported need,
future zoned time and caller walk estimate. Synthetic fixture features can become stale at future
times: honest abstention is expected, and freshness limits must not be widened to obtain a score.
Real mode needs non-synthetic, independently reviewed publishable sources and selected IDs; current
OSM data is private and remains denied. /sports cannot invent courts or availability.

Troubleshooting: access denied means private chat/allowlist/key/source policy needs review; it is not
an invitation to disable authentication. Invalid request requires zoned times/finite estimates/known
IDs. Evidence unavailable requires checking local API/DB configuration. Do not enable raw HTTPX or
Telegram debug logs: Telegram URLs contain the bot token. No third-party account creation or token
lookup was performed by Codex.
