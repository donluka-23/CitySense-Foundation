"""Small parameterized PostGIS repository; callers own transaction boundaries."""

import math
from typing import Any
from uuid import UUID

from psycopg import Connection
from psycopg.rows import dict_row
from psycopg.types.json import Jsonb

from .models import FEATURE_KEYS, FeatureSnapshot, Observation, SpatialPlace
from .parameters import Parameters, load_parameters
from .platform import GeometryRevision


class Repository:
    def __init__(self, connection: Connection[Any]) -> None:
        self.connection = connection

    def add_source(self, source_id: str, metadata: dict[str, Any]) -> None:
        self.connection.execute(
            "INSERT INTO sources(id,metadata) VALUES (%s,%s)", (source_id, Jsonb(metadata))
        )

    def add_place(self, place: SpatialPlace) -> None:
        place = SpatialPlace.model_validate(place.model_dump())
        self.connection.execute(
            "INSERT INTO places(id,city_id,label,longitude,latitude,source_id,source_license,"
            "retrieved_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
            (
                place.place_id,
                place.city_id,
                place.name,
                place.longitude,
                place.latitude,
                place.source_id,
                place.license_id,
                place.retrieved_at,
            ),
        )

    def nearby(self, longitude: float, latitude: float, radius_m: float, city_id: str) -> list[str]:
        if not all(math.isfinite(v) for v in (longitude, latitude, radius_m)):
            raise ValueError("Spatial arguments must be finite")
        if not -180 <= longitude <= 180 or not -90 <= latitude <= 90 or not 0 <= radius_m <= 100000:
            raise ValueError("Invalid coordinates/radius")
        rows = self.connection.execute(
            "SELECT id FROM places WHERE city_id=%s AND ST_DWithin(location,"
            "ST_SetSRID(ST_MakePoint(%s,%s),4326)::geography,%s) ORDER BY id",
            (city_id, longitude, latitude, radius_m),
        ).fetchall()
        return [row[0] for row in rows]

    def add_observation(self, observation: Observation) -> None:
        o = Observation.model_validate(observation.model_dump())
        self.connection.execute(
            "INSERT INTO observations(id,place_id,feature_key,feature_value,unit,data_kind,"
            "quality_class,source_id,source_version,source_license,valid_at,valid_until,issued_at,"
            "retrieved_at,method_version,spatial_resolution_m,payload) "
            "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            (
                o.observation_id,
                o.place_id,
                o.feature_key,
                o.value,
                o.unit,
                o.data_kind.value,
                o.quality.value,
                o.source_id,
                o.source_version,
                o.license_id,
                o.observed_or_valid_at,
                o.valid_until,
                o.issued_at,
                o.retrieved_at,
                o.method_version,
                o.spatial_resolution_m,
                Jsonb(o.model_dump(mode="json")),
            ),
        )

    def add_geometry_revision(self, revision: GeometryRevision) -> None:
        r = GeometryRevision.model_validate(revision.model_dump())
        self.connection.execute(
            "INSERT INTO place_geometry_revisions(id,place_id,longitude,latitude,valid_at,"
            "retrieved_at,source_id,source_version,source_license) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            (
                r.revision_id,
                r.place_id,
                r.longitude,
                r.latitude,
                r.valid_at,
                r.retrieved_at,
                r.source_id,
                r.source_version,
                r.license_id,
            ),
        )

    def get_observation(self, observation_id: UUID) -> Observation:
        row = self.connection.execute(
            "SELECT payload FROM observations WHERE id=%s", (observation_id,)
        ).fetchone()
        if row is None:
            raise KeyError(observation_id)
        return Observation.model_validate(row[0])

    def add_model(self, parameters: Parameters) -> None:
        self.connection.execute(
            "INSERT INTO model_versions(version,parameter_hash,parameters) VALUES (%s,%s,%s) "
            "ON CONFLICT (version,parameter_hash) DO NOTHING",
            (parameters.version, parameters.digest, Jsonb(parameters.model_dump(mode="json"))),
        )

    def add_snapshot(self, snapshot: FeatureSnapshot) -> None:
        s = FeatureSnapshot.model_validate(snapshot.model_dump())
        with self.connection.transaction():
            self.connection.execute(
                "INSERT INTO feature_snapshots(id,build_version,decision_at,target_time,"
                "created_at,model_version,parameter_hash,payload) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                (
                    s.snapshot_id,
                    s.build_version,
                    s.request.decision_at,
                    s.request.target_time,
                    s.created_at,
                    s.model_version,
                    s.parameter_hash,
                    Jsonb(s.model_dump(mode="json")),
                ),
            )
            ids = {
                getattr(p, k).observation_id
                for p in s.request.places
                for k in FEATURE_KEYS
                if getattr(p, k) is not None
            }
            for observation_id in sorted(ids, key=str):
                self.connection.execute(
                    "INSERT INTO feature_snapshot_inputs(snapshot_id,observation_id) VALUES (%s,%s)",
                    (s.snapshot_id, observation_id),
                )

    def replay(self, snapshot_id: UUID) -> tuple[FeatureSnapshot, Parameters]:
        with self.connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute(
                "SELECT s.payload,m.parameters FROM feature_snapshots s JOIN model_versions m "
                "ON (s.model_version,s.parameter_hash)=(m.version,m.parameter_hash) WHERE s.id=%s",
                (snapshot_id,),
            )
            row = cursor.fetchone()
        if row is None:
            raise KeyError(snapshot_id)
        snapshot = FeatureSnapshot.model_validate(row["payload"])
        parameters = Parameters.model_validate(row["parameters"])
        if parameters.digest != snapshot.parameter_hash:
            raise ValueError("Parameter hash mismatch")
        # JSONB discards object key order. Restore the content-identical packaged artifact
        # so quiet-rest component/reason order replays exactly as originally evaluated.
        packaged = load_parameters()
        if packaged.digest == parameters.digest:
            parameters = packaged
        return snapshot, parameters
