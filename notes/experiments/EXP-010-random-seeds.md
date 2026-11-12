# EXP-010 — Random-seed performance follow-up

## Question and status

Does the measured benefit of the original-to-EXP-003 and original-to-EXP-005 comparisons persist across a wider, randomly selected collection of input fixtures on the same platform? The direct EXP-003-to-EXP-005 contrast also retains the small additional benefits and regressions relevant to candidate selection.

This is a planned follow-up to the completed EXP-009 study. Collection has not yet begun. The selected EXP-005 arithmetic, the original comparison source and the existing C benchmark remain unchanged. EXP-009's accepted estimates and figures remain the original closing result; EXP-010 is reported separately, without pooling the two studies. The purpose is performance robustness, not a new optimisation search or timing-leakage assessment.

## Sampling and fixed collection budget

The [protocol](../../tests/random_seed_protocol.json) pins a [saved seed and order plan](../../tests/random_seed_plan.json). Before any measurements, 60 distinct unsigned 64-bit values were drawn using Python's OS-backed `secrets.SystemRandom`, excluding the previously used EXP-009 block seeds. Decimal strings retain every seed bit in JSON and CSV readers. The saved list defines the experiment and is not regenerated after inspecting results.

Five sessions are launched separately, each with 12 matched blocks for each of Kyber512, Kyber768 and Kyber1024. A block uses one new seed shared by the original, EXP-003 and EXP-005. The benchmark encodes the parameter set, warm-up/measurement phase, seed and iteration in its SHAKE256 fixture. Thus every exchange receives fresh deterministic inputs, and the implementations within a block receive identical fixtures. Fixture generation is outside the operation timing windows; operating-system random-generation cost is excluded.

For each session and parameter, all six variant orders occur exactly twice. These 12 orders were shuffled before measurement and saved in the plan. Every variant occupies each position four times. Parameter order rotates across blocks. New seeds vary between blocks and sessions, not between implementations within a comparison. All variants use the same 100 warm-up and 1000 measured exchanges per process.

There are 108 measurement processes per session, 540 across five sessions, 540000 measured exchanges and 1620000 retained operation-duration rows. Another 54000 warm-up exchanges are checked but do not enter the timing tables. Timings use CLOCK_MONOTONIC_RAW nanoseconds, guest logical CPU 0 and the accepted GCC 13.3.0 normal build flags. The compiler/disassembler hashes and 108 extracted function bodies must match the accepted build evidence in every session. The runner checks all 35 selected working-source files and restores exact historical candidates only inside each run's ignored build directory.

The five-session budget is a practical predeclared budget, not a power calculation or guarantee of precision. Separate launches on one WSL machine do not establish independence or cross-platform performance. Breaks, power mode, background activity and relevant physical/thermal observations should be recorded using the runner's metadata options. Unknown conditions remain explicitly unknown.

## Retention and analysis

All durations are retained; no timer overhead is subtracted and no outliers are removed. The benchmark checks every warm-up and measured shared-secret round trip. Build diagnostics, mismatched source/tool/assembly identities, malformed data, failed round trips or interruption invalidate the whole attempt. Failed attempts remain archived. A retry uses a new run ID and the same planned session seeds/order. A completed session cannot be replaced and the budget is not extended because an effect is disappointing. A collection lock prevents simultaneous sessions.

For every operation and parameter, the process median is calculated from its 1000 timings. Within each matched block, time reduction is `100 * (1 - candidate_median / reference_median)` and speedup is `reference_median / candidate_median`. Positive reduction means faster. The session estimate is the median of 12 paired effects. The five-session summary is the median of those five estimates, with their observed range and signs. Inner observations are not treated as independent experiments. All three direct contrasts and all nine operation/parameter groups are reported.

The analyser independently rereads raw CSVs, checks seeds, order, diagnostics and all retained output hashes, recomputes normalised assembly, and reproduces the per-session derived tables before combining them. It requires exactly five distinct successful sessions with matching source, support, protocol and tool identities. It rejects development records. Ignored executables are not required for retained-data analysis; their build commands and hashes remain in the manifests.

## Dot-and-box figures

The primary figure has nine panels: parameter sets by operation. Each panel compares EXP-003 and EXP-005 against the original. A second figure shows the direct EXP-005-versus-EXP-003 effects on its own scale, so small adverse changes remain visible.

Every dot is one matched block effect; colour and shape identify the session. Horizontal offsets are fixed by session and block solely for visibility. A box spans the middle 50% of all 60 block effects, using inclusive linearly interpolated quartiles; its line is the pooled block median and its whiskers show the entire observed minimum-to-maximum range. All observations remain visible, including points at the extremes. The black diamond is the median of five session medians, which can differ from the box's pooled median. A zero line separates observed improvements and regressions. No box, whisker or range is a confidence interval.

The measured spread combines input variation and changing measurement conditions. Since each seed is used in one matched block, this design does not separately estimate a causal seed effect or isolate input-only variance. All parameter groups share the block seeds, and the three contrasts share measurements; they are not independent datasets. This Monte Carlo-style random-input experiment does not establish whole-program constant time, a universal speedup or final ML-KEM conformance.

Exports include SVG/PDF, 300-dpi PNG, every plotted paired effect, explicit box statistics, session-based summaries and input/code/output hashes. Figure generation revalidates the five raw-data runs and refuses existing output directories.

## Execution in Ubuntu/WSL

Commit the new support, plan and documentation before collecting formal results. The metadata collector requires a clean Git-visible tree outside results/. Do not change support or arithmetic between sessions.

The preflight is read-only and does not run benchmarks or Git commands:

```sh
python3 -B scripts/run_random_seed_comparison.py --check
```

Launch the following commands separately, inspecting completion and allowing a break under comparable conditions between sessions. These are not a shell loop. Each command should finish with `completed` and exit code zero.

```sh
python3 -B scripts/run_random_seed_comparison.py --run RUN-0001 --session 1 --cpu 0
echo $?
```

```sh
python3 -B scripts/run_random_seed_comparison.py --run RUN-0002 --session 2 --cpu 0
echo $?
```

```sh
python3 -B scripts/run_random_seed_comparison.py --run RUN-0003 --session 3 --cpu 0
echo $?
```

```sh
python3 -B scripts/run_random_seed_comparison.py --run RUN-0004 --session 4 --cpu 0
echo $?
```

```sh
python3 -B scripts/run_random_seed_comparison.py --run RUN-0005 --session 5 --cpu 0
echo $?
```

Accurate optional fields are `--host-os`, `--power-mode`, `--background-load` and `--session-note`. The session note can record the preceding break and any physical-core/thermal observations actually available. Do not guess these values. If an attempt fails, retain it, investigate the cause and retry that same session with the next unused run ID. Adjust the run paths below accordingly. Do not remove a collection lock until verifying that no collection process is active; a forced kill may leave a stale lock.

After all five sessions succeed:

```sh
python3 -B scripts/analyse_random_seed_comparison.py \
  --runs results/EXP-010/RUN-0001 results/EXP-010/RUN-0002 \
         results/EXP-010/RUN-0003 results/EXP-010/RUN-0004 results/EXP-010/RUN-0005 \
  --output analysis/random-seed-EXP-010
```

Install the existing pinned plotting requirements into a temporary directory if needed. This works with the available WSL pip even when the optional venv package is absent, and does not modify system Python:

```sh
python3 -m pip install --target /tmp/kyber-exp010-plot-deps -r analysis/requirements-figures.txt
PYTHONPATH=/tmp/kyber-exp010-plot-deps python3 -B analysis/build_random_seed_figures.py \
  --runs results/EXP-010/RUN-0001 results/EXP-010/RUN-0002 \
         results/EXP-010/RUN-0003 results/EXP-010/RUN-0004 results/EXP-010/RUN-0005 \
  --output analysis/figures/EXP-010
```

Analysis and figure output directories must be new. For later reproduction use another output directory. The comparison and conclusion are updated only after reviewing the actual five-session observations; support tests and synthetic plot checks are not EXP-010 results.
