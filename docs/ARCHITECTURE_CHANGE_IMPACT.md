# Architecture change impact — Sprint 2

## Preserved foundation and additive changes

ADRs 0001–0008, migration 0001, deterministic feature weights/transformation, temporal snapshots,
replay and protected evaluation protocol remain intact. ADR-0009 adds service/transport boundaries,
five read APIs, city configuration, geometry revision migration 0002, provider-native parsers,
agent delegation prototype, opportunity contracts and baseline capture audit. No new service,
neural model, reinforcement learning, payment system or production MCP stack is introduced.

| Impact | Result / tradeoff | Evidence / remaining limit |
|---|---|---|
| Stable geometry | Revisions preserve place ID and historical point | Real DB as-of/search/immutability tests; lines/polygons and conflation deferred |
| External contracts | Bounded stored-data reads with rights and city scope | OpenAPI/security/negative tests; one operator only, no external release |
| Scientific core | Same feature definitions and engine outputs | Stored-input parity and old replay tests; constructs remain unvalidated |
| Ingestion | Native count and weather parsing; one real aggregate capture | Count not a scoring fraction; weather issuance/licensing still blocks live replay |
| Evaluation | More auditable genuine-run receipts and information envelopes | No genuine A1 executed; receipts need independent verification |
| Operations | Read-only repeatable transactions, bounded response families | Revised geometry search can require broad scan; five-second timeout is not capacity evidence |
| Commercialization | Publication and purpose checks, future registry isolation | No signed supplier rights, metered ledger, billing or market validation |

Migration 0002 can be applied forward to the local database without modifying old rows. Do not
run downgrade against retained research evidence; test round-trips use their own disposable schemas.
No public deployment or destructive changes to existing project data are part of this sprint.

## Competitive Differentiation and Defensibility

[Competitive analysis](COMPETITIVE_TECHNICAL_ANALYSIS.md) shows substantial overlap with geospatial
infrastructure and tourism digitization. Synta's published API/MCP/GIS direction means an agent
interface alone is not differentiation. Placewave's venue distribution and GOAGENTIC's supplier
data workflows suggest integration boundaries; they do not validate CitySense's environmental model.
Biliki's documented product evolution informs scope discipline; its present operational status is
unconfirmed. These are interpretations of public sources, not independently tested competitor facts.

Candidate defensibility requires a lawful, consented, high-quality micro-place evidence corpus;
observable outcome definitions; withheld independent labels; matched tool-equipped baselines;
versioned replay; honest coverage/uncertainty; and repeatable cross-city validation. Current code
supports these practices but provides no empirical advantage. Avoid a broad “city intelligence”
novelty claim. Human-centered suitability should win a specific independent decision test before
expanding commercial scope. Organic model parameters must remain unaffected by supplier payments.

## Review required and release sequencing

Research lead/statistician: constructs, pairing, blocked holdouts, bootstrap, missingness estimand,
sample adequacy and calibration. Data steward: source-specific purpose/publication and derivative
licenses. Privacy steward: consent/withdrawal/retention before people. Security reviewer: identities,
quotas, TLS, egress and least-privilege DB before exposure. These are pending human reviews, not
fictional approvals. Existing eight-week plan is updated with explicit evidence gates.
