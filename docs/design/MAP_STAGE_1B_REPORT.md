# CitySense map infrastructure — Stage 1B report

Date: **2026-10-10, Asia/Tbilisi**. Workspace: `D:\citysense-foundation` only.
**Status: PARTIAL. Comparison tooling delivered; actual provider visual validation incomplete.**
**Stage 2 has not started and is not authorized.** No production frontend, public deployment,
provider purchase, visual approval, surveyed 3D or mobile performance success is claimed.

## Implemented work

Extended the existing `tools/map-stage-1` diagnostic with official SDKs and supplier styles:
A MapLibre 6.13.0 + MapTiler Streets v4; B Mapbox GL JS 3.32.0 + Standard;
C MapLibre + existing OpenFreeMap Liberty. No dependencies were added or upgraded.
New configuration reads **MAPTILER_API_KEY** and **MAPBOX_PUBLIC_ACCESS_TOKEN** from the
server terminal; legacy names remain aliases. Mapbox secret tokens are rejected before
configuration is sent to the browser. Missing credentials/resource failures visibly block
the selected provider with no substitution. No key is stored in source or diagnostics.

Added deterministic provider/style/preset/condition/language/camera URL configuration,
three equal side-by-side panes and single-map mode. Styles are restricted to the three official
comparison styles; arbitrary/mislabeled combinations are rejected. Canonical cameras use
Mercator and verified coordinates. Optional coordinates are validated and labeled unverified
user overrides. Historical `view` URLs retain their old centers and are explicitly outside
the verified Stage 1B preset set. Independent camera interactions require reload before comparison.

Added JSON export of camera/viewport/DPR/version/hash, language adaptation, provider extrusion
inventory, load/idle/stable-tile proxies, observable resource/memory aggregates and sanitized
errors/context loss. A stable gate requires more than style load and never certifies content
correctness or a screenshot. No CitySense API, private geometry, weather, scores, routes,
availability, synthetic data, geolocation or service worker was connected.

The flat and moderate-pitch conditions disable provider extrusions; the 3D condition retains
only provider-supplied content and original style limits or Standard configuration. No geometry
or heights are invented. A supplied style with no 3D layer is reported unavailable. Original
attribution and logos remain; actual narrow-screen placement needs visual inspection.

## Repository and contract audit

Re-read current Sprint 3 report, architecture, OpenAPI, registry/security documentation,
actual map test and retained Stage 1 receipts. Checked executable platform publication/caller-
walking semantics and generated contracts. Source of truth remains the supplied workspace,
not past chat or the unrelated demo, which was not searched for or reused.

Foundation remains FastAPI/PostGIS modular monolith, immutable evidence and frozen unvalidated
suitability/research contracts. City reads are bounded point geometry; sparse/null assessments,
rights and timestamps are material map semantics. Opportunity Registry is contracts only;
routing, isochrones, weather tiles and operational partner availability are absent. Operator
credentials/publication restrictions/CORS/user identity remain unresolved for a future browser
product. A basemap POI cannot become a verified opportunity or a published research point.

No AGENTS.md or `.git` entry exists in this workspace. Git status is unavailable; no branch,
commit/diff or hosted CI is claimed. Before/after hash checks cover 182 existing non-generated
files: 178 unchanged, four intentionally modified map-test files (`README.md`, `index.html`,
`map.mjs`, `serve.py`). All **176 files preserved by Stage 1** and all protected Sprint 3 digests
still match. Historical Stage 1 design/evidence files are unchanged. Its old tool-delivery hashes
describe the historical version; intentional Stage 1B changes have their own receipt.
[Preservation evidence](../evidence/map-stage-1b/preservation.json).

## Actual Batumi evidence and visual findings

One fresh bounded OSM skeleton-coordinate query succeeded; provider database
**2026-10-09T21:21:06Z**, retrieved **2026-10-09T21:22:19.243Z** (October 10 locally).
The [receipt](../evidence/map-stage-1b/camera-receipt.json) retains query/response hashes.
It contains no contributor/contact records and is independent of the private research inventory.
A second bounded name-only query verified the four source names, including the exact English
name **Memed Abashidze Street**. Its [receipt](../evidence/map-stage-1b/camera-labels-receipt.json)
and Georgian/English projected labels are retained. Source-language names are not rendered labels.

| Canonical location | Exact longitude, latitude | Actual source point |
|---|---|---|
| City overview | 41.6360085, 41.6509502 | Batumi node 160257516 |
| Northern Boulevard/waterfront | 41.6395066, 41.6560289 | Alphabet Tower way 405852444, vertex node 4080074547 |
| Central neighborhood | 41.6407375, 41.649547 | Piazza way 294880812, vertex node 2985014410 |
| Street detail | 41.6349322, 41.6500931 | Memed Abashidze Street way 1152779731, vertex node 409475078 |

These are exact recorded source points, not invented centroids, surveyed positions or verified
entrances. Zoom/pitch/bearing are authored comparison settings in [MAP_CAMERA_PRESETS.json](MAP_CAMERA_PRESETS.json).
Four cameras do not audit all Batumi or guarantee every district fits a mobile viewport.

Stage 1's retained OSM counts show substantial roads/pedestrian/building presence and sparse
explicit heights. They do not prove hosted-provider content. See its unchanged
[coverage audit](BATUMI_MAP_COVERAGE_AUDIT.md). Current English/Georgian visual labels, glyphs,
collision behavior, park/coast detail and provider-specific heights remain unverified.

The user reports OpenFreeMap loads but finds its building detail/hierarchy, spatial depth,
sparsity and urban differentiation unacceptable. This is feedback about the tested presentation,
not evidence against MapLibre or for paid-provider superiority. No screenshot accompanied the
attachment. The [visual matrix](MAP_VISUAL_COMPARISON.md) separates that report from unassessed
criteria; it assigns no fabricated provider ratings.

## Genuinely rendered providers and screenshots

**Agent-rendered providers: none. Actual screenshot files/paths: none.** Supported browser
selection returned `No browser is available`; recovery discovery returned `[]`. No standalone
browser substitute or simulated map was used. The user-reported C rendering remains distinct.

Agent credential variables were empty, including legacy aliases; the user will configure both
locally. That intention does not establish setup or successful A/B access. The credential-free
reference also cannot be captured without a connected browser. Style/HTTP checks are not renders.
[Rendering status](../evidence/map-stage-1b/rendering-status.json).

Manual instructions, dimensions (1440×900, 390×844, 320×700), metadata, readiness limits and
the intended `artifacts/map-stage-1b/screenshots/` hierarchy are in
[MAP_RENDERING_EVIDENCE.md](MAP_RENDERING_EVIDENCE.md). That directory name describes future
captures, not delivered images. Stage 1B waits for real browser screenshots and diagnostics.

## Mobile/performance and technical QA results

No actual desktop rendering latency, first meaningful render, gesture/FPS, WebGL memory,
physical-mobile or Telegram WebView result is available. Instrumentation is implemented but
unexecuted in a browser. Observable Resource Timing is incomplete and not account billing.
Exact installed bundle bytes/gzip estimates were measured; they cannot select a mobile winner.
See [bundle receipt](../evidence/map-stage-1b/bundle-footprint.json) and rendering evidence.

| Completed engineering check | Result / scope |
|---|---|
| JavaScript syntax | `map.mjs`, `comparison.mjs` passed `node --check` |
| Python server | Executed; Ruff lint and format pass |
| Canonical configuration | All 108 provider/preset/condition/language combinations passed |
| Invalid configuration | 15 invalid style/coordinate/camera/language/mode cases rejected |
| Source coordinate parity | All four centers exactly match retained OSM source point/vertex |
| HTTP | Eleven allowed routes 200/no-store; three restricted paths 404; untrusted Host 403 |
| Credential handling | Invalid secret-token sentinel omitted; explicit empty new variable overrides legacy alias; no provider calls |
| Contract exporter | `Contract exports match` |
| Preservation | Backend/protocol/Stage 1 evidence parity confirmed; only four intended existing-tool changes |
| Browser/mobile | Unavailable, not passed |

No backend regression suite was rerun: no backend/contract/dependency changes, with parity and
export verification used. Sprint 3's 179-test result is historical, not a new map-stage execution.
No dependencies added; Stage 1's audit is not rebranded as a new vulnerability scan.
[Verification receipt](../evidence/map-stage-1b/verification.json).
No direct stop/reconfigure command was issued for the initially existing server on 8765.
It was no longer listening at the final read-only check; the cause is unverified. Agent HTTP
checks used 8766 and that temporary instance was stopped. No public listener/deployment was created.

## Licensing, cost and provisional recommendation

[MAP_PROVIDER_COST_COMPARISON.md](MAP_PROVIDER_COST_COMPARISON.md) records current official
units, commercial/attribution/token/cache/offline/export restrictions, support entitlement and
explicit MAU sensitivities. Plain MapLibre/MapTiler is request-metered; this is not SDK session
pricing. Mapbox's GL JS web-load model can be cheaper under the modeled usage assumptions;
actual tile requests remain unknown. Neither renderer's license clears environmental/route
or commercial provider-derived analytical data. Public image sharing/export needs account-
specific terms resolution. OpenFreeMap offers no production SLA.

Retain **MapLibre + MapTiler Streets v4 as the provisional primary engineering candidate**
for controllable custom layers, a separable supplier and maintainability. **Confidence: moderate
in architecture fit, low in actual Batumi visual/mobile fitness.** Its compatible stack is identified
in [official MapTiler documentation](https://docs.maptiler.com/maplibre/); this does not prove
local quality or low total cost. **Fallback/conditional alternative: Mapbox GL JS + Standard**,
pending local evidence and acceptance of its supplier coupling/ordering/rights. No runtime
failover is enabled. Current OpenFreeMap Liberty remains the reference; it lacks user visual
acceptance. Choose neither provider solely for richer 3D. Final visual/provider approval is pending.

## Exact local launch

In the terminal with your authorized public browser credentials:

```powershell
Set-Location D:\citysense-foundation\tools\map-stage-1
npm.cmd ci --ignore-scripts
$env:MAPTILER_API_KEY = 'YOUR_AUTHORIZED_BROWSER_KEY'
$env:MAPBOX_PUBLIC_ACCESS_TOKEN = 'pk.YOUR_AUTHORIZED_PUBLIC_TOKEN'
$env:MAP_STAGE1_PORT = '8766'
python serve.py
```

Replace credential placeholders locally; do not send or commit keys. Omit assignment lines
if these variables already exist in that terminal. Port 8766 avoids the older server on 8765;
the configurable default is still 8765. Ctrl+C stops the newly started server. It binds loopback
only, reads no `.env` and serves only allowlisted test assets/config/presets.

Open **http://127.0.0.1:8766/?mode=compare&preset=waterfront&condition=2d&lang=en**.
For real capture/mobile checks use single mode, for example
`http://127.0.0.1:8766/?provider=maptiler&style=streets-v4&preset=street&condition=2d&lang=ka`.
Use `mapbox`/`standard` or `openfreemap`/`liberty` for other candidates; presets
`overview|waterfront|central|street`, conditions `2d|detail|3d`, languages `native|en|ka`.
[Full configuration README](../../tools/map-stage-1/README.md).

## Deliverables and remaining gate

All six requested files are present:

- [MAP_STAGE_1B_REPORT.md](MAP_STAGE_1B_REPORT.md): outcomes, limitations and launch.
- [MAP_VISUAL_COMPARISON.md](MAP_VISUAL_COMPARISON.md): criteria, capabilities, honest evidence status.
- [MAP_CAMERA_PRESETS.json](MAP_CAMERA_PRESETS.json): verified centers and complete camera settings.
- [MAP_RENDERING_EVIDENCE.md](MAP_RENDERING_EVIDENCE.md): capture protocol, instrumentation and pending mobile tests.
- [MAP_PROVIDER_COST_COMPARISON.md](MAP_PROVIDER_COST_COMPARISON.md): commercial constraints and MAU sensitivities.
- [MAP_STAGE_2_READINESS.md](MAP_STAGE_2_READINESS.md): NOT READY, explicit exit gates and plan only.

Remaining blockers: connected browser/actual captures, locally configured provider access,
measured bilingual coverage and building/3D behavior, physical mobile/Telegram tests, eligible
account/rights/budget/support decisions and final user visual approval. Stage 2 plan is documented
but **implementation is not authorized**. Complete outstanding Stage 1B evidence, review the
decision with the user, and obtain explicit Stage 2 approval before any product implementation.
