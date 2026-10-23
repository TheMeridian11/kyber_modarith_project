# Project activity log

I append one entry for each substantive activity, using sequential identifiers. I distinguish completed actions from proposed instructions and record corrections explicitly. I link experiments and runs when available and retain failed or inconclusive outcomes.

## ACT-0001 — Research records and setup handoff

- **Completed:** I established the workflow, experiment register, baseline plan, templates and literature record, and documented corrected paths and reduction-map findings.
- **Pending at this stage:** Apply the supplied root .gitignore and .gitmodules edits, review the existing script correction and documentation, verify the setup and commit it. Implement per-run metadata collection and the benchmark harness.
- **Results:** No builds, correctness tests or benchmarks were executed during this activity. No new performance or security findings were established. The proposed configuration edits were not yet confirmed.
- **Learned:** The baseline script's directory correction was already present as an uncommitted change. Reproducibility and evidence capture still required preparation; the existing summary output was insufficient for the raw-data study.
- **Next:** Verify and commit the setup, then implement automatic metadata collection.

### Starting state observed

I record the inspected starting state as branch reduction-counters, project HEAD eefad7ec998fa529fa8fa11f91a0a00370a9a548 and upstream 3edd5af5991927164edd4aacebfcbee00b8064e7 with the official GitHub remote.

An existing uncommitted change corrected scripts/run_baseline.sh from impl/ to implementation/. The root .gitignore still used old paths and ignored all .log files. The .gitmodules mapping was missing despite the upstream gitlink. No files were found under analysis/ or results/.

### Historical context

The preliminary review reported identical reference source/build files across upstream, baseline and optimised copies, and passing existing correctness binaries for all parameter sets, including valid exchanges, invalid keys and corrupted ciphertexts. No saved performance results were reported.

I retain those observations as historical context. A persistent full raw run archive was not retained, so they do not establish the accepted EXP-000 baseline. Earlier reduction-count predictions remain hypotheses until implementation and measurement.

### Documentation verification

The recorded checks confirmed valid local Markdown links and unchanged SHA-256 fingerprints for 90 existing implementation, script and root-ignore files. Git diff inspection showed only the pre-existing script directory edit outside documentation. No compilation, runtime validation or benchmarking was performed. The configured project remote was https://github.com/TheMeridian11/kyber_modarith_project.git; no remote synchronisation was performed.

## ACT-0002 — Setup verification and metadata collector handoff

- **Completed:** I committed the setup and retained terminal evidence. Repository inspection confirmed commit c584c16d7b8a8e8de5e071a4edd5bc1450f92592, the upstream mapping and corrected ignore rules. I revised the research records to use sequential IDs and first-person project wording. The proposed metadata collector received an in-memory syntax check and design review.
- **Pending:** I still need to create scripts/collect_run_metadata.py from the supplied code, commit it with the revised records, run the metadata smoke check and verify that an existing run ID cannot be overwritten.
- **Results:** The working tree was clean before these documentation revisions. All 36 reference source/build files in each local implementation copy matched pinned upstream. No code was changed during this review, and no Kyber builds, tests or benchmarks were run. The proposed collector has not been installed or executed.
- **Learned:** Setup provenance is established. A metadata snapshot identifies the source and observable environment, but does not establish build provenance, correctness, arithmetic safety, timing behaviour or performance.
- **Next:** Complete the collector smoke check and retain its JSON, source commit, command output and separate results commit for review.

### Verified setup evidence

- Project branch: reduction-counters.
- Setup commit: c584c16d7b8a8e8de5e071a4edd5bc1450f92592.
- Committed upstream gitlink and checked-out upstream: 3edd5af5991927164edd4aacebfcbee00b8064e7.
- Upstream URL: https://github.com/pq-crystals/kyber.git.
- Root ignore paths match implementation/; research .log files are no longer globally ignored.
- The script's implementation/ directory correction is committed.
- Source equality was checked by file hashes; this does not substitute for runtime validation.

### Record-format amendment

I replaced work-date and timezone fields with sequential identifiers throughout the current research records and removed role-agreement wording. I retained the factual distinction between planned, reported and inspected evidence. Publication years and software version identifiers remain intact. Existing commits remain unchanged.

The legacy scripts/run_baseline.sh still generates calendar-based directory names. I will leave it unused while the sequential-ID launcher and raw-data harness are developed. Its summary output is not the formal baseline dataset.

### Collector scope and acceptance

The supplied proposal targets Python 3.12 on Ubuntu/WSL with GCC-compatible version queries. It records selected environment observations, full source/upstream commits, compiler and collector hashes, optional executable identity and manually reported conditions. It omits work timestamps and refuses an existing run directory.

I will commit the collector and revised documentation before the first snapshot. Changes outside results/ must be committed; prior result files may remain pending. Unknown controls remain unknown. The optional executable hash does not establish its build command or flags. All execution checks remain not-run for a metadata-only record.

The proposal was compiled in memory for syntax inspection only. I still need runtime evidence from the file I create in the repository. I will preserve an incomplete output directory if writing fails and use a new run ID after correcting the problem.

### Verification of the revised records

The documentation-only diff passed Git whitespace checks and local Markdown link checks. A read-only review found the setup, proposal and execution status consistent across all ten records. Before/after SHA-256 fingerprints matched for 91 implementation, script and configuration files. The collector file was still absent from the repository. These checks validate this documentation update and do not establish collector runtime behaviour.

## ACT-0003 — Metadata checkpoint accepted and functional runner prepared

- **Completed:** I verified the committed metadata snapshot and overwrite-refusal evidence, revised the working method, and prepared the recorded functional-validation runner with infrastructure tests and usage notes.
- **Results:** The saved metadata and collector hashes match their committed files. All 15 infrastructure tests passed using dummy processes and mocked workflows. No Kyber arithmetic files were changed, and the new runner has not executed Kyber.
- **Pending:** I need to review and commit the support files, then launch EXP-000/RUN-0002 and inspect its manifest and raw logs.
- **Learned:** The metadata checkpoint establishes source identity and observed environment. Functional compatibility, arithmetic safety and performance still require their own evidence.
- **Next:** Record fresh baseline functional tests for all three parameter sets before developing the raw timing harness.

### Verified metadata checkpoint

The source commit is 7eea4121e19896cc21773c81530ea5201bb235f3. Its direct child, results commit d2a50d7d6f610f28e4e8f5dcb10c09ed46e93750, adds only results/EXP-000/RUN-0001/metadata.json. Read-only inspection of stored Git objects and current files confirmed the relationship and hashes without executing Git commands.

- Collector SHA-256: 0270459b5c508bfbdd1ce0d9cef59860e8fade7333a0145a9c5d8a5136c5e7e7.
- Metadata SHA-256: edb4d4d38012efc4f33f890d4afe12c9662deca8caf26431111124c29a828c3e.
- Upstream revision remains 3edd5af5991927164edd4aacebfcbee00b8064e7.
- Supplied terminal evidence shows the duplicate ID was refused with exit code 2 and an unchanged metadata hash. I preserved the [overwrite-check screenshot](evidence/ACT-0003/metadata-overwrite-check.png).
- The metadata records the i9-12900KS, 24 visible logical CPUs, Ubuntu under WSL2, GCC 13.3.0 and Python 3.12.3. Host power settings, background load and physical-core placement remain unknown.

The snapshot is accepted as metadata-only. It contains no completed Kyber tests or performance observations. See the [run review](runs/EXP-000-RUN-0001.md).

### Support implementation and validation

I prepared scripts/run_validation.py to reserve a new run through the existing collector, require the baseline to match upstream, build fresh functional-test binaries with explicit flags, and retain commands, environment, stdout/stderr, exit codes and file hashes. It handles nonzero exits, timeouts and ordinary interruption without marking incomplete tests as successful. The source, compiler and executables are rechecked before accepting completion.

The runner reads 35 C/header/Makefile files and confirms their contents match the pinned reference. The earlier 36-file inventory also included the reference .gitignore. The original collector and RUN-0001 metadata remain unchanged. The root ignore rules now exclude only rebuildable run/build/ contents in addition to existing exclusions; raw logs and manifests remain trackable.

The support tests in tests/test_run_validation.py use temporary dummy processes and mocked build/test orchestration. They check output preservation, nonzero exits, launch failure, timeout, interruption, changed/missing source, all parameter sets, stop-on-failure, invalidated provenance and setup failure. The final check returned exit code 0 with 15 passing tests. This does not substitute for running the real compiler and Kyber tests through the new runner.

- Tested runner SHA-256: e54636a2335400d35c7103f2e6a5669e4fda88794136d5ac94b6b5a2d1a61071.
- Tested infrastructure-test SHA-256: f11170421ab569708df61f0da8b0d2c59e002ee17d567e1b620c90826087005b.
- [Captured support-test console output](evidence/ACT-0003/support-tests.log).

These checks were development validation of uncommitted support files identified by the hashes above. I will commit them before creating a formal Kyber run. I retain manual application of arithmetic optimisations and all Git operations; supporting automation and records are reviewed before inclusion.

Final read-only verification checked links and work-record formatting across 12 Markdown files, confirmed the collector and saved metadata hashes remain unchanged, and confirmed both implementation copies still match all 36 upstream reference source/configuration files. The support-script hashes match the versions that passed the infrastructure tests. No Git commands or new Kyber executions were performed during this activity.

## ACT-0004 — Functional baseline accepted and raw timing harness prepared

- **Completed:** I verified RUN-0002 and prepared the C raw timing harness, Python runner and measurement protocol.
- **Results:** All three reference functional tests passed. The archived logs and hashes matched. Short harness checks produced 108 valid timing rows with matching shared secrets across all parameter sets; invalid inputs and malformed CSVs were rejected.
- **Pending:** I need to commit the harness and launch the first recorded timing pilot, EXP-000/RUN-0003.
- **Learned:** The sampled functional baseline is established. The timing harness measures reproducible KEM computation in nanoseconds with randomness generation excluded; no optimisation speedup has been measured.
- **Next:** Collect and inspect the raw baseline timing data, then proceed to reduction-count instrumentation.

### Accepted functional evidence

Source commit 75b0e38b5436dfa3f2672822edb178087b542b43 produced RUN-0002. Results commit e1d3734be7d890e0697678a8ae336e0a8a210f92 directly follows it. The manifest is completed with all six steps exiting 0, all three functional checks passing and provenance recheck passing.

I verified 12 raw-log hashes, three retained executable hashes, metadata and source-file hashes, and runner/collector identity. The existing test completed 1000 iterations of each of three cases for every parameter set, totalling 9000 case executions. No new functional rerun was needed. See [RUN-0002 review](runs/EXP-000-RUN-0002.md).

### Timing implementation and checks

I prepared benchmarks/bench_kem.c for per-operation CLOCK_MONOTONIC_RAW durations, reproducible SHAKE256 fixtures passed to the existing deterministic APIs, warm-up, buffered CSV output and exchange checks outside measured intervals. I prepared scripts/run_timing.py to reuse the existing collector and run-record helpers, pin one logical CPU, build fresh binaries, preserve every measurement and generate per-process summaries. All Kyber arithmetic sources remain unchanged.

- Tested C harness SHA-256: 103feedada227af4a170b561a05a5268d31845e3ddbe758553ba5f7f3a11dc3a.
- Tested timing runner SHA-256: 7101f8978bbf2591bf802f26a7b0b6f63127460561fcfa952b923361d77cf500.
- [Development evidence](evidence/ACT-0004/harness-smoke.json): three successful real compilations, 108 retained operation rows, all round trips matching and all durations positive. Zero iterations was rejected by each binary; missing rows, failed round trips, duplicate iteration labels and incorrect headers were rejected by CSV validation.

These development checks exercised the real C harness and CSV parser. The committed full timing orchestration remains pending RUN-0003. Development durations are retained for traceability and are not thesis performance results.

The pilot protocol is five fresh processes per parameter set, 100 warm-up exchanges and 1000 measured exchanges per process. I expect 45000 raw rows and 45 summary rows. I will retain all observations without outlier removal and assess variation before interpreting later optimisation effects. See the [protocol](raw_timing.md).

Final read-only checks confirmed that both 36-file reference copies, the accepted RUN-0002 manifest, the original collector and the functional runner remain unchanged. The new harness files match their tested hashes, local documentation links resolve and RUN-0003 has not been created. No Git commands were executed during this activity.

## ACT-0005 — Timing baseline accepted and reduction counters prepared

- **Completed:** I verified RUN-0003 directly, updated the baseline progress records, prepared separate reduction-counting support and corrected future CSV summary line endings.
- **Results:** All 45000 timing rows and 45 summary rows validated; all measured exchanges passed. The process-median ranges were 0.56% to 1.94%. Three counter builds and 18 development observations passed, matching all source-derived reduction predictions.
- **Pending:** I need to review and commit the support changes, then execute and preserve EXP-000/RUN-0004.
- **Learned:** Five batches of 1000 exchanges per parameter set are a practical pilot. These are repeated automated observations, not 45000 independent experiments. Reduction-call counts explain arithmetic work but do not establish a speedup.
- **Next:** Accept the recorded count baseline, then begin EXP-001 with range analysis and the isolated fused-base-multiplication change.

### Accepted timing evidence

Source commit d690cfb580f0dd2d1b0805a6635ed56e553ca5f9 produced RUN-0003; its direct child 8a76f3f1c0bf9da8157b0901b2defbf8f3f618d2 records the results. I checked the relationship through stored Git objects without executing Git commands.

All 18 steps exited 0. I checked 36 raw-log hashes, 15 dataset hashes, three executable hashes, four support-file hashes, metadata, summary and the recorded source files. I reproduced all per-process summary values from the raw CSVs. The [run review](runs/EXP-000-RUN-0003.md) and [verification record](evidence/ACT-0005/run-0003-review.json) preserve the findings and scope.

Median-of-process-median durations in microseconds were:

| Parameter set | Keygen | Encap | Decap |
|---|---:|---:|---:|
| Kyber512 | 18.6885 | 21.2705 | 27.8050 |
| Kyber768 | 32.5920 | 34.7770 | 43.0455 |
| Kyber1024 | 49.5855 | 55.0405 | 64.8405 |

I retained the pilot without outlier removal. Its 45000 intervals total approximately 1.80 seconds of measured duration. This excludes other harness work and does not make the observations independent. WSL host controls remain a limitation. Fresh matched baseline/candidate runs will support the optimisation comparisons; small uncertain effects may require additional complete comparison blocks.

### Support changes and checks

I added benchmarks/count_reductions.c and scripts/run_counts.py. GNU linker wrappers count external calls to the original reduction functions in a separate build with LTO disabled. The wrappers reset before each KEM operation, preserve original function arguments/results and do not alter either implementation copy. The first recorded count run will use ten exchanges per parameter set, producing 90 raw rows and nine summary rows.

The [counter protocol](reduction_counts.md) records the instrumentation boundary and acceptance rules. [Development evidence](evidence/ACT-0005/counts-smoke.json) retains three clean builds, two exchanges per parameter set, successful wrapper self-checks, matching shared secrets and agreement with every predicted count. The executable rejected zero iterations; CSV validation rejected a missing row, a failed exchange and an incorrect count. These checks cover the harness and parser; committed full-run orchestration remains pending RUN-0004.

- Counter C SHA-256: adc3efa6f3bf543d5383a4f0611b23b2b0065e517d34b01b4ddc7c046fd17c2a.
- Counter runner SHA-256: 67da80bc1de61c618443e175b56f92778f2cfc2762c03385fc8769553e85ea17.
- Updated timing runner SHA-256: 690af59011de1794be5f59097135581bd5ea624aca82fc171bf7ed8f4e6306f6.

The Git whitespace warnings arose from CRLF in the saved derived CSV. I preserved RUN-0003 byte-for-byte and changed only the future summary writer to specify LF. A direct check of the updated writer confirmed LF output and identical parsed values. The timing C harness remains unchanged, and I did not repeat the timing pilot.

No arithmetic optimisation or Git operation was performed during this activity. Functional agreement, arithmetic safety, timing behaviour and performance remain separate evidence categories. RUN-0004 is the last planned baseline measurement before EXP-001; candidate-specific validation proceeds with the optimisation.

Final verification confirmed that both 36-file implementation copies and every tracked file in RUN-0001, RUN-0002 and RUN-0003 remain unchanged. The timing runner differs only in its summary writer's line terminator, tested support hashes still match, and local documentation links and whitespace checks pass. RUN-0004 has not been created.

## ACT-0006 — Baseline counts accepted and first optimisation specified

- **Completed:** I verified RUN-0004, closed initial baseline preparation, recorded the EXP-001 algebra/range argument and implementation-security assessment, and prepared candidate-validation support.
- **Results:** All 90 baseline count observations and nine summary rows validated. All predictions and exchanges agreed. Six support-check builds using unchanged reference arithmetic passed the kernel oracle and normal/UBSan transcript comparisons.
- **Pending:** I need to apply the supplied basemul replacement manually, review and commit the source/support/records, and execute EXP-001/RUN-0001.
- **Learned:** Reduction fusion must preserve Montgomery scaling and cover deserialised coefficients up to 4095. The proposed int32_t sums remain within the existing reducer's input bounds. Internal representatives may differ by q while final encoded results must remain identical.
- **Next:** Review candidate correctness, exercised-path sanitizer results, counts and generated code before collecting fresh matched timings.

### Accepted baseline record

The count source commit is 3757df58a02408fb9a701869cc1f3ac6f6159a8d; results commit 2a8388c1701dcf66cb5dfa6906921f63bc574c55 directly follows it. Stored Git objects confirmed the relationship without executing Git commands.

I verified all six steps, 12 raw-log hashes, three executable hashes, metadata, source/support identity and summary. All 90 rows reproduced the nine summary entries and matched the prior source predictions. No timing was collected. See the [RUN-0004 review](runs/EXP-000-RUN-0004.md) and [verification evidence](evidence/ACT-0006/run-0004-review.json).

EXP-000 is closed as initial baseline preparation. Sampled correctness, the timing pilot and count evidence remain subject to their recorded scope; closure does not establish complete security or final ML-KEM conformance.

### Proposed arithmetic and security assessment

I propose changing only basemul in the experimental ntt.c. I retain M(a1*b1), combine the remaining products in two int32_t accumulators, and reduce each output once. Predicted calls change from five to three per coefficient pair; Barrett counts remain unchanged. The [EXP-001 plan](experiments/EXP-001-fused-basemul.md) records full KEM count predictions, source-derived algebra and downstream compatibility.

The reviewed conservative input envelope is |a| <= 4095, |b| <= 1664 and |zeta| <= 1664. The largest fused sum is bounded by 13628160, within the reducer's documented input interval and int32_t. Each output has magnitude at most 3328, so up to four products accumulate within 13312 before the unchanged final Barrett reduction.

I explicitly record risks from wrong Montgomery scale, overflow/narrowing, changed representatives, invalid-input/rejection behaviour and secret-dependent execution. The proposal introduces fixed scalar arithmetic with fixed indices; candidate generated-code review and leakage assessment remain outstanding. The existing GCC-specific signed conversions/shifts remain an implementation assumption. Passing tests or observing fewer calls will not be recorded as a blanket security pass.

### Support implementation and checks

I added tests/test_fused_basemul.c and scripts/run_candidate_validation.py. The support compares normal and UBSan builds of both variants, checks a test-only modular oracle and output bounds, compares public deterministic KEM transcripts byte for byte including invalid-input cases, runs the candidate's existing functional suite, checks candidate counts and retains disassembly.

I extended run_counts.py helpers with optional source-directory and prediction arguments. Default baseline parsing still accepts the saved RUN-0004 data; presenting those baseline observations as candidate predictions is rejected.

Development checks used unchanged reference arithmetic only, with two KEM fixtures and 3200 small kernel cases per executable. All six builds passed, normal and UBSan transcripts were identical, no sanitizer diagnostics appeared, and a deliberately altered transcript was rejected. The runner also rejects a missing arithmetic change before reserving a run. [Retained support evidence](evidence/ACT-0006/validation-support-smoke.json) identifies the exact files and commands.

- Validation runner SHA-256: 7b7fc5d0c779303bd3d8bb2898b052e7ca5ab9f3afd6cf26f2867808ab135939.
- Validation C SHA-256: 2aad45e50a26bf54a3241570aba173f2d238836ba17b5fd267ccb57910b8752b.
- Extended counting runner SHA-256: 8f41dc934e7d21b071b67ffd3b529b181ffcfe9fc26bcfde21bdc6838d42710d.

The proposed arithmetic itself has not been written into the repository or tested. Full recorded candidate validation remains pending manual application. No optimisation speedup, complete safety proof or constant-time guarantee is claimed.

Final read-only verification confirmed that both 36-file reference copies and every archived result remain unchanged. The support files match their tested hashes, documentation links and whitespace checks pass, and the candidate-count table agrees with the source-derived savings formulas. EXP-001/RUN-0001 has not been created. No Git commands were executed during this activity.

## ACT-0007 — First optimisation validated and matched timings prepared

- **Completed:** I verified EXP-001/RUN-0001, reviewed normal-build basemul and its Montgomery reducer for both variants and all parameter sets, recorded the results and security scope, and prepared matched timing support.
- **Results:** All 42 saved steps passed. Twelve transcripts agree within parameter sets, all exercised kernel/oracle/output-bound and UBSan checks pass, and all 90 count observations match predictions. Reviewed basemul uses three reducer calls instead of five, shrinks from 138 to 114 bytes and retains the same local stack setup. The new comparison support passed a short six-build, two-block development check.
- **Learned:** The candidate reduces complete-operation Montgomery calls by approximately 15.4% to 23.1% while preserving the tested external outputs. This establishes the arithmetic mechanism, not a speedup. The generated code introduces no branch/index-based leakage mechanism in the inspected functions; complete constant-time security remains unestablished.
- **Pending:** I need to review and commit the comparison support and records, then execute and preserve EXP-001/RUN-0002. No formal baseline/candidate timing comparison has run.
- **Next:** Compare fresh matched process medians, check consistency across pairs and execution orders, and interpret any benefit, regression or uncertainty alongside the correctness/security evidence.

### Accepted execution and provenance

The actual validation source is 8345f6a0fb273917ed4499356f0966d1c5dc7fc2. It follows b935e1566567fd91335c4dee8e5a0dd4b611af47 from the screenshots. Results commit 00398d18dddbccb99854bb6519fc896a23d90f22 directly follows the actual source. I confirmed these relationships and all 264 tracked file contents through stored objects without executing Git commands.

I checked all 84 raw-stream hashes, 18 retained executable hashes, six support-file hashes, metadata and committed/current source contents. The baseline matches upstream; only candidate basemul differs. The [run review](runs/EXP-001-RUN-0001.md) and [verification evidence](evidence/ACT-0007/run-0001-review.json) record the checks, transcript sizes and counts.

Each parameter set produced four identical transcripts containing 100 public deterministic fixtures, including tested invalid-input and rejection behaviour. Each of twelve test binaries passed 3200 kernel-oracle/output-bound checks; six used UBSan without diagnostics. The repeated builds exercise common fixtures, not thousands of independently designed experiments. The candidate also passed the upstream functional suites. I reviewed saved evidence without rerunning this validation.

### Analysis and implementation-security scope

The observed savings match the source-derived predictions for keygen, encapsulation and decapsulation, with Barrett counts unchanged. Removing two of five local reducer calls does not remove the five product multiplications or other KEM work. Runtime improvement therefore remains an empirical question.

All six normal basemul disassemblies show the intended 32-bit accumulators, fixed-offset accesses and direct calls. The unchanged reducer has register arithmetic and a fixed shift. Neither reviewed body contains a conditional branch, division or indirect call. Both basemul versions save four registers and reserve eight additional stack bytes. The smaller 114-byte candidate symbol is a local code-size finding; it is not a whole-binary or peak-stack measurement.

The caller bounds still give at most 13628160 for a fused sum and 13312 for four accumulated outputs. Existing signed-narrowing/compiler assumptions remain. Sampled byte agreement and exercised-path sanitizer results support the bounded argument, while all-input safety, whole-program constant-time behaviour, statistical leakage, power/EM leakage and fault resistance are not established by this run. I record those limitations separately from the decision to proceed to timing.

I left RUN-0001 unchanged, including its original assembly_review=pending entry. The new review records the later completion of that action without rewriting historical evidence.

### Timing support and checks

I added scripts/run_comparison.py, reusing the existing C timing harness, CSV validation, metadata collector and process-record helpers. It builds both implementations with the reviewed compiler/flags, verifies their basemul/reducer instruction sequences against the review, and executes five adjacent pairs per parameter set in alternating order. It records all raw durations and produces process summaries, paired effects and nine descriptive aggregate rows using LF CSVs.

The initial budget remains 100 warm-up and 1000 measured exchanges per process. Two implementations yield 30 processes and 90000 operation durations. This is the expected doubling of the pilot volume, not a new requirement for 90000 independent tests. The same public fixture indices are reused. I interpret matched process pairs and observed variation rather than treating inner rows as independent runs. The [protocol](paired_timing.md) records formulas, the three-versus-two order imbalance, WSL limitations and rules for inconclusive results.

[Development evidence](evidence/ACT-0007/comparison-smoke.json) records six real compilations, twelve assembly matches and two short blocks yielding 432 valid operation rows. Known synthetic improvement and regression pairs verified effect direction and median-of-paired-effects aggregation. Missing variants, duplicate groups, unequal sample counts and changed candidate source hashes were rejected. Git-state checks were mocked for this temporary development check and the metadata collector was not invoked; formal clean-source execution remains pending.

- Comparison runner SHA-256: a492a1f5efe5292049f46d544b64092b4faf0b15a9459faa5e5d47fad1ce8378.
- Unchanged timing C SHA-256: 103feedada227af4a170b561a05a5268d31845e3ddbe758553ba5f7f3a11dc3a.
- Review evidence SHA-256: fafed1a5cb1f1cbe67e72f27bac453b64e3608adca905551f0c61c990c94bae9.

I made no arithmetic or Git changes during this activity. No development duration is used as evidence of a speedup.

Final verification confirmed that all 155 archived result files, the arithmetic implementation files, pinned upstream sources and Git HEAD remain unchanged. The tested support hashes still match, documentation links and whitespace checks pass, and EXP-001/RUN-0002 has not been created. The changes comprise one new runner, two evidence records, two explanatory records and four updated project documents.

## ACT-0008 — First timing result analysed and vector-wide fusion specified

- **Completed:** I verified EXP-001/RUN-0002 from saved artifacts, interpreted the timing effects and execution-order checks, recorded the source-commit clarification, and prepared the EXP-002 range/security plan, exact manual replacement and validation support.
- **Results:** All 90000 timing rows, 90 process summaries, 45 paired effects and nine aggregate rows verified. EXP-001 improved Kyber512 by 4.12%/5.87%/6.01% and Kyber1024 by 7.43%/8.55%/8.43% for keygen/encap/decap. Kyber768 keygen improved by 1.68%; its 0.87%/0.86% encap/decap effects remain inconclusive. Twelve support-check builds of the existing implementations passed the new vector oracle and transcript comparisons.
- **Learned:** RUN-0001 validated the first optimisation; RUN-0002 measured its performance. Reduction savings do help several operations here, but their timing effect differs by parameter set. Repeated observations are not independent experiments, and small mixed effects need qualified conclusions.
- **Pending:** I need to apply the EXP-002 function and includes manually, review/commit source and support, then execute EXP-002/RUN-0001. The new candidate has not been implemented or tested.
- **Next:** Review the new vector arithmetic, invalid-input compatibility, UBSan, counts and assembly before a fresh incremental timing comparison against EXP-001.

### Verified timing record and interpretation

The source commit is d407b5134f14a96a4572b3af1132a8f715e0a28d; results commit 337e4ba6ff1fc8783c47ea7c34dc2ee52c1e8712 directly follows it. I verified the relationship through stored objects without executing Git commands. All 370 tracked files matched the results commit before these support/document changes.

All 48 steps exited zero. I verified 96 raw-stream hashes, 30 datasets, six retained executables, source/support identity, metadata and derived artifacts. All twelve timing-build function disassemblies match the accepted review. I re-parsed every raw observation and reproduced the complete analysis with the existing versioned summary/comparison functions. See the [run review](runs/EXP-001-RUN-0002.md) and [verification evidence](evidence/ACT-0008/exp-001-run-0002-review.json).

Every Kyber512/Kyber1024 pair improved, including both orders. Kyber768 keygen improved in all five pairs but by a smaller amount. Kyber768 encap/decap each regressed in block 5; I retained those observations and classify the small median effects as inconclusive. Order-group medians are positive, but the three-versus-two order split and single-session WSL conditions limit inference. No significance, independent-row or cross-machine claim is made. Host power mode, background load and physical-core placement remain unknown.

The counts and code review explain which arithmetic work was removed; they do not isolate why Kyber768's timing gain is smaller. Possible code-layout/compiler/environment effects remain hypotheses, not findings. I keep EXP-001 as a research reference and proceed without an unnecessary repeat merely to make every comparison favourable. Any stronger claim about the small effects requires further planned evidence. Performance results add no security proof.

### Earlier source-commit clarification

I reported that my first attempt left the old basemul in a comment; replacing the complete function allowed the next attempt to pass. The inspected source guard would reject that changed prefix before allocating a run. This supports a source-layout explanation rather than an observed arithmetic-test failure; the failed invocation log is not available for independent verification. The accepted validation still identifies 8345f6a0fb273917ed4499356f0966d1c5dc7fc2, after b935e1566567fd91335c4dee8e5a0dd4b611af47. I preserve both commits and the successful evidence.

### Next optimisation and security argument

[EXP-002](experiments/EXP-002-wide-dot.md) extends reduction fusion across the K vector components. For each coefficient pair I propose accumulating S00, S11 and S01 in int32_t, then computing M(M(S11)*zeta + S00) and M(S01). I retain final poly_reduce and the accepted ntt.c. The KEM vector path will compute directly, so the original and first-optimisation savings must not be added as independent treatments.

For |a| <= 4095, |b| <= 1664, |zeta| <= 1664 and K <= 4, S00/S11 are bounded by 27256320, S01 by 54512640 and the twiddle-containing sum by 32794112. All fit int32_t and the existing Montgomery input contract. The output narrows only after reduction and remains centred after poly_reduce. The preserved inner Montgomery reduction is necessary for the correct scale.

Predicted dot-product calls fall from EXP-001's 384K to 384, compared with the original reference's 640K. Proposed full-operation counts are 4864/6400/9728 for Kyber512, 7296/8832/13056 for Kyber768, and 9728/11264/16384 for Kyber1024. Barrett counts should remain unchanged. These predictions have not been measured.

The source introduces only public-index loops and a public parity branch, with fixed coefficient bounds and no new heap allocation. Actual generated code, stack allocation and candidate compatibility remain pending. Invalid-input/rejection behaviour, signed narrowing, overflow and any new timing/indexing mechanism are explicit gates. Statistical leakage, full constant-time security, power/EM and fault resistance remain unestablished or unassessed.

### Support implementation and development checks

I added tests/test_fused_dot.c and scripts/run_dot_validation.py. The test driver reuses the established public KEM fixtures and binary transcript format while checking 41+K whole vectors against an independent int64_t oracle. It covers aligned and cancelling sign corners, zero, each isolated component and deterministic interior inputs across all 128 coefficient pairs. It does not repeat the unchanged standalone basemul test. The runner checks both normal/UBSan variants, 100 KEM fixtures, the existing candidate functional suite, ten count fixtures and retained dot-product/reducer assembly.

[Development evidence](evidence/ACT-0008/dot-validation-support-smoke.json) records twelve builds using only the original baseline and accepted EXP-001 implementation, with two KEM fixtures each. All vector oracles and four-way transcript comparisons passed without compiler/sanitizer diagnostics. The source preflight rejects the unapplied change before run allocation; the count parser rejects EXP-001 observations against EXP-002 predictions. These are support checks, not results for the proposed arithmetic. No full formal validation or timing was repeated.

- EXP-002 validation runner SHA-256: 723c00730bb8afa778e6cb651995cb9bbcf55fd9f161024e3bac437f51f45c6d.
- Vector test driver SHA-256: 03f2c33a595ee4e0a70a2f641759758dfc0f0096464c9727f69deada2b6930ab.

I made no arithmetic or Git changes during this activity. Existing result records are preserved, and the exact optimisation code is supplied for manual application.

Final verification confirmed that all 256 archived result files, every arithmetic source, the pinned upstream files and Git HEAD remain unchanged. Tested support hashes match, proposed count formulas and bounds agree, documentation links and whitespace checks pass, and EXP-002/RUN-0001 has not been created. The pending change set contains the two new support files, two new research records, two evidence records and five updated project documents.

## ACT-0009 — Vector-wide fusion validated and incremental timings prepared

- **Completed:** I verified EXP-002/RUN-0001, reviewed its normal-build dot-product/reducer assembly and the retained EXP-001 control, recorded correctness/security and code/stack findings, and prepared a fresh paired timing runner.
- **Results:** All 48 steps, 96 raw-stream hashes, 18 executable hashes and seven support-file identities verified. Twelve transcripts agree within parameter sets, vector oracles and exercised-path UBSan checks pass, and all 90 count observations match predictions. Six development builds matched the reviewed assembly and produced 432 valid operation rows in two short blocks.
- **Learned:** EXP-002 reduces each dot product from EXP-001's 384K Montgomery calls to 384. Its local stack setup is smaller, its function body is larger, and the compiler emits no local stack-canary check in the new function. These are observed implementation tradeoffs, not a measured speedup or complete security guarantee.
- **Pending:** I need to review/commit the new comparison support and records, then execute and preserve EXP-002/RUN-0002. EXP-002 has no formal performance result yet.
- **Next:** Compare fresh EXP-001 and EXP-002 process pairs, inspect effect size/variation and both execution orders, then decide whether the incremental change helps under these conditions.

### Accepted evidence and analysis

The validation source is 61279b2b2373c7594e40f06712bc9f93b734b8ed; results commit b943e50b9fee417ae21bffb4822b2aa6f3309a83 directly follows it. All 474 tracked files initially matched the results commit. I verified those identities through stored objects without running Git commands. Current sources/support also match the committed build inputs. Only polyvec.c differs from accepted EXP-001; ntt.c and the pinned baseline are preserved.

The [run review](runs/EXP-002-RUN-0001.md) and [verification evidence](evidence/ACT-0009/exp-002-run-0001-review.json) record exact hashes, transcripts, counts and reviewed instructions. Four transcripts per parameter agree, with 100 deterministic fixtures per build including tested invalid-input/rejection behaviour. Every build passes 43/44/45 whole-vector oracle cases across 128 coefficient pairs; these common cases repeat across variants/build modes, rather than representing independent input designs. Six UBSan builds have no sanitizer diagnostics. The three candidate upstream functional suites pass. I did not repeat the full saved validation.

Observed keygen/encap/decap Montgomery calls are 4864/6400/9728 for Kyber512, 7296/8832/13056 for Kyber768 and 9728/11264/16384 for Kyber1024. Barrett calls are unchanged. The new assembly unrolls the K-component loop and executes three reductions for each of 128 coefficient pairs. Its four static reducer-call sites include alternative first calls for odd/even paths; they are not four dynamic calls per pair. This confirms the mechanism without predicting a timing percentage.

### Implementation security and resource tradeoffs

The reviewed branches test public pair termination and parity. Coefficient/output addresses, component offsets and zeta selection follow public indices. Products and accumulators remain 32-bit, consistent with the maximum 54512640 cross sum and 32794112 twiddle-containing sum. The unchanged 22-byte Montgomery reducer and final poly_reduce preserve the required scale and centred outputs. No new secret-dependent branch/index, division or indirect call was identified in the inspected bodies. Existing compiler assumptions and caller bounds remain conditions of this conclusion.

The dot-product symbols grow from 132/173/155 to 285/355/413 bytes. Explicit stack reservations fall from 528/536/528 to 24 bytes; including saved registers, local stack setup falls from 552/568/568 to 72 bytes. Entry return addresses and callee stack use are excluded; I make no whole-binary or peak-stack claim.

The generated EXP-001 function has stack-canary checks; the new EXP-002 function does not after removal of its local array, with compiler flags unchanged. This changes local corruption-detection coverage and is documented as a hardening tradeoff. No flag was disabled, and the fixed-index bounds/exercised checks do not become an all-input memory-safety or security proof. Any runtime change includes code layout, loop/memory changes and this compiler-generated difference as well as reduction savings. Whole-program constant-time security, statistical leakage, power/EM leakage and fault resistance remain unestablished or unassessed.

### Incremental timing support and preservation

I added scripts/run_incremental_comparison.py, reusing the established C harness, build/record helpers, strict CSV parser and paired-effect calculation. When I invoke it, read-only git show restores the accepted EXP-001 sources from d407b5134f14a96a4572b3af1132a8f715e0a28d into the new run's ignored build directory, with every file hash verified. It rebuilds both variants and compares their dot-product/reducer instructions with this review before measurement. It does not check out or modify the current arithmetic. Explicit exp001_/exp002_ analysis columns prevent ambiguity about the control.

The [incremental protocol](incremental_timing.md) retains five pairs per parameter, 100 warm-ups and 1000 measured exchanges per process, alternating order and fixed logical-CPU affinity. That is 30 processes and 90000 operation durations, the same budget as EXP-001's comparison. Old measurements are context, not the fresh control. Repeated rows are not independent experiments. I will preserve regressions/inconclusive effects and will not repeat the run merely to obtain a preferred outcome.

[Development evidence](evidence/ACT-0009/incremental-comparison-smoke.json) records six real builds, twelve assembly matches, twelve short processes and 432 valid operation rows. Hash/source guards, changed assembly, comparison labels/direction and missing/duplicate/unequal groups were checked. Git-state/existence operations were mocked, historical bytes came from verified stored objects, and the read-only Git invocation was tested with a mocked subprocess. No Git commands or metadata collector ran. These short durations are excluded from performance conclusions.

The 33 whitespace warnings in six saved assembly logs are objdump byte-continuation formatting. I preserved them and the original manifest's execution-time assembly_review=pending field; this later review resolves the pending action. New disassembly uses --insn-width=16 and the development outputs have no trailing whitespace. No arithmetic files or archived results were changed.

- Incremental runner SHA-256: 0f82a43e55aa3b6b1d15aa88c31707d63da6a3547d108161cbda5dfa996c84d7.
- Review evidence SHA-256: 532c6144783764d11b7c429325d8e964d19072f9be82a03c7cdf4b9d92d563ad.

Final verification confirmed that all 354 archived result files, all arithmetic/upstream sources and Git HEAD remain unchanged. The tested support/review hashes still match, documentation links and whitespace checks pass, and EXP-002/RUN-0002 has not been created. This activity changes four existing project documents and adds one runner, two evidence records and two explanatory records.

## ACT-0010 — Incremental timing benefit verified and inverse-NTT schedule specified

- **Completed:** I verified EXP-002/RUN-0002, reproduced its entire timing analysis, documented provenance/conditions/order checks and thesis limitations, retained EXP-002, and prepared the EXP-003 bounds/security plan, exact manual replacement and validation support.
- **Results:** All 90000 raw durations, 90 process summaries, 45 paired effects and nine aggregates verify. All 45 pairs favoured EXP-002 over fresh EXP-001. Median keygen/encap/decap time reductions are 2.02%/6.07%/6.00% for Kyber512, 11.83%/13.46%/13.55% for Kyber768 and 8.66%/8.09%/8.30% for Kyber1024. Twelve support-check builds of existing implementations pass the new inverse-transform oracle and short KEM transcripts.
- **Learned:** Vector-wide fusion provides further observed benefit in this session, but reduction-call savings alone do not isolate the timing mechanism. The next proposed change can remove six of seven inverse-NTT Barrett stages while keeping a conservative maximum sum/difference of 26624 under the preserved centred-input contract.
- **Pending:** I need to manually replace invntt, review/commit the new support and records, then execute EXP-003/RUN-0001. The new arithmetic has not been applied or executed; its correctness/counts/assembly/performance remain not-run.
- **Next:** Review the new candidate's saved validation and assembly before a fresh EXP-002/EXP-003 timing comparison. Key generation has no predicted arithmetic benefit from this inverse-transform change.

### Verified timing result and thesis record

The run source is a32a81d12225e00a8b3e0baeb32734f44cf78ab3; results commit 5a09a01496fae8dd4b908934c2e5524f5d3ecc9f directly follows it. The control was freshly restored from EXP-001 source d407b5134f14a96a4572b3af1132a8f715e0a28d. All 580 tracked files matched the results commit at review. I checked stored objects without executing Git commands.

The [run review](runs/EXP-002-RUN-0002.md) and [verification evidence](evidence/ACT-0010/exp-002-run-0002-review.json) preserve source/result/control identities, hashes, absolute durations, all observed pair ranges, order-group medians, compiler/flags, protocol and interpretation. All 48 saved steps exited zero; 96 raw-stream hashes, six binaries, source/support identities and all twelve reviewed assembly matches verify. Every raw row and roundtrip passes; the versioned analysis code reproduces the saved derived CSVs byte for byte. The 35 restored control-source files match their accepted identities. I did not repeat any benchmark or full validation during this review.

All nine parameter/operation groups have five positive pairs and positive medians in both order groups. Kyber512 keygen is the smallest effect: median 2.02%, range 1.39% to 3.64%. Its order-group medians differ, as do other small groups; the three-versus-two split cannot establish absence of ordering/time-drift effects. Kyber768 has the largest incremental reductions. I retain all observations, including higher first-block absolute durations, without exclusion or a retry intended to improve the result.

These results support retaining EXP-002 within the measured conditions: GCC 13.3.0 normal builds, i9-12900KS reported by Ubuntu/WSL2, guest logical CPU 0, five fresh pairs per parameter, 100 warm-ups and 1000 measured exchanges per process. Host OS details, background load, power mode and physical-core placement remain unknown. Reused fixtures and a shared session mean the 90000 rows are not independent experiments. No confidence interval, formal significance or cross-machine guarantee is claimed.

The known mechanism is fewer Montgomery calls per dot product, with unchanged Barrett counts; loop/memory/code-layout and local stack-canary coverage also change. Their separate timing contributions are not identified. The inherited range/compatibility/security limitations remain; speed does not establish constant-time behaviour or memory safety. I do not add or multiply separately measured median effects to claim total gain over the original baseline. A direct final-selected-variant versus original-reference comparison is needed for that later thesis claim.

### Next treatment and scope decision

[EXP-003](experiments/EXP-003-staged-invntt.md) will add a fixed inverse-NTT Barrett schedule on top of retained EXP-002. It is a conditional incremental treatment, not an independent main effect on the original reference. This avoids an automatic redundant combination step; EXP-004 remains available only if a separate interaction/combination question warrants it.

I propose keeping sum reduction only at public stage length 16. The seven stages each have 128 butterflies, giving 128 Barrett calls instead of 896. All 1152 Montgomery calls per inverse transform remain. Keygen has no inverse transforms; encap has K+1, and decap has K+2 including re-encryption. Predicted full-operation Barrett counts are 2048/2432/3584, 3072/3328/4736 and 4096/4224/5888 for keygen/encap/decap in Kyber512/768/1024. Montgomery counts remain those accepted for EXP-002. These predictions are not measurements or runtime percentages.

The caller analysis preserves final poly_reduce after the vector dot product, including malformed/noncanonical input paths already covered by EXP-002. Thus inverse inputs remain centred within 1664. The proposed stage output bounds are 3328, 6656, 13312, 3328, 6656, 13312 and 26624. Every sum/difference fits int16_t; twiddle products are at most 44302336 and final scaling at most 38365184, within int32_t and the Montgomery input contract. Final outputs remain bounded by 3328. Existing noise/message additions and decryption subtraction remain within 3330/4995/6656 before their retained reductions.

The new branch depends only on stage length; secret values do not choose reduction timing or addresses. Actual generated code, local stack, hardening behaviour and timing effects remain pending. The precondition is not valid for arbitrary int16_t inputs or changed callers. Explicit narrowing bounds remain necessary: passing UBSan alone does not establish them. I checked the relevant official GCC documentation and added LIT-005 with its limited review scope. Whole-program constant-time, statistical leakage, power/EM and fault-resistance claims remain unestablished or unassessed.

### Focused support checks

I added tests/test_staged_invntt.c and scripts/run_invntt_validation.py. Each build checks 47 vectors across all 256 coefficients against ordinary modular arithmetic with no reducer calls in the oracle. Dense extremes, index-bit sign patterns, sparse boundary positions and deterministic interiors target the changed arithmetic. The established KEM fixture/rejection transcript is reused; unchanged standalone basemul/dot-product oracle suites are not repeated. The formal runner adds normal/UBSan builds, 100 KEM fixtures, existing upstream functional suites, ten count fixtures and invntt/Montgomery/Barrett assembly; no timings.

[Support evidence](evidence/ACT-0010/invntt-validation-support-smoke.json) records twelve real builds using only the existing baseline and accepted EXP-002, with two KEM fixtures each. Every oracle/transcript check passes without compiler or sanitizer diagnostics. The unapplied-change guard rejects the current source before run allocation; EXP-002 count observations are rejected against EXP-003 predictions. The interval induction and count formulas were checked separately. I did not apply the proposed arithmetic, including to temporary source copies, and did not run Git or the metadata collector.

- Inverse-NTT validation runner SHA-256: c2ef075fe1f4d8b803b09b1f775e56faa7938e83e88dc44a28bfe36f0a51f795.
- Inverse-NTT test driver SHA-256: 5974f6b83f8c0e178d2e20f31ca96746a48657e90d0b33af7f38ff5ed997bec5.

Final verification confirmed that all 455 archived result files, the arithmetic and pinned upstream source files, prior support/evidence and Git HEAD remain unchanged. Tested support hashes match, the proposed snippet changes only the intended sum-reduction schedule, documentation links/whitespace checks pass, and no EXP-003 run directory exists. This activity adds two support files, two research records and two evidence records, and updates seven existing project documents.

## ACT-0011 — Inverse-NTT validation accepted and incremental timings prepared

- **Completed:** I verified EXP-003/RUN-0001, reviewed actual inverse-transform/reducer assembly against retained EXP-002 binaries, documented correctness/range/security findings, and prepared the fresh EXP-002 versus EXP-003 timing runner and protocol.
- **Results:** All 54 saved steps, 108 raw hashes, eighteen executable hashes and seven support-file hashes verify. Twelve builds pass 47-vector inverse-transform oracles and 100-fixture KEM transcripts; all tested external bytes match the original reference. Six UBSan builds have no diagnostics, three upstream suites pass and all 90 count observations match predictions. The timing support check passes six real builds and eighteen assembly comparisons.
- **Learned:** Keeping Barrett reduction at length 16 removes 768 of 896 calls per inverse transform with Montgomery counts unchanged, under centred inputs and the 26624 sum/difference bound. Generated inverse code grows 347 -> 458 bytes while local stack use falls 104 -> 72 bytes including saved registers, excluding return address/callees. No inverse-function canary is removed; the inherited EXP-002 dot-product tradeoff remains relevant.
- **Pending:** EXP-003 performance and final retention are unmeasured. Whole-program constant-time proof, statistical leakage, other-target behaviour and broader implementation-security guarantees remain unestablished or unassessed. I still need to review/commit the new support and records, then execute the formal timing run.
- **Next:** Run EXP-003/RUN-0002 through scripts/run_invntt_comparison.py with guest logical CPU 0, then review every pair, both order groups and reproduced derived results. Keygen has no predicted arithmetic benefit and is retained as a useful comparison control.

### Evidence identity and saved checks

Source commit 9ec22141e6acc98812438544be0bec5b35d00b5c produced RUN-0001; results commit 705f21f7f07dcd4162052aacda3adbcc54c4051a directly follows it. The manifest SHA-256 is 70a9d98f92494ffa5ead0804565797060f3349f35d167cb68607ca66f2cb4615 and metadata SHA-256 is 21a6e595b26d3f1f0754b514d89446b7992cd081f3b7b9626eebf5b3192af89a. All 696 tracked files matched the results commit before this activity's changes. I read verified stored objects without executing Git commands.

The [run review](runs/EXP-003-RUN-0001.md) and [machine-readable evidence](evidence/ACT-0011/exp-003-run-0001-review.json) retain the source/result/control identities, hashes, transcript sizes, counts, normalised assembly, symbol-table size checks and scoped findings. Only invntt differs from EXP-002, and it exactly matches the recorded replacement. The rest of ntt.c, polyvec.c and all other arithmetic files remain unchanged; the original baseline still matches pinned upstream.

Each parameter's four normal/UBSan transcripts agree byte for byte at 416000/595200/806400 bytes, including valid exchanges, malformed/noncanonical key inputs and corrupted/random-ciphertext rejection outputs. Each of twelve builds passes 47 inverse vectors and 12032 coefficient comparisons. The ordinary modular oracle calls neither reducer but shares the transform layout and twiddle table; this is arithmetic-equivalence evidence, not an independent certification of the complete specification. The same fixtures repeat across builds, and targeted samples do not exhaust all inputs. Each candidate passes the existing 1000-valid/1000-replaced-secret-key/1000-corrupted-ciphertext upstream suite. I did not repeat full validation during this review.

### Confirmed reduction mechanism and safety scope

For Kyber512/768/1024, observed Barrett keygen/encap/decap counts are 2048/2432/3584, 3072/3328/4736 and 4096/4224/5888. Montgomery counts remain 4864/6400/9728, 7296/8832/13056 and 9728/11264/16384. All 90 instrumented observations agree. The fixed schedule gives 128 Barrett calls instead of 896 per inverse transform, with all 1152 Montgomery calls retained. Keygen has no inverse transform; encap has K+1 and decap K+2, including re-encryption. Counts establish the mechanism but do not quantify runtime improvement.

The preserved final poly_reduce in the vector dot product supplies centred inputs bounded by 1664. The stage output bounds remain 3328/6656/13312/3328/6656/13312/26624. All sum/difference narrowing is representable; products are bounded by 44302336 for twiddles and 38365184 for final scaling, within int32_t and the Montgomery input contract. Final outputs stay within 3328; existing encryption/decryption additions/subtractions stay within 3330/4995/6656 before retained reductions. Montgomery scaling and final factor 1441 are unchanged. Internal representatives can differ modulo q while tested KEM bytes remain identical.

These bounds depend on the current caller envelope. Removing input reductions, changing the reset stage or supplying arbitrary int16_t arrays invalidates this acceptance until reassessed. UBSan passing is supplementary and does not alone certify narrowing. Existing implementation-defined signed conversion/shift assumptions remain tied to the inspected GCC/x86-64 environment.

### Generated code and security interpretation

I extracted invntt and both reducers from the saved normal binaries and retained EXP-002 timing binaries after verifying hashes. All reviewed functions match the symbol-table byte extents; parameter variants have the same normalised instruction sequences after namespace substitution. GCC 13.3.0 separates the length-16 and general butterfly bodies using a public stage test. Remaining branches use public loop counters/endpoints, and memory/table addresses use public indices and fixed offsets. No coefficient-dependent branch/address, division or indirect call was identified in these bodies.

One static Barrett site executes 128 times. Three static Montgomery sites cover general butterflies, length-16 butterflies and final scaling, totalling the unchanged 1152 dynamic calls. Both reducers are instruction-identical to EXP-002: Montgomery 22 bytes and Barrett 36 bytes. Static call-site counts are not dynamic operation counts.

Inverse body size increases by 111 bytes; explicit stack reservation falls 56 -> 24 bytes while six saved registers still use 48 bytes. Local stack totals fall 104 -> 72 bytes, excluding the entry return address and callees. This is neither whole-binary size nor peak-stack measurement. The split loops, register/spill changes and layout may affect timing alongside reduction savings. Neither inverse version has a local stack-canary check; endbr64 remains. The previously recorded EXP-002 dot-product canary change remains inherited, with no protection flag disabled.

I accept these bounded findings for research timing. They do not establish whole-program constant-time security, statistical leakage resistance, power/EM or fault resistance, absence of all memory errors, portability to untested compilers/targets, production readiness or final ML-KEM conformance. Ordinary speed measurements cannot fill those gaps.

### Timing support and preservation

I added scripts/run_invntt_comparison.py and the [next-run protocol](invntt_timing.md). When I invoke it, read-only git show restores all 35 accepted EXP-002 source files from a32a81d12225e00a8b3e0baeb32734f44cf78ab3 into the new run's ignored build/exp002-source directory, with each hash verified. The current candidate must match accepted EXP-003 validation. Both are freshly built with identical reviewed compiler/normal flags, and all eighteen inverse/reducer function bodies must match the review before any timing. The new orchestration commit and historical control/validation commits are recorded separately.

The fixed formal budget remains five pairs per parameter, 100 warm-ups and 1000 measured exchanges per process, seed 1 and logical CPU 0. EXP-002 runs first in odd blocks and EXP-003 first in even blocks. Thirty processes provide 90000 operation durations, 90 process summaries, 45 paired effects and nine aggregates. Primary effects use medians of paired ratios/reductions; ranges describe observed pairs rather than confidence intervals. Reused fixtures and a shared session limit independence. Unknown manual conditions remain unknown, and guest affinity does not establish physical-core placement.

[Development evidence](evidence/ACT-0011/invntt-comparison-smoke.json) records six real builds, eighteen assembly matches and two short blocks of twelve measured exchanges, with 432 valid rows. Synthetic positive/negative effects verify direction, experiment labels and paired aggregation; source/hash/assembly/group-integrity guards pass. Git state/existence checks were mocked, source bytes came from verified stored objects, and the git show argv was checked through a mocked subprocess. No Git commands or metadata collector ran. Development durations are excluded from performance conclusions; no formal EXP-003/RUN-0002 was allocated.

I will retain all negative and inconclusive timing findings and examine unexpected keygen movement rather than crediting it to removed inverse-transform calls. I will not retry to obtain a preferred result or combine medians from separate runs into a claimed total gain over the original reference. A later direct final-variant comparison is needed for that claim.

- Comparison runner SHA-256: 39424762798f7f6563df1447591cc71c89a6511ab45142d71daf7ed366d48e28.
- Validation/assembly review SHA-256: b37952601e09e6eff2564132e77b977aadf4debe262a0a8ea37bc85e9125504e.
- Development evidence SHA-256: 70ccf423f334d590fa7583f4ea0da2368657a84a11f245061ba4857727492f7a.

The archived manifest retains its original assembly_review=pending field; this later review records completion separately. Raw logs and hashes are preserved, and new full-width assembly has no trailing whitespace. No cryptographic arithmetic or historical support/evidence was edited in this activity.

Final verification confirms that all 565 archived result files, arithmetic/upstream sources, earlier support/evidence and Git HEAD remain unchanged. The tested runner/review/support hashes still match; documentation links, whitespace and the independent interval/count checks pass. EXP-003/RUN-0002 does not exist yet. This activity updates five existing documents and adds one runner, two explanatory records and two evidence records.

## ACT-0012 — Inverse-NTT timing benefit verified and error-vector reduction specified

- **Completed:** I verified EXP-003/RUN-0002, reproduced the complete paired analysis, checked actual timing-build assembly and unchanged keygen entry points, documented the results/security interpretation, retained EXP-003, and prepared EXP-005 bounds, exact manual call-site edit and validation support.
- **Results:** All 90000 raw durations, 90 process summaries, 45 paired effects and nine aggregates verify. All 30 encap/decap pairs improve over fresh EXP-002. Median keygen/encap/decap reductions are -0.31%/+4.69%/+4.64% for Kyber512, -0.51%/+4.98%/+4.90% for Kyber768 and +0.70%/+4.30%/+4.63% for Kyber1024. Negative values mean slower. Twelve support builds of existing implementations pass the new error-vector oracle/addition/serialization checks and short KEM transcripts.
- **Learned:** The inverse schedule provides the targeted encap/decap benefit in this session, with small keygen tradeoffs that cannot be attributed to saved inverse calls. The next local-source argument allows keygen's error-vector reduction to be deferred while keeping conservative raw-transform/addition bounds of 23299/26627 and preserving all other caller contracts.
- **Pending:** I need to manually apply the EXP-005 edit, review/commit source/support/records and execute EXP-005/RUN-0001. Proposed candidate correctness, counts, assembly and speed are not-run. Whole-program constant-time security, statistical leakage, broader side-channel/fault behaviour and other-target guarantees remain unestablished or unassessed.
- **Next:** Review the saved EXP-005 validation/assembly before a fresh EXP-003/EXP-005 timing comparison. EXP-004 remains deferred for the previously reserved interaction/combination question; I allocate a new ID rather than repurpose it.

### Timing identity, analysis and retention

The timing/support source is cf8ae0dd700bb41628c158016a7c15926a0b790f; results commit 23b4736206a8f79d13fb4898d474eb327e1dab3c directly follows it. Fresh control files came from accepted EXP-002 source a32a81d12225e00a8b3e0baeb32734f44cf78ab3; the current candidate matches EXP-003 validation source 9ec22141e6acc98812438544be0bec5b35d00b5c. Manifest SHA-256 is ce1d1514a6d61039572c4dd3cd6d8005bf36f938d1968b2db1e5e60defec2b72 and metadata SHA-256 is 46fece92a55cf7d0cab096100452ee611b303750ea18c047c63b11122e4002b4. All 814 tracked files matched the results commit before this activity. I read verified stored objects without executing Git commands.

The [run review](runs/EXP-003-RUN-0002.md) and [verification evidence](evidence/ACT-0012/exp-003-run-0002-review.json) retain absolute medians, all pair ranges, order-group medians, raw extrema, timer diagnostics, source/tool/support identities, assembly comparisons and keygen follow-up. All 54 steps exited zero. I verified 108 raw-stream hashes, six binaries, fifteen support-file hashes and committed bytes, all 35 restored control files and current source identities. The strict parser and independent median/min/max calculations agree. Recomputed CSV files match all three saved derived files byte for byte. Every measured roundtrip passes, and all eighteen inverse/reducer function bodies match the accepted assembly review and fresh disassembly of the retained binaries. I repeated no benchmark or full validation.

Encap/decap medians improve by 4.30–4.98%, with all 30 pairs positive and positive medians in both execution-order groups. Their smallest individual effect is Kyber768 decap block 4 at +3.684%. The five-pair keygen medians are -0.3124%, -0.5132% and +0.7039%. Kyber512 has four negative and one positive pair; Kyber768 all five negative; Kyber1024 all five positive. These small regressions/gains remain part of the result, not excluded noise or arithmetic savings credited to the inverse change.

Keygen calls no inverse transform and has unchanged source-level counts. A focused disassembly comparison shows unchanged normalised keypair_derand and indcpa_keypair_derand instructions and entry locations for each parameter. This does not establish that every reachable instruction/address is unchanged or identify the cause of timing movement. Layout elsewhere in the binaries and environment/measurement variability remain possible contributors; no causal separation was performed.

The protocol is five adjacent pairs per parameter, 100 warm-up and 1000 measured exchanges per process, seed 1, guest logical CPU 0, parameter order 512/768/1024 and EXP-002 first in odd blocks. The order groups have three versus two pairs and different medians; this does not demonstrate order independence. Kyber768 candidate block 4 has higher medians across all operations and smaller encap/decap benefits; it and all raw extremes are retained. No overhead subtraction, outlier exclusion or rerun to obtain a preferred result occurred. All timer diagnostics report 1 ns resolution and 11–12 ns minimum empty-pair probes; resolution is not a proof of measurement accuracy.

Recorded conditions remain GCC 13.3.0 normal -O3 builds, i9-12900KS as reported by Ubuntu 24.04.2/WSL2, x86_64, 24 visible logical CPUs and kernel 5.15.167.4-microsoft-standard-WSL2. Host details, power mode, background load and physical-core placement remain unknown. Timing excludes operating-system randomness through deterministic APIs; generation/check/output costs remain outside each interval. Repeated fixtures and one shared session mean 90000 inner durations are not independent experimental units. Five matched pairs do not establish formal significance, confidence intervals or a cross-platform guarantee.

I close the initial EXP-003 evaluation as supported for its targeted encap/decap benefit and keep it as the next research reference with the observed keygen tradeoffs. I do not combine medians from separate incremental runs into a claimed total original-reference gain. A later direct comparison of the selected final variant against the original reference remains necessary for that thesis claim.

### Security and mechanism interpretation

The validated centred-input contract remains intact: inverse inputs bounded by 1664, sum/difference bound 26624, product/reducer bounds and scale unchanged, and normal/UBSan KEM transcripts matching the original reference including tested invalid-input behaviour. The timing source hashes and actual reviewed functions match that accepted evidence. No new leakage test or whole-program proof was performed.

The known mechanism is 896 -> 128 Barrett calls per inverse transform with all 1152 Montgomery calls retained. The inverse body also grows 347 -> 458 bytes, local stack use falls 104 -> 72 bytes including saved registers (excluding return address/callees), and the compiler splits public-stage loop bodies. The run measures these changes jointly; it does not isolate the time cost of the removed reductions. The reviewed inverse/reducer branches and addresses remain public. Neither inverse version has a local canary, and EXP-003 removes none there; the earlier EXP-002 dot-product canary change remains inherited.

I preserve limitations for constant-time/security, memory safety, signed narrowing/shift portability, power/EM leakage and fault resistance. Passing sampled checks and a favourable speed result do not establish production approval, final ML-KEM conformance or safety under changed caller ranges. These distinctions are retained in the experiment record and thesis-facing run review.

### Next candidate and arithmetic argument

I allocate [EXP-005](experiments/EXP-005-error-ntt.md) to the previously optional error-vector pilot. Only the polyvec_ntt(&e) call inside indcpa_keypair_derand is replaced by a public K-iteration loop calling ntt on each error polynomial. The skpv transform/reduction, all encryption/decryption reductions, the wide-dot final poly_reduce and EXP-003 inverse schedule remain unchanged. ntt.h is already included and the existing loop variable i is reused. The exact proposed source hash is recorded, but no arithmetic implementation was edited.

Every sampled error coefficient is bounded by ETA1, which is 3 for Kyber512 and 2 for Kyber768/1024. This follows from cbd2/cbd3 sums-of-bits differences for all PRF outputs, not a probabilistic typical-case assumption. The unchanged forward NTT has seven stages, and the Montgomery output envelope 3328 gives a stage bound B -> B+3328. Under ETA1=3 the output bounds are 3331/6659/9987/13315/16643/19971/23299. The largest twiddle product is 19971*1664 = 33231744, within int32_t and the Montgomery input contract. Every butterfly result fits int16_t.

After the transform, raw e is bounded by 23299/23298. The other operand pkpv has passed through unchanged poly_tomont and is bounded by 3328, so the addition is at most 26627/26626 before the existing final polyvec_reduce. That reduction restores the same unique centred residues for serialization. e is not used as a multiplication input, inverse input or serialized secret key. The skpv reduction remains, and no Montgomery operation or representation factor is removed. This establishes the conditional modular/bounds argument; the actual manual edit still needs whole-KEM validation.

Predicted keygen Barrett counts fall 2048 -> 1536, 3072 -> 2304 and 4096 -> 3072, saving K*256 calls (512/768/1024). All Montgomery and encap/decap Barrett counts remain those accepted for EXP-003. A quarter of keygen Barrett calls is not a quarter of keygen time. The expected target is keygen; encap/decap become useful operations without a predicted direct arithmetic benefit.

The scope must remain this one consumer path. Global removal of poly_ntt's reduction, altered noise bounds, new consumers or use of raw e in the wide dot product would invalidate the argument. The preserved wide-dot exit reduction continues to establish EXP-003's centred inverse input. The new loop uses public K and fixed indices, with no data-dependent reduction choice or new allocation, but actual generated keygen/NTT/reducer code, stack/canary behaviour and all broader security limits must still be reviewed. Larger representatives can also change stored bit patterns; public control flow alone does not assess power/EM or fault behaviour.

### Support checks and next recorded execution

I added tests/test_error_ntt.c and scripts/run_error_ntt_validation.py. The test covers 47 bounded error polynomials against ordinary modular forward arithmetic, raw/centred residues and bounds, four subsequent addition patterns, retained reduction and exact serialization. Per build it performs 12032 forward coefficient checks, 48128 addition/reduction checks and 188 serialization comparisons. It shares the twiddle table/layout but calls no reducer in the oracle; it is not exhaustive specification validation. The established deterministic KEM transcript is reused.

[Development evidence](evidence/ACT-0012/error-ntt-validation-support-smoke.json) records twelve real normal/UBSan builds using only the original reference and existing EXP-003, two KEM fixtures per build. All targeted checks, transcript comparisons and diagnostics pass. The unapplied candidate is rejected before run allocation, changed preserved source is rejected, and old counts are rejected against the new keygen predictions. The conservative induction and count formulas were checked separately. No temporary candidate implementation, Git command, metadata collector or formal EXP-005 run was executed. These support checks do not establish the unapplied candidate's KEM correctness or speed.

After manual application and a clean source/support commit, EXP-005/RUN-0001 will collect normal/UBSan builds, 100 KEM fixtures per build, upstream suites, ten count fixtures per parameter and four function bodies from each normal build. This totals 60 steps and no timings. The earlier unchanged standalone arithmetic oracles are not repeated. I will review this new evidence before accepting a later comparison against freshly rebuilt EXP-003.

- Timing review SHA-256: 87b17e423dad4e1a7043c6d484894da4851916cc0453cdad220af0f885b6809e.
- Error-NTT validation runner SHA-256: 18ed7694210b1cac0443ffbe15ff4d9edc4f59276b1d75d89ef4a48e756b55d6.
- Error-NTT test SHA-256: 7fae4a09b1ca651af149a48665c3e6cde717c5103f2d6f7647f44f5a0170b9e2.
- Development support evidence SHA-256: 61ca3b8004d14619b90450b958200f0f17e0b4533aea59bea8492ef5af4612eb.

Final verification confirms that all 678 archived result files, arithmetic/upstream sources, prior support/evidence and Git HEAD remain unchanged. Tested support hashes match; the manual snippet produces the intended proposed hash in memory only, the range table agrees with the independent induction, and documentation links/whitespace/syntax checks pass. No EXP-005 run directory exists. This activity updates seven existing documents and adds two support files, two research records and two evidence records.

## ACT-0013 — Error-vector correctness and assembly accepted; incremental timing prepared

- **Completed:** I verified EXP-005/RUN-0001 against saved raw data, binaries, tools and committed source; reviewed keygen/forward-NTT/reducer assembly against EXP-003; documented correctness, arithmetic, memory and security findings; clarified the deferred EXP-004 question; and prepared the fresh timing comparison.
- **Results:** All sixty steps, twelve deterministic validation transcripts, six exercised UBSan builds, three upstream suites and ninety count observations pass. Keygen Barrett counts fall 2048->1536, 3072->2304 and 4096->3072; all Montgomery and encap/decap counts remain unchanged. Keygen canaries remain, code grows by 17/33/40 bytes, and local stack changes by +16/+16/0 bytes. Six development builds, 24 assembly matches and twelve short processes pass the new comparison pipeline.
- **Learned:** Only the keygen error vector can defer this reduction under the reviewed consumer/range argument. I verified the actual manual edit and its implementation, including preserved skpv/inverse-input reductions. Fewer calls are established; a speed benefit is not yet established. The whole Kyber1024 keygen body also contains existing public-matrix rejection branches, so the scoped assembly result is not a claim of branchless whole-program execution.
- **Pending:** I need to review/commit the new support and records, then execute EXP-005/RUN-0002. Keygen speed, other-operation tradeoffs and performance retention remain pending. Whole-program constant-time proof, statistical leakage, broader side-channel/fault behaviour, other-target portability and complete memory safety remain unestablished or unassessed.
- **Next:** Compare fresh EXP-003 and EXP-005 builds using the [recorded protocol](error_ntt_timing.md), then verify all saved pairs and provenance before deciding whether to retain EXP-005 for performance. No additional arithmetic edit or repeat of RUN-0001 is needed.

### Identity and evidence audit

The executed source/support commit is 5a499bd1940ce0ff8fd5d973f6f46b62b50c0648. Results commit af3408156a334c52676b51a5348540c17234390c directly follows it. Different source/results hashes are expected: the former identifies executed code, the latter archives its outputs. The current branch is reduction-counters. Before editing records, I verified all 942 tracked files against SHA-1-checked stored objects, including 800 archived result files. I did not invoke Git commands.

Validation manifest SHA-256 is 6bf9833c02e9744e92360cecd37d6668cb4c4dc01ad4803ee72315fce8f0bd5d; metadata SHA-256 is 544e5f302219c16933cb66dce7ce4a65beb2838ed76bc5c50958a657cec83cbd. The [run review](runs/EXP-005-RUN-0001.md) and [structured verification](evidence/ACT-0013/exp-005-run-0001-review.json) preserve all identities, exact assembly and detailed checks. I verified the 120 raw-stream hashes, eighteen binary hashes, seven support-file hashes, both 35-file source sets, committed source/support bytes, tools, command arguments, working directories and step order. All sixty steps exit zero and the original provenance recheck passes. Build diagnostics are empty. No full validation was rerun.

The only incremental source change is the exact reviewed indcpa.c call-site replacement, SHA-256 900541c7291e25feb86e0d42fc2e8daa3fc606d99130e496edddd1955ec479c2; the other 34 files retain EXP-003 identities. The original reference still matches pinned upstream 3edd5af5991927164edd4aacebfcbee00b8064e7. GCC 13.3.0 normal/UBSan modes and the observed x86_64 Ubuntu/WSL environment are recorded in the run review; manually controlled host/power/background/physical-core facts remain unknown.

For each parameter I verified all four 100-fixture KEM transcripts against the original reference: normal and UBSan for both implementations. Sizes are 416000/595200/806400 bytes, covering keys, valid ciphertext/secrets and the established malformed/noncanonical input cases. All twelve builds also pass 47 targeted error-polynomial vectors, 12032 forward coefficient checks, 48128 addition/final-reduction coefficient checks and 188 serialization comparisons per build. The oracle uses ordinary modular arithmetic without production reducers but shares transform layout/twiddles; it is not exhaustive or independent specification certification. Each candidate parameter passes the upstream 1000 valid/1000 invalid-secret-key/1000 invalid-ciphertext cases. Six UBSan builds emit no diagnostics on exercised paths. Earlier unchanged standalone basemul/dot/inverse oracles are not repeated.

I reconstructed the nine count summaries from all ninety observations. Saving K*256 Barrett calls affects keygen only: 512, 768 or 1024 calls, representing 25% of EXP-003 keygen Barrett calls, not 25% of duration. Montgomery keygen/encap/decap remains 4864/6400/9728, 7296/8832/13056 and 9728/11264/16384. Encap/decap Barrett remains 2432/3584, 3328/4736 and 4224/5888. This supports the intended mechanism and defines the primary timing target and comparison controls.

### Correctness, representation and security interpretation

I rechecked the conservative induction for both ETA1=3 and ETA1=2. The unchanged seven-stage forward NTT gives raw-error bounds 23299/23298, with maximum twiddle product 33231744 within int32_t and the Montgomery contract. The current CBD noise distribution guarantees the input bound for every seed. All butterfly results fit int16_t. After unchanged poly_tomont, the other operand is bounded by 3328, so the addition is bounded by 26627/26626 before the retained final reduction. The resulting unique centred residues and tested external bytes match.

Only the error representative is deferred. e is not a multiplication/inverse input or serialized secret-key vector. skpv retains its forward reduction, the wide-dot exit remains centred, and the accepted inverse-input contract is unchanged. No Montgomery scale operation, cryptographic parameter or noise distribution changes. The argument does not extend to global reduction removal, larger noise, other parameter sets or new consumers. Passing UBSan alone does not prove narrowing safety; inherited signed conversion/shift assumptions remain target-specific.

I inspected the saved normal keygen/NTT/reducer bodies, re-extracted candidate code from verified binaries, and extracted the same functions from the accepted EXP-003 timing executables. All sizes agree with nm. Original-reference keygen bodies match the EXP-003 control after relocation normalisation. The forward NTT (254 bytes), Montgomery (22 bytes) and Barrett (36 bytes) match across all three variants for each parameter, and across parameter namespaces. The new error-vector loop becomes K fixed direct ntt calls; skpv still uses polyvec_ntt, and final addition/reduction/serialization remain. No error-coefficient-dependent branch/address is introduced in this changed path. NTT control/indexing is public and the reducers use fixed arithmetic without division or indirect transfer.

Kyber512's keygen entry body contains the canary conditional, Kyber768 also the public matrix-vector loop, and Kyber1024 includes the existing inlined public-matrix rejection sampler, fixed noise/matrix loops and canary check. The rejection branches depend on public-seed-derived matrix candidates. I do not describe every keygen branch as a fixed public counter or claim input-independent whole-program timing. Callees outside this scope have not received a new exhaustive audit.

Keygen code sizes change 425->442, 479->512 and 948->988 bytes. Stack reservations change 5208->5224, 9320->9336 and 14984->14984 bytes; each saves six registers (48 bytes). Local totals are 5256->5272, 9368->9384 and 15032->15032, excluding entry return address and callees. These are not peak KEM stack estimates. Canary loads/checks/failure calls, endbr64 and one/two/three stack-page probes remain in both variants. Instruction presence does not establish runtime CET enforcement. No keygen canary or protection flag is removed by EXP-005; the earlier EXP-002 dot-product canary tradeoff persists.

Reduced calls, wrapper bypass, code growth, register spills and layout can jointly affect timing. I do not infer an individual reduction's time cost from the future speed difference. Larger stored representatives also change internal bit patterns; no power/EM or fault assessment follows from public control flow. I retain the limits for whole-program constant time, statistical leakage, exhaustive memory safety, signed portability, production approval and final ML-KEM conformance. The original manifest keeps assembly_review=pending; this later review records completed inspection separately without altering archived evidence.

### EXP-004 clarification and fresh comparison

EXP-004 was reserved for a possible interaction/combination study: whether optimisations behave differently together. EXP-002 already includes EXP-001; EXP-003 includes both; EXP-005 adds its treatment to EXP-003. Merely running that same combined source again would repeat the current treatment. A distinct interaction study would need separately controlled variants or ablations. I defer it unless that question becomes useful; it was never executed or rejected, and no failure is hidden. I keep IDs stable instead of renumbering EXP-005.

The new scripts/run_error_ntt_comparison.py restores the 35 accepted EXP-003 source files from cf8ae0dd700bb41628c158016a7c15926a0b790f and checks each hash. Historical manifest identity is ce1d1514a6d61039572c4dd3cd6d8005bf36f938d1968b2db1e5e60defec2b72. The current candidate must match accepted EXP-005 validation. The formal runner uses read-only Git queries/restoration without modifying the checkout/index. Its new source/support commit will be recorded separately; old EXP-003 durations are not reused as fresh controls.

The actual six timing executables must match all 24 reviewed keygen/NTT/reducer bodies before measurement. Normal flags and compiler are identical, with no counter/sanitizer instrumentation. Five adjacent pairs per parameter, alternating order, 100 warm-ups, 1000 measured exchanges, seed 1 and logical CPU 0 give sixty steps and 90000 operation durations. Analysis produces ninety summaries, 45 pairs and nine aggregates. I inspect all pairs, both order groups, absolute timings and any regressions without outlier removal or overhead subtraction. Encap/decap have no predicted direct arithmetic benefit. Positive time reduction favours EXP-005; aggregation uses the median of pairwise percentages. Five pairs from one session do not establish formal significance, order independence or a total original-reference gain.

[Development evidence](evidence/ACT-0013/error-ntt-comparison-smoke.json) records six actual builds, 24 exact assembly matches and twelve short processes: two blocks, twelve measured exchanges and two warm-ups each. All 432 rows, 36 summaries, eighteen pairs and nine aggregates pass. Synthetic improvements/regressions verify direction, experiment columns and median-of-paired-effects calculation; incomplete/duplicate/unequal groups, wrong variants, changed source identities and wrong historical hashes are rejected. Altered resolved call/branch targets fail assembly matching. One initial synthetic branch fixture changed only the absolute address, which is intentionally normalised; I corrected the fixture to alter its resolved symbolic target. The runner itself required no correction.

I used temporary files and mocked Git state/existence checks; historical bytes came from verified stored objects. The validation snapshot supplied compiler/provenance inputs for the development test only. No Git command, metadata collector, formal run or arithmetic edit was executed in this activity. Short support timings do not supply a thesis speed estimate. Temporary outputs were removed after their hashes/commands were recorded. RUN-0002 remains reserved for the user-executed formal comparison after a clean support commit.

- Validation review SHA-256: e583f1ef74776363536778f409be2bc872ec6a99dfa223628c6557e9fee1669f.

- Comparison runner SHA-256: 4ae286303c2a1e1bd88026a86da95510f39adbdc9d939d372d8091cba7aab54f.

- Comparison support evidence SHA-256: 0922f936bb0a7d792ce1df3f1b4e93999816256896a68339c52b1d79c3a2a7bb.

Final verification confirms that all 800 archived result files, validated arithmetic/upstream sources, previous support/evidence and Git HEAD remain unchanged. The accepted gate loads, all fifteen tested support hashes match, and syntax, JSON, links and whitespace checks pass. EXP-005/RUN-0002 does not exist yet. This activity changes five existing documents and adds one runner, two explanatory records and two evidence records.

## ACT-0014 — Error-vector timings accepted; final candidate and security/completion plan prepared

- **Completed:** I verified EXP-005/RUN-0002 against raw data, binaries, tools and committed source; reproduced every derived table; checked timing-build assembly and unchanged-operation layout; recorded performance/security findings; prepared EXP-006's exact manual edits and validation support; and defined a finite practical completion plan in response to the supervisor requirements.
- **Results:** All sixty run steps and provenance checks pass. All 90000 durations reproduce the ninety summaries, 45 pairs and nine aggregate rows exactly. All fifteen keygen pairs favour EXP-005, with median reductions +5.18%/+0.48%/+1.36% for Kyber512/768/1024. Kyber1024 encap/decap medians are -0.12%/-0.50%, retained as tradeoffs. All 24 keygen/NTT/reducer bodies match accepted validation. Twelve support-only builds on existing baseline/EXP-005 pass the new oracle and normal/UBSan KEM checks.
- **Learned:** EXP-005 has an observed targeted keygen benefit, but the small Kyber768 effect needs confirmation and unchanged-operation movements cannot be assigned to removed keygen reductions. IND-CPA function addresses shift despite matching normalised bodies. Security needs its own measurements: compatibility, bounds and assembly contribute evidence but do not replace secret-flow and secret-class timing tests. VTune is optional explanatory profiling.
- **Pending:** EXP-006 arithmetic is unapplied; its actual validation/counts/assembly/timing are not-run. Focused dynamic security checks, final direct/repeat-session comparisons, thesis figures/tables and the reproducibility handover remain. Whole-program/formal/physical-security claims remain unestablished.
- **Next:** Manually apply/review/commit the three [EXP-006 edits](experiments/EXP-006-keygen-dot.md) and execute its RUN-0001. Review that result before preparing fresh timing against EXP-005. After this final planned trial, freeze the optimisation search and complete the [remaining practical stages](practical_completion.md), even if EXP-006 does not improve performance.

### Timing identity, verification and interpretation

The timing/support source is 4bd813ed71a90c7722275dc802336852214a5388 and its direct results child is eb4c34586c7531bc87dcd165e952d3278cea0b5e on reduction-counters. The fresh control restores EXP-003 source cf8ae0dd700bb41628c158016a7c15926a0b790f; the candidate matches EXP-005 validation source 5a499bd1940ce0ff8fd5d973f6f46b62b50c0648. Upstream remains 3edd5af5991927164edd4aacebfcbee00b8064e7. Before updates I verified all 1072 tracked files, including 925 archived result files, against SHA-1-verified stored objects without invoking Git commands.

Manifest SHA-256 is 22cf2fcc0533c6e35a8063b6709b4d11cb391b742e0850cd0204d94bf0db6668; metadata SHA-256 is d1258c5e19aad1ac051932ae069d3ba9a0639718c237f0aa39f9b7304e55350c. I verified sixty step commands/order/directories/exit codes, all 120 raw streams, six executable hashes, fifteen support identities and committed bytes, 35 restored control files, source/tool/review hashes and provenance. All measured roundtrips pass. No benchmark or full validation was rerun. The [run record](runs/EXP-005-RUN-0002.md) and [structured audit](evidence/ACT-0014/exp-005-run-0002-review.json) preserve exact tables, pairs, source/assembly identities and checks.

I independently checked per-process medians/extrema and paired formulas, then reconstructed all three derived CSVs byte-for-byte from the 90000 raw durations. Effects are medians of pairwise percentages, not percentages derived from aggregate medians. Pair ranges are descriptive, not confidence intervals. The full result is:

| Parameter | Operation | EXP-003 median-of-medians ns | EXP-005 median-of-medians ns | Median paired reduction | Pair range | Positive pairs |
|---|---|---:|---:|---:|---:|---:|
| Kyber512 | keygen | 17746 | 16761.5 | +5.1832% | +5.1427% to +5.8418% | 5/5 |
| Kyber512 | encap | 18107 | 17942 | +0.7825% | +0.5680% to +1.2793% | 5/5 |
| Kyber512 | decap | 23606 | 23469 | +0.5401% | +0.2889% to +1.0130% | 5/5 |
| Kyber768 | keygen | 28603 | 28479.5 | +0.4761% | +0.4318% to +1.0811% | 5/5 |
| Kyber768 | encap | 28725.5 | 28496.5 | +0.8860% | +0.6082% to +1.3584% | 5/5 |
| Kyber768 | decap | 35458 | 35309.5 | +0.4216% | +0.2808% to +0.6991% | 5/5 |
| Kyber1024 | keygen | 42032 | 41471.5 | +1.3643% | +1.0843% to +2.2123% | 5/5 |
| Kyber1024 | encap | 44781 | 44805.5 | -0.1150% | -0.2846% to +0.3094% | 2/5 |
| Kyber1024 | decap | 52282.5 | 52564.5 | -0.5000% | -0.8562% to +0.2532% | 1/5 |

All keygen order-group medians favour EXP-005. The groups contain three and two pairs, so this does not establish order independence. Kyber1024 encap changes sign between groups (+0.0413% with EXP-003 first, -0.2822% with EXP-005 first); decap is negative in both (-0.5000%/-0.5190%). Across all operations there are 38 positive and seven negative pairs. I retain larger block-3 movements across several Kyber768/1024 operations without asserting their cause. Kyber768's keygen gain is comparable to small control-operation changes and needs final confirmation.

The protocol has five adjacent pairs per parameter, alternating order, 100 warm-ups, 1000 measured exchanges, seed 1 and guest logical CPU 0. Both variants use the same normal GCC 13.3.0 -O3 build. The recorded x86_64 Ubuntu 24.04.2/WSL2 environment reports i9-12900KS and 24 logical CPUs; unknown host/power/background/physical-core conditions remain unknown. CLOCK_MONOTONIC_RAW reports 1 ns resolution and 11–12 ns empty-pair probes; resolution is not accuracy. All timings, including the full 15803–1190035 ns raw range, remain retained without overhead subtraction or outlier deletion. Repeated fixtures/inner observations are not independent replications. This is a single-session incremental result, not a universal, statistically established or cumulative original-reference gain.

### Assembly, correctness and security findings

All 24 normal keygen/forward-NTT/reducer bodies match the accepted ACT-0013 review after relocation normalisation. Accepted correctness and invalid-input transcripts, conservative bounds, exercised UBSan findings and measured counts apply through verified source/build identities; they were not newly inferred from the faster timings.

To investigate unchanged-operation movements, I extracted enc_derand, dec, indcpa_enc and indcpa_dec from all six timing binaries. Normalised bodies match for each parameter. KEM enc_derand/dec entry addresses remain unchanged, with body sizes 180/243 bytes. IND-CPA enc/dec entry addresses move by 16 bytes for Kyber512 and 32 bytes for Kyber768/1024; their body sizes remain 514/215, 601/224 and 1036/227 bytes. This establishes a layout change, not its causal contribution to timing or identity of every reachable byte/address. Compiler/layout effects and environmental variation can affect controls alongside the changed keygen path.

EXP-005's mechanism is K*256 fewer keygen Barrett calls; Montgomery and encap/decap counts stay unchanged. The raw-error/addition bounds remain 23299/26627 for Kyber512 and 23298/26626 otherwise. skpv and all earlier inverse-input centring remain intact. Keygen code grows by 17/33/40 bytes, and local stack including saved registers changes by +16/+16/0 bytes, excluding entry return address and callees. Keygen canaries, endbr64 and page probes remain. The EXP-002 dot-product local-canary tradeoff persists. Wrapper bypass, register/spill and layout effects prevent interpretation as an isolated Barrett-call cost.

The changed error-vector path introduces no observed secret-dependent choice of loop/index in the scoped assembly. Existing public-matrix rejection branches remain in the larger keygen body. Larger representatives change internal bit patterns, which this software timing review does not assess for power/EM or faults. No secret-class timing or dynamic secret-flow test has yet run. Whole-program constant-time proof, exhaustive memory safety, all-target signed portability and final ML-KEM conformance remain unestablished.

I retain EXP-005 as the next research reference with its observed targeted benefit and recorded regressions. The small effects and final retention decision remain subject to the closing evaluation rather than being dismissed as noise or promoted to a universal benefit.

### Supervisor clarification and finite completion scope

The user reports no required extra platform or minimum optimisation count. The supervisor specifically expects a method to evaluate how the code changes affect implementation security and suggested VTune optionally. The intended handover is the completed practical work followed by a thesis draft and repository for supervisor feedback.

I therefore made the [implementation-security assessment](implementation_security.md) a required remaining stage: existing mathematical/functional/assembly evidence, plus dynamic secret-flow checking and focused statistical secret-class timing measurements. I reviewed primary dudect repository/author guidance, ctgrind's author repository and the official Memcheck manual. The planned protocol will document public/secret operands, valid ranges, positive/negative sensitivity controls, pinned tools/builds, finite predeclared budgets/statistical rules and raw evidence. It will report detected/no-evidence-within-tested-scope/inconclusive outcomes, never a blanket secure/constant-time certificate. New candidate-specific dependencies or reproducible timing signals require investigation before an unqualified retention decision.

I reviewed official Intel Hotspots, collection and system-requirement documentation. VTune can help explain CPU costs/hot functions, but it is optional and does not replace leakage tests. Profiling runs must remain separate from primary uninstrumented timing. WSL PATH/default-location inspection found no valgrind, vtune or perf executable, no usual Memcheck header and no standard /opt/intel/oneapi/vtune directory; this does not inspect Windows installations or prove every installation is absent. No installation or dynamic security/profiler run occurred. The dudect ePrint PDF retrieval returned HTTP 403; I record repository/author-page review, not full-paper access. [Literature entries](literature.md) preserve these sources and outstanding checks.

The [completion checklist](practical_completion.md) requires: finish EXP-006; freeze selection; complete security testing; directly compare original reference and selected implementation across repeat sessions; and produce reproducible tables/figures/methods and a repository audit. Three sessions with ten balanced pairs per parameter is a starting final-protocol proposal, not an executed or yet-finalised run. Small/adverse incremental effects should receive matched confirmation if they affect selection. I do not need endless new optimisations, a compulsory EXP-004 interaction study or VTune usage to finish. Practical work is not yet complete even though arithmetic exploration is near its endpoint.

### Final planned candidate and development support

[EXP-006](experiments/EXP-006-keygen-dot.md) proposes a separate polyvec_basemul_acc_keygen function with the existing wide-dot body and retained poly_tomont, omitting only its intermediate poly_reduce. Its keygen call replaces the old dot-plus-tomont pair; the general dot and its inverse-facing centred output stay unchanged. The copied kernel can grow code and alter layout, so performance and hardening remain measured questions. I do not modify arithmetic, including temporary candidate copies; exact snippets and SHA-256 expectations are recorded for manual application.

For actual keygen matrix [0,3328] and centred skpv [-1664,1664], raw sums, partial sums and twiddled sums fit int32_t and the Montgomery input interval. Raw Montgomery outputs fit int16_t with bound 3328; poly_tomont's product is bounded by 4502784 and output by 3328. EXP-005 final addition bounds remain 26627/26626 before the retained reduction. Keeping exactly one poly_tomont preserves scale. The new API must not replace the general inverse-facing API. Source predictions save another 512/768/1024 keygen Barrett calls: 1536->1024, 2304->1536, 3072->2048, with all other counts unchanged. These predictions are not collected EXP-006 results.

I added scripts/run_keygen_dot_validation.py and tests/test_keygen_dot.c. The runner guards all three exact proposed source hashes against accepted EXP-005, preserving the remaining 32 files. Formal validation is planned for 69 steps, 138 raw streams, eighteen executables and 33 assembly extracts, including normal/UBSan exact 100-fixture KEM comparisons, upstream suites and reduction counts. The new ordinary-int64 dot oracle checks residues, post-tomont bounds, four error-addition/final-reduction patterns and serialized polynomial bytes. It shares twiddle/layout information and is not an independent specification certification.

[Support evidence](evidence/ACT-0014/keygen-dot-validation-support-smoke.json) records twelve actual existing-baseline/EXP-005 builds with EXPECT_KEYGEN=0 and two KEM fixtures each. All builds, targeted oracle checks, normal/UBSan runs and four-way transcript comparisons pass, with transcript sizes 8320/11904/16128 bytes. There are 45/53/61 dot vectors per build, 11520/13568/15616 coefficient checks, 46080/54272/62464 addition checks and 180/212/244 serialization comparisons. Unapplied/altered-source preflight guards, rejection of old EXP-005 counts against new predictions, count formulas and independent range checks pass. These checks exercise the test machinery on existing arithmetic, not the proposed EXP-006 function. Temporary outputs were removed after recording their identities. No Git commands, metadata collector, formal EXP-006 run or performance measurement occurred.

- Timing review SHA-256: 990d53bfb8de3a454f1ac6dab55ebfea26ec4582becaf830a38deae76eb6630c.
- Keygen-dot validation runner SHA-256: 5b695fd9ae5b4c30fbbe3a5d9508eb2090e83e1f9345286e7655c31fed148bd5.
- Keygen-dot test SHA-256: 3b7f45c0dc08a2e10c37a7684ab2b6af1d4ffbc4880ce10a8865b1cce5f63490.
- Development support evidence SHA-256: 1af66b3b0eaef71330e93cc8d10ea7cf6f4c9e8bc89bf12d5f927123c61689b5.

Final verification confirms that all 925 archived result files, arithmetic/upstream identities, previous support/evidence and Git HEAD remain unchanged. The current EXP-005 acceptance gate loads; the unapplied EXP-006 guard rejects before collection. All seven tested support hashes and both new evidence hashes match. The published manual snippets reproduce all three guarded proposed hashes in memory only. Syntax, JSON, relative links, LF line endings and whitespace checks pass. No EXP-006 result directory exists. This activity changes seven existing documents and adds two support files, four explanatory records and two evidence records. Arithmetic application, Git operations and the formal candidate run remain manual next steps.

## ACT-0015 — Keygen-dot validation and assembly accepted; timing against EXP-005 prepared

- **Completed:** I verified EXP-006/RUN-0001 against committed source, retained raw output, binaries and tools; reviewed the actual keygen/dot/reducer assembly; documented correctness, ranges, count savings, memory/hardening findings and limitations; prepared the fresh EXP-005/EXP-006 timing runner/protocol; and removed VTune from the remaining plan at my request.
- **Results:** All 69 validation steps, twelve deterministic normal/UBSan transcripts, targeted arithmetic/addition/serialization checks, three upstream suites and ninety count observations pass. Keygen Barrett falls 1536->1024, 2304->1536 and 3072->2048; Montgomery and encap/decap counts remain unchanged. The new dot ends in the retained poly_tomont, and keygen canaries remain. Six development timing builds match all 33 reviewed bodies and twelve short processes pass the comparison pipeline in both orders.
- **Learned:** The keygen-specific consumer permits this extra Barrett deferral while the general dot must retain its centred inverse-facing output. Fewer calls are confirmed, but added code and changed compiler unrolling/call layout can affect speed. Keygen local stack changes by 0/-16/0 bytes. These findings support a bounded implementation review rather than a blanket security result.
- **Pending:** Review/commit the new comparison support and records, then execute EXP-006/RUN-0002. Formal speed and performance retention remain pending. Focused dynamic secret-flow/timing-leakage tests, final direct/repeat-session comparisons and thesis artifacts/reproducibility remain required. VTune installation/profiling is excluded.
- **Next:** Run the [fresh matched timing protocol](keygen_dot_timing.md) after a clean support commit, then review actual pairs/provenance before selecting the implementation. No further arithmetic edit or repeat of RUN-0001 is needed. EXP-006 remains the final planned optimisation trial before the closing evaluation.

### Provenance and accepted correctness evidence

The executed source/support commit is 4c9d539eba8903c2404591b8024e7afef15bbf47. Results commit 571f597a0b35fd0c9df264402d4b74d07a725204 directly follows it on reduction-counters. The source identifies the executed implementation and harness; the results commit archives outputs. Before updating records I verified all 1220 tracked files against SHA-1-verified stored objects, including 1065 archived result files, without invoking Git commands.

Validation manifest SHA-256 is 738fe9501ed4f7df3f5766577f5d6e0e359d1d6f0630b4617175e5bee527c499; metadata SHA-256 is 7b737d9bf0555e146ae79d226b2e64834b4f50f8f2ac0fde912e8270f1955c71. The [run review](runs/EXP-006-RUN-0001.md) and [structured evidence](evidence/ACT-0015/exp-006-run-0001-review.json) preserve exact identities, instructions and checks. I verified 69 step commands/order/directories/exit codes, 138 raw-stream hashes, eighteen executable hashes, seven support files, both 35-file source sets and committed source/support bytes. Tools and the passing provenance recheck agree; build diagnostics are empty. No full validation was rerun and the archived pending assembly-review field was not rewritten.

The applied polyvec.c/polyvec.h/indcpa.c bytes match all three proposed SHA-256 values from ACT-0014; the other 32 candidate files retain EXP-005 identities. The baseline still matches upstream 3edd5af5991927164edd4aacebfcbee00b8064e7. Normal -O3 and UBSan modes use the recorded GCC 13.3.0 tool. The available environment is x86_64 Ubuntu 24.04.2 under WSL2, kernel 5.15.167.4, on a reported i9-12900KS with 24 guest-visible logical CPUs. Host/power/background/physical-core fields remain unknown. No timing or leakage property is inferred from that metadata snapshot alone.

For each parameter, all four 100-fixture baseline/candidate normal/UBSan transcripts match exactly: 416000/595200/806400 bytes. The fixtures include keys, valid ciphertext/shared secrets, corrupted/random ciphertexts, malformed secret keys and noncanonical public keys. Twelve builds also pass 45/53/61 targeted dot vectors, 11520/13568/15616 coefficient checks, 46080/54272/62464 error-addition/final-reduction checks and 180/212/244 polynomial serialization comparisons per build. The ordinary-int64 oracle avoids production reducers but shares twiddle/layout information; it is not independent specification certification. Each candidate passes the upstream 1000 valid/1000 invalid-secret-key/1000 invalid-ciphertext cases. Six exercised UBSan builds emit no diagnostics. Unchanged standalone basemul/inverse oracle suites are not separately repeated.

I reconstructed all nine count summaries from ninety observations. Keygen Barrett falls by K*256: 512/768/1024 calls, giving 1024/1536/2048 remaining. Montgomery keygen/encap/decap remains 4864/6400/9728, 7296/8832/13056 and 9728/11264/16384. Encap/decap Barrett stays 2432/3584, 3328/4736 and 4224/5888. A complete keygen dot still uses 384 Montgomery reductions in its wide-product body plus 256 in poly_tomont. Saving one third of EXP-005 keygen Barrett calls is not a prediction of one-third duration savings.

### Range, scale, generated code and security findings

The actual keygen matrix is bounded by [0,3328] and skpv retains [-1664,1664]. For K=2/3/4, sum00/sum11 bounds are 11075584/16613376/22151168; cross sums 22151168/33226752/44302336; and twiddled sums 16613376/22151168/27688960. Each product/partial sum fits int32_t and each reducer input fits [-109084672,109084671]. Raw Montgomery results already fit int16_t with magnitude at most 3328. Keeping poly_tomont gives product bound 4502784 and output bound 3328, preserving EXP-005's final raw-error addition bound 26627/26626 before the retained final reduction.

Barrett only changes representatives, while exactly one retained poly_tomont supplies the original scale conversion. Final centred public-key coefficients and tested bytes therefore agree. skpv, secret-key serialization, general-dot centring and EXP-003 inverse-input contracts remain unchanged. The dedicated API includes poly_tomont and must not be used as an interchangeable general dot. The proof depends on these callers, parameter/noise bounds and signed target assumptions; UBSan alone cannot establish all narrowing safety.

I re-extracted the normal control/candidate functions from verified binaries: fifteen EXP-005 bodies and eighteen EXP-006 bodies, with sizes checked against nm. I also checked all 33 saved original-baseline/candidate extracts against their binaries. General dot, poly_tomont and both reducers match EXP-005 after relocation normalisation; overlapping original-baseline functions match earlier validation. After self-symbol renaming, each new dedicated-dot body differs from the general dot only in its tail jump, poly_reduce -> poly_tomont. Its local frame is restored before that jump.

The dot arithmetic remains int32 operations with unrolled components; its branches use public pair parity and termination at 128 pairs. Operand addresses and twiddle indices follow public positions. poly_tomont retains a fixed 256-coefficient loop and multiplier 1353. Both reducers remain fixed arithmetic without division or conditional branches. In keygen, the new call replaces the old dot-plus-tomont pair, while skpv reduction, direct error NTT, final addition/reduction and serialization remain. Kyber512 has two direct dot calls; Kyber768's formerly looped three calls become unrolled; Kyber1024 keeps its public four-row loop and public-matrix rejection sampler. I do not describe whole-keygen execution as branchless or independent of all public inputs.

| Parameter | Keygen body bytes EXP-005 -> EXP-006 | Added dot body bytes | Net change in these function bodies | Keygen local stack bytes EXP-005 -> EXP-006 |
|---|---:|---:|---:|---:|
| Kyber512 | 442 -> 423 | 285 | +266 | 5272 -> 5272 |
| Kyber768 | 512 -> 521 | 355 | +364 | 9384 -> 9368 |
| Kyber1024 | 988 -> 980 | 413 | +405 | 15032 -> 15032 |

This is a scoped function-size sum, not total executable growth or measured instruction-cache cost. Local stack includes register saves and excludes entry return address/callees; it is not peak KEM stack. Candidate keygen reservations are 5224/9320/14984 bytes plus 48 saved-register bytes. Each new dot has a 24-byte reservation and 48 bytes of saves, the same 72-byte local footprint as the preserved general dot.

Keygen canary loads/checks/failure calls, endbr64 and one/two/three page probes remain. The earlier EXP-002 general-dot canary change persists; the additional dedicated dot also has no local canary. No protection flag is disabled. Canary presence does not prove memory safety and endbr64 presence does not prove runtime CET enforcement. Code duplication, loop unrolling, calls and layout can affect speed alongside removed reductions, so a timing result will not isolate one Barrett call's cost.

I observed no new secret-coefficient-dependent branch/address selection in the scoped changed path. This supports the reviewed implementation under its contracts, not whole-program constant time or leakage resistance. Larger representatives alter internal bit patterns; physical power/EM/fault behaviour, exhaustive memory safety, all-target signed portability and final ML-KEM conformance remain unestablished. Required dynamic secret-flow and statistical timing-leakage checks remain not-run. I retain these distinctions in the [security plan](implementation_security.md).

### VTune scope and thesis progress

I chose to avoid VTune in this activity. Installation, profiling and VTune analysis are excluded from the remaining plan; the earlier literature entry remains as historical provenance. This does not remove the supervisor's requirement to evaluate implementation-security effects. Active README, register, security plan and completion checklist now reflect that decision.

The study has a concrete chain of evidence: a proposed arithmetic mechanism, bounded caller contracts, confirmed reduction counts, compatibility/invalid-input checks, generated-code tradeoffs and measured incremental effects where collected. Small regressions and inconclusive effects remain available for the thesis rather than being hidden. This is useful research progress, while the final security assessment and direct/repeat-session performance evaluation are still necessary to close the practical component. EXP-006 remains the last planned optimisation trial; a slower timing result would still complete that trial without requiring another candidate.

### Fresh timing support and development verification

I added scripts/run_keygen_dot_comparison.py. It restores all 35 EXP-005 files from 4bd813ed71a90c7722275dc802336852214a5388 and checks them against accepted timing manifest 22cf2fcc0533c6e35a8063b6709b4d11cb391b742e0850cd0204d94bf0db6668. The current candidate must match the accepted EXP-006 validation. The user-executed formal runner uses read-only Git queries/restoration and does not alter the checkout/index. Fresh control durations replace any temptation to compare separate-run medians.

Before timing, all six normal executables must match 33 reviewed bodies: five common functions per variant/parameter plus the candidate-only dot. The committed support/review, manifests, source/tool/binary hashes and affinity are rechecked. Five adjacent pairs per parameter alternate order, with 100 warm-ups, 1000 measured exchanges, seed 1 and logical CPU 0: 69 steps, 138 raw streams and 90000 operation durations. Derived outputs contain ninety process summaries, 45 pairs and nine aggregates. I report median paired effects, observed ranges, both execution orders, absolute timings and all regressions. I remove no outliers or timer overhead. The five-pair single-session limits remain explicit; this is not a leakage test or total original-reference comparison.

[Development evidence](evidence/ACT-0015/keygen-dot-comparison-smoke.json) records six real builds, 33 exact actual-assembly matches and twelve short processes covering both orders. All 432 rows, thirty-six summaries, eighteen pairs and nine aggregates pass. Synthetic improvement/regression cases verify labels, direction, order and median-of-paired-effects calculation. Missing/duplicate/unequal pairs, wrong variants, changed candidate identities and wrong historical hashes are rejected; changed symbolic call/branch targets and a wrong dedicated-dot tail target fail matching.

The first smoke attempt stopped before building because the copied review filename still named EXP-005. I corrected that reference to the ACT-0015 EXP-006 review and the complete check passed. I used isolated temporary files, mocked Git state/existence checks and supplied exact historical source bytes from SHA-1-verified objects. The existing validation snapshot supplied development provenance/compiler inputs only. No Git command, metadata collector, formal timing run or arithmetic edit occurred. Temporary binaries/CSVs were removed after recording their commands/hashes. Short support timings provide no thesis speed estimate. EXP-006/RUN-0002 remains uncreated until the user commits the support and runs the recorded protocol.

- Validation review SHA-256: b9e7f1e0a633c6abab769057086c7908cf2b3a49b8f8727fa52117a40e199696.
- Comparison runner SHA-256: 60ffa8f4b83d060e7cb9902b935fb46383943acc9146e2556e50542bb3d2b9e7.
- Comparison support evidence SHA-256: 86489182eab9c0aa7d9f6f4479bf76c60797df65136a25468504b0b6d7f2568d.

Final verification confirms that all 1065 archived result files, arithmetic/upstream identities, earlier support/evidence and Git HEAD remain unchanged. The accepted EXP-006 gate loads with all 33 required control/candidate bodies; all fifteen tested timing-support hashes and both new evidence hashes match. The preserved manual-edit record matches the actually applied source. Syntax, JSON, relative links, LF and whitespace checks pass. EXP-006/RUN-0002 does not exist. This activity changes eight existing documents and adds one comparison runner, two explanatory records and two evidence records. The next action is the user's review/commit and formal timing execution, with no further arithmetic edit required.

## ACT-0016 — Review EXP-006 timings, freeze trials and start security testing

### Request, evidence and selection

I received the committed EXP-006/RUN-0002 result and a request to review it against EXP-005, record correctness/security implications, begin security testing and produce useful thesis visuals at appropriate milestones. The source/support commit is 02cdbb13b49e649953dc05653bcb94002491b236; result commit 42d68a7da90f5d19d0539a0e8825a24852121e41 is its child. I inspected the actual repository and binary/data artifacts rather than relying only on the supplied terminal screenshots.

The arithmetic trials are now complete. I select EXP-005 as the primary implementation for closing evaluation and retain EXP-006 as a secondary research comparison. I freeze the optimisation search. EXP-006's general keygen-benefit hypothesis is not supported by this run, although Kyber1024 keygen shows an observed benefit. I make no new parameter dispatch or arithmetic rollback; the current checkout remains EXP-006 and security support restores EXP-005 faithfully into an ignored build directory. Final retention still requires the security assessment and direct repeat-session confirmation. EXP-004 remains a deferred separate interaction question, not an omitted failure. VTune stays excluded.

### Performance audit and interpretation

The [full timing review](runs/EXP-006-RUN-0002.md) and [machine-readable audit](evidence/ACT-0016/exp-006-run-0002-review.json) record all identities, paired observations, order groups and limitations. I verified 1368 tracked files against SHA-1-checked stored objects at the initial clean result commit, without executing Git commands. I checked 69 completed steps, 138 raw streams, six actual binaries, fifteen support files, all 35 restored EXP-005 source files and 33 scoped assembly bodies. All 90000 raw durations, ninety summaries, 45 paired effects and nine aggregates reproduce the three saved CSVs byte-for-byte, with independent formula/median/range checks. Measured round trips and provenance checks pass.

| Parameter | Keygen median paired reduction | Encap | Decap |
|---|---:|---:|---:|
| Kyber512 | -2.55% | -2.39% | -1.89% |
| Kyber768 | +0.22% | -0.82% | -0.72% |
| Kyber1024 | +1.67% | -0.43% | -0.02% |

Positive means faster. Ten of 45 pairs improve, including eight of fifteen keygen pairs. Every Kyber512 pair is slower. All five Kyber1024 keygen pairs improve, and that direction persists in both order groups. Kyber768 keygen and Kyber1024 decap are mixed. I preserve negative control-operation results and do not dismiss them as proven noise. The paired statistic differs from the ratio of aggregate medians; this explains the small sign difference in Kyber1024 decap's separate absolute summaries.

The comparison uses five adjacent pairs, alternating order (three EXP-005-first and two EXP-006-first), 100 warm-ups, 1000 measurements per process and fixed seed-1 fixtures. I preserve the entire raw range, including long observations, without exclusions or timer subtraction. GCC 13.3.0/-O3, CLOCK_MONOTONIC_RAW nanoseconds, Ubuntu/WSL and guest logical CPU 0 define the target. Manual host/power/background/physical-core conditions remain unknown where unrecorded. Inner observations are not independent process/session replications. The result is not a cumulative original-baseline improvement or a leakage measurement.

### Correctness, assembly and security continuity

ACT-0015's accepted validation supplies deterministic byte compatibility including sampled invalid/noncanonical inputs, targeted int64-oracle checks, explicit range/scale/narrowing arguments, exercised UBSan and upstream functional evidence. All 33 timing bodies match that review. I did not rerun full correctness or throughput tests unnecessarily, or modify prior result manifests to replace historical pending-review fields.

The confirmed extra K*256 keygen Barrett saving reduces EXP-005's 1536/2304/3072 calls to 1024/1536/2048, with Montgomery and other-operation counts unchanged. It does not predict a proportional time saving. The new dot body and changed keygen body add a scoped 266/364/405 bytes; local keygen stack changes by 0/-16/0 bytes, with Kyber768 call unrolling. Keygen canaries, endbr64 and page probes remain; the inherited general-dot local-canary removal remains and the additional dot has no local canary. These observations do not prove memory safety or runtime CET enforcement.

I additionally compared KEM enc_derand/dec and IND-CPA enc/dec in each timing pair. All twelve function comparisons match after relocation normalisation. IND-CPA entry addresses move by -16/+16/0 bytes for Kyber512/768/1024, while the KEM entries match. This preserves evidence of layout differences without attributing the measured regressions to a demonstrated cache/layout mechanism. Public-index/control observations in reviewed arithmetic remain bounded; no result establishes whole-program constant time, physical power/EM/fault resistance, all-target portability or final ML-KEM conformance.

### Executable dynamic secret-flow support

I allocated [EXP-007](experiments/EXP-007-secret-flow.md) to dynamic secret-flow assessment, not an optimisation. scripts/run_secret_flow.py and tests/test_secret_flow.c compare original/EXP-005/EXP-006 under GCC 13.3.0 with normal flags plus -g. The runner pins accepted manifests/reviews, restores all 35 EXP-005 files byte-for-byte, records tool/source/support/binary identities and archives build output, assembly, stdout/stderr, XML, occurrence counts and outcomes. Formal execution requires the committed source/support and clean-tree checks through the existing collector. No production arithmetic is changed.

The local system had no Valgrind executable/header. I downloaded Ubuntu valgrind 1:3.22.0-0ubuntu3 and extracted it under a temporary directory; the installed libc6-dbg was available. I inspected the actual client macros and tested the real Valgrind 3.22.0 runtime. This did not install system software. The exact package, launcher and valgrind.bin, Memcheck runtime/preloads, headers and disassembler hashes are retained. I use defined twins to distinguish real uninitialised memory from intentionally marked secrets, origin tracking, no default suppressions and explicit test-boundary declassification.

The initial six-path development matrix completed nine builds and 162 processes, with eighteen detected marked positive controls and no target diagnostics. I retained that [initial snapshot](evidence/ACT-0016/secret-flow-support-initial.json). Subsequent caller inspection made the operand-role difference explicit: encryption passes secret sp second; decryption passes decoded skpv first. I expanded the focused matrix with basemul-first and dot-first, including the [0,4095] encoded-secret stress envelope and a defined centred second operand. This improves coverage beyond the generated-key integration case without changing arithmetic or inventing a new optimisation.

The [final development evidence](evidence/ACT-0016/secret-flow-support-smoke.json) records nine builds, 198 Memcheck processes, 129 assembly extractions and 870 retained raw files embedded with hashes. The total is 336 steps, counting intentional nonzero control exits as raw observations. All eighteen marked positive controls detect their intended branch or indexed-address dependency. All 27 defined controls and nine marked negative controls are quiet. All 72 defined and 72 marked target processes are quiet. Each target has eight fixtures; basemul cases each expand into 128 coefficient pairs. The full integration scope is IND-CPA decryption on two valid, two single-bit-corrupted, two all-255 and two deterministic-random public ciphertexts, with marked generated secret-key bytes. Full KEM reencryption/implicit-rejection secret-flow coverage is not claimed.

All 102 extracted production bodies match accepted normal validation/timing binaries after relocation normalisation. I inspected all 27 control bodies: deliberate branches/indexed addresses remain, and the negative control has no branch or call. Native execution is rejected. Parser/classifier checks reject incomplete XML, suppressions, wrong completion markers, quiet positives, diagnostics outside the intended control and tampered accepted review/restored source bytes. The final saved evidence matches the actual support file hashes. Both development snapshots retain exact support text; the initial text was reconstructed by reversing the documented coverage edit and its captured SHA-256 identities matched exactly.

Development execution used temporary directories, SHA-1-verified source-object reads and replacements only for user-reserved Git state/existence operations. Actual compiler/Valgrind processes, file hashes, source gates, restoration, report parsing and body comparisons ran. The uncommitted support check is not formal EXP-007/RUN-0001. Its quiet result is limited to exercised marked paths/operands and says nothing about every operand-latency, unexecuted or physical channel. Formal dynamic collection/review and the separate statistical leakage pilot, finite committed protocol and runs remain required.

### Thesis visuals and closing scope

I added analysis/build_thesis_figures.py, a 22-file input-hash index and pinned plotting requirements. [Three figures](thesis_figures.md) cover EXP-006's individual paired effects and order, all implemented incremental timing effects, and original-to-EXP-006 Montgomery/Barrett call counts. Each has SVG/PDF vector and 300-dpi PNG exports. Three data tables retain exact values; captions distinguish observed ranges from confidence intervals, conditional incremental effects from cumulative gains, and calls from time/instructions/security.

The plotting code recomputes 225 paired effects, 45 group medians/extrema and checks 54 count groups. I rendered and inspected all figures, corrected an overlapping median label, and regenerated in a separate directory: all twelve figure/table outputs and the provenance manifest match byte-for-byte. [Figure review evidence](evidence/ACT-0016/figure-review.json) records these checks. Matplotlib 3.10.8 and its exact dependencies were installed only in a temporary virtual environment; the existing pip --python option supplied pip when the bare environment lacked it. I preserved source/output hashes and omitted calendar metadata from SVG/PDF exports.

I recorded the request to produce further relevant thesis visuals at evidence milestones. Final direct/repeat-session effects, code/local-stack tradeoffs and the formal security matrix/timing diagnostics will follow their evidence, with adverse and inconclusive findings retained. I updated README, the register, reduction map, experiment/protocol status, security plan and practical checklist. The remaining work is finite: formal secret-flow testing, the separate statistical leakage assessment, direct original-reference/repeat-session performance and the final reproducibility/security handover. Then I can write the thesis draft and present it with the repository for supervisor feedback.

### Handoff and recorded identities

I next review/commit the support and records, install the pinned packaged Valgrind tool and execute EXP-007/RUN-0001 using its recorded commands. No new arithmetic edit is needed. Formal results stay separate from development evidence and use a new run ID after any failed/interrupted attempt. I continue to perform Git operations manually.

- notes/evidence/ACT-0016/exp-006-run-0002-review.json: cd08444809dbde25021221388c0fa9fe4b4cf109f74e988c0b2744e008c3327d.
- notes/evidence/ACT-0016/secret-flow-support-smoke.json: 77424357658c6f7340bdd5f04d0b7eda3b4afd6cf2be1f51b6873c46b2e064ff.
- notes/evidence/ACT-0016/secret-flow-support-initial.json: 0d95b75626ee8a17e4246160605f0fe46a51b06684582c59727a6139f51f949c.
- notes/evidence/ACT-0016/figure-review.json: 12760428ef0c0912a07a267d9c7887a4a8869895e0b5733c9bc81ae0c483d57e.
- scripts/run_secret_flow.py: 4b27cb1f0501ec0eea9c5ad9dc016058fe88c92872f1a2b53ce0a8b2e309e4cc.
- tests/test_secret_flow.c: ea2efcbcec2ae999d0253e07db7f965c75eb5078c5b3efcfb73bb22248cf4f3f.
- analysis/build_thesis_figures.py: 8c72c1df31ee158bc2825435101ee51a0432dd8f450d7d6c704685c41bd4fda6.
- analysis/figures/ACT-0016/provenance.json: c9b7a24a43fb2a988dfe681241a214b0434e4cf52d1d32def0cfa027857ffd2c.

Final ACT-0016 verification preserves all 1208 archived result files, production arithmetic, earlier scripts/tests/evidence and Git HEAD. Both development snapshots retain support/raw bytes matching their recorded hashes; the final runner's five support hashes match the current files. All nine final security builds emit no warnings. The final matrix has 336 steps, 198 reports and 102 matching production bodies. JSON, Python syntax, relative links, LF and trailing-whitespace checks pass. Formal EXP-007/RUN-0001 remains uncreated. This activity changes ten existing documents and adds the new support, evidence, result record and reproducible figure package; no Git operation or arithmetic edit was performed.

## ACT-0017 — Accept secret-flow evidence and prepare bounded timing-leakage testing

### Starting evidence and decision

I inspected the actual EXP-007/RUN-0001 files after the supplied execution screenshots. HEAD and source/support commit are 5dfac7ba0a775dfe8812a9ef1ef3e2403c0b9ba4; all 1393 tracked files matched that commit before this work. EXP-007 results were present but not yet committed. I preserved all 2080 existing archived result files, and did not execute Git commands or edit production arithmetic.

I accepted [EXP-007/RUN-0001](runs/EXP-007-RUN-0001.md) after checking the metadata/source/tool/support/binary identities, all 870 raw files, all 198 XML reports and all 129 assembly bodies. All 72 marked and 72 defined target processes were quiet. All 18 deliberate branch/address positive controls were detected, all 27 defined controls and nine marked negatives were quiet. Expected exit-99 raw steps remain labelled failed by the generic execution helper; the review explicitly interprets them as expected controls. The 102 production bodies match the prior accepted normal-code review, and all 27 control bodies match the sensitive development build.

This supports no marked-secret branch/address dependency observed in these executed paths. It does not prove whole-program constant time or rule out operand latency, other microarchitectural channels, power/EM or faults. IND-CPA integration is narrower than full KEM reencryption/implicit rejection. Existing correctness/range/invalid-input/UBSan evidence remains separate; the inherited EXP-002 local-canary tradeoff remains recorded.

### EXP-003 and EXP-005 interpretation

I clarified that the variants are cumulative. EXP-003's staged inverse NTT improved every one of the 30 encapsulation/decapsulation pairs over EXP-002, with median reductions 4.30–4.98%. EXP-005 retains that benefit and adds the error-vector change: keygen +5.18%/+0.48%/+1.36% against freshly rebuilt EXP-003. These percentages have different denominators. They are not absolute performance rankings and cannot be added or multiplied across sessions.

I keep EXP-005 as the provisional primary closing candidate and explicitly include EXP-003 as comparator/fallback for the remaining assessment. EXP-003 deserves substantial thesis emphasis irrespective of final selection. Small effects and Kyber1024 control-operation regressions require matched repeat sessions; no universal winner is declared from one session. EXP-006 remains the useful mixed/adverse result demonstrating that fewer reductions alone do not guarantee a speed improvement. No further arithmetic search or VTune work is added.

### Statistical timing support and sensitivity pilot

I added [EXP-008's protocol](experiments/EXP-008-timing-leakage.md), native test harness, runner and raw-stream analysis. I pinned dudect source revision dc269651fb2567e46755cfb2a13d3875592968b5 as a method/reference oracle and retained its header/license. This is a custom dudect-style screen, with documented differences in timer, views and stopping, not unmodified dudect.

The formal protocol compares original/EXP-003/EXP-005 across all parameters, eight paths, two synthetic secret-class profiles and two process repetitions. It fixes 50000 analysis observations plus 2000 retained calibration observations per process, two looks, three views and threshold |t| > 10. There are 324 measurement processes: 288 target cells and 36 controls. Every interval, AUX pair and class is retained in lossless archives, including predefined exclusions. The criterion is diagnostic; no calibrated family-wise error probability or constant-time proof is claimed.

I development-checked all nine builds, 180 assembly extractions and 324 processes with a reduced 4000-observation budget. All 99 production bodies match accepted normal code, and the final build emits no warnings. No target signal was flagged at that small development budget, but two final uncropped positive controls were insensitive; I retain that inconclusive result. A separate 50000-observation control pilot detects all 18 positive controls in the final uncropped view (absolute t approximately 23.50–287.94); all 18 negative controls remain quiet under the final analysis. Detection of these deliberately large differences is not a sensitivity guarantee for tiny leaks.

The initial analysis used a calibration-only cropping cutoff. One positive control subsequently shifted enough to leave only 9711 class-1 samples at the first cropped look. I preserved that attempt and changed to a fixed-rule pooled class-blind 99th percentile at each planned look before formal collection. The uncropped view remains mandatory and visible. All 36 control processes meet the final coverage/sensitivity rules on reanalysis. No target observations were used to choose this correction. Four numerical/corrupt-stream tests pass, including an independent oracle compiled from the pinned upstream Welch core.

[Support review](evidence/ACT-0017/timing-leakage-support-review.json) links exact support/raw development archives, initial failures and final control analysis. Temporary drivers substituted Git/source-cleanliness gates only for explicitly uncommitted development, restoring historical bytes from verified repository objects. The production runner enforces committed clean support, pins accepted inputs and restores both historical variants without editing the production checkout. It fails if any of the 99 production assembly bodies differs from the accepted normal code. Formal EXP-008/RUN-0001 has not been created.

### Visual artifacts and correction

I added a [formal EXP-007 coverage matrix](../analysis/figures/ACT-0017/exp007-secret-flow.svg), with PDF/PNG, 99 marked-process data rows, provenance and a bounded caption. I inspected its rendering. It distinguishes quiet targets from sensitive deliberate controls and is not a security score.

I corrected trailing spaces/tabs in the three initial SVGs and their generator. My ACT-0016 whitespace check omitted SVG files, so its unqualified passing-check statement was incomplete. All original PNG/PDF/CSV outputs and all 22 data inputs remain byte-identical. I retain the pre-correction provenance and old/new SVG hashes in [correction evidence](evidence/ACT-0017/figure-review.json); the initial figure directory now identifies the ACT-0017 revision. Earlier result directories and review evidence are unchanged.

### Remaining practical work and manual handoff

The arithmetic trials and formal dynamic-flow assessment are complete. I next commit the accepted EXP-007 run and reviewed ACT-0017 support, then collect EXP-008/RUN-0001. I review all signals/controls, diagnose or reproduce findings, complete a fresh original/EXP-003/EXP-005 comparison across sessions, and assemble the final security/results/reproduction package. That finite closing sequence precedes the thesis draft and supervisor feedback.

I use these commands manually from the repository root, reviewing the staged content before committing:

```sh
git diff --check
git add -- README.md notes/ analysis/ \
  scripts/run_timing_leakage.py scripts/analyse_timing_leakage.py \
  tests/test_timing_leakage.c tests/timing_leakage_protocol.json \
  tests/check_welch_reference.c tests/test_timing_leakage_analysis.py \
  tests/reference/dudect/ results/EXP-007/RUN-0001/
git diff --cached --check
git diff --cached --stat
git diff --cached
git commit -m "Review EXP-007 and prepare bounded timing-leakage testing"
git status --short
python3 -B scripts/run_timing_leakage.py --experiment EXP-008 --run RUN-0001 --cpu 0
echo $?
```

If the run completes, I preserve and commit its result directory and request review of the assessment, control results, raw streams and assembly. An exit-zero completion is not a security pass. A failed/interrupted attempt remains under its original ID; any retry uses a new ID.

Final verification preserves all 2080 pre-existing archived result files, all production arithmetic, all earlier scripts/tests/evidence and HEAD. Python syntax, JSON, relative links, SVG XML and LF/trailing-whitespace checks pass, explicitly including SVG. Every archived development raw stream and support snapshot matches its recorded hash, including decompression identity. Formal protocol pins and all three source contracts verify. The [verification record](evidence/ACT-0017/final-verification.json) lists the 14 modified tracked files and 25 new support/evidence files; EXP-007 result files are additionally awaiting their user commit. No formal EXP-008 directory was created.

## ACT-0018 — Accept the timing screen and prepare the final comparison

### Recorded starting state and security finding

I inspected EXP-008/RUN-0001 after the supplied completion screenshots. Source/support HEAD is 50db1e8cb1cbd7eada48b4a47a1fe5bd92ae2f6d on reduction-counters; EXP-008 results were untracked. I snapshotted all 3109 existing archived result files before editing. I performed no Git commands or production-arithmetic edits.

I accepted [EXP-008/RUN-0001](runs/EXP-008-RUN-0001.md) after checking 513 completed steps, 1026 raw files, nine binaries, compiler/disassembler/support identities and 105 source-file identities. I checked the 70 restored historical files against verified Git blobs and the support against the source commit. All 99 production and 81 harness assembly bodies match the accepted reviews/development snapshot.

[Independent NumPy analysis](evidence/ACT-0018/exp-008-run-0001-review.json) reproduces all 1944 Welch statistics, sample counts, crop thresholds, exclusions and flags from the retained compressed streams. There are 16.2 million analysis and 648000 calibration observations, with zero invalid-interval/AUX exclusions. All 288 target processes are quiet at both planned looks in all three views; the largest target absolute t is 2.91016 against threshold 10. All 18 positive controls are detected in the final uncropped view (absolute t 20.55887–269.92644), and all 18 negatives are quiet (maximum absolute t 2.11025). The smallest per-class view/look count is 12257.

The outcome is no difference detected within the finite paths/classes/budget, not constant-time certification or a sensitivity guarantee for tiny leaks. I preserve the distinct variant matrices of EXP-007 and EXP-008, synthetic encoded-key IND-CPA scope, WSL/build limitations, unassessed whole-KEM/physical/fault channels and the inherited general-dot local-canary tradeoff. The frozen rule triggers no further signal diagnosis for this run. The planned security collection is complete; consolidated final reporting remains.

### Final direct-performance protocol and support

I prepared [EXP-009](experiments/EXP-009-final-comparison.md) for original/EXP-003/EXP-005 with three separately launched sessions, each containing 12 triplet blocks per parameter. This replaces the earlier provisional ten-pair idea: all six orders occur twice, every variant occupies every position four times, and parameter order rotates. I predeclared distinct session/block seeds with identical fixtures within each triplet, 100 warm-ups and 1000 measured exchanges per process. Each session contains 324000 nanosecond duration rows.

The runner faithfully restores each historical candidate, reuses the unchanged normal benchmark, verifies 108 production bodies, checks source/support/tool/binary identities and retains complete raw output and round-trip diagnostics. Clean committed support remains required for formal collection. Three contrasts are analysed: original to EXP-003, original to EXP-005 and EXP-003 to EXP-005. I keep process medians, within-block effects and session estimates distinct. Three-session ranges are descriptive, not confidence intervals or independent-host evidence. I retain all adverse cells and do not silently replace completed sessions or extend sampling for a preferred outcome.

The [development review](evidence/ACT-0018/final-comparison-support-review.json) records nine warning-free builds, 108 matching bodies, all 225 successful steps, 108 measurement processes and 324000 valid duration rows. All three derived tables reproduce exactly. Four focused tests protect paired-effect calculations, matching/coverage, balanced ordering, distinct sessions and stable build conditions. Formal analysis explicitly rejects development records.

I retained the full development output and exact support/driver snapshot in a checksum-bound archive. Only the Git commit-presence/clean-tree gates were replaced in that temporary driver; historical bytes were read directly from verified objects. The metadata environment snapshot was reused and labelled. These are uncommitted support checks, not an EXP-009 thesis performance result. An archive-report writer initially passed a string to a Path-only checksum helper after all data/archive checks succeeded; I corrected the report conversion without changing any measurement or archive. No formal EXP-009 run directory was created.

### Figures, writing and Git handoff

I added a [timing-screen figure](../analysis/figures/ACT-0018/exp008-timing-screen.svg), with vector PDF/SVG, 300-dpi PNG, all 1944 statistics and provenance. Each upper cell is the maximum over its 24 planned target statistics; the lower control panel follows the predeclared control criteria. I inspected the rendered PNG and regenerated all five outputs byte-for-byte. The figure is diagnostic, not a security ranking. Final direct-performance graphs await formal EXP-009 observations.

The user clarified that the original draft was supplied at the beginning of the conversation. It was initially absent from the visible history/repository search; I subsequently recovered its attachment path through the app thread reader and read the existing Word file. [Source review](evidence/ACT-0018/thesis-draft-review.json) records its hash and scope. The document contains Introduction and Methodology chapters and four research questions that still fit the study. I updated the [writing plan](thesis_writing_plan.md) with a direct question-to-evidence map and concrete proposed-versus-delivered revisions: targeted wider intermediates rather than blanket coefficient-storage widening, reduction audit/counts rather than runtime profiling, matched blocks/sessions rather than treating inner measurements as independent experiments, scoped code/stack observations, and complementary bounded security methods. The existing Word file was not edited; this is a content review, not a layout or literature-verification claim. The original AVX2 collaborator question remains a separate follow-on study. Methods and accepted Results can be drafted now; final comparisons and candidate conclusions await EXP-009.

[Direct object inspection](evidence/ACT-0018/source-and-branch-review.json) finds local main and origin/main at dac387fe75fa260ccecd1211c57b716025ed2ad4, an ancestor 33 commits behind the work branch. I did not contact the remote. A normal branch backup push can happen after committing; final history-preserving integration into main follows closing review. Existing cited commit identities must be retained. The [Git handoff](git_handoff.md) supplies exact staging/run/backup instructions and explains the later fast-forward/divergence decision without executing it.

The screenshot's raw objdump whitespace warnings are formatting in retained evidence. I added scoped .gitattributes rules to preserve results bytes across checkouts and exempt only raw .log files from whitespace diagnostics; source/docs/SVG checks remain active. No old log or result byte was rewritten. I updated README, the register, reduction map, security status, figure captions and practical checklist. The finite remaining practical work is the three final sessions and review, final candidate interpretation, consolidated tables/figures and a reproduction/handover audit. Methods and the accepted Results can be written while that collection proceeds.

Final [verification](evidence/ACT-0018/final-verification.json) preserves all 3109 archived result files, production source, prior scripts/tests/evidence and HEAD. The frozen input hashes and all development support snapshots still match. Python syntax, JSON, SVG XML, relative links and LF/trailing-whitespace checks pass for changed/new support. Seven tracked documents change and 23 new support/evidence/figure files are added, including the verification record; previously ignored baseline binaries are excluded from that inventory. EXP-008's 1029 previously untracked result files additionally need their user commit. No formal EXP-009 directory exists. Formal Git clean-tree/presence gates remain for the user-launched committed run.

## ACT-0019 — Accept final-comparison session 1 and continue the fixed protocol

### Starting state and independent review

I inspected the completed EXP-009/RUN-0001 from source/support commit 8a5e36e5d041507cc5649c7d43edb8468000f476 on reduction-counters. I snapshotted all 3564 existing archived result files, including 455 session-1 files, before editing. All 3342 tracked working files matched HEAD. The supplied successful push output and matching local origin/reduction-counters ref establish a branch backup through that commit; RUN-0001 itself remained untracked and was not included. I performed no Git commands, production edits or new benchmark runs.

I accept [session 1](runs/EXP-009-RUN-0001.md) after the [reproducible audit](evidence/ACT-0019/exp-009-run-0001-review.json). All 225 steps completed, all 450 raw files match their hashes, all nine builds are warning-free, and all nine binaries plus compiler/disassembler identities match. I verified 105 source-file identities and all 108 archived production bodies against the accepted normal assembly. Direct verified-object reads additionally establish all 37 unique committed support/pinned-input identities and all 70 historical candidate source blobs. The original 35 files match the baseline commit and upstream checkout.

The frozen analyser reproduces all three tables byte-for-byte from 324000 retained duration rows. A separate calculation independently checks process medians, min/max, paired ratios/effects and aggregate signs/medians/ranges. All 108000 measured and 10800 warm-up KEM exchanges passed the harness round-trip check. I checked the complete build/assembly/timing order, rotating parameter order, seeds and the six variant permutations occurring twice per parameter. Every contrast has six reference-first and six candidate-first pairs. No outlier is removed and no timer overhead is subtracted.

### Findings and bounded interpretation

Both cumulative candidates improve every original-reference operation/block pair in this first session. Across the nine operation/parameter groups, median reductions are 5.97–19.94% for EXP-003 and 10.72–19.59% for EXP-005. These are ranges across different workloads, not a global score. The run record includes all 27 contrasts with paired ranges/sign counts and all absolute timing levels.

EXP-005's additional keygen medians over EXP-003 are +5.26%/+0.49%/+1.62%. The middle parameter has one slower block. Kyber1024 encapsulation is −0.01236% with six positive and six negative pairs; decapsulation is −0.35645%, with all twelve pairs slower. I preserve these and all unchanged-operation movements. The pattern supports evaluating EXP-005's modest extra benefit against EXP-003 after all three sessions; it does not yet settle final selection or identify a compiler/layout cause. EXP-003 remains an important cumulative comparator whose separate inverse-NTT contribution is assessed by its earlier incremental experiment.

The CPU/timer/flags match the recorded protocol. The actual timer is CLOCK_MONOTONIC_RAW in ns, with 1 ns reported resolution and 11–12 ns minimum empty-pair diagnostics. Affinity is logical CPU 0 in WSL; physical placement and manually controlled host/power/load facts remain unknown. I do not promote one session, inner samples, pair ranges or descriptive order strata into cross-session significance or general hardware evidence.

Identical source/normal-code identities justify scoped reuse of accepted correctness, range and security findings. EXP-009 adds round-trip and build-continuity evidence; it is not a new invalid-input, UBSan, dynamic-flow or leakage run. The original/EXP-003/EXP-005 statistical screen and distinct original/EXP-005/EXP-006 dynamic-flow matrix retain their limits. The inherited general-dot local-canary tradeoff remains visible. No further security collection is triggered by these ordinary performance measurements.

### Figure, records and remaining sessions

I added a [session-1 figure](../analysis/figures/ACT-0019/exp009-session1-effects.svg), vector PDF, 300-dpi PNG, all 324 plotted pairs and checksum provenance. Its nine panels show every contrast/operation and all parameters, paired ranges and medians, with regressions visible. It explicitly states session 1 of 3 and pending final selection. I inspected the PNG and regenerated all five outputs byte-for-byte. The new audit report also reproduces byte-for-byte. [Figure review](evidence/ACT-0019/figure-review.json).

I updated README, the register, completion checklist, security status, reduction map, writing plan, captions and [Git handoff](git_handoff.md). The original Word draft remains unchanged. I did not modify the frozen EXP-009 protocol, runner, analyser, benchmark or pinned experiment notes. The new audit/figure scripts are outside the frozen support set, and all 23 measurement-support hashes still match session 1.

I next review/commit the ACT-0019 changes and RUN-0001 results, optionally make a normal backup push, and launch session 2 separately after a genuine break. After checking successful completion and allowing another break, I launch session 3 without changing support. Untracked results are allowed by the collector; a separate support commit between sessions 2 and 3 is unnecessary if nothing else changes. Failed attempts keep their IDs and any retry uses the next unused run ID with the same session number. This accepted session is not replaced and the budget is not extended based on its effect.

After both remaining sessions, I audit/combine all three, interpret the closing candidate, build final direct-performance and consolidated security/code/stack outputs, and complete the reproduction/handover review. The practical component is not yet labelled complete. Local main remains an ancestor 34 commits behind; final history-preserving integration remains for the closing handoff. [Final preservation and file checks](evidence/ACT-0019/final-verification.json) record the exact scope of this review.

## ACT-0020 — Complete the final comparison and select EXP-005

### Starting state and accepted collection

I inspected completed EXP-009/RUN-0002 and RUN-0003 after the user committed ACT-0019 and session 1 in 99733b9f5401236708ca25be9efd807cff60d7ce. The supplied push succeeded and the local origin/reduction-counters ref matches that commit. It did not include the two new uncommitted run directories. I snapshotted all 4474 archived result files and all 3809 tracked files before editing; the tracked tree matched HEAD. I performed no Git command, production arithmetic edit or new benchmark run.

I re-audited session 1 and accepted [session 2](runs/EXP-009-RUN-0002.md) and [session 3](runs/EXP-009-RUN-0003.md). All three use identical protocol, 23 frozen support files, compiler, flags, disassembler and source-file identities. Source/support commits differ only because the user committed documentation/results between sessions 1 and 2. [Verified object/branch evidence](evidence/ACT-0020/source-and-branch-review.json) checks all 37 support/pinned-input blobs per source commit, the original 35 baseline files and both 35-file historical snapshots.

The [complete audit](evidence/ACT-0020/exp-009-three-session-review.json) verifies 675 successful steps, 1350 raw files, 27 warning-free normal builds/binaries and 324 matching production-body extractions. All 324000 measured and 32400 warm-up exchanges pass shared-secret checks. All 972000 duration rows and all nine per-session derived tables reproduce. Independent calculations confirm medians, ranges, ratios, signs and complete actual execution order. Every session follows 12 balanced triplets per parameter, all six variant orders twice and distinct predeclared seeds. No duration is removed or adjusted.

I ran the unchanged predeclared three-session analyser into analysis/final-comparison-EXP-009. It retains 81 session estimates and 27 combined contrasts, taking the median of the three session medians with an observed range. I do not pool inner samples or replace that estimator with a pooled 36-pair median. The recorded WSL CPU/compiler/timer/affinity match; manual power/background/physical placement and break duration remain unknown. Three invocations are not a claim of environmental independence, statistical significance or portability.

### Final result and candidate judgement

I record all values and ranges in the [complete comparison](final_comparison.md). Both cumulative candidates beat the original in every paired operation/block comparison across all three sessions. EXP-003's three-session median reductions span 5.97–20.00% across the nine groups; EXP-005's span 10.72–19.71%. Those are workload-group ranges, not one aggregate score or uncertainty interval.

EXP-005's additional keygen medians are +5.26%/+0.49%/+1.52%, with observed session ranges 5.18–5.31%/0.46–0.49%/1.32–1.62%. The session signs are positive throughout. Kyber1024 encapsulation and decapsulation are −0.15%/−0.36% in the combined median, negative in all three sessions. The all-pairs plot preserves individual adverse effects larger than these summaries. Different original-reference medians cannot simply be subtracted to obtain the direct marginal contrast; median ratios are nonlinear.

I [select EXP-005](final_candidate.md) as the primary final thesis candidate for its repeated additional keygen benefit, explicitly accepting its small Kyber1024 control-operation costs and scoped code/local-stack growth. EXP-003 remains a substantial comparator and reasonable alternative for those operation-heavy workloads or a simpler keygen path. This is a qualitative decision under the predeclared tradeoff rule, not an arbitrary operation-weighted score, universal fastest claim or production recommendation. EXP-006 remains the adverse trial; no hybrid parameter-specific implementation is introduced.

I verify the accepted keygen facts in all three sessions: body growth 17/33/40 bytes and additional local-stack use 16/16/0 bytes relative to EXP-003, with keygen canaries/endbr/probe instructions retained. Only indcpa.c differs between EXP-003 and EXP-005 source snapshots; the other reviewed arithmetic bodies match. Both inherit the general-dot local-canary change from EXP-002. The [security matrix](final_security_summary.md) consolidates range/scale/narrowing, sampled compatibility and invalid inputs, exercised UBSan, assembly, direct dynamic-flow and statistical evidence, and the unestablished properties. The timing comparison supplies no new leakage evidence. No additional security measurement is required by the completed protocol.

### Graphs, preservation and handoff

I generated the [three-session plot](../analysis/figures/ACT-0020/exp009-three-session-effects.svg), [all 972 paired effects](../analysis/figures/ACT-0020/exp009-all-paired-effects.svg) and [keygen tradeoff chart](../analysis/figures/ACT-0020/exp005-keygen-tradeoffs.svg), each in SVG/PDF/300-dpi PNG with full data. I inspected all renderings. All thirteen figure/data/provenance files, three combined-analysis files and three new audit reports independently regenerate byte-for-byte. [Reproduction review](evidence/ACT-0020/figure-review.json). Earlier results, audit records, figures and frozen protocols remain unchanged.

I updated README, the register, completion checklist, security status, reduction map, thesis writing plan, captions and [Git handoff](git_handoff.md). EXP-009 is closed and the predeclared experimental collection is finished. The original Word draft is unchanged; complete Methods/Results/Discussion writing can now proceed from the accepted evidence. Full-text literature-dependent claims still require their own verification.

The exact selected EXP-005 snapshot is pinned by 35 hashes in analysis/final_candidate.json at historical commit 4bd813ed71a90c7722275dc802336852214a5388. The working production tree still contains EXP-006, with indcpa.c, polyvec.c and polyvec.h differing. I prepared exact manual restoration and hash-check instructions without executing them. Remaining practical handoff is the selected-source/reproduction/repository check, not more optimisations or performance sessions. Local main remains an ancestor 35 commits behind; remote integration follows a fresh user-controlled check and preserves all cited commits.

The next manual commit includes ACT-0020 plus the 910 newly collected archived files in RUN-0002/RUN-0003, followed by a normal push. The [final verification](evidence/ACT-0020/final-verification.json) records preservation of all 4474 archived result files, unchanged source/HEAD/frozen support and the authored-file checks. I do not mark the entire practical handoff complete before the selected working-source and repository checks occur.

## ACT-0021 — Verify the closing-results backup and prepare selected-source handoff

I inspected the user's closing commit 66c707f9dc8cef556d1133fb48d6fb1f71e989e7 and successful push output. The local reduction-counters and origin/reduction-counters refs match that commit. Its parent is 99733b9f5401236708ca25be9efd807cff60d7ce. The exact 950-file change contains the 910 archived RUN-0002/RUN-0003 files and 40 ACT-0020 support/review files; no tracked file was removed. All ACT-0020 recorded file hashes agree with the commit. All 4750 tracked regular working files matched their verified committed blobs before these documentation edits, and all 4474 archived result files are tracked. The supplied final git status --short is empty. I did not contact the remote or execute Git. [Local object/source evidence](evidence/ACT-0021/source-and-handoff-review.json).

I verified all 35 source files in the historical selected EXP-005 snapshot, 4bd813ed71a90c7722275dc802336852214a5388, against analysis/final_candidate.json. The actual working directory remains EXP-006. Only indcpa.c, polyvec.c and polyvec.h differ; the other 32 match. I reviewed the prospective restoration: replace the dedicated keygen call with the general dot product followed by poly_tomont, and remove the EXP-006-only function/declaration. The diff is 2 insertions and 41 deletions. Substituting those three historical file identities in memory yields all 35 selected identities. No production source was written and no test or benchmark was rerun.

I updated README, the completion checklist and the [Git handoff](git_handoff.md) to distinguish the now-backed-up closing evidence from the pending manual restoration. The handoff includes the exact three paths, a complete 35-file hash check, the expected diff, and later history-preserving main integration. Local main/origin/main remain dac387fe75fa260ccecd1211c57b716025ed2ad4, an ancestor 36 commits behind; a later manual fetch must establish fresh remote state. The branch itself is not a problem and its deletion is unnecessary.

I retain the manual Git/arithmetic workflow. After the actual restoration, the final review must inspect the working bytes and update current-status documentation before the source/handoff commit and push. I do not mark restoration, main integration or the entire practical handoff complete in advance. No further experimental collection is needed under the completed protocol; Methods, Results and Discussion writing can already proceed using the accepted evidence and writing plan. All previous raw results, reports, figures, selected-source pins and frozen support remain unchanged. [File-preservation verification](evidence/ACT-0021/final-verification.json).

## ACT-0022 — Accept the restored EXP-005 source and complete the handoff review

I supplied the restoration output and a one-time permission for the assistant to repair the actual optimisation source if necessary. The restoration was already correct. Direct inspection confirms that all 35 working source files match analysis/final_candidate.json and the verified historical Git blobs at 4bd813ed71a90c7722275dc802336852214a5388. The actual patch matches ACT-0021's expected patch exactly: indcpa.c restores the general dot followed by poly_tomont, polyvec.c removes the EXP-006-only function and polyvec.h removes its declaration/macro. The complete diff has 2 insertions and 41 deletions. The assistant made no production-source repair or other arithmetic edit. [Selected-source review](evidence/ACT-0022/selected-source-review.json).

I matched the restored 35-file identity to EXP-005 in both accepted security manifests and all three final comparison manifests. The EXP-005 raw error-vector transform, secret-vector post-NTT centring and final public-key reduction remain intact; the EXP-006-only function is absent. All 23 frozen support files match, and all 4474 archived result files remain byte-for-byte equal to their committed blobs. No new build, correctness/security test or benchmark was executed. Exact source identity supports reuse of the existing bounded evidence, not a new measurement or broader security claim.

The Git HEAD and local origin/reduction-counters ref remain 66c707f9dc8cef556d1133fb48d6fb1f71e989e7. The user's three restored files and the ACT-0021 preparation were the only tracked changes at the start of this review. Local main/origin/main remain dac387fe75fa260ccecd1211c57b716025ed2ad4; I inspected local objects/refs without executing Git or contacting the remote. The one-time source-repair permission does not change the standing manual Git workflow.

I updated current-status documentation to identify the actual selected working source, retaining historical run records, earlier activity entries and the selection manifest's checkout-at-selection field. The [handoff](git_handoff.md) now supplies one explicit reviewed commit scope and the subsequent history-preserving main integration commands. It explains the expected red deletion lines and diff pager, and distinguishes accepted manifest binaries from any older ignored local executables. The scientific work and source/documentation handoff review are complete; only the user's final commit/push and branch integration remain before Git publication is complete. I do not label those unexecuted actions as successful or request another experiment.

I added a plain-language one-paragraph supervisor summary to the [thesis writing plan](thesis_writing_plan.md), covering the five arithmetic trials, the selected cumulative implementation's 10.7-19.7% observed time reductions across workload groups, the important EXP-003 contribution, adverse EXP-006 result, scoped code/stack costs and bounded security findings. The original Word draft remains unchanged. Methods, Results and Discussion writing can proceed from the accepted tables and graphs. [Final preservation and commit-scope verification](evidence/ACT-0022/final-verification.json).
