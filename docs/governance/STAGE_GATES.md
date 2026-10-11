# Sequential stage gates

Authority: [AEOS v1.2](CITYSENSE_AGENTIC_ENGINEERING_OPERATING_SYSTEM_v1_2.md) appendix,
Blueprint P-005–007 and [current request](evidence/document-intake/USER_REQUEST.md).
Owner: Chief maintains central stage/approval records sequentially. Founder alone approves scope, completion and advancement.

## Permission and lifecycle

Delivery-stage lifecycle:
DRAFT_PLAN → READY_FOR_SCOPE_REVIEW → APPROVED_TO_EXECUTE → IN_PROGRESS → TECH_QA →
FOUNDER_REVIEW → APPROVED_COMPLETE | CHANGES_REQUESTED | REJECTED | ON_HOLD.

Permission is separate: every new phase is BLOCKED_AWAITING_FOUNDER_APPROVAL until a written decision identifies
the exact stage ID, artifact version and scope. TECH_QA includes independent review before FOUNDER_REVIEW.
Chief cannot grant Founder acceptance. Green CI, technical PASS, silence, elapsed time, agent consensus,
roadmap dates and predecessor completion never authorize a successor.
Revisions retain the same stage ID and identify the revised artifact; expanded scope needs a CR and fresh approval.
Existing task states (including CONTRACT_READY/TASK_READY) remain subordinate to their enclosing stage permission.
This is a documentary/manual control, not a proven CI or runtime permissions enforcement mechanism.

## Current gate

| Stage | Lifecycle / permission | Artifact and owner | Evidence / incomplete | Next permitted action |
|---|---|---|---|---|
| DOC-INTAKE-2026-10-10 | FOUNDER_REVIEW / authorized maintenance only | Blueprint v0.4 + AEOS v1.2; intake-final-1; Chief | [approval](FOUNDER_APPROVALS.md), [verification](evidence/document-intake/verification.json), [independent reviews](evidence/document-intake/REVIEW_HANDOFFS.md); independent QA PASS, Founder completion not recorded | Submit [packet](FOUNDER_REVIEW_PACKET.md) and stop |
| Any new development / map stage | DRAFT_PLAN / BLOCKED_AWAITING_FOUNDER_APPROVAL | Unapproved next-stage artifact | T-01–03 remain proposals; no accepted scope/contract/UX approval inferred | Prepare bounded scope for Founder review; no execution |
| Map provider Stage 1B closure | Existing PARTIAL evidence / no new execution authority | Existing reports; Cartography + QA | [Stage 1B report](../design/MAP_STAGE_1B_REPORT.md); no new closure or explicit waiver recorded | Request evidence-backed closure scope or explicit Founder waiver with risks |

Stage 1B must be closed or explicitly waived with recorded risks before any map visual-style sign-off.
Conditional Stage 1C desktop feedback does not close Stage 1B, all visual phases or physical-mobile acceptance.

## UI/UX checkpoints — each independently Founder gated

All five rows are DRAFT_PLAN / BLOCKED_AWAITING_FOUNDER_APPROVAL. No checkpoint is accepted.
Actual checkpoint artifacts and visual approval are absent; old map screenshots are not integrated-journey approval.

| Stage | Required actual review evidence | Founder decision / dependency |
|---|---|---|
| UX-0 | Reference board, journeys, constraints, design principles, anti-patterns, authorized reference inventory; real visual references or interactive evidence with rights | Approve direction before screen design. First obtain scoped execution approval. |
| UX-1 | Low-fidelity flows/navigation, PWA versus Telegram entry, map/search/card/compare state transitions; actual screenshots or interactive low-fidelity prototype | After UX-0 completion, separately approve scope; Founder approves interactions before high-fidelity exploration. |
| UX-2 | Distinct high-fidelity alternatives from actual production basemaps and realistic Batumi content; mobile-first previews at stated viewports | After UX-1 completion and separate execution approval; select/reject direction. Stage 1B closed or explicitly waived before map-style sign-off. |
| UX-3 | Approved design-system implementation and interactive prototype; screen diffs, localization, empty/unknown/error/loading, touch/accessibility | After UX-2 completion and separate execution approval; sign off before broad functional integration. |
| UX-4 | Verified end-to-end journey with real or explicitly sandboxed data, physical-mobile QA, truthful provenance/attribution, dated screenshots/video and reproducible demo | After UX-3 completion and separate execution approval; Founder decides pilot readiness. |

Do not approve missing visuals from prose. Artificial pseudo-screens do not prove running UI.
Screenshots/prototypes support visual judgment; tests support correctness; physical-device checks remain distinct.
Capture/artifact creation itself requires approved scope and lawful source/provider rights.

## Journey coverage, without relabeling history

Historical orchestration phases 0–7 are journey segments, not design-maturity stages.
Reference, QR entry, need/clarification, alternatives, compare/refine, map/evidence,
selection/actions and integrated mobile must each be represented in UX-0 reference/journey work,
UX-1 interaction flows, UX-2 screen alternatives, UX-3 prototype/state coverage and UX-4 end-to-end acceptance
where applicable. For each segment record actual artifact path, revision, viewport/device, source rights,
independent QA result and explicit Founder visual decision. An N/A needs a reason and Founder-reviewed scope.
Telegram extension is deferred; UX-1 must explain its boundary, not implement another client.

## Required stage packet

Use [HANDOFF_TEMPLATE](HANDOFF_TEMPLATE.md): stage ID; goal/user value; original approved scope;
completed/uncompleted work; actual working demo URL and reproduction command where applicable;
dated desktop/mobile screenshots/video; source rights/provenance; tests/failures;
security/accessibility/performance knowns/unknowns; deviations; risks; before/after; dependencies;
next-stage proposal; specific requested decision. Include independent QA identity, reviewed artifact version and result.
Documentation-only intake demos/screenshots are N/A: no UI changes or captures authorized.
Missing evidence must be marked missing, never replaced by a descriptive claim.

