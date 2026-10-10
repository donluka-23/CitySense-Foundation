# Controlled Digital Twin rollback report

Status: **ABORTED BEFORE DELETION ? rollback not completed.**
Recorded 2026-10-10T08:43:14.036015+00:00. The existing foundation remains intact, but the rejected
frontend is still present. No Git initialization, commit, replacement interface, new development
stage or deployment occurred.

## Backup and recovery

Archive: `D:\citysense-foundation\.local\rollback-archives\rejected-digital-twin-20261010T082826Z-b923dc6c\rejected-digital-twin.zip`

SHA-256: `50573c28cc0e6c5cfb1a4066fc7787965e569f12ec7b51f9f23659e9f86bcf28`

Size: 9,179,277 bytes. ZIP CRC validation passed. Isolated extraction under
`D:\citysense-foundation\.local\rollback-archives\rejected-digital-twin-20261010T082826Z-b923dc6c\recovery-check` verified all **1,794 payload files** against their
recorded SHA-256 hashes. The archive remains unchanged and retained. Recovery includes
22 source files, two approved caches, verified public installed dependencies, retained historical
reports/diagnostics and recovery hash evidence. Root configuration, actual environment files,
process environment, npm configuration/cache and unrelated private data were excluded.
The only environment example archived was the matching app template with an empty key.
Ambiguous Ruff cache contents were not archived or deleted.

Recovery procedure: read the archive's `_rollback/archive-manifest.json`, extract to a new
isolated directory, check CRC/path confinement and each SHA-256, then restore only explicitly
approved paths after checking they will not overwrite newer user work. No current restoration
is necessary because deletion stopped before the first file.

## Exact deleted and retained paths

**Deleted files: none. Deleted directories: none.** See [deleted-paths.json](deleted-paths.json).

The 22 approved rejected source files, two approved Python caches and all 1,742 byte-matched
isolated dependency files remain. The matching clean install used the unchanged pinned
lockfile, a separate npm cache and `npm ci --ignore-scripts`; no foundation dependency was
installed, upgraded or removed. All 2,001 enumerated retained paths are recorded in
[retained-paths.json](retained-paths.json), including the protected snapshot, historical documents,
diagnostics and hash evidence. The original delivery manifest remains unchanged at
`docs/evidence/digital-twin/delivery-manifest.json`.

## Why removal stopped

The removal guard compared the complete app file enumeration with the authorized candidate
inventory. It found four omitted generated Ruff cache files:

- `apps/digital-twin/.ruff_cache/.gitignore`
- `apps/digital-twin/.ruff_cache/CACHEDIR.TAG`
- `apps/digital-twin/.ruff_cache/0.14.0/11342656421739877572`
- `apps/digital-twin/.ruff_cache/0.14.0/13759013275288462140`

Their recorded modification times precede this rollback. They were omitted from the original
inventory because its scan excluded Ruff caches; this was an inventory omission, not a newly
approved deletion target. The guard correctly stopped before any removal. The user's instruction,
?Abort destructive operations if archive verification fails, protected hashes change, or
unexpected filesystem differences appear,? is why destructive work was not resumed automatically.
These four paths remain unchanged. Root `.env.example` is also retained; its contents were not
read, and its size/modification metadata did not change.

The current archive and source inventory are ready for review. Proposed continuation requires
explicit authorization to retain the four Ruff cache files, exclude them from removal, and resume
only the originally approved 22 source/two cache/byte-matched dependency removals. All gates
must be rechecked before resumption. No further deletion is authorized by this report itself.

## Foundation comparison and tests

All **203** protected pre-implementation files match before/after SHA-256. All **176** retained
original digests and **22** Sprint 3 protected digests also match. Historical design/evidence files
and the comparison harness are unchanged. [Complete hash comparison](foundation-hashes.json).

Regression: **148 passed, 31 skipped, zero failures/errors**. The skipped tests require a dedicated
PostGIS database; no test URL was configured and the retained local server had no running PID
file. No database, authentication configuration or dataset was changed to manufacture a pass.
Lint, format checks, mypy, contract exports, Bandit, CI/Compose structural checks, comparison
module syntax and comparison HTTP asset checks passed. The temporary HTTP test host closed
normally. No actual provider/browser rendering was claimed. [Test results](regression-results.json).

## Processes and restoration state

PID 8560 was absent on the final observed check. Neither port 8765 nor 8770 had a listener.
The agent did not terminate any existing process. Regression helper processes and their
temporary host finished normally. Other unrelated system processes were not targeted.

**The requested active-development rollback has not been completed.** The protected foundation
is intact, but the rejected app and its installed artifacts remain until the inventory exception
is reviewed and continuation is explicitly authorized.

## Separate Git initialization plan ? approval required

After rollback has been completed and verified:

1. Audit the candidate baseline and ignored files for credentials, private/unlicensed datasets,
   archives, recovery copies, dependency trees and generated outputs. Review any needed
   `.gitignore` addition, particularly `**/node_modules/`, as a separate approved change.
2. Present an exact allowlist for the baseline: preserved foundation and intentionally retained
   historical evidence/rollback report. Historical rejection evidence is not product acceptance.
   Exclude `.local/`, artifacts, actual environment files, dependency trees and caches.
3. Obtain approval for repository initialization, branch name and commit identity. Then initialize
   Git only in `D:\citysense-foundation`; do not create a remote or publish anything.
4. Stage only reviewed paths, inspect the staged diff and secret exclusions, and create a local
   baseline commit with an accurate message describing the preserved foundation and rejected
   implementation's disposition. Verify clean status for the approved allowlist and record the hash.

This is a proposal only. No Git commands that initialize, stage or commit have been executed.
