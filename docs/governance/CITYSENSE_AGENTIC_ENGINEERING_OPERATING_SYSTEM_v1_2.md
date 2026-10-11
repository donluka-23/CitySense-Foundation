# CitySense Lab — Agentic Engineering Operating System (AEOS)
Version 1.1 · 2026-10-10 · PROPOSED governance system (not yet installed)

## Mission and source hierarchy
Preserve the founder-approved product vision while allowing narrow independent technical work. Founder decisions remain in `CITYSENSE_PRODUCT_BLUEPRINT_v0_3.md`; accepted ADRs, protected research protocol and actual code govern their respective domains. No new governance text silently supersedes an accepted ADR. Decision status (DECIDED/PROPOSED/TO VALIDATE/TO VERIFY/DEFERRED) differs from implementation status (UNBUILT/IN_PROGRESS/TESTED/PILOT_VERIFIED). Conflicts are escalated, not guessed.

**North-star product:** Batumi tourist scans an accommodation QR, describes a need, gets *up to five* defensible, constraint-valid, high-relevance alternatives, compares them on a synchronized detailed mobile map with source freshness and unknowns, selects a feasible option, and optionally acts through a verified partner. No forced five, invented weather/availability/route, or commercial influence on basic suitability. November 2026 target: closed, permissioned pilot, not production launch. Orbi City A Block 30-apartment distribution opportunity remains unverified for actual permission, occupancy and pilot access.

**Primary experiment:** Independent Valid Decision Completion Rate (VDCR) and Time to Valid Decision, definitions and measurement instrument subject to approval. Do not conflate selection, attendance, satisfaction, or paid conversion. Long-term API/agent infrastructure and research A1/B1 remain in scope but must not displace the MVP outcome.

## Architecture pattern: small context, explicit contracts
```
Founder / product owner — approves scope, tradeoffs, major changes
             |
Chief Engineer / Orchestrator — owns dependency graph and integration gates
             |
   +---------+----------+---------+---------+---------+
   |         |          |         |         |         |
Map/Geo   Evidence   Decision   Client UX PartnerOps  Platform/QA
             & Data   & Research  Web/Telegram Booking   Security
```
These are logical responsibilities, not proof that persistent autonomous agents are running. They may be executed as Codex subagents when supported, or as separate Codex sessions using scoped tickets. The chief owns cross-team conflict resolution and integration; reviewers do not self-approve their own changes. Product owner remains the final gate.

### Role contracts
| Role | Primary owned scope | Required inputs | Required output | Must not do |
|---|---|---|---|---|
| Chief Engineer | priorities, integration, contracts, ADR conflicts, technical roadmap | brief, decisions, handoffs, CI | approved plan, integration report, escalations | silently override founder/ADR |
| Product & Research | needs, eligibility definitions, pilot metrics, real-user study | blueprint, consent restrictions | acceptance scenarios, research gate | relabel proxies as truth |
| Geospatial/Cartography | basemap, camera, symbols, clusters, routes, visual evidence | geo contracts, rights, design refs | map adapter contract, snapshots, benchmark | invent spatial heatmaps |
| Evidence/Data | POIs, source validation, time, quality, rights, entity IDs | source register, API schemas | bounded verified candidate snapshots | bypass license/privacy controls |
| Decision Engine | candidate retrieval, constraint checks, ranking, uncertainty | frozen B0, model API, feature provenance | scored/abstained versioned decisions | change protected engine casually |
| Mobile Experience | QR PWA, five-card compare, accessible map/chat state | approved design, API contract | screenshot-tested mobile workflow | duplicate scoring client-side |
| Telegram | command bot, future Mini App bridge, auth, shared API | PWA and backend contracts | tested adapter | build separate recommendation logic |
| Partner Operations | supply onboarding, slot status, manual confirmation, eventual booking | consented partner terms, registry | status transitions, idempotency, audit | assert booking/charge without confirmation |
| Platform/Security/QA | auth, CI, reliability, rights, privacy, reproducibility | all interface diffs | independent gates and incident risks | treat local tests as hosted evidence |

## Mandatory artifacts in repository (small, machine-readable where possible)
- `AGENTS.md`: <= 120 lines, navigation rules only, no giant manual.
- `docs/governance/PROJECT_CHARTER.md`: stable why, who and north-star flow; links to full blueprint.
- `docs/governance/DECISION_REGISTER.md`: decision ID/status/date/owner/source/supersession.
- `docs/governance/PORTFOLIO_BOARD.yaml`: initiative IDs, owner, dependencies, stage, gate, blocker, evidence location.
- `docs/governance/INTERFACE_REGISTRY.yaml`: producer, consumer, schema/version, compatibility and test owner.
- `docs/governance/CHANGE_REQUESTS/CR-XXXX.md`: impact assessment and founder approval.
- `docs/governance/INTEGRATION_MATRIX.md`: full user-journey seams and coverage.
- `docs/governance/RELEASE_GATES.md`: quality/security/legal/UX/pilot gates.
- `docs/governance/HANDOFF_TEMPLATE.md`: scoped agent-to-agent message schema.
- `.codex/agents/*.toml` and `.codex/config.toml` only if installed Codex supports them; use exact locally verified syntax. `docs/governance/ROLES/*.md` portable alternative.
- `docs/governance/STATUS.md`: concise confirmed/blocked/next report, edited only by Chief.

## Ticket contract (mandatory)
`ticket_id, founder_decision_ids, user_outcome, scope, owned_paths, read_only_dependencies, inputs/contracts, prerequisites, forbidden_changes, tests, screenshots/evidence, acceptance criteria, rollback, delivery_state, open_questions`.
Only the Chief creates integration tickets after checking dependencies. A technical agent receives 1–2 page ticket + relevant schemas, not the full conversation. Agent may read necessary repository code, but may not reinterpret the commercial roadmap.

## Changes arising midstream
1. Record a new idea as INBOX; do not automatically rewrite roadmap or code.
2. Product owner classifies DECIDED / PROPOSED / TO VERIFY / etc.
3. Chief prepares CR describing value, affected user journey, interfaces, ADR conflicts, cost, sequencing and test changes.
4. If no founder approval on cross-domain change: branch/ticket remains BLOCKED, not silently implemented.
5. Approved CR increments relevant contract versions, updates impacted tickets, docs and tests.
6. Chief integrates changes and ensures product remains coherent end to end.
Emergency security fixes may be triaged immediately, with exact documented scope and retrospective review.

## Handoff (no global chat replay)
A worker returns a compact structured handoff:
```
Ticket ID:
Decision IDs:
Changed paths (or read-only):
Contracts consumed/produced and version:
What actually runs:
Tests and screenshots/evidence paths:
Data source/rights/temporal caveats:
Remaining risks/blockers:
Upstream/downstream implications:
Requested Chief decision:
```
No fabricated results or invisible dependencies. Chief records merge conflict/API changes in central registry.

## Multi-agent execution and integration
Parallelize only independent tasks with disjoint write ownership. Reserve contracts shared by two teams for Chief-approved sequential editing. Run branches/worktrees if actual Git repository supports them; if absent, first ask approval before Git initialization and never allow concurrent agents editing same working tree. Prefer short lived task agents over permanent context-heavy conversations. If subagent features unavailable, use separate scoped sessions and the same handoff template. Never assume Codex can autonomously notify one isolated session of another session's edits.

## Cross-domain invariants and integration tests
- One user/request/selected-place context across map, shortlist, chat, route and partner action. Stale async responses discarded.
- Ranking: retrieve eligible universe robustly; hard constraints before soft ranking; no arbitrary ID cutoff; up to five defensible choices; allow more/refinement; unknown critical attributes not presented as verified.
- Business influence: suitability independent of commission; disclosed partner priority only among materially equivalent alternatives and only after approved policy.
- Live data: rights and temporal validity, honest missingness; synthetic data explicitly segregated.
- Partner booking: `REQUESTED -> PENDING_PARTNER -> CONFIRMED -> COMPLETED` with decline/expiry/cancel exceptions. Booking request is not confirmation; payment not live until authorized provider/legal clearance.
- QR attribution: anonymous, minimum data, permission/retention review.
- Science: B0 unvalidated, real A1 pending until evidenced, no claimed predictive advantage.
- Visual QA: approved Figma/reference package, professional basemap and truthful geospatial layers, mobile screenshots inspected by human before release.
- Each PR/change links decision ID, API schema/test, owner, rollback, and current release gate.

## First rollout (proposed, approval required)
G0: Chief reads real repo + blueprint, snapshots status and active changes; read-only audit.
G1: Install governance skeleton and documented roles; check Codex tool support, no feature code edits.
G2: Create 4–6 narrow pilot tickets ranked by dependencies; founder approves.
G3: Parallel safe investigations: Batumi inventory/rights, map UX evidence, QR pilot access & user task definitions. Shared interfaces frozen before implementation.
G4: Implement vertical slice QR -> need -> up to five honest choices -> compare/map focus -> verified selection, with independent QA.
G5: Add manual partner availability requests after partner commitments; payment only after legal/provider gates.

## Portfolio operating rhythm
At each session start, Chief reads STATUS, BOARD, last accepted blueprint + relevant ADRs, changed API contracts and current blockers. At task close Chief updates STATUS, board, integration matrix and unresolved founder questions. No attempt to keep all agents synchronized by copying whole chats.

## Honest limitations
Agent roles and files reduce context loss but do not create an always-running independent team, enforce quality automatically, guarantee clean parallelism, or substitute for founder approvals, field evidence, rights reviews and real CI. Budget concurrency and cross-role review explicitly.


## v1.1 Extension: Service Platform & External Agents

The core is *not* one monolithic tourist chatbot. Shared contract boundaries: `UserNeed -> Eligible Discovery -> ServiceOffering -> Evidence/Availability -> ActionPolicy -> Provider Confirmation`. Represent geographically fixed places, service areas/on-demand drivers and remotely fulfilled digital products without falsely assuming all have a map pin. Keep current Place Registry and frozen evidence models intact; introduce proposals through migrations/ADRs, not broad rewrites.

### Additional workstream ownership
- **Service Platform & Integrations** (new bounded workstream): owns provider adapters, service taxonomy/capability registry, external connectors, fulfillment state, public contact data policies, per-city configurability. Interfaces with Evidence/Data, Partner Operations, Security and Product. Does not own suitability weights, visual map styles or payments.
- **Agent Interface & Ecosystem** (new bounded workstream): owns versioned OpenAPI surface, optional MCP adapter, auth/scope boundaries, tool permissions, agent action confirmation/audit and compatibility tests. Does not publish unrestricted tools or bypass end-user approvals.
- **Chief Engineer**: maintains Interface Registry entries for read discovery, get offering/details, request availability/quote, initiate action, booking status and partner callback with producer/consumer, data rights, contract version and test owner; detects privacy and ranking conflicts.

### Capability and rights gates
Every proposed category/integration receives a capability card: market/city, provider, offering schema, location model (point/service-area/digital), verified contact, quote/price freshness, availability authority, allowed actions, disclosure/consent, permitted clients (PWA/Telegram/agent), legal/rights owner, SLA or unknown, tests, status. No vendor integration, token use, purchase path or fulfillment action can be enabled without documented authorization, tests and founder approval.

### Architecture evaluation before implementation
Chief Engineer must audit existing API/registry schemas, classify minimally compatible extension points, and propose additive versioned contracts. Reject a rewrite of Sprint 1–3 solely to achieve an abstract 'platform'. Demonstrate one end-to-end service offering across PWA and one read-only machine-client test *before* building broad provider abstractions. No automatic public-agent deployment.

### Change intake for new ideas
New categories (eSIM, rides, private drivers, contact methods, external agent actions) enter `IDEA_INBOX -> TRIAGE -> IMPACT/RIGHTS REVIEW -> FOUNDER DECISION -> CONTRACT -> TICKET`, with explicit MVP scope effect and dependency map. Record independently whether strategic inclusion was decided versus implementation still deferred.


## v1.2 Mandatory Founder-Gated Sequential Delivery (APPROVED GOVERNANCE POLICY)

**Non-negotiable:** Only the founder authorizes progression between delivery stages. A technical PASS, elapsed time, agent agreement, silence, or CI green state does **not** constitute founder approval. Changes are approved for one explicitly bounded stage only. Every new phase begins in `BLOCKED_AWAITING_FOUNDER_APPROVAL` until a written decision cites the exact stage ID, artifact version, and approved scope. The Chief Engineer can prepare a next-stage proposal but cannot start its implementation while blocked.

**Stage lifecycle:** `DRAFT_PLAN -> READY_FOR_SCOPE_REVIEW -> APPROVED_TO_EXECUTE -> IN_PROGRESS -> TECH_QA -> FOUNDER_REVIEW -> APPROVED_COMPLETE | CHANGES_REQUESTED | REJECTED | ON_HOLD`. A revision returns to the same stage; scope increases require a separate change request and fresh approval. Never auto-chain stages or treat approval of a plan as approval of its successor.

**Stage packet required for Founder Review:** `stage ID; goal and user value; original approved scope; completed and uncompleted work; actual demo/working URL and reproducible run command (if applicable); dated screenshots/video at desktop and mobile sizes; data provenance and source rights; tests and failures; security/accessibility/performance knowns and unknowns; deviations; risks; before/after comparisons; dependencies; next-stage proposal; specific decision requested`. Do not mark something verified merely because a screenshot looks correct. Link to evidence paths that actually exist. Chief Engineer explicitly identifies what requires visual or real-device judgment.

**UI/UX special gates (human review mandatory):**
1. `UX-0` reference board, user journeys, constraints, design principles, anti-patterns and real authorized reference source inventory -> founder approves direction before screen design.
2. `UX-1` low-fidelity flows and navigation, PWA vs Telegram entry, map/search/card/compare state transitions -> founder approves interactions before high-fidelity exploration.
3. `UX-2` high-fidelity *distinct* visual alternatives based on actual production basemaps and realistic Batumi content, mobile-first; screenshot/preview at stated viewports -> founder selects or rejects a visual direction. Avoid made-up cartography or AI-generated pseudo-screens accepted as working UI.
4. `UX-3` implementation of **approved** design system and interactive prototype; screen-by-screen visual diff with approved refs, localization, empty/unknown/error/loading states, touch, a11y -> founder signs off before broad functional integration.
5. `UX-4` verified end-to-end app journey with real or explicitly sandboxed data, mobile-device QA, honest provenance and required attributions -> founder pilot readiness decision.
Each UX gate is separately approved; a screenshot/automated test is supportive evidence, not automatic acceptance. Map provider Stage 1B remains independent and must be closed or explicitly waived with noted risks before any map visual-style sign-off.

**Change protocol:** novel founder ideas are entered as `CR-###` with linked blueprint requirement, user impact, affected workstreams/contracts, scope/time/risk estimate, alternatives and proposed stage. Only the founder can accept scope/budget/schedule trade-offs; approved CRs revise stage contracts and test plans. Never silently reclassify `PROPOSED` to `DECIDED` or alter the November pilot. Emergency security fixes may be proposed urgently, but are not authorization for unrelated changes.

**Persistent ledger:** `docs/governance/FOUNDER_APPROVALS.md` stores immutable append-only decision entries (`timestamp, decision-maker, exact stage/CR ID, artifact version or commit, APPROVE/CHANGES/REJECT/HOLD, scope, conditions`). `docs/governance/STAGE_GATES.md` stores the current gate, evidence links, and next allowed action. If governance files do not exist, create only during explicitly authorized bootstrap. Absence of a recorded approval means blocked; historical chat inferences are not substituted for recorded stage authorization.

**Multi-agent integration:** workstream agents can research, test and implement only within their approved stage ticket and assigned surfaces; Chief Engineer owns cross-workstream compatibility checks and submits one stage packet. Agents must not tell downstream agents to proceed before the founder's stage approval. Parallel independent tasks inside one approved stage are permissible where safe; sequential gates are mandatory across stages.
