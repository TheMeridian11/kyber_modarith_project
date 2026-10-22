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
