"""Append-only spatial evidence and versioned replay snapshots."""

from pathlib import Path

from alembic import op

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(Path(__file__).with_suffix(".sql").read_text(encoding="utf-8"))


def downgrade() -> None:
    # Explicit downgrade destroys research evidence; only use on disposable databases.
    op.execute(
        "DROP TABLE feature_snapshot_inputs, feature_snapshots, observations, "
        "model_versions, places, sources CASCADE"
    )
    op.execute(
        "DROP FUNCTION reject_evidence_mutation(), check_snapshot_input(), check_snapshot_payload(), check_observation_payload()"
    )
    # PostGIS may be shared by unrelated schemas; do not remove the extension.
