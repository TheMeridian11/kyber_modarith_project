# EXP-010 — Accepted random-seed follow-up

## Outcome

All five sessions planned before collection were accepted in ACT-0026. The follow-up supports the substantial cumulative performance gains reported in EXP-009 on the recorded platform. Both optimised implementations beat the original in every one of their 540 matched operation/block comparisons. The selected EXP-005 implementation retains additional key-generation benefit in every session median for all three parameter sets.

The smaller differences between the two candidates need a more careful interpretation. Kyber1024 decapsulation remains slower than EXP-003, while the earlier small Kyber1024 encapsulation penalty does not recur consistently. EXP-005 remains the selected candidate, with EXP-003 retained as an alternative where Kyber1024 decapsulation or the simpler keygen path is the priority. Neither candidate is the fastest in every individual observation.

## Evidence and acceptance

The [frozen protocol](experiments/EXP-010-random-seeds.md) and [saved plan](../tests/random_seed_plan.json) preceded collection. I keep their original wording about planned work and leave the files unchanged. Sixty distinct random uint64 seeds are spread over five separately launched sessions, with 12 matched blocks per parameter in each session. A block uses the same seed for all three implementations; the unchanged SHAKE256 fixture generator includes the parameter, phase and iteration. Each of the six variant orders occurs twice per parameter/session.

| Session | Retained record | Build / measurement processes | Duration rows | Review |
|---|---|---:|---:|---|
| 1 | [RUN-0001](../results/EXP-010/RUN-0001/manifest.json) | 9 / 108 | 324000 | accepted |
| 2 | [RUN-0002](../results/EXP-010/RUN-0002/manifest.json) | 9 / 108 | 324000 | accepted |
| 3 | [RUN-0003](../results/EXP-010/RUN-0003/manifest.json) | 9 / 108 | 324000 | accepted |
| 4 | [RUN-0004](../results/EXP-010/RUN-0004/manifest.json) | 9 / 108 | 324000 | accepted |
| 5 | [RUN-0005](../results/EXP-010/RUN-0005/manifest.json) | 9 / 108 | 324000 | accepted |

The [reproducible audit](../analysis/review_random_seed_comparison.py) and [review record](evidence/ACT-0026/exp010-five-session-review.json) verify 1125 successful steps, 2250 raw output files, 45 warning-free builds, 45 retained executable hashes and 540 normalised production-function bodies. Source snapshots, all 31 recorded support files, compiler/flags, seed/order schedules and recorded affinity match the declared study. All 35 working optimisation files still match the selected source pin.

Across the five sessions, 540 fresh measurement processes contain 540000 measured exchanges and 1620000 duration rows. Every measured round-trip flag is successful. Another 54000 warm-up exchanges are checked by the unchanged hash-verified harness before measurement; I establish their success from the successful process exits, rather than from separate warm-up CSV records.

The audit independently sorts the raw integer durations and uses rational arithmetic for process medians, paired ratios, session medians and interpolated quartiles. All 1620 paired effects, 135 session estimates and 27 combined summaries agree with the saved analysis. The 15 per-session derived tables reproduce byte-for-byte. EXP-009's raw data also reproduce its existing summary tables. No new measurements or Git commands were executed during this review.

## Estimator and conditions

Each process contributes the median of 1000 timings. Within a matched block, percentage time reduction is `100 × (1 − candidate median / reference median)`. The session estimate is the median of its 12 block effects. The final estimate is the median of five session estimates. Positive values mean faster. No observations were trimmed, excluded or adjusted by timer overhead.

The recorded environment matches the earlier study: Intel Core i9-12900KS, Ubuntu 24.04.2 under WSL2, GCC 13.3.0, CLOCK_MONOTONIC_RAW nanoseconds and guest logical CPU 0. All runs use the same recorded source/support commit. Timer resolution is 1 ns in every process; the minimum empty-pair diagnostics range from 11 to 19 ns across the study, without subtraction. Power plan, background workload, breaks, physical core placement, frequency and temperature remain unrecorded for these sessions. The earlier retrospective workload account is not automatically applied to this follow-up. See [benchmark conditions](benchmark_conditions.md).

EXP-009 and EXP-010 remain separate studies. The following tables compare their declared three-session and five-session summaries. They do not pool the sessions or reinterpret inner durations as independent experimental repetitions. The differences between columns are in percentage points. They are not additional relative speedups and do not tell me how much of the change was caused by the seeds.

## Cumulative inverse-transform candidate versus original

EXP-003 includes the preceding fused base-multiplication and wide-dot changes as well as the staged inverse transform. All 45 session estimates and all 540 block effects against the original are positive.

| Parameter | Operation | EXP-009 median | EXP-010 median | Change (percentage points) | Five-session range |
|---|---|---:|---:|---:|---:|
| Kyber512 | keygen | +5.968% | +5.885% | -0.083 | +5.436 to +6.575% |
| Kyber512 | encap | +15.389% | +15.323% | -0.066 | +15.121 to +15.975% |
| Kyber512 | decap | +15.586% | +15.435% | -0.151 | +15.164 to +16.005% |
| Kyber768 | keygen | +13.184% | +13.429% | +0.245 | +13.066 to +13.565% |
| Kyber768 | encap | +18.476% | +18.602% | +0.126 | +18.506 to +18.966% |
| Kyber768 | decap | +18.643% | +18.638% | -0.004 | +18.521 to +18.959% |
| Kyber1024 | keygen | +16.066% | +16.391% | +0.325 | +16.371 to +16.865% |
| Kyber1024 | encap | +19.484% | +20.096% | +0.612 | +19.689 to +20.332% |
| Kyber1024 | decap | +20.002% | +20.739% | +0.737 | +20.264 to +20.914% |

## Selected implementation versus original

EXP-005 includes EXP-003 and the keygen error-vector reduction deferral. All 45 session estimates and all 540 block effects against the original are positive. Its five-session reductions span 10.93–20.18% across the nine workloads, compared with 10.72–19.71% in EXP-009. This span is across different operations and parameters, not an uncertainty interval or single overall speed score.

| Parameter | Operation | EXP-009 median | EXP-010 median | Change (percentage points) | Five-session range |
|---|---|---:|---:|---:|---:|
| Kyber512 | keygen | +10.720% | +10.929% | +0.209 | +10.535 to +10.972% |
| Kyber512 | encap | +16.092% | +16.092% | +0.001 | +15.818 to +16.233% |
| Kyber512 | decap | +15.962% | +16.061% | +0.099 | +15.714 to +16.111% |
| Kyber768 | keygen | +13.441% | +13.617% | +0.176 | +13.406 to +13.875% |
| Kyber768 | encap | +19.075% | +19.223% | +0.148 | +19.094 to +19.605% |
| Kyber768 | decap | +18.801% | +19.014% | +0.213 | +18.777 to +19.342% |
| Kyber1024 | keygen | +17.468% | +17.842% | +0.375 | +17.705 to +17.940% |
| Kyber1024 | encap | +19.302% | +19.866% | +0.565 | +19.644 to +20.019% |
| Kyber1024 | decap | +19.711% | +20.182% | +0.471 | +19.952 to +20.236% |

The selected implementation's nine summaries differ from the earlier values by at most 0.565 percentage points. This supports a similar scale of improvement under the additional sampled inputs and measurement conditions. It does not prove that the numerical results are equivalent or that the random seeds caused the small shifts.

## Additional selected-candidate effect

This direct contrast measures EXP-005 relative to EXP-003. It is calculated from their matched process medians; subtracting their separate original-reference summaries would not give the same statistic.

| Parameter | Operation | EXP-009 median | EXP-010 median | Five-session range | Faster / slower sessions | Faster / slower blocks |
|---|---|---:|---:|---:|---:|---:|
| Kyber512 | keygen | +5.261% | +5.241% | +4.838 to +5.413% | 5 / 0 | 60 / 0 |
| Kyber512 | encap | +0.694% | +0.728% | +0.536 to +0.873% | 5 / 0 | 52 / 8 |
| Kyber512 | decap | +0.453% | +0.638% | +0.351 to +0.769% | 5 / 0 | 47 / 13 |
| Kyber768 | keygen | +0.486% | +0.200% | +0.020 to +0.495% | 5 / 0 | 41 / 19 |
| Kyber768 | encap | +0.691% | +0.714% | +0.416 to +0.875% | 5 / 0 | 49 / 11 |
| Kyber768 | decap | +0.229% | +0.321% | -0.038 to +0.447% | 4 / 1 | 43 / 17 |
| Kyber1024 | keygen | +1.523% | +1.687% | +1.459 to +1.921% | 5 / 0 | 58 / 2 |
| Kyber1024 | encap | -0.147% | +0.091% | -0.219 to +0.244% | 3 / 2 | 31 / 29 |
| Kyber1024 | decap | -0.356% | -0.405% | -0.692 to -0.133% | 0 / 5 | 11 / 49 |

The additional keygen reductions are 5.24%, 0.20% and 1.69% for Kyber512/768/1024. All five session medians are positive for each parameter, but the Kyber768 benefit is smaller than the earlier 0.49% and includes 19 negative block effects. Kyber1024 keygen includes two negative blocks. These observations remain in the data and figures.

Kyber1024 decapsulation has a median change of −0.405%, with all five session medians negative and 49 of 60 blocks slower. This supports the earlier observed cost of −0.356%. Kyber1024 encapsulation instead has a median of +0.091%, with three positive and two negative session medians and 31 faster versus 29 slower blocks. Its earlier −0.147% penalty is therefore not supported as a consistent cross-study effect. Kyber768 decapsulation also has one slightly negative session despite a positive five-session median.

The last arithmetic treatment changes keygen only. Small encapsulation/decapsulation movements must not be attributed to arithmetic removed from those unchanged call paths. Code layout and environmental variation are possible explanations, not demonstrated causes.

## Graphs and reproducibility

The [original-reference graph](../analysis/figures/EXP-010/exp010-original-reference-dot-box.pdf) contains all 1080 baseline-reference effects. The [direct-candidate graph](../analysis/figures/EXP-010/exp010-direct-candidate-dot-box.pdf) contains all 540 additional effects. Each is also available as SVG and 300-dpi PNG, with plotted CSV data, box statistics and [provenance](../analysis/figures/EXP-010/provenance.json).

Colour and shape identify sessions. Boxes show the middle 50% of the 60 block effects with their pooled median; whiskers span the full observed minimum and maximum. Black diamonds retain the declared median of five session medians, which can differ from the pooled block median. All adverse effects are included. Neither boxes nor ranges are confidence intervals.

The five combined-analysis files and eleven graph/data/provenance files reproduced byte-for-byte in a separate temporary directory. Both PNG layouts were visually reviewed for readable labels, visible negative effects, complete axes and clear summary definitions. See [reproduction evidence](evidence/ACT-0026/artifact-reproduction.json) and [figure review](evidence/ACT-0026/figure-review.json). The original outputs require no correction.

To repeat the full retained-data and local-binary audit, use a new output path:

```sh
python3 -B analysis/review_random_seed_comparison.py --output /tmp/exp010-review-copy.json
```

This full audit requires the retained ignored executables and restored source directories. The analysis and graph commands in the [protocol](experiments/EXP-010-random-seeds.md) can reproduce retained-data summaries without those binaries; choose new output directories.

## Thesis interpretation and limits

The follow-up strengthens the observed robustness of the large original-reference gains and supports retaining the selected candidate for its additional keygen benefit. It also refines the tradeoff account: the Kyber1024 decapsulation cost repeats, while encapsulation is mixed and close to zero in the direct comparison. The earlier findings remain a valid record of EXP-009; the new evidence qualifies their broader interpretation rather than replacing those measurements.

A thesis-ready statement is: “A separate five-session random-input follow-up reproduced the substantial cumulative performance gains on the same WSL platform. The selected implementation reduced key-generation time by 10.93–17.84%, encapsulation by 16.09–19.87% and decapsulation by 16.06–20.18% across the three parameter sets, using medians of five session estimates. Every matched original-reference comparison favoured both optimised implementations. Additional key-generation benefit over the preceding candidate persisted, while small control-operation differences were less uniform: the Kyber1024 decapsulation penalty repeated, but its earlier encapsulation penalty did not recur consistently.”

These are descriptive, single-platform findings. Each seed occurs in one matched block, so I cannot separate variation caused by the inputs from changes in measurement conditions. Parameter groups and comparisons also share seeds and measurements, which makes them related. Five invocations do not establish statistical independence, population significance, portability or a universal speedup. The follow-up adds identity checks and round trips, not a new leakage test, constant-time proof or final ML-KEM conformance result. The [existing security conclusion](final_security_summary.md) retains its original limits. No optimisation change or additional outcome-dependent session is warranted by this review.

