# Git handoff and final branch integration

## Current verified state — ACT-0022

I work on reduction-counters at 66c707f9dc8cef556d1133fb48d6fb1f71e989e7, the closing-results commit. The supplied successful push and matching local origin/reduction-counters ref establish the reported backup. All 4474 archived result files and ACT-0020's reports, final selection and graphs are committed. ACT-0021 verified that commit's exact scope. [Backup review](evidence/ACT-0021/source-and-handoff-review.json).

I have now restored and reviewed the actual selected EXP-005 working source. All 35 files match analysis/final_candidate.json, the verified historical snapshot at 4bd813ed71a90c7722275dc802336852214a5388, both accepted security manifests and all three final comparison manifests. The actual source diff exactly matches the previously reviewed 2 insertions and 41 deletions across indcpa.c, polyvec.c and polyvec.h. No repair was needed. The red deletion lines in git diff remove the expected EXP-006-only function and declaration; they do not indicate an error. [Final source review](evidence/ACT-0022/selected-source-review.json).

The source now contains cumulative EXP-001/002/003/005. Keygen calls the general dot product followed by poly_tomont, retains the EXP-005 raw error-vector transform and keeps secret-vector centring and the final public-key reduction. EXP-006 remains preserved in historical commits and results. The selection manifest's checkout_at_selection field accurately describes ACT-0020 and is retained unchanged as historical evidence.

I granted a one-time exception allowing the assistant to repair this restoration if needed. Inspection found it already correct, so no assistant production-source edit was necessary. Git operations remain manual under the research workflow. The scientific work, source review, reproduced evidence and handoff documentation are complete. No additional experiment or source repair is required before the commands below. The final commit/push and main integration have not yet happened.

## 1. Commit and push the reviewed handoff

I review and commit the existing restoration together with ACT-0021/ACT-0022 documentation and evidence. I do not rerun the restore command. The exact intended scope is:

- Three source files: implementation/kyber-optimised-ref/indcpa.c, polyvec.c and polyvec.h.
- README.md and ten notes: experiment_register.md, final_candidate.md, final_comparison.md, final_security_summary.md, git_handoff.md, implementation_security.md, practical_completion.md, project_log.md, reduction_map.md and thesis_writing_plan.md.
- Two evidence files in notes/evidence/ACT-0021/ and two in notes/evidence/ACT-0022/.

That is 18 changed/new files relative to the closing-results commit: 14 modified tracked files and four new evidence files. Existing results, analysis code/data, selection pins and figures are unchanged. [Final verification](evidence/ACT-0022/final-verification.json) records the exact reviewed hashes. I run each command in order, inspect its output and stop on any failure or unexpected staged file:

```sh
git diff --check
git status --short
git add -- README.md \
  implementation/kyber-optimised-ref/indcpa.c \
  implementation/kyber-optimised-ref/polyvec.c \
  implementation/kyber-optimised-ref/polyvec.h \
  notes/experiment_register.md notes/final_candidate.md \
  notes/final_comparison.md notes/final_security_summary.md \
  notes/git_handoff.md notes/implementation_security.md \
  notes/practical_completion.md notes/project_log.md \
  notes/reduction_map.md notes/thesis_writing_plan.md \
  notes/evidence/ACT-0021/ notes/evidence/ACT-0022/
git diff --cached --check
git diff --cached --stat
git diff --cached
git commit -m "Restore selected EXP-005 source and complete the thesis handoff"
git push
git status --short
```

I expect the final status to be empty. A pager may show a colon or END while viewing a long diff; I press q to return to the terminal prompt. Diff colours and a pager are not build/test failures. I preserve cited commits; no reset, history rewrite or force push is needed. This handoff review is complete, so a successful staged review/commit/push does not require another experimental review before proceeding to main integration.

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

Existing ignored binaries are not relabelled by restoring source files. Accepted executable identities remain those recorded by their manifests and retained run build directories. The current source identity review reuses those accepted results; it does not claim that a new build or test was executed in ACT-0022. Historical measurement/validation runners retain their original variant gates and frozen support; replaying an old experiment uses its documented source revision and a new run ID, rather than editing those gates to fit the final checkout. No such replay is required to finish this study.

## 2. Integrate the reviewed branch into main

After the handoff commit is pushed and git status --short is empty, I fetch origin so the remote-tracking refs reflect the server. [Git fetch documentation](https://git-scm.com/docs/git-fetch). I run each command separately, inspect its result and stop on any failure:

```sh
git fetch origin
git status --short
git switch main
git merge --ff-only origin/main
git merge --ff-only reduction-counters
git push origin main
git status --short
git branch -vv
```

I proceed past the status check only with a clean working tree. The first merge updates local main from fetched origin/main; the second advances main to the reviewed research branch if ancestry permits. Fast-forward-only merges refuse divergent histories instead of creating an unexpected merge. [Git merge documentation](https://git-scm.com/docs/git-merge). If either merge or the push is rejected, I retain the output and review the changed history before proceeding. A protected main branch may instead require a pull request with history-preserving integration. I do not squash, rebase or force-push the cited experiment history.

I retain reduction-counters as a research-history branch; deleting it is unnecessary. I report successful main integration only after the commands actually succeed. Local main and origin/main were still dac387fe75fa260ccecd1211c57b716025ed2ad4 at the ACT-0022 inspection, 36 commits behind the closing-results commit; the pending handoff commit will add another commit. The fetch above establishes fresh remote state. The assistant has executed no Git command or production arithmetic edit. Branch integration is repository housekeeping and does not delay drafting the thesis from the already accepted evidence.
