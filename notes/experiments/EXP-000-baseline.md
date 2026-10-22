# EXP-000 Reproducible reference baseline

Lifecycle: running. Metadata and sampled functional validation accepted through ACT-0004. The first committed timing pilot is pending.

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

## Preparation

1. Completed in ACT-0002: I repaired the root ignore rules, supplied the submodule mapping, and committed the script correction and research documentation.
2. Completed in ACT-0003: I implemented the collector, saved EXP-000/RUN-0001 and verified its provenance and overwrite refusal. The raw timing harness was prepared in ACT-0004. The legacy summary script remains unused.
3. Completed in ACT-0004: EXP-000/RUN-0002 passed all three existing functional tests using fresh builds. The saved logs, metadata and executables match the manifest hashes. See [accepted run](../runs/EXP-000-RUN-0002.md).
4. Functional validation is recorded. The raw timing harness is ready; reduction-count instrumentation remains pending and will use separate builds.
5. Record live host/guest conditions and manual controls. The conditions worksheet is not a completed manifest.
6. Record the final timer, warm-up, independent repetitions, input mode, order, exclusion rules and analysis method before primary collection. The initial pilot uses five fresh processes per parameter set, 100 warm-up triplets and 1000 measured triplets per process. I will use its variation to guide later comparison repetitions.
7. Commit source/harness, build with recorded commands, record binary hashes and allocate run IDs.

## Evidence and decision

- Metadata-only snapshot: verified; see [EXP-000/RUN-0001](../runs/EXP-000-RUN-0001.md).
- Support-script tests: 15 passed with dummy processes and mocked workflows.
- New Kyber builds/tests during ACT-0003: not-run.
- Sampled functional archive: accepted, EXP-000/RUN-0002.
- Measured reduction counts: not-run.
- Formal timing dataset: not-run.
- Timing-behaviour assessment: not-run.
- Functional baseline acceptance: accepted within the existing tests' scope.
- Performance baseline acceptance: pending.

The earlier review reported passing existing correctness binaries without a persistent full run archive. That historical context is recorded in ACT-0001 and does not substitute for this baseline.

## Next recorded run

I will use EXP-000/RUN-0003 for the first committed raw timing pilot after reviewing and committing the harness. See the [timing protocol](../raw_timing.md). The expected output is 15 raw CSV files containing 45000 measured operation rows and a generated summary with 45 per-process/operation rows.

I expect matching shared secrets and positive durations for every measured exchange. I make no speedup prediction because no arithmetic has changed. The pilot will establish representative durations and process-to-process variation for the specified environment and input mode.

I retain all observations without exclusions. The results measure the existing deterministic key-generation and encapsulation APIs plus decapsulation; operating-system random-number generation is outside the measurement. These are nanosecond durations, not CPU-cycle counts. Formal arithmetic-safety and timing-leakage claims require separate checks.
