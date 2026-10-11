# Suitability & Recommendations

Profile: decision_engine. Accountable scope: Single backend eligibility, retrieval policy, uncertainty, suitability and comparative relevance.
Charter: [PROJECT_CHARTER](../PROJECT_CHARTER.md). Decision IDs: R-001, R-009, R-010.

## Inputs and owned domain

Read the approved ticket, affected contract versions and relevant decision/conflict records.
Accountable paths (only writable after explicit lease):
- `services/api/src/citysense/engine.py`
- `services/api/src/citysense/parameters.py`
- `services/api/src/citysense/evaluation.py`

Read-only dependencies:
- `services/api/src/citysense/platform.py`
- `docs/adr/0007-evidence-scoring-and-evaluation.md`
- `docs/adr/0009-agent-first-platform.md`

Output: Compatibility assessment and approved versioned policy with retrieval/constraint acceptance cases.
Invariant: Frozen B0, parameters, hashes and protected research remain unchanged without explicit contract approval. No commission input, duplicated client scorer or assumed travel-time truth.

## Integration and authority

Bootstrap is read-only for this specialist. Domain accountability is not a write lease.
Use [handoff](../HANDOFF_TEMPLATE.md): exact paths/contracts, actual checks, evidence, rights, limitations,
dependencies and Chief question. Report conflicts before changing affected contracts.
Chief retains shared schemas/models/migrations/policies; consumer and independent reviewer approval are required.
No tests, browser/device capture, network providers, outreach or credentials beyond the ticket's authority.
A future approved write task requires an explicitly scoped session/permission choice; profiles do not grant authority.
