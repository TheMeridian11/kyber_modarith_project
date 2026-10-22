# EXP-005 — Defer reduction of the key-generation error NTT

## Identity and scope

- Originating activity: ACT-0012.
- Lifecycle: running; manual edit committed and RUN-0001 correctness/counts/scoped assembly accepted in ACT-0013. Performance and retention decision pending.
- Variant: raw-error-ntt, cumulative on retained EXP-003.
- Predecessor: EXP-003 staged-invntt, validated at 9ec22141e6acc98812438544be0bec5b35d00b5c and timed at cf8ae0dd700bb41628c158016a7c15926a0b790f; timing results 23b4736206a8f79d13fb4898d474eb327e1dab3c.
- Original reference: pinned upstream 3edd5af5991927164edd4aacebfcbee00b8064e7.
- Accepted record: [EXP-005/RUN-0001](../runs/EXP-005-RUN-0001.md), correctness/counts/assembly only.
- Source commit: 5a499bd1940ce0ff8fd5d973f6f46b62b50c0648; results commit: af3408156a334c52676b51a5348540c17234390c.
- Next record: EXP-005/RUN-0002, [fresh timing comparison against EXP-003](../error_ntt_timing.md).
- Idea origin: the previously noted optional error-vector pilot, developed through local inspection of LIT-003: indcpa_keypair_derand, polyvec_ntt, poly_ntt, ntt, poly_tomont, poly_add, poly_reduce, params.h and cbd.c. No novelty claim or attribution of this exact edit to an unreviewed paper is made.

I allocate EXP-005 because EXP-004 is already reserved for a distinct optional interaction/combination question. EXP-004 remains deferred; I do not silently repurpose that record or add a redundant combination run. EXP-005 estimates an incremental treatment conditional on the retained preceding variants.

## Hypothesis and isolated change

In EXP-003 key generation, both skpv and the error vector e pass through polyvec_ntt. That wrapper calls poly_ntt for each polynomial, which performs the forward NTT and then 256 Barrett reductions. The transformed error e is subsequently added once to pkpv, immediately before the existing final polyvec_reduce. It is not a multiplication input, a serialized secret-key vector, or an inverse-transform input.

I proposed, and have now manually applied, calling ntt directly only for each polynomial of e. This leaves its transformed coefficients unreduced until the existing public-key reduction. The forward transform and its Montgomery calls are unchanged; the intervening addition preserves residues as long as its signed representation does not overflow. The skpv reduction, all encryption/decryption forward reductions, the vector-dot-product exit reduction and the inverse-transform schedule remain unchanged.

The hypothesis is a key-generation duration reduction from removing K*256 Barrett calls. Encap and decap have no predicted arithmetic benefit and remain comparison controls. Compiler/layout effects or noise can still change any measured duration. No runtime percentage is inferred from call counts.

| Parameter | Error coefficient bound ETA1 | Keygen Barrett EXP-003 -> EXP-005 | Calls removed | Encap / decap Barrett, unchanged | Montgomery keygen / encap / decap, unchanged |
|---|---:|---:|---:|---:|---:|
| Kyber512 | 3 | 2048 -> 1536 | 512 | 2432 / 3584 | 4864 / 6400 / 9728 |
| Kyber768 | 2 | 3072 -> 2304 | 768 | 3328 / 4736 | 7296 / 8832 / 13056 |
| Kyber1024 | 2 | 4096 -> 3072 | 1024 | 4224 / 5888 | 9728 / 11264 / 16384 |

I specified these source-derived predictions before execution. RUN-0001 now confirms all ninety instrumented observations against them. They remove one quarter of EXP-003 keygen Barrett calls, not one quarter of keygen time.

## Caller contract, scale and conservative bounds

poly_getnoise_eta1 samples each e coefficient within [-ETA1,ETA1] for every possible seed; ETA1 is 3 for Kyber512 and 2 for the other parameters. This bound follows the CBD sum-of-bits difference, not an assumed typical random distribution. Secret-key coefficients skpv are sampled separately and keep their existing post-NTT reduction.

The unchanged forward NTT has seven stages at lengths 128,64,32,16,8,4,2. Let B be the incoming absolute coefficient bound. With |zeta| <= 1664, the product magnitude is at most 1664B. When this lies within the Montgomery input contract [-109084672,109084671], its result is at most 3328 in magnitude. Both butterfly outputs are therefore bounded by B+3328. The following induction uses the larger ETA1=3 envelope; ETA1=2 gives one less at each output.

| Stage length | Input bound B | Maximum product 1664B | Output bound B+3328 |
|---|---:|---:|---:|
| 128 | 3 | 4992 | 3331 |
| 64 | 3331 | 5542784 | 6659 |
| 32 | 6659 | 11080576 | 9987 |
| 16 | 9987 | 16618368 | 13315 |
| 8 | 13315 | 22156160 | 16643 |
| 4 | 16643 | 27693952 | 19971 |
| 2 | 19971 | 33231744 | 23299 |

All products fit int32_t and the documented Montgomery interval. All additions/subtractions stored in int16_t fit its range. The final raw error transform is bounded by 23299 for Kyber512 or 23298 for Kyber768/1024. These are conservative envelopes, not measured maxima or optimal bounds. The internal forward NTT already executes with these unreduced intermediates in EXP-003; the proposed change removes only the reduction after that transform.

The other operand pkpv has just passed through poly_tomont, whose Montgomery outputs are bounded by 3328. Adding the raw error therefore yields at most 26627 or 26626, below 32767. The existing final polyvec_reduce is retained, so Barrett receives representable int16_t values and returns centred coefficients. Serialization receives the same canonical residues as before. Error e has no other consumer in this function and the input/output objects remain distinct.

I do not remove or move any Montgomery multiplication or poly_tomont. The error NTT's scale is unchanged because Barrett changes only the representative, not the residue or Montgomery factor. The public-key product is converted by the same poly_tomont before addition. The two paths give the same sum modulo 3329 and the final centred representative is unique. Thus the mathematical argument supports identical public-key bytes; secret-key bytes stay unchanged because skpv and its reduction are preserved. Whole-KEM validation must still check that the actual edit implements this argument.

The final dot-product reductions that establish EXP-003's inverse-input bound of 1664 remain intact. EXP-003's inverse bound of 26624 is therefore unaffected. This proposal does not justify removing poly_ntt's reduction globally, omitting the secret-vector reduction, or passing unreduced error coefficients into the wide dot product. Changed consumers, parameter sets, noise distributions or reduction contracts require a new assessment.

## Applied manual edit

I applied the following replacement in implementation/kyber-optimised-ref/indcpa.c, inside indcpa_keypair_derand. This is the preserved edit record, not another edit to perform. I replaced only:

~~~c
  polyvec_ntt(&skpv);
  polyvec_ntt(&e);
~~~

with exactly:

~~~c
  polyvec_ntt(&skpv);
  /* e is only added to pkpv before the existing final reduction. */
  for(i=0;i<KYBER_K;i++)
    ntt(e.vec[i].coeffs);
~~~

ntt.h is already included, and the existing unsigned loop variable i is reused. The following matrix-vector loop resets i to zero as before. Preserve every other byte of the source, including polyvec_reduce(&pkpv), all other calls and the complete ntt.c/polyvec.c changes from earlier experiments. Do not keep the replaced block in a comment.

The preflight requires the exact reviewed indcpa.c hash 900541c7291e25feb86e0d42fc2e8daa3fc606d99130e496edddd1955ec479c2 and unchanged hashes for the other source files. RUN-0001 and the ACT-0013 review now verify this exact applied source hash and all unchanged predecessor files. An unapplied or different edit is rejected before run allocation.

## Correctness and implementation-security gates

| Concern | Required argument and evidence |
|---|---|
| Overflow and narrowing | Preserve sampled error bounds, the unchanged forward transform and the final public-key reduction. Review the 23299/26627 envelopes and verify raw/residue/addition bounds with targeted tests and UBSan. Passing sanitizer alone does not prove narrowing safety. |
| External compatibility | Compare deterministic KEM bytes across original reference/candidate and normal/UBSan modes, including corrupted/random ciphertexts, malformed secret keys and noncanonical public keys. |
| Input contract interactions | Keep skpv and all other forward reductions plus the wide-dot exit reduction. EXP-003 still requires centred inverse inputs. Any change to these consumers invalidates this scoped argument. |
| Timing/indexing | The new loop count is compile-time public K; there is no coefficient-dependent choice to reduce. Existing NTT/table indices are public. Inspect actual normal-build keygen/NTT/reducer assembly before accepting for timing. |
| Memory and hardening | No new allocation or array is introduced and the existing e/pkpv arrays remain distinct. Register use, local stack, code size and canary/CET instructions may change under optimisation and require actual assembly review. No protection flag is disabled. |
| Inherited assumptions | Signed narrowing/right-shift behaviour in existing reducers remains tied to the recorded GCC/x86-64 target. Preserve earlier EXP-001/002/003 bounds and the EXP-002 dot-product canary tradeoff. |
| Wider security | Larger internal representatives change stored values; public control flow alone does not assess power/EM or fault behaviour. No whole-program constant-time proof, statistical leakage result, portability, memory-safety certification, final ML-KEM conformance or production approval is established. |

I reject or revise a candidate that fails the arithmetic/compatibility/security gate before timing. This experiment optimises implementation scheduling; it changes no cryptographic parameter, noise distribution or algorithmic security level. I do not infer implementation security from speed.

## Validation support and execution

I added tests/test_error_ntt.c and scripts/run_error_ntt_validation.py. The test checks 47 full error-polynomial patterns: zero, dense extremes, both signs for eight index-bit patterns, both signs at ten boundary positions and eight deterministic interiors. The input range is the applicable ETA1. An ordinary modular forward-transform oracle calls neither reducer; it shares the twiddle table/transform layout, so it checks arithmetic equivalence rather than independently certifying the full specification.

For each vector, I compare raw ntt and centred poly_ntt residues and bounds, then add four offset patterns covering the conservative post-poly_tomont range [-3328,3328]. After the retained poly_reduce, both paths must give identical centred coefficients and serialized polynomial bytes. Per build this gives 12032 forward coefficient checks, 48128 addition/final-reduction coefficient checks and 188 serialization comparisons. The test explicitly checks representability before calling the addition. These targeted cases supplement the range proof; they are not exhaustive input coverage.

The formal run uses the original reference and actual candidate, all three parameters, normal and UBSan modes, and 100 established deterministic KEM fixtures per build. It also runs the existing candidate upstream suites and ten count fixtures per parameter. It extracts indcpa_keypair_derand, ntt, Montgomery and Barrett bodies from all six normal binaries. The expected total is 60 steps, including 24 assembly extractions. Unchanged standalone basemul/dot/inverse oracle suites are not repeated; their source identities and accepted evidence are preserved. No timings are collected.

After manual application, review and commit of source/support/notes, I executed the following command. RUN-0001 exists and must not be reused:

~~~bash
python3 -B scripts/run_error_ntt_validation.py --experiment EXP-005 --run RUN-0001
echo $?
~~~

The runner invokes the metadata collector itself. It requires committed source/support and a clean Git-visible tree outside results/. I preserve a failed/interrupted attempt and use a fresh ID for a retry. After exit code zero and completed status, I preserve the entire run directory for review:

~~~bash
git add -- results/EXP-005/RUN-0001/
git diff --cached --check
git diff --cached --stat
git commit -m "Record EXP-005 error-vector reduction validation"
~~~

The execution manifest retains assembly review pending as originally written. [ACT-0013](../runs/EXP-005-RUN-0001.md) now records acceptance separately without editing archived evidence. I prepared the fresh EXP-003/EXP-005 comparison after that acceptance.

## Historical development support status (ACT-0012)

[ACT-0012 support evidence](../evidence/ACT-0012/error-ntt-validation-support-smoke.json) records twelve actual builds of only the existing original reference and accepted EXP-003, each with two KEM fixtures. The new oracle, addition/serialization checks and four-way transcripts pass for every parameter, with no compiler or exercised UBSan diagnostics. It verifies the test design through existing functions; it does not execute an edited EXP-005 key-generation call path.

Before manual application, the unapplied-change guard rejected the then-current EXP-003 source before metadata collection/run allocation, a changed preserved arithmetic hash was rejected, and old EXP-003 counts failed the new predicted keygen counts. The interval induction and count formulas were checked independently. No arithmetic implementation was edited, including in temporary copies; no Git commands, metadata collector or formal EXP-005 run were executed. At that earlier activity, proposed candidate correctness, counts, assembly and performance were not-run. Subsequent manual application and RUN-0001 are reviewed below.

## Accepted validation and security findings (ACT-0013)

I verified all sixty steps, 120 raw streams, eighteen binaries, seven support files and exact committed source identities. All twelve normal/UBSan builds pass the targeted error-NTT/addition/serialization checks and 100 KEM fixtures; the four-way transcripts match for every parameter, including tested malformed/noncanonical cases. Three upstream suites and all ninety instrumented observations pass. No sanitizer diagnostics were emitted on the exercised paths. The [run review](../runs/EXP-005-RUN-0001.md) retains scope, hashes and limitations.

The range/scale argument remains valid for the exact applied call site: raw e is bounded by 23299/23298, the post-addition bound is 26627/26626, and the existing final reduction restores identical centred residues. skpv and all wide-dot/inverse input contracts remain unchanged. These claims depend on current noise bounds and consumers; sampled tests and UBSan do not establish arbitrary-input narrowing safety.

The compiler unrolls the new loop into K fixed direct ntt calls while retaining the skpv polyvec_ntt call. Forward NTT and both reducers match prior normalised assembly. Keygen code sizes change 425->442, 479->512 and 948->988 bytes. Local stack including saved registers changes 5256->5272, 9368->9384 and 15032->15032 bytes, excluding entry return address/callees. Canary checks, endbr64 and page probes remain in all compared keygen bodies. The earlier EXP-002 dot-product canary tradeoff remains inherited.

No new secret-error-dependent branch/index appears in the changed call path. The larger Kyber1024 keygen body includes existing public-matrix rejection sampling, so I do not claim all keygen branches are fixed loop counters or the whole program is constant-time. I preserve limits for statistical leakage, power/EM and faults, signed portability, exhaustive memory safety and final ML-KEM conformance. Larger representatives and code/register/layout changes require their own interpretation; speed cannot establish security or isolate Barrett-call cost.

I accept the validation gate and proceed to [RUN-0002](../error_ntt_timing.md). Six real development builds match all 24 reviewed functions and twelve short processes pass the comparison pipeline. These support checks are not thesis performance results. Keygen benefit, encap/decap tradeoffs and the final performance-retention decision remain pending the formal paired run.
