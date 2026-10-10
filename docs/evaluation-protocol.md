# Pre-registered evaluation protocol | draft v0.1 (requires scientific reviewer sign-off)

## Primary question
Does CitySense increase correct paired-choice prediction of *experienced suitability* against a strong tool-equipped LLM+Maps+weather baseline under matched information and time budgets?

## Unit and sample
Batumi, ~20–30 purposively sampled micro-places across nearby matched contrasts (shade/open, green/hardscape, low/high traffic proxy) and 3 narrowly defined needs. Planned 150–250 consented independent survey records as exploratory pilot, **not a confirmatory power guarantee**. Multiple observations at same place/time are clustered; comparisons need both places experienced by participants or independent blinded assessors.

## Ground truth
Participants independently report 1–5 activity suitability and thermal/quietness perception after exposure; retain visit time and route, exposure duration, weather, limitations and consent. For paired places, require comparable circumstances, randomized order where practical, plus stratification by time/day. Do not treat acceptance/clicks as ground truth.

## Models
- A0: trivial nearest/open/popularity rule, for sanity check.
- A1: **strong** tool-equipped LLM + available maps, weather and same candidate information as CitySense.
- B0: CitySense deterministic model with predeclared weights.
- B1: CitySense calibrated on training subset only.

## Split and leakage
Freeze evaluation data dictionary and primary metric before pilot. Group splits by place and collection-time windows; avoid person leakage. Primary independent holdout reserved and not used for tuning. Freeze model hashes, source snapshots and prompt/tool configurations, including forecast `issued_at` <= recommendation timestamp. If 250 examples insufficient for robust group holdout, report uncertainty prominently; no misleading significance.

## Outcomes
Primary: paired-choice accuracy on independent holdout with participant/place-time clustered bootstrap confidence interval, comparing B1-A1 and B0-A1. Secondary: Brier score for calibrated probabilities (only if genuine probabilities), abstention/coverage, API response latency p95, error/retry rate, per-session cost, and subgroup performance across needs/micro-settings. Report denominator and missingness.

## Decision gates (project targets, not funder requirements)
- Data quality: ≥95% snapshots include time/source/quality, 0 unsupported high-resolution sensor claims.
- Functionality: 100% mandatory rule invariant tests pass; evaluation reproducible from immutable versioned manifest.
- Research: enough independently labeled paired contrasts to estimate improvement interval; no claim of superiority if 95% interval includes zero.
- Safety: 0 known critical privacy/security issues before any real-user exposure.
- Business: at least 3 external interviews or integration demonstrations are *learning signals*, not claimed purchase commitments.

## Failure modes and mitigations
Weather homogeneity => focus matched micro-place contrasts. Spatial proxy not equal perception => human ground truth. Weak comparator => shared candidate feeds and tool budgets. Seasonality => restrict extrapolation. Selection effects => blinded exposure + stratification. Provider deals => separate from evaluator and organic ranking.

## Sign-offs required before field use
Research lead; privacy steward; reviewer external to scoring implementation. Store decisions/change log. Any post-preregistration change tagged exploratory.

## Sprint 1 technical support (2026-10-09)

The protocol above remains a draft; no scientific sign-off or field results have been added.
`evaluation.py` implements paired manifests with provenance/synthetic flags and participant,
place, place-time, spatial-block and time-block split checks. Chronological separation has
a declared embargo. Connected components propose splits; the manifest gate rejects invalid
overlap and insufficient independent groups. All shipped records are software fixtures.

A1 accepts frozen tool-equipped outputs with matching request hashes, information/time
budgets and prompt/tool configurations. Bundled A1 outputs are synthetic; no tool-equipped
model was executed. B0 invokes the deterministic engine. B1 remains a future adapter whose
train-only fit and validation-only tuning declarations require independent verification.

The harness reports paired accuracy denominators, abstention and need-level errors. Seeded
crossed participant/place-time bootstrap intervals use common scored pairs and are exploratory;
too few clusters yield no interval. The estimator, blocks, freshness assumptions and sample
sufficiency require scientific review before field use. Brier score is only for genuine
probabilities. Operational latency/retry/cost measurements remain separate from deterministic
experiment hashes. Telemetry stubs are not operational benchmark results. See ADR-0007.
