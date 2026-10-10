# Batumi 3D data coverage

Reviewed 10 October 2026. **No live MapTiler Batumi tiles or volumetric buildings were
observed in this session.** Launching process/app-local configuration has no authorized key;
supported browser discovery returns no browser. Coverage must remain unknown rather than
being inferred from an SDK demonstration or an OSM count.

## Current schema and implemented height handling

MapTiler Planet **v4** documents a polygon `building` layer: `height` and `height_min` are
approximate metres derived from levels/height attributes; `underground` identifies underground
features. Building IDs are not declared unique. The layer starts at zoom 12 and supports
overzooming beyond its maximum native zoom 15. This is schema capability, not proof of
Batumi completeness, source accuracy or an authenticated Streets v4 source revision.
[Official Planet v4 building schema](https://docs.maptiler.com/schema/planet-v4/#building).

The older Planet v3 schema instead documents approximate `render_height`/`render_min_height`
and a `hide_3d` outline flag. Retained history is not rewritten; new rendering accepts both
schemas and honors exclusion flags. [Legacy schema](https://docs.maptiler.com/schema/planet/#building).

| Display input | Current behavior | Claimed accuracy |
|---|---|---|
| Positive numeric `height`, including numeric string | Prefer this approximate provider value | Provider approximation; not surveyed |
| Otherwise positive `render_height` | Compatible legacy approximation | Estimation/default lineage unspecified |
| `height_min`, legacy `min_height`/`render_min_height` | Base clamped to nonnegative height | Approximate; not terrain elevation |
| Missing/invalid/zero height, Illustrative Geometry off | Flat footprint; inspector says Data unavailable | No invented vertical measurement |
| Missing height, Illustrative Geometry on | Configurable 3–80m placeholder plus persistent banner | Explicitly illustrative, never coverage evidence |
| Underground or hidden outline | Excluded from custom volumes | No fabricated above-ground object |

Rendered heights are defensively capped at 1,000m; inspection retains the provided value.
No floors-to-height guess is performed locally. Building parts may have separate bases/heights.
Geometry is taken from live vector features, never traced from screenshots or downloaded as
unlicensed models. IDs are tile-local context, not stable Opportunity Registry/building identities.
Missing IDs are displayed as unavailable. Selected feature geometry is transient in-memory
highlighting only; reports and diagnostics do not export it.

## Existing bounded geographic evidence

Stage 1's retained OSM audit covers west 41.60, south 41.61, east 41.67, north 41.67.
It reports 15,406 building ways, 76 height-tagged ways, and 3,854 with height and/or levels
(about 25.02%). It also reports 7,796 highway ways and 2,973 pedestrian-related ways.
These are historical bounded OSM tag counts, **not** unique whole-city buildings, surveyed
heights, network accessibility, walkable connectivity or MapTiler-hosted coverage.
Source receipts/limitations: [Stage 1 coverage audit](BATUMI_MAP_COVERAGE_AUDIT.md).
No new bulk geographic query or hosted tile extraction was performed for this prototype.

| Geographic component | Retained evidence | Current hosted visual status |
|---|---|---|
| Streets and pedestrian spaces | Bounded OSM tag counts; Piazza pedestrian source/name receipts | Unverified; no route/isochrone quality finding |
| Buildings and 3D heights | OSM footprint/tag counts; current provider field documentation | Actual visible volumes, height distribution and coverage unknown |
| Coastline/waterfront | Documented northern waterfront anchor | Coastline alignment/detail not visually checked |
| Parks/vegetation | Retained Stage 1 source findings | Canopy geometry and rendered completeness unknown |
| Landmarks/labels | OSM names/coordinates for the four presets | Actual provider label placement/density unknown |
| Georgian/English | Retained name receipts contain both for checked locations | Partial UI translation implemented; hosted label/script rendering unverified |

## Exact fictional monitoring anchors

All coordinates are WGS84 longitude, latitude. Nodes/status/readings/coverage are fictional.
They are not installed sensors, surveyed entrances, exact feature centroids or access permissions.

| Node | Anchor | Longitude, latitude | Public source |
|---|---|---|---|
| SIM-01 | Alphabetic Tower / northern waterfront vertex | 41.6395066, 41.6560289 | Way 405852444, node 4080074547 |
| SIM-02 | Batumi Piazza vertex | 41.6407375, 41.6495470 | Way 294880812, node 2985014410 |
| SIM-03 | Memed Abashidze Street first vertex | 41.6349322, 41.6500931 | Way 1152779731, node 409475078 |
| SIM-04 | Batumi city place node | 41.6360085, 41.6509502 | Node 160257516 |
| SIM-05 | Same street's second documented vertex | 41.6350424, 41.6501425 | Way 1152779731, node 10711255033 |

Sources: [camera presets](MAP_CAMERA_PRESETS.json),
[retained public source geometry](../evidence/map-stage-1b/camera-source.json),
[name receipt](../evidence/map-stage-1b/camera-labels-receipt.json).
Source retrieval: 2026-10-09T21:22:19.243Z, OSM database timestamp 21:21:06Z (10 October locally).
No protected research geometry supplies these markers. Piazza is a documented pedestrian focus;
high pedestrian density is not measured.

Three synthetic groups use authored 55m waterfront, 450m central and 45m street disks.
Each node has an illustrative 18m radius. The larger central disk includes both of its anchor
points; none of the disks is an administrative district, sensor field of view or measured influence
surface. There is no spatial interpolation, weather heatmap or measured coloring outside nodes.

## Required completion evidence

After authorized launch, inspect all four presets with placeholders **off**. At central/waterfront
capture the same visible volumes at bearings 0° and 90°, pitch 50°, plus 2D comparison.
Record style hash, timestamp, viewport, DPR, exact camera, readiness and attribution. Log
actual fragment counts via Export diagnostics; these may duplicate tile fragments and omit
hidden/filtered buildings, so they cannot yield a city-wide percentage. Independently licensed
building IDs and reference survey/height data would be needed for completeness/accuracy evaluation.
Keep placeholder captures separate, explicitly labeled, and never count them as verified heights.
