# Final candidate decision — EXP-005

## Decision and exact identity

I select **EXP-005 as the primary final thesis candidate** after accepting all three predeclared EXP-009 sessions. I retain EXP-003 as a substantial result, explicit comparator and a reasonable alternative for workloads prioritising Kyber1024 encapsulation/decapsulation or a simpler keygen path. I retain EXP-006 as the mixed/adverse trial; I do not adopt it as the general candidate.

The selected source is the 35-file implementation/kyber-optimised-ref snapshot at **4bd813ed71a90c7722275dc802336852214a5388**, pinned file-by-file in the [selection manifest](../analysis/final_candidate.json). This is cumulative EXP-001 fused base multiplication, EXP-002 wide vector dot product, EXP-003 staged inverse NTT and EXP-005 keygen error-vector reduction deferral. The original is upstream 3edd5af5991927164edd4aacebfcbee00b8064e7. I do not describe this historical Kyber implementation as certified final-standard ML-KEM.

ACT-0022 verifies that the actual production checkout now matches all 35 selected EXP-005 source hashes and the verified historical Git blobs. I manually restored indcpa.c, polyvec.c and polyvec.h; the other 32 files already matched. The actual diff is exactly the reviewed 2 insertions and 41 deletions, with no repair needed. [Source review](evidence/ACT-0022/selected-source-review.json). The selection manifest retains its accurate historical checkout-at-selection observation from ACT-0020; it is not the current checkout status. This restores the already tested candidate and introduces no new optimisation or measurement.

## Why I choose it

The [complete comparison](final_comparison.md) independently audits 972000 duration rows and retains all three contrasts, all operations, all parameters and all adverse pairs. Each candidate beats the original in every paired operation/block comparison across the three sessions. The following additional keygen benefits recur in every session median:

| Parameter | EXP-005 vs EXP-003 median reduction | Observed range of three session estimates | Faster / slower blocks across sessions |
|---|---:|---:|---:|
| Kyber512 | +5.26% | +5.18% to +5.31% | 36 / 0 |
| Kyber768 | +0.49% | +0.46% to +0.49% | 29 / 7 |
| Kyber1024 | +1.52% | +1.32% to +1.62% | 34 / 2 |

I judge this repeated keygen benefit useful for the reference-C study, particularly for Kyber512 and Kyber1024. This judgement accepts the explicit costs below; it does not claim that every workload benefits or assign unmotivated weights to operations. The predeclared decision was a documented tradeoff after three sessions, not an automatic score or an effect-dependent extension. Three same-host sessions provide descriptive repeatability, not calibrated population significance.

## Costs retained in the decision

EXP-005's Kyber1024 encapsulation and decapsulation session medians are slower than EXP-003 in all three sessions. The combined medians are **−0.15%** and **−0.36%**, with observed session ranges **−0.19 to −0.01%** and **−0.58 to −0.30%**. These effects are small in this setting, but consistent enough to report rather than dismiss. A workload dominated by those operations may reasonably prefer EXP-003. I do not label the differences insignificant: no calibrated significance test was specified.

Kyber512/768 control-operation medians are mildly positive, but EXP-005 changes only the keygen call path. I do not attribute those movements to removed arithmetic in encapsulation or decapsulation. Compiler layout and environmental effects are possible explanations, not established mechanisms. Some individual pairs are worse than their session summaries; all remain visible in the full data and all-pairs figure.

I rechecked the following scoped code/local-stack facts against all three sessions' matching keygen bodies and the accepted ACT-0013 review:

| Parameter | Keygen body bytes EXP-003 → EXP-005 | Additional body bytes | Local stack bytes EXP-003 → EXP-005 | Additional local stack |
|---|---:|---:|---:|---:|
| Kyber512 | 425 → 442 | +17 | 5256 → 5272 | +16 |
| Kyber768 | 479 → 512 | +33 | 9368 → 9384 | +16 |
| Kyber1024 | 948 → 988 | +40 | 15032 → 15032 | +0 |

Local stack includes saved registers, but excludes the entry return address and all callees. These numbers are not peak KEM stack, total memory or whole-binary size. EXP-005 removes 512/768/1024 keygen Barrett calls, 25% of the preceding keygen Barrett count, but the observed time reduction is much smaller and parameter dependent. This supports the thesis's distinction between reduction counts and measured performance.

## Security interpretation

The [consolidated matrix](final_security_summary.md) separates reviewed arithmetic contracts, sampled compatibility/invalid-input evidence, exercised UBSan, generated code, dynamic secret flow and statistical timing. No failing gate or new observed leakage finding appears for the selected source in those scopes. This is a bounded implementation assessment, not production approval or a constant-time proof.

EXP-005 retains the keygen canary load/check/failure call, endbr64 and stack probes. Both EXP-003 and EXP-005 inherit the EXP-002 general-dot change: removing the local array also removed that function's compiler-generated canary under the same flags. Thus EXP-003 does not avoid this inherited tradeoff, and EXP-005 does not add a new keygen-canary loss. I do not interpret instruction presence as runtime CET enforcement or assert that the canary change is exploitable or harmless.

The raw error-vector change has a caller-specific bound/consumer argument and sampled equivalence evidence. It does not permit removing reductions globally, widening the admissible input contract arbitrarily or claiming unchanged physical leakage when intermediate bit patterns change. EXP-008 directly tested original/EXP-003/EXP-005; EXP-007 directly tested original/EXP-005/EXP-006. I retain that distinction and all unassessed physical, fault, full-program and other-platform properties.

## Thesis emphasis and stopping decision

I give EXP-003 substantial emphasis because its inverse-transform scheduling produced a clear incremental encapsulation/decapsulation benefit and is already part of EXP-005. The final cumulative improvement must not be attributed wholly to EXP-005's last change. EXP-006 is also valuable evidence: fewer reductions alone did not ensure better measured performance. Together, the progression, adverse trial and layered security assessment answer the study's performance/correctness/tradeoff questions.

All predeclared performance and security collection is complete. I close EXP-009, keep both candidates and the adverse trial, and move to thesis writing with the selected source and handoff documentation verified in ACT-0022. I do not add hybrid parameter-specific variants, new optimisations or more timing sessions based on these outcomes. The [Git handoff](git_handoff.md) separates committing this evidence, backing up the branch and later preserving all cited history during main integration.
