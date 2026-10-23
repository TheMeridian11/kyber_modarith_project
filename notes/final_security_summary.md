# Consolidated implementation-security conclusion

I select EXP-005 for the reference-C thesis with a bounded implementation-security assessment. I separate security mechanisms and evidence rather than turn a passing benchmark or an absence of diagnostics into a blanket security rating. The [candidate decision](final_candidate.md) identifies exact source files, code/local-frame costs and the inherited canary tradeoff. The [machine-readable matrix](../analysis/final-security-evidence.csv) retains the following distinctions.

| Evidence layer | EXP-003 | EXP-005 | Practical limit |
|---|---|---|---|
| Range, scale and narrowing | Reviewed conditional contracts | Inherited contracts plus raw-error/addition bounds | Caller/parameter/compiler assumptions; no arbitrary-input guarantee |
| Compatibility and invalid inputs | Accepted sampled equality to original | Accepted sampled equality to original | Deterministic transcript and sampled malformed/noncanonical cases; not exhaustive conformance |
| Undefined behaviour checks | No UBSan report on exercised paths | No UBSan report on exercised paths | Not proof of all memory/arithmetic safety; narrowing also needs explicit bounds |
| Normal generated-code identity | All closing-session reviewed bodies match | All closing-session reviewed bodies match | Scoped functions, compiler/flags/platform; not every callee or whole-binary semantics |
| Marked-secret branch/address flow | Not directly in EXP-007; identity-based reuse only | Direct EXP-007 tested paths quiet; controls sensitive | Executed paths and secret marking; no instruction-latency or full-KEM proof |
| Secret-class timing screen | Direct EXP-008 screen: no detected difference within budget | Direct EXP-008 screen: no detected difference within budget | Finite classes/paths/budget and target; no tiny-leak sensitivity or whole-program proof |
| Keygen hardening | Canary, endbr64 and probes present | Canary, endbr64 and probes retained | Instruction presence does not establish runtime CET or memory safety |
| General-dot local canary | Absent after inherited EXP-002 local-array removal | Same inherited absence | Changed local stack-corruption detection coverage; no exploitability claim |
| Physical/fault/formal/security certification | Not established | Not established | No power/EM/fault campaign, whole-program proof, other-target guarantee or final ML-KEM certification |

## Evidence chain and what changed

I retain the original source at 3edd5af5991927164edd4aacebfcbee00b8064e7 as the compatibility/performance comparator. Accepted validation for [EXP-001](runs/EXP-001-RUN-0001.md), [EXP-002](runs/EXP-002-RUN-0001.md), [EXP-003](runs/EXP-003-RUN-0001.md) and [EXP-005](runs/EXP-005-RUN-0001.md) links the successive bounds, Montgomery scale, narrowing, outputs, invalid-input cases and exercised sanitizer evidence. Exact restoration and all 324 matching final-comparison body extractions preserve the relevant source/build connection across the three sessions; they do not create a new proof of correctness.

The optimisations preserve the intended mathematical algorithm and parameters under the reviewed contracts, but change intermediate representatives, reduction scheduling, code layout and local memory use. EXP-002 reduces the local dot-product frame while losing that function's compiler-generated canary; EXP-003 reduces the inverse function's local frame while growing its body; EXP-005 grows the keygen body and slightly grows two local frames. These are concrete implementation tradeoffs. I do not infer total-memory savings or physical leakage equivalence from them.

EXP-005's caller-specific raw-error bound is 23299/23298/23298 and the addition bound is 26627/26626/26626 for Kyber512/768/1024. Secret-vector centring, inverse-input contracts, Montgomery scale conversion and final public-key reduction remain. These arguments explain why deferral is justified at this call site, rather than claiming any reduction can be removed. The detailed accepted validation retains the premises and test coverage.

## Dynamic and statistical findings

[EXP-007](runs/EXP-007-RUN-0001.md) directly includes original/EXP-005/EXP-006. All 144 target processes are quiet across marked and defined modes; all 18 deliberately marked branch/address controls are detected. I interpret this as no marked-secret dependency observed in the exercised branches/addresses. The tested decryption integration is IND-CPA, not a claim covering the whole KEM's reencryption and implicit rejection. EXP-003 was not a separate EXP-007 target; reuse rests on reviewed body identity where applicable.

[EXP-008](runs/EXP-008-RUN-0001.md) directly includes original/EXP-003/EXP-005. All 288 target processes stay below the fixed diagnostic threshold in every planned view/look; all 18 positive controls meet their detection criterion and all 18 negatives are quiet. I independently reproduced all 1944 statistics. The maximum target absolute Welch t is 2.91016 against threshold 10. The finding is **no timing difference detected within the selected paths, synthetic classes, platform and finite budget**. It is not a whole-program constant-time proof, calibrated family-wise significance claim or sensitivity bound for tiny leaks. Maximum t values are not a ranking of implementations' security.

The methods address different failure mechanisms: range/scale reasoning supports arithmetic validity; deterministic/invalid-input tests support sampled compatibility; UBSan checks exercised operations; assembly and marked-secret flow inspect control/address behavior; the statistical screen looks for timing differences under chosen classes. These complementary methods and their limits answer the supervisor's request to explain how security impact is evaluated. VTune is not part of this assessment.

## Closing claim

I observed no correctness failure or new secret-dependent timing/control/address finding within the accepted candidate tests and reviewed contracts. I explicitly observed and retained the inherited local-canary change and the scoped code/stack costs. The final performance results neither strengthen nor weaken the leakage finding by themselves. Further deployment, different compilers/targets, new caller ranges, physical/fault attacks or formal certification would require evidence beyond this honours study. No additional security collection is required by the completed predeclared project protocol; final source/reproduction handover remains a separate task.
