# Research workflow

Agreed on 22 October 2026, Australia/Sydney. This document defines how work and evidence are recorded.

## Collaboration agreement

- The researcher applies every implementation, script, analysis-code, build-file and Git-configuration change. The assistant supplies exact paths, snippets or complete replacements, commands, expected outcomes and verification instructions in chat.
- The assistant may maintain research documentation, experiment records, literature records and result summaries, and inspect files and outputs. It does not change executable code/configuration, commit, tag, push, build or run benchmarks unless separately requested.
- The researcher normally runs the supplied commands and shares outputs or repository locations. The assistant checks available evidence and records its interpretation.
- Each substantive final response ends with an activity-log entry covering completed work, pending work, results, interpretation and next actions. The same entry is saved in project_log.md. Corrections are appended explicitly.
- Chat supplies instructions and discussion; the repository is the durable research record. Distinguish directly inspected evidence, researcher-reported evidence and historical observations.
- Preserve user changes. Proposed changes and commands are not marked implemented or executed until confirmed or inspected.

## Identifiers

| Identifier | Meaning | Example |
|---|---|---|
| Activity | One session of decisions, changes or review | ACT-0001 |
| Experiment | One research question or comparison protocol | EXP-001 |
| Variant | A specific implementation treatment | baseline or fused-basemul |
| Run | One execution attempt within an experiment | EXP-001/RUN-0001 |
| Comparison block | Related baseline and candidate executions | EXP-001/BLOCK-0001 |

Activity and experiment numbers increase and are never reused. Run numbers are unique within an experiment; the full experiment/run pair is globally unique. Retries receive new run IDs, including after failure. Record variant, parameter set and build mode explicitly.

Lifecycle: proposed, planned, running, analysed, closed. Record the outcome separately: supported, not-supported, inconclusive, invalid-implementation, execution-error. Record the retention decision separately: keep, reject, revise, defer. Unperformed checks are not-run, never pass.

## Evidence sequence

1. Before collecting comparison data, specify the hypothesis, isolated change, baseline, predictions, arithmetic assumptions, validation gates, measurement protocol and decision criteria. Label predictions as source-derived or literature-derived.
2. The researcher implements the change and reviews the diff. Complete required correctness and arithmetic checks before formal performance collection.
3. Commit the source and harness before formal execution. Record the full source commit, upstream commit, submodule state, compiler command, build mode and executable SHA-256. Preserve build output. Rebuild explicitly when headers or flags change.
4. Allocate a run ID and capture metadata before launch. The future launcher should create a manifest before execution and finalise its timestamps, exit codes and completion status. Preserve partial output after failure.
5. Keep raw observations, stdout/stderr and exit codes. Analysis writes derived files separately. Record comparison blocks and order, and link any baseline run reused in a comparison.
6. Record outcomes and limitations, update the register and activity log, and commit results and records after the run.
7. The results commit differs from the source commit that produced the measurements. Do not try to embed a results commit's own hash in a file in that same commit. Git history identifies it, or a later index can reference it. Record the analysis-code revision separately.

Formal runs require the tested code, configuration and harness to be committed. Prefer a clean tracked tree at launch. If an exploratory run uses uncommitted work, preserve the exact diff and all relevant untracked sources and label it exploratory. A dirty flag alone cannot reconstruct an experiment.

Do not amend or force-move commits or tags already cited by results. Correct records through new commits. Milestone tags are useful labels, but manifests retain full commit IDs.

## Result preservation

Use a directory such as results/EXP-001/RUN-0001/ containing a manifest.json, a raw/ directory for measurements/build/test output, and a derived/ directory for summaries and generated figures. This is a convention for future runs, not evidence that a run exists.

Counting, correctness, sanitizer and performance runs have distinct build modes and evidence. A failed run keeps its ID and partial files. A retry gets a new ID. Never overwrite raw files to remove an outlier or repair a failure. Record exclusion rules and affected observations in analysis.

Keep complete raw datasets in Git while practical. If size requires an external archive, preserve its stable location, checksum and retrieval procedure in the repository. Never retain only medians or charts. Use a backed-up location or appropriate remote when available; do not assume a remote is configured.

## Conditions and measurement

Implement automatic per-run system metadata collection next. Manually controlled facts remain explicit manual fields; unknown values stay unknown. Capture defined fields rather than dumping all process environment variables.

Record host/guest versions, CPU and visible topology, RAM with guest/physical scope, compiler path/version/flags, timer and units, executable hash, affinity, power/frequency controls where observable, warm-up, iterations, input/RNG mode, fixture identifiers, comparison order and timestamps. Distinguish observed and manually reported fields. WSL guest affinity does not prove physical-core placement.

Instrumentation and sanitizer builds do not supply primary performance measurements. Function-call counts are not processor instruction counts or timing measurements. Keep individual observations and report run-level variation with appropriate uncertainty. Predetermine exclusion and rerun rules. Compare like units, inputs, flags and protocols. Generate charts from retained data using versioned analysis code.

## Correctness and implementation-safety evidence

Record three evidence categories separately:

- Functional compatibility: vectors, deterministic byte comparisons, cross-implementation tests, round trips and invalid-ciphertext behaviour.
- Arithmetic safety: input/output bounds, Montgomery scale, intermediate widths, narrowing, edge cases and relevant sanitizer checks.
- Timing behaviour: source review, generated-code inspection and focused statistical tests with their limits.

Individual checks use not-run/pass/fail/inconclusive and link their evidence. This is an implementation-safety evidence record, not a blanket security-equivalence certificate. Low benchmark variance and passing correctness tests do not prove constant-time behaviour. Combining individually successful variants requires new range and compatibility checks.

## Literature and interpretation

Maintain APA 7 references, stable URLs/DOIs, exact versions and verified page/section locators. Link ideas and claims to experiments. Distinguish abstract access from full-text review, predictions from measurements, and observed failures from proved causes.

Keep slower, failed and inconclusive variants. A failed command is an execution outcome; a correct but slower implementation is a performance finding. Neither should be silently deleted or treated as evidence for a mechanism that was not tested.
