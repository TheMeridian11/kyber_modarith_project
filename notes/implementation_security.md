# Implementation-security methods and coverage

## Purpose and current status

The assessment examines arithmetic validity, compatibility, secret-dependent control/address use, timing differences and compiler-hardening changes in the pinned Kyber reference C implementation. It covers the recorded GCC/x86-64 build and tested environment. The optimisations change reduction scheduling and intermediate representatives while retaining the intended algorithm and parameters. The completed findings are consolidated in the [security conclusion](final_security_summary.md); VTune and final-standard ML-KEM certification are outside the study.

| Evidence layer | What I can establish | Current status |
|---|---|---|
| Mathematical contracts | Caller ranges, Montgomery scale, intermediate/narrowing bounds and downstream contracts | Documented and reviewed for EXP-001/002/003/005/006 |
| Functional and invalid-input checks | Agreement on deterministic outputs and sampled malformed/noncanonical cases | Accepted for EXP-001/002/003/005/006 within the tested scope |
| Exercised undefined behaviour | UBSan observations on selected paths, alongside explicit narrowing arguments | Accepted for existing candidates including EXP-006; not an exhaustive proof |
| Generated code and hardening | Actual branches, addresses, reducers, code size, local stack and protection instructions in scoped functions | Reviewed per run; inherited EXP-002 local-canary tradeoff retained |
| Dynamic secret-flow checking | Executed branches/addresses influenced by marked secrets | Formal EXP-007/RUN-0001 accepted in ACT-0017: 144 quiet target processes, 18 sensitive positive controls |
| Statistical timing-leakage checks | Detectable timing differences between chosen secret classes on this build/target | EXP-008/RUN-0001 accepted in ACT-0018: 288 quiet target processes, maximum absolute t 2.91016; all 36 controls meet criteria |
| Whole-program/formal/physical security | Exhaustive constant time, power/EM, fault resistance, all-target behaviour | Not established; outside this practical claim |

## Complementary methods

The dudect authors describe comparing timing distributions for input classes and warn that failure to detect a difference is not proof of constant time. The result depends on the tested code, compiler and platform. The study uses a custom dudect-style harness for empirical timing evidence, separately from operation-performance benchmarks. [Author repository](https://github.com/oreparaz/dudect).

A ctgrind-style check instead marks secret-derived values and observes whether they reach control flow or memory addressing on executed paths. This provides a useful diagnosis when a timing test finds a difference, and can detect problematic data flow even when that machine's timing measurements are insensitive. The author's discussion contrasts these roles; the historical ctgrind repository demonstrates the marking approach. The dynamic tests use the verified Valgrind/Memcheck client-request interface. [dudect author discussion](https://www.reparaz.net/oscar/misc/dudect.html), [ctgrind repository](https://github.com/agl/ctgrind).

Memcheck tracks undefined values and reports problematic uses, including conditional decisions. Its diagnostics and origin tracking can help locate a dependency, but the test must intentionally distinguish marked secrets from genuinely uninitialised test data. Tool output requires interpretation; a passing run covers only the paths exercised. [Official Memcheck manual, section 4.2.2](https://valgrind.org/docs/manual/mc-manual.html).

These methods complement the range proofs, byte comparisons and assembly review. Arithmetic correctness answers whether the implementation computes the intended result. Leakage checks ask whether its execution reveals information about secrets. Neither question is answered by reducing the count of modular reductions.

## Threat model and input classification

I assess software-observable timing and secret-dependent branches/addresses in the changed arithmetic paths. An attacker may know public keys, ciphertexts, public matrix seeds, parameter sets and operation selection; these must not be confused with secret noise, secret-key coefficients or secret intermediate values. A variable branch based only on public data is not by itself secret leakage.

The Kyber1024 keygen body includes public-matrix rejection sampling. Marking all keygen coins or every value as secret without following the public/secret split would misclassify that path. The tests cover focused kernels with explicit caller contracts and secret operands, plus an IND-CPA decryption integration check with a written declassification policy. This scope does not cover the full KEM's reencryption and implicit rejection.

| Changed path | Public/fixed controls | Secret classes or flow to exercise | Validity constraint |
|---|---|---|---|
| Fused base multiplication / wide dot | K, coefficient positions, twiddle indices; fixed public matrix or ciphertext-side operand where appropriate | Secret transformed-vector values and relevant secret intermediates | Use the documented operand-specific bounds, including general noncanonical-input envelopes where applicable |
| Staged inverse NTT | Stage schedule, loop bounds and twiddle table | Centred secret-derived transform inputs, fixed versus random and boundary versus interior patterns | Entry coefficients in [-1664,1664]; retained stage bounds apply |
| Raw error NTT and final addition | K, NTT schedule and fixed public operands | Secret error coefficients and resulting additions | Sample noise within [-ETA1,ETA1]; stress patterns separately labelled within proven internal bounds |
| Keygen dot path (EXP-006) | Public matrix, K, indices and scale conversion | Centred secret vector and error-addition values | Matrix [0,3328], secret vector [-1664,1664], EXP-005 addition bounds |

Synthetic stress classes within a proven kernel contract need not all be reachable as whole-KEM inputs. I label them as stress tests and also include valid generated fixtures. I do not interpret an out-of-contract overflow as an attack against the documented implementation, or silently discard a within-contract finding.

## Collection and acceptance procedure

The [dynamic-flow protocol](experiments/EXP-007-secret-flow.md) and [timing-screen protocol](experiments/EXP-008-timing-leakage.md) fix their respective variant matrices, tools, inputs and acceptance rules. Instrumentation and deliberately leaky controls are confined to test harnesses. Production source identities and normal compiled bodies are checked separately.

1. **Identity and environment.** Record source/support hashes, compiler commands, tool versions, executable hashes, affinity and timer. The formal dynamic run uses Valgrind 3.22.0 with recorded client headers, launcher, runtime and preload identities. Default suppressions are disabled. Native execution is rejected so client requests cannot silently become no-ops.
2. **Sensitivity controls.** Use deliberately secret-dependent positive controls and fixed-trace negative controls, with observable outputs and inspected compiled bodies. Quiet positive controls, incomplete diagnostics or a failed setup make the assessment inconclusive.
3. **Dynamic flow.** Mark the documented secret operands, preserve defined twins and inspect branch/address diagnostics. Distinguish deliberate marking from actual uninitialised test data. Declassify outputs only at explicit boundaries and retain all reports without suppressing production findings.
4. **Statistical timing.** Prepare balanced, randomly ordered secret classes outside the measured interval. Use fixed/random and boundary/interior profiles within each kernel contract, observable outputs and explicit reset/copy rules. The frozen protocol specifies 50000 analysis observations per process, two fixed looks, three statistical views and a diagnostic threshold of |t| > 10. It does not claim a calibrated family-wise error probability.
5. **Fixed procedure and retained evidence.** Fix budgets, seeds, repetitions, views and acceptance rules before formal collection. Retain timing/class streams, intermediate statistics and exclusions. A detected difference requires diagnosis and comparison with the original/predecessor; sampling is not extended until a preferred conclusion appears. WSL scheduling and host activity limit sensitivity.

The formal records distinguish development checks from accepted collection. The [initial dynamic pilot](evidence/ACT-0016/secret-flow-support-initial.json) was expanded from six to eight path/operand-role cases because encryption and decryption place the secret operand differently. The [completed development check](evidence/ACT-0016/secret-flow-support-smoke.json) includes the encoded-secret [0,4095] envelope and a defined centred second operand. Its temporary Git-gate substitutes do not count as formal collection. Earlier timing pilots exposed insensitive controls and a stale calibration-only crop cutoff; the final protocol uses a class-blind within-look percentile. The earlier observations and analyses remain retained in [ACT-0017](project_log.md#act-0017--dynamic-secret-flow-result-and-timing-screen-design).

## Reporting and selection rules

For each test/build/parameter I record: input classification and valid bounds; tool/source/binary identity; paths and number of samples exercised; sensitivity-control outcomes; warnings/statistics; observed baseline/candidate difference; reproduction status; explanation and remaining limitations.

I use separate outcomes: detected dependency or timing difference; no evidence detected within the stated tested paths/classes/budget; or inconclusive because the setup lacked sensitivity or failed. A statistical difference requires diagnosis and does not alone demonstrate practical key recovery. A negative result does not establish the absence of leakage. Unexplained new secret-dependent control/address use or reproducible candidate-specific timing dependence blocks an unqualified retention decision; I investigate, revise/reject, or retain it only as an explicitly adverse research finding.

I also retain non-timing findings: code growth, measured local stack changes, protection instructions and the EXP-002 dot-product canary removal. Canary presence is a compiler-hardening observation, not proof of memory safety; endbr64 presence does not prove runtime CET enforcement. Larger representatives change bit patterns, so timing evidence does not answer power/EM/fault questions. These limitations belong in the thesis security results table, including negative and unresolved findings.

## Accepted evidence and source continuity

[EXP-007/RUN-0001](runs/EXP-007-RUN-0001.md) directly tests original/EXP-005/EXP-006. Its 144 marked/defined target processes are quiet, all 18 marked positive controls report the intended dependency, and nine marked negative plus 27 defined controls are quiet. Each target case exercises eight fixtures, with 128 pairs per basemul fixture. The integration cases use generated secret keys and valid/corrupted/all-255/random public ciphertexts. The audit checks 870 raw files and 129 assembly bodies. These are executed-path branch/address observations, not operand-latency or whole-program guarantees.

[EXP-008/RUN-0001](runs/EXP-008-RUN-0001.md) directly tests original/EXP-003/EXP-005. All 288 target processes remain below the frozen threshold; all 18 positive and 18 negative controls meet their criteria. The review recalculates all 1944 statistics and checks 1026 raw files, 105 source identities and 180 assembly bodies. No observations are excluded for invalid intervals/AUX changes. The maximum target absolute t is 2.91016 against threshold 10. Detection of the deliberately large control leaks does not establish sensitivity to tiny leaks.

The distinct variant matrices are retained: EXP-003 was not a direct EXP-007 target, and EXP-006 was not a direct EXP-008 target. Identity-based reuse applies only to matching reviewed bodies within the stated contracts. Other platforms/compilers, whole-KEM implicit rejection, physical/fault channels and exhaustive constant-time properties remain unassessed.

All three [final comparison sessions](final_comparison.md) match the reviewed source and normal-code identities. Their operation timings and successful round trips provide performance/build continuity, not additional leakage evidence. The [final candidate decision](final_candidate.md) retains code/local-stack costs and the inherited general-dot canary change.

The [ACT-0022 source review](evidence/ACT-0022/selected-source-review.json) confirms that all 35 restored EXP-005 files match the selected historical snapshot, both security manifests and all three final comparison manifests. Restoration introduced no new treatment and did not rerun the security tests. The completed [repository record](git_handoff.md) preserves the link from source to the bounded evidence.
