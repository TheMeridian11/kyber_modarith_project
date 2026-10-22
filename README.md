# Kyber Modular Arithmetic Optimisation

In this honours project, I evaluate whether reduction scheduling and wider intermediate arithmetic improve a pinned Kyber reference C implementation while preserving compatibility and satisfying documented arithmetic and implementation-safety checks. I compare key generation, encapsulation and decapsulation for Kyber512, Kyber768 and Kyber1024.

The source is [pq-crystals/kyber](https://github.com/pq-crystals/kyber), pinned to commit 3edd5af5991927164edd4aacebfcbee00b8064e7. Relevance to ML-KEM does not establish conformance to final FIPS 203. Claims will identify the implementation actually tested. Improvements over reference C do not establish improvements over contemporary optimised implementations.

## Research records

- [Research workflow](notes/research_workflow.md)
- [Cumulative activity log](notes/project_log.md)
- [Master experiment register](notes/experiment_register.md)
- [Baseline experiment plan](notes/experiments/EXP-000-baseline.md)
- [Experiment record template](notes/templates/experiment.md)
- [Run record template](notes/templates/run_record.md)
- [Literature and idea provenance](notes/literature.md)
- [Reduction map](notes/reduction_map.md)
- [Benchmark conditions worksheet](notes/benchmark_conditions.md)

These records distinguish planned changes, observed changes, executed checks, measured results and interpretations. Failed and inconclusive experiments are retained. The repository preserves the evidence supporting the thesis; the thesis will explain and evaluate that evidence.

## Repository structure

- external/kyber-official/: pinned upstream checkout; preserve its source.
- implementation/kyber-baseline-ref/: reference source used for the baseline.
- implementation/kyber-optimised-ref/: experimental source; no arithmetic modifications recorded yet.
- scripts/: environment collection and benchmark automation.
- results/: raw outputs, per-run provenance and derived results.
- analysis/: reproducible analysis and chart-generation code.
- notes/: research plans, logs, literature and evidence records.

## Current state

I have committed the setup at c584c16d7b8a8e8de5e071a4edd5bc1450f92592 on branch reduction-counters. Repository inspection confirms the upstream submodule mapping, corrected ignore rules and a clean working tree before the ACT-0002 documentation updates. All 36 reference source/build files in each local implementation copy match the pinned upstream reference.

I am preparing the automatic metadata collector next. The proposed collector has only been syntax-checked in memory; its implementation and runtime checks are pending. It will record a metadata-only snapshot and will not build or run Kyber. The existing scripts/run_baseline.sh still uses calendar-based output names and summary measurements; I will leave it unused until the sequential-ID launcher and raw-data harness replace that workflow.

I have no formal benchmark dataset. The earlier review reported passing existing correctness binaries for all three parameter sets, but a complete raw test archive was not retained. Those historical observations do not establish the accepted baseline.

I apply and review code changes before committing the exact source used for a run. I preserve raw outputs, evidence limitations and failed experiments alongside successful results. The activity log distinguishes proposed instructions from confirmed changes and executed checks.
