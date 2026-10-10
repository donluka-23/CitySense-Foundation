# Map provider costs and commercial constraints — Stage 1B

Reviewed **2026-10-10, Asia/Tbilisi** against official sources. Planning assessment; no account
purchase, production agreement, invoice, quota telemetry or deployment. Historical Stage 1
rights evidence is retained in [MAP_DATA_RIGHTS_AND_COSTS.md](MAP_DATA_RIGHTS_AND_COSTS.md).

## Billing units and explicit model

Mapbox GL JS test uses **Map Loads for Web**, not native mobile MAU or the separate Seats option.
First 50,000 monthly loads are free; the next 50,000 cost $5/1,000, next 100,000 $4/1,000,
next 800,000 $3/1,000. [Official rates](https://www.mapbox.com/pricing).
Initialization counts; a session has a 12-hour maximum. Normal pan/zoom does not add map loads.
[GL JS accounting](https://docs.mapbox.com/mapbox-gl-js/guides/pricing/).

Plain MapLibre uses MapTiler **API requests**, not SDK sessions. Flex is $30/month with 500,000
included requests and $0.15/1,000 extra. Vector tiles count once; style/TileJSON/fonts are listed
free. Raster 512px tiles count four requests. Free is intended for PoC/personal/non-commercial
use; it pauses at quota. Custom offers 99.9% SLA; Flex is not assigned that guarantee here.
[Official pricing and unit table](https://www.maptiler.com/cloud/pricing/),
[session/request distinction](https://docs.maptiler.com/guides/account/sessions-vs-requests/).

Assumptions: every modeled active user initializes **2 maps/month**; all map sessions under 12h;
**25 billable vector tile requests/load**, sensitivity **50**. Request counts are assumptions,
not measured network entries; free style/font requests are excluded. Account has no other usage.
USD before tax; full monthly quotas available; no discounts, routing, search, weather, custom
data hosting, cloud/backend costs or support subscriptions. MAU is an input to this model,
not either tested integration's billing unit. Tiles, languages, DPR, cache, 3D and gestures can
change real request volume. Use account analytics to calibrate, not incomplete Resource Timing.

| Assumed MAU | Loads (2/user) | Mapbox web loads | MapTiler Flex: 25 tiles/load | MapTiler Flex: 50 tiles/load | OpenFreeMap hosting |
|---:|---:|---:|---:|---:|---:|
| 1,000 | 2,000 | $0 | 50,000 requests → $30 | 100,000 → $30 | $0, no SLA |
| 10,000 | 20,000 | $0 | 500,000 → $30 | 1,000,000 → $105 | $0, no SLA |
| 100,000 | 200,000 | $650 | 5,000,000 → $705 | 10,000,000 → $1,455 | $0, no SLA |

Sensitivity at **10 map initializations/user/month**, all other assumptions unchanged:

| Assumed MAU | Loads | Mapbox | MapTiler: 25 tiles/load | MapTiler: 50 tiles/load |
|---:|---:|---:|---:|---:|
| 1,000 | 10,000 | $0 | $30 | $30 |
| 10,000 | 100,000 | $250 | $330 | $705 |
| 100,000 | 1,000,000 | $3,050 | $3,705 | $7,455 |

For `L = MAU × maps_per_user` and `T = L × billable_tiles_per_load`:

```text
MapTiler Flex = 30 + max(0, T - 500000) / 1000 × 0.15
Mapbox (L ≤ 1000000) =
  min(max(L - 50000, 0), 50000) / 1000 × 5
  + min(max(L - 100000, 0), 100000) / 1000 × 4
  + min(max(L - 200000, 0), 800000) / 1000 × 3
```

These are our calculations from published tiers, not forecasts or guaranteed invoice rounding.
Quotas/usage across an account, other apps and support contracts can alter the total. Actual
per-load tiles and long sessions remain unknown. Comparison reloads initialize maps and consume
quota; do not run this QA matrix as unattended polling. OpenFreeMap advertises free commercial
hosting, but self-hosting needs storage/CDN/updates/operations quotes, currently unknown.
[OpenFreeMap overview](https://openfreemap.org/).

## Commercial rights, attribution and access

| Provider/component | Use and notices | Access / production support |
|---|---|---|
| MapLibre renderer | BSD-3-Clause; incorporated notices retained | Open renderer license does not clear MapTiler/OpenFreeMap data or guarantee support |
| MapTiler Cloud | Eligible paid commercial plan for product; source attribution, applicable linked logo; PoC retains logo | Dedicated origin-restricted browser API key; direct provider requests; Custom SLA/contract and premium support need agreement |
| Mapbox GL JS / Standard | Proprietary product/account license; Mapbox logo plus Mapbox/OSM/Improve-map text | Dedicated `pk.` token with read scopes/URL restrictions; eligible executed order needed for documented SLA |
| OpenFreeMap | Provider advertises commercial display; source/OpenMapTiles/OSM notices; style/font licenses separate | No key; as-is public service can be discontinued; no SLA or production commitment inferred |

[MapLibre license](https://github.com/maplibre/maplibre-gl-js/blob/main/LICENSE.txt),
[Mapbox SDK license](https://github.com/mapbox/mapbox-gl-js/blob/main/LICENSE.txt),
[Mapbox attribution](https://docs.mapbox.com/help/dive-deeper/attribution/),
[MapTiler attribution](https://docs.maptiler.com/guides/map-design/attribution/add-attribution/),
[MapTiler Cloud terms](https://www.maptiler.com/terms/cloud/),
[OpenFreeMap license ledger](https://github.com/hyperknot/openfreemap/blob/main/LICENSE.md),
[OpenFreeMap terms](https://openfreemap.org/tos/).
Mapbox's [SLA](https://www.mapbox.com/legal/sla) conditions 99.9% API service credits on an active
executed order and covered APIs; this PoC has no verified such entitlement. SLA is not label/height accuracy.

MapTiler's [API-key guide](https://docs.maptiler.com/guides/credentials/api-key/) specifies local
origin entries `127.0.0.1` / `localhost` without protocol/port. These are distinct origins and
localhost restrictions match other machines; keep local and production keys separate. Mapbox
[public tokens/URL restrictions](https://docs.mapbox.com/help/dive-deeper/access-tokens/) require
least-privilege read scopes and allowed local URLs. Never transmit `sk.` account tokens; server
filters them. MapTiler must receive a browser API key, not account-management/service secrets.
Do not send keys in chat, URLs, repository files, HAR evidence or screenshots of configuration.

## Cache, offline, extraction and redistribution

MapTiler terms §§5–7 allow temporary personal single-user device caching and require direct
API requests. Proxying, bulk downloads and export outside the service need agreement; commercial
extraction/derivatives and service-substitute datasets are restricted. Internal inspection images
must remain within permitted QA purpose; verify external sharing/export rights for the account.
Screenshots cannot substitute for API map delivery. [Current terms](https://www.maptiler.com/terms/cloud/).

Mapbox's [current product-terms portal](https://www.mapbox.com/legal/product-terms) links the
[July 21, 2026 PDF](https://cdn.prod.website-files.com/609ed46055e27a02ffc0749b/6a60463142f6478d57642594_Mapbox%20Product%20Terms%20%28July%2021%2C%202026%29.pdf).
The portal was rechecked; web PDF access failed again. The official PDF/text already retained
in Stage 1 was used for clause review, with hashes in its verification receipt. §§1.9/1.10
restrict acquisition/storage/redistribution; §2.8.1 allows directly populated requesting-device
Mapping API cache up to 30 days, subject to applicable conditions. It does not clear shared
proxies, offline archives or screenshot substitutes. §2.8.3 preserves qualified-renderer
accounting. No vendor accounting/metrics behavior was modified.

OpenFreeMap's September 9, 2026 [terms](https://openfreemap.org/tos/) forbid unpermitted automated
data collection and make public hosting as-is. Normal documented map display differs from bulk
tile extraction. Use documented planet downloads/self-hosting only with the corresponding
data/service license assessment; no offline/shared cache was built here.

Independently acquired OSM data is ODbL, with attribution and applicable derivative database
obligations. Hosted style/display rights are separate. Our bounded camera receipt is OSM source
evidence, not extracted paid tiles or publication of restricted Sprint 3 geometry.
[OSM copyright](https://www.openstreetmap.org/copyright).
MapLibre portability offers an exit path, not rights to export a managed provider's content.

## PWA / WebView and unresolved commercial decisions

These providers document web/app display; a PWA or Telegram WebView does not create a licensing
exemption or automatically select native mobile billing. The test loads browser JS, uses normal
accounting and keeps notices. Origin/referrer behavior and WebGL2 in actual Telegram/iOS/Android
clients are unverified. Do not weaken restrictions or switch to account secrets to make a WebView
work. The current text Telegram adapter is not proof of Mini App readiness.
[Telegram Mini Apps](https://core.telegram.org/bots/webapps).

Before commercial commitment: select an eligible account/plan, confirm screenshot sharing and
required retention/offline rights, set budget limits, measure account usage, determine service
support entitlement and review vendor request privacy. API/user identity, independently licensed
weather/routing/availability, provider exports and self-hosting costs remain unresolved. No basemap
contract fixes source-publication prohibitions, sparse scientific evidence or research validity.
