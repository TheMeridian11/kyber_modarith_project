# Implementation-security assessment and remaining practical work

## Purpose and current status

In ACT-0014 I clarified the supervisor's requirements: I need to evaluate how the optimisations affect implementation security and justify the measurement method. VTune was a suggestion, not a mandatory tool. I therefore treat the focused security assessment below as required practical work. I do not treat successful performance measurements, public-looking source or a passing sanitizer as a complete security result.

My scope is the pinned Kyber reference C implementation, the recorded GCC/x86-64 build and the tested execution environment. The changes alter reduction scheduling and intermediate representatives, not parameters or the intended mathematical algorithm. The question is whether they introduce incorrect arithmetic, changed invalid-input behaviour, secret-dependent control/address use, observable timing dependence or compiler-hardening tradeoffs. The project does not establish final FIPS 203 conformance or certification of a production implementation.

| Evidence layer | What I can establish | Current status |
|---|---|---|
| Mathematical contracts | Caller ranges, Montgomery scale, intermediate/narrowing bounds and downstream contracts | Documented for EXP-001/002/003/005; EXP-006 argument proposed |
| Functional and invalid-input checks | Agreement on deterministic outputs and sampled malformed/noncanonical cases | Accepted for retained EXP-001/002/003/005; EXP-006 not-run |
| Exercised undefined behaviour | UBSan observations on selected paths, alongside explicit narrowing arguments | Accepted for existing candidates; not an exhaustive proof |
| Generated code and hardening | Actual branches, addresses, reducers, code size, local stack and protection instructions in scoped functions | Reviewed per run; inherited EXP-002 local-canary tradeoff retained |
| Dynamic secret-flow checking | Executed branches/addresses influenced by marked secrets | Not-run; required |
| Statistical timing-leakage checks | Detectable timing differences between chosen secret classes on this build/target | Not-run; required |
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
| Proposed keygen dot path | Public matrix, K, indices and scale conversion | Centred secret vector and error-addition values | Matrix [0,3328], secret vector [-1664,1664], EXP-005 addition bounds |

Synthetic stress classes within a proven kernel contract need not all be reachable as whole-KEM inputs. I label them as stress tests and also include valid generated fixtures. I do not interpret an out-of-contract overflow as an attack against the documented implementation, or silently discard a within-contract finding.

## Executable protocol to prepare after the last optimisation

I will write and commit a dedicated security harness/protocol before formal collection. I keep all instrumentation and deliberately leaky controls in test files, leaving production arithmetic user-applied and separately identified. At minimum I compare the original reference with the selected final implementation; the preceding variant is added when needed to locate a new finding. I cover all three parameter sets and every retained changed kernel.

1. Pin the tool versions/source revisions and record compiler commands, source/support hashes and executable hashes. Establish which Valgrind and timing facilities actually work in this WSL environment. The ACT-0014 inspection found no valgrind, vtune or perf executable on the WSL PATH, no usual Memcheck header and no /opt/intel/oneapi/vtune directory. This does not inventory Windows installations. No tool has been installed or run by this activity.
2. Validate harness sensitivity using a deliberately secret-dependent positive control and a fixed-trace negative control. Keep their outputs observable so the compiler cannot remove the work. Verify their compiled bodies and investigate diagnostics in the harness itself. If the positive control cannot be detected, the setup is inconclusive; a quiet candidate is not accepted as evidence of no leakage.
3. For dynamic checking, mark only the documented secret operands, execute the targeted paths and inspect every reported conditional/address dependency. Track actual uninitialised-memory errors separately. Outputs are made public/defined only at the explicit test boundary. Preserve reports and explain baseline versus candidate differences. Do not suppress a production-code warning merely to obtain a pass.
4. For timing tests, use balanced, randomly ordered secret classes with preparation and classification outside the measured interval. Use fixed-versus-random classes and complementary boundary/interior patterns under each contract. The measured kernel must have an observable output and the appropriate reset/copy discipline for in-place transforms. Check the compiled measured body against the intended normal code; instrumentation is not used for primary performance claims.
5. In a pilot, select a finite sample budget and sensitivity controls. Then commit the exact budgets, class generators/seeds, batching, repetitions, statistical tests/thresholds and any multiple-test or sequential-stopping policy before formal candidate runs. Use the pinned tool's documented test interpretation. Do not extend sampling until a desired conclusion appears or select only favourable classes after seeing candidate results.
6. Preserve raw timing/class observations or an equivalently auditable retained stream, tool output and intermediate/final statistics. Record affinity, timer, sample count, environment and exclusions. Repeat a detected effect with the same predeclared procedure and compare the original/predecessor to distinguish inherited behaviour, harness defects and candidate changes. WSL scheduling and host activity can reduce sensitivity; a noisy or insensitive setup is reported as inconclusive and investigated.

The numerical budget/thresholds and exact build commands are intentionally not fabricated here: they depend on the pinned tool and sensitivity pilot. They remain a protocol preparation task, not completed measurements. This is a bounded assessment plan, not a claim that all possible secret distributions or microarchitectural effects will be tested.

## Reporting and selection rules

For each test/build/parameter I record: input classification and valid bounds; tool/source/binary identity; paths and number of samples exercised; sensitivity-control outcomes; warnings/statistics; observed baseline/candidate difference; reproduction status; explanation and remaining limitations.

I use separate outcomes: detected dependency or timing difference; no evidence detected within the stated tested paths/classes/budget; or inconclusive because the setup lacked sensitivity or failed. A statistical difference requires diagnosis and does not alone demonstrate practical key recovery. A negative result does not establish the absence of leakage. Unexplained new secret-dependent control/address use or reproducible candidate-specific timing dependence blocks an unqualified retention decision; I investigate, revise/reject, or retain it only as an explicitly adverse research finding.

I also retain non-timing findings: code growth, measured local stack changes, protection instructions and the EXP-002 dot-product canary removal. Canary presence is a compiler-hardening observation, not proof of memory safety; endbr64 presence does not prove runtime CET enforcement. Larger representatives change bit patterns, so timing evidence does not answer power/EM/fault questions. These limitations belong in the thesis security results table, including negative and unresolved findings.

## Optional role of VTune

VTune Hotspots can help identify functions consuming CPU time and relate performance to call stacks. This could explain why a reduction-count saving produces a small or uneven whole-KEM gain. Our preserved CSVs already provide the primary durations; VTune is not required to view those results. [Intel Hotspots documentation](https://www.intel.com/content/www/us/en/docs/vtune-profiler/user-guide/2025-4/basic-hotspots-analysis.html).

I would use a separate profiling run after selecting the final candidate, only if the performance explanation needs it. Intel distinguishes software sampling from hardware event collection; availability, privileges and overhead depend on the collection method. WSL support does not guarantee access to every hardware counter in this configuration. I would check the actual setup before relying on those metrics. [Intel collection documentation](https://www.intel.com/content/www/us/en/docs/vtune-profiler/user-guide/2025-4/collect.html), [Intel system requirements](https://www.intel.com/content/www/us/en/developer/articles/release-notes/vtune-profiler/current.html).

A profile showing fewer hotspots or CPU cycles does not test whether different secrets take different time. Profiling therefore remains optional explanatory evidence; it does not replace the required secret-flow/timing-leakage assessment. I keep profiler-instrumented measurements separate from the normal primary benchmarks.
