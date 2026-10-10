# Map rendering evidence — Stage 1B

Date: 2026-10-10 (Asia/Tbilisi). **PARTIAL. Actual screenshots captured by this agent: 0.**
No PNG/JPEG evidence exists for Stage 1B. No screenshots accompanied the attached request.
The user reports OpenFreeMap rendered successfully and rejects its current style; that is
qualitative feedback, not an agent-observed or independently captured rendering.

## Exact blockers and executed checks

Supported browser selection for `http://127.0.0.1:8765/` returned **`No browser is available`**.
After documented recovery, browser discovery returned **`[]`**. No controllable browser was
exposed through this session's supported connection. This does not establish whether a manually
opened browser on the user's machine works.

The [Browser skill](C:/Users/Lenovo/.codex/plugins/cache/openai-bundled/browser/26.623.101652/skills/control-in-app-browser/SKILL.md)
says: “Do not use external MCP browser-control tools, separate browser automation servers,
or other browser skills for this surface.” No standalone Playwright browser was substituted.
Node/HTTP checks are not image evidence.

Both new and legacy credential variables were absent in the agent's environment. The user
subsequently said they will configure both locally. That response is not evidence of successful
setup or provider requests; another terminal's environment is not inherited by this agent or
an already-running server. A/B styles, tiles, glyphs and attribution remain untested.

A server already listening on 127.0.0.1:8765 was neither interrupted nor reconfigured. The agent
checked the updated server on 8766 and stopped only that test instance afterward. HTTP routes,
rejected file paths/Host, syntax and contracts passed. See [HTTP receipt](../evidence/map-stage-1b/http-checks.json)
and [configuration checks](../evidence/map-stage-1b/configuration-checks.json).
At the final read-only check 8765 was no longer listening; the cause is unverified. No direct
stop/reconfiguration command for that server was issued. The exact launch below remains available.

| Provider | Agent actual render | Screenshot | Local visual evidence |
|---|---|---|---|
| A MapTiler Streets v4 | Unavailable: credentials + connected browser | None | Not assessed |
| B Mapbox Standard | Unavailable: credentials + connected browser | None | Not assessed |
| C OpenFreeMap Liberty | Unavailable: connected browser | None | User-reported render/style objections; no image retained |

The [rendering status](../evidence/map-stage-1b/rendering-status.json) contains zero captures.
SDK support alone is not geographic/visual validation.

## Reproducible manual capture

1. Follow [launcher and credential instructions](../../tools/map-stage-1/README.md), using
   port 8766. Open a canonical single-map URL:
   `http://127.0.0.1:8766/?provider=maptiler&style=streets-v4&preset=street&condition=2d&lang=en`.
   Replace provider/style together with `mapbox`/`standard` or `openfreemap`/`liberty`.
2. In Chrome/Chromium DevTools enable Device Mode, select Responsive and set **1440×900**,
   **390×844**, or **320×700**. For controlled pixel dimensions set DPR 1 and browser zoom 100%.
   Declare desktop/emulation; physical tests use native DPR separately. Keep browser version,
   network and CPU profile identical across matched comparisons.
3. Reload without touching the camera. Wait for **tiles + idle + fonts ready; errors 0**.
   Inspect roads/buildings, blank/flickering tiles, glyphs and readable uncropped attribution.
   Check DevTools failures; do not export raw HARs containing credentials. A 401/403 or visibly
   incomplete map is a failure even if some SDK events succeed.
4. Use **Export diagnostic JSON** immediately before capture. Confirm `renderReady=true`, actual
   camera equals requested camera, viewport matches the test and errors/context losses are zero.
   The fixed 84px diagnostic strip leaves map heights of 816, 760 and 616 CSS pixels respectively;
   export records both page and map dimensions.
5. Use DevTools command menu **Capture screenshot**, capturing the viewport with diagnostic strip
   and attribution. Do not use full-page, canvas-only or provider static-image substitutes.
   Verify PNG dimensions match the requested viewport at DPR 1. Preserve original pixels.
6. Save PNG and diagnostics together under the layout below. Add a separate capture record with
   actual ISO-8601 capture time, image path/SHA256, physical pixel dimensions, DPR, device class,
   browser/device/network, camera parity, failures and **human visual findings**. Export time is
   not capture time. Diagnostic JSON deliberately retains `screenshotCaptured=false`; the separate
   record certifies only an actual capture.
7. Repeat identical preset/condition/language/viewport for accessible providers. Mark blocked cells
   unavailable without substitution. Reload to reset cameras. Supply real PNGs, diagnostics and
   records for review; Stage 1B stays PARTIAL while waiting for them.

[Chrome Device Mode documentation](https://developer.chrome.com/docs/devtools/device-mode/).
Mobile viewport emulation is not an actual mobile-device benchmark.

## Capture organization and matrix

Intended layout, currently **no screenshot files**:

```text
artifacts/map-stage-1b/screenshots/
  <provider>/<preset>/<condition>/<lang>/<width>x<height>/
    <actual-UTC-time>.png
    <actual-UTC-time>.diagnostic.json
    <actual-UTC-time>.capture.json
```

Raw account data/keys/HARs do not belong here. Keep attribution-preserving internal QA images
within the permitted purpose; external sharing/export needs [plan/terms resolution](MAP_PROVIDER_COST_COMPARISON.md).
Screenshots cannot replace runtime maps or become training/tracing/analytical data. Reference
accepted actual artifacts in an additive manifest; never overwrite Stage 1 evidence or record
guessed filenames as completed captures.

Full matrix: **3 providers × 4 locations × 3 conditions × 2 languages (en/ka) × 3 viewports = 216
single-map cases**, with unsupported/blocked cases recorded. Add native-label captures to separate
provider composition from language adaptation. Start with street/2D/en for all providers at desktop
and mobile, then expand. Follow the [visual inspection matrix](MAP_VISUAL_COMPARISON.md).

Quick comparison:
`http://127.0.0.1:8766/?mode=compare&preset=waterfront&condition=2d&lang=en`.
At 1440×900 each iframe is 480×816 and its map 480×732; all candidates have equal dimensions.
The parent and each pane have an 84px strip. This differs from single-map captures. Interactions
are independent; reload to reset. Three concurrent WebGL contexts are not a single-map benchmark.
Comparison export includes each actual pane camera.

## Diagnostic definitions and limits

`window.mapStage1b.diagnostic()` exports sanitized metadata rather than provider features:
SDK/style ID, style-spec version/hash and unknown style revision, coordinate/preset provenance,
requested/current cameras, viewport/DPR, export time, events and observable aggregates.
Style spec 8 is a schema, not an immutable style release. Pins do not freeze remote styles/tiles.
Hash is a retrieval fingerprint and may vary across account-specific URLs. Mapbox hash covers
exposed style configuration, not an archive of Standard imports or tiles.

| Metric | Definition / practical limit | Actual session result |
|---|---|---|
| First meaningful map render | Human-visible useful map; not inferred from `load` | Not measured |
| `firstFullyLoadedFrameMs` | First render with style/tile predicates true, since map construction; event proxy | Browser not executed |
| `styleLoadMs`, `firstIdleMs` | Events since map construction; omit initial SDK/style fetch | Browser not executed |
| `stableVisibleTilesMs` | Load/hash + style/tile predicates + idle after source/camera change + fonts + 750ms quiet + no errors | Browser not executed |
| `startupToStableMs` | Stable gate from module startup; includes SDK/style initialization, not whole navigation | Browser not executed |
| Resource counts / transfer | Resource Timing; workers/cross-origin sizes can be missing; not billable counts | Not measured |
| Errors / WebGL loss | Sanitized SDK count/status and canvas event counts | Instrumented, unexecuted |
| Memory | Optional Chromium JS heap; excludes GPU/native/worker memory | Unavailable |
| Interaction responsiveness | Frame/input latency on controlled gesture trace | Not implemented/measured |
| Bundle footprint | Installed bytes / local gzip estimate | Measured below |

The stable gate is stricter than style-load; it still does not prove correct labels, complete
geography or height accuracy. Attribution layout/logo loads require inspection. Retain failures
after retries; reload for a clean capture rather than hiding error counts.

## Package footprint and pending mobile work

[Bundle receipt](../evidence/map-stage-1b/bundle-footprint.json) contains exact files/hashes.
MapLibre main+worker: **1,587,671 raw bytes**, estimated gzip **429,040 bytes**. Mapbox JS:
**1,897,230 raw bytes**, estimated gzip **516,487 bytes**. CSS separately: MapLibre 83,290 raw /
10,485 gzip bytes; Mapbox 48,946 raw / 5,750 gzip bytes. The loopback server sends **uncompressed**,
no-store resources. Tiles, fonts, sprites, textures and requests are additional. These are not
network, FPS, battery, GPU-memory or actual compressed-download results.

Physical Android Chrome, iOS Safari and Telegram Android/iOS/desktop remain pending. A later
operator-run Android USB test can use `adb reverse tcp:8766 tcp:8766` and the same phone loopback
URL, then `adb reverse --remove tcp:8766`. Retain native DPR/device details. No LAN/public bind
is needed. iOS/Telegram need a separately permitted local setup; none was enabled here.

Run five cold and five warm single-map loads under a documented network/CPU profile, followed
by the same 30-second pan/zoom trace. Record first useful map, stable tiles, failures, actual
requests/account totals, frame/input responsiveness, context loss, observable memory and
attribution/Georgian readability. Since local assets are no-store, describe warm provider/browser
caches and SDK re-fetches explicitly. Performance budgets require agreement; none has been achieved.
