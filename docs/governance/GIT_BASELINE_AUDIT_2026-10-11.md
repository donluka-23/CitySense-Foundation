# Git baseline audit and commit preparation

Date: **2026-10-11**, Asia/Tbilisi. Review artifact: GIT-AUDIT-2026-10-11 / plan-1.
Readiness: **READY_TO_COMMIT** after independent QA. Commit execution: **NOT AUTHORIZED**.
Scope: current user's audit and commit preparation only. No staging, commits, pushes, product edits or history rewrites.
This report does not approve document-intake completion, protected-contract proposals, map/product stages or deployment.

## Actual Git baseline

- Branch: `stage/1c-map-navigation`.
- HEAD: `eadf331e4b7c262fb5c2216d051f7f6e56a456bf`.
- Tracked files: **387**, all unchanged from HEAD and their recorded intake baseline hashes.
- Staged changes: **0**. Unstaged tracked changes: **0**. Deleted files: **0**.
- Pending at audit start: **79 untracked files**; normal short status collapses these into four entries:
  `.codex/`, `AGENTS.md`, `docs/governance/`, `docs/product/`.
- This audit adds this report and its [manifest](evidence/git-baseline-2026-10-11.json) only:
  **81 untracked files at submission**, with all original 466 visible files preserved.

[Machine-readable manifest](evidence/git-baseline-2026-10-11.json) records every original pending file,
Git status, SHA-256, size, creation provenance, latest contributor and exact proposed commit group.
There are no unknown or unrelated pending files.

## Workstream classification

| Category | First-created provenance, disjoint | Latest contributor, disjoint |
|---|---:|---:|
| Governance bootstrap | 56 | 39 |
| Orchestration acceptance | 9 | 8 |
| Blueprint/AEOS intake | 14 | 32 |
| Map Stage 1 / 1B | 0 | 0 |
| Existing product or research edits | 0 | 0 |
| Unknown/unrelated | 0 | 0 |
| Original pending total | **79** | **79** |

Intake updated **17 bootstrap files and one orchestration Founder packet**, while they were still untracked.
Thus 14 new intake files plus 18 overlays form C3's 32 files. They are additions to Git, not tracked modifications.
Provenance comes from [bootstrap receipt](BOOTSTRAP_VERIFICATION.json),
[orchestration receipt](evidence/orchestration-acceptance/verification.json) and
[intake receipt](evidence/document-intake/verification.json), whose lists cover all 79 paths exactly.

Map Stage 1/1B are already committed. HEAD's difference from the protected foundation commit
`0e0440a28b2d1c82a70aa545c3e8bf3479e0cea0` is nine added Stage 1C report/harness/test files,
already recorded in commit `eadf331`. They are absent from this pending plan.
Protected Sprint 1–3 code, API contracts, ADRs, research protocol/parameters and prior evidence are unchanged.

## Secret and content audit

Scanned **466 tracked/nonignored files**, **4,968,720 bytes**: 387 tracked +79 pending.
No values were printed or placed in this report/manifest.
Patterns covered private keys, common provider/access tokens, JWTs, token/key URL parameters,
credential-shaped URLs and literal sensitive assignments; filenames and binary/cache/archive extensions were reviewed.
**Pending matches: 0. Confirmed real-secret findings: 0. Unresolved candidates: 0.**

The 21 tracked-file matches were reviewed:
- Two variable/documentation references.
- Seven placeholders/examples.
- Nine synthetic credential-shaped HTTPS URLs in a test and copied historical pytest evidence,
  with reserved test/example-domain hosts; these are not newly discovered production credentials.
- Three synthetic fixtures in authentication and known-secret-sentinel tests.

The manifest lists each match's file, line, category and review explanation without its value.
The root tracked `.env.example` has empty sensitive-value fields and is the explicit ignore-rule exception.
No real environment file, private key, token file, binary, dependency installation or cache is proposed.
Ignored `.local/`, virtual environments, caches, node_modules, restricted research captures, temporary logs and
rights-restricted third-party copies were inventoried by path only; their contents are outside this scan.

Existing tracked 75 log and eight XML files are intentional historical validation evidence, not new cache output.
They were scanned, remain byte-identical and are excluded from these commits.
The generated intake BASELINE.json, MAINTENANCE_DIFF.patch and decision traceability are deliberate audit artifacts,
not disposable build output. Largest pending file is the 144,829-byte baseline; no pending binaries.
Pattern scanning has limits; ignored private contents and old Git object history were not scanned.

## Validation and approval evidence

All **18 current validation checks PASS**:
- All 387 tracked files and all 434 protected pre-intake files match recorded SHA-256.
- Current intake after-hashes and 14 addition hashes match; maintenance diff regenerates exactly.
- All five approved source-copy hashes match; the two current Downloads sources equal canonical bytes.
- Original 45 statuses are unchanged; exactly 48 source/register/traceability IDs, with P-005–007 DECIDED.
- Exact clause/line/status/interface traceability, acyclic portfolio and 14 TOML parses pass.
- All future initiatives stay blocked; ledger contains only actual intake maintenance authorization,
  with no fabricated completion, commit approval or successor permission.
- 278 local references checked: current links resolve. The unchanged archived packet has one
  original-directory-context link; it remains historical byte evidence, not a current navigation document.
  Two external references were identified without browsing.
- Git prospective blob hashes preserve all 79 files' raw bytes. `core.autocrlf=false`,
  `core.safecrlf=true`, no active path attributes/filters; source hashes are safe under current settings.
- HEAD equals all prior receipts; staged/unstaged tracked changes are empty.

New source headers still say v0.3 and v1.1/PROPOSED; [VERSION_REGISTER](VERSION_REGISTER.md) explicitly
records the filename/addendum/adoption distinction. No source is silently repaired.
Historical receipt counts and draft-review hashes remain dated snapshots, not claims about new commit boundaries.
CF-01/02/03 remain protected proposals; no scientific metric, commercial priority or /v1 change is accepted.

A validator initially used Windows default decoding and failed; explicit UTF-8 reads resolved it and the final run passes.
Missing optional .gitattributes / exploratory old filenames were inspection misses, not waived contract checks.
The secret scan's process output was recaptured successfully after an initial asynchronous capture mistake.
No product tests or runtime/integration checks were needed or executed for this unchanged-code baseline.

## Proposed commits — exact current-file groups

| Order | Files | Commit message | Boundary |
|---|---:|---|---|
| C1 | 39 | `chore(governance): establish agent roles and bootstrap reference artifacts` | Unchanged bootstrap files; reserve all intake-updated files for C3 |
| C2 | 8 | `docs(governance): record multi-agent orchestration acceptance and audit handoffs` | Preserved historical PARTIAL report/agent evidence; current packet reserved for C3 |
| C3 | 32 | `docs(governance): adopt Blueprint v0.4 and AEOS v1.2 with founder stage gates` | 14 additions +18 overlays, source/version/decision/stage infrastructure and current packet |
| C4 | 2 | `docs(governance): record Git baseline audit and reviewed commit plan` | This report and manifest only |
| Total | **81** | Original 79 plus two audit artifacts | No product, map, research or ignored content |

The [manifest](evidence/git-baseline-2026-10-11.json) contains exact sorted file allowlists under
`commit_groups[].files`, hashes under `files[]`, and no directory-wide staging instructions.
Each original file appears once, with its creation and latest-workstream provenance retained.
C3 holds every file changed by intake even when first created earlier; do not recreate old working-tree states,
overwrite current work, split a file by guessing its history, or claim these Git commits reproduce prior session snapshots.
The full series is the coherent baseline: intermediate commits may refer to artifacts in later groups,
so they are not independent documentation releases and must not be used to advance product stages.
C4 depends on the whole reviewed series. All groups are proposals; no Git mutation command is executed.

## Risks and Founder decision

No unknown changes, secret candidates or unresolved current validation failures block storing this documentation.
The original intake remains FOUNDER_REVIEW; governance adoption is not acceptance of its contract proposals.
Historical orchestration remains PARTIAL; native profile loading/isolation, visual/device/runtime and pilot readiness
remain unverified or blocked. These are product-development gates, not reasons to fabricate commit permission.
Use current exact hashes/status before any approved staging; new edits require re-audit and updated file groups.
Preserve original archives, approvals and receipts. No amendments, force-push, resets, cleaning or checkout overwrites.

Independent QA: **PASS**, /root/intake_independent_qa, portable read-only QA instructions;
reviewer-reported 2026-10-11 approximately 11:25–11:30 Asia/Tbilisi, Windows 11 / PowerShell / Python 3.12.13.
No isolation or native-profile loader acceptance is claimed. No files changed by reviewer.
Independent verification confirms exact C1–C4 memberships, all original hashes/status/provenance, 387 tracked
and 434 protected-file preservation, empty staged/unstaged changes, index content equal to HEAD tree,
source and decision/contract checks, byte-preserved blobs and all future permissions still blocked.
Its bounded scan of all **81 pending files**, including these audit artifacts, found zero secret-pattern candidates.
Its 285-reference local link check includes seven new report links; only the historical archive context exception remains.
Two QA corrections were resolved: reviewed secret counts now match individual classifications, with initial counts
retained separately, and captured HEAD-tree metadata is named accurately without a raw index-byte claim.

Reviewed draft report SHA-256: 942c4bf46d83f0a95d13ae7483a2a87ff41b6affc63f3f9dd57ff9f52358bd58.
Reviewed draft manifest SHA-256: a505eb6d78245ade500560fc679e60e9b8d77bccc108f640ce53218f677f3a7e.
Preserved intake receipt SHA-256: 19865f44c26965c031a827119812f0edef6b9d290508921a63abce812e72ed07.
Final administrative metadata records this actual handoff and readiness; the manifest holds the refreshed final report hash.
No substantive file group, contract or existing file changed after QA. All 466 original visible file bytes remain intact.
READY_TO_COMMIT means technical preparation is complete; the worktree is still uncommitted and the commit plan awaits approval.
Approve or revise **C1–C4 / plan-1** as exact groups and messages before any staging/commit.
Approval to store the baseline must not be interpreted as product implementation, map-stage or release permission.
**STOP awaiting Founder approval of the commit plan.**

