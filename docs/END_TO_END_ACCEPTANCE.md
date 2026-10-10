# End-to-end acceptance — Sprint 3, 2026-10-09

**PARTIAL acceptance; empirical performance NOT EVALUATED.** Real geometry ingestion, stored
feature joins, hard filtering, original-engine abstention and persisted replay executed locally.
The Telegram adapter's synthetic and rights-denied real transcripts executed through authenticated
ASGI REST and PostGIS, without Telegram connectivity. A genuine model call and usable real-data
ranking did not occur. These are engineering observations, not independent certification.

Outdoor target: an evening Batumi outdoor decision with current/forecast conditions, walking
constraints, real geometry and uncertainty. The retained explicit time is 2026-10-09 20:00 Tbilisi
(16:00Z), selected while still in the future; there is no natural-language time inference. The
`quiet_rest` feasibility target is narrower than general outdoor/psychological suitability.

| Acceptance dimension | Actual test/observation | Result and limit |
|---|---|---|
| Entity discovery | Five real skeleton OSM park ways, stable IDs/raw geometry | Source discovery demonstrated; entity accuracy/entrances not independently verified |
| Environmental completeness | Stored join finds no eligible scoring fractions or weather | Missing inputs explicit; 0/5 environmental coverage |
| Hard constraints | Four caller estimates 20 min, one 45 min, cap 30 | One exclusion; four pass estimated filter only, no verified walking route |
| Suitability | Original quiet-rest engine, frozen 0.2.0-unvalidated parameters | Four null scores, zero valid recommendations; no reweighting/count proxy |
| Actual availability | No access/opening/operational source | Unknown; no claim facilities are available |
| Explanation | Missing greenery/traffic, estimates, unknown weather/access, provenance | Machine-readable reasons and honest no-result; human explanation-quality review pending |
| Replay | DB snapshot plus frozen parameters and private full decision receipt | Exact assessment replay, including quiet-rest reason order |
| Telegram | Local synthetic adapter → key-protected REST → DB; real mode → same policy | Fictional scores displayed; real-source output denied, not silently published |
| A1 | Three offline CLI captures and later synthetic receipt/label join tests | Invented responses/usage; no real provider/model performance |

Sports fixture: three outdoor basketball courts at 19:00, weather exposure, walking access and
verified availability. /sports explicitly reports insufficient court inventory, weather, routes
and availability, returning zero court suggestions. No court discovery/availability API exists.
This deterministic failure is implemented and tested; the sports product capability is not delivered.
If 19:00 has already passed, a later real request must explicitly choose another date rather than
claim a current forecast for a past decision.

Private raw inventory and both real snapshots are in ignored `artifacts/sprint3/real-data/`; the
20:00 snapshot is `69d05735-0024-4375-84dc-04ca7a5a8b46`. Local transcripts are
`artifacts/sprint3/telegram-synthetic.json` and `telegram-real.json`. Public retained summaries under
`docs/evidence/sprint-3/` omit raw source coordinates/records and secrets. Reproduction commands are
in [coverage](REAL_WORLD_DATA_COVERAGE.md), [A1 runner](A1_BASELINE_RUNNER.md) and
[Telegram setup](TELEGRAM_SETUP.md). No external model or Telegram account was contacted.

Full product acceptance still needs publishable verified activity sites, eligible environmental
features, lawful run-aware weather, routes/access/availability, actual authorized model/Telegram
receipts and independent protocol/privacy/security reviews. A scored synthetic transcript proves
transport and software composition only. It does not establish accuracy, utility, superiority,
commercial conversion or a defensible empirical corpus.
