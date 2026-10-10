# Digital Twin performance

10 October 2026. **No actual browser/GPU/physical-device measurements are available.**
60 FPS on capable desktop hardware is a target, not an achieved result. Code tests and
HTTP reachability do not establish perceived smoothness, mobile usability or input latency.

## Implemented controls

| Preset | DPR cap | Antialias at initialization | Native facade gradient / footprint edges | Building minimum zoom | Orbit update cap |
|---|---|---|---|---|---|
| Performance | 1 | Off | Off / off | 14.5 | 20Hz |
| Balanced | 1.5 | On | On / on | 13.5 | 30Hz |
| High Quality | 2 | On | On / on | 13 | 30Hz |

Mobile-width startup defaults to Performance; this is a heuristic, not GPU capability detection.
Runtime quality changes adjust pixel ratio, detail and effects without recreating the map.
WebGL antialias context attributes cannot be changed that way; select quality and **Retry map**
to reinitialize with its antialias setting. No new hardware-detection or cosmetic rendering dependency.

Timeline updates only five existing own GeoJSON sources (nodes, zone polygons, zone centres,
illustrative node footprints and city aggregate), plus a selection filter. Selection has a sixth
independent source. No tile sources/layers/map are rebuilt per timestamp. Maximum data size is
five nodes and three groups, thirteen frames and twenty prior-day baseline records. This
bounded prototype is not evidence of performance at production sensor/building volumes.
Native GPU extrusion drawing and paint transitions avoid CPU mesh construction. Hidden
pages stop playback/orbit; requested frame sampling stops if hidden. Reduced motion is honored.

Error paths expose configuration/resource/context-loss failures without a replacement map.
Retry destroys the previous renderer before creating a new one. Context loss stops motion and
playback and offers Performance quality/retry; restoration is not treated as verified recovery.
Offline basemap operation is intentionally unavailable; no service worker or hosted-tile store.

## Measurements actually made

| Check | Result and scope |
|---|---|
| Local served asset footprint | **1,757,495 bytes** across own HTML/CSS/modules and SDK main/worker/CSS; provider resources excluded |
| SDK main module | 1,079,357 bytes, uncompressed |
| SDK worker module | 508,314 bytes, uncompressed |
| SDK CSS | 83,290 bytes, uncompressed |
| Dependency advisory audit | 0 known vulnerabilities in isolated npm tree at recorded check time; no guarantee of absence |
| Domain/style/expression checks | 16 Node tests pass; includes actual SDK expression/style validators, not GPU output |
| Local host checks | 7 Python tests pass; includes exact assets, config scope, Host policy and secret/path refusal |
| Contract/preservation checks | Exports match; all 203 retained pre-prototype files unchanged; 176 original and 22 protected digests also match |
| Actual render/frame time/load/input latency/GPU memory | **Unavailable**, no supported browser and no authorized MapTiler key in launch config |
| Physical mobile/Telegram WebView | **Not tested**; loopback-only host is not reachable from another device |

Exact sizes, runtimes, timestamps, stdout logs and checks:
[bundle footprint](../evidence/digital-twin/bundle-footprint.json),
[verification](../evidence/digital-twin/verification.json),
[dependency audit](../evidence/digital-twin/dependency-audit.json).
The stdlib local host serves assets uncompressed with no-store for diagnostic repeatability.
Hypothetical gzip sizes in evidence are not network measurements. No production/CDN
optimization was enabled; cold local loads are not representative of a future PWA build.

## Reproducible browser measurement plan

Use the manual matrix in the validation report. Identify physical hardware vs desktop device
emulation, browser/version, viewport, DPR/rendering DPR, quality, power mode and connection.
Warm up real visible tiles, stop auto motion, verify attribution and zero errors, then separately
sample idle, ordinary pan/zoom, controlled orbit and timeline playback. Repeat central and
waterfront, both themes and placeholders off. Record cold/warm first visible geographic
content manually with actual video/trace; SDK load/idle events alone cannot establish it.

Console helpers after authorized rendering:

```javascript
window.citysenseTwin.sampleFrames(10000)
window.citysenseTwin.diagnostic()
```

Wait for the sample to finish before exporting diagnostics. Recorded RAF p95 intervals are
page scheduling intervals, **not GPU FPS**, input latency or compositor performance. Browser
performance traces and actual interaction evidence must corroborate the 60 FPS desktop
target. Resource entries may omit worker/cross-origin traffic; JS heap excludes GPU/native
memory and workers; neither is a complete memory/billing measurement. Diagnostics preserve
these limitations and keep meaningful-render status unverified until visual evidence exists.
SDK load/ready timers start at renderer construction, excluding the preceding module/style fetch;
they are not total page-load times.

Inspect three viewports and a separately authorized physical-device/WebView test setup.
Current host must not be exposed publicly or rebound to LAN as an implicit next step.
Retest context-loss/retry, quota/auth failures, missing glyphs, tab hide/resume, reduced motion,
portrait resizing and weaker GPU settings. Set a real mobile performance budget after those
measurements; do not manufacture timings or infer mobile success from desktop emulation.

## Provider usage and operational costs

Plain MapLibre is a third-party SDK, so MapTiler bills tile **API requests**, not an unlimited
MapTiler SDK session. Published Flex pricing: $30/month with 500k API requests and $0.15
per additional 1,000, excluding VAT. Free includes 100k/month for testing/prototyping/personal
or non-commercial use and pauses at quota. Confirm commercial-plan eligibility before any
customer release. Example budget at 1m billable requests: $30 + $75 = $105 before tax/other
services; it is a request-volume scenario, not measured traffic. Panning, multiple maps and
extra sources increase requests; monitor account analytics and spending limits. Native building
extrusion here does not initiate the separate MapTiler 3D SDK-session product. No purchase
or plan change occurred. [Official pricing and third-party billing FAQ](https://www.maptiler.com/cloud/pricing/).

Cloud terms allow temporary personal caching for a single end user, require direct provider
requests absent an agreement, and restrict server caching/proxying, exported/bulk content and
commercial derivatives. Prototype reports export only own synthetic records; selected building
geometry remains in-memory display state. Keep source attribution/logo visible; no tile
extraction, offline tile packs, screenshot basemap substitute or publication is implemented.
Any external screenshot distribution/print use must fit the account's rights and retain notices.
This is an engineering rights review, not contractual approval. [Cloud terms](https://www.maptiler.com/terms/cloud/).
