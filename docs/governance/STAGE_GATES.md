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


## Scoped Landing UX-0 overlay - 2026-10-11

Administrative stage LANDING-UX0-VISUAL-v1; artifact landing-ux0-r1. Chief-assigned labels identify this exact task.
The Founder explicitly authorized creating high-fidelity **static landing concepts inside UX-0**, after selecting the hybrid direction.
See [actual request](../design/landing/SOURCES/USER_REQUEST.md), [source reconciliation](../design/landing/SOURCE_INTAKE.md)
and [execution approval](FOUNDER_APPROVALS.md#fa-landing-ux0-2026-10-11-001).
This is a task-specific overlay, not a change to generic integrated-product UX-0 through UX-4 definitions or protected technical contracts.
Brief high-fidelity approval was pending; current authority permits bounded exploration, not acceptance of completed layouts.

Lifecycle: APPROVED_TO_EXECUTE -> IN_PROGRESS -> TECH_QA -> FOUNDER_REVIEW only after actual independent QA.
The [Landing packet](../design/landing/UX0_FOUNDER_REVIEW_PACKET.md) records the current exact result/revision.
Current result: FOUNDER_REVIEW after actual independent QA PASS on landing-ux0-r1. This is static artifact readiness only.
Founder completion and visual acceptance remain NOT RECORDED. No successor is authorized.
Actual static artboards are evidence for composition review, not screenshots of a running UI or map provider.
Generic product UX-1/2, map Stage 1B closure/waiver, implementation, publication and deployment retain separate gates.


## LANDING-WEB r2 track and revision overlay - 2026-10-11

Source: [current direct Founder request](../design/landing/revisions/landing-web-ux0-r2/SOURCES/CONSOLIDATED_FOUNDER_REQUEST.md).
Historical r1 human review is now REQUEST CHANGES. CR-0001 explicitly authorizes same-stage static revision and one Partners desktop/mobile concept.
LANDING-UX0-VISUAL-v1 stays the administrative stage; LANDING-WEB is the track; landing-web-ux0-r2 is the reviewed artifact.
Lifecycle: CHANGES_REQUESTED -> APPROVED_TO_EXECUTE -> IN_PROGRESS -> TECH_QA -> FOUNDER_REVIEW after actual image QA;
APPROVED_COMPLETE requires a real scoped Founder decision. No completion approval is recorded.

LANDING-WEB serves small corporate/partner public presence. PRODUCT-APP is a separate PWA/desktop track with its own independent UX-0 through UX-4 Founder gates.
Website palette, layout, component patterns, illustrative interactions and motion do not bind PRODUCT-APP. Shared brand may be proposed, separately evaluated and approved.
Every future UI/UX phase requires its own approved scope, actual visual evidence and Founder visual review; no acceptance inherits by silence or predecessor success.
Public contact/policies are pending facts. Static EOI collects nothing. Publication, production UI and affiliate/partner integrations require separate authorization.
Stage 1B remains PARTIAL; this photo/diagram concept grants no map-style sign-off, risk waiver or new map stage.
