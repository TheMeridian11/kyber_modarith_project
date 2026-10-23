# Git handoff and final branch integration

## Current verified state

I work on reduction-counters at 99733b9f5401236708ca25be9efd807cff60d7ce. The supplied push output reports success and the local origin/reduction-counters ref equals that commit. This backs up ACT-0019 and EXP-009/RUN-0001, but not the two later uncommitted result directories. Local main and origin/main remain dac387fe75fa260ccecd1211c57b716025ed2ad4, an ancestor 35 commits behind. I verified local objects/refs without running Git or contacting the remote. [Evidence](evidence/ACT-0020/source-and-branch-review.json).

All three sessions are accepted and the [final candidate is EXP-005](final_candidate.md). The 910 archived files in RUN-0002/RUN-0003 and the ACT-0020 reports/graphs still need the user commit and push. The ignored build directories remain local; their commands and binary identities are retained. All original raw bytes and all frozen measurement support are preserved.

## Commit and back up the closing evidence

I perform Git commands manually, review the staged content and stop if a command fails:

```sh
git diff --check
git add -- README.md notes/ analysis/ \
  results/EXP-009/RUN-0002/ results/EXP-009/RUN-0003/
git diff --cached --check
git diff --cached --stat
git diff --cached
git commit -m "Complete EXP-009 comparisons and select EXP-005 for the thesis"
git push
git status --short
```

A normal push sends committed history. It does not include any untracked result files merely because a benchmark finished. I preserve all cited experiment commits and do not use force push to resolve a rejection. No further timing session is required by the completed protocol.

## Manual selected-source handoff

The current implementation/kyber-optimised-ref directory still contains EXP-006. I checked all 35 source identities against [the selected snapshot](../analysis/final_candidate.json); only indcpa.c, polyvec.c and polyvec.h differ. The selected EXP-005 bytes have already been validated and measured in all closing sessions.

After committing the evidence above and checking the tree, I can restore those exact three historical files as a separate, reviewable source commit. This is restoration of the measured candidate, not a new arithmetic treatment. The assistant has not executed this step:

```sh
git restore --source=4bd813ed71a90c7722275dc802336852214a5388 --worktree -- \
  implementation/kyber-optimised-ref/indcpa.c \
  implementation/kyber-optimised-ref/polyvec.c \
  implementation/kyber-optimised-ref/polyvec.h
python3 -B - <<'PY'
from pathlib import Path
import hashlib, json
root = Path.cwd()
pin = json.loads((root / "analysis/final_candidate.json").read_text())
directory = root / "implementation/kyber-optimised-ref"
actual = {p.relative_to(directory).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
          for p in directory.rglob("*") if p.is_file()
          and (p.suffix in (".c", ".h") or p.name == "Makefile")}
assert actual == pin["source_file_sha256"], "Selected-source identity mismatch; stop and inspect"
print("Selected EXP-005 source identity: pass (35 files)")
PY
git diff --check
git diff -- implementation/kyber-optimised-ref/
```

I request the final handoff review after this identity check, before labelling the working checkout or practical handoff complete. That review updates the current-status documentation from EXP-006 to the actually verified selected source, checks reproduction instructions and records the final commit scope. I then commit the exact restored files and the corresponding reviewed documentation together, and make a normal push. There is no need to invent new optimisations or rerun a valid session merely because its effect is small. If the restored source does not match all 35 pinned files, I stop and resolve the discrepancy before making equivalence claims.

## Reproduce the accepted analysis

The retained-data analysis does not need ignored binaries or another benchmark run. I use a new output directory:

```sh
python3 -B scripts/analyse_final_comparison.py \
  --runs results/EXP-009/RUN-0001 results/EXP-009/RUN-0002 results/EXP-009/RUN-0003 \
  --output /tmp/exp009-final-analysis-copy
```

The complete identity audit also needs the exact retained tools, binaries and restored source files:

```sh
python3 -B analysis/review_final_comparison.py --output /tmp/exp009-final-audit-copy
```

[Figure instructions](thesis_figures.md) use the pinned plotting environment and a new output directory. ACT-0020 reproduced all three combined-analysis files, all three audit reports and all thirteen final figure/data/provenance files byte-for-byte. This demonstrates reproduction from retained evidence, not a new clean-environment performance study. The frozen protocol/experiment files remain unchanged so those identities remain verifiable.

## Final integration later

Once all EXP-009 results, final selection, figures and reproduction checks are accepted and committed, I fetch origin and inspect current branch ancestry. If main is still an ancestor, a fast-forward merge can move main to the reviewed work while preserving every cited commit; `git merge --ff-only reduction-counters` refuses if that condition is not met. I first update local main appropriately from the fetched origin/main. If either history has diverged, I inspect it and prepare a normal history-preserving merge or pull request instead. I do not squash, rebase or force-push the cited experiment history. [Git merge documentation](https://git-scm.com/docs/git-merge).

The initial local ancestry makes a straightforward final integration likely, but it does not establish the remote state. No push, fetch, switch, merge, commit, reset or branch deletion was executed by the assistant. Branch cleanup is optional after the final history is safely present on the remote.
