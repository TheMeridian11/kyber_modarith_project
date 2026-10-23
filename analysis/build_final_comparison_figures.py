#!/usr/bin/env python3
"""Plot all closing EXP-009 sessions and the scoped EXP-005 keygen tradeoffs."""
import argparse
import csv
import hashlib
import json
import math
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
COLORS = ("#0072b2", "#d55e00", "#009e73")
MARKERS = ("o", "s", "^")
CONTRASTS = (("baseline", "exp003", "EXP-003 vs original"),
             ("baseline", "exp005", "EXP-005 vs original"),
             ("exp003", "exp005", "EXP-005 vs EXP-003"))
OPS = ("keygen", "encap", "decap")
PARAMETERS = ("Kyber512", "Kyber768", "Kyber1024")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def export(fig, directory, name, rows):
    for suffix in ("svg", "pdf", "png"):
        dest = directory / (name + "." + suffix)
        if dest.exists():
            raise ValueError("Refusing to overwrite a figure")
        extra = {"metadata": {"Date": None}} if suffix == "svg" else {"metadata": {"CreationDate": None, "ModDate": None}} if suffix == "pdf" else {}
        fig.savefig(dest, dpi=300, **extra)
        if suffix == "svg":
            dest.write_text("\n".join(line.rstrip() for line in dest.read_text().splitlines()) + "\n")
    plt.close(fig)
    with (directory / (name + ".csv")).open("x", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def effects_plot(directory, session_rows, totals, pair_rows, all_pairs):
    fig, axes = plt.subplots(3, 3, figsize=(12, 9.6))
    data = pair_rows if all_pairs else session_rows
    field = "improvement_pct" if all_pairs else "median_paired_improvement_pct"
    for row_index, (reference, candidate, label) in enumerate(CONTRASTS):
        row_values = [float(r[field]) for r in data if (r["reference"], r["candidate"]) == (reference, candidate)]
        if all_pairs:
            limits = (0, math.ceil(max(float(r[field]) for r in data if r["reference"] == "baseline") / 5) * 5) if row_index < 2 else (
                     math.floor(min(row_values)) - .5, math.ceil(max(row_values)) + .5)
        else:
            limits = (0, 22) if row_index < 2 else (-1.2, 6.3)
        for column, operation in enumerate(OPS):
            ax = axes[row_index, column]
            for y, parameter in enumerate(PARAMETERS):
                selected = [r for r in data if (r["reference"], r["candidate"], r["operation"], r["parameter_set"]) ==
                            (reference, candidate, operation, parameter)]
                assert len(selected) == (36 if all_pairs else 3)
                values = [float(r[field]) for r in selected]
                ax.hlines(y, min(values), max(values), color="#747b82", alpha=.42, linewidth=1)
                for session in (1, 2, 3):
                    group = sorted([r for r in selected if int(r["session"]) == session], key=lambda r: int(r.get("block", 0)))
                    offsets = [y + ((session - 1) * 12 + b - 17.5) * .011 for b in range(12)] if all_pairs else [y + (session - 2) * .105]
                    ax.scatter([float(r[field]) for r in group], offsets, marker=MARKERS[session - 1], color=COLORS[session - 1],
                               s=17 if all_pairs else 29, alpha=.8 if all_pairs else 1, linewidths=0, zorder=3)
                summary = next(r for r in totals if (r["reference"], r["candidate"], r["operation"], r["parameter_set"]) ==
                               (reference, candidate, operation, parameter))
                median = summary["median_session_improvement_pct"]
                ax.scatter([median], [y], marker="D", color="#161f28", s=34, edgecolors="white", linewidths=.5, zorder=4)
                ax.text(median, y - .29, f"{median:+.2f}%", ha="center", va="center", fontsize=9)
            ax.axvline(0, color="#777777", linestyle="--", linewidth=.8)
            ax.set_xlim(limits)
            ax.set_ylim(2.45, -.6)
            ax.set_yticks(range(3), ("512", "768", "1024"))
            ax.grid(axis="x", alpha=.14)
            for edge in ("top", "right"):
                ax.spines[edge].set_visible(False)
            if column == 0:
                ax.set_ylabel(label + "\nParameter set", labelpad=10)
            if row_index == 0:
                ax.set_title(("Key generation", "Encapsulation", "Decapsulation")[column], pad=14, fontsize=12)
            if row_index == 2:
                ax.set_xlabel("Paired time reduction (%)", labelpad=8)
    title = "Closing Kyber comparison — all matched blocks" if all_pairs else "Closing Kyber comparison — all three sessions"
    subtitle = "All 972 paired effects retained; 12 blocks per parameter in each session." if all_pairs else "Each session contributes one median of 12 paired effects per group."
    fig.suptitle(title, x=.075, ha="left", fontsize=16, y=.97)
    fig.text(.075, .928, subtitle, fontsize=10)
    handles = [Line2D([], [], color=c, marker=mark, linestyle="None", markersize=5, label=f"Session {s}")
               for s, (c, mark) in enumerate(zip(COLORS, MARKERS), 1)]
    handles.append(Line2D([], [], color="#161f28", marker="D", linestyle="None", markersize=5, label="Median of 3 session estimates"))
    fig.legend(handles=handles, loc="lower center", bbox_to_anchor=(.55, .014), frameon=False, ncol=4, fontsize=9)
    fig.subplots_adjust(left=.14, right=.97, top=.86, bottom=.19, hspace=.31, wspace=.23)
    span = "Horizontal spans: observed block-effect ranges, not confidence intervals." if all_pairs else "Horizontal spans: observed three-session ranges, not confidence intervals."
    fig.text(.075, .088, "Positive = faster candidate. Top two rows share a scale; bottom row expands the marginal effects.\n" + span +
             "\nOne WSL host; no population significance or portability claim. No timing exclusions or overhead subtraction.", fontsize=9, color="#333333")
    export(fig, directory, "exp009-all-paired-effects" if all_pairs else "exp009-three-session-effects", data)


def tradeoff_plot(directory, rows):
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 5.7))
    deltas = []
    for parameter in PARAMETERS:
        old, new = [next(r for r in rows if r["parameter_set"] == parameter and r["variant"] == v) for v in ("exp003", "exp005")]
        deltas.append((new["body_bytes"] - old["body_bytes"], new["local_stack_bytes"] - old["local_stack_bytes"]))
    for column, (ax, title) in enumerate(zip(axes, ("Keygen function-body growth", "Keygen local-stack growth"))):
        values = [d[column] for d in deltas]
        ax.bar(range(3), values, color=("#417893" if column == 0 else "#b97b3b"), width=.55)
        ax.set_xticks(range(3), ("Kyber512", "Kyber768", "Kyber1024"))
        ax.set_ylim(0, 48 if column == 0 else 20)
        ax.set_ylabel("Additional bytes relative to EXP-003")
        ax.set_title(title, fontsize=12)
        ax.grid(axis="y", alpha=.15)
        ax.set_axisbelow(True)
        for i, value in enumerate(values):
            ax.text(i, value + (.8 if column == 0 else .4), f"+{value}", ha="center", fontsize=11)
        for edge in ("top", "right"):
            ax.spines[edge].set_visible(False)
    fig.suptitle("EXP-005 keygen: the measured code and local-stack tradeoff", x=.06, ha="left", fontsize=14, y=.96)
    fig.subplots_adjust(left=.08, right=.97, top=.81, bottom=.32, wspace=.3)
    fig.text(.06, .105, "Function bodies (EXP-003 → EXP-005): 425 → 442, 479 → 512, 948 → 988 bytes.\n"
             "Local stack: 5,256 → 5,272; 9,368 → 9,384; 15,032 → 15,032 bytes.\n"
             "Local stack includes saved registers; excludes entry return address and all callee frames.\n"
             "Keygen canaries remain present. These are scoped observations, not total memory or a security score.", fontsize=9)
    export(fig, directory, "exp005-keygen-tradeoffs", rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "analysis/figures/ACT-0020")
    args = parser.parse_args()
    runs = [ROOT / f"results/EXP-009/RUN-{i:04d}" for i in (1, 2, 3)]
    loaded, estimates, totals = analysis.combine(runs)
    review_path = ROOT / "notes/evidence/ACT-0020/exp-009-three-session-review.json"
    review = json.loads(review_path.read_text())
    assert review["all_three_sessions_accepted"]
    for run in runs:
        assert sha(run / "manifest.json") == review["manifest_sha256"][run.relative_to(ROOT).as_posix()]
    assert totals == [{k: r[k] for k in totals[0]} for r in review["contrasts"]]
    pairs = []
    for run in runs:
        with (run / "derived/paired-comparison.csv").open(newline="") as stream:
            pairs.extend(csv.DictReader(stream))
    assert len(pairs) == 972
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10,
                         "svg.hashsalt": "kyber-act0020", "pdf.fonttype": 42})
    args.output.mkdir(parents=True, exist_ok=True)
    effects_plot(args.output, estimates, totals, pairs, False)
    effects_plot(args.output, estimates, totals, pairs, True)
    tradeoff_plot(args.output, review["keygen_code_and_local_stack"])
    inputs = [review_path, ROOT / "analysis/final-comparison-EXP-009/provenance.json"]
    inputs += [run / "manifest.json" for run in runs]
    provenance = dict(activity_id="ACT-0020", complete_sessions=3, inputs={p.relative_to(ROOT).as_posix(): sha(p) for p in inputs},
                      generator_sha256=sha(__file__), frozen_analyser_sha256=sha(ROOT / "scripts/analyse_final_comparison.py"),
                      python=platform.python_version(), matplotlib=matplotlib.__version__,
                      outputs={p.name: sha(p) for p in sorted(args.output.iterdir()) if p.is_file()},
                      interpretation="Three-session descriptive effects and scoped frame costs; no calibrated confidence intervals or universal winner.")
    with (args.output / "provenance.json").open("x") as stream:
        json.dump(provenance, stream, indent=2)
        stream.write("\n")
    print("Generated three figures in SVG/PDF/PNG, their complete data tables, and provenance")


if __name__ == "__main__":
    main()
