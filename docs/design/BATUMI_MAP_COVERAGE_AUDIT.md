# Batumi map coverage audit — Stage 1

Audit date: **2026-10-10, Asia/Tbilisi**. **Actual source coverage was inspected; provider
rendering was not verified.** OSM presence must not be promoted to Mapbox/MapTiler coverage,
field completeness, navigability, measured heights or CitySense suitability.

## Evidence and geographical scope

One successful, manually invoked, aggregate Overpass query sampled the rectangle
**west 41.60, south 41.61, east 41.67, north 41.67**, EPSG:4326. It covers a central/southern
Batumi sample including the old-town/waterfront/6 May Park area, not the administrative city.
It excludes the Botanical Garden test view, Gonio and portions of the airport/periphery.
Overpass selects objects intersecting its node-based bounding-box semantics; counts are not
clipped areas, independent buildings, unique streets or network length.

- Retrieval: **2026-10-09T20:45:42.554Z = 2026-10-10 00:45:42.554 Tbilisi**.
- Provider database timestamp: **2026-10-09T20:44:33Z**; not the objects' field survey times.
- Projected response: **10,734 bytes**; 19 count results and 24 geographic name records.
- Raw response SHA256: `7db0d9848b55f11b1ed4d15fb2e967d2993ca8879efd8d4550058f9c66497af7`.
- Query SHA256: `e0ae37776e7bc302077dff77c6f3a1fe16d30f2a1456627384e913283e08be14`.
- Checked-in aggregate evidence: [summary](../evidence/map-stage-1/osm-coverage-summary.json)
  and [exact query](../evidence/map-stage-1/osm-query.overpassql).
- Private full projected response: `artifacts/map-stage-1/osm-final-2026-10-10/response.json`;
  full receipt: adjacent `coverage-summary.json`.

The query returns counts and explicitly projected geographic names/IDs, without contributor,
contact, participant or personal location data. Two earlier attempts returned HTTP 400 because
the server rejected a Unicode character-range regex. The final query uses explicit-character
alternation and has no partial-execution remark. Failure receipts remain in ignored artifacts.
There is no polling or ingestion into CitySense. The [Overpass operator policy](https://dev.overpass-api.de/overpass-doc/en/preface/commons.html)
supports bounded manual use; it does not provide a production backend/SLA.

## Observed source coverage

| Required dimension | Actual observed OSM evidence in this rectangle | What remains unverified |
|---|---|---|
| Street network | **7,796** `highway` ways | Geometry correctness, turn restrictions, crossings, connected topology, access and completeness |
| Pedestrian network | **2,973** ways tagged footway/path/pedestrian/steps | Continuous Boulevard traversal, gates, steps/accessibility, surface and field safety; steps are not step-free paths |
| Building footprint candidates | **15,406** building ways and **45** building relations; **237** building-part ways separately | Closed/valid footprint geometry, deduplication of relations/parts, unmapped/new construction |
| Available height metadata | **76** building ways with `height`; **3,846** with `building:levels`; union **3,854** | Numeric/unit validity, surveying, roof shape, currency and each provider's delivered heights |
| Coastline/waterfront | **8** coastline ways; named Nuri/Ardagani water objects and mapped pedestrian objects | Shoreline position, complete water polygons, erosion/new works, exact waterfront path continuity |
| Parks/vegetation | **49** park ways, **3** park relations; **1,368** ways with selected wood/grassland/scrub/forest/grass/meadow/orchard tags | Distinct parks, canopy/seasonality, area fraction, species, current vegetation or street shade |
| Landmarks | **18** tourism-attraction objects; actual names include Piazza, Alphabetic Tower, Lighthouse and Cathedral | All landmark tag families, POI placement/rank, label collision and any detailed 3D landmark model |
| Georgian/English streets | **1,376** named highway ways; **1,371** have `name:en`, **1,362** have `name:ka`; **1,376** have Georgian letters in `name` | Translations' accuracy, counts' overlap, hosted-tile retention, glyphs and on-screen readability |
| Georgian/English attractions | **14** of 18 attraction objects have `name:en`; **8** have `name:ka` | Other attractions may have Georgian in `name`; lack of explicit `name:ka` is not proof of no Georgian label |

The highway denominator includes small unnamed paths and service ways. Named-street counts
do not measure the proportion of independent streets translated. Vegetation tags are presence
evidence only; this audit computes no surface fractions, weather field or shade score.

## Explicit geographic label evidence

These are actual projected OSM records, not translations invented for this report. Clickable
OSM references identify the source objects; they are not inspected field sites.

| Source object | `name` / Georgian field | English field |
|---|---|---|
| [node/160257516](https://www.openstreetmap.org/node/160257516) | ბათუმი | Batumi |
| [relation/3164797](https://www.openstreetmap.org/relation/3164797) | 6 მაისი პარკი | 6 May Park |
| [way/34910874](https://www.openstreetmap.org/way/34910874) | ნურის ტბა | Nuri Lake |
| [way/294880812](https://www.openstreetmap.org/way/294880812) | პიაცა მოედანი | Batumi Piazza |
| [way/405852444](https://www.openstreetmap.org/way/405852444) | ანბანის კოშკი | Alphabetic Tower |
| [way/1306367386](https://www.openstreetmap.org/way/1306367386) | ბათუმის შუქურა | Batumi Lighthouse |

Source-specific tags differ: some attractions are artwork, historic objects or pedestrian
squares rather than `tourism=attraction`. Ali and Nino/Europe Square were not independently
verified by this selector; their omission is not evidence of absence. Botanical Garden lies
outside this query and is an unexecuted POC view, not verified coverage.

## Heights and lawful 3D interpretation

Only **0.49%** of sampled building ways carry a `height` tag. About **25.02%** carry either
height or floor count; **11,552** carry neither of these two tags. These are tag-presence rates,
not numeric-validity or surveyed-height rates. Alternative height tags/relations/parts were not
included in that denominator. No authoritative Batumi height dataset was acquired.

The OpenMapTiles schema labels `render_height` an approximation; upstream Planetiler code
uses source height where parseable, otherwise levels × 3.66, otherwise a 5 m default.
The actual OpenFreeMap build's generator revision/configuration is unconfirmed. Therefore a
tile `render_height` is insufficient to distinguish a measured/tagged height from an estimate.
[Schema](https://github.com/openmaptiles/openmaptiles/blob/master/layers/building/building.yaml),
[generator implementation](https://raw.githubusercontent.com/openmaptiles/planetiler-openmaptiles/main/src/main/java/org/openmaptiles/layers/Building.java).

The POC hides MapLibre extrusion layers and adds no guessed heights. Standard's optional
provider-built 3D is an inspection mode only; local availability/fidelity is unverified.
Neither option is used for shadow, shade or psychological/environmental inference.

## Provider-specific verification matrix

| Dimension | Mapbox Standard | MapTiler Streets v4 | OpenFreeMap Liberty |
|---|---|---|---|
| Streets/paths/buildings/coast/parks/landmarks in actual Batumi rendering | **Not verified: no authorized token and no browser** | **Not verified: no authorized key and no browser** | **Not verified: no browser** |
| Style/metadata service access | Credentialed style/tile calls not made | Credentialed style/tile calls not made | Style and TileJSON returned HTTP 200 using Node fetch; Python urllib default got 403 |
| Local Georgian/English label delivery | Documentation supports `ka`/`en`; Batumi delivery unverified | Compatible schema/language mechanisms documented; live delivery unverified | TileJSON lists `name:ka`/`name:en`; actual tile values and glyph rendering unverified |
| Actual 3D content/height fidelity | Unverified | Unverified | Schema has processed height fields; no tile height audit or 3D rendering |

OpenFreeMap metadata is retained in [provider-metadata.json](../evidence/map-stage-1/provider-metadata.json).
Its tile template names build `20261004_113936_pt`, max native zoom 14. No vector tiles
were downloaded/extracted for a derived data inventory. Normal POC rendering requests the
provider directly; its availability/CORS/fonts remain to be tested in a browser.

OSM is a source used in map supply chains, but this successful October 10 source audit cannot
establish provider processing lag, schema filtering or local completeness. Mapbox's data sources
are composite, including proprietary suppliers, as described in its
[Streets v8 reference](https://docs.mapbox.com/data/tilesets/reference/mapbox-streets-v8/).

## Screenshot evidence and remaining checks

**Actual screenshots: none. Paths: none.** The supported Browser runtime returned
`No browser is available` and browser discovery returned `[]`. There is no canvas rendering
receipt, visual approval or physical-mobile result. Placeholder or reconstructed images are
not supplied. Static HTTP checks must not be called a successful rendering test.

After access becomes available, capture overview/old-town/waterfront/park/south and the separately
unverified Botanical Garden view for each provider, English and Georgian, flat and permitted
provider 3D. Preserve attribution and record viewport/DPR/time/style/build/error count. Manually
inspect shoreline/path continuity, footprints, label glyphs/collisions and heights against a lawful
independent source. Treat surveyed height, path connectivity and accessibility as separate audits.

OSM audit outputs carry **© OpenStreetMap contributors**, [ODbL 1.0](https://www.openstreetmap.org/copyright).
This separate aggregate audit changes no publication permission on Sprint 3's private inventory.
