# EXP-006 incremental timing comparison

I specify this protocol after accepting [EXP-006/RUN-0001](runs/EXP-006-RUN-0001.md). It asks whether omitting only the keygen dot's intermediate Barrett centring improves on retained EXP-005. Keygen is the predicted beneficiary; encap/decap have unchanged arithmetic and serve as control operations. The protocol was executed as RUN-0002 and reviewed in ACT-0016; the [complete result](runs/EXP-006-RUN-0002.md) records the mixed outcome and EXP-005 primary-candidate decision. The commands below preserve the historical execution procedure; RUN-0002 must not be reused.

## Sources and acceptance gates

I use scripts/run_keygen_dot_comparison.py with the existing normal-build timing harness, strict CSV parser, paired-effect calculation and assembly normaliser. The control is raw-error-ntt (EXP-005); the candidate is keygen-dot (EXP-006). Both are rebuilt and measured together. I do not reuse old EXP-005 durations as fresh controls.

The runner restores the exact 35 accepted EXP-005 source files from commit 4bd813ed71a90c7722275dc802336852214a5388 into the new run's ignored build/exp005-source directory using read-only git show, checking every file's SHA-256 against the accepted timing manifest. It does not alter the checkout/index. Reference manifest SHA-256 is 22cf2fcc0533c6e35a8063b6709b4d11cb391b742e0850cd0204d94bf0db6668. Current candidate arithmetic must match accepted validation source 4c9d539eba8903c2404591b8024e7afef15bbf47. The new support/orchestration commit is recorded separately.

Both variants use the same reviewed GCC executable and normal -O3 flags without counters or sanitizer. The actual six timing executables must match 33 reviewed bodies before measurement: keygen, general dot, poly_tomont and both reducers for both variants, plus the dedicated dot for EXP-006. Instruction offsets, operands, function sizes and resolved symbolic targets are retained; only relocation addresses are normalised. A mismatch stops the attempt and preserves diagnostics.

The accepted validation/review, reference manifest, tool/source/support hashes, restored files, executables and requested affinity are checked before and after measurement. Source/support/review must be committed and the tree clean outside results/. The runner creates a new run directory exclusively and invokes the metadata collector. Failed/interrupted attempts remain preserved and a diagnosed retry receives a fresh run ID.

## Measurement and interpretation

I retain five adjacent pairs per parameter, 100 warm-up exchanges, 1000 measured exchanges per process, fixture seed 1, guest logical CPU 0 and CLOCK_MONOTONIC_RAW nanoseconds. Within each block, parameters run in 512/768/1024 order. EXP-005 runs first in odd blocks and EXP-006 first in even blocks; the three-versus-two order imbalance is explicit.

The formal run has six builds, 33 assembly extractions and thirty timing processes: 69 steps, 138 raw streams and 90000 operation durations. Analysis produces ninety process summaries, 45 paired effects and nine aggregate rows. Fixture preparation, verification and CSV output occur outside measured intervals. Deterministic APIs exclude operating-system randomness. Repeated fixtures and inner observations are not independent experimental replications.

- Speedup = EXP-005 process median / EXP-006 process median; above one favours EXP-006.
- Time reduction (%) = 100 * (1 - EXP-006 process median / EXP-005 process median); positive means faster and negative means slower.
- I aggregate the median of paired effects and report observed pair extrema and both medians of process medians. Pair ranges are descriptive, not confidence intervals; the effect is not computed from the two aggregate medians.

I inspect all pairs, both order groups, absolute timings, timer diagnostics and regressions. I accept a performance benefit only if the validated candidate shows a consistent useful keygen reduction in these measurements with magnitude and tradeoffs stated. Small/mixed results remain inconclusive. Slower outcomes remain valid findings. I remove no outliers, subtract no timer overhead and do not rerun merely to obtain a preferred outcome.

The source-derived benefit is another K*256 fewer keygen Barrett calls; Montgomery and encap/decap counts stay unchanged. Encap/decap timing changes cannot be credited to the removed keygen reductions. Added code, altered keygen unrolling/calls, register use, layout and environment can influence the observed timings. These data cannot isolate the cost of one Barrett call. All control-operation regressions remain visible.

Five pairs from one session do not establish formal significance, a universal gain or order independence. Unknown host/power/background/physical-core facts stay unknown; WSL guest affinity does not guarantee physical-core placement. Incremental effects depend on earlier optimisations already being present and cannot be added or multiplied across separate runs into a total original-reference gain. The final direct and repeat-session evaluation remains separate. Performance measurements are not a leakage test.

## Review, commit, run and preserve

No further arithmetic change is required. I review and commit the new support and thesis records:

~~~bash
git diff --check
git add -- README.md scripts/run_keygen_dot_comparison.py \
  notes/project_log.md notes/experiment_register.md notes/reduction_map.md \
  notes/experiments/EXP-006-keygen-dot.md notes/runs/EXP-006-RUN-0001.md \
  notes/keygen_dot_timing.md notes/implementation_security.md \
  notes/practical_completion.md notes/literature.md notes/evidence/ACT-0015/
git diff --cached --check
git diff --cached --stat
git diff --cached
git commit -m "Review EXP-006 validation and add comparison against EXP-005"
git status --short
~~~

With a clean source/support tree, I run:

~~~bash
python3 -B scripts/run_keygen_dot_comparison.py \
  --experiment EXP-006 \
  --run RUN-0002 \
  --cpu 0
echo $?
~~~

Optional --host-os, --power-mode and --background-load arguments record observed facts; unknown values remain unknown. I keep workload and power conditions steady. RUN-0002 has not been created by the development check and must not be reused after an attempt.

After exit code zero and Comparison status: completed, I inspect and preserve the full result:

~~~bash
cat results/EXP-006/RUN-0002/derived/comparison.csv
git add -- results/EXP-006/RUN-0002/
git diff --cached --check
git diff --cached --stat
git commit -m "Record EXP-006 incremental timing comparison"
git status --short
~~~

A failed run is preserved for diagnosis instead of accepted by the success sequence. A completed run still needs review of hashes, actual generated code, all pairs and reproduced derived data before deciding whether to retain EXP-006 for performance.

## Development verification

[ACT-0015 support evidence](evidence/ACT-0015/keygen-dot-comparison-smoke.json) records six real builds, 33 exact reviewed-assembly matches and twelve short timing processes: two blocks, twelve measured exchanges and two warm-ups per process. All 432 operation rows, thirty-six summaries, eighteen pairs and nine aggregates pass. Both execution orders are covered. Synthetic gains/regressions verify direction, EXP-005/EXP-006 columns and median-of-paired-effects calculation. Missing/duplicate/unequal groups, wrong variants and altered source identities are rejected. Wrong historical hashes and changed symbolic call/branch targets, including a wrong dedicated-dot tail target, are detected.

I used an isolated temporary directory and mocked Git state/existence checks. Exact historical bytes came from SHA-1-verified stored objects; the existing validation snapshot supplied development compiler/provenance inputs only. No Git command, metadata collector, formal run or arithmetic edit occurred. The first smoke attempt stopped before building because the copied review filename still referred to EXP-005; I corrected it to the ACT-0015 EXP-006 review. The completed check passed and temporary binaries/CSVs were removed after their hashes and commands were recorded. These short measurements verify the runner and provide no thesis speed estimate.
