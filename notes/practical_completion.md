# Practical completion record

The planned experimental programme, final source review and repository integration are complete. The selected implementation is cumulative EXP-005; all 35 working source files match the measured snapshot. The ACT-0023 repository check found the final source/results history on local main and its matching remote-tracking ref at [b2bd620d3eac](source_revisions.md).

## Completed work

| Stage | Outcome | Detailed record |
|---|---|---|
| Baseline and measurement process | Source identity, sampled functional checks, raw timing pilot and reduction counts accepted | [EXP-000](experiments/EXP-000-baseline.md) |
| Arithmetic trials | Five cumulative treatments evaluated; mixed and inconclusive outcomes retained | [Experiment register](experiment_register.md) |
| Dynamic secret-flow assessment | 144 quiet target processes; all 18 deliberate positive controls detected | [EXP-007 result](runs/EXP-007-RUN-0001.md) |
| Statistical timing screen | No target threshold crossing within the finite budget; all positive/negative controls meet criteria | [EXP-008 result](runs/EXP-008-RUN-0001.md) |
| Final performance comparison | Three sessions completed; 972000 duration rows audited | [Complete comparison](final_comparison.md) |
| Candidate selection | Repeated additional keygen benefit balanced against small regressions and code/local-stack costs | [Selection rationale](final_candidate.md) |
| Reproducible outputs | Final tables, audit reports and figures regenerate byte-for-byte | [Figures and captions](thesis_figures.md) |
| Final source | Exact 35-file selected snapshot verified and integrated | [Source review](evidence/ACT-0022/selected-source-review.json) |

The numerical and security findings retain their recorded scope. No further performance session or optimisation is required by the completed protocol. A fresh-environment rerun, formal constant-time proof, physical/fault testing, final ML-KEM certification and an AVX2 transfer study are not established by this work.

## Thesis preparation

The remaining work is composition and presentation: describe the completed methods, present the measured effects and adverse findings, discuss the implementation tradeoffs and limitations, and verify literature-dependent claims against full text before using them. The [writing plan](thesis_writing_plan.md) maps the evidence to the original research questions. The [conditions record](benchmark_conditions.md) supplies the recorded setup and explicitly separates retrospective recollections and unavailable controls. The thesis draft and code/evidence repository will support supervisor feedback.

EXP-004 remains an optional interaction study requiring separately controlled variants. Its deferral does not create an unfinished part of the completed experimental programme. VTune was excluded from the chosen scope; reduction counts and controlled comparisons do not become profiler-based time attribution.
