# CitySense Founder technical readiness handoff

**2026-10-14, Asia/Tbilisi — assessment only.** Repository: `stage/1c-map-navigation`, HEAD `aae7d9bd52d5e786406896eba94a22abc58cda5d`, including preserved uncommitted landing/governance work. No application code/configuration/database/dependency/Git/publication changes.

**Keep the technical foundation; build the missing tourist journey through approved additive contracts.** The codebase is a tested research backend plus disconnected map experiments and a local corporate website. It cannot yet execute the three-hour family/budget/return-to-hotel scenario. Estimated integrated demo readiness **45/100**; real pilot readiness **15/100**, as technical judgments rather than measured progress or business viability.

[Full evidence-based audit](CITYSENSE_CODEBASE_READINESS.md) · [architecture, dependencies and effort plan](CITYSENSE_CONTEXTUAL_COMMERCE_GAP_PLAN.md). E references below resolve to exact paths/line ranges in the audit.

## Founder questions answered

| Question | Technical answer |
|---|---|
| 1. What actually works? | Strict typed research requests, deterministic walking exclusion/weighted comparison/missing-data abstention, evidence lineage and frozen replay infrastructure; private stored-evidence REST service; standalone native map camera/attribution components; six locally generated corporate HTML pages. Current offline backend/map checks pass; current DB operation and live maps were not exercised. E01–E14/E20–E26 |
| 2. What is only a demonstration? | Synthetic evidence/provider fixtures and invented A1 model replies; private Telegram command flow; standalone basemap/provider/navigation experiments. Historical real OSM capture is genuine geometry, but produced zero suitability scores and is not cleared for this publication use. The landing explains future interactions; it has no functioning search/chat/map/booking. E13/E16–E18/E22/E24/E32 |
| 3. How close are we? | Useful components, incomplete journey. There is no tourist natural-language input, party/budget/return contract, eligible activity feed, five-option UI, shared card/map selection, approved referral pipeline or guest funnel. Pilot gates dominate readiness; a passing backend cannot close them |
| 4. Greatest reuse? | One modular backend/service, provenance/rights/time checks, deterministic abstention patterns, PostGIS/stable geometry identity, MapLibre/native cameras/attribution, transport bounds and meaningful negative tests. Corporate site remains a separate useful asset. E02/E04–E14/E20–E30 |
| 5. Five most important gaps? | **(1)** lawful usable activity/entrance inventory; **(2)** approved party/budget/window/return/access eligibility and coverage retrieval; **(3)** guest-safe synchronized mobile input/cards/map/selection; **(4)** actual permitted provider destinations/data/attribution; **(5)** privacy/event/deployment/physical-device acceptance. These must be solved in dependency order |
| 6. External permissions blocking live deployment? | Inventory/content/display/cache rights; actual affiliate/deep-link/subID permissions; weather/routes rights where required; hotel QR placement/branding/recruitment; privacy/measurement and hosting/release approvals. No current credentials/acceptance are established. GetYourGuide API access is distinct from affiliate linking, and higher Viator access needs separate approval/certification. [GetYourGuide requirements](https://partner.getyourguide.support/hc/en-us/articles/13981133907613-API-integration-and-requirements), [Viator access levels](https://partnerresources.viator.com/travel-commerce/levels-of-access/) |
| 7. What in seven days? | At roughly 35 focused hours and **only after separate scope approval**, the 12–20h offline synthetic constraint experiment plus independent review/readiness work is credible. It can demonstrate party/total-budget/full-trip deadline preservation, known rejection and unknown abstention. A polished full integrated map journey is outside the base seven-day estimate. No affiliate API or account is needed |
| 8. What in twenty days? | Roughly 100h at the same sustained capacity: a low-scope synthetic contextual demo may be achievable toward M1's low estimate **if contracts, relevant UX/map permissions and reviewer access are supplied early**. Base M1 is 150h, so twenty days is not a promise. Permissioned affiliate/hotel pilot readiness is not supported by that window; external waiting may be indefinite |
| 9. What waits for market research? | Guest-paid checkout/10-GEL entitlements, hotel billing/payouts/refunds, commission optimization or sponsored ranking, booking callbacks, partner SaaS dashboards, four simultaneous provider integrations, complex ML/embeddings, sensing/3D expansion and public agent writes. Preserve existing research/code rather than delete it |
| 10. Recommended next action? | Select one tourist task and required facts, then consider separately authorizing the bounded **offline synthetic constraint-validity comparison** in gap-plan §9. It is the smallest engineering experiment that answers the new job without assuming a partner. In parallel planning, define inventory/rights prerequisites; do not collect data or execute successor stages on the basis of this audit |

## Verification and specific current defects

Current results: **148 backend tests passed** with 31 DB integration cases deliberately deselected; **18 map JavaScript + 9 map-host tests passed**; contract exports, backend Ruff and Bandit passed. Initial backend attempt had 26 Windows temp-directory setup errors; rerun passed in a fresh isolated ignored temp directory. A Starlette/HTTPX deprecation warning remains. No installation, migration, real provider call or fresh vulnerability-feed audit occurred.

**Landing test command fails:** its manifest advertises unittest discovery but `apps/landing-web/tests/` is absent. Existing six generated pages and 14 manifest hashes match source, which proves artifact consistency only. Publication-readiness check returns BLOCKED for missing approved origin, publication authority, actual hosting/privacy facts, legal applicability decision and approved disclosures. No actual implementation visual QA/Founder packet was located; the newer preserved local implementation request grants execution authority despite the incomplete governance overlay. See audit §§1, 10–11.

Before external reuse also close the confirmed Stage 1 MapTiler configuration risk: `tools/map-stage-1/serve.py` 52–68 returns any configured MapTiler value to the browser, unlike Stage 1C's secret-sentinel checks. No configured real key or active leak was found. Existing private API operator identity, optional dev calculator/replay authentication and immutable storage are unsuitable for guest-facing sessions/retention without a reviewed boundary.

## Effort/cash decision

| Milestone | Incremental hours low / base / high | Direct setup/testing allowance low / base / high | Monthly operating allowance low / base / high |
|---|---:|---:|---:|
| Contextual labeled demo | 80 / 150 / 250 | $0 / $75 / $250 | $0 / $0 / $50 |
| Authorized affiliate pilot | +130 / 240 / 400 | +$50 / $250 / $800 | $30 / $100 / $250 |
| Small-hotel distribution | +50 / 100 / 180 | +$20 / $100 / $350 | +$0 / $25 / $75 |

Total cumulative engineering: **260 / 490 / 830 hours**, approximately 7.4 / 14.0 / 23.7 focused 35h weeks **excluding permission/UX/partner waiting**. Cash amounts are planning allowances in USD, not vendor quotes; Founder labor, external legal/field/translation review, hardware, taxes and negotiated supplier minimums are excluded. Those excluded costs are unquoted and may materially change a live-pilot budget. Paid access is outside these estimates. Full task allocation, prerequisites, test criteria and cost caveats are in gap-plan §8. No November/date guarantee follows.

## Disposition and handoff boundary

| KEEP | REFACTOR / REBUILD | DEFER |
|---|---|---|
| Modular backend, frozen B0/evidence/replay, typed rights, source transports, native maps, corporate site, negative checks | Refactor approved tourist eligibility/retrieval/activity contracts; rebuild missing guest-safe request/session state, integrated mobile comparison/map and permitted referral/events/hotel entry through new implementation | Payments/direct bookings/public agent writes, multi-provider breadth, hotel SaaS, complex ML/sensing/3D, commercial priority pending CF-02 |

These three reports are complete as assessment artifacts. They are not independent release QA, Founder acceptance, amended contracts or successor-stage permission. CF-01/02/03/08, PRODUCT-APP UX gates, Stage 1B closure/waiver and separately approved implementation/release scope remain applicable. No subagents or new visual captures were used. Rollback, if desired, consists only of removing these three newly created audit reports; existing user work is never rollback material.
