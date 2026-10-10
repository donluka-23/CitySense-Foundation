# Opportunity Registry | narrow phase-2 spec

This earlier proposal remains a future boundary. Sprint 2 implements typed contracts and limited
tests only: see [Opportunity Registry design](OPPORTUNITY_REGISTRY_DESIGN.md). No supplier outreach,
operational availability, payment or booking API runs. Schema declarations do not prove confirmation.

Separate bounded context: create `provider`, `service_offer`, `verification_event`, `booking_request`, `booking_confirmation`, `attribution_event`.

## Minimum offline onboarding
Provider-provided coordinates (no Google ID required); phone/contact consent; service type/capacity/price/currency/duration/languages; weather suitability flags; cancellation policy; last verified timestamp; preferred manual confirmation method.

## Lifecycle
`discovered` → `claimed` → `verified` → `bookable_manual` → `suspended` (with reversible audit trail). Do not market `discovered` listings as verified or promise booking without a positive confirmation event.

## Safety and commercial neutrality
An organic suitability ranking never uses commissions, referral fees or hotel identity. Sponsored offers are separately marked. Store evidence for booking provenance and commission reconciliation; avoid assuming payment-split capability or supplier consent. No supplier onboarding is necessary to validate the environmental model.

## Initial success metric
Verified supply coverage in one micro-vertical, confirmation rate/latency and incremental confirmed bookings; report separately from human suitability accuracy.
