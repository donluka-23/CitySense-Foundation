# Opportunity Registry — future integration boundary

`opportunities.py` and [provider schema](contracts/provider-entity.schema.json) define contracts
only. There is no supplier onboarding, discovery feed, availability endpoint, booking, payment
or dashboard. The registry is independent of environmental suitability and research labels.

ProviderEntity has stable internal provider/place/city IDs, display name, provenance-bearing
WGS84 point geometry, optional external aliases, SourceMetadata, publication permission,
verification evidence, lifecycle and bounded offers. An entity does not require a Google ID.
An Offer supplies category/title, optional paired nonnegative price and ISO-style currency,
optional duration, availability state, check/expiry times and confirmation method. Unknown
prices, duration or availability remain null/unknown, never fabricated.

| Lifecycle | Required evidence | Claims permitted |
|---|---|---|
| Discovered | Source and geometry | Candidate entity; not independently verified |
| Verified | Non-none verification method and last verification time | Identity review declaration; currency must still be checked |
| Bookable | Verified plus named confirmation adapter and offers | Structural readiness declaration only; runtime adapter acceptance required |

`confirmed_available` additionally requires operational confirmation method and an expiring
dated check. Runtime consumers must expire checks relative to query time, verify adapter is
deployed/authorized, apply source rights and verify price/terms before describing anything as
currently bookable. A schema cannot prove a named adapter exists. Sprint 2 has none; no entity
is operationally bookable. Tests reject missing verification, confirmation, price currency and
exceeded publication rights.

OpportunityReader declares future discovery/availability interfaces. BookingAttribution binds
request, tenant, agent application, provider/offer and organic assessment hash; it has no
personal booking data. Any future action requires separately reviewed consent, transaction,
cancellation, identity, publication and audit procedures.

Provider-reported facts, identity verification and environmental evidence must stay separate.
Commission/affiliate rates are deliberately absent from the engine and registry scoring path.
Future sponsored distribution must be explicitly labeled and must not alter organic scores.
Service information freshness, withdrawals and supplier publication revocation need a separate
retention/revocation design; append-only research evidence is not permission to publish forever.

## Potential future Meni.ge integration — assessed 2026-10-09

[Meni.ge's public site](https://meni.ge/) advertises restaurant/POS, reservations and waitlist
features and an AI-agent guest API. These are vendor descriptions, not tested integration facts.
Meni.ge is a potential future restaurant-systems source, not an approved partner. CitySense has
no Meni credential, account, contractual permission or verified waitlist/availability endpoint;
no partner endpoint or transaction was called. Any future adapter would need provider/entity
mapping, dated operational confirmation, purpose/publication/retention review and scoped identity.
Hotel distribution and queue/availability remain separate from organic environmental scoring.
Commission or attribution must not change ranking. No booking/payment workflow is implemented.
