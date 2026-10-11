# Chief Engineer orchestration and integration

This operating procedure follows the approved AEOS/bootstrap; product implementation still requires a ticket.

1. Read STATUS, portfolio, decisions, relevant ADRs/contracts and actual Git diff. Check approvals and active agents.
2. Translate the founder request into decision IDs, user outcome and affected interfaces. Record new ideas without executing them.
3. Resolve prerequisites and approval-sensitive contradictions through a CR. Unaffected additive work may continue.
4. Assign one accountable owner and a path lease with ticket ID, base revision, allowed paths and expiry at handoff.
   Shared models, generated schemas, migrations, API semantics, auth policy and central governance have one sequential writer.
5. Give each worker the ticket, its role and necessary contracts. Delegate independent read audits or disjoint authorized writes.
   Default to few workers; this session has four total slots including Chief. Profiles are not a running workforce.
6. Accept a HANDOFF_TEMPLATE response, inspect changed paths against lease, verify actual execution and rights caveats.
   Return incomplete or conflicting handoffs; stop overlapping writes before resolving.
7. Integrate sequentially. Check schema/semantic compatibility, protected hashes and downstream consumers.
   Do not create branches/worktrees, stage/commit or merge unless the authorized task calls for it.
8. Run change-appropriate checks. Use independent QA and security review where impacted; preserve failed/invalid evidence.
   Visual changes need actual lawful screenshots and human review; emulation does not prove physical-device acceptance.
9. Prepare a concrete founder packet: behavior, paths, contracts, tests, screenshots, risks, rollback and unresolved decisions.
   Human acceptance is distinct from integration and tests.
10. Update STATUS, board stage, interface versions, integration evidence and risks. Close ownership leases and record next context.

## Task lifecycle

IDEA_INBOX → TRIAGED → CR_DRAFT → FOUNDER_APPROVED → CONTRACT_READY → TASK_READY
→ IN_PROGRESS → INTEGRATION_REVIEW → QA → HUMAN_ACCEPTED.

Record blocking conditions separately from lifecycle stage; never skip a missing prerequisite.
Minor internal repairs may use a brief scope/acceptance record inside existing authorization.
Material product/science/commercial ranking/privacy/vendor/payment changes require explicit founder decisions.
An urgent security finding may be triaged immediately; urgency does not expand current session authorization.

## Shared-file and interface rule

No producer changes a contract without consumer review, version strategy and acceptance cases.
Chief reserves docs/contracts/, models.py, migrations and shared platform policy for sequential assignment.
Owners listed in ROLES are accountable domains, not blanket permission to edit paths.
New frontend/service paths are unassigned until approved; do not create speculative modules.

## Handoff and recovery

Use ticket IDs and repository artifacts, not whole-chat replay. Give a worker 1–2 pages of scope plus exact dependencies.
On interruption, preserve changes and record lease, pending checks, approval state and safe next action in STATUS.
On restart compare actual HEAD/diff with the handoff base before applying it.
If native roles are unavailable, separate scoped sessions use the same lease and handoff; do not assume they synchronize.

## Mandatory delivery-stage overlay — AEOS v1.2

Read [versions](VERSION_REGISTER.md), [stage gates](STAGE_GATES.md) and [approval ledger](FOUNDER_APPROVALS.md).
The task lifecycle above operates only inside an explicitly approved delivery stage. CONTRACT_READY/TASK_READY,
technical PASS, green CI, silence or predecessor completion cannot authorize execution/advancement.
Use the exact new stage lifecycle in STAGE_GATES. Chief assigns bounded tickets, base/artifact version,
path leases and role/consumer contracts only within the approved scope; shared contracts and ledgers stay sequential.
Stage 1B closure or explicit Founder risk waiver must precede map-style sign-off.
UX-0–4 each require separate scope and actual visual evidence/Founder decisions; journey segments are coverage cases,
not substitutes. No capture or prototype is created without its scoped authority.

Integrate handoffs, inspect protected bytes and contracts, then obtain independent QA before Founder review.
If review finds material changes, correct within current scope and obtain targeted independent re-review.
Prepare every field in HANDOFF_TEMPLATE's stage packet; mark missing/N/A evidence truthfully.
Append exact Founder decisions with timestamps/provenance and stage/artifact/scope; never infer old approvals.
CHANGES_REQUESTED keeps the same stage; expanded scope needs CR and fresh approval.
Stop at FOUNDER_REVIEW; only Founder may approve completion and separately authorize the successor.
Future service/OpenAPI/MCP proposals remain gated, and idea intake cannot create automatic November scope.
