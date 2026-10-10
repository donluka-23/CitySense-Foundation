# Map data rights and costs — Stage 1

Reviewed **2026-10-10, Asia/Tbilisi**. Engineering assessment, not a signed agreement or legal
approval. Display rights, data extraction, retention, caching, commercial access and attribution
are distinct. No paid plan, provider account, deployment or partner access was enabled.

## Rights matrix

| Component | Commercial use / attribution | Caching, extraction and limitation |
|---|---|---|
| MapLibre GL JS 6.13.0 | BSD-3-Clause renderer; retain license/notices when distributing | Renderer license grants no rights to a supplier's tiles, fonts or styles |
| Mapbox GL JS 3.32.0 + Standard | Proprietary product/account terms; retain Mapbox logo and Mapbox/OSM/Improve-this-map text | Licensed display through relevant Mapbox products; no general reusable dataset or third-party renderer license inferred |
| MapTiler Cloud Streets v4 | Eligible commercial plan and source attribution; logo requirements depend on plan/product | Temporary single-user device cache; direct provider requests; proxy/export/bulk acquisition require agreement; commercial derivative extraction restricted |
| OpenFreeMap Liberty / public hosting | Provider states commercial display allowed; OpenMapTiles/OSM attribution and style/font notices apply | Public service is as-is, no SLA; automated data collection without permission restricted; no blanket offline/bulk cache right inferred |
| Independently sourced OSM data | ODbL commercial use with attribution and applicable derivative database/share-alike requirements | Data rights differ from OSM's public API/tile service policies; use a lawful extract/own service for operational derivation |
| Georgian authoritative geoportal/cadastral resources | Dataset-level access, license, CRS and attribution remain unconfirmed | Viewing/catalogue availability does not grant downloadable commercial building/height data; no such feed obtained |
| Environmental / partner data | Independent source/partner terms and dated publication rights required | Basemap purchase grants no forecast, route archival, supplier availability or CitySense evidence rights |

Sources: [MapLibre license](https://github.com/maplibre/maplibre-gl-js/blob/main/LICENSE.txt),
[Mapbox SDK license](https://github.com/mapbox/mapbox-gl-js/blob/main/LICENSE.txt),
[Mapbox attribution](https://docs.mapbox.com/help/dive-deeper/attribution/),
[MapTiler Cloud terms](https://www.maptiler.com/terms/cloud/),
[OpenFreeMap terms](https://openfreemap.org/tos/),
[OSM copyright](https://www.openstreetmap.org/copyright),
[NSDI terms entry point](https://nsdi.gov.ge/en/terms-of-use).
NSDI's terms page exposed no readable text through the web tool; resource-specific rights remain open.

The test retains MapTiler's official linked logo, including for Free-plan inspection, following
its [attribution guide](https://docs.maptiler.com/guides/map-design/attribution/add-attribution/).

## Mapbox current product terms

The current [July 21, 2026 product terms PDF](https://cdn.prod.website-files.com/609ed46055e27a02ffc0749b/6a60463142f6478d57642594_Mapbox%20Product%20Terms%20%28July%2021%2C%202026%29.pdf)
was downloaded from the official legal portal and text-read locally; web-tool PDF access failed.
Sections 1.9/1.10 restrict automated/bulk acquisition, storage and redistribution by default.
Section 2.8.1 permits Mapping API content caching on the requesting end-user device for up to
30 days, with direct API population and applicable mobile SDK limits; it does not authorize a
shared tile proxy/cache or screenshots replacing API access. Section 2.8.3 links map-load/seat
pricing to a qualified renderer and unmodified accounting behavior. Section 2.7 treats temporary
geocode retention differently from eligible permanent geocodes. No geocoding/routing archive is
automatically cleared for immutable research replay.

Retained legal source: `artifacts/map-stage-1/mapbox-product-terms-2026-07-21.pdf` and text;
SHA256/pages are recorded in [verification](../evidence/map-stage-1/verification.json).
No Mapbox map content was fetched or archived. Future screenshots need attribution and a
permitted evidence/export purpose; they must not substitute for runtime API access.

## MapTiler and independent data derivation

Under [Cloud terms §§5–7](https://www.maptiler.com/terms/cloud/), temporary end-user caching is
allowed, while shared server caching/proxying and exported map content require separate permission.
Commercial derivatives and service-substitute datasets are restricted. CitySense should use
MapTiler for display and derive any future greenery/building/road features from independently
licensed source data, not from extracted hosted tiles or traced screenshots. Basemap display
and analytical data pipelines remain separate. No provider tile extraction was performed here.

MapLibre's license does not weaken these restrictions. Self-hosted OSM/OpenMapTiles is a possible
future exit path, with its own notices, ODbL assessment, storage/egress, update and operational
burden. It is not a completed replacement infrastructure.

## OpenFreeMap rights and service risk

[OpenFreeMap's overview](https://openfreemap.org/) advertises free public hosting without keys or
view/request limits, commercial use and documented planet downloads/self-hosting. It offers no
SLA. Its [September 9, 2026 terms](https://openfreemap.org/tos/) restrict unpermitted automated
data collection and permit discontinuation. This session inspected configuration metadata and
prepared a normal map client; it did not harvest vector tiles. Dataset acquisition should use
the documented download route and resolved service permissions, not assume that unrestricted
map display permits scraping.

The [license ledger](https://github.com/hyperknot/openfreemap/blob/main/LICENSE.md) distinguishes
MIT infrastructure, BSD style/schema code, CC BY design, ODbL data and SIL OFL fonts. Preserve
these if redistributing adapted assets. Ordinary browser behavior is not an authorization for
a CitySense offline-pack service or shared cache; resolve that use before implementing it.

## Published pricing and modeled operational costs

USD, excluding tax, reviewed October 10; public list prices may change. These are planning
calculations, not invoices, provider measurements or forecasts of actual CitySense traffic.

**Mapbox web map loads:** first 50,000 monthly loads free; next 50,000 at $5/1,000; next
100,000 at $4/1,000. A map instance initialization counts as a load; avoid recreating the
map on every view/query. Long sessions can incur another load after the documented maximum
session window. Native mobile MAU pricing is not the PWA model.
[Pricing](https://www.mapbox.com/pricing), [GL JS metering](https://docs.mapbox.com/mapbox-gl-js/guides/pricing/).

**MapTiler Flex:** $30/month; 500,000 API requests included; extra requests $0.15/1,000.
For this plain MapLibre integration, use the request model, not MapTiler SDK session pricing.
The advertised 25,000 sessions and 3D-session quotas are separate metering paths, not another
free pool to add to the request model. The Custom plan advertises a 99.9% SLA; do not claim
that Flex has the same guarantee.
[Plans/rates](https://www.maptiler.com/cloud/pricing/), [metering](https://docs.maptiler.com/guides/account/sessions-vs-requests/).

| Monthly map initializations | Mapbox map-load model | MapTiler Flex, assumed 25 requests/init | MapTiler sensitivity, 50 requests/init |
|---:|---:|---:|---:|
| 20,000 | $0 | 500,000 requests → **$30** | 1,000,000 → **$105** |
| 100,000 | **$250** | 2,500,000 → **$330** | 5,000,000 → **$705** |
| 200,000 | **$650** | 5,000,000 → **$705** | 10,000,000 → **$1,455** |

Request counts include whatever billable requests the actual provider integration makes:
styles/tiles/resources and user interaction must be measured against account analytics. The
25/50 assumptions are illustrative, not measured. Panning, zooming, languages, DPR, caching,
session length and extra sources change the result. Request metering can make MapTiler more
expensive for intensive interaction even with an open source renderer. SDK/session metering
would require a separate implementation/cost comparison.

OpenFreeMap's advertised public hosting fee is $0, with optional support/donations and no
contractual availability guarantee. Self-hosting is not zero cost: provision extracts/builds,
tile storage, CDN/egress, updates, monitoring and operational ownership. No infrastructure quote
or volume benchmark was obtained.

Directions, isochrones, geocoding, weather, custom tiling, server hosting and any supplier calls
are separate costs. The Mapbox pricing page lists Directions and Isochrone first 100,000 monthly
requests free, then $2/1,000 in their first paid tier; no such calls were made. Weather commercial
API access needs a separately eligible plan; [Open-Meteo terms](https://open-meteo.com/en/terms)
do not let the basemap subscription grant those rights.

## Operational controls to carry into an approved later stage

Restrict browser tokens/keys by origin and scope, keep operator/account secrets server-side,
set account spending limits/alerts and measure actual usage. Keep legal snapshots, provider
versions and source attribution with the release evidence. Do not proxy a hosted provider to
hide a key when its terms require direct requests. Direct provider traffic reveals requester IP
and viewed tile region even without CitySense geolocation; review that data flow before users.

A later PWA may cache its own permitted shell/assets. Provider tile/font/style caching must
follow the chosen contract, freshness and per-user limits; no service worker/offline maps were
enabled here. CitySense API responses already specify no-store and must remain outside offline
caches. Preserve research/cache/publication separation and expiry/revocation; a visual basemap
does not authorize publishing the retained five Sprint 3 park geometries.
