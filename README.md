# Kyber modular-arithmetic optimisation

This honours project evaluates changes to modular-reduction scheduling and intermediate arithmetic in the reference C implementation of Kyber. The study covers key generation, encapsulation and decapsulation for Kyber512, Kyber768 and Kyber1024, with separate correctness, performance and implementation-security assessments.

The original source is [pq-crystals/kyber](https://github.com/pq-crystals/kyber), pinned to [3edd5af59919](notes/source_revisions.md). The results concern that implementation and the recorded platform; they do not establish final-standard ML-KEM conformance or superiority over other optimised implementations.

## Main findings

Five arithmetic treatments were evaluated. The selected implementation combines fused base multiplication, wider vector-dot-product accumulation, staged inverse-transform reduction and deferred reduction of the key-generation error vector. A further keygen-specific treatment reduced call counts but produced mixed performance, demonstrating that fewer reductions alone do not guarantee faster execution.

The final comparison used three separately launched sessions, each with 12 matched blocks for the original reference and two cumulative candidates. The table shows percentage time reductions against the original. Each value is the median of three session estimates; each session estimate is the median of its 12 paired effects.

| Implementation | Parameter | Key generation | Encapsulation | Decapsulation |
|---|---|---:|---:|---:|
| EXP-003 | Kyber512 | 5.97% | 15.39% | 15.59% |
| EXP-003 | Kyber768 | 13.18% | 18.48% | 18.64% |
| EXP-003 | Kyber1024 | 16.07% | 19.48% | 20.00% |
| EXP-005 | Kyber512 | 10.72% | 16.09% | 15.96% |
| EXP-005 | Kyber768 | 13.44% | 19.08% | 18.80% |
| EXP-005 | Kyber1024 | 17.47% | 19.30% | 19.71% |

EXP-003 is the cumulative implementation through the inverse-transform change. EXP-005 includes those changes and adds the keygen error-vector treatment. EXP-005 is the selected version: its additional keygen reductions over EXP-003 are 5.26%, 0.49% and 1.52%. Kyber1024 encapsulation and decapsulation are 0.15% and 0.36% slower than EXP-003 in the combined medians; these tradeoffs remain part of the result. The [complete comparison](notes/final_comparison.md) reports all sessions, block effects and conditions, and the [selection rationale](notes/final_candidate.md) explains the decision.

Correctness and compatibility checks passed within the tested inputs and reviewed arithmetic contracts. Dynamic secret-flow tests observed no marked-secret branch/address dependencies on the exercised paths, and the finite statistical screen detected no class-dependent timing difference. These findings, the inherited local-canary change and the code/local-stack costs are documented in the [security assessment](notes/final_security_summary.md). They do not constitute a whole-program constant-time proof or production certification.

## Research record

- [Experiment register](notes/experiment_register.md): treatments, outcomes and detailed experiment/run records.
- [Activity log](notes/project_log.md): concise chronology of the research decisions and findings.
- [Methods and record conventions](notes/research_workflow.md): provenance, measurement units and acceptance rules.
- [Benchmark conditions](notes/benchmark_conditions.md): recorded environment and protocols, retrospective host details and remaining unknowns.
- [Source revision index](notes/source_revisions.md): full commit IDs behind the shortened references.
- [Reduction map](notes/reduction_map.md) and [literature record](notes/literature.md): arithmetic boundaries and idea provenance.
- [Thesis figures and reproduction](notes/thesis_figures.md): PDF/SVG/PNG outputs, captions and plot data.
- [Repository state and reproducibility](notes/git_handoff.md): selected source and retained-data analysis commands.
- [Completion record](notes/practical_completion.md) and [thesis writing plan](notes/thesis_writing_plan.md).

## Source and repository layout

The selected working source matches all 35 EXP-005 files pinned in [final_candidate.json](analysis/final_candidate.json), originally measured from [4bd813ed71a9](notes/source_revisions.md). The [repository record](notes/git_handoff.md) documents the integrated source/results history and reproduction checks.

- external/kyber-official/: pinned upstream source.
- implementation/kyber-baseline-ref/: unchanged comparison source.
- implementation/kyber-optimised-ref/: selected cumulative EXP-005 source.
- scripts/, benchmarks/, tests/: collection, validation and measurement support.
- results/: raw observations, manifests and per-run derived data.
- analysis/: reproducible calculations, figures and plot data.
- notes/: methods, experiment/run records, interpretation and retained audit evidence.

All planned experimental collection and final-source review are complete. EXP-004 remains a deferred interaction study, not an omitted failure. The earlier variants, mixed results and failed development attempts remain traceable in the detailed records. Three hash-pinned protocol documents retain their precollection wording; the accepted run records give their completed outcomes.
