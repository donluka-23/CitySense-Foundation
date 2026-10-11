# Repository reconciliation and founder gates

2026-10-10; read-only scans by Chief, product/contract, service/security and map/QA auditors.
Existing code, protocols, ADRs and receipts remain unchanged. Safe additive governance proceeds.
All options below are proposals; approval is required before the affected contract changes.

## Material conflicts

| ID | Approved direction | Existing protected clause/behavior | Gated recommendation |
|---|---|---|---|
| CF-01 | Blueprint V-001/V-006: constraint-valid informed selection; service satisfaction not primary | docs/evaluation-protocol.md lines 4/10/22: experienced suitability, post-exposure ratings, paired-choice accuracy; docs/architecture.md research goal | Separate named product-pilot protocol from protected research. Approve estimand/instruments/priority; do not rename current evaluation/harness. |
| CF-02 | R-002: disclosed commercial priority among materially equivalent suitable alternatives | docs/OPPORTUNITY_REGISTRY_DESIGN.md lines 46–47 prohibits commission/attribution changing ranking; ADR-0009 boundaries excludes commission from organic ranking; architecture.md | Keep priority inactive. Approve whether a distinct disclosed presentation layer may reorder equivalents; define evidence/tolerance/disclosure. Preserve organic scores/order/hash. |
| CF-03 | R-009: no arbitrary early ID cutoff before suitability | docs/OPENAPI_CONTRACT.md bounds: stable-ID sort, limit ≤30, no cursor; platform.py search ORDER BY p.id LIMIT; ADR-0009 requires /v2 for breaking semantics | Approve additive recommendation retrieval/coverage policy or /v2. Do not repurpose current /v1 search semantics. |

Links: [protected protocol](../evaluation-protocol.md), [opportunity policy](../OPPORTUNITY_REGISTRY_DESIGN.md),
[API](../OPENAPI_CONTRACT.md), [ADR-0009](../adr/0009-agent-first-platform.md),
[platform](../../services/api/src/citysense/platform.py).

## Extension gaps and scope tensions

- CF-04: X-008 service-area/digital proposal cannot use point-required ProviderEntity honestly
  (opportunities.py ProviderEntity requires place_id/city_id/Geometry). Proposed additive versioned contracts,
  no weakened fields/migration. [RFC](SERVICE_PLATFORM_EXTENSION_RFC.md).
- CF-05: R-003 up to five PWA options versus TELEGRAM_DEMO_SPEC three-result private cap.
  Separate channels can coexist; preserve Telegram. Five shortlist does not change exactly-two comparison API.
- CF-06: tourist-first positioning versus agent-first architecture. A tourist client over one shared
  backend is compatible; existing infrastructure does not implement that client. No ADR rewrite.
- CF-07: historical quiet-rest/A1 next-step research priority versus November tourist choice direction.
  Preserve delivery-plan.md and protocol; approve product-pilot task and capacity allocation separately.
- CF-08: append-only research evidence versus future deletion/revocation of restricted partner/personal data.
  Do not store new revocable data there by default; approve retention/archival policy before collection.
- ADR-0009/0010 exclude booking/model parser runtime in their sprint scopes. Future strategic support
  is an extension direction, not current permission to change those boundaries.

## Historical receipts versus present facts

Git now exists: branch stage/1c-map-navigation, HEAD eadf331e4b7c262fb5c2216d051f7f6e56a456bf,
baseline 0e0440a28b2d1c82a70aa545c3e8bf3479e0cea0; no remote output; initial working tree clean.
HEAD adds Stage 1C's nine files. Earlier no-Git/uncommitted statements remain dated history.
No merge/publication or hosted CI success follows. Stage 1D approval/report was not found in repository.
Stage 1C has conditional desktop qualitative acceptance; strict raw measurements and physical mobile remain unverified.

## Founder decision queue (all PENDING)

| ID | Decision needed | Blocks |
|---|---|---|
| FA-01 | Separate product protocol and research priority; approve VDCR/TVD definitions, required-criterion audits, denominator/exclusions, comparator and no numeric claims without evidence | CF-01/07; instrumentation and pilot evaluation |
| FA-02 | Choose first tourist tasks/inventory near Orbi, supported constraints/languages, staffing and budget; keep no-data fallback explicit | T-01, T-02; feasible shortlist |
| FA-03 | Confirm QR placement/access/occupancy, supervised recruitment and rollout size (3–5 is proposed) | Tourist exposure |
| FA-04 | Approve minimal events, consent/notice, location use, retention, withdrawal/deletion, access and archival rights | CF-08; participant collection |
| FA-05 | Resolve commercial ordering/equivalence/disclosure; leave inactive if not needed | CF-02; commercial priority |
| FA-06 | Select compatibility/version path for coverage-aware retrieval and future constraint representation | CF-03; T-01 contract readiness |
| FA-07 | Approve lawful visual reference/provider/capture rights, target physical devices and acceptance scope; Stage 2 remains a separate later gate | T-03; map integration |
| FA-08 | Choose November information/verified-contact scope versus a separately authorized manual partner request; verify actual partners/terms | Partner/action release |
| FA-09 | Approve any specific additive service schemas/endpoints/rights/access policy after RFC review; strategic inclusion is already decided | CF-04; future services/public reads |
| FA-10 | Explicitly authorize at most three next tickets and their scope after governance review | All engineering execution |

Payment topology, suppliers, eSIM/driver launch order, external writes and new cities require future separate decisions.
No governance approval automatically authorizes these features.

## Approved-source intake overlay — 2026-10-10

See [v0.4/v1.2 reconciliation](GOVERNANCE_RECONCILIATION_v0_4_v1_2.md) for exact three proposals,
affected files, backward compatibility and required approvals.
Source availability is resolved; inherited header discrepancies are recorded in [versions](VERSION_REGISTER.md).
All 45 old statuses remain unchanged; P-005–007 add approved process controls only.
FA-07 must now enforce UX-0–4 separately and Stage 1B closure/explicit risk waiver before map-style sign-off.
FA-10 approval must identify exact stage/artifact/scope; approving a ticket list does not authorize all its phases.
No protected contract conflict is resolved by document adoption.
