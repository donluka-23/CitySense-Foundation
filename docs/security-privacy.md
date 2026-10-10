# Security, privacy, reliability | threat model v0.1

Sprint 2 private controls, future external identity/quotas and current release gates are in
[platform architecture](AGENT_PLATFORM_ARCHITECTURE.md), [data governance](DATA_GOVERNANCE_AND_LICENSING.md)
and [risk register](KNOWN_RISKS.md). New city APIs require an operator key even in development;
legacy local calculator/replay semantics remain. No participant collection or external release is enabled.

## Data minimization
Default to no account, no exact personal location retention, no microphone/camera, no inferred mental health or stress diagnoses. For field-study opt-in, pseudonymize, set short retention and explicit withdrawal channel. Avoid precise device tracking. City context can be public; user-specific mobility needs remain private.

## Boundaries
- API: validate payload size, enums, numeric limits, coordinate ranges, rate limit, CORS allowlist and auth before public deployment.
- Providers: secrets server side, timeouts, retries with jitter, circuit breakers, quotas and key rotation. Prevent SSRF by allowlisted provider hosts.
- LLM: prompt-injection exposure from provider descriptions; structured JSON output validation, source-bound explanations, explicit uncertainty; never execute generated tools without policy validation.
- Supplier registry: verified vs claimed status, ownership verification, identity/permission boundaries, anti-spam and fraud reporting; no automatic payouts in v0.
- Logs: omit precise user location and prompts by default; sampled traces with redaction; no unconsented raw personal data export.
- Dependency chain: version lock, SBOM, Dependabot, CI SAST/dependency scan and release signatures planned as production gates.

## Risk register
| Risk | Severity | Mitigation | Exit evidence |
|---|---|---|---|
| False microclimate precision | High | quality labels and abstention | domain review, tests |
| Unsafe mobility/heat guidance | High | informational disclaimer, no health decisions | documented test scenarios |
| Data license infringement | High | rights matrix before commercial launch | legal review |
| Location/person reidentification | High | retention minimization; group data | privacy review |
| Low accuracy / evaluation leakage | High | blinded holdout, preregistered evaluation | experiment audit |
| Supplier booking mismatch | Medium | manual acceptance only | transaction-state tests |

No SOC2/ISO27001 certification is claimed. Use those standards as maturity references, not as badges.

## Sprint 1 controls and limits

Implemented: strict contracts, candidate/field bounds, finite values, 256 KiB streamed
body limit, per-process direct-peer rate limits, optional development keys and mandatory
generated production keys. Keys use constant-time comparison. Errors omit submitted values
and database details. No cross-origin CORS access is enabled. Logs use route templates,
status and duration; no IPs, profiles, bodies or snapshot IDs. OpenTelemetry API spans and
bounded counters/latency buckets are stubs without collectors/exporters. The documented
Uvicorn command binds loopback and disables access logs and forwarded-header trust.

The HTTP gateway requires operator HTTPS host allowlists, disables redirects and bounds
timeouts, attempts, bytes, cache size and circuit recovery. Validation failures are not
retried. Caching requires explicit rights and never falls back to stale data. Live rights
claims require dated terms review; software cannot certify legal permission. No live source,
participant collection or LLM is enabled. CI audits every locked runtime/development dependency
and runs Bandit. Exact findings and fixes appear in the Sprint 1 report.

Before public exposure: explicitly configure production mode, TLS, ingress deadlines,
trusted proxy/shared quotas, least-privilege database roles, backup recovery, egress DNS/IP
controls and security review. Keys provide no per-user authorization. Limits/caches are
per process. Triggers do not restrain database superusers. Consent, retention and withdrawal
workflows need a separately approved design before real participant storage.
Follow [KNOWN_RISKS.md](KNOWN_RISKS.md); no certification or production safety is claimed.
