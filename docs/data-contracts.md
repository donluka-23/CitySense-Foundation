# Data contracts | v0.2

Sprint 2 adds [agent read contracts](OPENAPI_CONTRACT.md), generated schemas in `contracts/`,
[point revisions](MULTI_CITY_ARCHITECTURE.md) and [opportunity contracts](OPPORTUNITY_REGISTRY_DESIGN.md).
The existing evidence and calculator contracts below remain intact.

## Canonical entities
- `Place`: stable `place_id`, WGS84 point/geometry, type, provenance, update time, owner verification state.
- `Observation`: `observation_id`, `feature_id`, value/unit, valid-time, issued-time, fetched-time, source id, resolution, lineage, licensing, quality class.
- `FeatureSnapshot`: immutable decision-level envelope (`snapshot_id`, `build_version`, `created_at`, full candidate request, model version/hash). Each nested place retains its input observation IDs. ADR-0006 extends the per-place concept to preserve the complete candidate universe atomically.
- `NeedProfile`: explicit activity, mobility limits, walking/time radius, tolerances and *opt-in* preferences; avoid protected health inference.
- `SuitabilityResult`: model version, candidate universe, excluded candidates and reasons, per-feature contributions, coverage, score (relative utility only), abstain flags.
- `Evaluation`: opt-in independent observed rating, study condition, event-time group, pseudonymous participant, consent flag; not a child of a click log.
- `ProviderOffer`: provider verification, price and currency, eligibility, manually-confirmed booking state and timestamp.

## Feature semantics
`temperature_c` = regional forecast, not street sensor; `green_fraction` may be remote/geometric proxy; `shade_fraction` only observed/derived when methodology recorded; `noise_db` cannot be synthesized from traffic-distance proxy; `crowding` unavailable until validated feed/sensing.

## Quality classes
- `measured_local`: instrument observed, with calibrated sensor and method
- `observed_manual`: consented/on-site observation with method
- `derived_spatial`: GIS proxy with derivation version
- `regional_forecast`: meteorological forecast with disclosed resolution
- `reported_provider`: supplier input, not verified measurement
- `unknown`: no claim

## Required columns for each numeric value
`value`, `unit`, `quality_class`, `source_id`, `observed_or_valid_at`, `issued_at?`, `retrieved_at`, `spatial_resolution_m?`, `method_version`, `license_id`.

## Provenance & legal safeguards
Maintain a source inventory and explicit decision `research_allowed`, `commercial_allowed`, `cache_allowed`, `redistribution_allowed`, `attribution_required`; do not infer downstream redistribution rights from free read access. Open-Meteo free tier is noncommercial. OSM-derived database use may impose ODbL obligations. Mapbox/Google content licensing must be vetted separately.

## API contracts
`POST /v1/evaluate` requires need, timezone-aware `decision_at` and `target_time`,
`max_walk_minutes` and 1-100 unique candidates. Supplied features are caller assertions,
not verified live measurements. The generated schema and synthetic example live in `schemas/`.
Unknown keys, non-finite floats, out-of-range fractions and naive timestamps fail closed.
Times normalize to UTC. Features require source/version/license, method, unit, kind,
quality, valid/issued/retrieved times, optional validity end/resolution and quality metadata.
Normalized features use `fraction`; other raw observation units require a versioned transform.

`GET /v1/replay/{snapshot_id}` loads persisted evidence and historical parameters.
404 means absent snapshot; 409 means integrity failure; 503 means absent/unavailable database.
Results contain candidates, exclusions/reasons, weighted components, coverage,
model/version/hash and confidence limitations. Scores have no psychological units and are
not calibrated probabilities. Old v0.1 fixtures must supply the new required provenance fields.

## Missingness policy
Unknown values never equal zero. Explicit null values require `data_kind=unavailable` and
`quality=unknown`. Every required scoring feature must be usable; otherwise score is null
and status is `insufficient_data`. No hidden defaults or missing-feature reweighting occur.

## Temporal and persistence invariants

- Data kinds: observed, forecast, derived, estimated_proxy and unavailable; separate from quality.
- Forecasts require issuance and regional_forecast quality; issuance cannot exceed retrieval.
- Other evidence cannot occur after retrieval; validity end cannot precede start.
- Every retrieval and issuance must precede or equal the historical decision timestamp.
- HTTP ingestion stamps local receipt, preserving upstream retrieval in quality metadata; remote archive time cannot backdate local knowledge.
- Target cannot precede decision; forecast freshness is checked separately from target validity.
- Versioned freshness limits are engineering hypotheses, not empirical lifetimes.
- Persisted features must match a stored observation for the same place/key, including provenance.
- Normal writers cannot update/delete sources, places, observations, models or snapshots.
- Model hashes use sorted canonical JSON so database object key order does not alter replay.

Spatial places include city ID, bounded WGS84 coordinates and provenance. Walk minutes are
caller-provided estimates; Sprint 1 has no accessible-route computation. Human needs beyond
the three current hypotheses, real licensing and field measurement validity require review.
