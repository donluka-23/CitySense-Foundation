# ADR-0007: Explicit hypothesis parameters and fail-closed paired evaluation

Date: 2026-10-09. Status: implemented infrastructure; independent research review pending.
Extends ADR-0003. The protected evaluation protocol remains a draft requiring sign-off.

## Problem and constraints

The engine has no validated psychological construct or locally calibrated labels.
Software must reproduce ranking, preserve missingness, explain each contribution and
support a fair future comparison without inventing an accuracy result or a weak baseline.

## Decision

Keep the three existing need hypotheses and existing weights, now in a packaged,
versioned JSON model. Validate positive weights, completeness and sums; compute a
canonical JSON SHA-256 hash. Transform only normalized fractions through a named identity
transform. Traffic proximity means a structural proxy with higher values farther from
traffic; it is not noise dB. Walking-time eligibility precedes ranking. Every required
feature must be present and usable, irrespective of its weight. Missing or stale values
cause abstention without reweighting. Parameterized freshness limits are conservative
engineering hypotheses, not empirically established lifetimes. Forecast freshness is age
at the decision, separate from target validity. Contributions and confidence limitations
are returned; no psychological units or probability claims appear.

Use typed, immutable-content dataset manifests and synthetic paired-choice fixtures.
Train/validation/test separation checks participant, both places, spatial block, time
block and paired place-time group. Chronological separation includes a declared embargo.
Connected components propose splits; invalid or insufficient independent groups fail.
The manifest validator is the final gate, including for proposed splits.

A0 is nearest eligible. A1 imports frozen tool-equipped outputs with exact request hashes,
source availability, configuration/prompt hashes and matching information/time budgets.
The shipped A1 artifact is synthetic, with no LLM or mapping tools executed. B0 invokes
the deterministic engine. B1 is an adapter boundary only; supplied artifacts must declare
train-only fitting and validation-only tuning IDs. Software cannot prove those declarations
truthful; a real fitted artifact requires independent review and reproducible training code.

Metrics retain scored and total denominators, abstention, paired accuracy and need-level
errors. Brier scoring accepts probability arrays explicitly and is not applied to heuristic
scores. Paired differences use seeded crossed participant/place-time bootstrap resampling
on common scored records, with unavailable intervals for insufficient clusters. This
exploratory estimator needs scientific review, especially with few clusters. Outputs use
exclusive-create files and content hashes so experiments are reproducible and not overwritten.

## Alternatives and risks

LLM ranking is unrepeatable without frozen tools and prompts; trainable models lack data.
Event-wise random splits leak shared people/places. Reweighting missing features changes
the meaning of scores. Proxy quality classes are categorical provenance, not confidence
probabilities. Overlapping participant/place/time groups can collapse to one component;
the protocol must acquire independent groups, never relax checks to force a holdout.
No sample-size sufficiency, construct validity, superiority or field results are claimed.

## Evidence and revisit

Tests exercise fixture determinism, abstention, calibration holdout rejection, baseline
information mismatch and all leakage dimensions. Revisit weights, freshness, blocks,
bootstrap design and labeling only with independent research review and train-only evidence.
See [Sprint report](../SPRINT_1_REPORT.md) and [protocol](../evaluation-protocol.md).
