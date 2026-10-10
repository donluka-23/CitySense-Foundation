# Digital Twin validation report

10 October 2026, Asia/Tbilisi. Repository: `D:\citysense-foundation` only.
**Status: PARTIAL — executable visual prototype delivered; genuine Batumi 3D/browser
acceptance incomplete.** Stage 2 backend/production remains unauthorized and has not started.
No visual approval, photorealism, full-building coverage, 60 FPS success or production readiness.

## Delivered implementation and evidence

New isolated `apps/digital-twin/` contains MapLibre 6.13.0 + MapTiler Streets v4 integration,
native provider-footprint extrusions with approximate height/base provenance, opt-in labeled
Illustrative Geometry, two runtime map/UI themes, building/node selection, camera controls/tour,
five fictional real-coordinate monitoring anchors, zoom-adaptive sources, deterministic timeline,
three configurable analytical templates, paired historical baselines, synthetic intervention
comparison, report export, quality presets, reduced motion, error/retry and diagnostics.
Five architecture layers remain separate from the protected backend.

Created documentation: [architecture](DIGITAL_TWIN_ARCHITECTURE.md),
[Batumi coverage](BATUMI_3D_DATA_COVERAGE.md), [visual system](DIGITAL_TWIN_VISUAL_SYSTEM.md),
[performance/rights/costs](DIGITAL_TWIN_PERFORMANCE.md), this report.
Complete created-file inventory/digests: [delivery manifest](../evidence/digital-twin/delivery-manifest.json).
**Existing files modified: none.** Generated npm modules, local logs and caches are excluded
from deliverable source inventory. `package-lock.json` pins the isolated dependency tree;
no existing package, backend dependency or provider-comparison source was changed.

Git metadata is absent; a Git clean/dirty/branch/commit claim is unavailable. Digest evidence
confirms all **203** pre-prototype files, all **176** retained original files and **22** Sprint 3
protected foundation files match their snapshots. Contract exports still match. Existing
Stage 1/1B reports, evidence, comparison harness, frozen engine and research protocol are
preserved. [Preservation receipt](../evidence/digital-twin/preservation.json).

## Actual verification status

16 Node tests pass: deterministic anchors/records, numeric normalization/missingness,
equal-node aggregation, paired baseline gaps, past-only observation timestamps, partial
metric coverage, bounded intervention comparison and all three report workflows; height
provenance/extrusion semantics use the **actual SDK expression evaluator**. Generated style
changes pass the SDK style validator across themes/quality/placeholder modes using an
explicit engineering fixture. That fixture is never served as a basemap and is not coverage.
7 Python host/config tests pass, including all assets, no-store/CSP, Host checks, `.env`/path/
backend-route refusal, public-key precedence/scope and rejection of obvious secret tokens.
Module syntax, Python lint/format, contract checks and isolated npm advisory audit pass.
[Verification](../evidence/digital-twin/verification.json),
[HTTP receipt](../evidence/digital-twin/http-checks.json),
[dependency audit](../evidence/digital-twin/dependency-audit.json).

| Requested browser demonstration | Implemented | Actually visually verified / blocker |
|---|---|---|
| 1. MapTiler map loads | Direct authenticated Streets v4 style/tile path | No: authorized key missing; no browser |
| 2. Genuine volumetric buildings | Native real-footprint extrusion with approximate heights; placeholders off by default | No: actual tile heights/visible multiangle volumes inaccessible |
| 3. Pitch and bearing | Native controls/sliders, bounded zoom/pitch | No browser execution |
| 4. Building selection | Displayed feature query, in-memory highlight, ID/position/height/provenance | Actual feature support/selection unverified |
| 5. Two visual themes | Runtime source-preserving paint and UI themes; style syntax checked | Actual readability/style-revision compatibility unverified |
| 6. Five monitoring nodes | Exact retained public OSM anchors; all nodes fictional | Geographic data tests pass; visible markers unverified |
| 7. Dynamic overlays | Numeric index colors, low-opacity illustrative disks, null grey | Data/style tests pass; actual color transitions unverified |
| 8. Timeline | 13 deterministic frames, play/pause/time/speed/reset; source updates bounded | Data/source-mutation tests pass; interactive playback unverified |
| 9. Zoom-dependent views | City aggregate, zone groups, close nodes | Layer ranges validated; observed zoom transitions unverified |
| 10. Camera motion | Fly-to, orbit, guided hierarchy, north/reset, reduced motion | Input interruption/clearance require actual browser |
| 11. No unexpected errors | Sanitized error tracking, missing-key notice, retry/context-loss path | Browser console/GPU/resource result unavailable |
| 12. Attribution visible | Expanded native source attribution + MapTiler logo control | Implementation present; actual logo/text/overlap unverified |

The six-step operational workflow is verified at the **pure synthetic report/data layer**.
It has not been demonstrated end to end through a browser. Scientific validation: **none**.
Commercial validation: **none**. Customer demand, willingness to pay, measured stress, sales,
cost savings, real environmental conditions, reliable sensor coverage and causal outcomes
are not established. Missing/degraded fixture readings and unknown uncertainty remain explicit.

## Browser blockers and screenshots

Supported browser discovery returned `[]`; opening the local URL returned exactly
**`No browser is available`**. The launch's `/config.json` shows only `publicKeyPresent: false`
in recorded evidence; no key value is saved. There was no authorized authenticated provider
request, actual map/GPU/browser interaction or screenshot. **Actual screenshot paths: none.**
[Rendering status receipt](../evidence/digital-twin/rendering-status.json).

Applied skill: [control-in-app-browser SKILL.md](C:/Users/Lenovo/.codex/plugins/cache/openai-bundled/browser/26.623.101652/skills/control-in-app-browser/SKILL.md).
Its explicit instruction is: “Do not use external MCP browser-control tools, separate browser
automation servers, or other browser skills for this surface.” Browser discovery/recovery was
attempted through the supported connection. The user's current prompt also explicitly prohibits
starting prohibited automation servers and authorizes manual verification steps if browser
control is unavailable. No alternative automation server, borrowed credential or generated
map evidence was used. No additional permission is being requested.

## Exact local launch

Local host was started and checked at **http://127.0.0.1:8770/**; HTTP 200 verifies asset
reachability only. It is loopback-only, with no public deployment, API/backend connection or PWA
offline functionality. If the current instance is still running, Ctrl+C in its terminal stops it.

```powershell
Set-Location D:\citysense-foundation\apps\digital-twin
npm.cmd ci --ignore-scripts
$env:MAPTILER_API_KEY = 'YOUR_AUTHORIZED_PUBLIC_BROWSER_KEY'
python serve.py
```

Requires Node/npm, Python 3.12+ and an authorized browser key. Alternatively fill
`apps/digital-twin/.env` from its blank example. No root secret configuration is loaded.
Changing the process key requires server restart; app-local file changes support Retry map.
No Mapbox key is needed. Read [complete launch and checks](../../apps/digital-twin/README.md).

## Manual verification and exact evidence requirements

1. Launch with an authorized key, open the URL in a WebGL2-capable browser and inspect the
   console/network. Verify style, tiles, glyphs, sprites and logo; stop on any auth/quota/CORS/
   WebGL error. Wait for idle/visible-tile/font readiness and inspect real content. Readiness
   events alone cannot prove a correct view or label language.
2. At **1440×900**, choose central and waterfront, Balanced quality, pitch 50°, placeholders
   **off**. In each theme capture the same genuine visible volumes at bearings **0° and 90°**.
   Verify sidewalls/base/roofs and actual viewpoint change; flat tilted footprints fail. Also
   inspect overview/street, pan/zoom, reset/north and 2D switch. Verify building selection/ID
   gaps/height source and camera clearance; do not present provider approximation as survey.
3. Click five nodes at close zoom or select their zone/node controls. Check coordinates,
   synthetic labels, source/status/latest timestamp and numeric index. Zoom through 13, 15,
   17: city/zone/node representations must change without duplicate semantic markers.
   Footprints must remain dashed/illustrative and not obscure buildings.
4. Complete a reproducible workflow: public-space profile → waterfront zone → **11:00** →
   SIM-01 → occupancy **70 count**, baseline **26.5 count**, rise about **164.2%** → review a
   listed hypothetical action → Generate demo report. Confirm six workflow steps, source,
   unknown uncertainty, timestamp, current/baseline/coverage and synthetic/unvalidated flags;
   no provider geometry/key or enacted action. Repeat with the other profiles. This expectation
   is fixture-derived, not a real measured event or economic finding.
5. Play/pause, change 1×/2×/4× speed, scrub/reset. At 10:00/10:30, street SIM-05 stays offline
   with null score and past latest-reading time; no stale value fills a gap. At 12:00+, SIM-02
   research PM2.5 is missing/degraded. Waterfront intervention after-period must not appear
   before 13:00 and must never claim causality.
6. Toggle nodes/footprints; both themes; Performance/Balanced/High; partial EN/KA labels.
   Enable Illustrative Geometry only in a separate capture and verify its persistent banner,
   placeholder provenance and unchanged positive provider heights. It cannot pass the real
   height-coverage test. Confirm attribution/logo remain visible in every state.
7. Repeat at **390×844** and **320×700** portrait: inspect clipping, touch targets, controls,
   timeline, scroll, inspector, legend, logo/attribution and Georgian script. Record device
   emulation separately from actual physical mobile/Telegram WebView tests, still outstanding.
8. Enable reduced motion, hide/resume the tab, stop/touch-interrupt the camera tour, test
   missing/invalid key and retry/context-loss recovery. Record actual errors and performance
   using the [measurement plan](DIGITAL_TWIN_PERFORMANCE.md), not assumed timings.

Future **actual** PNG captures belong in ignored `artifacts/digital-twin/screenshots/`:

```text
desktop-{central|waterfront}-{twin|daylight}-3d-b{0|90}-provider.png
desktop-central-daylight-2d.png
desktop-overview-twin.png
desktop-street-twin-selected-node.png
desktop-waterfront-twin-selected-building.png
desktop-waterfront-twin-workflow-1100.png
desktop-central-twin-illustrative-explicit.png
mobile-390-twin-workflow.png
compact-320-daylight-attribution.png
```

These are **required future names, not existing evidence**. Save adjacent metadata with actual
UTC/local time, screenshot path/hash, viewport/DPR/rendering DPR, browser/device and physical
vs emulated classification, preset/camera, theme/quality/simulation timestamp, placeholder
state, style hash, visible attribution and honest readiness/error/coverage results. Do not
capture/export provider network URLs containing keys. Screenshots require the account's
permitted internal QA use; no publication or redistribution is authorized here.

## Remaining risks and next step

Actual style/source revision, hosted height coverage/accuracy, label language, camera
clearance, multi-source duplicate volumes, UI legibility, physical mobile/WebView usability,
browser error recovery and frame/memory performance remain unverified. Source/style
pattern matching may need revision after actual provider rendering. This is a local visual
prototype, not the final product frontend or deployable/offline PWA.
Supplier access/quotas/attribution and request-based cost exposure remain material; full
[rights/cost assessment](DIGITAL_TWIN_PERFORMANCE.md#provider-usage-and-operational-costs)
is documented, with no plan purchase or permanent provider-data extraction.

**Exact next step:** configure the authorized MapTiler public key locally and run the above
multiangle/operational/mobile acceptance matrix in an available browser; record actual captures
and diagnostics, then correct demonstrated rendering/usability defects within this prototype.
Only after visual acceptance and further explicit authorization should future Stage 2 work
specify bounded licensed observation/opportunity/suitability/route adapters, validate source
quality and publication/access contracts, and integrate them without changing the frozen
engine/protocol. No Stage 2 implementation has begun.
