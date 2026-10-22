# EXP-000 Reproducible reference baseline

Lifecycle: running. Metadata, sampled functional validation and the first timing pilot are accepted through ACT-0005. The committed reduction-count run is pending.

## Purpose and provenance

I will establish reproducible builds, functional validation, reduction counts and timing baselines for Kyber512, Kyber768 and Kyber1024 key generation, encapsulation and decapsulation. This is a control experiment, not an arithmetic optimisation.

Upstream: pq-crystals/kyber, commit 3edd5af5991927164edd4aacebfcbee00b8064e7.

Verified setup commit: c584c16d7b8a8e8de5e071a4edd5bc1450f92592, branch reduction-counters. I will record the actual source/harness commit separately for each execution; the setup commit is not a benchmark result.

## Expected observations

- Preserve baseline arithmetic and formats.
- Build and execute all correctness tests, retaining output and exit status.
- Add deterministic differential/vector checks as the harness develops. Identify the exact vector source; a generator alone is not an independent known-answer oracle.
- Separate counting and uninstrumented timing builds.
- Estimate environmental variation across baseline sessions before interpreting small effects.
- Make no runtime or speedup prediction during setup.

The earlier source review derived these instrumentation sanity checks:

| Parameter set | Keygen Montgomery / Barrett | Encap Montgomery / Barrett | Decap Montgomery / Barrett |
|---|---|---|---|
| Kyber512 | 6656 / 2048 | 9088 / 4736 | 13312 / 6656 |
| Kyber768 | 11904 / 3072 | 14976 / 6400 | 20736 / 8576 |
| Kyber1024 | 18432 / 4096 | 22144 / 8064 | 29440 / 10496 |

These predict reduction-function invocations per KEM call, not measured instructions or performance. Exclude setup work from per-operation counts. Investigate discrepancies rather than silently changing the prediction. Decapsulation includes re-encryption.

## Progress

1. Source identity and environment: RUN-0001 accepted.
2. Sampled functional baseline: RUN-0002 accepted for all three parameter sets.
3. Timing baseline: RUN-0003 accepted; 45000 raw rows and 45 reproduced summary rows.
4. Reduction counts: separate support implemented and checked in ACT-0005; commit and execute RUN-0004 next.

I retain the unchanged reference as the control. After RUN-0004, no additional general baseline infrastructure is planned before EXP-001. Candidate-specific range proofs, deterministic byte comparisons, arithmetic checks and timing-behaviour review remain necessary parts of the optimisation work.

## Evidence and decision

- Metadata-only snapshot: verified; see [EXP-000/RUN-0001](../runs/EXP-000-RUN-0001.md).
- Support-script tests: 15 passed with dummy processes and mocked workflows.
- New Kyber builds/tests during ACT-0003: not-run.
- Sampled functional archive: accepted, EXP-000/RUN-0002.
- Recorded reduction counts: pending RUN-0004; 18 development observations matched the source predictions.
- Committed timing dataset: RUN-0003 accepted as a pilot; all 45000 rows validated.
- Timing-behaviour assessment: not-run.
- Functional baseline acceptance: accepted within the existing tests' scope.
- Performance baseline acceptance: accepted as a pilot in the recorded environment; no speedup claim.

The earlier review reported passing existing correctness binaries without a persistent full run archive. That historical context is recorded in ACT-0001 and does not substitute for this baseline.

## Accepted timing pilot and next run

I accepted [RUN-0003](../runs/EXP-000-RUN-0003.md). Median-of-process-median durations in microseconds were 18.6885 / 21.2705 / 27.8050 for Kyber512, 32.5920 / 34.7770 / 43.0455 for Kyber768, and 49.5855 / 55.0405 / 64.8405 for Kyber1024, in keygen / encap / decap order. All measured exchanges passed. Process-median ranges were 0.56% to 1.94%; these are descriptive observations, not confidence intervals.

I will use EXP-000/RUN-0004 for [reduction counting](../reduction_counts.md): ten distinct exchanges per parameter set, 90 operation observations and no timing measurements. I expect the source-derived counts above. Short development checks already agreed, but the committed run is still required for the baseline record.

For initial optimisation comparisons, I retain five processes of 1000 exchanges per parameter set and compare fresh baseline and candidate builds in alternating matched blocks. I will add complete comparison blocks if a small effect remains uncertain, preserving all results. Repeated fixture sequences and within-process timing rows are not independent experiments.

I retain all timing observations without exclusions. The pilot measures the existing deterministic key-generation and encapsulation APIs plus decapsulation; operating-system random-number generation is outside the measurement. These are nanosecond durations, not CPU-cycle counts. Arithmetic-safety and timing-leakage claims require their own evidence.
