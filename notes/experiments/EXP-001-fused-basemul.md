# EXP-001 — Fused base multiplication

## Identity and status

- Originating activity: ACT-0006.
- Lifecycle: planned; the arithmetic change is supplied for manual application and is not yet implemented.
- Candidate variant: fused-basemul.
- Candidate source commit: pending.
- Baseline: pinned reference at upstream 3edd5af5991927164edd4aacebfcbee00b8064e7.
- Baseline evidence: EXP-000/RUN-0002 functional checks, RUN-0003 timing pilot and [RUN-0004 counts](../runs/EXP-000-RUN-0004.md).
- Baseline count source/results commits: 3757df58a02408fb9a701869cc1f3ac6f6159a8d / 2a8388c1701dcf66cb5dfa6906921f63bc574c55.
- Next record: EXP-001/RUN-0001, candidate validation.
- Origin: local analysis of the pinned source, LIT-003. I do not claim that this rearrangement is novel or attribute it to an unreviewed paper.

I test whether combining products before Montgomery reduction improves key generation, encapsulation and decapsulation while preserving externally visible behaviour and the reviewed implementation assumptions.

## Isolated change and hypothesis

I will replace only the body of basemul in implementation/kyber-optimised-ref/ntt.c. I retain the initial reduction of a[1]*b[1], accumulate each output's remaining products in int32_t, then apply one Montgomery reduction to each accumulator. This changes five reducer invocations to three per coefficient pair. The NTT, inverse NTT, Barrett reducer, vector accumulation and final vector reduction remain unchanged.

A polynomial contains 128 such pairs, so its base multiplication changes from 640 to 384 Montgomery calls. A K-element dot product changes from 640K to 384K calls. For keygen, encapsulation and decapsulation, predicted savings are respectively 256K^2, 256K(K+1) and 256K(K+2). Decapsulation includes re-encryption.

| Parameter set | Keygen baseline -> candidate | Encap baseline -> candidate | Decap baseline -> candidate |
|---|---:|---:|---:|
| Kyber512 | 6656 -> 5632 | 9088 -> 7552 | 13312 -> 11264 |
| Kyber768 | 11904 -> 9600 | 14976 -> 11904 | 20736 -> 16896 |
| Kyber1024 | 18432 -> 14336 | 22144 -> 17024 | 29440 -> 23296 |

These are predicted Montgomery calls per operation. Barrett counts should remain exactly as recorded in RUN-0004. The C counter supplies observations independently of these predictions.

The local kernel uses 40% fewer reductions. The complete KEM still performs hashing, sampling, transforms and other work, so this is not a 40% runtime forecast. Register use, instruction scheduling, compiler optimisation and measurement variation may yield a smaller benefit, no benefit or a regression.

## Algebra and Montgomery representation

Let q = 3329, R = 65536 and M(x) denote the existing Montgomery reducer, with M(x) congruent to x*R^-1 modulo q. The zeta table stores twiddle factors in Montgomery representation.

Write t = M(a1*b1). The original outputs are congruent to:

- r0 = M(t*zeta) + M(a0*b0).
- r1 = M(a0*b1) + M(a1*b0).

Within the reducer's input contract, modular linearity permits:

- r0 = M(t*zeta + a0*b0).
- r1 = M(a0*b1 + a1*b0).

The initial computation of t is retained. Removing it would introduce the wrong power of R. The candidate must not simply reduce the ordinary three-factor product.

The original and candidate raw basemul outputs can differ by a multiple of q. I require equal residues at this internal boundary, then byte-identical public keys, secret keys, ciphertexts and shared secrets at the API boundary. The existing final poly_reduce in polyvec_basemul_acc_montgomery maps both sums to the same centred representatives.

## Caller ranges and intermediate bounds

I reviewed all KEM callers in indcpa.c:

- Key generation passes matrix coefficients from rejection sampling in 0..3328 as a, and a transformed/reduced secret vector as b.
- Encryption passes either matrix coefficients or deserialised public-key coefficients as a, and a transformed/reduced ephemeral vector as b.
- Decryption passes deserialised secret-key coefficients as a, and the transformed/reduced ciphertext vector as b.
- poly_frombytes masks each encoded coefficient to 12 bits. Arbitrary encoded key bytes therefore permit 0..4095, not merely 0..3328.
- poly_ntt calls poly_reduce, giving b in -1664..1664. This remains the boundary after transforming arbitrary ciphertext bytes.
- The actual twiddles and their negations lie within -1664..1664.

I use the conservative envelope |a_i| <= 4095, |b_i| <= 1664 and |zeta| <= 1664. The negative part of the a envelope is additional coverage beyond the current nonnegative KEM callers.

| Quantity | Conservative absolute bound |
|---|---:|
| a1*b1, a0*b0, a0*b1 or a1*b0 | 6814080 |
| t = M(a1*b1) | 3328 |
| t*zeta + a0*b0 | 12351872 |
| a0*b1 + a1*b0 | 13628160 |
| Each candidate output after reduction | 3328 |
| Sum of up to four candidate products before poly_reduce | 13312 |

Every new product is explicitly evaluated in int32_t, and each fused sum remains int32_t until reduction. These bounds are below INT32_MAX and within the existing Montgomery input contract [-109084672, 109084671]. The output sums fit int16_t before the unchanged Barrett reduction.

This establishes a caller-specific argument for the proposed change. It is not a general contract for arbitrary int16_t pairs. A later optimisation that widens the inputs or removes an upstream reduction must redo the argument. I do not pass a wide accumulator to barrett_reduce, whose input type is int16_t.

The unchanged reducer depends on GCC's documented signed narrowing and arithmetic right-shift behaviour. Those implementation-defined assumptions are retained, not newly removed or made portable. See [GCC integer semantics](https://gcc.gnu.org/onlinedocs/gcc/Integers-implementation.html). Compiler/target changes require review.

## Implementation-security assessment

| Concern | Mechanism or risk | Current evidence and gate |
|---|---|---|
| Modular correctness | Incorrect grouping can change the Montgomery scale or output residue | Algebra recorded above; candidate kernel and API checks pending |
| Overflow and narrowing | A wide sum narrowed too early can corrupt arithmetic; signed overflow can invalidate compiler assumptions | Explicit int32_t arithmetic and bounded inputs proposed; UBSan and output-bound checks pending |
| Downstream assumptions | Equivalent residues can have different integer representatives | Candidate outputs have a smaller bound; unchanged final poly_reduce restores identical centred values |
| Invalid inputs and rejection | Arithmetic disagreement can change decryption, re-encryption or the selected rejection secret | Compare baseline/candidate responses to corrupted/random ciphertexts and malformed keys byte for byte |
| Secret-dependent timing | Branches, divisions or data-indexed memory could introduce leakage | Proposed body has fixed arithmetic and fixed a/b indices; generated-code review pending |
| Compiler behaviour | Source-level control flow alone does not establish machine-code behaviour | Retain normal-build disassembly for both variants; review before performance interpretation |
| Memory behaviour | New buffers or changed indexing could introduce corruption | No array layout, allocation or indexing change is proposed; only scalar temporaries |
| Broader leakage | Power, EM, fault behaviour and complete constant-time guarantees are not established by these tests | Not assessed; do not generalise timing/correctness results to those properties |

The KEM verification, rejection-key derivation and conditional selection functions remain untouched. This does not itself prove equivalence: the candidate's preceding arithmetic must supply the same values. The validation specifically compares rejection outputs as well as successful exchanges.

I do not mark security as passed merely because the program is faster or its secrets match on valid exchanges. The evidence record keeps algebra/range review, sampled correctness, sanitizer results, generated-code review and statistical leakage assessment separate.

## Validation prepared for manual application

I added tests/test_fused_basemul.c and scripts/run_candidate_validation.py as support code. I extended the existing count helpers with explicit optional source/prediction arguments; their baseline defaults remain unchanged. I did not apply the arithmetic replacement.

After applying the supplied basemul body and committing source, tests, scripts and records, I run:

~~~bash
python3 -B scripts/run_candidate_validation.py --experiment EXP-001 --run RUN-0001
echo $?
~~~

This is a new run ID within EXP-001. It does not reuse or modify EXP-000/RUN-0001.

The runner performs, for each parameter set:

1. Baseline and candidate builds with normal flags and with -fsanitize=undefined -fno-sanitize-recover=all.
2. 3200 kernel checks per executable: 2048 sign corners, 128 zero cases and 1024 deterministic interior samples. A test-only int64_t modular oracle checks residues independently of Montgomery reduction. Output bounds are checked separately for baseline and candidate.
3. 100 reproducible KEM fixtures per executable. It retains keys, valid ciphertexts/secrets, corrupted/random-ciphertext decapsulation outputs, malformed-secret-key outputs and noncanonical-public-key encapsulation outputs as binary transcripts.
4. Exact byte comparison across all four transcripts. The public fixtures are reproducible test material, not deployment secrets.
5. The candidate's existing upstream functional suite, including 1000 cases each of successful exchange, replaced secret key and corrupted ciphertext.
6. A separate ten-exchange counter build, checked against the candidate predictions.
7. Retained normal-build basemul disassembly for later review.

The deterministic transcripts contain pk, sk, valid ct, encapsulated ss, decapsulated ss, corrupted-ct ss, random-ct ss, malformed-sk ss, noncanonical-pk ct and noncanonical-pk ss, in that order for each fixture. Each fixture occupies pkbytes + skbytes + 2*ctbytes + 6*ssbytes. Expected sizes are checked before byte comparison. The total archived transcript data for this protocol is about 7.3 MB.

UndefinedBehaviorSanitizer instruments executed operations and can report signed overflow and other supported errors. It does not prove all paths safe, check every narrowing conversion, or establish constant-time execution. The arithmetic argument remains necessary. See [GCC instrumentation documentation](https://gcc.gnu.org/onlinedocs/gcc/Instrumentation-Options.html).

A completed run requires all commands and per-parameter checks to pass, exact transcript agreement, predicted counts and a successful provenance recheck. Generated-code review still remains pending; a completed validation manifest is not a security certification. Failed or interrupted records remain under their original IDs. No performance measurements are collected by this command.

## Measurement and decision plan

Once candidate validation and generated-code review are accepted, I will prepare fresh alternating baseline/candidate timing blocks with the same compiler flags, public fixture rule, logical CPU, warm-up and input mode. The starting budget is five process repetitions of 1000 exchanges per parameter set. Instrumented and sanitized builds cannot supply timing results.

I will compare process-level medians within matched blocks and preserve the raw observations. Small uncertain effects require additional complete blocks and explicit uncertainty, not selective repetition or outlier removal. A correct candidate with a reproducible improvement may be retained; a regression, no detectable effect or inconclusive result remains a reportable outcome. Any failed arithmetic or compatibility gate stops performance collection.

The change adds two int32_t local accumulators and one int16_t temporary. It does not add heap allocation or change key/ciphertext storage. Compiler register/stack allocation remains to be inspected; source variable sizes are not a measured stack increase.

## Execution evidence and decision

- Proposal algebra and caller-bound review: recorded with the stated assumptions.
- Candidate implementation: pending manual application.
- Candidate tests/counts/sanitizer checks: not-run.
- Candidate assembly review: pending.
- Statistical timing-leakage assessment: not-run.
- Performance comparison: not-run.
- Retention decision: pending.

[Development support evidence](../evidence/ACT-0006/validation-support-smoke.json) records six builds of unchanged reference arithmetic, two public KEM fixtures per build and successful kernel-oracle/normal-versus-UBSan transcript checks. It also records rejection of an altered transcript and baseline counts presented as candidate predictions. These checks validate support behaviour; they do not test or validate the proposed candidate. The complete committed orchestration remains pending manual application and EXP-001/RUN-0001.
