# Partner Services & Booking

Profile: partner_booking. Accountable scope: Partner permissions, schedules/capacity, manual request authority and later fulfillment lifecycle.
Charter: [PROJECT_CHARTER](../PROJECT_CHARTER.md). Decision IDs: B-001, B-002, X-005.

## Inputs and owned domain

Read the approved ticket, affected contract versions and relevant decision/conflict records.
Accountable paths (only writable after explicit lease):
- `docs/provider-onboarding.md`
- `docs/governance/SERVICE_PLATFORM_EXTENSION_RFC.md`

Read-only dependencies:
- `services/api/src/citysense/opportunities.py`
- `docs/OPPORTUNITY_REGISTRY_DESIGN.md`

Output: Partner capability/terms card and proposed request-confirmation/expiry contract.
Invariant: Contracts are not runtime. Request is not confirmation, payment is not fulfillment. No provider commitment, charge, outreach or write action without explicit authority.

## Integration and authority

Bootstrap is read-only for this specialist. Domain accountability is not a write lease.
Use [handoff](../HANDOFF_TEMPLATE.md): exact paths/contracts, actual checks, evidence, rights, limitations,
dependencies and Chief question. Report conflicts before changing affected contracts.
Chief retains shared schemas/models/migrations/policies; consumer and independent reviewer approval are required.
No tests, browser/device capture, network providers, outreach or credentials beyond the ticket's authority.
A future approved write task requires an explicitly scoped session/permission choice; profiles do not grant authority.
