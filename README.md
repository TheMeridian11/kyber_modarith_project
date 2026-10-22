# Kyber Modular Arithmetic Optimisation

This honours project evaluates whether reduction scheduling and wider intermediate arithmetic improve a pinned Kyber reference C implementation while preserving compatibility and satisfying documented arithmetic and implementation-safety checks. It compares key generation, encapsulation and decapsulation for Kyber512, Kyber768 and Kyber1024.

The source is [pq-crystals/kyber](https://github.com/pq-crystals/kyber), pinned to commit 3edd5af5991927164edd4aacebfcbee00b8064e7. Relevance to ML-KEM does not establish conformance to final FIPS 203. Claims will identify the implementation actually tested. Improvements over reference C do not establish improvements over contemporary optimised implementations.

## Research records

- [Research workflow and collaboration agreement](notes/research_workflow.md)
- [Cumulative activity log](notes/project_log.md)
- [Master experiment register](notes/experiment_register.md)
- [Baseline experiment plan](notes/experiments/EXP-000-baseline.md)
- [Experiment record template](notes/templates/experiment.md)
- [Run record template](notes/templates/run_record.md)
- [Literature and idea provenance](notes/literature.md)
- [Reduction map](notes/reduction_map.md)
- [Original benchmark conditions worksheet](notes/benchmark_conditions.md)

These records distinguish planned changes, observed changes, executed checks, measured results and interpretations. Failed and inconclusive experiments are retained. The repository preserves the evidence supporting the thesis; the thesis will explain and evaluate that evidence.

## Repository structure

- external/kyber-official/: pinned upstream checkout; preserve its source.
- implementation/kyber-baseline-ref/: reference source used for the baseline.
- implementation/kyber-optimised-ref/: experimental source; no arithmetic modifications recorded yet.
- scripts/: automation written and applied by the researcher.
- results/: raw outputs, per-run provenance and derived results.
- analysis/: reproducible analysis and chart-generation code.
- notes/: research plans, logs, literature and evidence records.

## Current state as of 22 October 2026

Research record-keeping has been established. Source preparation, a reproducible benchmark harness and a recorded baseline still require completion. The baseline script's directory correction is present but uncommitted. It produces summary text rather than the planned complete raw-measurement dataset. No formal benchmark dataset has been recorded.

The earlier review reported passing existing correctness binaries for all three parameter sets. Those observations are historical checks, not a newly reproduced baseline or a complete archived test run. See the activity log for evidence limitations and outstanding setup work.

The researcher applies all code, script, build and Git-configuration changes. The assistant maintains research documentation and summaries, supplies proposed changes in chat and reviews evidence without changing implementation files.
