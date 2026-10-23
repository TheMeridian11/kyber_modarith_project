# Thesis figures, tables and reproduction

## Current artifacts

I generated these initial figures in ACT-0016 from retained measurements and counts. Each has SVG and PDF vector exports plus a 300-dpi PNG. I inspected every rendered figure, corrected overlapping labels in the first draft and retained the final exports. The tables contain unrounded values; display labels are rounded for readability. The figures include slower and mixed outcomes.

| Figure | Vector master | Raster preview | Supporting data |
|---|---|---|---|
| EXP-006 paired effects | [SVG](../analysis/figures/ACT-0016/exp006-paired-effects.svg), [PDF](../analysis/figures/ACT-0016/exp006-paired-effects.pdf) | [PNG](../analysis/figures/ACT-0016/exp006-paired-effects.png) | [All 45 pairs](../analysis/figures/ACT-0016/exp006-paired-effects.csv) |
| Incremental results across experiments | [SVG](../analysis/figures/ACT-0016/incremental-effects-overview.svg), [PDF](../analysis/figures/ACT-0016/incremental-effects-overview.pdf) | [PNG](../analysis/figures/ACT-0016/incremental-effects-overview.png) | [45 parameter/operation/experiment groups](../analysis/figures/ACT-0016/incremental-effects.csv) |
| Modular-reduction counts | [SVG](../analysis/figures/ACT-0016/reduction-counts.svg), [PDF](../analysis/figures/ACT-0016/reduction-counts.pdf) | [PNG](../analysis/figures/ACT-0016/reduction-counts.png) | [54 count groups](../analysis/figures/ACT-0016/reduction-counts.csv) |

ACT-0017 corrects trailing whitespace in the three initial SVG files and updates their provenance. The original PNG/PDF/CSV bytes and all 22 data inputs are unchanged. The [original provenance](evidence/ACT-0017/figure-provenance-before-correction.json) is retained, and [correction evidence](evidence/ACT-0017/figure-review.json) records old/new hashes. My ACT-0016 whitespace check omitted SVG files; its broad statement of a passing whitespace check was incomplete. The generator now canonicalises SVG line endings, and the final check includes SVG.

The [provenance manifest](../analysis/figures/ACT-0016/provenance.json) records 22 input file hashes, analysis-code identity, package versions and all output hashes. [The input index](../analysis/figure_inputs.json) pins the original manifests/CSV files. All five timing comparisons use RUN-0002; original counts use EXP-000/RUN-0004, and implemented-variant counts use their RUN-0001 validation manifests. The [EXP-006 review](runs/EXP-006-RUN-0002.md) records raw-data reconstruction and source/build provenance. Earlier timing reviews remain linked in the experiment register.

## Draft captions and interpretation

**Paired effects.** I compare EXP-006 with a freshly built EXP-005 in five adjacent process pairs per parameter. Each point is 100*(control process median - candidate process median)/control process median; positive values indicate less time. Circles and squares distinguish execution order. Black ticks mark medians and horizontal segments show observed extrema, not confidence intervals. Warm-up is 100 exchanges and measurement is 1000 exchanges per process, under the recorded GCC/WSL guest-CPU-0 setup. All Kyber512 pairs regress, whereas Kyber1024 keygen improves in every pair. This is a single-session performance result, not a leakage test.

**Incremental overview.** I show the median of five paired time reductions for each implemented experiment relative to its stated immediate predecessor; EXP-001 uses the original reference. Each column comes from its own matched session. The underlying table also retains extrema and positive-pair counts. These conditional incremental effects cannot be added or multiplied to claim a total original-baseline gain. The heatmap summarises magnitude/direction, not statistical significance or uncertainty. EXP-004 is absent because no separate interaction experiment was executed, not because a result was removed.

**Reduction counts.** I show observed Montgomery and Barrett calls per complete keygen, encapsulation and decapsulation operation in the separate instrumented builds. Each group contains ten deterministic fixtures with agreeing counts. Stage labels identify actual cumulative implementations, with the original reference shown separately. Lines connect discrete implementation stages; they are not a calendar-time trend. Function-call savings are not instruction counts, proportional speed predictions or security evidence. EXP-006 remains visible even though it was not adopted as the general final candidate.

## Reproduce

I use Python 3.12, Matplotlib 3.10.8 and the exact dependency versions in [requirements-figures.txt](../analysis/requirements-figures.txt). The ACT-0016 environment used existing pip to install into an isolated temporary virtual environment; no system Python package was changed. From the repository root, with Python venv and pip available:

```sh
python3 -m venv --without-pip /tmp/kyber-thesis-figures
python3 -m pip --python /tmp/kyber-thesis-figures/bin/python install -r analysis/requirements-figures.txt
/tmp/kyber-thesis-figures/bin/python -B analysis/build_thesis_figures.py
```

[build_thesis_figures.py](../analysis/build_thesis_figures.py) verifies every pinned input hash, checks completed run/provenance status, verifies recorded derived-file hashes, recomputes all 225 paired percentage effects and 45 group medians/extrema, and checks 54 count groups. It writes only derived figure/table files, not results/. The optional --output selects another figure directory; otherwise it regenerates analysis/figures/ACT-0016. SVG IDs are deterministic and PDF/SVG calendar metadata is omitted. Package and Python versions remain recorded. The raw data and full precision are preserved independently of the graphic format.

## Further figures at the next milestones

I will extend the set when relevant evidence exists:

- Direct original-versus-selected performance, showing each session/pair and the predeclared uncertainty summary rather than a constructed cumulative gain.
- Repeat-session effects for small or adverse findings that affect selection, including control-operation movements.
- A code-size/local-stack table or plot with the exact scoped functions and measurement definitions, keeping the canary observation separate from a numeric safety score.
- A security evidence matrix that distinguishes range arguments, compatibility, exercised sanitizers, assembly/hardening, formal dynamic-flow results and statistical timing outcomes, with clear not-run/inconclusive states.
- Statistical leakage diagnostics including sensitivity controls and chosen secret classes/budgets once those are fixed and collected. A quiet plot will not be labelled proof of constant time.

I will choose additional visuals when they clarify a defensible thesis claim. I will preserve adverse results, units, comparators, sample structure, tool/source identities and limitations in captions and linked evidence. These initial figures are ready to use as report drafts; final direct-performance and consolidated security reporting remain pending.

## ACT-0017 formal secret-flow coverage figure

I generated [SVG](../analysis/figures/ACT-0017/exp007-secret-flow.svg), [PDF](../analysis/figures/ACT-0017/exp007-secret-flow.pdf) and [PNG](../analysis/figures/ACT-0017/exp007-secret-flow.png) versions of the accepted EXP-007 coverage matrix, with [99 marked-mode process outcomes](../analysis/figures/ACT-0017/exp007-secret-flow.csv) and [provenance](../analysis/figures/ACT-0017/provenance.json). I visually inspected the rendering.

**Draft caption.** I show marked-mode outcomes for eight target path/operand-role cases and three controls across original/EXP-005/EXP-006 and all parameter sets. All 72 target processes and nine negative controls are quiet; all nine branch and nine address positive controls are detected. Each target process exercises eight fixtures, with 128 pairs per basemul fixture. The 99 defined twins are also quiet and retained in the raw run. Colour identifies expected outcomes; it is not a numerical security rating. Quiet means no marked-secret branch/address dependency observed on the exercised paths. This is neither a statistical timing result nor whole-program constant-time proof.

I reproduce it using the same figure environment:

```sh
/tmp/kyber-thesis-figures/bin/python -B analysis/build_security_figures.py
```

The initial exports remain under ACT-0016 with their explicit ACT-0017 whitespace revision; the new security figure is under ACT-0017. ACT-0018 below adds the audited formal EXP-008 timing plot. I retain the existing incremental heatmap to explain that EXP-003's sizeable inverse-NTT benefit is already part of EXP-005. A final original/EXP-003/EXP-005 figure will use fresh matched data, not constructed cumulative percentages.

## ACT-0018 formal timing-screen diagnostics

I generated [SVG](../analysis/figures/ACT-0018/exp008-timing-screen.svg), [PDF](../analysis/figures/ACT-0018/exp008-timing-screen.pdf) and [PNG](../analysis/figures/ACT-0018/exp008-timing-screen.png), with [all 1944 statistics](../analysis/figures/ACT-0018/exp008-timing-screen.csv) and [provenance](../analysis/figures/ACT-0018/provenance.json). I inspected the PNG and independently regenerated all five outputs byte-for-byte.

**Draft caption.** I show the maximum absolute Welch statistic for each target path and implementation/parameter combination in EXP-008/RUN-0001. Each cell covers two synthetic profiles, two process repetitions, two fixed looks and three views (24 statistics); no target statistic exceeds the predeclared diagnostic threshold 10. Every process retains 50000 analysis observations plus 2000 calibration observations. The lower panel shows each negative control's maximum across its six statistics, and each deliberate positive control's final uncropped mean statistic, matching their acceptance rules. All 18 positives are detected and all 18 negatives are quiet. Timing uses TSC ticks. These are bounded empirical observations, not calibrated family-wise inference, tiny-leak sensitivity guarantees, an implementation ranking or a whole-program constant-time proof.

I reproduce the audit with local ignored build files still present, then generate the figure into a new directory using the pinned plotting environment:

```sh
/tmp/kyber-thesis-figures/bin/python -B analysis/review_timing_leakage.py --out /tmp/exp008-review-copy.json
/tmp/kyber-thesis-figures/bin/python -B analysis/build_timing_leakage_figures.py --output /tmp/exp008-figure-copy
```

The retained review supplies all plot data even if ignored binaries later disappear; repeating the full identity audit requires those exact binaries or a separately documented rebuild. The next figures will use EXP-009's actual three sessions and show each session's effects and all three direct contrasts. I do not turn the development session into a thesis performance result.

## ACT-0019 preliminary direct-performance figure

I generated [SVG](../analysis/figures/ACT-0019/exp009-session1-effects.svg), [PDF](../analysis/figures/ACT-0019/exp009-session1-effects.pdf) and [300-dpi PNG](../analysis/figures/ACT-0019/exp009-session1-effects.png) exports of the accepted first EXP-009 session. I retain [all 324 plotted pairs](../analysis/figures/ACT-0019/exp009-session1-effects.csv), [input/code/output provenance](../analysis/figures/ACT-0019/provenance.json) and [render/reproduction review](evidence/ACT-0019/figure-review.json). I inspected the rendering and regenerated all five outputs byte-for-byte.

**Draft caption.** I show the direct original-to-EXP-003, original-to-EXP-005 and EXP-003-to-EXP-005 time reductions for EXP-009/RUN-0001, session 1 of the three predeclared sessions. Each dot is a within-block comparison of process medians, each based on 1000 operation timings. Diamonds show medians of 12 paired effects; horizontal spans show their observed ranges, not confidence intervals. The three parameter sets and all operations are shown, including mixed and negative effects. Positive means faster. The top two comparison rows share a scale; the bottom row expands the marginal effects. Point jitter follows block order only to improve visibility and has no numerical meaning. No durations are excluded. These single-host WSL results are preliminary; no cross-session repeatability or final candidate ranking is established here.

I reproduce the raw/build audit while the exact local ignored binaries and restored sources remain available, then generate into a new directory with the previously pinned plotting environment:

```sh
python3 -B analysis/review_final_session.py --output /tmp/exp009-session1-review-copy.json
/tmp/kyber-thesis-figures/bin/python -B analysis/build_final_session_figures.py --output /tmp/exp009-session1-figure-copy
```

The figure generator reanalyses the retained raw data and checks the accepted review, so it does not require ignored binaries. Repeating the full identity audit does require the original build files or a separately documented rebuild. The first-session graph is a progress artifact for later thesis composition. I will show all three session estimates and their descriptive range in the final performance figures after the remaining sessions are accepted; I will not substitute this preliminary figure for that closing evidence.
