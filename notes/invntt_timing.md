# EXP-003 incremental timing comparison

This comparison followed acceptance of [EXP-003/RUN-0001 correctness, counts and assembly](runs/EXP-003-RUN-0001.md). The [accepted RUN-0002 review](runs/EXP-003-RUN-0002.md) records consistent encap/decap benefit and small keygen tradeoffs. This document preserves the protocol specified before measurement, conditional on retained earlier optimisations.

## Sources and acceptance gate

scripts/run_invntt_comparison.py reuses the existing timing harness, CSV checks, paired-effect calculation and assembly normaliser. The control is wide-dot (EXP-002); the candidate is staged-invntt (EXP-003). Both are freshly built and timed in the same session. Previously recorded EXP-002 durations are not the control measurements for this run.

The runner restores 35 accepted EXP-002 files from source commit [a32a81d12225](source_revisions.md) into the new run's ignored build/exp002-source directory using read-only git show. Every byte sequence must match the accepted EXP-002 manifest's SHA-256. This preserves the current arithmetic and Git checkout/index. The current candidate must match EXP-003/RUN-0001 source hashes, validated at [9ec22141e6ac](source_revisions.md). The new orchestration/support source commit is recorded separately from these treatment identities.

Both variants use the same GCC executable and normal -O3 flags as the reviewed evidence, with no counters or sanitizer in the timing builds. Before any timing, invntt, Montgomery and Barrett assembly from all six actual timing executables must match ACT-0011: eighteen function comparisons. The normaliser retains instruction offsets, operands, sizes and symbolic targets while resolving code/data addresses. A changed stage constant, branch target or variant fails the match. The runner preserves the failed attempt rather than continuing measurement.

The formal run requires committed support/review/source and a clean Git-visible tree outside results/. Source, tools, restored files, support, evidence, executable hashes and selected affinity are checked before and after collection. Any failed/interrupted attempt retains its record and gets a new ID for a diagnosed retry. No result directory is overwritten.

## Fixed protocol and interpretation

I retain the [paired protocol](paired_timing.md) and the same practical budget as EXP-001 and EXP-002: five adjacent pairs per parameter set, 100 warm-up and 1000 measured exchanges per process, seed 1, guest logical CPU 0 and CLOCK_MONOTONIC_RAW nanoseconds. Parameter order is 512/768/1024 inside each block. EXP-002 runs first in blocks 1/3/5 and EXP-003 first in blocks 2/4; the three-versus-two order imbalance remains explicit.

This produces 30 measured processes and 90000 operation durations, 90 process summaries, 45 paired effects and nine aggregate rows. Including six builds and eighteen assembly extractions gives 54 recorded steps. Warm-up, fixture generation, shared-secret checks and CSV formatting are outside each measured interval. Deterministic APIs exclude operating-system randomness. The fixture sequences repeat across blocks; inner observations are not independent experiments.

- Speedup = EXP-002 process median / EXP-003 process median; values above one favour EXP-003.
- Time reduction (%) = 100 * (1 - EXP-003 process median / EXP-002 process median); positive values favour EXP-003 and negative values are regressions.
- Each aggregate reports the median paired effect and its observed minimum/maximum, plus both medians of process medians. The primary effect is not calculated from those two aggregate medians. The range is descriptive, not a confidence interval.

Analysis considers all pairs, both order groups, absolute durations, timer diagnostics and effect size/consistency. Encapsulation and decapsulation are the predicted beneficiaries. Key generation does not call the inverse transform; its measurements help reveal noise, shared-environment or code-layout effects and cannot be credited to removed inverse-transform calls. A large keygen change would need explanation, not selective exclusion.

No overhead subtraction, outlier deletion or retry to obtain a preferred outcome is permitted. I retain mixed or negative findings and keep small effects inconclusive where warranted. Unknown host/power/background/physical-core conditions remain unknown; guest affinity does not prove physical placement. I keep workload and power conditions steady and record observed manual facts with the optional arguments. Five pairs in one session support a bounded observation, not a universal guarantee or formal significance claim.

The earlier correctness/security limits remain, including centred inputs and the inherited dot-product hardening tradeoff. These speed measurements are not leakage tests. Reductions, loop splitting, local stack use and layout jointly change; their separate timing contributions are not identified. I do not add or multiply medians from different experimental runs to claim a total original-reference improvement; that is supplied by the separate [final direct comparison](final_comparison.md).

## Execute and preserve

Historical invocation (new executions require a fresh ID):

~~~bash
python3 -B scripts/run_invntt_comparison.py --experiment EXP-003 --run RUN-0002 --cpu 0
echo $?
~~~

The runner invokes the metadata collector itself. Optional --host-os, --power-mode and --background-load values describe observed facts. The ACT-0011 support check created no formal run; the subsequently completed RUN-0002 was verified in ACT-0012.

ACT-0012 accepted the completed run after reviewing saved hashes, assembly, all timing rows, provenance and reproduction of the derived analysis. Failed or interrupted attempts retain their evidence and require a fresh ID for any retry.

## Development check

[ACT-0011 support evidence](evidence/ACT-0011/invntt-comparison-smoke.json) records six real builds, eighteen assembly matches and two short blocks with twelve measured exchanges and two warm-ups per process. All 432 operation rows, 36 summaries, eighteen pairs and nine aggregates pass, including both execution orders. Synthetic improvements and regressions confirm direction, EXP-002/EXP-003 columns and median-of-paired-effects aggregation. Changed source identities, wrong historical hashes, changed stage/branch targets, wrong-variant assembly and incomplete/duplicate/unequal groups were rejected or failed matching.

I used temporary files and mocked Git state/existence checks; historical bytes came from verified stored objects. Historical-source retrieval and exact-byte handling were checked with a mocked subprocess; this was a development check, not a formal timing run. This checks the support path without repeating full validation; its development timings are excluded from performance findings.
