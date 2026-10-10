# Stage G1 — local Git baseline prepared

**STATUS: GIT BASELINE PREPARED — AWAITING COMMIT AUTHORIZATION.**

Local repository: `D:\citysense-foundation`; initial branch: `main`. No first commit, tag or remote exists. No push or application development occurred.

## Baseline scope and inventory

378 files are staged: 369 reviewed existing files and nine additive G1 evidence files. The complete inventory is [staged-inventory.txt](staged-inventory.txt), with categories in [staged-inventory.json](staged-inventory.json). Final index blob IDs, working SHA-256 values and byte sizes are retained in `D:\citysense-foundation\.local\git-baseline-20261010T085930Z-1aba8c2e/staged-index-inventory.json`.

The baseline includes API source/tests/migrations/scripts and pinned dependency definitions, safe root environment example, CI configuration, schema exports, research contracts/fixtures, architecture and stage documentation, the existing map comparison harness, and reviewed historical reproducibility evidence. Old rejected Digital Twin design/validation documents and logs remain historical records alongside the completed rollback evidence. The rejected implementation source and installed dependencies are absent.

No blanket exclusion applies to `artifacts/`. Historical log files and JUnit, synthetic receipts, dependency audits, aggregate coverage summaries/queries/results and redacted evidence are retained after scanning. Private research captures, duplicate install workspaces and third-party document copies without established redistribution rights remain intact outside the index.

## Git ignore proposal applied locally

The exact proposed and applied contents are [proposed.gitignore](proposed.gitignore), byte-identical to the root `.gitignore`. It excludes credential environments/key files, installed dependencies, virtual environments, caches, private `.local/` recovery/database state, temporary build/test outputs, machine/editor files and specifically identified restricted artifacts. The audited root `.env.example` is explicitly included. No global Git settings were changed.

Excluded categories/counts and rationale appear in [excluded-categories.json](excluded-categories.json). Counts describe the initial inspection; subsequent G1 work files also remain under ignored `.local/`.

## Inspection and credential audit

Read-only inspection covered 51,613 files and 4,632 directories, including ignored installation/local trees. No nested Git repository, symlink or reparse point was found. Files at or above 10 MiB occur only in excluded local tools/dependencies. No baseline candidate is binary or oversized.

Credential scans inspect the candidate text and actual Git index blobs. There are zero unresolved or operational credential findings. Seventeen generic matches were individually adjudicated as documentation placeholders, runtime-generated password expressions or explicit deterministic/SSRF test sentinels. These are bounded findings, not blanket test-file exemptions. No scanner values or real credentials are published.

The root example's six credential/credential-URL fields are empty; Telegram allowlists are empty; remaining values are non-secret local defaults. Restricted raw capture contents were read only as bytes for preservation hashes and were not staged. Ignored environment/credential contents were not inspected.

Patterns cover private keys, AWS/GitHub/OpenAI/Mapbox/Telegram tokens, JWTs, credential URLs and literal secret assignments. Pattern scanning cannot prove absence of every possible secret or personal datum. Full finding adjudications and limitations are in [credential-scan.json](credential-scan.json).

## Foundation and historical integrity

All 203 protected files were checked before and after. Before changes, all 203 matched. Afterward, **202 remain byte-identical; the sole difference is the explicitly authorized root `.gitignore` update**. This is not a claim that all 203 original hashes still match. Full old/new hashes and authorization appear in [foundation-integrity.json](foundation-integrity.json). The original before-hash records are preserved unchanged.

All 432 other pre-existing reviewable project/historical files match the G1 inspection snapshot. The four Ruff files and original recovery archive remain unchanged. Historical generated artifacts retain their rollback inventory hashes. No source, test, schema, engine, protocol, migration, parameter or historical report was edited.

Fresh checks: **148 passed, 31 database-dependent tests skipped, zero failures/errors**. Contract export and CI structure checks passed. The dedicated database remains unavailable; integration tests were not claimed as passed. See [regression-results.json](regression-results.json). Other quality gates passed in the preceding verified rollback and were not repeated for metadata-only Git preparation.

Repository-local settings disable automatic line-ending conversion and fsmonitor, use empty local global-attribute/exclusion override files, recognize existing CRLF endings for whitespace checks, and allow the staged bytes to match working files exactly. System attributes were disabled during the audited staging commands; no clean filters or active attributes apply. Existing nested map ignore rules were preserved.

## Remaining limits

- The 31 database-dependent tests remain unexecuted in this G1 run; historical executed database evidence remains dated.
- Hosted CI and Docker were not executed here; the repository has no remote.
- Historical reports include machine paths and references to intentionally excluded private artifacts and recovery archives. Such references are preserved for accuracy; a clone will not contain those private captures or local databases.
- Old Digital Twin documentation describes a rejected implementation. It is historical evidence, not current functionality or visual acceptance.
- The source/reproducibility baseline is portable with pinned dependencies. Exact private real-source replay requires separately authorized local captures and a dedicated database.
- Two pre-existing whitespace warnings remain in historical `artifacts/sprint2/checks-initial/pytest.xml:10` and `tests.log:15`. These outputs are preserved byte-for-byte. Git whitespace checking reports them; no application source warning remains after recognizing existing CRLF endings.
- Pattern scanning is a bounded local safety check, not independent security/privacy certification.
- Original aggregate map evidence retains its source/attribution context. No provider tile dumps, credentials, paid-service requests or publication-right changes were added.

## Proposed first commit

`chore: establish verified CitySense foundation baseline`

The staged inventory is ready for user review. **Do not commit until explicit approval of the staged inventory.** No commit, tag, remote setup, push or new functionality is authorized by this preparation.
