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
- [EXP-003 inverse-NTT plan, bounds and applied replacement](notes/experiments/EXP-003-staged-invntt.md)
- [EXP-003 accepted validation and security/assembly findings](notes/runs/EXP-003-RUN-0001.md)
- [EXP-002 versus EXP-003 timing protocol](notes/invntt_timing.md)
- [EXP-003 measured timings and security interpretation](notes/runs/EXP-003-RUN-0002.md)
- [EXP-005 error-vector plan, bounds and exact manual edit](notes/experiments/EXP-005-error-ntt.md)
- [Experiment record template](notes/templates/experiment.md)
- [Run record template](notes/templates/run_record.md)
- [Literature and idea provenance](notes/literature.md)
- [Reduction map](notes/reduction_map.md)
- [Benchmark conditions worksheet](notes/benchmark_conditions.md)

These records distinguish planned changes, observed changes, executed checks, measured results and interpretations. Failed and inconclusive experiments are retained. The repository preserves the evidence supporting the thesis; the thesis will explain and evaluate that evidence.

## Repository structure

- external/kyber-official/: pinned upstream checkout; preserve its source.
- implementation/kyber-baseline-ref/: reference source used for the baseline.
- implementation/kyber-optimised-ref/: experimental source containing the manually applied EXP-001 basemul, EXP-002 vector-dot-product and EXP-003 inverse-NTT changes.
- scripts/: environment collection and benchmark automation.
- benchmarks/: measurement harnesses that leave cryptographic arithmetic unchanged.
- results/: raw outputs, per-run provenance and derived results.
- analysis/: reproducible analysis and chart-generation code.
- notes/: research plans, logs, literature and evidence records.

## Current state

I have completed baseline preparation and the first three optimisations' initial correctness/timing evaluations. EXP-001 fuses base-multiplication products, EXP-002 extends fusion across vector components and EXP-003 reduces inverse-NTT Barrett frequency. The latest matched comparison gives these median time reductions for EXP-003 relative to fresh EXP-002:

| Parameter | Keygen | Encap | Decap |
|---|---:|---:|---:|
| Kyber512 | -0.31% | +4.69% | +4.64% |
| Kyber768 | -0.51% | +4.98% | +4.90% |
| Kyber1024 | +0.70% | +4.30% | +4.63% |

Negative values mean slower. All 30 encap/decap pairs favour EXP-003, including both order groups. Keygen does not call invntt: its small movements are retained, including the five-pair Kyber768 regression, without assigning a proven cause. I reproduced all 90000 raw durations into the saved 90 summaries, 45 pairs and nine aggregates, and verified all eighteen timing-build assembly matches. I keep EXP-003 as the next research reference for its targeted benefit with these tradeoffs.

The [timing review](notes/runs/EXP-003-RUN-0002.md) records absolute durations, ranges, order checks, unchanged keygen entry-point instructions, provenance and security limitations. The [EXP-001](notes/runs/EXP-001-RUN-0002.md) and [EXP-002](notes/runs/EXP-002-RUN-0002.md) results remain preserved. These are single-session incremental effects, not cumulative gains over the original reference or cross-machine guarantees.

| Stage | Status | Question answered |
|---|---|---|
| EXP-000: baseline preparation | Complete | What does the unchanged reference do? |
| EXP-001: base multiplication | Initial validation/timings accepted | Does fusion inside each coefficient pair help? |
| EXP-002: vector-wide fusion | Initial validation/timings accepted | Does fusion across vector components improve further? |
| EXP-003: inverse-NTT schedule | Initial validation/timings accepted | Does reducing Barrett frequency improve further within the required bounds? |
| EXP-004: optional interaction study | Deferred | Is a distinct combination/interaction question worth testing later? |
| EXP-005: error-vector NTT reduction | Plan/support ready; manual edit pending | Can keygen defer this one reduction until its existing final reduction? |

EXP-003 reduces Barrett calls from 896 to 128 per inverse transform while retaining Montgomery counts and the centred-input contract. Its inverse body grows 347 -> 458 bytes and local stack use falls 104 -> 72 bytes including saved registers, excluding return address/callees. Neither inverse version has a local canary. The earlier EXP-002 dot-product canary tradeoff remains inherited. Scoped public-control-flow assembly and passing sampled correctness/UBSan checks do not establish whole-program constant-time security or production approval.

Next I manually apply the [EXP-005 call-site edit](notes/experiments/EXP-005-error-ntt.md) in indcpa_keypair_derand only: retain the skpv transform/reduction and transform each error polynomial e directly with ntt. The existing final public-key reduction stays in place. Conservative raw-error/addition bounds are 23299/26627, and predicted keygen Barrett savings are 512/768/1024 calls; encap/decap arithmetic counts remain unchanged. All reductions establishing EXP-003's inverse-input bounds are preserved. EXP-005 is not yet applied or validated; its first run collects correctness/counts/assembly, with performance considered only after acceptance.

The latest accepted timing source is cf8ae0dd700bb41628c158016a7c15926a0b790f with results 23b4736206a8f79d13fb4898d474eb327e1dab3c. EXP-003 validation used source 9ec22141e6acc98812438544be0bec5b35d00b5c with results 705f21f7f07dcd4162052aacda3adbcc54c4051a. Statistical leakage resistance and final ML-KEM conformance remain unestablished. A later direct comparison with the original reference is needed for a total selected-variant speed claim.

I manually apply arithmetic changes and perform Git operations, reviewing support code before committing it. I retain failed and inconclusive outcomes, use distinct experiment/run IDs, and keep validation evidence separate from performance results. The legacy summary script remains unused.
