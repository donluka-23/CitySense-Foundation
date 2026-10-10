# Controlled Digital Twin rollback — completed and verified

Verification time: 2026-10-10T08:54:39.177792+00:00

The approved 203-file pre-Digital-Twin foundation is restored within the authorized scope. The rejected implementation and its reviewed installation files are removed. Historical reports, recovery evidence, root configuration and all four explicitly protected Ruff files remain intact. No Git repository, commit, interface or development stage was created.

The earlier aborted rollback report remains historical evidence and was not rewritten. This separate resumption implements the subsequent authorization to preserve the four Ruff files.

## Backup and recovery

- Archive: `D:\citysense-foundation\.local\rollback-archives\rejected-digital-twin-20261010T082826Z-b923dc6c\rejected-digital-twin.zip`.
- SHA-256: `50573c28cc0e6c5cfb1a4066fc7787965e569f12ec7b51f9f23659e9f86bcf28`.
- Size: 9,179,277 bytes; archive unchanged.
- Existing isolated extraction: `D:\citysense-foundation\.local\rollback-archives\rejected-digital-twin-20261010T082826Z-b923dc6c\recovery-check`.
- ZIP CRC and SHA-256 rechecked for all 1,794 payload files in both the archive and existing isolated extraction; manifest also matches.
- Original credential-safe archive retained without modification. The Ruff files remain in place and were not added to that archive.
- Machine-readable verification: [recovery-verification.json](recovery-verification.json).

## Exact removals

22 approved implementation files, two approved Python cache files and 1,742 previously reviewed disposable dependency files were deleted: 1,766 files total. Installed dependency bytes were rechecked against the previously approved recovery digests before removal; the earlier isolated locked installation comparison remains unchanged. No shared dependency was altered.

Every deleted path, SHA-256, provenance/category, and each of the 138 individually removed empty generated directories appears in [deleted-paths.json](deleted-paths.json). No directory was deleted recursively.

Implementation and Python cache paths:

- `apps/digital-twin/.env.example`
- `apps/digital-twin/.gitignore`
- `apps/digital-twin/README.md`
- `apps/digital-twin/THIRD_PARTY_NOTICES.txt`
- `apps/digital-twin/app.css`
- `apps/digital-twin/app.mjs`
- `apps/digital-twin/camera.mjs`
- `apps/digital-twin/decision.mjs`
- `apps/digital-twin/domain.mjs`
- `apps/digital-twin/geometry.mjs`
- `apps/digital-twin/i18n.mjs`
- `apps/digital-twin/index.html`
- `apps/digital-twin/map-scene.mjs`
- `apps/digital-twin/observations.mjs`
- `apps/digital-twin/package-lock.json`
- `apps/digital-twin/package.json`
- `apps/digital-twin/serve.py`
- `apps/digital-twin/tests/domain.test.mjs`
- `apps/digital-twin/tests/geometry.test.mjs`
- `apps/digital-twin/tests/scene.test.mjs`
- `apps/digital-twin/tests/test_server.py`
- `apps/digital-twin/verify.py`
- `apps/digital-twin/__pycache__/serve.cpython-312.pyc`
- `apps/digital-twin/tests/__pycache__/test_server.cpython-312.pyc`

The 1,742 dependency paths are listed individually in the manifest; all are under `apps/digital-twin/node_modules/`. That isolated dependency directory is now absent.

## Retained files

Protected Ruff files, unchanged:

- `apps/digital-twin/.ruff_cache/.gitignore` — 35 bytes; SHA-256 `9e3a60f1e6ec4ae60215c11d54b171392745ec25e9dded433d5bd921363af316`.
- `apps/digital-twin/.ruff_cache/0.14.0/11342656421739877572` — 84 bytes; SHA-256 `287b81a8fc1fc535688b812f1d731d29368b4b93cf55f8c760369f8a41920e44`.
- `apps/digital-twin/.ruff_cache/0.14.0/13759013275288462140` — 102 bytes; SHA-256 `421f937f3b6f072af5c9c1c1934a0e42918f6eaf5811fd21b65571e8b6cc3f43`.
- `apps/digital-twin/.ruff_cache/CACHEDIR.TAG` — 43 bytes; SHA-256 `5953156d7e0c564a427251316eaf26f8870e6483ae2197f916b630e4f93e31ae`.

The app parent remains with these four files. Remaining subdirectories: `apps/digital-twin/.ruff_cache`, `apps/digital-twin/.ruff_cache/0.14.0`, `apps/digital-twin/tests`. The empty `tests` directory is preserved.

No ambiguous dependency files remain. The four protected Ruff files are retained regardless of disposability. All 162 frozen historical/evidence records match their pre-resumption hashes, including the earlier aborted report, original archive and original rollback records. All 203 protected foundation hashes match. Root `.env.example` was neither read nor modified; its byte count and modification timestamp match the previous capture.

[retained-paths.json](retained-paths.json) lists retained foundation/evidence paths and hashes, four Ruff files, root configuration metadata and 1,794 retained isolated recovery payload paths. Unrelated generated files and user-controlled files were left untouched.

## Foundation and regression results

- 203 protected files: 203 unchanged, zero changed, zero missing. Full before/after values: [foundation-hashes.json](foundation-hashes.json).
- API pytest: 148 passed, 31 skipped, zero failures/errors (179 collected).
- The 31 database/PostGIS tests remain skipped because a dedicated test database is not configured and the retained Postgres instance is not running. They are not claimed as passed; no database or database configuration was changed.
- Ruff lint and formatting, mypy, contract export check, Bandit, CI structure validation, and both retained map harness JavaScript syntax checks passed.
- Retained comparison harness HTTP smoke check passed for allowlisted assets on a temporary loopback port. The temporary host was closed. This does not establish browser rendering or visual approval.
- Full results: [regression-results.json](regression-results.json). Test logs and JUnit XML: `D:\citysense-foundation\.local\rollback-archives\resumed-digital-twin-20261010T084916Z-ed570b51`.
- No foundation dependency installation, root configuration changes or public deployment.

## Remaining processes

PID 8560 is absent. No listener remains on ports 8765 or 8770. No process identified by an explicit rejected-app path remains. Zero processes were stopped.

Codex-managed browser runtime `node.exe`, PID 23328, remains; its command line mentions neither the rejected app nor a serve script. Its executable is under the Codex `runtimes/cua_node` directory. It was preserved. This is a check of the requested PID, relevant listeners and identifiable repository processes, not a system-wide process termination audit.

## Final status and next authorization boundary

**COMPLETED AND VERIFIED.** No further unexpected files or hash mismatches appeared. The approved foundation is restored, with historical evidence and the four explicitly retained Ruff files left in place.

Git metadata remains absent. A separate plan, pending explicit authorization, is to review secret-safe exclusions and generated/recovery artifacts, agree baseline scope (including how rejected historical evidence is handled), initialize Git locally, stage only the reviewed baseline and inspect staged paths/diffs for secrets, then create a baseline commit after required checks. No remote push, deployment or new development is implied.

Stop here. Await explicit authorization for Git initialization and baseline creation. No replacement interface or new stage is authorized.

Machine-readable final status: [post-rollback-status.json](post-rollback-status.json).
