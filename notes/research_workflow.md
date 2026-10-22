# Research workflow

I use this workflow to preserve the connection between research questions, source changes, validation, measurements and conclusions.

## Working method

- I manually apply arithmetic optimisation changes and perform Git operations myself. I review supporting scripts, tests, build automation and research-record changes before committing them.
- I record completed work, pending work, results, interpretation and next actions under sequential activity IDs in project_log.md.
- I distinguish directly inspected repository evidence, supplied execution output and historical observations. A proposed snippet or command is not an implemented change or an executed check.
- I keep the repository as the durable research record. Chat discussion alone does not establish a reproducible result.
- I write project records in first person and keep conclusions tied to the available evidence.
- I identify work through activity IDs, experiment IDs, run IDs and full Git commits. I omit calendar dates, clock times and timezone fields from project work records. Publication years in APA references and software version identifiers retain their meaning. Benchmark durations and cycle/tick counts remain essential measurements.

## Identifiers

| Identifier | Meaning | Example |
|---|---|---|
| Activity | One set of decisions, changes or review | ACT-0001 |
| Experiment | One research question or comparison protocol | EXP-001 |
| Variant | A specific implementation treatment | baseline or fused-basemul |
| Run | One execution attempt or explicitly labelled metadata snapshot | EXP-001/RUN-0001 |
| Comparison block | Related baseline and candidate executions | EXP-001/BLOCK-0001 |

I increase activity and experiment numbers without reusing them. Run numbers are unique within an experiment; the full experiment/run pair is globally unique. A retry after an incomplete attempt receives a new ID. I record the record type, variant, parameter set and build mode where applicable. A metadata-only snapshot is not a benchmark repetition.

Lifecycle: proposed, planned, running, analysed, closed. I record the outcome separately: supported, not-supported, inconclusive, invalid-implementation, execution-error. I record the retention decision separately: keep, reject, revise, defer. Unperformed checks are not-run, never pass.

## Evidence sequence

1. Before collecting comparison data, I specify the hypothesis, isolated change, baseline, predictions, arithmetic assumptions, validation gates, measurement protocol and decision criteria. I label predictions as source-derived or literature-derived.
2. I implement the change and review the diff. I complete required correctness and arithmetic checks before formal performance collection.
3. I commit the source and harness before formal execution. I record the full source commit, upstream commit, submodule state, compiler command, build mode and executable SHA-256, and preserve build output. I rebuild explicitly when headers or flags change.
4. I allocate a run ID and capture metadata before launch. The runners preserve their invocation, execution order, exit codes and completion status. I retain partial output after failure.
5. I keep raw observations, stdout/stderr and exit codes. Analysis writes derived files separately. I record comparison blocks and order, and link any baseline run reused in a comparison.
6. I record outcomes and limitations, update the register and activity log, and commit results and records after the run.
7. The results commit differs from the source commit that produced the measurements. I do not embed a results commit's own hash in a file in that same commit. Git history identifies it, or a later index can reference it. I record the analysis-code revision separately.

Formal runs require the tested code, configuration and harness to be committed. The metadata collector requires a clean Git-visible tree outside results/, including tracked changes and non-ignored untracked files. Existing result records may accumulate without blocking collection. This is a Git cleanliness check, not proof that ignored build files were produced from the recorded source. An executable hash alone does not establish build provenance.

If an exploratory run uses uncommitted work, I preserve the exact diff and relevant untracked sources and label it exploratory through a separately documented procedure. The initial collector deliberately rejects that source state; a dirty flag alone cannot reconstruct an experiment.

I preserve commits and tags already cited by results. Corrections use new commits. Milestone tags are useful labels, but manifests retain full commit IDs. This record-format change does not rewrite existing Git history.

## Result preservation

The collector wrote results/EXP-000/RUN-0001/metadata.json for the verified metadata-only smoke check recorded in ACT-0003. Its execution fields remain not-run and build details remain not-recorded. Its available compiler and environment observations describe the collector process; they do not establish a future benchmark's conditions.

The functional validation runner adds manifest.json and raw/ build/test logs to a newly reserved run directory, and builds executables under build/. The metadata.json remains the immutable pre-execution snapshot; manifest.json records the actual attempt and final status. Rebuildable binaries are kept locally and ignored by Git; their hashes and build commands remain in the manifest. The timing runner also preserves each raw CSV and generates per-process/operation summaries under derived/. Figures remain pending.

I accept functional validation only when the manifest status is completed, the provenance recheck passes, all three upstream functional checks pass and all six build/test steps complete with exit code zero. Failed, interrupted or still-running records are not accepted. Abrupt system termination may prevent finalisation; I preserve that incomplete evidence and retry with a new ID.

Counting, correctness, sanitizer and performance runs have distinct build modes and evidence. I preserve failed runs and partial files under their original IDs. A retry receives a new ID. I never overwrite raw files to remove an outlier or repair a failure; exclusions are recorded in analysis.

I keep complete raw datasets in Git while practical. If size requires an external archive, I retain its stable location, checksum and retrieval procedure. I preserve individual observations rather than only medians or charts.

## Conditions and measurement

I collect defined system fields rather than dumping all environment variables. Manually controlled facts remain explicit manual fields; unknown values stay unknown.

For full benchmark runs, I record host/guest versions, CPU and visible topology, RAM with guest/physical scope, compiler path/version/flags, timer and units, executable hash, affinity, observable power/frequency controls, warm-up, iterations, input/RNG mode, fixture identifiers and comparison order. I distinguish observed and manually reported fields. WSL guest affinity does not prove physical-core placement.

Instrumentation and sanitizer builds do not supply primary performance measurements. Function-call counts are not processor instruction counts or timing measurements. I retain individual observations and report run-level variation with appropriate uncertainty. I predetermine exclusion and rerun rules, compare like units/inputs/flags/protocols, and generate charts from retained data using versioned analysis code.

## Correctness and implementation-safety evidence

I maintain three evidence categories separately:

- Functional compatibility: vectors, deterministic byte comparisons, cross-implementation tests, round trips and invalid-ciphertext behaviour.
- Arithmetic safety: input/output bounds, Montgomery scale, intermediate widths, narrowing, edge cases and relevant sanitizer checks.
- Timing behaviour: source review, generated-code inspection and focused statistical tests with their limits.

Individual checks use not-run/pass/fail/inconclusive and link their evidence. These records support bounded implementation-safety claims. Low benchmark variance and passing correctness tests do not prove constant-time behaviour. Combining individually successful variants requires new range and compatibility checks.

## Literature and interpretation

I maintain APA 7 references, stable URLs/DOIs, exact versions and verified page/section locators. I link ideas and claims to experiments and distinguish abstract access from full-text review, predictions from measurements, and observed failures from proved causes.

I retain slower, failed and inconclusive variants. A failed command is an execution outcome; a correct but slower implementation is a performance finding. Neither establishes an untested mechanism.

## Current timing pilot

I use the [raw timing protocol](raw_timing.md): fixed logical-CPU affinity, reproducible public fixtures, uninstrumented reference builds, nanosecond duration measurements and five fresh processes per parameter set. Warm-up, fixture generation, shared-secret comparison and CSV formatting occur outside each operation's measured interval. The deterministic API mode excludes operating-system random-number generation.

I keep implementation work focused on the next necessary experiment. I reuse the existing run-record machinery and perform checks that protect correctness, measurement validity and retained evidence, without adding unrelated infrastructure.

## Per-optimisation security record

For each candidate I record the potential failure mechanisms, caller ranges, Montgomery representation, intermediate widths, downstream consumers, invalid-input behaviour and any new timing or memory risks before measurement. I distinguish a reviewed argument from executed evidence. I record exact transcript comparisons, sanitizer outcomes, generated-code findings and any leakage-test limitations separately; a successful benchmark or round trip never becomes a blanket security pass.

EXP-001's [assessment](experiments/EXP-001-fused-basemul.md) applies this rule to fused base multiplication, including noncanonical encoded keys and implicit-rejection outputs. Any later change that invalidates its input bounds requires a new assessment.
