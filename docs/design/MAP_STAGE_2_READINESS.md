# Map Stage 2 readiness after Stage 1B

**Status: NOT READY. Stage 2 has not started and is not authorized.**
Stage 1B is PARTIAL. Local comparison tooling is available; actual hosted-provider captures,
visual acceptance and mobile/WebView performance remain open. Setting map credentials is
authorization for Stage 1B testing only, not Stage 2, deployment or a provider purchase.

## Gates and exact outstanding evidence

| Gate | Current evidence | Exit requirement |
|---|---|---|
| Stage 1B engineering harness | Isolated real-SDK client, presets, provider error states, diagnostics; syntax/configuration/HTTP checks | Browser execution with no unexplained errors; review capture metadata |
| A/B provider access | User will configure locally; agent saw no credential | Authorized provider style/tile requests from the actual permitted origin |
| Batumi visual comparison | Verified source camera points; C user feedback; zero agent screenshots | Matched real PNGs + diagnostics for locations/conditions/languages/viewports, unavailable features explicitly documented |
| Provider choice and visual direction | MapTiler engineering candidate; Mapbox alternative; no visual ranking | Evidence-backed decision and explicit user visual approval |
| Height/3D honesty | Source heights sparse; provider 3D unverified | Document supplied extrusion/model content; keep unknown heights out of analytical shade/thermal claims |
| Mobile / WebView | No physical-device, gesture, frame-latency or memory benchmark | Android Chrome, iOS Safari and target Telegram clients tested separately; accessibility/attribution/context-loss reviewed |
| Commercial readiness | Dated public terms and modeled cost sensitivity | Eligible plan, measured request/load usage, attribution, retention/offline/evidence-image rights and support/budget agreement |
| Backend/research preservation | Hash checks and OpenAPI export check | Continue frozen engine/protocol/contract boundaries; no independent browser scoring |
| Browser/API integration | Operator key, no CORS/public identity; point-only bounded reads; private inventory publication denied | Review a safe authorized boundary before any product/API map integration; never embed operator key |
| Environmental/routing/partner data | No weather tile, routing, isochrone or operational availability endpoints | Independent lawful sources, quality/timing/access and additive contracts; not a requirement to invent missing features |
| User Stage 2 authorization | None | Explicit approval after reviewing completed Stage 1B evidence and proposed scope |
| Public release | No deployment | Separate explicit authorization plus existing security/research/data-publication gates |

Physical-mobile and Telegram limitations cannot be closed by a desktop screenshot. A published
API or registry schema does not prove licensed live geometry, current availability or genuine
environmental coverage. Public deployment remains outside this proposal.

## Proposed Stage 2 scope — plan only

1. Finish the remaining Stage 1B captures/benchmarks/terms decisions and revise the recommendation
   against actual Batumi evidence. Obtain explicit user visual/provider and Stage 2 approval.
2. Record the selected stack and constraints in additive ADR-0011: renderer/style supplier,
   update/version strategy, commercial units, source separation and supplier exit boundary.
3. Implement only the approved local map foundation: one persistent map instance, attribution,
   responsive container, gesture/accessibility/reduced-motion handling and honest resource errors.
   Select the frontend host/build approach after scope approval; no framework chosen or installed now.
4. Define an authorized API projection preserving CitySense IDs, source rights, WGS84 points,
   timestamps, missingness and engine abstentions. Resolve operator authentication/CORS/user identity
   before browser integration. Do not publish the restricted research inventory or recalculate scores.
5. Add a narrowly approved real-data layer only after its source/contract is available. Routes,
   isochrones, environmental rasters and verified opportunity availability each require their own
   lawful adapters; leave them absent until then. Keep provider basemap data out of analytical ingestion.
6. Validate the approved implementation on target devices/WebViews and against measured account
   quotas. Cache only permitted app assets; provider offline packs require explicit rights. Review
   the result locally with the user. Public deployment is a separate future authorization.

No product navigation, chatbot, booking/payment, supplier dashboard, full tourist UI, synthetic
weather or frozen engine change is included. Current changes are confined to `tools/map-stage-1`
and additive Stage 1B design/evidence files. See [Stage 1B report](MAP_STAGE_1B_REPORT.md) and
[preservation evidence](../evidence/map-stage-1b/preservation.json).
