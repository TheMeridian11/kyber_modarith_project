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
