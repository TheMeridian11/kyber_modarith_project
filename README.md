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
- [EXP-002 plan, bounds and applied replacement](notes/experiments/EXP-002-wide-dot.md)
- [EXP-002 accepted validation and assembly](notes/runs/EXP-002-RUN-0001.md)
- [EXP-001 versus EXP-002 timing protocol](notes/incremental_timing.md)
- [EXP-002 measured timing results](notes/runs/EXP-002-RUN-0002.md)
- [EXP-003 inverse-NTT plan, bounds and manual replacement](notes/experiments/EXP-003-staged-invntt.md)
- [Experiment record template](notes/templates/experiment.md)
- [Run record template](notes/templates/run_record.md)
- [Literature and idea provenance](notes/literature.md)
- [Reduction map](notes/reduction_map.md)
- [Benchmark conditions worksheet](notes/benchmark_conditions.md)

These records distinguish planned changes, observed changes, executed checks, measured results and interpretations. Failed and inconclusive experiments are retained. The repository preserves the evidence supporting the thesis; the thesis will explain and evaluate that evidence.

## Repository structure

- external/kyber-official/: pinned upstream checkout; preserve its source.
- implementation/kyber-baseline-ref/: reference source used for the baseline.
- implementation/kyber-optimised-ref/: experimental source containing the manually applied EXP-001 basemul and EXP-002 vector-dot-product changes.
- scripts/: environment collection and benchmark automation.
- benchmarks/: measurement harnesses that leave cryptographic arithmetic unchanged.
- results/: raw outputs, per-run provenance and derived results.
- analysis/: reproducible analysis and chart-generation code.
- notes/: research plans, logs, literature and evidence records.

## Current state

I have completed baseline preparation and the first two optimisations' initial correctness/timing evaluations. EXP-001 fused products inside basemul; EXP-002 extended fusion across vector components. The latest fresh paired comparison shows the following median time reductions for EXP-002 relative to EXP-001:

| Parameter set | Keygen | Encap | Decap |
|---|---:|---:|---:|
| Kyber512 | 2.02% | 6.07% | 6.00% |
| Kyber768 | 11.83% | 13.46% | 13.55% |
| Kyber1024 | 8.66% | 8.09% | 8.30% |

All 45 paired comparisons favoured EXP-002, including both execution orders. I verified all 90000 raw operation durations and reproduced the complete derived analysis. I retain EXP-002 as the reference for the next incremental experiment. These are single-session improvements over EXP-001; they are not a total gain over the original baseline or a cross-machine guarantee. The [timing review](notes/runs/EXP-002-RUN-0002.md) records absolute durations, pair ranges, order checks, provenance and limitations. The [earlier EXP-001 findings](notes/runs/EXP-001-RUN-0002.md) remain preserved separately.

| Stage | Status | Question answered |
|---|---|---|
| EXP-000: baseline preparation | Complete | What does the unchanged reference do? |
| EXP-001: base multiplication | Initial validation and timings accepted | Does fusion inside each coefficient pair help? |
| EXP-002: vector-wide fusion | Initial validation and timings accepted | Does fusion across vector components improve further? |
| EXP-003/RUN-0001: inverse-NTT schedule | Plan/support ready; manual arithmetic edit pending | Can I reduce less often while preserving bounds and outputs? |
| EXP-003 timings | Later, after candidate validation and assembly | Does that additional change improve on EXP-002? |

EXP-002 retains its bounded correctness/security assessment, including smaller local stack use, a larger dot-product body and absence of its previous local stack-canary check under the same flags. The performance improvement does not remove that documented hardening tradeoff or establish constant-time security.

Next I manually apply the [EXP-003 replacement](notes/experiments/EXP-003-staged-invntt.md) to invntt only. It keeps Barrett sum reductions at stage length 16, predicting 896 to 128 calls per inverse transform while retaining centred input reductions and all Montgomery operations. Key generation has no predicted arithmetic benefit. The first run checks the new candidate; performance comes after acceptance. EXP-004 is optional if a distinct interaction/combination question later warrants it.

The latest timing source is a32a81d12225e00a8b3e0baeb32734f44cf78ab3 and its results commit is 5a09a01496fae8dd4b908934c2e5524f5d3ecc9f. Complete constant-time guarantees, statistical leakage resistance and final ML-KEM conformance remain unestablished. A later direct comparison with the original reference is needed for a total final-variant speed claim.

I manually apply arithmetic changes and perform Git operations, reviewing support code before committing it. I retain failed and inconclusive outcomes, use distinct experiment/run IDs, and keep validation evidence separate from performance results. The legacy summary script remains unused.
