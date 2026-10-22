# EXP-001 matched timing comparison

I now have an unchanged baseline, an implemented candidate and accepted [candidate validation and assembly review](runs/EXP-001-RUN-0001.md). This run asks whether the reduction savings make complete KEM operations faster.

## Fixed starting protocol

I use scripts/run_comparison.py and the unchanged benchmarks/bench_kem.c. The runner builds both variants with the same reviewed GCC executable and normal -O3 flags. Counters and sanitizers are absent. It checks current source hashes against RUN-0001 and compares basemul and montgomery_reduce assembly in each timing binary with the reviewed instructions before collecting any timings.

For each of Kyber512, Kyber768 and Kyber1024:

- Five matched process pairs use the same logical CPU, compiler, flags and public fixtures.
- Each process performs 100 warm-up exchanges and 1000 measured exchanges. Keygen, encapsulation and decapsulation are timed separately.
- The order is baseline then candidate in blocks 1, 3 and 5, and candidate then baseline in blocks 2 and 4. Both members of each pair run consecutively.
- The outer loop is block, followed by parameter sets 512, 768 and 1024. Five blocks give three baseline-first and two candidate-first pairs per parameter set; this small order imbalance is explicit.
- Seed 1 and the existing SHAKE256 fixture rule are reused across variants and blocks. There are 1000 measured fixture indices per parameter set, not 5000 independent inputs.
- All observations are retained. No timer-overhead subtraction, outlier removal, selective retry or early stopping is used.

This produces 30 measured processes, 90000 operation durations, 90 per-process summary rows, 45 paired comparison rows and nine aggregate rows. It doubles the baseline pilot's observation count because it measures two implementations. This is a practical automated comparison budget, not 90000 manually designed tests. The prior pilot remains context; the primary comparison uses the freshly measured baseline in each pair.

The timer remains CLOCK_MONOTONIC_RAW in nanoseconds. Fixture generation, warm-up, CSV formatting and secret comparisons remain outside measured intervals. Deterministic APIs exclude operating-system randomness. These timings do not include invalid-ciphertext performance or establish timing-leakage resistance.

## Run and preserve

After reviewing and committing the support files and records, I launch from the repository root:

~~~bash
python3 -B scripts/run_comparison.py --experiment EXP-001 --run RUN-0002 --cpu 0
echo $?
~~~

I do not run the metadata collector separately. The runner reserves a fresh ID and refuses to overwrite existing records. I keep host activity and power conditions steady, avoiding heavy concurrent work. Optional --host-os, --power-mode and --background-load arguments record facts I can verify; otherwise those fields remain unknown. WSL guest CPU affinity cannot establish host physical-core placement or eliminate scheduling/frequency effects.

I accept the run only if exit code is zero, manifest status is completed, all steps exit zero, reviewed_assembly_match, measured_roundtrips, csv_integrity and provenance_recheck pass, and the recorded artifacts remain intact. A failed or interrupted attempt remains under its original ID; any retry uses a new ID after diagnosis. Source/flag/compiler changes invalidate the current validation/review match.

The runner preserves metadata, build commands, binary and source hashes, all assembly, raw CSVs, stderr and actual process order. If interrupted, raw partial output may remain a stdout.log. I do not edit raw results or the existing RUN-0001 manifest.

## Interpretation

I compare process medians within each parameter/operation/block:

- Speedup = baseline median / candidate median; values above 1 favour the candidate.
- Improvement (%) = 100 * (1 - candidate median / baseline median); positive values favour the candidate.

derived/process-summary.csv retains each process's median/minimum/maximum. derived/paired-comparison.csv retains every paired effect and which variant ran first. derived/comparison.csv reports the median paired effect and its observed minimum/maximum, alongside the two variants' medians of process medians.

The primary estimate is the median of the paired effects. It is not generally the ratio of the two medians of process medians. The minimum/maximum describe these five pairs; they are not confidence intervals. Inner timing rows and repeated processes may share input, thermal and scheduling conditions, so I do not treat them as independent experiments.

I will examine consistency across pairs and both orders before deciding whether the result supports improvement, regression or an inconclusive outcome. If an effect is small relative to variation or depends on order, I will report that and plan additional complete pairs if needed. I will not add repetitions simply to obtain a preferred result.

## Support verification

[Development evidence](evidence/ACT-0007/comparison-smoke.json) records six real builds and two short blocks with twelve exchanges per process. All 432 operation rows passed; all twelve function assembly comparisons matched. Known synthetic improvement/regression pairs verified effect direction and aggregation. Missing variants, duplicate groups, unequal sample counts and a changed source hash were rejected.

The development run used temporary files, bypassed Git-state checks through mocks and did not invoke the metadata collector. It is support verification, not a committed benchmark or evidence of a speedup. Formal execution and its clean-source checks remain pending RUN-0002.
