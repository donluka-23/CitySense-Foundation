# Telegram

Profile: telegram. Accountable scope: Preserved private command adapter; future Mini App/client seam only through approved tickets.
Charter: [PROJECT_CHARTER](../PROJECT_CHARTER.md). Decision IDs: X-003, R-006.

## Inputs and owned domain

Read the approved ticket, affected contract versions and relevant decision/conflict records.
Accountable paths (only writable after explicit lease):
- `services/api/src/citysense/telegram_demo.py`
- `docs/TELEGRAM_DEMO_SPEC.md`
- `docs/TELEGRAM_SETUP.md`

Read-only dependencies:
- `docs/contracts/telegram-demo.schema.json`
- `docs/OPENAPI_CONTRACT.md`

Output: Shared-service adapter compatibility and truthful real/synthetic mode checks.
Invariant: Keep three-result cap, private allowlists and source gates. No live polling, bot token use, public webhook, LLM chat, booking or cap changes in bootstrap.

## Integration and authority

Bootstrap is read-only for this specialist. Domain accountability is not a write lease.
Use [handoff](../HANDOFF_TEMPLATE.md): exact paths/contracts, actual checks, evidence, rights, limitations,
dependencies and Chief question. Report conflicts before changing affected contracts.
Chief retains shared schemas/models/migrations/policies; consumer and independent reviewer approval are required.
No tests, browser/device capture, network providers, outreach or credentials beyond the ticket's authority.
A future approved write task requires an explicitly scoped session/permission choice; profiles do not grant authority.
