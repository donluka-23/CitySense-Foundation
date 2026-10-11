# CitySense Lab — Product & Business Blueprint

**Version:** 0.3 · **Date:** 2026-10-10 · **Status:** Founder direction updated; repository reconciliation pending

**Purpose:** Preserve decisions across Codex sessions and connect product outcomes, commercial processes, UX, data, and software implementation. This file is not evidence that features are implemented, validated, or legally cleared.

## 0. Interpretation and change control

- **DECIDED**: explicitly selected product direction or workflow in the current founder discussion; only a founder-approved decision can supersede it.
- **PROPOSED**: actionable design recommendation, not yet an approved hard requirement.
- **TO VALIDATE**: product, market, usability, or economic hypothesis requiring evidence.
- **TO VERIFY**: technical, data, legal, or provider feasibility not yet established.
- **DEFERRED**: part of the longer-term product, intentionally not a November pilot guarantee.
- **IMPLEMENTATION STATUS** must be recorded separately from decision status: a decided feature can remain unbuilt.
- Existing accepted repository ADRs/contracts remain in force. If this document conflicts with them, report the exact conflict to the founder; do not silently override either source. Preserve research and test evidence. Never equate this blueprint with proof of implementation.

## 1. Product identity

**DECIDED — P-001.** CitySense is a context-aware urban discovery, decision-support, and experience-action platform, initially for **tourists in Batumi**. It matches individual needs, location, time, and credible city conditions to suitable places/activities; provides understandable alternatives, mapping, travel feasibility, and routes; and can connect users to bookings or partner offers. It must not devolve into a generic tourist chatbot, directory, coupon catalogue, or sensor dashboard.

**DECIDED — P-002.** User needs and hard constraints determine eligibility and suitability before commercial prioritization. Place/time/urban-state evidence and the uncertainty of that evidence must remain explainable. Dynamic facts are never fabricated.

**DECIDED — P-003.** The long-term product includes partner workflows and a path from recommendation to action or booking. These are integral product concerns, even when outside a narrow implementation ticket.

**DECIDED — P-004.** Initial use and validation are **mobile web** via a QR entry channel in guest accommodations; no mandatory app installation for this pilot.

## 2. Audience, pilot, and distribution

**DECIDED — G-001.** Target November 2026: **closed, supervised MVP pilot with actual tourists**, not a public production launch.

**DECIDED — G-002.** Initial distribution opportunity: a founder contact manages **30 apartments in Orbi City A Block, Batumi**. A QR entry point in rooms is the proposed acquisition channel. Placement and access permissions, active occupancy, and operational arrangements remain **TO VERIFY**; the existence of 30 apartments is not a claim of 30 participants or scans.

**PROPOSED — G-003.** Start with 3–5 permitted apartments for a moderated usability shakedown, then extend to up to 30 if the experience and instrumentation pass review.

**DECIDED — G-004.** **Tourist value precedes commercial conversion** as the primary research hypothesis. The product must provide value even when no partner offer is available.

**TO VALIDATE — G-005.** Relative to tourists' ordinary Google Maps / AI assistant / host-advice workflow, CitySense helps people reach a **constraint-valid, informed selection** more easily and efficiently: fewer steps, less time, clearer comparison and fewer verifiable constraint violations. This is not a claim of superior venue-service quality or post-visit satisfaction.

## 3. Initial commercial segments and partner operating model

**DECIDED — B-001.** Initial commercial partner segments are (a) tours, (b) paid attractions, and (c) paid sports courts. Cafés/restaurants are a separate potential low-friction extension, not a replacement for these first segments.

**DECIDED — B-002.** Hybrid inventory and booking integration: initial **manual confirmation by partners**, later provider/API synchronization where available and permitted. Partner-provided opening hours, bookable capacity, time slots, prices, cancellation policies, and exceptions are distinct fields. A booking request is not a confirmed booking. No guaranteed availability without authoritative confirmation.

**DECIDED — B-003.** The payment transaction should be processed by an **authorized third-party payment provider**, not a home-built payment-processing system. This choice does **not** establish an exemption from all payment, platform, consumer-protection, tax, privacy, or marketplace obligations. Exact merchant-of-record, settlement, refund and liability topology remain **TO VERIFY** with the provider and legal review.

**TO VALIDATE — B-004.** Commission on a **completed/eligible booking** is an initial monetization hypothesis, with rate and settlement timing to be negotiated, not a finalized pricing policy. Count incremental value rather than all attributed clicks as incremental revenue.

**PROPOSED — B-005.** Café/restaurant acquisition experiment: voluntary, verified, contextual offer codes / QR redemption or manually confirmed reservation requests, with simple operator verification and a clear attribution ledger. No automatic POS integration required in the first experiment. This mechanism is neither implemented nor proven to drive incremental purchases.

**PROPOSED — B-006.** Partner-facing minimum workspace: verified listing and locations, offerings, schedules/capacity, request queue, confirm/decline/expire, cancellation/refund-policy references, and completed-service reporting. API integrations and advanced analytics follow later.

### Booking lifecycle — proposed minimum

`REQUESTED → PENDING_PARTNER → CONFIRMED → COMPLETED`

Alternative paths: `DECLINED`, `EXPIRED`, `CANCELLED`, and (if applicable) `REFUND_PENDING/REFUNDED`. Concurrency/hold expiry, idempotency, double-book prevention, modification, no-show, dispute, notification delivery, and settlement policies remain **TO DESIGN/VERIFY**. User-facing messages must accurately reflect the current status.

## 4. Core recommendation policy

**DECIDED — R-001.** Stage 1: validate required user constraints and build an eligible set using interest/intent, budget, time budget, mobility/accessibility requirements, actual place coordinates/entrances, travel feasibility, operational availability, and credible city conditions where available. Distinguish required constraints from soft preferences. If evidence cannot establish a hard safety/access constraint, do not state that it is satisfied.

**DECIDED — R-002.** Stage 2: rank by user suitability without partner status changing the underlying suitability score. Only within **materially equivalent suitable alternatives** may eligible partner options receive an additional **transparent commercial priority**. Equivalence tolerance/policy is **TO VALIDATE**, not an invented fixed score delta. Paid/partner ranking influence must not be presented as an organic quality signal; disclosure and applicable consumer rules must be reviewed.

**DECIDED — R-003.** Following a natural-language request, the interface presents **five alternatives as the desired default** and allows active user choice and comparison. **Safety fallback:** if fewer than five defensible, feasible candidates exist, show fewer and explain why; never fabricate or relax hard constraints to fill five slots.

**DECIDED — R-004.** A card selection synchronizes a persistent shared UI state, focuses the MapLibre/MapTiler map on the exact place/entrance, animates camera zoom/pitch only as feasible and accessible, and visually highlights the selected point/object. High-quality **3D-looking emphasis** is an interaction goal; custom 3D geometry is not a prerequisite. Do not imply a 3D building exists where map data does not supply one.

**DECIDED — R-005.** A concise anchored information window or contextual side/bottom panel shows **why recommended**, suitability criteria, evidence sources and timestamps, verified vs inferred vs unavailable vs partner-confirmed facts, important caveats, ETA/distance if actually available, availability/accessibility status, and next actions (route, compare, contact, booking/request where supported). Avoid a cluttered overlay obscuring the map.

**DECIDED — R-006.** The map, chat, five-result list, selected place, route and action/booking share the same active request/selection context. Reject stale asynchronous responses; preserve state when preferences change. Do not duplicate the ranking algorithm in the browser or let an LLM invent attributes, live conditions, places, availability or routes.

**TO VERIFY — R-007.** Live traffic quality, physical mobility accessibility data, public operating hours, route/ETA accuracy, weather and local dynamics in Batumi. Unsupported coverage must be marked unavailable rather than simulated. Distinguish static proxies (e.g., distance from traffic) from current measured noise/crowding.

**DECIDED — R-008.** The system supports **informed user choice**, not an objective claim to find the psychologically or experientially "best" venue. Present up to five credible, high-relevance options as the initial shortlist, with transparent differences and user-controlled reordering/refinement; support additional eligible results without unnecessary repeats. Never imply a mathematically calibrated probability of "best" unless independently modeled and validated.

**DECIDED — R-009.** Candidate retrieval must not accidentally discard superior eligible options due to arbitrary ID ordering or an early fixed limit. Define a measurable retrieval/coverage policy, then apply hard-constraint verification, suitability ranking, bounded diversity when relevant, and only then the conditional partner policy in R-002. Diversity must not contradict an explicit narrow user interest.

**DECIDED — R-010.** Validation is layered: (a) **constraint validity** for known, independently checkable requirements; (b) **comparative relevance** using documented criteria and, where appropriate, blinded human review; (c) **choice-interface efficiency and usability**. Unknown critical facts must not be silently counted as satisfied, and an abstention is preferable to a fabricated fifth suggestion. The overall 0–100 suitability score and "probability of best experience" are not empirically calibrated without separate studies.


## 5. User journeys and interfaces

**Tourist:** QR/open → express need or choose prompts → clarify essential constraints → receive up to five justified alternatives → compare cards and adjust sorting/preferences → click one → map focus/highlight + evidence panel → make an informed selection → route/contact/availability/booking request where supported. Post-visit venue feedback is optional and not the primary recommendation KPI.

**Partner:** invitation/onboarding and authorization → listing/offer verification → price/schedule/capacity updates → booking request → manual confirm/decline → service delivery/report → settlement/fee review where applicable.

**Platform operations:** verify sources and partner identity → moderate accuracy/rights → route requests and notifications → handle failures, cancellation/support, disputes and data deletion → monitor model and conversion evidence.

**UX principles:** mobile-first, no false real-time claims, clear origin and constraints, alternative comparison controlled by the user, visible uncertainty, keyboard-accessible navigation, map labels and attribution retained, progressive disclosure of evidence, clear commercial labels.

## 6. Evidence and measurement plan — decision quality, not venue-service quality

**DECIDED — V-001 (supersedes v0.1).** The primary closed-pilot hypothesis is that CitySense helps a tourist **identify and select an option that satisfies their explicit, objectively checkable requirements, using a fast, understandable and visually effective comparison process**. Quality of the service eventually delivered by an attraction, tour operator, café or sports venue, psychological utility and post-visit satisfaction are **not primary MVP KPIs**. They may be collected separately as exploratory feedback, not represented as proof of ranking accuracy.

**PROPOSED — V-002.** Primary product KPIs should be measured jointly rather than collapsed into a subjective "usefulness" score:

| Metric | Operational definition | Interpretation / caveat |
|---|---|---|
| **Valid Decision Completion Rate (VDCR)** | Sessions with an explicit selected candidate whose independently checkable **required** criteria are verified at decision time ÷ all eligible started decision-task sessions, with pre-declared exclusions | Primary candidate KPI. Unknown essential evidence does not count as verified; report unknown/abstained/unfinished separately. Selection is **not** proof of attendance. |
| **Time to Valid Decision (TVD)** | Elapsed seconds from a defined valid request start to qualifying selection; report median, spread and censored/unfinished sessions | Primary complementary efficiency KPI. Never improve this number by excluding difficult failures. |
| **Hard-Constraint Violation Rate** | Confirmed violations among assessed top-5 suggestions and selected options; report separately by constraint | Safety and functional correctness guardrail. Unknown is not a violation **or** verification. |
| **Evidence Coverage / Freshness** | Share of required candidate criteria with lawful, timestamped, current evidence; report stale/missing separately | Prevents treating absent data as good matches. |
| **Ranking Relevance Audit** | Explicit intent-to-attribute agreement using a predefined rubric; spot-check retrieval recall against a reviewed larger candidate pool | Ranking quality proxy, **not** proof of best eventual experience. |
| **Decision UX Error / Task Completion** | Observed selection errors, wrong map target/entrance, confusing status, incomplete tasks | Interface quality and reliability. |

**PROPOSED — V-003.** Secondary funnel metrics include QR scan-to-start, prompt submission, shortlist render, priority/filter change, cards compared, map focus/highlight, detail view, selection, route opened, contact/booking intent, and partner-confirmed commercial conversion **only where independent confirmation exists**. Define precise event schemas, denominators, duplicate-session handling, retention, missing-response rates and participant privacy boundaries before instrumentation. Clicks and route launches are behavioral signals, not verified visits or service satisfaction.

**PROPOSED — V-004.** Compare matched decision tasks against each participant's ordinary Maps/AI/host-advice workflow, measuring VDCR/violations, decision time and UX errors. Account for order effects and unequal information access. With the likely small Orbi City sample, report exploratory results and uncertainty, not statistical superiority.

**TO VERIFY — V-005.** Lawful, privacy-minimizing event collection; any consent/notice requirements; room-group-level QR attribution without unnecessary person-level identification; opt-out/withdrawal and deletion policy; data retention and access control. Never collect continuous location tracking by default.

**DECIDED — V-006.** Keep three outcome classes separate: (1) **verified decision validity** and decision efficiency (MVP core), (2) **self-reported or inferred user action** (secondary), and (3) **provider-confirmed fulfilled booking/payment** (commercial outcome, unavailable without partner/provider evidence). Do not claim any of these establishes the quality of the consumed service or causal incrementality by itself.

### Measurement events and evidence boundaries

| Stage | Instrument / evidence | Permitted interpretation | Not established |
|---|---|---|---|
| QR opened | Anonymous campaign/room-group source | Entry-channel engagement | Unique visitors or satisfaction |
| Request submitted | Structured needs, consented session event | Intent / task started | Correct match |
| Top-5 shown / refined | Candidate/evidence version IDs, explicit UI events | Exposure, comparison behavior | Best experience |
| Option selected | Selection event + independent constraint audit | Decision made; optionally constraint-verified | Venue visit or satisfaction |
| Map focused / route opened | Map/action event | Interaction or intent | Arrival or completed service |
| Optional user confirmation | Short self-report | Self-reported subsequent behavior | Provider-verified conversion |
| Partner booking/fulfillment receipt | Authorized partner/provider evidence | Confirmed commercial outcome at its stated stage | Incremental sale without comparator |

## 7. Business economics

**TO VALIDATE — E-001.** Tourist benefit: faster and easier **constraint-valid selection**, understandable comparisons and lower search friction. Better experienced venue/service quality and post-visit satisfaction are outside the primary MVP claim.

**TO VALIDATE — E-002.** Partner benefit: verified **incremental** bookings/visits, filled unused capacity, improved qualified leads; net benefit must account for discounts, commissions, service cost, no-shows and cannibalization.

**TO VALIDATE — E-003.** CitySense benefit: revenue from eligible transactions or later subscriptions vs customer acquisition cost, partner onboarding, API/provider fees, support, payment fees (where applicable), infrastructure, refunds/disputes and regulatory overhead.

**TO VALIDATE — E-004.** QR rooms offer a bounded acquisition experiment, not proven scalable distribution. Hotel/operator permission, economics, churn and permission to message visitors require separate validation.

## 8. November pilot scope and gates

**Goal:** A closed, real-tourist mobile pilot by November 30, 2026. The following are proposed readiness gates, NOT a claim of feasibility at current team capacity.

- **Gate 0 — Product contract:** Founder approves this blueprint after comparison with accepted ADRs and product docs, including explicit unresolved choices.
- **Gate 1 — Real evidence:** Legitimate place/entrance IDs, reviewed opening/availability/price and relevance features, rights/provenance, honest unknowns; existing engine preserved.
- **Gate 2 — Recommendation decision path:** Actual request → up to five eligible alternatives → documented constraint checks, explainable comparisons and a valid selection path; negative/abstention paths tested.
- **Gate 3 — Integrated mobile experience:** Chat/prompt, adjustable and comparable recommendation cards, MapLibre focus/highlight/evidence popup, routing where lawful/verified, graceful unavailable states; no unsupported "best experience" claims.
- **Gate 4 — Pilot operations:** Consent/privacy/access-control review, QR test placements with permission, decision-validity and time-to-decision instrumentation, support procedures, baseline evaluation and partner actions only where onboarded.

**DEFERRED/CONDITIONAL:** Citywide live crowd/noise maps, custom 3D assets, comprehensive wheelchair-safe routing, proven live traffic ETA, fully automated booking APIs, complete integrated marketplace payments, public launch, cross-city rollout. These remain part of the longer-term vision as relevant; no synthetic replacement is acceptable.

## 9. Repository reality from the October 10 strategic audit

The audit (a read-only snapshot; **not independently re-run for this blueprint**) reported: deterministic need-scoring engine, evidence provenance/replay, PostGIS and API contracts, Telegram command adapter, isolated MapLibre stage-1C experiment. No connected tourist web experience, real routing/ETA, public booking pipeline, maintained live city-state feed or validated partner conversion. Its retained quiet-rest real-data sample did not yield a scored recommendation. Exact implementation/file/line status must be verified by Codex in the live repository. The existing scorer and its weights are research hypotheses, not product-validated decision superiority.

## 10. Repository governance and Codex workflow

1. Use this blueprint as the **founder decision register**, after explicit reconciliation with existing architecture.md, accepted ADRs, research protocols and protected contracts; DO NOT silently replace them.
2. Each Codex ticket must cite relevant decision IDs, existing code/contracts, dependencies, evidence gates, tests and rollback; specify customer and partner consequences.
3. Separate **read-only analysis** from **authorized implementation**. No code, migrations, dependencies, branches, commits, or existing ADR rewrites without explicit task authority.
4. When technical experiments are scoped narrowly (e.g., map focus), show how they serve the overall request → choice → action flow, but do not implement unrelated product areas.
5. Treat claims of suitability, commercial performance, local data coverage, usability and legality as unverified until supported by appropriate evidence.
6. Maintain a dated decision log: `ID | status | decision | rationale | source | affected workflows | evidence needed | owner | last updated`.

## 11. Critical open decisions (do not silently assume)

- Which first use cases/attraction inventory are realistically verifiable for a tourist near Orbi City?
- Which routing and place-data providers lawfully cover Batumi at adequate quality?
- How to verify offers, slot freshness, expirations, double-booking, cancellation and partner response SLAs?
- How will third-party payment flow work: provider type, merchant of record, settlement, refunds, compliance?
- What equivalence rule for partner re-ranking preserves user satisfaction and disclosure requirements?
- What genuine early commercial commitments and data rights can each partner provide?
- Which user feedback and event data may be collected, under which legal basis and retention policy?
- What pilot sample, pre-declared VDCR criteria/denominator, comparator tasks and unbiased assessment rubric can actually be recruited from the 30 apartments?
- Team capacity, pilot budget, language/localization and accelerator-specific evidence requirements?

## 12. Decision log (seed)

| ID | Status | Decision or hypothesis |
|---|---|---|
| P-001–004 | DECIDED | Batumi tourist decision platform; evidence-first; partner/action-capable; mobile QR entry |
| G-001–002, G-004 | DECIDED | November closed pilot; Orbi City 30-unit opportunity; user-value-first |
| G-003, G-005 | PROPOSED / TO VALIDATE | Small rollout first; value vs current workflow |
| B-001–003 | DECIDED | Tours/attractions/sports courts; manual then API; authorized third-party payment processing |
| B-004–006 | TO VALIDATE / PROPOSED | Completed-booking commission; café offer redemption; small partner workspace |
| R-001–006, R-008–010 | DECIDED | Eligibility before partner priority; five default alternatives with honest fallback; map zoom/highlight and evidence panel; shared state; user-controlled selection; coverage-aware retrieval and layered validity |
| R-007 | TO VERIFY | Real dynamic/routing/accessibility data coverage |
| V-001, V-006 | DECIDED | Core pilot outcome is independently checkable constraint-valid, informed user choice; service satisfaction is not a primary KPI; keep decision/action/commercial outcomes separate |
| V-002–005 | PROPOSED / TO VERIFY | VDCR + time to valid decision; measurement instruments; baseline study; privacy |
| E-001–004 | TO VALIDATE | Stakeholder economic and acquisition value |

**Next action:** Founder review → Codex read-only conflict/traceability reconciliation against existing repository → approval of narrow changes → scoped implementation tickets.

## 13. Change log

- **v0.2 — 2026-10-10:** Founder corrected the meaning of "useful recommendation." Replaced post-service satisfaction / vaguely defined value as primary pilot KPI with **constraint-valid decision completion** and **time to valid decision**. Explicitly separated recommendation eligibility, auditable relevance, user-directed comparison, experience quality and commercial outcomes. Added R-008–010 and V-005–006; preserved original booking, payment, partner, QR and map decisions. Numeric ranking probabilities remain uncalibrated hypotheses.


## 14. Extensible services and agent-access strategy (v0.3)

**DECIDED — X-001. Platform extensibility.** CitySense must be designed as an extensible **place × service × provider × availability × action** platform, not a hardcoded list of tourism categories. This is an architectural requirement, not a claim that the integrations exist or have commercial agreements. Preserve the November pilot's narrower core user journey.

**DECIDED — X-002. Expandable service taxonomy.** Initial architecture must be capable of representing: travel eSIM/SIM offers and activation links; licensed/private tour operators; authorized drivers, private transfers and transport contacts; destination and partner contact details; paid experiences/sports facilities; future city-specific digital services. Each concrete category's product scope and implementation remains PROPOSED or DEFERRED until prioritized. No implicit assumption that independent drivers or tour providers are licensed, insured, available, or willing to contract.

**DECIDED — X-003. Single domain core, multiple clients.** Mobile PWA, Telegram bot/Mini App, partner workspace and future external AI agents should consume versioned, governed service/action APIs, not separately implement availability, ranking, booking or entitlements. A provider adapter / connector layer separates external inventory and fulfillment from the domain model. Do not prematurely build a generic plug-in runtime or force every domain into an impoverished single schema.

**DECIDED — X-004. Agent-ready interface.** Maintain machine-readable OpenAPI schemas for public/partner access where permitted and explore an MCP-facing adapter as a secondary distribution surface. Read-only tools (service discovery, details, eligibility, availability with freshness/provenance) are distinct from write tools (quote, request, confirm, cancel). Auth, scopes, partner permissions, user consent, usage quotas and audit are mandatory before external agent access. A tool schema alone is not an externally accessible service.

**DECIDED — X-005. Honest transactions.** Distinguish VERIFIED_CONTACT, INFORMATION_ONLY, REDIRECT_TO_PROVIDER, REQUESTED, PENDING_PARTNER, CONFIRMED, DECLINED, EXPIRED, CANCELLED, COMPLETED. Fulfillment must come from an authorized source. SIM/eSIM purchase and activation, transportation reservations and payments can have different provider/legal obligations; never simulate activation/availability/confirmation. No raw payment data handling or unapproved booking writes.

**DECIDED — X-006. Multi-city design without premature rollout.** City-dependent providers, locales, currencies, taxonomies, map coverage, law, rights and service-area geometry must be configurable by city/market. Stable globally unique entity IDs, versioned schemas, geo/timezones/currency and source provenance are essential. Batumi remains the only initial pilot market. No global scale claim until interoperability, supply acquisition, costs and regional legal feasibility are demonstrated.

**DECIDED — X-007. Human relevance over promotion.** Services can be candidates only if they genuinely fit a stated need and hard constraints; paid inventory must not bypass evidence and ranking rules. Disclose commercial relationships and price/availability uncertainty. Do not infer personalization attributes or collect location/identity beyond the purpose and consent.

**PROPOSED — X-008. Capability-oriented service contract.** Model a `ServiceOffering` connected to a `Provider`, `Place` or service area, `Capability`, `PriceQuote`, `AvailabilityAssertion`, `ContactChannel`, `ActionPolicy` and `EvidenceRecord`. Distinguish place-based offerings (court), mobile/on-demand services (driver), remote/digital services (eSIM) and informational contact listings; do not require all offerings to have a single geographic point. Extend through category-specific validated attributes rather than dozens of nullable universal columns.

**PROPOSED — X-009. Connector lifecycle and trust.** `DISCOVERED -> CONTACTED -> APPROVED -> TESTING -> ACTIVE -> SUSPENDED/REVOKED`; per-connector capability negotiation, sandbox contract tests, inventory freshness, error handling, rate limits, rights records and revocation. Do not publish partner contact details or integrate private endpoints without authorization.

**PROPOSED — X-010. Phased implementation.** Phase A: schema and interfaces compatible with the current registry, read-only service discovery and verified contacts, no agent write tools. Phase B: partner-verified availability/request workflows for one narrow segment. Phase C: eSIM/private transfer partner integrations following signed terms, legal review and provider sandbox tests. Phase D: independently authorized external agent API/MCP actions, tenant scopes and monitored production reliability. Stages require founder gates; they are not automatic scope for November.

### External AI agent safety and contracts

- OpenAPI must document version, errors, idempotency requirements, pagination, locale/currency/timezone and field-level provenance/freshness.
- External MCP/tools must expose clearly bounded capabilities and indicate unsupported or unverified fields. Tool outputs are untrusted content; follow authorization and prompt-injection boundaries.
- Split *informational reads* from *consent-bearing actions*. Any action with booking, purchase, disclosure of personal information or third-party fulfillment must require appropriate authority, explicit end-user confirmation where relevant and auditable consent.
- Never allow a client/agent to assert a booking as CONFIRMED based solely on its own request. Provider confirmations are authoritative.
- Apply authentication, least-privilege authorization, consent, tenant isolation, request signing where appropriate, rate limiting, replay prevention, logs with minimal personal data, and documented revocation/incident workflows.
- Permit controlled access to verified content only within data-provider licensing and redistribution rights; an internal map tile or booking API license does not imply external AI-agent redistribution permission.

### Service category readiness matrix

| Segment | Strategic place | November pilot commitment | Dependency before activation |
|---|---|---|---|
| Tours, paid attractions, sports courts | Initial commercial segments | Discovery pilot; manually verified actions only if partners authorized | Provider identity, data rights, current prices/slots, confirmation terms |
| Driver/private transfer | Priority future service vertical | Deferred | Verification, licensing/insurance checks, service geography, quoting, consent and fulfillment |
| eSIM/SIM | Future digital service vertical | Deferred | Reseller/affiliate contract, coverage/activation/refund rights, compliance and payment topology |
| Partner contacts | Cross-cutting metadata/action | Verified public or permissioned contacts only | Accuracy, permissions, phone/link safety, updated timestamp |
| Agent-facing public access | Long-term platform distribution | Interface-readiness only | Versioned contracts, auth, quotas, consent, data redistribution rights, security validation |

### New founder decisions and open questions

The platform-level extensibility direction is approved; the **specific monetization, launch order, commercial terms, suppliers, API endpoints, city expansion order, agent access policies, and November scope expansion are not approved**. Chief Engineer must record these as unknowns and prohibit domain-specific implementations without a separate ticket.

## 15. Version history
- **v0.3 — 2026-10-10:** Added extensible digital services, transportation, SIM/eSIM, contact channels, versioned external agent access and multi-city architecture as strategic constraints; no implied November MVP feature or provider authorization.
- **v0.2 — 2026-10-10:** Retained the prior experimental and booking decisions, including constraint-valid user decisions as pilot north star.


## 16. Founder-Gated Product and UX Acceptance (APPROVED — governance addition, 2026-10-10)

**P-005 DECIDED:** CitySense development uses sequential founder-controlled stage gates: scope approved first, work performed within that scope, technical QA, founder evaluation of concrete outcomes, and explicit approval before the next stage. No agent, including the Chief Engineer, may infer approval from silence, reports, green tests or roadmap position. Approval is specific to stage and artifact version; changed requirements need a new recorded decision.

**P-006 DECIDED:** UI/UX and cartographic presentation require visual founder approval at distinct design checkpoints before broad production implementation. Review must use genuine rendered previews and reproducible demos where available, at representative mobile/desktop viewports, with realistic and rights-compliant Batumi data; no fabricated map evidence. Design quality and usability are separate acceptance dimensions from code correctness.

**P-007 DECIDED:** Scope changes and new ideas must be logged, evaluated for impact across modules and approved before entering implementation. The Chief Engineer curates dependency-aware stage packets and a durable decision record; specialist agents cannot change accepted product outcomes through incidental technical decisions.

**Implementation status:** governance procedures require repository bootstrap and verified enforcement; these additions alone do not mean an executable agent team or CI permission gate is installed.

### Version history addition
- **v0.4 — 2026-10-10:** Founder-directed sequential stage authorization, mandatory visual UX review and formal change control. Carries v0.3 service extensibility decisions forward unchanged.
