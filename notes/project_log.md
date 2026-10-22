# Project activity log

Append one entry for each substantive response/session. Correct earlier conclusions through explicit amendments. Proposed instructions are not completed actions. Dates specify timezone; link experiments/runs when available and preserve failed or inconclusive outcomes.

## ACT-0001 — 22 October 2026 — Research records and setup handoff

Timezone: Australia/Sydney.

- **Completed:** Agreed the division of work; established the research workflow, experiment register, baseline plan, templates and literature record; corrected documentation paths and reduction-map inaccuracies.
- **Pending:** Researcher applies the supplied root .gitignore and .gitmodules edits, reviews the existing script change and documentation, runs the verification commands and commits the setup. Per-run metadata collection and the benchmark harness remain to be implemented.
- **Results:** No builds, correctness tests or benchmarks were run in this session. No new performance or security findings. Proposed configuration edits are not yet confirmed applied.
- **Learned:** The baseline script's directory correction already exists as an uncommitted change. The remaining preparation is reproducibility and evidence capture; the script's current summary output is insufficient for the raw-data study.
- **Next:** Return setup verification output and the commit hash. Then implement automatic per-run metadata collection.

### Starting state observed

Branch reduction-counters; project HEAD eefad7ec998fa529fa8fa11f91a0a00370a9a548; upstream 3edd5af5991927164edd4aacebfcbee00b8064e7 with official GitHub remote.

A pre-existing uncommitted edit changes scripts/run_baseline.sh from impl/ to implementation/. The assistant did not make that edit. Root .gitignore still uses old paths and ignores all .log files. .gitmodules is missing despite the upstream gitlink. No files were found under analysis/ or results/. Assistant edits in this session are research documentation only.

### Historical context recorded retrospectively

The conversation's 29 September 2026 review reported identical reference source/build files across upstream, baseline and optimised copies and passing existing correctness binaries for all parameter sets, including valid exchanges, invalid keys and corrupted ciphertexts. It reported no saved performance results and no source changes by the assistant.

Those checks were reported in chat without a persistent full raw run archive. They are historical observations, not newly executed tests or the accepted EXP-000 baseline. Earlier reduction-count predictions remain hypotheses until implementation and measurement. This retrospective note was added on 22 October, not backdated.

### Documentation verification

Local Markdown links were checked successfully. A before/after SHA-256 fingerprint of 90 existing implementation, script and root-ignore files was identical, confirming no assistant changes to those files. Git diff inspection showed only the pre-existing script directory edit outside research documentation. No compilation, runtime validation or benchmarking was performed. The configured project remote is https://github.com/TheMeridian11/kyber_modarith_project.git; no push or remote synchronisation was performed.
