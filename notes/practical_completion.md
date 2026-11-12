# Practical completion record

I have completed the original experiments, checked the selected source and finished the separate random-seed follow-up. The selected implementation is EXP-005; the [candidate decision](final_candidate.md) records its identity, rationale and tradeoffs.

| Completed work | Authoritative record |
|---|---|
| Baseline preparation and five arithmetic trials, including mixed/adverse findings | [Experiment register](experiment_register.md) |
| Dynamic secret-flow checks and bounded statistical timing screen | [Security conclusion and coverage](final_security_summary.md) |
| Main three-session comparison and candidate selection | [EXP-009 results](final_comparison.md) |
| Supplementary five-session random-seed robustness check | [EXP-010 results](random_seed_followup.md) |
| Selected-source identity and reproducible outputs | [Source review](evidence/ACT-0022/selected-source-review.json), [follow-up verification](evidence/ACT-0026/final-verification.json), [reproduction guide](git_reproduce.md) |

The remaining work is to write the thesis. This includes explaining the methods, presenting both the improvements and adverse findings, discussing the limitations, and checking literature-dependent claims against the full text. The [writing plan](thesis_writing_plan.md) maps those tasks to the original research questions.

EXP-004 was a deferred interaction study, not an unfinished required experiment. VTune was excluded. A fresh-platform evaluation, AVX2 transfer, whole-program constant-time proof, physical/fault testing and final ML-KEM certification remain outside the established results. No further measurement is required by the completed protocols.
