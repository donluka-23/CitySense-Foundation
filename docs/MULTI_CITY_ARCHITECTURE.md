# Multi-city architecture and onboarding

Implemented city configuration is `citysense/parameters/cities.json`: city ID, IANA timezone,
finite WGS84 bounds and validation status. Batumi is the initial research city. `tbilisi-fixture`
only exercises configuration, isolation and missing-data abstention with synthetic evidence.
It is not a second-city field test. Neither city changes engine parameters automatically.

## Identity and revisions

`places.id` remains stable and globally unique; city membership is immutable. Migration 0002
adds `place_geometry_revisions` with UUID, stable place FK, point, valid/retrieved times and
source/version/license. Update/delete triggers reuse the evidence immutability control.
As-of reads select revisions valid and retrieved by decision time, ordered by valid time,
retrieval then UUID. No revision leaves the original geometry as the initial historical state.
Corrections do not rewrite stored observations or snapshots. A corrected point can change
later radius search while an earlier decision returns the original location.

Stable identity is not automatic conflation: moving a business, splitting a park or merging
OSM/Overture objects requires an identity policy. Future source-ID aliases, replaced-by relations,
polygon/line revisions and feature derivation references must be append-only. Current point
accuracy is unknown; a research-window anchor is explicitly not a provider park point.

## Repeatable onboarding

1. Assign an internal city ID, timezone, bounds/CRS and validation status. Review CRS conversion
   before import; store longitude then latitude in EPSG:4326 and query distances in meters.
2. Inventory sources by variable and geographic coverage. Obtain purpose, storage and publication
   rights, attribution, costs/quotas and revision/version evidence separately for each dataset.
3. Validate city bounds and source coordinates during import review; current bounds are configuration,
   not a legally authoritative boundary or automatic ingestion clipping rule.
4. Create stable place IDs and resolve source aliases; record uncertain matches. Ingest dated raw
   archives only where permitted, retain lineage and transformations, append geometry corrections.
5. Measure missingness, source/temporal coverage and spatial uncertainty; keep unavailable features
   null. Do not replace missing observations with default scores or another city's averages.
6. Extend the operator city allowlist deliberately; run city isolation, meter-distance, as-of,
   rights, abstention and replay tests before using the city in private integration trials.
7. Freeze a city-specific research manifest. Independently review labels and transfer assumptions;
   compare holdout error and coverage under identical model/version before any transfer claim.

Regional weather can be shared context across nearby places, never invented street weather zones.
Places, small sampling windows and future route segments express local spatial contrasts.
City-specific quality audits/configuration may vary; scoring must not secretly vary by city.
Initial environmental model transfer remains unvalidated in both cities.
