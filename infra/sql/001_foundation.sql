-- Legacy proposal, retained for audit only. Do NOT apply this file.
-- Executable, versioned schema is services/api/migrations/versions/0001_foundation.sql.
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE TABLE IF NOT EXISTS places (
  id TEXT PRIMARY KEY,
  label TEXT NOT NULL,
  location GEOGRAPHY(POINT,4326) NOT NULL,
  source_id TEXT NOT NULL,
  source_license TEXT NOT NULL,
  retrieved_at TIMESTAMPTZ NOT NULL,
  verified_at TIMESTAMPTZ
);
CREATE INDEX IF NOT EXISTS places_location_gist ON places USING GIST(location);
CREATE TABLE IF NOT EXISTS observations (
  id UUID PRIMARY KEY,
  place_id TEXT REFERENCES places(id),
  feature_key TEXT NOT NULL,
  feature_value DOUBLE PRECISION,
  unit TEXT NOT NULL,
  quality_class TEXT NOT NULL CHECK (quality_class IN ('measured_local','observed_manual','derived_spatial','regional_forecast','reported_provider','unknown')),
  source_id TEXT NOT NULL,
  source_license TEXT NOT NULL,
  valid_at TIMESTAMPTZ NOT NULL,
  issued_at TIMESTAMPTZ,
  retrieved_at TIMESTAMPTZ NOT NULL,
  method_version TEXT NOT NULL,
  spatial_resolution_m DOUBLE PRECISION CHECK (spatial_resolution_m > 0),
  CHECK (issued_at IS NULL OR issued_at <= retrieved_at)
);
CREATE INDEX IF NOT EXISTS observations_place_time ON observations(place_id, valid_at DESC);
-- Never assume a local street observation from an unlocated regional forecast.
