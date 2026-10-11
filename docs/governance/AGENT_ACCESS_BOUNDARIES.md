# Proposed external agent access boundaries

Status: PROPOSED / UNRELEASED. Owner: Agent Interfaces; Security independently reviews.
X-004–007 approves strategic constraints; specific identity/scope/endpoints/MCP design remains gated.

## Current executable access

Private operator REST requires configured X-API-Key for the five city reads, even in development.
Legacy /v1/evaluate has environment-dependent auth; do not expose it as a public gateway.
AccessContext uses one local-operator and city.read/suitability.read, not a tenant/account service.
agent_tools.py validates/delegates in-process; tool annotations/catalog are not an MCP transport.
Current peer/per-process rates/body bounds and redacted logs do not establish distributed quotas or consent.
No public API, partner action, external agent write or provider transport is authorized.

## Proposed trust seams

| Principal/surface | Proposed permissions | Required evidence |
|---|---|---|
| Tourist/session PWA or Telegram | Approved bounded discovery/selection with minimum identity/location | Source/publication rights, session privacy, no operator key in browser |
| Partner/operator | Only owned verified inventory and separately permitted status actions | Verified authority, resource/tenant checks, terms and auditable confirmation |
| Integrator/external agent | Versioned authorized reads; actions separately consent-gated | Revocable scoped identity, market/dataset/resource rights, quotas/audit |
| Internal research | Trusted code-only special purpose | No HTTP/Telegram/MCP self-assertion of local_research |

Identity/scope checks must also enforce city, tenant, offering, dataset, purpose and downstream rights.
Commercial source permission and redistribution permission are distinct.
Untrusted clients cannot mint internal research purpose, select arbitrary callback endpoints or bypass rights.
Unknown/unsupported capability output remains explicit.

## Reads versus actions

OpenAPI is primary versioned contract; optional MCP maps the same governed service, with no second scorer.
Exact routes/tool names and schemas require separate review. Document errors, pagination/coverage semantics,
timezone/locale/currency, field provenance/freshness, quotas and compatibility.
Read-only annotations do not convey permissions.

Quotes, requests, confirmation, cancellation, purchase, activation and personal-data disclosure are distinct actions.
End-user confirmation must bind principal, offering/version, terms/quote, recipients, action and expiry where relevant.
Natural-language interest is not consent. Provider/operator confirmation is authoritative.
Require scoped idempotency/payload conflicts, audited consent, authenticated callbacks and replay/dedupe controls.
Payment receipt is not booking confirmation or service fulfillment.

## External-release prerequisites

TLS/revocable credentials, trusted proxy policy, tenant/resource isolation, multi-worker quotas, least-privilege DB,
controlled provider egress, safe contact URLs/rendering, injection boundaries and minimal-data audits.
Provider/tool descriptions are untrusted content; a model cannot override policy.
Define retention, deletion/withdrawal, archival/revocation and incident/credential-revocation workflow.
Run allowed/denied/stale/replayed/cross-tenant/cross-city/rights-revoked contract and security cases;
confirm unchanged internal replay/export behavior and no confidential logging.

Bootstrap provides no external endpoint, credentials, MCP server, write tool or consent ledger.
External reads need independent release approval; writes/eSIM/transport/payments/new cities are deferred.
