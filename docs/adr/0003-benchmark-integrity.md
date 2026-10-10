# ADR-0003: Strong baseline, protected test set, preregistration
Status: **Accepted for research starter** | Date: 2026-10-09

## Decision
Compare geographic rule baseline, strong tool-equipped LLM+Map/weather baseline, CitySense non-calibrated engine, and calibrated engine. Freeze all candidates/source-time snapshots, blind survey ordering, group by place/time and participant, and protect final test set from tuning.
## Alternatives
Compare against text-only LLM (too weak); evaluate only clicks (exposure bias); random event-wise split (leakage).
## Consequence
Slower experiment than demo; honest measurement of incremental value. Test criteria may fail, which is a valid result.

## Sprint 1 evidence

ADR-0007 implements the manifest, split gates, comparator boundary and exploratory metrics.
All delivered comparison data and A1 outputs are synthetic. No tool-equipped model,
calibration, study or superiority measurement has been performed. The protected draft
protocol still requires independent scientific/privacy review before field use.
