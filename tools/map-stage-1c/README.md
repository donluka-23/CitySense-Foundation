# Stage 1C isolated navigation experiment

Status: implemented for technical testing; **visual acceptance and commit authorization pending**.
This is one standalone map, with no CitySense backend or Digital Twin functionality.

## Run locally

From PowerShell in `D:\citysense-foundation`:

```powershell
$env:MAPTILER_API_KEY = 'YOUR_AUTHORIZED_PUBLIC_BROWSER_KEY'
$env:MAP_STAGE1C_PORT = '8767'
python -B tools/map-stage-1c/serve.py
```

Open **http://127.0.0.1:8767/**. Stop with Ctrl+C. Use a free port if another process is listening.
Set your own key in that terminal; another terminal's environment is not inherited. Never commit
the key or paste it into diagnostic notes. The host reads no `.env` file. An explicit empty
`MAPTILER_API_KEY` overrides the legacy `MAP_STAGE1_MAPTILER_PUBLIC_KEY` alias.

Requires Python 3.12+, a WebGL2 browser and the **existing** MapLibre 6.13.0 installation in
`tools/map-stage-1/node_modules/`. No installation, CDN SDK, provider substitution, tile proxy,
service worker, database connection or public/LAN binding is provided. Missing SDK or keys
block rendering explicitly. The SDK's shared-module file in this installation is a zero-byte
placeholder; HTTP verification compares served bytes to the existing files.

## Compare configurations

| Setting | Behavior | Interpretation |
|---|---|---|
| Immediate | Native `jumpTo` | Baseline for explicit camera changes |
| Native transition | Native `easeTo`, initial candidate 400 ms | Change Candidate ms to compare 150/250/400/600; no duration is accepted yet |
| Native dragging | Default drag response and release inertia | Independent of the explicit-camera transition selection |
| Wheel/trackpad | Default pointer-anchored native zoom | Test physical wheel and trackpad separately |
| Rotation/pitch | Right-button or Ctrl drag; native zoom/compass control | Default pitch range 0–60°, roll disabled by upstream default |
| Provider 3D | Original supplied extrusion layers/visibility restored, or hidden | No added buildings, height expressions or style effects |

Four canonical presets and all three conditions are read from the unchanged Stage 1B JSON.
Native labels remain intact. Mercator matches the canonical geography. No additional camera
bounds, zoom/pitch restrictions, sensitivity changes, orbit, tour, artificial camera loop or
custom input handler is introduced. Reduced-motion preference makes explicit transitions immediate.

Example matched building-load pair:

```text
http://127.0.0.1:8767/?preset=central&condition=3d&buildings=on&motion=short&duration=400&dpr=1
http://127.0.0.1:8767/?preset=central&condition=3d&buildings=off&motion=short&duration=400&dpr=1
```

The on/off pair keeps identical center, zoom, pitch, bearing and DPR. Comparing the canonical
2D camera directly with the canonical 3D camera also changes zoom/pitch and therefore cannot
isolate extrusion cost. `buildings=on` preserves original minzoom, filters, height expressions
and supplied visibility. A supplied layer can still be hidden or have no local buildings;
actual Batumi volumes require inspection. No extrusion layer means 3D validation is unavailable.

URL options: `preset=overview|waterfront|central|street`, `condition=2d|detail|3d`,
`motion=immediate|short`, `duration=<nonnegative milliseconds>`, `buildings=on|off`,
optional `dpr=<positive number>`. Without `dpr`, native device DPR is retained. Apply camera
uses the selected settings and resets to the canonical camera; dragging itself remains native.

## Record interaction evidence

1. Record the physical machine/GPU, browser/version, display refresh, browser zoom, power state,
   viewport and any throttling separately. Use a physical desktop, 60 Hz display, browser zoom
   100% and `dpr=1` for the initial reference. Adjust page height to obtain the intended actual
   map viewport of 1440×900; toolbar size is not included in map dimensions. Record actual sizes.
2. Check style, tiles, glyphs, buildings and visible source attribution/MapTiler logo. Stop on
   auth/quota/CORS/WebGL errors. Error counts are cumulative; fix the failure and reload for a
   clean session. No missing-content fallback is used.
3. Apply settings. Warm the intended gesture path, return to its preset, and wait until complete
   tiles, fonts and idle have been quiet for 750 ms. Readiness is a software predicate, not visual
   completeness. Recording refuses to start before it or while the page is hidden/unfocused.
4. In the console declare the conditions, then return focus to the page:

   ```javascript
   window.stage1c.setTestConditions({
     deviceClass: 'physical-desktop', inputDevice: 'mouse', cacheState: 'warm',
     networkProfile: 'unthrottled', powerMode: 'normal', displayHz: 60,
     purpose: 'gestures'
   });
   window.stage1c.diagnostic();
   ```

5. Set Repetition 1 and click **Record 30s**. Follow the same manual sequence each time:
   0–7 s horizontal and vertical drags with releases; 7–14 s wheel zoom in/out at one fixed pointer
   position; 14–22 s right-button/Ctrl rotation and pitch; 22–27 s return movement; finish with
   at least two seconds of a stationary endpoint. Timing is an operator protocol, not automatic
   camera movement. Repeat five times per preset/condition. Test trackpad runs separately.
6. For explicit transitions, set purpose to `transition`, choose Immediate or a candidate duration,
   move away from the chosen camera, start recording, then click Apply camera. Repeat uninterrupted
   and user-interrupted changes. Return movement/Apply is recorded as a command; input sampling
   remains separate. Keep preset, building state and transition configuration fixed within a run.
7. Compare each 3D condition with a matched buildings-off run. Save exports after recording stops;
   exporting during a run serializes an unfinished snapshot and can itself perturb timing. Export
   saves `stage-1c-navigation.json`; rename it by configuration/repetition under ignored
   `.local/map-stage-1c/`. It contains no key, provider URLs or archived provider geometry.
8. Collect a separate browser performance trace with the same sequence to examine main-thread work
   and frame presentation. Keep instrumented and uninstrumented trials separate to estimate probe
   overhead. Redact credential-bearing URLs before retaining/sharing traces; never commit raw HARs.
9. Write your own navigation-quality observations separately, referencing run IDs. Machine output
   leaves `userAssessment` null and `visualAcceptance` pending. Automated tests do not approve feel.

The console also supports `startRun({ repetition: 2, purpose: 'transition' })` and `finishRun()`.
Stopping early is flagged. Recording length is bounded to 1–120 seconds to contain diagnostic
memory/timer lifetime; this does not restrict navigation. Unknown device class invalidates reference
comparison. Unknown cache/input conditions warn rather than invent a physical-device classification.

## Metric definitions and provisional budgets

| Observation | Definition / candidate acceptance |
|---|---|
| Input-to-camera-render proxy | Input timestamp to first changed-camera render following an originalEvent-matched native move; p95 ≤50 ms, p99 ≤100 ms |
| Gesture onset proxy | First captured input of a sequence to its first matched render; helps expose latency hidden by coalescing |
| Input listener delay | Listener entry minus normalized browser event timestamp; not hardware/OS delay or exact event-dispatch start |
| Active render intervals | Map render callbacks during movement, excluding idle gaps between gestures; p95 ≤33.4 ms, p99 ≤50 ms, no unexplained gap >100 ms |
| Wheel settling/anchor | Flat-ground wheel endpoint; settle ≤350 ms after last wheel listener, drift ≤2 CSS pixels at a fixed pointer |
| Endpoint stability | Camera difference over an uninterrupted two-second window: center ≤1 CSS pixel, zoom/bearing/pitch ≤0.001 |
| Explicit transition | 400 ms candidate completes ≤650 ms; endpoint center ≤1 CSS pixel, zoom ≤0.001, bearing/pitch ≤0.1° |
| Rendering health | Zero resource/script/render errors and context losses; actual completeness/attribution inspected manually |
| Repeatability | All five valid repetitions per configuration/preset meet proposed budgets; inspect individual runs, not only pooled percentiles |

Proxy timing is **not measured visual latency**. Render callbacks/RAF scheduling are **not GPU FPS**.
Only input objects matched through SDK `originalEvent` qualify; coalesced, threshold-filtered or
unmatched inputs are counted rather than assigned fabricated render timestamps. Native smoothing
or inertia may reuse an event; it qualifies only once. Browser coalescing can hide physical input
history. INP/Event Timing alone cannot measure continuous pointer/wheel performance.

The flat anchor check is unavailable for pitched views, moving wheel pointers or interrupted
sequences. Inertia settling observations retain a caveat for interrupted/programmatic movement.
Transition target mismatch is labeled interrupted-or-not-reached rather than assumed successful.
Completed stability windows record their actual elapsed time; interrupted or truncated windows
remain unavailable. Optional long-task observations exclude GPU/worker time.

Hidden/blurred pages, viewport/DPR changes, overflow, context loss and rendering errors invalidate
comparisons. Cold tiles, throttling, weak/software GPUs, remote desktop, thermal changes, competing
maps, debugger pauses and profiling overhead need separate treatment. New resource activity is
counted; warm-start readiness cannot guarantee the full gesture path is cached. Style fingerprints
can vary with key/account URLs and do not freeze live tiles. Mobile emulation is not physical mobile.
No metric automatically certifies these budgets or user acceptance.
Require adequate matched samples (at least 100 per input kind across the five repetitions), inspect
match coverage and onset measurements, and corroborate sparse/coalesced samples with the trace;
an attractive percentile from a few surviving samples is insufficient evidence.

Provider display rights and renderer licensing remain separate. Preserve the existing
[dependency/data notices](../map-stage-1/LICENSE_NOTICE.md), expanded source attribution and official
MapTiler logo. No tile/geometry archive or provider-derived analytical dataset is created.

## Automated verification and change control

```powershell
node --test tools/map-stage-1c/tests/navigation.test.mjs
python -B -m unittest discover -s tools/map-stage-1c/tests -p test_server.py -v
node --check tools/map-stage-1c/navigation.mjs
node --check tools/map-stage-1c/diagnostics.mjs
```

Tests use controlled engineering fixtures, not browser interaction measurements. Python tests
serve only loopback fixtures/assets and contact no provider. No database tests are needed because
backend code is unchanged. Results and exact file manifest are in
`docs/evidence/map-stage-1c/verification.json`; implementation report is
`docs/design/MAP_STAGE_1C_REPORT.md`.

Branch: `stage/1c-map-navigation`, based on `0e0440a28b2d1c82a70aa545c3e8bf3479e0cea0`.
Existing foundation/harness/presets/historical evidence and dependencies are protected. No commit
or merge is automatic. After visual acceptance, await explicit commit authorization. Rollback:
stop only this host and return to `main`, retaining uncommitted experiment files for review; never
use a broad reset/clean or restore the rejected application. No Stage 2 or deployment is authorized.
