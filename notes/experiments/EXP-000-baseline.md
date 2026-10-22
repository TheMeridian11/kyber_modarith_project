# EXP-000 Reproducible reference baseline

Lifecycle: planned. Setup verified in ACT-0002. No formal runs recorded.

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
2. Pending: I will implement and smoke-test the proposed metadata collector, then develop the raw-data harness. A metadata-only snapshot is not a baseline performance run. I will leave the legacy summary script unused because it still uses calendar-based output names.
3. Establish reliable rebuild behaviour for header and flag changes, preserving attribution for upstream changes.
4. Implement validation and separate counting/performance modes.
5. Record live host/guest conditions and manual controls. The conditions worksheet is not a completed manifest.
6. Record the final timer, warm-up, independent repetitions, input mode, order, exclusion rules and analysis method before primary collection. The suggested 30 by 1000 schedule is a pilot proposal, not executed or finalised.
7. Commit source/harness, build with recorded commands, record binary hashes and allocate run IDs.

## Evidence and decision

- Current-session builds/tests: not-run.
- Formal correctness archive: pending.
- Measured reduction counts: not-run.
- Formal timing dataset: not-run.
- Timing-behaviour assessment: not-run.
- Baseline acceptance: pending.

The earlier review reported passing existing correctness binaries without a persistent full run archive. That historical context is recorded in ACT-0001 and does not substitute for this baseline.
