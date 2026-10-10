"""Companion capture audit; does not modify protected statistical protocols."""

from typing import Self

from pydantic import AwareDatetime, Field, model_validator

from .evaluation import (
    BaselineArtifact,
    DatasetManifest,
    FrozenPrediction,
    FrozenToolBaseline,
    content_hash,
)
from .models import Contract, Identifier


class ToolReceipt(Contract):
    tool_id: Identifier
    request_hash: str = Field(pattern="^[a-f0-9]{64}$")
    response_hash: str = Field(pattern="^[a-f0-9]{64}$")
    requested_at: AwareDatetime
    received_at: AwareDatetime
    evidence_available_at: AwareDatetime

    @model_validator(mode="after")
    def ordered(self) -> Self:
        if self.requested_at > self.received_at or self.evidence_available_at > self.received_at:
            raise ValueError("Invalid tool receipt chronology")
        return self


class CapturedRun(Contract):
    record_id: Identifier
    request_hash: str = Field(pattern="^[a-f0-9]{64}$")
    choice: Identifier | None
    started_at: AwareDatetime
    finished_at: AwareDatetime
    model_response_hash: str = Field(pattern="^[a-f0-9]{64}$")
    total_tokens: int = Field(ge=0)
    tools: list[ToolReceipt] = Field(max_length=100)


class CaptureManifest(Contract):
    synthetic: bool
    dataset_hash: str = Field(pattern="^[a-f0-9]{64}$")
    model_id: Identifier
    prompt_hash: str = Field(pattern="^[a-f0-9]{64}$")
    tool_configuration_hash: str = Field(pattern="^[a-f0-9]{64}$")
    information_budget_id: Identifier
    latency_budget_seconds: float = Field(gt=0)
    max_tool_calls: int = Field(ge=1, le=100)
    max_total_tokens: int = Field(ge=1, le=1000000)
    allowed_tools: list[Identifier] = Field(min_length=1, max_length=20)
    # Frozen by the independent information steward; hashes of permitted responses per query.
    allowed_response_hashes: dict[str, list[str]]
    runs: list[CapturedRun] = Field(min_length=3)


def audit_capture(capture: CaptureManifest, dataset: DatasetManifest) -> BaselineArtifact:
    capture = CaptureManifest.model_validate(capture.model_dump())
    dataset = DatasetManifest.model_validate(dataset.model_dump())
    if capture.dataset_hash != dataset.digest or capture.synthetic != dataset.synthetic:
        raise ValueError("Capture does not match frozen dataset")
    records = {r.record_id: r for r in dataset.records}
    if set(capture.allowed_response_hashes) != set(records):
        raise ValueError("Information envelope must cover exactly the candidate universe")
    predictions: list[FrozenPrediction] = []
    for run in capture.runs:
        if run.record_id not in records:
            raise ValueError("Unknown captured record")
        record = records[run.record_id]
        elapsed = (run.finished_at - run.started_at).total_seconds()
        if (
            not 0 <= elapsed <= capture.latency_budget_seconds
            or run.finished_at > record.request.decision_at
        ):
            raise ValueError("Capture exceeds decision/time budget")
        if run.request_hash != content_hash(record.request.model_dump(mode="json")):
            raise ValueError("Capture input differs from frozen request")
        if len(run.tools) > capture.max_tool_calls or run.total_tokens > capture.max_total_tokens:
            raise ValueError("Capture exceeds tool/token budget")
        if not capture.synthetic and not run.tools:
            raise ValueError("A genuine tool-equipped run requires tool receipts")
        for receipt in run.tools:
            if (
                receipt.tool_id not in capture.allowed_tools
                or receipt.response_hash not in capture.allowed_response_hashes[run.record_id]
            ):
                raise ValueError("Tool response is outside frozen information envelope")
            if not run.started_at <= receipt.requested_at <= receipt.received_at <= run.finished_at:
                raise ValueError("Tool receipt is outside run interval")
            if receipt.evidence_available_at > record.request.decision_at:
                raise ValueError("Tool evidence contains future knowledge")
        predictions.append(
            FrozenPrediction(
                record_id=run.record_id,
                request_hash=run.request_hash,
                choice=run.choice,
                available_at=run.finished_at,
            )
        )
    artifact = BaselineArtifact(
        name="A1-tool-equipped",
        synthetic=capture.synthetic,
        model_id=capture.model_id,
        prompt_hash=capture.prompt_hash,
        tool_configuration_hash=capture.tool_configuration_hash,
        information_budget_id=capture.information_budget_id,
        latency_budget_seconds=capture.latency_budget_seconds,
        predictions=predictions,
    )
    FrozenToolBaseline(artifact, dataset)
    return artifact
