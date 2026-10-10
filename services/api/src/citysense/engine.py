"""Explicit deterministic *hypothesis*, NOT validated human comfort inference."""

from .models import (
    DataKind,
    EvaluateRequest,
    EvaluateResponse,
    Exclusion,
    RankedPlace,
    ScoreComponent,
)
from .parameters import Parameters, load_parameters

MODEL_VERSION = load_parameters().version


def evaluate(request: EvaluateRequest, parameters: Parameters | None = None) -> EvaluateResponse:
    # Revalidation protects direct callers that mutated a previously validated model.
    request = EvaluateRequest.model_validate(request.model_dump())
    parameters = Parameters.model_validate((parameters or load_parameters()).model_dump())
    ranked = []
    excluded = []
    exclusions = []
    for place in request.places:
        if place.walk_minutes > request.max_walk_minutes:
            excluded.append(place.place_id)
            exclusions.append(Exclusion(place_id=place.place_id, reason="walk_time_exceeded"))
            continue
        weights = parameters.weights[request.need]
        seen = []
        reasons = []
        components = []
        for key, weight in weights.items():
            feature = getattr(place, key)
            if feature is None or feature.value is None:
                reasons.append(f"{key}:unavailable")
                continue
            if not 0 <= feature.value <= 1:
                # Refuse silent clipping: raw source ingestion must validate ranges.
                raise ValueError(f"{place.place_id}:{key} must be normalized to [0,1]")
            reference_time = feature.issued_at or feature.observed_or_valid_at
            freshness_at = (
                request.decision_at
                if feature.data_kind == DataKind.FORECAST
                else request.target_time
            )
            age = (freshness_at - reference_time).total_seconds()
            valid = feature.valid_until is None or request.target_time <= feature.valid_until
            if feature.data_kind == DataKind.FORECAST:
                valid = valid and request.target_time >= feature.observed_or_valid_at
                if feature.valid_until is None:
                    valid = valid and request.target_time == feature.observed_or_valid_at
            if age < 0 or age > parameters.max_age_seconds[feature.quality] or not valid:
                reasons.append(f"{key}:stale_or_outside_validity")
                continue
            # traffic_proximity is normalized high=quieter/farther from traffic,
            # NOT actual dB and never described as acoustic measurement.
            seen.append((feature.value, weight))
            reasons.append(f"{key}={feature.value:.2f} ({feature.quality.value})")
            components.append(
                ScoreComponent(
                    feature_key=key,
                    value=feature.value,
                    weight=weight,
                    contribution=feature.value * weight,
                    data_kind=feature.data_kind,
                    quality=feature.quality,
                    source_id=feature.source_id,
                )
            )
        coverage = sum(weight for _, weight in seen)
        # Absolute score only with ALL required features. Never re-weight missing features.
        if len(seen) != len(weights):
            ranked.append(
                RankedPlace(
                    place_id=place.place_id,
                    score=None,
                    coverage=round(coverage, 4),
                    status="insufficient_data",
                    reasons=reasons,
                    components=components,
                    confidence="insufficient_evidence",
                )
            )
        else:
            score = sum(val * weight for val, weight in seen)
            ranked.append(
                RankedPlace(
                    place_id=place.place_id,
                    score=round(score, 4),
                    coverage=round(coverage, 4),
                    status="scored_unvalidated",
                    reasons=reasons,
                    components=components,
                    confidence="unvalidated",
                )
            )
    ranked.sort(key=lambda p: (p.score is None, -(p.score or 0), p.place_id))
    return EvaluateResponse(
        model_version=parameters.version,
        parameter_hash=parameters.digest,
        candidate_ids=sorted(p.place_id for p in request.places),
        ranked=ranked,
        excluded=sorted(excluded),
        exclusions=sorted(exclusions, key=lambda e: e.place_id),
        warning="Scores are hypothesis-based and unvalidated; features are provided by caller, not live measurements.",
    )
