# Proposed November engineering backlog

Planning status: PROPOSED; no task authorized. Chief owns priorities; Founder owns scope/capacity approval.
Charter: [PROJECT_CHARTER](PROJECT_CHARTER.md). Target November 30, 2026 is contingent, not a promise.
At most three next engineering tickets are proposed. Reviews/prerequisites below are phases, not extra dispatches.

| Priority / ticket | Owner and dependencies | Acceptance |
|---|---|---|
| P0 [T-02 lawful inventory](TICKETS/T-02-INVENTORY.md) | Geospatial Data + Product/Research; FA-02 first tasks, source/provider rights, field access and freshness policy | Reviewed candidate/entrance/constraint coverage manifest; verified vs unknown/stale; publication evidence; no claims of five until supported |
| P0 [T-03 existing-map visual approval](TICKETS/T-03-VISUAL-REVIEW.md) | Cartography + Mobile + independent QA; FA-07 reference/provider/capture/device approval; recover raw evidence first | Lawful actual visual artifacts, attribution/config metadata and separated qualitative/strict/mobile acceptance; no Stage 2 |
| P1 [T-01 integrated selection slice](TICKETS/T-01-VERTICAL-SLICE.md) | Mobile with Platform/Decision; T-02/T-03, FA-01/04/06, approved shared request/retrieval/constraint contract, auth and scope | QR→need→honest shortlist→compare/refine→correct map/evidence→explicit informed selection; stale-response, rights, no-data and access cases; independent QA/human review |

T-01 starts with a contract/readiness phase after explicit authorization. Implementation needs a subsequent
CONTRACT_READY/TASK_READY gate and a Stage 2 authorization if its integration entails Stage 2.
Current Stage 1C code cannot be silently promoted to a production host.
Native roles are read-only defaults; future writer sessions require explicit scoped authorization and path leases.

## Proposed first three weeks after approval

Calendar assumes approval by October 11; shift dates/dependencies if later. Staffing/duration are unverified.
Do not start work because a date passes.

| Window | Dependency-aware proposal | Exit evidence |
|---|---|---|
| Oct 12–18 | Chief obtains FA-01–04/06/07 scope decisions. T-02 inventory and T-03 existing-evidence review may proceed independently if authorized. T-01 phase A scopes shared request/required constraints/retrieval and source/auth boundary. | Named first tasks, honest data coverage/rights, approved privacy/protocol draft, contract/version recommendation; lawful map evidence gap list |
| Oct 19–25 | Complete inventory freshness and visual/device review; resolve retrieval compatibility and freeze consumer contracts. Authorize only a narrow T-01 implementation after readiness and any Stage 2 gate. | Reviewed references/contracts; one lawful end-to-end path, honest fewer/no results, no privileged browser key |
| Oct 26–Nov 1 | Integrate sequentially, exercise stale async responses/refinement/selected geometry and no-data scenarios; independent QA/security plus human physical-mobile/visual acceptance. | Integration matrix evidence, known failures, explicit go/no-go for supervised shakedown |

## November milestones and release dependencies

| Target window | Milestone / predecessor | Gate |
|---|---|---|
| Nov 2–8 | Supervised permissioned shakedown only after data, contract, mobile, privacy and QR permission gates | Founder approves actual rooms/recruitment; proposed 3–5 rollout is not assumed |
| Nov 9–15 | Correct observed failures within approved scope; freeze pilot build/tasks/instrument and support procedure | Independent repeat checks only for changes/failures; versioned evidence and no-go criteria |
| Nov 16–22 | Closed tourist tasks with independently checkable decision evidence and consented minimal events | Actual permission/participants; unknown/unfinished/abstained outcomes included; no superiority claim |
| Nov 23–30 | Decision-quality/efficiency report and founder readiness review; controlled extension only if prior gates pass | State sample/limitations, denominators, costs, incidents; selection/action/fulfillment distinct |

If critical inventory/rights/access/privacy/physical-mobile gates fail, report BLOCKED and reduce scope or
replan with Founder. Never replace missing real evidence with synthetic demonstration or announce pilot success.

## Dependency graph

GOV review → scope/protocol/permissions → T-02 + T-03 → approved shared contract → T-01 integration
→ independent QA/security/human mobile review → closed supervised shakedown → tourist evaluation.

Optional verified contacts depend on actual publication/verification; manual partner request depends additionally
on terms/authority/lifecycle/consent/idempotency/support. Neither blocks standalone tourist selection.
Commercial ordering remains inactive pending CF-02.
A1/B1 research retains its separate protocol and approval gates; genuine A1 is still unverified.
Service RFC review and API readiness preserve future extensibility without building a framework.

## Deferred

No fourth next ticket. Telegram extension, partner workspace, provider integration, payments, eSIM activation,
transport booking, external agent access/writes and multi-city launch require later separate scope/rights decisions.
Proposed numeric VDCR/TVD definitions and performance thresholds do not become release criteria by this plan.

## Stage and next-ticket overlay — approved policy, proposed execution

[STAGE_GATES](STAGE_GATES.md) and [FOUNDER_APPROVALS](FOUNDER_APPROVALS.md) control all future phases.
Existing dates are advisory and must be replanned after actual approvals; no automatic calendar execution.
T-01 Phase A/B each need exact stage/artifact/scope authorization; task readiness is insufficient.
T-03 must satisfy Stage 1B closure or explicit Founder risk waiver before map-style sign-off.
Only T-01–03 remain proposed; no fourth ticket or implementation is dispatched.

Dependency graph (approval arrows require a separate written Founder decision):
UX-0 scope approval → UX-0 actual reference/direction review → UX-1 scope/interaction review →
UX-2 scope/visual review → UX-3 scope/prototype review → UX-4 scope/end-to-end pilot review.
T-02 lawful candidates + approved T-01 contracts/privacy/access and T-03 map evidence feed this chain.
Stage 1B closed/waived → map-style sign-off; UX-3 sign-off → broad functional integration;
independent QA → Founder review at each stage. No predecessor PASS authorizes its successor.

Next scope proposal: bounded UX-0 reference/direction readiness within existing T-03 preparation,
with actual authorized reference evidence, full tourist journey and constraint inventory, independent QA and
Founder direction review; no screen design, new map stage or implementation. Remains BLOCKED.
Smallest later implementation ticket remains [T-01](TICKETS/T-01-VERTICAL-SLICE.md):
one approved need/constraint set, two or more independently evidenced lawful candidates for positive comparison
(up to five only if defensible), QR→need→compare→correct map/evidence→explicit selection and truthful available actions.
Also verify missing/stale/denied evidence yields honest fewer/no options; measure completed selection against the
approved validity instrument without inventing accuracy or numeric pilot success thresholds.
Dependencies: FA-01–04/06/07/10, T-02/T-03, approved schemas/access/privacy, relevant completed UX checkpoints
and separately scoped implementation/map approval. No contacts/booking/payment integration is required.
