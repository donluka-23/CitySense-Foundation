# RFC: additive service platform extension

Status: PROPOSED / UNIMPLEMENTED. Strategic direction X-001–007 is approved;
X-008–010, exact schemas/storage/endpoints and rollout remain proposed.
Owner: Service Platform & Integrations; Chief reserves shared interfaces.
No migration, contract export or runtime change is part of bootstrap.

## Existing foundation and minimum gap

opportunities.py provides Offer, point-required ProviderEntity, BookingAttribution and OpportunityReader declarations.
Offer validates price/currency pairing and confirmed-availability timestamps/method. None is an operational registry.
ProviderEntity requires place_id, city_id and Point Geometry; no digital/service-area representation.
Evidence is numeric and frozen; it cannot honestly encode all contacts or textual action/availability assertions.
Five private REST reads and in-process tools reuse IntelligenceService. No availability/action/MCP transport exists.

Preserve these contracts, /v1 behavior, generated exports, numeric Evidence, snapshots and migrations.
Propose new versioned contracts plus an explicit fixed-place compatibility mapper.
Do not weaken required point fields or create fictional places; no separate tables are presumed necessary.

## Proposed contracts

| Contract | Responsibility |
|---|---|
| Provider | Stable identity, aliases, authority/verification evidence, approved markets and connector lifecycle; no mandatory point. Identity is not licensing/insurance/capacity proof. |
| ServiceOffering | Stable/versioned provider-linked typed offering; capability, tagged location, price/availability/contact/action and evidence references. |
| Capability | Versioned supported category attributes/actions; declaration distinct from deployed authorized implementation. |
| PriceQuote | Decimal amount/currency, taxes/fees/terms, quantity/duration, authoritative check/expiry, quote ID/version; no inferred FX. |
| AvailabilityAssertion | Offering/slot/quantity scope, status, source/authority/method, check/retrieval/validity/expiry, evidence/revision. Availability is not a hold. |
| ContactChannel | Validated kind/destination, owner, verification date/method, public/permissioned classification, purpose/rights and expiry/revocation. |
| ActionPolicy | Permitted client/principal/actions, authority, consent/confirmation, terms/version/expiry and legal/rights prerequisites; unsupported writes by default. |
| EvidenceRecord | Typed nonnumeric assertion with subject/property/value, source/version/method, observed/issued/retrieved/valid times, rights and uncertainty; references numeric Evidence without changing it. |
| MarketConfig | Market/city/timezone, allowed locale/currency, coverage, taxonomy and rights policy; Batumi-only activation initially. |
| ConnectorCapabilityCard | Provider/market/category, supported location/actions, authorization/rights owner, freshness, SLA or unknown, clients, test and revocation state. |

Location variants: fixed-place with reviewed place/entrance geometry; service-area/on-demand with coverage
and optional explicitly named meeting/dispatch points; remote/digital with eligible markets and no invented pin;
contact/information with optional spatial relevance and explicit read/redirect status.
Validate category-specific attributes instead of a universal nullable-column model.

## Proposed seams and honest states

Read: governed discovery → offering detail → eligibility/availability with provenance.
Action: quote/request → authorized provider status/callback → cancellation/fulfillment.
No exact callable endpoints or tool names are adopted here; see INTERFACE_REGISTRY proposed entries.
Maintain VERIFIED_CONTACT, INFORMATION_ONLY, REDIRECT_TO_PROVIDER, REQUESTED, PENDING_PARTNER,
CONFIRMED, DECLINED, EXPIRED, CANCELLED and COMPLETED; refunds only under separately approved topology.
No request or click is confirmation, activation, payment or fulfillment.

Writes need scoped idempotency keys/payload hashes and retry/conflict/expiry rules.
Holds, concurrency, double-book prevention, out-of-order events and terminal transitions require review.
Callbacks require configured provider authority, signature/equivalent verification, timestamp/nonce/replay
prevention, event/version identity, persistent deduplication and controlled transitions; no user-supplied callback URL.
Booking confirmation, payment and service completion are separate authoritative outcomes.

## Rights, access and sequencing

[Agent boundaries](AGENT_ACCESS_BOUNDARIES.md) apply equally to PWA/Telegram/partner clients.
Provider publication, commercial use, redistribution, archival and revocation rights are distinct.
Do not put revocable private contacts/participant data into append-only research tables by default.
Partner licenses/insurance/terms require actual evidence; verified contact alone proves none of them.

November core remains tourist selection. Verified contacts or one manually confirmed action are optional
only after separate permissions/tickets. Drivers/transfers, eSIM/SIM activation, payments, external writes
and multi-city rollout remain deferred. Restaurant experiment remains proposed.
Proposed connector lifecycle: DISCOVERED → CONTACTED → APPROVED → TESTING → ACTIVE → SUSPENDED/REVOKED.

## Acceptance before any future implementation

Founder approves scope/compatibility (CF-04/FA-09); consumer review names schema/version and storage strategy.
Check old provider exports/replay unchanged; exercise fixed-place compatibility plus service-area/digital no-pin cases.
Test stale/unknown/unauthoritative price and availability; denial/revocation/invalid contacts; timezone/currency rules.
Prove one authorized offering across PWA and a read-only machine-client contract test before broad abstractions.
Provider sandbox and negative lifecycle/idempotency/access tests precede actions.
No tests are executed and no supplier is committed by this RFC.
