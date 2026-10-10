# ADR-0010: Prospective capture, local research audience and private Telegram adapter

Date: 2026-10-09. Status: implemented locally; independent review pending.

Sprint 2 had a receipt validator but no model runner. Its publication-only rights check also
prevented explicitly permitted local research from reading privately cached OSM evidence. An
external chat interface must retain that publication check, rather than inherit local access.

Decision: keep the modular monolith and frozen engine. A separate typed prospective manifest
contains candidate geometry, request inputs, evidence lineage and permission declarations, with
no outcome labels or CitySense results. A provider-neutral client runs a bounded frozen-context
tool loop; the optional OpenAI Responses client uses the existing HTTPX dependency. Receipts are
exclusive-created, flushed, hash-chained files. A separate later join validates them against the
labelled evaluation dataset; generation never accepts that dataset. Actual execution authenticity
still requires independent provider/account review, not merely hashes and declarations.

AccessContext gains a trusted, code-created `local_research` audience: research and cache
permissions are mandatory. The default `publication` audience still requires redistribution.
HTTP and Telegram cannot request or mint the local audience. This is a trust boundary for an
authorized local operator, not isolation from an administrator or arbitrary trusted Python code.
Search predicates and individual-record checks enforce the same audience policy.

Telegram uses the five existing authenticated REST operations, with a loopback-only operator
client, static private-user/place allowlists, bounded input/response sizes and explicit modes.
The maintained python-telegram-bot library supplies transport only. No additional scoring engine,
LLM intent parser, hosted webhook, account store, booking or payment path is introduced.

Alternatives: handing the labelled DatasetManifest to a runner would permit leakage; importing
raw arbitrary JSON tools would widen that risk. Direct Telegram database access would bypass the
operator API policy. Relaxing redistribution globally would expose private evidence. A separate
MCP service or agent framework adds infrastructure without solving these boundaries.

Consequences: real Telegram output remains blocked for the currently private OSM inventory.
Broad data feeds, route graphs, source revocation and distributed quotas remain future work.
Fixture capture is deterministic in response behavior but UUIDs/wall timestamps vary. Hash chains
detect ordinary mutation; they do not stop privileged replacement or attest provider execution.
Network phase timeouts bound blocking I/O; late model replies invalidate the entire prediction.
Independent information-budget, model-strength, missingness and tariff review precede empirical use.

Verification: negative manifest, chronology, provenance, label annotation, tool/token/cost/latency,
receipt-chain and later-universe tests; real PostGIS local/publication separation; Telegram auth,
mode, quota and transport tests. Original calculator, agent delegation and migration tests remain.
