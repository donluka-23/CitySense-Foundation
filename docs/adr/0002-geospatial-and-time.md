# ADR-0002: Place-time snapshots, PostGIS geography and lineage
Status: **Accepted for research starter** | Date: 2026-10-09

## Decision
Store stable place IDs, WGS84 locations, meter-distance queries through PostGIS `geography`, event/issued/retrieved timestamps, optional validity window, source version/license, resolution and provenance. Immutable raw input snapshots for experiment replay.
## Reason
Nearby places share regional weather; distinguishing signal is often micro-place geometry and subjective ground truth, not invented neighborhood weather. Forecast revisions must not leak future knowledge.
## Alternatives
District averages: hide variation. Latest-value-only table: cannot replay. Raw OSM geometry as sole long-lived identity: changes/dedup issues.
## Consequence
Storage and ingest complexity, but reproducible evaluation and explicit uncertainty.

## Sprint 1 evidence

ADR-0006 records executable persistence and the decision-level snapshot envelope.
Both forecast issuance and retrieval are checked against historical decisions. A real
PostGIS cluster exercised geography, indexes, observation integrity and replay; exact
outcomes are in the Sprint 1 report. Full route/polygon ingestion remains future work.
