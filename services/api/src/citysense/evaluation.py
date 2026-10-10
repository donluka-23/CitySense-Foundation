"""Fail-closed paired-choice harness; synthetic checks are never research results."""

import hashlib
import json
import random
from collections import Counter, defaultdict
from collections.abc import Sequence
from datetime import timedelta
from pathlib import Path
from typing import Any, Literal, Protocol, Self

from pydantic import AwareDatetime, Field, model_validator

from .engine import evaluate
from .models import Contract, EvaluateRequest, Identifier

Split = Literal["train", "validation", "test"]


def content_hash(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
    ).hexdigest()


class EvaluationRecord(Contract):
    record_id: Identifier
    participant_id: Identifier
    place_time_group: Identifier
    spatial_block: Identifier
    time_block: Identifier
    collected_at: AwareDatetime
    consent: bool
    split: Split
    request: EvaluateRequest
    preferred_place_id: Identifier

    @model_validator(mode="after")
    def paired_label(self) -> Self:
        if len(self.request.places) != 2:
            raise ValueError("Paired-choice evaluation requires exactly two candidates")
        if self.preferred_place_id not in {p.place_id for p in self.request.places}:
            raise ValueError("Label must identify one experienced candidate")
        if self.collected_at < self.request.target_time:
            raise ValueError("Label precedes place exposure")
        return self


class DatasetManifest(Contract):
    dataset_id: Identifier
    dataset_version: Identifier
    synthetic: bool
    provenance: str = Field(min_length=1)
    license_id: Identifier
    protocol_version: Identifier
    information_budget_id: Identifier
    latency_budget_seconds: float = Field(gt=0)
    frozen_at: AwareDatetime
    embargo_hours: int = Field(default=24, ge=0, le=168)
    records: list[EvaluationRecord] = Field(min_length=3)

    @model_validator(mode="after")
    def leakage_checks(self) -> Self:
        if len({r.record_id for r in self.records}) != len(self.records):
            raise ValueError("Duplicate evaluation record")
        by_split = {
            s: [r for r in self.records if r.split == s] for s in ("train", "validation", "test")
        }
        if any(not rows for rows in by_split.values()):
            raise ValueError("Train, validation and test must all exist")
        owners: dict[tuple[str, str], str] = {}
        for r in self.records:
            if r.collected_at > self.frozen_at:
                raise ValueError("Record collected after dataset freeze")
            if not self.synthetic and not r.consent:
                raise ValueError("Real participant records require consent")
            groups = [
                ("participant", r.participant_id),
                ("place_time", r.place_time_group),
                ("spatial", r.spatial_block),
                ("time", r.time_block),
            ]
            groups += [("place", p.place_id) for p in r.request.places]
            for group in groups:
                previous = owners.setdefault(group, r.split)
                if previous != r.split:
                    raise ValueError(f"Leakage across splits: {group[0]}")
        embargo = timedelta(hours=self.embargo_hours)
        for earlier, later in (("train", "validation"), ("validation", "test")):
            if max(r.collected_at for r in by_split[earlier]) + embargo >= min(
                r.request.decision_at for r in by_split[later]
            ):
                raise ValueError("Temporal split overlap or embargo violation")
        return self

    @property
    def digest(self) -> str:
        return content_hash(self.model_dump(mode="json"))


def grouped_split(records: Sequence[EvaluationRecord]) -> dict[str, Split]:
    """Connected components prevent leakage through overlapping group identities.

    This helper proposes a chronological split. DatasetManifest is the final gate;
    interleaved components/embargo violations fail rather than silently relaxing rules.
    """
    parent = list(range(len(records)))

    def find(i: int) -> int:
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    seen: dict[tuple[str, str], int] = {}
    for i, r in enumerate(records):
        groups = [
            ("participant", r.participant_id),
            ("place_time", r.place_time_group),
            ("spatial", r.spatial_block),
            ("time", r.time_block),
        ]
        groups += [("place", p.place_id) for p in r.request.places]
        for group in groups:
            if group in seen:
                parent[find(i)] = find(seen[group])
            else:
                seen[group] = i
    components: dict[int, list[EvaluationRecord]] = defaultdict(list)
    for i, row in enumerate(records):
        components[find(i)].append(row)
    ordered = sorted(
        components.values(),
        key=lambda rows: (max(r.collected_at for r in rows), min(r.record_id for r in rows)),
    )
    if len(ordered) < 3:
        raise ValueError("Fewer than three independent components; cannot create holdouts")
    n_train = max(1, min(len(ordered) - 2, int(len(ordered) * 0.6)))
    n_validation = max(1, int(len(ordered) * 0.2))
    output: dict[str, Split] = {}
    for i, rows in enumerate(ordered):
        split: Split = (
            "train" if i < n_train else ("validation" if i < n_train + n_validation else "test")
        )
        for row in rows:
            output[row.record_id] = split
    return output


class Comparator(Protocol):
    name: str

    def predict(self, record: EvaluationRecord) -> str | None: ...
    def configuration(self) -> dict[str, Any]: ...


class NearestBaseline:
    name = "A0-nearest-eligible"

    def predict(self, record: EvaluationRecord) -> str | None:
        eligible = [
            p for p in record.request.places if p.walk_minutes <= record.request.max_walk_minutes
        ]
        return (
            min(eligible, key=lambda p: (p.walk_minutes, p.place_id)).place_id if eligible else None
        )

    def configuration(self) -> dict[str, Any]:
        return {"version": "nearest-1", "tie_policy": "place_id"}


class RuleComparator:
    name = "B0-citysense"

    def predict(self, record: EvaluationRecord) -> str | None:
        response = evaluate(record.request)
        if len(response.ranked) != 2 or any(p.score is None for p in response.ranked):
            return None
        return response.ranked[0].place_id

    def configuration(self) -> dict[str, Any]:
        from .parameters import load_parameters

        parameters = load_parameters()
        return {"model_version": parameters.version, "parameter_hash": parameters.digest}


class FrozenPrediction(Contract):
    record_id: Identifier
    request_hash: str = Field(pattern=r"^[0-9a-f]{64}$")
    choice: Identifier | None
    available_at: AwareDatetime


class BaselineArtifact(Contract):
    name: Literal["A1-tool-equipped"]
    synthetic: bool
    model_id: Identifier
    prompt_hash: str = Field(pattern=r"^[0-9a-f]{64}$")
    tool_configuration_hash: str = Field(pattern=r"^[0-9a-f]{64}$")
    information_budget_id: Identifier
    latency_budget_seconds: float = Field(gt=0)
    predictions: list[FrozenPrediction]


class FrozenToolBaseline:
    name = "A1-tool-equipped"

    def __init__(self, artifact: BaselineArtifact, dataset: DatasetManifest) -> None:
        artifact = BaselineArtifact.model_validate(artifact.model_dump())
        dataset = DatasetManifest.model_validate(dataset.model_dump())
        if artifact.synthetic != dataset.synthetic:
            raise ValueError("Synthetic and real baseline artifacts cannot be mixed")
        if (
            artifact.information_budget_id != dataset.information_budget_id
            or artifact.latency_budget_seconds != dataset.latency_budget_seconds
        ):
            raise ValueError("Baseline information/time budgets differ from frozen experiment")
        self.artifact = artifact
        self.predictions = {p.record_id: p for p in artifact.predictions}
        if len(self.predictions) != len(artifact.predictions):
            raise ValueError("Duplicate baseline prediction")
        if set(self.predictions) != {r.record_id for r in dataset.records}:
            raise ValueError("Baseline must cover the frozen candidate universe")
        for record in dataset.records:
            self.predict(record)

    def predict(self, record: EvaluationRecord) -> str | None:
        prediction = self.predictions[record.record_id]
        if prediction.request_hash != content_hash(record.request.model_dump(mode="json")):
            raise ValueError("Baseline used different candidates/evidence")
        if prediction.available_at > record.request.decision_at:
            raise ValueError("Baseline contains future knowledge")
        if prediction.choice is not None and prediction.choice not in {
            p.place_id for p in record.request.places
        }:
            raise ValueError("Baseline choice outside candidate universe")
        return prediction.choice

    def configuration(self) -> dict[str, Any]:
        return self.artifact.model_dump(mode="json", exclude={"predictions"})


class PairedOutcome(Contract):
    record_id: str
    participant_id: str
    place_time_group: str
    need: str
    correct: bool | None


def clustered_difference(
    left: list[PairedOutcome],
    right: list[PairedOutcome],
    *,
    seed: int = 20261009,
    resamples: int = 2000,
) -> dict[str, Any]:
    """Crossed participant/place-time pigeonhole bootstrap on common scored pairs."""
    if not 100 <= resamples <= 100000:
        raise ValueError("Invalid bootstrap budget")
    if [r.record_id for r in left] != [r.record_id for r in right]:
        raise ValueError("Paired outcomes must share record order")
    pairs = [
        (a, b)
        for a, b in zip(left, right, strict=True)
        if a.correct is not None and b.correct is not None
    ]
    people = sorted({a.participant_id for a, _ in pairs})
    groups = sorted({a.place_time_group for a, _ in pairs})
    if len(people) < 2 or len(groups) < 2:
        return {"status": "insufficient_independent_clusters", "n": len(pairs), "interval": None}
    differences = [int(bool(a.correct)) - int(bool(b.correct)) for a, b in pairs]
    # Deterministic statistical bootstrap; no secrets or security identifiers.
    rng = random.Random(seed)  # nosec B311
    draws = []
    for _ in range(resamples):
        person_weights = Counter(rng.choices(people, k=len(people)))
        group_weights = Counter(rng.choices(groups, k=len(groups)))
        weights = [
            person_weights[a.participant_id] * group_weights[a.place_time_group] for a, _ in pairs
        ]
        denominator = sum(weights)
        if denominator:
            draws.append(
                sum(w * d for w, d in zip(weights, differences, strict=True)) / denominator
            )
    if len(draws) < resamples // 2:
        return {"status": "insufficient_bootstrap_support", "n": len(pairs), "interval": None}
    draws.sort()
    return {
        "status": "exploratory_cluster_bootstrap",
        "n": len(pairs),
        "difference": sum(differences) / len(differences),
        "interval": [
            draws[int(len(draws) * 0.025)],
            draws[min(len(draws) - 1, int(len(draws) * 0.975))],
        ],
        "participant_clusters": len(people),
        "place_time_clusters": len(groups),
        "seed": seed,
        "requested_resamples": resamples,
        "usable_resamples": len(draws),
    }


def brier_score(probabilities: Sequence[float], labels: Sequence[bool]) -> float:
    if not probabilities or len(probabilities) != len(labels):
        raise ValueError("Probability/label length mismatch")
    if any(not 0 <= p <= 1 for p in probabilities):
        raise ValueError("Brier score requires genuine finite probabilities in [0,1]")
    return sum((p - int(y)) ** 2 for p, y in zip(probabilities, labels, strict=True)) / len(labels)


def run_experiment(
    dataset: DatasetManifest,
    baseline: FrozenToolBaseline,
    output: Path,
    calibrated: Comparator | None = None,
) -> dict[str, Any]:
    dataset = DatasetManifest.model_validate(dataset.model_dump())
    comparators: list[Comparator] = [NearestBaseline(), baseline, RuleComparator()]
    if calibrated is not None:
        config = calibrated.configuration()
        train_ids = {r.record_id for r in dataset.records if r.split == "train"}
        validation_ids = {r.record_id for r in dataset.records if r.split == "validation"}
        fitted = set(config.get("fit_record_ids", []))
        tuned = set(config.get("tuning_record_ids", []))
        if (
            calibrated.name != "B1-calibrated"
            or config.get("dataset_hash") != dataset.digest
            or not fitted
            or not fitted <= train_ids
            or not tuned <= validation_ids
        ):
            raise ValueError(
                "Calibrated artifact must declare train-only fit and validation-only tuning"
            )
        comparators.append(calibrated)
    test_records = [r for r in dataset.records if r.split == "test"]
    outcomes: dict[str, list[PairedOutcome]] = {}
    metrics: dict[str, Any] = {}
    for comparator in comparators:
        rows = []
        for record in test_records:
            prediction = comparator.predict(record)
            if prediction is not None and prediction not in {
                p.place_id for p in record.request.places
            }:
                raise ValueError("Comparator predicted an unknown candidate")
            rows.append(
                PairedOutcome(
                    record_id=record.record_id,
                    participant_id=record.participant_id,
                    place_time_group=record.place_time_group,
                    need=record.request.need.value,
                    correct=None if prediction is None else prediction == record.preferred_place_id,
                )
            )
        outcomes[comparator.name] = rows
        scored = [r for r in rows if r.correct is not None]
        metrics[comparator.name] = {
            "denominator": len(rows),
            "scored": len(scored),
            "abstentions": len(rows) - len(scored),
            "coverage": len(scored) / len(rows),
            "paired_choice_accuracy": sum(bool(r.correct) for r in scored) / len(scored)
            if scored
            else None,
            "errors": [r.record_id for r in scored if not r.correct],
            "by_need": {
                need: {
                    "n": sum(r.need == need for r in scored),
                    "errors": sum(r.need == need and not r.correct for r in scored),
                }
                for need in sorted({r.need for r in rows})
            },
            "configuration": comparator.configuration(),
        }
    result = {
        "dataset_id": dataset.dataset_id,
        "dataset_hash": dataset.digest,
        "protocol_version": dataset.protocol_version,
        "synthetic": dataset.synthetic,
        "interpretation": "Software fixture only; no empirical validation"
        if dataset.synthetic
        else "Exploratory; independent protocol review required",
        "metrics": metrics,
        "B0_minus_A1": clustered_difference(outcomes["B0-citysense"], outcomes["A1-tool-equipped"]),
        "B1_status": "not_implemented" if calibrated is None else "supplied_comparator",
        "outcomes": {name: [row.model_dump() for row in rows] for name, rows in outcomes.items()},
    }
    result["experiment_hash"] = content_hash(result)
    if calibrated is not None:
        result["B1_minus_A1"] = clustered_difference(
            outcomes["B1-calibrated"], outcomes["A1-tool-equipped"]
        )
        result["experiment_hash"] = content_hash(
            {k: v for k, v in result.items() if k != "experiment_hash"}
        )
    output.parent.mkdir(parents=True, exist_ok=True)
    # Exclusive create prevents accidental replacement of an experiment artifact.
    with output.open("x", encoding="utf-8") as artifact:
        json.dump(result, artifact, sort_keys=True, indent=2, allow_nan=False)
    return result
