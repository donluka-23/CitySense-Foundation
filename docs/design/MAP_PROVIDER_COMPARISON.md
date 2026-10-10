# Map provider comparison — Stage 1

Assessment date: **2026-10-10, Asia/Tbilisi**. Scope: map infrastructure, not application
design. Recommendation is provisional; provider-specific Batumi rendering and mobile
benchmarks were unavailable. See [coverage](BATUMI_MAP_COVERAGE_AUDIT.md),
[rights/costs](MAP_DATA_RIGHTS_AND_COSTS.md) and [report](MAP_STAGE_1_REPORT.md).

## Recommendation and decision basis

Prefer **MapLibre GL JS + MapTiler Cloud Streets v4** for the eventual PWA, conditional on
authorized Batumi visual/language checks, acceptable request costs and the required service
agreement. This offers a replaceable renderer, explicit layer control and a managed supplier.
CitySense's own evidence must remain independently licensed and supplied through its API.
MapTiler's official [MapLibre integration](https://docs.maptiler.com/maplibre/) identifies
`https://api.maptiler.com/maps/streets-v4/style.json?key=...` as a compatible style.

**Fallback: Mapbox GL JS + Mapbox Standard**, if the same Batumi tests show materially better
coverage/cartography or managed 3D and its ordering, rights and costs meet CitySense needs.
This is a conditional alternative, not an automatic runtime failover. The current evidence
cannot establish which provider looks better or has more complete local data.

**Credential-free Stage 1 test source: OpenFreeMap Liberty**,
`https://tiles.openfreemap.org/styles/liberty`. Its documented compatibility makes it useful
for local inspection. Its public service has no SLA; use as a production provider would need
an explicit reliability decision and a viable self-hosting/supplier switch plan. Commercial
display is allowed according to the [provider overview](https://openfreemap.org/).

The priority order is lawful display/data separation, local coverage, controllable overlay
ordering, measured mobile performance, operations and cost. Managed 3D alone cannot resolve
the current absence of CitySense observations, verified entrances or route data. No weighted
numeric score is invented for candidates that have not been rendered.

## Exact stacks evaluated

| Stack | Renderer / style / data | Actual Stage 1 evidence |
|---|---|---|
| Mapbox | GL JS **3.32.0**, `mapbox://styles/mapbox/standard`; Mapbox-maintained proprietary/open-source composite map content | Package/official documentation and current product terms examined; no token or style/tile rendering |
| Managed MapLibre | GL JS **6.13.0**, MapTiler **Streets v4**, MapTiler Cloud data; provider-controlled style/schema version must be recorded after access | Compatible official integration and plan/terms examined; no key or live style/tile rendering |
| Local test MapLibre | Same renderer, OpenFreeMap **Liberty**, OSM/OpenMapTiles schema | Live style and TileJSON HTTP 200; tile path build `20261004_113936_pt`, max native zoom 14; no tiles extracted/rendered |

Versions were resolved from the official npm registry and pinned in the isolated lockfile.
They are test pins, not a promise that future upstream releases/styles remain unchanged.
OpenFreeMap's build-path date is not a verified OSM extract cutoff or field observation date.
OSM audit results below are not automatically the content of either paid provider's tiles.

## Official technical capability comparison

Capabilities are documented, not experimentally certified by this session. MapLibre is a
renderer: data quality, routing, weather and availability are separate services.

| Capability | Mapbox GL JS + Standard | MapLibre GL JS + compatible provider | Implication for CitySense |
|---|---|---|---|
| Custom spatial layers | Custom sources/layers alongside imported basemap; supported insertion slots | Custom point/line/fill/symbol layers, expressions and feature state | Render authorized CitySense features independently of basemap POIs |
| Cluster aggregation | GeoJSON clustering and `clusterProperties` expressions | GeoJSON clustering and `clusterProperties` expressions | Count authorized records and missing/stale classes; do not treat clustered averages as engine scores |
| 3D buildings | Standard supports provider buildings, models and lighting; Batumi presence unverified | `fill-extrusion` and custom 3D layers; supplied heights required | Keep unknown heights flat; no shadow/thermal inference from display geometry |
| GeoJSON / vector tiles | GeoJSON and MVT sources; Standard-specific imports/featuresets remain vendor-specific | GeoJSON and MVT with compatible style/sources | Current bounded point reads can later become a GeoJSON projection; large geometry needs a separate contract |
| Raster / weather overlays | Raster/image/video/DEM sources; specialized capabilities do not include a weather license | Raster/image/video/DEM sources; custom layers possible | Licensed raster forecasts can be displayed with valid time/resolution; no generated heatmaps |
| GPU animation | Custom WebGL render hooks and repaint scheduling; newer style features are vendor-specific | Custom WebGL render hooks and repaint scheduling | Shader animation is possible, but a render engine does not supply truthful weather/time series |
| Mobile browsers | GPU rendering; GL JS v3 requires WebGL2 | GPU rendering; selected GL JS v6 requires WebGL2 | Real iOS Safari / Android Chrome and context-loss testing are mandatory |
| Ordering | Standard uses `bottom`, `middle`, `top`; imported basemap internals have limited direct customization | Explicit `beforeId`, `moveLayer`, paint/layout/filter control for supplied accessible layers | MapLibre offers finer placement around roads, buildings and labels; provider layer IDs still need regression checks |
| Maintenance | Managed basemap updates; proprietary SDK/product coupling | Open source renderer plus independent provider/schema/asset maintenance | Pins alone do not freeze remotely hosted style or tile changes |

Primary capability references: [Mapbox Standard guide](https://docs.mapbox.com/map-styles/guides/standard-styles/),
[Mapbox cluster example](https://docs.mapbox.com/mapbox-gl-js/example/cluster-html/),
[MapLibre cluster example](https://maplibre.org/maplibre-gl-js/docs/examples/display-html-clusters-with-custom-properties/),
[MapLibre sources](https://maplibre.org/maplibre-style-spec/sources/),
[MapLibre 3D buildings](https://maplibre.org/maplibre-gl-js/docs/examples/display-buildings-in-3d/),
[Mapbox custom layers](https://docs.mapbox.com/mapbox-gl-js/api/properties/#customlayerinterface),
[MapLibre custom layers](https://maplibre.org/maplibre-gl-js/docs/API/interfaces/CustomLayerInterface/).
WebGL2 requirements were also checked in the installed versions' source/types.

Standard is not a MapLibre-compatible style: imports, featuresets, model layers and lighting
must not be assumed interchangeable. Imported Standard basemap interaction uses supported
featuresets; custom CitySense layers remain separately owned/queryable. Standard configuration
is more constrained than arbitrary classic-style layer edits. Draped overlays can be reordered
under globe/terrain; final overlay visibility must be tested in the selected projection.
These constraints follow the [Standard guide](https://docs.mapbox.com/map-styles/guides/standard-styles/)
and [layer-order documentation](https://docs.mapbox.com/help/troubleshooting/layer-rendering-order/).

## Batumi language and height implications

Mapbox documents both `ka` and `en`, with local-name fallback where a translation is absent.
Support does not establish that every Batumi feature has both labels.
[Mapbox internationalization](https://docs.mapbox.com/help/dive-deeper/maps-internationalization/).

OpenFreeMap TileJSON actually exposes `name:ka` and `name:en` for place labels; its default
Liberty style also uses Latin/non-Latin name expressions. The POC selects source names explicitly,
without translating missing names. Georgian glyph presence and text shaping have not been tested.
MapTiler's local label delivery remains unverified until authorized live access.

OpenMapTiles describes `render_height` as an approximation. Upstream Planetiler code can derive
it from `height`, estimate it from levels, or fall back to a default. This is a reason to hide
extrusions in the test, not proof of the exact generator version used for the fetched tile build.
[Building schema](https://github.com/openmaptiles/openmaptiles/blob/master/layers/building/building.yaml),
[upstream processing code](https://raw.githubusercontent.com/openmaptiles/planetiler-openmaptiles/main/src/main/java/org/openmaptiles/layers/Building.java).

## Mobile performance assessment

No measured FPS, map load time, GPU memory, battery use, physical-device behavior or provider
latency is available. The local asset sizes are uncompressed package bytes, not download budgets
or comparative mobile results: MapLibre main module about 1.08 MB plus 0.51 MB worker; Mapbox
bundle about 1.90 MB. Compression, cache, style complexity, data size and DPR can reverse the
apparent ordering. A package-byte comparison is not a performance winner.

For later tests, keep a single map instance, load it only when needed, constrain visible data,
prefer GL layers to many DOM markers, use point clustering and simplify authorized geometry.
Use vector tiles for larger datasets and change feature state instead of repeatedly sending full
GeoJSON. These are engineering starting points, supported by
[MapLibre large-data guidance](https://maplibre.org/maplibre-gl-js/docs/guides/large-data/)
and [Mapbox large-GeoJSON guidance](https://docs.mapbox.com/help/troubleshooting/working-with-large-geojson-data/).

The proposed verification matrix is recent iPhone Safari, a lower-end supported Android Chrome
device and desktop, at 390×844 and a larger viewport, native DPR and controlled network conditions.
Run five cold/warm loads per provider/view/language, plus a fixed 30-second pan/zoom trace.
Record first usable map/idle, requested bytes, requests, p95 frame intervals, errors/context loss,
readable Georgian glyphs and attribution. Proposed initial targets are a usable basemap within
3 seconds on a defined 4G profile and responsive interaction at at least 30 FPS; these are proposed
engineering targets, not achieved measurements or release approval. Respect reduced motion and
pause nonessential animation on hidden tabs.

## Future integration compatibility against actual contracts

| CitySense area | Repository reality | Compatibility / remaining requirement |
|---|---|---|
| Place / Opportunity Registry | `PlaceResult.geometry` is WGS84 Point; provider/place/city IDs and rights are typed; registry contracts only | Both engines can display a later authorized GeoJSON projection with stable CitySense IDs. Basemap POIs must not become verified partner records |
| Observations / forecasts | Sparse per-place `EvidenceResult`, timestamps/kind/quality/rights; no weather tile API | Both can show separately licensed point/raster layers. No interpolation of missing measurements; no forecast issuance invented from retrieval time |
| Suitability | `/suitability` returns state, inputs and assessment; null scores/exclusions and unvalidated model/hash | Join by internal `place_id`; carry coverage/missingness. Neither renderer computes or repairs engine output |
| Walking routes | `walking_time_source=caller_estimate`; no route endpoint or graph | Line rendering is supported, but geometry/time/access/rights need a new reviewed adapter and additive contract |
| Isochrones | Absent | Polygon rendering supported; contours must come from an authorized network service, not radius circles mislabeled as travel times |
| Authorized partner availability | `Offer` requires confirmation/expiry; no operational partner adapter | Map rendering is compatible; runtime freshness and partner authorization remain independent blockers |

The five city operations require a configured operator `X-API-Key` and city scope, have no-store
responses and enforce publication rights. There is no browser CORS support or per-user identity
contract. Do not expose the operator key in a PWA. A future authorized local integration can use
an appropriately scoped server boundary; public product identity is a separate reviewed task.
No API integration, registry mutation, engine modification or architecture ADR was implemented here.

## Conditions that could change the recommendation

Choose Mapbox if the credentialed Batumi audit demonstrates a material benefit and Standard's
placement controls meet the actual overlay requirements. Choose a contracted/self-hosted MapLibre
source if supplier retention requirements cannot accommodate evidence archival or if request costs
are unsuitable. Choose OpenFreeMap public hosting only after accepting its no-SLA dependence and
service-policy limits. No provider can supply missing CitySense scientific validity or supplier consent.
