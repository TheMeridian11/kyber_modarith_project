# Repository state and reproducibility

## Selected source and history

The selected working implementation is cumulative EXP-005. All 35 source files match [final_candidate.json](../analysis/final_candidate.json) and the historical snapshot at [4bd813ed71a9](source_revisions.md). The [final source review](evidence/ACT-0022/selected-source-review.json) also matches those identities to the accepted security runs and all three final comparison sessions.

Final source restoration and documentation were committed at [b2bd620d3eac](source_revisions.md). ACT-0023 inspected the local refs: main, reduction-counters, origin/main and origin/reduction-counters all point to that commit. ACT-0024 confirmed the same local ref identities before its documentation edits. No remote query was made during either editorial review. The 4474 archived result files are tracked. Historical experiment commits and the adverse EXP-006 result remain preserved.

The source restoration changed three files: indcpa.c restored the general dot followed by poly_tomont; polyvec.c and polyvec.h removed the EXP-006-only function and declaration. Its 2 insertions and 41 deletions recovered the already measured candidate. The selection manifest retains its original checkout-at-selection field as historical evidence.

## Reproduce the final tables

From the repository root, use a new output directory:

```sh
python3 -B scripts/analyse_final_comparison.py \
  --runs results/EXP-009/RUN-0001 results/EXP-009/RUN-0002 results/EXP-009/RUN-0003 \
  --output /tmp/exp009-final-analysis-copy
```

This reconstructs the final tables from retained measurements without ignored binaries or a new benchmark run. It is retained-data reproduction, not a fresh-environment performance study.

The complete source/tool/binary identity audit requires the recorded build directories and exact tools:

```sh
python3 -B analysis/review_final_comparison.py --output /tmp/exp009-final-audit-copy
```

[Figure instructions](thesis_figures.md) describe the pinned plotting environment and new output directories. ACT-0020 reproduced the three combined-analysis files, three audit reports and thirteen final figure/data/provenance files byte-for-byte.

## Revision references

The [revision index](source_revisions.md) keeps the full commit IDs used by these records. Short linked IDs in the readable notes preserve traceability without repeating long hashes. This file provides reproduction and archive guidance; it is not a list of unfinished Git work. References to staging instructions in frozen protocols describe their collection-time workflow; this file now records the completed state.

## Preservation rules

Existing ignored executables are not relabelled by source restoration. Their accepted identities remain those in the run manifests. Historical runners keep their original source gates and frozen support; replay uses the documented source revision and a new run ID. No replay is required for the completed study.

Documentation corrections use new commits. Cited experiment history, raw observations and audit records are preserved. Routine commit/push command sequences are omitted from the research narrative; normal Git review remains the repository-maintenance process.
