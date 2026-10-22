# EXP-002 incremental timing comparison

I completed this protocol after [EXP-002/RUN-0001 validation and assembly](runs/EXP-002-RUN-0001.md). The accepted [RUN-0002 results](runs/EXP-002-RUN-0002.md) show improvements beyond EXP-001 in all 45 observed pairs. This document preserves the measurement protocol.

## What is compared

I use scripts/run_incremental_comparison.py with the existing timing harness, CSV parser and paired-effect calculations. The control is fused-basemul (EXP-001); the candidate is wide-dot (EXP-002). I rebuild and time both in the same session. Historical EXP-001 durations do not substitute for a fresh control.

The runner restores the 35 accepted EXP-001 source files from d407b5134f14a96a4572b3af1132a8f715e0a28d into the new run's ignored build/exp001-source directory using read-only git show. Each file must match the SHA-256 in the accepted EXP-001 manifest. This does not check out a branch, modify the current arithmetic, or alter Git history/index state. The current candidate must match EXP-002/RUN-0001. Both source identities are recorded separately from the new support/run source commit.

Both variants use the same reviewed GCC executable, normal -O3 flags and uninstrumented harness. Before measurement, their actual vector-dot-product and Montgomery-reducer assembly must match the ACT-0009 review. The comparison preserves instruction offsets, sizes, operands and symbolic branch targets while normalising resolved code/data locations. Objdump uses --insn-width=16 for new logs. A mismatch stops the attempt and preserves its evidence.

## Measurement and interpretation

I retain the [established paired timing protocol](paired_timing.md): five pairs per parameter set, 100 warm-up and 1000 measured exchanges per process, seed 1, logical CPU 0, and CLOCK_MONOTONIC_RAW nanoseconds. Blocks 1/3/5 run EXP-001 first; blocks 2/4 run EXP-002 first. Each pair is adjacent, with parameter order 512/768/1024 inside each block. The three-versus-two order imbalance remains explicit.

There are 30 processes and 90000 operation durations, producing 90 process summaries, 45 paired effects and nine aggregate rows. This is the same practical automated budget as the first comparison. Fixtures repeat across blocks; these rows are not 90000 independent experiments. No full validation is repeated for this timing step.

- Speedup = EXP-001 process median / EXP-002 process median; above 1 favours EXP-002.
- Improvement (%) = 100 * (1 - EXP-002 process median / EXP-001 process median); positive means EXP-002 took less time.
- The primary descriptive estimate is the median of paired effects, with observed pair minimum/maximum. These ranges are not confidence intervals.

The derived CSVs use exp001_ and exp002_ column prefixes so the control cannot be confused with the original baseline. I inspect all pairs and both execution orders before classifying improvement, regression or an inconclusive effect. I preserve negative observations and do not rerun merely to obtain a favourable result. Any further repetition needs a stated reason. I do not add these percentages to EXP-001's historical baseline comparison; a claim against the original reference requires suitable direct evidence.

Input generation, output checks and CSV formatting remain outside measured operations. Operating-system randomness is excluded by the deterministic API mode. No timer-overhead subtraction or outlier removal is used. Unknown host power/background/core placement stays unknown; guest affinity does not establish physical-core placement. Timing gains do not resolve the security limitations or local stack-canary change recorded in the validation review.

## Run and preserve

I used the following command after committing the runner, evidence and notes. It is historical; RUN-0002 exists and must not be reused:

~~~bash
python3 -B scripts/run_incremental_comparison.py --experiment EXP-002 --run RUN-0002 --cpu 0
echo $?
~~~

The runner invokes the metadata collector itself. Optional --host-os, --power-mode and --background-load values should describe observed facts. I keep the machine's workload and power conditions steady during the run.

I accept execution only with exit code zero, completed status, passing assembly/CSV/roundtrip/provenance checks, and intact hashes. I then inspect derived/comparison.csv and preserve the complete run directory. Failed/interrupted attempts remain under their original ID; any retry receives a fresh ID after diagnosis. I never overwrite a run or edit raw evidence to remove warnings/outliers.

## Support check

[Development evidence](evidence/ACT-0009/incremental-comparison-smoke.json) records six real compilations, twelve assembly matches and two short blocks of twelve measured exchanges, yielding 432 operation rows. Historical-file hash failures, changed restored/candidate source, changed loop bounds/branch targets, wrong-variant assembly and incomplete/duplicate/unequal comparison groups were rejected or failed matching. Synthetic positive and negative effects confirmed direction, experiment labels and aggregation.

The short check used temporary files, mocked Git-state/existence operations and read historical source directly from verified stored objects. The read-only git show invocation was checked with a mocked subprocess; no Git commands or metadata collector ran. The saved formal EXP-002 validation was not repeated. Development durations are excluded from performance conclusions. This check preceded the formal clean-source execution, whose saved artifacts and complete derived analysis were verified in ACT-0010.
