# Real Batumi place/context coverage — 2026-10-09

**Observed engineering result:** five actual mapped OSM park ways were acquired; four candidates
abstained and one was excluded under an explicitly invented caller walking estimate. Zero real
suitability scores were produced. This is a private geometry demonstration, not verified entrances,
representative city coverage, an environmental measurement or a scientifically validated recommendation.

`real_context.py` builds one fixed bounded Overpass query: park ways within west 41.615,
south 41.638, east 41.635, north 41.658; `out skel geom 5`. Skeleton output excludes author identities,
contacts and free-form tags upstream. Returned polygons/vertices and provider database timestamp
are archived; each stable ID is `batumi:osm:way:OSM_ID`. Labels explicitly say mapped park way.
The stored point is the first returned vertex within the selection window, not a centroid, entrance
or independently checked activity site. Complete raw geometry remains private. Relations, multi-way
park deduplication, polygon interiors, routing and access verification are not implemented.

Actual capture retrieval: **2026-10-09T15:15:11.042337Z**. Provider database timestamp:
**2026-10-09T15:13:08Z**, separately preserved. Raw SHA256:
`9c54e6cde7ebbd2b1dfdd8b6d138c3bf86a8692c43ca517209ce219e93db11b8`.
Private inventory: `artifacts/sprint3/real-inventory.json`; raw and decision receipts:
`artifacts/sprint3/real-data/`. They are intentionally ignored from public delivery. The retained
database uses a separate immutable source ID `osm-batumi-geometries`; Sprint 2's aggregate source,
count and sampling-window identity remain unchanged. No contributors or participants were collected.

| Evidence dimension | Coverage in these five records | Decision consequence |
|---|---|---|
| Mapped identity/geometry | Five actual ways; source-reported boundary vertices | Can identify records, cannot promise suitable interior/entrance |
| Independent entity/access verification | None | Existence and accessibility are unverified |
| Greenery fraction | Missing 5/5 | Park presence/count is never converted to greenery |
| Traffic feature | Missing 5/5 | No distance-to-noise conversion or unreviewed normalization |
| Shade | Missing 5/5 | Cool/family hypotheses cannot score |
| Licensed run-aware weather | Missing 5/5 | Weather/exposure comparisons unavailable |
| Walking route/accessibility | None | 20/45-minute values are deliberate operator estimates, not route measurements |
| Operating/court availability | Unknown; no court inventory | No claim of open facilities or three available courts |
| Publication/LLM transfer | Not cleared for this derivative inventory | Authenticated REST/Telegram publication remains denied |

Source-rights/publication ledger, reviewed 2026-10-09:

| Source | Local research/storage | Commercial/publication/external transfer | Required evidence |
|---|---|---|---|
| OSM/Overpass bounded geometry | Narrow private nonpersonal capture permitted by reviewed public terms | Flags false pending derivative/attribution/revocation review | Data-steward approval of export, ODbL share-alike and attribution plan |
| Open-Meteo | Live disabled; fixture parser only | No approved account/access/issuance contract | Source-specific eligible research/commercial use and authenticated forecast lineage |
| Routing provider/local network | No feed/call made | Unapproved | Route geometry/validity, walking assumptions, licensing and accessibility audit |
| Independent local site inventory | None supplied | Unapproved | Site IDs/entrances/access and dated verification |

[OSM licence terms](https://www.openstreetmap.org/copyright) require attribution and applicable
ODbL obligations; this ledger does not constitute blanket clearance. The
[Overpass service policy](https://dev.overpass-api.de/overpass-doc/en/preface/commons.html) supports
small manual requests and discourages using the public instance as an app backend. No polling
feed was started. [Open-Meteo terms](https://open-meteo.com/en/terms) require access eligibility review;
the existing null-issuance forecast candidates remain outside historical scoring/replay.

The local operator uses a code-created research/cache audience; publication is the default for
all existing HTTP routes and for Telegram. No request field grants local-research privileges.
Missing feature joins are visible in stored state. Hard walking filters and the original engine
execute normally; dynamic reads do not fabricate observations. A FeatureSnapshot and parameter
artifact preserve scoring replay; a separate immutable decision file preserves geometry, state,
rights, exclusions, target time and missingness. The retained 20:00 Tbilisi evaluation is snapshot
`69d05735-0024-4375-84dc-04ca7a5a8b46`. The earlier next-day 19:00 execution is also retained;
the request time is explicit in each artifact.

Selected narrow feasibility target: **quiet-rest comparison at fixed site/time windows, with
independent acoustic-exposure checks**. This is a proposal requiring research review, not scientific
approval. Local LAeq measurements could test acoustic contrast without pretending traffic proximity
is noise. Human rest-suitability labels still require consent and blinded matched exposure. The
positive orientation/normalization of the legacy traffic-named feature must be independently
specified before genuine ingestion; no conversion, weight or protected protocol was changed.

The smallest inputs needed for a technically non-abstaining `quiet_rest` result are two fresh,
lawful, method-versioned normalized fraction features per eligible place: `feature_greenery` and
`feature_traffic_proximity`, with reviewed orientation, footprint and lineage. Such a score would
remain unvalidated. To answer the user's full outdoor request additionally requires site/entrance
verification, lawful forecast issuance/retrieval, walking routes and operating access evidence.
Thermal/family safety/psychological claims require different constructs; no successful score alone
would establish them.

From services/api, load an existing permitted archive using `scripts/real_workflow.py --inventory
PATH --output NEW_DIRECTORY` with a local CITYSENSE_DATABASE_URL. `--acquire` explicitly makes a
bounded public-source request and exclusive inventory/raw capture; use a new inventory path and
review terms first. Re-acquisition does not silently overwrite immutable geometry/source versions.
