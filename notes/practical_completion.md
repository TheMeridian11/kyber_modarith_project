# Practical completion checklist

## Where I am

I have completed the planned arithmetic trials, dynamic secret-flow assessment, bounded statistical timing screen and all three final performance sessions. In ACT-0020 I select EXP-005 as the primary thesis candidate, retain EXP-003 as a substantial comparator/workload-dependent alternative and preserve EXP-006 as the adverse trial. The experimental work, final comparison, candidate decision and consolidated evidence outputs are complete. ACT-0022 verifies the restored selected source and completes the source/documentation handoff review. The remaining actions are the manual handoff commit/push and history-preserving main integration. I do not need additional timing sessions or optimisations under the completed protocol.

| Experiment | Simple description | State |
|---|---|---|
| EXP-000 | Establish the unchanged reference and measurement process | Initial preparation complete |
| EXP-001 | Combine products before reducing each small multiplication | Correctness and initial timings reviewed |
| EXP-002 | Extend that fusion across a whole vector dot product | Correctness and initial timings reviewed; local-canary tradeoff recorded |
| EXP-003 | Reduce less often during the inverse transform | Correctness and initial timings reviewed; targeted encap/decap gains |
| EXP-004 | Ask whether independently controlled optimisations interact when combined | Deferred; no implementation/run or failed result |
| EXP-005 | Delay centring the keygen error vector until its final addition | Correctness and initial timings reviewed; keygen gains and small other-operation regressions recorded |
| EXP-006 | Delay keygen dot-product centring before its existing scale conversion | Initial trial closed; mixed timings, not adopted as general candidate |
| EXP-007 | Check whether secret values affect executed branches/addresses | RUN-0001 accepted with sensitive controls and bounded claims |
| EXP-008 | Check timing differences between selected secret classes | RUN-0001 accepted: no difference detected within budget; sensitive controls |
| EXP-009 | Compare original, EXP-003 and EXP-005 directly across sessions | All three sessions accepted in ACT-0020; EXP-005 selected with documented tradeoffs |

The numbers are identifiers, not a required sequence of six successful optimisations. EXP-004 was reserved for a different interaction question. The retained implementations already build on one another, so repeating that same combination would not answer a new question. A distinct interaction study needs controlled separate variants/ablations. It is optional and does not block this project's completion.

The [EXP-005 timing review](runs/EXP-005-RUN-0002.md) finds median paired keygen time reductions of 5.18%, 0.48% and 1.36% against fresh EXP-003. Kyber1024 encap/decap medians are -0.12%/-0.50%; these tradeoffs remain visible. Single-session incremental percentages cannot be added or multiplied to claim a total gain over the original reference.

## What remains, in order

### 1. Finish the final candidate trial

- [x] Manually apply the three [EXP-006 edits](experiments/EXP-006-keygen-dot.md), review/commit source and support, and execute RUN-0001.
- [x] Review actual correctness, bounds, counts, assembly, local stack and hardening findings: [ACT-0015 acceptance](runs/EXP-006-RUN-0001.md).
- [x] Prepare and development-check the [fresh EXP-005/EXP-006 timing protocol](keygen_dot_timing.md).
- [x] Review/commit that support and execute EXP-006/RUN-0002; [ACT-0016 review](runs/EXP-006-RUN-0002.md) retains all regressions and mixed outcomes.
- [x] Select EXP-005 as primary, keep EXP-006 as a secondary research comparison and freeze the optimisation search. At that checkpoint the checkout remained EXP-006; ACT-0022 verifies its exact restoration to selected EXP-005.

### 2. Complete the required implementation-security assessment

My supervisor asked me to determine a suitable way to evaluate security effects. I therefore need more than a statement that tests passed. The [assessment plan](implementation_security.md) combines existing range/compatibility/assembly evidence with dynamic secret-flow checking and focused statistical timing-leakage tests.

- [x] Pin dynamic-check tools, write the public/secret map and prepare [EXP-007](experiments/EXP-007-secret-flow.md): seven arithmetic path/operand-role cases plus IND-CPA decryption.
- [x] Exercise the full development matrix: 9 builds, 198 Memcheck processes, 18 detected marked positive controls, quiet target/defined/negative checks; 102 production bodies match accepted normal code.
- [x] Commit support, execute EXP-007/RUN-0001 and review all controls/diagnostics: accepted bounded secret-flow findings in ACT-0017; results committed in 50db1e8cb1cbd7eada48b4a47a1fe5bd92ae2f6d.
- [x] Prepare/pin the EXP-008 custom dudect-style harness and reference, run sensitivity pilots and specify finite budgets/classes/seeds/thresholds/stopping rules.
- [x] Commit ACT-0017 support, collect formal EXP-008/RUN-0001 and audit all controls/statistics/assembly in ACT-0018. Its results and ACT-0018 support are committed in 8a5e36e5d041507cc5649c7d43edb8468000f476.
- [x] Compare original/EXP-003/EXP-005 in the statistical screen and record bounded conclusions. No target exceeds the frozen diagnostic threshold; no signal-triggered follow-up is required by this protocol.
- [x] Complete the [final security matrix](final_security_summary.md), including the inherited canary tradeoff, code/local-stack changes and unassessed attack classes.

This is required practical work. It is not a formal whole-program proof or a new physical side-channel project. VTune is excluded from the plan at my request in ACT-0015. The security tests remain required. If the local setup is insensitive or unsupported, I need to diagnose that limitation and choose a workable test setup; I cannot label an unrun or inconclusive test as passed.

### 3. Confirm the final performance result directly

- [x] Prepare and development-check [EXP-009](experiments/EXP-009-final-comparison.md), including exact restoration and 108 matching production bodies.
- [x] Commit ACT-0018 support and EXP-008 results before formal EXP-009 collection: 8a5e36e5d041507cc5649c7d43edb8468000f476.
- [x] Collect and audit [EXP-009/RUN-0001, session 1](runs/EXP-009-RUN-0001.md): 324000 valid durations, all three tables reproduced, 108 reviewed bodies matched.
- [x] Finish and audit all three separately launched EXP-009 sessions, each with 12 triplet blocks per parameter: [complete result](final_comparison.md). The six possible variant orders occur twice each; session/block seeds are predeclared. This replaces the provisional ten-pair proposal with a balanced three-way protocol.
- [x] Confirm small/adverse marginal effects with the matched three-way comparison: Kyber768 keygen gains and Kyber1024 encap/decap regressions recur in all session medians; [selection rationale](final_candidate.md) retains them.
- [x] Recheck measured final source/binary identities and round trips: all 27 binaries, 324 bodies and 972000 timing rows audited. Earlier correctness/security evidence is reused only for matching files/builds/contracts; altered arithmetic would require affected validation again.

The session or matched process pair is an experimental unit for the corresponding claim. Thousands of inner timings are not thousands of independent replications. I followed the predeclared analysis, preserved all raw observations and report descriptive three-session ranges with environmental limits. More repeated measurements on one host do not establish portability or performance on other machines.

### 4. Produce the practical handover package

- [x] Generate the first [thesis figures/tables](thesis_figures.md): all EXP-006 pairs, incremental-result overview and observed reduction-count progression, with PNG/SVG/PDF exports and input/code hashes.
- [x] Add audited EXP-007 coverage and EXP-008 timing-screen figures with reproducible tables/captions.
- [x] Add the explicitly preliminary EXP-009 session-1 plot, showing all 324 pairs and all three contrasts.
- [x] Add final direct-reference/session/spread figures, keygen code/local-stack tradeoffs and the consolidated security matrix in ACT-0020.
- [x] Write the [complete comparison and method summary](final_comparison.md), [candidate rationale](final_candidate.md) and [security conclusion](final_security_summary.md), retaining the adverse EXP-006 and deferred EXP-004 context.
- [x] Reproduce the retained-data analysis, all final audit reports and all three final figures byte-for-byte; verify source/tool/build identities and preserve all original results.
- [x] Commit and back up the complete experimental evidence, final reports and graphs: verified in ACT-0021 at 66c707f9dc8cef556d1133fb48d6fb1f71e989e7.
- [x] Complete the manual selected-source restoration and actual 35-file identity review: accepted in ACT-0022, with the expected three-file diff and no repair needed.
- [x] Finish current-status documentation, evidence-preservation checks and the reviewed [Git handoff](git_handoff.md). Scientific work and source/documentation review are complete. Retained-data reproduction is not a fresh-environment rerun.
- [ ] Execute the final handoff commit/push and main integration, checking the resulting status. These are repository publication steps, not unfinished experiments.
- [ ] Complete the thesis draft and present it with the repository to the supervisor for feedback.

## What does not need to expand automatically

I do not need to implement every possible reduction change, complete EXP-004, port to another hardware family, prove whole-program constant time, establish final ML-KEM certification or use VTune. I explicitly excluded VTune in ACT-0015. New work is justified if a finding prevents a defensible conclusion or supervisor feedback changes the scope. The optional full-text literature checks and bibliographic work also belong in thesis preparation; I must complete them before making claims that depend on those sources.

ACT-0021 verifies that both new session directories and ACT-0020 are committed in 66c707f9dc8cef556d1133fb48d6fb1f71e989e7 and that the supplied push succeeded with a matching local tracking ref. All 4474 archived result files are tracked. ACT-0022 accepts that restoration and completes the working-source/documentation review. The immediate repository action is the final handoff commit/push, followed by the documented main integration. No additional measurements are scheduled. I can write the complete Methods, Results and Discussion using the [writing plan](thesis_writing_plan.md), then present the thesis draft and repository for supervisor feedback. I record Git publication as completed only after the manual commands succeed.
