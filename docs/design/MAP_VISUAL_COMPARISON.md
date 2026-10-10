# Batumi visual comparison — Stage 1B

Reviewed 2026-10-10 (Asia/Tbilisi). **PARTIAL: no agent browser-rendered captures.**
MapTiler and Mapbox visual quality is unassessed. OpenFreeMap loading/style feedback is
user-reported, without an attached image available for independent inspection. No visual winner
or user visual approval is claimed. See [rendering evidence](MAP_RENDERING_EVIDENCE.md).

## Tested stacks and evidence strength

| Candidate | Exact renderer / official style | Actual evidence available |
|---|---|---|
| A | MapLibre GL JS 6.13.0 + MapTiler Streets v4 | Official compatible integration, pinned package, launch/configuration checks; no credentialed style, tiles or screenshot |
| B | Mapbox GL JS 3.32.0 + Mapbox Standard | Official capabilities/terms, pinned package, launch/configuration checks; no credentialed style, tiles or screenshot |
| C | Same MapLibre + OpenFreeMap Liberty | Stage 1 live style/TileJSON inspection; user reports a successful render but unacceptable current presentation; no agent screenshot |

A uses `https://api.maptiler.com/maps/streets-v4/style.json`; B uses
`mapbox://styles/mapbox/standard`; C uses `https://tiles.openfreemap.org/styles/liberty`.
Separate official renderers are loaded. Standard is not assumed compatible with MapLibre.
[Official MapTiler integration](https://docs.maptiler.com/maplibre/).

## Geographic controls

Centers below are exact source points from the fresh
[camera receipt](../evidence/map-stage-1b/camera-receipt.json), database timestamp
2026-10-09T21:21:06Z. Coordinate order is **longitude, latitude**. OSM source geometry is not
surveyed accuracy, a verified entrance or a claim of pedestrian access. A second bounded
[projected name-only query](../evidence/map-stage-1b/camera-labels.json) verified all four source
names in Georgian and English. The selected road segment is **Memed Abashidze Street**
(`highway=residential`), not a source-verified avenue designation.

| Preset | Verified center | Source / observation purpose |
|---|---|---|
| `overview` | 41.6360085, 41.6509502 | [Batumi place node 160257516](https://www.openstreetmap.org/node/160257516); coast, district structure, roads, large parks and density |
| `waterfront` | 41.6395066, 41.6560289 | First actual vertex of [Alphabet Tower way 405852444](https://www.openstreetmap.org/way/405852444), node 4080074547; northern Boulevard, waterfront paths and landmarks |
| `central` | 41.6407375, 41.649547 | First actual vertex of [Piazza way 294880812](https://www.openstreetmap.org/way/294880812), node 2985014410; blocks, small streets, POIs and bilingual labels |
| `street` | 41.6349322, 41.6500931 | Actual road vertex, node 409475078, [Memed Abashidze Street way 1152779731](https://www.openstreetmap.org/way/1152779731); building/path/label detail |

The [preset JSON](MAP_CAMERA_PRESETS.json) records every zoom, pitch and bearing.
Flat 2D is north-up/pitch 0; detail uses pitch 35; 3D uses pitch 60.
Camera zoom is an authored comparison setting. All candidates use Mercator and identical
settings within a location/condition. At equal zoom, visible detail also depends on tile
filtering, overscaling, minzoom and label collisions. This is an intended comparison outcome.

The overview is centered on the documented city node rather than an invented shifted location.
Actual city-edge framing still needs capture; a point preset does not prove that every district
fits every narrow viewport. Northern Boulevard does not audit the entire waterfront, Botanical
Garden, Gonio or peri-urban roads. Stage 1 source counts cover only its published bounding box.

## Cartographic inspection results

“Unavailable” below is a test state, not a negative rating of provider coverage. No numeric
scores are assigned to missing evidence. Each criterion must be reviewed across all presets,
zoom conditions and both requested languages with the same single-map viewport.

| Criterion | A: MapTiler | B: Mapbox | C: OpenFreeMap |
|---|---|---|---|
| Road hierarchy | Unavailable | Unavailable | Unassessed from retained captures |
| Building visibility / differentiation | Unavailable | Unavailable | User reports limited detail, weak urban hierarchy; actual footprints remain uninspected |
| Coastline detail | Unavailable | Unavailable | Unassessed from retained captures |
| Pedestrian paths / crossings | Unavailable | Unavailable | Unassessed; presence is not access/connectivity |
| Park / vegetation geometry | Unavailable | Unavailable | Unassessed; green styling is not measured canopy |
| Landmarks | Unavailable | Unavailable | Source names exist; visual representation unassessed |
| Label placement / collisions | Unavailable | Unavailable | Unassessed |
| Georgian labels / glyphs | Unavailable | Unavailable | Schema includes Georgian fields; rendering unassessed |
| English labels / fallback | Unavailable | Unavailable | Schema includes English fields; rendering unassessed |
| Icon / POI density | Unavailable | Unavailable | User reports excessive sparsity; exact camera/language unknown |
| Overall clarity / spatial depth | Unavailable | Unavailable | User finds current style unacceptable and low-depth |
| 3D representation / height lineage | Unavailable | Unavailable | Style has extrusion layer; visual presence/height accuracy unassessed |
| Consistency between zoom levels | Unavailable | Unavailable | Unassessed |

The feedback rejects the current Liberty presentation as a production choice. It does not
establish absent underlying buildings, inferior MapLibre rendering or superior paid-provider
coverage. Stage 1 intentionally hid extrusions; that explains an absence of extrusion in that
configuration but does not establish the cause of every visual concern. Flat building style,
zoom filtering, labels and source coverage must be distinguished through the controlled tests.
No screenshot was recreated and no cartography was redesigned.

## Building truth and 3D conditions

Stage 1 independently found 15,406 building ways but only 76 height-tagged ways within its
bounded OSM audit; 3,854 had height and/or levels. Those are source-tag counts, not verified
numeric/surveyed heights or the content of any provider. Heights remain unavailable for
scientific shade/thermal analysis. See [source coverage audit](BATUMI_MAP_COVERAGE_AUDIT.md).

| Candidate | Condition 3 behavior | What can honestly be claimed now |
|---|---|---|
| MapTiler | Retain any existing provider extrusion layer with original filters, visibility and minzoom; add none | Streets v4 authenticated style not fetched. Local 3D presence and height origin unknown; zero supplied layers is reported unavailable |
| Mapbox | Standard `show3dObjects=true`, daylight; provider models/buildings only | Official 3D capability, not verified Batumi models or surveyed height |
| OpenFreeMap | Retain Liberty's original `building-3d` extrusion layer | Style metadata uses `render_height` / `render_min_height`; approximation/default paths possible, exact feature lineage unknown |

Extrusion is a vertical rendering of a footprint with an assigned height. It is not proof of
surveyed roofs, facades, meshes or a digital twin. Provider model layers, where present, are
also not a measurement-quality claim. Record real/estimated/default/unknown lineage only when
source evidence identifies it; the current Batumi classification is **unknown**.
[OpenMapTiles building schema](https://github.com/openmaptiles/openmaptiles/blob/master/layers/building/building.yaml),
[upstream height-processing code](https://raw.githubusercontent.com/openmaptiles/planetiler-openmaptiles/main/src/main/java/org/openmaptiles/layers/Building.java).

## Documented technical capabilities (not exercised as CitySense overlays)

| Capability | MapLibre (A/C) | Mapbox (B) | Native versus additional work |
|---|---|---|---|
| Custom spatial layers | GeoJSON, vector, fill/line/circle/symbol | Same core types around Standard imports | Native SDK; no overlays implemented |
| Vector/raster/image/video overlays | Supported source types | Supported source types | Native renderer; content/rights and CRS handling separate |
| Cluster aggregation | GeoJSON clustering / `clusterProperties` | GeoJSON clustering / `clusterProperties` | Native; record counts/missingness, never manufacture suitability scores |
| Feature interaction | Events, querying, feature state | Custom-layer interaction; Standard basemap uses supported featuresets | Native APIs; exact interactions untested |
| Layer ordering | `beforeId`, move/paint/filter access to supplied layers | Standard insertion slots; imported internals constrained | Native; provider layer IDs/updates require maintenance |
| Time-dependent data | Update source/filter/paint | Update source/filter/paint | Native primitives; time controller, issuance/validity and interpolation policy are application work |
| Camera transitions | `jumpTo`, `easeTo`, `flyTo` | Equivalent camera methods | Native; accessibility/reduced-motion policy requires testing |
| GPU wind animation | Custom WebGL layer + repaint | Custom WebGL layer + repaint | Native hooks; shader/particle code or plugin, lawful wind field, units/timestep and validation are additional work |
| Touch / WebGL | Native gestures; selected version WebGL2 | Native gestures; selected version WebGL2 | Target hardware/WebView support untested |

Primary references: [MapLibre Map API](https://maplibre.org/maplibre-gl-js/docs/API/classes/Map/),
[MapLibre source spec](https://maplibre.org/maplibre-style-spec/sources/),
[MapLibre clusters](https://maplibre.org/maplibre-gl-js/docs/examples/display-html-clusters-with-custom-properties/),
[Mapbox clusters](https://docs.mapbox.com/mapbox-gl-js/example/cluster-html/),
[Mapbox Map API](https://docs.mapbox.com/mapbox-gl-js/api/map/),
[Mapbox Standard](https://docs.mapbox.com/map-styles/guides/standard-styles/),
[MapLibre custom WebGL interface](https://maplibre.org/maplibre-gl-js/docs/API/interfaces/CustomLayerInterface/),
[Mapbox custom WebGL interface](https://docs.mapbox.com/mapbox-gl-js/api/properties/#customlayerinterface).
No shader, weather plugin or deck.gl dependency was added. Raster/vector fields remain independently
licensed; MapTiler SDK weather is an additional product, not bundled into plain MapLibre.

Standard/globe/terrain can drape fill/line/raster under symbols regardless of requested order;
this test uses Mercator without terrain to reduce that variable. Future terrain overlays need
separate testing. [Official ordering constraints](https://docs.mapbox.com/help/troubleshooting/layer-rendering-order/).

## CitySense suitability and portability

Both engines can later render authorized point results, raster observations, independently
computed route lines and isochrone polygons. Neither supplies engine truth, route connectivity,
authorized availability or data-publication rights. Current REST geometry is point-only, bounded
to 30 results; null scores/abstentions and evidence timestamps must survive map projection.
The Opportunity Registry is contracts only. Walking times are caller estimates. No route,
weather-tile or operational availability API exists. The operator key must stay out of browsers.
[Actual OpenAPI contract](../OPENAPI_CONTRACT.md), [registry](../OPPORTUNITY_REGISTRY_DESIGN.md).

A PWA browser renderer is technically feasible; this directory contains no PWA implementation.
Telegram's Mini App environment exposes viewport/gesture controls, not a guarantee of WebGL2
or any provider's mobile performance. Current Telegram repository adapter is not a tested map
Mini App. Android/iOS/desktop Telegram must each be inspected for WebGL2, safe-area/viewport
changes, map gesture conflicts, origin restrictions and context restoration. No Telegram token
or deployment was enabled. [Official Mini App and debugging documentation](https://core.telegram.org/bots/webapps).

## Decision and confidence

Retain **MapLibre + MapTiler Streets v4 as an engineering candidate**, with moderate confidence
in integration fit, low confidence in its Batumi visual/performance suitability. Keep **Mapbox
Standard as the conditional alternative**, with no visual superiority claim. OpenFreeMap remains
a reference/technical contingency; the tested presentation has no user visual acceptance.

Local readability, urban detail and professional mobile quality cannot be ranked yet.
Both candidates have documented custom layers; honest environmental rendering depends on
CitySense data rather than basemap aesthetics. Performance/accessibility remain untested.
Commercial terms are identifiable but plan/evidence-export permissions need resolution.
The cost model is sensitive to tile interaction and can favor Mapbox even where MapLibre is
more portable. Renderer portability does not transfer a provider's style/data license.
See [cost comparison](MAP_PROVIDER_COST_COMPARISON.md). No amount of decorative 3D closes
these evidence gaps. Final provider and visual direction remain subject to user approval.
