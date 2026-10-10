"""Content-addressed hypothesis parameters; never fitted using a holdout."""

import hashlib
import json
from importlib.resources import files
from math import isclose
from typing import Self

from pydantic import Field, model_validator

from .models import FEATURE_KEYS, Contract, FeatureQuality, Need


class Parameters(Contract):
    model_config = {"frozen": True, "extra": "forbid", "allow_inf_nan": False}
    version: str
    transformation: str
    weights: dict[Need, dict[str, float]]
    max_age_seconds: dict[FeatureQuality, int] = Field(min_length=1)

    @model_validator(mode="after")
    def complete_model(self) -> Self:
        if set(self.weights) != set(Need) or set(self.max_age_seconds) != set(FeatureQuality):
            raise ValueError("Incomplete parameters")
        if self.transformation != "identity_normalized_fraction-v1":
            raise ValueError("Unknown feature transformation")
        for weights in self.weights.values():
            if not weights or not set(weights) <= set(FEATURE_KEYS):
                raise ValueError("Unknown/empty feature weights")
            if any(w <= 0 or w > 1 for w in weights.values()):
                raise ValueError("Weights must be positive fractions")
            if not isclose(sum(weights.values()), 1.0, abs_tol=1e-12):
                raise ValueError("Weights must sum to one")
        if any(age < 0 for age in self.max_age_seconds.values()):
            raise ValueError("Negative freshness limit")
        return self

    @property
    def digest(self) -> str:
        canonical = json.dumps(self.model_dump(mode="json"), sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(canonical.encode()).hexdigest()


def load_parameters() -> Parameters:
    return Parameters.model_validate_json(
        files("citysense").joinpath("parameters/heuristic-0.2.0.json").read_text(encoding="utf-8")
    )
