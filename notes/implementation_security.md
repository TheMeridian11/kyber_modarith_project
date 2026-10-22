# Implementation-security assessment and remaining practical work

## Purpose and current status

In ACT-0014 I clarified the supervisor's requirements: I need to evaluate how the optimisations affect implementation security and justify the measurement method. VTune was a suggestion, not a mandatory tool; in ACT-0015 I chose to exclude it from the remaining work. I therefore treat the focused security assessment below as required practical work. I do not treat successful performance measurements, public-looking source or a passing sanitizer as a complete security result.

My scope is the pinned Kyber reference C implementation, the recorded GCC/x86-64 build and the tested execution environment. The changes alter reduction scheduling and intermediate representatives, not parameters or the intended mathematical algorithm. The question is whether they introduce incorrect arithmetic, changed invalid-input behaviour, secret-dependent control/address use, observable timing dependence or compiler-hardening tradeoffs. The project does not establish final FIPS 203 conformance or certification of a production implementation.

| Evidence layer | What I can establish | Current status |
|---|---|---|
| Mathematical contracts | Caller ranges, Montgomery scale, intermediate/narrowing bounds and downstream contracts | Documented and reviewed for EXP-001/002/003/005/006 |
| Functional and invalid-input checks | Agreement on deterministic outputs and sampled malformed/noncanonical cases | Accepted for EXP-001/002/003/005/006 within the tested scope |
| Exercised undefined behaviour | UBSan observations on selected paths, alongside explicit narrowing arguments | Accepted for existing candidates including EXP-006; not an exhaustive proof |
| Generated code and hardening | Actual branches, addresses, reducers, code size, local stack and protection instructions in scoped functions | Reviewed per run; inherited EXP-002 local-canary tradeoff retained |
| Dynamic secret-flow checking | Executed branches/addresses influenced by marked secrets | Formal EXP-007/RUN-0001 accepted in ACT-0017: 144 quiet target processes, 18 sensitive positive controls |
| Statistical timing-leakage checks | Detectable timing differences between chosen secret classes on this build/target | EXP-008 support/pilot prepared; formal collection not-run and required |
| Whole-program/formal/physical security | Exhaustive constant time, power/EM, fault resistance, all-target behaviour | Not established; outside this practical claim |

## Why I use complementary methods

The dudect authors describe comparing timing distributions for input classes and warn that failure to detect a difference is not proof of constant time. The result depends on the tested code, compiler and platform. I will use it for empirical timing evidence, separately from throughput benchmarks. [Author repository](https://github.com/oreparaz/dudect).

A ctgrind-style check instead marks secret-derived values and observes whether they reach control flow or memory addressing on executed paths. This provides a useful diagnosis when a timing test finds a difference, and can detect problematic data flow even when that machine's timing measurements are insensitive. The author's discussion contrasts these roles; the historical ctgrind repository demonstrates the marking approach. I will use a supported Valgrind/Memcheck interface after checking the installed headers, rather than assuming the old patch applies. [dudect author discussion](https://www.reparaz.net/oscar/misc/dudect.html), [ctgrind repository](https://github.com/agl/ctgrind).

Memcheck tracks undefined values and reports problematic uses, including conditional decisions. Its diagnostics and origin tracking can help locate a dependency, but the test must intentionally distinguish marked secrets from genuinely uninitialised test data. Tool output requires interpretation; a passing run covers only the paths exercised. [Official Memcheck manual, section 4.2.2](https://valgrind.org/docs/manual/mc-manual.html).

These methods complement the range proofs, byte comparisons and assembly review. Arithmetic correctness answers whether the implementation computes the intended result. Leakage checks ask whether its execution reveals information about secrets. Neither question is answered by reducing the count of modular reductions.

## Threat model and input classification

I assess software-observable timing and secret-dependent branches/addresses in the changed arithmetic paths. An attacker may know public keys, ciphertexts, public matrix seeds, parameter sets and operation selection; these must not be confused with secret noise, secret-key coefficients or secret intermediate values. A variable branch based only on public data is not by itself secret leakage.

The Kyber1024 keygen body includes public-matrix rejection sampling. Marking all keygen coins or every value as secret without following the public/secret split would misclassify that path. I start with focused kernels whose caller contracts and secret operands are explicit, then add a representative integration check with a written declassification policy. I document any integration coverage I cannot achieve; kernel results are not renamed whole-KEM proof.

| Changed path | Public/fixed controls | Secret classes or flow to exercise | Validity constraint |
|---|---|---|---|
| Fused base multiplication / wide dot | K, coefficient positions, twiddle indices; fixed public matrix or ciphertext-side operand where appropriate | Secret transformed-vector values and relevant secret intermediates | Use the documented operand-specific bounds, including general noncanonical-input envelopes where applicable |
| Staged inverse NTT | Stage schedule, loop bounds and twiddle table | Centred secret-derived transform inputs, fixed versus random and boundary versus interior patterns | Entry coefficients in [-1664,1664]; retained stage bounds apply |
| Raw error NTT and final addition | K, NTT schedule and fixed public operands | Secret error coefficients and resulting additions | Sample noise within [-ETA1,ETA1]; stress patterns separately labelled within proven internal bounds |
| Keygen dot path (EXP-006) | Public matrix, K, indices and scale conversion | Centred secret vector and error-addition values | Matrix [0,3328], secret vector [-1664,1664], EXP-005 addition bounds |

Synthetic stress classes within a proven kernel contract need not all be reachable as whole-KEM inputs. I label them as stress tests and also include valid generated fixtures. I do not interpret an out-of-contract overflow as an attack against the documented implementation, or silently discard a within-contract finding.

## Executable assessment after the last optimisation

I prepared EXP-007 in ACT-0016 and accepted its formal RUN-0001 in ACT-0017. The [EXP-008 statistical protocol](experiments/EXP-008-timing-leakage.md) now fixes the custom dudect-style harness, finite budget and interpretation before formal collection. I keep all instrumentation and deliberately leaky controls in test files, leaving production arithmetic user-applied and separately identified. At minimum I compare the original reference with the selected final implementation; the preceding variant is added when needed to locate a new finding. I cover all three parameter sets and every retained changed kernel.

1. Pin the tool versions/source revisions and record compiler commands, source/support hashes and executable hashes. Establish which Valgrind and timing facilities actually work in this WSL environment. The ACT-0014 inspection found no valgrind, vtune or perf executable on the WSL PATH, no usual Memcheck header and no /opt/intel/oneapi/vtune directory. This does not inventory Windows installations. That ACT-0014 inspection did not install or run those tools. ACT-0016 subsequently downloaded/extracted Ubuntu Valgrind 3.22.0 in a temporary directory and executed development checks; it did not install a system package.
2. Validate harness sensitivity using a deliberately secret-dependent positive control and a fixed-trace negative control. Keep their outputs observable so the compiler cannot remove the work. Verify their compiled bodies and investigate diagnostics in the harness itself. If the positive control cannot be detected, the setup is inconclusive; a quiet candidate is not accepted as evidence of no leakage.
3. For dynamic checking, mark only the documented secret operands, execute the targeted paths and inspect every reported conditional/address dependency. Track actual uninitialised-memory errors separately. Outputs are made public/defined only at the explicit test boundary. Preserve reports and explain baseline versus candidate differences. Do not suppress a production-code warning merely to obtain a pass.
4. For timing tests, use balanced, randomly ordered secret classes with preparation and classification outside the measured interval. Use fixed-versus-random classes and complementary boundary/interior patterns under each contract. The measured kernel must have an observable output and the appropriate reset/copy discipline for in-place transforms. Check the compiled measured body against the intended normal code; instrumentation is not used for primary performance claims.
5. In a pilot, select a finite sample budget and sensitivity controls. Then commit the exact budgets, class generators/seeds, batching, repetitions, statistical tests/thresholds and any multiple-test or sequential-stopping policy before formal candidate runs. Use the pinned tool's documented test interpretation. Do not extend sampling until a desired conclusion appears or select only favourable classes after seeing candidate results.
6. Preserve raw timing/class observations or an equivalently auditable retained stream, tool output and intermediate/final statistics. Record affinity, timer, sample count, environment and exclusions. Repeat a detected effect with the same predeclared procedure and compare the original/predecessor to distinguish inherited behaviour, harness defects and candidate changes. WSL scheduling and host activity can reduce sensitivity; a noisy or insensitive setup is reported as inconclusive and investigated.

ACT-0017 completes the pinned-reference review and development sensitivity pilot. EXP-008 specifies 50000 analysis observations per process, two fixed looks, three statistical views and a threshold of |t| > 10; it records multiple-test and dependence limitations without claiming a calibrated family-wise probability. Formal collection remains pending. This is a bounded assessment plan, not a claim that all possible secret distributions or microarchitectural effects will be tested.

## Reporting and selection rules

For each test/build/parameter I record: input classification and valid bounds; tool/source/binary identity; paths and number of samples exercised; sensitivity-control outcomes; warnings/statistics; observed baseline/candidate difference; reproduction status; explanation and remaining limitations.

I use separate outcomes: detected dependency or timing difference; no evidence detected within the stated tested paths/classes/budget; or inconclusive because the setup lacked sensitivity or failed. A statistical difference requires diagnosis and does not alone demonstrate practical key recovery. A negative result does not establish the absence of leakage. Unexplained new secret-dependent control/address use or reproducible candidate-specific timing dependence blocks an unqualified retention decision; I investigate, revise/reject, or retain it only as an explicitly adverse research finding.

I also retain non-timing findings: code growth, measured local stack changes, protection instructions and the EXP-002 dot-product canary removal. Canary presence is a compiler-hardening observation, not proof of memory safety; endbr64 presence does not prove runtime CET enforcement. Larger representatives change bit patterns, so timing evidence does not answer power/EM/fault questions. These limitations belong in the thesis security results table, including negative and unresolved findings.

## Scope decision: no VTune work

In ACT-0015 I chose to exclude VTune installation, profiling and analysis from the remaining practical plan. The ACT-0014 literature review remains recorded as historical provenance, but no profiling task is pending. Primary performance evidence comes from the retained normal-build paired timing data, reduction counts and generated-code review. Required secret-flow and statistical timing-leakage checks remain in scope; removing an optional profiler does not remove the supervisor's security-assessment requirement.

## ACT-0016 executed support checks and remaining claims

This section records the earlier handoff; ACT-0017 below updates completion status.

I selected EXP-005 as the primary closing candidate after EXP-006's mixed timing result; EXP-006 remains a secondary comparison. The new tests leave arithmetic untouched and restore all 35 EXP-005 files from their committed source. I pinned Valgrind 3.22.0, used actual installed client-request headers and recorded the launcher, valgrind.bin, Memcheck runtime/preloads, headers, compiler and disassembler hashes. I disable default suppressions and preserve XML/error counts and process outputs.

[Development evidence](evidence/ACT-0016/secret-flow-support-smoke.json) records all nine builds and 198 processes. All eighteen marked positive controls report their intended branch/address dependency. Twenty-seven defined controls and nine marked negative controls are quiet. All 72 defined and 72 marked target processes are quiet. Eight target path/operand-role cases each exercise eight fixtures per parameter/variant; basemul expands each fixture into 128 pairs. The integration path covers IND-CPA decryption with generated secret keys and valid/corrupted/all-255/random public ciphertexts. Output declassification happens only at explicit test boundaries. Kernel stress fixtures are not all claimed to be reachable whole-KEM states.

I checked 102 production function bodies against accepted normal binaries: all match after relocation normalisation, despite the diagnostic -g build flag. All 27 control bodies are retained; positive branches/indexed addresses remain present, and the negative control contains no branch/call. Native execution is rejected, so client requests cannot silently become a passing no-op test. Parser/classifier checks reject incomplete XML, suppressions, wrong completion markers, quiet positive controls and diagnostics outside the named control. Git commit/clean-tree gates were replaced only for this uncommitted temporary development check; formal collection must still exercise them after committing support.

This result establishes that the prepared dynamic setup detects the selected controls and found no dependency on the exercised marked paths. It is not a formal EXP-007 result, timing-leakage measurement or whole-KEM proof. It cannot detect every operand-latency channel or unexecuted path. The same production compiler/body identities support relevance to the existing experiments but do not establish all-target behaviour. I still need formal dynamic collection/review, a pinned statistical leakage pilot with finite committed budgets and the final security matrix. The throughput figures provide no substitute for these checks. VTune remains excluded.

I expanded the initial six-path development matrix after checking the actual operand roles: encryption places the secret vector second, while decryption places decoded skpv first. The final eight-case matrix adds basemul-first and dot-first with a [0,4095] encoded-secret stress envelope and a defined centred second operand. The [initial development snapshot](evidence/ACT-0016/secret-flow-support-initial.json) remains preserved; the final support evidence supersedes it for the formal protocol.

## ACT-0017 accepted dynamic evidence and statistical handoff

[EXP-007/RUN-0001](runs/EXP-007-RUN-0001.md) now supplies formal executed-path evidence. I checked all defined twins, marked operands, control diagnostics and 870 raw-file hashes; all 129 assembly bodies match the reviewed support. No new branch/address dependency was observed. This leaves the existing canary tradeoff and unassessed attack classes visible.

I prepared a native [EXP-008 fixed-budget screen](experiments/EXP-008-timing-leakage.md) for original/EXP-003/EXP-005. Development control measurements at 50000 observations detect all 18 deliberately leaky controls, with all 18 negatives quiet under the final analysis. Smaller development matrices remain labelled support tests and retain their insensitive controls. The final protocol uses a class-blind within-look percentile after a calibration-only cutoff proved stale in one development control. I retain both analyses and raw observations. The Welch calculation agrees with the pinned upstream implementation on independent numerical fixtures. Formal candidate security conclusions await committed collection and review.

I distinguish a large deliberate leak detected by the controls from a sensitivity bound on small real effects, which is not established. No signal within the finite budget is not proof of constant time. No implementation-security numeric score is inferred from the coverage figure.
