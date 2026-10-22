# Practical completion checklist

## Where I am

I am near the end of the arithmetic optimisation trials, but the practical component is not complete. I have a reproducible original reference, working validation/count/timing machinery and four cumulatively evaluated optimisations. The final narrow candidate, EXP-006, is now applied and its correctness/count/scoped assembly review is accepted; its timing comparison remains before freezing the search. There is no requirement to invent more optimisations to fill an experiment count.

| Experiment | Simple description | State |
|---|---|---|
| EXP-000 | Establish the unchanged reference and measurement process | Initial preparation complete |
| EXP-001 | Combine products before reducing each small multiplication | Correctness and initial timings reviewed |
| EXP-002 | Extend that fusion across a whole vector dot product | Correctness and initial timings reviewed; local-canary tradeoff recorded |
| EXP-003 | Reduce less often during the inverse transform | Correctness and initial timings reviewed; targeted encap/decap gains |
| EXP-004 | Ask whether independently controlled optimisations interact when combined | Deferred; no implementation/run or failed result |
| EXP-005 | Delay centring the keygen error vector until its final addition | Correctness and initial timings reviewed; keygen gains and small other-operation regressions recorded |
| EXP-006 | Delay keygen dot-product centring before its existing scale conversion | Correctness/counts/scoped assembly accepted; timing pending |

The numbers are identifiers, not a required sequence of six successful optimisations. EXP-004 was reserved for a different interaction question. The retained implementations already build on one another, so repeating that same combination would not answer a new question. A distinct interaction study needs controlled separate variants/ablations. It is optional and does not block this project's completion.

The [EXP-005 timing review](runs/EXP-005-RUN-0002.md) finds median paired keygen time reductions of 5.18%, 0.48% and 1.36% against fresh EXP-003. Kyber1024 encap/decap medians are -0.12%/-0.50%; these tradeoffs remain visible. Single-session incremental percentages cannot be added or multiplied to claim a total gain over the original reference.

## What remains, in order

### 1. Finish the final candidate trial

- [x] Manually apply the three [EXP-006 edits](experiments/EXP-006-keygen-dot.md), review/commit source and support, and execute RUN-0001.
- [x] Review actual correctness, bounds, counts, assembly, local stack and hardening findings: [ACT-0015 acceptance](runs/EXP-006-RUN-0001.md).
- [x] Prepare and development-check the [fresh EXP-005/EXP-006 timing protocol](keygen_dot_timing.md).
- [ ] Review/commit that support and execute EXP-006/RUN-0002; review the result and retain slower/inconclusive outcomes.
- [ ] Select the candidate to carry forward and freeze the optimisation search. A negative EXP-006 result is a useful completed experiment; I can retain EXP-005 or another earlier variant.

### 2. Complete the required implementation-security assessment

My supervisor asked me to determine a suitable way to evaluate security effects. I therefore need more than a statement that tests passed. The [assessment plan](implementation_security.md) combines existing range/compatibility/assembly evidence with dynamic secret-flow checking and focused statistical timing-leakage tests.

- [ ] Pin tools and prepare the public/secret input map and focused harnesses.
- [ ] Establish sensitivity with positive/negative controls and commit the formal testing budget/protocol.
- [ ] Compare the original reference and selected implementation, investigate any new dependencies or timing signals, and record bounded conclusions and limitations.
- [ ] Complete the final security matrix, including the inherited canary tradeoff, code/local-stack changes and unassessed attack classes.

This is required practical work. It is not a formal whole-program proof or a new physical side-channel project. VTune is excluded from the plan at my request in ACT-0015. The security tests remain required. If the local setup is insensitive or unsupported, I need to diagnose that limitation and choose a workable test setup; I cannot label an unrun or inconclusive test as passed.

### 3. Confirm the final performance result directly

- [ ] Commit a final protocol comparing freshly built original reference with the selected frozen candidate using the same fixtures, compiler, flags and conditions.
- [ ] Repeat in fresh sessions with balanced execution order, recording variation rather than relying on five pairs from one session. My starting protocol proposal is three sessions with ten matched pairs per parameter per session, with fixed within-pair inputs and predeclared fixture seeds across sessions; exact settings and resource budget must be fixed before collection.
- [ ] Confirm small or adverse incremental effects when they affect final selection, especially EXP-005's Kyber768 keygen result and Kyber1024 control-operation changes. Rebuild the relevant preceding variant for a matched check rather than comparing old summary medians.
- [ ] Recheck final source/binary identity and the final correctness gates. Reuse earlier evidence only where exact source/build identities and unchanged caller contracts justify it; any final source change requires affected validation again.

The session or matched process pair is an experimental unit for the corresponding claim. Thousands of inner timings are not thousands of independent replications. I will predeclare analysis and uncertainty summaries, preserve all raw observations and explain environmental limits. More repeated measurements on one host do not establish portability or performance on other machines.

### 4. Produce the practical handover package

- [ ] Generate reproducible thesis tables/figures from retained data: per-operation timing, paired effects and repeat-session spread; reduction counts; code/local-stack and security findings.
- [ ] Write the practical results/methods summary linking every claim to a source commit, run, protocol and analysis artifact, including unsuccessful/deferred ideas.
- [ ] Audit clean reproduction instructions and tool/build identities. Preserve original results and resolve stale links or unexplained findings.
- [ ] Mark practical work complete only once these outputs and bounded conclusions exist. Then write the thesis draft and present it with the repository to the supervisor for feedback, as planned.

## What does not need to expand automatically

I do not need to implement every possible reduction change, complete EXP-004, port to another hardware family, prove whole-program constant time, establish final ML-KEM certification or use VTune. I explicitly excluded VTune in ACT-0015. New work is justified if a finding prevents a defensible conclusion or supervisor feedback changes the scope. The optional full-text literature checks and bibliographic work also belong in thesis preparation; I must complete them before making claims that depend on those sources.

The immediate action is to commit the new comparison support/records and execute EXP-006/RUN-0002 against a freshly restored EXP-005. The arithmetic is already applied and RUN-0001 is accepted; no further arithmetic edit is required. After the timing result, the work changes from finding optimisations to checking and explaining the selected result.
