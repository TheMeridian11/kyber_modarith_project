# Kyber Modular Arithmetic Optimisation

In this honours project, I evaluate whether reduction scheduling and wider intermediate arithmetic improve a pinned Kyber reference C implementation while preserving compatibility and satisfying documented arithmetic and implementation-safety checks. I compare key generation, encapsulation and decapsulation for Kyber512, Kyber768 and Kyber1024.

The source is [pq-crystals/kyber](https://github.com/pq-crystals/kyber), pinned to commit 3edd5af5991927164edd4aacebfcbee00b8064e7. Relevance to ML-KEM does not establish conformance to final FIPS 203. Claims will identify the implementation actually tested. Improvements over reference C do not establish improvements over contemporary optimised implementations.

## Research records

- [Research workflow](notes/research_workflow.md)
- [Cumulative activity log](notes/project_log.md)
- [Master experiment register](notes/experiment_register.md)
- [Baseline experiment plan](notes/experiments/EXP-000-baseline.md)
- [Verified metadata checkpoint](notes/runs/EXP-000-RUN-0001.md)
- [Functional validation runner](notes/validation_runner.md)
- [Accepted functional run](notes/runs/EXP-000-RUN-0002.md)
- [Raw timing protocol](notes/raw_timing.md)
- [Accepted timing pilot](notes/runs/EXP-000-RUN-0003.md)
- [Reduction counting protocol](notes/reduction_counts.md)
- [Accepted reduction counts](notes/runs/EXP-000-RUN-0004.md)
- [EXP-001 plan and security assessment](notes/experiments/EXP-001-fused-basemul.md)
- [Accepted candidate validation and assembly review](notes/runs/EXP-001-RUN-0001.md)
- [Matched baseline/candidate timing protocol](notes/paired_timing.md)
- [Experiment record template](notes/templates/experiment.md)
- [Run record template](notes/templates/run_record.md)
- [Literature and idea provenance](notes/literature.md)
- [Reduction map](notes/reduction_map.md)
- [Benchmark conditions worksheet](notes/benchmark_conditions.md)

These records distinguish planned changes, observed changes, executed checks, measured results and interpretations. Failed and inconclusive experiments are retained. The repository preserves the evidence supporting the thesis; the thesis will explain and evaluate that evidence.

## Repository structure

- external/kyber-official/: pinned upstream checkout; preserve its source.
- implementation/kyber-baseline-ref/: reference source used for the baseline.
- implementation/kyber-optimised-ref/: experimental source containing the manually applied EXP-001 basemul change.
- scripts/: environment collection and benchmark automation.
- benchmarks/: measurement harnesses that leave cryptographic arithmetic unchanged.
- results/: raw outputs, per-run provenance and derived results.
- analysis/: reproducible analysis and chart-generation code.
- notes/: research plans, logs, literature and evidence records.

## Current state

Initial baseline preparation is complete. I have implemented the first optimisation, fused base multiplication, and accepted its correctness, exercised-path UBSan, reduction-count and scoped assembly evidence. I am ready to measure its effect on complete KEM operations with a fresh baseline alongside it.

| Step | Status | What it establishes |
|---|---|---|
| EXP-000/RUN-0001: metadata | Accepted | Source and environment identity |
| EXP-000/RUN-0002: functional tests | Accepted | Sampled unchanged-Kyber correctness |
| EXP-000/RUN-0003: timing pilot | Accepted | Baseline duration and observed variation |
| EXP-000/RUN-0004: reduction counts | Accepted | Baseline calls per operation |
| EXP-001/RUN-0001: candidate validation and assembly | Accepted for timing comparison | Sampled compatibility, arithmetic checks and reviewed code |
| EXP-001/RUN-0002: matched timings | Support ready; formal execution pending | Whether fewer reductions improve measured performance |

EXP-001/RUN-0001 used source commit 8345f6a0fb273917ed4499356f0966d1c5dc7fc2; results commit 00398d18dddbccb99854bb6519fc896a23d90f22 directly follows it. All 42 steps passed, the twelve deterministic transcripts agree within each parameter set, and all predicted candidate counts matched. Normal-build basemul contains three Montgomery calls instead of five, with unchanged Barrett counts and no new branch or data-dependent index in the reviewed bodies.

I have not measured an optimisation speedup yet. The next run uses five adjacent baseline/candidate pairs per parameter set, alternating their order, with the existing timing harness. It preserves all 90000 operation durations and reports effects from matched process medians. The prior pilot is context, not the primary comparison control.

The [candidate review](notes/runs/EXP-001-RUN-0001.md) records the bounds, sampled evidence and generated-code findings. Complete constant-time guarantees and statistical leakage assessment remain unestablished or unperformed. Timing results will not be used as a blanket security claim or as evidence of final ML-KEM conformance.

I manually apply arithmetic optimisation changes and review supporting automation before committing the exact source used for a run. I preserve raw outputs, evidence limitations and failed experiments alongside successful results. The legacy summary script remains unused.
