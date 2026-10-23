# EXP-009 — Closing original/EXP-003/EXP-005 comparison

## Question and decisions fixed before measurement

I measure the cumulative effect of EXP-003 and EXP-005 against the original pinned reference, and the additional effect of EXP-005 against EXP-003. I use direct matched measurements rather than adding or multiplying incremental percentages from earlier sessions. EXP-005 remains provisional; EXP-003 is an explicit comparator/fallback. EXP-006 remains an adverse/secondary result and the production checkout remains unchanged.

I reuse the accepted functional, invalid-input, range, narrowing and UBSan evidence for identical source files. EXP-007 supplies bounded branch/address evidence for original/EXP-005/EXP-006; EXP-008 supplies separate statistical evidence for original/EXP-003/EXP-005. Neither establishes whole-KEM constant time, physical side-channel resistance or certification. The inherited general-dot local-canary tradeoff remains relevant to both EXP-003 and EXP-005. I check the final benchmark's actual normal-code bodies before collecting times.

The machine-readable [protocol](../../tests/final_comparison_protocol.json) pins all evidence inputs. The [runner](../../scripts/run_final_comparison.py) restores 35 exact historical files for each candidate into the ignored build directory. It compares 108 extracted function bodies with accepted normal assembly, including key generation, all changed arithmetic kernels, reducers and IND-CPA decryption. All production arithmetic remains user-applied. The existing benchmark is unchanged.

## Finite collection protocol

- I launch three sessions separately, each with a new run ID and a fresh build. A session is one complete invocation, not three labels applied to one pooled run. I allow a genuine break between invocations and record comparable power/background conditions. Separate launches on one host are not independent machines or proof of statistical independence.
- Each session has 12 matched blocks per parameter set. All six orders of original/EXP-003/EXP-005 occur twice for each parameter, and each variant occupies each position four times. Parameter order rotates across blocks. This replaces the earlier provisional ten-pair idea because three variants have six possible orders.
- I collect 1000 measured KEM exchanges after 100 warm-up exchanges in each process: one keygen, encapsulation and decapsulation duration per exchange. There are 108 measurement processes, 108000 exchanges and 324000 duration rows per session; three sessions retain 972000 duration rows. Warm-up is additional and unrecorded as timing data.
- Session base seeds are 1, 2027 and 4051. The block seed is base + block - 1. Each triplet uses identical deterministic fixtures; blocks and sessions use distinct seeds. Fixture generation, output checking and buffered CSV output stay outside operation timing intervals.
- I retain CLOCK_MONOTONIC_RAW nanoseconds, normal GCC 13.3.0 flags and logical CPU 0 affinity. These are operation durations, not TSC ticks or core cycles. Operating-system random generation is excluded by deterministic APIs. WSL affinity does not prove physical-core placement or fixed frequency.
- I retain every duration without subtracting timer overhead or trimming outliers. The harness checks every warm-up and measured shared-secret round trip. Diagnostics, source/support/tool/binary hashes, metadata and the complete order are archived.
- Any failed build, changed identity, unexpected assembly, functional error, malformed output or interruption makes the attempt unusable. I retain it, document the cause, then use a new run ID for the same session. A completed session cannot be silently replaced. I do not extend or repeat collection because an effect is disappointing.

## Analysis and candidate decision

For each operation/parameter/block I calculate the process median, then paired speedup = reference median / candidate median and time reduction = 100 * (1 - candidate/reference). Positive means faster. I report all three contrasts and all nine operation/parameter groups, including unchanged-operation movements and regressions.

Each session reports the median of its 12 paired effects, all individual effects, order and observed range. The three-session analysis shows each session estimate, their median and descriptive range, with sign consistency. I do not count the inner 1000 observations as 1000 independent experiments. The range is not a confidence interval; three sessions provide limited evidence about broader conditions. No arbitrary aggregate workload score or total-gain calculation from old incremental results is used.

I judge the cumulative benefit and EXP-005's marginal benefit by size, repeatability, adverse operations and the documented security/code/stack tradeoffs. Direction agreement across three sessions is descriptive support, not a significance test. If EXP-005's small marginal advantage is inconsistent or accompanied by material regressions, I retain that uncertainty and may prefer the simpler EXP-003 closing candidate. I will not declare a universal winner from favourable cells alone. The final choice is a documented interpretation after all predeclared sessions, not an automatic score.

## Manual execution after reviewing and committing ACT-0018

I first commit the accepted EXP-008/RUN-0001 results and all ACT-0018 support. Exact staging commands are in the [Git handoff](../git_handoff.md). A clean tree outside results/ is required. I execute session 1:

```sh
python3 -B scripts/run_final_comparison.py --experiment EXP-009 --run RUN-0001 --session 1 --cpu 0
echo $?
```

I retain and inspect completion before the next session. After a break under comparable conditions, I launch these separately, without changing support or arithmetic:

```sh
python3 -B scripts/run_final_comparison.py --experiment EXP-009 --run RUN-0002 --session 2 --cpu 0
echo $?
```

```sh
python3 -B scripts/run_final_comparison.py --experiment EXP-009 --run RUN-0003 --session 3 --cpu 0
echo $?
```

I can supply accurate `--host-os`, `--power-mode` and `--background-load` strings; otherwise these remain explicitly unknown. I keep unrelated workloads quiet for each session. If a run fails, I preserve it and use the next unused run ID with the same session number. Subsequent run IDs then advance accordingly.

After all three successful sessions, the analysis independently re-reads the raw CSVs and reproduces every per-session table before combining session estimates:

```sh
python3 -B scripts/analyse_final_comparison.py   --runs results/EXP-009/RUN-0001 results/EXP-009/RUN-0002 results/EXP-009/RUN-0003   --output analysis/final-comparison-EXP-009
```

If retries changed run IDs, I name the actual three successful runs. The output directory must be new. Failed attempts remain in the record; I request a final audit and graph generation before selecting the closing candidate. These commands are prepared, not executed formal results.
