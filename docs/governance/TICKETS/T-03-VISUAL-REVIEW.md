# T-03 — Existing cartography evidence and human approval

Owner: Cartography. Review: Mobile PWA, independent QA and Founder.
Decision IDs: R-004, R-005, R-006, G-001; uncertainty R-007.
Charter: [PROJECT_CHARTER](../PROJECT_CHARTER.md).
User outcome: an approved lawful mobile map reference and honest navigation acceptance for later integration.

## Scope, inputs and paths

Review Stage 1/1B/1C harnesses and retained evidence. Recover existing raw exports/screenshots first.
Proposed owned paths: new docs/evidence/map-review/ and additive review report only, assigned after approval.
Read-only dependencies: tools/map-stage-1*, docs/design/MAP_STAGE_* and their historical receipts.
No SDK/style redesign, layer changes, fake 3D, diagnostics instrumentation, backend integration or Stage 2.
400 ms is a candidate duration, not a selected default.

Prerequisites: FA-07 provider/visual reference and screenshot rights, target languages/physical devices,
authorized browser/device capture and review budget. Figma is optional; no tool/plugin install.

## Acceptance and checks

- Report what actual artifacts exist versus proposed destinations; retain invalid/missing exports and their reasons.
- Lawful actual screenshots have visible attribution, matched configuration, source preset/language and device metadata.
- Distinguish source-language names from rendered labels; use only provider-supplied extrusions.
- Human review selects/reference-approves visuals/provider; MapTiler remains provisional until that record.
- Attribute conditional desktop GOOD feedback separately from strict timing measurements.
- Recover validity/sample/repeats/input-target metadata before claiming strict performance.
- Physical Android/iOS acceptance remains separate; emulation/desktop do not establish it.
- Preserve reduced motion and report accessibility gaps; do not infer GPU/FPS/present latency from event timing.

Test plan after approval: inspect lawful artifacts and measurement metadata; reuse valid existing cells.
Request only missing/invalid authorized capture cells, not automatic full-matrix reruns.
Evidence: actual screenshots/raw exports/configuration and human approval record at assigned locations.
Open questions: languages, device access, strict-performance scope, capture rights, visual reference/provider.
No Stage 2 permission is granted by acceptance of this review.

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
