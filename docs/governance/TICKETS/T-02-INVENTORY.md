# T-02 — Rights-cleared tourist candidate inventory

Owner: Geospatial Evidence & Data. Review: Product/Research, Security and Chief.
Decision IDs: P-002, R-001, R-007, R-009, G-001, X-007.
Charter: [PROJECT_CHARTER](../PROJECT_CHARTER.md).
User outcome: first selected tourist tasks can be supported by lawful verifiable candidate facts.

## Scope, inputs and paths

Review current coverage and proposed task-specific place/activity inventory near Orbi.
Inputs: REAL_WORLD_DATA_COVERAGE, source-register, END_TO_END_ACCEPTANCE, geometry/evidence schemas,
SourceRights and the selected first tasks. Existing Batumi polygon-boundary anchors do not establish
verified entrances or task-specific tourist coverage.
Proposed owned paths: new docs/evidence/pilot-inventory/ review manifest/report only; not created in bootstrap.
Read-only dependencies: existing captures, protected models/ingestion/platform and source restrictions.
No data import/API/storage change; an ingestion implementation would need separate approved scope.

Prerequisites: FA-02 task/constraint scope and staffing; source display/publication rights;
authority for field/partner verification and any network retrieval; retention/freshness policy.
Report every unsupported criterion. Do not demand five entries if fewer defensible ones exist.

## Acceptance and checks

- Actual stable identity and geometry meaning; do not label first polygon vertex as entrance.
- Required vs soft task criteria; hours, budget, time, entrance/access and travel facts separately evidenced or unknown.
- Source/method/version, checked/retrieved/valid times and publication/redistribution/archival rights per assertion.
- Reviewed larger candidate pool and missing coverage; no selected ID cutoff presented as retrieval recall.
- Missing/stale/contradictory/unauthoritative values fail safely; inaccessible source remains blocked.
- Explicit time for re-verification and responsible owner. No model-accuracy or availability guarantee.
- Chief/Research review establishes whether the chosen tasks can honestly yield defensible results.

Test plan after authority: validate the manifest against approved evidence/geometry semantics;
independent spot-check required criteria and denial/staleness examples. No test of invented values.
Evidence: approved manifest and reviewer records; real/synthetic segregated, no private contacts.
Open questions: first tasks, eligible source rights, field access, operational hours/access/price authority,
inventory size/coverage and refresh cost. Unknowns are permitted outputs, not completion claims.

No execution is authorized by this proposed ticket. Use HANDOFF_TEMPLATE and a Chief-assigned base/path lease.
Protected: Sprint 1–3 code/contracts/ADRs/protocol/parameters/migrations, Stage 1/1B/1C evidence and user work.
Rollback: remove/revert only ticket-owned additions or patches after inspecting current diff; never reset unrelated work.
Delivery state: PROPOSED / CR_DRAFT. Founder approval and open prerequisites remain PENDING.

## Current stage permission

[STAGE_GATES](../STAGE_GATES.md) and [FOUNDER_APPROVALS](../FOUNDER_APPROVALS.md) govern this proposed ticket.
Permission: BLOCKED_AWAITING_FOUNDER_APPROVAL. Every phase needs its exact stage/artifact/scope approval;
CONTRACT_READY/TASK_READY and predecessor completion are insufficient.
Independent QA precedes Founder review; UX-0–4 each need actual visual artifacts and separate Founder approval.
Stage 1B closure or explicit Founder waiver with risks is required before map visual-style sign-off.
No product, capture, new map stage or downstream execution is authorized by this update.
