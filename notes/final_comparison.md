# EXP-009 — Complete three-session result

I accept all three predeclared sessions in ACT-0020 and close the direct comparison. I select EXP-005 as the primary thesis candidate with the explicit tradeoffs in [the decision record](final_candidate.md). EXP-003 remains a retained comparator and a reasonable alternative for workloads prioritising Kyber1024 encapsulation/decapsulation or the simpler keygen call path. EXP-006 remains the adverse/secondary research result.

## Evidence and method

[Session 1](runs/EXP-009-RUN-0001.md) uses source/support commit 8a5e36e5d041507cc5649c7d43edb8468000f476. [Session 2](runs/EXP-009-RUN-0002.md) and [session 3](runs/EXP-009-RUN-0003.md) use 99733b9f5401236708ca25be9efd807cff60d7ce. Exact frozen support, protocol, source files, compiler, flags and disassembler identities match across all three. The actual source variants are the original pinned reference, EXP-003 from cf8ae0dd700bb41628c158016a7c15926a0b790f and EXP-005 from 4bd813ed71a90c7722275dc802336852214a5388. The current production checkout remains EXP-006 and was not measured as a closing candidate.

The [combined audit](evidence/ACT-0020/exp-009-three-session-review.json) checks all 675 successful steps, 1350 raw files, 27 binaries and 324 production-body extractions. All 27 builds are warning-free. The three sessions contain 324 fresh measurement processes, 324000 measured exchanges and 972000 duration rows, plus 32400 checked warm-up exchanges. Every measured and warm-up shared-secret round trip succeeds. Each session's three derived tables reproduce byte-for-byte; independent arithmetic recalculates the medians, ratios, effects, ranges and signs. No durations are excluded or adjusted.

The [predeclared analyser](../scripts/analyse_final_comparison.py) writes [81 session estimates](../analysis/final-comparison-EXP-009/session-effects.csv), [27 combined contrasts](../analysis/final-comparison-EXP-009/three-session-effects.csv) and [provenance](../analysis/final-comparison-EXP-009/provenance.json). For each block I first compare process medians, then take the median of 12 effects within a session, then the median of those three session estimates. I report the three estimates and their observed min–max; the range is descriptive, not a confidence interval. I do not treat 1000 inner durations as independent repetitions or pool the 36 block effects to replace the predeclared final estimator.

All six variant orders occur twice per parameter in every session, with distinct predeclared block/session seeds. The recorded environment is one i9-12900KS WSL2 guest, GCC 13.3.0 normal builds, CLOCK_MONOTONIC_RAW in ns and logical CPU 0. Manual power/background/physical placement fields remain unknown. Three complete invocations are established; break duration and environmental independence are not. These results do not establish cross-platform performance or population significance.

## EXP-003 relative to the original

Positive means faster. Values are percentage time reductions. Block signs count all 36 pairs descriptively; those counts do not define a significance test.

| Parameter | Operation | Session 1 | Session 2 | Session 3 | Median | Session range | Faster / slower blocks |
|---|---|---:|---:|---:|---:|---:|---:|
| Kyber512 | keygen | +5.968 | +5.801 | +6.234 | +5.968 | +5.801 to +6.234 | 36 / 0 |
| Kyber512 | encap | +15.287 | +15.389 | +15.843 | +15.389 | +15.287 to +15.843 | 36 / 0 |
| Kyber512 | decap | +15.432 | +15.586 | +15.798 | +15.586 | +15.432 to +15.798 | 36 / 0 |
| Kyber768 | keygen | +13.237 | +13.117 | +13.184 | +13.184 | +13.117 to +13.237 | 36 / 0 |
| Kyber768 | encap | +18.476 | +18.558 | +18.474 | +18.476 | +18.474 to +18.558 | 36 / 0 |
| Kyber768 | decap | +18.643 | +18.644 | +18.574 | +18.643 | +18.574 to +18.644 | 36 / 0 |
| Kyber1024 | keygen | +16.009 | +16.066 | +16.076 | +16.066 | +16.009 to +16.076 | 36 / 0 |
| Kyber1024 | encap | +19.319 | +19.591 | +19.484 | +19.484 | +19.319 to +19.591 | 36 / 0 |
| Kyber1024 | decap | +19.944 | +20.086 | +20.002 | +20.002 | +19.944 to +20.086 | 36 / 0 |

## EXP-005 relative to the original

Positive means faster. Values are percentage time reductions. Block signs count all 36 pairs descriptively; those counts do not define a significance test.

| Parameter | Operation | Session 1 | Session 2 | Session 3 | Median | Session range | Faster / slower blocks |
|---|---|---:|---:|---:|---:|---:|---:|
| Kyber512 | keygen | +10.720 | +10.655 | +10.921 | +10.720 | +10.655 to +10.921 | 36 / 0 |
| Kyber512 | encap | +15.896 | +16.092 | +16.232 | +16.092 | +15.896 to +16.232 | 36 / 0 |
| Kyber512 | decap | +15.843 | +15.962 | +16.052 | +15.962 | +15.843 to +16.052 | 36 / 0 |
| Kyber768 | keygen | +13.540 | +13.441 | +13.230 | +13.441 | +13.230 to +13.540 | 36 / 0 |
| Kyber768 | encap | +19.067 | +19.130 | +19.075 | +19.075 | +19.067 to +19.130 | 36 / 0 |
| Kyber768 | decap | +18.682 | +18.932 | +18.801 | +18.801 | +18.682 to +18.932 | 36 / 0 |
| Kyber1024 | keygen | +17.377 | +17.520 | +17.468 | +17.468 | +17.377 to +17.520 | 36 / 0 |
| Kyber1024 | encap | +19.270 | +19.702 | +19.302 | +19.302 | +19.270 to +19.702 | 36 / 0 |
| Kyber1024 | decap | +19.586 | +20.145 | +19.711 | +19.711 | +19.586 to +20.145 | 36 / 0 |

## EXP-005 relative to EXP-003

Positive means faster. Values are percentage time reductions. Block signs count all 36 pairs descriptively; those counts do not define a significance test.

| Parameter | Operation | Session 1 | Session 2 | Session 3 | Median | Session range | Faster / slower blocks |
|---|---|---:|---:|---:|---:|---:|---:|
| Kyber512 | keygen | +5.261 | +5.180 | +5.313 | +5.261 | +5.180 to +5.313 | 36 / 0 |
| Kyber512 | encap | +0.707 | +0.694 | +0.667 | +0.694 | +0.667 to +0.707 | 30 / 6 |
| Kyber512 | decap | +0.553 | +0.453 | +0.431 | +0.453 | +0.431 to +0.553 | 28 / 8 |
| Kyber768 | keygen | +0.486 | +0.488 | +0.465 | +0.486 | +0.465 to +0.488 | 29 / 7 |
| Kyber768 | encap | +0.594 | +0.730 | +0.691 | +0.691 | +0.594 to +0.730 | 34 / 2 |
| Kyber768 | decap | +0.038 | +0.332 | +0.229 | +0.229 | +0.038 to +0.332 | 26 / 10 |
| Kyber1024 | keygen | +1.621 | +1.325 | +1.523 | +1.523 | +1.325 to +1.621 | 34 / 2 |
| Kyber1024 | encap | -0.012 | -0.186 | -0.147 | -0.147 | -0.186 to -0.012 | 16 / 20 |
| Kyber1024 | decap | -0.356 | -0.583 | -0.301 | -0.356 | -0.583 to -0.301 | 6 / 30 |

## Interpretation

Every session median against the original is positive for both candidates, and all 324 paired operation/block comparisons per candidate are positive. This establishes substantial cumulative benefit in the tested setting. EXP-003's three-session median reductions span 5.97–20.00% across the nine groups; EXP-005's span 10.72–19.71%. These are ranges across different workloads, not an overall speed score.

EXP-005's additional keygen benefit recurs in all three session medians for all parameters. Its median additional reductions are 5.26%, 0.49% and 1.52%; observed session ranges are 5.18–5.31%, 0.46–0.49% and 1.32–1.62%. Kyber1024 encapsulation and decapsulation regress in all three session medians, by 0.15% and 0.36% respectively in the three-session median, with observed session ranges −0.19 to −0.01% and −0.58 to −0.30%. These are modest but repeatable observed costs; they are not discarded because the absolute cumulative benefit remains large.

Some individual effects are substantially less favourable than the session medians; the [all-pairs figure](../analysis/figures/ACT-0020/exp009-all-paired-effects.svg) retains every one. Session direction agreement describes repeatability here, not a calibrated significance result. No additional session or outlier exclusion is selected from these results.

I use the direct EXP-003-to-EXP-005 contrast to assess the additional change. Medians of paired ratios are nonlinear: differences between two original-reference summaries need not equal the median direct contrast, even for the same three variants. I do not subtract these summary columns, add old incremental percentages or infer the runtime of a single Barrett call. The EXP-005 source change is only in keygen; unchanged-operation movements may involve layout/environment effects, but this experiment does not identify a cause.

## Correctness, security and artifacts

Exact source and normal-code matches support reuse of accepted arithmetic, byte-compatibility, malformed/noncanonical-input and exercised UBSan findings. The distinct EXP-007 dynamic-flow and EXP-008 statistical-screen matrices retain their coverage limits. EXP-009 contributes operation timing, round trips and identity checks; it is not additional leakage evidence. The inherited dot-product canary change and keygen code/local-frame costs are retained in the [candidate decision](final_candidate.md) and [consolidated security matrix](final_security_summary.md).

I generated complete [three-session effects](../analysis/figures/ACT-0020/exp009-three-session-effects.svg), [all paired effects](../analysis/figures/ACT-0020/exp009-all-paired-effects.svg) and [keygen tradeoff](../analysis/figures/ACT-0020/exp005-keygen-tradeoffs.svg) figures, each with vector PDF/SVG, 300-dpi PNG and machine-readable data. [Captions and reproduction](thesis_figures.md) identify units, experimental units and scope. Earlier preliminary figures remain unchanged as historical artifacts.

All predeclared performance and security collection is complete. I do not add more benchmark sessions to strengthen a preferred result. Remaining work is the final source/reproduction/repository handoff and thesis composition, including verification of literature claims that require full-text sources. A final source snapshot must be identified accurately; the current EXP-006 checkout must not be labelled the chosen EXP-005 implementation.
