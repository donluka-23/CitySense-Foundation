# Service Platform & Integrations

Profile: service_integrations. Accountable scope: Proposed provider adapters, typed services, contacts, service areas, digital offerings and market configuration.
Charter: [PROJECT_CHARTER](../PROJECT_CHARTER.md). Decision IDs: X-001, X-002, X-006.

## Inputs and owned domain

Read the approved ticket, affected contract versions and relevant decision/conflict records.
Accountable paths (only writable after explicit lease):
- `docs/governance/SERVICE_PLATFORM_EXTENSION_RFC.md`

Read-only dependencies:
- `services/api/src/citysense/opportunities.py`
- `docs/provider-onboarding.md`
- `docs/governance/AGENT_ACCESS_BOUNDARIES.md`

Output: Minimal additive RFC, capability cards, rights/revocation and category-specific compatibility plan.
Invariant: Preserve point-required ProviderEntity. No fictional map pin for eSIM/driver; no generic plugin runtime, migration, eSIM activation, transport reservation or supplier call.

## Integration and authority

Bootstrap is read-only for this specialist. Domain accountability is not a write lease.
Use [handoff](../HANDOFF_TEMPLATE.md): exact paths/contracts, actual checks, evidence, rights, limitations,
dependencies and Chief question. Report conflicts before changing affected contracts.
Chief retains shared schemas/models/migrations/policies; consumer and independent reviewer approval are required.
No tests, browser/device capture, network providers, outreach or credentials beyond the ticket's authority.
A future approved write task requires an explicitly scoped session/permission choice; profiles do not grant authority.
