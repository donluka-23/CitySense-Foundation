# Integrated tourist journey acceptance matrix

Charter: [PROJECT_CHARTER](PROJECT_CHARTER.md). Decision IDs P-004, R-001–010, V-001/V-006, X-003/X-005.
These are future acceptance seams, not claims of completed integration.
Chief coordinates producer/consumer compatibility; independent QA and human review accept the integrated result.

| Seam | Owner / producer → consumer | Current evidence | Future acceptance / gate |
|---|---|---|---|
| QR → mobile request | Mobile → PWA session | UNBUILT; rooms/access unverified | Permissioned entry, no install, minimum attribution/identity; FA-03/04 |
| Need → essential constraints | Product + Decision → shared request service | Current engine has only three research Need values; no tourism parser | Approved parsing/clarification and hard/soft vocabulary; unknown required constraints explicit |
| Retrieval → eligible set | Data + Decision → request service | Existing /v1 stable-ID search limit≤30; CF-03 | Reviewed wider pool/coverage before shortlist, time/budget/access/operational constraints; compatibility approval |
| Evidence → eligibility/explanation | Data → Decision/PWA | Numeric stored-evidence temporal/rights gates implemented; real contexts abstain | Lawful current task facts, entrance meaning, no unknown/stale safety as satisfied; T-02 |
| Eligible set → alternatives | Decision → PWA | Deterministic unvalidated research engine; no tourist shortlist | Single backend policy, honest up to five/fewer/no results; relevance audit and no arbitrary cutoff |
| Cards/chat/refinement → map/panel | Mobile + Cartography → selected state | Stage 1C isolated camera experiment | Request revision/candidate/evidence identities, persistent map, correct supplied target, stale-response denial |
| Map → visual/accessibility acceptance | Cartography → mobile user | Conditional desktop qualitative acceptance; raw strict/mobile evidence missing | Lawful attribution/reference, reduced motion, true provider extrusions, independent physical-device/human review; T-03 |
| Selection → decision validity | Product/Research → pilot audit | No product-pilot instrument | Approved independent required-criterion checks; denominator retains unknown/unfinished/abstained; CF-01 |
| Route/ETA/access | Future adapter → PWA | UNIMPLEMENTED; caller walk estimates only | Show unavailable unless lawful verified route/travel/access coverage; never fabricate |
| Contact/offer → optional action | Integrations + Partner → user | Contracts only | Verified publication/contact safety; truthful information/redirect/request statuses; FA-08 |
| Request → provider confirmation | Partner → action service/user | NO RUNTIME/PARTNERS | Authority, terms, consent, idempotency/expiry/hold/callback tests; no request-as-confirmed |
| Shared domain → Telegram | Platform → private adapter | Historical tests, three-result cap; real bot unverified | Preserve accepted cap/mode/rights; future extension separately scoped |
| Shared domain → external API/MCP | Platform + Agent Interfaces → external client | In-process tools only | Versioned auth/tenant/rights/quota/consent and security gates; no public release |

## Current coverage

Component tests are historical; they do not establish the future seams above.
Current contract export parity is in BOOTSTRAP_VERIFICATION.json.
No integrated PWA screenshots, Android/iOS tourist flow, real ranking-accuracy study, booking receipt or MCP transport exists.
Populate actual evidence paths and environment/time at each authorized integration gate; do not mark proposed paths delivered.

Minimum negative cases: missing/stale/denied evidence, fewer/no candidates, invalid time, wrong geometry meaning,
out-of-order/refined requests, interrupted network/context loss, operator-key leakage, unsafe contact links,
expired/unconfirmed action and cross-client policy drift. Only relevant cases execute after scoped authorization.
