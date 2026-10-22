# EXP-NNN RUN-NNNN Run record

I use this field specification for the future full execution manifest and as a readable fallback for exploratory runs. No values here are observations. Unavailable fields say unknown/not-collected with a reason.

The initial metadata collector writes metadata.json for a metadata-only snapshot. It does not fill the build or execution evidence described below. Its record type remains metadata-only, benchmark_executed is false, and execution checks remain not-run.

## Identity and provenance

- Experiment ID, run ID, record type and optional comparison block:
- Linked activity ID and sequence/order:
- Variant, parameter set and build mode:
- Full project source commit and upstream commit:
- Working-tree and submodule status before execution:
- Exact patch/relevant untracked-source archive if exploratory:
- Build command, working directory, compiler path/version/full flags:
- Executable path and SHA-256:
- Build stdout/stderr locations and exit code:
- Harness revision if different:

## Conditions

- Linux distribution/kernel and Windows host/WSL versions:
- CPU model, visible topology and scope:
- RAM and whether guest or physical:
- Requested/observed affinity; physical-core mapping if verified:
- Power/frequency/turbo/SMT settings and thermal observations where collected:
- Background workload and manual controls:
- Timer, unit and overhead policy:
- Warm-up and measured iterations:
- RNG-inclusive or deterministic API:
- Fixture/seed identifiers and generation procedure:
- Valid/invalid ciphertext class where relevant:
- Comparison order and paired baseline run ID:

## Execution

- Exact invocation and working directory:
- Status: started/completed/failed/interrupted:
- Process exit code or signal:
- Per-check results and stdout/stderr evidence:
- Raw-file paths and SHA-256 checksums:
- Expected/actual observation counts:
- Missing data, interruptions and anomalies:

I preserve the tested command's exit status rather than the success of a later logging command. Unperformed checks are not-run. Failed and partial outputs remain evidence.

## Derived analysis

- Analysis command, code commit and dependency versions:
- Input raw paths/checksums:
- Exclusions and reasons:
- Summary/generated-figure paths:
- Metric, uncertainty method and comparison-block handling:
- Interpretation and linked experiment decision:

Raw observations are immutable. Reanalysis creates separately identifiable outputs or revisions. The results-saving commit is not the source commit that generated the measurements.
