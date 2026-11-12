# Thesis figures, tables and reproduction

## Choosing figures for the thesis

Use the completed three-session comparison (EXP-009) for the main performance results and the choice between EXP-003 and EXP-005. The arithmetic and security figures explain how the changes were developed and checked. The five-session random-seed follow-up (EXP-010) provides an additional check of those findings using the same implementations. The preliminary first-session plot remains part of the research record.

| Purpose | Recommended figure |
|---|---|
| Main comparison of the original, EXP-003 and EXP-005 | [Three-session estimates (PDF)](../analysis/figures/ACT-0020/exp009-three-session-effects.pdf) |
| Additional benefit and costs of selecting EXP-005 over EXP-003 | Bottom contrast row of the [three-session estimates (PDF)](../analysis/figures/ACT-0020/exp009-three-session-effects.pdf) and [code/local-stack costs (PDF)](../analysis/figures/ACT-0020/exp005-keygen-tradeoffs.pdf) |
| Arithmetic motivation and research progression | [Reduction counts (PDF)](../analysis/figures/ACT-0016/reduction-counts.pdf) and [incremental effects (PDF)](../analysis/figures/ACT-0016/incremental-effects-overview.pdf) |
| Bounded security findings | [Secret-flow coverage (PDF)](../analysis/figures/ACT-0017/exp007-secret-flow.pdf) and [timing-screen diagnostics (PDF)](../analysis/figures/ACT-0018/exp008-timing-screen.pdf) |

For the supplementary random-input check, use the dot-and-box plots of [both candidates against the original (PDF)](../analysis/figures/EXP-010/exp010-original-reference-dot-box.pdf) and the [direct candidate contrast (PDF)](../analysis/figures/EXP-010/exp010-direct-candidate-dot-box.pdf). Present these after the main results, with their separate interpretation of which findings repeated and which small differences were less consistent.

PDF is the usual thesis export; SVG and 300-dpi PNG alternatives, plotted data and provenance are linked below. Tables preserve unrounded values; display labels are rounded. When adapting a figure, keep the slower or mixed outcomes and the limits explained in its caption. [Reproduction commands](#reproduce) generate fresh copies without replacing accepted artifacts.

## ACT-0016 incremental measurements and counts

| Figure | Vector exports | Raster preview | Supporting data |
|---|---|---|---|
| EXP-006 paired effects | [PDF](../analysis/figures/ACT-0016/exp006-paired-effects.pdf), [SVG](../analysis/figures/ACT-0016/exp006-paired-effects.svg) | [PNG](../analysis/figures/ACT-0016/exp006-paired-effects.png) | [All 45 pairs](../analysis/figures/ACT-0016/exp006-paired-effects.csv) |
| Incremental results across experiments | [PDF](../analysis/figures/ACT-0016/incremental-effects-overview.pdf), [SVG](../analysis/figures/ACT-0016/incremental-effects-overview.svg) | [PNG](../analysis/figures/ACT-0016/incremental-effects-overview.png) | [45 parameter/operation/experiment groups](../analysis/figures/ACT-0016/incremental-effects.csv) |
| Modular-reduction counts | [PDF](../analysis/figures/ACT-0016/reduction-counts.pdf), [SVG](../analysis/figures/ACT-0016/reduction-counts.svg) | [PNG](../analysis/figures/ACT-0016/reduction-counts.png) | [54 count groups](../analysis/figures/ACT-0016/reduction-counts.csv) |

ACT-0017 corrects trailing whitespace in the three initial SVG files and updates their provenance. The original PNG/PDF/CSV bytes and all 22 data inputs are unchanged. The [original provenance](evidence/ACT-0017/figure-provenance-before-correction.json) is retained, and [correction evidence](evidence/ACT-0017/figure-review.json) records old/new hashes. The ACT-0016 whitespace check omitted SVG files, so its broad passing statement was incomplete. The generator now canonicalises SVG line endings, and the final check includes SVG.

The [provenance manifest](../analysis/figures/ACT-0016/provenance.json) records 22 input file hashes, analysis-code identity, package versions and all output hashes. [The input index](../analysis/figure_inputs.json) pins the original manifests/CSV files. All five timing comparisons use RUN-0002; original counts use EXP-000/RUN-0004, and implemented-variant counts use their RUN-0001 validation manifests. The [EXP-006 review](runs/EXP-006-RUN-0002.md) records raw-data reconstruction and source/build provenance. Earlier timing reviews remain linked in the experiment register.

## Draft captions and interpretation

**Paired effects.** The figure compares EXP-006 with a freshly built EXP-005 in five adjacent process pairs per parameter. Each point is 100*(control process median - candidate process median)/control process median; positive values indicate less time. Circles and squares distinguish execution order. Black ticks mark medians and horizontal segments show observed minimum and maximum, not confidence intervals. Warm-up is 100 exchanges and measurement is 1000 exchanges per process, under the recorded GCC/WSL guest-CPU-0 setup. All Kyber512 pairs regress, whereas Kyber1024 keygen improves in every pair. This is a single-session performance result, not a leakage test.

**Incremental overview.** The figure shows the median of five paired time reductions for each implemented experiment relative to its stated immediate predecessor; EXP-001 uses the original reference. Each column comes from its own matched session. The underlying table also retains extrema and positive-pair counts. Each effect measures a change on top of the preceding implementation. I cannot add or multiply these effects to claim a total gain over the original baseline. The heatmap summarises magnitude/direction, not statistical significance or uncertainty. EXP-004 is absent because no separate interaction experiment was executed, not because a result was removed.

**Reduction counts.** The figure shows observed Montgomery and Barrett calls per complete keygen, encapsulation and decapsulation operation in the separate instrumented builds. Each group contains ten deterministic fixtures with agreeing counts. Stage labels identify actual cumulative implementations, with the original reference shown separately. Lines connect discrete implementation stages. They are not a calendar-time trend. Function-call savings are not instruction counts, proportional speed predictions or security evidence. EXP-006 remains visible even though it was not adopted as the general final candidate.

## ACT-0017 formal secret-flow coverage figure

[PDF](../analysis/figures/ACT-0017/exp007-secret-flow.pdf), [SVG](../analysis/figures/ACT-0017/exp007-secret-flow.svg), [PNG](../analysis/figures/ACT-0017/exp007-secret-flow.png), [99 marked-mode process outcomes](../analysis/figures/ACT-0017/exp007-secret-flow.csv), [provenance](../analysis/figures/ACT-0017/provenance.json). The rendering was visually reviewed.

**Caption.** The figure shows marked-mode outcomes for eight target path/operand-role cases and three controls across original/EXP-005/EXP-006 and all parameter sets. All 72 target processes and nine negative controls are quiet. All nine branch and nine address positive controls are detected. Each target process exercises eight fixtures, with 128 pairs per basemul fixture. The 99 defined twins are also quiet and retained in the raw run. Colour shows whether the observed outcome matches what was expected. It is not a numerical security rating. Quiet means no marked-secret branch/address dependency observed on the exercised paths. This is neither a statistical timing result nor whole-program constant-time proof.

## ACT-0018 formal timing-screen diagnostics

[PDF](../analysis/figures/ACT-0018/exp008-timing-screen.pdf), [SVG](../analysis/figures/ACT-0018/exp008-timing-screen.svg), [PNG](../analysis/figures/ACT-0018/exp008-timing-screen.png), [all 1944 statistics](../analysis/figures/ACT-0018/exp008-timing-screen.csv), [provenance](../analysis/figures/ACT-0018/provenance.json). The PNG was visually reviewed and all five outputs independently regenerated byte-for-byte.

**Caption.** The figure shows the maximum absolute Welch statistic for each target path and implementation/parameter combination in EXP-008/RUN-0001. Each cell covers two synthetic profiles, two process repetitions, two fixed looks and three views (24 statistics). No target statistic exceeds the diagnostic threshold set before collection 10. Every process retains 50000 analysis observations plus 2000 calibration observations. The lower panel shows each negative control's maximum across its six statistics, and each deliberate positive control's final uncropped mean statistic, matching their acceptance rules. All 18 positives are detected and all 18 negatives are quiet. Timing uses TSC ticks. These are bounded empirical observations, not calibrated family-wise inference, tiny-leak sensitivity guarantees, an implementation ranking or a whole-program constant-time proof.

## ACT-0019 preliminary direct-performance figure

[PDF](../analysis/figures/ACT-0019/exp009-session1-effects.pdf), [SVG](../analysis/figures/ACT-0019/exp009-session1-effects.svg), [PNG](../analysis/figures/ACT-0019/exp009-session1-effects.png), [all 324 plotted pairs](../analysis/figures/ACT-0019/exp009-session1-effects.csv), [provenance](../analysis/figures/ACT-0019/provenance.json). The [review](evidence/ACT-0019/figure-review.json) records visual inspection and byte-for-byte reproduction of all five outputs. Use the complete three-session figure for the closing result.

**Caption.** The figure shows the direct original-to-EXP-003, original-to-EXP-005 and EXP-003-to-EXP-005 time reductions for EXP-009/RUN-0001, session 1 of the three sessions planned before collection. Each dot is a within-block comparison of process medians, each based on 1000 operation timings. Diamonds show medians of 12 paired effects; horizontal spans show their observed ranges, not confidence intervals. The three parameter sets and all operations are shown, including mixed and negative effects. Positive means faster. The top two comparison rows share a scale; the bottom row expands the marginal effects. Point jitter follows block order only to improve visibility and has no numerical meaning. No durations are excluded. These single-host WSL results are preliminary. No cross-session repeatability or final candidate ranking is established here.

## ACT-0020 final three-session and tradeoff figures

These completed results support the closing comparison. The [provenance](../analysis/figures/ACT-0020/provenance.json) identifies inputs and outputs; the [review](evidence/ACT-0020/figure-review.json) records inspection of all three renderings and byte-for-byte reproduction of thirteen files. The [complete result](final_comparison.md), [candidate rationale](final_candidate.md) and [security matrix](final_security_summary.md) provide the interpretation. Cumulative effects are measured directly, not assembled from earlier incremental percentages.

### Three session estimates

[PDF](../analysis/figures/ACT-0020/exp009-three-session-effects.pdf), [SVG](../analysis/figures/ACT-0020/exp009-three-session-effects.svg), [PNG](../analysis/figures/ACT-0020/exp009-three-session-effects.png), [81 session estimates](../analysis/figures/ACT-0020/exp009-three-session-effects.csv).

**Caption.** The figure compares original-to-EXP-003, original-to-EXP-005 and EXP-003-to-EXP-005 operation-time reductions for Kyber512/768/1024 across all three predeclared EXP-009 sessions. A coloured marker is one session's median of 12 within-block effects, each calculated from two process medians of 1000 timings. The black diamond is the median of those three session estimates. The horizontal span is their observed range, not a confidence interval. Positive means faster. All adverse operation/parameter groups are shown. The first two contrast rows share a scale, and the bottom row expands the marginal effects. Vertical marker offsets improve visibility and carry no numerical meaning. These three separate invocations on one WSL host do not establish independent-host performance or population significance.

### Complete paired spread

[PDF](../analysis/figures/ACT-0020/exp009-all-paired-effects.pdf), [SVG](../analysis/figures/ACT-0020/exp009-all-paired-effects.svg), [PNG](../analysis/figures/ACT-0020/exp009-all-paired-effects.png), [all 972 paired effects](../analysis/figures/ACT-0020/exp009-all-paired-effects.csv).

**Caption.** The figure shows every paired effect across 12 matched blocks per parameter in each of the three sessions. Colours/shapes identify sessions; slight vertical offsets distinguish blocks. Horizontal spans are the full observed block-effect ranges. The black diamond remains the median of three session estimates, not a pooled median of 36 pairs. No durations or adverse pairs are excluded and no timer overhead is subtracted. This spread plot complements the session-estimate figure; its ranges are not confidence intervals, and individual timings within each process are not treated as independent experiments. The three comparisons use some of the same measurements, so they are not independent datasets.

### Keygen code and local-stack cost

[PDF](../analysis/figures/ACT-0020/exp005-keygen-tradeoffs.pdf), [SVG](../analysis/figures/ACT-0020/exp005-keygen-tradeoffs.svg), [PNG](../analysis/figures/ACT-0020/exp005-keygen-tradeoffs.png), [six variant/parameter rows](../analysis/figures/ACT-0020/exp005-keygen-tradeoffs.csv).

**Caption.** The figure shows EXP-005's additional keygen function-body bytes (17/33/40) and local-stack bytes (16/16/0) relative to EXP-003 for Kyber512/768/1024. The reviewed costs agree with identical normalized keygen bodies in all three closing sessions. Local stack includes saved registers and excludes the entry return address and every callee frame. This is not peak KEM memory. Keygen canary/probe instructions remain present. The inherited general-dot canary change is separate and retained in the security matrix. The chart is a scoped implementation-cost comparison, not a numerical security score.

## ACT-0026 accepted random-seed dot-and-box figures

All five sessions of the [follow-up protocol](experiments/EXP-010-random-seeds.md) are accepted in ACT-0026. The [generator](../analysis/build_random_seed_figures.py) validates the raw-data runs before plotting. Both renderings were visually reviewed, and all eleven figure/data/provenance files reproduced byte-for-byte. The five combined-analysis files also reproduced. [Reproduction evidence](evidence/ACT-0026/artifact-reproduction.json), [figure review](evidence/ACT-0026/figure-review.json), [complete interpretation](random_seed_followup.md).

| Figure | Exports | Plotted observations |
|---|---|---|
| Both candidates versus the original | [PDF](../analysis/figures/EXP-010/exp010-original-reference-dot-box.pdf), [SVG](../analysis/figures/EXP-010/exp010-original-reference-dot-box.svg), [PNG](../analysis/figures/EXP-010/exp010-original-reference-dot-box.png), [CSV](../analysis/figures/EXP-010/exp010-original-reference-dot-box.csv) | 1080 effects: 60 for each of 18 candidate/parameter/operation groups |
| Selected candidate versus the inverse-transform candidate | [PDF](../analysis/figures/EXP-010/exp010-direct-candidate-dot-box.pdf), [SVG](../analysis/figures/EXP-010/exp010-direct-candidate-dot-box.svg), [PNG](../analysis/figures/EXP-010/exp010-direct-candidate-dot-box.png), [CSV](../analysis/figures/EXP-010/exp010-direct-candidate-dot-box.csv) | 540 effects: 60 for each of nine parameter/operation groups |

The [box statistics](../analysis/figures/EXP-010/box-statistics.csv), [five-session summaries](../analysis/figures/EXP-010/five-session-effects.csv) and [input/code/output provenance](../analysis/figures/EXP-010/provenance.json) retain the exact plotted quantities. EXP-003 is cumulative through the inverse-transform treatment, and EXP-005 adds the keygen error-vector treatment.

**Caption.** Each coloured marker is one matched comparison of process medians, with 1000 timings per process. Colour and shape identify five separately launched sessions. All 60 effects per group are plotted. Boxes show inclusive-interpolated quartiles and the pooled block median, with full observed min–max whiskers. Black diamonds show the median of five session medians, preserving the declared summary unit. Positive means faster. All adverse values remain.

Boxes and ranges are descriptive, not confidence intervals. Offsets distinguish points without numerical meaning. Panels share a vertical scale within each figure; the direct-candidate figure uses a separate scale to expose the smaller effects. The spread includes both input variation and measurement variation on one host. It does not separate input-only variance, show that the results transfer to other platforms or provide new leakage evidence.

The original-reference figure shows every effect above zero. The direct figure retains the additional keygen benefit alongside mixed small effects and the repeated Kyber1024 decapsulation cost. Kyber1024 encapsulation is mixed around zero, qualifying the earlier small penalty. The [full record](random_seed_followup.md) gives the exact medians and signs; the visual spread alone is not a significance test.

ACT-0025's explicitly labelled synthetic rendering checks remain support evidence only. These ACT-0026-reviewed figures use actual measurements. The earlier closing-study artifacts remain separate and are not pooled with the follow-up.

## Reproduce

Run these commands from the repository root in Ubuntu/WSL with Python 3.12 and pip available. The [requirements](../analysis/requirements-figures.txt) pin Matplotlib 3.10.8 and its dependencies. A fresh temporary directory keeps generated copies separate from the accepted artifacts; installing into its `plot-deps` directory leaves system packages unchanged.

```sh
repro_root=$(mktemp -d /tmp/kyber-figures.XXXXXX)
figure_deps="$repro_root/plot-deps"
python3 -m pip install --target "$figure_deps" -r analysis/requirements-figures.txt
```

Run the required generators below in the same shell. Each destination is new. The commands recalculate figures from retained data. They collect no new measurements.

```sh
PYTHONPATH="$figure_deps" python3 -B analysis/build_thesis_figures.py \
  --output "$repro_root/act0016"

PYTHONPATH="$figure_deps" python3 -B analysis/build_timing_leakage_figures.py \
  --output "$repro_root/exp008"

PYTHONPATH="$figure_deps" python3 -B analysis/build_final_session_figures.py \
  --output "$repro_root/exp009-session1"

PYTHONPATH="$figure_deps" python3 -B analysis/build_final_comparison_figures.py \
  --output "$repro_root/exp009-final"

PYTHONPATH="$figure_deps" python3 -B analysis/build_random_seed_figures.py \
  --runs results/EXP-010/RUN-0001 results/EXP-010/RUN-0002 \
         results/EXP-010/RUN-0003 results/EXP-010/RUN-0004 results/EXP-010/RUN-0005 \
  --output "$repro_root/exp010"
```

The older [secret-flow generator](../analysis/build_security_figures.py) has a fixed output location and no `--output` option. Run an unchanged copy with its two input files in the temporary directory so it cannot overwrite the accepted coverage figure:

```sh
security_copy="$repro_root/exp007-copy"
mkdir -p "$security_copy/analysis" \
         "$security_copy/notes/evidence/ACT-0017" \
         "$security_copy/results/EXP-007/RUN-0001"

cp analysis/build_security_figures.py "$security_copy/analysis/"
cp notes/evidence/ACT-0017/exp-007-run-0001-review.json \
   "$security_copy/notes/evidence/ACT-0017/"
cp results/EXP-007/RUN-0001/manifest.json \
   "$security_copy/results/EXP-007/RUN-0001/"

PYTHONPATH="$figure_deps" python3 -B "$security_copy/analysis/build_security_figures.py"
```

Its regenerated files appear under `$security_copy/analysis/figures/ACT-0017`. All six generators check their retained inputs or accepted reviews and record output provenance. The initial generator also checks the fixed identities of its 22 input files. It then recalculates 225 paired effects, 45 group summaries and 54 count groups. Deterministic SVG IDs and omitted PDF/SVG calendar metadata support byte comparison under the recorded environment; package and Python versions remain in provenance where recorded.

These figure commands do not require the ignored original executables. Full source/build-identity audits are separate checks that require those local artifacts or a separately documented rebuild; see the [reproduction guide](git_reproduce.md). Keep the generator scripts, pinned requirements, inputs, reviews and plotted data alongside the exports so the figures remain reproducible.
