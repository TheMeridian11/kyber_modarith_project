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
