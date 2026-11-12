#!/usr/bin/env python3
"""Render EXP-010 dot-and-box plots from five verified raw-data sessions."""
import argparse
import json
from pathlib import Path
import platform
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import analyse_random_seed_comparison as analysis
import collect_run_metadata as metadata
import random_seed_common as common

COLORS = ("#0072B2", "#D55E00", "#009E73", "#CC79A7", "#7A5A2E")
MARKERS = ("o", "s", "^", "D", "P")
OPS = ("keygen", "encap", "decap")
TITLES = ("Key generation", "Encapsulation", "Decapsulation")


def plot(directory, pairs, totals, boxes, direct=False, development=False):
    contrasts = (("exp003", "exp005", "Selected vs transform"),) if direct else (
        ("baseline", "exp003", "Transform\n(EXP-003)"), ("baseline", "exp005", "Selected\n(EXP-005)"))
    data = [r for r in pairs if (r["reference"], r["candidate"]) in [(a, b) for a, b, _ in contrasts]]
    fig, axes = plt.subplots(3, 3, figsize=(12, 10.6), sharey=True)
    values = [r["improvement_pct"] for r in data]
    low, high = min(0.0, min(values)), max(0.0, max(values))
    pad = max((high - low) * .12, .15)
    for i, parameter in enumerate(common.PARAMETERS):
        for j, operation in enumerate(OPS):
            ax = axes[i, j]
            for x, (reference, candidate, label) in enumerate(contrasts, 1):
                match = lambda r: (r["reference"], r["candidate"], r["parameter_set"], r["operation"]) == (
                    reference, candidate, f"Kyber{parameter}", operation)
                selected = [r for r in data if match(r)]
                if len(selected) != 60:
                    raise ValueError("Plot group is missing paired observations")
                box = next(r for r in boxes if match(r))
                total = next(r for r in totals if match(r))
                ax.bxp([dict(med=box["pooled_block_median_pct"], q1=box["q1_pct"], q3=box["q3_pct"],
                             whislo=box["min_pct"], whishi=box["max_pct"], fliers=[])],
                       positions=[x], widths=.53, showfliers=False, patch_artist=True, manage_ticks=False,
                       boxprops=dict(facecolor="#EFF2F4", edgecolor="#6D747A", linewidth=.9),
                       medianprops=dict(color="#4A4A4A", linewidth=1.3),
                       whiskerprops=dict(color="#899198"), capprops=dict(color="#899198"))
                for session in range(1, 6):
                    group = sorted([r for r in selected if r["session"] == session], key=lambda r: r["block"])
                    offsets = [x + (session - 3) * .075 + (r["block"] - 6.5) * .004 for r in group]
                    ax.scatter(offsets, [r["improvement_pct"] for r in group], color=COLORS[session - 1],
                               marker=MARKERS[session - 1], s=19, alpha=.85, linewidths=0, zorder=3)
                ax.scatter([x], [total["median_session_improvement_pct"]], marker="D", s=45,
                           color="#111111", edgecolor="white", linewidth=.8, zorder=5)
            ax.axhline(0, color="#707070", linestyle="--", linewidth=.8)
            ax.set_ylim(low - pad, high + pad)
            ax.set_xlim(.5, len(contrasts) + .5)
            ax.set_xticks(range(1, len(contrasts) + 1), [c[2] for c in contrasts], fontsize=9)
            ax.grid(axis="y", alpha=.15)
            ax.set_axisbelow(True)
            if i == 0:
                ax.set_title(TITLES[j], fontsize=12, pad=12)
            if j == 0:
                ax.set_ylabel(f"Kyber{parameter}\nTime reduction (%)", fontsize=10)
            for edge in ("top", "right"):
                ax.spines[edge].set_visible(False)
    title = "Random-seed follow-up: additional selected-variant effect" if direct else "Random-seed follow-up: improvements relative to the original"
    if development:
        title = "DEVELOPMENT CHECK — synthetic data only"
    fig.suptitle(title, fontsize=15, x=.075, y=.98, ha="left")
    fig.text(.075, .94, "Five sessions; 12 matched trials per session and parameter. Every paired effect is shown.", fontsize=10)
    handles = [Line2D([], [], color=color, marker=mark, linestyle="None", label=f"Session {i}", markersize=5)
               for i, (color, mark) in enumerate(zip(COLORS, MARKERS), 1)]
    handles.append(Line2D([], [], color="#111111", marker="D", linestyle="None", markersize=6,
                          label="Median of 5 session medians"))
    fig.legend(handles=handles, loc="lower center", bbox_to_anchor=(.52, .105), ncol=3, frameon=False, fontsize=9)
    fig.text(.075, .025,
        "Positive = faster candidate. One dot = a matched comparison of process medians, each based on 1000 timings.\n"
        "Box: middle 50% of the 60 block effects; line: pooled block median; whiskers: full observed min–max.\n"
        "The black diamond is the session-based summary. Boxes and ranges are not confidence intervals.\n"
        "One WSL host. Spread includes input and measurement variation; no timing exclusions or overhead subtraction.",
        fontsize=9, color="#333333")
    fig.subplots_adjust(left=.095, right=.98, top=.885, bottom=.22, hspace=.32, wspace=.16)
    stem = "exp010-direct-candidate-dot-box" if direct else "exp010-original-reference-dot-box"
    for extension in ("svg", "pdf", "png"):
        dest = directory / (stem + "." + extension)
        if dest.exists():
            raise ValueError("Refusing to overwrite a figure")
        extra = {"metadata": {"Date": None}} if extension == "svg" else {
            "metadata": {"CreationDate": None, "ModDate": None}} if extension == "pdf" else {}
        fig.savefig(dest, dpi=300, **extra)
        if extension == "svg":
            dest.write_text("\n".join(line.rstrip() for line in dest.read_text().splitlines()) + "\n")
    plt.close(fig)
    analysis.write_csv(directory / (stem + ".csv"), data)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runs", nargs=5, type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    loaded, pairs, _, totals, boxes = analysis.combine(args.runs)
    args.output.mkdir(parents=True, exist_ok=False)
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10,
                         "svg.hashsalt": "kyber-exp010-dot-box-v1", "pdf.fonttype": 42})
    plot(args.output, pairs, totals, boxes)
    plot(args.output, pairs, totals, boxes, direct=True)
    analysis.write_csv(args.output / "box-statistics.csv", boxes)
    analysis.write_csv(args.output / "five-session-effects.csv", totals)
    report = dict(experiment="EXP-010", record_type="random-seed-dot-box-figures",
        seed_plan_sha256=loaded[0][0]["protocol"]["seed_plan_sha256"], sessions=5, unique_block_seeds=60,
        inputs={str(run / "manifest.json"): metadata.sha256(run / "manifest.json") for run in args.runs},
        code_sha256={name: metadata.sha256(ROOT / name) for name in
            ("analysis/build_random_seed_figures.py", "scripts/analyse_random_seed_comparison.py",
             "scripts/random_seed_common.py", "scripts/analyse_final_comparison.py")},
        python=platform.python_version(), matplotlib=matplotlib.__version__,
        quantiles="statistics.quantiles(n=4, method='inclusive'); whiskers=min/max; all points retained",
        interpretation="Pooled boxes describe spread; diamonds retain the median of five session estimates. No confidence intervals or input-only variance claim.",
        outputs={p.name: metadata.sha256(p) for p in sorted(args.output.iterdir()) if p.is_file()})
    (args.output / "provenance.json").write_text(json.dumps(report, indent=2) + "\n")
    print("Generated two dot-and-box figures in SVG/PDF/PNG, plot data and provenance.")


if __name__ == "__main__":
    main()
