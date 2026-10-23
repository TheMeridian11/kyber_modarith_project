# Baseline reduction counting

I use benchmarks/count_reductions.c and scripts/run_counts.py to count Montgomery and Barrett reduction-function invocations during key generation, encapsulation and valid-ciphertext decapsulation. This is a separate instrumented build; it produces no performance measurements.

## How the counters work

I use GNU linker's --wrap option to redirect references to each namespaced reduction function through a small wrapper. The wrapper increments a uint64_t counter and calls the original function with the original argument and return type. The original Kyber source files remain unchanged.

The [GNU linker documentation](https://sourceware.org/binutils/docs/ld/Options.html) specifies that --wrap redirects undefined symbol references. Calls resolved within the defining translation unit are not intercepted. In this pinned source, callers are outside reduce.c, and reduce.c contains the two reduction definitions without calls between them. Separate compilation with -fno-lto preserves this instrumentation boundary. If a later treatment moves, replaces or inlines a reduction, I must revisit counter coverage.

The executable first checks that one direct call to each reducer increments the corresponding counter once. I then reset both counters immediately before each KEM operation and capture them immediately afterwards. Fixture generation, wrapper checks, output formatting and shared-secret comparison are excluded from per-operation counts. Decapsulation includes its re-encryption work.

## Protocol

| Item | Choice |
|---|---|
| Source | Unchanged pinned baseline |
| Parameters | Kyber512, Kyber768, Kyber1024 |
| Inputs | Same derand-shake256-v1 fixture rule as the timing harness, phase 1, seed 1 |
| Exchanges | 10 per parameter set, one process per parameter set |
| Measurements | Three operation rows per exchange; 90 rows in total |
| Outputs | Three raw CSV files and nine generated summary rows |
| Build | Existing explicit GCC flags plus -fno-lto and two namespaced --wrap options |
| Timing | No timer, warm-up, CPU affinity requirement or speed interpretation |

Ten distinct fixture indices provide a small check of the fixed-loop prediction. Thousands of repetitions would add little information about these counts. Count constancy across this sample is not proof of constant-time execution.

I compare observations with the source-derived table in [EXP-000](experiments/EXP-000-baseline.md). Predictions are stored separately from observations. A mismatch, changing count, malformed CSV or failed exchange stops acceptance and preserves the raw evidence for investigation.

The C harness computes observations without using the predicted totals. The Python summary reports observed calls per operation after checking consistency across fixtures. Function invocations are not instruction counts, and fewer calls do not guarantee a runtime improvement.

## Recorded execution

The accepted RUN-0004 used the command below. I use a new run ID for any further execution:

~~~bash
python3 -B scripts/run_counts.py --experiment EXP-000 --run RUN-0004
echo $?
~~~

The runner invokes the existing metadata collector itself. I do not reserve this ID separately. A previously used ID is refused; failed or interrupted attempts retain their files and any retry receives a new ID.

A successful run has exit code 0, manifest status completed, all three checks.reduction_counts entries pass, provenance_recheck pass and all six build/count steps completed with exit code 0. Those per-parameter checks cover CSV structure, complete exchanges, fixed counts and agreement with the predictions. Arithmetic-safety and timing-behaviour checks remain not-run.

The run directory contains metadata.json, manifest.json, raw/counts-512.csv, raw/counts-768.csv, raw/counts-1024.csv, build/count stderr/stdout logs and derived/summary.csv. Rebuildable executables remain ignored under build/. Source, support, compiler, binary and data hashes connect the observations to their implementation.

## Development check

I compiled all three parameter sets and ran two fixture exchanges each: 18 operation rows in total. All wrapper self-checks, exchanges and source-derived count predictions passed. Zero iterations was rejected, and the parser rejected a missing row, a failed exchange flag and an incorrect reduction count.

[Retained development evidence](evidence/ACT-0005/counts-smoke.json) contains the exact source hashes, compile commands, raw observations and check outcomes. This is a check of uncommitted support files, not the committed RUN-0004. The recorded baseline orchestration was subsequently accepted as RUN-0004 in ACT-0006.

## Subsequent experiments

The accepted [RUN-0004 baseline](runs/EXP-000-RUN-0004.md) supplies the original counts for the later arithmetic trials. [EXP-001](experiments/EXP-001-fused-basemul.md) first reduced base multiplication from five to three Montgomery calls per coefficient pair. Each trial then paired its bounds, compatibility and count checks with a fresh uninstrumented timing comparison. The [final comparison](final_comparison.md) measures cumulative effects directly against the original.
