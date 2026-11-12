# Repository state and reproducibility

## Choose the task

Reproduction uses the measurements I already saved. Collecting new measurements is a separate task. The table below shows which tools to use and what each one needs. Their recorded paths and code stay unchanged.

| Task | Tools | Required material |
|---|---|---|
| Recalculate the completed performance tables | [EXP-009 analyser](../scripts/analyse_final_comparison.py), [EXP-010 analyser](../scripts/analyse_random_seed_comparison.py) | Raw records, manifests and recorded support. No ignored executables |
| Regenerate plots and plotted CSVs | The six [figure generators](thesis_figures.md#reproduce) | Retained data/reviews and pinned plotting dependencies; use fresh destinations |
| Check source/build identities and independent calculations | [EXP-009 full review](../analysis/review_final_comparison.py), [EXP-010 full review](../analysis/review_random_seed_comparison.py), [timing-screen review](../analysis/review_timing_leakage.py) | Recorded ignored binaries/restored sources and the tools required by each audit; the timing review also reads its retained development archive |
| Inspect historical collection procedures | `scripts/run_*.py` and the [experiment register](experiment_register.md) | The appropriate recorded source/support revision, exact source gates and a fresh run ID for any new collection |
| Check the analysis and validation machinery | Python and C files under `tests/` | The dependencies declared by each test; development checks are distinct from formal observations |

Some current analysers import functions from older runners. Keep those runners even if no more measurements are planned. Historical collection commands are not guaranteed to work against today's selected checkout; the [record conventions](research_workflow.md) explain the source and preservation rules.

## Reproduce the completed tables

Run from the repository root in Ubuntu/WSL with Python 3.12. Create a fresh scratch directory; each analyser creates its own new subdirectory.

```sh
repro_root=$(mktemp -d /tmp/kyber-reproduce.XXXXXX)

python3 -B scripts/analyse_final_comparison.py \
  --runs results/EXP-009/RUN-0001 results/EXP-009/RUN-0002 results/EXP-009/RUN-0003 \
  --output "$repro_root/exp009-analysis"

python3 -B scripts/analyse_random_seed_comparison.py \
  --runs results/EXP-010/RUN-0001 results/EXP-010/RUN-0002 \
         results/EXP-010/RUN-0003 results/EXP-010/RUN-0004 results/EXP-010/RUN-0005 \
  --output "$repro_root/exp010-analysis"
```

These commands read existing measurements and write copies beneath `repro_root`. They do not rerun benchmarks or overwrite the accepted outputs. Keep the two studies separate. [EXP-009](final_comparison.md) and [EXP-010](random_seed_followup.md) give their interpretations; [the figure guide](thesis_figures.md#reproduce) gives plotting setup and safe output paths.

Full local-artifact audits are optional additional checks. With the original ignored build artifacts still present, use new destinations under the same scratch directory:

```sh
python3 -B analysis/review_final_comparison.py \
  --output "$repro_root/exp009-audit"

python3 -B analysis/review_random_seed_comparison.py \
  --output "$repro_root/exp010-audit.json"
```

The saved data can still be analysed if ignored build directories are removed. However, those directories contain the original executables needed for full identity checks. If an executable is rebuilt, record the new build separately. It will not automatically match the original binary.

## Selected source and historical checkpoints

All 35 selected implementation files match [final_candidate.json](../analysis/final_candidate.json), the EXP-005 snapshot identified in the [revision index](source_revisions.md). [ACT-0022](evidence/ACT-0022/selected-source-review.json) verified the restoration of the already measured candidate; [ACT-0026](evidence/ACT-0026/final-verification.json) confirmed it remained unchanged during follow-up review.

ACT-0023 and ACT-0024 recorded local refs and 4474 archived result files for the original programme. Those are historical observations, not the current branch, remote or whole-project file count. The later EXP-010 source/support checkpoint is recorded in all five manifests. Current commit/push state is established through the normal manual Git workflow.

ACT-0020 reproduced the closing-study tables, audits and figures. ACT-0026 reproduced the five follow-up analysis files and eleven figure/data/provenance files byte-for-byte. The [activity log](project_log.md) links the detailed verification records.

## Revision references and preservation

Readable notes use descriptive implementation names and short linked revisions where needed; the [revision index](source_revisions.md) retains full commit IDs. Manifests, source pins and prior audits keep exact hashes. Source/support commits identify the files used to collect the data. Results commits identify the later versions that saved the observations.

Preserve raw records, metadata, previous audits, accepted figure bundles and protocol versions. Existing ignored executables retain their recorded identities. Editorial corrections belong in new commits, with no rewriting of experimental history or relabelling of development data as formal results.
