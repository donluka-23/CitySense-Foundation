# CitySense map infrastructure — Stage 1 report

Date: **2026-10-10, Asia/Tbilisi**. Work stayed in `D:\citysense-foundation`.
**Stage 1 assessment and isolated test delivered; visual/provider validation is partial.**
**Stage 2 has not started and requires explicit user approval.** No visual approval,
production readiness or scientific validity is claimed.

## 1. Primary technology recommendation

Provisionally select **MapLibre GL JS + MapTiler Cloud Streets v4** for the mobile-first PWA
map foundation. Full overlay control, a provider-independent renderer and managed supply fit
the repository's evidence-first boundaries. This is an engineering recommendation pending
credentialed Batumi rendering, actual request costs, Georgian/English labels and physical-mobile
performance checks. It does not establish a visual/coverage winner. See
[provider comparison](MAP_PROVIDER_COMPARISON.md) and [rights/costs](MAP_DATA_RIGHTS_AND_COSTS.md).

The compatible MapTiler style is explicitly identified in its
[official MapLibre integration](https://docs.maptiler.com/maplibre/). No plan was purchased.
MapLibre's open source license does not permit extracting MapTiler's hosted data for CitySense
analytical features. Those features need independently authorized source data and methods.

## 2. Fallback

**Mapbox GL JS + Mapbox Standard**, conditional on the same local audit and acceptable product
terms/cost/overlay placement. Its managed cartography and provider-built 3D merit a credentialed
comparison. There is no evidence yet that they are better in Batumi. Standard is not a drop-in
style for MapLibre; the isolated test loads separate renderers.

**OpenFreeMap Liberty** is the credential-free test provider, not a production SLA substitute.
Its commercial display and public hosting are documented, but service terms/availability and
any acquisition/self-hosting rights must be assessed for the intended deployment.
[OpenFreeMap overview](https://openfreemap.org/), [terms](https://openfreemap.org/tos/).

## Repository, architecture and Git audit

Inspected README/handoff, Sprint 3 report and evidence, architecture/review/impact, relevant ADRs,
multi-city/API/registry/governance/coverage/research/security documents, executable API/platform/
models/engine/opportunity code, packaged city configuration, migrations/legacy SQL and exported
OpenAPI. The protected evaluation protocol was read and left unchanged. No AGENTS.md was found
in the supplied workspace. No previous web demo was searched for, copied or migrated.

The actual foundation is a Python 3.12.13 FastAPI/Pydantic modular monolith with PostGIS,
append-only evidence/revisions and a frozen deterministic suitability hypothesis. Package version
is 0.2.0; API metadata 0.3.0; migration head 0002. Sprint 3 reports partial acceptance, 179 passing
tests with 31 PostGIS cases and no empirical research results. Those are retained Sprint 3
results, not tests rerun for this map stage. `infra/sql/001_foundation.sql` is a legacy proposal
and was not applied. There was no existing PWA/frontend/package manifest in the audited tree.

`git status --short` and `git branch --show-current` failed with “not a git repository.” The
root has no `.git` entry; no branch/HEAD/upstream, tracked/untracked classification, diff, commit
or hosted CI can be attributed to this workspace. No Git metadata was initialized. To preserve
existing work, a pre-change snapshot recorded **176 existing non-generated workspace files**;
final hash comparison is in [preservation.json](../evidence/map-stage-1/preservation.json).

### Actual OpenAPI / integration findings

| API area | Actual implementation | Map consequence |
|---|---|---|
| Five `/v1/cities/{city_id}` operations | Place search/details, sparse state, suitability and comparison; authenticated city-scoped stored reads | Future projections can use internal place IDs, WGS84 points and rights; current limits are 30 records, radius ≤10 km |
| Geometry | Point only, provenance-bearing revisions; unknown positional accuracy | Current results are not park polygons, entrances or walking network geometry |
| Suitability | Null scores/coverage/exclusions, inputs/model hash; unvalidated frozen engine | The map must preserve abstention and cannot calculate replacement scores |
| Weather/environment | Source/kind/quality/valid/issued/retrieved/resolution semantics | No citywide raster/forecast endpoint; weather retrieval without issuance is not replay-ready evidence |
| Routing/isochrones | Absent; walking times explicitly caller estimates | Basemap paths cannot become route guarantees or measured travel times |
| Opportunity Registry | Provider/Offer contracts, lifecycle/confirmation/expiry; no operational API | Basemap POIs are not verified suppliers or confirmed availability |
| Browser security | Operator key, rights checks, no-store responses; no CORS/user identity contract | The privileged operator key must not be embedded in a PWA |

The API denies publication of the retained Sprint 3 real inventory. This stage neither read its
private polygons into the test nor changed their rights. Five boundary anchors, four abstentions
and one estimated walking exclusion remain the research state, not a full city inventory.

## 3. Batumi coverage evidence

A fresh bounded OSM source audit succeeded for **[west 41.60, south 41.61, east 41.67, north 41.67]**.
It returned 7,796 highway ways, 2,973 pedestrian/path/step ways, 15,406 building ways plus 45
building relations, 8 coastline ways, 49 park ways plus 3 relations and 1,368 selected vegetation
ways. Only 76 building ways carry a `height` tag; 3,854 carry height and/or levels (~25.02%).
Tag presence is not numeric-validity/surveyed-height coverage. No default building height was added.

Actual bilingual source names include ბათუმი / Batumi, 6 მაისი პარკი / 6 May Park,
პიაცა მოედანი / Batumi Piazza and ანბანის კოშკი / Alphabetic Tower. These source records
do not verify any hosted provider's tile filtering, label rendering, glyph support or update lag.
The query excludes Botanical Garden and some peripheral areas; absence from its selectors does
not prove a missing landmark. See [coverage audit](BATUMI_MAP_COVERAGE_AUDIT.md) and
[aggregate receipt](../evidence/map-stage-1/osm-coverage-summary.json).

OpenFreeMap style/TileJSON inspection succeeded with Node fetch and lists Georgian/English name
fields, processed heights and a dated tile template. Python urllib access returned 403. No provider
vector tiles were extracted. Mapbox/MapTiler actual Batumi map content remains unverified because
no dedicated authorized token/key or supported browser was available.

## 4. Actual screenshots and paths

**None captured; no screenshot paths exist.** The Browser skill/runtime was used, but connection
reported `No browser is available`; supported discovery returned `[]`. No standalone browser
workaround, reconstructed map or placeholder screenshot was substituted. Rendering, mobile
gestures, on-screen attribution and visual quality remain unexecuted checks.

Existing evidence paths:

- `docs/evidence/map-stage-1/osm-coverage-summary.json`: counts, selected source labels and hashes.
- `docs/evidence/map-stage-1/osm-query.overpassql`: exact successful source query.
- `docs/evidence/map-stage-1/provider-metadata.json`: live OpenFreeMap configuration inspection.
- `docs/evidence/map-stage-1/verification.json`: HTTP/syntax/dependency/contract results and unavailable browser.
- `docs/evidence/map-stage-1/preservation.json`: original-file and protected-file parity.
- `artifacts/map-stage-1/`: ignored raw projected OSM response, failed-request receipts, npm audit and current legal PDF/text.

Future screenshots belong in `artifacts/map-stage-1/screenshots/`, with an actual capture manifest
and visible attribution. This is a proposed location, not an existing screenshot deliverable.

## 5. Licensing and cost risks

Hosted display permission does not clear source extraction, long-term immutable evidence storage,
offline packs, shared caching or external publication. Preserve ODbL obligations for independently
acquired OSM data, provider/style/font notices, and CitySense's own source-purpose permissions.
The OSM source audit is separate from current source flags and authorizes no publication changes.

Plain MapLibre + MapTiler is request-metered; intensive panning/resource requests can cost more
than anticipated from SDK session pricing. Mapbox initialization/session metering and proprietary
SDK/Standard coupling also affect operations. OpenFreeMap has no SLA. Models of 20k/100k/200k
monthly map initializations, rights clauses and dated official price references are in
[MAP_DATA_RIGHTS_AND_COSTS.md](MAP_DATA_RIGHTS_AND_COSTS.md). They are assumptions, not invoices.

Current Mapbox product terms were obtained as a 14-page official PDF and inspected under the
[PDF skill](C:/Users/Lenovo/.codex/plugins/cache/openai-primary-runtime/pdf/26.630.12135/skills/pdf/SKILL.md).
On-device Mapping API caching is bounded and does not authorize a shared proxy/archive.
MapTiler commercial derivative restrictions are material to analytical ingestion. NSDI terms
could not be read through the web tool; no Batumi authoritative height/access license was verified.
Weather access/forecast lineage, partner availability and routing rights remain separately uncleared.

## 6. Technical blockers and QA status

| Check / blocker | Actual result |
|---|---|
| Authorized paid-provider credentials | Dedicated test config contained no Mapbox public token or MapTiler key; no secrets inspected or demo tokens borrowed |
| Browser/WebGL/rendering/screenshots | Unavailable; no style, glyph, gesture or physical-device result |
| Mobile performance | Unmeasured; package bytes are not FPS, load latency or battery evidence |
| Heights/connectivity/access | Sparse source tags, no survey or topology/entrance audit; MapLibre extrusions hidden |
| CitySense API integration | Deliberately not implemented; operator browser-auth/CORS and publication constraints remain |
| Routes/weather/availability | No operational sources/endpoints; no data generated or service enabled |
| Git/hosted CI | No metadata/upstream; unavailable |
| Isolated installation | `npm.cmd ci --ignore-scripts` passed; lock pins MapLibre 6.13.0 / Mapbox 3.32.0 |
| Dependency audit | 27 npm packages audited, zero reported vulnerabilities; not an OS or undisclosed-defect assessment |
| Syntax | Both `.mjs` files passed `node --check`; Python server compiled successfully |
| Loopback server HTTP | Test page/config/library/worker/CSS assets returned 200 with no-store; traversal/repository paths 404; untrusted Host 403 |
| Source audit | Final HTTP 200, all count outputs present, 24 projected labels; earlier regex failures retained |
| OpenAPI exports | Existing exporter `--check` passed: `Contract exports match` |
| Preservation | Existing files and Sprint 3 protected-file hashes unchanged; final receipt linked above |

HTTP and syntax checks verify launch plumbing, not WebGL execution. No CitySense regression suite
was rerun because its code/contracts/dependencies were unchanged; original-file parity and contract
verification are the relevant checks. Runtime resource errors are surfaced in the POC without
fabricated fallback data. The locally started test server was stopped after verification.

## 7. Exact proof-of-concept launch

From a PowerShell terminal:

```powershell
Set-Location D:\citysense-foundation\tools\map-stage-1
npm.cmd ci --ignore-scripts
python serve.py
```

Open **http://127.0.0.1:8765/**. This is the key-free OpenFreeMap Liberty inspection page.
Use `?view=oldtown&lang=en` or `?view=park&lang=ka` to inspect named views.
Stop with Ctrl+C. The server binds only `127.0.0.1:8765`, reads no repository `.env`, and has
no CitySense API/database adapter or public hosting path. Python 3.12 and Node/npm are required;
network access and a compatible WebGL2 browser are necessary for actual rendering.

For a later authorized provider comparison, set **your own public browser** credentials in the
same terminal before starting the server:

```powershell
$env:MAP_STAGE1_MAPTILER_PUBLIC_KEY = 'YOUR_AUTHORIZED_BROWSER_KEY'
$env:MAP_STAGE1_MAPBOX_PUBLIC_TOKEN = 'pk.YOUR_AUTHORIZED_PUBLIC_TOKEN'
python serve.py
```

Then open `http://127.0.0.1:8765/?provider=maptiler&view=oldtown&lang=en` or
`http://127.0.0.1:8765/?provider=mapbox&view=oldtown&lang=ka`.
No token should be posted in chat or committed; browser keys are public to their intended local
client. Missing credentials block the selected provider. Full options/reproduction instructions
are in [tools/map-stage-1/README.md](../../tools/map-stage-1/README.md).

## 8. Proposed Stage 2 implementation plan — not started

Only after **explicit user approval**, with scope kept to an incremental map foundation:

1. Close credential/browser gaps: compare the same Batumi views, both languages, real attribution
   and provider-built 3D where permitted; complete physical mobile/4G benchmarks and revise the
   recommendation if evidence warrants. Accept the service/retention/budget requirements separately.
2. Record the final renderer/provider decision in a reviewed additive ADR (next is 0011), with
   pinned dependencies, source/style version handling and supplier-switch boundaries. Define only
   the map foundation scope; do not redesign the entire product.
3. Add the approved local PWA map host with one persistent map instance, responsive viewport,
   attribution, gesture/accessibility/context-loss behavior and provider error states. Cache only
   the permitted shell/assets; defer provider offline packs until rights are resolved.
4. Integrate existing authorized CitySense reads through a scoped server boundary, preserving
   IDs, selected geometry revision, rights, no-store, timestamps, null scores and missingness.
   Keep the frozen engine/protocol unchanged and operator secrets out of the browser. Never publish
   private research geometry merely because the map can display it.
5. Add real point/line/polygon/raster overlays only when the required source data/contracts are
   authorized. Cluster permitted points with separate missing/stale counts. Defer weather,
   routes/isochrones and partner availability until actual adapters, expiry and publication rights
   exist; new geometry/route contracts must be additive and reviewed.
6. Run focused API/rights/time/abstention integration checks, physical-device performance and
   attribution/Georgian visual QA; deliver actual screenshot and cost receipts for review. Any
   visual approval or public deployment is a separate explicit decision.

No Stage 2 files, full application design, fake buildings, synthetic city state, weather heatmaps,
engine/protocol changes, live partner/LLM calls or public deployment were implemented.

## Deliverables

- [MAP_PROVIDER_COMPARISON.md](MAP_PROVIDER_COMPARISON.md)
- [BATUMI_MAP_COVERAGE_AUDIT.md](BATUMI_MAP_COVERAGE_AUDIT.md)
- [MAP_DATA_RIGHTS_AND_COSTS.md](MAP_DATA_RIGHTS_AND_COSTS.md)
- This report and the isolated [technical test](../../tools/map-stage-1/README.md).

**Stop point: Stage 1. Await explicit approval before Stage 2.**
