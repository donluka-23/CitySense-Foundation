from datetime import timedelta

import pytest
from test_evaluation import dataset

from citysense.baseline_capture import CapturedRun, CaptureManifest, ToolReceipt, audit_capture
from citysense.evaluation import content_hash


def captured(data):
    runs = []
    for record in data.records:
        end = record.request.decision_at
        runs.append(
            CapturedRun(
                record_id=record.record_id,
                request_hash=content_hash(record.request.model_dump(mode="json")),
                choice=None,
                started_at=end - timedelta(seconds=2),
                finished_at=end,
                model_response_hash="a" * 64,
                total_tokens=100,
                tools=[
                    ToolReceipt(
                        tool_id="frozen-map-read",
                        request_hash="b" * 64,
                        response_hash="c" * 64,
                        requested_at=end - timedelta(seconds=1),
                        received_at=end,
                        evidence_available_at=end - timedelta(hours=1),
                    )
                ],
            )
        )
    return CaptureManifest(
        synthetic=True,
        dataset_hash=data.digest,
        model_id="synthetic-model-no-execution",
        prompt_hash="d" * 64,
        tool_configuration_hash="e" * 64,
        information_budget_id=data.information_budget_id,
        latency_budget_seconds=data.latency_budget_seconds,
        max_tool_calls=2,
        max_total_tokens=1000,
        allowed_tools=["frozen-map-read"],
        allowed_response_hashes={r.record_id: ["c" * 64] for r in data.records},
        runs=runs,
    )


def test_capture_produces_compatible_frozen_artifact_with_receipts():
    data = dataset()
    capture = captured(data)
    artifact = audit_capture(capture, data)
    assert artifact.synthetic and len(artifact.predictions) == len(data.records)
    assert all(p.choice is None for p in artifact.predictions)


@pytest.mark.parametrize(
    "mutation", ["hash", "future", "tokens", "tools", "envelope", "chronology", "duplicate"]
)
def test_capture_rejects_budget_information_time_and_universe_violations(mutation):
    data = dataset()
    capture = captured(data)
    if mutation == "hash":
        capture.dataset_hash = "f" * 64
    elif mutation == "future":
        capture.runs[0].finished_at += timedelta(hours=1)
    elif mutation == "tokens":
        capture.runs[0].total_tokens = 1001
    elif mutation == "tools":
        capture.runs[0].tools[0].tool_id = "unapproved-tool"
    elif mutation == "envelope":
        capture.runs[0].tools[0].response_hash = "f" * 64
    elif mutation == "chronology":
        capture.runs[0].tools[0].requested_at -= timedelta(hours=1)
    else:
        capture.runs.append(capture.runs[0])
    with pytest.raises(ValueError):
        audit_capture(capture, data)


def test_real_capture_without_tools_is_rejected():
    data = dataset().model_copy(deep=True)
    data.synthetic = False
    # Mock consent to exercise the next guard; these remain invented test records.
    for record in data.records:
        record.consent = True
    capture = captured(data)
    capture.synthetic = False
    capture.runs[0].tools = []
    with pytest.raises(ValueError, match="tool receipts"):
        audit_capture(capture, data)
