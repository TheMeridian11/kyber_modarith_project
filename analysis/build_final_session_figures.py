#!/usr/bin/env python3
"""Plot all EXP-009 session-1 paired effects; the closing comparison remains incomplete."""
import argparse
import csv
import hashlib
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
import analyse_final_comparison as analysis


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "analysis/figures/ACT-0019")
    args = parser.parse_args()
    run = ROOT / "results/EXP-009/RUN-0001"
    review_path = ROOT / "notes/evidence/ACT-0019/exp-009-run-0001-review.json"
    review = json.loads(review_path.read_text())
    manifest, aggregate = analysis.read_run(run)
    assert review["accepted_session"] and review["manifest_sha256"] == sha(run / "manifest.json")
    assert aggregate == review["session_estimates"] and manifest["session"] == 1
    data_path = run / "derived/paired-comparison.csv"
    with data_path.open(newline="") as stream:
        pairs = list(csv.DictReader(stream))
    assert len(pairs) == 324
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10,
                         "svg.hashsalt": "kyber-act0019-session1", "pdf.fonttype": 42})
    fig, axes = plt.subplots(3, 3, figsize=(12, 9))
    colors = ("#2479a1", "#188166", "#a76521")
    operations = ("keygen", "encap", "decap")
    titles = ("Key generation", "Encapsulation", "Decapsulation")
    contrasts = (("baseline", "exp003", "EXP-003 vs original"),
                 ("baseline", "exp005", "EXP-005 vs original"),
                 ("exp003", "exp005", "EXP-005 vs EXP-003"))
    for row_index, (reference, candidate, label) in enumerate(contrasts):
        for column, operation in enumerate(operations):
            ax = axes[row_index, column]
            for y, parameter in enumerate(("Kyber512", "Kyber768", "Kyber1024")):
                values = [r for r in pairs if (r["reference"], r["candidate"], r["operation"], r["parameter_set"]) ==
                          (reference, candidate, operation, parameter)]
                assert len(values) == 12
                values.sort(key=lambda r: int(r["block"]))
                effects = [float(r["improvement_pct"]) for r in values]
                summary = next(r for r in aggregate if (r["reference"], r["candidate"], r["operation"], r["parameter_set"]) ==
                               (reference, candidate, operation, parameter))
                median = summary["median_paired_improvement_pct"]
                ax.hlines(y, min(effects), max(effects), color=colors[row_index], alpha=.3, linewidth=1)
                ax.scatter(effects, [y + (b - 5.5) * .022 for b in range(12)], color=colors[row_index], s=19, alpha=.85, linewidths=0, zorder=3)
                ax.scatter([median], [y], marker="D", color="#18212a", s=34, edgecolors="white", linewidths=.6, zorder=4)
                ax.text(median, y - .24, f"{median:+.2f}%", ha="center", va="center", fontsize=9, color="#18212a")
            ax.axvline(0, color="#777777", linewidth=.8, linestyle="--")
            ax.set_ylim(2.45, -.55)
            ax.set_xlim((0, 22) if row_index < 2 else (-3.6, 7.8))
            ax.set_xticks((0, 5, 10, 15, 20) if row_index < 2 else (-3, 0, 3, 6))
            ax.set_yticks(range(3), ("512", "768", "1024"))
            ax.grid(axis="x", alpha=.14)
            for edge in ("top", "right"):
                ax.spines[edge].set_visible(False)
            if column == 0:
                ax.set_ylabel(label + "\nParameter set", fontsize=10, labelpad=10)
            if row_index == 0:
                ax.set_title(titles[column], fontsize=12, pad=14)
            if row_index == 2:
                ax.set_xlabel("Paired time reduction (%)", labelpad=8)
    fig.suptitle("Direct Kyber comparison — session 1 of 3", x=.075, ha="left", fontsize=16, y=.97)
    fig.text(.075, .928, "Preliminary: all 12 matched blocks shown; final candidate selection awaits sessions 2 and 3.", fontsize=10)
    fig.legend(handles=[Line2D([], [], color=colors[0], marker="o", linestyle="None", markersize=5, label="Matched block"),
                        Line2D([], [], color="#18212a", marker="D", linestyle="None", markersize=5, label="Median of 12 effects")],
               loc="lower right", bbox_to_anchor=(.965, .015), frameon=False, fontsize=9)
    fig.subplots_adjust(left=.14, right=.97, top=.86, bottom=.16, hspace=.29, wspace=.22)
    fig.text(.075, .066, "Positive = faster candidate. Each effect compares two process medians (1,000 timings per operation).\n"
             "Top two rows share a scale; the bottom row expands the marginal effects. Horizontal spans are observed ranges,\n"
             "not confidence intervals. No timings excluded. One WSL host; no cross-session conclusion yet.", fontsize=9, color="#333333")
    args.output.mkdir(parents=True, exist_ok=True)
    stem = args.output / "exp009-session1-effects"
    for suffix in ("svg", "pdf", "png"):
        dest = stem.with_suffix("." + suffix)
        if dest.exists():
            raise ValueError("Refusing to overwrite a figure")
        extra = {"metadata": {"Date": None}} if suffix == "svg" else {"metadata": {"CreationDate": None, "ModDate": None}} if suffix == "pdf" else {}
        fig.savefig(dest, dpi=300, **extra)
        if suffix == "svg":
            dest.write_text("\n".join(line.rstrip() for line in dest.read_text().splitlines()) + "\n")
    plt.close(fig)
    with stem.with_suffix(".csv").open("xb") as stream:
        stream.write(data_path.read_bytes())
    inputs = (run / "manifest.json", run / "derived/comparison.csv", data_path, review_path)
    provenance = dict(activity_id="ACT-0019", session=1, planned_sessions=3,
                      inputs={p.relative_to(ROOT).as_posix(): sha(p) for p in inputs},
                      generator_sha256=sha(__file__), frozen_analyser_sha256=sha(ROOT / "scripts/analyse_final_comparison.py"),
                      python=platform.python_version(), matplotlib=matplotlib.__version__,
                      outputs={p.name: sha(p) for p in sorted(args.output.iterdir()) if p.is_file()},
                      interpretation="All within-session paired effects; no confidence intervals or final candidate ranking.")
    with (args.output / "provenance.json").open("x") as stream:
        json.dump(provenance, stream, indent=2)
        stream.write("\n")
    print("Generated session-1 SVG/PDF/PNG, all 324 paired effects, and provenance")


if __name__ == "__main__":
    main()
