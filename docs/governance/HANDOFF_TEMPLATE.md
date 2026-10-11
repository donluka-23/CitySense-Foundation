# Scoped ticket and handoff

Copy only the relevant sections into a short ticket. Planning does not authorize execution.

## Ticket contract

- ticket_id / owner / independent reviewers:
- founder_decision_ids and dated approval reference:
- user_outcome:
- scope and explicit exclusions:
- owned_paths / base revision / lease expiry:
- read_only_dependencies:
- inputs/contracts (producer, consumer, version, schema owner):
- prerequisites / blocked_by:
- forbidden_changes (protected code, contracts, ADRs, data and credentials):
- tests (commands, environment, positive and negative behavior):
- screenshots/evidence (actual artifact destinations, rights and validity metadata):
- acceptance criteria / human gate:
- rollback (exact owned changes; preserve user work):
- delivery_state:
- open_questions:

## Worker handoff

- Ticket / decision IDs / owner / base:
- Changed files (or READ_ONLY):
- Contracts consumed/produced and compatibility:
- What actually runs; what is only proposed:
- Checks actually run (command, time, environment, exit/result):
- Checks not run and reason:
- Screenshot/evidence paths; invalid/missing evidence:
- Sources, rights, provenance, freshness, synthetic/real caveats:
- Risks/blockers:
- Upstream/downstream impact:
- Rollback:
- Requested Chief decision:

## Chief integration record

Lease checked; diff reviewed; interface consumers reviewed; protected evidence preserved;
independent QA result; unresolved approvals; founder acceptance reference; current board/status update.

## Delivery stage and Founder packet — mandatory overlay

- stage_id / lifecycle / authorization_state:
- approved artifact version or commit / exact bounded scope / FOUNDER_APPROVALS entry:
- task lifecycle (separate from stage) / one-writer lease / current base:
- UX checkpoint and journey segments covered / predecessor approval / Stage 1B closure or explicit waiver:
- goal and measurable user value / original approved scope:
- completed and uncompleted work / before-after / deviations:
- actual working demo URL and reproducible command (or N/A with reason):
- dated actual desktop/mobile screenshot or video paths, viewport/config/device and provenance/rights:
- tests/failures / security-accessibility-performance knowns and unknowns:
- independent QA identity / reviewed artifact version / actual result before Founder review:
- risks / dependencies / next-stage proposal / specific Founder decision:
- missing evidence and approval state / next permitted action:

All UI/UX checkpoints require actual screenshots or interactive evidence and explicit Founder visual approval.
A prototype is not runtime/device acceptance. Descriptive claims are not visual evidence.
Approval complete and next-stage execution are distinct decisions. No successor is auto-dispatched.
