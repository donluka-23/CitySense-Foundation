# Stage 1C navigation experiment — implementation report

Date: 2026-10-10, Asia/Tbilisi. **Implemented; automated/HTTP verification passed.
Browser performance and visual acceptance remain pending. No commit or merge.**

## Scope and configurations

One loopback-only MapLibre 6.13.0 + MapTiler Streets v4 map. Four existing Batumi presets and
their canonical cameras are read from the unchanged Stage 1B JSON. No backend, research,
existing harness, historical evidence, dependency manifest or lockfile was changed.

| Configuration | Implemented behavior | Measured navigation outcome |
|---|---|---|
| Immediate | Native `jumpTo` for explicit changes | Unavailable |
| Short native transition | Native `easeTo`; editable initial candidate 400 ms | Unavailable; 400 ms is not accepted |
| Drag/inertia | Native defaults, independent of explicit-change mode | Unavailable |
| Wheel/trackpad and rotation/pitch | Native handlers, default sensitivity and bounds | Unavailable |
| Provider 3D on/off | Original provider extrusion layers restored or hidden at identical cameras | Actual layers/content unavailable in this verification |

No artificial camera loops, extra geographic bounds or new camera restrictions. Canonical Mercator
projection is explicit; upstream default pitch range is 0–60°. Reduced-motion preference makes
explicit transitions immediate. Supplied hidden/minzoom-restricted buildings remain restricted;
geometry and heights are never invented. Building clarity and coverage need visual inspection.

## Diagnostics and evidence

Implemented software observations: normalized input timestamp/listener entry, originalEvent-matched
camera-to-render timing, gesture-onset timing, matched/unmatched inputs, render callback intervals,
optional long tasks, flat wheel-anchor drift/settling, command completion/interruption, two-second
endpoint stability, errors and WebGL context loss/restoration. Exports include camera/configuration,
repetition/purpose, declared physical/emulated device/cache/input conditions, viewport, native/rendering
DPR, browser/WebGL renderer information, SDK version and supplied-style/preset SHA-256 fingerprints.

No SDK exception strings, key values, provider URLs, raw styles, tiles or building features enter
exports. Resource-only renders cannot certify input response. Coalesced/unmatched inputs remain
unmeasured. Frame callbacks are not GPU FPS; software timing is not measured visual latency.
User quality assessment is separate, null/pending until supplied by the operator.

**Actual interaction measurements: none.** Browser selection returned `No browser is available`;
supported recovery discovery returned `[]`. The launching host had no configured MapTiler public key.
Zero authenticated provider requests, rendered maps, screenshots or physical-device trials were
performed. This says nothing about credentials or a manually opened browser in another terminal.
Controlled test fixtures establish calculations/wiring, not real interaction performance.

## Technical verification

- 18 JavaScript tests passed: all canonical cameras, input/command matching and timing, no fabricated
  missing metrics, overflow/invalid conditions, completed/interrupted stability windows, transition
  candidates/reduced motion, extrusion preservation, circular bearing comparisons, browser-adapter
  wiring and actual installed SDK API compatibility.
- 9 Python tests passed: allowlisted asset byte parity, HTTP HEAD/no-store/security headers,
  Host/traversal/repository-path refusal and public-key configuration precedence/refusal.
- Module syntax, Python AST parsing, Ruff lint and formatting checks passed using existing tools.
- Real service launched on loopback port 8767: eight allowlisted asset routes returned 200;
  configuration returned explicit missing-key state. No provider calls or public/LAN listener.
- Approved baseline files were compared by Git blob hashes; `main`, branch HEAD and index remain
  at `0e0440a28b2d1c82a70aa545c3e8bf3479e0cea0`. Exact counts/hashes/results are in the evidence receipt.

The temporary smoke-test service was stopped. No existing process was stopped. Dependencies were
reused without installation/upgrades. No backend regression result is claimed for this stage.

## Exact change manifest

All nine files are **new additions**, on `stage/1c-map-navigation`; no existing baseline file changed:

1. `tools/map-stage-1c/index.html`
2. `tools/map-stage-1c/navigation.mjs`
3. `tools/map-stage-1c/diagnostics.mjs`
4. `tools/map-stage-1c/serve.py`
5. `tools/map-stage-1c/README.md`
6. `tools/map-stage-1c/tests/navigation.test.mjs`
7. `tools/map-stage-1c/tests/test_server.py`
8. `docs/design/MAP_STAGE_1C_REPORT.md`
9. `docs/evidence/map-stage-1c/verification.json`

The verification receipt includes SHA-256 values for the other eight files; it excludes its own
self-referential hash. Transient host/test logs and HTTP receipts are under ignored
`.local/map-stage-1c/`; no extra tracked files, new packages or configuration changes were needed.

## Run and remaining manual acceptance

From repository root, set your authorized public browser key in the launching terminal:

```powershell
$env:MAPTILER_API_KEY = 'YOUR_AUTHORIZED_PUBLIC_BROWSER_KEY'
$env:MAP_STAGE1C_PORT = '8767'
python -B tools/map-stage-1c/serve.py
```

Open **http://127.0.0.1:8767/**. Ctrl+C stops that host. See
[README](../../tools/map-stage-1c/README.md) for paired URLs, condition declarations, recording,
five-repetition protocol, provisional budgets, capture safety and automated check commands.

Manually assess dragging, wheel and trackpad zoom, rotation/pitch, camera stability, building
readability and predictability across all four presets. Compare Immediate with several short
transition candidates, interrupt transitions with input, inspect native inertia and matched 3D
on/off views. Verify actual source attribution/logo, glyphs, tile completeness and error-free
WebGL rendering. Capture JSON plus a corroborating performance trace; keep user notes separate.

Cold tiles, changed DPR/viewport, hidden/blurred pages, profiler/debugger overhead, software/weak GPUs,
remote desktop, competing maps and thermal/power changes can invalidate comparisons. Observe
instrumentation overhead with separate uninstrumented trials. Desktop emulation cannot establish
physical-mobile performance. Live provider fingerprints do not freeze tile content. No collision-
avoidance, surveyed height, offline support, measured GPU FPS or visual-latency claim is made.

Commit only after visual acceptance and **explicit commit authorization**. Do not merge into `main`.
Rollback: stop only this host and return to `main`, preserving the uncommitted additions for review.
No broad reset/clean, Stage 2 work or deployment is authorized.

**STAGE 1C — IMPLEMENTED / TECHNICAL CHECKS PASSED / VISUAL ACCEPTANCE AND COMMIT AUTHORIZATION PENDING**


---

## Acceptance review — 2026-10-10, Asia/Tbilisi

This additive review supersedes the earlier pending qualitative-navigation status only. The
implementation report above and the original verification receipt remain historical evidence.
**Recommendation: conditional Stage 1C acceptance for the isolated desktop navigation experiment;
strict performance acceptance remains NOT VERIFIED. Commit and next-stage authorization remain absent.**

### Repository integrity and verified scope — PASS

Current branch is `stage/1c-map-navigation`; HEAD and `main` remain at the approved baseline
`0e0440a28b2d1c82a70aa545c3e8bf3479e0cea0`. All **378 baseline files** were rechecked by their
working-byte Git blob hashes: zero changed or missing. The index is unchanged. The complete
nonignored additions are exactly the nine files listed in the implementation manifest above.
No application source was modified during this review; only this acceptance section was appended.
Dependency definitions/lockfiles are unchanged, the installed MapLibre remains 6.13.0, and imports
use only the existing SDK, local experiment modules and standard-library test/host facilities.
No unrelated tracked additions, unapproved rendering framework or generated artifact was found.

### A. Functional verification — PASS within automated-test scope

The retained verification receipt and logs confirm **18 JavaScript tests and 9 Python tests passed**,
with zero failures. They cover canonical camera parity, native command selection, reduced motion,
provider-layer preservation, timing/event correlation, missing metrics, invalid runs, endpoint
stability/interruption, actual installed SDK APIs, browser-adapter wiring and host/credential/path
boundaries. The existing receipt also records successful syntax, lint/format and HTTP checks.
Implementation/test/README hashes still match that receipt. Since this is documentation-only and
those files are unchanged, tests were not unnecessarily rerun. Controlled fixtures do not verify
live browser rendering, physical input latency, GPU performance or user experience.

### B. User-assessed navigation quality — PASS, explicit user feedback

The user reports manual evaluation with the following results:

| Category | User evaluation |
|---|---|
| Mouse dragging | GOOD |
| Zooming | GOOD |
| Camera rotation and pitch | GOOD |
| Navigation with 3D buildings | GOOD |
| Camera transitions | GOOD |

This is qualitative approval of the tested navigation experience, not independent agent observation
or a physical-device performance certification. It does not select 400 ms as a final transition
value, verify surveyed building accuracy, or establish results for every preset/device.

### C. Performance evidence — PARTIAL, user-reported preliminary values

Source: the user's acceptance-review request. No raw Stage 1C interaction export was located in
`docs/evidence/map-stage-1c/`, `.local/map-stage-1c/`, or the searched repository JSON filenames
identifying Stage 1C/navigation/diagnostics. The available JSON files are the original implementation
receipt, host-process metadata and HTTP smoke receipt; they contain no interaction runs. The older
OSM coverage diagnostic is unrelated. Files outside the repository were not searched. Consequently,
these values are **user-reported, not independently inspected or reproduced**:

| Metric | 2D / buildings OFF | Oblique / buildings OFF | Oblique / buildings ON |
|---|---:|---:|---:|
| Input-to-camera-render proxy median | 11.2 ms | 11.2 ms | 12.3 ms |
| Input-to-camera-render proxy p95 | 24.0 ms | 19.8 ms | 20.0 ms |
| Input-to-camera-render proxy p99 | 35.7 ms | 27.4 ms | 26.4 ms |
| Active render interval p95 | 21.9 ms | 19.3 ms | 20.0 ms |

All reported input p95/p99 values lie below the proposed 50/100 ms budgets; reported active-render
p95 values lie below 33.4 ms. This is encouraging preliminary evidence, not a valid-run PASS.
No values were normalized, pooled, trimmed or substituted. Active-render p99/max, sample/match
counts, run IDs, full camera/style/DPR parity, repetitions and environment details are unavailable.
The comparison cannot establish negligible 3D cost. Software timing proxies do not measure physical
display latency; render callback intervals do not measure GPU FPS.

### D. Invalid/incomplete evidence and remaining uncertainty — NOT VERIFIED

The user reports window-focus validity flags, unclassified device information and isolated long
render intervals. Their exact flags, counts, timestamps, magnitudes and affected runs cannot be
checked without exports. In the existing recorder, `window-blurred` and `device-class-unclassified`
invalidate reference comparison; low percentiles do not override those flags. Preserve them rather
than removing or retrospectively reclassifying measurements. Long intervals cannot be assumed to be
focus artifacts, idle gaps or harmless outliers without event/trace evidence.

Five valid repetitions and coverage of all four approved presets have not been demonstrated.
Numeric stability/anchor/settling/transition endpoints, active-render p99/max, rendering-error and
context-loss counts are also not established by the supplied table. Physical-mobile performance is
NOT VERIFIED; it is not an additional blocker to an explicitly desktop-only Stage 1C claim. Stage 1B
is still PARTIAL. No Stage 1D or Stage 2 work is authorized.

### Minimum remaining requirements for strict desktop performance acceptance

1. Recover and inspect the original JSON exports first. Verify run completion/validity flags,
   input/match counts, declared hardware/browser/input/cache/power state, display refresh, actual
   map viewport/DPR, preset cameras and style fingerprint. Missing declarations cannot be guessed.
2. Reuse valid existing runs. Replace only invalid or missing repetitions/cells needed for the
   already approved five-repeat preset/configuration matrix; retain invalid originals. Keep the
   oblique buildings-OFF/ON comparison at identical camera and rendering conditions.
3. Locate the isolated long intervals in existing arrays/trace. If needed, use the already planned
   browser trace for the affected sequence only. A genuine unexplained active gap over 100 ms
   prevents that run passing; do not hide it through percentile summaries or blanket trimming.
4. Confirm the existing recorder's numeric stability, flat zoom anchor/settling, command completion
   and rendering-health criteria in those valid runs. Keep user quality feedback separate.

No new instrumentation, source changes, fresh full provider comparison or mobile certification is
required by this review. Additional code fixes would require evidence and separate authorization.

### Git readiness — scoped commit may be authorized with conditional wording

The exact proposed commit contains **only** the nine paths in the manifest above: seven experiment
HTML/module/host/README/test files, this report, and the unchanged original verification receipt.
All remain untracked and unstaged; no commit, merge, server launch or dependency installation was
performed during this review. A bounded scan of the nine files found no unresolved operational
credential matches; documentation key placeholders and explicit test sentinels were distinguished.
This scan is not a proof of absence of every possible secret.

Retain this assessment, attributed preliminary measurements, source/tests/README, and the original
verification receipt. Keep `.local/` runtime outputs, installs/caches, credentials, raw HARs and
unreviewed/raw browser traces excluded. Future raw exports remain local; a sanitized summary may
be incorporated within the same authorized documentation/evidence scope after review.

The historical receipt's report SHA-256 refers to the **pre-acceptance report snapshot**, verified
before this append. Its other seven implementation/README/test hashes still match. Do not present
that old report digest as the hash of the extended document or rewrite the original receipt.
The original report bytes remain an intact prefix of this file. This expected documentation-hash
change is the only review delta; no baseline-integrity discrepancy was found.

Proposed commit message:

`test(map): add verified Stage 1C navigation experiment`

Proposed commit body: Add the isolated MapLibre/MapTiler navigation experiment with passing
functional checks and positive user-assessed navigation feedback. Preserve the preliminary timing
values as user-reported evidence; strict performance acceptance and mobile verification remain
incomplete. No backend integration, deployment or renderer migration is included.

The word "verified" refers to functional checks only. Commit authorization is still required;
conditional navigation acceptance does not authorize a commit, merge or subsequent stage.

**STAGE 1C — ACCEPTANCE REPORT READY / COMMIT NOT AUTHORIZED**
