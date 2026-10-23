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
- [EXP-006 measured results and candidate selection](notes/runs/EXP-006-RUN-0002.md)
- [EXP-007 executable secret-flow protocol](notes/experiments/EXP-007-secret-flow.md)
- [EXP-007 accepted security results and assembly](notes/runs/EXP-007-RUN-0001.md)
- [EXP-008 statistical timing-leakage protocol](notes/experiments/EXP-008-timing-leakage.md)
- [EXP-008 accepted timing-screen findings](notes/runs/EXP-008-RUN-0001.md)
- [EXP-009 final three-session comparison](notes/experiments/EXP-009-final-comparison.md)
- [EXP-009 accepted session 1 and direct results](notes/runs/EXP-009-RUN-0001.md)
- [Thesis writing plan](notes/thesis_writing_plan.md) and [Git/branch handoff](notes/git_handoff.md)
- [Reproducible thesis figures and captions](notes/thesis_figures.md)
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

I have completed the five planned arithmetic trials (EXP-001/002/003/005/006) and frozen the optimisation search. I select EXP-005 as the provisional primary candidate, with EXP-003 retained as an explicit closing comparator/fallback. EXP-005 includes EXP-003's inverse-NTT improvements; its percentages describe an additional change, not a competing replacement. EXP-006 remains a secondary research comparison: fewer reductions did not produce a general speed improvement. The current arithmetic checkout still contains EXP-006; the security runner restores EXP-005 faithfully into its build directory, without changing that checkout.

The latest direct comparison is accepted [EXP-009/RUN-0001](notes/runs/EXP-009-RUN-0001.md), session 1 of 3. Its median paired time reductions relative to the original are:

| Candidate | Parameter | Keygen | Encap | Decap |
|---|---|---:|---:|---:|
| EXP-003 | Kyber512 | +5.97% | +15.29% | +15.43% |
| EXP-003 | Kyber768 | +13.24% | +18.48% | +18.64% |
| EXP-003 | Kyber1024 | +16.01% | +19.32% | +19.94% |
| EXP-005 | Kyber512 | +10.72% | +15.90% | +15.84% |
| EXP-005 | Kyber768 | +13.54% | +19.07% | +18.68% |
| EXP-005 | Kyber1024 | +17.38% | +19.27% | +19.59% |

Positive means faster; each cell is the median of 12 within-block percentage reductions. Both candidates beat the original in every paired operation/block comparison in this session. EXP-005 additionally improves keygen over EXP-003 by +5.26%/+0.49%/+1.62%, while Kyber1024 decapsulation is 0.36% slower in all twelve pairs. I retain those tradeoffs and defer final selection until sessions 2 and 3. All 324000 duration rows and three derived tables reproduce; 108 production bodies match accepted assembly. These performance results are separate from leakage testing.

The [EXP-006 review](notes/runs/EXP-006-RUN-0002.md) remains the adverse/secondary trial: keygen −2.55%/+0.22%/+1.67% against EXP-005, with mostly regressive control operations. No result or raw evidence is removed from the history.

| Stage | Current state |
|---|---|
| Original reference and measurement process | Initial preparation complete |
| EXP-001/002/003/005 | Correctness, counts, scoped assembly and initial timings accepted; EXP-005 selected for closing evaluation |
| EXP-004 | Deferred interaction/ablation idea; never implemented or run; not needed to finish |
| EXP-006 | Trial closed with mixed performance; not adopted as the general candidate; preserved as a research result |
| EXP-007 secret-flow assessment | RUN-0001 accepted: 144 quiet target processes, all 18 deliberate dependencies detected; bounded branch/address finding |
| EXP-008 statistical timing-leakage assessment | RUN-0001 accepted: 288 quiet target processes; 18 positive controls detected and 18 negatives quiet; bounded claim |
| EXP-009 final direct comparison | RUN-0001/session 1 accepted; two formal sessions remain, with unchanged support and 12 balanced blocks each |
| Thesis artifacts | Performance/count, secret-flow and timing-screen figures available; final direct-performance and consolidated handover remain |

EXP-006 saves another 512/768/1024 keygen Barrett calls but grows the scoped keygen-plus-new-dot code by 266/364/405 bytes. Keygen local-stack changes are 0/-16/0 bytes. Existing keygen protections remain; the EXP-002 general-dot local-canary tradeoff persists, and the extra dedicated dot has the same no-canary pattern. Correctness, sampled invalid inputs, range/scale/narrowing arguments and exercised UBSan checks support bounded implementation-safety conclusions. Layout/compiler effects are possible performance contributors, not established causes.

The [accepted EXP-007 run](notes/runs/EXP-007-RUN-0001.md) compares original/EXP-005/EXP-006 across all parameters and eight path/operand-role cases. All 144 target processes and all negative/defined controls were quiet; all 18 deliberately marked branch/address controls were detected. I verified 870 raw files and 129 assembly bodies. This supports no marked-secret branch/address dependency observed on those executed paths; it is not whole-KEM constant-time proof. The [accepted EXP-008 screen](notes/runs/EXP-008-RUN-0001.md) compares original/EXP-003/EXP-005: all 1944 statistics reproduce, the largest target |t| is 2.91016 against threshold 10, and all controls meet their criteria. No difference was detected within the finite tested budget. VTune is excluded; physical side channels, faults and final ML-KEM certification remain outside the established claim.

I now move from finding optimisations to checking and explaining the selected result. The [completion checklist](notes/practical_completion.md) specifies the remaining direct repeat-session evaluation, consolidated security report and reproducible handover. There is no requirement to invent more optimisations. EXP-004 was reserved for a separately controlled interaction study; existing cumulative variants do not by themselves isolate interactions.

I generated [paired effects](analysis/figures/ACT-0016/exp006-paired-effects.svg), an [incremental-results overview](analysis/figures/ACT-0016/incremental-effects-overview.svg) and [reduction-count plots](analysis/figures/ACT-0016/reduction-counts.svg). PNG/PDF versions, exact data, captions and input/code checksums accompany them. ACT-0017 adds the [EXP-007 coverage matrix](analysis/figures/ACT-0017/exp007-secret-flow.svg) and corrects generated SVG trailing whitespace without changing the original plotted data. ACT-0018 adds the [timing-screen diagnostics](analysis/figures/ACT-0018/exp008-timing-screen.svg), full statistic table and a thesis writing plan. ACT-0019 adds a [preliminary session-1 comparison](analysis/figures/ACT-0019/exp009-session1-effects.svg) with all 324 pairs; final cross-session figures await sessions 2 and 3.

EXP-006 timing/support source is 02cdbb13b49e649953dc05653bcb94002491b236; results are committed in 42d68a7da90f5d19d0539a0e8825a24852121e41. The [run record](notes/runs/EXP-006-RUN-0002.md) identifies validation and historical control commits separately. I manually perform arithmetic edits and Git operations, reviewing support before committing it. Formal runs require that commit; ACT-0017 accepts the formal EXP-007 run from source 5dfac7ba0a775dfe8812a9ef1ef3e2403c0b9ba4. ACT-0018 accepts formal EXP-008/RUN-0001 from source 50db1e8cb1cbd7eada48b4a47a1fe5bd92ae2f6d. Those results and ACT-0018 support are committed in 8a5e36e5d041507cc5649c7d43edb8468000f476 and the supplied push output/local tracking ref agree that this branch history was backed up. ACT-0019 accepts EXP-009 session 1; I next commit its results and review, then collect sessions 2 and 3. A normal branch push after committing backs up the new results; final main integration follows closing review. The legacy summary script remains unused.
