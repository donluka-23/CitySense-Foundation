# ADR-0006: Append-only PostGIS evidence and database-checked replay

Date: 2026-10-09. Status: implemented; human release review pending.
Extends ADR-0002 without replacing the modular monolith.

## Problem and measurable requirements

Store timestamped urban evidence and reproduce a recommendation using the exact
candidate features and parameters available at its historical decision. Verify meter
distance queries, coordinate bounds, index availability, immutable records and rejection
of forecasts issued or retrieved after the decision. Support city IDs without Batumi-specific code.

## Decision

Use psycopg parameterized SQL and explicit Alembic migrations. SQLAlchemy is limited to
Alembic's connection infrastructure; a small repository exposes persistence operations.
The executable revision is `services/api/migrations/versions/0001_foundation.*`;
`infra/sql/001_foundation.sql` remains a marked legacy proposal and must not be applied.

Store sources, stable point places, generic observations, model parameters, multi-place
feature snapshots and input links. Place coordinates generate `geography(Point,4326)`;
GiST supports `ST_DWithin` in meters. Coordinate bounds are checked before geography
can normalize invalid coordinates. Observations preserve data kind, quality, units,
source/version/license, valid/issued/retrieved times, resolution, method and canonical payload.
Triggers check column/payload agreement and block update/delete of evidence.

Snapshot payload validation requires every supplied feature to match a stored observation
for that place and key. Both retrieval and forecast issuance must precede the decision.
Snapshots retain the complete candidate request and reference an immutable parameter
version/hash. Replay reloads and verifies parameters, never silently using current weights.
Application code and database both enforce temporal constraints. Migrations run explicitly,
never at API startup. All snapshot inserts and their lineage links share one transaction.

## Alternatives and consequences

SQLite cannot exercise PostGIS semantics. An ORM with spatial wrappers would add a second
spatial representation without a present benefit. Latest-value tables lose forecast revisions.
Event streaming adds operational cost for the current small workload. The selected design
is simple but uses one connection per replay; pooling, partitioning, retention and backup
recovery tests follow measured load. Immutable places currently need a new identifier for
coordinate corrections; a stable-ID revision table is a Sprint 2 dependency.

The snapshot is a decision-level envelope rather than one row per place; it preserves the
candidate universe atomically. Features remain nested by place. Arbitrary route geometry,
polygon ingestion and provider-native raw response archives are outside Sprint 1.
Triggers constrain normal SQL writers, not superusers; production needs least-privilege roles.

## Evidence

Real PostgreSQL 16.14 / PostGIS 3.6.2 tests cover round trips, forecast history, forged
payloads, immutable records, WGS84 validity, a Batumi distance check and GiST query plans.
Upgrade, repeated upgrade, downgrade and re-upgrade run in isolated disposable schemas.
See [report](../SPRINT_1_REPORT.md). The Docker CI variant remains unexecuted locally.

References: [PostGIS ST_DWithin](https://postgis.net/docs/ST_DWithin.html),
[Alembic tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html).
