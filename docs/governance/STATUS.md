# Project status

As of 2026-10-10 (Asia/Tbilisi). Bootstrap: governance/configuration prepared; founder review pending.
Scope: no new functionality, Stage 2, integrations, deployment or field study.

## Implementation and evidence dashboard

| Capability | Implementation | Verification / blocker |
|---|---|---|
| Deterministic engine, evidence/time semantics, persisted snapshot replay | IMPLEMENTED | Historical Sprint 1–3 tests; B0 weights/accuracy unvalidated |
| Shared stored-evidence service, five private REST reads, geometry revisions/rights | IMPLEMENTED | Historically locally tested; external identity/access absent |
| Native OSM/weather parsers and bounded capture | IMPLEMENTED COMPONENTS | No operational live recommendation feeds; forecast eligibility unresolved |
| Prospective baseline/A1 runner and audit | IMPLEMENTED TOOLING | Synthetic fixtures tested; genuine model A1 and B1 training not verified |
| Private Telegram command adapter | IMPLEMENTED COMPONENT | Historically tested; real bot/token connection not verified; max three results |
| Registry Offer/ProviderEntity/BookingAttribution/OpportunityReader | CONTRACTS ONLY | No offering discovery/availability/booking runtime |
| Agent tool catalog | IN-PROCESS PROTOTYPE | No MCP server, public agent transport or external authorization |
| Real tourist recommendations | BLOCKED | Five boundary anchors: four missing-data abstentions, one caller walk exclusion; zero scored |
| Stage 1/1B provider comparison | EXPERIMENT IMPLEMENTED; PARTIAL | Technical evidence retained; lawful visual/provider/mobile approval pending |
| Stage 1C MapLibre/MapTiler navigation | EXPERIMENT IMPLEMENTED | Historical 18 JS +9 Python checks; conditional desktop qualitative acceptance |
| Strict map performance / physical mobile | UNVERIFIED | Raw measurement exports and Android/iOS evidence not located in the inspected repository |
| Integrated QR PWA / request / shortlist / map / selection | UNBUILT | Proposed T-01; depends on rights/inventory, versioned constraints/retrieval and design approval |
| Routes/ETA/access/operational availability | UNIMPLEMENTED / UNVERIFIED COVERAGE | Caller walking estimates are not routing or access guarantees |
| Partner workspace, booking/payments/eSIM/drivers | UNBUILT / DEFERRED | No commitments, providers, consent/action runtime |
| Governance and declared role configuration | INSTALLED FOR REVIEW | Current validation receipt; profiles are definitions, not persistent workers |

## Evidence attribution

Sprint 1: 66 passed /12 real PostGIS cases; Sprint 2: 115 /16; Sprint 3: 179 /31.
Sources: [Sprint reports](../SPRINT_3_REPORT.md) and [Sprint 3 count receipt](../evidence/sprint-3/test-counts.json).
Rollback G1 receipt records 148 passed /31 skipped; environment/run differs from retained full DB execution.
These are historical results, not bootstrap reruns. No current API/map test suite was run.
Current governance/configuration/export checks appear only in [bootstrap receipt](BOOTSTRAP_VERIFICATION.json).
No hosted CI, pinned Linux image, field accuracy or tourist pilot is established.

Map evidence: [1B report](../design/MAP_STAGE_1B_REPORT.md), [1C report](../design/MAP_STAGE_1C_REPORT.md),
[1C receipt](../evidence/map-stage-1c/verification.json). User preliminary timing/GOOD feedback
does not establish strict performance; proposed capture directories are not delivered screenshots.
MapTiler Streets v4 is provisional. Stage 2 is unstarted and unauthorized.

## Current repository and team state

Branch stage/1c-map-navigation; audited HEAD eadf331e4b7c262fb5c2216d051f7f6e56a456bf.
Protected baseline 0e0440a28b2d1c82a70aa545c3e8bf3479e0cea0. Initial diff clean; no remote output.
Bootstrap adds only files listed in FILE_MANIFEST. No commits or global settings changed.
Three real read-only subagents audited product/contracts, services/security and map/QA.
Thirteen declared role profiles and portable contracts exist; not thirteen running workers.
Default role layers are read-only and inherit model settings; runtime parent permissions can override defaults.

## Blocked, proposed and next

Contract gates CF-01–03 and extension/privacy seams: [reconciliation](RECONCILIATION.md).
Data/rights, QR access, privacy, scope/capacity and map/device acceptance: [risk register](RISK_REGISTER.md).
November target is at risk; no delivery guarantee or approved numeric KPI threshold.
Proposed next order: T-02 inventory/rights plus T-03 existing-map visual review;
T-01 integrated slice contract design then implementation only after prerequisites and founder authorization.
[Backlog](BACKLOG.md) defines all dependencies and acceptance.
STOP: await governance approval and explicit next-ticket scope; do not start these tickets automatically.

## Current document-intake overlay — 2026-10-10

Blueprint v0.4 and AEOS v1.2 now exist as full verified canonical files; see [versions](VERSION_REGISTER.md).
The source-availability gap in the historical acceptance report is closed. All 45 inherited statuses are unchanged;
P-005–007 add three DECIDED controls. Header version discrepancies are recorded outside unchanged sources.
Current maintenance verification: see [receipt](evidence/document-intake/verification.json) and
[Founder packet](FOUNDER_REVIEW_PACKET.md); maintenance PASS with independent QA; stage DOC-INTAKE-2026-10-10
is FOUNDER_REVIEW, not APPROVED_COMPLETE. Review artifact: intake-final-1.

Orchestration acceptance remains historical PARTIAL. Native profile loading, enforced filesystem isolation,
actual integrated UI/runtime and physical-device acceptance remain unverified.
Governance controls are documentation, not executable permission enforcement.
[STAGE_GATES](STAGE_GATES.md) defines UX-0–4; every future stage is blocked pending explicit approval.
Stage 1B remains PARTIAL; map-style approval requires closure or explicit risk waiver.
CF-01/02/03 are proposals only; no pilot metrics, commercial priority or /v1 semantic change accepted.
Inventory/rights/placement/privacy/access/visual/device blockers remain in [risks](RISK_REGISTER.md).
No product implementation, visual captures, map stage or deployment occurred during this intake.

## Landing visual overlay - 2026-10-11

LANDING-UX0-VISUAL-v1 / landing-ux0-r1: FOUNDER_REVIEW; static artifact verification and independent QA PASS.
Six desktop/mobile compositions and source/reference package in [packet](../design/landing/UX0_FOUNDER_REVIEW_PACKET.md).
Founder layout acceptance is pending. These drawings are not a running landing page or proof of tourist-product readiness.
Integrated journey remains BLOCKED; Stage 1B PARTIAL, Stage 2 unauthorized. No new partner/integration/runtime claim.
Historical rows and documentation-stage completion approvals are unchanged.


## Latest Founder-directed LANDING-WEB revision - 2026-10-11

This overlay supersedes the earlier r1 awaiting-review status only: Founder reviewed H1/H2/H3 as REQUEST CHANGES.
Historical r1 technical QA PASS and all artifacts remain untouched. Current administrative stage LANDING-UX0-VISUAL-v1;
track LANDING-WEB, artifact landing-web-ux0-r2, CR-0001; [current packet](../design/landing/revisions/landing-web-ux0-r2/FOUNDER_REVIEW_PACKET.md).
Bounded revision: six S1/S2/S3 Home artboards, eight fold details, one Partners desktop/mobile page, state sheets and optional timed previews.
Execution is approved; final direction/completion is NOT APPROVED. Final QA outcome and FOUNDER_REVIEW transition are recorded in the current packet after actual review.
PRODUCT-APP remains out of scope with independent UX-0 through UX-4. No layout/color/component inheritance or product readiness is inferred.
Contact/publisher/jurisdiction/policies and actual affiliate/partner qualification remain pending. Stage 1B PARTIAL, integrated product BLOCKED, Stage 2 unauthorized.
No protected code/research/API/decision source is modified; no integrations, accounts, publication or Git mutation performed.

R2 final technical delivery: **FOUNDER_REVIEW**; independent corrected visual QA PASS and scoped integrity/export checks PASS.
The initial mobile-divider PARTIAL finding and correction/review history are retained in the r2 evidence.
Stage completion/direction acceptance remains NOT APPROVED; public release remains BLOCKED by inputs and separate authorization.
