# Git handoff and final branch integration

## Current verified state

I work on reduction-counters. In ACT-0018 I read verified Git objects without running Git: HEAD is 50db1e8cb1cbd7eada48b4a47a1fe5bd92ae2f6d, 33 commits ahead of local main dac387fe75fa260ccecd1211c57b716025ed2ad4. Local origin/main names the same older commit. Main is an ancestor of the branch; the remote has not been contacted, so its current state is unknown. [Evidence](evidence/ACT-0018/source-and-branch-review.json).

A working branch is normal and does not invalidate any results. I preserve all experiment commit identities. I can back up the branch before the practical work or thesis is finished. The final main-branch integration is a separate step after closing review.

## Review and commit this handoff

I perform these Git commands manually from the repository root and stop if a command fails. I inspect the diff before committing:

```sh
git diff --check
git add -- .gitattributes README.md notes/ analysis/   scripts/run_final_comparison.py scripts/analyse_final_comparison.py   tests/final_comparison_protocol.json tests/test_final_comparison_analysis.py   results/EXP-008/RUN-0001/
git diff --cached --check
git diff --cached --stat
git diff --cached
git commit -m "Review EXP-008 and prepare final three-way comparisons"
git status --short
```

This includes the previously untracked EXP-008 results. Formal EXP-009 collection requires these support/evidence files to be committed. The [EXP-009 protocol](experiments/EXP-009-final-comparison.md) contains the three separate run commands and final analysis command.

The warnings in the supplied screenshot are trailing spaces emitted by objdump in raw EXP-007 logs. I preserve those bytes and hashes. The new root .gitattributes disables end-of-line conversion for results and whitespace-error reporting only for raw .log files. It does not rewrite logs or turn off checks on source, notes or generated SVGs. I do not run a repository-wide whitespace fixer or renormalisation. These attribute semantics follow the [Git attributes documentation](https://git-scm.com/docs/gitattributes).

## Backup push

After reviewing and committing the intended files, I can push the existing branch:

```sh
git push -u origin reduction-counters
```

This sends committed branch history; uncommitted or ignored build files are not backed up by it. It does not require moving main or finishing the thesis. The configured origin is https://github.com/TheMeridian11/kyber_modarith_project.git. I use a normal push, never a force push to resolve a rejection. [GitHub push documentation](https://docs.github.com/en/get-started/using-git/pushing-commits-to-a-remote-repository).

## Final integration later

Once all EXP-009 results, final selection, figures and reproduction checks are accepted and committed, I fetch origin and inspect current branch ancestry. If main is still an ancestor, a fast-forward merge can move main to the reviewed work while preserving every cited commit; `git merge --ff-only reduction-counters` refuses if that condition is not met. I first update local main appropriately from the fetched origin/main. If either history has diverged, I inspect it and prepare a normal history-preserving merge or pull request instead. I do not squash, rebase or force-push the cited experiment history. [Git merge documentation](https://git-scm.com/docs/git-merge).

The initial local ancestry makes a straightforward final integration likely, but it does not establish the remote state. No push, fetch, switch, merge, commit, reset or branch deletion was executed by the assistant. Branch cleanup is optional after the final history is safely present on the remote.
