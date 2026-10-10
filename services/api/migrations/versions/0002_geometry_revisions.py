"""Append-only geometry revisions preserve stable place IDs and Sprint 1 evidence."""

from alembic import op

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""CREATE TABLE place_geometry_revisions (
        id uuid PRIMARY KEY, place_id text NOT NULL REFERENCES places(id),
        longitude double precision NOT NULL CHECK(longitude BETWEEN -180 AND 180),
        latitude double precision NOT NULL CHECK(latitude BETWEEN -90 AND 90),
        location geography(Point,4326) GENERATED ALWAYS AS
            (ST_SetSRID(ST_MakePoint(longitude,latitude),4326)::geography) STORED,
        valid_at timestamptz NOT NULL, retrieved_at timestamptz NOT NULL,
        source_id text NOT NULL REFERENCES sources(id), source_version text NOT NULL,
        source_license text NOT NULL, CHECK(valid_at<=retrieved_at)
    )""")
    op.execute(
        "CREATE INDEX geometry_revision_place_time ON place_geometry_revisions(place_id,valid_at DESC,retrieved_at DESC)"
    )
    op.execute(
        "CREATE INDEX geometry_revision_location_gist ON place_geometry_revisions USING gist(location)"
    )
    op.execute(
        "CREATE TRIGGER immutable_geometry_revisions BEFORE UPDATE OR DELETE ON place_geometry_revisions FOR EACH ROW EXECUTE FUNCTION reject_evidence_mutation()"
    )


def downgrade() -> None:
    op.execute("DROP TABLE place_geometry_revisions")
