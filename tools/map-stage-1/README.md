# Stage 1B Batumi basemap comparison

Isolated mapping diagnostic. No CitySense application UI, data adapters, service worker,
API/operator keys, geolocation, scores, weather, routes or supplier availability.
Stage 2 requires explicit user approval. Stage 1's historical documents and evidence remain intact.

## Launch (PowerShell)

Node/npm and Python 3.12 are required. Pinned renderers: MapLibre GL JS 6.13.0 and
Mapbox GL JS 3.32.0. Internet access and WebGL2 are required for real maps.
Configure **your own authorized public browser credentials** in the same terminal:

```powershell
Set-Location D:\citysense-foundation\tools\map-stage-1
npm.cmd ci --ignore-scripts
$env:MAPTILER_API_KEY = 'YOUR_AUTHORIZED_BROWSER_KEY'
$env:MAPBOX_PUBLIC_ACCESS_TOKEN = 'pk.YOUR_AUTHORIZED_PUBLIC_TOKEN'
$env:MAP_STAGE1_PORT = '8766'
python serve.py
```

Port 8766 avoids the existing user's Stage 1 server on 8765. The default remains 8765
when `MAP_STAGE1_PORT` is unset. Stop only the server you started with Ctrl+C.
Restart an older server to use the new routes/configuration. Environment variables set in
another terminal are not inherited by an already-running server. The server reads no `.env`.
Legacy `MAP_STAGE1_MAPTILER_PUBLIC_KEY` / `MAP_STAGE1_MAPBOX_PUBLIC_TOKEN` remain aliases;
new names take precedence, including an explicitly empty value. Mapbox secret tokens are
filtered before sending configuration. The MapTiler variable must contain a browser API key,
not an account management credential. Keys are visible to the browser but never saved in exports.

No credentials are necessary for OpenFreeMap. Missing credentials visibly block the requested
provider. A blocked tile/style fetch is never replaced with another provider's map.
Provider calls can use your account quota; comparison mode initializes all three maps.

## Deterministic URLs

Three equally sized side-by-side panes:

`http://127.0.0.1:8766/?mode=compare&preset=waterfront&condition=2d&lang=en`

Single-map captures / performance:

- A: `http://127.0.0.1:8766/?provider=maptiler&style=streets-v4&preset=street&condition=2d&lang=en`
- B: `http://127.0.0.1:8766/?provider=mapbox&style=standard&preset=street&condition=2d&lang=en`
- C: `http://127.0.0.1:8766/?provider=openfreemap&style=liberty&preset=street&condition=2d&lang=en`

| Parameter | Supported configuration |
|---|---|
| `provider` | `maptiler`, `mapbox`, `openfreemap` (default) |
| `style` | Exact selected-provider style: `streets-v4`, `standard`, `liberty`; mismatches rejected |
| `preset` | `overview` (default), `waterfront`, `central`, `street` |
| `condition` | `2d` (default), `detail`, `3d` |
| `lang` | `native` (default, preserves provider label expressions), `en`, `ka` |
| `mode` | `single` (default), `compare` (3 concurrent maps) |
| `center` | Optional `longitude,latitude`; validated finite Mercator bounds; marked unverified URL override |
| `zoom`, `pitch`, `bearing` | Optional numeric overrides: 0–22, 0–60°, −180–180°; clean 2D requires pitch/bearing 0 |

Canonical coordinates and authored camera settings are loaded from
[MAP_CAMERA_PRESETS.json](../../docs/design/MAP_CAMERA_PRESETS.json). Each canonical center
is an actual OSM node/geometry vertex, not an invented centroid or surveyed entrance.
Legacy `view=overview|oldtown|waterfront|park|south|botanical` retains historical Stage 1
centers and is marked unverified for Stage 1B. Do not mix `view` with `preset` in comparisons.
Legacy `provider3d=1` selects the 3D condition when `condition` is absent.

All canonical cameras are Mercator, north-up. 2D uses pitch 0; detail 35; 3D 60.
The two flat-building conditions suppress existing MapLibre extrusion layers and Standard's
3D objects. 3D retains only provider-supplied layers/configuration and their original visibility,
filters and zoom limits. No height, geometry, tree or landmark model is generated or added.
MapTiler may supply no extrusion layer in Streets v4: then report it unavailable.

Requested MapLibre label languages rewrite only recognized name-bearing layer expressions
using existing fields and documented fallback; modified IDs are exported. This is a test adaptation
of an official style, not untouched cartography. No translation is generated. `lang=native`
preserves the provider's label composition. Mapbox uses its documented language option.

Each pane starts at the same camera. Manual interactions are independent; reload to reset
before comparison. There is no camera synchronization or performance interpretation across
three simultaneous WebGL contexts. Use single mode at 1440×900, 390×844 and 320×700.
A fixed 84px diagnostic strip leaves map dimensions height−84; export records both dimensions.
Comparison adds a parent strip and each iframe's strip; all three pane sizes are equal.

## Actual screenshots and diagnostics

See [MAP_RENDERING_EVIDENCE.md](../../docs/design/MAP_RENDERING_EVIDENCE.md) for exact manual
capture instructions, naming and evidence fields. This session has no connected browser and
has captured no images. User-reported OpenFreeMap rendering is separate from agent captures.

`window.mapStage1b.diagnostic()` / **Export diagnostic JSON** provide current camera,
SDK version, style-spec version/hash, preset hash, viewport/DPR, event-based timings,
aggregate resource counts, heap visibility and sanitized error counts. Comparison export
includes all three pane diagnostics. No raw source features, tile URLs, credentials or logs
are exported; vendor accounting is unmodified. Diagnostic JSON does not claim a screenshot.

Wait for `tiles + idle + fonts ready`, then visually inspect the map and attribution.
Readiness requires load + style/tile predicates + idle after the last change + fonts + 750ms
quiet + no errors. It is an instrumentation gate, not proof of complete geographic content,
correct labels or permission to redistribute screenshots. Resource Timing can omit worker
requests and cross-origin bytes; counts are not billing estimates. Heap data excludes GPU
and worker memory. Actual mobile hardware and Telegram WebViews remain untested.

## Existing source coverage audit

The unchanged `audit-coverage.mjs` still supports the optional Stage 1 OSM aggregate audit:

```powershell
node audit-coverage.mjs ..\..\artifacts\map-stage-1\new-osm-audit
```

This manually bounded live Overpass request is not a product backend. Existing directories
are rejected. Preserve the [public usage policy](https://dev.overpass-api.de/overpass-doc/en/preface/commons.html).
Hosted map coverage is not inferred from its source counts.

## Credentials and attribution

Use separate development keys, least-privilege public scopes and account limits.
For MapTiler local origin rules, enter `127.0.0.1` (or `localhost` if that is the actual origin)
without scheme/port, per its [API-key guide](https://docs.maptiler.com/guides/credentials/api-key/).
Localhost rules match other computers too; do not leave them on a production key.
Use Mapbox's [URL restrictions](https://docs.mapbox.com/help/dive-deeper/access-tokens/)
for the exact intended local origin. No keys in URL parameters, source, screenshots or chat.

Expanded provider attribution, Mapbox logo and official MapTiler logo are retained.
Inspect narrow-screen overlap/cropping before accepting evidence. No tile proxy/cache/export
service is implemented. Review [rights and cost comparison](../../docs/design/MAP_PROVIDER_COST_COMPARISON.md)
for commercial plan, evidence-image sharing, caching and service-level conditions.
