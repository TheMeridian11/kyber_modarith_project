# Writing the honours thesis from the practical evidence

## Aim and relation to the draft

The original Draft Introduction Chapter.docx contains an Introduction, Methodology, four research questions and a proposed experiment table. The [draft review](evidence/ACT-0018/thesis-draft-review.json) identifies the source and reviewed sections. Its central aim remains suitable:

**How do changes to modular-reduction placement in a pinned Kyber reference implementation affect operation time, and what evidence supports their correctness and bounded implementation-security properties?**

Retain the four-question structure and replace proposed procedures with the work actually performed. The study evaluates implementation choices on the recorded reference-C/WSL platform; it does not propose a new cryptographic scheme or stronger mathematical security. VTune was excluded. The Word draft is unchanged by this plan.

## Writing order

1. **Methods.** Describe the pinned sources, cumulative variants, arithmetic bounds, compatibility/invalid-input checks, sanitizer runs, separate reduction-count instrumentation, timing design and complementary security methods. Use [benchmark conditions](benchmark_conditions.md) for recorded settings, retrospective recollections and unknowns, and [record conventions](research_workflow.md) for the units and preservation rules.
2. **Results.** For each treatment, connect the expected reduction saving to its validation, measured effect and tradeoff. Include the mixed EXP-006 result and explain EXP-004 as an unperformed, deferred interaction study. Present the [three-session closing comparison](final_comparison.md) and then the separate [five-session random-seed follow-up](random_seed_followup.md); do not pool them.
3. **Discussion.** Explain why fewer reduction calls need not give proportional speed gains. Distinguish observed code/layout effects from possible causes, preserve adverse results, and discuss the security and measurement limits. EXP-010 supports the large baseline-reference gains while qualifying smaller direct effects; the [candidate decision](final_candidate.md) gives the current interpretation.
4. **Introduction and background.** Align the original motivation with the completed scope. Explain the NTT, Montgomery/Barrett reduction and implementation-security methods. Verify full-text literature and page locators before making detailed literature-dependent claims.
5. **Conclusion and abstract.** Answer the four questions using the accepted result records. Identify which study supports each number, state the workload-dependent candidate decision, and preserve the boundaries of the security conclusion.

## Research questions and evidence

| Original question | Evidence and emphasis | Boundary |
|---|---|---|
| RQ1: Which stages/components are most affected by modular-arithmetic overhead? | [Reduction-site map](reduction_map.md), separate call counts and targeted arithmetic changes. Connect admissible ranges and representations to each removed or deferred reduction. | Counts establish frequency, not time spent in each function. Without a runtime profile, do not claim a complete hotspot ranking or exact runtime attribution. |
| RQ2: How do optimisations affect keygen, encapsulation and decapsulation runtime? | Incremental studies in the [register](experiment_register.md), EXP-009 and EXP-010. Give the staged inverse transform substantial emphasis: it is already part of the selected implementation. Retain EXP-006 as the counterexample to “fewer reductions always means faster.” | Separate conditional incremental effects, cumulative baseline-reference effects and the additional EXP-003-to-EXP-005 contrast. Individual durations are not independent experiments; descriptive ranges are not confidence intervals. |
| RQ3: Are correctness and interoperability with the baseline preserved? | Accepted validation run records, deterministic byte/transcript comparisons, cross-implementation checks, round trips, malformed/noncanonical inputs and exercised UBSan checks. | Explain the caller bounds and tested coverage. Successful shared-secret round trips alone do not establish complete correctness. |
| RQ4: What performance, memory and constant-time tradeoffs arise? | [Candidate rationale](final_candidate.md), scoped generated-code/local-stack reviews and the [security matrix](final_security_summary.md). EXP-007 covers original/EXP-005/EXP-006; EXP-008 directly covers original/EXP-003/EXP-005. | Local stack is not peak KEM memory or heap usage. Canary/endbr instructions are not broad safety guarantees. Dynamic marked-secret tests and a finite statistical screen are distinct, bounded methods—not a whole-program constant-time proof. |

The follow-up retains additional keygen benefit and the Kyber1024 decapsulation cost, but does not support the earlier encapsulation penalty as a consistent cross-study effect. Use the complete tables and their adverse cells rather than a single overall speed score.

## Changes to make in the original draft

| Draft proposal or wording | Revision supported by the record |
|---|---|
| Increasing coefficient storage capacity as the main treatment | Describe targeted int32_t products/accumulation and call-site reduction deferrals. Stored polynomial coefficients remain int16_t. This is not an established faithful replication of a paper's entire storage scheme. |
| Profiling in the planned-experiment table | Replace it with source/reduction-site audit, separate call-count instrumentation and controlled timing comparisons. VTune was excluded; counts are not profiler-based time attribution. |
| Individual operations as independent experimental units | Distinguish inner durations, matched process blocks and separately launched sessions. Explain each study's pairing, order and fixture plan. |
| Runtime measured in ns, ms or CPU cycles | Use CLOCK_MONOTONIC_RAW nanoseconds for performance. The separate leakage screen uses RDTSCP TSC ticks, not measured core cycles. |
| Mean, median and standard deviation as interchangeable summaries | Describe the actual median of paired effects and separate three-session/five-session summaries. For EXP-010, explain pooled box quartiles/full-range whiskers and the distinct session-based diamond. Do not promise unreported mean/SD or confidence intervals. |
| Stack, heap or coefficient-storage measurements | State the precise function-body/local-stack scope. Whole-program peak memory and heap use were not measured. |
| Timing consistency as a security review | Replace this with the public/secret threat model, bounds, compatibility checks, generated-code review, dynamic marked-secret checks and a predeclared statistical screen with controls. Ordinary performance spread is not leakage evidence. |
| Kyber and final-standard ML-KEM used interchangeably | Identify the pinned Kyber revision; do not claim final ML-KEM certification or verified conformance. |
| Literature maximum speedups used as targets or direct comparisons | Retain only verified source context. Different implementations, platforms and protocols do not provide a matched comparison. Full-text review remains necessary for detailed replication claims. |
| Completed procedures described in future tense | Write Methods in past tense and cite the accepted run records. Keep prospective wording inside historical protocols unchanged. |

A suitable security-results sentence is: “Across the prespecified EXP-008 target cells, no statistic exceeded the diagnostic threshold; positive and negative controls met their criteria. This supports no detected class-dependent timing difference within the tested paths, input classes, compiler, platform and sample budget.” Do not replace it with a claim that the implementation is secure or that the changes have no security effect.

## Figures and remaining work

The [figure guide](thesis_figures.md) supplies the captions and exports. Use the incremental/count overview to explain the progression, the completed EXP-009 session comparison for closing performance, the separate EXP-010 dot-and-box graphs for robustness, and the security/code/local-stack figures for tradeoffs. Preliminary session-1 and fuller spread plots can support an appendix; keep their historical status clear.

The [completion record](practical_completion.md) identifies the finished practical scope. Remaining work is the written argument, full-text literature verification and supervisor feedback. Unrecorded power settings, breaks, background activity and physical placement belong in the limitations; they do not prevent writing. The original brief's AVX2 collaborator transfer study remains a separate follow-on beyond this reference-C work.
