"""Later, separate receipt-to-label join. Not imported by generation or model clients."""

import json
from datetime import datetime
from pathlib import Path

from .baseline_capture import CapturedRun, CaptureManifest, ToolReceipt, audit_capture
from .baseline_runner import (
    PROMPT,
    TOOLS,
    Choice,
    ProspectiveManifest,
    RunnerConfig,
    verify_receipt,
)
from .evaluation import BaselineArtifact, DatasetManifest, content_hash


def join_reviewed_receipts(
    manifest: ProspectiveManifest,
    config: RunnerConfig,
    receipts: list[Path],
    dataset: DatasetManifest,
) -> BaselineArtifact:
    manifest = ProspectiveManifest.model_validate(manifest.model_dump())
    config = RunnerConfig.model_validate(config.model_dump())
    dataset = DatasetManifest.model_validate(dataset.model_dump())
    scenarios = {s.scenario_id: s for s in manifest.scenarios}
    if (
        set(scenarios) != {r.record_id for r in dataset.records}
        or manifest.information_budget_id != dataset.information_budget_id
        or config.latency_seconds != dataset.latency_budget_seconds
    ):
        raise ValueError("Candidate universe or information/latency budget mismatch")
    runs = []
    for path in receipts:
        events = verify_receipt(path)
        start, finish = events[0]["value"], events[-1]["value"]
        scenario = scenarios.get(finish["scenario_id"])
        if scenario is None or start["frozen_context"] != scenario.model_dump(mode="json"):
            raise ValueError("Captured context differs from prospective manifest")
        if (
            start["dataset_hash"] != manifest.digest
            or finish["dataset_hash"] != manifest.digest
            or start["scenario_hash"] != scenario.digest
            or finish["scenario_hash"] != scenario.digest
            or start["config"] != config.model_dump(mode="json")
            or start["prompt_hash"] != content_hash(PROMPT)
            or start["tools_hash"] != content_hash(TOOLS)
            or finish["synthetic"] != dataset.synthetic
            or finish["provider"] != config.provider
            or finish["model_id"] != config.model_id
        ):
            raise ValueError("Receipt provenance/configuration mismatch")
        if finish["status"] not in {"completed", "abstained"}:
            # No silently dropping failed runs from the comparison denominator.
            raise ValueError("Failed run requires reviewed missingness policy; comparison blocked")
        tool_events = [e for e in events if e["kind"] == "tool"]
        responses = [e["value"]["raw"] for e in events if e["kind"] == "response"]
        requests = [e["value"] for e in events if e["kind"] == "request"]
        if (
            not tool_events
            or not responses
            or finish["tool_calls"] != len(tool_events)
            or finish["reserved_tokens"] > config.max_total_tokens
            or finish["reserved_cost_usd"] > config.max_cost_usd
        ):
            raise ValueError("Receipt budget or tool mismatch")
        if not 1 <= len(requests) <= config.max_requests:
            raise ValueError("Request count outside capture budget")
        if (
            sum(r["reserved_tokens"] for r in requests) != finish["reserved_tokens"]
            or abs(sum(r["reserved_cost_usd"] for r in requests) - finish["reserved_cost_usd"])
            > 1e-12
        ):
            raise ValueError("Request reservations differ from reported totals")
        for r in requests:
            payload = r["payload"]
            if (
                payload.get("model") != config.model_id
                or payload.get("store") is not False
                or payload.get("instructions") != PROMPT
                or payload.get("tools") != TOOLS
                or payload.get("max_output_tokens") != config.max_output_tokens
            ):
                raise ValueError("Submitted request differs from frozen configuration")
        actual_tokens, actual_cost = 0, 0.0
        parsed_responses = [json.loads(raw) for raw in responses]
        for response in parsed_responses:
            counts = [
                response["usage"][k] for k in ("input_tokens", "output_tokens", "total_tokens")
            ]
            if (
                any(type(n) is not int or n < 0 for n in counts)
                or sum(counts[:2]) != counts[2]
                or response.get("model") != config.model_id
                or not response.get("id")
                or response.get("status") != "completed"
            ):
                raise ValueError("Retained provider response is invalid")
            actual_tokens += counts[2]
            actual_cost += (
                counts[0] * config.input_usd_per_million + counts[1] * config.output_usd_per_million
            ) / 1000000
        if (
            actual_tokens != finish["total_tokens"]
            or abs(actual_cost - finish["tariff_cost_usd"]) > 1e-12
        ):
            raise ValueError("Provider usage differs from reported accounting")
        text = "".join(
            c["text"]
            for o in parsed_responses[-1]["output"]
            if o.get("type") == "message"
            for c in o.get("content", [])
            if c.get("type") == "output_text"
        )
        terminal = Choice.model_validate_json(text)
        if terminal.model_dump() != finish["prediction"]:
            raise ValueError("Prediction differs from retained model output")
        if terminal.choice is not None and terminal.choice not in {
            p.place_id
            for p in scenario.request.places
            if p.walk_minutes <= scenario.request.max_walk_minutes
        }:
            raise ValueError("Prediction violates hard walking constraint")
        tools = []
        for e in tool_events:
            value = e["value"]
            if (
                value["output_hash"] != scenario.digest
                or value["name"] != "read_frozen_context"
                or json.loads(value["arguments"]) != {}
                or content_hash(json.loads(value["output"])) != scenario.digest
            ):
                raise ValueError("Tool output outside frozen envelope")
            at = datetime.fromisoformat(e["at"])
            tools.append(
                ToolReceipt(
                    tool_id="read_frozen_context",
                    request_hash=content_hash({}),
                    response_hash=scenario.digest,
                    requested_at=at,
                    received_at=at,
                    evidence_available_at=scenario.frozen_at,
                )
            )
        runs.append(
            CapturedRun(
                record_id=scenario.scenario_id,
                request_hash=finish["request_hash"],
                choice=finish["prediction"]["choice"],
                started_at=datetime.fromisoformat(finish["started_at"]),
                finished_at=datetime.fromisoformat(finish["finished_at"]),
                model_response_hash=content_hash(responses),
                total_tokens=finish["total_tokens"],
                tools=tools,
            )
        )
    capture = CaptureManifest(
        synthetic=dataset.synthetic,
        dataset_hash=dataset.digest,
        model_id=config.model_id,
        prompt_hash=content_hash(PROMPT),
        tool_configuration_hash=content_hash(TOOLS),
        information_budget_id=manifest.information_budget_id,
        latency_budget_seconds=config.latency_seconds,
        max_tool_calls=config.max_tool_calls,
        max_total_tokens=config.max_total_tokens,
        allowed_tools=["read_frozen_context"],
        allowed_response_hashes={key: [s.digest] for key, s in scenarios.items()},
        runs=runs,
    )
    return audit_capture(capture, dataset)
