# Digital Twin visual system

10 October 2026. Implemented in isolated executable code; **not visually verified**.
Map readability, geography, analytical clarity and performance take priority over effects.

## Visual hierarchy

Desktop: map-dominant main area, compact camera controls, 322px analytical inspector,
bottom timeline and unobtrusive status line. Mobile below 760px: map first, camera controls
collapsed initially, scrollable observation workspace below, wrapped timeline and header.
Branding is CitySense Lab; a permanent Simulation — Synthetic Data badge identifies every
application. No fabricated city screenshot, generated background or decorative globe is used.

Dark mode uses navy/charcoal context, subdued blue-grey buildings, cyan selected-object
accents and readable pale labels. Daylight uses light neutral land, muted blue water, restrained
green context, grey buildings and darker labels. UI typography uses available system fonts
(Inter only if already installed). Basemap fonts, glyph URLs, text fields and sprites are retained.
Partial Georgian translations cover shared controls/headings; technical caveats, metrics and
application options remain English. No claim of complete localization or hosted Georgian labels.

Theme changes preserve sources and semantic layers and mutate paint by layer/source-layer
role. This must be inspected against the actual live Streets v4 revision: patterned fills or
unrecognized roles may need targeted adjustment. Tests validate style syntax against an
explicit engineering fixture, not the inaccessible supplier style or actual cartographic output.

## Native geometry and effects

Real provider polygon source layers drive native `fill-extrusion` heights/bases. Custom
volumes replace the provider's existing extrusion display while keeping flat footprints and
context. Provider labels remain above volumes in style order. Illustrative ground fills are
inserted below building geometry; outlines/markers and selected object highlight support
inspection. No new city mesh, roof model or surveyed geometry is manufactured.

The implemented native light, vertical facade gradient, zoom-sensitive building color and
optional antialiasing provide inexpensive depth cues. Thin optional **ground-footprint** edges
emphasize outlines; they are not roof-edge illumination, bloom, reflections, shadows or true
ambient occlusion. These choices use supported layer/light properties.
[MapLibre layer specification](https://maplibre.org/maplibre-style-spec/layers/),
[native light specification](https://maplibre.org/maplibre-style-spec/light/).

Terrain, atmospheric fog/sky, AO shaders, reflections, custom WebGL, Three.js and deck.gl
were considered and deferred: no suitable terrain feed is verified, and another GPU pipeline
would add depth synchronization, memory and maintenance costs without proven analytical
benefit. A flat ground plane also does not constitute elevation accuracy. Native extrusion
rendering must still pass the actual multiangle visual test; a tilted flat map cannot pass.

## Analytical encodings

Continuous numeric index palette: green at 0, yellow at 35, orange at 65, red at 100. Missing
scores are grey. Colors communicate only a normalized synthetic metric, not risk, distress,
psychological state or danger. Values/coverage are exposed as text so interpretation does
not depend solely on hue. All polygons have low opacity (zone 0.06, node radius 0.08) and
dashed borders. They are explicitly illustrative, not measured influence or weather fields.

| Map scale | Display | Interpretation |
|---|---|---|
| Zoom <14 | Single aggregate demo-city marker plus all zone summaries in inspector | Available-node arithmetic mean, not measured entire-city state |
| Zoom 14–<16 | Three zone-centre markers and authored group disks | District names are fictional groupings; no administrative boundary claim |
| Zoom ≥16 | Five exact anchor markers and optional illustrative 18m disks | No claim of actual installed hardware or validated coverage |

The selected node outline appears only at close scale. Building selection uses transient
feature geometry, cyan display highlight and metadata with approximate position/height
provenance. A 2D footprint may also be inspected where the provider has a displayed fill.
Unknown attributes remain explicitly unavailable. The same visual engine serves all profiles.

## Camera and motion

Four retained geographic presets: city place node, northern waterfront, Piazza pedestrian
focus and Memed Abashidze Street. Initial view is waterfront. 3D presets use pitch 50° and
zoom ≤17; controls allow pitch 0–60°, bounded zoom 10–18, bearing, pan and north reset.
Native fly-to and orbit are stoppable; drag/zoom/rotation/pitch input interrupts scripted motion.
Guided sequence: city overview → waterfront demo district → monitoring zone → hypothetical
node → overview. District/group semantics remain synthetic throughout.

Inspection uses a conservative screen-space distance estimate informed by provided height,
with a larger fallback when unknown. This is **not** a terrain/building collision detector;
camera clearance requires manual validation against actual volumes and mobile aspect ratios.
No guarantee against intersecting an unseen building is claimed.

Reduced-motion preference disables orbit, makes camera moves immediate, removes CSS
animation and uses zero-duration native color/height transitions. Explicit timeline playback
remains available with discrete timestamp updates; it pauses on page hide. Orbit is capped
at 20/30 updates per second, not advertised as the renderer's FPS.

## Accessibility and visual QA pending

Semantic buttons/selects, keyboard focus indicators, skip-to-inspector link, status text,
SVG accessible description and numeric legends are implemented. Map canvas interaction,
screen reader usability, map-control reachability and contrast are not browser-tested.
Desktop 1440×900, mobile 390×844 and compact 320×700 must be checked for clipping,
touch usability, reading order and logo/attribution overlap in both themes/locales.
The current desktop controls favor compactness; a minimum 44px touch-target override is
applied on mobile. Partial translation needs review by a Georgian speaker.

See [manual acceptance and capture matrix](DIGITAL_TWIN_VALIDATION_REPORT.md).
