# Beginning the honours thesis from the practical evidence

## Relation to the original draft

The original Draft Introduction Chapter.docx contains an Introduction and Methodology, including four research questions, a planned-experiment table and reliability/validity discussion. The [draft review](evidence/ACT-0018/thesis-draft-review.json) identifies the document and reviewed sections. This plan maps that draft to the completed research; the Word document remains unchanged.

The draft's central aim still fits: an evidence-based comparison of modular-arithmetic choices across Kyber performance, correctness and implementation security. I can retain its four-question structure while updating the proposed method to describe the work actually performed.

The study includes an explicit assessment of how implementation changes affect security. Its scope is the pinned reference-C implementation on the recorded platform; VTune is excluded. The thesis and supporting repository form the research submission.

## Central research story

A concise framing consistent with the draft is: **How do changes to modular-reduction placement in a pinned Kyber reference implementation affect operation time, and what evidence supports their correctness and bounded implementation-security properties?**

I study implementation choices, not a new cryptographic scheme or stronger mathematical security. I progressively fuse or defer reductions under explicit operand/representation contracts. I then measure both useful improvements and a counterexample to the assumption that fewer reductions always means faster execution. Finally I examine correctness, generated code and secret-flow/timing behaviour through complementary methods.

The strongest narrative connects an argument to each experiment: expected reduction saving, admissible bounds and scale, byte-level compatibility and safety checks, measured effects, generated-code/security tradeoffs, and retention decision. EXP-003's consistent encapsulation/decapsulation benefit deserves emphasis. EXP-005 includes it and adds a keygen treatment; EXP-006 supplies a valuable mixed/adverse finding. ACT-0020 supplies the [complete cumulative comparison](final_comparison.md) and [EXP-005 selection](final_candidate.md), while retaining the small Kyber1024 regressions.

## Writing order

1. **Methods first.** The [benchmark conditions](benchmark_conditions.md) distinguish recorded settings, retrospective recollection and remaining unknowns. I can write the reproducible setup now: pinned upstream revision, reference C/WSL/GCC scope, cumulative variants, deterministic fixtures, correctness/invalid-input checks, bounds/UBSan, normal versus instrumented builds, timer/affinity/order, paired-process units and repeat-session design. I explain the security threat model and why dynamic branch/address checking and a finite statistical screen answer different questions.
2. **Results next.** I organise by research question rather than a terminal-command diary. Each optimisation gets its change, count effect, timing result and tradeoff. I include EXP-006 and explain EXP-004 as a deferred unperformed idea. I insert the existing figures with their exact captions. I now use the audited ACT-0020 cumulative tables and figures, keeping all three session estimates and adverse groups visible.
3. **Discussion after results.** I explain why operation/parameter effects differ, why fewer calls can fail to improve time, and what compiler layout/code/stack observations do and do not establish. I distinguish measured facts from plausible mechanisms. I discuss the local-canary tradeoff and the limits of quiet leakage tests.
4. **Revisit introduction and background.** I align the original motivation and aims with what was actually evaluated, then use literature to explain the NTT, Montgomery/Barrett reduction and implementation-security methods. I verify full-text sources and page locators before relying on claims not yet checked.
5. **Write conclusion and abstract last.** I state measured cumulative results, the final candidate decision and bounded security findings from the accepted EXP-009 closing comparison and decision. I avoid promising universal gains, ML-KEM certification or a constant-time proof.

## Claim-to-evidence map

| Thesis claim or question | Evidence to use | Boundary to state |
|---|---|---|
| Why these reduction schedules are admissible | EXP-001/002/003/005/006 plans and range/representation arguments | Caller contracts and compiler assumptions; not every possible arbitrary input |
| Functional compatibility and arithmetic safety | Accepted RUN-0001 validation records, deterministic transcripts, malformed/noncanonical cases and UBSan | Executed coverage plus explicit arguments; successful round trips alone are insufficient |
| Conditional incremental gains | Each RUN-0002 review and incremental-effects overview | Different predecessors/sessions; percentages are not a cumulative ranking |
| EXP-003's targeted result | EXP-003/RUN-0002: all 30 encap/decap pairs positive | Relative to EXP-002; keygen movements also retained |
| Fewer reductions can have mixed performance | EXP-006/RUN-0002, count and paired-effect plots | Counts are calls, not instruction counts or proof of speed |
| Secret branch/address findings | EXP-007/RUN-0001 and coverage figure | Directly tests original/EXP-005/EXP-006 on exercised paths |
| Statistical timing findings | EXP-008/RUN-0001 and timing-screen figure | Directly tests original/EXP-003/EXP-005; no detected difference within finite classes/budget |
| Code, local stack and hardening tradeoffs | Scoped assembly review in each accepted run | Local function observations; canary/endbr instructions are not broad safety guarantees |
| Cumulative benefit and closing candidate | EXP-009's three direct sessions and final interpretation | All three sessions accepted in ACT-0020; EXP-005 selected with explicit costs. Report descriptive session ranges and adverse cells, no pooled-inner-sample inference |

Suggested results sentence: “Across the prespecified EXP-008 target cells, no statistic exceeded the diagnostic threshold; positive and negative controls met their criteria. This supports no detected class-dependent timing difference within the tested paths, input classes, compiler, platform and sample budget.” I do not replace it with “the implementation is secure” or “the optimisations have no effect on security.”

## Practical finish line

The practical study is complete: arithmetic trials, planned security tests, three-session comparison, candidate selection and source verification. The analysis and figures reproduce from retained data, and the [repository record](git_handoff.md) records integration of the selected source. Methods, Results and Discussion can now be written from accepted evidence. Reproducing retained-data analysis is distinct from rerunning the experiments in a fresh environment. Historical power settings, breaks and other unrecorded controls remain limitations in the conditions record; they do not prevent beginning the thesis. Full-text literature verification and the written argument remain to be completed.

## Map the original four research questions to the completed study

| Original question | Evidence and writing decision |
|---|---|
| RQ1: Which stages/components are most affected by modular-arithmetic overhead? | Use the reduction-site audit, per-operation call counts and targeted changes to explain where reducing work affected complete KEM time. Narrow the wording to reduction frequency and measured impact; without a runtime profile I cannot claim an exact percentage of time spent inside every function or rank all hotspots. |
| RQ2: How do optimisations affect keygen, encapsulation and decapsulation runtime? | Use the incremental studies plus the EXP-009 direct comparisons, with all three sessions accepted. Separate the cumulative original-to-EXP-003/005 result from the additional EXP-003-to-005 effect, and retain EXP-006's adverse cells. |
| RQ3: Are correctness and interoperability with the baseline preserved? | Describe deterministic byte/transcript comparisons, cross-implementation checks, round trips, malformed/noncanonical cases and unchanged formats. These substantially expand the draft's proposed shared-secret check, with tested coverage and bounds stated. |
| RQ4: What performance, memory and constant-time tradeoffs arise? | Connect operation times, reduction counts, scoped code/local-stack observations, range/scale arguments, canary changes, EXP-007 and EXP-008. State the limits of every layer. There is no measured whole-program peak-memory/heap result or complete constant-time proof. |

## Specific changes to make in the draft

| Draft proposal or wording | Revision supported by the actual work |
|---|---|
| Increasing coefficient storage capacity as the main treatment | Describe targeted int32_t product/accumulation intermediates and fixed/call-site reduction deferrals. Stored polynomial coefficient arrays remain int16_t. The work is inspired by the reduction-overhead question, not an established faithful replication of a paper's entire storage scheme. |
| A profiling row in the planned-experiment table | Replace it with source/reduction-site audit, separate call-count instrumentation and controlled per-treatment timing comparisons. VTune is excluded. Counts identify reduction frequency, not time attribution. |
| Individual operation executions as the main experimental units | Distinguish inner observations from matched process blocks and separately launched sessions. The latter units support the reported repeatability statements. |
| Runtime may use ns, ms or CPU cycles | Specify CLOCK_MONOTONIC_RAW nanoseconds for performance and TSC ticks for the separate leakage screen. Do not label RDTSCP ticks as core cycles. |
| Median, average and standard deviation listed as primary measures | Describe the actual paired-median effects, individual block effects and three-session descriptive ranges. Explain this choice; do not promise unreported mean/SD or present ranges as confidence intervals. |
| Possible stack, heap or coefficient-storage measurements | Define the scoped generated-code/local-stack observations precisely. Do not imply peak total-memory or heap profiling was performed. |
| Timing consistency as security review | Replace this vague method with the public/secret threat model, bounds and compatibility checks, generated-code review, dynamic marked-secret branch/address tests and predeclared statistical screen with controls. Ordinary timing spread is not leakage evidence by itself. |
| Kyber described interchangeably with standardised ML-KEM | Identify the exact pinned Kyber revision as the evaluated implementation, distinguish it from a verified final-standard ML-KEM implementation, and avoid certification/conformance claims. |
| Literature maximum speedups cited as motivation | Retain them only with verified source context. They are not targets this study must match and are not direct comparisons without matched implementations/platforms/protocols. Full-text review remains required before detailed replication claims. |
| Proposed methodology in future tense | Convert completed procedures to past tense and cite actual run IDs. Use the accepted EXP-009 three-session results and ACT-0022 verified EXP-005 source, with the completed repository state recorded separately. |

The original brief places an AVX2 collaborator's transfer study after this reference-C work. That remains a separate follow-on study outside the completed practical scope.

Retain the draft's Introduction → Methodology foundation, remove repeated motivation from Methods, and add Results and Discussion organised by the four questions. Begin by expanding the methodology with the actual protocols and evidence references, then write results around the available tables and figures.

## Main results and figures

I can state that the selected cumulative EXP-005 variant reduces operation times by 10.72–19.71% across the nine parameter/operation groups in the median of the three session estimates on this setup. I follow that with the complete table, rather than imply a single overall gain. I separately report its additional keygen benefit over EXP-003 and the repeated Kyber1024 control-operation regressions. The range across groups is not an uncertainty interval.

I use the [three-session figure](../analysis/figures/ACT-0020/exp009-three-session-effects.pdf) in the main Results, the [all-pairs plot](../analysis/figures/ACT-0020/exp009-all-paired-effects.pdf) where spread matters or in an appendix, and the [keygen tradeoff figure](../analysis/figures/ACT-0020/exp005-keygen-tradeoffs.pdf) beside the memory/hardening discussion. The [final security matrix](final_security_summary.md) supports the security-method justification. I continue to verify literature-dependent claims separately; these local results do not establish full-text claims from external papers.

## One-paragraph supervisor summary

I investigated five ways to reduce unnecessary modular-arithmetic work in Kyber's reference C implementation, combining operations and delaying reductions only where explicit bounds showed that the intermediate values remained valid. I checked compatibility with the original implementation, tested invalid inputs and exercised arithmetic-safety checks, then compared the original and two cumulative variants in three measurement sessions across all three parameter sets. On the tested setup, the selected implementation reduced key-generation time by approximately **10.7–17.5%**, encapsulation time by **16.1–19.3%**, and decapsulation time by **16.0–19.7%**; these ranges describe the final estimates across parameter sets. The tests also showed that removing more reductions did not always improve performance, and I retained the slower cases and code-size/local-stack costs in the findings. Focused security tests detected no secret-dependent branch/address behaviour or timing differences within the tested paths and budgets, without establishing a complete constant-time proof. The resulting code, raw measurements, reproducible analysis and figures provide the evidence for the thesis.
