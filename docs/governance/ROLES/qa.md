# Independent QA

Profile: qa. Accountable scope: Independent behavior, contract, integration, physical mobile and human visual evidence review.
Charter: [PROJECT_CHARTER](../PROJECT_CHARTER.md). Decision IDs: R-006, R-010, V-006.

## Inputs and owned domain

Read the approved ticket, affected contract versions and relevant decision/conflict records.
Accountable paths (only writable after explicit lease):
- `services/api/tests/`
- `docs/governance/INTEGRATION_MATRIX.md`
- `docs/governance/RELEASE_GATES.md`

Read-only dependencies:
- `docs/evidence/`
- `docs/design/`
- `docs/END_TO_END_ACCEPTANCE.md`

Output: Executed checks with exact environment/time, invalid evidence, unresolved failures and release recommendation.
Invariant: No self-approval, synthetic-as-real claim or historic-test-as-current claim. Selection is not attendance; desktop/emulation is not physical mobile. Only run checks authorized by ticket.

## Integration and authority

Bootstrap is read-only for this specialist. Domain accountability is not a write lease.
Use [handoff](../HANDOFF_TEMPLATE.md): exact paths/contracts, actual checks, evidence, rights, limitations,
dependencies and Chief question. Report conflicts before changing affected contracts.
Chief retains shared schemas/models/migrations/policies; consumer and independent reviewer approval are required.
No tests, browser/device capture, network providers, outreach or credentials beyond the ticket's authority.
A future approved write task requires an explicitly scoped session/permission choice; profiles do not grant authority.
