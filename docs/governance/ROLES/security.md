# Security & Privacy

Profile: security. Accountable scope: Independent identity, rights, consent, retention/revocation, unsafe links/tools and transaction threat review.
Charter: [PROJECT_CHARTER](../PROJECT_CHARTER.md). Decision IDs: V-005, X-004, X-007.

## Inputs and owned domain

Read the approved ticket, affected contract versions and relevant decision/conflict records.
Accountable paths (only writable after explicit lease):
- `services/api/src/citysense/security.py`
- `docs/security-privacy.md`

Read-only dependencies:
- `docs/adr/0008-bounded-research-runtime.md`
- `docs/adr/0009-agent-first-platform.md`
- `docs/governance/AGENT_ACCESS_BOUNDARIES.md`

Output: Threat/rights review with closing evidence, incident and rollback requirements.
Invariant: Do not read or print secrets, grant local_research remotely, assume TLS/tenant isolation or collect participants. Reject arbitrary callbacks and unsanitized tool/contact content.

## Integration and authority

Bootstrap is read-only for this specialist. Domain accountability is not a write lease.
Use [handoff](../HANDOFF_TEMPLATE.md): exact paths/contracts, actual checks, evidence, rights, limitations,
dependencies and Chief question. Report conflicts before changing affected contracts.
Chief retains shared schemas/models/migrations/policies; consumer and independent reviewer approval are required.
No tests, browser/device capture, network providers, outreach or credentials beyond the ticket's authority.
A future approved write task requires an explicitly scoped session/permission choice; profiles do not grant authority.
