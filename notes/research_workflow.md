# Research methods and record conventions

The research record explains what each experiment asked, what I changed, how I checked it and what the measurements showed. Each conclusion stays within what those checks can support. The experiment register is the index, while run manifests, raw outputs and review records provide the detailed evidence.

## Identifiers and evidence

| Identifier | Meaning |
|---|---|
| ACT | Research activity or review checkpoint |
| EXP | Experiment question and protocol |
| RUN | One execution attempt within an experiment |
| Variant | Source treatment used in a comparison |
| Block | Matched executions used to calculate a paired effect |

I do not reuse identifiers. If a run fails or is interrupted, I keep its files and give any retry a new run ID. A metadata-only record describes the setup. It does not mean a benchmark ran. Experiment states distinguish proposed, planned, running, analysed and closed work; outcomes distinguish supported, not-supported, inconclusive and execution errors. Unperformed checks are recorded as not-run.

Source commits identify the code and support present before execution; results commits archive the later observations. Full commit IDs, tool/source/executable hashes, commands, exit codes and raw outputs make that distinction reproducible. Calendar dates, clock times and timezone fields are omitted from project narratives; publication years, software versions and measured durations retain their meaning.

Arithmetic changes and Git operations are performed manually. Research documentation uses direct first-person or neutral technical prose without attributing actions beyond the evidence. Corrections use new commits and preserve cited history.

## Experimental sequence

1. Specify the question, isolated change, predecessor, expected count effect, arithmetic assumptions, validation gates and measurement rules before collection.
2. Check caller ranges, Montgomery scale, intermediate widths, narrowing and downstream consumers, including invalid inputs.
3. Commit source and support before a formal run. The collector requires a clean Git-visible tree outside results/ and refuses an existing run directory.
4. Build explicitly, record tool and executable identities, collect raw observations and retain partial output after failure.
5. Analyse matched observations with the declared estimator. Preserve negative, mixed and inconclusive results.
6. Record the outcome, limitations and retention decision separately from the completion status of the runner.

A clean working tree and a binary hash are not enough to show how an executable was built. The manifests also save the commands, inputs and outputs that connect each executable to its source. Development checks using uncommitted support are labelled separately and do not become formal performance results.

## Preservation and reproduction

Raw results, metadata snapshots, manifests, previous audit records and published figure/data artifacts remain unchanged. Derived corrections are recorded separately. Rebuildable binaries are ignored by Git; their commands and hashes remain in the manifests. Retained-data analysis can be repeated without recollecting measurements, while full binary-identity audits require the recorded executables or a separately documented rebuild.

Protocol versions are part of the recorded support identity. EXP-008/009/010 retain the collection-time Markdown bytes; EXP-010's JSON protocol also pins the saved random-seed plan. EXP-007's current protocol includes a later ACT-0017 result section, so its collection-time identity must be recovered from the source revision recorded in its manifest. Some older support scripts likewise have later revisions. A file at the same path may have changed since collection. Always check which historical version the record refers to.

All experiment protocol files are preserved during editorial cleanup. Accepted result records state the completed findings separately. Use the [reproduction guide](git_reproduce.md) for retained-data analysis and the historical timing guides for their experiment-specific collection gates; editorial revisions do not change what was planned before measurement.

## Measurement and interpretation

I measure performance with ordinary reference-C builds without counters or sanitizers, deterministic public test inputs and CLOCK_MONOTONIC_RAW durations in nanoseconds. Fixture generation, warm-up, output comparison and CSV formatting are outside each measured operation. Operating-system randomness is excluded by the deterministic API mode. Reduction counts use separate instrumented builds and measure function calls, not instructions or runtime.

The early paired studies use five fresh process pairs per parameter. The closing study uses three separately launched sessions with 12 balanced three-variant blocks per parameter. Process medians produce paired time reductions; session medians and the median of three session estimates produce the closing summary. The separate EXP-010 follow-up uses 60 saved random seeds over five sessions and reports the median of five session estimates. Its box plots show pooled block quartiles and full ranges, with the session-based summary distinguished. The two studies are not pooled. Inner timing rows are not independent experimental repetitions. Pair/session ranges are descriptive, not confidence intervals, and separate-run incremental percentages cannot be added or multiplied into a cumulative gain.

Pinning a process to a logical CPU inside WSL does not establish which physical core runs it. Host/power/background conditions that were not recorded remain unknown. Compiler, source, tool, timer and observed-affinity identities constrain the interpretation. The findings do not establish performance on other platforms.

## Correctness and implementation security

The study keeps three evidence categories distinct:

- Functional compatibility: deterministic transcripts, cross-implementation checks, round trips and sampled invalid-input behaviour.
- Arithmetic safety: caller bounds, representation, intermediate widths, narrowing, targeted oracles and exercised UBSan checks.
- Secret-dependent behaviour: generated-code inspection, marked-secret branch/address tests and finite statistical timing screens with positive and negative controls.

Successful correctness tests or ordinary benchmark stability do not prove constant time. Code size and local-stack observations do not measure whole-program peak memory. Physical side channels, faults, complete formal proof and final ML-KEM certification are outside the established result.

## Terms used in these notes

- **Fixture:** a prepared test input. Deterministic fixtures can be recreated from the recorded seed and generation rule.
- **Instrumented build:** a build with extra checks or counters. I use ordinary builds for performance so those additions do not affect the timings.
- **Manifest:** the run record that lists commands, files, hashes, outcomes and checks.
- **Provenance:** the information connecting a result to its source code, build, tools and inputs. A hash helps check whether file contents have changed.
- **Caller contract:** the input ranges and representation that a function expects, together with the output guarantees that later code relies on.
- **Narrowing:** converting a value to a smaller integer type. The range argument must show that the value fits where the method requires it to.
- **Oracle:** a test calculation used to check the implementation's output. Each experiment states which details its oracle shares with the implementation.
- **Paired effect:** the relative difference between matched control and candidate process summaries. Its exact formula and aggregation are recorded for each study.
- **Quiet secret-flow check:** no marked-secret branch/address dependency was reported on the paths that ran. It does not mean that every possible leak has been ruled out.
- **Normalised assembly:** generated instructions compared after accounting for specified relocation or symbol differences. Each review records what the comparison preserves.

## Literature and presentation

The literature record distinguishes verified sources, abstract-only access and unverified full-text claims. References use APA 7 with stable identifiers and locators where verified. Local inspection is not presented as a novel result or attributed to an unread paper.

Figures are generated from retained data with versioned code, exact input/output hashes, clear units and comparator labels. Vector PDF/SVG and high-resolution PNG outputs accompany machine-readable plot data. Captions preserve adverse findings and the limits of each measurement.
