# Retained generated historical artifacts

189 additional earlier foundation, Sprint 2, Sprint 3 and map-stage artifact files remain under `artifacts/`. Their paths, current SHA-256 values, sizes and timestamps are in [historical-artifact-inventory.json](historical-artifact-inventory.json). All modification timestamps predate the rollback resumption. The removal guard confined every deletion to reviewed `apps/digital-twin/` paths; regression output was written to a separate unique directory.

These generated artifacts were excluded from the original 203-file protected snapshot and recovery archive. No earlier SHA-256 baseline is available for a retrospective before/after hash comparison of them. This inventory records retained evidence without asserting such a comparison. The 203 protected files, 162 frozen evidence records, four Ruff files and recovery archive did receive before/after integrity checks, as documented in [POST_ROLLBACK_REPORT.md](POST_ROLLBACK_REPORT.md).
