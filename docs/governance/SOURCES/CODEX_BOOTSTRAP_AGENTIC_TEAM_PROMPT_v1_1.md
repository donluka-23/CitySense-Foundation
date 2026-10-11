# Codex — CitySense Agentic Engineering Team Bootstrap (Governance-First)

Repository: `D:\citysense-foundation`
Attachments: `CITYSENSE_AGENTIC_ENGINEERING_OPERATING_SYSTEM_v1_1.md` and `CITYSENSE_PRODUCT_BLUEPRINT_v0_3.md`.

You are acting as Chief Engineer / Integration Orchestrator. The goal is to create a durable, low-context, multi-role engineering operating system inside the existing repository. This is NOT a request to implement the entire MVP, redesign the map, enable payments, or declare a production launch.

## Hard operating rules
1. FIRST inspect the actual repository, active changes, accepted ADRs, protected research protocols, latest Sprint 3 and mapping Stage 1/1B status, exact existing Codex configuration, and source/rights restrictions. Do not assume reports are current. Do not reuse unrelated legacy web-demo code.
2. Read the two attached governance and product files fully. The Product Blueprint holds founder decisions; the governance proposal specifies a method. Do not silently supersede protected contracts or accepted ADRs. Distinguish proposed architecture from implementation reality.
3. Do a **read-only reconciliation and conflict report first**. Report any material contradiction with exact file path and clause, propose options and STOP if a founder decision is required. Routine additive documentation may proceed only if within explicit scope and nonconflicting.
4. **I authorize additive governance documentation and agent-config files only** after the conflict scan, not feature-code, DB, provider, payments, deployment, Git init, or modifications to accepted ADR/protocol. Preserve the user's uncommitted changes.
5. Check current installed Codex multi-agent/subagent, AGENTS.md, skills, MCP and branch/worktree support using actual local documentation/capabilities. Never invent config keys or claim workers are live when only profiles were written. If uncertain, produce portable role docs and instructions to enable safely instead of untested configuration.
6. Keep root `AGENTS.md` concise (<=120 lines), mostly link/navigation and invariant policy. Do not place the entire product blueprint in it. If existing AGENTS.md exists, inspect and merge carefully without replacing user-defined constraints.
7. Create thin project governance with stable ownership and explicit contracts, not an elaborate task management framework requiring continuous busywork.

## Required structure (adapt paths to repository conventions)
- `docs/governance/PROJECT_CHARTER.md`
- `docs/governance/DECISION_REGISTER.md` (keep decision IDs and statuses, do not reclassify founder approvals)
- `docs/governance/STATUS.md`
- `docs/governance/PORTFOLIO_BOARD.yaml`
- `docs/governance/INTERFACE_REGISTRY.yaml`
- `docs/governance/INTEGRATION_MATRIX.md`
- `docs/governance/RELEASE_GATES.md`
- `docs/governance/HANDOFF_TEMPLATE.md`
- `docs/governance/CHANGE_REQUESTS/README.md` and `CR-TEMPLATE.md`
- `docs/governance/ROLES/` role files for Chief, Product/Research, Geospatial, Data, Decision Engine, Mobile PWA, Telegram, Partner/Booking, Security/QA.
- Root `AGENTS.md` as short project route guide if appropriate.
- Optional `.codex/agents/` profiles/config only if verified supported by current installed Codex. Provide compatibility fallback.

## Team orchestration semantics
The Chief receives founder requests, identifies impacted decision IDs, assigns one owner per write area, resolves dependencies, enforces shared interface versions, delegates bounded tasks and summarizes handoffs. Workers read only scoped tickets, their specific contracts and necessary code. Worker deliverables must include changed files, actual executable tests, evidence, open risks and integration implications.

For independent audits, explicitly spawn specialized subagents IF multi-agent execution is available and safe. Do NOT parallelize writes to the same files, and do not spawn agents simply to create an appearance of teamwork. If unavailable, document manual multi-session protocol instead. Any Git worktree setup requires an actual valid Git repo and clean ownership conventions; never silently initialize Git.

Create or update a master lifecycle:
`IDEA_INBOX -> TRIAGED -> CR_DRAFT -> FOUNDER_APPROVED -> CONTRACT_READY -> TASK_READY -> IN_PROGRESS -> INTEGRATION_REVIEW -> QA -> HUMAN_ACCEPTED`.
Minor internal repairs can be governed proportionately; material product, science, commercial ranking, privacy, vendor and payment changes always require explicit approval.

## Product invariants
- Batumi tourist mobile QR-first PWA, November supervised closed pilot target; 30 Orbi City A Block apartments are distribution opportunity, not permission or participant count.
- User-first constraint-valid decision and efficiency, not claim of objectively best experience.
- Up to five honest results; no fabricated fifth, unjustified fixed retrieval truncation or missing-data guessing.
- Shared synchronized selected-place context among cards, map, chat, route and actions.
- Professional map visuals with lawful geodata; no fake local 3D/weather/wind/heatmaps.
- Verified offers and manual partner confirmation first; tours/attractions/paid sports courts initial partner categories; restaurants optional experiment.
- No payment handling without authorized provider and legal approval.
- Suitability scores unvalidated; frozen B0 and protected research protocol preserved; baseline work distinct from product pilot.
- One backend API/domain engine reused by PWA/Telegram/agents; no parallel scorers.

## Mandatory checks
- Governance consistency: every workstream references charter and at least one affected decision or verified uncertainty.
- Explicit status separation: DECIDED ≠ IMPLEMENTED; TESTED ≠ PILOT VERIFIED.
- Interface ownership: no undefined producer/consumer or silent breaking change.
- Stage boundaries: cartography and UX can be reviewed independently but vertical slice is integrated.
- Each scoped task defines dependencies, protected files, rollback, test plan, human gate.
- Reports and evidence do not claim tests were run when they weren't.
- Verify governance YAML syntax and links; run existing lightweight quality checks if practical without modifying code.

## First execution and stop point
A. Perform read-only audit and decision/ADR conflict scan.
B. Install only safe additive governance artifacts within the authorization above.
C. Prepare a **proposed**, not automatically executing, dependency-ranked 3-week work plan for November-pilot readiness, including owners and clear blockers.
D. Propose at most THREE next engineering tickets for founder approval, prioritizing a coherent QR -> need -> eligible shortlist -> map focus -> informed selection vertical slice, a rights-cleared place inventory, and visual cartography approval.
E. Give a compact Chief Engineer status report: actual files created, config validated, agents truly spawned vs merely defined, exact tests, conflicts, founder decisions needed, and next task recommendation.

STOP. Do not launch the engineering tasks, Stage 2, provider integrations, Telegram work, booking or deployment without approval.


## Addendum — mandatory v0.3 extensibility reconciliation
- Treat strategic support for eSIM/SIM, private guides/tours, drivers/transfers, partner contacts, service areas and future city markets as **approved architecture direction**, not authorization to launch these products.
- Inspect actual Place/Opportunity registry, API schemas, adapter boundaries, Telegram and authentication, and draft an ADDITIVE extension RFC for `ServiceOffering`, `Provider`, `Capability`, `AvailabilityAssertion`, `ContactChannel`, `ActionPolicy`, and provenance/freshness. Explain what the existing system already does; do not assume these entities need their own tables or implement migration now.
- Add **Service Platform & Integrations** and **Agent Interface & Ecosystem** as bounded role contracts. Capture exact producer/consumer/schema/owner for internal REST, future public OpenAPI and potential MCP adapter. Existing read-only in-process agent prototype does not mean external access is released.
- Produce `docs/governance/SERVICE_PLATFORM_EXTENSION_RFC.md` and `docs/governance/AGENT_ACCESS_BOUNDARIES.md` as proposed documents only, and link them from the interface registry and portfolio plan. Include city, locale/currency, point vs service-area vs digital offering, rights, partner approval, authentication/authorization, user confirmations, rate limits, idempotency, audit and API contract tests.
- Explicitly defer building eSIM activation, transport booking, payments, external agent write calls and multi-city rollout. Do not let framework building delay the November tourist choice pilot.
- Report every blueprint/ADR conflict and founder-gated choice rather than silently reconciling it.
