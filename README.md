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
- [EXP-005 error-vector plan, bounds and applied edit](notes/experiments/EXP-005-error-ntt.md)
- [EXP-005 accepted correctness and security/assembly review](notes/runs/EXP-005-RUN-0001.md)
- [EXP-003 versus EXP-005 timing protocol](notes/error_ntt_timing.md)
- [EXP-005 measured timings and security interpretation](notes/runs/EXP-005-RUN-0002.md)
- [EXP-006 plan, bounds and applied changes](notes/experiments/EXP-006-keygen-dot.md)
- [EXP-006 accepted correctness and security/assembly review](notes/runs/EXP-006-RUN-0001.md)
- [EXP-005 versus EXP-006 timing protocol](notes/keygen_dot_timing.md)
- [Required implementation-security assessment](notes/implementation_security.md)
- [Practical completion checklist](notes/practical_completion.md)
- [Experiment record template](notes/templates/experiment.md)
- [Run record template](notes/templates/run_record.md)
- [Literature and idea provenance](notes/literature.md)
- [Reduction map](notes/reduction_map.md)
- [Benchmark conditions worksheet](notes/benchmark_conditions.md)

These records distinguish planned changes, observed changes, executed checks, measured results and interpretations. Failed and inconclusive experiments are retained. The repository preserves the evidence supporting the thesis; the thesis will explain and evaluate that evidence.

## Repository structure

- external/kyber-official/: pinned upstream checkout; preserve its source.
- implementation/kyber-baseline-ref/: reference source used for the baseline.
- implementation/kyber-optimised-ref/: experimental source containing the manually applied EXP-001 basemul, EXP-002 vector-dot-product, EXP-003 inverse-NTT, EXP-005 keygen error-vector and EXP-006 keygen dot-product changes.
- scripts/: environment collection and benchmark automation.
- benchmarks/: measurement harnesses that leave cryptographic arithmetic unchanged.
- results/: raw outputs, per-run provenance and derived results.
- analysis/: reproducible analysis and chart-generation code.
- notes/: research plans, logs, literature and evidence records.

## Current state

I have completed baseline preparation and four optimisations' initial correctness/timing evaluations: EXP-001, EXP-002, EXP-003 and EXP-005. The latest matched comparison gives these median paired time reductions for EXP-005 relative to fresh EXP-003:

| Parameter | Keygen | Encap | Decap |
|---|---:|---:|---:|
| Kyber512 | +5.18% | +0.78% | +0.54% |
| Kyber768 | +0.48% | +0.89% | +0.42% |
| Kyber1024 | +1.36% | -0.12% | -0.50% |

Positive means faster; negative means slower. All fifteen keygen pairs favour EXP-005. Kyber768's small gain needs confirmation, particularly because unchanged operations also move. Kyber1024 encap is mixed and decap is slower in four of five pairs. I retain EXP-005 as the next research reference with these tradeoffs; final selection remains subject to repeat-session and security evaluation.

The [timing review](notes/runs/EXP-005-RUN-0002.md) records absolute durations, all pair ranges, both order groups, provenance and limitations. I reproduced all 90000 raw durations into the saved ninety summaries, 45 pairs and nine aggregates. All 24 timing-build keygen/NTT/reducer bodies match accepted validation. Additional encryption/decryption bodies match after normalisation, while IND-CPA entry addresses move by 16/32/32 bytes. This demonstrates layout changes but does not establish their timing contribution. I do not credit encap/decap movements to a keygen-only reduction change.

The [EXP-001](notes/runs/EXP-001-RUN-0002.md), [EXP-002](notes/runs/EXP-002-RUN-0002.md) and [EXP-003](notes/runs/EXP-003-RUN-0002.md) results remain preserved. These are single-session incremental effects, not cumulative gains over the original reference or cross-machine guarantees. I do not add or multiply percentages from separate runs.

| Stage | Status | Question answered |
|---|---|---|
| EXP-000: baseline preparation | Complete | What does the unchanged reference do? |
| EXP-001: base multiplication | Initial validation/timings accepted | Does fusion inside each coefficient pair help? |
| EXP-002: vector-wide fusion | Initial validation/timings accepted | Does fusion across vector components improve further? |
| EXP-003: inverse-NTT schedule | Initial validation/timings accepted | Does reducing Barrett frequency help within the required bounds? |
| EXP-004: optional interaction study | Deferred; never run | Would controlled separate variants answer a distinct interaction question? |
| EXP-005: error-vector NTT reduction | Initial validation/timings accepted with tradeoffs | Does deferring this reduction improve keygen over EXP-003? |
| EXP-006: keygen dot-product reduction | Correctness/counts/scoped assembly accepted; timing pending | Can keygen omit dot-output centring before its retained scale conversion? |
| Final security assessment | Required; dynamic checks pending | Do the selected changes introduce detectable implementation-security problems? |
| Final direct/repeat-session comparison and thesis artifacts | Pending | What total improvement and limitations can I defend? |

EXP-005 saves 512/768/1024 keygen Barrett calls while preserving Montgomery and encap/decap counts. Accepted deterministic/invalid-input transcripts, targeted arithmetic tests, upstream suites and exercised UBSan checks agree. Raw-error/addition bounds are 23299/26627 for Kyber512 and 23298/26626 otherwise; skpv and inverse-input centring remain intact. Reviewed keygen canaries, endbr64 and page probes remain. Keygen code grows by 17/33/40 bytes and local stack changes by +16/+16/0 bytes; the earlier EXP-002 dot-product canary tradeoff persists.

These checks support bounded correctness and implementation-safety conclusions. They do not establish whole-program constant time, statistical leakage resistance or production approval. Following the supervisor requirement clarified in ACT-0014, I will complete the [focused security assessment](notes/implementation_security.md): secret-flow checks and secret-class timing measurements alongside the existing proofs/tests/assembly. VTune is excluded from the remaining work at my request in ACT-0015; the focused security assessment remains required. Final ML-KEM conformance and physical side-channel/fault resistance remain outside the established claims.

I am near the end of arithmetic changes, but practical work remains. [EXP-006](notes/experiments/EXP-006-keygen-dot.md) is the final planned candidate: a dedicated keygen dot function retains poly_tomont while omitting its preceding Barrett centring. The general dot and inverse-input contracts stay unchanged. The actual [RUN-0001 validation](notes/runs/EXP-006-RUN-0001.md) passes all 69 steps, normal/UBSan compatibility checks, targeted arithmetic oracles, upstream suites and counts. Keygen saves another 512/768/1024 Barrett calls, with all other counts unchanged. The scoped assembly confirms the retained scale conversion and general dot, keygen canaries and public control/indexing. A new 285/355/413-byte dot body is added; keygen local stack changes by 0/-16/0 bytes. These code/stack findings and the inherited dot-canary tradeoff are recorded. Next I commit the new support/records and run the [fresh EXP-005/EXP-006 timing comparison](notes/keygen_dot_timing.md); no further arithmetic edit is needed. After this trial, I freeze the search, assess security, compare the selected version directly with the original reference across repeat sessions, and prepare reproducible thesis tables/figures. The [completion checklist](notes/practical_completion.md) defines the remaining work and stopping criteria.

EXP-004 was reserved for studying interactions between independently controlled optimisations. Existing retained variants already build on one another, so repeating the same combination would duplicate work. It was not run or rejected and is not required to finish this scope.

EXP-005 validation source is 5a499bd1940ce0ff8fd5d973f6f46b62b50c0648 with results af3408156a334c52676b51a5348540c17234390c. Latest timing/support source is 4bd813ed71a90c7722275dc802336852214a5388 with results eb4c34586c7531bc87dcd165e952d3278cea0b5e. The source identifies executed code; the results commit archives outputs. EXP-006 validation source/support is 4c9d539eba8903c2404591b8024e7afef15bbf47, with results 571f597a0b35fd0c9df264402d4b74d07a725204. EXP-006 formal performance remains pending.

I manually apply arithmetic changes and perform Git operations, reviewing support code before committing it. I retain failed and inconclusive outcomes, use distinct experiment/run IDs, and keep validation evidence separate from performance results. The legacy summary script remains unused.
