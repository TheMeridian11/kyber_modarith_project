# EXP-005 incremental timing comparison

I specify this protocol after accepting [EXP-005/RUN-0001](runs/EXP-005-RUN-0001.md). The question is whether deferring only the keygen error-vector reduction improves on retained EXP-003. Keygen is the predicted beneficiary. Encap and decap retain their arithmetic counts and serve as operations without a predicted direct benefit. ACT-0014 now accepts the completed [RUN-0002 result](runs/EXP-005-RUN-0002.md). I preserve this original protocol separately from its outcome; RUN-0002 exists and must not be reused.

## Sources and gates

I use scripts/run_error_ntt_comparison.py with the existing timing harness, strict CSV parser, paired-effect calculation and assembly normaliser. The control is staged-invntt (EXP-003); the candidate is raw-error-ntt (EXP-005). I rebuild and time both in the same session. Historical EXP-003 durations are not substituted for fresh control measurements.

The runner restores 35 exact accepted EXP-003 files from source commit [cf8ae0dd700b](source_revisions.md) into the new run's ignored build/exp003-source directory, using read-only git show and checking every file against its accepted SHA-256. The current checkout/index and arithmetic stay in place. The current candidate must match EXP-005 validation source [5a499bd1940c](source_revisions.md). The new support/orchestration commit is recorded separately from both arithmetic identities.

Both variants use the same reviewed GCC executable and normal -O3 flags without counters or sanitizer. Before timing, the actual six executables must match all 24 reviewed function bodies: indcpa_keypair_derand, ntt, montgomery_reduce and barrett_reduce. Instruction offsets, operands, sizes and resolved symbolic targets remain part of the match; only relocation addresses are normalised. A mismatch stops the run and preserves its diagnostic record.

The accepted validation/review, tool hashes, source identities, support files, restored source, executable hashes and requested affinity are checked before and after collection. The formal run requires a clean Git-visible tree outside results/ and committed source/support/review. The runner creates a new run directory exclusively and invokes the metadata collector itself. A failed/interrupted run is preserved; any diagnosed retry receives a fresh ID.

## Protocol and interpretation

I keep five adjacent variant pairs per parameter, 100 warm-up and 1000 measured exchanges per process, seed 1, guest logical CPU 0 and CLOCK_MONOTONIC_RAW nanoseconds. Within each block, parameter order is 512/768/1024. EXP-003 runs first in blocks 1/3/5 and EXP-005 first in blocks 2/4; the three-versus-two order imbalance remains explicit.

The formal run records six builds, 24 assembly extractions and 30 timing processes: 60 steps, 120 raw streams and 90000 operation durations. Analysis produces 90 process summaries, 45 paired effects and nine aggregate rows. Warm-up, fixture generation, shared-secret comparison and CSV output occur outside measured intervals. Deterministic APIs exclude operating-system randomness. Repeated fixtures and inner observations are not independent experimental runs.

- Speedup = EXP-003 process median / EXP-005 process median; above one favours EXP-005.
- Time reduction (%) = 100 * (1 - EXP-005 process median / EXP-003 process median); positive means faster, negative means slower.
- I report the median paired effect, the observed pair minimum/maximum and both medians of process medians. The primary effect is the median of paired percentages, not a percentage computed from the two aggregate medians. The range is descriptive, not a confidence interval.

I inspect every pair, both order groups, absolute durations, timer diagnostics and effect consistency. I retain all encap/decap movements, including regressions. They cannot be credited to saved error-vector reductions because those operations do not execute keygen. Layout changes or environmental variability may affect all operations; this experiment does not identify their separate contributions. The keygen body/code and local-stack changes recorded in the assembly review also prevent attribution solely to Barrett-call cost.

I accept a performance benefit only when the validated candidate shows a consistent useful keygen reduction in the collected pairs, with the magnitude, order dependence and any other-operation tradeoffs documented. Small/mixed effects remain inconclusive; a slower result is retained. I subtract no timer overhead, remove no outliers and do not rerun merely to obtain a preferred outcome. Five pairs in one session do not establish formal significance or a universal gain. Unknown host/power/background/physical-core conditions stay unknown; guest affinity does not establish physical-core placement.

The correctness, range and scoped security conclusions remain those in RUN-0001. Performance timing is not a leakage test. Incremental effects are conditional on EXP-001/002/003 already being present. I do not add or multiply medians from separate sessions into a total gain over the original reference; that requires the separate [direct comparison](final_comparison.md).

## Recorded execution

The completed comparison used support commit [4bd813ed71a9](source_revisions.md); its results were archived in [eb4c34586c75](source_revisions.md). Historical invocation (new executions require a fresh run ID):

~~~bash
python3 -B scripts/run_error_ntt_comparison.py \
  --experiment EXP-005 \
  --run RUN-0002 \
  --cpu 0
echo $?
~~~

Optional environment fields record observed facts; unverified values remain unknown. ACT-0014 accepted the run after checking hashes, generated code, paired data and reproduced analysis. Failed or interrupted attempts remain preserved under their original IDs.

## Development check

[ACT-0013 support evidence](evidence/ACT-0013/error-ntt-comparison-smoke.json) records six real builds, 24 assembly matches and two short blocks of twelve measured exchanges and two warm-ups per process. All 432 operation rows, 36 summaries, eighteen pairs and nine aggregate rows pass, including both orders. Synthetic improvements/regressions confirm the sign, EXP-003/EXP-005 labels and median-of-paired-effects calculation. Changed source identities, wrong historical hashes, altered call/branch targets, wrong-variant assembly and missing/duplicate/unequal groups are rejected or fail matching.

The development check used an isolated temporary directory, mocked Git state/existence checks and exact historical bytes from SHA-1-verified objects. The validation snapshot supplied compiler/provenance test inputs; this was not formal collection. Short development timings check the pipeline and provide no thesis speed estimate. An initial synthetic branch fixture changed only an absolute relocation address, which the normaliser correctly ignores; I corrected the fixture to change the resolved symbolic target. No runner correction was needed. Temporary binaries and CSVs were removed after verification, with their commands/hashes recorded in the development evidence.
