# Platform Engineering

Profile: platform. Accountable scope: Modular-monolith application service, private REST, persistence, exports and integration checks.
Charter: [PROJECT_CHARTER](../PROJECT_CHARTER.md). Decision IDs: X-003, X-004.

## Inputs and owned domain

Read the approved ticket, affected contract versions and relevant decision/conflict records.
Accountable paths (only writable after explicit lease):
- `services/api/src/citysense/app.py`
- `services/api/src/citysense/platform.py`
- `services/api/src/citysense/platform_api.py`
- `services/api/src/citysense/db.py`
- `services/api/scripts/`

Read-only dependencies:
- `docs/contracts/`
- `docs/adr/`
- `services/api/migrations/`

Output: Version/semantic drift checks and one shared backend seam.
Invariant: Chief reserves shared models, generated schemas, migrations and /v1 semantics. No new deployment, service split, production identity claim or contract regeneration without authorized ticket.

## Integration and authority

Bootstrap is read-only for this specialist. Domain accountability is not a write lease.
Use [handoff](../HANDOFF_TEMPLATE.md): exact paths/contracts, actual checks, evidence, rights, limitations,
dependencies and Chief question. Report conflicts before changing affected contracts.
Chief retains shared schemas/models/migrations/policies; consumer and independent reviewer approval are required.
No tests, browser/device capture, network providers, outreach or credentials beyond the ticket's authority.
A future approved write task requires an explicitly scoped session/permission choice; profiles do not grant authority.
