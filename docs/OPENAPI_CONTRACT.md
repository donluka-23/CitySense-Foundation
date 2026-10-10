# Versioned read API contract

Executable specification: [contracts/openapi.json](contracts/openapi.json), generated from
typed code by `services/api/scripts/export_contracts.py`. `/openapi.json` describes the running
service. Exports contain no credentials, real participant data or invented performance results.

| Operation ID | HTTP endpoint | Inputs / output |
|---|---|---|
| `search_places` | GET `/v1/cities/{city_id}/places` | WGS84 lon/lat, radius, decision time, limit → places and truncation flag |
| `get_place_details` | GET `/v1/cities/{city_id}/places/{place_id}` | Decision time → place with selected geometry revision and rights |
| `get_city_state` | POST `/v1/cities/{city_id}/state` | Decision/target time and place IDs → sparse evidence, freshness and missing keys |
| `evaluate_suitability` | POST `/v1/cities/{city_id}/suitability` | Need, candidates with caller walking estimates, time and max walk → state, exact engine inputs and assessment |
| `compare_places` | POST `/v1/cities/{city_id}/comparison` | Same contract, exactly two distinct candidates → same assessment service |

POST here represents a structured read query. It does not insert snapshots, update evidence or
take actions. Service discovery, availability and booking are future interfaces, absent from
the executable API. Existing `/v1/evaluate`, `/v1/replay/{snapshot_id}` and `/health` remain.

## Bounds, semantics and errors

All times require timezone; state inputs normalize to UTC. `target_time >= decision_at`.
IDs allow letters, digits, `.`, `_`, `:`, `-`, maximum 128 characters. Search radius is
`0 < radius_m <= 10000`, limit 1–30; state/suitability use 1–30 unique place IDs. Comparison
requires exactly two. Longitude/latitude are finite WGS84; extra body fields are rejected.
Walking times are caller estimates, not a routing service or step-free-access guarantee.

Search sorts stable IDs and reports whether more authorized results exist; there is no cursor.
The query returns at most 30 places and four recognized evidence keys per selected place:
the three model features plus `park_way_count`. Unknown feature types are withheld until their
contract is reviewed. `missing_features` describes absent/non-numeric fraction inputs; present
but stale evidence has an explicit freshness status and can still cause engine abstention.

| Status | Meaning |
|---|---|
| 401 | Missing/wrong key or no configured operator authentication |
| 403 | City/scope or source publication rights denied |
| 404 | City/place not available in authorized city at decision time |
| 409 | Stored schema/lineage integrity failure |
| 413 / 429 | Existing body/rate bounds |
| 422 | Invalid query/body; validation response omits input values |
| 503 | Missing/unavailable database; five-second statement/connection limits |

Authentication precedes database access. Errors expose no credentials or SQL. Success/error
responses have `no-store` and `nosniff`. Unknown unauthorised cities produce 403 to enforce scope.

## Example

With the existing Sprint 1 synthetic seed, this candidate ID and fixed timestamps are available:

```json
{"decision_at":"2026-10-09T10:00:00Z","target_time":"2026-10-09T10:00:00Z",
 "need":"cool_walk","candidates":[{"place_id":"synthetic-example-a","walk_minutes":10}],
 "max_walk_minutes":45}
```

The complete synthetic candidate IDs/times are in
`services/api/tests/fixtures/request.json`. Missing IDs return 404. Every result includes
city/internal identity, geometry provenance, rights and uncertainty. Evidence additionally
retains validity, issuance, retrieval, resolution, kind and quality. Assessments expose model
version/hash, coverage, exclusions and components; confidence is unvalidated, not a probability.

`inputs` plus selected state/geometry can be archived by an authorized research operator.
Read queries do not persist a replay snapshot. Replay guarantees apply to stored immutable
FeatureSnapshots; re-running a dynamic query is not a substitute for freezing its output.
