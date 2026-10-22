# Thesis figures, tables and reproduction

## Current artifacts

I generated these initial figures in ACT-0016 from retained measurements and counts. Each has SVG and PDF vector exports plus a 300-dpi PNG. I inspected every rendered figure, corrected overlapping labels in the first draft and retained the final exports. The tables contain unrounded values; display labels are rounded for readability. The figures include slower and mixed outcomes.

| Figure | Vector master | Raster preview | Supporting data |
|---|---|---|---|
| EXP-006 paired effects | [SVG](../analysis/figures/ACT-0016/exp006-paired-effects.svg), [PDF](../analysis/figures/ACT-0016/exp006-paired-effects.pdf) | [PNG](../analysis/figures/ACT-0016/exp006-paired-effects.png) | [All 45 pairs](../analysis/figures/ACT-0016/exp006-paired-effects.csv) |
| Incremental results across experiments | [SVG](../analysis/figures/ACT-0016/incremental-effects-overview.svg), [PDF](../analysis/figures/ACT-0016/incremental-effects-overview.pdf) | [PNG](../analysis/figures/ACT-0016/incremental-effects-overview.png) | [45 parameter/operation/experiment groups](../analysis/figures/ACT-0016/incremental-effects.csv) |
| Modular-reduction counts | [SVG](../analysis/figures/ACT-0016/reduction-counts.svg), [PDF](../analysis/figures/ACT-0016/reduction-counts.pdf) | [PNG](../analysis/figures/ACT-0016/reduction-counts.png) | [54 count groups](../analysis/figures/ACT-0016/reduction-counts.csv) |

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

I will choose additional visuals when they clarify a defensible thesis claim. I will preserve adverse results, units, comparators, sample structure, tool/source identities and limitations in captions and linked evidence. These initial figures are ready to use as report drafts; final direct-performance and security conclusions are still pending.
