CREATE EXTENSION IF NOT EXISTS postgis;
CREATE TABLE sources (
  id TEXT PRIMARY KEY,
  metadata JSONB NOT NULL CHECK (jsonb_typeof(metadata) = 'object')
);
CREATE TABLE places (
  id TEXT PRIMARY KEY,
  city_id TEXT NOT NULL,
  label TEXT NOT NULL,
  longitude DOUBLE PRECISION NOT NULL CHECK (longitude BETWEEN -180 AND 180),
  latitude DOUBLE PRECISION NOT NULL CHECK (latitude BETWEEN -90 AND 90),
  location GEOGRAPHY(POINT,4326) GENERATED ALWAYS AS
    (ST_SetSRID(ST_MakePoint(longitude, latitude),4326)::geography) STORED,
  source_id TEXT NOT NULL REFERENCES sources(id),
  source_license TEXT NOT NULL,
  retrieved_at TIMESTAMPTZ NOT NULL
);
CREATE INDEX places_location_gist ON places USING GIST(location);
CREATE INDEX places_city ON places(city_id);
CREATE TABLE observations (
  id UUID PRIMARY KEY,
  place_id TEXT NOT NULL REFERENCES places(id),
  feature_key TEXT NOT NULL,
  feature_value DOUBLE PRECISION CHECK (feature_value > '-Infinity'::float8 AND feature_value < 'Infinity'::float8),
  unit TEXT NOT NULL,
  data_kind TEXT NOT NULL CHECK (data_kind IN ('observed','forecast','derived','estimated_proxy','unavailable')),
  quality_class TEXT NOT NULL CHECK (quality_class IN ('measured_local','observed_manual','derived_spatial','regional_forecast','reported_provider','unknown')),
  source_id TEXT NOT NULL REFERENCES sources(id),
  source_version TEXT NOT NULL,
  source_license TEXT NOT NULL,
  valid_at TIMESTAMPTZ NOT NULL,
  valid_until TIMESTAMPTZ,
  issued_at TIMESTAMPTZ,
  retrieved_at TIMESTAMPTZ NOT NULL,
  method_version TEXT NOT NULL,
  spatial_resolution_m DOUBLE PRECISION CHECK (spatial_resolution_m > 0 AND spatial_resolution_m < 'Infinity'::float8),
  payload JSONB NOT NULL CHECK (jsonb_typeof(payload) = 'object'),
  CHECK ((data_kind = 'unavailable') = (feature_value IS NULL)),
  CHECK (data_kind <> 'unavailable' OR quality_class = 'unknown'),
  CHECK (feature_key NOT IN ('feature_shade','feature_greenery','feature_traffic_proximity')
         OR (unit = 'fraction' AND (feature_value IS NULL OR feature_value BETWEEN 0 AND 1))),
  CHECK ((data_kind = 'forecast') = (issued_at IS NOT NULL)),
  CHECK ((data_kind = 'forecast') = (quality_class = 'regional_forecast')),
  CHECK (issued_at IS NULL OR issued_at <= retrieved_at),
  CHECK (data_kind = 'forecast' OR valid_at <= retrieved_at),
  CHECK (valid_until IS NULL OR valid_until >= valid_at),
  CHECK (data_kind NOT IN ('derived','estimated_proxy') OR quality_class = 'derived_spatial'),
  CHECK (data_kind <> 'observed' OR quality_class IN ('measured_local','observed_manual','reported_provider'))
);
CREATE INDEX observations_place_time ON observations(place_id, feature_key, valid_at DESC);
CREATE INDEX observations_available_time ON observations(retrieved_at, issued_at);
CREATE FUNCTION check_observation_payload() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
  IF (NEW.payload->>'observation_id')::uuid IS DISTINCT FROM NEW.id
     OR NEW.payload->>'place_id' IS DISTINCT FROM NEW.place_id
     OR NEW.payload->>'feature_key' IS DISTINCT FROM NEW.feature_key
     OR (NEW.payload->>'value')::float8 IS DISTINCT FROM NEW.feature_value
     OR NEW.payload->>'unit' IS DISTINCT FROM NEW.unit
     OR NEW.payload->>'data_kind' IS DISTINCT FROM NEW.data_kind
     OR NEW.payload->>'quality' IS DISTINCT FROM NEW.quality_class
     OR NEW.payload->>'source_id' IS DISTINCT FROM NEW.source_id
     OR NEW.payload->>'source_version' IS DISTINCT FROM NEW.source_version
     OR NEW.payload->>'license_id' IS DISTINCT FROM NEW.source_license
     OR NEW.payload->>'method_version' IS DISTINCT FROM NEW.method_version
     OR (NEW.payload->>'spatial_resolution_m')::float8 IS DISTINCT FROM NEW.spatial_resolution_m
     OR (NEW.payload->>'observed_or_valid_at')::timestamptz IS DISTINCT FROM NEW.valid_at
     OR (NEW.payload->>'valid_until')::timestamptz IS DISTINCT FROM NEW.valid_until
     OR (NEW.payload->>'issued_at')::timestamptz IS DISTINCT FROM NEW.issued_at
     OR (NEW.payload->>'retrieved_at')::timestamptz IS DISTINCT FROM NEW.retrieved_at THEN
    RAISE EXCEPTION 'Observation columns disagree with payload';
  END IF;
  RETURN NEW;
END $$;
CREATE TRIGGER observation_payload_valid BEFORE INSERT ON observations FOR EACH ROW EXECUTE FUNCTION check_observation_payload();
CREATE TABLE model_versions (
  version TEXT NOT NULL,
  parameter_hash TEXT NOT NULL CHECK (parameter_hash ~ '^[0-9a-f]{64}$'),
  parameters JSONB NOT NULL,
  PRIMARY KEY(version, parameter_hash),
  UNIQUE(version)
);
CREATE TABLE feature_snapshots (
  id UUID PRIMARY KEY,
  build_version TEXT NOT NULL,
  decision_at TIMESTAMPTZ NOT NULL,
  target_time TIMESTAMPTZ NOT NULL CHECK (target_time >= decision_at),
  created_at TIMESTAMPTZ NOT NULL CHECK (created_at >= decision_at),
  model_version TEXT NOT NULL,
  parameter_hash TEXT NOT NULL,
  payload JSONB NOT NULL CHECK (jsonb_typeof(payload) = 'object'),
  FOREIGN KEY(model_version, parameter_hash) REFERENCES model_versions(version, parameter_hash)
);
CREATE TABLE feature_snapshot_inputs (
  snapshot_id UUID NOT NULL REFERENCES feature_snapshots(id),
  observation_id UUID NOT NULL REFERENCES observations(id),
  PRIMARY KEY(snapshot_id, observation_id)
);
CREATE FUNCTION reject_evidence_mutation() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
  RAISE EXCEPTION 'Evidence is append-only; create a new version';
END $$;
CREATE TRIGGER sources_immutable BEFORE UPDATE OR DELETE ON sources FOR EACH ROW EXECUTE FUNCTION reject_evidence_mutation();
CREATE TRIGGER places_immutable BEFORE UPDATE OR DELETE ON places FOR EACH ROW EXECUTE FUNCTION reject_evidence_mutation();
CREATE TRIGGER observations_immutable BEFORE UPDATE OR DELETE ON observations FOR EACH ROW EXECUTE FUNCTION reject_evidence_mutation();
CREATE TRIGGER models_immutable BEFORE UPDATE OR DELETE ON model_versions FOR EACH ROW EXECUTE FUNCTION reject_evidence_mutation();
CREATE TRIGGER snapshots_immutable BEFORE UPDATE OR DELETE ON feature_snapshots FOR EACH ROW EXECUTE FUNCTION reject_evidence_mutation();
CREATE TRIGGER inputs_immutable BEFORE UPDATE OR DELETE ON feature_snapshot_inputs FOR EACH ROW EXECUTE FUNCTION reject_evidence_mutation();

CREATE FUNCTION check_snapshot_payload() RETURNS trigger LANGUAGE plpgsql AS $$
DECLARE place JSONB; feature JSONB; key TEXT; obs observations%ROWTYPE;
BEGIN
  IF (NEW.payload->'request'->>'decision_at')::timestamptz IS DISTINCT FROM NEW.decision_at
     OR (NEW.payload->'request'->>'target_time')::timestamptz IS DISTINCT FROM NEW.target_time
     OR (NEW.payload->>'created_at')::timestamptz IS DISTINCT FROM NEW.created_at
     OR (NEW.payload->>'snapshot_id')::uuid IS DISTINCT FROM NEW.id
     OR NEW.payload->>'model_version' IS DISTINCT FROM NEW.model_version
     OR NEW.payload->>'parameter_hash' IS DISTINCT FROM NEW.parameter_hash
     OR NEW.payload->>'build_version' IS DISTINCT FROM NEW.build_version THEN
    RAISE EXCEPTION 'Snapshot columns disagree with payload';
  END IF;
  FOR place IN SELECT * FROM jsonb_array_elements(NEW.payload->'request'->'places') LOOP
    IF NOT EXISTS (SELECT 1 FROM places WHERE id = place->>'place_id') THEN
      RAISE EXCEPTION 'Unknown snapshot place';
    END IF;
    FOREACH key IN ARRAY ARRAY['feature_shade','feature_greenery','feature_traffic_proximity'] LOOP
      feature := place->key;
      IF feature IS NULL OR feature = 'null'::jsonb THEN CONTINUE; END IF;
      SELECT * INTO obs FROM observations WHERE id = (feature->>'observation_id')::uuid;
      IF NOT FOUND THEN RAISE EXCEPTION 'Feature requires stored observation'; END IF;
      IF obs.place_id <> place->>'place_id' OR obs.feature_key <> key
         OR obs.retrieved_at > NEW.decision_at
         OR obs.issued_at > NEW.decision_at
         OR feature - 'observation_id' IS DISTINCT FROM
            obs.payload - ARRAY['observation_id','place_id','feature_key'] THEN
        RAISE EXCEPTION 'Snapshot evidence mismatch or future knowledge';
      END IF;
    END LOOP;
  END LOOP;
  RETURN NEW;
END $$;
CREATE TRIGGER snapshot_payload_valid BEFORE INSERT ON feature_snapshots FOR EACH ROW EXECUTE FUNCTION check_snapshot_payload();

CREATE FUNCTION check_snapshot_input() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM feature_snapshots s, observations o,
      jsonb_array_elements(s.payload->'request'->'places') p,
      jsonb_each(p) f
    WHERE s.id=NEW.snapshot_id AND o.id=NEW.observation_id
      AND f.key IN ('feature_shade','feature_greenery','feature_traffic_proximity')
      AND f.value->>'observation_id'=o.id::text
      AND o.retrieved_at <= s.decision_at
      AND (o.issued_at IS NULL OR o.issued_at <= s.decision_at)
  ) THEN RAISE EXCEPTION 'Invalid snapshot lineage'; END IF;
  RETURN NEW;
END $$;
CREATE TRIGGER snapshot_input_valid BEFORE INSERT ON feature_snapshot_inputs FOR EACH ROW EXECUTE FUNCTION check_snapshot_input();
