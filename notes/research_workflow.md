# Research methods and record conventions

The research record connects each question to a defined source treatment, validation checks, measurements and a bounded conclusion. The experiment register provides the index; run manifests, raw outputs and audit records supply the detailed evidence.

## Identifiers and evidence

| Identifier | Meaning |
|---|---|
| ACT | Research activity or review checkpoint |
| EXP | Experiment question and protocol |
| RUN | One execution attempt within an experiment |
| Variant | Source treatment used in a comparison |
| Block | Matched executions used to calculate a paired effect |

Identifiers are not reused. Failed or interrupted attempts retain their files, and retries receive new run IDs. A metadata-only record is not a benchmark. Experiment states distinguish proposed, planned, running, analysed and closed work; outcomes distinguish supported, not-supported, inconclusive and execution errors. Unperformed checks are recorded as not-run.

Source commits identify the code and support present before execution; results commits archive the later observations. Full commit IDs, tool/source/executable hashes, commands, exit codes and raw outputs make that distinction reproducible. Calendar dates, clock times and timezone fields are omitted from project narratives; publication years, software versions and measured durations retain their meaning.

Arithmetic changes and Git operations are performed manually. Research documentation uses direct first-person or neutral technical prose without attributing actions beyond the evidence. Corrections use new commits and preserve cited history.

## Experimental sequence

1. Specify the question, isolated change, predecessor, expected count effect, arithmetic assumptions, validation gates and measurement rules before collection.
2. Check caller ranges, Montgomery scale, intermediate widths, narrowing and downstream consumers, including invalid inputs.
3. Commit source and support before a formal run. The collector requires a clean Git-visible tree outside results/ and refuses an existing run directory.
4. Build explicitly, record tool and executable identities, collect raw observations and retain partial output after failure.
5. Analyse matched observations with the declared estimator. Preserve negative, mixed and inconclusive results.
6. Record the outcome, limitations and retention decision separately from the completion status of the runner.

A clean tree and a binary hash alone do not establish build provenance. The manifests retain the commands, inputs and outputs needed to connect each executable to its source. Development checks using uncommitted support are labelled separately and do not become formal performance results.

## Preservation and reproduction

Raw results, metadata snapshots, manifests, previous audit records and published figure/data artifacts remain unchanged. Derived corrections are recorded separately. Rebuildable binaries are ignored by Git; their commands and hashes remain in the manifests. Retained-data analysis can be repeated without recollecting measurements, while full binary-identity audits require the recorded executables or a separately documented rebuild.

The EXP-007/008/009 protocol Markdown files are hash-pinned inputs to existing collection and audit code. Their historical wording is retained verbatim. The corresponding accepted run records report the completed findings. Editorial revisions to other narratives do not modify numerical observations or change what was planned before measurement.

## Measurement and interpretation

Performance uses uninstrumented reference-C builds, deterministic public fixtures and CLOCK_MONOTONIC_RAW durations in nanoseconds. Fixture generation, warm-up, output comparison and CSV formatting are outside each measured operation. Operating-system randomness is excluded by the deterministic API mode. Reduction counts use separate instrumented builds and measure function calls, not instructions or runtime.

The early paired studies use five fresh process pairs per parameter. The closing study uses three separately launched sessions with 12 balanced three-variant blocks per parameter. Process medians produce paired time reductions; session medians and the median of three session estimates produce the final summary. Inner timing rows are not independent experimental repetitions. Pair/session ranges are descriptive, not confidence intervals, and separate-run incremental percentages cannot be added or multiplied into a cumulative gain.

Logical CPU affinity under WSL does not establish physical-core placement. Host/power/background conditions that were not recorded remain unknown. Compiler, source, tool, timer and observed-affinity identities constrain the interpretation. The findings do not establish performance on other platforms.

## Correctness and implementation security

The study keeps three evidence categories distinct:

- Functional compatibility: deterministic transcripts, cross-implementation checks, round trips and sampled invalid-input behaviour.
- Arithmetic safety: caller bounds, representation, intermediate widths, narrowing, targeted oracles and exercised UBSan checks.
- Secret-dependent behaviour: generated-code inspection, marked-secret branch/address tests and finite statistical timing screens with positive and negative controls.

Successful correctness tests or ordinary benchmark stability do not prove constant time. Code size and local-stack observations do not measure whole-program peak memory. Physical side channels, faults, complete formal proof and final ML-KEM certification are outside the established result.

## Literature and presentation

The literature record distinguishes verified sources, abstract-only access and unverified full-text claims. References use APA 7 with stable identifiers and locators where verified. Local inspection is not presented as a novel result or attributed to an unread paper.

Figures are generated from retained data with versioned code, exact input/output hashes, clear units and comparator labels. Vector PDF/SVG and high-resolution PNG outputs accompany machine-readable plot data. Captions preserve adverse findings and the limits of each measurement.
