# Data governance and licensing — reviewed 2026-10-09

This is a source-grounded engineering assessment, not legal certification. Access, data
licensing, storage, publication and downstream commercial use are separate decisions. A
dated terms URL in SourceMetadata records a review declaration, not a signed contract.
Uncleared sources stay disabled. No services were purchased and no participant data collected.

Sprint 3's dated [real-world coverage ledger](REAL_WORLD_DATA_COVERAGE.md) extends this assessment
with five private OSM skeleton geometries. Research/cache audience is trusted local code only;
HTTP, Telegram and model transfer still require separate publication permissions. Raw inventory
and full decisions stay in ignored private artifacts. No environmental/routing/availability feed
or partner account was enabled. Geometry acquisition is not site verification or scientific validation.

## Provider assessment

| Source / use | Access, research/commercial and publication | Cost/quota | Resolution/time and gaps | Sprint 2 disposition |
|---|---|---|---|---|
| Open-Meteo weather | Data CC BY 4.0 with attribution/modification notice; free hosted access restricted to eligible noncommercial uses; undisclosed commercial-entity research is not automatically eligible | Free: 600/min, 5,000/hour, under 10,000/day; subscription for commercial API | Regional/model-dependent grid, hourly output; coast/grid representativeness unknown, no street shade/noise | Native hourly parser tested on invented fixtures; live disabled |
| Open-Meteo AQ/UV | Review Open-Meteo and underlying CAMS attribution; API access rules separate from data license | Same plan review; no paid account | CAMS Europe ~11 km hourly; global ~45 km/3-hourly underlying forecast; Batumi selected domain must be verified; no curbside pollutant sensor claim | Assessed only, no AQ/UV ingestion |
| OSM roads, paths, parks, buildings | ODbL attribution and derivative database/share-alike obligations; data permits research/commercial use subject to conditions | Data free; public API services have separate policy, no SLA | Community geometry with unknown local positional/completeness accuracy; database timestamp is not visit/verification time; edits irregular | One small aggregate park-way query archived; API publication withheld pending derivative policy |
| Overture places/buildings/transport | Theme/source-specific licenses; places include CDLA Permissive 2.0, Apache/NOTICE and CC0 contributions; buildings/transport ODbL | Public release downloads; client query, storage/egress costs depend on execution environment; no hosted lookup quota assumed | Versioned monthly releases, source-derived point/geometry, confidence is not local verification; Georgia completeness untested | No live download; pin release/schema and source notices before adapter |
| Mapbox routing/geocoding | Commercial service contract/token; no assumption of raw result redistribution. Temporary geocodes cannot be cached; permanent storage requires eligible account/contract | Directions published free first 100,000 monthly requests, then first paid tier $2/1,000; default max 300/min; other APIs priced separately | Route geometry/time estimates, map-dependent freshness; no guarantee of shade, step-free access or live business availability | No credentials/purchase; disabled, product-specific archival review required |
| Georgian NSDI/NAPR resources | Geoportal viewing/search free; downloads/use governed by each resource metadata/access agreement, not blanket open licensing | Resource-specific restrictions/fees possible; no verified API quota | Authoritative source/CRS/resolution/update vary per dataset; catalogue presence does not prove Batumi suitability | Disabled until dataset, CRS, access agreement, attribution and privacy scope reviewed |

Primary references, checked on 2026-10-09:

- [Open-Meteo terms](https://open-meteo.com/en/terms), [forecast docs](https://open-meteo.com/en/docs),
  [plans](https://open-meteo.com/en/pricing), [AQ docs](https://open-meteo.com/en/docs/air-quality-api).
  Plans describe monthly call budgets (Standard 1M, Professional 5M, Enterprise 50M+); monetary
  subscription rates were not exposed in the retrieved text and are not invented here.
- [OSM copyright](https://www.openstreetmap.org/copyright), [main API policy](https://operations.osmfoundation.org/policies/api/),
  [Overpass operator policy](https://dev.overpass-api.de/overpass-doc/en/preface/commons.html),
  [native query language](https://wiki.openstreetmap.org/wiki/Overpass_API/Overpass_QL).
  Public Overpass is suitable for this manual bounded demonstration, not a commercial application
  backend. Its guidance of roughly 10,000 requests/1 GB daily is not a purchased quota or SLA.
- [Overture attribution](https://docs.overturemaps.org/attribution/) and
  [places/release/quality guide](https://docs.overturemaps.org/guides/places/).
  Retain source and release-specific notices; do not apply a single license to the whole platform.
- [Mapbox product terms](https://www.mapbox.com/legal/product-terms), [storage rules](https://docs.mapbox.com/api/search/geocoding/),
  [Directions limits](https://docs.mapbox.com/api/navigation/directions/), [pricing](https://www.mapbox.com/pricing).
  Pricing is an observation of the public page, not a contracted CitySense price.
- [Georgia National Geoportal](https://nsdi.gov.ge/en), [resource-specific use terms](https://nsdi.gov.ge/en/terms-of-use).

## Implemented ingestion and exact real-data scope

`native_sources.py` maps aggregate-only Overpass JSON to a derived `park_way_count` observation,
with query/bounds/raw hashes, provider database timestamp and locally stamped retrieval. The
query returns only count metadata: no contributor identities, contact tags or participant data.
The selected ~0.02° × 0.02° Batumi window is a sampling area, not a park geometry or weather zone.
Counts may include multiple ways per park or omit unmapped parks. No fraction transformation,
greenery coverage or recommendation evidence is inferred from it.

The one live retrieval yielded 10 ways. Raw SHA256:
`057c1cfa6e6f0587e27ef79f4aeb26bb500fea2effe45dd1b03f02667e39712f`.
Private capture lives in `artifacts/sprint2/live-osm/`; its attribution is © OpenStreetMap
contributors, ODbL 1.0. Cache/research access is recorded for this bounded use; external
redistribution remains false until the derivative database/publication plan is reviewed.
No production feed, human validation or commercial clearance follows from this demonstration.

Open-Meteo parsing converts Fahrenheit to Celsius and km/h to m/s, validates finite WGS84
coordinates, UTC offsets, hourly ordering/units/array lengths and preserves nulls. Ordinary
forecast responses lack authenticated issuance/run metadata; candidates explicitly have null
issuance and `historical_replay_eligible=false`. Neither retrieval time nor `generationtime_ms`
is fabricated as issuance. A reviewed run-aware source must supply this before numeric forecast
evidence can enter the existing immutable replay model. Grid resolution stays null when unconfirmed.

Native retrieval uses fixed HTTPS endpoints, disabled redirects, 20-second request timeouts,
two attempts, 256 KiB decompressed body limit and bounded retry delay. 429/5xx/transport failures
never substitute fabricated or stale values. Unit tests use MockTransport; no network polling
or startup tasks are enabled. Unknown source rights reject live calls and raw storage.

## Required source ledger and release controls

Before enabling any regular source, record owner, dataset/release, version/hash, terms/access-plan
snapshot, territory, variables/units, raw retention, research/commercial/cache/publication permissions,
attribution/NOTICE, derivative obligations, costs/quotas, issue/valid/retrieval semantics, resolution,
coverage and reviewer/date/expiry. A boolean is a runtime gate, not the complete legal ledger.

Keep restricted raw archives out of Git and public APIs. Source revocation cannot be solved by
immutable storage alone: before real participants or revocable provider feeds, design restricted
retention, access revocation and lawful deletion/withdrawal independently of research audit trails.
Do not put participant records into these append-only evidence tables. No account/consent workflow
is implemented. Independent data steward/privacy review remains a release and field-collection gate.
