# Prospective strong A1 execution infrastructure — Sprint 3

Implemented: `baseline_runner.py`, `prospective_audit.py`, `scripts/run_a1.py` and
`scripts/compare_a1_b0.py`. Genuine external A1 execution: **NOT RUN**. Empirical accuracy:
**NOT EVALUATED**. No credential, paid call or human label was used during this sprint.

The prospective manifest freezes unique scenario IDs, a shared information-budget ID, candidate
geometry, an EvaluateRequest, freeze time, source/version/licence and capture/transfer declarations.
Its JSON schema forbids extra fields. Request candidates and geometry IDs must match. Source
research/cache permission, evidence retrieval/issuance and geometry availability are checked at
freeze time. Free-form feature annotations are restricted to provenance fields. Human labels,
participant IDs, CitySense outputs and scoring weights have no input fields. Names/provenance
still need steward review: a schema cannot detect every semantic leak embedded in allowed text.

The model sees need, times, walking limit and candidate IDs, then must call `read_frozen_context`.
That tool returns only the frozen typed manifest context; there is no live search or arbitrary URL
tool. Candidate geometry is source-reported, not field verification. Missing routing, weather and
availability stay unknown. Terminal output is strictly `{"choice": ID_OR_NULL, "reason": TEXT}`;
invented or walking-ineligible choices invalidate the run. This is a controlled comparator envelope,
not proof that this model/tool configuration constitutes a sufficiently strong scientific baseline.

ModelClient separates orchestration from provider I/O. OpenAIResponsesClient uses a fixed HTTPS
Responses endpoint, no redirects/proxy environment/SDK retries, `store:false`, configurable model,
output-token limit and optional reasoning effort. Response model ID must exactly match the configured
ID; choose a reviewed supported snapshot, not an unpinned alias that resolves to another ID.
All returned function/reasoning output items are retained and passed into the next request.
Implementation follows [official function calling](https://developers.openai.com/api/docs/guides/function-calling).
`store:false` does not guarantee zero provider retention; review
[provider data controls](https://developers.openai.com/api/docs/guides/your-data) before transfer.

Each request reserves UTF-8 payload bytes plus 4096 framing tokens and the output cap against the
total token/cost budget. This conservative engineering allowance is not a provider tokenizer proof.
Reported input/output/total usage must reconcile and fit the reservation; otherwise the run is
invalid. Declared per-million tariffs are operator-reviewed configuration, not fetched prices or an
invoice. Reported tariff cost and reserved worst-case cost are separate; billing_verified stays false.
Reservations include unsuccessful attempts. Only 429 is retried, at most max_requests with a one-second
delay and the same caps. Timeouts, transport errors, redirects, other HTTP errors, excessive response
size, malformed outputs, tool/request/token/cost exhaustion, model mismatch and late completion have
explicit terminal states. Ambiguous billed timeouts/5xx are not automatically retried.

The latency budget limits dispatch and transport timeouts; each body chunk checks the deadline.
A blocked network phase may return after the nominal deadline; late results are never eligible.
Future live deployment needs measured cancellation/account usage behavior and provider-side spending
limits. No numeric cost or latency observation here describes a real model call.

Receipts use unique exclusive `.jsonl` files, hash-chained start/request/response/tool/failure/finish
events. Successful raw response text and exact submitted JSON/messages/tool outputs are retained;
authorization headers and keys are omitted. Provider IDs/model/usage appear in the raw response.
`verify_receipt` detects truncation and ordinary tampering. An OS administrator can replace a file
and recompute hashes; independent archive anchoring/account receipts remain required. Permission
declarations cover local capture and no personal data. No generic raw participant prompts are accepted.

From `services/api`, reproduce the invented offline cases:

```powershell
uv run --locked python scripts/run_a1.py --manifest tests/fixtures/prospective-manifest.json --config tests/fixtures/a1-fixture-config.json --output ../../artifacts/sprint3/new-offline-a1
```

The shipped scenarios are fixed historical synthetic fixtures; only fixture mode permits their
retrospective timing. They are not scientifically eligible historical model runs. Response behavior
is deterministic; receipt IDs/times are actual local execution metadata. The CLI completed three
synthetic captures with null choices and invented usage of 280 tokens each. Live mode rejects
synthetic inputs, missing transfer/redistribution permissions and decisions already reached.

For a later authorized live run, independently freeze a real label-free manifest before a future
decision and prepare a config matching `docs/contracts/a1-runner-config.schema.json`: provider
`openai`, reviewed exact model ID, positive current tariffs, pricing_reviewed_at, budgets and optional
reasoning_effort. Set OPENAI_API_KEY in the local process; do not place it in a manifest or receipt.

```powershell
uv run --locked python scripts/run_a1.py --manifest PATH_TO_APPROVED_MANIFEST --config PATH_TO_REVIEWED_CONFIG --output PATH_TO_PRIVATE_RECEIPTS --authorize-live
```

After separate consent/protocol/privacy approval and independent blinded labels, freeze dataset
and holdout groups. Join only with the same scenario/record IDs, exact request hashes and information/
latency budget. The later join requires complete successful/abstaining receipt coverage, compatible
real/synthetic flags and frozen output hashes. Failed runs block comparison until an independently
reviewed missingness policy exists; they cannot be silently removed from the denominator.

```powershell
uv run --locked python scripts/compare_a1_b0.py --manifest MANIFEST --config CONFIG --receipts RECEIPT1 RECEIPT2 RECEIPT3 --dataset INDEPENDENT_LABEL_DATASET --output NEW_RESULT --review-approved-data
```

The flag is an operator declaration, not an approval system. Existing A0/A1/B0, holdout, embargo,
crossed-bootstrap and B1 fit/tuning safeguards remain unchanged. The synthetic later-join test is
software evidence only. Genuine comparator strength, approved estimand, source equivalence and
sufficient independent clusters remain open.
