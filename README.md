# Kyber modular-arithmetic optimisation

This honours project evaluates changes to modular-reduction scheduling and intermediate arithmetic in the reference C implementation of Kyber. The study covers key generation, encapsulation and decapsulation for Kyber512, Kyber768 and Kyber1024, with separate correctness, performance and implementation-security assessments.

The original source is [pq-crystals/kyber](https://github.com/pq-crystals/kyber), pinned to [3edd5af59919](notes/source_revisions.md). The results concern that implementation and the recorded platform; they do not establish final-standard ML-KEM conformance or superiority over other optimised implementations.

Validation combined bounds on intermediate values with deterministic comparisons against the original implementation, invalid-input checks and undefined-behaviour sanitizer tests. Separate instrumented builds counted reduction calls, while ordinary builds supplied performance measurements. Benchmarks ran under Ubuntu WSL on an Intel Core i9-12900KS, using matched input fixtures and controlled process ordering. Raw measurements, build identities and analysis scripts are retained so the reported tables and figures can be traced back to the recorded runs.

## Findings

The selected implementation (EXP-005) combines fused base multiplication, wider vector-dot accumulation, staged inverse-transform reduction and deferred reduction of the keygen error vector. The preceding candidate (EXP-003) contains the first three changes. A further keygen-specific trial reduced call counts but gave mixed timings: fewer reductions did not always mean faster execution.

The table reports the selected implementation's percentage time reduction against the original reference. Each value is the median of session estimates, each based on 12 matched block effects. The three-session closing comparison and five-session random-seed follow-up are separate studies.

| Study | Parameter | Key generation | Encapsulation | Decapsulation |
|---|---|---:|---:|---:|
| Closing comparison (EXP-009) | Kyber512 | 10.72% | 16.09% | 15.96% |
| Closing comparison (EXP-009) | Kyber768 | 13.44% | 19.08% | 18.80% |
| Closing comparison (EXP-009) | Kyber1024 | 17.47% | 19.30% | 19.71% |
| Random-seed follow-up (EXP-010) | Kyber512 | 10.93% | 16.09% | 16.06% |
| Random-seed follow-up (EXP-010) | Kyber768 | 13.62% | 19.22% | 19.01% |
| Random-seed follow-up (EXP-010) | Kyber1024 | 17.84% | 19.87% | 20.18% |

The follow-up used 60 saved random seeds and supports the substantial gains over the original. Additional keygen benefit over the preceding candidate persisted. The small Kyber1024 decapsulation cost also repeated, while encapsulation differences were mixed. [Candidate selection and tradeoffs](notes/final_candidate.md) explain why both implementations remain useful.

Reviewed arithmetic bounds, compatibility and exercised sanitizer checks support correctness within their stated scope. Dynamic secret-flow checks and a finite statistical timing screen found no targeted dependency or class-dependent timing difference in the tested cases. [The security conclusion](notes/final_security_summary.md) retains the code/local-stack and inherited local-canary tradeoffs. These single-platform findings do not establish a whole-program constant-time proof, production certification or final-standard ML-KEM conformance.

## Read the project

| Route | Start here |
|---|---|
| Read the findings | [Closing comparison](notes/final_comparison.md), [random-seed follow-up](notes/random_seed_followup.md), [candidate decision](notes/final_candidate.md), [figures and captions](notes/thesis_figures.md) |
| Reproduce the results | [Analysis, audit and script guide](notes/git_reproduce.md), [benchmark conditions](notes/benchmark_conditions.md), [safe figure reproduction](notes/thesis_figures.md#reproduce) |
| Inspect the research record | [Experiment register](notes/experiment_register.md), [activity log](notes/project_log.md), [methods and record conventions](notes/research_workflow.md), [reduction map](notes/reduction_map.md), [literature](notes/literature.md) |

The [thesis writing plan](notes/thesis_writing_plan.md) maps the evidence to the original research questions; the [completion record](notes/practical_completion.md) identifies the remaining writing work.

## Source and layout

The original [pq-crystals/kyber](https://github.com/pq-crystals/kyber) revision and evaluated source snapshots are recorded in the [revision index](notes/source_revisions.md). All 35 selected source files match [the source pin](analysis/final_candidate.json).

| Directory | Purpose |
|---|---|
| `implementation/` | Original reference and selected optimised implementation |
| `external/` | Pinned upstream checkout |
| `scripts/`, `benchmarks/`, `tests/` | Collection support, measurement harnesses and validation |
| `results/` | Raw observations, manifests and per-run derived tables |
| `analysis/` | Analysers, independent reviews, figure generators and outputs |
| `notes/` | Interpretation, methods and detailed historical evidence |

Code, historical protocols and adverse findings remain available for reproducibility. The experiment register links accepted outcomes separately from precollection plans; the original programme and random-seed follow-up are complete.
