# Kyber modular-arithmetic optimisation

This honours project evaluates changes to modular-reduction scheduling and intermediate arithmetic in the reference C implementation of Kyber. The study covers key generation, encapsulation and decapsulation for Kyber512, Kyber768 and Kyber1024, with separate correctness, performance and implementation-security assessments.

The original source is [pq-crystals/kyber](https://github.com/pq-crystals/kyber). The results only apply to that exact implementation and do not prove that the code meets the final ML-KEM standard or outperforms other optimised versions.

To verify the code, I checked that internal values stayed within the required limits and compared outputs directly against the original implementation. I also tested invalid inputs and ran sanitizers to check for undefined behaviour. I used separate builds with counters to count reduction calls, and ordinary builds to measure speed. All benchmarks ran on an Intel Core i9-12900KS using Ubuntu WSL, with identical inputs within each matched comparison and a controlled execution order. I saved the raw data, build details and analysis scripts so every chart and table can be traced back to its test runs.

## Findings

I developed the optimisations in stages. The two versions in the final comparison were:

- **EXP-003:** combines fused base multiplication, wider vector-dot accumulation and a staged reduction schedule in the inverse transform.
- **EXP-005:** keeps all of those changes and also delays reduction of the key-generation error vector until the existing final public-key reduction.

I compared the original implementation with both versions across three separate sessions. This [main performance comparison](notes/final_comparison.md) is recorded as EXP-009. EXP-003 and EXP-005 identify the implementations; EXP-009 identifies the experiment that compared them.

The table shows the percentage reduction in execution time compared with the original. Positive values mean faster execution. Each session used 12 matched blocks, comparing process medians with the same input sequence. I calculated the median percentage reduction for each session, then took the median of the three session results.

| Implementation | Parameter | Key generation | Encapsulation | Decapsulation |
|---|---|---:|---:|---:|
| EXP-003 | Kyber512 | 5.97% | 15.39% | 15.59% |
| EXP-005 | Kyber512 | 10.72% | 16.09% | 15.96% |
| EXP-003 | Kyber768 | 13.18% | 18.48% | 18.64% |
| EXP-005 | Kyber768 | 13.44% | 19.08% | 18.80% |
| EXP-003 | Kyber1024 | 16.07% | 19.48% | 20.00% |
| EXP-005 | Kyber1024 | 17.47% | 19.30% | 19.71% |

Both versions were faster than the original in every matched operation comparison. EXP-003 already provides substantial improvements, including the benefit of the inverse-transform change. The results for EXP-005 include those earlier improvements, so they should not all be credited to its final key-generation change.

**I selected EXP-005 as the final implementation because it provided further key-generation improvements over EXP-003.** In their direct comparison, key-generation time fell by another **5.26%, 0.49% and 1.52%** for Kyber512, Kyber768 and Kyber1024 respectively. These percentages come from matched comparisons between the two versions, rather than subtracting the table entries above. There were tradeoffs: Kyber1024 encapsulation was **0.15% slower** and decapsulation was **0.36% slower** than EXP-003 in the main study, and the keygen code grew with some additional local stack use. The [candidate decision](notes/final_candidate.md) explains these costs and why EXP-003 remains a useful alternative for some workloads.

A further keygen-specific trial, EXP-006, reduced call counts but produced mixed timings. This was an important finding: removing more reductions did not always make the code faster.

The arithmetic bounds, output comparisons and sanitizer checks support correctness within the cases and assumptions reviewed. Secret-flow checks and a finite statistical timing test found no targeted dependency or class-dependent timing difference in the tested cases. The [security conclusion](notes/final_security_summary.md) also records the changes in code size, local stack use and inherited stack-canary coverage. These checks do not prove whole-program constant-time behaviour, production readiness or final-standard ML-KEM conformance.

### Additional check with random inputs

After the main comparison and candidate selection, I ran a separate follow-up using **60 saved random seeds across five sessions**, recorded as [EXP-010](notes/random_seed_followup.md). It used the same implementations to check whether the performance findings held across different input fixtures. The large improvements over the original and the additional key-generation benefit repeated, supporting the main findings and the choice of EXP-005. The small Kyber1024 decapsulation cost also repeated, while its encapsulation difference was mixed and close to zero. This follow-up adds supporting evidence; its results and dot-and-box graphs are reported separately from the main comparison.

## Read the project

| Route | Start here |
|---|---|
| Read the main findings | [Original, EXP-003 and EXP-005 comparison](notes/final_comparison.md), [candidate decision](notes/final_candidate.md), [figures and captions](notes/thesis_figures.md) |
| Read the additional check | [Random-seed follow-up and dot-and-box graphs](notes/random_seed_followup.md) |
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
