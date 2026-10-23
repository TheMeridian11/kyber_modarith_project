# Research activity log

This log records the sequence of research decisions and findings. Detailed protocols, run reviews and machine-readable evidence are linked from each checkpoint. Development checks remain distinct from formal measurements; historical pending states are reported as historical, not current instructions. The numerical results and accepted scope are unchanged by the editorial revision.

## ACT-0001 — Research records and baseline source

The initial source review established the project structure, experiment/run identifiers, reduction map and literature record. It identified obsolete implementation paths, overly broad log-file ignore rules and a missing upstream submodule mapping. Earlier correctness-binary observations had no complete persistent run archive and were not treated as accepted baseline measurements.

## ACT-0002 — Setup identity and metadata design

Setup commit [c584c16d7b8a](source_revisions.md) established the corrected paths and pinned upstream mapping. The metadata collector was designed to retain defined environment/source fields and refuse reused run IDs. Syntax inspection at this checkpoint did not constitute runtime or benchmark evidence.

## ACT-0003 — Metadata checkpoint and validation support

EXP-000/RUN-0001 was accepted as a metadata-only checkpoint. The recorded overwrite attempt was refused without changing the existing metadata. Fifteen infrastructure tests covered dummy-process output, nonzero exits, launch failure, timeout, interruption, source changes and invalidated provenance. These support checks did not execute Kyber.

Records: [overwrite-check screenshot](evidence/ACT-0003/metadata-overwrite-check.png), [run review](runs/EXP-000-RUN-0001.md), [Captured support-test console output](evidence/ACT-0003/support-tests.log).

## ACT-0004 — Functional baseline and timing harness

EXP-000/RUN-0002 passed all three reference functional suites. Development checks of the timing harness compiled all parameters and retained 108 positive-duration rows with matching shared secrets. Invalid iterations, missing/duplicate rows, incorrect headers and failed round trips were rejected. Development timings were excluded from performance conclusions.

Records: [RUN-0002 review](runs/EXP-000-RUN-0002.md), [Development evidence](evidence/ACT-0004/harness-smoke.json).

## ACT-0005 — Timing pilot and reduction instrumentation

EXP-000/RUN-0003 contained 45000 valid timing rows and 45 reproduced summary rows; all measured exchanges passed. Process-median ranges were 0.56–1.94%, describing this pilot rather than a confidence interval. Separate reduction-counter development produced 18 observations matching the source-derived predictions. Summary-file line endings were corrected for subsequent outputs; the archived pilot remained unchanged.

Records: [run review](runs/EXP-000-RUN-0003.md), [verification record](evidence/ACT-0005/run-0003-review.json), [Development evidence](evidence/ACT-0005/counts-smoke.json).

## ACT-0006 — Baseline counts and fused-multiplication design

EXP-000/RUN-0004 confirmed all 90 baseline count observations. The first treatment combined products before Montgomery reduction, with explicit caller bounds, representation and narrowing arguments. Six support builds used unchanged reference arithmetic, an ordinary modular oracle and normal/UBSan transcript comparisons. Deliberately altered transcripts and baseline counts presented as candidate predictions were rejected; these checks preceded candidate validation.

Records: [RUN-0004 review](runs/EXP-000-RUN-0004.md), [verification evidence](evidence/ACT-0006/run-0004-review.json), [EXP-001 plan](experiments/EXP-001-fused-basemul.md), [Retained support evidence](evidence/ACT-0006/validation-support-smoke.json).

## ACT-0007 — Fused base multiplication validated

EXP-001/RUN-0001 passed all 42 steps, sampled deterministic and invalid-input transcript comparisons, kernel/output-bound checks, exercised UBSan and predicted reduction counts. The reviewed base-multiplication body used three Montgomery calls instead of five, shrank from 138 to 114 bytes and retained its local stack setup. Six development timing builds and two short blocks checked matched-pair analysis; they were not a formal speed result.

Records: [run review](runs/EXP-001-RUN-0001.md), [verification evidence](evidence/ACT-0007/run-0001-review.json), [Development evidence](evidence/ACT-0007/comparison-smoke.json).

## ACT-0008 — First timing results and vector-wide fusion

EXP-001/RUN-0002 reproduced 90000 durations, 90 process summaries, 45 paired effects and nine aggregates. Keygen/encap/decap reductions were 4.12%/5.87%/6.01% for Kyber512 and 7.43%/8.55%/8.43% for Kyber1024. Kyber768 keygen improved by 1.68%; its 0.87%/0.86% encap/decap effects remained inconclusive. A reported earlier attempt retained the old basemul body in a comment; source-guard behaviour supports a layout explanation, but the failed invocation log is unavailable. The accepted source remains [8345f6a0fb27](source_revisions.md). The next treatment extended accumulation across vector components.

Records: [run review](runs/EXP-001-RUN-0002.md), [verification evidence](evidence/ACT-0008/exp-001-run-0002-review.json), [EXP-002](experiments/EXP-002-wide-dot.md), [Development evidence](evidence/ACT-0008/dot-validation-support-smoke.json).

## ACT-0009 — Wide-dot validation and hardening tradeoff

EXP-002/RUN-0001 passed all 48 steps, sampled transcripts, vector-oracle cases, exercised UBSan and predicted counts. The changed dot product reduced local stack use but lost the compiler-generated local canary after the array was removed under unchanged flags. This is a recorded hardening tradeoff, not evidence that the change is harmless or exploitable. Six development builds checked the actual assembly and produced 432 valid short-run operation rows.

Records: [run review](runs/EXP-002-RUN-0001.md), [verification evidence](evidence/ACT-0009/exp-002-run-0001-review.json), [Development evidence](evidence/ACT-0009/incremental-comparison-smoke.json).

## ACT-0010 — Wide-dot timing result and inverse-transform design

All 45 EXP-002/RUN-0002 pairs favoured the wide-dot treatment over freshly rebuilt EXP-001. Median keygen/encap/decap reductions were 2.02%/6.07%/6.00%, 11.83%/13.46%/13.55% and 8.66%/8.09%/8.30% for Kyber512/768/1024. The inverse-transform treatment was then specified as a conditional cumulative change with a public reduction schedule and retained centred-input contract. EXP-004 was reserved for a distinct interaction study rather than duplicating an already cumulative combination.

Records: [run review](runs/EXP-002-RUN-0002.md), [verification evidence](evidence/ACT-0010/exp-002-run-0002-review.json), [EXP-003](experiments/EXP-003-staged-invntt.md), [Support evidence](evidence/ACT-0010/invntt-validation-support-smoke.json).

## ACT-0011 — Staged inverse transform validated

EXP-003/RUN-0001 passed all 54 steps, 47-vector inverse-transform oracles, sampled KEM transcripts, exercised UBSan, upstream suites and counts. Tested external bytes matched the original reference. The inverse body grew from 347 to 458 bytes while local stack fell from 104 to 72 bytes. The arithmetic oracle shared the transform layout and twiddle table, so it established sampled arithmetic equivalence rather than independent certification of the specification.

Records: [run review](runs/EXP-003-RUN-0001.md), [machine-readable evidence](evidence/ACT-0011/exp-003-run-0001-review.json), [Development evidence](evidence/ACT-0011/invntt-comparison-smoke.json).

## ACT-0012 — Inverse-transform timing result and error-vector design

EXP-003/RUN-0002 reproduced the full 90000-duration analysis. All 30 encap/decap pairs improved over EXP-002, with median reductions of 4.30–4.98%; keygen medians were −0.31%, −0.51% and +0.70%. The next treatment deferred reduction only for the keygen error vector, whose next consumer is an addition followed by the existing final public-key reduction. Secret-vector and inverse-input centring were retained. Development checks exercised existing arithmetic and did not establish results for the then-unapplied candidate.

Records: [run review](runs/EXP-003-RUN-0002.md), [verification evidence](evidence/ACT-0012/exp-003-run-0002-review.json), [EXP-005](experiments/EXP-005-error-ntt.md), [Development evidence](evidence/ACT-0012/error-ntt-validation-support-smoke.json).

## ACT-0013 — Keygen error-vector validation and code/stack costs

EXP-005/RUN-0001 passed all 60 steps, twelve normal/UBSan transcripts, upstream suites and 90 count observations. Keygen Barrett counts fell 2048→1536, 3072→2304 and 4096→3072; Montgomery and encap/decap counts were unchanged. Keygen code grew by 17/33/40 bytes and local stack by 16/16/0 bytes. Canary loads/checks, endbr64 and stack-page probes remained. Existing public-matrix rejection branches were distinguished from secret-dependent control flow; instruction presence did not establish runtime CET enforcement.

Records: [run review](runs/EXP-005-RUN-0001.md), [structured verification](evidence/ACT-0013/exp-005-run-0001-review.json), [Development evidence](evidence/ACT-0013/error-ntt-comparison-smoke.json).

## ACT-0014 — Error-vector timing result and final arithmetic proposal

EXP-005/RUN-0002 reproduced all 90000 durations and derived tables. All fifteen keygen pairs favoured the treatment, with median reductions of 5.18%, 0.48% and 1.36% relative to EXP-003. Kyber1024 encap/decap medians were −0.12%/−0.50%, retained as costs. The final arithmetic proposal deferred keygen-dot centring before its existing scale conversion. The remaining evaluation scope explicitly included dynamic secret-flow testing, a bounded statistical timing screen and direct repeat-session comparisons.

Records: [EXP-006 edits](experiments/EXP-006-keygen-dot.md), [run record](runs/EXP-005-RUN-0002.md), [structured audit](evidence/ACT-0014/exp-005-run-0002-review.json), [Support evidence](evidence/ACT-0014/keygen-dot-validation-support-smoke.json).

## ACT-0015 — Keygen-specific dot validated

EXP-006/RUN-0001 passed all 69 validation steps, sampled dot/addition/serialization checks, normal/UBSan transcripts, upstream suites and counts. Keygen Barrett counts fell to 1024/1536/2048 while other counts stayed unchanged. Keygen-plus-new-dot code grew by 266/364/405 bytes; keygen local-stack changes were 0/−16/0 bytes. Keygen protections remained, and the additional dot had the same no-local-canary pattern as the general dot. Six development timing builds matched all 33 reviewed bodies; a copied review-filename error was corrected before the completed support check.

Records: [run review](runs/EXP-006-RUN-0001.md), [structured evidence](evidence/ACT-0015/exp-006-run-0001-review.json), [Development evidence](evidence/ACT-0015/keygen-dot-comparison-smoke.json).

## ACT-0016 — Mixed timing result and arithmetic search closed

EXP-006/RUN-0002 showed keygen medians of −2.55%/+0.22%/+1.67% relative to EXP-005, with mostly slower control operations. The general-benefit hypothesis was not supported despite fewer reductions. EXP-005 was retained for closing evaluation and EXP-006 preserved as an adverse/parameter-specific comparison; no hybrid implementation was introduced. Reduction-count, incremental-effect and paired-effect figures were generated. Dynamic secret-flow support exercised sensitive controls and retained its development diagnostics separately from the later formal run.

Records: [full timing review](runs/EXP-006-RUN-0002.md), [machine-readable audit](evidence/ACT-0016/exp-006-run-0002-review.json), [EXP-007](experiments/EXP-007-secret-flow.md), [initial snapshot](evidence/ACT-0016/secret-flow-support-initial.json), [final development evidence](evidence/ACT-0016/secret-flow-support-smoke.json), [Figure review evidence](evidence/ACT-0016/figure-review.json).

## ACT-0017 — Dynamic secret-flow result and timing-screen design

EXP-007/RUN-0001 was accepted after checking 870 raw files, 198 reports and 129 assembly bodies. All 72 marked and 72 defined target processes were quiet; all 18 deliberate branch/address controls were detected. The nine marked negatives and 27 defined controls were quiet. Expected control exits of 99 remain nonzero in the raw record. Timing-screen pilots exposed outlier sensitivity and a stale calibration-based crop cutoff; these attempts were retained and the fixed analysis protocol was revised before formal collection. The dynamic result covers executed branch/address dependencies, not operand latency, full-KEM or physical leakage.

Records: [EXP-007/RUN-0001](runs/EXP-007-RUN-0001.md), [EXP-008's protocol](experiments/EXP-008-timing-leakage.md), [Support review](evidence/ACT-0017/timing-leakage-support-review.json), [correction evidence](evidence/ACT-0017/figure-review.json), [verification record](evidence/ACT-0017/final-verification.json).

## ACT-0018 — Statistical timing screen and closing-comparison protocol

EXP-008/RUN-0001 was accepted after checking its source/tool/build identities, 1026 raw files and 180 production/harness assembly bodies. All 1944 planned statistics reproduced; all 288 target processes stayed below the threshold, with maximum target |t| 2.91016 against 10. All 18 positive controls detected their intended effect and all 18 negatives were quiet. The three-session direct-comparison protocol was fixed before formal collection. A development report-writer type error was corrected without changing measurements or the retained archive. The original thesis questions were mapped to the completed methods and bounded claims.

Records: [EXP-008/RUN-0001](runs/EXP-008-RUN-0001.md), [Independent NumPy analysis](evidence/ACT-0018/exp-008-run-0001-review.json), [EXP-009](experiments/EXP-009-final-comparison.md), [development review](evidence/ACT-0018/final-comparison-support-review.json), [Source review](evidence/ACT-0018/thesis-draft-review.json), [Direct object inspection](evidence/ACT-0018/source-and-branch-review.json), [verification](evidence/ACT-0018/final-verification.json).

## ACT-0019 — First final-comparison session accepted

EXP-009/RUN-0001 was accepted as the first of three predeclared sessions: 225 completed steps, 450 raw files, nine warning-free builds, 108 matching production bodies and 324000 valid duration rows. Both cumulative candidates improved every original-reference pair. Additional EXP-005 keygen medians were 5.26%/0.49%/1.62%; Kyber1024 decapsulation was slower than EXP-003 in all twelve pairs. Final selection remained open at this checkpoint, and the two remaining sessions followed the unchanged protocol. The preliminary figure remains labelled session 1 of 3.

Records: [session 1](runs/EXP-009-RUN-0001.md), [reproducible audit](evidence/ACT-0019/exp-009-run-0001-review.json), [Figure review](evidence/ACT-0019/figure-review.json), [Final preservation and file checks](evidence/ACT-0019/final-verification.json).

## ACT-0020 — Three-session result and final selection

All three EXP-009 sessions were accepted. The audit covered 675 steps, 27 builds, 324 production-body extractions and 972000 duration rows, with all derived tables reproduced. The final estimator is the median of three session medians, not a pooled inner-sample statistic. Both candidates improved every original-reference pair. EXP-005 was selected for repeated additional keygen benefit of 5.26%/0.49%/1.52%, while Kyber1024 encap/decap costs of 0.15%/0.36%, code/local-stack growth and inherited hardening limits remained explicit. Final session, all-pairs and tradeoff figures and the security matrix were completed. All final analysis/audit/figure outputs reproduced byte-for-byte.

Records: [session 2](runs/EXP-009-RUN-0002.md), [session 3](runs/EXP-009-RUN-0003.md), [Verified object/branch evidence](evidence/ACT-0020/source-and-branch-review.json), [complete audit](evidence/ACT-0020/exp-009-three-session-review.json), [Reproduction review](evidence/ACT-0020/figure-review.json), [final verification](evidence/ACT-0020/final-verification.json).

## ACT-0021 — Closing-results archive and selected-source identity

Commit [66c707f9dc8c](source_revisions.md) archived the closing results and final analysis. All 4474 result files were tracked. The selected 35-file historical EXP-005 snapshot was verified; only indcpa.c, polyvec.c and polyvec.h differed from the then-current EXP-006 checkout. The prospective restoration was reviewed as 2 insertions and 41 deletions. This checkpoint described a planned restoration, not an executed source change.

Records: [Local object/source evidence](evidence/ACT-0021/source-and-handoff-review.json), [File-preservation verification](evidence/ACT-0021/final-verification.json).

## ACT-0022 — Selected source restored and verified

The actual working source matched all 35 EXP-005 hashes and verified historical blobs. The three-file diff exactly matched the reviewed restoration. It also matched EXP-005 source identities in both accepted security manifests and all three final comparison manifests. No new build, security test or benchmark was needed or claimed. The final source and documentation were subsequently committed at [b2bd620d3eac](source_revisions.md). The scientific programme and source review were complete.

Records: [Selected-source review](evidence/ACT-0022/selected-source-review.json), [Final preservation and commit-scope verification](evidence/ACT-0022/final-verification.json).

## ACT-0023 — Documentation consolidation

The documentation was revised to remove repeated Git instructions, conversational wording and obsolete next steps while retaining experimental rationale, numerical results, adverse findings, limitations and provenance. The 35 selected source files, all raw results, prior audit records, analysis code/data and figures were preserved. The three hash-pinned protocol documents retain their original bytes. Local main, the research branch and both tracking refs identify [b2bd620d3eac](source_revisions.md); the editorial changes do not rewrite experiment history. The editorial audit records changed documents and preservation/reproduction checks.

Records: [Editorial and preservation review](evidence/ACT-0023/documentation-review.json).

## ACT-0024 — Thesis-readiness and benchmark conditions review

The documentation received a final consistency review. Repeated full commit IDs were replaced by shorter linked references, with the complete identities retained in a source revision index. The benchmark conditions record now consolidates the nine performance runs' recorded environment and protocols, separates retrospective host/workload information from current observations, and identifies unrecorded controls. Selected source, raw results, existing audit evidence, scientific findings and the three frozen protocols were preserved. The completed practical evidence supports writing Methods, Results and Discussion; literature-dependent claims and the thesis argument still require completion.

Records: [Benchmark conditions](benchmark_conditions.md), [revision index](source_revisions.md), [documentation and preservation review](evidence/ACT-0024/documentation-and-conditions-review.json).
