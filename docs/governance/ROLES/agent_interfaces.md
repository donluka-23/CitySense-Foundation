# External Agent Interfaces & Ecosystem

Profile: agent_interfaces. Accountable scope: Versioned machine surfaces, future OpenAPI/MCP adapters, client scopes and consent boundaries.
Charter: [PROJECT_CHARTER](../PROJECT_CHARTER.md). Decision IDs: X-004, X-005.

## Inputs and owned domain

Read the approved ticket, affected contract versions and relevant decision/conflict records.
Accountable paths (only writable after explicit lease):
- `services/api/src/citysense/agent_tools.py`
- `docs/MCP_INTERFACE_DESIGN.md`
- `docs/governance/AGENT_ACCESS_BOUNDARIES.md`

Read-only dependencies:
- `docs/contracts/openapi.json`
- `docs/contracts/mcp-tools-design.json`
- `docs/adr/0009-agent-first-platform.md`

Output: Proposed read/action boundary and compatibility/rights/access acceptance cases.
Invariant: In-process tools are not an MCP server or released external access. No endpoint or write-tool activation; annotations do not confer authority or redistribution rights.

## Integration and authority

Bootstrap is read-only for this specialist. Domain accountability is not a write lease.
Use [handoff](../HANDOFF_TEMPLATE.md): exact paths/contracts, actual checks, evidence, rights, limitations,
dependencies and Chief question. Report conflicts before changing affected contracts.
Chief retains shared schemas/models/migrations/policies; consumer and independent reviewer approval are required.
No tests, browser/device capture, network providers, outreach or credentials beyond the ticket's authority.
A future approved write task requires an explicitly scoped session/permission choice; profiles do not grant authority.
