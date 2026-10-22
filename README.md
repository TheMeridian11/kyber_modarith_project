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
- [EXP-001 measured timing results](notes/runs/EXP-001-RUN-0002.md)
- [EXP-002 plan, bounds and manual replacement](notes/experiments/EXP-002-wide-dot.md)
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

I have completed initial baseline preparation and the first optimisation's correctness and timing evaluation. EXP-001 fuses products before reduction inside basemul. It preserved the tested outputs and produced the following median paired improvements in the first matched timing run:

| Parameter set | Keygen | Encap | Decap |
|---|---:|---:|---:|
| Kyber512 | 4.12% | 5.87% | 6.01% |
| Kyber768 | 1.68% | 0.87% (inconclusive) | 0.86% (inconclusive) |
| Kyber1024 | 7.43% | 8.55% | 8.43% |

All five pairs favoured EXP-001 for Kyber512, Kyber1024 and Kyber768 keygen. Kyber768 encapsulation and decapsulation each included one slower pair; I do not claim a reliable sub-one-percent gain for them. I retain EXP-001 as a validated research reference. The [timing review](notes/runs/EXP-001-RUN-0002.md) records the verified 90000 observations, pair ranges, order checks and limits of this single WSL run.

| Stage | Status | Question answered |
|---|---|---|
| EXP-000: baseline preparation | Complete | What does the unchanged reference do? |
| EXP-001/RUN-0001: validation and assembly | Accepted | Does the first change preserve tested behaviour under the reviewed bounds? |
| EXP-001/RUN-0002: matched timings | Accepted and analysed | Did the first change make complete KEM operations faster here? |
| EXP-002: vector-wide fusion | Plan and validation support ready; manual change pending | Can delaying reductions across all K vector components improve further? |
| EXP-002/RUN-0001: next validation run | Pending manual application and commit | Does the larger accumulation remain correct and safe within the new bounds? |

EXP-002 replaces polyvec_basemul_acc_montgomery in the candidate polyvec.c and retains the accepted ntt.c. I apply the [exact replacement](notes/experiments/EXP-002-wide-dot.md) manually. Its next run checks vector arithmetic, KEM compatibility, UBSan and predicted counts, and retains assembly. That run will not measure speed. A later fresh EXP-001/EXP-002 timing comparison follows accepted validation and assembly review.

The first timing comparison used source d407b5134f14a96a4572b3af1132a8f715e0a28d; results are in 337e4ba6ff1fc8783c47ea7c34dc2ee52c1e8712. Source, binaries and measurements are preserved. Complete constant-time guarantees, statistical leakage resistance and final ML-KEM conformance remain unestablished; faster execution is not a security certificate.

I manually apply arithmetic changes and perform Git operations, reviewing support code before committing it. I retain failed and inconclusive outcomes, use distinct experiment/run IDs, and keep validation evidence separate from performance results. The legacy summary script remains unused.
