# Practical completion checklist

## Where I am

I have finished the planned arithmetic trials and frozen the search in ACT-0016. I select EXP-005 as the provisional primary candidate, explicitly retain EXP-003 as comparator/fallback, and preserve EXP-006 as the secondary mixed-result trial. The practical component is now in its assessment and reporting phase: formal EXP-007 dynamic-flow results are accepted; statistical timing leakage, repeat-session/direct performance confirmation and the final evidence package remain. I do not need more optimisations to reach an arbitrary count.

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
| EXP-008 | Check timing differences between selected secret classes | Protocol/support and control pilot ready; formal collection pending |

The numbers are identifiers, not a required sequence of six successful optimisations. EXP-004 was reserved for a different interaction question. The retained implementations already build on one another, so repeating that same combination would not answer a new question. A distinct interaction study needs controlled separate variants/ablations. It is optional and does not block this project's completion.

The [EXP-005 timing review](runs/EXP-005-RUN-0002.md) finds median paired keygen time reductions of 5.18%, 0.48% and 1.36% against fresh EXP-003. Kyber1024 encap/decap medians are -0.12%/-0.50%; these tradeoffs remain visible. Single-session incremental percentages cannot be added or multiplied to claim a total gain over the original reference.

## What remains, in order

### 1. Finish the final candidate trial

- [x] Manually apply the three [EXP-006 edits](experiments/EXP-006-keygen-dot.md), review/commit source and support, and execute RUN-0001.
- [x] Review actual correctness, bounds, counts, assembly, local stack and hardening findings: [ACT-0015 acceptance](runs/EXP-006-RUN-0001.md).
- [x] Prepare and development-check the [fresh EXP-005/EXP-006 timing protocol](keygen_dot_timing.md).
- [x] Review/commit that support and execute EXP-006/RUN-0002; [ACT-0016 review](runs/EXP-006-RUN-0002.md) retains all regressions and mixed outcomes.
- [x] Select EXP-005 as primary, keep EXP-006 as a secondary research comparison and freeze the optimisation search. The current checkout remains EXP-006; test runners restore the exact EXP-005 source separately.

### 2. Complete the required implementation-security assessment

My supervisor asked me to determine a suitable way to evaluate security effects. I therefore need more than a statement that tests passed. The [assessment plan](implementation_security.md) combines existing range/compatibility/assembly evidence with dynamic secret-flow checking and focused statistical timing-leakage tests.

- [x] Pin dynamic-check tools, write the public/secret map and prepare [EXP-007](experiments/EXP-007-secret-flow.md): seven arithmetic path/operand-role cases plus IND-CPA decryption.
- [x] Exercise the full development matrix: 9 builds, 198 Memcheck processes, 18 detected marked positive controls, quiet target/defined/negative checks; 102 production bodies match accepted normal code.
- [x] Commit support, execute EXP-007/RUN-0001 and review all controls/diagnostics: accepted bounded secret-flow findings in ACT-0017; results still need their user commit.
- [x] Prepare/pin the EXP-008 custom dudect-style harness and reference, run sensitivity pilots and specify finite budgets/classes/seeds/thresholds/stopping rules.
- [ ] Review/commit ACT-0017 support and collect formal EXP-008/RUN-0001; assess every control and timing signal before drawing conclusions.
- [ ] Compare the original reference and selected implementation, investigate any new dependencies or timing signals, and record bounded conclusions and limitations.
- [ ] Complete the final security matrix, including the inherited canary tradeoff, code/local-stack changes and unassessed attack classes.

This is required practical work. It is not a formal whole-program proof or a new physical side-channel project. VTune is excluded from the plan at my request in ACT-0015. The security tests remain required. If the local setup is insensitive or unsupported, I need to diagnose that limitation and choose a workable test setup; I cannot label an unrun or inconclusive test as passed.

### 3. Confirm the final performance result directly

- [ ] Commit a final protocol comparing freshly built original reference, EXP-003 and EXP-005 using the same fixtures, compiler, flags and conditions.
- [ ] Repeat in fresh sessions with balanced execution order, recording variation rather than relying on five pairs from one session. My starting protocol proposal is three sessions with ten matched pairs per parameter per session, with fixed within-pair inputs and predeclared fixture seeds across sessions; exact settings and resource budget must be fixed before collection.
- [ ] Confirm small or adverse incremental effects when they affect final selection, especially EXP-005's Kyber768 keygen result and Kyber1024 control-operation changes. Rebuild the relevant preceding variant for a matched check rather than comparing old summary medians.
- [ ] Recheck final source/binary identity and the final correctness gates. Reuse earlier evidence only where exact source/build identities and unchanged caller contracts justify it; any final source change requires affected validation again.

The session or matched process pair is an experimental unit for the corresponding claim. Thousands of inner timings are not thousands of independent replications. I will predeclare analysis and uncertainty summaries, preserve all raw observations and explain environmental limits. More repeated measurements on one host do not establish portability or performance on other machines.

### 4. Produce the practical handover package

- [x] Generate the first [thesis figures/tables](thesis_figures.md): all EXP-006 pairs, incremental-result overview and observed reduction-count progression, with PNG/SVG/PDF exports and input/code hashes.
- [ ] Extend figures after statistical leakage and repeat-session results (EXP-007 coverage matrix now produced): direct original-reference timing/spread, code/local-stack tradeoffs and a bounded security-evidence matrix.
- [ ] Write the practical results/methods summary linking every claim to a source commit, run, protocol and analysis artifact, including unsuccessful/deferred ideas.
- [ ] Audit clean reproduction instructions and tool/build identities. Preserve original results and resolve stale links or unexplained findings.
- [ ] Mark practical work complete only once these outputs and bounded conclusions exist. Then write the thesis draft and present it with the repository to the supervisor for feedback, as planned.

## What does not need to expand automatically

I do not need to implement every possible reduction change, complete EXP-004, port to another hardware family, prove whole-program constant time, establish final ML-KEM certification or use VTune. I explicitly excluded VTune in ACT-0015. New work is justified if a finding prevents a defensible conclusion or supervisor feedback changes the scope. The optional full-text literature checks and bibliographic work also belong in thesis preparation; I must complete them before making claims that depend on those sources.

The immediate action is to commit the accepted EXP-007 results and ACT-0017 support, then run [EXP-008/RUN-0001](experiments/EXP-008-timing-leakage.md). No arithmetic edit or VTune setup is needed. I then diagnose any leakage findings, confirm direct/repeat-session performance for original/EXP-003/EXP-005, and assemble the thesis/reproduction package. The arithmetic search and dynamic-flow stage are complete; the statistical stage and final confirmation remain. This is the closing evaluation phase, not an open-ended search for more optimisations.
