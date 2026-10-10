# Research validation readiness — REVIEW REQUIRED

Sprint 3 improves engineering readiness only. No participants, independent labels, strong model
run or calibrated model were produced. Synthetic test accuracy is not empirical performance.
The existing `evaluation-protocol.md` is protected and unchanged: SHA256
`1186d4cf97620b4144ac87fc41beca91851d7ae14c58bf93d96f588ca84f2b61`.
This document is a proposal beside that draft, not a silent protocol amendment or preregistration.

## Observable targets and feasible scope

| Need hypothesis | Proposed observable paired target | Missing evidence / feasibility |
|---|---|---|
| Thermal walking suitability (`cool_walk`) | Independently reported experienced walking suitability after matched exposure; separately record thermal perception | Regional forecast cannot measure street temperature/radiation. Current shade/green proxies lack wind/radiant heat/humidity; October Batumi contrast may be weak. Review primary feasibility before field work |
| Quiet rest (`quiet_rest`) | Experienced short-rest suitability, separate acoustic/traffic assessment using reviewed measurement method | Road proximity is not dB or quietness. Nontraffic noise and event timing uncontrolled. Best candidate for initial narrow pilot if paired contrast/reliability sufficient |
| Family walking (`family_walk`) | Reviewed adult assessor route/place suitability under explicit access/safety conditions | Shade/greenery omit crossing safety, pavement, step-free access and facilities; broad construct unreliable within timeline. Defer primary family claim pending operational definition; no child recruitment |

Retain all three engine enums and frozen hypotheses; do not change weights because one appears
unpromising. A research reviewer may prioritize one observable primary task and classify others
exploratory. Any change requires dated amendment and new protocol/model version, not retuning holdout.
Hard walking constraints remain separate from soft scores. A null score is abstention; weights are
not renormalized. Proxy/forecast/spatial uncertainty and measured values remain distinct.

## Initial 24 micro-location sampling proposal

Propose twelve nearby matched pairs (24 locations), with four pairs each exploring vegetation/open
exposure, building/tree shade/open hardscape, and low/high traffic-proximity contrasts. Cross these
with coastal/inland setting, pedestrian continuity, sheltered/open exposure and observation time.
Use candidate polygons/short route segments where appropriate; current API stores point anchors.
Select approximate contrasts from licensed spatial evidence, then confirm physically under an
approved protocol. No actual 24 named locations or measured contrasts are fabricated here.

Reject unsafe/inaccessible sites, uncertain identity and insufficient evidence before enrollment.
Record exclusion reasons and overlaps. Confirm pair exposure durations and separation preserve
comparable weather/time; randomized order and blinded assessment should be considered. Regional
weather is shared context, not artificial Batumi weather zones. Purposive sampling is not citywide
representation. Planned 150–250 records in the existing draft is not a power guarantee: number of
independent people, places, days and components determines usable inference.

## Systems, information and freezing

| System | Executable / planned | Required evidence |
|---|---|---|
| A0 | Existing nearest-eligible transparent static rule | Same candidates/hard eligibility; no contextual evidence |
| A1 | FrozenToolBaseline plus new capture audit; genuine run pending | Exact strong model version, prompt hash, tool config, lawful Maps/weather/context archives, candidate hash, timed receipts, token/tool/time budgets and response hash |
| B0 | Existing deterministic `heuristic-0.2.0` engine | Frozen parameters/feature transformation and identical available candidate evidence |
| B1 | Future train-only calibration adapter | Independent fit provenance and code/artifact review; tuning on validation only, test never used |

CaptureManifest binds the dataset hash, information budget, allowed tools/response hashes, token
and tool caps, wall time and run receipts. `audit_capture` rejects input/universe mismatch, duplicate
outputs, unapproved tool responses, future knowledge and excessive budgets; it returns the existing
baseline format after its normal validation. Real-design captures require tool receipts. All shipped
tests invent receipts; no model calls are represented as genuine.

Future execution sequence: independent steward freezes per-record input envelopes and lawful tool
responses before decision; freeze model/prompt/config/budgets; run model with those responses and
archive actual provider response/usage evidence; hash and audit outputs; independently verify receipts;
then collect labels without exposing rankings; freeze dataset/splits; evaluate once on holdout.
Current dataset schema includes labels, so a future runner must receive an explicitly label-free
projection. Never hand full DatasetManifest to a model. Hashes and declared token counts alone do
not prove provider execution, model strength, envelope equivalence or absence of label leakage.
Prospective runs must finish before decision, rather than retrospectively calling current Maps
and pretending that data was historically available.

## Statistical review proposal

The existing estimator separately resamples participants and place-time groups, multiplying
resampling counts on common scored pairs. This is a pigeonhole-style crossed bootstrap, motivated
by [Owen's original paper](https://arxiv.org/abs/0712.1111) and
[Owen/Eckles on crossed arrays](https://arxiv.org/abs/1106.2125). Those results do not automatically
validate this pilot design, binary paired accuracy, chosen grouping or percentile interval.

REVIEW REQUIRED: repeated place across days and shared weather/time blocks can correlate across
place-time IDs. Two clusters per dimension, the software's minimum, is not adequate scientific
sample evidence. Unbalanced sparse crossing, missing scores and discarded empty bootstrap samples
can destabilize intervals. The current difference conditions on both systems scoring; selective
abstention can bias its interpretation. It is not an all-query improvement estimate.

Before field use, propose a statistician-reviewed target estimand and dependence graph; simulate
the planned participants/place/day structure and abstention; inspect effective independent clusters;
compare crossed-place/time resampling, component-block or randomization-based alternatives as
appropriate; set minimum cluster and supported-draw criteria and publish sensitivity/coverage.
Retain the current estimator as exploratory until approval. Do not silently replace it.

Existing grouped splits prevent participant, place, place-time, spatial and time leakage and require
chronological embargo. Connected components may collapse most records into too few groups; preflight
the real collection plan and report inability to hold out rather than relaxing checks. Review whether
the estimand is unseen-place transfer or repeated-place temporal generalization; these need different
explicitly approved split designs. Calibration fit/tuning declarations require actual artifact review.

Primary draft metric is paired-choice accuracy on independent holdout; report total/scored/common
denominators, coverage/abstention, needs/errors and uncertainty. Scores are not probabilities; Brier
is allowed only after genuine probability calibration. Separately observe p95 latency, retries/errors,
provider/tool/tokens cost and subgroup missingness. No superiority claim from software fixture intervals.

## Field collection gate

No participant-level information until independent consent, retention, lawful basis, withdrawal,
access controls, blinded assessor instructions and safety review are complete. `consent=true` in
a manifest is a declaration, not evidence that those workflows exist. Keep withdrawal-capable
participant stores separate from immutable nonpersonal environmental evidence. Named sign-offs
are research lead, external statistician/reviewer, privacy steward and source data steward;
all remain pending. The prospective runner is implemented; the next task is an actual reviewed
lawful micro-site/feature envelope and authorized strong A1 capture, alongside primary-need review.

## Sprint 3 implementation and outstanding scientific decisions

Generation now accepts ProspectiveManifest only, containing typed candidates/geometry/features,
freeze/source times and permission declarations, without labels, participant IDs or B0 results.
The later `join_reviewed_receipts` validates request hashes/universe, envelope, budgets, capture
chronology and complete receipts before returning the original frozen-baseline artifact. Failed
runs block joining; they cannot be selectively removed. The independent missingness/estimand policy
must define failed runs, abstentions and common-score denominators before genuine comparison.
See [runner](A1_BASELINE_RUNNER.md). Synthetic receipts are not actual model/account attestation.

Proposed initial narrow target is quiet-rest comparison at fixed site/time windows with independent
acoustic-exposure checks. LAeq contrast can test one observable dimension; it cannot replace
independent experienced-rest labels or establish psychological benefit. Site/entrance/access,
greenery footprint, traffic-fraction orientation and nontraffic noise require reviewed methods.
Five real OSM boundary points provide geometry only, not the proposed 24 verified locations. No
LAeq values, field labels, weather or scoring fractions were fabricated or collected.

Information equivalence requires steward approval of candidate geometry, legitimate historical
feature/forecast availability, walking assumptions and tool budget. More raw geometry for A1 is not
automatically equivalent to B0's normalized features. Strong model selection/configuration and a
real run are pending. The protected draft and exploratory estimator remain unchanged. Without
approved independent labels, A1/B0 accuracy, effect size, statistical superiority and cross-city
transfer are **NOT EVALUATED**. A technically non-null score would not change this status.
