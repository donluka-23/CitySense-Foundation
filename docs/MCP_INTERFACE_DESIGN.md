# MCP interface design — no production server

The executable interface is REST/OpenAPI. `agent_tools.py` is an in-process validation/delegation
prototype. [Tool catalog](contracts/mcp-tools-design.json) exports five input schemas and explicit
read-only, non-destructive, idempotent, closed-world annotations. It is not an MCP endpoint,
transport implementation or interoperable hosted service.

| Tool | Shared service method | Status |
|---|---|---|
| `search_places` | `IntelligenceService.search_places` | Prototype delegates; REST operational locally |
| `get_place_details` | `get_place_details` | Same |
| `get_city_state` | `get_city_state` | Same |
| `evaluate_suitability` | `evaluate_suitability` | Same deterministic engine |
| `compare_places` | `compare_places` | Exact two-candidate validation, same engine |
| `discover_local_services` | Future `OpportunityReader` | Contract only; no tool registered |
| `get_service_availability` | Future `OpportunityReader` | Contract only; no tool registered |
| `request_booking` | Future action service | Explicitly unavailable; unknown-tool error |

Prototype calls take `{city_id, query}` except details `{city_id, place_id, decision_at}` and
return structured JSON identical to the corresponding service result. No natural-language
orchestration or scoring logic appears in the adapter. Transport implementation must translate
PermissionError, missing data and schema errors into safe protocol errors without disclosing
raw payloads. Test coverage verifies delegation parity and shared city/rights policy.

## Future transport requirements

Pin/review a negotiated MCP protocol version when actually implementing a server. The current
[official specification](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2026-07-28/basic/index.mdx)
is a design reference, not an implemented compatibility claim. Follow transport authorization,
token audience/resource binding, session/origin protections, TLS and gateway limits. Do not trust
client-provided tenant/purpose/scope metadata; derive AccessContext from verified credentials.
Do not proxy arbitrary URLs or give database/raw SQL tools to agents.

Annotations are behavioral hints, not an authorization boundary, as discussed by the
[MCP project](https://blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations/).
Source labels, descriptions and future supplier text are untrusted data, never tool instructions.
Future resource retrieval needs the same rights and city checks as tool calls. Return bounded
structured objects and provenance; cap response size and total session usage at the gateway.

Booking must be a separate scoped action with user confirmation, operational provider mechanism,
idempotency key, auditable attribution, cancellation/expiry semantics and privacy review. A model
choice or a `bookable` declaration cannot authorize a transaction. No such workflow is enabled.
